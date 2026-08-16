"""
Pure, Minimalist Void Black (#000000) Color Stylesheet Engine.
Non-destructive: preserves 100% of native Anki layout, tables, icons, and positioning while applying pure black theme.
"""

from typing import Optional
from .palette import PALETTE, ThemePalette


def generate_qss(palette: ThemePalette = PALETTE, accent: Optional[str] = None, bg_color: Optional[str] = None) -> str:
    """
    Clean, Minimalist Qt StyleSheet (QSS) for native Anki windows and dialogs.
    Applies custom RGB background color (default #000000) and clean glass borders.
    """
    acc = accent or palette.ACCENT_PRIMARY
    bg = bg_color or palette.BACKGROUND_PURE_BLACK  # #000000 by default or custom RGB
    border_subtle = palette.BORDER_SUBTLE
    border_strong = palette.BORDER_STRONG
    text = palette.TEXT_PRIMARY
    text_sec = palette.TEXT_SECONDARY
    text_muted = palette.TEXT_MUTED

    return f"""
    /* =========================================================================
       NATIVE ANKI WIDGETS - CLEAN VOID BLACK COLOR PALETTE & SQUARE GLASS
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
        border-radius: 6px;
    }}
    QMenu::item {{
        padding: 6px 20px 6px 10px;
        color: {text_sec};
        border-radius: 4px;
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
        border-radius: 6px;
        padding: 5px 12px;
    }}
    QToolBar QToolButton:hover {{
        background-color: rgba(255, 255, 255, 0.09);
        color: {text};
    }}

    /* Modern Minimalist Glass Buttons */
    QPushButton {{
        background-color: rgba(255, 255, 255, 0.05);
        color: {text_sec};
        border: 1px solid {border_subtle};
        border-radius: 6px;
        padding: 7px 18px;
        font-size: 13px;
        font-weight: 500;
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
        background-color: #FFFFFF;
        color: #000000;
        border: 1px solid #FFFFFF;
        font-weight: 600;
    }}
    QPushButton:default:hover, QPushButton[primary="true"]:hover {{
        background-color: #E4E4E7;
        border-color: #E4E4E7;
        color: #000000;
    }}

    /* Modern Sleek Input Fields */
    QLineEdit, QTextEdit, QPlainTextEdit, QSpinBox, QComboBox {{
        background-color: #060608;
        color: {text};
        border: 1px solid {border_subtle};
        border-radius: 6px;
        padding: 7px 10px;
        font-size: 13px;
    }}
    QLineEdit:focus, QTextEdit:focus, QPlainTextEdit:focus, QSpinBox:focus, QComboBox:focus {{
        border: 1px solid {palette.BORDER_FOCUS};
        background-color: #0B0B0F;
    }}

    /* Modern Minimalist Section Card Group Boxes */
    QGroupBox {{
        background-color: rgba(255, 255, 255, 0.025);
        border: 1px solid {border_subtle};
        border-radius: 8px;
        margin-top: 14px;
        padding: 16px 14px 14px 14px;
        font-weight: 600;
        font-size: 12px;
        color: #FFFFFF;
    }}
    QGroupBox::title {{
        subcontrol-origin: margin;
        subcontrol-position: top left;
        left: 12px;
        padding: 0 6px;
        background-color: #0A0A0E;
        border-radius: 4px;
        color: {text_sec};
    }}

    /* Modern CheckBoxes */
    QCheckBox {{
        color: {text};
        font-size: 13px;
        spacing: 8px;
    }}
    QCheckBox::indicator {{
        width: 16px;
        height: 16px;
        border: 1px solid rgba(255, 255, 255, 0.20);
        border-radius: 4px;
        background-color: #060608;
    }}
    QCheckBox::indicator:checked {{
        background-color: #FFFFFF;
        border-color: #FFFFFF;
    }}
    QCheckBox::indicator:hover {{
        border-color: rgba(255, 255, 255, 0.50);
    }}

    /* Tables and Lists */
    QTableView, QListView, QTreeView, QTableWidget, QListWidget, QTreeWidget {{
        background-color: {bg};
        color: {text};
        border: 1px solid {border_subtle};
        border-radius: 6px;
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


def generate_webview_css(palette: ThemePalette = PALETTE, accent: Optional[str] = None, bg_color: Optional[str] = None) -> str:
    """
    Pure, Minimalist Custom Background (#000000 by default or custom RGB) CSS for Anki WebViews.
    Changes ONLY the colors:
    - Pure black / custom RGB background canvas and backgrounds
    - Crisp high-contrast text
    - Preserves 100% of native Anki layout, tables, buttons, and centering
    """
    acc = accent or palette.ACCENT_PRIMARY
    bg = bg_color or palette.BACKGROUND_PURE_BLACK  # #000000 by default or custom RGB
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
