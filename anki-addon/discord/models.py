"""
Domain Data Models for Discord Events, Card Payloads, and Sync Jobs.
Completely decoupled from Anki's internal database layout.
"""

from dataclasses import asdict, dataclass, field
from enum import Enum
import hashlib
import time
from typing import Any, Dict, List, Optional


class JobStatus(str, Enum):
    """Lifecycle states of a card synchronization job."""
    PENDING = "PENDING"
    PROCESSING = "PROCESSING"
    SUCCESS = "SUCCESS"
    FAILED = "FAILED"
    DUPLICATE = "DUPLICATE"
    RETRY = "RETRY"


@dataclass
class DiscordAttachment:
    """Discord file/image attachment."""
    id: str
    url: str
    filename: str
    content_type: str = ""
    size: int = 0


@dataclass
class DiscordUser:
    """Discord user metadata."""
    id: str
    name: str
    discriminator: str = ""

    def __str__(self) -> str:
        return f"{self.name}#{self.discriminator}" if self.discriminator else self.name


@dataclass
class DiscordChannel:
    """Discord channel metadata."""
    id: str
    name: str = ""
    guild_id: str = ""


@dataclass
class DiscordMessageEvent:
    """Represents an incoming message event received from Discord."""
    id: str
    content: str
    author: DiscordUser
    channel: DiscordChannel
    attachments: List[DiscordAttachment] = field(default_factory=list)
    timestamp: float = field(default_factory=time.time)
    # Image URLs found in embeds/attachments by the poller (webhooks post images as embeds)
    image_urls: List[str] = field(default_factory=list)
    is_webhook: bool = False


@dataclass
class CardPayload:
    """
    Standardized domain representation of a flashcard.
    Normalized from Discord messages, images, or external inputs before touching Anki.
    """
    front: str
    back: str = ""
    deck: str = "Default"
    tags: List[str] = field(default_factory=list)
    note_type: str = "Basic"
    extra: str = ""
    image_url: str = ""
    image_filename: str = ""
    source: str = "discord"
    message_id: str = ""
    author_id: str = ""
    author_name: str = ""
    channel_id: str = ""
    guild_id: str = ""
    timestamp: float = field(default_factory=time.time)
    raw_content: str = ""
    # Image pipeline: file waiting in user_files/staging, hash of the source bytes
    staging_path: str = ""
    image_hash: str = ""
    bytes_saved: int = 0

    def compute_hash(self) -> str:
        """Compute unique content fingerprint to detect identical cards."""
        if self.image_hash:
            # Image cards: same picture into the same deck is a duplicate, whatever
            # (signed, expiring) URL it came from.
            raw = f"image|{self.deck.strip().lower()}|{self.image_hash}"
            return hashlib.sha256(raw.encode("utf-8")).hexdigest()
        norm_front = " ".join(self.front.strip().split()).lower()
        norm_back = " ".join(self.back.strip().split()).lower()
        norm_deck = self.deck.strip().lower()
        norm_img = self.image_url.strip().lower() or self.image_filename.strip().lower()
        raw = f"{norm_front}|{norm_back}|{norm_deck}|{norm_img}"
        return hashlib.sha256(raw.encode("utf-8")).hexdigest()

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "CardPayload":
        return cls(
            front=data.get("front", ""),
            back=data.get("back", ""),
            deck=data.get("deck", "Default"),
            tags=list(data.get("tags", [])),
            note_type=data.get("note_type", "Basic"),
            extra=data.get("extra", ""),
            image_url=data.get("image_url", ""),
            image_filename=data.get("image_filename", ""),
            source=data.get("source", "discord"),
            message_id=data.get("message_id", ""),
            author_id=data.get("author_id", ""),
            author_name=data.get("author_name", ""),
            channel_id=data.get("channel_id", ""),
            guild_id=data.get("guild_id", ""),
            timestamp=data.get("timestamp", time.time()),
            raw_content=data.get("raw_content", ""),
            staging_path=data.get("staging_path", ""),
            image_hash=data.get("image_hash", ""),
            bytes_saved=int(data.get("bytes_saved", 0) or 0),
        )
