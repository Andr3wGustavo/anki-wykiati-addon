"""
Discord Client and Local HTTP Webhook Bridge Server.
Cards arrive via the Discord poller (image channels fed by webhooks, or !anki text
commands) or via the local HTTP bridge.
"""

import hmac
import http.server
import json
import os
import socketserver
import threading
import time
from typing import Any, Dict, List, Optional

try:
    from ..core.config import config
    from ..core.constants import ADDON_NAME, ADDON_VERSION, MAX_PAYLOAD_SIZE_BYTES
    from ..core.image_urls import extract_image_urls
    from ..core.logger import logger
    from ..core.paths import user_file
    from . import api
    from .bridge import discord_bridge
    from .models import DiscordAttachment, DiscordChannel, DiscordMessageEvent, DiscordUser
except (ImportError, ValueError):
    from core.config import config
    from core.constants import ADDON_NAME, ADDON_VERSION, MAX_PAYLOAD_SIZE_BYTES
    from core.image_urls import extract_image_urls
    from core.logger import logger
    from core.paths import user_file
    from discord import api
    from discord.bridge import discord_bridge
    from discord.models import DiscordAttachment, DiscordChannel, DiscordMessageEvent, DiscordUser


_ALLOWED_HOSTNAMES = {"127.0.0.1", "localhost", "::1", "[::1]"}
DISCORD_STATE_FILENAME = "discord_state.json"


def _get_secret_token() -> str:
    return str(config.get("discord.secret_token", "") or "").strip()


class _BridgeHTTPRequestHandler(http.server.BaseHTTPRequestHandler):
    """Handles incoming HTTP POST / GET webhook requests.

    Security model:
    - Every POST must carry the configured secret token
      (``Authorization: Bearer <token>`` or ``X-AWT-Token: <token>``).
    - No CORS headers are sent, so browser pages cannot read responses.
    - The Host header must point at the loopback interface (DNS-rebinding guard).
    """

    def log_message(self, format: str, *args: Any) -> None:
        logger.debug(f"[HttpBridge] {self.client_address[0]} - {format % args}")

    def _send_json(self, status_code: int, data: Dict[str, Any]) -> None:
        body = json.dumps(data, indent=2).encode("utf-8")
        self.send_response(status_code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("X-Content-Type-Options", "nosniff")
        self.end_headers()
        self.wfile.write(body)

    def _host_is_allowed(self) -> bool:
        host_header = (self.headers.get("Host") or "").strip().lower()
        if not host_header:
            return False
        if host_header.startswith("["):
            hostname = host_header.split("]")[0] + "]"
        else:
            hostname = host_header.rsplit(":", 1)[0] if ":" in host_header else host_header
        configured = str(config.get("discord.http_bridge_host", "127.0.0.1")).strip().lower()
        return hostname in _ALLOWED_HOSTNAMES or hostname == configured

    def _is_authorized(self) -> bool:
        expected = _get_secret_token()
        if not expected:
            return False
        provided = ""
        auth_header = (self.headers.get("Authorization") or "").strip()
        if auth_header.lower().startswith("bearer "):
            provided = auth_header[7:].strip()
        if not provided:
            provided = (self.headers.get("X-AWT-Token") or "").strip()
        return bool(provided) and hmac.compare_digest(provided.encode("utf-8"), expected.encode("utf-8"))

    def do_OPTIONS(self) -> None:
        # Cross-origin requests are intentionally not supported.
        self._send_json(405, {"error": "Method Not Allowed"})

    def do_GET(self) -> None:
        if not self._host_is_allowed():
            self._send_json(403, {"error": "Forbidden host"})
            return
        if self.path in ("/", "/health", "/api/health"):
            data: Dict[str, Any] = {"status": "healthy"}
            if self._is_authorized():
                data.update({
                    "addon": ADDON_NAME,
                    "version": ADDON_VERSION,
                    "stats": config.get("stats", {}),
                })
            self._send_json(200, data)
        else:
            self._send_json(404, {"error": "Not Found"})

    def do_POST(self) -> None:
        try:
            try:
                content_length = int(self.headers.get("Content-Length", 0))
            except (TypeError, ValueError):
                self.close_connection = True
                self._send_json(400, {"success": False, "error": "Invalid Content-Length"})
                return
            if content_length < 0 or content_length > MAX_PAYLOAD_SIZE_BYTES:
                self.close_connection = True
                self._send_json(413, {"success": False, "error": "Payload too large"})
                return

            # Consume the (bounded) body before answering, even when rejecting:
            # replying with unread data in the socket makes Windows reset the
            # connection before the client can read the status code.
            body_bytes = self.rfile.read(content_length)

            if not self._host_is_allowed():
                self._send_json(403, {"success": False, "error": "Forbidden host"})
                return

            if not _get_secret_token():
                self._send_json(503, {
                    "success": False,
                    "error": "HTTP bridge is locked: set 'discord.secret_token' in the add-on config.",
                })
                return

            if not self._is_authorized():
                self._send_json(401, {"success": False, "error": "Unauthorized"})
                return

            body_str = body_bytes.decode("utf-8", errors="replace")

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
            self._send_json(500, {"success": False, "error": "Internal error"})


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
    Background poller for Discord channels (REST, no external dependencies).

    Image channels (e.g. a Pinterest → Discord webhook):
    - accepts webhook/bot authors (except this bot itself);
    - reads images from attachments AND embeds;
    - remembers the last processed message per channel in user_files, and on each
      cycle fetches everything *after* it (paginated), so posts made while Anki was
      closed are imported on the next start;
    - stays silent (no replies in the channel).

    Command channels (`discord.channel_ids`) keep the `!anki` text workflow and
    still ignore other bots.
    """

    MAX_PAGES_PER_CYCLE = 10       # up to 1000 messages per channel per cycle
    MAX_DOWNLOAD_RETRIES = 3       # transient download failures before giving up on a message
    MESSAGE_TYPES = (0, 19)        # DEFAULT, REPLY

    def __init__(self) -> None:
        self._running = False
        self._thread: Optional[threading.Thread] = None
        self._stop_event = threading.Event()
        self._state_lock = threading.RLock()
        self._state: Dict[str, str] = {}
        self._state_loaded = False
        self._bot_user_id: Optional[str] = None
        self._retry_counts: Dict[str, int] = {}
        self._empty_streak: Dict[str, int] = {}
        self._intent_warned: set = set()
        self._last_error: str = ""
        self.status: Dict[str, Any] = {"last_poll": 0.0, "last_error": "", "imported": 0}

    # --------------------------------------------------------------- state

    def _state_path(self) -> str:
        return user_file(DISCORD_STATE_FILENAME)

    def _load_state(self) -> None:
        with self._state_lock:
            if self._state_loaded:
                return
            path = self._state_path()
            if os.path.exists(path):
                try:
                    with open(path, "r", encoding="utf-8") as f:
                        data = json.load(f)
                    self._state = {str(k): str(v) for k, v in data.get("last_message_ids", {}).items()}
                except Exception as e:
                    logger.error(f"[DiscordPoller] Could not read sync state: {e}")
            self._state_loaded = True

    def _save_state(self) -> None:
        with self._state_lock:
            path = self._state_path()
            try:
                tmp = path + ".tmp"
                with open(tmp, "w", encoding="utf-8") as f:
                    json.dump({"last_message_ids": self._state}, f)
                os.replace(tmp, path)
            except Exception as e:
                logger.error(f"[DiscordPoller] Could not save sync state: {e}")

    def get_last_id(self, channel_id: str) -> Optional[str]:
        self._load_state()
        with self._state_lock:
            return self._state.get(channel_id)

    def _set_last_id(self, channel_id: str, message_id: str) -> None:
        with self._state_lock:
            if api.snowflake(message_id) >= api.snowflake(self._state.get(channel_id, "0")):
                self._state[channel_id] = str(message_id)
        self._save_state()

    # ------------------------------------------------------------ channels

    @staticmethod
    def _clean_ids(values: Any) -> List[str]:
        out: List[str] = []
        for v in values or []:
            clean = str(v).strip()
            if clean and clean not in out:
                out.append(clean)
        return out

    def _image_channels(self) -> List[str]:
        return self._clean_ids(config.get("discord.image_channels", []))

    def _get_target_channels(self) -> List[str]:
        combined = self._image_channels()
        for c in self._clean_ids(config.get("discord.channel_ids", [])):
            if c not in combined:
                combined.append(c)
        return combined

    # ----------------------------------------------------------- lifecycle

    def start(self) -> None:
        bot_token = str(config.get("discord.bot_token", "") or "").strip()
        channels = self._get_target_channels()
        if not bot_token or not channels:
            logger.info("[DiscordPoller] Bot token or channel IDs missing. Poller idle.")
            return

        if self._thread is not None and self._thread.is_alive():
            # Re-arm a thread that is still finishing its last request instead of starting a second one
            self._running = True
            self._stop_event.clear()
            return

        self._load_state()
        self._running = True
        self._stop_event.clear()
        self._thread = threading.Thread(target=self._poll_loop, name="AWT-DiscordPoller", daemon=True)
        self._thread.start()
        logger.info(f"[DiscordPoller] Polling started for {len(channels)} channel(s).")

    def stop(self) -> None:
        if not self._running:
            return
        self._running = False
        self._stop_event.set()
        if self._thread and self._thread.is_alive():
            self._thread.join(timeout=2.0)
        logger.info("[DiscordPoller] Polling stopped.")

    def is_running(self) -> bool:
        return self._running and self._thread is not None and self._thread.is_alive()

    def _report_error(self, message: str) -> None:
        self.status["last_error"] = message
        if message != self._last_error:  # avoid flooding the log every cycle
            logger.warning(f"[DiscordPoller] {message}")
            self._last_error = message

    def _poll_loop(self) -> None:
        while not self._stop_event.is_set():
            interval = max(3, int(config.get("discord.polling_interval_seconds", 5) or 5))
            token = str(config.get("discord.bot_token", "") or "").strip()
            channels = self._get_target_channels()

            if not token or not channels:
                self._stop_event.wait(timeout=interval)
                continue

            try:
                if self._bot_user_id is None:
                    me = api.get_me(token)
                    self._bot_user_id = str(me.get("id", ""))
                    logger.info(f"[DiscordPoller] Connected as bot '{me.get('username', '?')}'.")

                cycle_ok = True
                for channel_id in channels:
                    if self._stop_event.is_set():
                        break
                    try:
                        self.poll_channel(channel_id, token)
                    except api.DiscordApiError as e:
                        cycle_ok = False
                        self._report_error(f"Channel {channel_id}: {e.message}")

                self.status["last_poll"] = time.time()
                if cycle_ok and not self._intent_warned:
                    if self._last_error:
                        logger.info("[DiscordPoller] Connection healthy again.")
                    self.status["last_error"] = ""
                    self._last_error = ""
            except api.DiscordApiError as e:
                self._report_error(e.message)
                if e.status == 401:
                    self._bot_user_id = None
                    self._stop_event.wait(timeout=60)
                    continue
            except Exception as e:
                logger.error(f"[DiscordPoller] Unexpected polling error: {e}", exc_info=True)

            self._stop_event.wait(timeout=interval)

    def poll_channel(self, channel_id: str, token: str) -> int:
        """Process every message after the last one seen. Returns how many were handled."""
        last_id = self.get_last_id(channel_id)

        if last_id is None:
            # First run for this channel: start from "now". Older images can be pulled
            # explicitly with "Import existing images" in the settings panel.
            latest = api.get_messages(token, channel_id, limit=1)
            baseline = str(latest[0]["id"]) if latest else "0"
            self._set_last_id(channel_id, baseline)
            logger.info(f"[DiscordPoller] Channel {channel_id}: tracking new messages from now on.")
            return 0

        handled = 0
        for _ in range(self.MAX_PAGES_PER_CYCLE):
            messages = api.get_messages(token, channel_id, after=last_id, limit=100)
            if not messages:
                break
            messages.sort(key=lambda m: api.snowflake(m.get("id")))
            for msg in messages:
                if self._stop_event.is_set():
                    return handled
                result = self.handle_message(channel_id, msg, token)
                if result == "retry":
                    return handled  # keep last_id: this message is retried next cycle
                last_id = str(msg.get("id"))
                self._set_last_id(channel_id, last_id)
                handled += 1
            if len(messages) < 100:
                break
        return handled

    # ------------------------------------------------------------- messages

    def handle_message(self, channel_id: str, msg: Dict[str, Any], token: str, backfill: bool = False) -> str:
        """
        Turn one raw Discord message into card jobs.
        Returns "ok" (handled/ignored, advance) or "retry" (transient failure, do not advance).
        """
        msg_id = str(msg.get("id", ""))
        author = msg.get("author") or {}
        author_id = str(author.get("id", ""))
        is_webhook = bool(msg.get("webhook_id"))
        is_image_channel = channel_id in self._image_channels()

        if msg.get("type", 0) not in self.MESSAGE_TYPES:
            return "ok"
        if self._bot_user_id and author_id == self._bot_user_id:
            return "ok"  # our own replies
        if author.get("bot") and not is_webhook and not is_image_channel:
            return "ok"

        content = msg.get("content") or ""
        image_urls = extract_image_urls(msg)

        if is_image_channel:
            if not image_urls:
                self._track_possibly_hidden_content(channel_id, msg)
                return "ok"
            self._empty_streak[channel_id] = 0
        elif not content.strip() and not image_urls:
            return "ok"

        attachments = [
            DiscordAttachment(
                id=str(a.get("id")),
                url=str(a.get("url")),
                filename=str(a.get("filename", "image.png")),
                content_type=str(a.get("content_type", "")),
                size=int(a.get("size", 0) or 0),
            )
            for a in (msg.get("attachments") or [])
        ]
        event = DiscordMessageEvent(
            id=msg_id,
            content=content,
            author=DiscordUser(id=author_id, name=author.get("username", "Unknown"),
                               discriminator=author.get("discriminator", "") if author.get("discriminator") != "0" else ""),
            channel=DiscordChannel(id=channel_id, guild_id=str(msg.get("guild_id", "") or "")),
            attachments=attachments,
            timestamp=time.time(),
            image_urls=image_urls,
            is_webhook=is_webhook,
        )

        success, reply = discord_bridge.handle_incoming_message(content, event)

        if is_image_channel:
            if success:
                self.status["imported"] = self.status.get("imported", 0) + 1
                self._retry_counts.pop(msg_id, None)
                return "ok"
            if reply.startswith("Failed to download") and not backfill:
                attempts = self._retry_counts.get(msg_id, 0) + 1
                self._retry_counts[msg_id] = attempts
                if attempts < self.MAX_DOWNLOAD_RETRIES:
                    logger.warning(f"[DiscordPoller] {reply} (message {msg_id}, attempt {attempts}); will retry.")
                    return "retry"
                logger.error(f"[DiscordPoller] Giving up on message {msg_id} after {attempts} attempts: {reply}")
                self._retry_counts.pop(msg_id, None)
            return "ok"

        if success and reply and config.get("discord.reply_in_channel", True):
            self._send_discord_reply(channel_id, msg_id, reply, token)
        return "ok"

    def _track_possibly_hidden_content(self, channel_id: str, msg: Dict[str, Any]) -> None:
        """Without the Message Content intent, Discord sends messages with no content/embeds/attachments."""
        if msg.get("content") or msg.get("embeds") or msg.get("attachments"):
            self._empty_streak[channel_id] = 0
            return
        streak = self._empty_streak.get(channel_id, 0) + 1
        self._empty_streak[channel_id] = streak
        if streak >= 3 and channel_id not in self._intent_warned:
            self._intent_warned.add(channel_id)
            self._report_error(
                "Messages arrive empty. Enable 'Message Content Intent' in the Discord Developer "
                "Portal → your app → Bot → Privileged Gateway Intents."
            )

    def _send_discord_reply(self, channel_id: str, message_id: str, text: str, bot_token: str) -> None:
        try:
            api.request("POST", f"/channels/{channel_id}/messages", bot_token,
                        body={"content": text[:1900], "message_reference": {"message_id": message_id}},
                        timeout=8, max_retries=1)
        except api.DiscordApiError as e:
            logger.debug(f"[DiscordPoller] Failed sending Discord reply: {e.message}")

    # -------------------------------------------------------- user actions

    def import_history(self, channel_id: str, token: str, limit: int = 100) -> Dict[str, Any]:
        """
        Backfill: import images from the most recent `limit` messages of a channel
        (oldest first). Already imported messages/images are skipped by dedup.
        Runs on a background thread; never touches the collection directly.
        """
        channel_id = str(channel_id).strip()
        limit = max(1, min(1000, int(limit)))
        if self._bot_user_id is None:
            self._bot_user_id = str(api.get_me(token).get("id", ""))

        collected: List[Dict[str, Any]] = []
        before: Optional[str] = None
        while len(collected) < limit:
            page = api.get_messages(token, channel_id, before=before, limit=min(100, limit - len(collected)))
            if not page:
                break
            collected.extend(page)
            before = str(min(api.snowflake(m.get("id")) for m in page))
            if len(page) < 100:
                break

        collected.sort(key=lambda m: api.snowflake(m.get("id")))
        before_count = self.status.get("imported", 0)
        with_images = 0
        for msg in collected:
            if extract_image_urls(msg):
                with_images += 1
            self.handle_message(channel_id, msg, token, backfill=True)
        imported = self.status.get("imported", 0) - before_count

        # Make sure the live poller continues after the newest message we just saw
        if collected and channel_id in self._image_channels():
            newest = str(collected[-1]["id"])
            if self.get_last_id(channel_id) is None or api.snowflake(newest) > api.snowflake(self.get_last_id(channel_id)):
                self._set_last_id(channel_id, newest)

        return {
            "scanned": len(collected),
            "with_images": with_images,
            "imported": imported,
            "skipped": max(0, with_images - imported),
        }


def test_discord_connection(token: str, channel_id: str) -> Dict[str, Any]:
    """
    Check token, channel access and whether message content is visible.
    Returns {"ok": bool, "lines": [str, ...]} — safe to call from a background thread.
    """
    lines: List[str] = []
    token = (token or "").strip()
    channel_id = (channel_id or "").strip()
    if not token:
        return {"ok": False, "lines": ["Bot token is empty."]}
    if not channel_id:
        return {"ok": False, "lines": ["Channel ID is empty."]}
    try:
        me = api.get_me(token)
        lines.append(f"✓ Bot: {me.get('username', '?')}")
        channel = api.get_channel(token, channel_id)
        lines.append(f"✓ Channel: #{channel.get('name', channel_id)}")
        messages = api.get_messages(token, channel_id, limit=20)
    except api.DiscordApiError as e:
        return {"ok": False, "lines": lines + [f"✗ {e.message}"]}

    if not messages:
        lines.append("• The channel has no messages yet — post an image to test.")
        return {"ok": True, "lines": lines}

    images = sum(1 for m in messages if extract_image_urls(m))
    webhook_msgs = sum(1 for m in messages if m.get("webhook_id"))
    blank = sum(1 for m in messages if not (m.get("content") or m.get("embeds") or m.get("attachments")))
    lines.append(f"✓ Last {len(messages)} messages: {images} with images ({webhook_msgs} from webhooks)")
    if blank == len(messages):
        lines.append("✗ All messages arrive empty: enable 'Message Content Intent' "
                     "(Developer Portal → Bot → Privileged Gateway Intents).")
        return {"ok": False, "lines": lines}
    return {"ok": True, "lines": lines}


class DiscordClientManager:
    """
    Controls lifetime of Discord Poller and HTTP Bridge server.
    """
    def __init__(self) -> None:
        self.http_server: Optional[HttpBridgeServer] = None
        self.poller = DiscordPollingWorker()

    def initialize(self) -> None:
        if config.get("discord.http_bridge_enabled", False):
            if not _get_secret_token():
                logger.warning(
                    "[DiscordClientManager] HTTP bridge is enabled but 'discord.secret_token' is empty. "
                    "Refusing to start an unauthenticated server."
                )
            else:
                host = config.get("discord.http_bridge_host", "127.0.0.1")
                port = int(config.get("discord.http_bridge_port", 8765))
                self.http_server = HttpBridgeServer(host=host, port=port)
                self.http_server.start()

        if config.get("discord.enabled", False):
            self.poller.start()

        config.subscribe("discord", self._on_config_changed)

    def shutdown(self) -> None:
        """Stop the Discord poller and the HTTP bridge (called when the profile closes)."""
        try:
            config.unsubscribe("discord", self._on_config_changed)
        except Exception:
            pass
        self.poller.stop()
        if self.http_server is not None:
            self.http_server.stop()
            self.http_server = None

    def _on_config_changed(self, *args: Any) -> None:
        if config.get("discord.enabled", False):
            self.poller.start()
        else:
            self.poller.stop()

    def import_history(self, channel_id: str, limit: int = 100, token: Optional[str] = None) -> Dict[str, Any]:
        token = (token or str(config.get("discord.bot_token", "") or "")).strip()
        try:
            result = self.poller.import_history(channel_id, token, limit)
        except api.DiscordApiError as e:
            return {"success": False, "error": e.message}
        result["success"] = True
        return result


# Global client manager singleton
discord_client_manager = DiscordClientManager()
