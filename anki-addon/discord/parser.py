"""
Discord Message Protocol Parser.
Parses formatted !anki messages into validated CardPayload domain models.
"""

import re
from typing import Dict, List, Optional, Tuple

try:
    from ..core.constants import (
        DISCORD_COMMAND_PREFIX,
        FIELD_BACK,
        FIELD_CLOZE,
        FIELD_DECK,
        FIELD_EXTRA,
        FIELD_FRONT,
        FIELD_NOTE_TYPE,
        FIELD_TAGS,
        FIELD_TEMPLATE,
        FIELD_TYPE,
        MAX_MESSAGE_CHARACTERS,
    )
    from ..core.exceptions import ParserError, ValidationError
    from ..core.logger import logger
    from .models import CardPayload, DiscordMessageEvent
except (ImportError, ValueError):
    from core.constants import (
        DISCORD_COMMAND_PREFIX,
        FIELD_BACK,
        FIELD_CLOZE,
        FIELD_DECK,
        FIELD_EXTRA,
        FIELD_FRONT,
        FIELD_NOTE_TYPE,
        FIELD_TAGS,
        FIELD_TEMPLATE,
        FIELD_TYPE,
        MAX_MESSAGE_CHARACTERS,
    )
    from core.exceptions import ParserError, ValidationError
    from core.logger import logger
    from discord.models import CardPayload, DiscordMessageEvent


class DiscordParser:
    """
    Parses structured Discord messages into normalized CardPayload objects.
    """
    # Regex to match key: headers at line starts
    HEADER_REGEX = re.compile(
        r"^(front|back|deck|tags|tag|type|note_type|template|extra|cloze)\s*:\s*(.*)$",
        re.IGNORECASE | re.MULTILINE,
    )

    def is_anki_command(self, raw_text: str) -> bool:
        """Check if message starts with !anki command trigger."""
        if not raw_text:
            return False
        stripped = raw_text.strip()
        return stripped.startswith(DISCORD_COMMAND_PREFIX)

    def parse_message(
        self,
        raw_text: str,
        event: Optional[DiscordMessageEvent] = None,
    ) -> CardPayload:
        """
        Parse raw message string into a verified CardPayload.
        """
        if not raw_text or not raw_text.strip():
            raise ParserError("Empty message received.")

        if len(raw_text) > MAX_MESSAGE_CHARACTERS:
            raise ParserError(f"Message exceeds maximum allowed character length ({MAX_MESSAGE_CHARACTERS}).")

        text = raw_text.strip()

        # Remove the leading '!anki' command if present
        if text.lower().startswith(DISCORD_COMMAND_PREFIX):
            text = text[len(DISCORD_COMMAND_PREFIX):].strip()

        fields, extra_lines = self._extract_key_value_blocks(text)

        # Extract values
        front = fields.get(FIELD_FRONT, "").strip()
        back = fields.get(FIELD_BACK, "").strip()
        deck = fields.get(FIELD_DECK, "").strip()
        tags_raw = fields.get(FIELD_TAGS, "").strip()
        note_type = fields.get(FIELD_TYPE, fields.get(FIELD_NOTE_TYPE, fields.get(FIELD_TEMPLATE, ""))).strip()
        extra = fields.get(FIELD_EXTRA, "").strip()

        # Fallback for shorthand / quick format: Front? / Back on next lines
        if not front and extra_lines:
            front = extra_lines[0].strip()
            if len(extra_lines) > 1 and not back:
                back = "\n".join(extra_lines[1:]).strip()

        # Cloze keyword alias
        if FIELD_CLOZE in fields and not front:
            front = fields[FIELD_CLOZE].strip()
            if not note_type:
                note_type = "Cloze"

        # Auto-detect Cloze deletion syntax {{c1::...}}
        if not note_type and re.search(r"\{\{c\d+::", front):
            note_type = "Cloze"

        # Validate mandatory field
        if not front:
            raise ParserError(
                "Invalid format: Card must contain a 'front:' field.\n"
                "Example:\n"
                "!anki\n"
                "front: Question\n"
                "back: Answer\n"
                "deck: MyDeck\n"
                "tags: tag1, tag2"
            )

        # Standardize note type
        if not note_type:
            note_type = "Basic"

        # Parse tags
        tags = self._parse_tags(tags_raw)

        # Build payload
        payload = CardPayload(
            front=front,
            back=back,
            deck=deck or "Default",
            tags=tags,
            note_type=note_type,
            extra=extra,
            source="discord",
            message_id=event.id if event else "",
            author_id=event.author.id if event else "",
            author_name=str(event.author) if event else "",
            channel_id=event.channel.id if event else "",
            guild_id=event.channel.guild_id if event else "",
            timestamp=event.timestamp if event else 0.0,
            raw_content=raw_text,
        )

        return payload

    def _extract_key_value_blocks(self, text: str) -> Tuple[Dict[str, str], List[str]]:
        """
        Split message text into structured key-value blocks supporting multiline values.
        """
        lines = text.split("\n")
        fields: Dict[str, List[str]] = {}
        extra_preamble_lines: List[str] = []
        current_key: Optional[str] = None

        for line in lines:
            # Check for header
            match = re.match(r"^(front|back|deck|tags|tag|type|note_type|template|extra|cloze)\s*:\s*(.*)$", line, re.IGNORECASE)
            if match:
                raw_key = match.group(1).lower()
                first_line_val = match.group(2)
                # Normalize key names
                if raw_key == "tag":
                    raw_key = FIELD_TAGS
                elif raw_key in ("note_type", "template"):
                    raw_key = FIELD_TYPE

                current_key = raw_key
                fields[current_key] = [first_line_val] if first_line_val else []
            elif current_key is not None:
                fields[current_key].append(line)
            else:
                if line.strip():
                    extra_preamble_lines.append(line)

        # Join lines for each field
        result: Dict[str, str] = {}
        for k, v_lines in fields.items():
            result[k] = "\n".join(v_lines).strip()

        return result, extra_preamble_lines

    def _parse_tags(self, tags_raw: str) -> List[str]:
        """Normalize comma, space, hashtag, or semicolon separated tags."""
        if not tags_raw:
            return []

        # Replace hashtags #tag with space
        cleaned = re.sub(r"#([\w\-]+)", r"\1", tags_raw)
        # Split by comma or semicolon
        items = re.split(r"[,;]+", cleaned)
        tags: List[str] = []

        for item in items:
            parts = item.strip().split()
            for part in parts:
                clean_tag = part.strip()
                if clean_tag and clean_tag not in tags:
                    tags.append(clean_tag)

        return tags


# Global parser instance
discord_parser = DiscordParser()
