"""
app_controller.py
Top-level orchestrator. Boots core services based on which features
are enabled for the active customer/license.
"""

from app.core.logger import get_logger
from app.core.config_manager import load as load_config
from app.core.feature_manager import feature_enabled

logger = get_logger(__name__)


class AppController:
    def __init__(self, customer_id: int):
        self.customer_id = customer_id
        self.app_config = load_config("app")
        logger.info(f"AppController starting for customer_id={customer_id}")

    def start(self):
        logger.info("Booting Smart Showroom services...")

        if feature_enabled(self.customer_id, "voice"):
            self._start_voice()

        if feature_enabled(self.customer_id, "display"):
            self._start_display()

        if feature_enabled(self.customer_id, "led"):
            self._start_led()

        if feature_enabled(self.customer_id, "signboard"):
            self._start_signboard()

        logger.info("All enabled services started.")

    def _start_voice(self):
        logger.info("Starting voice service...")
        # from app.services.voice_service import start_voice
        # start_voice()

    def _start_display(self):
        logger.info("Starting display service...")
        # from app.services.display_service import start_display
        # start_display()

    def _start_led(self):
        logger.info("Starting LED service...")
        # from app.modules.led.led_controller import start_led
        # start_led()

    def _start_signboard(self):
        logger.info("Starting signboard scheduler...")
        # from app.services.scheduler_service import start_scheduler
        # start_scheduler()
