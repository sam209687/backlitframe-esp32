"""
voice_worker.py

Main voice engine.

Responsibilities

IDLE
 ↓
Wait for activation keyword
 ↓
Listen for product
 ↓
Match product
 ↓
Return matched product

No UI code belongs here.
No PySide widgets belong here.
"""

import threading
import time

from app.services.settings_service import SettingsService
from app.services.whisper_service import WhisperService
from app.services.welcome_service import WelcomeService
from app.services.product_service import ProductService


class VoiceWorker:

    STATE_IDLE = "idle"
    STATE_ACTIVATED = "activated"
    STATE_PROCESSING = "processing"
    STATE_STOPPED = "stopped"

    def __init__(self):

        self.running = False

        self.thread = None

        self.state = self.STATE_STOPPED

        self.whisper = WhisperService()

        self.last_product = None

        self.last_text = ""

    # -------------------------------------------------

    def start(self):

        if self.running:
            return

        self.running = True

        self.state = self.STATE_IDLE

        self.thread = threading.Thread(
            target=self.run,
            daemon=True
        )

        self.thread.start()

        self.log("Voice Worker Started")

    # -------------------------------------------------

    def stop(self):

        self.running = False

        self.state = self.STATE_STOPPED

        self.log("Voice Worker Stopped")

    # -------------------------------------------------

    def run(self):

        while self.running:

            try:

                self.process_once()

            except Exception as e:

                self.log(f"ERROR : {e}")

                time.sleep(1)

    # -------------------------------------------------

    def process_once(self):

        self.state = self.STATE_IDLE

        self.log("Waiting for activation...")

        text = self.listen_for_activation()

        if not text:
            return

        self.state = self.STATE_ACTIVATED

        self.log(f"Activated : {text}")

        timeout = int(
            SettingsService.get(
                "activation_timeout",
                10
            )
        )

        text = self.listen_for_product(timeout)

        if not text:

            self.log("Activation timeout")

            return

        self.state = self.STATE_PROCESSING

        self.last_text = text

        self.log(f"Heard : {text}")

        product = self.match_product(text)

        if product:

            self.last_product = product

            self.execute_product(product)

        else:

            self.log("No product matched")

    # -------------------------------------------------

    def listen_for_activation(self):

        """
        Returns activation keyword.

        Current implementation simply records one phrase.

        Later:
            Continuous microphone stream
            VAD
            Wake-word optimization
        """

        text = self.whisper.listen()

        if not text:
            return None

        if WelcomeService.is_activation(text):

            return text

        return None

    # -------------------------------------------------

    def listen_for_product(self, timeout):

        """
        Listen after activation.

        timeout comes from Settings table.
        """

        self.log(
            f"Listening {timeout} sec..."
        )

        return self.whisper.listen(seconds=timeout)

    # -------------------------------------------------

    def match_product(self, text):

        return ProductService.find_by_voice(text)

    # -------------------------------------------------

    def execute_product(self, product):

        self.log(
            f"Matched : {product.name}"
        )

        """
        Later

        ESP32Service.send(product.led_effect)

        HDMIPlayer.play(product)

        TTSService.speak(...)
        """

    # -------------------------------------------------

    def reset(self):

        self.last_text = ""

        self.last_product = None

        self.state = self.STATE_IDLE

    # -------------------------------------------------

    def log(self, message):

        print(
            f"[VOICE] {message}"
        )