import sounddevice as sd


DEVICE = 1

duration = 5

samplerate = 44100



print(
    "Using:",
    sd.query_devices(DEVICE)
)


print(
    "Speak now..."
)



audio = sd.rec(

    int(duration * samplerate),

    samplerate=samplerate,

    channels=1,

    device=DEVICE

)



sd.wait()



print(
    "Max:",
    audio.max()
)


print(
    "Min:",
    audio.min()
)