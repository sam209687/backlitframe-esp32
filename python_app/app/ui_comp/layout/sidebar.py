"""
Modern Sidebar
"""

from PySide6.QtCore import Signal

from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
)

from app.ui_comp.base import BaseButton


class Sidebar(QWidget):

    page_changed = Signal(str)

    def __init__(self):

        super().__init__()

        self.setFixedWidth(220)

        layout = QVBoxLayout(self)

        layout.setContentsMargins(12,12,12,12)

        layout.setSpacing(8)

        pages = [

            ("Dashboard","fa5s.home"),

            ("Products","fa5s.box"),

            ("LED Effects","fa5s.lightbulb"),

            ("Media","fa5s.images"),

            ("Voice","fa5s.microphone"),

            ("Scheduler","fa5s.clock"),

            ("Relay","fa5s.plug"),

            ("Settings","fa5s.cog"),

        ]

        for name,icon in pages:

            btn = BaseButton(

                name,

                icon=icon,

                button_type=BaseButton.SECONDARY

            )

            btn.clicked.connect(

                lambda _,n=name:

                self.page_changed.emit(n)

            )

            layout.addWidget(btn)

        layout.addStretch()