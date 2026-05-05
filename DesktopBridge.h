/**
 * @file DesktopBridge.h
 * @brief Thin JSON-over-Serial bridge.
 *
 * Replaces the entire LVGL/touch UI layer.
 * Desktop → ESP32 : one JSON object per line, ending with '\n'
 * ESP32 → Desktop : one JSON object per line, ending with '\n'
 */
#pragma once
#include <Arduino.h>

namespace DesktopBridge {

    void begin();                                 // call once in setup()
    void update();                                // call every loop() tick

    // Helpers for sending events back to the desktop
    void sendEvent(const char* event, const char* jsonPayload);
    void sendError(const char* msg);
    void sendState(const char* stateName);

    // Accessors set by the last "SET_ID" command
    String getSampleID();

    // Called by StateMachine to report moisture data
    void reportMoistureData(const struct MoistureData& d);

    // Called by StateMachine to report a history row
    void reportHistoryRow(const struct MoistureData& d);
    void reportHistoryEnd();

    // Called by StateMachine to report WiFi status
    void reportWifiStatus(bool connected, const char* ip);
}
