#include <Arduino.h>
#include "config.h"
#include "network/wifi_manager.h"
#include "api/api_server.h"
#include "led/led_controller.h"

void setup() {
    Serial.begin(115200);

    initWiFi();
    initLED();
    initAPI();
}

void loop() {
    handleAPI();
    updateLED();
}
