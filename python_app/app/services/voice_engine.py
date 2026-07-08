"""
voice_engine.py

Simple Voice Engine
Microphone -> Whisper -> VoiceRouter -> ProductMatcher -> Action
"""

from threading import Thread
import time

from app.services.settings_service import SettingsService
from app.services.microphone_service import MicrophoneService
from app.services.whisper_service import WhisperService
from app.services.voice_router import VoiceRouter
from app.services.voice.wakeword_service import WakeWordService
from app.services.product_matcher import ProductMatcher
from app.services.action_service import ActionService


class VoiceEngine:

    def __init__(self):

        self.settings = SettingsService()

        self.microphone = MicrophoneService()

        self.whisper = WhisperService()

        self.wake = WakeWordService()

        self.running = False
        self.thread = None

        # dashboard callbacks

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

    # -------------------------------------------------

    def run(self):

        while self.running:

            try:

                self.listen()

            except Exception as e:

                print("\nVoice Engine Error")
                print(e)

                if self.on_error:
                    self.on_error(str(e))

                time.sleep(1)

    # -------------------------------------------------

    def listen(self):

        if self.on_idle:
            self.on_idle()

        print()
        print("========================================")
        print("Listening...")
        print("========================================")

        audio = self.microphone.record(seconds=3)

        if audio is None:

            print("Microphone Error")
            return

        text = self.whisper.transcribe(audio)

        print()
        print("Whisper")
        print("--------------------------------")
        print(repr(text))
        print("--------------------------------")

        if not text:

            print("Nothing recognized")
            return

        if self.wake.activated(text):

            print("Wake keyword detected")

            if self.on_wakeup:
                self.on_wakeup(text)

            return

        route = VoiceRouter.route(text)

        intent = route["intent"]

        print()
        print("Intent :", intent.value)

        # ----------------------------
        # Greeting
        # ----------------------------

        if route["greeting"]:

            print("Greeting detected")

            if self.on_wakeup:
                self.on_wakeup(text)

            return

        # ----------------------------
        # Help
        # ----------------------------

        if route["help"]:

            print("Help requested")

            return

        # ----------------------------
        # Repeat
        # ----------------------------

        if route["repeat"]:

            print("Repeat requested")

            return

        # ----------------------------
        # Stop
        # ----------------------------

        if route["stop"]:

            print("Stop requested")

            return

        # ----------------------------
        # Product Search
        # ----------------------------

        if route["search_product"]:

            result = ProductMatcher.match(text)

            if not result:

                print("No Product Found")

                if self.on_timeout:
                    self.on_timeout()

                return

            product = result["product"]

            print()
            print("Matched Product")
            print("--------------------------------")
            print(product.name)
            print(product.led_effect)
            print(product.media_path)
            print("--------------------------------")

            if self.on_product:
                self.on_product(product)

            ActionService.execute(product)

            print("LED Animation Started")

            return

        print("Unknown command")
