"""
microphone_service.py

Records microphone audio using ALSA (arecord).

Priority:
1. USB PnP Sound Device
2. First available capture device

This implementation avoids PortAudio/sounddevice completely,
making it much more reliable on Linux.
"""

import os
import subprocess


class MicrophoneService:

    def __init__(self):

        self.device = self.find_microphone()

    # -------------------------------------------------

    def find_microphone(self):

        try:

            output = subprocess.check_output(
                ["arecord", "-l"],
                text=True
            )

            print("--------------------------------")
            print("Available Capture Devices")
            print("--------------------------------")
            print(output)

            # Prefer USB microphone
            if "USB" in output:

                for line in output.splitlines():

                    if "USB" in line and "card" in line:

                        # Example:
                        # card 2: Device [USB PnP Sound Device], device 0: USB Audio

                        card = line.split("card")[1].split(":")[0].strip()
                        device = line.split("device")[1].split(":")[0].strip()

                        hw = f"hw:{card},{device}"

                        print(f"Using USB microphone: {hw}")

                        return hw

            # Fallback to first capture device

            for line in output.splitlines():

                if "card" in line and "device" in line:

                    card = line.split("card")[1].split(":")[0].strip()
                    device = line.split("device")[1].split(":")[0].strip()

                    hw = f"hw:{card},{device}"

                    print(f"Using microphone: {hw}")

                    return hw

        except Exception as e:

            print("Unable to detect microphone:", e)

        print("Falling back to default device")

        return "default"

    # -------------------------------------------------

    def record(
        self,
        filename="voice.wav",
        seconds=5,
        samplerate=16000,
    ):

        print("\n================================")
        print(f"Listening ({seconds} sec)...")
        print("================================")
        print(f"Device      : {self.device}")
        print(f"Sample Rate : {samplerate}")
        print(f"Channels    : 1")

        if os.path.exists(filename):
            os.remove(filename)

        command = [

            "arecord",

            "-D", self.device,

            "-f", "S16_LE",

            "-r", str(samplerate),

            "-c", "1",

            "-d", str(seconds),

            filename,

        ]

        try:

            subprocess.run(
                command,
                check=True,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )

        except subprocess.CalledProcessError as e:

            print("Recording failed:", e)

            return None

        if not os.path.exists(filename):

            print("Recording file not created.")

            return None

        size = os.path.getsize(filename)

        print("\nRecorded Successfully")
        print("----------------------------")
        print(f"File : {filename}")
        print(f"Size : {size} bytes")
        print("----------------------------")

        if size < 2048:

            print("Recording appears to be empty.")

            return None

        return filename