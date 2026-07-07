from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout
)

from app.ui.widgets.voice.status_panel import StatusPanel
from app.ui.widgets.voice.configuration_panel import ConfigurationPanel
from app.ui.widgets.voice.controls_panel import ControlsPanel
from app.ui.widgets.voice.recognition_panel import RecognitionPanel
from app.ui.widgets.voice.log_panel import LogPanel


class VoiceEnginePage(QWidget):

    def __init__(self, runtime = None):
        super().__init__()

        main = QVBoxLayout()

        top = QHBoxLayout()

        self.status = StatusPanel()
        self.config = ConfigurationPanel()

        top.addWidget(self.status, 1)
        top.addWidget(self.config, 2)

        main.addLayout(top)

        self.controls = ControlsPanel()
        self.recognition = RecognitionPanel()
        self.logs = LogPanel()

        main.addWidget(self.controls)
        main.addWidget(self.recognition)
        main.addWidget(self.logs)

        self.setLayout(main)