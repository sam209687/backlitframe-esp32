"""
device_discovery.py

UDP listener for ESP32 auto discovery
"""


import socket
import json
import threading


from app.core.database import get_session
from app.models.device import Device



DISCOVERY_PORT = 4210



class DeviceDiscovery:


    def __init__(self):

        self.running = False

        self.thread = None



    def start(self):

        if self.running:
            return


        self.running = True


        self.thread = threading.Thread(
            target=self.listen,
            daemon=True
        )


        self.thread.start()



    def listen(self):

        sock = socket.socket(
            socket.AF_INET,
            socket.SOCK_DGRAM
        )


        sock.setsockopt(
            socket.SOL_SOCKET,
            socket.SO_BROADCAST,
            1
        )


        sock.bind(
            (
                "",
                DISCOVERY_PORT
            )
        )


        print(
            "ESP32 discovery started..."
        )



        while self.running:


            try:

                data, addr = sock.recvfrom(
                    1024
                )


                message = json.loads(
                    data.decode()
                )


                self.register_device(
                    message,
                    addr[0]
                )


            except Exception as e:

                print(
                    "Discovery error:",
                    e
                )




    def register_device(self, data, ip):

        name = data.get("device")

        if not name:
            return

        session = get_session()

        try:

            device = (
                session.query(Device)
                .filter_by(device_name=name)
                .first()
            )

            if device:

                # Only print if IP changed or device was disconnected
                if device.ip != ip or device.status != "connected":
                    print(f"Device updated: {name} ({ip})")

                device.ip = ip
                device.status = "connected"

            else:

                device = Device(
                    device_name=name,
                    ip=ip,
                    status="connected"
                )

                session.add(device)

                print(f"Device registered: {name} ({ip})")

            session.commit()

        finally:
            session.close()