"""
esp32_service.py

Service responsible for communicating with ESP32 devices.
"""

import json
import socket

from app.core.database import get_session
from app.models.device import Device


class ESP32Service:

    PORT = 4210

    @classmethod
    def send(cls, ip: str, payload: dict):

        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

            sock.sendto(
                json.dumps(payload).encode(),
                (ip, cls.PORT)
            )

            sock.close()

            return True

        except Exception as e:
            print("ESP32 Error:", e)
            return False

    @classmethod
    def send_effect(cls, effect: str):

        session = get_session()

        try:

            device = (
                session.query(Device)
                .filter_by(status="connected")
                .first()
            )

            if not device:
                print("No ESP32 connected")
                return False

            return cls.send(
                device.ip,
                {
                    "effect": effect
                }
            )

        finally:
            session.close()


def send_command(ip, payload):
    """
    Compatibility wrapper for older modules.
    """

    return ESP32Service.send(ip, payload)