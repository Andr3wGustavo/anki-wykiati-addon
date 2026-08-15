"""
Templates and Note Types Dialog.
Displays available Anki note types and configured template mappings.
"""

from typing import Any, Optional

try:
    from ..core.config import config
    from ..core.logger import logger
    from ..templates.manager import template_manager
    from .components.base_dialog import BaseToolkitDialog, QT_AVAILABLE
except (ImportError, ValueError):
    from core.config import config
    from core.logger import logger
    from templates.manager import template_manager
    from ui.components.base_dialog import BaseToolkitDialog, QT_AVAILABLE

if QT_AVAILABLE:
    try:
        from aqt.qt import (
            QComboBox,
            QFormLayout,
            QGroupBox,
            QLabel,
            QListWidget,
            QVBoxLayout,
        )
    except ImportError:
        try:
            from PyQt6.QtWidgets import (
                QComboBox,
                QFormLayout,
                QGroupBox,
                QLabel,
                QListWidget,
                QVBoxLayout,
            )
        except ImportError:
            from PyQt5.QtWidgets import (
                QComboBox,
                QFormLayout,
                QGroupBox,
                QLabel,
                QListWidget,
                QVBoxLayout,
            )
else:
    QComboBox = QFormLayout = QGroupBox = QLabel = QListWidget = QVBoxLayout = object


class TemplatesDialog(BaseToolkitDialog):
    """
    Dialog for inspecting and setting default note types and templates.
    """
    def __init__(self, parent: Optional[Any] = None) -> None:
        super().__init__(
            parent,
            title="Gerenciador de Templates de Cartão",
            subtitle="Modelos de cartões suportados e mapeamento inteligente de campos.",
        )
        if not QT_AVAILABLE:
            return

        self._build_ui()
        self._load_data()

    def _build_ui(self) -> None:
        layout = QVBoxLayout()
        layout.setSpacing(12)

        # Default Template Choice
        group_default = QGroupBox("Tipo Padrão", self)
        form = QFormLayout(group_default)

        self.combo_default_type = QComboBox(self)
        available = template_manager.get_available_models_in_anki()
        for model in available:
            self.combo_default_type.addItem(model)
        form.addRow("Modelo Padrão para novos cartões:", self.combo_default_type)
        layout.addWidget(group_default)

        # Installed models list
        group_list = QGroupBox("Modelos de Notas Detectados no Anki", self)
        list_layout = QVBoxLayout(group_list)

        self.list_models = QListWidget(self)
        for m in available:
            self.list_models.addItem(f"• {m}")
        list_layout.addWidget(self.list_models)

        info = QLabel(
            "O Anki Discord Toolkit detecta automaticamente se sua mensagem utiliza sintaxe de Cloze ({{c1::...}}) "
            "ou campos específicos e mapeia os campos Front/Back/Extra de forma inteligente.",
            self,
        )
        info.setWordWrap(True)
        info.setStyleSheet("font-size: 11px; color: #A0AAB4;")
        list_layout.addWidget(info)

        layout.addWidget(group_list)
        self.body_layout.addLayout(layout)

    def _load_data(self) -> None:
        default_tpl = config.get("anki.default_template", "Basic")
        idx = self.combo_default_type.findText(default_tpl)
        if idx >= 0:
            self.combo_default_type.setCurrentIndex(idx)

    def accept(self) -> None:
        try:
            chosen = self.combo_default_type.currentText()
            config.set("anki.default_template", chosen, save=True)
            logger.info(f"[TemplatesDialog] Updated default template to '{chosen}'.")
            super().accept()
        except Exception as e:
            logger.error(f"[TemplatesDialog] Error saving template preference: {e}")
