from app.services.microphone_service import MicrophoneService

from app.services.whisper_service import WhisperService



mic = MicrophoneService()

whisper = WhisperService()



file = mic.record(
    seconds=5
)



text = whisper.transcribe(
    file
)



print(
    "Heard:",
    text
)
