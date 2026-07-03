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

    app = QApplication(sys.argv)


    # Start ESP32 discovery listener

    discovery = DeviceDiscovery()

    discovery.start()



    window = MainWindow()

    window.show()


    sys.exit(app.exec())

if __name__ == "__main__":
    main()
