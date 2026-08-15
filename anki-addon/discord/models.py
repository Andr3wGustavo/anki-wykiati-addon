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
    timestamp: float = field(default_factory=time.time)


@dataclass
class CardPayload:
    """
    Standardized domain representation of a flashcard.
    Normalized from Discord messages or external inputs before touching Anki.
    """
    front: str
    back: str
    deck: str = "Default"
    tags: List[str] = field(default_factory=list)
    note_type: str = "Basic"
    extra: str = ""
    source: str = "discord"
    message_id: str = ""
    author_id: str = ""
    author_name: str = ""
    channel_id: str = ""
    guild_id: str = ""
    timestamp: float = field(default_factory=time.time)
    raw_content: str = ""

    def compute_hash(self) -> str:
        """Compute unique content fingerprint to detect identical cards."""
        norm_front = " ".join(self.front.strip().split()).lower()
        norm_back = " ".join(self.back.strip().split()).lower()
        norm_deck = self.deck.strip().lower()
        norm_type = self.note_type.strip().lower()
        raw = f"{norm_front}|{norm_back}|{norm_deck}|{norm_type}"
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
            source=data.get("source", "discord"),
            message_id=data.get("message_id", ""),
            author_id=data.get("author_id", ""),
            author_name=data.get("author_name", ""),
            channel_id=data.get("channel_id", ""),
            guild_id=data.get("guild_id", ""),
            timestamp=data.get("timestamp", time.time()),
            raw_content=data.get("raw_content", ""),
        )
