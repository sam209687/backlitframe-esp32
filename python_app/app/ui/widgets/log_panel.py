from PySide6.QtWidgets import (
    QGroupBox,
    QTextEdit,
    QVBoxLayout
)


class LogPanel(QGroupBox):

    def __init__(self):
        super().__init__("Live Log")

        layout = QVBoxLayout()

        self.log = QTextEdit()
        self.log.setReadOnly(True)

        layout.addWidget(self.log)

        self.setLayout(layout)