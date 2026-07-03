from PySide6.QtWidgets import (
    QGroupBox,
    QFormLayout,
    QComboBox,
    QSpinBox,
    QCheckBox,
    QPushButton
)

from app.services.settings_service import SettingsService
from PySide6.QtWidgets import QMessageBox


class ConfigurationPanel(QGroupBox):

    def __init__(self):
        super().__init__("Configuration")

        layout = QFormLayout()

        self.load_settings()

        self.save.clicked.connect(
            self.save_settings
        )

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



        def load_settings(self):

            self.model.setCurrentText(
                SettingsService.get(
                    "whisper_model",
                    "tiny"
                )
            )

            self.language.setCurrentText(
                SettingsService.get(
                    "voice_language",
                    "Auto"
                )
            )

            self.beam.setValue(
                SettingsService.get_int(
                    "beam_size",
                    5
                )
            )

            self.activation.setValue(
                SettingsService.get_int(
                    "activation_timeout",
                    10
                )
            )

            self.recognition.setValue(
                SettingsService.get_int(
                    "recognition_timeout",
                    5
                )
            )

            self.cooldown.setValue(
                SettingsService.get_int(
                    "cooldown",
                    3
                )
            )

            self.vad.setChecked(
                SettingsService.get_bool(
                    "vad_enabled",
                    True
                )
            )
    

        def save_settings(self):

            SettingsService.set(
            "whisper_model",
            self.model.currentText()
        )

            SettingsService.set(
            "voice_language",
            self.language.currentText()
        )

            SettingsService.set(
            "beam_size",
            self.beam.value()
        )

            SettingsService.set(
            "activation_timeout",
            self.activation.value()
        )

            SettingsService.set(
            "recognition_timeout",
            self.recognition.value()
        )

            SettingsService.set(
            "cooldown",
            self.cooldown.value()
        )

            SettingsService.set(
            "vad_enabled",
            self.vad.isChecked()
        )

            QMessageBox.information(
            self,
            "Settings",
            "Voice settings saved successfully."
        )

        layout.addRow("Whisper Model", self.model)
        layout.addRow("Language", self.language)
        layout.addRow("Beam Size", self.beam)
        layout.addRow("Activation Delay", self.activation)
        layout.addRow("Recognition Timeout", self.recognition)
        layout.addRow("Cooldown", self.cooldown)
        layout.addRow("Enable VAD", self.vad)
        layout.addRow(self.save)

        self.setLayout(layout)