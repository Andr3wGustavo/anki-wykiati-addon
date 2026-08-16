"""
Zero-Lag, Hardware-Accelerated Void Black (#000000) Stylesheet Engine.
Rock-solid alignment, perfectly centered cards and images, and crisp Inter typography.
"""

from typing import Optional
from .palette import PALETTE, ThemePalette


def generate_qss(palette: ThemePalette = PALETTE, accent: Optional[str] = None) -> str:
    """
    High-Performance, Zero-Lag Qt StyleSheet (QSS) for Anki's native widgets.
    Uses crisp square glass buttons, subtle transparencies, and Void Black (#000000) base.
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
       NATIVE WIDGET STYLES - ZERO-LAG VOID BLACK & SQUARE GLASS
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
        border-radius: 4px;
        padding: 6px 12px;
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
        padding: 6px 10px;
        border-radius: 4px;
    }}
    QMenuBar::item:selected {{
        background-color: {surf_hov};
        color: {text};
    }}
    QMenu {{
        background-color: #09090B;
        color: {text};
        border: 1px solid {border_strong};
        border-radius: 6px;
        padding: 4px;
    }}
    QMenu::item {{
        padding: 6px 20px 6px 10px;
        border-radius: 4px;
        color: {text_sec};
    }}
    QMenu::item:selected {{
        background-color: rgba(255, 255, 255, 0.08);
        color: {text};
    }}

    /* Square Glass Buttons */
    QPushButton {{
        background-color: rgba(255, 255, 255, 0.04);
        color: {text};
        border: 1px solid {border};
        border-radius: 4px;
        padding: 7px 16px;
        font-size: 13px;
        font-weight: 500;
        min-height: 18px;
    }}
    QPushButton:hover {{
        background-color: rgba(255, 255, 255, 0.09);
        border-color: {border_strong};
        color: #FFFFFF;
    }}
    QPushButton:pressed {{
        background-color: rgba(255, 255, 255, 0.02);
        border-color: {border_subtle};
    }}
    QPushButton:default, QPushButton[primary="true"] {{
        background-color: rgba(255, 255, 255, 0.14);
        color: #FFFFFF;
        border: 1px solid rgba(255, 255, 255, 0.30);
        font-weight: 600;
        border-radius: 4px;
    }}
    QPushButton:default:hover, QPushButton[primary="true"]:hover {{
        background-color: rgba(255, 255, 255, 0.22);
        border-color: rgba(255, 255, 255, 0.45);
    }}

    /* Input Fields */
    QLineEdit, QTextEdit, QPlainTextEdit, QSpinBox, QComboBox {{
        background-color: #060608;
        color: {text};
        border: 1px solid {border};
        border-radius: 4px;
        padding: 7px 10px;
        font-size: 13px;
    }}
    QLineEdit:focus, QTextEdit:focus, QPlainTextEdit:focus, QSpinBox:focus, QComboBox:focus {{
        border: 1px solid {palette.BORDER_FOCUS};
        background-color: #0C0C10;
    }}

    /* Group Boxes */
    QGroupBox {{
        background-color: rgba(255, 255, 255, 0.02);
        border: 1px solid {border_subtle};
        border-radius: 6px;
        margin-top: 14px;
        padding-top: 14px;
        font-size: 12px;
        font-weight: 600;
        color: {text_sec};
    }}
    QGroupBox::title {{
        subcontrol-origin: margin;
        subcontrol-position: top left;
        left: 10px;
        padding: 0 4px;
    }}

    /* Tables and Lists */
    QTableView, QListView, QTreeView, QTableWidget, QListWidget, QTreeWidget {{
        background-color: {bg};
        color: {text};
        border: 1px solid {border_subtle};
        border-radius: 6px;
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
        padding: 6px 10px;
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
        background-color: rgba(255, 255, 255, 0.12);
        min-height: 24px;
        border-radius: 3px;
    }}
    QScrollBar::handle:vertical:hover {{
        background-color: rgba(255, 255, 255, 0.25);
    }}
    QScrollBar:horizontal {{
        background: transparent;
        height: 6px;
        margin: 0;
    }}
    QScrollBar::handle:horizontal {{
        background-color: rgba(255, 255, 255, 0.12);
        min-width: 24px;
        border-radius: 3px;
    }}
    """


def generate_webview_css(palette: ThemePalette = PALETTE, accent: Optional[str] = None) -> str:
    """
    Ultra-Lightweight, Zero-Lag Solid Void Black (#000000) CSS for Anki WebViews.
    - True #000000 pure black (no grey boxes)
    - Perfectly centered bottom ease buttons
    - Correctly sized sync button & toolbar items (no giant icons)
    - Square glass buttons with crisp borders
    - Fluid, responsive standard typography
    """
    acc = accent or palette.ACCENT_PRIMARY
    bg = palette.BACKGROUND_PURE_BLACK  # #000000
    border_subtle = palette.BORDER_SUBTLE
    text = palette.TEXT_PRIMARY
    text_sec = palette.TEXT_SECONDARY
    text_muted = palette.TEXT_MUTED

    return f"""
    /* =========================================================================
       1. GLOBAL RESET & SOLID VOID BLACK (#000000)
       ========================================================================= */
    :root, .nightMode, body.nightMode {{
        --canvas: {bg} !important;
        --surface: {bg} !important;
        --surface-ground: {bg} !important;
        --surface-card: {bg} !important;
        --surface-overlay: {bg} !important;
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
    }}

    html, body {{
        background-color: {bg} !important;
        background: {bg} !important;
        color: {text} !important;
        font-family: "Inter", -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif !important;
        margin: 0 !important;
        padding: 0 !important;
        width: 100% !important;
        min-height: 100% !important;
        box-sizing: border-box !important;
        -webkit-font-smoothing: antialiased !important;
    }}

    *, *::before, *::after {{
        box-sizing: border-box !important;
    }}

    /* Global Scrollbar */
    ::-webkit-scrollbar {{
        width: 5px !important;
        height: 5px !important;
        background: transparent !important;
    }}
    ::-webkit-scrollbar-thumb {{
        background: rgba(255, 255, 255, 0.12) !important;
        border-radius: 2px !important;
    }}
    ::-webkit-scrollbar-thumb:hover {{
        background: rgba(255, 255, 255, 0.25) !important;
    }}

    /* =========================================================================
       2. TOP TOOLBAR (DECKS, ADD, BROWSE, STATS, SYNC)
       ========================================================================= */
    #header, header, .toolbar, nav.navbar, #toolbar {{
        background-color: {bg} !important;
        background: {bg} !important;
        border-bottom: 1px solid {border_subtle} !important;
        padding: 4px 12px !important;
        display: flex !important;
        align-items: center !important;
        justify-content: space-between !important;
        flex-wrap: wrap !important;
        gap: 4px !important;
        width: 100% !important;
        min-height: 38px !important;
    }}

    /* Constrain all icons/SVGs so Sync never becomes gigantic */
    #header svg, #header img, .toolbar svg, .toolbar img, nav.navbar svg, nav.navbar img, 
    #sync svg, #sync img, #sync-button svg, #sync-button img, .sync-button svg, .sync-button img {{
        width: 13px !important;
        height: 13px !important;
        max-width: 13px !important;
        max-height: 13px !important;
        vertical-align: middle !important;
        display: inline-block !important;
        margin-right: 4px !important;
        object-fit: contain !important;
    }}

    .toolbar a, nav.navbar a, .nav-link, a.nav-link, .toolbar button, .toolbar-button, 
    #header a, #header button, #sync, #sync-button {{
        background: rgba(255, 255, 255, 0.04) !important;
        color: {text_sec} !important;
        border: 1px solid rgba(255, 255, 255, 0.10) !important;
        border-radius: 4px !important;
        padding: 4px 10px !important;
        margin: 0 2px !important;
        font-size: 12px !important;
        font-weight: 500 !important;
        text-decoration: none !important;
        display: inline-flex !important;
        align-items: center !important;
        justify-content: center !important;
        height: 28px !important;
        min-height: 28px !important;
        max-height: 30px !important;
        line-height: normal !important;
        cursor: pointer !important;
        box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.06) !important;
        transition: background 0.08s ease, border-color 0.08s ease !important;
    }}

    .toolbar a:hover, nav.navbar a:hover, .nav-link:hover, a.nav-link:hover, .toolbar button:hover, #header a:hover, #header button:hover {{
        background: rgba(255, 255, 255, 0.09) !important;
        color: #FFFFFF !important;
        border-color: rgba(255, 255, 255, 0.22) !important;
    }}

    /* =========================================================================
       3. DECK BROWSER (START SCREEN - PURE VOID BLACK)
       ========================================================================= */
    #deckbrowser {{
        background-color: {bg} !important;
        background: {bg} !important;
        display: flex !important;
        flex-direction: column !important;
        align-items: center !important;
        width: 100% !important;
        max-width: 860px !important;
        margin: 0 auto !important;
        padding: 10px 14px 28px 14px !important;
    }}

    #deckbrowser table.deck-table, .deck-table {{
        background-color: {bg} !important;
        background: {bg} !important;
        border-collapse: separate !important;
        border-spacing: 0 4px !important;
        width: 100% !important;
        margin: 8px auto 16px auto !important;
    }}

    tr.deck {{
        background: {bg} !important;
        background-color: {bg} !important;
        border: 1px solid rgba(255, 255, 255, 0.07) !important;
        border-radius: 4px !important;
        transition: background 0.08s ease, border-color 0.08s ease !important;
    }}

    tr.deck:hover {{
        background: rgba(255, 255, 255, 0.05) !important;
        border-color: rgba(255, 255, 255, 0.16) !important;
    }}

    td.decktd {{
        padding: 9px 12px !important;
        border: none !important;
        vertical-align: middle !important;
        background: transparent !important;
    }}

    a.deckname {{
        color: {text} !important;
        font-weight: 500 !important;
        text-decoration: none !important;
        font-size: 13px !important;
    }}

    /* Minimalist High-Contrast Counters */
    .new-count, .count-new, .new-count-badge {{
        color: #38BDF8 !important;
        font-weight: 600 !important;
        font-family: "JetBrains Mono", monospace !important;
        font-size: 12px !important;
    }}
    .learn-count, .count-learn, .learn-count-badge {{
        color: #FBBF24 !important;
        font-weight: 600 !important;
        font-family: "JetBrains Mono", monospace !important;
        font-size: 12px !important;
    }}
    .review-count, .count-review, .review-count-badge {{
        color: #4ADE80 !important;
        font-weight: 600 !important;
        font-family: "JetBrains Mono", monospace !important;
        font-size: 12px !important;
    }}

    /* =========================================================================
       4. CARD REVIEWER (SOLID VOID BLACK #000000 - NO GREY CARD BOX)
       ========================================================================= */
    #qa {{
        background-color: {bg} !important;
        background: {bg} !important;
        width: 100% !important;
        max-width: 860px !important;
        margin: 0 auto !important;
        padding: 16px !important;
        text-align: center !important;
        box-sizing: border-box !important;
    }}

    .card {{
        background: {bg} !important;
        background-color: {bg} !important;
        color: {text} !important;
        width: 100% !important;
        max-width: 840px !important;
        margin: 0 auto !important;
        border: 1px solid rgba(255, 255, 255, 0.08) !important;
        border-radius: 4px !important;
        padding: 24px 20px !important;
        box-shadow: 0 8px 30px rgba(0, 0, 0, 0.9) !important;
        text-align: center !important;
        box-sizing: border-box !important;
        word-break: break-word !important;
    }}

    .card p, .card div, .card h1, .card h2, .card h3 {{
        text-align: center !important;
        margin-left: auto !important;
        margin-right: auto !important;
        line-height: 1.6 !important;
    }}

    /* Answer Separator Line */
    hr, #answer, hr#answer {{
        border: none !important;
        border-top: 1px solid rgba(255, 255, 255, 0.12) !important;
        margin: 16px auto !important;
        width: 100% !important;
        max-width: 440px !important;
        height: 1px !important;
        background: transparent !important;
    }}

    /* Responsive Centered Images */
    .card img, #qa img, img {{
        display: block !important;
        margin: 12px auto !important;
        max-width: 100% !important;
        max-height: 480px !important;
        width: auto !important;
        height: auto !important;
        object-fit: contain !important;
        border-radius: 4px !important;
        border: 1px solid rgba(255, 255, 255, 0.10) !important;
        background: #000000 !important;
    }}

    /* Cloze Deletion */
    .cloze {{
        color: #38BDF8 !important;
        font-weight: 600 !important;
        background: rgba(56, 189, 248, 0.10) !important;
        padding: 2px 6px !important;
        border-radius: 3px !important;
        border: 1px solid rgba(56, 189, 248, 0.25) !important;
    }}

    /* Code Blocks */
    pre, code {{
        background-color: rgba(255, 255, 255, 0.03) !important;
        border: 1px solid {border_subtle} !important;
        color: #E4E4E7 !important;
        border-radius: 4px !important;
        padding: 2px 6px !important;
        font-family: "JetBrains Mono", Consolas, monospace !important;
        font-size: 13px !important;
        text-align: left !important;
        margin: 8px auto !important;
    }}
    pre code {{
        padding: 10px !important;
        display: block !important;
    }}

    /* =========================================================================
       5. BOTTOM ACTION BAR (PERFECTLY CENTERED SQUARE GLASS BUTTONS)
       ========================================================================= */
    #bottomWeb, body#bottomWeb, #bottomBar, footer {{
        background-color: {bg} !important;
        background: {bg} !important;
        border-top: 1px solid {border_subtle} !important;
        padding: 6px 10px !important;
        width: 100% !important;
        margin: 0 !important;
        text-align: center !important;
        box-sizing: border-box !important;
        display: flex !important;
        justify-content: center !important;
        align-items: center !important;
    }}

    /* Center Anki's internal table and cells */
    #outer, #middle, table.nobootstrap, table#outer {{
        margin: 0 auto !important;
        text-align: center !important;
        border: none !important;
        background: transparent !important;
        width: auto !important;
    }}

    table.nobootstrap tr, table.nobootstrap td, #middle td, #outer td {{
        text-align: center !important;
        vertical-align: middle !important;
        padding: 2px 3px !important;
        border: none !important;
        background: transparent !important;
    }}

    /* Uniform Square Glass Bottom Buttons */
    #bottomWeb button, .nobootstrap button, button.ease-button, button.btn, 
    button#ease1, button#ease2, button#ease3, button#ease4, button#ansbtn {{
        background: rgba(255, 255, 255, 0.04) !important;
        color: {text} !important;
        border: 1px solid rgba(255, 255, 255, 0.12) !important;
        border-radius: 4px !important;
        padding: 6px 18px !important;
        margin: 0 3px !important;
        font-family: "Inter", sans-serif !important;
        font-size: 13px !important;
        font-weight: 500 !important;
        cursor: pointer !important;
        height: 34px !important;
        min-height: 34px !important;
        max-height: 36px !important;
        display: inline-flex !important;
        flex-direction: column !important;
        align-items: center !important;
        justify-content: center !important;
        box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.08) !important;
        transition: background 0.08s ease, border-color 0.08s ease !important;
        vertical-align: middle !important;
    }}

    #bottomWeb button:hover, button.ease-button:hover, button#ansbtn:hover {{
        background: rgba(255, 255, 255, 0.10) !important;
        border-color: rgba(255, 255, 255, 0.28) !important;
        color: #FFFFFF !important;
    }}

    /* Show Answer Button */
    button#ansbtn {{
        min-width: 140px !important;
        background: rgba(255, 255, 255, 0.10) !important;
        border-color: rgba(255, 255, 255, 0.25) !important;
        font-weight: 600 !important;
    }}
    button#ansbtn:hover {{
        background: rgba(255, 255, 255, 0.18) !important;
        border-color: rgba(255, 255, 255, 0.40) !important;
    }}

    /* Discrete Color Accents for Ease Buttons */
    button#ease1, .ease1 {{ border-color: rgba(248, 113, 113, 0.40) !important; color: #FCA5A5 !important; }}
    button#ease1:hover, .ease1:hover {{ background: rgba(248, 113, 113, 0.15) !important; border-color: #F87171 !important; color: #FFFFFF !important; }}

    button#ease2, .ease2 {{ border-color: rgba(251, 191, 36, 0.40) !important; color: #FDE047 !important; }}
    button#ease2:hover, .ease2:hover {{ background: rgba(251, 191, 36, 0.15) !important; border-color: #FBBF24 !important; color: #FFFFFF !important; }}

    button#ease3, .ease3 {{ border-color: rgba(56, 189, 248, 0.40) !important; color: #7DD3FC !important; }}
    button#ease3:hover, .ease3:hover {{ background: rgba(56, 189, 248, 0.15) !important; border-color: #38BDF8 !important; color: #FFFFFF !important; }}

    button#ease4, .ease4 {{ border-color: rgba(74, 222, 128, 0.40) !important; color: #86EFAC !important; }}
    button#ease4:hover, .ease4:hover {{ background: rgba(74, 222, 128, 0.15) !important; border-color: #4ADE80 !important; color: #FFFFFF !important; }}
    """
