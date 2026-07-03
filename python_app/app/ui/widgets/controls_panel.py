from PySide6.QtWidgets import (
    QGroupBox,
    QPushButton,
    QHBoxLayout
)


class ControlsPanel(QGroupBox):

    def __init__(self):
        super().__init__("Controls")

        layout = QHBoxLayout()

        self.start = QPushButton("Start Engine")
        self.stop = QPushButton("Stop Engine")
        self.test = QPushButton("Test Microphone")
        self.reload = QPushButton("Reload Settings")

        layout.addWidget(self.start)
        layout.addWidget(self.stop)
        layout.addWidget(self.test)
        layout.addWidget(self.reload)

        self.setLayout(layout)