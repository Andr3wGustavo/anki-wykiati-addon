"""
Pure, Minimalist Void Black (#000000) Color Stylesheet Engine.
Non-destructive: preserves 100% of native Anki layout, tables, icons, and positioning while applying pure black theme.
"""

from typing import Optional
from .palette import PALETTE, ThemePalette


def generate_qss(palette: ThemePalette = PALETTE, accent: Optional[str] = None) -> str:
    """
    Clean, Minimalist Qt StyleSheet (QSS) for native Anki windows and dialogs.
    Applies pure void black and clean borders without altering layout.
    """
    acc = accent or palette.ACCENT_PRIMARY
    bg = palette.BACKGROUND_PURE_BLACK  # #000000
    border_subtle = palette.BORDER_SUBTLE
    border_strong = palette.BORDER_STRONG
    text = palette.TEXT_PRIMARY
    text_sec = palette.TEXT_SECONDARY
    text_muted = palette.TEXT_MUTED

    return f"""
    /* =========================================================================
       NATIVE ANKI WIDGETS - CLEAN VOID BLACK COLOR PALETTE
       ========================================================================= */
    QMainWindow, QDialog, QFrame, QSplitter, QStackedWidget, QScrollArea, QAbstractScrollArea {{
        background-color: {bg};
        color: {text};
        selection-background-color: {acc};
        selection-color: #000000;
    }}

    /* Menu Bars & Menus */
    QMenuBar {{
        background-color: {bg};
        color: {text_sec};
        border-bottom: 1px solid {border_subtle};
    }}
    QMenuBar::item:selected {{
        background-color: rgba(255, 255, 255, 0.08);
        color: {text};
    }}
    QMenu {{
        background-color: #0C0C0E;
        color: {text};
        border: 1px solid {border_strong};
        padding: 4px;
    }}
    QMenu::item {{
        padding: 6px 20px 6px 10px;
        color: {text_sec};
    }}
    QMenu::item:selected {{
        background-color: rgba(255, 255, 255, 0.08);
        color: {text};
    }}

    /* Toolbars */
    QToolBar {{
        background-color: {bg};
        border-bottom: 1px solid {border_subtle};
    }}
    QToolBar QToolButton {{
        background-color: rgba(255, 255, 255, 0.04);
        color: {text_sec};
        border: 1px solid {border_subtle};
        border-radius: 4px;
        padding: 4px 10px;
    }}
    QToolBar QToolButton:hover {{
        background-color: rgba(255, 255, 255, 0.09);
        color: {text};
    }}

    /* Native Standard Buttons */
    QPushButton {{
        background-color: rgba(255, 255, 255, 0.05);
        color: {text};
        border: 1px solid {border_subtle};
        border-radius: 4px;
        padding: 5px 14px;
    }}
    QPushButton:hover {{
        background-color: rgba(255, 255, 255, 0.10);
        color: #FFFFFF;
        border-color: {border_strong};
    }}
    QPushButton:pressed {{
        background-color: rgba(255, 255, 255, 0.02);
    }}
    QPushButton:default, QPushButton[primary="true"] {{
        background-color: rgba(255, 255, 255, 0.15);
        color: #FFFFFF;
        border: 1px solid rgba(255, 255, 255, 0.35);
        font-weight: 600;
    }}
    QPushButton:default:hover, QPushButton[primary="true"]:hover {{
        background-color: rgba(255, 255, 255, 0.22);
        border-color: rgba(255, 255, 255, 0.50);
    }}

    /* Input Fields */
    QLineEdit, QTextEdit, QPlainTextEdit, QSpinBox, QComboBox {{
        background-color: #08080A;
        color: {text};
        border: 1px solid {border_subtle};
        border-radius: 4px;
        padding: 5px 8px;
    }}
    QLineEdit:focus, QTextEdit:focus, QPlainTextEdit:focus, QSpinBox:focus, QComboBox:focus {{
        border: 1px solid {palette.BORDER_FOCUS};
        background-color: #0E0E12;
    }}

    /* Group Boxes */
    QGroupBox {{
        background-color: transparent;
        border: 1px solid {border_subtle};
        border-radius: 4px;
        margin-top: 10px;
        padding-top: 10px;
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
        gridline-color: {border_subtle};
        selection-background-color: rgba(255, 255, 255, 0.08);
        selection-color: {text};
    }}
    QHeaderView::section {{
        background-color: {bg};
        color: {text_muted};
        border: none;
        border-bottom: 1px solid {border_subtle};
        padding: 5px 8px;
    }}

    /* Slim Scrollbars */
    QScrollBar:vertical {{
        background: transparent;
        width: 6px;
        margin: 0;
    }}
    QScrollBar::handle:vertical {{
        background-color: rgba(255, 255, 255, 0.15);
        min-height: 20px;
        border-radius: 3px;
    }}
    QScrollBar::handle:vertical:hover {{
        background-color: rgba(255, 255, 255, 0.28);
    }}
    QScrollBar:horizontal {{
        background: transparent;
        height: 6px;
        margin: 0;
    }}
    QScrollBar::handle:horizontal {{
        background-color: rgba(255, 255, 255, 0.15);
        min-width: 20px;
        border-radius: 3px;
    }}
    """


def generate_webview_css(palette: ThemePalette = PALETTE, accent: Optional[str] = None) -> str:
    """
    Pure, Minimalist Void Black (#000000) CSS for Anki WebViews.
    Changes ONLY the colors:
    - Pure black (#000000) canvas and backgrounds
    - Crisp high-contrast text
    - Preserves 100% of native Anki layout, tables, buttons, and centering
    """
    acc = accent or palette.ACCENT_PRIMARY
    bg = palette.BACKGROUND_PURE_BLACK  # #000000
    border_subtle = palette.BORDER_SUBTLE
    text = palette.TEXT_PRIMARY
    text_sec = palette.TEXT_SECONDARY
    text_muted = palette.TEXT_MUTED

    return f"""
    /* =========================================================================
       1. NATIVE ANKI CSS VARIABLES - VOID BLACK PALETTE
       ========================================================================= */
    :root, .nightMode, body.nightMode {{
        --canvas: {bg} !important;
        --surface: {bg} !important;
        --surface-ground: {bg} !important;
        --surface-card: {bg} !important;
        --surface-overlay: {bg} !important;
        --fg: {text} !important;
        --fg-muted: {text_sec} !important;
        --fg-faint: {text_muted} !important;
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

    /* 2. BACKGROUNDS & BASE COLOR */
    html, body {{
        background-color: {bg} !important;
        background: {bg} !important;
        color: {text} !important;
    }}

    #header, header, .toolbar, #toolbar, nav.navbar,
    #deckbrowser, .deck-table,
    #qa, .card,
    #bottomWeb, body#bottomWeb, #bottomBar, footer {{
        background-color: {bg} !important;
        background: {bg} !important;
        color: {text} !important;
    }}

    /* 3. DECK BROWSER ROWS & LINKS */
    tr.deck {{
        background-color: {bg} !important;
    }}
    a, a.deckname, a.deck {{
        color: {text} !important;
    }}
    a:hover, a.deckname:hover, a.deck:hover {{
        color: #FFFFFF !important;
    }}

    /* 4. BUTTONS & TOOLBAR ITEMS (Pure Color, Native Dimensions) */
    button, .toolbar a, .nav-link {{
        background-color: rgba(255, 255, 255, 0.05) !important;
        color: {text} !important;
        border: 1px solid {border_subtle} !important;
        border-radius: 4px !important;
    }}
    button:hover, .toolbar a:hover, .nav-link:hover {{
        background-color: rgba(255, 255, 255, 0.12) !important;
        color: #FFFFFF !important;
        border-color: rgba(255, 255, 255, 0.25) !important;
    }}

    /* 5. MINIMALIST COUNTER BADGES */
    .new-count, .count-new, .new-count-badge {{
        color: #38BDF8 !important;
        font-weight: 600 !important;
    }}
    .learn-count, .count-learn, .learn-count-badge {{
        color: #FBBF24 !important;
        font-weight: 600 !important;
    }}
    .review-count, .count-review, .review-count-badge {{
        color: #4ADE80 !important;
        font-weight: 600 !important;
    }}

    /* 6. CLOZE & CODE BLOCKS */
    .cloze {{
        color: #38BDF8 !important;
        font-weight: 600 !important;
    }}
    code, pre {{
        background-color: rgba(255, 255, 255, 0.05) !important;
        color: #E4E4E7 !important;
        border-radius: 3px !important;
    }}

    /* 7. EASE RATING BUTTON ACCENTS */
    button#ease1, .ease1 {{ border-color: rgba(248, 113, 113, 0.40) !important; color: #FCA5A5 !important; }}
    button#ease1:hover, .ease1:hover {{ background-color: rgba(248, 113, 113, 0.15) !important; border-color: #F87171 !important; color: #FFFFFF !important; }}

    button#ease2, .ease2 {{ border-color: rgba(251, 191, 36, 0.40) !important; color: #FDE047 !important; }}
    button#ease2:hover, .ease2:hover {{ background-color: rgba(251, 191, 36, 0.15) !important; border-color: #FBBF24 !important; color: #FFFFFF !important; }}

    button#ease3, .ease3 {{ border-color: rgba(56, 189, 248, 0.40) !important; color: #7DD3FC !important; }}
    button#ease3:hover, .ease3:hover {{ background-color: rgba(56, 189, 248, 0.15) !important; border-color: #38BDF8 !important; color: #FFFFFF !important; }}

    button#ease4, .ease4 {{ border-color: rgba(74, 222, 128, 0.40) !important; color: #86EFAC !important; }}
    button#ease4:hover, .ease4:hover {{ background-color: rgba(74, 222, 128, 0.15) !important; border-color: #4ADE80 !important; color: #FFFFFF !important; }}

    /* 8. CLEAN SCROLLBARS */
    ::-webkit-scrollbar {{
        width: 6px !important;
        height: 6px !important;
        background: transparent !important;
    }}
    ::-webkit-scrollbar-thumb {{
        background: rgba(255, 255, 255, 0.15) !important;
        border-radius: 3px !important;
    }}
    ::-webkit-scrollbar-thumb:hover {{
        background: rgba(255, 255, 255, 0.28) !important;
    }}
    """
