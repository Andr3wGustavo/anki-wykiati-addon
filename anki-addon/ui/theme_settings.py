"""
Appearance (theme) settings panel for Anki Wykiati Toolkit.
Preset swatches for background and accent, a full custom picker, hex input and a
live miniature preview of Anki. RGBWheelWidget is kept for backward compatibility.
"""

import math
from typing import Any, Callable, Optional

try:
    from ..core.config import DEFAULT_CONFIG, config
    from ..core.logger import logger
    from ..theme.engine import theme_engine
    from ..theme.palette import PALETTE, contrast_ratio, is_light_color, is_valid_hex, mix, normalize_hex, readable_text_on, semantic_colors, with_alpha
    from ..theme.styles import generate_qss
    from .components.base_dialog import BaseToolkitDialog, QT_AVAILABLE
except (ImportError, ValueError):
    from core.config import DEFAULT_CONFIG, config
    from core.logger import logger
    from theme.engine import theme_engine
    from theme.palette import PALETTE, contrast_ratio, is_light_color, is_valid_hex, mix, normalize_hex, readable_text_on, semantic_colors, with_alpha
    from theme.styles import generate_qss
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
        if QT_AVAILABLE:
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
        self._dragging = False
        self._on_color_changed: Optional[Callable[[str], None]] = None
        self._sync_marker_from_hex(initial_hex)

    def set_on_color_changed(self, callback: Callable[[str], None]) -> None:
        self._on_color_changed = callback

    def set_color_hex(self, hex_code: str) -> None:
        self._current_hex = hex_code
        self._sync_marker_from_hex(hex_code)
        if hasattr(self, "update"):
            self.update()

    def _sync_marker_from_hex(self, hex_code: str) -> None:
        """Place the selection marker at the hue/saturation of the given color."""
        if not QT_AVAILABLE or not is_valid_hex(hex_code) or not hasattr(QColor, "hsvHueF"):
            return
        try:
            color = QColor(hex_code)
            hue = color.hsvHueF()
            self._selected_hue = 0.0 if hue < 0 else hue * 360.0  # achromatic colors report -1
            self._selected_sat = max(0.0, min(1.0, color.hsvSaturationF()))
        except Exception:
            pass

    def paintEvent(self, event: Any) -> None:
        # PyQt6 only exposes scoped enums (QPainter.RenderHint.Antialiasing); checking the
        # legacy unscoped name alone made the wheel invisible outside Anki's compat shim.
        if not QT_AVAILABLE or not (hasattr(QPainter, "RenderHint") or hasattr(QPainter, "Antialiasing")):
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

            # 4. Selection marker (same geometry as _handle_mouse: hue grows counter-clockwise)
            angle_rad = math.radians(self._selected_hue)
            dist = self._selected_sat * radius
            marker = QPointF(center.x() + math.cos(angle_rad) * dist, center.y() - math.sin(angle_rad) * dist)
            painter.setPen(QPen(QColor(0, 0, 0, 200), 3.0))
            painter.setBrush(QBrush(QColor(0, 0, 0, 0)))
            painter.drawEllipse(marker, 5.0, 5.0)
            painter.setPen(QPen(QColor(255, 255, 255, 240), 1.5))
            painter.drawEllipse(marker, 5.0, 5.0)
            painter.end()
        except Exception:
            pass

    def mousePressEvent(self, event: Any) -> None:
        self._handle_mouse(event, is_press=True)

    def mouseMoveEvent(self, event: Any) -> None:
        self._handle_mouse(event, is_press=False)

    def _handle_mouse(self, event: Any, is_press: bool = False) -> None:
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

            # Pressing must start inside the wheel; dragging may leave it (clamped to the edge).
            if is_press:
                self._dragging = dist <= radius
            if not self._dragging:
                return
            dist = min(dist, radius)

            if radius > 0:
                # Angle in degrees [0, 360). QConicalGradient runs counter-clockwise
                # while screen Y grows downward, so dy must be negated; otherwise the
                # picked hue is mirrored (clicking yellow returned magenta).
                angle = (math.degrees(math.atan2(-dy, dx)) + 360.0) % 360.0
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
                    self._selected_hue = angle
                    self._selected_sat = sat
                    if hasattr(self, "update"):
                        self.update()
                    if self._on_color_changed:
                        self._on_color_changed(hex_code)
        except Exception:
            pass


BACKGROUND_PRESETS = [
    ("Void Black", "#000000"),
    ("Midnight", "#0B0E14"),
    ("Graphite", "#18181B"),
    ("Navy", "#0D1117"),
    ("Forest", "#08120C"),
    ("Violet", "#0E0B14"),
    ("Paper", "#F5F5F4"),
    ("White", "#FFFFFF"),
]

ACCENT_PRESETS = [
    ("Mono", None),  # resolved to white on dark backgrounds, near-black on light ones
    ("Blue", "#0A84FF"),
    ("Purple", "#BF5AF2"),
    ("Pink", "#FF375F"),
    ("Orange", "#FF9F0A"),
    ("Green", "#30D158"),
    ("Teal", "#40C8E0"),
]

MONO_DARK = "#FFFFFF"
MONO_LIGHT = "#09090B"


def _mono_for(bg_hex: str) -> str:
    return MONO_LIGHT if is_light_color(bg_hex) else MONO_DARK


def _set_pointer_cursor(widget: Any) -> None:
    try:
        if hasattr(Qt, "CursorShape"):
            widget.setCursor(Qt.CursorShape.PointingHandCursor)
        else:
            widget.setCursor(Qt.PointingHandCursor)
    except Exception:
        pass


class ColorSwatch(QPushButton):
    """
    Round, clickable color chip, painted by hand (stylesheets cannot draw a ring
    with a gap). Selected = outer ring + gap + color dot, which stays visible even
    when the ring and the chip have the same color.
    """

    SIZE = 28

    def __init__(self, hex_code: str, name: str, parent: Optional[Any] = None) -> None:
        super().__init__(parent)
        self.hex_code = hex_code
        self._selected = False
        self._ring = "#FFFFFF"
        self.setFixedSize(self.SIZE, self.SIZE)
        self.setToolTip(f"{name}  {hex_code}")
        self.setAutoDefault(False)
        self.setFlat(True)
        _set_pointer_cursor(self)

    def set_color(self, hex_code: str, name: Optional[str] = None) -> None:
        self.hex_code = hex_code
        if name:
            self.setToolTip(f"{name}  {hex_code}")
        self.update()

    def set_state(self, selected: bool, ring_color: str) -> None:
        self._selected = selected
        self._ring = ring_color
        self.update()

    def paintEvent(self, event: Any) -> None:
        try:
            painter = QPainter(self)
            hint = QPainter.RenderHint.Antialiasing if hasattr(QPainter, "RenderHint") else QPainter.Antialiasing
            painter.setRenderHint(hint)
            center = QPointF(self.width() / 2.0, self.height() / 2.0)
            outer = self.SIZE / 2.0 - 1.5
            no_brush = QBrush(QColor(0, 0, 0, 0))
            hovered = self.underMouse()

            if self._selected:
                painter.setPen(QPen(QColor(self._ring), 2.0))
                painter.setBrush(no_brush)
                painter.drawEllipse(center, outer, outer)
                dot = outer - 4.0
            else:
                dot = outer - 2.0
                if hovered:
                    ring = QColor(self._ring)
                    ring.setAlpha(110)
                    painter.setPen(QPen(ring, 2.0))
                    painter.setBrush(no_brush)
                    painter.drawEllipse(center, outer, outer)

            edge = QColor(readable_text_on(self.hex_code))
            edge.setAlpha(60)
            painter.setPen(QPen(edge, 1.0))
            painter.setBrush(QBrush(QColor(self.hex_code)))
            painter.drawEllipse(center, dot, dot)
            painter.end()
        except Exception:
            pass

    def enterEvent(self, event: Any) -> None:
        self.update()
        super().enterEvent(event)

    def leaveEvent(self, event: Any) -> None:
        self.update()
        super().leaveEvent(event)


class ColorRow(QWidget):
    """
    One line of the picker: preset swatches, an extra chip for a custom color,
    a hex field and a 'Custom…' button that opens the full Qt color dialog.
    """

    def __init__(self, presets: list, on_change: Callable[[str], None], dialog_title: str, parent: Optional[Any] = None) -> None:
        super().__init__(parent)
        self._on_change = on_change
        self._dialog_title = dialog_title
        self._current = "#000000"
        self._ring = "#FFFFFF"

        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(8)

        self.swatches = []
        for name, hex_code in presets:
            sw = ColorSwatch(hex_code or MONO_DARK, name, self)
            sw.preset_name = name
            sw.clicked.connect(lambda _=False, s=sw: self._pick(s.hex_code))
            layout.addWidget(sw)
            self.swatches.append(sw)

        # Shows the current value when it is not one of the presets
        self.custom_swatch = ColorSwatch("#000000", "Custom", self)
        self.custom_swatch.clicked.connect(lambda _=False: self._pick(self.custom_swatch.hex_code))
        self.custom_swatch.setVisible(False)
        layout.addWidget(self.custom_swatch)

        layout.addStretch(1)

        self.hex_input = QLineEdit(self)
        self.hex_input.setFixedWidth(86)
        self.hex_input.setMaxLength(7)
        self.hex_input.setPlaceholderText("#RRGGBB")
        self.hex_input.setToolTip("Type a hex color, e.g. #0B0E14")
        self.hex_input.textEdited.connect(self._on_hex_edited)
        self.hex_input.editingFinished.connect(self._on_hex_finished)
        layout.addWidget(self.hex_input)

        self.btn_custom = QPushButton("Custom…", self)
        self.btn_custom.setToolTip("Open the full color picker")
        self.btn_custom.setAutoDefault(False)
        _set_pointer_cursor(self.btn_custom)
        self.btn_custom.clicked.connect(self._open_picker)
        layout.addWidget(self.btn_custom)

    # -- public
    def set_value(self, hex_code: str, ring_color: str) -> None:
        self._current = normalize_hex(hex_code, self._current)
        self._ring = ring_color
        matched = False
        for sw in self.swatches:
            selected = sw.hex_code.upper() == self._current
            matched = matched or selected
            sw.set_state(selected, ring_color)
        self.custom_swatch.setVisible(not matched)
        if not matched:
            self.custom_swatch.set_color(self._current, "Custom")
            self.custom_swatch.set_state(True, ring_color)
        if not self.hex_input.hasFocus():
            self.hex_input.setText(self._current)

    def set_preset_color(self, preset_name: str, hex_code: str) -> None:
        for sw in self.swatches:
            if sw.preset_name == preset_name:
                sw.set_color(hex_code, preset_name)

    def value(self) -> str:
        return self._current

    # -- internal
    def _pick(self, hex_code: str) -> None:
        self._on_change(normalize_hex(hex_code, self._current))

    def _on_hex_edited(self, text: str) -> None:
        text = text.strip()
        if text and not text.startswith("#"):
            text = "#" + text
        if is_valid_hex(text) and len(text) == 7:
            self._on_change(normalize_hex(text))

    def _on_hex_finished(self) -> None:
        text = self.hex_input.text().strip()
        if text and not text.startswith("#"):
            text = "#" + text
        if is_valid_hex(text):
            self._on_change(normalize_hex(text))
        self.hex_input.setText(self._current)

    def _open_picker(self) -> None:
        if not hasattr(QColorDialog, "getColor"):
            return
        color = QColorDialog.getColor(QColor(self._current), self, self._dialog_title)
        if color.isValid():
            self._on_change(normalize_hex(color.name()))


class ThemePreview(QFrame):
    """Miniature of Anki's deck list + reviewer, rendered with the chosen colors."""

    def __init__(self, parent: Optional[Any] = None) -> None:
        super().__init__(parent)
        self.setObjectName("awtPreview")
        root = QVBoxLayout(self)
        root.setContentsMargins(14, 12, 14, 12)
        root.setSpacing(10)

        # Deck row
        deck_row = QHBoxLayout()
        deck_row.setSpacing(10)
        self.lbl_deck = QLabel("Medicine::Cardiology", self)
        self.lbl_counts = QLabel(self)
        self.btn_study = QLabel("Study Now", self)
        deck_row.addWidget(self.lbl_deck)
        deck_row.addStretch(1)
        deck_row.addWidget(self.lbl_counts)
        deck_row.addWidget(self.btn_study)
        root.addLayout(deck_row)

        # Card
        self.card = QFrame(self)
        self.card.setObjectName("awtPreviewCard")
        card_layout = QVBoxLayout(self.card)
        card_layout.setContentsMargins(12, 12, 12, 12)
        card_layout.setSpacing(6)
        self.lbl_question = QLabel("Which node starts the cardiac impulse?", self.card)
        self.lbl_answer = QLabel(self.card)
        self.lbl_link = QLabel(self.card)
        for lbl in (self.lbl_question, self.lbl_answer, self.lbl_link):
            lbl.setWordWrap(True)
            card_layout.addWidget(lbl)
        root.addWidget(self.card)

        # Answer buttons
        ease_row = QHBoxLayout()
        ease_row.setSpacing(6)
        self.ease_labels = []
        for text in ("Again", "Hard", "Good", "Easy"):
            lbl = QLabel(text, self)
            try:
                lbl.setAlignment(Qt.AlignmentFlag.AlignCenter if hasattr(Qt, "AlignmentFlag") else Qt.AlignCenter)
            except Exception:
                pass
            ease_row.addWidget(lbl, 1)
            self.ease_labels.append(lbl)
        root.addLayout(ease_row)

    def render_colors(self, bg: str, accent: str, enabled: bool = True) -> None:
        light = is_light_color(bg)
        text = "#09090B" if light else "#FFFFFF"
        muted = "#52525B" if light else "#A1A1AA"
        border = "rgba(0, 0, 0, 0.12)" if light else "rgba(255, 255, 255, 0.10)"
        sem = semantic_colors(light)
        link = accent if contrast_ratio(accent, bg) >= 3.0 else mix(accent, "#000000" if light else "#FFFFFF", 0.55)

        self.setStyleSheet(
            f"QFrame#awtPreview {{ background-color: {bg}; border: 1px solid {border}; border-radius: 10px; }}"
            f"QFrame#awtPreviewCard {{ background-color: {bg}; border: 1px solid {border}; border-radius: 8px; }}"
            "QLabel { background: transparent; border: none; }"
        )
        self.lbl_deck.setStyleSheet(f"color: {text}; font-weight: 600;")
        self.lbl_counts.setText(
            f"<span style='color:{sem['new']}; font-weight:600'>12</span>&nbsp;&nbsp;"
            f"<span style='color:{sem['learn']}; font-weight:600'>3</span>&nbsp;&nbsp;"
            f"<span style='color:{sem['review']}; font-weight:600'>48</span>"
        )
        self.btn_study.setStyleSheet(
            f"background-color: {accent}; color: {readable_text_on(accent)}; border-radius: 6px;"
            f" padding: 4px 10px; font-weight: 600;"
        )
        self.lbl_question.setStyleSheet(f"color: {text}; font-size: 14px;")
        self.lbl_answer.setText(
            f"<span style='color:{muted}'>Answer:</span> "
            f"<span style='color:{sem['cloze']}; font-weight:600'>Sinoatrial (SA) node</span>"
        )
        self.lbl_link.setText(f"<span style='color:{link}; text-decoration: underline'>Read more</span>")
        for lbl, key in zip(self.ease_labels, ("again", "hard", "good", "easy")):
            color = sem[key]
            lbl.setStyleSheet(
                f"color: {color}; border: 1px solid {with_alpha(color, 0.40)}; border-radius: 6px;"
                f" padding: 5px 0px; font-weight: 600; background: transparent;"
            )
        self.setEnabled(enabled)


class ThemeSettingsDialog(BaseToolkitDialog):
    """
    Minimal appearance panel: pick a background and an accent from presets
    (or any custom color), see a live miniature of Anki, save.
    """
    def __init__(self, parent: Optional[Any] = None) -> None:
        super().__init__(
            parent,
            title="Appearance",
            subtitle="Pick a background and an accent color. The preview updates as you choose.",
            width=580,
            height=640,
        )
        if not QT_AVAILABLE:
            return

        self._bg = normalize_hex(config.get("theme.background"), PALETTE.BACKGROUND_PURE_BLACK)
        self._accent = normalize_hex(config.get("theme.accent"), _mono_for(self._bg))
        self._build_ui()
        self._load_values()

    # ----------------------------------------------------------------- layout

    def _section_label(self, text: str) -> Any:
        lbl = QLabel(text.upper(), self)
        lbl.setObjectName("awtSectionLabel")
        return lbl

    def _build_ui(self) -> None:
        layout = QVBoxLayout()
        layout.setSpacing(8)

        self.chk_theme_enabled = QCheckBox("Use custom theme", self)
        self.chk_theme_enabled.setToolTip("Turn off to go back to Anki's standard look")
        self.chk_theme_enabled.toggled.connect(lambda _=False: self._refresh())
        layout.addWidget(self.chk_theme_enabled)
        layout.addSpacing(6)

        self.colors_box = QWidget(self)
        colors_layout = QVBoxLayout(self.colors_box)
        colors_layout.setContentsMargins(0, 0, 0, 0)
        colors_layout.setSpacing(8)

        colors_layout.addWidget(self._section_label("Background"))
        self.bg_row = ColorRow(BACKGROUND_PRESETS, self._set_bg, "Background color", self.colors_box)
        colors_layout.addWidget(self.bg_row)
        colors_layout.addSpacing(8)

        colors_layout.addWidget(self._section_label("Accent"))
        self.accent_row = ColorRow(ACCENT_PRESETS, self._set_accent, "Accent color", self.colors_box)
        colors_layout.addWidget(self.accent_row)
        colors_layout.addSpacing(10)

        colors_layout.addWidget(self._section_label("Preview"))
        self.preview = ThemePreview(self.colors_box)
        colors_layout.addWidget(self.preview)
        colors_layout.addSpacing(6)

        self.chk_webviews = QCheckBox("Also theme the deck list, reviewer and toolbar", self.colors_box)
        self.chk_webviews.setToolTip("When off, only Anki's native windows and dialogs are themed")
        colors_layout.addWidget(self.chk_webviews)

        layout.addWidget(self.colors_box)
        layout.addStretch(1)
        self.body_layout.addLayout(layout)

        self.btn_reset = QPushButton("Reset to default", self)
        self.btn_reset.setToolTip("Void Black background with the default accent (applied when you save)")
        self.btn_reset.setAutoDefault(False)
        self.btn_reset.clicked.connect(self._reset_defaults)
        self.footer_layout.insertWidget(0, self.btn_reset)

    # ------------------------------------------------------------------ state

    def _load_values(self) -> None:
        self.chk_theme_enabled.setChecked(bool(config.get("theme.enabled", True)))
        self.chk_webviews.setChecked(bool(config.get("theme.apply_to_webviews", True)))
        self._refresh()

    def _set_bg(self, hex_code: str) -> None:
        old_mono = _mono_for(self._bg)
        self._bg = hex_code
        # Keep "Mono" accent meaningful when switching between light and dark backgrounds
        if self._accent in (MONO_DARK, MONO_LIGHT) and self._accent == old_mono:
            self._accent = _mono_for(hex_code)
        self._refresh()

    def _set_accent(self, hex_code: str) -> None:
        self._accent = hex_code
        self._refresh()

    def _reset_defaults(self) -> None:
        defaults = DEFAULT_CONFIG["theme"]
        self.chk_theme_enabled.setChecked(True)
        self.chk_webviews.setChecked(bool(defaults.get("apply_to_webviews", True)))
        self._bg = normalize_hex(defaults.get("background"), PALETTE.BACKGROUND_PURE_BLACK)
        self._accent = normalize_hex(defaults.get("accent"), _mono_for(self._bg))
        self._refresh()

    def _refresh(self) -> None:
        enabled = self.chk_theme_enabled.isChecked()
        ring = "#09090B" if is_light_color(self._bg) else "#FFFFFF"

        self.accent_row.set_preset_color("Mono", _mono_for(self._bg))
        self.bg_row.set_value(self._bg, ring)
        self.accent_row.set_value(self._accent, ring)
        self.preview.render_colors(self._bg, self._accent, enabled)
        self.colors_box.setEnabled(enabled)

        # The dialog itself previews the theme (QSS) while you pick
        muted = "#71717A" if is_light_color(self._bg) else "#A1A1AA"
        try:
            self.setStyleSheet(
                generate_qss(accent=self._accent, bg_color=self._bg)
                + f"\nQLabel#awtSectionLabel {{ color: {muted}; font-size: 11px; font-weight: 600; letter-spacing: 1px; }}"
            )
        except Exception:
            pass

    def keyPressEvent(self, event: Any) -> None:
        # Enter inside a hex field should apply the color, not save & close the dialog.
        try:
            key = event.key()
            enter_keys = (Qt.Key.Key_Return, Qt.Key.Key_Enter) if hasattr(Qt, "Key") else (Qt.Key_Return, Qt.Key_Enter)
            focused = self.focusWidget()
            if key in enter_keys and focused in (self.bg_row.hex_input, self.accent_row.hex_input):
                focused.clearFocus()
                return
        except Exception:
            pass
        super().keyPressEvent(event)

    def accept(self) -> None:
        try:
            enabled = self.chk_theme_enabled.isChecked()
            bg = normalize_hex(self._bg, PALETTE.BACKGROUND_PURE_BLACK)
            accent = normalize_hex(self._accent, _mono_for(bg))

            # The theme engine listens to "theme" changes and re-applies once
            # (debounced) after this batch, so no explicit activate() is needed.
            config.set("theme.enabled", enabled, save=False)
            config.set("theme.background", bg, save=False)
            config.set("theme.accent", accent, save=False)
            config.set("theme.apply_to_webviews", self.chk_webviews.isChecked(), save=True)

            logger.info(f"[ThemeSettingsDialog] Theme preferences saved (bg={bg}, accent={accent}, enabled={enabled}).")
            super().accept()
        except Exception as e:
            logger.error(f"[ThemeSettingsDialog] Failed saving theme settings: {e}")
