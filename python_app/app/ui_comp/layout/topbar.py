"""
topbar.py
"""

from PySide6.QtCore import Signal
from PySide6.QtWidgets import QWidget, QLabel, QHBoxLayout, QApplication

from app.ui_comp.base import BaseButton, BaseLineEdit
from app.ui_comp.theme import ThemeManager, Style


class TopBar(QWidget):

    theme_changed = Signal()

    def __init__(self):

        super().__init__()

        layout = QHBoxLayout(self)
        layout.setContentsMargins(18, 10, 18, 10)
        layout.setSpacing(12)

        self.logo = QLabel("Smart Showroom AI")
        self.logo.setStyleSheet("""
            font-size:18px;
            font-weight:800;
            background:transparent;
        """)

        self.search = BaseLineEdit(
            placeholder="Search...",
            icon="fa5s.search"
        )
        self.search.setFixedWidth(320)

        self.theme_btn = BaseButton(
            "Theme",
            icon="fa5s.moon",
            button_type=BaseButton.SECONDARY
        )
        self.theme_btn.clicked.connect(self.toggle_theme)

        layout.addWidget(self.logo)
        layout.addStretch()
        layout.addWidget(self.search)
        layout.addWidget(self.theme_btn)

    def toggle_theme(self):

        ThemeManager.toggle()

        app = QApplication.instance()

        if app:
            app.setStyleSheet(Style.build())

        self.theme_changed.emit()