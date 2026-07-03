#include <Arduino.h>
#include <WiFiUdp.h>
#include <ArduinoJson.h>

#include "config.h"
#include "network/wifi_manager.h"
#include "api/api_server.h"
#include "led/led_controller.h"


// ===============================
// ESP32 Device Discovery
// ===============================

WiFiUDP udp;


const int DISCOVERY_PORT = 4210;


unsigned long discoveryTimer = 0;



void sendDiscovery()
{

    StaticJsonDocument<200> doc;


    doc["device"] = "SMART_SHOWROOM_FRAME";


    String message;


    serializeJson(
        doc,
        message
    );



    udp.beginPacket(
        "255.255.255.255",
        DISCOVERY_PORT
    );


    udp.print(
        message
    );


    udp.endPacket();



    Serial.println(
        "Discovery sent:"
    );


    Serial.println(
        message
    );

}



// ===============================
// Setup
// ===============================

void setup() {


    Serial.begin(
        115200
    );


    delay(500);



    // WiFi

    initWiFi();



    // Start UDP discovery

    udp.begin(
        DISCOVERY_PORT
    );



    Serial.println(
        "UDP Discovery Ready"
    );



    // LED

    initLED();



    // API Server

    initAPI();


}



// ===============================
// Main Loop
// ===============================

void loop() {


    handleAPI();



    updateLED();



    // Broadcast device every 5 seconds

    if(
        millis() - discoveryTimer > 5000
    )
    {


        discoveryTimer = millis();


        sendDiscovery();


    }


}