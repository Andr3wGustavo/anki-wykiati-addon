"""
Minimal Discord REST client (stdlib only) used by the poller and the settings panel.

- Sends the User-Agent format Discord requires for bots.
- Honors HTTP 429 rate limits (waits `retry_after` and retries).
- Raises DiscordApiError with a human-readable message for common failures.
"""

import json
import time
import urllib.error
import urllib.parse
import urllib.request
from typing import Any, Dict, List, Optional

try:
    from ..core.constants import ADDON_VERSION
except (ImportError, ValueError):
    from core.constants import ADDON_VERSION

API_BASE = "https://discord.com/api/v10"
USER_AGENT = f"DiscordBot (https://github.com/Andr3wGustavo/anki-wykiati-addon, {ADDON_VERSION})"
MAX_RATE_LIMIT_WAIT = 30.0


class DiscordApiError(Exception):
    def __init__(self, status: int, message: str) -> None:
        super().__init__(message)
        self.status = status
        self.message = message


_FRIENDLY = {
    401: "Invalid bot token (401). Copy the token again from the Discord Developer Portal → Bot.",
    403: "The bot cannot read this channel (403). Invite it to the server and give it "
         "'View Channel' and 'Read Message History' permissions.",
    404: "Channel not found (404). Check the channel ID (right-click the channel → Copy Channel ID).",
}


def request(method: str, path: str, token: str, params: Optional[Dict[str, Any]] = None,
            body: Optional[Dict[str, Any]] = None, timeout: float = 12.0, max_retries: int = 3) -> Any:
    url = API_BASE + path
    if params:
        url += "?" + urllib.parse.urlencode({k: v for k, v in params.items() if v is not None})
    data = json.dumps(body).encode("utf-8") if body is not None else None

    for attempt in range(max_retries + 1):
        req = urllib.request.Request(url, data=data, method=method, headers={
            "Authorization": f"Bot {token}",
            "User-Agent": USER_AGENT,
            "Content-Type": "application/json",
        })
        try:
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                raw = resp.read()
                return json.loads(raw.decode("utf-8")) if raw else None
        except urllib.error.HTTPError as e:
            if e.code == 429 and attempt < max_retries:
                retry_after = 1.0
                try:
                    retry_after = float(json.loads(e.read().decode("utf-8")).get("retry_after", 1.0))
                except Exception:
                    header = e.headers.get("Retry-After") if e.headers else None
                    if header:
                        try:
                            retry_after = float(header)
                        except ValueError:
                            pass
                time.sleep(min(MAX_RATE_LIMIT_WAIT, max(0.5, retry_after)))
                continue
            raise DiscordApiError(e.code, _FRIENDLY.get(e.code, f"Discord API error {e.code}: {e.reason}"))
        except urllib.error.URLError as e:
            raise DiscordApiError(0, f"Network error while contacting Discord: {e.reason}")
    raise DiscordApiError(429, "Discord rate limit: too many requests, try again shortly.")


def get_me(token: str) -> Dict[str, Any]:
    return request("GET", "/users/@me", token)


def get_channel(token: str, channel_id: str) -> Dict[str, Any]:
    return request("GET", f"/channels/{channel_id}", token)


def get_messages(token: str, channel_id: str, after: Optional[str] = None,
                 before: Optional[str] = None, limit: int = 100) -> List[Dict[str, Any]]:
    params = {"limit": max(1, min(100, int(limit))), "after": after, "before": before}
    result = request("GET", f"/channels/{channel_id}/messages", token, params=params)
    return result if isinstance(result, list) else []


def snowflake(value: Any) -> int:
    try:
        return int(str(value))
    except (TypeError, ValueError):
        return 0
