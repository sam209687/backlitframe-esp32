from PySide6.QtWidgets import (
    QGroupBox,
    QFormLayout,
    QComboBox,
    QSpinBox,
    QCheckBox,
    QPushButton
)


class ConfigurationPanel(QGroupBox):

    def __init__(self):
        super().__init__("Configuration")

        layout = QFormLayout()

        self.model = QComboBox()
        self.model.addItems([
            "tiny",
            "base",
            "small",
            "medium"
        ])

        self.language = QComboBox()
        self.language.addItems([
            "Auto",
            "English",
            "Tamil"
        ])

        self.beam = QSpinBox()
        self.beam.setRange(1, 10)
        self.beam.setValue(5)

        self.activation = QSpinBox()
        self.activation.setRange(1, 30)
        self.activation.setValue(10)

        self.recognition = QSpinBox()
        self.recognition.setRange(1, 30)
        self.recognition.setValue(5)

        self.cooldown = QSpinBox()
        self.cooldown.setRange(0, 30)

        self.vad = QCheckBox()

        self.save = QPushButton("Save Settings")

        layout.addRow("Whisper Model", self.model)
        layout.addRow("Language", self.language)
        layout.addRow("Beam Size", self.beam)
        layout.addRow("Activation Delay", self.activation)
        layout.addRow("Recognition Timeout", self.recognition)
        layout.addRow("Cooldown", self.cooldown)
        layout.addRow("Enable VAD", self.vad)
        layout.addRow(self.save)

        self.setLayout(layout)