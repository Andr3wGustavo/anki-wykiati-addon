"""
UI module exports for Anki Discord Toolkit.
"""

from .about_dialog import AboutDialog
from .dashboard import DashboardDialog
from .deck_rules_dialog import DeckRulesDialog
from .discord_settings import DiscordSettingsDialog
from .menu import ToolkitMenuManager, menu_manager
from .templates_dialog import TemplatesDialog
from .theme_settings import ThemeSettingsDialog

__all__ = [
    "menu_manager",
    "ToolkitMenuManager",
    "DashboardDialog",
    "ThemeSettingsDialog",
    "DiscordSettingsDialog",
    "DeckRulesDialog",
    "TemplatesDialog",
    "AboutDialog",
]
