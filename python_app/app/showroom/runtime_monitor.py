"""
runtime_monitor.py

Keeps the latest showroom runtime information.

The Dashboard subscribes only to this class.

Responsibilities
----------------
• Current runtime state
• Current product
• Current media
• Last voice command
• Runtime errors

No business logic.
"""

from app.showroom.runtime_events import RuntimeEvents


class RuntimeMonitor:

    def __init__(self, runtime):

        self.runtime = runtime

        self.state = runtime.state

        self.product = None

        self.media = None

        self.voice_text = ""

        self.error = ""

        self.listeners = []

        bus = runtime.events

        bus.subscribe(
            RuntimeEvents.STATE_CHANGED,
            self._state_changed
        )

        bus.subscribe(
            RuntimeEvents.PRODUCT_FOUND,
            self._product_changed
        )

        bus.subscribe(
            RuntimeEvents.MEDIA_CHANGED,
            self._media_changed
        )

        bus.subscribe(
            RuntimeEvents.WAKEWORD_DETECTED,
            self._voice_changed
        )

        bus.subscribe(
            RuntimeEvents.ERROR,
            self._error_changed
        )

    # -------------------------------------------------

    def subscribe(self, callback):

        if callback not in self.listeners:

            self.listeners.append(callback)

    # -------------------------------------------------

    def unsubscribe(self, callback):

        if callback in self.listeners:

            self.listeners.remove(callback)

    # -------------------------------------------------

    def notify(self):

        for callback in list(self.listeners):

            try:

                callback()

            except Exception as e:

                print("Dashboard callback error:", e)

    # -------------------------------------------------

    def _state_changed(self, state):

        self.state = state

        self.notify()

    # -------------------------------------------------

    def _product_changed(self, product):

        self.product = product

        self.notify()

    # -------------------------------------------------

    def _media_changed(self, media):

        self.media = media

        self.notify()

    # -------------------------------------------------

    def _voice_changed(self, text):

        self.voice_text = text

        self.notify()

    # -------------------------------------------------

    def _error_changed(self, message):

        self.error = message

        self.notify()