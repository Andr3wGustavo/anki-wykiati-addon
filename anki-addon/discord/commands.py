"""
Discord Bot Command Handlers.
Processes commands like !anki-help, !anki-status, !anki-decks, and !anki-ping.
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
            return "🏓 **Pong!** Anki Discord Toolkit bridge is active, connected, and healthy."

        return None

    def _help_command(self) -> str:
        return (
            f"📖 **{ADDON_NAME} v{ADDON_VERSION} — Guia de Comandos**\n\n"
            "**Criar Cartão Básico:**\n"
            "```text\n"
            "!anki\n"
            "front: O que é Docker?\n"
            "back: Docker é uma plataforma de containers baseada em Linux cgroups e namespaces.\n"
            "deck: Programming::DevOps\n"
            "tags: docker, devops, infra\n"
            "```\n\n"
            "**Criar Cartão com Omissão de Palavras (Cloze):**\n"
            "```text\n"
            "!anki\n"
            "front: O {{c1::TCP}} garante entrega ordenada, enquanto o {{c2::UDP}} foca em baixa latência.\n"
            "deck: Networking\n"
            "tags: redes, tcp, udp\n"
            "```\n\n"
            "**Outros Comandos Disponíveis:**\n"
            f"• `{DISCORD_COMMAND_STATUS}` — Verifica status e métricas do Anki\n"
            f"• `{DISCORD_COMMAND_DECKS}` — Lista todos os Decks disponíveis\n"
            f"• `{DISCORD_COMMAND_PING}` — Testa conectividade com o Anki\n"
        )

    def _status_command(self) -> str:
        stats = config.get("stats", {})
        cards_created = stats.get("cards_created", 0)
        messages_processed = stats.get("messages_processed", 0)
        failed_jobs = stats.get("failed_jobs", 0)
        theme_enabled = "Ativado (Pure Black #000000)" if config.get("theme.enabled", True) else "Desativado"

        return (
            f"⚡ **{ADDON_NAME} — Status do Sistema**\n"
            f"• **Versão:** v{ADDON_VERSION}\n"
            f"• **Tema:** {theme_enabled}\n"
            f"• **Cartões Criados:** {cards_created}\n"
            f"• **Mensagens Processadas:** {messages_processed}\n"
            f"• **Falhas Registradas:** {failed_jobs}\n"
            f"• **Deck Padrão:** {config.get('anki.default_deck', 'Default')}\n"
        )

    def _decks_command(self) -> str:
        decks = deck_adapter.list_all_decks()
        formatted = "\n".join(f"• `{d}`" for d in sorted(decks))
        return f"📚 **Decks Disponíveis no Anki ({len(decks)}):**\n{formatted}"


# Global command router instance
command_router = CommandRouter()
