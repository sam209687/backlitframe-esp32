"""
esp32_service.py

Central ESP32 communication service.

Used by:
- DeviceDiscovery
- LED page
- Voice actions
- Runtime action service
"""

import socket

from app.core.database import get_session
from app.models.device import Device


class ESP32Service:

    PORT = 4210
    _ip = None

    @classmethod
    def set_ip(cls, ip):
        """
        Called by device discovery when ESP32 is found.
        Updates memory and database.
        """

        if not ip:
            return False

        cls._ip = ip

        session = get_session()

        try:
            device = (
                session.query(Device)
                .filter(Device.device_name == "SMART_SHOWROOM_FRAME")
                .first()
            )

            if not device:
                device = Device(
                    device_name="SMART_SHOWROOM_FRAME",
                    ip=ip,
                    status="connected",
                )
                session.add(device)
            else:
                device.ip = ip
                device.status = "connected"

            session.commit()

            print(f"ESP32 IP Updated: {ip}")

            return True

        except Exception as error:
            session.rollback()
            print("ESP32 DB update error:", error)
            return False

        finally:
            session.close()

    @classmethod
    def get_ip(cls):
        if cls._ip:
            return cls._ip

        return cls.connected_ip()

    @classmethod
    def send_effect(cls, effect, ip=None):
        """
        Send LED effect name to ESP32 using UDP.
        """

        if not effect:
            print("No LED effect supplied")
            return False

        if not ip:
            ip = cls.get_ip()

        if not ip:
            print("No ESP32 connected")
            return False

        try:
            sock = socket.socket(
                socket.AF_INET,
                socket.SOCK_DGRAM,
            )

            sock.settimeout(1)

            sock.sendto(
                str(effect).encode(),
                (
                    ip,
                    cls.PORT,
                ),
            )

            sock.close()

            print(f"Sent LED effect: {effect} -> {ip}:{cls.PORT}")

            return True

        except Exception as error:
            print("ESP32 send error:", error)
            return False

    @classmethod
    def send_command(cls, ip, data):
        """
        Backward compatible API.
        Example:
            ESP32Service.send_command(ip, {"effect": "SESAME"})
        """

        if not isinstance(data, dict):
            return False

        effect = data.get("effect")

        if not effect:
            return False

        return cls.send_effect(
            effect,
            ip,
        )

    @staticmethod
    def connected_ip():
        session = get_session()

        try:
            device = (
                session.query(Device)
                .filter(Device.status == "connected")
                .first()
            )

            if device:
                return device.ip

            return None

        finally:
            session.close()

    @staticmethod
    def mark_disconnected(ip=None):
        session = get_session()

        try:
            query = session.query(Device)

            if ip:
                query = query.filter(Device.ip == ip)

            devices = query.all()

            for device in devices:
                device.status = "disconnected"

            session.commit()

        except Exception as error:
            session.rollback()
            print("ESP32 disconnect update error:", error)

        finally:
            session.close()
