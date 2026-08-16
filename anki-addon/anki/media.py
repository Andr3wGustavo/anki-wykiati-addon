"""
Media Collection Manager for Anki Discord Toolkit.
Handles image downloading, hashing, duplication check, and saving to Anki media collection.
"""

import hashlib
import mimetypes
import os
import re
import urllib.error
import urllib.parse
import urllib.request
from typing import Optional, Tuple

try:
    from ..core.config import config
    from ..core.logger import logger
except (ImportError, ValueError):
    from core.config import config
    from core.logger import logger

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
                    # Update metrics
                    config.set("stats.bytes_saved", config.get("stats.bytes_saved", 0) + bytes_saved, save=False)
                    config.set("stats.images_ingested", config.get("stats.images_ingested", 0) + 1, save=False)
                    return optimized_data, target_ext, bytes_saved

            buffer.close()
        except Exception as opt_err:
            logger.warning(f"[MediaManager] Image optimization skipped due to error: {opt_err}")

        return raw_data, clean_ext, 0

    def download_and_save_image(
        self,
        image_url: str,
        custom_filename: Optional[str] = None,
    ) -> Tuple[bool, str, str]:
        """
        Download an image from a URL, optimize it in memory, compute its hash, save it to Anki media storage.
        Returns: (success: bool, media_filename: str, image_hash: str)
        """
        if not image_url or not image_url.startswith(("http://", "https://")):
            return False, "", "Invalid image URL"

        try:
            req = urllib.request.Request(
                image_url,
                headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AnkiDiscordToolkit/1.0"},
            )
            with urllib.request.urlopen(req, timeout=12) as response:
                raw_data = response.read()
                content_type = response.headers.get("Content-Type", "")

            if not raw_data:
                return False, "", "Empty image data received"

            # Determine initial extension
            orig_ext = self._extract_extension(image_url, content_type)

            # In-memory image optimization & downscaling
            data, final_ext, _ = self.optimize_image_data(raw_data, orig_ext)

            # Compute SHA-256 hash of the optimized binary image
            img_hash = hashlib.sha256(data).hexdigest()
            clean_name = f"discord_{img_hash[:12]}.{final_ext}"

            # Save to Anki Collection media
            if ANKI_AVAILABLE and mw is not None and mw.col is not None and hasattr(mw.col, "media"):
                try:
                    # Anki's official media write_data API
                    mw.col.media.write_data(clean_name, data)
                    logger.info(f"[MediaManager] Saved optimized image '{clean_name}' directly into Anki Media collection.")
                except Exception as media_err:
                    logger.warning(f"[MediaManager] write_data failed, trying add_file: {media_err}")
                    temp_path = os.path.join(self._get_fallback_media_dir(), clean_name)
                    with open(temp_path, "wb") as f:
                        f.write(data)
                    if hasattr(mw.col.media, "add_file"):
                        mw.col.media.add_file(temp_path)
            else:
                # Standalone fallback storage for headless test runs
                temp_path = os.path.join(self._get_fallback_media_dir(), clean_name)
                with open(temp_path, "wb") as f:
                    f.write(data)
                logger.info(f"[MediaManager] Headless mode: Saved image to '{temp_path}'")

            return True, clean_name, img_hash

        except urllib.error.URLError as url_err:
            logger.error(f"[MediaManager] Failed to download image from {image_url}: {url_err}")
            return False, "", str(url_err)
        except Exception as e:
            logger.error(f"[MediaManager] Unexpected error processing image: {e}", exc_info=True)
            return False, "", str(e)

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

