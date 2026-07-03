"""
esp32_service.py

Send commands to ESP32.
"""

import socket

from app.core.database import get_session
from app.models.device import Device


class ESP32Service:

    PORT = 4210

    @classmethod
    def send_effect(cls, effect):

        session = get_session()

        try:

            device = (
                session.query(Device)
                .filter_by(status="connected")
                .first()
            )

            if not device:
                print("No ESP32 connected")
                return

            sock = socket.socket(
                socket.AF_INET,
                socket.SOCK_DGRAM
            )

            message = effect.encode()

            sock.sendto(
                message,
                (device.ip, cls.PORT)
            )

            print("Sent:", effect)

        except Exception as e:

            print(e)

        finally:

            session.close()