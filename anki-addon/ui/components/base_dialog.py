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
        QScrollArea,
        QSizePolicy,
        QVBoxLayout,
        QWidget,
        Qt,
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
            QScrollArea,
            QSizePolicy,
            QVBoxLayout,
            QWidget,
        )
        from PyQt6.QtCore import Qt
        QT_AVAILABLE = True
    except ImportError:
        try:
            from PyQt5.QtWidgets import (
                QDialog,
                QFrame,
                QHBoxLayout,
                QLabel,
                QPushButton,
                QScrollArea,
                QSizePolicy,
                QVBoxLayout,
                QWidget,
            )
            from PyQt5.QtCore import Qt
            QT_AVAILABLE = True
        except ImportError:
            QDialog = QFrame = QHBoxLayout = QLabel = QPushButton = QScrollArea = QSizePolicy = QVBoxLayout = QWidget = Qt = object
            QT_AVAILABLE = False


class BaseToolkitDialog(QDialog):
    """
    Standard base dialog with Void Black background, square glass cards,
    and a fluid, responsive scrollable body container.
    """
    def __init__(
        self,
        parent: Optional[Any] = None,
        title: str = "Wykiati Toolkit",
        subtitle: str = "",
        width: int = 640,
        height: int = 540,
    ) -> None:
        if not QT_AVAILABLE:
            return
        super().__init__(parent)

        self.setWindowTitle(title)
        self.resize(width, height)
        self.setMinimumSize(480, 360)

        # Allow resizing & maximizing
        if hasattr(self, "setSizeGripEnabled"):
            self.setSizeGripEnabled(True)

        # Apply zero-lag glass stylesheet
        self.setStyleSheet(generate_qss())

        self._root_layout = QVBoxLayout(self)
        self._root_layout.setContentsMargins(16, 16, 16, 16)
        self._root_layout.setSpacing(12)

        # Header Frame (Fixed Top)
        header_frame = QFrame(self)
        header_frame.setStyleSheet(
            f"background-color: {PALETTE.BACKGROUND_SURFACE}; "
            f"border: 1px solid {PALETTE.BORDER_DEFAULT}; "
            f"border-radius: 6px; padding: 10px;"
        )
        header_layout = QVBoxLayout(header_frame)
        header_layout.setContentsMargins(8, 4, 8, 4)
        header_layout.setSpacing(3)

        self.lbl_title = QLabel(title, header_frame)
        self.lbl_title.setStyleSheet("font-size: 15px; font-weight: bold; color: #FFFFFF;")
        header_layout.addWidget(self.lbl_title)

        if subtitle:
            self.lbl_subtitle = QLabel(subtitle, header_frame)
            self.lbl_subtitle.setStyleSheet(f"font-size: 12px; color: {PALETTE.TEXT_MUTED};")
            self.lbl_subtitle.setWordWrap(True)
            header_layout.addWidget(self.lbl_subtitle)

        self._root_layout.addWidget(header_frame)

        # Responsive Body Scroll Area (makes ALL panels scrollable & responsive)
        self.scroll_area = QScrollArea(self)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setFrameShape(QFrame.Shape.NoFrame if hasattr(QFrame, "Shape") else 0)
        self.scroll_area.setStyleSheet(
            "QScrollArea { background: transparent; border: none; }"
            "QScrollBar:vertical { background: transparent; width: 6px; margin: 0; }"
            "QScrollBar::handle:vertical { background: rgba(255, 255, 255, 0.20); border-radius: 3px; min-height: 24px; }"
            "QScrollBar::handle:vertical:hover { background: rgba(255, 255, 255, 0.35); }"
        )

        self.scroll_content = QWidget()
        self.scroll_content.setStyleSheet("background: transparent;")
        
        self.body_layout = QVBoxLayout(self.scroll_content)
        self.body_layout.setContentsMargins(0, 4, 4, 4)
        self.body_layout.setSpacing(12)

        self.scroll_area.setWidget(self.scroll_content)
        self._root_layout.addWidget(self.scroll_area, 1)

        # Footer Actions (Fixed Bottom)
        footer_layout = QHBoxLayout()
        footer_layout.setContentsMargins(0, 4, 0, 0)
        footer_layout.addStretch()

        self.btn_cancel = QPushButton("Cancel", self)
        self.btn_cancel.clicked.connect(self.reject)
        footer_layout.addWidget(self.btn_cancel)

        self.btn_save = QPushButton("Save Changes", self)
        self.btn_save.setProperty("primary", "true")
        self.btn_save.clicked.connect(self.accept)
        footer_layout.addWidget(self.btn_save)

        self._root_layout.addLayout(footer_layout)

