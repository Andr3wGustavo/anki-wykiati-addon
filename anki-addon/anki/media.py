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
    from ..core.logger import logger
except (ImportError, ValueError):
    from core.logger import logger

try:
    from aqt import mw
    ANKI_AVAILABLE = True
except ImportError:
    mw = None
    ANKI_AVAILABLE = False


class MediaManager:
    """
    Manages downloading and persisting external media files to Anki's collection media database.
    """
    def __init__(self) -> None:
        self._fallback_media_dir: Optional[str] = None

    def _get_fallback_media_dir(self) -> str:
        if self._fallback_media_dir is None:
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            self._fallback_media_dir = os.path.join(base_dir, "data", "media")
            os.makedirs(self._fallback_media_dir, exist_ok=True)
        return self._fallback_media_dir

    def download_and_save_image(
        self,
        image_url: str,
        custom_filename: Optional[str] = None,
    ) -> Tuple[bool, str, str]:
        """
        Download an image from a URL, compute its hash, save it to Anki media storage.
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
                data = response.read()

            if not data:
                return False, "", "Empty image data received"

            # Compute SHA-256 hash of the binary image
            img_hash = hashlib.sha256(data).hexdigest()

            # Determine extension
            ext = self._extract_extension(image_url, response.headers.get("Content-Type", ""))
            clean_name = f"discord_{img_hash[:12]}.{ext}"

            # Save to Anki Collection media
            if ANKI_AVAILABLE and mw is not None and mw.col is not None and hasattr(mw.col, "media"):
                try:
                    # Anki's official media write_data API
                    mw.col.media.write_data(clean_name, data)
                    logger.info(f"[MediaManager] Saved image '{clean_name}' directly into Anki Media collection.")
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
