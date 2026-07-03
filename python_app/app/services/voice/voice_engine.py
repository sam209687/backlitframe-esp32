"""
voice_engine.py

Main voice pipeline controller.
"""

from app.services.voice.whisper_service import WhisperService
from app.services.voice.wakeword_service import WakeWordService
from app.services.voice.product_matcher import ProductMatcher


class VoiceEngine:

    IDLE = 0
    LISTEN_PRODUCT = 1

    def __init__(self):

        self.whisper = WhisperService()

        self.wake = WakeWordService()

        self.matcher = ProductMatcher()

        self.state = self.IDLE

    def process_audio(self, audio_file):

        text = self.whisper.transcribe(audio_file)

        print(f"Detected: {text}")

        if not text:
            return None

        if self.state == self.IDLE:

            if self.wake.activated(text):

                print("Wake keyword detected")

                self.state = self.LISTEN_PRODUCT

            return None

        if self.state == self.LISTEN_PRODUCT:

            product = self.matcher.match(text)

            self.state = self.IDLE

            if product:

                print("Matched:", product.name)

                return product

        return None