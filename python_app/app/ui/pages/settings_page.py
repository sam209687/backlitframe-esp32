"""
settings_page.py

Premium settings page.
Edit JSON configuration files from the dashboard.
"""

import json

from PySide6.QtWidgets import (
    QComboBox,
    QHBoxLayout,
    QLabel,
    QMessageBox,
    QTextEdit,
    QVBoxLayout,
)

from app.core.config_manager import load as load_config, save as save_config
from app.ui_comp.base import BaseButton, BaseCard, BasePage


CONFIG_FILES = [
    "app",
    "voice",
    "led",
    "display",
    "device",
]


class SettingsPage(BasePage):

    def __init__(self, runtime=None):
        super().__init__()

        self.runtime = runtime
        self.current_config = None

        self._build_ui()
        self.load_selected_config()

    def _build_ui(self):
        main_layout = self.layout()

        if main_layout is None:
            main_layout = QVBoxLayout()
            self.setLayout(main_layout)

        main_layout.setContentsMargins(24, 24, 24, 24)
        main_layout.setSpacing(16)

        # Header
        header_layout = QHBoxLayout()

        title_box = QVBoxLayout()
        title_box.setSpacing(4)

        title = QLabel("Settings")
        title.setObjectName("PageTitle")

        subtitle = QLabel("Edit application JSON configuration files")
        subtitle.setObjectName("PageSubtitle")

        title_box.addWidget(title)
        title_box.addWidget(subtitle)

        header_layout.addLayout(title_box)
        header_layout.addStretch()

        self.save_btn = BaseButton("Save Configuration")
        self.save_btn.clicked.connect(self.save_current_config)

        header_layout.addWidget(self.save_btn)

        main_layout.addLayout(header_layout)

        # Config selector card
        selector_card = BaseCard()
        selector_layout = QVBoxLayout(selector_card)
        selector_layout.setContentsMargins(16, 16, 16, 16)
        selector_layout.setSpacing(12)

        selector_layout.addWidget(QLabel("Configuration File"))

        self.config_selector = QComboBox()

        for config_name in CONFIG_FILES:
            self.config_selector.addItem(config_name)

        self.config_selector.currentIndexChanged.connect(
            self.load_selected_config
        )

        selector_layout.addWidget(self.config_selector)

        main_layout.addWidget(selector_card)

        # Editor card
        editor_card = BaseCard()
        editor_layout = QVBoxLayout(editor_card)
        editor_layout.setContentsMargins(16, 16, 16, 16)
        editor_layout.setSpacing(12)

        editor_title = QLabel("JSON Editor")
        editor_title.setObjectName("SectionTitle")

        self.editor = QTextEdit()
        self.editor.setPlaceholderText("Configuration JSON will appear here...")

        editor_layout.addWidget(editor_title)
        editor_layout.addWidget(self.editor)

        main_layout.addWidget(editor_card, 1)

    def load_selected_config(self):
        name = self.config_selector.currentText()

        if not name:
            return

        try:
            data = load_config(name)
            self.current_config = name

            self.editor.setText(
                json.dumps(
                    data,
                    indent=4,
                )
            )

        except Exception as error:
            QMessageBox.warning(
                self,
                "Error",
                str(error),
            )

    def save_current_config(self):
        if not self.current_config:
            QMessageBox.warning(
                self,
                "No Config Selected",
                "Please select a configuration file first.",
            )
            return

        try:
            data = json.loads(self.editor.toPlainText())

            save_config(
                self.current_config,
                data,
            )

            QMessageBox.information(
                self,
                "Saved",
                f"{self.current_config}.json updated successfully.",
            )

        except json.JSONDecodeError as error:
            QMessageBox.warning(
                self,
                "Invalid JSON",
                f"Please fix JSON syntax:\n{error}",
            )

        except Exception as error:
            QMessageBox.warning(
                self,
                "Error",
                str(error),
            )