#include "gaming_effects.h"

// Simple rainbow cycle for "PC / gaming" mode
void pcModeEffect(CRGB leds[]) {
    static uint8_t hue = 0;
    fill_rainbow(leds, LED_COUNT, hue, 7);
    hue++;
    FastLED.setBrightness(200);
}
