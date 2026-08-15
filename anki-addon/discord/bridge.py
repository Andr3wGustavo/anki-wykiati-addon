"""
Discord Bridge Orchestrator.
Receives raw Discord messages/events, runs security verification, parses payloads, and enqueues card jobs.
"""

from typing import Dict, Optional, Tuple

try:
    from ..core.config import config
    from ..core.event_bus import event_bus
    from ..core.exceptions import DiscordToolkitError, ParserError, SecurityError
    from ..core.logger import logger
    from ..sync.queue import job_queue
    from .commands import command_router
    from .models import CardPayload, DiscordMessageEvent
    from .parser import discord_parser
    from .security import auth_policy
except (ImportError, ValueError):
    from core.config import config
    from core.event_bus import event_bus
    from core.exceptions import DiscordToolkitError, ParserError, SecurityError
    from core.logger import logger
    from sync.queue import job_queue
    from discord.commands import command_router
    from discord.models import CardPayload, DiscordMessageEvent
    from discord.parser import discord_parser
    from discord.security import auth_policy


class DiscordBridge:
    """
    Decoupled bridge that translates Discord events into Anki cards.
    """
    def __init__(self) -> None:
        pass

    def handle_incoming_message(
        self,
        raw_text: str,
        event: Optional[DiscordMessageEvent] = None,
    ) -> Tuple[bool, str]:
        """
        Process incoming text from Discord or HTTP bridge.
        Returns (success: bool, response_message: str).
        """
        if not raw_text or not raw_text.strip():
            return False, "Empty message."

        try:
            # 1. Update processed metrics
            stats = config.get("stats", {})
            stats["messages_processed"] = stats.get("messages_processed", 0) + 1
            config.set("stats", stats, save=False)

            # 2. Security validation
            if event:
                auth_policy.validate_event(event)

            # 3. Check for operational commands (!anki-help, !anki-status, !anki-decks, !anki-ping)
            cmd_reply = command_router.handle_command(raw_text, event)
            if cmd_reply:
                return True, cmd_reply

            # 4. Check if message is an !anki card creation prompt
            if not discord_parser.is_anki_command(raw_text):
                return False, "Message does not contain the `!anki` command trigger."

            # 5. Parse message into CardPayload
            payload: CardPayload = discord_parser.parse_message(raw_text, event)

            # 6. Enqueue card creation job
            job = job_queue.enqueue(payload)

            # 7. Publish event
            event_bus.publish("discord:card_enqueued", payload, job)

            success_response = (
                f"✅ **Card Enqueued!** (Job `{job.id}`)\n"
                f"• **Front:** {payload.front[:60]}{'...' if len(payload.front) > 60 else ''}\n"
                f"• **Deck:** `{payload.deck}`\n"
                f"• **Tags:** {', '.join(payload.tags) if payload.tags else '*(none)*'}"
            )
            logger.info(f"[DiscordBridge] Successfully enqueued card from Discord user '{payload.author_name or 'Anonymous'}'.")
            return True, success_response

        except SecurityError as sec_err:
            logger.warning(f"[DiscordBridge] Security rejection: {sec_err}")
            return False, f"⛔ **Acesso Negado:** {sec_err.message}"

        except ParserError as parse_err:
            logger.warning(f"[DiscordBridge] Parser error: {parse_err}")
            return False, f"⚠️ **Erro de Formato:**\n{parse_err.message}"

        except DiscordToolkitError as dt_err:
            logger.error(f"[DiscordBridge] Toolkit error: {dt_err}")
            return False, f"❌ **Erro:** {dt_err.message}"

        except Exception as e:
            logger.error(f"[DiscordBridge] Unexpected bridge exception: {e}", exc_info=True)
            return False, f"❌ **Erro Interno no Anki:** {e}"


# Global bridge singleton
discord_bridge = DiscordBridge()
