"""
Reviewer Hooks for Anki Review Screen.
"""

from typing import Any
from ..core.event_bus import event_bus
from ..core.logger import logger

try:
    from aqt import gui_hooks
    ANKI_AVAILABLE = True
except ImportError:
    gui_hooks = None
    ANKI_AVAILABLE = False


def _on_card_answered(reviewer: Any, card: Any, ease: int) -> None:
    event_bus.publish("reviewer:card_answered", card=card, ease=ease)


def register_reviewer_hooks() -> None:
    if not ANKI_AVAILABLE or gui_hooks is None:
        logger.debug("[Hooks:Reviewer] Anki environment not detected. Skipping reviewer hooks.")
        return

    try:
        if hasattr(gui_hooks, "reviewer_did_answer_card"):
            gui_hooks.reviewer_did_answer_card.append(_on_card_answered)
    except Exception as e:
        logger.error(f"[Hooks:Reviewer] Error registering reviewer hooks: {e}")
