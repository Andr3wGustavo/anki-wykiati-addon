"""
Background Sync Worker.
Pulls jobs from JobQueue, applies deck routing, verifies anti-duplication, and invokes NoteAdapter.
"""

import os
import threading
import time
from typing import Optional

try:
    from ..anki.media import media_manager
    from ..anki.notes import note_adapter
    from ..discord.models import JobStatus
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
    from anki.media import media_manager
    from anki.notes import note_adapter
    from discord.models import JobStatus
    from anki.operations import run_on_main_thread
    from core.config import config
    from core.event_bus import event_bus
    from core.exceptions import DuplicateCardError
    from core.logger import logger
    from routing.router import deck_router
    from sync.dedup import dedup_registry
    from sync.jobs import SyncJob
    from sync.queue import job_queue


try:
    from aqt import mw
    from aqt.qt import QTimer
    ANKI_AVAILABLE = True
except ImportError:
    mw = None
    QTimer = None
    ANKI_AVAILABLE = False


class SyncWorker:
    """
    Background worker loop that processes card generation tasks safely.
    """
    def __init__(self) -> None:
        self._running = False
        self._thread: Optional[threading.Thread] = None
        self._stop_event = threading.Event()
        self._refresh_pending = False

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
        """
        Resolve the deck here (pure logic), then run dedup + media commit + note
        creation as ONE unit on Anki's main thread: the collection is not thread-safe,
        and doing the duplicate check in the same place as the registration removes
        the race where two identical jobs both passed the check.
        """
        payload = job.payload
        payload.deck = deck_router.resolve_deck(payload)
        run_on_main_thread(self._execute_on_main, job)

    def _discard_staging(self, payload) -> None:
        if payload.staging_path and os.path.exists(payload.staging_path):
            try:
                os.remove(payload.staging_path)
            except OSError:
                pass

    def _execute_on_main(self, job: SyncJob) -> None:
        payload = job.payload
        content_hash = payload.compute_hash()

        try:
            # 1. Anti-duplication
            if dedup_registry.is_duplicate(payload.message_id, content_hash):
                self._discard_staging(payload)
                dedup_registry.mark_message_seen(payload.message_id)
                job_queue.mark_duplicate(job)
                event_bus.publish("sync:duplicate_detected", job)
                return

            # 2. Move staged image into the collection media folder
            if payload.staging_path:
                final_name = media_manager.commit_staged_image(payload.image_filename, payload.staging_path)
                if final_name != payload.image_filename:
                    old_src = f'src="{payload.image_filename}"'
                    new_src = f'src="{final_name}"'
                    payload.front = payload.front.replace(old_src, new_src)
                    payload.back = payload.back.replace(old_src, new_src)
                    payload.image_filename = final_name
                payload.staging_path = ""

            # 3. Create the note
            note_id = note_adapter.create_note_from_payload(payload)

            dedup_registry.register_processed(payload.message_id, content_hash, note_id)
            job_queue.mark_success(job, note_id)

            stats = dict(config.get("stats", {}))
            stats["cards_created"] = stats.get("cards_created", 0) + 1
            if payload.source == "discord_image":
                stats["images_ingested"] = stats.get("images_ingested", 0) + 1
                stats["bytes_saved"] = stats.get("bytes_saved", 0) + int(payload.bytes_saved or 0)
            stats["last_sync_timestamp"] = time.time()
            config.set("stats", stats, save=False)
            self._schedule_persist_and_refresh()

            event_bus.publish("sync:card_created", job, note_id)

        except DuplicateCardError:
            self._discard_staging(payload)
            job_queue.mark_duplicate(job)
            event_bus.publish("sync:duplicate_detected", job)
        except Exception as err:
            error_msg = str(err)
            logger.error(f"[SyncWorker] Job '{job.id}' failed: {error_msg}")
            job_queue.mark_failed(job, error_msg)
            if job.status == JobStatus.FAILED:
                self._discard_staging(payload)
                stats = dict(config.get("stats", {}))
                stats["failed_jobs"] = stats.get("failed_jobs", 0) + 1
                config.set("stats", stats, save=False)
                self._schedule_persist_and_refresh()
            event_bus.publish("sync:job_failed", job, error_msg)

    def _schedule_persist_and_refresh(self) -> None:
        """Coalesce bursts (e.g. importing 100 images): one config save + one UI refresh."""
        if self._refresh_pending:
            return
        self._refresh_pending = True

        def _flush() -> None:
            self._refresh_pending = False
            try:
                config.save_config()
            except Exception as e:
                logger.debug(f"[SyncWorker] Stats save skipped: {e}")
            if not ANKI_AVAILABLE or mw is None or getattr(mw, "col", None) is None:
                return
            try:
                # Update counts without interrupting a review session
                if mw.state == "deckBrowser":
                    mw.deckBrowser.refresh()
                elif mw.state == "overview":
                    mw.overview.refresh()
            except Exception as e:
                logger.debug(f"[SyncWorker] UI refresh skipped: {e}")

        if ANKI_AVAILABLE and QTimer is not None and mw is not None:
            QTimer.singleShot(1500, _flush)
        else:
            _flush()


# Global worker instance
sync_worker = SyncWorker()
