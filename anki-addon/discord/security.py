"""
Security and Authorization Policy for Discord Integration.
Enforces user whitelist, channel whitelist, rate limiting, and input sanitization.
"""

import time
from typing import Dict, List, Optional

try:
    from ..core.config import config
    from ..core.constants import MAX_MESSAGE_CHARACTERS
    from ..core.exceptions import RateLimitExceededError, SecurityError
    from ..core.logger import logger
    from .models import DiscordMessageEvent
except (ImportError, ValueError):
    from core.config import config
    from core.constants import MAX_MESSAGE_CHARACTERS
    from core.exceptions import RateLimitExceededError, SecurityError
    from core.logger import logger
    from discord.models import DiscordMessageEvent


class AuthorizationPolicy:
    """
    Validates incoming events against configured security policies and rate limits.
    """
    def __init__(self) -> None:
        self._user_request_timestamps: Dict[str, List[float]] = {}

    def is_user_authorized(self, user_id: str) -> bool:
        """Check if user ID is in whitelist (or if whitelist is empty)."""
        allowed = config.get("discord.authorized_users", [])
        if not allowed:
            # If no users explicitly restricted, allow
            return True
        return str(user_id) in [str(u) for u in allowed]

    def is_channel_authorized(self, channel_id: str) -> bool:
        """Check if channel ID is in whitelist (or if whitelist is empty)."""
        allowed = config.get("discord.channel_ids", [])
        if not allowed:
            return True
        return str(channel_id) in [str(c) for c in allowed]

    def is_guild_authorized(self, guild_id: str) -> bool:
        """Check if guild ID is in whitelist (or if whitelist is empty)."""
        allowed = config.get("discord.guild_ids", [])
        if not allowed or not guild_id:
            return True
        return str(guild_id) in [str(g) for g in allowed]

    def check_rate_limit(self, user_id: str) -> None:
        """Enforce sliding window rate limit per user."""
        max_per_minute = config.get("discord.rate_limit_per_minute", 60)
        now = time.time()
        window_start = now - 60.0

        if user_id not in self._user_request_timestamps:
            self._user_request_timestamps[user_id] = []

        # Filter timestamps within current 60s window
        timestamps = [t for t in self._user_request_timestamps[user_id] if t > window_start]
        self._user_request_timestamps[user_id] = timestamps

        if len(timestamps) >= max_per_minute:
            logger.warning(f"[Security] User {user_id} exceeded rate limit ({max_per_minute} req/min).")
            raise RateLimitExceededError(f"Rate limit exceeded. Maximum {max_per_minute} cards per minute.")

        self._user_request_timestamps[user_id].append(now)

    def validate_event(self, event: DiscordMessageEvent) -> None:
        """
        Comprehensive security verification of an incoming Discord event.
        Raises SecurityError if authorization checks fail.
        """
        # 1. Payload size check
        if len(event.content) > MAX_MESSAGE_CHARACTERS:
            raise SecurityError(f"Message exceeds maximum character length of {MAX_MESSAGE_CHARACTERS}.")

        # 2. Guild authorization
        if event.channel.guild_id and not self.is_guild_authorized(event.channel.guild_id):
            logger.warning(f"[Security] Rejected event from unauthorized Guild: {event.channel.guild_id}")
            raise SecurityError("Unauthorized Discord server/guild.")

        # 3. Channel authorization
        if event.channel.id and not self.is_channel_authorized(event.channel.id):
            logger.warning(f"[Security] Rejected event from unauthorized Channel: {event.channel.id}")
            raise SecurityError("Unauthorized Discord channel.")

        # 4. User authorization
        if event.author.id and not self.is_user_authorized(event.author.id):
            logger.warning(f"[Security] Rejected event from unauthorized User: {event.author.id} ({event.author})")
            raise SecurityError("Unauthorized user. You do not have permission to create Anki cards.")

        # 5. Rate limiting
        self.check_rate_limit(event.author.id or "anonymous")


# Global policy instance
auth_policy = AuthorizationPolicy()
