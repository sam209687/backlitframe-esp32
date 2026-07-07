"""
base_card.py

Reusable Card Component.

Used everywhere in Smart Showroom.

Features
--------
✓ Rounded corners
✓ Padding
✓ Drop shadow
✓ Optional title
✓ Optional subtitle
✓ Content Layout
"""

from PySide6.QtCore import Qt

from PySide6.QtWidgets import (
    QLabel,
    QVBoxLayout,
)

from app.ui_comp.base.base_widget import BaseWidget


class BaseCard(BaseWidget):

    def __init__(
        self,
        title="",
        subtitle="",
        parent=None,
    ):

        super().__init__(parent)

        self.apply_shadow()

        self.layout = QVBoxLayout(self)

        self.layout.setContentsMargins(
            self.theme.space_lg,
            self.theme.space_lg,
            self.theme.space_lg,
            self.theme.space_lg,
        )

        self.layout.setSpacing(
            self.theme.space_md
        )

        self.title_label = QLabel(title)

        self.title_label.setStyleSheet(
            f"""
            font-size:{self.theme.heading_size}px;
            font-weight:700;
            color:{self.theme.text};
            background:transparent;
            """
        )

        self.subtitle_label = QLabel(subtitle)

        self.subtitle_label.setWordWrap(True)

        self.subtitle_label.setStyleSheet(
            f"""
            color:{self.theme.text_secondary};
            background:transparent;
            font-size:{self.theme.small_size}px;
            """
        )

        if title:
            self.layout.addWidget(self.title_label)

        if subtitle:
            self.layout.addWidget(self.subtitle_label)

        self.layout.addStretch()

        self.setStyleSheet(f"""
        BaseCard{{
            background:{self.theme.card};
            border:1px solid {self.theme.border};
            border-radius:{self.theme.radius_lg}px;
        }}
        """)

        self.fade_in()

    # --------------------------------------------------

    def set_title(self, text):

        self.title_label.setText(text)

        if self.title_label.parent() is None:
            self.layout.insertWidget(0, self.title_label)

    # --------------------------------------------------

    def set_subtitle(self, text):

        self.subtitle_label.setText(text)

        if self.subtitle_label.parent() is None:
            self.layout.insertWidget(1, self.subtitle_label)

    # --------------------------------------------------

    def add_widget(self, widget):

        self.layout.insertWidget(
            self.layout.count() - 1,
            widget,
        )

    # --------------------------------------------------

    def add_layout(self, layout):

        self.layout.insertLayout(
            self.layout.count() - 1,
            layout,
        )

    # --------------------------------------------------

    def clear(self):

        while self.layout.count() > 1:

            item = self.layout.takeAt(1)

            if item.widget():
                item.widget().deleteLater()

    # --------------------------------------------------

    def refresh_theme(self):

        super().refresh_theme()

        self.setStyleSheet(f"""
        BaseCard{{
            background:{self.theme.card};
            border:1px solid {self.theme.border};
            border-radius:{self.theme.radius_lg}px;
        }}
        """)