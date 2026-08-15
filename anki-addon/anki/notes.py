"""
Anki Note Adapter.
Handles note instantiation, field assignment, tag sanitation, and saving to Collection.
"""

import html
import re
from typing import Any, Dict, List, Optional

try:
    from ..core.config import config
    from ..core.exceptions import AnkiAdapterError, DuplicateCardError, ValidationError
    from ..core.logger import logger
    from ..discord.models import CardPayload
    from ..templates.manager import template_manager
    from .decks import deck_adapter
except (ImportError, ValueError):
    from core.config import config
    from core.exceptions import AnkiAdapterError, DuplicateCardError, ValidationError
    from core.logger import logger
    from discord.models import CardPayload
    from templates.manager import template_manager
    from anki.decks import deck_adapter

try:
    from aqt import mw
    ANKI_AVAILABLE = True
except ImportError:
    mw = None
    ANKI_AVAILABLE = False


def _format_markdown_to_anki_html(text: str) -> str:
    """
    Lightweight, deterministic converter for Discord markdown formatting into HTML for Anki cards.
    Handles bold, italics, code blocks, inline code, and line breaks.
    """
    if not text:
        return ""

    # Replace code blocks ```lang ... ```
    def _code_block_sub(match):
        code_text = html.escape(match.group(1).strip(), quote=False)
        return f"<pre><code>{code_text}</code></pre>"

    text = re.sub(r"```(?:\w+)?\n?(.*?)```", _code_block_sub, text, flags=re.DOTALL)

    # Replace inline code `code`
    def _inline_code_sub(match):
        code_text = html.escape(match.group(1), quote=False)
        return f"<code>{code_text}</code>"

    text = re.sub(r"`([^`\n]+)`", _inline_code_sub, text)

    # Bold **text**
    text = re.sub(r"\*\*([^*]+)\*\*", r"<b>\1</b>", text)

    # Italic *text* or _text_
    text = re.sub(r"\*([^*]+)\*", r"<i>\1</i>", text)
    text = re.sub(r"_([^_]+)_", r"<i>\1</i>", text)

    # Convert linebreaks to <br> outside <pre>
    parts = re.split(r"(<pre><code>.*?</code></pre>)", text, flags=re.DOTALL)
    for i in range(len(parts)):
        if not parts[i].startswith("<pre>"):
            parts[i] = parts[i].replace("\n", "<br>")

    return "".join(parts)


class NoteAdapter:
    """
    Bridge between CardPayload domain models and Anki Collection Notes.
    """
    def __init__(self) -> None:
        pass

    def create_note_from_payload(self, payload: CardPayload) -> int:
        """
        Create and persist a Note in Anki from a CardPayload.
        Returns the created Note ID.
        """
        if not payload.front.strip():
            raise ValidationError("Card 'front' field cannot be empty.")

        if not ANKI_AVAILABLE or mw is None or mw.col is None:
            logger.info(f"[NoteAdapter] Headless simulation: Created note '{payload.front[:30]}' in deck '{payload.deck}'.")
            return 999001

        try:
            # 1. Resolve Note Model
            target_model_name = template_manager.normalize_template_name(payload.note_type)
            model = mw.col.models.by_name(target_model_name)
            if not model:
                model = mw.col.models.current()
                if not model:
                    raise AnkiAdapterError(f"No suitable Anki model found for '{payload.note_type}'.")

            # 2. Instantiate Note
            note = mw.col.new_note(model)

            # 3. Format & Map Fields
            formatted_payload = CardPayload(
                front=_format_markdown_to_anki_html(payload.front),
                back=_format_markdown_to_anki_html(payload.back),
                deck=payload.deck,
                tags=payload.tags,
                note_type=payload.note_type,
                extra=_format_markdown_to_anki_html(payload.extra),
            )

            field_map = template_manager.map_fields_to_model(formatted_payload, model)
            for field_name, field_value in field_map.items():
                if field_name in note:
                    note[field_name] = field_value

            # 4. Process Tags
            sanitized_tags: List[str] = []
            prefix = config.get("anki.tags_prefix", "")
            if prefix:
                sanitized_tags.append(re.sub(r"[^\w\-]", "_", prefix))

            for tag in payload.tags:
                clean_tag = re.sub(r"[^\w\-]", "_", tag.strip())
                if clean_tag and clean_tag not in sanitized_tags:
                    sanitized_tags.append(clean_tag)

            for tag in sanitized_tags:
                if hasattr(note, "add_tag"):
                    note.add_tag(tag)
                elif hasattr(note, "tags"):
                    if tag not in note.tags:
                        note.tags.append(tag)

            # 5. Resolve Target Deck
            deck_id = deck_adapter.get_or_create_deck(payload.deck)

            # 6. Add Note to Collection
            mw.col.add_note(note, deck_id)

            logger.info(f"[NoteAdapter] Created Note ID {note.id} in deck '{payload.deck}' with tags {sanitized_tags}")
            return note.id

        except Exception as e:
            if isinstance(e, (ValidationError, AnkiAdapterError)):
                raise
            raise AnkiAdapterError(f"Failed to add note to Anki Collection: {e}") from e


# Global note adapter instance
note_adapter = NoteAdapter()
