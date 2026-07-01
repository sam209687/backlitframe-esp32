#include "led_controller.h"
#include <FastLED.h>
#include "config.h"
#include "../effects/oil_effects.h"
#include "../effects/ambient_effects.h"
#include "../effects/gaming_effects.h"

CRGB leds[LED_COUNT];
static LedEffect currentEffect = EFFECT_NONE;

void initLED() {
    FastLED.addLeds<WS2812B, DATA_PIN, GRB>(leds, LED_COUNT);
    FastLED.setBrightness(200);
    FastLED.clear();
    FastLED.show();
}

void setEffect(LedEffect effect) {
    currentEffect = effect;
}

LedEffect effectFromString(const String &name) {
    if (name == "SESAME") return SESAME;
    if (name == "GROUNDNUT") return GROUNDNUT;
    if (name == "COCONUT") return COCONUT;
    if (name == "MUSTARD") return MUSTARD;
    if (name == "PC_MODE") return PC_MODE;
    if (name == "COZY_READING") return COZY_READING;
    if (name == "FILLING_OIL") return FILLING_OIL;
    return EFFECT_NONE;
}

// Called every loop() iteration. Dispatches to the effect functions
// defined in src/effects/.
void updateLED() {
    switch (currentEffect) {
        case SESAME:
            sesameEffect(leds);
            break;
        case GROUNDNUT:
            groundnutEffect(leds);
            break;
        case COCONUT:
            coconutEffect(leds);
            break;
        case MUSTARD:
            mustardEffect(leds);
            break;
        case PC_MODE:
            pcModeEffect(leds);
            break;
        case COZY_READING:
            cozyReadingEffect(leds);
            break;
        case FILLING_OIL:
            fillingOilEffect(leds);
            break;
        case EFFECT_NONE:
        default:
            // idle - leave LEDs as-is
            break;
    }
    FastLED.show();
}
