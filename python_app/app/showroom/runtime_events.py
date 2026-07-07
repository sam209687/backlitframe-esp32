"""
runtime_events.py

Central list of events used by the Smart Showroom Runtime.

Every service publishes events here instead of directly
calling another module.
"""


class RuntimeEvents:

    # --------------------------------------------------
    # Runtime
    # --------------------------------------------------

    STATE_CHANGED = "state_changed"

    ERROR = "runtime_error"

    WARNING = "runtime_warning"

    # --------------------------------------------------
    # Voice
    # --------------------------------------------------

    WAKEWORD_DETECTED = "wakeword_detected"

    LISTENING_STARTED = "listening_started"

    LISTENING_STOPPED = "listening_stopped"

    VOICE_TEXT = "voice_text"

    PRODUCT_FOUND = "product_found"

    PRODUCT_NOT_FOUND = "product_not_found"

    VOICE_TIMEOUT = "voice_timeout"

    # --------------------------------------------------
    # Media
    # --------------------------------------------------

    MEDIA_STARTED = "media_started"

    MEDIA_CHANGED = "media_changed"

    MEDIA_FINISHED = "media_finished"

    SLIDESHOW_STARTED = "slideshow_started"

    SLIDESHOW_FINISHED = "slideshow_finished"

    DEFAULT_MEDIA = "default_media"

    # --------------------------------------------------
    # LED
    # --------------------------------------------------

    LED_EFFECT_CHANGED = "led_effect_changed"

    # --------------------------------------------------
    # ESP32
    # --------------------------------------------------

    ESP32_CONNECTED = "esp32_connected"

    ESP32_DISCONNECTED = "esp32_disconnected"

    RELAY_CHANGED = "relay_changed"

    HEARTBEAT = "heartbeat"

    # --------------------------------------------------
    # Customer Session
    # --------------------------------------------------

    SESSION_STARTED = "session_started"

    SESSION_ENDED = "session_ended"

    CUSTOMER_DETECTED = "customer_detected"

    CUSTOMER_LEFT = "customer_left"

    # --------------------------------------------------
    # Dashboard

    DASHBOARD_REFRESH = "dashboard_refresh"

    LOG_MESSAGE = "log_message"