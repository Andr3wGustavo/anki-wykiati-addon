"""
Anti-Duplication Registry.
Prevents duplicate card creation by fingerprinting Discord message IDs and content hashes.

Stored in `user_files/` so it survives add-on updates. Entries are kept in insertion
order and trimmed oldest-first.
"""

import json
import os
import threading
import time
from typing import Any, Dict

try:
    from ..core.constants import PROCESSED_MESSAGES_FILENAME
    from ..core.logger import logger
    from ..core.paths import user_file
except (ImportError, ValueError):
    from core.constants import PROCESSED_MESSAGES_FILENAME
    from core.logger import logger
    from core.paths import user_file

MAX_ENTRIES = 20000


class AntiDuplicationRegistry:
    """
    Maintains a persistent record of processed messages and content hashes to ensure idempotency.
    """
    def __init__(self) -> None:
        # dicts preserve insertion order → trimming keeps the newest entries
        self._processed_message_ids: Dict[str, float] = {}
        self._processed_content_hashes: Dict[str, Dict[str, Any]] = {}
        self._lock = threading.RLock()
        self._load()

    def _get_storage_path(self) -> str:
        return user_file(PROCESSED_MESSAGES_FILENAME)

    def _load(self) -> None:
        path = self._get_storage_path()
        if not os.path.exists(path):
            return
        try:
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
            ids = data.get("message_ids", {})
            if isinstance(ids, list):  # legacy format
                ids = {str(i): 0.0 for i in ids}
            self._processed_message_ids = {str(k): float(v or 0) for k, v in ids.items()}
            self._processed_content_hashes = dict(data.get("content_hashes", {}))
            logger.info(
                f"[AntiDuplication] Loaded {len(self._processed_message_ids)} message IDs and "
                f"{len(self._processed_content_hashes)} hashes."
            )
        except Exception as e:
            logger.error(f"[AntiDuplication] Failed loading registry: {e}")

    @staticmethod
    def _trim(d: Dict[str, Any]) -> Dict[str, Any]:
        if len(d) <= MAX_ENTRIES:
            return d
        return dict(list(d.items())[-MAX_ENTRIES:])

    def _save(self) -> None:
        path = self._get_storage_path()
        try:
            with self._lock:
                self._processed_message_ids = self._trim(self._processed_message_ids)
                self._processed_content_hashes = self._trim(self._processed_content_hashes)
                data = {
                    "message_ids": dict(self._processed_message_ids),
                    "content_hashes": dict(self._processed_content_hashes),
                }
            tmp = path + ".tmp"
            with open(tmp, "w", encoding="utf-8") as f:
                json.dump(data, f)
            os.replace(tmp, path)
        except Exception as e:
            logger.error(f"[AntiDuplication] Failed saving registry: {e}")

    def is_message_processed(self, message_id: str) -> bool:
        with self._lock:
            return bool(message_id) and (
                message_id in self._processed_message_ids
                or f"{message_id}#0" in self._processed_message_ids
            )

    def is_duplicate(self, message_id: str, content_hash: str) -> bool:
        with self._lock:
            if message_id and message_id in self._processed_message_ids:
                logger.info(f"[AntiDuplication] Duplicate message ID detected: '{message_id}'")
                return True

            if content_hash and content_hash in self._processed_content_hashes:
                logger.info(f"[AntiDuplication] Duplicate content hash detected: '{content_hash[:12]}'")
                return True

            return False

    def register_processed(self, message_id: str, content_hash: str, note_id: int) -> None:
        with self._lock:
            now = time.time()
            if message_id:
                self._processed_message_ids[message_id] = now

            if content_hash:
                self._processed_content_hashes[content_hash] = {"note_id": note_id, "timestamp": now}

            self._save()
            logger.debug(f"[AntiDuplication] Registered card Note ID {note_id} (hash {content_hash[:8]})")

    def mark_message_seen(self, message_id: str) -> None:
        """Record a message as handled without creating a note (e.g. duplicate image)."""
        if not message_id:
            return
        with self._lock:
            self._processed_message_ids[message_id] = time.time()
            self._save()

    def clear(self) -> None:
        with self._lock:
            self._processed_message_ids.clear()
            self._processed_content_hashes.clear()
            self._save()


# Global registry instance
dedup_registry = AntiDuplicationRegistry()
