"""
Main Window

Every page loads here.
"""

from PySide6.QtWidgets import (

    QMainWindow,

    QWidget,

    QVBoxLayout,

    QHBoxLayout,

    QStackedWidget,

)

from app.ui_comp.layout.sidebar import Sidebar

from app.ui_comp.layout.topbar import TopBar

from app.ui_comp.layout.statusbar import StatusBar


class MainWindow(QMainWindow):

    def __init__(self):

        super().__init__()

        self.setWindowTitle(

            "Smart Showroom AI"

        )

        self.resize(

            1600,

            900

        )

        central = QWidget()

        self.setCentralWidget(central)

        root = QVBoxLayout(central)

        root.setContentsMargins(0,0,0,0)

        root.setSpacing(0)

        self.topbar = TopBar()

        root.addWidget(

            self.topbar

        )

        body = QHBoxLayout()

        root.addLayout(body)

        self.sidebar = Sidebar()

        body.addWidget(

            self.sidebar

        )

        self.stack = QStackedWidget()

        body.addWidget(

            self.stack,

            1

        )

        self.status = StatusBar()

        root.addWidget(

            self.status

        )

        self.sidebar.page_changed.connect(

            self.change_page

        )

    def add_page(

        self,

        widget

    ):

        self.stack.addWidget(widget)

    def change_page(

        self,

        name

    ):

        print(

            "Switch Page :",

            name

        )