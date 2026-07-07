"""
media_service.py

Media playback service.

Responsibilities
----------------
• Play product media
• Stop current media
• Resume idle slideshow

The actual player implementation (Qt/VLC/etc.)
can be plugged in through register_player().
"""


class MediaService:

    _player = None

    # -------------------------------------------------

    @classmethod
    def register_player(cls, player):

        """
        Register your MediaPlayer instance.

        Example:
            MediaService.register_player(player)
        """

        cls._player = player

        print("Media Player Registered")

    # -------------------------------------------------

    @classmethod
    def available(cls):

        return cls._player is not None

    # -------------------------------------------------

    @classmethod
    def play(cls, media_path):

        if not cls.available():

            print("Media player not registered")
            return False

        try:

            print(f"Playing : {media_path}")

            cls._player.play_folder(media_path)

            return True

        except Exception as e:

            print("Media Error:", e)

            return False

    # -------------------------------------------------

    @classmethod
    def stop(cls):

        if not cls.available():
            return

        try:

            cls._player.stop()

            print("Media Stopped")

        except Exception as e:

            print("Media Error:", e)

    # -------------------------------------------------

    @classmethod
    def idle(cls):

        """
        Resume showroom idle slideshow.
        """

        if not cls.available():
            return

        try:

            cls._player.play_idle()

            print("Idle Slideshow Started")

        except Exception as e:

            print("Media Error:", e)