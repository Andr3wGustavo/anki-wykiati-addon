"""
Zero-Lag, Hardware-Accelerated Void Black (#000000) Stylesheet Engine.
Optimized for 144Hz fluidity, responsive fluid zoom scaling, and zero GPU composite stall.
"""

from typing import Optional
from .palette import PALETTE, ThemePalette


def generate_qss(palette: ThemePalette = PALETTE, accent: Optional[str] = None) -> str:
    """
    High-Performance Qt StyleSheet (QSS) without expensive universal selectors.
    Targets specific Qt classes directly to prevent widget tree restyle lag.
    """
    acc = accent or palette.ACCENT_PRIMARY
    bg = palette.BACKGROUND_PURE_BLACK  # #000000
    surf = palette.BACKGROUND_SURFACE
    surf_hov = palette.BACKGROUND_SURFACE_HOVER
    border = palette.BORDER_DEFAULT
    border_subtle = palette.BORDER_SUBTLE
    border_strong = palette.BORDER_STRONG
    text = palette.TEXT_PRIMARY
    text_sec = palette.TEXT_SECONDARY
    text_muted = palette.TEXT_MUTED

    return f"""
    /* =========================================================================
       SPECIFIC WIDGET SELECTORS (Avoids Qt Restyle Spikes on Resize/Zoom)
       ========================================================================= */
    QMainWindow, QDialog, QFrame, QSplitter, QStackedWidget, QScrollArea, QAbstractScrollArea {{
        background-color: {bg};
        background: {bg};
        color: {text};
        font-family: "Inter", "Geist", -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
        selection-background-color: {acc};
        selection-color: #000000;
        border: none;
    }}

    /* Main Window Separator */
    QMainWindow::separator, QSplitter::handle {{
        background-color: {bg};
        width: 1px;
        height: 1px;
    }}

    /* Native Toolbars */
    QToolBar {{
        background-color: {bg};
        background: {bg};
        border-bottom: 1px solid {border_subtle};
        padding: 4px 8px;
        spacing: 6px;
    }}
    QToolBar QToolButton {{
        background-color: {surf};
        color: {text_sec};
        border: 1px solid {border_subtle};
        border-radius: 16px;
        padding: 6px 14px;
        font-weight: 500;
        font-size: 12px;
    }}
    QToolBar QToolButton:hover {{
        background-color: {surf_hov};
        color: {text};
        border-color: {border_strong};
    }}

    /* Menu Bars & Menus */
    QMenuBar {{
        background-color: {bg};
        color: {text_sec};
        border-bottom: 1px solid {border_subtle};
        padding: 4px 8px;
    }}
    QMenuBar::item {{
        background: transparent;
        padding: 6px 12px;
        border-radius: 6px;
    }}
    QMenuBar::item:selected {{
        background-color: {surf_hov};
        color: {text};
    }}
    QMenu {{
        background-color: #0C0C0E;
        color: {text};
        border: 1px solid {border_strong};
        border-radius: 10px;
        padding: 6px;
    }}
    QMenu::item {{
        padding: 7px 22px 7px 12px;
        border-radius: 6px;
        color: {text_sec};
    }}
    QMenu::item:selected {{
        background-color: rgba(255, 255, 255, 0.08);
        color: {text};
    }}

    /* Floating Pill Buttons */
    QPushButton {{
        background-color: {surf};
        color: {text};
        border: 1px solid {border};
        border-radius: 18px;
        padding: 8px 20px;
        font-size: 13px;
        font-weight: 500;
        min-height: 20px;
    }}
    QPushButton:hover {{
        background-color: {surf_hov};
        border-color: {border_strong};
    }}
    QPushButton:pressed {{
        background-color: {palette.BACKGROUND_SURFACE_ACTIVE};
    }}
    QPushButton:default, QPushButton[primary="true"] {{
        background-color: #FFFFFF;
        color: #000000;
        border: 1px solid #FFFFFF;
        font-weight: 600;
    }}
    QPushButton:default:hover, QPushButton[primary="true"]:hover {{
        background-color: #E4E4E7;
        border-color: #E4E4E7;
    }}

    /* Input Fields */
    QLineEdit, QTextEdit, QPlainTextEdit, QSpinBox, QComboBox {{
        background-color: #0A0A0C;
        color: {text};
        border: 1px solid {border};
        border-radius: 10px;
        padding: 8px 12px;
        font-size: 13px;
    }}
    QLineEdit:focus, QTextEdit:focus, QPlainTextEdit:focus, QSpinBox:focus, QComboBox:focus {{
        border: 1px solid {palette.BORDER_FOCUS};
        background-color: #101014;
    }}

    /* Tables and Lists */
    QTableView, QListView, QTreeView, QTableWidget, QListWidget, QTreeWidget {{
        background-color: {bg};
        color: {text};
        border: 1px solid {border_subtle};
        border-radius: 12px;
        gridline-color: {border_subtle};
        selection-background-color: rgba(255, 255, 255, 0.06);
        selection-color: {text};
    }}
    QHeaderView::section {{
        background-color: {bg};
        color: {text_muted};
        border: none;
        border-bottom: 1px solid {border_subtle};
        border-right: 1px solid {border_subtle};
        padding: 8px 12px;
        font-weight: 500;
        font-size: 11px;
    }}

    /* Slim Scrollbars */
    QScrollBar:vertical {{
        background: transparent;
        width: 6px;
        margin: 0;
    }}
    QScrollBar::handle:vertical {{
        background-color: rgba(255, 255, 255, 0.15);
        min-height: 24px;
        border-radius: 3px;
    }}
    QScrollBar::handle:vertical:hover {{
        background-color: rgba(255, 255, 255, 0.30);
    }}
    QScrollBar:horizontal {{
        background: transparent;
        height: 6px;
        margin: 0;
    }}
    QScrollBar::handle:horizontal {{
        background-color: rgba(255, 255, 255, 0.15);
        min-width: 24px;
        border-radius: 3px;
    }}
    """


def generate_webview_css(palette: ThemePalette = PALETTE, accent: Optional[str] = None) -> str:
    """
    Hardware-accelerated, responsive CSS for Anki WebViews.
    Employs fluid units clamp(), translateZ(0) GPU promotion, and zero composite stalls.
    """
    acc = accent or palette.ACCENT_PRIMARY
    bg = palette.BACKGROUND_PURE_BLACK  # #000000
    border_subtle = palette.BORDER_SUBTLE
    text = palette.TEXT_PRIMARY
    text_sec = palette.TEXT_SECONDARY
    text_muted = palette.TEXT_MUTED

    return f"""
    /* =========================================================================
       HARDWARE-ACCELERATED DOM RESET & CSS VARIABLES
       ========================================================================= */
    :root, html, body, #outer, #main, #main-content, #header, #footer, #qa, #content,
    header, nav, .navbar, .toolbar, #toolbar, #deckbrowser, .deck-table, table,
    #overview, .overview, #stats, .stats, #bottomWeb, .nightMode, body.nightMode,
    body:not(.nightMode), [data-bs-theme="dark"], [data-bs-theme="light"] {{
        --canvas: {bg} !important;
        --surface: {bg} !important;
        --surface-ground: {bg} !important;
        --surface-card: #08080A !important;
        --surface-overlay: #0C0C0E !important;
        --fg: {text} !important;
        --fg-muted: {text_sec} !important;
        --card-bg: {bg} !important;
        --card-border: {border_subtle} !important;
        --border: {border_subtle} !important;
        --border-subtle: {border_subtle} !important;
        --window-bg: {bg} !important;
        --toolbar-bg: {bg} !important;
        --header-bg: {bg} !important;
        --footer-bg: {bg} !important;
        --bs-body-bg: {bg} !important;
        --bs-body-color: {text} !important;
        --link: {acc} !important;
        --accent: {acc} !important;
        background-color: {bg} !important;
        background: {bg} !important;
        color: {text} !important;
        font-family: "Inter", "Geist", -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif !important;
        letter-spacing: -0.015em !important;
        box-sizing: border-box !important;
    }}

    /* GPU Layer Acceleration for Smooth 144Hz Animation */
    .card, tr.deck, #header, #bottomWeb, button {{
        transform: translateZ(0) !important;
        backface-visibility: hidden !important;
        will-change: transform, opacity !important;
    }}

    /* Fluid Viewport Base */
    html, body {{
        width: 100% !important;
        min-height: 100% !important;
        margin: 0 !important;
        padding: 0 !important;
        overflow-x: hidden !important;
    }}

    /* =========================================================================
       1. TOP TOOLBAR WEBVIEW (Decks, Add, Browse, Stats, Sync)
       ========================================================================= */
    #header, header, .toolbar, nav.navbar, #toolbar {{
        background-color: {bg} !important;
        background: {bg} !important;
        border-bottom: 1px solid {border_subtle} !important;
        padding: clamp(4px, 1vh, 8px) clamp(8px, 2vw, 16px) !important;
        display: flex !important;
        align-items: center !important;
        justify-content: space-between !important;
        width: 100% !important;
    }}

    .toolbar a, nav.navbar a, .nav-link, a.nav-link, .toolbar button, .toolbar-button {{
        background: #0D0D10 !important;
        color: {text_sec} !important;
        border: 1px solid {border_subtle} !important;
        border-radius: 18px !important;
        padding: clamp(4px, 0.8vh, 8px) clamp(10px, 1.2vw, 18px) !important;
        margin: 0 4px !important;
        font-size: clamp(11px, 1vw, 13px) !important;
        font-weight: 500 !important;
        text-decoration: none !important;
        transition: background 0.08s ease, color 0.08s ease !important;
        display: inline-flex !important;
        align-items: center !important;
    }}

    .toolbar a:hover, nav.navbar a:hover, .nav-link:hover, a.nav-link:hover, .toolbar button:hover {{
        background: #18181C !important;
        color: #FFFFFF !important;
        border-color: rgba(255, 255, 255, 0.18) !important;
    }}

    /* =========================================================================
       2. DECK BROWSER (MIDDLE LIST OF DECKS) - WITH SUBTLE WATERMARK LOGO
       ========================================================================= */
    #deckbrowser {{
        background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 400 130' width='400' height='130'%3E%3Cg fill='none' stroke='rgba(255,255,255,0.05)' stroke-width='1.5' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpolygon points='200,10 238,55 200,100 162,55' /%3E%3Cline x1='200' y1='10' x2='200' y2='100' /%3E%3Cline x1='162' y1='55' x2='238' y2='55' /%3E%3Ccircle cx='200' cy='55' r='4' fill='rgba(255,255,255,0.09)' /%3E%3C/g%3E%3Ctext x='200' y='122' text-anchor='middle' font-family='Inter, Segoe UI, sans-serif' font-size='11' font-weight='600' letter-spacing='7' fill='rgba(255,255,255,0.07)'%3EWYKIATI%3C/text%3E%3C/svg%3E") !important;
        background-repeat: no-repeat !important;
        background-position: center 24px !important;
        background-size: min(340px, 50vw) auto !important;
        padding-top: clamp(100px, 14vh, 140px) !important;
    }}

    #deckbrowser, .deck-table, table.deck-table {{
        background-color: {bg} !important;
        background: {bg} !important;
        border-collapse: separate !important;
        border-spacing: 0 4px !important;
        width: min(94%, 900px) !important;
        margin: 0 auto clamp(12px, 2vh, 28px) auto !important;
    }}

    tr.deck {{
        background-color: #0A0A0D !important;
        background: #0A0A0D !important;
        border: 1px solid {border_subtle} !important;
        border-radius: 12px !important;
        transition: background 0.08s ease !important;
    }}

    tr.deck:hover {{
        background-color: #141418 !important;
        background: #141418 !important;
        border-color: rgba(255, 255, 255, 0.15) !important;
    }}

    td.decktd {{
        padding: clamp(8px, 1.2vh, 14px) clamp(10px, 1.5vw, 18px) !important;
        border: none !important;
    }}

    a.deckname {{
        color: {text} !important;
        font-weight: 500 !important;
        text-decoration: none !important;
        font-size: clamp(12px, 1.1vw, 15px) !important;
    }}

    /* Minimalist Counters */
    .new-count, .count-new, .new-count-badge {{
        color: #38BDF8 !important;
        font-weight: 600 !important;
        font-family: "JetBrains Mono", monospace !important;
        font-size: clamp(11px, 1vw, 13px) !important;
    }}
    .learn-count, .count-learn, .learn-count-badge {{
        color: #FBBF24 !important;
        font-weight: 600 !important;
        font-family: "JetBrains Mono", monospace !important;
        font-size: clamp(11px, 1vw, 13px) !important;
    }}
    .review-count, .count-review, .review-count-badge {{
        color: #4ADE80 !important;
        font-weight: 600 !important;
        font-family: "JetBrains Mono", monospace !important;
        font-size: clamp(11px, 1vw, 13px) !important;
    }}

    /* =========================================================================
       3. CARD REVIEWER - FULLY RESPONSIVE CENTERED CONTAINER
       ========================================================================= */
    body#body, body {{
        display: flex !important;
        flex-direction: column !important;
        justify-content: center !important;
        align-items: center !important;
        text-align: center !important;
    }}

    #qa {{
        width: 100% !important;
        max-width: min(92vw, 860px) !important;
        display: flex !important;
        flex-direction: column !important;
        align-items: center !important;
        justify-content: center !important;
        text-align: center !important;
        margin: 0 auto !important;
        padding: clamp(12px, 2vh, 32px) clamp(8px, 2vw, 24px) !important;
    }}

    .card {{
        width: 100% !important;
        max-width: min(92vw, 860px) !important;
        margin: 0 auto !important;
        text-align: center !important;
        display: flex !important;
        flex-direction: column !important;
        align-items: center !important;
        justify-content: center !important;
        background: #0A0A0C !important;
        background-color: #0A0A0C !important;
        border: 1px solid {border_subtle} !important;
        border-radius: clamp(12px, 2vw, 20px) !important;
        padding: clamp(18px, 3vh, 40px) clamp(16px, 3vw, 36px) !important;
        box-shadow: 0 12px 36px rgba(0, 0, 0, 0.8) !important;
    }}

    /* Dynamic Zoom-Responsive Image Container */
    img {{
        margin: clamp(10px, 2vh, 20px) auto !important;
        display: block !important;
        max-width: 100% !important;
        max-height: min(58vh, 520px) !important;
        width: auto !important;
        height: auto !important;
        object-fit: contain !important;
        border-radius: 12px !important;
        border: 1px solid {border_subtle} !important;
    }}

    .card p, .card div, .card h1, .card h2, .card h3 {{
        text-align: center !important;
        margin-left: auto !important;
        margin-right: auto !important;
        font-size: clamp(13px, 1.2vw, 17px) !important;
        line-height: 1.6 !important;
    }}

    /* Minimalist Cloze Deletion */
    .cloze {{
        color: #38BDF8 !important;
        font-weight: 600 !important;
        background: rgba(56, 189, 248, 0.10) !important;
        padding: 2px 8px !important;
        border-radius: 4px !important;
        border: 1px solid rgba(56, 189, 248, 0.20) !important;
    }}

    /* =========================================================================
       4. BOTTOM ACTION BAR (Again, Hard, Good, Easy)
       ========================================================================= */
    #bottomWeb, #outer, #bottomBar, footer {{
        background-color: {bg} !important;
        background: {bg} !important;
        border-top: 1px solid {border_subtle} !important;
        padding: clamp(6px, 1.2vh, 12px) clamp(8px, 2vw, 16px) !important;
        display: flex !important;
        justify-content: center !important;
        align-items: center !important;
        width: 100% !important;
    }}

    #bottomWeb button, .nobootstrap button, button.ease-button, button.btn, button#ease1, button#ease2, button#ease3, button#ease4, button#ansbtn {{
        background: #0D0D10 !important;
        color: {text} !important;
        border: 1px solid {border_subtle} !important;
        border-radius: 20px !important;
        padding: clamp(6px, 1vh, 10px) clamp(14px, 2vw, 26px) !important;
        margin: 0 4px !important;
        font-weight: 500 !important;
        font-size: clamp(11px, 1vw, 13px) !important;
        cursor: pointer !important;
        transition: background 0.08s ease !important;
    }}

    #bottomWeb button:hover, button.ease-button:hover, button#ansbtn:hover {{
        background: #18181C !important;
        border-color: rgba(255, 255, 255, 0.20) !important;
        color: #FFFFFF !important;
    }}

    button#ease1, .ease1 {{ border-color: rgba(248, 113, 113, 0.3) !important; }}
    button#ease2, .ease2 {{ border-color: rgba(251, 191, 36, 0.3) !important; }}
    button#ease3, .ease3 {{ border-color: rgba(56, 189, 248, 0.3) !important; }}
    button#ease4, .ease4 {{ border-color: rgba(74, 222, 128, 0.3) !important; }}
    """
