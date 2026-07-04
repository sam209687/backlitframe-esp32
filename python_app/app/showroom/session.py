"""
session.py

Stores the current showroom visitor session.
"""


from datetime import datetime


class ShowroomSession:

    def __init__(self):

        self.reset()

    # -------------------------------------

    def reset(self):

        self.session_id = None

        self.start_time = datetime.now()

        self.end_time = None

        self.voice_text = ""

        self.product = None

        self.media = None

        self.led_effect = None

    # -------------------------------------

    def end(self):

        self.end_time = datetime.now()

    # -------------------------------------

    @property
    def duration(self):

        end = self.end_time or datetime.now()

        return (end - self.start_time).total_seconds()