"""
base_switch.py

Animated Toggle Switch

Features
--------
✓ Smooth animation
✓ Theme aware
✓ Dark / Light
✓ Compact
✓ No external libraries
"""

from PySide6.QtCore import (
    Qt,
    Property,
    QPropertyAnimation,
    QEasingCurve,
    QRectF,
)

from PySide6.QtGui import (
    QColor,
    QPainter,
)

from PySide6.QtWidgets import QWidget

from app.ui_comp.theme import ThemeManager


class BaseSwitch(QWidget):

    def __init__(self, checked=False, parent=None):

        super().__init__(parent)

        self.theme = ThemeManager.current()

        self.setFixedSize(56, 30)

        self.checked = checked

        self._offset = 28 if checked else 2

        self.animation = QPropertyAnimation(
            self,
            b"offset"
        )

        self.animation.setDuration(180)

        self.animation.setEasingCurve(
            QEasingCurve.OutCubic
        )

    # -------------------------------------------------

    def mousePressEvent(self, event):

        self.toggle()

        super().mousePressEvent(event)

    # -------------------------------------------------

    def toggle(self):

        self.checked = not self.checked

        self.animation.stop()

        self.animation.setStartValue(self._offset)

        self.animation.setEndValue(
            28 if self.checked else 2
        )

        self.animation.start()

    # -------------------------------------------------

    def isChecked(self):

        return self.checked

    def setChecked(self, value):

        self.checked = value

        self._offset = 28 if value else 2

        self.update()

    # -------------------------------------------------

    def getOffset(self):

        return self._offset

    def setOffset(self, value):

        self._offset = value

        self.update()

    offset = Property(
        float,
        getOffset,
        setOffset
    )

    # -------------------------------------------------

    def paintEvent(self, event):

        t = self.theme

        painter = QPainter(self)

        painter.setRenderHint(
            QPainter.Antialiasing
        )

        if self.checked:

            bg = QColor(t.primary)

        else:

            bg = QColor(t.border)

        painter.setBrush(bg)

        painter.setPen(Qt.NoPen)

        painter.drawRoundedRect(
            QRectF(0, 0, 56, 30),
            15,
            15
        )

        painter.setBrush(QColor("white"))

        painter.drawEllipse(
            int(self._offset),
            2,
            26,
            26
        )