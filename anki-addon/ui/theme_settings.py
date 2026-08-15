"""
Theme Settings Dialog for Anki Wykiati Toolkit.
Allows toggling Full Black AMOLED (#000000) and customizing iOS accent colors.
"""

from typing import Any, Optional

try:
    from ..core.config import config
    from ..core.logger import logger
    from ..theme.engine import theme_engine
    from ..theme.palette import PALETTE
    from .components.base_dialog import BaseToolkitDialog, QT_AVAILABLE
except (ImportError, ValueError):
    from core.config import config
    from core.logger import logger
    from theme.engine import theme_engine
    from theme.palette import PALETTE
    from ui.components.base_dialog import BaseToolkitDialog, QT_AVAILABLE

if QT_AVAILABLE:
    try:
        from aqt.qt import (
            QCheckBox,
            QColor,
            QColorDialog,
            QFormLayout,
            QGroupBox,
            QHBoxLayout,
            QLabel,
            QLineEdit,
            QPushButton,
            QVBoxLayout,
        )
    except ImportError:
        try:
            from PyQt6.QtWidgets import (
                QCheckBox,
                QColorDialog,
                QFormLayout,
                QGroupBox,
                QHBoxLayout,
                QLabel,
                QLineEdit,
                QPushButton,
                QVBoxLayout,
            )
            from PyQt6.QtGui import QColor
        except ImportError:
            from PyQt5.QtWidgets import (
                QCheckBox,
                QColorDialog,
                QFormLayout,
                QGroupBox,
                QHBoxLayout,
                QLabel,
                QLineEdit,
                QPushButton,
                QVBoxLayout,
            )
            from PyQt5.QtGui import QColor
else:
    QCheckBox = QColorDialog = QColor = QFormLayout = QGroupBox = QHBoxLayout = QLabel = QLineEdit = QPushButton = QVBoxLayout = object


class ThemeSettingsDialog(BaseToolkitDialog):
    """
    Dialog for configuring theme options and accent colors.
    """
    def __init__(self, parent: Optional[Any] = None) -> None:
        super().__init__(
            parent,
            title="Theme and Appearance Settings",
            subtitle="Full Black #000000 AMOLED base with iOS Liquid Glass styling.",
        )
        if not QT_AVAILABLE:
            return

        self._current_accent = config.get("theme.accent", PALETTE.ACCENT_PRIMARY)
        self._build_ui()
        self._load_values()

    def _build_ui(self) -> None:
        layout = QVBoxLayout()
        layout.setSpacing(14)

        # General Theme Options
        group_general = QGroupBox("General Theme Settings", self)
        form_general = QFormLayout(group_general)
        form_general.setSpacing(10)

        self.chk_theme_enabled = QCheckBox("Enable Full Black #000000 AMOLED Theme", self)
        self.chk_theme_enabled.setStyleSheet("font-weight: 600;")
        form_general.addRow("Theme Status:", self.chk_theme_enabled)

        self.chk_webviews = QCheckBox("Apply Full Black Styling to WebViews (Deck Browser, Stats, Reviewer)", self)
        form_general.addRow("WebViews:", self.chk_webviews)

        self.chk_reviewer = QCheckBox("Force Full Black Background during Card Reviews", self)
        form_general.addRow("Reviewer:", self.chk_reviewer)

        layout.addWidget(group_general)

        # Accent Color Options
        group_accent = QGroupBox("Interface Accent Color", self)
        form_accent = QFormLayout(group_accent)
        form_accent.setSpacing(10)

        accent_row = QHBoxLayout()
        self.txt_accent = QLineEdit(self)
        self.txt_accent.setPlaceholderText("#0A84FF")
        accent_row.addWidget(self.txt_accent)

        self.btn_pick_color = QPushButton("Pick Color...", self)
        self.btn_pick_color.clicked.connect(self._pick_color)
        accent_row.addWidget(self.btn_pick_color)

        self.color_preview = QLabel(self)
        self.color_preview.setFixedSize(28, 28)
        self.color_preview.setStyleSheet(f"background-color: {self._current_accent}; border-radius: 6px; border: 1px solid #FFFFFF;")
        accent_row.addWidget(self.color_preview)

        form_accent.addRow("Accent Color (Hex):", accent_row)

        # Quick Presets
        presets_layout = QHBoxLayout()
        presets = [
            ("Apple Blue", "#0A84FF"),
            ("Emerald Green", "#30D158"),
            ("Indigo Purple", "#5E5CE6"),
            ("Crimson Red", "#FF453A"),
            ("Amber Orange", "#FF9F0A"),
            ("Cyan Mint", "#64D2FF"),
        ]
        for name, hex_code in presets:
            btn_p = QPushButton(name, self)
            btn_p.setStyleSheet(f"font-size: 11px; padding: 4px 8px; border-left: 3px solid {hex_code};")
            btn_p.clicked.connect(lambda _, c=hex_code: self._set_accent_hex(c))
            presets_layout.addWidget(btn_p)

        form_accent.addRow("Presets:", presets_layout)
        layout.addWidget(group_accent)

        self.body_layout.addLayout(layout)

    def _load_values(self) -> None:
        self.chk_theme_enabled.setChecked(config.get("theme.enabled", True))
        self.chk_webviews.setChecked(config.get("theme.apply_to_webviews", True))
        self.chk_reviewer.setChecked(config.get("theme.pure_black_reviewer", True))
        self.txt_accent.setText(config.get("theme.accent", PALETTE.ACCENT_PRIMARY))
        self._update_color_preview(self.txt_accent.text())

    def _pick_color(self) -> None:
        if not hasattr(QColorDialog, "getColor"):
            return
        initial_color = QColor(self.txt_accent.text().strip() or PALETTE.ACCENT_PRIMARY)
        color = QColorDialog.getColor(initial_color, self, "Select Accent Color")
        if color.isValid():
            hex_color = color.name()
            self._set_accent_hex(hex_color)

    def _set_accent_hex(self, hex_code: str) -> None:
        self.txt_accent.setText(hex_code)
        self._update_color_preview(hex_code)

    def _update_color_preview(self, hex_code: str) -> None:
        if hex_code.startswith("#") and len(hex_code) in (4, 7):
            self.color_preview.setStyleSheet(f"background-color: {hex_code}; border-radius: 6px; border: 1px solid #FFFFFF;")

    def accept(self) -> None:
        try:
            enabled = self.chk_theme_enabled.isChecked()
            accent = self.txt_accent.text().strip() or PALETTE.ACCENT_PRIMARY

            config.set("theme.enabled", enabled, save=False)
            config.set("theme.apply_to_webviews", self.chk_webviews.isChecked(), save=False)
            config.set("theme.pure_black_reviewer", self.chk_reviewer.isChecked(), save=False)
            config.set("theme.accent", accent, save=True)

            if enabled:
                theme_engine.activate()
            else:
                theme_engine.deactivate()

            logger.info(f"[ThemeSettingsDialog] Theme preferences updated (enabled={enabled}, accent={accent}).")
            super().accept()
        except Exception as e:
            logger.error(f"[ThemeSettingsDialog] Failed saving theme settings: {e}")
