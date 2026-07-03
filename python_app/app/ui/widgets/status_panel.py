from PySide6.QtWidgets import (
    QGroupBox,
    QLabel,
    QGridLayout
)


class StatusPanel(QGroupBox):

    def __init__(self):
        super().__init__("Status")

        layout = QGridLayout()

        self.voice = QLabel("🔴 Stopped")
        self.mic = QLabel("⚪ Unknown")
        self.whisper = QLabel("⚪ Not Loaded")
        self.esp32 = QLabel("⚪ Disconnected")

        layout.addWidget(QLabel("Voice Engine"), 0, 0)
        layout.addWidget(self.voice, 0, 1)

        layout.addWidget(QLabel("Microphone"), 1, 0)
        layout.addWidget(self.mic, 1, 1)

        layout.addWidget(QLabel("Whisper"), 2, 0)
        layout.addWidget(self.whisper, 2, 1)

        layout.addWidget(QLabel("ESP32"), 3, 0)
        layout.addWidget(self.esp32, 3, 1)

        self.setLayout(layout)