"""
slideshow_service.py

Controls slideshow timing.

Responsibilities
----------------
• Start slideshow
• Stop slideshow
• Pause slideshow
• Resume slideshow
• Next media
• Previous media
• Loop forever

No database.
No UI.
No voice.
"""

from threading import Thread, Event
import time


class SlideShowService:

    def __init__(self, media_player):

        self.player = media_player

        self.media_list = []

        self.current_index = 0

        self.running = False

        self.paused = False

        self.thread = None

        self.stop_event = Event()

        # callbacks
        self.on_media_changed = None
        self.on_finished = None

    # --------------------------------------------------

    def start(self, media_list):

        if not media_list:
            return

        self.stop()

        self.media_list = media_list

        self.current_index = 0

        self.running = True

        self.paused = False

        self.stop_event.clear()

        self.thread = Thread(
            target=self.run,
            daemon=True
        )

        self.thread.start()

    # --------------------------------------------------

    def stop(self):

        self.running = False

        self.stop_event.set()

        self.player.stop()

    # --------------------------------------------------

    def pause(self):

        self.paused = True

        self.player.pause()

    # --------------------------------------------------

    def resume(self):

        self.paused = False

        self.player.resume()

    # --------------------------------------------------

    def next(self):

        if not self.media_list:
            return

        self.current_index += 1

        if self.current_index >= len(self.media_list):
            self.current_index = 0

    # --------------------------------------------------

    def previous(self):

        if not self.media_list:
            return

        self.current_index -= 1

        if self.current_index < 0:
            self.current_index = len(self.media_list) - 1

    # --------------------------------------------------

    def current_media(self):

        if not self.media_list:
            return None

        return self.media_list[self.current_index]

    # --------------------------------------------------

    def run(self):

        while self.running:

            media = self.current_media()

            if media is None:
                break

            self.player.play(media)

            if self.on_media_changed:
                self.on_media_changed(media)

            duration = max(
                1,
                int(media.duration)
            )

            start = time.time()

            while (
                time.time() - start < duration
                and self.running
            ):

                if self.paused:

                    time.sleep(0.2)

                    continue

                if self.stop_event.is_set():
                    return

                time.sleep(0.2)

            self.next()

        if self.on_finished:
            self.on_finished()