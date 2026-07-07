"""
Application Status Bar
"""

from PySide6.QtWidgets import (

    QWidget,

    QLabel,

    QHBoxLayout

)


class StatusBar(QWidget):

    def __init__(self):

        super().__init__()

        layout = QHBoxLayout(self)

        self.left = QLabel("Ready")

        self.right = QLabel("ESP32 : Offline")

        layout.addWidget(self.left)

        layout.addStretch()

        layout.addWidget(self.right)

    def set_status(self,text):

        self.left.setText(text)

    def set_device(self,text):

        self.right.setText(text)