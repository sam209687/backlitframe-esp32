#include "wifi_manager.h"
#include <WiFi.h>
#include "config.h"

void initWiFi() {
    WiFi.mode(WIFI_STA);
    WiFi.begin(WIFI_SSID, WIFI_PASSWORD);

    Serial.print("Connecting to WiFi");
    unsigned long start = millis();
    while (WiFi.status() != WL_CONNECTED && millis() - start < 15000) {
        delay(500);
        Serial.print(".");
    }

    if (WiFi.status() == WL_CONNECTED) {
        Serial.println();
        Serial.print("Connected. IP address: ");
        Serial.println(WiFi.localIP());
    } else {
        Serial.println();
        Serial.println("WiFi connection failed - will retry in loop()");
    }
}

bool isWiFiConnected() {
    return WiFi.status() == WL_CONNECTED;
}
