"""
settings_page.py
Edit config/*.json files directly from the dashboard.
"""

import json

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QComboBox, QTextEdit,
    QPushButton, QMessageBox
)

from app.core.config_manager import load as load_config, save as save_config, reload as reload_config
from app.core.logger import get_logger

logger = get_logger(__name__)

CONFIG_FILES = ["app", "voice", "led", "display", "device"]


class SettingsPage(QWidget):
    def __init__(self):
        super().__init__()
        self._build_ui()
        self.load_selected()

    def _build_ui(self):
        layout = QVBoxLayout()

        title = QLabel("Settings")
        title.setStyleSheet("font-size: 18px; font-weight: bold;")
        layout.addWidget(title)

        selector_row = QHBoxLayout()
        selector_row.addWidget(QLabel("Config file:"))
        self.file_combo = QComboBox()
        self.file_combo.addItems([f"{name}.json" for name in CONFIG_FILES])
        self.file_combo.currentIndexChanged.connect(self.load_selected)
        selector_row.addWidget(self.file_combo)
        selector_row.addStretch()
        layout.addLayout(selector_row)

        self.editor = QTextEdit()
        self.editor.setStyleSheet("font-family: monospace;")
        layout.addWidget(self.editor)

        self.error_label = QLabel("")
        self.error_label.setStyleSheet("color: red;")
        layout.addWidget(self.error_label)

        button_row = QHBoxLayout()
        save_btn = QPushButton("Save")
        save_btn.clicked.connect(self.save_selected)
        reload_btn = QPushButton("Reload from Disk")
        reload_btn.clicked.connect(self.load_selected)
        button_row.addWidget(save_btn)
        button_row.addWidget(reload_btn)
        button_row.addStretch()
        layout.addLayout(button_row)

        self.setLayout(layout)

    def _current_name(self):
        return CONFIG_FILES[self.file_combo.currentIndex()]

    def load_selected(self):
        name = self._current_name()
        try:
            data = reload_config(name)
            self.editor.setPlainText(json.dumps(data, indent=2))
            self.error_label.setText("")
        except FileNotFoundError as e:
            self.error_label.setText(str(e))

    def save_selected(self):
        name = self._current_name()
        text = self.editor.toPlainText()
        try:
            data = json.loads(text)
        except json.JSONDecodeError as e:
            self.error_label.setText(f"Invalid JSON: {e}")
            return

        save_config(name, data)
        self.error_label.setText("")
        logger.info(f"Saved config/{name}.json")
        QMessageBox.information(self, "Saved", f"config/{name}.json updated.")