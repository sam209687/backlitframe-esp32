"""
showroom_runtime.py

Central runtime for Smart Showroom AI.

Every module communicates through this class.
"""

from app.showroom.showroom_state import ShowroomState
from app.showroom.session import ShowroomSession
from app.showroom.event_bus import EventBus

from app.showroom.runtime_manager import RuntimeManager
from app.showroom.runtime_monitor import RuntimeMonitor
from app.showroom.runtime_logger import RuntimeLogger

from app.services.voice_engine import VoiceEngine
from app.services.media_engine.media_engine import MediaEngine
from app.services.esp32_service import ESP32Service
from app.services.product_service import ProductService


class ShowroomRuntime:

    def __init__(self):

        # -------------------------------------------------
        # Runtime State
        # -------------------------------------------------

        self.state = ShowroomState.STARTING

        # -------------------------------------------------
        # Current Session
        # -------------------------------------------------

        self.session = ShowroomSession()

        # -------------------------------------------------
        # Event Bus
        # -------------------------------------------------

        self.events = EventBus()

        # -------------------------------------------------
        # Services
        # -------------------------------------------------

        self.voice_engine = VoiceEngine()

        self.media_engine = MediaEngine()

        self.esp32 = ESP32Service()

        self.products = ProductService()

        # -------------------------------------------------
        # Runtime Monitor
        # -------------------------------------------------

        self.monitor = RuntimeMonitor(self)

        # -------------------------------------------------
        # Runtime Logger
        # -------------------------------------------------

        self.logger = RuntimeLogger(self)

        # -------------------------------------------------
        # Runtime Manager
        # -------------------------------------------------

        self.manager = RuntimeManager(self)

    # -------------------------------------------------

    def start(self):

        self.manager.start()

    # -------------------------------------------------

    def stop(self):

        self.manager.stop()

    # -------------------------------------------------

    def pause(self):

        self.manager.pause()

    # -------------------------------------------------

    def resume(self):

        self.manager.resume()

    # -------------------------------------------------

    def reset(self):

        self.manager.reset()