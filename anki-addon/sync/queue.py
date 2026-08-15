"""
Thread-safe Persistent Job Queue.
Manages pending card creation tasks, retries, and status tracking.
"""

from collections import deque
import json
import os
import threading
from typing import Any, Dict, List, Optional

try:
    from ..core.constants import QUEUE_DATA_FILENAME
    from ..core.logger import logger
    from ..discord.models import CardPayload, JobStatus
    from .jobs import SyncJob
except (ImportError, ValueError):
    from core.constants import QUEUE_DATA_FILENAME
    from core.logger import logger
    from discord.models import CardPayload, JobStatus
    from sync.jobs import SyncJob


class JobQueue:
    """
    Thread-safe FIFO queue with retry capabilities and status tracking.
    """
    def __init__(self, max_history: int = 200) -> None:
        self._pending: deque[SyncJob] = deque()
        self._history: List[SyncJob] = []
        self._max_history = max_history
        self._lock = threading.RLock()
        self._load()

    def _get_storage_path(self) -> str:
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        data_dir = os.path.join(base_dir, "data")
        os.makedirs(data_dir, exist_ok=True)
        return os.path.join(data_dir, QUEUE_DATA_FILENAME)

    def _load(self) -> None:
        path = self._get_storage_path()
        if not os.path.exists(path):
            return

        try:
            with open(path, "r", encoding="utf-8") as f:
                raw_list = json.load(f)
                for item in raw_list:
                    job = SyncJob.from_dict(item)
                    if job.status in (JobStatus.PENDING, JobStatus.PROCESSING, JobStatus.RETRY):
                        self._pending.append(job)
                    else:
                        self._history.append(job)
            logger.info(f"[JobQueue] Restored {len(self._pending)} pending jobs and {len(self._history)} historical jobs.")
        except Exception as e:
            logger.error(f"[JobQueue] Failed restoring queue from disk: {e}")

    def _save(self) -> None:
        path = self._get_storage_path()
        try:
            with self._lock:
                all_jobs = list(self._pending) + self._history[-self._max_history:]
                serialized = [j.to_dict() for j in all_jobs]

            with open(path, "w", encoding="utf-8") as f:
                json.dump(serialized, f, indent=2)
        except Exception as e:
            logger.error(f"[JobQueue] Failed saving queue to disk: {e}")

    def enqueue(self, payload: CardPayload) -> SyncJob:
        """Add a new card payload to the processing queue."""
        with self._lock:
            job = SyncJob(payload=payload, status=JobStatus.PENDING)
            self._pending.append(job)
            self._save()
            logger.info(f"[JobQueue] Enqueued Job '{job.id}' for deck '{payload.deck}'")
            return job

    def get_next(self) -> Optional[SyncJob]:
        """Fetch next pending job for processing."""
        with self._lock:
            if not self._pending:
                return None
            job = self._pending.popleft()
            job.status = JobStatus.PROCESSING
            self._save()
            return job

    def mark_success(self, job: SyncJob, note_id: int) -> None:
        """Mark job as successfully executed and record note ID."""
        with self._lock:
            job.status = JobStatus.SUCCESS
            job.note_id = note_id
            self._history.append(job)
            if len(self._history) > self._max_history:
                self._history.pop(0)
            self._save()
            logger.info(f"[JobQueue] Job '{job.id}' succeeded with Note ID {note_id}")

    def mark_failed(self, job: SyncJob, error_msg: str) -> None:
        """Mark job as failed, or re-enqueue for retry if under retry limit."""
        with self._lock:
            job.error = error_msg
            job.retry_count += 1

            if job.retry_count < job.max_retries:
                job.status = JobStatus.RETRY
                self._pending.append(job)
                logger.warning(f"[JobQueue] Job '{job.id}' failed (Attempt {job.retry_count}/{job.max_retries}). Re-enqueued.")
            else:
                job.status = JobStatus.FAILED
                self._history.append(job)
                if len(self._history) > self._max_history:
                    self._history.pop(0)
                logger.error(f"[JobQueue] Job '{job.id}' permanently failed: {error_msg}")

            self._save()

    def mark_duplicate(self, job: SyncJob) -> None:
        """Mark job as duplicate."""
        with self._lock:
            job.status = JobStatus.DUPLICATE
            job.error = "Duplicate card ignored."
            self._history.append(job)
            self._save()

    def get_pending_count(self) -> int:
        with self._lock:
            return len(self._pending)

    def get_all_jobs(self) -> List[SyncJob]:
        """Return combined list of pending and completed jobs."""
        with self._lock:
            return list(self._pending) + list(self._history)

    def get_stats(self) -> Dict[str, int]:
        with self._lock:
            all_j = self.get_all_jobs()
            return {
                "pending": sum(1 for j in all_j if j.status in (JobStatus.PENDING, JobStatus.RETRY)),
                "processing": sum(1 for j in all_j if j.status == JobStatus.PROCESSING),
                "success": sum(1 for j in all_j if j.status == JobStatus.SUCCESS),
                "failed": sum(1 for j in all_j if j.status == JobStatus.FAILED),
                "duplicate": sum(1 for j in all_j if j.status == JobStatus.DUPLICATE),
            }

    def clear(self) -> None:
        with self._lock:
            self._pending.clear()
            self._history.clear()
            self._save()


# Global queue instance
job_queue = JobQueue()
