"""
media_player.py

Low level media playback.

Responsibilities
----------------
• Display image
• Play video
• Stop playback
• Pause
• Resume

No database.
No voice.
No slideshow.
"""

from pathlib import Path

from PySide6.QtCore import QUrl
from PySide6.QtGui import QPixmap
from PySide6.QtMultimedia import (
    QMediaPlayer,
    QAudioOutput
)
from PySide6.QtMultimediaWidgets import QVideoWidget


class MediaPlayer:

    def __init__(self):

        self.video_widget = QVideoWidget()

        self.audio = QAudioOutput()

        self.player = QMediaPlayer()

        self.player.setAudioOutput(self.audio)

        self.player.setVideoOutput(self.video_widget)

        self.image_callback = None
        self.video_callback = None

        self.current = None

    # -------------------------------------------------

    def set_image_callback(self, callback):

        self.image_callback = callback

    # -------------------------------------------------

    def set_video_callback(self, callback):

        self.video_callback = callback

    # -------------------------------------------------

    def play(self, media):

        self.current = media

        path = Path(media.file_path)

        if not path.exists():

            print("Missing media:", path)

            return False

        media_type = media.media_type.lower()

        if media_type == "image":

            self.show_image(path)

            return True

        if media_type == "video":

            self.play_video(path)

            return True

        print("Unsupported media:", media_type)

        return False

    # -------------------------------------------------

    def show_image(self, path):

        self.player.stop()

        pixmap = QPixmap(str(path))

        if self.image_callback:
            self.image_callback(pixmap)

    # -------------------------------------------------

    def play_video(self, path):

        self.player.stop()

        self.player.setSource(
            QUrl.fromLocalFile(str(path))
        )

        if self.video_callback:
            self.video_callback()

        self.player.play()

    # -------------------------------------------------

    def stop(self):

        self.player.stop()

    # -------------------------------------------------

    def pause(self):

        self.player.pause()

    # -------------------------------------------------

    def resume(self):

        self.player.play()

    # -------------------------------------------------

    def is_playing(self):

        return (
            self.player.playbackState()
            == QMediaPlayer.PlayingState
        )

    # -------------------------------------------------

    def current_media(self):

        return self.current

    # -------------------------------------------------

    def widget(self):

        return self.video_widget