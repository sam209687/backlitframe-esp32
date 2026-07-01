#include "ambient_effects.h"

void cozyReadingEffect(CRGB leds[]) {
    fill_solid(leds, LED_COUNT, CRGB(255, 184, 119));
    FastLED.setBrightness(150);
}
