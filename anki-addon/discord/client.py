"""
Discord Client and Local HTTP Webhook Bridge Server.
Allows cards to be pushed via Discord Bot Poller (including automated image channels) or Local HTTP REST Webhook.
"""

import http.server
import json
import socketserver
import threading
import time
import urllib.error
import urllib.request
from typing import Any, Dict, List, Optional

try:
    from ..core.config import config
    from ..core.constants import ADDON_NAME, ADDON_VERSION
    from ..core.logger import logger
    from .bridge import discord_bridge
    from .models import DiscordAttachment, DiscordChannel, DiscordMessageEvent, DiscordUser
except (ImportError, ValueError):
    from core.config import config
    from core.constants import ADDON_NAME, ADDON_VERSION
    from core.logger import logger
    from discord.bridge import discord_bridge
    from discord.models import DiscordAttachment, DiscordChannel, DiscordMessageEvent, DiscordUser


class _BridgeHTTPRequestHandler(http.server.BaseHTTPRequestHandler):
    """Handles incoming HTTP POST / GET webhook requests."""

    def log_message(self, format: str, *args: Any) -> None:
        logger.debug(f"[HttpBridge] {self.client_address[0]} - {format % args}")

    def _send_json(self, status_code: int, data: Dict[str, Any]) -> None:
        body = json.dumps(data, indent=2).encode("utf-8")
        self.send_response(status_code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Headers", "Content-Type, Authorization")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.end_headers()
        self.wfile.write(body)

    def do_OPTIONS(self) -> None:
        self._send_json(200, {"status": "ok"})

    def do_GET(self) -> None:
        if self.path in ("/", "/health", "/api/health"):
            stats = config.get("stats", {})
            self._send_json(200, {
                "status": "healthy",
                "addon": ADDON_NAME,
                "version": ADDON_VERSION,
                "stats": stats,
            })
        else:
            self._send_json(404, {"error": "Not Found"})

    def do_POST(self) -> None:
        try:
            content_length = int(self.headers.get("Content-Length", 0))
            if content_length > 100 * 1024:  # 100 KB limit
                self._send_json(413, {"error": "Payload too large"})
                return

            body_bytes = self.rfile.read(content_length)
            body_str = body_bytes.decode("utf-8")

            raw_text = ""
            event = None
            attachments: List[DiscordAttachment] = []

            content_type = self.headers.get("Content-Type", "")
            if "application/json" in content_type:
                data = json.loads(body_str) if body_str else {}

                # Check if image_url was explicitly sent in JSON
                if "image_url" in data:
                    attachments.append(DiscordAttachment(
                        id=f"http_att_{int(time.time()*1000)}",
                        url=data.get("image_url", ""),
                        filename=data.get("filename", "image.png"),
                    ))
                    raw_text = data.get("caption", data.get("front", data.get("content", "")))
                elif "content" in data or "message" in data:
                    raw_text = data.get("content") or data.get("message", "")
                else:
                    front = data.get("front", "")
                    back = data.get("back", "")
                    deck = data.get("deck", "")
                    tags = ", ".join(data.get("tags", [])) if isinstance(data.get("tags"), list) else data.get("tags", "")
                    note_type = data.get("type") or data.get("note_type", "Basic")

                    raw_text = f"!anki\nfront: {front}\nback: {back}\ndeck: {deck}\ntags: {tags}\ntype: {note_type}"

                author_name = data.get("author", "HTTP User")
                author_id = str(data.get("author_id", "http_user"))
                channel_id = str(data.get("channel_id", "http_bridge"))

                event = DiscordMessageEvent(
                    id=str(data.get("message_id", f"http_{int(time.time()*1000)}")),
                    content=raw_text,
                    author=DiscordUser(id=author_id, name=author_name),
                    channel=DiscordChannel(id=channel_id, name="http_channel"),
                    attachments=attachments,
                    timestamp=time.time(),
                )
            else:
                raw_text = body_str
                event = DiscordMessageEvent(
                    id=f"http_{int(time.time()*1000)}",
                    content=raw_text,
                    author=DiscordUser(id="http_user", name="HTTP User"),
                    channel=DiscordChannel(id="http_bridge", name="http_channel"),
                    timestamp=time.time(),
                )

            # Process with bridge
            success, reply_msg = discord_bridge.handle_incoming_message(raw_text, event)
            status_code = 200 if success else 400
            self._send_json(status_code, {
                "success": success,
                "message": reply_msg,
            })

        except Exception as e:
            logger.error(f"[HttpBridge] Error handling POST request: {e}", exc_info=True)
            self._send_json(500, {"success": False, "error": str(e)})


class HttpBridgeServer:
    """
    Background HTTP Server enabling REST webhook card submissions.
    """
    def __init__(self, host: str = "127.0.0.1", port: int = 8765) -> None:
        self.host = host
        self.port = port
        self._server: Optional[socketserver.TCPServer] = None
        self._thread: Optional[threading.Thread] = None

    def start(self) -> bool:
        if self._server is not None:
            return True

        try:
            socketserver.TCPServer.allow_reuse_address = True
            self._server = socketserver.TCPServer((self.host, self.port), _BridgeHTTPRequestHandler)
            self._thread = threading.Thread(target=self._server.serve_forever, daemon=True, name="ADT-HttpBridge")
            self._thread.start()
            logger.info(f"[HttpBridgeServer] Listening on http://{self.host}:{self.port}")
            return True
        except Exception as e:
            logger.error(f"[HttpBridgeServer] Failed to bind on {self.host}:{self.port}: {e}")
            self._server = None
            return False

    def stop(self) -> None:
        if self._server:
            try:
                self._server.shutdown()
                self._server.server_close()
            except Exception:
                pass
            self._server = None
            logger.info("[HttpBridgeServer] Server stopped.")


class DiscordPollingWorker:
    """
    Lightweight background worker that polls Discord channels (including image channels)
    using Bot Token and REST API without heavy external dependencies.
    """
    def __init__(self) -> None:
        self._running = False
        self._thread: Optional[threading.Thread] = None
        self._stop_event = threading.Event()
        self._last_seen_message_id: Dict[str, str] = {}

    def _get_target_channels(self) -> List[str]:
        standard_channels = config.get("discord.channel_ids", [])
        image_channels = config.get("discord.image_channels", [])
        combined = []
        for c in standard_channels + image_channels:
            clean = str(c).strip()
            if clean and clean not in combined:
                combined.append(clean)
        return combined

    def start(self) -> None:
        if self._running:
            return

        bot_token = config.get("discord.bot_token", "").strip()
        channels = self._get_target_channels()
        if not bot_token or not channels:
            logger.debug("[DiscordPollingWorker] Bot token or channel IDs missing. Poller idle.")
            return

        self._running = True
        self._stop_event.clear()
        self._thread = threading.Thread(target=self._poll_loop, name="ADT-DiscordPoller", daemon=True)
        self._thread.start()
        logger.info(f"[DiscordPollingWorker] Polling started for {len(channels)} channel(s).")

    def stop(self) -> None:
        if not self._running:
            return

        self._running = False
        self._stop_event.set()
        if self._thread and self._thread.is_alive():
            self._thread.join(timeout=2.0)
        logger.info("[DiscordPollingWorker] Polling stopped.")

    def _poll_loop(self) -> None:
        while not self._stop_event.is_set():
            interval = max(3, int(config.get("discord.polling_interval_seconds", 5)))
            channels = self._get_target_channels()
            bot_token = config.get("discord.bot_token", "").strip()

            if not bot_token or not channels:
                self._stop_event.wait(timeout=interval)
                continue

            for channel_id in channels:
                if self._stop_event.is_set():
                    break
                try:
                    self._poll_channel(str(channel_id).strip(), bot_token)
                except Exception as e:
                    logger.debug(f"[DiscordPollingWorker] Polling error on channel {channel_id}: {e}")

            self._stop_event.wait(timeout=interval)

    def _poll_channel(self, channel_id: str, bot_token: str) -> None:
        url = f"https://discord.com/api/v10/channels/{channel_id}/messages?limit=5"
        req = urllib.request.Request(
            url,
            headers={
                "Authorization": f"Bot {bot_token}",
                "User-Agent": f"AnkiDiscordToolkit/{ADDON_VERSION}",
            },
        )

        try:
            with urllib.request.urlopen(req, timeout=8) as response:
                if response.status == 200:
                    data = json.loads(response.read().decode("utf-8"))
                    self._process_channel_messages(channel_id, data, bot_token)
        except urllib.error.HTTPError as e:
            if e.code == 401:
                logger.error("[DiscordPollingWorker] Invalid Discord Bot Token (401 Unauthorized).")
            elif e.code == 403:
                logger.warning(f"[DiscordPollingWorker] Bot lacks permission to read channel {channel_id}.")
        except Exception as e:
            logger.debug(f"[DiscordPollingWorker] Network error: {e}")

    def _process_channel_messages(self, channel_id: str, messages: List[Dict[str, Any]], bot_token: str) -> None:
        if not messages:
            return

        last_id = self._last_seen_message_id.get(channel_id)
        newest_id = str(messages[0].get("id"))

        if last_id is None:
            self._last_seen_message_id[channel_id] = newest_id
            return

        new_msgs = []
        for msg in messages:
            msg_id = str(msg.get("id"))
            if int(msg_id) > int(last_id):
                new_msgs.append(msg)

        self._last_seen_message_id[channel_id] = newest_id

        for msg in reversed(new_msgs):
            author_info = msg.get("author", {})
            if author_info.get("bot", False):
                continue

            content = msg.get("content", "")
            raw_attachments = msg.get("attachments", [])

            # Extract attachment metadata
            parsed_attachments: List[DiscordAttachment] = []
            for a in raw_attachments:
                parsed_attachments.append(DiscordAttachment(
                    id=str(a.get("id")),
                    url=str(a.get("url")),
                    filename=str(a.get("filename", "image.png")),
                    content_type=str(a.get("content_type", "")),
                    size=int(a.get("size", 0)),
                ))

            # Must have either text or attachments
            if not content.strip() and not parsed_attachments:
                continue

            event = DiscordMessageEvent(
                id=str(msg.get("id")),
                content=content,
                author=DiscordUser(
                    id=str(author_info.get("id")),
                    name=author_info.get("username", "Unknown"),
                    discriminator=author_info.get("discriminator", ""),
                ),
                channel=DiscordChannel(id=channel_id),
                attachments=parsed_attachments,
                timestamp=time.time(),
            )

            success, reply_text = discord_bridge.handle_incoming_message(content, event)
            if success and reply_text:
                self._send_discord_reply(channel_id, str(msg.get("id")), reply_text, bot_token)

    def _send_discord_reply(self, channel_id: str, message_id: str, text: str, bot_token: str) -> None:
        url = f"https://discord.com/api/v10/channels/{channel_id}/messages"
        payload_data = json.dumps({
            "content": text,
            "message_reference": {"message_id": message_id},
        }).encode("utf-8")

        req = urllib.request.Request(
            url,
            data=payload_data,
            headers={
                "Authorization": f"Bot {bot_token}",
                "Content-Type": "application/json",
                "User-Agent": f"AnkiDiscordToolkit/{ADDON_VERSION}",
            },
            method="POST",
        )
        try:
            with urllib.request.urlopen(req, timeout=5):
                pass
        except Exception as e:
            logger.debug(f"[DiscordPollingWorker] Failed sending Discord reply: {e}")


class DiscordClientManager:
    """
    Controls lifetime of Discord Poller and HTTP Bridge server.
    """
    def __init__(self) -> None:
        self.http_server: Optional[HttpBridgeServer] = None
        self.poller = DiscordPollingWorker()

    def initialize(self) -> None:
        if config.get("discord.http_bridge_enabled", True):
            host = config.get("discord.http_bridge_host", "127.0.0.1")
            port = int(config.get("discord.http_bridge_port", 8765))
            self.http_server = HttpBridgeServer(host=host, port=port)
            self.http_server.start()

        if config.get("discord.enabled", False):
            self.poller.start()

        config.subscribe("discord", self._on_config_changed)

    def _on_config_changed(self, *args: Any) -> None:
        if config.get("discord.enabled", False):
            self.poller.start()
        else:
            self.poller.stop()

    def shutdown(self) -> None:
        self.poller.stop()
        if self.http_server:
            self.http_server.stop()


# Global client manager singleton
discord_client_manager = DiscordClientManager()
