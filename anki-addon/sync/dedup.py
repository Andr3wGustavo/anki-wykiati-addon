"""
Anti-Duplication Registry.
Prevents duplicate card creation by fingerprinting Discord message IDs and content hashes.
"""

import json
import os
import threading
import time
from typing import Any, Dict, Optional, Set

try:
    from ..core.constants import PROCESSED_MESSAGES_FILENAME
    from ..core.logger import logger
except (ImportError, ValueError):
    from core.constants import PROCESSED_MESSAGES_FILENAME
    from core.logger import logger


class AntiDuplicationRegistry:
    """
    Maintains a persistent record of processed messages and content hashes to ensure idempotency.
    """
    def __init__(self) -> None:
        self._processed_message_ids: Set[str] = set()
        self._processed_content_hashes: Dict[str, Dict[str, Any]] = {}
        self._lock = threading.RLock()
        self._load()

    def _get_storage_path(self) -> str:
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        data_dir = os.path.join(base_dir, "data")
        os.makedirs(data_dir, exist_ok=True)
        return os.path.join(data_dir, PROCESSED_MESSAGES_FILENAME)

    def _load(self) -> None:
        path = self._get_storage_path()
        if not os.path.exists(path):
            return

        try:
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
                self._processed_message_ids = set(data.get("message_ids", []))
                self._processed_content_hashes = data.get("content_hashes", {})
            logger.info(f"[AntiDuplication] Loaded {len(self._processed_message_ids)} message IDs and {len(self._processed_content_hashes)} hashes.")
        except Exception as e:
            logger.error(f"[AntiDuplication] Failed loading registry: {e}")

    def _save(self) -> None:
        path = self._get_storage_path()
        try:
            data = {
                "message_ids": list(self._processed_message_ids)[-1000:],
                "content_hashes": {k: v for k, v in list(self._processed_content_hashes.items())[-1000:]},
            }
            with open(path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            logger.error(f"[AntiDuplication] Failed saving registry: {e}")

    def is_duplicate(self, message_id: str, content_hash: str) -> bool:
        with self._lock:
            if message_id and message_id in self._processed_message_ids:
                logger.warning(f"[AntiDuplication] Duplicate message ID detected: '{message_id}'")
                return True

            if content_hash and content_hash in self._processed_content_hashes:
                logger.warning(f"[AntiDuplication] Duplicate content hash detected: '{content_hash[:12]}'")
                return True

            return False

    def register_processed(self, message_id: str, content_hash: str, note_id: int) -> None:
        with self._lock:
            if message_id:
                self._processed_message_ids.add(message_id)

            if content_hash:
                self._processed_content_hashes[content_hash] = {
                    "note_id": note_id,
                    "timestamp": time.time(),
                }

            self._save()
            logger.debug(f"[AntiDuplication] Registered card Note ID {note_id} (hash {content_hash[:8]})")

    def clear(self) -> None:
        with self._lock:
            self._processed_message_ids.clear()
            self._processed_content_hashes.clear()
            self._save()


# Global registry instance
dedup_registry = AntiDuplicationRegistry()
