"""
Background Sync Worker.
Pulls jobs from JobQueue, applies deck routing, verifies anti-duplication, and invokes NoteAdapter.
"""

import threading
import time
from typing import Optional

try:
    from ..anki.notes import note_adapter
    from ..anki.operations import run_on_main_thread
    from ..core.config import config
    from ..core.event_bus import event_bus
    from ..core.exceptions import DuplicateCardError
    from ..core.logger import logger
    from ..routing.router import deck_router
    from .dedup import dedup_registry
    from .jobs import SyncJob
    from .queue import job_queue
except (ImportError, ValueError):
    from anki.notes import note_adapter
    from anki.operations import run_on_main_thread
    from core.config import config
    from core.event_bus import event_bus
    from core.exceptions import DuplicateCardError
    from core.logger import logger
    from routing.router import deck_router
    from sync.dedup import dedup_registry
    from sync.jobs import SyncJob
    from sync.queue import job_queue


class SyncWorker:
    """
    Background worker loop that processes card generation tasks safely.
    """
    def __init__(self) -> None:
        self._running = False
        self._thread: Optional[threading.Thread] = None
        self._stop_event = threading.Event()

    def start(self) -> None:
        if self._running:
            return

        self._running = True
        self._stop_event.clear()
        self._thread = threading.Thread(target=self._run_loop, name="ADT-SyncWorker", daemon=True)
        self._thread.start()
        logger.info("[SyncWorker] Background sync worker started.")

    def stop(self) -> None:
        if not self._running:
            return

        self._running = False
        self._stop_event.set()
        if self._thread and self._thread.is_alive():
            self._thread.join(timeout=2.0)
        logger.info("[SyncWorker] Background sync worker stopped.")

    def _run_loop(self) -> None:
        while not self._stop_event.is_set():
            try:
                job = job_queue.get_next()
                if job:
                    self._process_single_job(job)
                else:
                    self._stop_event.wait(timeout=1.0)
            except Exception as e:
                logger.error(f"[SyncWorker] Unexpected worker loop error: {e}", exc_info=True)
                self._stop_event.wait(timeout=2.0)

    def process_all_pending(self) -> int:
        """Synchronously process all pending jobs in queue."""
        count = 0
        while True:
            job = job_queue.get_next()
            if not job:
                break
            self._process_single_job(job)
            count += 1
        return count

    def _process_single_job(self, job: SyncJob) -> None:
        """Execute a single card creation job with deduplication and routing."""
        payload = job.payload
        content_hash = payload.compute_hash()

        # 1. Anti-Duplication Check
        if dedup_registry.is_duplicate(payload.message_id, content_hash):
            job_queue.mark_duplicate(job)
            event_bus.publish("sync:duplicate_detected", job)
            return

        # 2. Smart Deck Routing
        target_deck = deck_router.resolve_deck(payload)
        payload.deck = target_deck

        # 3. Create Note via Adapter
        def _execute_creation():
            try:
                note_id = note_adapter.create_note_from_payload(payload)

                dedup_registry.register_processed(payload.message_id, content_hash, note_id)
                job_queue.mark_success(job, note_id)

                # Update stats
                stats = config.get("stats", {})
                stats["cards_created"] = stats.get("cards_created", 0) + 1
                stats["last_sync_timestamp"] = time.time()
                config.set("stats", stats, save=True)

                event_bus.publish("sync:card_created", job, note_id)

            except DuplicateCardError:
                job_queue.mark_duplicate(job)
                event_bus.publish("sync:duplicate_detected", job)
            except Exception as err:
                error_msg = str(err)
                job_queue.mark_failed(job, error_msg)

                # Update stats
                stats = config.get("stats", {})
                stats["failed_jobs"] = stats.get("failed_jobs", 0) + 1
                config.set("stats", stats, save=True)

                event_bus.publish("sync:job_failed", job, error_msg)

        run_on_main_thread(_execute_creation)


# Global worker instance
sync_worker = SyncWorker()
