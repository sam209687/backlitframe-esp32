"""
main.py

Application Entry Point
"""

import os
import sys

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

sys.path.insert(
    0,
    os.path.join(BASE_DIR, "python_app")
)

from PySide6.QtWidgets import QApplication

from app.ui.main_window import MainWindow

from app.services.settings_service import SettingsService
from app.services.device_discovery import DeviceDiscovery

from app.showroom.showroom_runtime import ShowroomRuntime


def main():

    SettingsService.load()

    app = QApplication(sys.argv)

    discovery = DeviceDiscovery()
    discovery.start()

    runtime = ShowroomRuntime()

    window = MainWindow(runtime)

    window.show()

    runtime.start()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()