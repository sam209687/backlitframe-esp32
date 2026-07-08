"""
sidebar.py

Application sidebar navigation.
"""

from PySide6.QtCore import Signal
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QPushButton,
    QLabel,
)


class Sidebar(QWidget):

    page_changed = Signal(str)

    def __init__(self):
        super().__init__()

        self.buttons = {}
        self.build_ui()

    def build_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(12, 16, 12, 16)
        layout.setSpacing(8)

        title = QLabel("Smart Showroom AI")
        title.setStyleSheet(
            """
            font-size:16px;
            font-weight:700;
            padding:8px;
            """
        )
        layout.addWidget(title)

        pages = [
            "Dashboard",
            "Products",
            "Devices",
            "LED Effects",
            "Media",
            "Voice",
            "Settings",
        ]

        for page_name in pages:
            button = QPushButton(page_name)
            button.setMinimumHeight(40)

            button.clicked.connect(
                lambda checked=False, name=page_name: self.on_page_clicked(name)
            )

            self.buttons[page_name] = button
            layout.addWidget(button)

        layout.addStretch()

    def on_page_clicked(self, page_name):
        print("Sidebar clicked:", page_name)
        self.page_changed.emit(page_name)