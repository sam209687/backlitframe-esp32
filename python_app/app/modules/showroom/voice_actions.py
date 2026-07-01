"""
voice_actions.py
Bridges recognized speech text to showroom actions.

Flow:
    voice -> product_manager -> LED -> Display
"""

from app.core.logger import get_logger
from app.modules.showroom.product_manager import activate_product

logger = get_logger(__name__)


def handle_transcript(text: str, device_ip: str):
    """
    Called by voice_service whenever a phrase is transcribed.
    Example: text = "show sesame"
    """
    text = text.lower().strip()
    logger.info(f"Voice transcript received: '{text}'")

    # naive keyword extraction - last word of the phrase
    # replace with a smarter matcher/NLU later if needed
    words = text.split()
    if not words:
        return

    keyword = words[-1]
    activate_product(keyword, device_ip)
