"""
Main Menu and Tools Menu Integration for Anki Desktop.
Injects the 'Anki Wykiati Toolkit' submenu and global shortcuts into Anki's GUI.
"""

from typing import Optional

try:
    from ..core.config import config
    from ..core.constants import TOOLS_MENU_ENTRY
    from ..core.logger import logger
    from ..theme.engine import theme_engine
    from .about_dialog import AboutDialog
    from .dashboard import DashboardDialog
    from .deck_rules_dialog import DeckRulesDialog
    from .discord_settings import DiscordSettingsDialog
    from .help_dialog import HelpDialog
    from .templates_dialog import TemplatesDialog
    from .theme_settings import ThemeSettingsDialog
except (ImportError, ValueError):
    from core.config import config
    from core.constants import TOOLS_MENU_ENTRY
    from core.logger import logger
    from theme.engine import theme_engine
    from ui.about_dialog import AboutDialog
    from ui.dashboard import DashboardDialog
    from ui.deck_rules_dialog import DeckRulesDialog
    from ui.discord_settings import DiscordSettingsDialog
    from ui.help_dialog import HelpDialog
    from ui.templates_dialog import TemplatesDialog
    from ui.theme_settings import ThemeSettingsDialog

# Qt Imports
try:
    from aqt import mw
    from aqt.qt import QAction, QKeySequence, QMenu
    ANKI_AVAILABLE = True
except ImportError:
    mw = None
    QAction = QKeySequence = QMenu = object
    ANKI_AVAILABLE = False


class ToolkitMenuManager:
    """
    Manages custom submenu items, shortcuts, and dialog openers in Anki's menu bar.
    """
    def __init__(self) -> None:
        self._submenu: Optional[QMenu] = None

    def setup_menu(self) -> None:
        """Create menu items under Anki's 'Tools' menu."""
        if not ANKI_AVAILABLE or mw is None:
            logger.debug("[MenuManager] Anki mw not available. Skipping GUI menu creation.")
            return

        try:
            self._submenu = QMenu(TOOLS_MENU_ENTRY, mw)

            # Dashboard Action
            act_dash = QAction("Dashboard and Metrics...", mw)
            act_dash.setShortcut(QKeySequence("Ctrl+Shift+D"))
            act_dash.triggered.connect(self.show_dashboard)
            self._submenu.addAction(act_dash)

            # Toggle Full Black Theme Quick Action
            act_toggle = QAction("Toggle Full Black Theme", mw)
            act_toggle.setShortcut(QKeySequence("Ctrl+Shift+B"))
            act_toggle.triggered.connect(self.toggle_pure_black_theme)
            self._submenu.addAction(act_toggle)

            self._submenu.addSeparator()

            # Theme Settings Action
            act_theme = QAction("Theme and Appearance Settings...", mw)
            act_theme.triggered.connect(self.show_theme_settings)
            self._submenu.addAction(act_theme)

            # Discord Settings Action
            act_discord = QAction("Discord and Image Settings...", mw)
            act_discord.triggered.connect(self.show_discord_settings)
            self._submenu.addAction(act_discord)

            # Deck Rules Action
            act_rules = QAction("Smart Deck Routing Rules...", mw)
            act_rules.triggered.connect(self.show_deck_rules)
            self._submenu.addAction(act_rules)

            # Templates Action
            act_templates = QAction("Card Template Manager...", mw)
            act_templates.triggered.connect(self.show_templates)
            self._submenu.addAction(act_templates)

            self._submenu.addSeparator()

            # Help Action
            act_help = QAction("Help & Setup Guide...", mw)
            act_help.triggered.connect(self.show_help)
            self._submenu.addAction(act_help)

            # About Action
            act_about = QAction("About Wykiati Toolkit...", mw)
            act_about.triggered.connect(self.show_about)
            self._submenu.addAction(act_about)

            # Add to Tools Menu
            mw.form.menuTools.addMenu(self._submenu)
            logger.info("[MenuManager] Registered 'Anki Wykiati Toolkit' in Tools menu.")

        except Exception as e:
            logger.error(f"[MenuManager] Failed registering menu items: {e}", exc_info=True)

    def show_dashboard(self) -> None:
        if not ANKI_AVAILABLE or mw is None:
            return
        dialog = DashboardDialog(mw)
        dialog.exec()

    def toggle_pure_black_theme(self) -> None:
        current_state = config.get("theme.enabled", True)
        new_state = not current_state
        config.set("theme.enabled", new_state, save=True)
        if new_state:
            theme_engine.activate()
        else:
            theme_engine.deactivate()

    def show_theme_settings(self) -> None:
        if not ANKI_AVAILABLE or mw is None:
            return
        dialog = ThemeSettingsDialog(mw)
        dialog.exec()

    def show_discord_settings(self) -> None:
        if not ANKI_AVAILABLE or mw is None:
            return
        dialog = DiscordSettingsDialog(mw)
        dialog.exec()

    def show_deck_rules(self) -> None:
        if not ANKI_AVAILABLE or mw is None:
            return
        dialog = DeckRulesDialog(mw)
        dialog.exec()

    def show_templates(self) -> None:
        if not ANKI_AVAILABLE or mw is None:
            return
        dialog = TemplatesDialog(mw)
        dialog.exec()

    def show_help(self) -> None:
        if not ANKI_AVAILABLE or mw is None:
            return
        dialog = HelpDialog(mw)
        dialog.exec()

    def show_about(self) -> None:
        if not ANKI_AVAILABLE or mw is None:
            return
        dialog = AboutDialog(mw)
        dialog.exec()


# Global menu manager singleton
menu_manager = ToolkitMenuManager()
