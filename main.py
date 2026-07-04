"""
main.py
Application entry point. Launches the PySide6 dashboard.

Run with (from repo root, venv activated):
    python main.py
"""

import os
import sys

# Make python_app/ importable as `app`
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(0, os.path.join(BASE_DIR, "python_app"))

from PySide6.QtWidgets import QApplication  # noqa: E402
from app.ui.main_window import MainWindow  # noqa: E402
from app.services.device_discovery import DeviceDiscovery  # noqa: E402
from app.services.settings_service import SettingsService

SettingsService.load()

def main():

    SettingsService.load()

    app = QApplication(sys.argv)

    discovery = DeviceDiscovery()
    discovery.start()

    dashboard = MainWindow()

    from app.ui.showroom_window import ShowroomWindow

    showroom = ShowroomWindow()

    dashboard.show()

    showroom.show()

    sys.exit(app.exec())