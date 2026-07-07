"""
base_page.py

Every screen in Smart Showroom inherits this.

Features
--------
✓ Responsive
✓ Scrollable
✓ Title
✓ Subtitle
✓ Toolbar
✓ Content Area
✓ Theme Aware
"""

from PySide6.QtCore import Qt

from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QScrollArea,
    QHBoxLayout,
    QVBoxLayout,
)

from app.ui_comp.theme import ThemeManager


class BasePage(QWidget):

    def __init__(
        self,
        title="",
        subtitle="",
        parent=None
    ):

        super().__init__(parent)

        self.theme = ThemeManager.current()

        self.root = QVBoxLayout(self)

        self.root.setContentsMargins(
            24,
            24,
            24,
            24
        )

        self.root.setSpacing(20)

        # ------------------------------------------
        # Header
        # ------------------------------------------

        self.header = QWidget()

        self.header_layout = QHBoxLayout(
            self.header
        )

        self.header_layout.setContentsMargins(
            0,
            0,
            0,
            0
        )

        self.header_layout.setSpacing(12)

        # left side

        self.header_left = QVBoxLayout()

        self.title = QLabel(title)

        self.subtitle = QLabel(subtitle)

        self.header_left.addWidget(
            self.title
        )

        self.header_left.addWidget(
            self.subtitle
        )

        self.header_layout.addLayout(
            self.header_left
        )

        self.header_layout.addStretch()

        # right side toolbar

        self.toolbar = QHBoxLayout()

        self.toolbar.setSpacing(8)

        self.header_layout.addLayout(
            self.toolbar
        )

        self.root.addWidget(
            self.header
        )

        # ------------------------------------------
        # Scroll Area
        # ------------------------------------------

        self.scroll = QScrollArea()

        self.scroll.setWidgetResizable(True)

        self.scroll.setFrameShape(
            QScrollArea.NoFrame
        )

        self.container = QWidget()

        self.content = QVBoxLayout(
            self.container
        )

        self.content.setSpacing(20)

        self.content.setContentsMargins(
            0,
            0,
            0,
            0
        )

        self.content.addStretch()

        self.scroll.setWidget(
            self.container
        )

        self.root.addWidget(
            self.scroll
        )

        self.refresh()

    # ------------------------------------------

    def refresh(self):

        t = self.theme

        self.setStyleSheet(f"""

        QWidget{{
            background:{t.background};
            color:{t.text};
        }}

        QLabel{{
            background:transparent;
        }}

        """)

        self.title.setStyleSheet(f"""
        font-size:{t.heading_size + 4}px;
        font-weight:700;
        color:{t.text};
        """)

        self.subtitle.setStyleSheet(f"""
        font-size:{t.body_size}px;
        color:{t.text_secondary};
        """)

    # ------------------------------------------

    def add_widget(self, widget):

        self.content.insertWidget(
            self.content.count() - 1,
            widget
        )

    # ------------------------------------------

    def add_layout(self, layout):

        self.content.insertLayout(
            self.content.count() - 1,
            layout
        )

    # ------------------------------------------

    def add_toolbar_widget(
        self,
        widget
    ):

        self.toolbar.addWidget(widget)

    # ------------------------------------------

    def clear(self):

        while self.content.count() > 1:

            item = self.content.takeAt(0)

            if item.widget():

                item.widget().deleteLater()