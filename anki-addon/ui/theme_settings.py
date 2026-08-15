"""
Theme Settings Dialog.
Allows users to configure Pure Black AMOLED styling, accent colors, and WebView overrides.
"""

from typing import Any, Optional

try:
    from ..core.config import config
    from ..core.logger import logger
    from ..theme.palette import PALETTE
    from .components.base_dialog import BaseToolkitDialog, QT_AVAILABLE
except (ImportError, ValueError):
    from core.config import config
    from core.logger import logger
    from theme.palette import PALETTE
    from ui.components.base_dialog import BaseToolkitDialog, QT_AVAILABLE

if QT_AVAILABLE:
    try:
        from aqt.qt import (
            QCheckBox,
            QComboBox,
            QFormLayout,
            QGroupBox,
            QHBoxLayout,
            QLabel,
            QVBoxLayout,
        )
    except ImportError:
        try:
            from PyQt6.QtWidgets import (
                QCheckBox,
                QComboBox,
                QFormLayout,
                QGroupBox,
                QHBoxLayout,
                QLabel,
                QVBoxLayout,
            )
        except ImportError:
            from PyQt5.QtWidgets import (
                QCheckBox,
                QComboBox,
                QFormLayout,
                QGroupBox,
                QHBoxLayout,
                QLabel,
                QVBoxLayout,
            )
else:
    QCheckBox = QComboBox = QFormLayout = QGroupBox = QHBoxLayout = QLabel = QVBoxLayout = object


ACCENT_OPTIONS = {
    "Vivid Blue (Padrão)": "#3B82F6",
    "Emerald Green": "#10B981",
    "Indigo Purple": "#6366F1",
    "Crimson Red": "#EF4444",
    "Amber Gold": "#F59E0B",
    "Cyan Neon": "#06B6D4",
}


class ThemeSettingsDialog(BaseToolkitDialog):
    """
    Settings interface for Pure Black theme.
    """
    def __init__(self, parent: Optional[Any] = None) -> None:
        super().__init__(
            parent,
            title="Configurações do Tema Pure Black",
            subtitle="Personalize o contraste visual e as cores de destaque para telas OLED / AMOLED.",
        )
        if not QT_AVAILABLE:
            return

        self._build_ui()
        self._load_values()

    def _build_ui(self) -> None:
        form = QVBoxLayout()
        form.setSpacing(14)

        # Main Theme Toggle Group
        group_general = QGroupBox("Aparência Geral", self)
        gen_layout = QVBoxLayout(group_general)
        gen_layout.setSpacing(8)

        self.chk_theme_enabled = QCheckBox("Habilitar Tema Pure Black (#000000 AMOLED)", self)
        self.chk_theme_enabled.setStyleSheet("font-weight: 600; font-size: 13px;")
        gen_layout.addWidget(self.chk_theme_enabled)

        desc_label = QLabel(
            "Substitui os cinzas do Dark Mode tradicional por preto absoluto #000000, economizando energia e aumentando o contraste.",
            self,
        )
        desc_label.setWordWrap(True)
        desc_label.setStyleSheet(f"color: {PALETTE.TEXT_MUTED}; font-size: 11px; margin-left: 20px;")
        gen_layout.addWidget(desc_label)

        form.addWidget(group_general)

        # Accent & Customization Group
        group_custom = QGroupBox("Customização e Destaques", self)
        custom_layout = QFormLayout(group_custom)
        custom_layout.setSpacing(10)

        self.combo_accent = QComboBox(self)
        for label in ACCENT_OPTIONS.keys():
            self.combo_accent.addItem(label)
        custom_layout.addRow("Cor de Destaque (Accent):", self.combo_accent)

        self.chk_webviews = QCheckBox("Aplicar Preto Puro aos WebViews (Deck Browser & Estatísticas)", self)
        custom_layout.addRow("", self.chk_webviews)

        self.chk_reviewer = QCheckBox("Aplicar Fundo Preto no Visualizador de Cartões (Reviewer)", self)
        custom_layout.addRow("", self.chk_reviewer)

        form.addWidget(group_custom)

        self.body_layout.addLayout(form)

    def _load_values(self) -> None:
        self.chk_theme_enabled.setChecked(config.get("theme.enabled", True))
        self.chk_webviews.setChecked(config.get("theme.apply_to_webviews", True))
        self.chk_reviewer.setChecked(config.get("theme.pure_black_reviewer", True))

        current_accent = config.get("theme.accent", PALETTE.ACCENT_PRIMARY)
        for idx, (label, color_code) in enumerate(ACCENT_OPTIONS.items()):
            if color_code.lower() == current_accent.lower():
                self.combo_accent.setCurrentIndex(idx)
                break

    def accept(self) -> None:
        try:
            selected_label = self.combo_accent.currentText()
            accent_hex = ACCENT_OPTIONS.get(selected_label, PALETTE.ACCENT_PRIMARY)

            config.set("theme.enabled", self.chk_theme_enabled.isChecked(), save=False)
            config.set("theme.accent", accent_hex, save=False)
            config.set("theme.apply_to_webviews", self.chk_webviews.isChecked(), save=False)
            config.set("theme.pure_black_reviewer", self.chk_reviewer.isChecked(), save=True)

            logger.info("[ThemeSettingsDialog] Theme settings updated successfully.")
            super().accept()
        except Exception as e:
            logger.error(f"[ThemeSettingsDialog] Error saving theme settings: {e}")
