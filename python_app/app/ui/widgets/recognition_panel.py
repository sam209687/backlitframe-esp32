from PySide6.QtWidgets import (
    QGroupBox,
    QLabel,
    QFormLayout
)


class RecognitionPanel(QGroupBox):

    def __init__(self):
        super().__init__("Recognition")

        layout = QFormLayout()

        self.wake = QLabel("-")
        self.speech = QLabel("-")
        self.product = QLabel("-")
        self.led = QLabel("-")
        self.device = QLabel("-")

        layout.addRow("Wake Word", self.wake)
        layout.addRow("Speech", self.speech)
        layout.addRow("Matched Product", self.product)
        layout.addRow("LED Effect", self.led)
        layout.addRow("ESP32", self.device)

        self.setLayout(layout)