"""
Unit Tests for UI Dialogs and Components in Headless Mode.
"""

import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ui.about_dialog import AboutDialog
from ui.components.base_dialog import BaseToolkitDialog
from ui.dashboard import DashboardDialog
from ui.deck_rules_dialog import DeckRulesDialog
from ui.discord_settings import DiscordSettingsDialog
from ui.help_dialog import HelpDialog
from ui.templates_dialog import TemplatesDialog
from ui.theme_settings import RGBWheelWidget, ThemeSettingsDialog


class TestUIDialogs(unittest.TestCase):
    def test_dialog_instantiations(self):
        """Verify all dialog classes instantiate cleanly without NameError or TypeError."""
        for cls in [
            BaseToolkitDialog,
            AboutDialog,
            DashboardDialog,
            DeckRulesDialog,
            DiscordSettingsDialog,
            HelpDialog,
            TemplatesDialog,
            ThemeSettingsDialog,
        ]:
            dlg = cls()
            self.assertIsNotNone(dlg)

    def test_rgb_wheel_widget_instantiation(self):
        """Verify RGBWheelWidget instantiates cleanly."""
        wheel = RGBWheelWidget(initial_hex="#000000")
        self.assertIsNotNone(wheel)
        self.assertEqual(wheel._current_hex, "#000000")
        wheel.set_color_hex("#0A84FF")
        self.assertEqual(wheel._current_hex, "#0A84FF")


if __name__ == "__main__":
    unittest.main()
