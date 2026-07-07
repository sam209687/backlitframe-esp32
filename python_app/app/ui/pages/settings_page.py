"""
settings_page.py

Edit JSON configuration files from the dashboard.
"""

import json
import os

from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QTextEdit,
    QPushButton,
    QComboBox,
    QMessageBox
)

from app.core.config_manager import load as load_config, save as save_config


CONFIG_FILES = [
    "app",
    "voice",
    "led",
    "display",
    "device"
]


class SettingsPage(QWidget):

    def __init__(self, runtime = None):
        super().__init__()

        self.current_config = None

        self._build_ui()
        self.load_selected_config()


    def _build_ui(self):

        layout = QVBoxLayout()


        title = QLabel("Settings")
        title.setStyleSheet(
            "font-size:18px;font-weight:bold;"
        )

        layout.addWidget(title)


        self.config_selector = QComboBox()

        for cfg in CONFIG_FILES:
            self.config_selector.addItem(cfg)


        self.config_selector.currentIndexChanged.connect(
            self.load_selected_config
        )


        layout.addWidget(
            QLabel("Configuration file:")
        )

        layout.addWidget(
            self.config_selector
        )


        self.editor = QTextEdit()

        layout.addWidget(
            self.editor
        )


        save_btn = QPushButton(
            "Save Configuration"
        )

        save_btn.clicked.connect(
            self.save_current_config
        )


        layout.addWidget(
            save_btn
        )


        self.setLayout(layout)



    def load_selected_config(self):

        name = self.config_selector.currentText()

        try:

            data = load_config(name)

            self.current_config = name

            self.editor.setText(
                json.dumps(
                    data,
                    indent=4
                )
            )


        except Exception as e:

            QMessageBox.warning(
                self,
                "Error",
                str(e)
            )



    def save_current_config(self):

        try:

            data = json.loads(
                self.editor.toPlainText()
            )


            save_config(
                self.current_config,
                data
            )


            QMessageBox.information(
                self,
                "Saved",
                "Configuration updated"
            )


        except json.JSONDecodeError:

            QMessageBox.warning(
                self,
                "Invalid JSON",
                "Please fix JSON syntax"
            )


        except Exception as e:

            QMessageBox.warning(
                self,
                "Error",
                str(e)
            )