from faster_whisper import WhisperModel

model = WhisperModel(
    "tiny",
    device="cpu",
    compute_type="int8"
)

segments, info = model.transcribe(
    "voice.wav",
    beam_size=5,
    vad_filter=False
)

print("Language:", info.language)
print("Probability:", info.language_probability)

found = False

for segment in segments:
    found = True
    print(
        f"[{segment.start:.2f}-{segment.end:.2f}] {segment.text}"
    )

if not found:
    print("No segments detected.")