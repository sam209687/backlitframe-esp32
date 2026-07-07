"""
base_widget.py

Base widget for the Smart Showroom UI.

Every reusable component should inherit from this class.

Features
--------
✓ Theme access
✓ Refresh theme
✓ Fade animation
✓ Drop shadow helper
✓ Rounded corners
✓ Consistent sizing
"""

from PySide6.QtCore import (
    QEasingCurve,
    Property,
    QPropertyAnimation,
)

from PySide6.QtGui import QColor

from PySide6.QtWidgets import (
    QWidget,
    QGraphicsDropShadowEffect,
)

from app.ui_comp.theme import ThemeManager


class BaseWidget(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.theme = ThemeManager.current()

        self._opacity = 1.0

        self.fade_animation = QPropertyAnimation(
            self,
            b"opacity"
        )

        self.fade_animation.setDuration(
            self.theme.animation
        )

        self.fade_animation.setEasingCurve(
            QEasingCurve.OutCubic
        )

    # --------------------------------------------------
    # Theme
    # --------------------------------------------------

    def refresh_theme(self):

        self.theme = ThemeManager.current()

        self.update()

    # --------------------------------------------------
    # Shadow
    # --------------------------------------------------

    def apply_shadow(
        self,
        blur=20,
        y=3,
        alpha=80
    ):

        shadow = QGraphicsDropShadowEffect(self)

        shadow.setBlurRadius(blur)

        shadow.setOffset(0, y)

        shadow.setColor(
            QColor(0, 0, 0, alpha)
        )

        self.setGraphicsEffect(shadow)

    # --------------------------------------------------
    # Fade
    # --------------------------------------------------

    def fade_in(self):

        self.fade_animation.stop()

        self.fade_animation.setStartValue(0)

        self.fade_animation.setEndValue(1)

        self.fade_animation.start()

    def fade_out(self):

        self.fade_animation.stop()

        self.fade_animation.setStartValue(1)

        self.fade_animation.setEndValue(0)

        self.fade_animation.start()

    # --------------------------------------------------
    # Opacity Property
    # --------------------------------------------------

    def getOpacity(self):
        return self._opacity

    def setOpacity(self, value):
        self._opacity = value
        self.setWindowOpacity(value)

    opacity = Property(
        float,
        getOpacity,
        setOpacity
    )

    # --------------------------------------------------
    # Helpers
    # --------------------------------------------------

    def set_fixed_height(self, height):

        self.setMinimumHeight(height)
        self.setMaximumHeight(height)

    def set_fixed_width(self, width):

        self.setMinimumWidth(width)
        self.setMaximumWidth(width)

    def set_fixed_size(self, w, h):

        self.setFixedSize(w, h)