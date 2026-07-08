"""
presets.py
Named LED effect presets that map to firmware-side effect identifiers.
Keep this list in sync with esp32_firmware/src/led/led_controller.h
"""

EFFECT_PRESETS = {
    "none": "NONE",
    "sesame": "SESAME",
    "groundnut": "GROUNDNUT",
    "coconut": "COCONUT",
    "mustard": "MUSTARD",
    "pc_mode": "PC_MODE",
    "cozy_reading": "COZY_READING",
    "filling_oil": "FILLING_OIL",

    "rainbow": "RAINBOW",
    "breathing": "BREATHING",
    "chase": "CHASE",
    "sparkle": "SPARKLE",
    "fill": "FILL",
    "off": "OFF",
}


def resolve_effect(product_name: str) -> str | None:
    return EFFECT_PRESETS.get(product_name.lower())
