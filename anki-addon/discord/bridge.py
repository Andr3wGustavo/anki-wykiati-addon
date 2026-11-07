"""
Discord Bridge Orchestrator.
Receives raw Discord messages/events, runs security verification,
handles automatic image channel ingestion, parses payloads, and enqueues card jobs.
"""

import html
import re
from typing import Dict, List, Optional, Tuple

try:
    from ..core.image_urls import IMAGE_URL_REGEX as _IMAGE_URL_REGEX
    from ..anki.media import media_manager
    from ..core.config import config
    from ..core.event_bus import event_bus
    from ..core.exceptions import DiscordToolkitError, ParserError, SecurityError
    from ..core.logger import logger
    from ..sync.dedup import dedup_registry
    from ..sync.queue import job_queue
    from .commands import command_router
    from .models import CardPayload, DiscordMessageEvent
    from .parser import discord_parser
    from .security import auth_policy
except (ImportError, ValueError):
    from core.image_urls import IMAGE_URL_REGEX as _IMAGE_URL_REGEX
    from anki.media import media_manager
    from core.config import config
    from core.event_bus import event_bus
    from core.exceptions import DiscordToolkitError, ParserError, SecurityError
    from core.logger import logger
    from sync.dedup import dedup_registry
    from sync.queue import job_queue
    from discord.commands import command_router
    from discord.models import CardPayload, DiscordMessageEvent
    from discord.parser import discord_parser
    from discord.security import auth_policy


# Shared with the poller's embed/attachment extraction
IMAGE_URL_REGEX = _IMAGE_URL_REGEX


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

            is_image_channel = self._is_designated_image_channel(event)

            # 2. Security validation
            if event:
                auth_policy.validate_event(event, trusted_image_channel=is_image_channel)

            # 3. Check for operational commands (!anki-help, !anki-status, !anki-decks, !anki-ping)
            if raw_text:
                cmd_reply = command_router.handle_command(raw_text, event)
                if cmd_reply:
                    return True, cmd_reply

            # 4. Check for Dedicated Image Channel or Image Attachments
            image_urls = self._extract_image_urls(raw_text, event)

            if image_urls:
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
        return str(event.channel.id) in [str(c).strip() for c in image_channels]

    def _extract_image_urls(self, raw_text: str, event: Optional[DiscordMessageEvent]) -> List[str]:
        urls: List[str] = []

        def add(url: str) -> None:
            if url and url not in urls:
                urls.append(url)

        if event:
            for url in event.image_urls:  # embeds + attachments, pre-extracted by the poller
                add(url)
            for att in event.attachments:
                add(att.url)

        if raw_text:
            for match in IMAGE_URL_REGEX.findall(raw_text):
                add(match)

        return urls

    def _process_image_ingestion(
        self,
        raw_text: str,
        event: Optional[DiscordMessageEvent],
        image_urls: List[str],
    ) -> Tuple[bool, str]:
        """
        Download + optimize each image into the staging area (safe on background threads)
        and enqueue one card job per image. The media file is written into the
        collection and the note is created later on Anki's main thread by SyncWorker.
        """
        if not image_urls:
            return False, "No valid image attachments or URLs detected."

        message_id = event.id if event else ""
        if message_id and dedup_registry.is_message_processed(message_id):
            logger.info(f"[DiscordBridge] Message {message_id} already imported; skipping.")
            return False, "Message already imported."

        default_image_deck = config.get("discord.image_default_deck", "Images::Discord")
        default_tags = list(config.get("discord.image_default_tags", ["discord", "image"]))
        layout = config.get("discord.image_card_layout", "image_only_front")

        caption = raw_text.strip() if raw_text else ""
        # Untrusted text inserted as HTML: strip image links, escape, keep line breaks
        clean_caption = html.escape(IMAGE_URL_REGEX.sub("", caption).strip(), quote=False)
        clean_caption = clean_caption.replace("\n", "<br>")

        enqueued_jobs = []
        failures: List[str] = []

        for index, url in enumerate(image_urls):
            staged = media_manager.stage_image(url)
            if not staged.ok:
                failures.append(staged.error)
                logger.error(f"[DiscordBridge] Could not download image '{url}': {staged.error}")
                continue

            img_tag = f'<img src="{html.escape(staged.filename, quote=True)}">'

            if layout == "image_back":
                front = clean_caption or "Identify this image"
                back = img_tag
            elif layout == "image_front":
                front = img_tag
                back = clean_caption or "Visual Reference"
            else:  # "image_only_front" (default): image on the front, empty back
                front = img_tag
                back = ""

            payload = CardPayload(
                front=front,
                back=back,
                deck=default_image_deck,
                tags=default_tags,
                note_type="Basic",
                image_url=staged.source_url or url,
                image_filename=staged.filename,
                source="discord_image",
                # Several images in one message: one card each, distinct message keys
                message_id=(f"{message_id}#{index}" if message_id and len(image_urls) > 1 else message_id),
                author_id=event.author.id if event else "",
                author_name=str(event.author) if event else "Anonymous",
                channel_id=event.channel.id if event else "",
                guild_id=event.channel.guild_id if event else "",
                timestamp=event.timestamp if event else 0.0,
                raw_content=raw_text,
                staging_path=staged.staging_path,
                image_hash=staged.image_hash,
                bytes_saved=staged.bytes_saved,
            )

            job = job_queue.enqueue(payload)
            enqueued_jobs.append(job)
            event_bus.publish("discord:image_enqueued", payload, job)

        if enqueued_jobs:
            logger.info(f"[DiscordBridge] Enqueued {len(enqueued_jobs)} image card(s) for deck '{default_image_deck}'.")
            return True, f"Successfully enqueued {len(enqueued_jobs)} image flashcard(s) to deck '{default_image_deck}'."

        reason = failures[0] if failures else "unknown error"
        return False, f"Failed to download image(s): {reason}"


# Global bridge singleton
discord_bridge = DiscordBridge()
