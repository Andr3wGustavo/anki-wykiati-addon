"""
Media Collection Manager for Anki Discord Toolkit.
Handles image downloading, hashing, duplication check, and saving to Anki media collection.
"""

import hashlib
from dataclasses import dataclass
import ipaddress
import mimetypes
import os
import re
import socket
import urllib.error
import urllib.parse
import urllib.request
from typing import Optional, Tuple

try:
    from ..core.config import config
    from ..core.logger import logger
    from ..core.paths import user_files_dir
    from ..core.image_urls import download_candidates
except (ImportError, ValueError):
    from core.config import config
    from core.logger import logger
    from core.paths import user_files_dir
    from core.image_urls import download_candidates

try:
    from aqt import mw
    ANKI_AVAILABLE = True
except ImportError:
    mw = None
    ANKI_AVAILABLE = False

# Qt Image Handling
try:
    from aqt.qt import QBuffer, QByteArray, QImage, QImageWriter, QIODevice, Qt
    QT_GUI_AVAILABLE = True
except ImportError:
    try:
        from PyQt6.QtCore import QBuffer, QByteArray, QIODevice, Qt
        from PyQt6.QtGui import QImage, QImageWriter
        QT_GUI_AVAILABLE = True
    except ImportError:
        try:
            from PyQt5.QtCore import QBuffer, QByteArray, QIODevice, Qt
            from PyQt5.QtGui import QImage, QImageWriter
            QT_GUI_AVAILABLE = True
        except ImportError:
            QT_GUI_AVAILABLE = False


MAX_IMAGE_DOWNLOAD_BYTES = 10 * 1024 * 1024  # 10 MB


@dataclass
class StagedImage:
    """Result of downloading + optimizing an image into the staging area."""
    ok: bool
    filename: str = ""
    image_hash: str = ""
    staging_path: str = ""
    bytes_saved: int = 0
    source_url: str = ""
    error: str = ""


class UnsafeURLError(ValueError):
    """Raised when a URL points at a non-public (loopback / private / link-local) address."""


def _assert_public_url(url: str) -> None:
    """
    SSRF guard: refuse URLs whose host resolves to loopback, private, link-local,
    multicast or reserved addresses. Image URLs come from untrusted input.
    """
    parsed = urllib.parse.urlparse(url)
    if parsed.scheme not in ("http", "https") or not parsed.hostname:
        raise UnsafeURLError(f"Unsupported URL: {url}")
    try:
        infos = socket.getaddrinfo(parsed.hostname, parsed.port or (443 if parsed.scheme == "https" else 80))
    except socket.gaierror as e:
        raise UnsafeURLError(f"Could not resolve host '{parsed.hostname}': {e}")
    for info in infos:
        ip = ipaddress.ip_address(info[4][0].split("%")[0])
        if (
            ip.is_private
            or ip.is_loopback
            or ip.is_link_local
            or ip.is_multicast
            or ip.is_reserved
            or ip.is_unspecified
        ):
            raise UnsafeURLError(f"Refusing to fetch non-public address {ip} for host '{parsed.hostname}'")


class _SafeRedirectHandler(urllib.request.HTTPRedirectHandler):
    """Re-validates every redirect target so a public URL cannot bounce to an internal one."""

    def redirect_request(self, req, fp, code, msg, headers, newurl):  # type: ignore[override]
        _assert_public_url(newurl)
        return super().redirect_request(req, fp, code, msg, headers, newurl)


_SAFE_OPENER = urllib.request.build_opener(_SafeRedirectHandler)


class MediaManager:
    """
    Manages downloading, optimizing (WebP/JPEG conversion & resizing), and persisting external media files.
    """
    def __init__(self) -> None:
        self._fallback_media_dir: Optional[str] = None

    def _get_fallback_media_dir(self) -> str:
        if self._fallback_media_dir is None:
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            self._fallback_media_dir = os.path.join(base_dir, "data", "media")
            os.makedirs(self._fallback_media_dir, exist_ok=True)
        return self._fallback_media_dir

    def optimize_image_data(self, raw_data: bytes, original_ext: str) -> Tuple[bytes, str, int]:
        """
        In-memory image optimization pipeline:
        1. Downscales 4K/huge images to max bounding dimension (default 1920px).
        2. Converts heavy PNG/JPEG to lightweight WebP (or optimized JPEG) at 85% quality.
        3. Preserves animated GIFs and vector SVGs.
        Returns: (optimized_data: bytes, final_extension: str, bytes_saved: int)
        """
        if not config.get("discord.optimize_images", True):
            return raw_data, original_ext, 0

        clean_ext = original_ext.lower().lstrip(".")
        if clean_ext in ("gif", "svg"):
            return raw_data, clean_ext, 0

        if not QT_GUI_AVAILABLE:
            return raw_data, clean_ext, 0

        try:
            image = QImage.fromData(raw_data)
            if image.isNull():
                return raw_data, clean_ext, 0

            orig_w, orig_h = image.width(), image.height()
            max_dim = int(config.get("discord.max_image_dimension", 1920))

            # Proportional downscaling
            if orig_w > max_dim or orig_h > max_dim:
                aspect_ratio_mode = getattr(Qt.AspectRatioMode, "KeepAspectRatio", 1) if hasattr(Qt, "AspectRatioMode") else 1
                transform_mode = getattr(Qt.TransformationMode, "SmoothTransformation", 1) if hasattr(Qt, "TransformationMode") else 1
                image = image.scaled(max_dim, max_dim, aspect_ratio_mode, transform_mode)
                logger.debug(f"[MediaManager] Rescaled image from {orig_w}x{orig_h} to {image.width()}x{image.height()}")

            # Determine target format
            convert_webp = config.get("discord.convert_to_webp", True)
            supported = []
            try:
                supported = [bytes(f).decode("utf-8").lower() for f in QImageWriter.supportedImageFormats()]
            except Exception:
                pass

            target_format = "JPEG"
            target_ext = "jpg"

            if convert_webp and ("webp" in supported):
                target_format = "WEBP"
                target_ext = "webp"
            elif image.hasAlphaChannel() and clean_ext == "png":
                target_format = "PNG"
                target_ext = "png"

            quality = int(config.get("discord.image_quality", 85))

            # Encode into memory buffer
            byte_array = QByteArray()
            buffer = QBuffer(byte_array)
            write_mode = getattr(QIODevice.OpenModeFlag, "WriteOnly", 2) if hasattr(QIODevice, "OpenModeFlag") else getattr(QIODevice, "WriteOnly", 2)
            buffer.open(write_mode)

            writer = QImageWriter(buffer, target_format.encode("utf-8"))
            writer.setQuality(quality)

            if writer.write(image):
                optimized_data = bytes(byte_array.data())
                buffer.close()

                # If optimized is smaller or converted to WebP, keep it
                if len(optimized_data) < len(raw_data) or target_ext == "webp":
                    bytes_saved = max(0, len(raw_data) - len(optimized_data))
                    saved_kb = bytes_saved / 1024.0
                    logger.info(
                        f"[MediaManager] Optimized image ({len(raw_data)/1024:.1f} KB -> {len(optimized_data)/1024:.1f} KB, "
                        f"saved {saved_kb:.1f} KB, format: {target_ext})"
                    )
                    return optimized_data, target_ext, bytes_saved

            buffer.close()
        except Exception as opt_err:
            logger.warning(f"[MediaManager] Image optimization skipped due to error: {opt_err}")

        return raw_data, clean_ext, 0

    def _download(self, image_url: str) -> Tuple[bytes, str]:
        """Fetch one URL with SSRF/size/content-type guards. Raises ValueError with a readable reason."""
        if not image_url or not image_url.startswith(("http://", "https://")):
            raise ValueError("Invalid image URL")
        _assert_public_url(image_url)
        req = urllib.request.Request(
            image_url,
            headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AnkiWykiatiToolkit"},
        )
        with _SAFE_OPENER.open(req, timeout=15) as response:
            content_type = response.headers.get("Content-Type", "")
            main_type = content_type.split(";")[0].strip().lower()
            if not main_type.startswith("image/"):
                raise ValueError(f"Refused non-image content type '{main_type or 'unknown'}'")
            declared = response.headers.get("Content-Length")
            if declared and declared.isdigit() and int(declared) > MAX_IMAGE_DOWNLOAD_BYTES:
                raise ValueError("Image exceeds maximum download size")
            raw_data = response.read(MAX_IMAGE_DOWNLOAD_BYTES + 1)
        if len(raw_data) > MAX_IMAGE_DOWNLOAD_BYTES:
            raise ValueError("Image exceeds maximum download size")
        if not raw_data:
            raise ValueError("Empty image data received")
        return raw_data, content_type

    def stage_image(self, image_url: str) -> "StagedImage":
        """
        Background-thread safe: download (trying higher-quality candidates first),
        optimize, and write the result to `user_files/staging`. Nothing touches the
        Anki collection here; `commit_staged_image` does that on the main thread.
        """
        last_error = "No download candidates"
        for candidate in download_candidates(image_url):
            try:
                raw_data, content_type = self._download(candidate)
            except UnsafeURLError as e:
                return StagedImage(False, error=str(e))
            except Exception as e:
                last_error = str(e)
                logger.debug(f"[MediaManager] Candidate failed ({candidate}): {e}")
                continue

            # Hash of the source bytes: identical images dedup regardless of URL or settings
            img_hash = hashlib.sha256(raw_data).hexdigest()
            orig_ext = self._extract_extension(candidate, content_type)
            data, final_ext, bytes_saved = self.optimize_image_data(raw_data, orig_ext)
            filename = f"discord_{img_hash[:16]}.{final_ext}"
            staging_path = os.path.join(user_files_dir("staging"), filename)
            with open(staging_path, "wb") as f:
                f.write(data)
            logger.info(f"[MediaManager] Staged '{filename}' ({len(data) / 1024:.1f} KB) from {candidate}")
            return StagedImage(True, filename=filename, image_hash=img_hash,
                               staging_path=staging_path, bytes_saved=bytes_saved, source_url=candidate)

        logger.error(f"[MediaManager] Failed to download image {image_url}: {last_error}")
        return StagedImage(False, error=last_error)

    def commit_staged_image(self, filename: str, staging_path: str) -> str:
        """
        MAIN THREAD ONLY. Move a staged file into the collection's media folder and
        return the final media filename (Anki may rename on conflicts).
        """
        if not staging_path or not os.path.exists(staging_path):
            raise FileNotFoundError(f"Staged image missing: {staging_path}")
        with open(staging_path, "rb") as f:
            data = f.read()

        final_name = filename
        if ANKI_AVAILABLE and mw is not None and getattr(mw, "col", None) is not None:
            final_name = mw.col.media.write_data(filename, data) or filename
        else:
            with open(os.path.join(self._get_fallback_media_dir(), filename), "wb") as f:
                f.write(data)
        try:
            os.remove(staging_path)
        except OSError:
            pass
        return final_name

    def _extract_extension(self, url: str, content_type: str) -> str:
        """Extract clean file extension from Content-Type header or URL."""
        if content_type:
            ct = content_type.split(";")[0].strip().lower()
            ext = mimetypes.guess_extension(ct)
            if ext:
                clean_ext = ext.lstrip(".").lower()
                if clean_ext == "jpeg":
                    return "jpg"
                return clean_ext

        # Fallback to URL path extension
        parsed = urllib.parse.urlparse(url)
        match = re.search(r"\.(png|jpg|jpeg|webp|gif|svg)$", parsed.path, re.IGNORECASE)
        if match:
            ext = match.group(1).lower()
            return "jpg" if ext == "jpeg" else ext

        return "png"


# Global media manager singleton
media_manager = MediaManager()

