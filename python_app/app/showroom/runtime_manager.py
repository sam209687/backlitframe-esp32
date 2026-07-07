"""
runtime_manager.py

Contains all showroom runtime logic.

Responsibilities
----------------
• Runtime state transitions
• Voice event handling
• Product activation
• Media playback
• LED control
• Runtime event publishing

No UI code.
"""

from app.showroom.showroom_state import ShowroomState
from app.showroom.runtime_events import RuntimeEvents

from app.modules.led.led_controller import trigger_effect


class RuntimeManager:

    def __init__(self, runtime):

        self.runtime = runtime

        self.voice = runtime.voice_engine

        self.media = runtime.media_engine

        self.products = runtime.products

        self.events = runtime.events

        self.session = runtime.session

        # Media callbacks
        self.media.on_media_changed = self.on_media_changed

        self.register_callbacks()

    # -------------------------------------------------

    def register_callbacks(self):

        self.voice.on_idle = self.on_idle
        self.voice.on_wakeup = self.on_wakeup
        self.voice.on_listening = self.on_listening
        self.voice.on_product = self.on_product
        self.voice.on_timeout = self.on_timeout
        self.voice.on_error = self.on_error

    # -------------------------------------------------

    def start(self):

        self.change_state(
            ShowroomState.IDLE
        )

        self.voice.start()

    # -------------------------------------------------

    def stop(self):

        self.voice.stop()

        self.media.stop()

        self.change_state(
            ShowroomState.STOPPED
        )

    # -------------------------------------------------

    def pause(self):

        self.media.pause()

        self.change_state(
            ShowroomState.PAUSED
        )

    # -------------------------------------------------

    def resume(self):

        self.media.resume()

        self.change_state(
            ShowroomState.PLAYING_MEDIA
        )

    # -------------------------------------------------

    def reset(self):

        self.media.stop()

        self.session.reset()

        self.change_state(
            ShowroomState.IDLE
        )

    # -------------------------------------------------

    def on_idle(self):

        self.change_state(
            ShowroomState.WAITING_WAKEWORD
        )

    # -------------------------------------------------

    def on_wakeup(self, text):

        self.session.reset()

        self.session.voice_text = text

        self.events.publish(
            RuntimeEvents.WAKEWORD_DETECTED,
            text
        )

    # -------------------------------------------------

    def on_listening(self, timeout):

        self.change_state(
            ShowroomState.LISTENING
        )

    # -------------------------------------------------

    def on_product(self, product):

        self.change_state(
            ShowroomState.PRODUCT_FOUND
        )

        self.session.product = product

        self.events.publish(
            RuntimeEvents.PRODUCT_FOUND,
            product
        )

        # Trigger LED effect
        if getattr(product, "led_effect", None):

            trigger_effect(product.led_effect)

        # Start media slideshow
        self.media.show_product(product)

        self.change_state(
            ShowroomState.PLAYING_MEDIA
        )

    # -------------------------------------------------

    def on_timeout(self):

        if hasattr(self.session, "end"):

            self.session.end()

        else:

            self.session.reset()

        self.change_state(
            ShowroomState.IDLE
        )

    # -------------------------------------------------

    def on_error(self, message):

        self.change_state(
            ShowroomState.ERROR
        )

        self.events.publish(
            RuntimeEvents.ERROR,
            message
        )

    # -------------------------------------------------

    def change_state(self, state):

        self.runtime.state = state

        self.events.publish(
            RuntimeEvents.STATE_CHANGED,
            state
        )

        print(f"Runtime State -> {state}")

    # -------------------------------------------------

    def on_media_changed(self, media):

        self.events.publish(
            RuntimeEvents.MEDIA_CHANGED,
            media
        )