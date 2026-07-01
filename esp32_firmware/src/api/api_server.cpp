#include "api_server.h"
#include <ESPAsyncWebServer.h>
#include <ArduinoJson.h>
#include "config.h"
#include "../led/led_controller.h"

static AsyncWebServer server(API_PORT);

static void handleStatus(AsyncWebServerRequest *request) {
    StaticJsonDocument<128> doc;
    doc["device"] = DEVICE_NAME;
    doc["status"] = "connected";

    String response;
    serializeJson(doc, response);
    request->send(200, "application/json", response);
}

// Unified JSON command endpoint. Body example:
// { "effect": "sesame", "time": 30 }
static void handleCommand(AsyncWebServerRequest *request, uint8_t *data, size_t len) {
    StaticJsonDocument<256> doc;
    DeserializationError err = deserializeJson(doc, data, len);
    if (err) {
        request->send(400, "application/json", "{\"error\":\"invalid json\"}");
        return;
    }

    if (doc.containsKey("effect")) {
        String effectName = doc["effect"].as<String>();
        effectName.toUpperCase();
        LedEffect effect = effectFromString(effectName);
        setEffect(effect);
    }

    request->send(200, "application/json", "{\"ok\":true}");
}

// Legacy-style per-product routes, kept for backward compatibility
// with the original firmware (e.g. GET /sesame, /groundnut).
static void registerLegacyRoutes() {
    server.on("/sesame", HTTP_GET, [](AsyncWebServerRequest *request) {
        setEffect(SESAME);
        request->send(200, "text/plain", "OK");
    });

    server.on("/groundnut", HTTP_GET, [](AsyncWebServerRequest *request) {
        setEffect(GROUNDNUT);
        request->send(200, "text/plain", "OK");
    });

    server.on("/effect/fire", HTTP_GET, [](AsyncWebServerRequest *request) {
        // example of a named/legacy effect route
        setEffect(PC_MODE);
        request->send(200, "text/plain", "OK");
    });
}

void initAPI() {
    server.on("/status", HTTP_GET, handleStatus);

    server.on(
        "/command",
        HTTP_POST,
        [](AsyncWebServerRequest *request) {},
        NULL,
        [](AsyncWebServerRequest *request, uint8_t *data, size_t len, size_t index, size_t total) {
            handleCommand(request, data, len);
        });

    registerLegacyRoutes();

    server.begin();
    Serial.println("API server started.");
}

void handleAPI() {
    // AsyncWebServer handles requests in the background; nothing needed here
    // unless you add polling logic later (e.g. OTA checks).
}
