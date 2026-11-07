"""
Theme Engine for Full Black (#000000) Void & Floating Glass Aesthetic.
Controls Qt application stylesheets and injects high-priority CSS & JS into all Anki WebViews:
- Top Toolbar (Decks, Add, Browse, Stats, Sync)
- Deck Browser (Middle Area)
- Card Reviewer (Centered Card, Centered Image & Question/Answer)
- Bottom Bar (Floating Answer Buttons)
"""

import re
from typing import Any, Optional, Tuple

try:
    from ..core.config import config
    from ..core.logger import logger
    from .palette import PALETTE, ThemePalette, is_light_color, normalize_hex, readable_text_on
    from .styles import generate_qss, generate_webview_css
except (ImportError, ValueError):
    from core.config import config
    from core.logger import logger
    from theme.palette import PALETTE, ThemePalette, is_light_color, normalize_hex, readable_text_on
    from theme.styles import generate_qss, generate_webview_css

# Check Anki & GUI availability
try:
    from aqt import gui_hooks, mw
    from aqt.qt import QApplication, QColor, QPalette, QTimer
    ANKI_AVAILABLE = True
except ImportError:
    gui_hooks = mw = QApplication = QColor = QPalette = QTimer = None
    ANKI_AVAILABLE = False


try:
    from .logo_data import LOGO_PNG_BASE64
except (ImportError, ValueError):
    try:
        from theme.logo_data import LOGO_PNG_BASE64
    except ImportError:
        LOGO_PNG_BASE64 = ""


# Markers around the add-on's QSS so it can be appended to (and stripped from)
# Anki's own application stylesheet without clobbering it.
_QSS_BEGIN = "/* AWT-THEME-BEGIN */"
_QSS_END = "/* AWT-THEME-END */"
_QSS_BLOCK_RE = re.compile(re.escape(_QSS_BEGIN) + r".*?" + re.escape(_QSS_END), re.DOTALL)


def _strip_own_qss(qss: Optional[str]) -> str:
    """Remove any add-on QSS block, leaving only Anki's (or other add-ons') styles."""
    return _QSS_BLOCK_RE.sub("", qss or "").rstrip()


class ThemeEngine:
    """
    Manages activation, deactivation, and real-time styling updates for Anki.

    - Config changes are coalesced: several `config.set("theme.*")` calls in a row
      produce a single re-apply and a single view refresh.
    - Anki's own stylesheet and palette are preserved: the add-on QSS is appended
      inside markers, and the originals are restored on deactivation.
    - When Anki re-applies its theme (light/dark switch), the add-on adopts Anki's
      fresh style as the new baseline and re-applies itself on top.
    """
    def __init__(self) -> None:
        self._is_active = False
        self._hook_registered = False
        self._theme_hook_registered = False
        self._palette = PALETTE
        self._original_app_qss: Optional[str] = None
        self._original_mw_qss: Optional[str] = None
        self._original_palette: Optional[Any] = None
        self._applied_palette_key: Optional[int] = None
        self._apply_pending = False
        self._refresh_pending = False

    # ------------------------------------------------------------------ setup

    def initialize(self) -> None:
        """Initialize theme based on configuration and subscribe to settings changes."""
        # The root "theme" subscription fires for every "theme.*" key change,
        # so one subscription is enough (several caused repeated re-applies).
        config.subscribe("theme", self._on_config_changed)
        self._register_theme_change_hook()

        if config.get("theme.enabled", True):
            self.activate()

    def _register_theme_change_hook(self) -> None:
        if not ANKI_AVAILABLE or gui_hooks is None or self._theme_hook_registered:
            return
        try:
            if hasattr(gui_hooks, "theme_did_change"):
                gui_hooks.theme_did_change.append(self._on_anki_theme_changed)
                self._theme_hook_registered = True
        except Exception as e:
            logger.warning(f"[ThemeEngine] Could not register theme_did_change hook: {e}")

    def _get_colors(self) -> Tuple[str, str]:
        """Return validated (background, accent) from config; invalid values fall back to defaults."""
        bg = normalize_hex(config.get("theme.background"), self._palette.BACKGROUND_PURE_BLACK)
        default_accent = "#09090B" if is_light_color(bg) else self._palette.ACCENT_PRIMARY
        accent = normalize_hex(config.get("theme.accent"), default_accent)
        return bg, accent

    # ------------------------------------------------------- change handling

    def _on_config_changed(self, *args: Any) -> None:
        """Handle theme setting updates (debounced)."""
        self.schedule_apply()

    def schedule_apply(self) -> None:
        """Coalesce several config changes into one activate()/deactivate() call."""
        if not ANKI_AVAILABLE or QTimer is None or mw is None:
            self._apply_now()
            return
        if self._apply_pending:
            return
        self._apply_pending = True
        QTimer.singleShot(0, self._apply_now)

    def _apply_now(self) -> None:
        self._apply_pending = False
        if config.get("theme.enabled", True):
            self.activate()
        else:
            self.deactivate()

    def _on_anki_theme_changed(self, *args: Any) -> None:
        """Anki just re-applied its own style: adopt it as the new baseline, then re-theme."""
        if not ANKI_AVAILABLE or QApplication is None:
            return
        try:
            app = QApplication.instance()
            if app is None:
                return
            self._original_app_qss = _strip_own_qss(app.styleSheet())
            if mw is not None:
                self._original_mw_qss = _strip_own_qss(mw.styleSheet())
            current_palette = app.palette()
            # Only adopt the palette if Anki actually replaced ours.
            if self._applied_palette_key is None or current_palette.cacheKey() != self._applied_palette_key:
                self._original_palette = QPalette(current_palette)
            if self._is_active:
                self.schedule_apply()
        except Exception as e:
            logger.error(f"[ThemeEngine] Error handling Anki theme change: {e}", exc_info=True)

    # ---------------------------------------------------- activate / restore

    def activate(self) -> None:
        """Activate Full Black #000000 / Custom RGB theme across Qt widgets and WebViews."""
        if not ANKI_AVAILABLE or mw is None:
            self._is_active = True
            logger.info("[ThemeEngine] Theme active (Headless/Mock mode).")
            return

        try:
            bg_color, accent = self._get_colors()
            qss = generate_qss(accent=accent, bg_color=bg_color)
            block = f"\n{_QSS_BEGIN}\n{qss}\n{_QSS_END}\n"

            app = QApplication.instance()

            # Remember Anki's own styling the first time we touch it
            if self._original_mw_qss is None:
                self._original_mw_qss = _strip_own_qss(mw.styleSheet())
            if app is not None and self._original_app_qss is None:
                self._original_app_qss = _strip_own_qss(app.styleSheet())
            if app is not None and self._original_palette is None and QPalette is not None:
                self._original_palette = QPalette(app.palette())

            # 1. Append our QSS on top of the existing stylesheet (never replace it)
            mw.setStyleSheet((self._original_mw_qss or "") + block)
            if app is not None:
                app.setStyleSheet((self._original_app_qss or "") + block)
                self._apply_palette(app, bg_color, accent)

            # 2. Webview hook follows the "apply_to_webviews" option both ways
            self._sync_webview_hook(bool(config.get("theme.apply_to_webviews", True)))

            self._is_active = True

            # 3. Refresh active webviews (debounced)
            self._refresh_views()

            logger.info(f"[ThemeEngine] Theme activated (bg={bg_color}, accent={accent}).")

        except Exception as e:
            logger.error(f"[ThemeEngine] Failed activating theme: {e}", exc_info=True)

    def _apply_palette(self, app: Any, bg_color: str, accent: str) -> None:
        """Native Qt palette adapted to background luminance (light background -> dark text)."""
        if QPalette is None or QColor is None:
            return
        light = is_light_color(bg_color)
        text = "#09090B" if light else "#FFFFFF"
        tooltip_bg = "#FFFFFF" if light else "#121214"
        placeholder = "#71717A" if light else "#A1A1AA"

        palette = QPalette(self._original_palette) if self._original_palette is not None else QPalette()
        roles = QPalette.ColorRole
        palette.setColor(roles.Window, QColor(bg_color))
        palette.setColor(roles.WindowText, QColor(text))
        palette.setColor(roles.Base, QColor(bg_color))
        palette.setColor(roles.AlternateBase, QColor(bg_color))
        palette.setColor(roles.ToolTipBase, QColor(tooltip_bg))
        palette.setColor(roles.ToolTipText, QColor(text))
        palette.setColor(roles.Text, QColor(text))
        palette.setColor(roles.Button, QColor(bg_color))
        palette.setColor(roles.ButtonText, QColor(text))
        palette.setColor(roles.BrightText, QColor(text))
        palette.setColor(roles.Highlight, QColor(accent))
        palette.setColor(roles.HighlightedText, QColor(readable_text_on(accent)))
        if hasattr(roles, "PlaceholderText"):
            palette.setColor(roles.PlaceholderText, QColor(placeholder))
        app.setPalette(palette)
        try:
            self._applied_palette_key = app.palette().cacheKey()
        except Exception:
            self._applied_palette_key = None

    def _sync_webview_hook(self, enabled: bool) -> None:
        if gui_hooks is None or not hasattr(gui_hooks, "webview_will_set_content"):
            return
        try:
            if enabled and not self._hook_registered:
                gui_hooks.webview_will_set_content.append(self._on_webview_will_set_content)
                self._hook_registered = True
            elif not enabled and self._hook_registered:
                if self._on_webview_will_set_content in gui_hooks.webview_will_set_content:
                    gui_hooks.webview_will_set_content.remove(self._on_webview_will_set_content)
                self._hook_registered = False
        except Exception as e:
            logger.warning(f"[ThemeEngine] Could not update webview hook: {e}")

    def deactivate(self) -> None:
        """Restore standard Anki appearance (its own stylesheet and palette)."""
        if not ANKI_AVAILABLE or mw is None:
            self._is_active = False
            return

        try:
            if self._original_mw_qss is not None:
                mw.setStyleSheet(self._original_mw_qss)
            app = QApplication.instance()
            if app is not None:
                if self._original_app_qss is not None:
                    app.setStyleSheet(self._original_app_qss)
                if self._original_palette is not None:
                    app.setPalette(self._original_palette)
            self._applied_palette_key = None

            self._sync_webview_hook(False)

            self._is_active = False
            self._refresh_views()
            logger.info("[ThemeEngine] Theme deactivated.")

        except Exception as e:
            logger.error(f"[ThemeEngine] Error deactivating theme: {e}", exc_info=True)

    # --------------------------------------------------------------- webviews

    def _on_webview_will_set_content(self, web_content: Any, context: Optional[Any] = None) -> None:
        """Inject zero-lag custom background CSS and direct Logo element into DeckBrowser start screen."""
        if not self._is_active:
            return

        try:
            bg_color, accent = self._get_colors()
            css = generate_webview_css(self._palette, accent=accent, bg_color=bg_color)

            logo_b64 = LOGO_PNG_BASE64
            style_tag = f"<style id='awt-fullblack-theme'>{css}</style>"

            # Lightweight logo banner injection only when logo data exists
            js_tag = ""
            if logo_b64:
                js_tag = f"""
                <script id='awt-fullblack-enforce'>
                (function() {{
                    function injectLogo() {{
                        var db = document.querySelector('#deckbrowser');
                        if (db && !document.querySelector('#wykiati-logo-banner')) {{
                            var banner = document.createElement('div');
                            banner.id = 'wykiati-logo-banner';
                            banner.style.cssText = 'text-align: center; margin: 18px auto 8px auto; width: 100%; max-width: 880px; pointer-events: none;';
                            banner.innerHTML = '<img src="{logo_b64}" alt="Wykiati Logo" style="max-width: 160px; height: auto; opacity: 0.92; display: block; margin: 0 auto; border: none !important; box-shadow: none !important; background: transparent !important;" />';
                            db.insertBefore(banner, db.firstChild);
                        }}
                    }}
                    if (document.readyState === 'loading') {{
                        document.addEventListener('DOMContentLoaded', injectLogo, {{ once: true }});
                    }} else {{
                        injectLogo();
                    }}
                }})();
                </script>
                """

            if hasattr(web_content, "head"):
                web_content.head += style_tag + js_tag
            elif hasattr(web_content, "css"):
                web_content.css.append(css)
        except Exception as e:
            logger.error(f"[ThemeEngine] Failed injecting webview content: {e}")

    def _refresh_views(self) -> None:
        """Schedule a single redraw of toolbar and current screen (coalesces bursts)."""
        if not ANKI_AVAILABLE or mw is None:
            return
        if QTimer is None:
            self._do_refresh()
            return
        if self._refresh_pending:
            return
        self._refresh_pending = True
        QTimer.singleShot(0, self._do_refresh)

    def _do_refresh(self) -> None:
        self._refresh_pending = False
        # Critical: Only refresh if collection is actually loaded and ready
        if mw is None or getattr(mw, "col", None) is None:
            return
        try:
            if hasattr(mw, "toolbar") and hasattr(mw.toolbar, "draw"):
                mw.toolbar.draw()
            # mw.reset() re-renders the current state (deck browser, overview or
            # reviewer incl. bottom bar), so a separate reviewer refresh is not needed.
            if hasattr(mw, "reset"):
                mw.reset()
            elif hasattr(mw, "deckBrowser") and hasattr(mw.deckBrowser, "refresh"):
                mw.deckBrowser.refresh()
        except Exception as e:
            logger.debug(f"[ThemeEngine] View refresh skipped: {e}")

    def is_active(self) -> bool:
        return self._is_active


# Global theme engine singleton
theme_engine = ThemeEngine()
