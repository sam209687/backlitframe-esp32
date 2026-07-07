"""
esp32_service.py

Single interface between Python and ESP32.
"""

import requests


class ESP32Service:

    _ip = None
    _timeout = 2

    # ------------------------------------

    @classmethod
    def set_ip(cls, ip):

        cls._ip = ip

        print(f"ESP32 IP : {ip}")

    # ------------------------------------

    @classmethod
    def connected(cls):

        return cls._ip is not None

    # ------------------------------------

    @classmethod
    def _url(cls, path):

        return f"http://{cls._ip}/{path}"

    # ------------------------------------

    @classmethod
    def send(cls, path):

        if not cls.connected():

            print("ESP32 not connected")
            return False

        try:

            url = cls._url(path)

            print("GET", url)

            requests.get(
                url,
                timeout=cls._timeout
            )

            return True

        except Exception as e:

            print("ESP32 Error:", e)

            return False

    # ------------------------------------

    @classmethod
    def play(cls, effect):

        return cls.send(
            f"effect/{effect}"
        )

    # ------------------------------------

    @classmethod
    def stop(cls):

        return cls.send("stop")

    # ------------------------------------

    @classmethod
    def brightness(cls, value):

        return cls.send(
            f"brightness/{value}"
        )

    # ------------------------------------

    @classmethod
    def reboot(cls):

        return cls.send("restart")

    # ------------------------------------

    @classmethod
    def ping(cls):

        return cls.send("ping")