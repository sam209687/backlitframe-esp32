from app.services.voice_router import VoiceRouter

tests = [
    "Hello",
    "Hi",
    "Vanga Sir",
    "Show sesame oil",
    "Groundnut oil",
    "Help",
    "Repeat",
    "Again",
    "Stop",
]

print("=" * 70)
print("VOICE ROUTER TEST")
print("=" * 70)

for text in tests:

    print(f"\nInput : {text}")

    try:
        result = VoiceRouter.route(text)

        print(f"Type   : {type(result)}")
        print(f"Result : {result}")

        if result is not None:
            print(vars(result) if hasattr(result, "__dict__") else result)

    except Exception as e:
        print("ERROR:", e)

print("\nFinished.")