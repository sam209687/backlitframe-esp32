#pragma once

#include <Arduino.h>

enum LedEffect {
    EFFECT_NONE,
    SESAME,
    GROUNDNUT,
    COCONUT,
    MUSTARD,
    PC_MODE,
    COZY_READING,
    FILLING_OIL
};

void initLED();
void updateLED();
void setEffect(LedEffect effect);
LedEffect effectFromString(const String &name);
