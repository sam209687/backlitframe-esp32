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


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
