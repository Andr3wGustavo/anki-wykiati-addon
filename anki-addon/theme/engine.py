"""
Theme Engine for Pure Black (#000000) AMOLED Theme.
Controls Qt application stylesheets and Webview CSS injection hooks.
"""

from typing import Any, Optional

try:
    from ..core.config import config
    from ..core.logger import logger
    from .palette import PALETTE, ThemePalette
    from .styles import generate_qss, generate_webview_css
except (ImportError, ValueError):
    from core.config import config
    from core.logger import logger
    from theme.palette import PALETTE, ThemePalette
    from theme.styles import generate_qss, generate_webview_css

# Check Anki & GUI availability
try:
    from aqt import gui_hooks, mw
    from aqt.qt import QApplication
    ANKI_AVAILABLE = True
except ImportError:
    gui_hooks = mw = QApplication = None
    ANKI_AVAILABLE = False


class ThemeEngine:
    """
    Manages activation, deactivation, and real-time styling updates for Anki.
    """
    def __init__(self) -> None:
        self._is_active = False
        self._hook_registered = False
        self._palette = PALETTE
        self._original_stylesheet: Optional[str] = None

    def initialize(self) -> None:
        """Initialize theme based on configuration and subscribe to settings changes."""
        config.subscribe("theme", self._on_config_changed)
        config.subscribe("theme.enabled", self._on_config_changed)
        config.subscribe("theme.accent", self._on_config_changed)

        if config.get("theme.enabled", True):
            self.activate()

    def _on_config_changed(self, *args: Any) -> None:
        """Handle dynamic theme setting updates."""
        if config.get("theme.enabled", True):
            self.activate()
        else:
            self.deactivate()

    def activate(self) -> None:
        """Activate Pure Black theme across Qt widgets and WebViews."""
        if not ANKI_AVAILABLE or mw is None:
            self._is_active = True
            logger.info("[ThemeEngine] Pure Black theme active (Headless/Mock mode).")
            return

        try:
            accent = config.get("theme.accent", self._palette.ACCENT_PRIMARY)
            qss = generate_qss(self._palette, accent=accent)

            # Store original stylesheet on first activation
            if self._original_stylesheet is None:
                self._original_stylesheet = mw.styleSheet() or ""

            # Apply QSS to Anki's main window and global app instance
            mw.setStyleSheet(qss)
            app = QApplication.instance()
            if app:
                app.setStyleSheet(qss)

            # Register Webview hook if enabled
            if config.get("theme.apply_to_webviews", True) and not self._hook_registered:
                try:
                    if hasattr(gui_hooks, "webview_will_set_content"):
                        gui_hooks.webview_will_set_content.append(self._on_webview_will_set_content)
                        self._hook_registered = True
                except Exception as e:
                    logger.warning(f"[ThemeEngine] Could not register webview hook: {e}")

            # Refresh active webviews if possible
            self._refresh_views()

            self._is_active = True
            logger.info("[ThemeEngine] Pure Black AMOLED Theme activated successfully.")

        except Exception as e:
            logger.error(f"[ThemeEngine] Failed activating theme: {e}", exc_info=True)

    def deactivate(self) -> None:
        """Restore standard Anki appearance."""
        if not ANKI_AVAILABLE or mw is None:
            self._is_active = False
            return

        try:
            # Restore original stylesheet
            restore_qss = self._original_stylesheet or ""
            mw.setStyleSheet(restore_qss)
            app = QApplication.instance()
            if app:
                app.setStyleSheet(restore_qss)

            # Remove webview hook
            if self._hook_registered:
                try:
                    if hasattr(gui_hooks, "webview_will_set_content"):
                        if self._on_webview_will_set_content in gui_hooks.webview_will_set_content:
                            gui_hooks.webview_will_set_content.remove(self._on_webview_will_set_content)
                    self._hook_registered = False
                except Exception as e:
                    logger.warning(f"[ThemeEngine] Could not unregister webview hook: {e}")

            self._refresh_views()
            self._is_active = False
            logger.info("[ThemeEngine] Pure Black AMOLED Theme deactivated.")

        except Exception as e:
            logger.error(f"[ThemeEngine] Error deactivating theme: {e}", exc_info=True)

    def _on_webview_will_set_content(self, web_content: Any, context: Optional[Any] = None) -> None:
        """Inject pure black CSS directly into Anki WebViews (DeckBrowser, Reviewer, etc.)."""
        if not self._is_active:
            return

        try:
            accent = config.get("theme.accent", self._palette.ACCENT_PRIMARY)
            css = generate_webview_css(self._palette, accent=accent)
            web_content.css.append(css)
        except Exception as e:
            logger.error(f"[ThemeEngine] Failed injecting webview CSS: {e}")

    def _refresh_views(self) -> None:
        """Trigger redraw of main window views."""
        try:
            if hasattr(mw, "reset"):
                mw.reset()
            elif hasattr(mw, "deckBrowser") and hasattr(mw.deckBrowser, "refresh"):
                mw.deckBrowser.refresh()
        except Exception:
            pass

    def is_active(self) -> bool:
        return self._is_active


# Global theme engine singleton
theme_engine = ThemeEngine()
