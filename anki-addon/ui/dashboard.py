"""
Rich Operational Dashboard for Anki Wykiati Toolkit.
Provides real-time statistics, job queue visualization, manual test card creation, and bridge health status.
"""

from datetime import datetime
import time
from typing import Any, Optional

try:
    from ..core.config import config
    from ..core.constants import ADDON_NAME, ADDON_VERSION
    from ..core.logger import logger
    from ..discord.bridge import discord_bridge
    from ..discord.models import CardPayload, DiscordChannel, DiscordMessageEvent, DiscordUser
    from ..sync.queue import job_queue
    from ..sync.worker import sync_worker
    from ..theme.palette import PALETTE
    from .components.base_dialog import BaseToolkitDialog, QT_AVAILABLE
except (ImportError, ValueError):
    from core.config import config
    from core.constants import ADDON_NAME, ADDON_VERSION
    from core.logger import logger
    from discord.bridge import discord_bridge
    from discord.models import CardPayload, DiscordChannel, DiscordMessageEvent, DiscordUser
    from sync.queue import job_queue
    from sync.worker import sync_worker
    from theme.palette import PALETTE
    from ui.components.base_dialog import BaseToolkitDialog, QT_AVAILABLE

if QT_AVAILABLE:
    try:
        from aqt.qt import (
            QComboBox,
            QFrame,
            QGridLayout,
            QHBoxLayout,
            QHeaderView,
            QLabel,
            QLineEdit,
            QMessageBox,
            QPushButton,
            QTableWidget,
            QTableWidgetItem,
            QTextEdit,
            QVBoxLayout,
            QWidget,
        )
    except ImportError:
        try:
            from PyQt6.QtWidgets import (
                QComboBox,
                QFrame,
                QGridLayout,
                QHBoxLayout,
                QHeaderView,
                QLabel,
                QLineEdit,
                QMessageBox,
                QPushButton,
                QTableWidget,
                QTableWidgetItem,
                QTextEdit,
                QVBoxLayout,
                QWidget,
            )
        except ImportError:
            from PyQt5.QtWidgets import (
                QComboBox,
                QFrame,
                QGridLayout,
                QHBoxLayout,
                QHeaderView,
                QLabel,
                QLineEdit,
                QMessageBox,
                QPushButton,
                QTableWidget,
                QTableWidgetItem,
                QTextEdit,
                QVBoxLayout,
                QWidget,
            )
else:
    QComboBox = QFrame = QGridLayout = QHBoxLayout = QHeaderView = QLabel = QLineEdit = QMessageBox = QPushButton = QTableWidget = QTableWidgetItem = QTextEdit = QVBoxLayout = QWidget = object


class DashboardDialog(BaseToolkitDialog):
    """
    Main operational dashboard and metrics control center.
    """
    def __init__(self, parent: Optional[Any] = None) -> None:
        super().__init__(
            parent,
            title="Dashboard and Synchronization Monitor",
            subtitle=f"{ADDON_NAME} v{ADDON_VERSION} - Control Center",
        )
        if not QT_AVAILABLE:
            return

        self.setMinimumSize(800, 560)
        self._build_ui()
        self._refresh_data()

    def _build_ui(self) -> None:
        main_layout = QVBoxLayout()
        main_layout.setSpacing(14)

        # 1. Metric Cards Grid
        metrics_grid = QGridLayout()
        metrics_grid.setSpacing(10)

        self.lbl_cards_created = self._create_stat_card("Cards Created", "0", PALETTE.SUCCESS, metrics_grid, 0, 0)
        self.lbl_images_ingested = self._create_stat_card("Images Ingested", "0", PALETTE.ACCENT_PRIMARY, metrics_grid, 0, 1)
        self.lbl_queue_pending = self._create_stat_card("Pending Queue", "0", PALETTE.WARNING, metrics_grid, 0, 2)
        self.lbl_failed_jobs = self._create_stat_card("Failed Jobs", "0", PALETTE.ERROR, metrics_grid, 0, 3)

        main_layout.addLayout(metrics_grid)

        # 2. Quick Card Test Box
        test_frame = QFrame(self)
        test_frame.setStyleSheet(
            f"background-color: {PALETTE.BACKGROUND_SURFACE}; "
            f"border: 1px solid {PALETTE.BORDER_DEFAULT}; "
            f"border-radius: 12px; padding: 10px;"
        )
        test_layout = QVBoxLayout(test_frame)
        test_layout.setSpacing(8)

        test_title = QLabel("Manual Flashcard Quick Creator", test_frame)
        test_title.setStyleSheet("font-weight: bold; color: #FFFFFF; font-size: 13px;")
        test_layout.addWidget(test_title)

        input_row = QHBoxLayout()
        self.txt_front = QLineEdit(test_frame)
        self.txt_front.setPlaceholderText("Front / Question")
        input_row.addWidget(self.txt_front, 2)

        self.txt_back = QLineEdit(test_frame)
        self.txt_back.setPlaceholderText("Back / Answer")
        input_row.addWidget(self.txt_back, 2)

        self.txt_deck = QLineEdit(test_frame)
        self.txt_deck.setPlaceholderText("Deck (e.g. Medicine::Cardiology)")
        input_row.addWidget(self.txt_deck, 1)

        self.txt_tags = QLineEdit(test_frame)
        self.txt_tags.setPlaceholderText("Tags (e.g. test, cardiology)")
        input_row.addWidget(self.txt_tags, 1)

        self.btn_create_test = QPushButton("Create Card", test_frame)
        self.btn_create_test.setProperty("primary", "true")
        self.btn_create_test.clicked.connect(self._create_manual_card)
        input_row.addWidget(self.btn_create_test)

        test_layout.addLayout(input_row)
        main_layout.addWidget(test_frame)

        # 3. Recent Activity & Jobs Table
        table_header_layout = QHBoxLayout()
        table_label = QLabel("Recent Synchronization Jobs", self)
        table_label.setStyleSheet("font-weight: bold; color: #FFFFFF; font-size: 13px;")
        table_header_layout.addWidget(table_label)
        table_header_layout.addStretch()

        self.btn_sync_now = QPushButton("Process Queue Now", self)
        self.btn_sync_now.clicked.connect(self._sync_queue_now)
        table_header_layout.addWidget(self.btn_sync_now)

        self.btn_refresh = QPushButton("Refresh", self)
        self.btn_refresh.clicked.connect(self._refresh_data)
        table_header_layout.addWidget(self.btn_refresh)

        main_layout.addLayout(table_header_layout)

        self.table_jobs = QTableWidget(self)
        self.table_jobs.setColumnCount(5)
        self.table_jobs.setHorizontalHeaderLabels(["Job ID", "Status", "Front Content", "Target Deck", "Time / Note ID"])
        if hasattr(self.table_jobs.horizontalHeader(), "setStretchLastSection"):
            self.table_jobs.horizontalHeader().setStretchLastSection(True)
        main_layout.addWidget(self.table_jobs)

        # Footer Button
        self.btn_save.setVisible(False)
        self.btn_cancel.setText("Close")

        self.body_layout.addLayout(main_layout)

    def _create_stat_card(self, title: str, initial_value: str, color: str, grid: QGridLayout, row: int, col: int) -> QLabel:
        frame = QFrame(self)
        frame.setStyleSheet(
            f"background-color: {PALETTE.BACKGROUND_SURFACE_ELEVATED}; "
            f"border: 1px solid {PALETTE.BORDER_DEFAULT}; "
            f"border-radius: 12px; padding: 10px;"
        )
        layout = QVBoxLayout(frame)
        layout.setContentsMargins(10, 8, 10, 8)
        layout.setSpacing(2)

        lbl_title = QLabel(title, frame)
        lbl_title.setStyleSheet(f"font-size: 11px; color: {PALETTE.TEXT_MUTED}; text-transform: uppercase; font-weight: 600;")
        layout.addWidget(lbl_title)

        lbl_val = QLabel(initial_value, frame)
        lbl_val.setStyleSheet(f"font-size: 22px; font-weight: bold; color: {color};")
        layout.addWidget(lbl_val)

        grid.addWidget(frame, row, col)
        return lbl_val

    def _refresh_data(self) -> None:
        stats = config.get("stats", {})
        cards_created = stats.get("cards_created", 0)
        images_ingested = stats.get("images_ingested", 0)
        failed_jobs = stats.get("failed_jobs", 0)
        queue_stats = job_queue.get_stats()

        self.lbl_cards_created.setText(str(cards_created))
        self.lbl_images_ingested.setText(str(images_ingested))
        self.lbl_queue_pending.setText(str(queue_stats.get("pending", 0)))
        self.lbl_failed_jobs.setText(str(failed_jobs))

        jobs = job_queue.get_all_jobs()
        self.table_jobs.setRowCount(0)

        for job in reversed(jobs[-50:]):
            row = self.table_jobs.rowCount()
            self.table_jobs.insertRow(row)

            # ID
            self.table_jobs.setItem(row, 0, QTableWidgetItem(job.id))

            # Status
            item_status = QTableWidgetItem(job.status.value)
            self.table_jobs.setItem(row, 1, item_status)

            # Front
            front_snippet = job.payload.front[:50] + ("..." if len(job.payload.front) > 50 else "")
            self.table_jobs.setItem(row, 2, QTableWidgetItem(front_snippet))

            # Deck
            self.table_jobs.setItem(row, 3, QTableWidgetItem(job.payload.deck))

            # Time / Details
            time_str = datetime.fromtimestamp(job.timestamp).strftime("%H:%M:%S")
            detail = f"{time_str} (Note #{job.note_id})" if job.note_id else f"{time_str} ({job.error or 'In Queue'})"
            self.table_jobs.setItem(row, 4, QTableWidgetItem(detail))

    def _create_manual_card(self) -> None:
        front = self.txt_front.text().strip()
        back = self.txt_back.text().strip()
        deck = self.txt_deck.text().strip()
        tags = [t.strip() for t in self.txt_tags.text().split(",") if t.strip()]

        if not front:
            return

        raw_text = f"!anki\nfront: {front}\nback: {back}\ndeck: {deck}\ntags: {', '.join(tags)}"
        event = DiscordMessageEvent(
            id=f"manual_{int(time.time()*1000)}",
            content=raw_text,
            author=DiscordUser(id="local_tester", name="Dashboard Manual User"),
            channel=DiscordChannel(id="dashboard_channel"),
            timestamp=time.time(),
        )

        success, msg = discord_bridge.handle_incoming_message(raw_text, event)
        if success:
            self.txt_front.clear()
            self.txt_back.clear()
            self.txt_deck.clear()
            self.txt_tags.clear()
            sync_worker.process_all_pending()
            self._refresh_data()
        else:
            if hasattr(QMessageBox, "warning"):
                QMessageBox.warning(self, "Error Creating Card", msg)

    def _sync_queue_now(self) -> None:
        processed = sync_worker.process_all_pending()
        self._refresh_data()
        logger.info(f"[Dashboard] Manually processed {processed} job(s) from queue.")
