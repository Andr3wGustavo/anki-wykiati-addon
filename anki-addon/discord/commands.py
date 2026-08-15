"""
Discord Bot Command Handlers for Anki Wykiati Toolkit.
Processes operational commands: !anki-help, !anki-status, !anki-decks, and !anki-ping.
"""

from typing import Optional

try:
    from ..anki.decks import deck_adapter
    from ..core.config import config
    from ..core.constants import (
        ADDON_NAME,
        ADDON_VERSION,
        DISCORD_COMMAND_DECKS,
        DISCORD_COMMAND_HELP,
        DISCORD_COMMAND_PING,
        DISCORD_COMMAND_STATUS,
    )
    from .models import DiscordMessageEvent
except (ImportError, ValueError):
    from anki.decks import deck_adapter
    from core.config import config
    from core.constants import (
        ADDON_NAME,
        ADDON_VERSION,
        DISCORD_COMMAND_DECKS,
        DISCORD_COMMAND_HELP,
        DISCORD_COMMAND_PING,
        DISCORD_COMMAND_STATUS,
    )
    from discord.models import DiscordMessageEvent


class CommandRouter:
    """
    Routes and responds to Discord operational and informational commands.
    """
    def handle_command(self, raw_text: str, event: Optional[DiscordMessageEvent] = None) -> Optional[str]:
        """
        Check if message is a built-in command and return response string if applicable.
        """
        cmd = raw_text.strip().split()[0].lower() if raw_text.strip() else ""

        if cmd == DISCORD_COMMAND_HELP:
            return self._help_command()
        elif cmd == DISCORD_COMMAND_STATUS:
            return self._status_command()
        elif cmd == DISCORD_COMMAND_DECKS:
            return self._decks_command()
        elif cmd == DISCORD_COMMAND_PING:
            return "Pong! Anki Wykiati Toolkit bridge is active, connected, and healthy."

        return None

    def _help_command(self) -> str:
        return (
            f"**{ADDON_NAME} v{ADDON_VERSION} - Command Guide**\n\n"
            "**Create Basic Flashcard:**\n"
            "```text\n"
            "!anki\n"
            "front: What is a Docker container?\n"
            "back: A standardized unit of software packaging code and dependencies.\n"
            "deck: Programming::DevOps\n"
            "tags: docker, devops, containers\n"
            "```\n\n"
            "**Create Cloze Deletion Flashcard:**\n"
            "```text\n"
            "!anki\n"
            "front: The {{c1::TCP}} protocol guarantees ordered delivery, while {{c2::UDP}} minimizes latency.\n"
            "deck: Computer Science::Networking\n"
            "tags: networking, tcp, udp\n"
            "```\n\n"
            "**Other Operational Commands:**\n"
            f"- `{DISCORD_COMMAND_STATUS}`: Check system status and sync metrics\n"
            f"- `{DISCORD_COMMAND_DECKS}`: List all available Anki decks\n"
            f"- `{DISCORD_COMMAND_PING}`: Test connectivity with Anki\n"
        )

    def _status_command(self) -> str:
        stats = config.get("stats", {})
        cards_created = stats.get("cards_created", 0)
        images_ingested = stats.get("images_ingested", 0)
        messages_processed = stats.get("messages_processed", 0)
        failed_jobs = stats.get("failed_jobs", 0)
        theme_enabled = "Enabled (Full Black #000000)" if config.get("theme.enabled", True) else "Disabled"

        return (
            f"**{ADDON_NAME} - System Status**\n"
            f"- Version: v{ADDON_VERSION}\n"
            f"- Theme: {theme_enabled}\n"
            f"- Cards Created: {cards_created}\n"
            f"- Images Ingested: {images_ingested}\n"
            f"- Messages Processed: {messages_processed}\n"
            f"- Failed Jobs: {failed_jobs}\n"
            f"- Default Deck: {config.get('anki.default_deck', 'Default')}\n"
        )

    def _decks_command(self) -> str:
        decks = deck_adapter.list_all_decks()
        formatted = "\n".join(f"- `{d}`" for d in sorted(decks))
        return f"**Available Decks in Anki ({len(decks)}):**\n{formatted}"


# Global command router instance
command_router = CommandRouter()
