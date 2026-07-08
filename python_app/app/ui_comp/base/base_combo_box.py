"""
base_combo_box.py

Reusable premium combo box.
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
    QCompleter,
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
        self.placeholder = placeholder

        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(6)

        self.label = QLabel(label)
        self.layout.addWidget(self.label)

        self.container = QWidget()
        self.container_layout = QHBoxLayout(self.container)
        self.container_layout.setContentsMargins(10, 6, 10, 6)
        self.container_layout.setSpacing(8)

        if icon:
            self.icon = QLabel()
            self.icon.setPixmap(
                qta.icon(
                    icon,
                    color=self.theme.text_secondary,
                ).pixmap(18, 18)
            )
            self.container_layout.addWidget(self.icon)

        self.combo = QComboBox()
        self.combo.setEditable(True)
        self.combo.setMinimumHeight(34)
        self.combo.setInsertPolicy(QComboBox.NoInsert)

        self.combo.lineEdit().setPlaceholderText(placeholder)

        completer = QCompleter(self.combo)
        completer.setCaseSensitivity(Qt.CaseInsensitive)
        completer.setFilterMode(Qt.MatchContains)

        self.combo.setCompleter(completer)

        self.container_layout.addWidget(self.combo, 1)

        self.clear_button = QPushButton("✕")
        self.clear_button.setFixedSize(22, 22)
        self.clear_button.clicked.connect(self.clear_selection)

        self.container_layout.addWidget(self.clear_button)

        self.layout.addWidget(self.container)

        self.refresh()

    def refresh(self):
        t = self.theme

        self.label.setStyleSheet(f"""
            color:{t.text_secondary};
            font-size:{t.small_size}px;
            background:transparent;
        """)

        self.container.setStyleSheet(f"""
            QWidget {{
                background:{t.surface};
                border:1px solid {t.border};
                border-radius:{t.radius_md}px;
            }}
        """)

        self.combo.setStyleSheet(f"""
            QComboBox {{
                border:none;
                background:transparent;
                color:{t.text};
                padding:6px;
                font-size:14px;
            }}

            QComboBox::drop-down {{
                border:none;
                width:28px;
            }}

            QComboBox::down-arrow {{
                image:none;
                border-left:5px solid transparent;
                border-right:5px solid transparent;
                border-top:6px solid {t.text_secondary};
                width:0px;
                height:0px;
                margin-right:8px;
            }}

            QComboBox QAbstractItemView {{
                background:{t.card};
                color:{t.text};
                selection-background-color:{t.primary};
                selection-color:white;
                border:1px solid {t.border};
                padding:6px;
                outline:none;
            }}

            QLineEdit {{
                border:none;
                background:transparent;
                color:{t.text};
                padding:4px;
            }}
        """)

        self.clear_button.setStyleSheet(f"""
            QPushButton {{
                border:none;
                background:transparent;
                color:{t.text_secondary};
            }}

            QPushButton:hover {{
                color:{t.primary};
            }}
        """)

    def add_item(self, text, data=None):
        self.combo.addItem(text, data)

    def add_items(self, values):
        for value in values:
            self.combo.addItem(value, value)

    def set_items(self, values):
        self.combo.clear()
        self.add_items(values)

    def clear(self):
        self.combo.clear()

    def clear_selection(self):
        self.combo.setCurrentIndex(-1)
        self.combo.lineEdit().clear()
        self.combo.lineEdit().setPlaceholderText(self.placeholder)

    def current_text(self):
        return self.combo.currentText()

    def current_data(self):
        return self.combo.currentData()

    def set_current_text(self, text):
        index = self.combo.findText(text)

        if index >= 0:
            self.combo.setCurrentIndex(index)

    def current_index(self):
        return self.combo.currentIndex()

    def set_current_index(self, index):
        self.combo.setCurrentIndex(index)

    def widget(self):
        return self.combo