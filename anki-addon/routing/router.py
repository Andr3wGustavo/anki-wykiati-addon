"""
Smart Deck Router.
Matches CardPayload against user-defined tag and keyword rules to determine the target deck.
"""

from typing import Any, Dict, List, Optional

try:
    from ..core.config import config
    from ..core.logger import logger
    from ..discord.models import CardPayload
except (ImportError, ValueError):
    from core.config import config
    from core.logger import logger
    from discord.models import CardPayload


class DeckRouter:
    """
    Evaluates hierarchical deck routing rules for incoming cards.
    """
    def __init__(self) -> None:
        pass

    def get_rules(self) -> List[Dict[str, str]]:
        """Fetch routing rules from configuration."""
        rules = config.get("routing.rules", [])
        return list(rules) if isinstance(rules, list) else []

    def set_rules(self, rules: List[Dict[str, str]]) -> None:
        """Update and persist routing rules."""
        config.set("routing.rules", rules)
        logger.info(f"[DeckRouter] Updated {len(rules)} deck routing rule(s).")

    def resolve_deck(self, payload: CardPayload) -> str:
        """
        Determine target deck for a card payload based on:
        1. Explicitly designated deck in message (if non-default)
        2. Tag-based rules (e.g. tag:python -> Programming::Python)
        3. Keyword-based rules in front/back (e.g. keyword:docker -> DevOps::Docker)
        4. Configured default fallback deck
        """
        default_deck = config.get("anki.default_deck", "Default")

        # 1. Explicit deck in payload
        if payload.deck and payload.deck.strip() and payload.deck.strip().lower() != "default":
            logger.debug(f"[DeckRouter] Using explicit deck '{payload.deck}'")
            return payload.deck.strip()

        if not config.get("routing.enabled", True):
            return default_deck

        rules = self.get_rules()
        normalized_tags = [t.strip().lower() for t in payload.tags]
        search_text = f"{payload.front} {payload.back}".lower()

        # 2. Check Tag Rules (High priority)
        for rule in rules:
            rule_type = rule.get("type", "").lower()
            pattern = rule.get("pattern", "").strip().lower()
            target_deck = rule.get("deck", "").strip()

            if not pattern or not target_deck:
                continue

            if rule_type == "tag":
                if pattern in normalized_tags:
                    logger.info(f"[DeckRouter] Matched tag rule '{pattern}' -> '{target_deck}'")
                    return target_deck

        # 3. Check Keyword Rules (Medium priority)
        for rule in rules:
            rule_type = rule.get("type", "").lower()
            pattern = rule.get("pattern", "").strip().lower()
            target_deck = rule.get("deck", "").strip()

            if not pattern or not target_deck:
                continue

            if rule_type == "keyword":
                if pattern in search_text:
                    logger.info(f"[DeckRouter] Matched keyword rule '{pattern}' -> '{target_deck}'")
                    return target_deck

        # 4. Fallback to default deck
        logger.debug(f"[DeckRouter] No rule matched. Falling back to default deck '{default_deck}'.")
        return default_deck


# Global router instance
deck_router = DeckRouter()
