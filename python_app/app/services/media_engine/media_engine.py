"""
media_engine.py

High-level media controller.
"""

from app.services.media_engine.media_service import MediaService
from app.services.media_engine.media_player import MediaPlayer
from app.services.media_engine.slideshow_service import SlideShowService


class MediaEngine:

    def __init__(self):

        self.player = MediaPlayer()

        self.slideshow = SlideShowService(
            self.player
        )

        self.current_product = None

        self.on_product_changed = None
        self.on_media_changed = None

        self.slideshow.on_media_changed = (
            self.media_changed
        )

    # -------------------------------------------------

    def show_product(self, product):

        print("\n========== MEDIA ENGINE ==========")

        if not product:
            print("Product is None")
            return False

        print("Product:", product.name)

        media = MediaService.validate_media(product.id)

        print("Media count:", len(media))

        if not media:

            print("No valid media found.")

            return False

        for item in media:

            print(
                "Media:",
                item.media_name,
                item.media_type,
                item.file_path
            )

        self.current_product = product

        print("Starting slideshow...")

        self.slideshow.start(media)

        if self.on_product_changed:
            self.on_product_changed(product)

        print("=================================\n")

        return True

    # -------------------------------------------------

    def show_default(self, product):

        media = MediaService.get_default_media(
            product.id
        )

        if media:

            self.player.play(media)

            return True

        return False

    # -------------------------------------------------

    def stop(self):

        self.slideshow.stop()

    # -------------------------------------------------

    def pause(self):

        self.slideshow.pause()

    # -------------------------------------------------

    def resume(self):

        self.slideshow.resume()

    # -------------------------------------------------

    def clear(self):

        self.stop()

    # -------------------------------------------------

    def media_changed(self, media):

        if self.on_media_changed:
            self.on_media_changed(media)

    # -------------------------------------------------

    def current_media(self):

        return self.player.current_media()

    # -------------------------------------------------

    def current_product_info(self):

        return self.current_product

    # -------------------------------------------------

    def video_widget(self):

        return self.player.widget()

    # -------------------------------------------------

    def set_image_callback(self, callback):

        self.player.set_image_callback(callback)

    # -------------------------------------------------

    def set_video_callback(self, callback):

        self.player.set_video_callback(callback)
