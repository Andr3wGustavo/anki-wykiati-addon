"""
Sync Job Data Model and Lifecycle States.
Tracks execution progress, retry attempts, errors, and associated note IDs.
"""

from dataclasses import asdict, dataclass, field
import time
from typing import Any, Dict, Optional
import uuid

try:
    from ..discord.models import CardPayload, JobStatus
except (ImportError, ValueError):
    from discord.models import CardPayload, JobStatus


@dataclass
class SyncJob:
    """Represents a discrete card creation job in the background queue."""
    payload: CardPayload
    id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    timestamp: float = field(default_factory=time.time)
    status: JobStatus = JobStatus.PENDING
    error: str = ""
    retry_count: int = 0
    max_retries: int = 3
    note_id: Optional[int] = None

    def to_dict(self) -> Dict[str, Any]:
        data = asdict(self)
        data["status"] = self.status.value
        return data

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "SyncJob":
        payload_dict = data.get("payload", {})
        payload = CardPayload.from_dict(payload_dict) if isinstance(payload_dict, dict) else payload_dict
        return cls(
            id=data.get("id", str(uuid.uuid4())[:8]),
            payload=payload,
            timestamp=data.get("timestamp", time.time()),
            status=JobStatus(data.get("status", JobStatus.PENDING.value)),
            error=data.get("error", ""),
            retry_count=data.get("retry_count", 0),
            max_retries=data.get("max_retries", 3),
            note_id=data.get("note_id"),
        )
