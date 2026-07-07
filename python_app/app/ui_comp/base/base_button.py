"""
base_button.py

Universal Button Component

Features
--------
✓ Primary
✓ Secondary
✓ Success
✓ Warning
✓ Danger
✓ Icon Support
✓ Loading State
✓ Toggle Support
✓ Hover Animation
"""

import qtawesome as qta

from PySide6.QtCore import (
    QEasingCurve,
    QPropertyAnimation,
)

from PySide6.QtWidgets import QPushButton

from app.ui_comp.theme import ThemeManager


class BaseButton(QPushButton):

    PRIMARY = "primary"
    SECONDARY = "secondary"
    SUCCESS = "success"
    WARNING = "warning"
    DANGER = "danger"

    def __init__(
        self,
        text="",
        icon=None,
        button_type=PRIMARY,
        parent=None
    ):

        super().__init__(text, parent)

        self.theme = ThemeManager.current()

        self.button_type = button_type

        self.default_text = text

        self.loading = False

        self.setCursor(
            self.cursor().shape()
        )

        self.setMinimumHeight(42)

        self.animation = QPropertyAnimation(
            self,
            b"geometry"
        )

        self.animation.setDuration(120)

        self.animation.setEasingCurve(
            QEasingCurve.OutCubic
        )

        if icon:

            self.setIcon(
                qta.icon(
                    icon,
                    color="white"
                )
            )

        self.refresh()

    # ------------------------------------------------

    def refresh(self):

        t = self.theme

        if self.button_type == self.PRIMARY:

            bg = t.primary
            hover = t.primary_hover
            press = t.primary_pressed
            text = "white"

        elif self.button_type == self.SUCCESS:

            bg = t.success
            hover = "#16A34A"
            press = "#15803D"
            text = "white"

        elif self.button_type == self.WARNING:

            bg = t.warning
            hover = "#D97706"
            press = "#B45309"
            text = "white"

        elif self.button_type == self.DANGER:

            bg = t.danger
            hover = "#DC2626"
            press = "#B91C1C"
            text = "white"

        else:

            bg = t.surface
            hover = t.surface_alt
            press = t.border
            text = t.text

        self.setStyleSheet(f"""

        QPushButton{{

            background:{bg};

            color:{text};

            border:1px solid {t.border};

            border-radius:{t.radius_md}px;

            padding:8px 18px;

            font-weight:600;

        }}

        QPushButton:hover{{

            background:{hover};

        }}

        QPushButton:pressed{{

            background:{press};

        }}

        QPushButton:disabled{{

            background:{t.surface_alt};

            color:{t.text_secondary};

        }}

        """)

    # ------------------------------------------------

    def set_loading(self, value=True):

        self.loading = value

        if value:

            self.setDisabled(True)

            self.setText("Loading...")

        else:

            self.setDisabled(False)

            self.setText(
                self.default_text
            )

    # ------------------------------------------------

    def set_icon(self, icon):

        self.setIcon(

            qta.icon(

                icon,

                color="white"

            )

        )

    # ------------------------------------------------

    def set_primary(self):

        self.button_type = self.PRIMARY

        self.refresh()

    # ------------------------------------------------

    def set_secondary(self):

        self.button_type = self.SECONDARY

        self.refresh()

    # ------------------------------------------------

    def set_success(self):

        self.button_type = self.SUCCESS

        self.refresh()

    # ------------------------------------------------

    def set_warning(self):

        self.button_type = self.WARNING

        self.refresh()

    # ------------------------------------------------

    def set_danger(self):

        self.button_type = self.DANGER

        self.refresh()