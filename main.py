"""
main.py

Application entry point.
"""

import os
import sys

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
PYTHON_APP_DIR = os.path.join(BASE_DIR, "python_app")

if PYTHON_APP_DIR not in sys.path:
    sys.path.insert(0, PYTHON_APP_DIR)

from PySide6.QtWidgets import QApplication

from app.ui_comp.layout.main_window import MainWindow
from app.ui.showroom_window import ShowroomWindow

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

    showroom_window = ShowroomWindow(runtime.media_engine)

    screens = app.screens()

    if len(screens) > 1:
        showroom_window.setGeometry(
            screens[1].availableGeometry()
        )

    showroom_window.show()

    app.discovery = discovery
    app.runtime = runtime
    app.main_window = window
    app.showroom_window = showroom_window

    runtime.start()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()