"""
microphone_service.py

Records microphone audio
"""


import sounddevice as sd
import scipy.io.wavfile as wav



class MicrophoneService:


    def record(

        self,

        filename="voice.wav",

        seconds=5,

        samplerate=44100

    ):


        print(
            "Listening..."
        )


        audio = sd.rec(

            int(seconds * samplerate),

            samplerate=samplerate,

            channels=1,

            device=1,

            dtype="int16"

        )


        sd.wait()



        wav.write(

            filename,

            samplerate,

            audio

        )


        print(
            "Recorded"
        )


        return filename