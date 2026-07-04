"""
event_bus.py

Simple publish/subscribe event system.

This keeps modules independent.
"""


class EventBus:

    def __init__(self):

        self._listeners = {}

    # ---------------------------------

    def subscribe(self, event, callback):

        self._listeners.setdefault(event, []).append(callback)

    # ---------------------------------

    def unsubscribe(self, event, callback):

        if event in self._listeners:

            if callback in self._listeners[event]:

                self._listeners[event].remove(callback)

    # ---------------------------------

    def publish(self, event, data=None):

        callbacks = self._listeners.get(event, [])

        for callback in callbacks:

            try:

                callback(data)

            except Exception as e:

                print(f"Event Error ({event}): {e}")