"""
runtime_logger.py

Central runtime logger.

Every important showroom event is stored here.

Dashboard, diagnostics and analytics
will use this logger.
"""

from datetime import datetime

from app.showroom.runtime_events import RuntimeEvents


class RuntimeLogger:

    def __init__(self, runtime):

        self.runtime = runtime

        self.logs = []

        bus = runtime.events

        events = [

            RuntimeEvents.STATE_CHANGED,

            RuntimeEvents.WAKEWORD_DETECTED,

            RuntimeEvents.VOICE_TEXT,

            RuntimeEvents.PRODUCT_FOUND,

            RuntimeEvents.PRODUCT_NOT_FOUND,

            RuntimeEvents.MEDIA_STARTED,

            RuntimeEvents.MEDIA_CHANGED,

            RuntimeEvents.MEDIA_FINISHED,

            RuntimeEvents.LED_EFFECT_CHANGED,

            RuntimeEvents.ESP32_CONNECTED,

            RuntimeEvents.ESP32_DISCONNECTED,

            RuntimeEvents.ERROR,

            RuntimeEvents.WARNING,

        ]

        for event in events:

            bus.subscribe(

                event,

                lambda data, e=event: self.add(e, data)

            )

    # -------------------------------------------------

    def add(self, event, data=None):

        now = datetime.now().strftime("%H:%M:%S")

        entry = {

            "time": now,

            "event": event,

            "data": data,

        }

        self.logs.append(entry)

        if len(self.logs) > 500:

            self.logs.pop(0)

        print(f"[{now}] {event} -> {data}")

    # -------------------------------------------------

    def latest(self, count=50):

        return self.logs[-count:]

    # -------------------------------------------------

    def clear(self):

        self.logs.clear()