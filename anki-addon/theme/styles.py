"""
High-Performance Ultra-Minimalist Void Black (#000000) & Floating Glass Styles.
Provides 100% coverage for Anki's Native Qt windows, Top Toolbar, Deck Browser, Reviewer, and Bottom Bar.
"""

from typing import Optional
from .palette import PALETTE, ThemePalette


def generate_qss(palette: ThemePalette = PALETTE, accent: Optional[str] = None) -> str:
    """
    Ultra-lightweight, zero-lag Qt StyleSheet (QSS) for Anki's native widgets.
    """
    acc = accent or palette.ACCENT_PRIMARY
    bg = palette.BACKGROUND_PURE_BLACK  # #000000
    surf = palette.BACKGROUND_SURFACE   # rgba(255, 255, 255, 0.03)
    surf_el = palette.BACKGROUND_SURFACE_ELEVATED
    surf_hov = palette.BACKGROUND_SURFACE_HOVER
    border = palette.BORDER_DEFAULT
    border_subtle = palette.BORDER_SUBTLE
    border_strong = palette.BORDER_STRONG
    text = palette.TEXT_PRIMARY
    text_sec = palette.TEXT_SECONDARY
    text_muted = palette.TEXT_MUTED

    return f"""
    /* =========================================================================
       GLOBAL VOID BLACK (#000000) BASE & MODERN INTER TYPOGRAPHY
       ========================================================================= */
    * {{
        font-family: "Inter", "Geist", -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
        outline: none;
        letter-spacing: -0.015em;
    }}

    QWidget, QMainWindow, QDialog, QFrame, QSplitter, QStackedWidget, QScrollArea, QAbstractScrollArea {{
        background-color: {bg};
        background: {bg};
        color: {text};
        selection-background-color: {acc};
        selection-color: #000000;
        border: none;
    }}

    /* Remove default gray borders on splitters and main window containers */
    QMainWindow::separator, QSplitter::handle {{
        background-color: {bg};
        width: 1px;
        height: 1px;
    }}

    /* =========================================================================
       NATIVE TOOLBARS & STATUS BARS
       ========================================================================= */
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
    QToolBar QToolButton:pressed {{
        background-color: {palette.BACKGROUND_SURFACE_ACTIVE};
    }}

    QStatusBar {{
        background-color: {bg};
        background: {bg};
        color: {text_muted};
        border-top: 1px solid {border_subtle};
    }}

    QMenuBar {{
        background-color: {bg};
        background: {bg};
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
        background-color: rgba(10, 10, 12, 0.98);
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
    QMenu::separator {{
        height: 1px;
        background-color: {border_subtle};
        margin: 4px 6px;
    }}

    /* =========================================================================
       FLOATING TRANSPARENT PILL BUTTONS
       ========================================================================= */
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
    QPushButton:disabled {{
        background-color: transparent;
        color: {palette.TEXT_DISABLED};
        border-color: {border_subtle};
    }}

    /* =========================================================================
       MINIMALIST INPUT FIELDS
       ========================================================================= */
    QLineEdit, QTextEdit, QPlainTextEdit, QSpinBox, QDoubleSpinBox, QComboBox {{
        background-color: rgba(255, 255, 255, 0.025);
        color: {text};
        border: 1px solid {border};
        border-radius: 10px;
        padding: 8px 12px;
        font-size: 13px;
    }}
    QLineEdit:focus, QTextEdit:focus, QPlainTextEdit:focus, QSpinBox:focus, QComboBox:focus {{
        border: 1px solid {palette.BORDER_FOCUS};
        background-color: rgba(255, 255, 255, 0.05);
    }}

    QComboBox::drop-down {{
        border: none;
        width: 24px;
    }}
    QComboBox QAbstractItemView {{
        background-color: rgba(10, 10, 12, 0.98);
        color: {text};
        border: 1px solid {border_strong};
        border-radius: 8px;
        padding: 4px;
        selection-background-color: rgba(255, 255, 255, 0.08);
        selection-color: #FFFFFF;
    }}

    /* =========================================================================
       GROUP BOXES & CONTAINERS
       ========================================================================= */
    QGroupBox {{
        background-color: {surf};
        border: 1px solid {border_subtle};
        border-radius: 14px;
        margin-top: 24px;
        padding: 20px 16px 16px 16px;
        font-weight: 500;
        color: {text};
    }}
    QGroupBox::title {{
        subcontrol-origin: margin;
        subcontrol-position: top left;
        left: 14px;
        top: 6px;
        padding: 0 6px;
        background-color: transparent;
        color: {text_sec};
        font-weight: 600;
    }}

    /* =========================================================================
       TABLES, LISTS & TREES
       ========================================================================= */
    QTableView, QListView, QTreeView, QTableWidget, QListWidget, QTreeWidget {{
        background-color: {bg};
        background: {bg};
        color: {text};
        border: 1px solid {border_subtle};
        border-radius: 12px;
        gridline-color: {border_subtle};
        selection-background-color: rgba(255, 255, 255, 0.06);
        selection-color: {text};
    }}
    QTableView::item:hover, QListView::item:hover, QTreeView::item:hover {{
        background-color: {surf_hov};
    }}
    QTableView::item:selected, QListView::item:selected, QTreeView::item:selected {{
        background-color: rgba(255, 255, 255, 0.08);
        color: #FFFFFF;
        font-weight: 500;
    }}
    QHeaderView::section {{
        background-color: {bg};
        background: {bg};
        color: {text_muted};
        border: none;
        border-bottom: 1px solid {border_subtle};
        border-right: 1px solid {border_subtle};
        padding: 8px 12px;
        font-weight: 500;
        font-size: 11px;
        text-transform: uppercase;
    }}

    /* =========================================================================
       SCROLLBARS
       ========================================================================= */
    QScrollBar:vertical {{
        background-color: transparent;
        width: 6px;
        margin: 0;
    }}
    QScrollBar::handle:vertical {{
        background-color: rgba(255, 255, 255, 0.12);
        min-height: 24px;
        border-radius: 3px;
        margin: 1px;
    }}
    QScrollBar::handle:vertical:hover {{
        background-color: rgba(255, 255, 255, 0.25);
    }}
    QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
        height: 0px;
    }}
    QScrollBar:horizontal {{
        background-color: transparent;
        height: 6px;
        margin: 0;
    }}
    QScrollBar::handle:horizontal {{
        background-color: rgba(255, 255, 255, 0.12);
        min-width: 24px;
        border-radius: 3px;
        margin: 1px;
    }}
    QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {{
        width: 0px;
    }}
    """


def generate_webview_css(palette: ThemePalette = PALETTE, accent: Optional[str] = None) -> str:
    """
    Generate comprehensive Void Black (#000000) and Centered Floating Glass CSS for ALL Anki WebViews:
    - Top Toolbar (Decks, Add, Browse, Stats, Sync)
    - Deck Browser (Middle Area)
    - Card Reviewer (Centered Card, Centered Image, Question, Answer)
    - Bottom Action Toolbar
    - Deck Overview & Stats
    """
    acc = accent or palette.ACCENT_PRIMARY
    bg = palette.BACKGROUND_PURE_BLACK  # #000000
    border = palette.BORDER_DEFAULT
    border_subtle = palette.BORDER_SUBTLE
    border_strong = palette.BORDER_STRONG
    text = palette.TEXT_PRIMARY
    text_sec = palette.TEXT_SECONDARY
    text_muted = palette.TEXT_MUTED

    return f"""
    /* =========================================================================
       TOTAL VOID BLACK (#000000) RESET FOR ALL ANKI DOM & SHADOW DOM
       ========================================================================= */
    :root, html, body, #outer, #main, #main-content, #header, #footer, #qa, #content,
    header, nav, .navbar, .toolbar, #toolbar, #deckbrowser, .deck-table, table,
    #overview, .overview, #stats, .stats, #bottomWeb, .nightMode, body.nightMode,
    body:not(.nightMode), [data-bs-theme="dark"], [data-bs-theme="light"] {{
        --canvas: {bg} !important;
        --surface: {bg} !important;
        --surface-ground: {bg} !important;
        --surface-card: rgba(255, 255, 255, 0.025) !important;
        --surface-overlay: rgba(14, 14, 16, 0.98) !important;
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
    }}

    /* Global Scrollbar */
    ::-webkit-scrollbar {{
        width: 6px !important;
        height: 6px !important;
        background: transparent !important;
    }}
    ::-webkit-scrollbar-thumb {{
        background: rgba(255, 255, 255, 0.12) !important;
        border-radius: 3px !important;
    }}
    ::-webkit-scrollbar-thumb:hover {{
        background: rgba(255, 255, 255, 0.25) !important;
    }}

    /* =========================================================================
       1. TOP TOOLBAR WEBVIEW (Decks, Add, Browse, Stats, Sync)
       ========================================================================= */
    #header, header, .toolbar, nav.navbar, #toolbar {{
        background-color: {bg} !important;
        background: {bg} !important;
        border-bottom: 1px solid {border_subtle} !important;
        padding: 6px 14px !important;
        display: flex !important;
        align-items: center !important;
        justify-content: space-between !important;
    }}

    /* Toolbar navigation items rendered as floating glass pills */
    .toolbar a, nav.navbar a, .nav-link, a.nav-link, .toolbar button, .toolbar-button {{
        background: rgba(255, 255, 255, 0.035) !important;
        color: {text_sec} !important;
        border: 1px solid rgba(255, 255, 255, 0.07) !important;
        border-radius: 18px !important;
        padding: 6px 16px !important;
        margin: 0 4px !important;
        font-size: 13px !important;
        font-weight: 500 !important;
        text-decoration: none !important;
        transition: all 0.1s ease !important;
        display: inline-flex !important;
        align-items: center !important;
    }}

    .toolbar a:hover, nav.navbar a:hover, .nav-link:hover, a.nav-link:hover, .toolbar button:hover {{
        background: rgba(255, 255, 255, 0.08) !important;
        color: #FFFFFF !important;
        border-color: rgba(255, 255, 255, 0.16) !important;
    }}

    /* =========================================================================
       2. DECK BROWSER (MIDDLE LIST OF DECKS)
       ========================================================================= */
    #deckbrowser, .deck-table, table.deck-table {{
        background-color: {bg} !important;
        background: {bg} !important;
        border-collapse: separate !important;
        border-spacing: 0 4px !important;
        width: 100% !important;
        max-width: 880px !important;
        margin: 16px auto !important;
    }}

    /* Floating Glass Deck Row */
    tr.deck {{
        background-color: rgba(255, 255, 255, 0.02) !important;
        background: rgba(255, 255, 255, 0.02) !important;
        border: 1px solid rgba(255, 255, 255, 0.06) !important;
        border-radius: 12px !important;
        transition: all 0.1s ease !important;
    }}

    tr.deck:hover {{
        background-color: rgba(255, 255, 255, 0.05) !important;
        background: rgba(255, 255, 255, 0.05) !important;
        border-color: rgba(255, 255, 255, 0.12) !important;
    }}

    td.decktd {{
        padding: 12px 16px !important;
        border: none !important;
    }}

    a.deckname {{
        color: {text} !important;
        font-weight: 500 !important;
        text-decoration: none !important;
        font-size: 14px !important;
        letter-spacing: -0.01em !important;
    }}

    a.deckname:hover {{
        color: {acc} !important;
    }}

    /* Minimalist Counters */
    .new-count, .count-new, .new-count-badge {{
        color: #38BDF8 !important;
        font-weight: 600 !important;
        font-family: "JetBrains Mono", monospace !important;
        font-size: 13px !important;
    }}
    .learn-count, .count-learn, .learn-count-badge {{
        color: #FBBF24 !important;
        font-weight: 600 !important;
        font-family: "JetBrains Mono", monospace !important;
        font-size: 13px !important;
    }}
    .review-count, .count-review, .review-count-badge {{
        color: #4ADE80 !important;
        font-weight: 600 !important;
        font-family: "JetBrains Mono", monospace !important;
        font-size: 13px !important;
    }}

    /* Study Deck Action Buttons in Deck Browser */
    #deckbrowser button, #deckbrowser .btn, #deckbrowser input[type="button"] {{
        background: rgba(255, 255, 255, 0.04) !important;
        color: {text} !important;
        border: 1px solid rgba(255, 255, 255, 0.08) !important;
        border-radius: 18px !important;
        padding: 6px 18px !important;
        font-size: 13px !important;
        font-weight: 500 !important;
        cursor: pointer !important;
    }}

    /* =========================================================================
       3. CARD REVIEWER (CENTERED CARD, CENTERED IMAGES & TYPOGRAPHY)
       ========================================================================= */
    body#body, html, body {{
        min-height: 100vh !important;
        display: flex !important;
        flex-direction: column !important;
        justify-content: center !important;
        align-items: center !important;
        margin: 0 !important;
        padding: 0 !important;
        text-align: center !important;
    }}

    #qa {{
        width: 100% !important;
        max-width: 860px !important;
        display: flex !important;
        flex-direction: column !important;
        align-items: center !important;
        justify-content: center !important;
        text-align: center !important;
        margin: 0 auto !important;
        padding: 24px 16px !important;
    }}

    /* Centered Floating Glass Card */
    .card {{
        width: 100% !important;
        max-width: 860px !important;
        margin: 0 auto !important;
        text-align: center !important;
        display: flex !important;
        flex-direction: column !important;
        align-items: center !important;
        justify-content: center !important;
        background: rgba(255, 255, 255, 0.025) !important;
        background-color: rgba(255, 255, 255, 0.025) !important;
        border: 1px solid rgba(255, 255, 255, 0.08) !important;
        border-radius: 20px !important;
        padding: 38px 32px !important;
        box-shadow: 0 24px 60px rgba(0, 0, 0, 0.95) !important;
    }}

    /* Perfectly Centered Images */
    img {{
        margin: 18px auto !important;
        display: block !important;
        max-width: 100% !important;
        max-height: 520px !important;
        height: auto !important;
        object-fit: contain !important;
        border-radius: 14px !important;
        border: 1px solid rgba(255, 255, 255, 0.08) !important;
        box-shadow: 0 12px 36px rgba(0, 0, 0, 0.8) !important;
    }}

    /* Centered Questions & Paragraphs */
    .card p, .card div, .card h1, .card h2, .card h3 {{
        text-align: center !important;
        margin-left: auto !important;
        margin-right: auto !important;
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

    /* Code Blocks */
    pre, code {{
        background-color: rgba(255, 255, 255, 0.03) !important;
        border: 1px solid {border_subtle} !important;
        color: #E4E4E7 !important;
        border-radius: 8px !important;
        padding: 3px 8px !important;
        font-family: "JetBrains Mono", Consolas, monospace !important;
        font-size: 13px !important;
        text-align: left !important;
        margin: 12px auto !important;
    }}
    pre code {{
        padding: 14px !important;
        display: block !important;
    }}

    /* =========================================================================
       4. BOTTOM ACTION BAR & FLOATING PILL BUTTONS (Again, Hard, Good, Easy)
       ========================================================================= */
    #bottomWeb, #outer, #bottomBar, footer {{
        background-color: {bg} !important;
        background: {bg} !important;
        border-top: 1px solid rgba(255, 255, 255, 0.06) !important;
        padding: 8px 12px !important;
        display: flex !important;
        justify-content: center !important;
        align-items: center !important;
    }}

    /* Floating Pill Answer Buttons */
    #bottomWeb button, .nobootstrap button, button.ease-button, button.btn, button#ease1, button#ease2, button#ease3, button#ease4, button#ansbtn {{
        background: rgba(255, 255, 255, 0.04) !important;
        color: {text} !important;
        border: 1px solid rgba(255, 255, 255, 0.10) !important;
        border-radius: 20px !important;
        padding: 9px 24px !important;
        margin: 0 6px !important;
        font-weight: 500 !important;
        font-size: 13px !important;
        cursor: pointer !important;
        transition: all 0.1s ease !important;
    }}

    #bottomWeb button:hover, button.ease-button:hover, button#ansbtn:hover {{
        background: rgba(255, 255, 255, 0.10) !important;
        border-color: rgba(255, 255, 255, 0.22) !important;
        color: #FFFFFF !important;
    }}

    /* Ease ratings subtle accent borders */
    button#ease1, .ease1 {{ border-color: rgba(248, 113, 113, 0.25) !important; }}
    button#ease2, .ease2 {{ border-color: rgba(251, 191, 36, 0.25) !important; }}
    button#ease3, .ease3 {{ border-color: rgba(56, 189, 248, 0.25) !important; }}
    button#ease4, .ease4 {{ border-color: rgba(74, 222, 128, 0.25) !important; }}
    """
