"""
Unit tests for ConfigManager.
"""

import os
import sys
import unittest

# Ensure path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.config import ConfigManager, DEFAULT_CONFIG


class TestConfigManager(unittest.TestCase):
    def setUp(self):
        self.config = ConfigManager()

    def test_default_values(self):
        self.assertTrue(self.config.get("addon_enabled"))
        self.assertEqual(self.config.get("theme.background"), "#000000")
        self.assertEqual(self.config.get("anki.default_deck"), "Default")
        self.assertEqual(self.config.get("discord.http_bridge_port"), 8765)

    def test_dot_notation_get_and_set(self):
        self.config.set("theme.accent", "#10B981", save=False)
        self.assertEqual(self.config.get("theme.accent"), "#10B981")

        self.config.set("custom.nested.key", 42, save=False)
        self.assertEqual(self.config.get("custom.nested.key"), 42)
        self.assertIsNone(self.config.get("nonexistent.key"))
        self.assertEqual(self.config.get("nonexistent.key", "fallback"), "fallback")

    def test_reactive_subscriber(self):
        changed_values = []

        def on_change(val):
            changed_values.append(val)

        self.config.subscribe("theme.accent", on_change)
        self.config.set("theme.accent", "#EF4444", save=False)
        self.config.set("theme.accent", "#F59E0B", save=False)

        self.assertEqual(changed_values, ["#EF4444", "#F59E0B"])

    def test_reset_to_defaults(self):
        self.config.set("theme.background", "#FFFFFF", save=False)
        self.assertEqual(self.config.get("theme.background"), "#FFFFFF")

        self.config.reset_to_defaults()
        self.assertEqual(self.config.get("theme.background"), "#000000")


if __name__ == "__main__":
    unittest.main()
