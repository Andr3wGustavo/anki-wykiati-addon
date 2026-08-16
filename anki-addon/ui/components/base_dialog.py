"""
Base Modal Dialog for Anki Wykiati Toolkit with iOS Liquid Glass styling.
Provides clean English header layout, translucent action buttons, and responsive geometry.
"""

from typing import Any, Optional

try:
    from ...core.config import config
    from ...theme.palette import PALETTE, is_light_color
    from ...theme.styles import generate_qss
except (ImportError, ValueError):
    try:
        from ..core.config import config
        from ..theme.palette import PALETTE, is_light_color
        from ..theme.styles import generate_qss
    except (ImportError, ValueError):
        from core.config import config
        from theme.palette import PALETTE, is_light_color
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
        width: int = 580,
        height: int = 460,
    ) -> None:
        if not QT_AVAILABLE:
            return
        super().__init__(parent)

        self.setWindowTitle(title)
        self.resize(width, height)
        self.setMinimumSize(440, 320)

        try:
            if hasattr(Qt, "WidgetAttribute") and hasattr(Qt.WidgetAttribute, "WA_StyledBackground"):
                self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        except Exception:
            pass

        # Allow resizing & maximizing
        if hasattr(self, "setSizeGripEnabled"):
            self.setSizeGripEnabled(True)

        # Apply adaptive theme stylesheet
        bg = config.get("theme.background", PALETTE.BACKGROUND_PURE_BLACK)
        accent = config.get("theme.accent", PALETTE.ACCENT_PRIMARY)
        self.setStyleSheet(generate_qss(accent=accent, bg_color=bg))

        is_light = is_light_color(bg)
        title_color = "#09090B" if is_light else "#FFFFFF"
        sub_color = "#3F3F46" if is_light else "#A1A1AA"
        border_color = "rgba(0, 0, 0, 0.10)" if is_light else "rgba(255, 255, 255, 0.08)"

        self._root_layout = QVBoxLayout(self)
        self._root_layout.setContentsMargins(18, 16, 18, 16)
        self._root_layout.setSpacing(12)

        # Header Frame (Fixed Top - Minimalist Linear style)
        header_frame = QFrame(self)
        header_frame.setStyleSheet(
            f"background: transparent; "
            f"border-bottom: 1px solid {border_color}; "
            f"padding-bottom: 8px; margin-bottom: 2px;"
        )
        header_layout = QVBoxLayout(header_frame)
        header_layout.setContentsMargins(0, 0, 0, 0)
        header_layout.setSpacing(2)

        self.lbl_title = QLabel(title, header_frame)
        self.lbl_title.setStyleSheet(f"font-size: 15px; font-weight: 700; color: {title_color}; letter-spacing: -0.01em;")
        header_layout.addWidget(self.lbl_title)

        if subtitle:
            self.lbl_subtitle = QLabel(subtitle, header_frame)
            self.lbl_subtitle.setStyleSheet(f"font-size: 11px; color: {sub_color}; line-height: 1.4;")
            self.lbl_subtitle.setWordWrap(True)
            header_layout.addWidget(self.lbl_subtitle)

        self._root_layout.addWidget(header_frame)

        # Responsive Body Scroll Area (Vertical-Only Scrolling)
        self.scroll_area = QScrollArea(self)
        self.scroll_area.setWidgetResizable(True)
        try:
            if hasattr(Qt, "ScrollBarPolicy"):
                self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
                self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
            elif hasattr(Qt, "ScrollBarAlwaysOff"):
                self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
                self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        except Exception:
            pass

        try:
            if hasattr(QFrame, "Shape") and hasattr(QFrame.Shape, "NoFrame"):
                self.scroll_area.setFrameShape(QFrame.Shape.NoFrame)
            elif hasattr(QFrame, "NoFrame"):
                self.scroll_area.setFrameShape(QFrame.NoFrame)
        except Exception:
            pass

        self.scroll_area.setStyleSheet(
            "QScrollArea { background: transparent; border: none; }"
            "QScrollBar:vertical { background: transparent; width: 6px; margin: 0; }"
            "QScrollBar::handle:vertical { background: rgba(255, 255, 255, 0.18); border-radius: 3px; min-height: 24px; }"
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
        footer_layout.setContentsMargins(0, 8, 0, 0)
        footer_layout.setSpacing(10)
        footer_layout.addStretch()

        self.btn_cancel = QPushButton("Cancel", self)
        self.btn_cancel.clicked.connect(self.reject)
        footer_layout.addWidget(self.btn_cancel)

        self.btn_save = QPushButton("Save Changes", self)
        self.btn_save.setProperty("primary", "true")
        self.btn_save.clicked.connect(self.accept)
        footer_layout.addWidget(self.btn_save)

        self._root_layout.addLayout(footer_layout)

