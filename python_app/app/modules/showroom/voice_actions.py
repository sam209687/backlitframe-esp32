"""
voice_actions.py

Handles live voice transcript from the Voice Page.

Flow:
    transcript
    -> wakeup check
    -> product keyword match
    -> ESP32 LED effect
    -> optional runtime media/dashboard update
"""

import time

from app.core.logger import get_logger
from app.services.product_service import ProductService
from app.services.esp32_service import ESP32Service

logger = get_logger(__name__)


WAKEUP_KEYWORDS = [
    "hello",
    "hi",
    "hey",
    "vanga sir",
    "வாங்க சார்",
    "how can i help you",
    "enna venum sir",
    "என்ன வேணும் சார்",
]

WAKEUP_WINDOW_SECONDS = 20

_active_until = 0


def normalize_text(text):
    if not text:
        return ""

    return (
        text.lower()
        .strip()
        .replace(".", "")
        .replace(",", "")
        .replace("?", "")
        .replace("!", "")
    )


def is_wakeup(text):
    normalized = normalize_text(text)

    for keyword in WAKEUP_KEYWORDS:
        if keyword.lower() in normalized:
            return True

    return False


def is_active():
    return time.time() <= _active_until


def activate_wakeup():
    global _active_until

    _active_until = time.time() + WAKEUP_WINDOW_SECONDS


def handle_transcript(text: str, device_ip: str, runtime=None):
    """
    Called by VoicePage whenever Whisper returns text.

    Returns:
        dict with action status for UI logging.
    """

    original_text = text or ""
    text = normalize_text(original_text)

    logger.info(f"Voice transcript received: '{text}'")

    if not text:
        return {
            "status": "empty",
            "message": "No speech detected.",
        }

    # -------------------------------------------------
    # Wakeup
    # -------------------------------------------------

    if is_wakeup(text):
        activate_wakeup()

        logger.info("Wakeup keyword detected")

        if runtime and hasattr(runtime, "monitor"):
            runtime.monitor.voice_text = original_text

        return {
            "status": "wakeup",
            "message": "Wakeup detected. Listening for product command.",
        }

    # -------------------------------------------------
    # Require wakeup before product command
    # -------------------------------------------------

    if not is_active():
        return {
            "status": "waiting_wakeup",
            "message": "Waiting for wakeup command.",
        }

    # -------------------------------------------------
    # Product Match
    # -------------------------------------------------

    product = ProductService.find_by_voice(text)

    if not product:
        logger.info("No product matched")

        return {
            "status": "no_product",
            "message": f"No product matched for: {original_text}",
        }

    logger.info(
        f"Matched product: {product.name}, "
        f"effect={product.led_effect}, "
        f"media={product.media_path}"
    )

    # -------------------------------------------------
    # Dashboard monitor update
    # -------------------------------------------------

    if runtime and hasattr(runtime, "monitor"):
        runtime.monitor.voice_text = original_text
        runtime.monitor.product = product

    # -------------------------------------------------
    # LED Action
    # -------------------------------------------------

    led_ok = False

    if product.led_effect:
        led_ok = ESP32Service.send_effect(
            product.led_effect,
            device_ip,
        )

    # -------------------------------------------------
    # Media Action
    # -------------------------------------------------

    media_ok = False

    if runtime and hasattr(runtime, "media_engine") and product.media_path:
        try:
            media_engine = runtime.media_engine

            if hasattr(media_engine, "play_folder"):
                media_engine.play_folder(product.media_path)
                media_ok = True

            elif hasattr(media_engine, "play"):
                media_engine.play(product.media_path)
                media_ok = True

        except Exception as error:
            logger.warning(f"Media play failed: {error}")

    return {
        "status": "product_matched",
        "message": f"Matched {product.name}",
        "product": product.name,
        "effect": product.led_effect,
        "media": product.media_path,
        "led_ok": led_ok,
        "media_ok": media_ok,
    }