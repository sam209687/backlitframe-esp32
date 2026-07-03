"""
whisper_service.py

Offline speech recognition using faster-whisper
"""


from faster_whisper import WhisperModel



class WhisperService:


    def __init__(self):

        print(
            "Loading Whisper model..."
        )


        self.model = WhisperModel(

            "tiny",

            device="cpu",

            compute_type="int8"

        )


        print(
            "Whisper ready"
        )




    def transcribe(
        self,
        audio_file
    ):


        segments, info = self.model.transcribe(

    audio_file,

    beam_size=5,

    language="en",

    vad_filter=True

)


        text = ""


        for segment in segments:

            text += segment.text



        return text.strip()
