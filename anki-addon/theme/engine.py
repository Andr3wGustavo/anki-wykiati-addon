"""
Theme Engine for Full Black (#000000) Void & Floating Glass Aesthetic.
Controls Qt application stylesheets and injects high-priority CSS & JS into all Anki WebViews:
- Top Toolbar (Decks, Add, Browse, Stats, Sync)
- Deck Browser (Middle Area)
- Card Reviewer (Centered Card, Centered Image & Question/Answer)
- Bottom Bar (Floating Answer Buttons)
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
    from aqt.qt import QApplication, QColor, QPalette
    ANKI_AVAILABLE = True
except ImportError:
    gui_hooks = mw = QApplication = QColor = QPalette = None
    ANKI_AVAILABLE = False


try:
    from .logo_data import LOGO_PNG_BASE64
except (ImportError, ValueError):
    try:
        from theme.logo_data import LOGO_PNG_BASE64
    except ImportError:
        LOGO_PNG_BASE64 = ""


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
        """Activate Full Black #000000 theme across Qt widgets and WebViews."""
        if not ANKI_AVAILABLE or mw is None:
            self._is_active = True
            logger.info("[ThemeEngine] Full Black theme active (Headless/Mock mode).")
            return

        try:
            accent = config.get("theme.accent", self._palette.ACCENT_PRIMARY)
            qss = generate_qss(self._palette, accent=accent)

            # Store original stylesheet on first activation
            if self._original_stylesheet is None:
                self._original_stylesheet = mw.styleSheet() or ""

            # 1. Apply QSS to Anki's main window and global app instance
            mw.setStyleSheet(qss)
            app = QApplication.instance()
            if app:
                app.setStyleSheet(qss)
                # Force Qt dark palette for native frames
                if QPalette is not None and QColor is not None:
                    palette = QPalette()
                    palette.setColor(QPalette.ColorRole.Window, QColor("#000000"))
                    palette.setColor(QPalette.ColorRole.WindowText, QColor("#FFFFFF"))
                    palette.setColor(QPalette.ColorRole.Base, QColor("#000000"))
                    palette.setColor(QPalette.ColorRole.AlternateBase, QColor("#08080A"))
                    palette.setColor(QPalette.ColorRole.ToolTipBase, QColor("#121214"))
                    palette.setColor(QPalette.ColorRole.ToolTipText, QColor("#FFFFFF"))
                    palette.setColor(QPalette.ColorRole.Text, QColor("#FFFFFF"))
                    palette.setColor(QPalette.ColorRole.Button, QColor("#0D0D10"))
                    palette.setColor(QPalette.ColorRole.ButtonText, QColor("#FFFFFF"))
                    palette.setColor(QPalette.ColorRole.BrightText, QColor("#FFFFFF"))
                    palette.setColor(QPalette.ColorRole.Highlight, QColor(accent))
                    palette.setColor(QPalette.ColorRole.HighlightedText, QColor("#000000"))
                    app.setPalette(palette)

            # 2. Register Webview hooks
            if config.get("theme.apply_to_webviews", True) and not self._hook_registered:
                try:
                    if hasattr(gui_hooks, "webview_will_set_content"):
                        gui_hooks.webview_will_set_content.append(self._on_webview_will_set_content)
                        self._hook_registered = True
                except Exception as e:
                    logger.warning(f"[ThemeEngine] Could not register webview hook: {e}")

            self._is_active = True

            # 3. Refresh active webviews safely
            self._refresh_views()

            logger.info("[ThemeEngine] Full Black #000000 Theme activated.")

        except Exception as e:
            logger.error(f"[ThemeEngine] Failed activating theme: {e}", exc_info=True)

    def deactivate(self) -> None:
        """Restore standard Anki appearance."""
        if not ANKI_AVAILABLE or mw is None:
            self._is_active = False
            return

        try:
            restore_qss = self._original_stylesheet or ""
            mw.setStyleSheet(restore_qss)
            app = QApplication.instance()
            if app:
                app.setStyleSheet(restore_qss)

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
            logger.info("[ThemeEngine] Full Black Theme deactivated.")

        except Exception as e:
            logger.error(f"[ThemeEngine] Error deactivating theme: {e}", exc_info=True)

    def _on_webview_will_set_content(self, web_content: Any, context: Optional[Any] = None) -> None:
        """Inject full black CSS and direct Logo element into DeckBrowser start screen."""
        if not self._is_active:
            return

        try:
            accent = config.get("theme.accent", self._palette.ACCENT_PRIMARY)
            css = generate_webview_css(self._palette, accent=accent)

            logo_b64 = LOGO_PNG_BASE64

            style_tag = f"<style id='awt-fullblack-theme'>{css}</style>"
            js_tag = f"""
            <script id='awt-fullblack-enforce'>
            (function() {{
                function applyBlackAndLogo() {{
                    document.documentElement.style.setProperty('background', '#000000', 'important');
                    document.documentElement.style.setProperty('background-color', '#000000', 'important');
                    if (document.body) {{
                        document.body.style.setProperty('background', '#000000', 'important');
                        document.body.style.setProperty('background-color', '#000000', 'important');
                    }}

                    // Direct injection of logo into Deck Browser
                    var db = document.querySelector('#deckbrowser');
                    if (db && !document.querySelector('#wykiati-logo-banner') && '{logo_b64}') {{
                        var banner = document.createElement('div');
                        banner.id = 'wykiati-logo-banner';
                        banner.style.cssText = 'text-align: center; margin: 24px auto 10px auto; width: 100%; max-width: 860px; pointer-events: none;';
                        banner.innerHTML = '<img src="{logo_b64}" alt="Wykiati Logo" style="max-width: 170px; height: auto; opacity: 0.9; display: block; margin: 0 auto; border: none !important; box-shadow: none !important; background: transparent !important;" />';
                        db.insertBefore(banner, db.firstChild);
                    }}
                }}
                applyBlackAndLogo();
                if (document.readyState === 'loading') {{
                    document.addEventListener('DOMContentLoaded', applyBlackAndLogo);
                }}
            }})();
            </script>
            """

            if hasattr(web_content, "head"):
                web_content.head += style_tag + js_tag
            if hasattr(web_content, "css"):
                web_content.css.append(css)
        except Exception as e:
            logger.error(f"[ThemeEngine] Failed injecting webview content: {e}")

    def _refresh_views(self) -> None:
        """Trigger redraw of main window, top toolbar, and web views safely."""
        if not ANKI_AVAILABLE or mw is None:
            return
        # Critical: Only refresh if collection is actually loaded and ready
        if getattr(mw, "col", None) is None:
            return
        try:
            if hasattr(mw, "toolbar") and hasattr(mw.toolbar, "draw"):
                mw.toolbar.draw()
            if hasattr(mw, "reset"):
                mw.reset()
            elif hasattr(mw, "deckBrowser") and hasattr(mw.deckBrowser, "refresh"):
                mw.deckBrowser.refresh()
            if hasattr(mw, "reviewer") and hasattr(mw.reviewer, "refresh"):
                mw.reviewer.refresh()
        except Exception as e:
            logger.debug(f"[ThemeEngine] View refresh skipped: {e}")

    def is_active(self) -> bool:
        return self._is_active


# Global theme engine singleton
theme_engine = ThemeEngine()
