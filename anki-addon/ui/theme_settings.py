"""
Theme Settings Dialog for Anki Wykiati Toolkit.
Allows toggling Full Black AMOLED (#000000), customizing background RGB with an interactive Color Wheel,
and selecting iOS liquid glass accent colors.
"""

import math
from typing import Any, Callable, Optional

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
            QBrush,
            QCheckBox,
            QColor,
            QColorDialog,
            QConicalGradient,
            QFormLayout,
            QFrame,
            QGridLayout,
            QGroupBox,
            QHBoxLayout,
            QLabel,
            QLineEdit,
            QPainter,
            QPainterPath,
            QPen,
            QPointF,
            QPushButton,
            QRadialGradient,
            QSlider,
            QVBoxLayout,
            QWidget,
            Qt,
        )
    except ImportError:
        try:
            from PyQt6.QtWidgets import (
                QCheckBox,
                QColorDialog,
                QFormLayout,
                QFrame,
                QGridLayout,
                QGroupBox,
                QHBoxLayout,
                QLabel,
                QLineEdit,
                QPushButton,
                QSlider,
                QVBoxLayout,
                QWidget,
            )
            from PyQt6.QtGui import (
                QBrush,
                QColor,
                QConicalGradient,
                QPainter,
                QPainterPath,
                QPen,
                QRadialGradient,
            )
            from PyQt6.QtCore import QPointF, Qt
        except ImportError:
            from PyQt5.QtWidgets import (
                QCheckBox,
                QColorDialog,
                QFormLayout,
                QFrame,
                QGridLayout,
                QGroupBox,
                QHBoxLayout,
                QLabel,
                QLineEdit,
                QPushButton,
                QSlider,
                QVBoxLayout,
                QWidget,
            )
            from PyQt5.QtGui import (
                QBrush,
                QColor,
                QConicalGradient,
                QPainter,
                QPainterPath,
                QPen,
                QRadialGradient,
            )
            from PyQt5.QtCore import QPointF, Qt
else:
    QBrush = QCheckBox = QColor = QColorDialog = QConicalGradient = QFormLayout = QFrame = QGridLayout = QGroupBox = QHBoxLayout = QLabel = QLineEdit = QPainter = QPainterPath = QPen = QPointF = QPushButton = QRadialGradient = QSlider = QVBoxLayout = QWidget = Qt = object


class RGBWheelWidget(QWidget):
    """
    Interactive circular RGB Color Wheel with live hue & saturation selection.
    Renders an antialiased circular spectrum and allows picking colors by clicking or dragging.
    """
    def __init__(self, parent: Optional[QWidget] = None, initial_hex: str = "#000000") -> None:
        super().__init__(parent)
        self.setFixedSize(130, 130)
        try:
            if hasattr(Qt, "CursorShape") and hasattr(Qt.CursorShape, "CrossCursor"):
                self.setCursor(Qt.CursorShape.CrossCursor)
            elif hasattr(Qt, "CrossCursor"):
                self.setCursor(Qt.CrossCursor)
        except Exception:
            pass
        self._current_hex = initial_hex
        self._selected_hue = 0.0
        self._selected_sat = 0.0
        self._on_color_changed: Optional[Callable[[str], None]] = None

    def set_on_color_changed(self, callback: Callable[[str], None]) -> None:
        self._on_color_changed = callback

    def set_color_hex(self, hex_code: str) -> None:
        self._current_hex = hex_code
        if hasattr(self, "update"):
            self.update()

    def paintEvent(self, event: Any) -> None:
        if not QT_AVAILABLE or not hasattr(QPainter, "Antialiasing"):
            return
        try:
            painter = QPainter(self)
            painter.setRenderHint(QPainter.RenderHint.Antialiasing if hasattr(QPainter, "RenderHint") else QPainter.Antialiasing)

            w = self.width()
            h = self.height()
            radius = min(w, h) / 2.0 - 4.0
            center = QPointF(w / 2.0, h / 2.0)

            # 1. Circular hue spectrum
            conical = QConicalGradient(center, 0)
            conical.setColorAt(0.0 / 6.0, QColor(255, 0, 0))
            conical.setColorAt(1.0 / 6.0, QColor(255, 255, 0))
            conical.setColorAt(2.0 / 6.0, QColor(0, 255, 0))
            conical.setColorAt(3.0 / 6.0, QColor(0, 255, 255))
            conical.setColorAt(4.0 / 6.0, QColor(0, 0, 255))
            conical.setColorAt(5.0 / 6.0, QColor(255, 0, 255))
            conical.setColorAt(1.0, QColor(255, 0, 0))

            painter.setPen(QPen(QColor(255, 255, 255, 40), 1))
            painter.setBrush(QBrush(conical))
            painter.drawEllipse(center, radius, radius)

            # 2. Dark/Light center overlay
            radial = QRadialGradient(center, radius)
            radial.setColorAt(0.0, QColor(0, 0, 0, 230))
            radial.setColorAt(0.7, QColor(0, 0, 0, 100))
            radial.setColorAt(1.0, QColor(0, 0, 0, 0))
            painter.setPen(QPen(QColor(0, 0, 0, 0)))
            painter.setBrush(QBrush(radial))
            painter.drawEllipse(center, radius, radius)

            # 3. Outer border ring
            painter.setPen(QPen(QColor(255, 255, 255, 60), 1.5))
            painter.setBrush(QBrush(QColor(0, 0, 0, 0)))
            painter.drawEllipse(center, radius, radius)
            painter.end()
        except Exception:
            pass

    def mousePressEvent(self, event: Any) -> None:
        self._handle_mouse(event)

    def mouseMoveEvent(self, event: Any) -> None:
        self._handle_mouse(event)

    def _handle_mouse(self, event: Any) -> None:
        try:
            pos = event.position() if hasattr(event, "position") else event.pos()
            w = self.width()
            h = self.height()
            cx = w / 2.0
            cy = h / 2.0
            dx = float(pos.x()) - cx
            dy = float(pos.y()) - cy
            dist = math.sqrt(dx * dx + dy * dy)
            radius = min(w, h) / 2.0 - 4.0

            if dist <= radius:
                # Angle in degrees [0, 360)
                angle = (math.degrees(math.atan2(dy, dx)) + 360.0) % 360.0
                # Saturation [0, 1]
                sat = min(1.0, dist / radius)
                # Value/Brightness scaled for deep dark tones
                val = max(0.05, min(0.95, sat))

                color = None
                if hasattr(QColor, "fromHsvF"):
                    color = QColor.fromHsvF(angle / 360.0, sat, val)
                if color is None or not getattr(color, "isValid", lambda: True)():
                    color = QColor()
                    if hasattr(color, "setHsvF"):
                        color.setHsvF(angle / 360.0, sat, val)
                
                if color and getattr(color, "isValid", lambda: True)():
                    hex_code = color.name()
                    self._current_hex = hex_code
                    if self._on_color_changed:
                        self._on_color_changed(hex_code)
        except Exception:
            pass


class ThemeSettingsDialog(BaseToolkitDialog):
    """
    Dialog for configuring theme options, custom RGB background colors, and accent colors.
    """
    def __init__(self, parent: Optional[Any] = None) -> None:
        super().__init__(
            parent,
            title="Theme & Appearance Studio",
            subtitle="Full Black #000000 AMOLED base or custom RGB background with iOS Liquid Glass styling.",
            width=680,
            height=580,
        )
        if not QT_AVAILABLE:
            return

        self._current_bg = config.get("theme.background", PALETTE.BACKGROUND_PURE_BLACK)
        self._current_accent = config.get("theme.accent", PALETTE.ACCENT_PRIMARY)
        self._build_ui()
        self._load_values()

    def _build_ui(self) -> None:
        layout = QVBoxLayout()
        layout.setSpacing(14)

        # 1. General Theme Toggles
        group_general = QGroupBox("General Theme Settings", self)
        form_general = QFormLayout(group_general)
        form_general.setSpacing(10)

        self.chk_theme_enabled = QCheckBox("Enable Full Black / Custom RGB Theme", self)
        self.chk_theme_enabled.setStyleSheet("font-weight: 600;")
        form_general.addRow("Theme Status:", self.chk_theme_enabled)

        self.chk_webviews = QCheckBox("Apply Theme to WebViews (Deck Browser, Stats, Reviewer)", self)
        form_general.addRow("WebViews:", self.chk_webviews)

        self.chk_reviewer = QCheckBox("Force Dark Background during Card Reviews", self)
        form_general.addRow("Reviewer:", self.chk_reviewer)

        layout.addWidget(group_general)

        # 2. RGB Background Color Studio (RGB Circle + Presets + Hex)
        group_bg = QGroupBox("Background Color Studio (RGB Circle / OLED Modes)", self)
        bg_main_layout = QVBoxLayout(group_bg)
        bg_main_layout.setSpacing(10)

        bg_controls_row = QHBoxLayout()
        bg_controls_row.setSpacing(16)

        # RGB Color Wheel Widget
        self.rgb_wheel = RGBWheelWidget(self, initial_hex=self._current_bg)
        self.rgb_wheel.set_on_color_changed(self._set_bg_hex)
        bg_controls_row.addWidget(self.rgb_wheel)

        # Inputs and Quick Controls
        bg_right_layout = QVBoxLayout()
        bg_right_layout.setSpacing(8)

        lbl_bg_desc = QLabel("Click on the RGB Circle to dynamically change the app background color, or enter a Hex code:", self)
        lbl_bg_desc.setStyleSheet(f"font-size: 11px; color: {PALETTE.TEXT_MUTED};")
        lbl_bg_desc.setWordWrap(True)
        bg_right_layout.addWidget(lbl_bg_desc)

        bg_input_row = QHBoxLayout()
        self.txt_bg = QLineEdit(self)
        self.txt_bg.setPlaceholderText("#000000")
        self.txt_bg.textChanged.connect(self._on_bg_text_changed)
        bg_input_row.addWidget(self.txt_bg)

        self.btn_pick_bg = QPushButton("Pick from Palette...", self)
        self.btn_pick_bg.clicked.connect(self._pick_bg_dialog)
        bg_input_row.addWidget(self.btn_pick_bg)

        self.bg_preview_swatch = QLabel(self)
        self.bg_preview_swatch.setFixedSize(32, 28)
        self.bg_preview_swatch.setStyleSheet(f"background-color: {self._current_bg}; border-radius: 4px; border: 1px solid rgba(255,255,255,0.3);")
        bg_input_row.addWidget(self.bg_preview_swatch)

        bg_right_layout.addLayout(bg_input_row)

        # Background Presets Grid
        lbl_bg_presets = QLabel("OLED & Dark Presets:", self)
        lbl_bg_presets.setStyleSheet(f"font-size: 11px; font-weight: 600; color: {PALETTE.TEXT_SECONDARY}; margin-top: 4px;")
        bg_right_layout.addWidget(lbl_bg_presets)

        bg_presets_grid = QGridLayout()
        bg_presets_grid.setSpacing(6)
        bg_presets = [
            ("🖤 Full Black AMOLED", "#000000"),
            ("🌌 Deep Midnight", "#0B0E14"),
            ("🌲 Forest Night", "#08120C"),
            ("🪐 Obsidian Dark", "#121214"),
            ("🔮 Cosmic Violet", "#0E0B14"),
            ("⚓ Cyberpunk Dark", "#0D1117"),
        ]
        for idx, (name, hex_c) in enumerate(bg_presets):
            btn = QPushButton(name, self)
            btn.setStyleSheet(f"font-size: 10px; padding: 4px 6px; text-align: left; border-left: 3px solid {hex_c if hex_c != '#000000' else '#333333'};")
            btn.clicked.connect(lambda _, c=hex_c: self._set_bg_hex(c))
            row = idx // 2
            col = idx % 2
            bg_presets_grid.addWidget(btn, row, col)

        bg_right_layout.addLayout(bg_presets_grid)
        bg_controls_row.addLayout(bg_right_layout, 1)

        bg_main_layout.addLayout(bg_controls_row)
        layout.addWidget(group_bg)

        # 3. Interface Accent Color
        group_accent = QGroupBox("Interface Accent Color", self)
        form_accent = QFormLayout(group_accent)
        form_accent.setSpacing(10)

        accent_row = QHBoxLayout()
        self.txt_accent = QLineEdit(self)
        self.txt_accent.setPlaceholderText("#FFFFFF")
        self.txt_accent.textChanged.connect(self._on_accent_text_changed)
        accent_row.addWidget(self.txt_accent)

        self.btn_pick_color = QPushButton("Pick Color...", self)
        self.btn_pick_color.clicked.connect(self._pick_accent_dialog)
        accent_row.addWidget(self.btn_pick_color)

        self.color_preview = QLabel(self)
        self.color_preview.setFixedSize(32, 28)
        self.color_preview.setStyleSheet(f"background-color: {self._current_accent}; border-radius: 4px; border: 1px solid #FFFFFF;")
        accent_row.addWidget(self.color_preview)

        form_accent.addRow("Accent Color (Hex):", accent_row)

        # Quick Accent Presets
        presets_layout = QHBoxLayout()
        accent_presets = [
            ("Monochrome", "#FFFFFF"),
            ("Apple Blue", "#0A84FF"),
            ("Emerald Green", "#30D158"),
            ("Indigo Purple", "#5E5CE6"),
            ("Crimson Red", "#FF453A"),
            ("Amber Orange", "#FF9F0A"),
            ("Cyan Mint", "#38BDF8"),
        ]
        for name, hex_code in accent_presets:
            btn_p = QPushButton(name, self)
            btn_p.setStyleSheet(f"font-size: 11px; padding: 4px 8px; border-left: 3px solid {hex_code};")
            btn_p.clicked.connect(lambda _, c=hex_code: self._set_accent_hex(c))
            presets_layout.addWidget(btn_p)

        form_accent.addRow("Presets:", presets_layout)
        layout.addWidget(group_accent)

        # 4. Live Visual Preview Card
        group_preview = QGroupBox("Live Theme Preview", self)
        preview_layout = QVBoxLayout(group_preview)
        
        self.preview_card = QFrame(self)
        self.preview_card.setStyleSheet(
            f"background-color: {self._current_bg}; border: 1px solid rgba(255,255,255,0.12); border-radius: 6px; padding: 14px;"
        )
        p_card_layout = QVBoxLayout(self.preview_card)
        p_card_layout.setSpacing(6)

        self.lbl_p_title = QLabel("Preview Deck: Medicine::Cardiology", self.preview_card)
        self.lbl_p_title.setStyleSheet("font-size: 13px; font-weight: bold; color: #FFFFFF;")
        p_card_layout.addWidget(self.lbl_p_title)

        self.lbl_p_text = QLabel("Front of flashcard with custom background and active accent highlight.", self.preview_card)
        self.lbl_p_text.setStyleSheet("font-size: 12px; color: #A1A1AA;")
        p_card_layout.addWidget(self.lbl_p_text)

        preview_btn_row = QHBoxLayout()
        self.btn_p_sample = QPushButton("Show Answer", self.preview_card)
        self.btn_p_sample.setStyleSheet(f"background-color: rgba(255,255,255,0.12); color: #FFFFFF; border: 1px solid {self._current_accent}; border-radius: 4px; padding: 5px 14px;")
        preview_btn_row.addWidget(self.btn_p_sample)
        preview_btn_row.addStretch()
        p_card_layout.addLayout(preview_btn_row)

        preview_layout.addWidget(self.preview_card)
        layout.addWidget(group_preview)

        self.body_layout.addLayout(layout)

    def _load_values(self) -> None:
        self.chk_theme_enabled.setChecked(config.get("theme.enabled", True))
        self.chk_webviews.setChecked(config.get("theme.apply_to_webviews", True))
        self.chk_reviewer.setChecked(config.get("theme.pure_black_reviewer", True))
        
        bg = config.get("theme.background", PALETTE.BACKGROUND_PURE_BLACK)
        accent = config.get("theme.accent", PALETTE.ACCENT_PRIMARY)
        
        self.txt_bg.setText(bg)
        self.txt_accent.setText(accent)
        self._update_all_previews(bg, accent)

    def _pick_bg_dialog(self) -> None:
        if not hasattr(QColorDialog, "getColor"):
            return
        initial = QColor(self.txt_bg.text().strip() or PALETTE.BACKGROUND_PURE_BLACK)
        color = QColorDialog.getColor(initial, self, "Select App Background Color (RGB)")
        if color.isValid():
            self._set_bg_hex(color.name())

    def _pick_accent_dialog(self) -> None:
        if not hasattr(QColorDialog, "getColor"):
            return
        initial = QColor(self.txt_accent.text().strip() or PALETTE.ACCENT_PRIMARY)
        color = QColorDialog.getColor(initial, self, "Select Interface Accent Color")
        if color.isValid():
            self._set_accent_hex(color.name())

    def _set_bg_hex(self, hex_code: str) -> None:
        self.txt_bg.setText(hex_code)
        self.rgb_wheel.set_color_hex(hex_code)
        self._update_all_previews(hex_code, self.txt_accent.text().strip())

    def _set_accent_hex(self, hex_code: str) -> None:
        self.txt_accent.setText(hex_code)
        self._update_all_previews(self.txt_bg.text().strip(), hex_code)

    def _on_bg_text_changed(self, text: str) -> None:
        if text.startswith("#") and len(text) in (4, 7):
            self._update_all_previews(text, self.txt_accent.text().strip())

    def _on_accent_text_changed(self, text: str) -> None:
        if text.startswith("#") and len(text) in (4, 7):
            self._update_all_previews(self.txt_bg.text().strip(), text)

    def _update_all_previews(self, bg_hex: str, accent_hex: str) -> None:
        if bg_hex.startswith("#") and len(bg_hex) in (4, 7):
            self._current_bg = bg_hex
            self.bg_preview_swatch.setStyleSheet(
                f"background-color: {bg_hex}; border-radius: 4px; border: 1px solid rgba(255,255,255,0.4);"
            )
            self.preview_card.setStyleSheet(
                f"background-color: {bg_hex}; border: 1px solid rgba(255,255,255,0.15); border-radius: 6px; padding: 14px;"
            )

        if accent_hex.startswith("#") and len(accent_hex) in (4, 7):
            self._current_accent = accent_hex
            self.color_preview.setStyleSheet(
                f"background-color: {accent_hex}; border-radius: 4px; border: 1px solid #FFFFFF;"
            )
            self.btn_p_sample.setStyleSheet(
                f"background-color: rgba(255,255,255,0.12); color: #FFFFFF; border: 1px solid {accent_hex}; border-radius: 4px; padding: 5px 14px;"
            )

    def accept(self) -> None:
        try:
            enabled = self.chk_theme_enabled.isChecked()
            bg = self.txt_bg.text().strip() or PALETTE.BACKGROUND_PURE_BLACK
            accent = self.txt_accent.text().strip() or PALETTE.ACCENT_PRIMARY

            config.set("theme.enabled", enabled, save=False)
            config.set("theme.background", bg, save=False)
            config.set("theme.accent", accent, save=False)
            config.set("theme.apply_to_webviews", self.chk_webviews.isChecked(), save=False)
            config.set("theme.pure_black_reviewer", self.chk_reviewer.isChecked(), save=True)

            if enabled:
                theme_engine.activate()
            else:
                theme_engine.deactivate()

            logger.info(f"[ThemeSettingsDialog] Theme preferences saved (bg={bg}, accent={accent}, enabled={enabled}).")
            super().accept()
        except Exception as e:
            logger.error(f"[ThemeSettingsDialog] Failed saving theme settings: {e}")

