"""
voice_engine.py

Central voice engine for Smart Showroom.

Responsibilities
----------------
- Wait for welcome keyword
- Listen for product request
- Match product
- Execute product action
- Notify dashboard via callbacks

This class DOES NOT know about:
    - PySide UI
    - ESP32 implementation
    - Media Player implementation

Everything is event driven.
"""

from threading import Thread
import time

from app.services.settings_service import SettingsService
from app.services.whisper_service import WhisperService
from app.services.microphone_service import MicrophoneService
from app.services.product_service import ProductService
from app.services.welcome_service import WelcomeService
from app.services.action_service import ActionService


class VoiceEngine:

    def __init__(self):

        self.settings = SettingsService()

        self.whisper = WhisperService()

        self.microphone = MicrophoneService()

        self.products = ProductService()

        self.welcome = WelcomeService()

        self.running = False

        self.thread = None

        # Dashboard callbacks
        self.on_idle = None
        self.on_listening = None
        self.on_wakeup = None
        self.on_timeout = None
        self.on_product = None
        self.on_error = None

    # -------------------------------------------------

    def start(self):

        if self.running:
            return

        self.running = True

        self.thread = Thread(
            target=self.run,
            daemon=True
        )

        self.thread.start()

        print("Voice Engine Started")

    # -------------------------------------------------

    def stop(self):

        self.running = False

        print("Voice Engine Stopped")

    # -------------------------------------------------

    def run(self):

        while self.running:

            try:

                self.wait_for_wakeup()

            except Exception as e:

                print("Voice Engine Error:", e)

                if self.on_error:
                    self.on_error(str(e))

                time.sleep(1)

    # -------------------------------------------------

    def wait_for_wakeup(self):

        if self.on_idle:
            self.on_idle()

        print("\nWaiting for welcome keyword...")

        audio = self.microphone.record()

        text = self.whisper.transcribe(audio)

        print("Heard:", text)

        if not text:
            return

        matched = self.welcome.match(text)

        if not matched:
            return

        print("Wake word detected")

        if self.on_wakeup:
            self.on_wakeup(text)

        self.listen_for_product()

    # -------------------------------------------------

    def listen_for_product(self):

        timeout = int(
            self.settings.get(
                "voice_listen_timeout",
                default="10"
            )
        )

        if self.on_listening:
            self.on_listening(timeout)

        print(f"Listening for product ({timeout} sec)...")

        audio = self.microphone.record(
            seconds=timeout
        )

        text = self.whisper.transcribe(audio)

        print("Customer:", text)

        if not text:

            if self.on_timeout:
                self.on_timeout()

            return

        product = self.products.find_by_voice(text)

        if not product:

            print("No product matched")

            if self.on_timeout:
                self.on_timeout()

            return

        print("Matched:", product)

        # Notify Dashboard
        if self.on_product:
            self.on_product(product)

        # Execute configured action
        ActionService.execute(product)

        print("Product action completed")