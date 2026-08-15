"""
Smart Deck Routing Rules Dialog for Anki Wykiati Toolkit.
Interactive table manager for tag-based and keyword-based smart deck routing.
"""

from typing import Any, Dict, List, Optional

try:
    from ..anki.decks import deck_adapter
    from ..core.config import config
    from ..core.logger import logger
    from ..routing.router import deck_router
    from .components.base_dialog import BaseToolkitDialog, QT_AVAILABLE
except (ImportError, ValueError):
    from anki.decks import deck_adapter
    from core.config import config
    from core.logger import logger
    from routing.router import deck_router
    from ui.components.base_dialog import BaseToolkitDialog, QT_AVAILABLE

if QT_AVAILABLE:
    try:
        from aqt.qt import (
            QComboBox,
            QHBoxLayout,
            QHeaderView,
            QLabel,
            QLineEdit,
            QPushButton,
            QTableWidget,
            QTableWidgetItem,
            QVBoxLayout,
        )
    except ImportError:
        try:
            from PyQt6.QtWidgets import (
                QComboBox,
                QHBoxLayout,
                QHeaderView,
                QLabel,
                QLineEdit,
                QPushButton,
                QTableWidget,
                QTableWidgetItem,
                QVBoxLayout,
            )
        except ImportError:
            from PyQt5.QtWidgets import (
                QComboBox,
                QHBoxLayout,
                QHeaderView,
                QLabel,
                QLineEdit,
                QPushButton,
                QTableWidget,
                QTableWidgetItem,
                QVBoxLayout,
            )
else:
    QComboBox = QHBoxLayout = QHeaderView = QLabel = QLineEdit = QPushButton = QTableWidget = QTableWidgetItem = QVBoxLayout = object


class DeckRulesDialog(BaseToolkitDialog):
    """
    Dialog for configuring automatic card-to-deck routing rules.
    """
    def __init__(self, parent: Optional[Any] = None) -> None:
        super().__init__(
            parent,
            title="Smart Deck Routing Rules",
            subtitle="Automatically route cards to target decks based on tags or message keywords.",
        )
        if not QT_AVAILABLE:
            return

        self._build_ui()
        self._load_rules()

    def _build_ui(self) -> None:
        main_layout = QVBoxLayout()
        main_layout.setSpacing(10)

        # Default Deck selector
        default_layout = QHBoxLayout()
        default_layout.addWidget(QLabel("Default Fallback Deck:", self))
        self.txt_default_deck = QLineEdit(self)
        self.txt_default_deck.setText(config.get("anki.default_deck", "Default"))
        default_layout.addWidget(self.txt_default_deck)
        main_layout.addLayout(default_layout)

        # Rules Table
        self.table = QTableWidget(self)
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["Match Type", "Pattern / Term", "Target Deck"])
        if hasattr(self.table.horizontalHeader(), "setStretchLastSection"):
            self.table.horizontalHeader().setStretchLastSection(True)
        main_layout.addWidget(self.table)

        # Action Buttons (Add, Remove)
        btn_layout = QHBoxLayout()
        self.btn_add = QPushButton("Add Rule", self)
        self.btn_add.clicked.connect(self._add_empty_row)
        btn_layout.addWidget(self.btn_add)

        self.btn_remove = QPushButton("Remove Selected", self)
        self.btn_remove.clicked.connect(self._remove_selected_row)
        btn_layout.addWidget(self.btn_remove)
        btn_layout.addStretch()

        main_layout.addLayout(btn_layout)

        self.body_layout.addLayout(main_layout)

    def _load_rules() -> None:
        rules = deck_router.get_rules()
        self.table.setRowCount(0)

        for rule in rules:
            self._insert_row(
                rule_type=rule.get("type", "tag"),
                pattern=rule.get("pattern", ""),
                deck=rule.get("deck", ""),
            )

    def _insert_row(self, rule_type: str = "tag", pattern: str = "", deck: str = "") -> None:
        row = self.table.rowCount()
        self.table.insertRow(row)

        combo = QComboBox(self.table)
        combo.addItems(["tag", "keyword"])
        combo.setCurrentText(rule_type)
        self.table.setCellWidget(row, 0, combo)

        item_pattern = QTableWidgetItem(pattern)
        self.table.setItem(row, 1, item_pattern)

        item_deck = QTableWidgetItem(deck)
        self.table.setItem(row, 2, item_deck)

    def _add_empty_row(self) -> None:
        self._insert_row("tag", "new_term", "Medicine::Cardiology")

    def _remove_selected_row(self) -> None:
        curr_row = self.table.currentRow()
        if curr_row >= 0:
            self.table.removeRow(curr_row)

    def accept(self) -> None:
        try:
            rules: List[Dict[str, str]] = []
            for row in range(self.table.rowCount()):
                combo = self.table.cellWidget(row, 0)
                rule_type = combo.currentText() if combo else "tag"

                pattern_item = self.table.item(row, 1)
                pattern = pattern_item.text().strip() if pattern_item else ""

                deck_item = self.table.item(row, 2)
                deck = deck_item.text().strip() if deck_item else ""

                if pattern and deck:
                    rules.append({
                        "type": rule_type,
                        "pattern": pattern,
                        "deck": deck,
                    })

            deck_router.set_rules(rules)
            config.set("anki.default_deck", self.txt_default_deck.text().strip() or "Default", save=True)

            logger.info(f"[DeckRulesDialog] Saved {len(rules)} deck routing rules.")
            super().accept()
        except Exception as e:
            logger.error(f"[DeckRulesDialog] Error saving rules: {e}")
