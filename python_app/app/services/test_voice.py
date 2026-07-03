from app.services.voice_service import VoiceService



voice = VoiceService()



print(
    voice.process_voice(
        "Vanga Sir"
    )
)



print(
    voice.process_voice(
        "show sesame oil"
    )
)
