"""
runtime_controller.py

Public API used by the dashboard.

The dashboard should never communicate directly
with VoiceEngine or MediaEngine.
"""


class RuntimeController:

    def __init__(self, runtime):

        self.runtime = runtime

    # ---------------------------------

    def start(self):

        self.runtime.start()

    # ---------------------------------

    def stop(self):

        self.runtime.stop()

    # ---------------------------------

    def pause(self):

        self.runtime.pause()

    # ---------------------------------

    def resume(self):

        self.runtime.resume()

    # ---------------------------------

    def reset(self):

        self.runtime.reset()

    # ---------------------------------

    def state(self):

        return self.runtime.state

    # ---------------------------------

    def session(self):

        return self.runtime.session