"""
Base Modal Dialog for Anki Wykiati Toolkit with iOS Liquid Glass styling.
Provides clean English header layout, translucent action buttons, and responsive geometry.
"""

from typing import Any, Optional

try:
    from ...theme.palette import PALETTE
    from ...theme.styles import generate_qss
except (ImportError, ValueError):
    try:
        from ..theme.palette import PALETTE
        from ..theme.styles import generate_qss
    except (ImportError, ValueError):
        from theme.palette import PALETTE
        from theme.styles import generate_qss

# Qt Imports
try:
    from aqt.qt import (
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
            QDialog = QFrame = QHBoxLayout = QLabel = QPushButton = QVBoxLayout = QWidget = object
            QT_AVAILABLE = False


class BaseToolkitDialog(QDialog):
    """
    Standard base dialog with iOS Liquid Glass header, body layout, and footer actions.
    """
    def __init__(
        self,
        parent: Optional[Any] = None,
        title: str = "Wykiati Toolkit",
        subtitle: str = "",
        width: int = 560,
        height: int = 420,
    ) -> None:
        if not QT_AVAILABLE:
            return
        super().__init__(parent)

        self.setWindowTitle(title)
        self.resize(width, height)
        self.setMinimumSize(460, 320)

        # Apply glass stylesheet
        self.setStyleSheet(generate_qss())

        self._root_layout = QVBoxLayout(self)
        self._root_layout.setContentsMargins(18, 18, 18, 18)
        self._root_layout.setSpacing(14)

        # Header Frame
        header_frame = QFrame(self)
        header_frame.setStyleSheet(
            f"background-color: {PALETTE.BACKGROUND_SURFACE}; "
            f"border: 1px solid {PALETTE.BORDER_DEFAULT}; "
            f"border-radius: 12px; padding: 12px;"
        )
        header_layout = QVBoxLayout(header_frame)
        header_layout.setContentsMargins(8, 4, 8, 4)
        header_layout.setSpacing(3)

        self.lbl_title = QLabel(title, header_frame)
        self.lbl_title.setStyleSheet("font-size: 16px; font-weight: bold; color: #FFFFFF;")
        header_layout.addWidget(self.lbl_title)

        if subtitle:
            self.lbl_subtitle = QLabel(subtitle, header_frame)
            self.lbl_subtitle.setStyleSheet(f"font-size: 12px; color: {PALETTE.TEXT_MUTED};")
            header_layout.addWidget(self.lbl_subtitle)

        self._root_layout.addWidget(header_frame)

        # Body Layout (subclasses insert content here)
        self.body_layout = QVBoxLayout()
        self.body_layout.setSpacing(12)
        self._root_layout.addLayout(self.body_layout, 1)

        # Footer Actions
        footer_layout = QHBoxLayout()
        footer_layout.addStretch()

        self.btn_cancel = QPushButton("Cancel", self)
        self.btn_cancel.clicked.connect(self.reject)
        footer_layout.addWidget(self.btn_cancel)

        self.btn_save = QPushButton("Save Changes", self)
        self.btn_save.setProperty("primary", "true")
        self.btn_save.clicked.connect(self.accept)
        footer_layout.addWidget(self.btn_save)

        self._root_layout.addLayout(footer_layout)
