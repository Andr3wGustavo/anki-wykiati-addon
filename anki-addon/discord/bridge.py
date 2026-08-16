"""
Discord Bridge Orchestrator.
Receives raw Discord messages/events, runs security verification,
handles automatic image channel ingestion, parses payloads, and enqueues card jobs.
"""

import re
from typing import Dict, List, Optional, Tuple

try:
    from ..anki.media import media_manager
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
    from anki.media import media_manager
    from core.config import config
    from core.event_bus import event_bus
    from core.exceptions import DiscordToolkitError, ParserError, SecurityError
    from core.logger import logger
    from sync.queue import job_queue
    from discord.commands import command_router
    from discord.models import CardPayload, DiscordMessageEvent
    from discord.parser import discord_parser
    from discord.security import auth_policy


IMAGE_URL_REGEX = re.compile(
    r"https?://\S+?\.(?:png|jpg|jpeg|webp|gif)(?:\?\S*)?",
    re.IGNORECASE,
)


class DiscordBridge:
    """
    Decoupled bridge that translates Discord events, commands, and images into Anki cards.
    """
    def __init__(self) -> None:
        pass

    def handle_incoming_message(
        self,
        raw_text: str,
        event: Optional[DiscordMessageEvent] = None,
    ) -> Tuple[bool, str]:
        """
        Process incoming text or images from Discord or HTTP bridge.
        Returns (success: bool, response_message: str).
        """
        try:
            # 1. Update processed metrics
            stats = config.get("stats", {})
            stats["messages_processed"] = stats.get("messages_processed", 0) + 1
            config.set("stats", stats, save=False)

            # 2. Security validation
            if event:
                auth_policy.validate_event(event)

            # 3. Check for operational commands (!anki-help, !anki-status, !anki-decks, !anki-ping)
            if raw_text:
                cmd_reply = command_router.handle_command(raw_text, event)
                if cmd_reply:
                    return True, cmd_reply

            # 4. Check for Dedicated Image Channel or Image Attachments
            image_urls = self._extract_image_urls(raw_text, event)
            is_image_channel = self._is_designated_image_channel(event)

            if image_urls or (is_image_channel and event and event.attachments):
                return self._process_image_ingestion(raw_text, event, image_urls)

            # 5. Check if message is a standard !anki card creation prompt
            if not discord_parser.is_anki_command(raw_text):
                return False, "Message does not contain the `!anki` command trigger or image attachment."

            # 6. Parse message into CardPayload
            payload: CardPayload = discord_parser.parse_message(raw_text, event)

            # 7. Enqueue card creation job
            job = job_queue.enqueue(payload)

            # 8. Publish event
            event_bus.publish("discord:card_enqueued", payload, job)

            success_response = (
                f"Card Enqueued (Job ID: {job.id})\n"
                f"• Front: {payload.front[:60]}{'...' if len(payload.front) > 60 else ''}\n"
                f"• Deck: {payload.deck}\n"
                f"• Tags: {', '.join(payload.tags) if payload.tags else '(none)'}"
            )
            logger.info(f"[DiscordBridge] Enqueued card from Discord user '{payload.author_name or 'Anonymous'}'.")
            return True, success_response

        except SecurityError as sec_err:
            logger.warning(f"[DiscordBridge] Security rejection: {sec_err}")
            return False, f"Access Denied: {sec_err.message}"

        except ParserError as parse_err:
            logger.warning(f"[DiscordBridge] Parser error: {parse_err}")
            return False, f"Format Error:\n{parse_err.message}"

        except DiscordToolkitError as dt_err:
            logger.error(f"[DiscordBridge] Toolkit error: {dt_err}")
            return False, f"Error: {dt_err.message}"

        except Exception as e:
            logger.error(f"[DiscordBridge] Unexpected bridge exception: {e}", exc_info=True)
            return False, f"Internal Error: {e}"

    def _is_designated_image_channel(self, event: Optional[DiscordMessageEvent]) -> bool:
        if not event or not event.channel or not event.channel.id:
            return False
        image_channels = config.get("discord.image_channels", [])
        return str(event.channel.id) in [str(c) for c in image_channels]

    def _extract_image_urls(self, raw_text: str, event: Optional[DiscordMessageEvent]) -> List[str]:
        urls: List[str] = []

        # From attachments
        if event and event.attachments:
            for att in event.attachments:
                if att.url:
                    urls.append(att.url)

        # From text URL patterns
        if raw_text:
            matches = IMAGE_URL_REGEX.findall(raw_text)
            for m in matches:
                if m not in urls:
                    urls.append(m)

        return urls

    def _process_image_ingestion(
        self,
        raw_text: str,
        event: Optional[DiscordMessageEvent],
        image_urls: List[str],
    ) -> Tuple[bool, str]:
        """
        Process images by downloading them, saving into Anki media storage, and generating cards.
        """
        if not image_urls:
            return False, "No valid image attachments or URLs detected."

        default_image_deck = config.get("discord.image_default_deck", "Images::Discord")
        default_tags = list(config.get("discord.image_default_tags", ["discord", "image"]))
        layout = config.get("discord.image_card_layout", "image_front")

        enqueued_jobs = []

        for url in image_urls:
            success, filename, img_hash = media_manager.download_and_save_image(url)
            if not success:
                logger.error(f"[DiscordBridge] Could not download image '{url}': {img_hash}")
                continue

            img_tag = f'<img src="{filename}">'
            caption = raw_text.strip() if raw_text else ""
            # Strip image URL from caption text
            clean_caption = IMAGE_URL_REGEX.sub("", caption).strip()

            if layout in ("image_only_front", "image_front_empty_back", "front_only"):
                front = img_tag
                back = ""
            elif layout == "image_back":
                front = clean_caption or "Identify this image"
                back = img_tag
            else:  # "image_front"
                front = img_tag
                back = clean_caption or "Visual Reference"

            payload = CardPayload(
                front=front,
                back=back,
                deck=default_image_deck,
                tags=default_tags,
                note_type="Basic",
                image_url=url,
                image_filename=filename,
                source="discord_image",
                message_id=event.id if event else "",
                author_id=event.author.id if event else "",
                author_name=str(event.author) if event else "Anonymous",
                channel_id=event.channel.id if event else "",
                guild_id=event.channel.guild_id if event else "",
                timestamp=event.timestamp if event else 0.0,
                raw_content=raw_text,
            )

            job = job_queue.enqueue(payload)
            enqueued_jobs.append(job)

            # Update stats
            stats = config.get("stats", {})
            stats["images_ingested"] = stats.get("images_ingested", 0) + 1
            config.set("stats", stats, save=False)

            event_bus.publish("discord:image_enqueued", payload, job)

        if enqueued_jobs:
            logger.info(f"[DiscordBridge] Ingested {len(enqueued_jobs)} image card(s).")
            return True, f"Successfully enqueued {len(enqueued_jobs)} image flashcard(s) to deck '{default_image_deck}'."

        return False, "Failed to download or persist image attachments."


# Global bridge singleton
discord_bridge = DiscordBridge()
