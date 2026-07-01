"""
esp32_service.py
Handles communication with ESP32 devices over HTTP (discovery, commands, status).
"""

import requests
from app.core.logger import get_logger

logger = get_logger(__name__)

DEFAULT_TIMEOUT = 3  # seconds


def send_command(ip: str, payload: dict, path: str = "/command") -> dict | None:
    """
    Send a JSON command to an ESP32 device.
    Example: send_command("192.168.1.50", {"effect": "sesame", "time": 30})
    """
    url = f"http://{ip}{path}"
    try:
        response = requests.post(url, json=payload, timeout=DEFAULT_TIMEOUT)
        response.raise_for_status()
        logger.info(f"Sent command to {ip}: {payload}")
        return response.json() if response.content else {}
    except requests.RequestException as e:
        logger.error(f"Failed to reach device {ip}: {e}")
        return None


def get_status(ip: str) -> dict | None:
    url = f"http://{ip}/status"
    try:
        response = requests.get(url, timeout=DEFAULT_TIMEOUT)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        logger.error(f"Failed to get status from {ip}: {e}")
        return None
