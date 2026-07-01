"""
product_manager.py
Looks up a Product by voice keyword and triggers the associated
LED effect + display media.
"""

from app.core.database import get_session
from app.core.logger import get_logger
from app.models.product import Product
from app.modules.led.led_controller import trigger_effect
from app.services.display_service import show_media

logger = get_logger(__name__)


def find_product_by_keyword(keyword: str) -> Product | None:
    session = get_session()
    try:
        products = session.query(Product).all()
        keyword = keyword.strip().lower()
        for product in products:
            if keyword in [k.lower() for k in product.keywords_list()]:
                return product
        return None
    finally:
        session.close()


def activate_product(keyword: str, device_ip: str):
    product = find_product_by_keyword(keyword)
    if not product:
        logger.warning(f"No product matched keyword: '{keyword}'")
        return None

    logger.info(f"Activating product '{product.name}' from keyword '{keyword}'")

    if product.led_effect:
        trigger_effect(device_ip, product.led_effect)

    if product.media_path:
        show_media(product.media_path)

    return product
