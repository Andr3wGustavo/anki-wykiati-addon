"""
Anki Deck Adapter.
Provides safe operations for locating, validating, and creating decks (including nested hierarchy).
"""

from typing import List, Optional

try:
    from ..core.exceptions import AnkiAdapterError
    from ..core.logger import logger
except (ImportError, ValueError):
    from core.exceptions import AnkiAdapterError
    from core.logger import logger

try:
    from aqt import mw
    ANKI_AVAILABLE = True
except ImportError:
    mw = None
    ANKI_AVAILABLE = False


class DeckAdapter:
    """
    Interacts with Anki's deck manager via official APIs.
    """
    def __init__(self) -> None:
        self.default_deck = "Default"

    def get_or_create_deck(self, deck_name: str) -> int:
        """
        Get existing deck ID or create a new deck (including hierarchical decks like 'DevOps::Docker').
        """
        target_name = (deck_name or self.default_deck).strip()

        if not ANKI_AVAILABLE or mw is None or mw.col is None:
            logger.info(f"[DeckAdapter] Simulated get_or_create_deck for '{target_name}' (Headless).")
            return 1

        try:
            deck_id = mw.col.decks.id(target_name)
            logger.debug(f"[DeckAdapter] Deck '{target_name}' resolved to ID {deck_id}.")
            return deck_id
        except Exception as e:
            raise AnkiAdapterError(f"Failed to resolve/create deck '{target_name}': {e}")

    def list_all_decks(self) -> List[str]:
        """Return names of all decks in current collection."""
        if not ANKI_AVAILABLE or mw is None or mw.col is None:
            return ["Default", "Programming::Python", "DevOps::Docker"]

        try:
            return [d["name"] for d in mw.col.decks.all()]
        except Exception as e:
            logger.error(f"[DeckAdapter] Failed to list decks: {e}")
            return [self.default_deck]

    def deck_exists(self, deck_name: str) -> bool:
        """Check if a deck already exists in the collection."""
        if not ANKI_AVAILABLE or mw is None or mw.col is None:
            return True

        try:
            deck = mw.col.decks.by_name(deck_name.strip())
            return deck is not None
        except Exception:
            return False


# Global deck adapter instance
deck_adapter = DeckAdapter()
