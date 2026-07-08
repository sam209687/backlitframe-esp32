"""
led_controller.py
Python-side LED controller. Sends effect commands to the ESP32 over HTTP.
The actual FastLED rendering lives in esp32_firmware/src/effects/.
"""

from app.core.config_manager import load as load_config
from app.core.logger import get_logger
from app.services.esp32_service import ESP32Service

logger = get_logger(__name__)


def send_command(command: str):
    """
    Backward-compatible wrapper.

    Older modules call send_command().
    Internally we delegate to ESP32Service.
    """

    ESP32Service.send_effect(command)


def start_led():
    cfg = load_config("led")
    logger.info(f"LED module ready (default_effect={cfg.get('default_effect')})")


def trigger_effect(device_ip: str, effect_name: str | None = None, duration: int = 30):
    """
    effect_name examples: SESAME, GROUNDNUT, COCONUT, PC_MODE, COZY_READING, FILLING_OIL
    """
    if effect_name is None:
        effect_name = device_ip
        device_ip = None

    if device_ip:
        ESP32Service.set_ip(device_ip)

    logger.info(f"Triggering LED effect '{effect_name}' on {device_ip} for {duration}s")
    return ESP32Service.send_effect(effect_name)
