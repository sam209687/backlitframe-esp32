"""
status_indicator.py

Reusable red / green / warning status button.
Used to show Connected, Disconnected, Ready, Error, Listening, Idle, etc.
"""

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QPushButton


class StatusIndicator(QPushButton):

    CONNECTED = "connected"
    DISCONNECTED = "disconnected"
    READY = "ready"
    ERROR = "error"
    IDLE = "idle"
    LISTENING = "listening"
    WARNING = "warning"
    PLAYING = "playing"

    STATUS_STYLES = {
        CONNECTED: {
            "text": "Connected",
            "bg": "#16a34a",
            "border": "#22c55e",
        },
        READY: {
            "text": "Ready",
            "bg": "#16a34a",
            "border": "#22c55e",
        },
        PLAYING: {
            "text": "Playing",
            "bg": "#16a34a",
            "border": "#22c55e",
        },
        DISCONNECTED: {
            "text": "Disconnected",
            "bg": "#dc2626",
            "border": "#ef4444",
        },
        ERROR: {
            "text": "Error",
            "bg": "#dc2626",
            "border": "#ef4444",
        },
        WARNING: {
            "text": "Warning",
            "bg": "#d97706",
            "border": "#f59e0b",
        },
        LISTENING: {
            "text": "Listening",
            "bg": "#2563eb",
            "border": "#3b82f6",
        },
        IDLE: {
            "text": "Idle",
            "bg": "#374151",
            "border": "#6b7280",
        },
    }

    def __init__(self, text="Idle", status=IDLE, parent=None):
        super().__init__(parent)

        self.status = status

        self.setCursor(Qt.PointingHandCursor)
        self.setMinimumHeight(34)
        self.setCheckable(False)
        self.setFocusPolicy(Qt.NoFocus)

        self.set_status(status, text)

    def set_status(self, status, text=None):
        self.status = status

        data = self.STATUS_STYLES.get(
            status,
            self.STATUS_STYLES[self.IDLE],
        )

        label = text if text is not None else data["text"]

        self.setText(f"● {label}")

        self.setStyleSheet(f"""
            QPushButton {{
                background: {data["bg"]};
                color: white;
                border: 1px solid {data["border"]};
                border-radius: 15px;
                padding: 6px 14px;
                font-size: 13px;
                font-weight: 700;
            }}

            QPushButton:hover {{
                border: 1px solid white;
            }}
        """)

    def set_connected(self, text="Connected"):
        self.set_status(self.CONNECTED, text)

    def set_disconnected(self, text="Disconnected"):
        self.set_status(self.DISCONNECTED, text)

    def set_ready(self, text="Ready"):
        self.set_status(self.READY, text)

    def set_error(self, text="Error"):
        self.set_status(self.ERROR, text)

    def set_idle(self, text="Idle"):
        self.set_status(self.IDLE, text)

    def set_listening(self, text="Listening"):
        self.set_status(self.LISTENING, text)

    def set_warning(self, text="Warning"):
        self.set_status(self.WARNING, text)

    def set_playing(self, text="Playing"):
        self.set_status(self.PLAYING, text)