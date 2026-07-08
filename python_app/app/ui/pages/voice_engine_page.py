from PySide6.QtWidgets import QHBoxLayout, QVBoxLayout

from app.ui.widgets.voice.status_panel import StatusPanel
from app.ui.widgets.voice.configuration_panel import ConfigurationPanel
from app.ui.widgets.voice.controls_panel import ControlsPanel
from app.ui.widgets.voice.recognition_panel import RecognitionPanel
from app.ui.widgets.voice.log_panel import LogPanel

from app.ui_comp.base import BaseCard, BasePage


class VoiceEnginePage(BasePage):

    def __init__(self, runtime=None):
        super().__init__()

        self.runtime = runtime
        self.build_ui()

    def build_ui(self):
        main = self.layout()

        if main is None:
            main = QVBoxLayout()
            self.setLayout(main)

        main.setContentsMargins(24, 24, 24, 24)
        main.setSpacing(16)

        top = QHBoxLayout()
        top.setSpacing(16)

        self.status = StatusPanel()
        self.config = ConfigurationPanel()

        status_card = BaseCard()
        status_layout = QVBoxLayout(status_card)
        status_layout.setContentsMargins(16, 16, 16, 16)
        status_layout.addWidget(self.status)

        config_card = BaseCard()
        config_layout = QVBoxLayout(config_card)
        config_layout.setContentsMargins(16, 16, 16, 16)
        config_layout.addWidget(self.config)

        top.addWidget(status_card, 1)
        top.addWidget(config_card, 2)

        main.addLayout(top)

        self.controls = ControlsPanel()
        self.recognition = RecognitionPanel()
        self.logs = LogPanel()

        for widget in [
            self.controls,
            self.recognition,
            self.logs,
        ]:
            card = BaseCard()
            card_layout = QVBoxLayout(card)
            card_layout.setContentsMargins(16, 16, 16, 16)
            card_layout.addWidget(widget)
            main.addWidget(card)