"""
media_display_widget.py

Displays images and videos for the showroom.

The MediaPlayer pushes images through a callback and
provides a QVideoWidget for video playback.
"""

from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QStackedLayout,
)

from PySide6.QtGui import (
    QPixmap,
)

from PySide6.QtCore import (
    Qt,
)


class MediaDisplayWidget(QWidget):

    def __init__(self, video_widget):

        super().__init__()

        self.image_label = QLabel()

        self.image_label.setAlignment(
            Qt.AlignCenter
        )

        self.image_label.setStyleSheet(
            "background:black;"
        )

        self.image_label.setScaledContents(False)

        self.video_widget = video_widget

        self.stack = QStackedLayout()

        self.stack.addWidget(
            self.image_label
        )

        self.stack.addWidget(
            self.video_widget
        )

        layout = QVBoxLayout()

        layout.setContentsMargins(
            0, 0, 0, 0
        )

        layout.addLayout(
            self.stack
        )

        self.setLayout(layout)

    # ----------------------------

    def show_image(self, pixmap: QPixmap):

        scaled = pixmap.scaled(

            self.image_label.size(),

            Qt.KeepAspectRatio,

            Qt.SmoothTransformation

        )

        self.image_label.setPixmap(
            scaled
        )

        self.stack.setCurrentWidget(
            self.image_label
        )

    # ----------------------------

    def show_video(self):

        self.stack.setCurrentWidget(
            self.video_widget
        )

    # ----------------------------

    def resizeEvent(self, event):

        if self.image_label.pixmap():

            self.show_image(
                self.image_label.pixmap()
            )

        super().resizeEvent(event)