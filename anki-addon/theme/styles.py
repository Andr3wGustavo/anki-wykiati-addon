"""
Adaptive Minimalist Stylesheet Engine for Anki Wykiati Toolkit.
Intelligently adapts contrast (dark vs light) based on background luminance.
Non-destructive: preserves 100% of native Anki layout, tables, icons, and positioning.
"""

from typing import Optional
from .palette import PALETTE, ThemePalette, get_adaptive_palette, is_light_color


def generate_qss(palette: Optional[ThemePalette] = None, accent: Optional[str] = None, bg_color: Optional[str] = None) -> str:
    """
    Generate Qt StyleSheet (QSS) for native Anki windows and dialogs.
    Dynamically adapts font colors, input borders, buttons, and selection highlights
    based on the luminance of the chosen background.
    """
    bg = bg_color or PALETTE.BACKGROUND_PURE_BLACK
    is_light = is_light_color(bg)
    pal = palette or get_adaptive_palette(bg)
    acc = accent or pal.ACCENT_PRIMARY

    # Adaptive tokens
    if is_light:
        text = "#09090B"
        text_sec = "#27272A"
        text_muted = "#71717A"
        surface_card = "rgba(0, 0, 0, 0.035)"
        surface_card_title_bg = "rgba(0, 0, 0, 0.08)"
        border_subtle = "rgba(0, 0, 0, 0.10)"
        border_strong = "rgba(0, 0, 0, 0.22)"
        border_focus = "rgba(0, 0, 0, 0.50)"
        input_bg = "#FFFFFF"
        btn_glass_bg = "rgba(0, 0, 0, 0.05)"
        btn_glass_hover = "rgba(0, 0, 0, 0.10)"
        btn_glass_pressed = "rgba(0, 0, 0, 0.16)"
        btn_primary_bg = "#09090B"
        btn_primary_text = "#FFFFFF"
        btn_primary_hover = "#27272A"
        item_hover_bg = "rgba(0, 0, 0, 0.06)"
        item_selected_bg = "rgba(0, 0, 0, 0.12)"
        item_selected_text = "#000000"
        menu_bg = "#FFFFFF"
        scrollbar_handle = "rgba(0, 0, 0, 0.22)"
        scrollbar_hover = "rgba(0, 0, 0, 0.40)"
        chk_indicator_bg = "#FFFFFF"
        chk_indicator_border = "rgba(0, 0, 0, 0.30)"
    else:
        text = "#FFFFFF"
        text_sec = "#E4E4E7"
        text_muted = "#A1A1AA"
        surface_card = "rgba(255, 255, 255, 0.03)"
        surface_card_title_bg = "rgba(255, 255, 255, 0.08)"
        border_subtle = "rgba(255, 255, 255, 0.08)"
        border_strong = "rgba(255, 255, 255, 0.18)"
        border_focus = "rgba(255, 255, 255, 0.45)"
        input_bg = "#060608"
        btn_glass_bg = "rgba(255, 255, 255, 0.05)"
        btn_glass_hover = "rgba(255, 255, 255, 0.12)"
        btn_glass_pressed = "rgba(255, 255, 255, 0.02)"
        btn_primary_bg = "#FFFFFF"
        btn_primary_text = "#000000"
        btn_primary_hover = "#E4E4E7"
        item_hover_bg = "rgba(255, 255, 255, 0.08)"
        item_selected_bg = "rgba(255, 255, 255, 0.16)"
        item_selected_text = "#FFFFFF"
        menu_bg = "#0C0C0E"
        scrollbar_handle = "rgba(255, 255, 255, 0.18)"
        scrollbar_hover = "rgba(255, 255, 255, 0.35)"
        chk_indicator_bg = "#060608"
        chk_indicator_border = "rgba(255, 255, 255, 0.25)"

    return f"""
    /* =========================================================================
       NATIVE ANKI WIDGETS - ADAPTIVE CONTRAST & MINIMALIST GLASS
       ========================================================================= */
    QMainWindow, QDialog, QFrame, QSplitter, QStackedWidget, QScrollArea, QAbstractScrollArea {{
        background-color: {bg};
        color: {text};
        selection-background-color: {item_selected_bg};
        selection-color: {item_selected_text};
    }}

    /* Menu Bars & Dropdowns */
    QMenuBar {{
        background-color: {bg};
        color: {text_sec};
        border-bottom: 1px solid {border_subtle};
    }}
    QMenuBar::item:selected {{
        background-color: {item_hover_bg};
        color: {text};
    }}
    QMenu {{
        background-color: {menu_bg};
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
        background-color: {item_selected_bg};
        color: {item_selected_text};
    }}

    /* Toolbars */
    QToolBar {{
        background-color: {bg};
        border-bottom: 1px solid {border_subtle};
    }}
    QToolBar QToolButton {{
        background-color: {btn_glass_bg};
        color: {text_sec};
        border: 1px solid {border_subtle};
        border-radius: 6px;
        padding: 5px 12px;
    }}
    QToolBar QToolButton:hover {{
        background-color: {btn_glass_hover};
        color: {text};
    }}

    /* Modern Minimalist Glass Buttons */
    QPushButton {{
        background-color: {btn_glass_bg};
        color: {text_sec};
        border: 1px solid {border_subtle};
        border-radius: 6px;
        padding: 7px 18px;
        font-size: 13px;
        font-weight: 500;
    }}
    QPushButton:hover {{
        background-color: {btn_glass_hover};
        color: {text};
        border-color: {border_strong};
    }}
    QPushButton:pressed {{
        background-color: {btn_glass_pressed};
    }}
    QPushButton:default, QPushButton[primary="true"] {{
        background-color: {btn_primary_bg};
        color: {btn_primary_text};
        border: 1px solid {btn_primary_bg};
        font-weight: 600;
    }}
    QPushButton:default:hover, QPushButton[primary="true"]:hover {{
        background-color: {btn_primary_hover};
        border-color: {btn_primary_hover};
        color: {btn_primary_text};
    }}

    /* Sleek Input Fields */
    QLineEdit, QTextEdit, QPlainTextEdit, QSpinBox, QComboBox {{
        background-color: {input_bg};
        color: {text};
        border: 1px solid {border_subtle};
        border-radius: 6px;
        padding: 7px 10px;
        font-size: 13px;
    }}
    QLineEdit:focus, QTextEdit:focus, QPlainTextEdit:focus, QSpinBox:focus, QComboBox:focus {{
        border: 1px solid {border_focus};
    }}

    /* Combobox Dropdown View */
    QComboBox QAbstractItemView {{
        background-color: {menu_bg};
        color: {text};
        border: 1px solid {border_strong};
        border-radius: 6px;
        padding: 4px;
        selection-background-color: {item_selected_bg};
        selection-color: {item_selected_text};
        outline: none;
    }}
    QComboBox QAbstractItemView::item {{
        padding: 6px 10px;
        border-radius: 4px;
    }}
    QComboBox QAbstractItemView::item:hover {{
        background-color: {item_hover_bg};
        color: {text};
    }}
    QComboBox QAbstractItemView::item:selected {{
        background-color: {item_selected_bg};
        color: {item_selected_text};
        font-weight: 600;
    }}

    /* Minimalist Section Card Group Boxes */
    QGroupBox {{
        background-color: {surface_card};
        border: 1px solid {border_subtle};
        border-radius: 8px;
        margin-top: 14px;
        padding: 16px 14px 14px 14px;
        font-weight: 600;
        font-size: 12px;
        color: {text};
    }}
    QGroupBox::title {{
        subcontrol-origin: margin;
        subcontrol-position: top left;
        left: 12px;
        padding: 2px 8px;
        background-color: {surface_card_title_bg};
        border-radius: 4px;
        color: {text};
    }}

    /* CheckBoxes */
    QCheckBox {{
        color: {text};
        font-size: 13px;
        spacing: 8px;
    }}
    QCheckBox::indicator {{
        width: 16px;
        height: 16px;
        border: 1px solid {chk_indicator_border};
        border-radius: 4px;
        background-color: {chk_indicator_bg};
    }}
    QCheckBox::indicator:checked {{
        background-color: {btn_primary_bg};
        border-color: {btn_primary_bg};
    }}
    QCheckBox::indicator:hover {{
        border-color: {border_focus};
    }}

    /* Tables, Lists, and Tree Views (Fixed Selection & Hover) */
    QTableView, QListView, QTreeView, QTableWidget, QListWidget, QTreeWidget {{
        background-color: {bg};
        color: {text};
        border: 1px solid {border_subtle};
        border-radius: 6px;
        gridline-color: {border_subtle};
        selection-background-color: {item_selected_bg};
        selection-color: {item_selected_text};
        outline: none;
    }}
    QTableView::item, QListView::item, QTreeView::item, QTableWidget::item, QListWidget::item, QTreeWidget::item {{
        padding: 6px 8px;
        border: none;
        border-radius: 4px;
        color: {text};
    }}
    QTableView::item:hover, QListView::item:hover, QTreeView::item:hover, QTableWidget::item:hover, QListWidget::item:hover, QTreeWidget::item:hover {{
        background-color: {item_hover_bg};
        color: {text};
    }}
    QTableView::item:selected, QListView::item:selected, QTreeView::item:selected, QTableWidget::item:selected, QListWidget::item:selected, QTreeWidget::item:selected {{
        background-color: {item_selected_bg};
        color: {item_selected_text};
        font-weight: 600;
    }}
    QHeaderView::section {{
        background-color: {bg};
        color: {text_muted};
        border: none;
        border-bottom: 1px solid {border_subtle};
        padding: 6px 8px;
        font-weight: 600;
        font-size: 11px;
    }}

    /* Slim Smooth Scrollbars */
    QScrollBar:vertical {{
        background: transparent;
        width: 6px;
        margin: 0;
    }}
    QScrollBar::handle:vertical {{
        background-color: {scrollbar_handle};
        min-height: 20px;
        border-radius: 3px;
    }}
    QScrollBar::handle:vertical:hover {{
        background-color: {scrollbar_hover};
    }}
    QScrollBar:horizontal {{
        background: transparent;
        height: 6px;
        margin: 0;
    }}
    QScrollBar::handle:horizontal {{
        background-color: {scrollbar_handle};
        min-width: 20px;
        border-radius: 3px;
    }}
    QScrollBar::handle:horizontal:hover {{
        background-color: {scrollbar_hover};
    }}
    """


def generate_webview_css(palette: Optional[ThemePalette] = None, accent: Optional[str] = None, bg_color: Optional[str] = None) -> str:
    """
    Adaptive Custom Background CSS for Anki WebViews.
    Dynamically adjusts CSS variables and element colors for dark and light backgrounds.
    """
    bg = bg_color or PALETTE.BACKGROUND_PURE_BLACK
    is_light = is_light_color(bg)
    pal = palette or get_adaptive_palette(bg)
    acc = accent or pal.ACCENT_PRIMARY

    if is_light:
        text = "#09090B"
        text_sec = "#27272A"
        text_muted = "#71717A"
        border_subtle = "rgba(0, 0, 0, 0.10)"
        btn_bg = "rgba(0, 0, 0, 0.05)"
        btn_hover = "rgba(0, 0, 0, 0.10)"
        code_bg = "rgba(0, 0, 0, 0.05)"
        code_color = "#18181B"
        scrollbar_thumb = "rgba(0, 0, 0, 0.20)"
        scrollbar_hover = "rgba(0, 0, 0, 0.38)"
    else:
        text = "#FFFFFF"
        text_sec = "#E4E4E7"
        text_muted = "#A1A1AA"
        border_subtle = "rgba(255, 255, 255, 0.08)"
        btn_bg = "rgba(255, 255, 255, 0.05)"
        btn_hover = "rgba(255, 255, 255, 0.12)"
        code_bg = "rgba(255, 255, 255, 0.05)"
        code_color = "#E4E4E7"
        scrollbar_thumb = "rgba(255, 255, 255, 0.15)"
        scrollbar_hover = "rgba(255, 255, 255, 0.28)"

    return f"""
    /* =========================================================================
       1. NATIVE ANKI CSS VARIABLES - ADAPTIVE CONTRAST
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
        color: {text_sec} !important;
    }}

    /* 4. BUTTONS & TOOLBAR ITEMS */
    button, .toolbar a, .nav-link {{
        background-color: {btn_bg} !important;
        color: {text} !important;
        border: 1px solid {border_subtle} !important;
        border-radius: 4px !important;
    }}
    button:hover, .toolbar a:hover, .nav-link:hover {{
        background-color: {btn_hover} !important;
        color: {text} !important;
        border-color: {border_subtle} !important;
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
        background-color: {code_bg} !important;
        color: {code_color} !important;
        border-radius: 3px !important;
    }}

    /* 7. EASE RATING BUTTON ACCENTS */
    button#ease1, .ease1 {{ border-color: rgba(248, 113, 113, 0.40) !important; color: #FCA5A5 !important; }}
    button#ease1:hover, .ease1:hover {{ background-color: rgba(248, 113, 113, 0.15) !important; border-color: #F87171 !important; color: {text} !important; }}

    button#ease2, .ease2 {{ border-color: rgba(251, 191, 36, 0.40) !important; color: #FDE047 !important; }}
    button#ease2:hover, .ease2:hover {{ background-color: rgba(251, 191, 36, 0.15) !important; border-color: #FBBF24 !important; color: {text} !important; }}

    button#ease3, .ease3 {{ border-color: rgba(56, 189, 248, 0.40) !important; color: #7DD3FC !important; }}
    button#ease3:hover, .ease3:hover {{ background-color: rgba(56, 189, 248, 0.15) !important; border-color: #38BDF8 !important; color: {text} !important; }}

    button#ease4, .ease4 {{ border-color: rgba(74, 222, 128, 0.40) !important; color: #86EFAC !important; }}
    button#ease4:hover, .ease4:hover {{ background-color: rgba(74, 222, 128, 0.15) !important; border-color: #4ADE80 !important; color: {text} !important; }}

    /* 8. CLEAN SCROLLBARS */
    ::-webkit-scrollbar {{
        width: 6px !important;
        height: 6px !important;
        background: transparent !important;
    }}
    ::-webkit-scrollbar-thumb {{
        background: {scrollbar_thumb} !important;
        border-radius: 3px !important;
    }}
    ::-webkit-scrollbar-thumb:hover {{
        background: {scrollbar_hover} !important;
    }}
    """

