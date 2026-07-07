"""
base_combo_box.py

Reusable ComboBox

Features
--------
✓ Searchable
✓ Icons
✓ Placeholder
✓ Dynamic Data
✓ Theme Aware
✓ Editable Search
"""

import qtawesome as qta

from PySide6.QtCore import Qt

from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QComboBox,
    QPushButton,
    QHBoxLayout,
    QVBoxLayout,
    QCompleter
)

from app.ui_comp.theme import ThemeManager


class BaseComboBox(QWidget):

    def __init__(
        self,
        label="",
        placeholder="Select...",
        icon=None,
        parent=None,
    ):

        super().__init__(parent)

        self.theme = ThemeManager.current()

        self.layout = QVBoxLayout(self)

        self.layout.setContentsMargins(0, 0, 0, 0)

        self.layout.setSpacing(6)

        # ---------------- Label ----------------

        self.label = QLabel(label)

        self.layout.addWidget(self.label)

        # ---------------- Container ----------------

        self.container = QWidget()

        self.container_layout = QHBoxLayout(self.container)

        self.container_layout.setContentsMargins(10, 6, 10, 6)

        self.container_layout.setSpacing(8)

        # ---------------- Icon ----------------

        if icon:

            self.icon = QLabel()

            self.icon.setPixmap(
                qta.icon(
                    icon,
                    color=self.theme.text_secondary
                ).pixmap(18, 18)
            )

            self.container_layout.addWidget(self.icon)

        # ---------------- Combo ----------------

        self.combo = QComboBox()

        self.combo.setEditable(True)

        self.combo.lineEdit().setPlaceholderText(
            placeholder
        )

        completer = QCompleter(self.combo)

        completer.setCaseSensitivity(
            Qt.CaseInsensitive
        )

        completer.setFilterMode(
            Qt.MatchContains
        )

        self.combo.setCompleter(completer)

        self.container_layout.addWidget(self.combo)

        # ---------------- Clear ----------------

        self.clear_button = QPushButton("✕")

        self.clear_button.setFixedSize(22, 22)

        self.clear_button.clicked.connect(
            self.combo.setCurrentIndex
        )

        self.container_layout.addWidget(
            self.clear_button
        )

        self.layout.addWidget(
            self.container
        )

        self.refresh()

    # -------------------------------------------------

    def refresh(self):

        t = self.theme

        self.label.setStyleSheet(f"""
        color:{t.text_secondary};
        font-size:{t.small_size}px;
        background:transparent;
        """)

        self.container.setStyleSheet(f"""
        QWidget{{
            background:{t.surface};
            border:1px solid {t.border};
            border-radius:{t.radius_md}px;
        }}
        """)

        self.combo.setStyleSheet(f"""

        QComboBox{{
            border:none;
            background:transparent;
            padding:6px;
            color:{t.text};
        }}

        QComboBox::drop-down{{
            border:none;
            width:20px;
        }}

        QComboBox QAbstractItemView{{
            background:{t.card};
            color:{t.text};
            selection-background-color:{t.primary};
            border:1px solid {t.border};
        }}

        """)

        self.clear_button.setStyleSheet(f"""

        QPushButton{{
            border:none;
            background:transparent;
            color:{t.text_secondary};
        }}

        QPushButton:hover{{
            color:{t.primary};
        }}

        """)

    # -------------------------------------------------

    def add_item(
        self,
        text,
        data=None,
    ):

        self.combo.addItem(
            text,
            data
        )

    def add_items(
        self,
        values
    ):

        self.combo.addItems(values)

    def clear(self):

        self.combo.clear()

    def current_text(self):

        return self.combo.currentText()

    def current_data(self):

        return self.combo.currentData()

    def set_current_text(
        self,
        text
    ):

        index = self.combo.findText(text)

        if index >= 0:
            self.combo.setCurrentIndex(index)

    def set_items(
        self,
        values
    ):

        self.combo.clear()

        self.combo.addItems(values)

    def current_index(self):

        return self.combo.currentIndex()

    def set_current_index(
        self,
        index
    ):

        self.combo.setCurrentIndex(index)

    def widget(self):

        return self.combo