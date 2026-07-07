"""
Top Navigation Bar
"""

from PySide6.QtWidgets import (

    QWidget,

    QLabel,

    QHBoxLayout,

)

from app.ui_comp.base import (

    BaseButton,

    BaseLineEdit,

)

class TopBar(QWidget):

    def __init__(self):

        super().__init__()

        layout = QHBoxLayout(self)

        self.logo = QLabel("SMART SHOWROOM AI")

        self.search = BaseLineEdit(

            placeholder="Search..."

        )

        self.theme = BaseButton(

            "",

            icon="fa5s.moon"

        )

        layout.addWidget(self.logo)

        layout.addStretch()

        layout.addWidget(self.search)

        layout.addWidget(self.theme)