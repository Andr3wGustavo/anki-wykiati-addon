"""
Image discovery in raw Discord message objects.

Webhook automations (e.g. Pinterest → Discord) usually post images as *embeds*,
not attachments, so both are inspected.
"""

import re
from typing import Any, Dict, List

IMAGE_EXTENSIONS = (".png", ".jpg", ".jpeg", ".webp", ".gif", ".bmp")
IMAGE_URL_REGEX = re.compile(r"https?://\S+?\.(?:png|jpe?g|webp|gif)(?:\?\S*)?", re.IGNORECASE)
_PINIMG_SIZE_RE = re.compile(r"^(https?://i\.pinimg\.com/)(?:\d+x\d*|originals)(/.+)$", re.IGNORECASE)


def _looks_like_image(url: str, content_type: str = "") -> bool:
    if content_type:
        return content_type.lower().startswith("image/")
    path = url.split("?", 1)[0].lower()
    return path.endswith(IMAGE_EXTENSIONS)


def extract_image_urls(message: Dict[str, Any]) -> List[str]:
    """
    Return image URLs from a Discord message, in display order and de-duplicated:
    attachments → embed.image → embed.thumbnail (only when the embed has no image)
    → image links in the text.
    """
    urls: List[str] = []

    def add(url: Any) -> None:
        if isinstance(url, str) and url.startswith(("http://", "https://")) and url not in urls:
            urls.append(url)

    for att in message.get("attachments") or []:
        url = att.get("url") or att.get("proxy_url")
        if url and _looks_like_image(url, att.get("content_type", "")):
            add(url)

    for embed in message.get("embeds") or []:
        image = embed.get("image") or {}
        thumb = embed.get("thumbnail") or {}
        if image.get("url"):
            add(image["url"])
        elif thumb.get("url"):
            # Link previews of an image (type "image") and many rich embeds only carry a thumbnail
            add(thumb["url"])
        elif embed.get("type") == "image" and embed.get("url"):
            add(embed["url"])

    for match in IMAGE_URL_REGEX.findall(message.get("content") or ""):
        add(match)

    return urls


def download_candidates(url: str) -> List[str]:
    """
    URLs to try, best quality first. Pinterest embeds point at resized copies
    (e.g. /236x/ or /736x/); the full-size file lives under /originals/.
    """
    match = _PINIMG_SIZE_RE.match(url)
    if not match:
        return [url]
    prefix, rest = match.groups()
    candidates = [f"{prefix}originals{rest}", f"{prefix}736x{rest}", url]
    seen: List[str] = []
    for c in candidates:
        if c not in seen:
            seen.append(c)
    return seen
