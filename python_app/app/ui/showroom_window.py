"""
showroom_window.py

Customer display window.

This window is completely independent of the dashboard.

Responsibilities
----------------
• Show product images
• Show product videos
• Fullscreen presentation
• Can be moved to second monitor
"""

from PySide6.QtWidgets import (
    QMainWindow,
)

from app.services.media_engine.media_engine import MediaEngine
from app.ui.widgets.media_display_widget import MediaDisplayWidget


class ShowroomWindow(QMainWindow):

    def __init__(self, media_engine=None):

        super().__init__()

        self.setWindowTitle(
            "Smart Showroom Display"
        )

        self.resize(
            1280,
            720
        )

        # -------------------------

        self.media_engine = media_engine or MediaEngine()

        self.display = MediaDisplayWidget(
            self.media_engine.video_widget()
        )

        self.media_engine.set_image_callback(
            self.display.show_image
        )

        self.media_engine.set_video_callback(
            self.display.show_video
        )

        self.setCentralWidget(
            self.display
        )

    # -----------------------------------

    def show_product(self, product):

        self.media_engine.show_product(
            product
        )

    # -----------------------------------

    def stop(self):

        self.media_engine.stop()

    # -----------------------------------

    def pause(self):

        self.media_engine.pause()

    # -----------------------------------

    def resume(self):

        self.media_engine.resume()
