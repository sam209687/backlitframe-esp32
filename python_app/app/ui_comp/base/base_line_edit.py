"""
base_line_edit.py

Universal Line Edit for Smart Showroom

Supports
--------
✓ Normal text
✓ Search
✓ Password
✓ Numbers
✓ Placeholder
✓ Icons
✓ Clear Button
✓ Validation Colors
"""

import qtawesome as qta

from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QLineEdit,
    QPushButton,
    QHBoxLayout,
    QVBoxLayout,
)

from PySide6.QtCore import Qt

from app.ui_comp.theme import ThemeManager


class BaseLineEdit(QWidget):

    def __init__(
        self,
        label="",
        placeholder="",
        icon=None,
        password=False,
        parent=None,
    ):

        super().__init__(parent)

        self.theme = ThemeManager.current()

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

                    color=self.theme.text_secondary

                ).pixmap(18, 18)

            )

            self.container_layout.addWidget(self.icon)

        self.edit = QLineEdit()

        self.edit.setPlaceholderText(placeholder)

        if password:

            self.edit.setEchoMode(QLineEdit.Password)

        self.container_layout.addWidget(self.edit)

        self.clear_btn = QPushButton("✕")

        self.clear_btn.setCursor(Qt.PointingHandCursor)

        self.clear_btn.clicked.connect(self.edit.clear)

        self.clear_btn.setFixedSize(22, 22)

        self.container_layout.addWidget(self.clear_btn)

        self.layout.addWidget(self.container)

        self.refresh()

    # ------------------------------------------------

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

        self.edit.setStyleSheet(f"""
        QLineEdit{{
            border:none;
            background:transparent;
            color:{t.text};
            padding:6px;
            font-size:{t.body_size}px;
        }}
        """)

        self.clear_btn.setStyleSheet(f"""
        QPushButton{{
            border:none;
            background:transparent;
            color:{t.text_secondary};
            font-size:14px;
        }}

        QPushButton:hover{{
            color:{t.primary};
        }}
        """)

    # ------------------------------------------------

    def text(self):

        return self.edit.text()

    def setText(self, value):

        self.edit.setText(value)

    def clear(self):

        self.edit.clear()

    def setPlaceholder(self, text):

        self.edit.setPlaceholderText(text)

    def setReadOnly(self, value):

        self.edit.setReadOnly(value)

    def setDisabled(self, value):

        self.edit.setDisabled(value)

    # ------------------------------------------------

    def set_error(self):

        self.container.setStyleSheet(f"""
        QWidget{{
            background:{self.theme.surface};
            border:2px solid {self.theme.danger};
            border-radius:{self.theme.radius_md}px;
        }}
        """)

    def set_success(self):

        self.container.setStyleSheet(f"""
        QWidget{{
            background:{self.theme.surface};
            border:2px solid {self.theme.success};
            border-radius:{self.theme.radius_md}px;
        }}
        """)

    def reset(self):

        self.refresh()