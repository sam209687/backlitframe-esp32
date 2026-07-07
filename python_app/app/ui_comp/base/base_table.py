"""
base_table.py

Reusable Smart Table

Features
--------
✓ Sorting
✓ Alternate Row Colors
✓ Full Row Selection
✓ Search Ready
✓ Double Click Signal
✓ Context Menu Ready
✓ Theme Aware
"""

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QHeaderView,
    QTableWidget,
    QTableWidgetItem,
)

from app.ui_comp.theme import ThemeManager


class BaseTable(QTableWidget):

    def __init__(self, parent=None):

        super().__init__(parent)

        self.theme = ThemeManager.current()

        self.initialize()

    # --------------------------------------------------

    def initialize(self):

        self.setAlternatingRowColors(True)

        self.setSortingEnabled(True)

        self.setSelectionBehavior(
            QTableWidget.SelectRows
        )

        self.setSelectionMode(
            QTableWidget.SingleSelection
        )

        self.setEditTriggers(
            QTableWidget.NoEditTriggers
        )

        self.verticalHeader().hide()

        self.horizontalHeader().setStretchLastSection(True)

        self.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeToContents
        )

        self.setShowGrid(False)

        self.refresh_theme()

    # --------------------------------------------------

    def refresh_theme(self):

        t = self.theme

        self.setStyleSheet(f"""

        QTableWidget{{

            background:{t.card};

            border:1px solid {t.border};

            border-radius:{t.radius_md}px;

            gridline-color:{t.divider};

            alternate-background-color:{t.surface};

            color:{t.text};

        }}

        QHeaderView::section{{

            background:{t.surface_alt};

            color:{t.text};

            padding:8px;

            border:none;

            font-weight:bold;

        }}

        QTableWidget::item{{

            padding:8px;

        }}

        QTableWidget::item:selected{{

            background:{t.primary};

            color:white;

        }}

        """)

    # --------------------------------------------------

    def set_headers(self, headers):

        self.setColumnCount(len(headers))

        self.setHorizontalHeaderLabels(headers)

    # --------------------------------------------------

    def add_row(self, values):

        row = self.rowCount()

        self.insertRow(row)

        for col, value in enumerate(values):

            item = QTableWidgetItem(str(value))

            item.setFlags(
                item.flags() & ~Qt.ItemIsEditable
            )

            self.setItem(row, col, item)

    # --------------------------------------------------

    def set_data(self, rows):

        self.setRowCount(0)

        for row in rows:

            self.add_row(row)

    # --------------------------------------------------

    def selected_row(self):

        row = self.currentRow()

        if row < 0:
            return None

        values = []

        for col in range(self.columnCount()):

            item = self.item(row, col)

            values.append("" if item is None else item.text())

        return values

    # --------------------------------------------------

    def clear_rows(self):

        self.setRowCount(0)

    # --------------------------------------------------

    def selected_value(self, column=0):

        row = self.currentRow()

        if row < 0:
            return None

        item = self.item(row, column)

        if item:

            return item.text()

        return None