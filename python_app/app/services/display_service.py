"""
display_service.py
Handles showing images/videos on HDMI display for a given product.
"""

import os
from app.core.config_manager import load as load_config
from app.core.logger import get_logger

logger = get_logger(__name__)


def start_display():
    cfg = load_config("display")
    logger.info(f"Display service started (resolution={cfg.get('resolution')})")


def show_media(product_media_path: str):
    """product_media_path e.g. 'media/sesame'"""
    images_dir = os.path.join(product_media_path, "images")
    videos_dir = os.path.join(product_media_path, "videos")
    logger.info(f"Showing media from {images_dir} / {videos_dir}")
    # TODO: integrate with OpenCV / Qt widget to actually render media
