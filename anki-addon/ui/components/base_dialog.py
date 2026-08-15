"""
Standard Base Dialog Component for Anki Discord Toolkit.
Provides unified padding, header hierarchy, and styling for all toolkit dialogs.
"""

from typing import Any, Optional

try:
    from ...core.constants import ADDON_NAME
    from ...core.logger import logger
    from ...theme.palette import PALETTE
except (ImportError, ValueError):
    try:
        from ..core.constants import ADDON_NAME
        from ..core.logger import logger
        from ..theme.palette import PALETTE
    except (ImportError, ValueError):
        from core.constants import ADDON_NAME
        from core.logger import logger
        from theme.palette import PALETTE

# Qt Imports with graceful fallback
try:
    from aqt.qt import (
        QDialog,
        QFrame,
        QHBoxLayout,
        QLabel,
        QPushButton,
        QVBoxLayout,
        QWidget,
        Qt,
    )
    QT_AVAILABLE = True
except ImportError:
    try:
        from PyQt6.QtCore import Qt
        from PyQt6.QtWidgets import (
            QDialog,
            QFrame,
            QHBoxLayout,
            QLabel,
            QPushButton,
            QVBoxLayout,
            QWidget,
        )
        QT_AVAILABLE = True
    except ImportError:
        try:
            from PyQt5.QtCore import Qt
            from PyQt5.QtWidgets import (
                QDialog,
                QFrame,
                QHBoxLayout,
                QLabel,
                QPushButton,
                QVBoxLayout,
                QWidget,
            )
            QT_AVAILABLE = True
        except ImportError:
            QDialog = object
            QT_AVAILABLE = False


class BaseToolkitDialog(QDialog if QT_AVAILABLE else object):
    """
    Standardized base modal dialog with dark UI header and action buttons.
    """
    def __init__(self, parent: Optional[Any] = None, title: str = "Toolkit Dialog", subtitle: str = "") -> None:
        if not QT_AVAILABLE:
            logger.debug(f"[BaseDialog] Qt unavailable. Simulated dialog '{title}'")
            return

        super().__init__(parent)
        self.setWindowTitle(f"{ADDON_NAME} — {title}")
        self.setMinimumSize(560, 420)
        if hasattr(Qt, "WindowType"):
            self.setWindowFlags(self.windowFlags() & ~Qt.WindowType.WindowContextHelpButtonHint)

        # Root Layout
        self.root_layout = QVBoxLayout(self)
        self.root_layout.setContentsMargins(20, 20, 20, 20)
        self.root_layout.setSpacing(14)

        # Header Container
        self.header_widget = QWidget(self)
        header_layout = QVBoxLayout(self.header_widget)
        header_layout.setContentsMargins(0, 0, 0, 4)
        header_layout.setSpacing(4)

        self.title_label = QLabel(title, self.header_widget)
        self.title_label.setStyleSheet("font-size: 18px; font-weight: 700; color: #FFFFFF;")
        header_layout.addWidget(self.title_label)

        if subtitle:
            self.subtitle_label = QLabel(subtitle, self.header_widget)
            self.subtitle_label.setStyleSheet("font-size: 12px; color: #A0AAB4;")
            header_layout.addWidget(self.subtitle_label)

        self.root_layout.addWidget(self.header_widget)

        # Subtle Header Divider
        divider = QFrame(self)
        if hasattr(QFrame, "Shape"):
            divider.setFrameShape(QFrame.Shape.HLine)
        divider.setStyleSheet(f"background-color: {PALETTE.BORDER_SUBTLE}; max-height: 1px; margin-bottom: 6px;")
        self.root_layout.addWidget(divider)

        # Body Container
        self.body_widget = QWidget(self)
        self.body_layout = QVBoxLayout(self.body_widget)
        self.body_layout.setContentsMargins(0, 0, 0, 0)
        self.body_layout.setSpacing(12)
        self.root_layout.addWidget(self.body_widget, stretch=1)

        # Bottom Button Bar
        self.button_layout = QHBoxLayout()
        self.button_layout.setContentsMargins(0, 8, 0, 0)
        self.button_layout.setSpacing(10)
        self.button_layout.addStretch()

        self.btn_cancel = QPushButton("Fechar", self)
        self.btn_cancel.clicked.connect(self.reject)
        self.button_layout.addWidget(self.btn_cancel)

        self.btn_save = QPushButton("Salvar", self)
        self.btn_save.setDefault(True)
        self.btn_save.clicked.connect(self.accept)
        self.button_layout.addWidget(self.btn_save)

        self.root_layout.addLayout(self.button_layout)
