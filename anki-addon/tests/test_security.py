"""
Unit tests for Security and AuthorizationPolicy.
"""

import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.config import config
from core.exceptions import RateLimitExceededError, SecurityError
from discord.models import DiscordChannel, DiscordMessageEvent, DiscordUser
from discord.security import AuthorizationPolicy


class TestSecurityPolicy(unittest.TestCase):
    def setUp(self):
        self.auth = AuthorizationPolicy()
        config.reset_to_defaults()

    def test_user_whitelist(self):
        # Empty whitelist allows all
        config.set("discord.authorized_users", [], save=False)
        self.assertTrue(self.auth.is_user_authorized("any_user_123"))

        # Explicit whitelist
        config.set("discord.authorized_users", ["user_allowed_1", "user_allowed_2"], save=False)
        self.assertTrue(self.auth.is_user_authorized("user_allowed_1"))
        self.assertFalse(self.auth.is_user_authorized("hacker_999"))

    def test_channel_whitelist(self):
        config.set("discord.channel_ids", ["chan_1", "chan_2"], save=False)
        self.assertTrue(self.auth.is_channel_authorized("chan_1"))
        self.assertFalse(self.auth.is_channel_authorized("chan_unauthorized"))

    def test_rate_limiting(self):
        config.set("discord.rate_limit_per_minute", 3, save=False)
        user = "spammer_user"

        # 3 calls should pass
        self.auth.check_rate_limit(user)
        self.auth.check_rate_limit(user)
        self.auth.check_rate_limit(user)

        # 4th call within same window should raise RateLimitExceededError
        with self.assertRaises(RateLimitExceededError):
            self.auth.check_rate_limit(user)

    def test_full_event_validation_rejection(self):
        config.set("discord.authorized_users", ["vip_user"], save=False)
        event = DiscordMessageEvent(
            id="1",
            content="!anki\nfront: test\nback: test",
            author=DiscordUser(id="unauthorized_user", name="Eve"),
            channel=DiscordChannel(id="chan_1"),
        )
        with self.assertRaises(SecurityError):
            self.auth.validate_event(event)


if __name__ == "__main__":
    unittest.main()
