#include "oil_effects.h"

// Simple helper: fade all LEDs toward a target color.
static void colorFade(CRGB leds[], CRGB from, CRGB to) {
    static uint8_t step = 0;
    step = (step + 1) % 256;
    CRGB blended = blend(from, to, step);
    fill_solid(leds, LED_COUNT, blended);
}

void sesameEffect(CRGB leds[]) {
    colorFade(leds, CRGB::White, CRGB(255, 180, 80));
}

void groundnutEffect(CRGB leds[]) {
    colorFade(leds, CRGB::White, CRGB(198, 142, 63));
}

void coconutEffect(CRGB leds[]) {
    colorFade(leds, CRGB::White, CRGB(245, 245, 220));
}

void mustardEffect(CRGB leds[]) {
    colorFade(leds, CRGB::White, CRGB(181, 166, 66));
}

void fillingOilEffect(CRGB leds[]) {
    // quick pulse effect
    static uint8_t brightness = 0;
    static int8_t direction = 5;
    brightness += direction;
    if (brightness == 0 || brightness == 255) direction = -direction;
    fill_solid(leds, LED_COUNT, CRGB(255, 215, 0));
    FastLED.setBrightness(brightness);
}
