"""
led_page.py
Pick a device, trigger LED effect presets, and adjust brightness.
Brightness is stored in config/led.json (the ESP32 firmware currently
applies brightness only at boot from its own default; sending a live
brightness value would require extending the /command API on the
firmware side - see the note below the slider).
"""

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QComboBox, QPushButton,
    QSlider, QMessageBox, QGridLayout
)
from PySide6.QtCore import Qt

from app.core.database import get_session
from app.core.logger import get_logger
from app.core.config_manager import load as load_config, save as save_config
from app.models.device import Device
from app.modules.led.presets import EFFECT_PRESETS
from app.modules.led.effects import EFFECT_META
from app.services.esp32_service import ESP32Service

logger = get_logger(__name__)


class LedPage(QWidget):
    def __init__(self, runtime = None):
        super().__init__()
        self._build_ui()
        self.refresh_devices()

    def _build_ui(self):
        layout = QVBoxLayout()

        title = QLabel("LED Control")
        title.setStyleSheet("font-size: 18px; font-weight: bold;")
        layout.addWidget(title)

        # --- Device selector ---
        device_row = QHBoxLayout()
        device_row.addWidget(QLabel("Device:"))
        self.device_combo = QComboBox()
        device_row.addWidget(self.device_combo)
        refresh_btn = QPushButton("Refresh Devices")
        refresh_btn.clicked.connect(self.refresh_devices)
        device_row.addWidget(refresh_btn)
        device_row.addStretch()
        layout.addLayout(device_row)

        # --- Effect preset buttons ---
        layout.addWidget(QLabel("Effects:"))
        grid = QGridLayout()
        row, col = 0, 0
        for effect_name in sorted(EFFECT_PRESETS.values()):
            label = EFFECT_META.get(effect_name, {}).get("label", effect_name)
            btn = QPushButton(label)
            btn.clicked.connect(lambda checked=False, e=effect_name: self.trigger_effect(e))
            grid.addWidget(btn, row, col)
            col += 1
            if col >= 3:
                col = 0
                row += 1
        layout.addLayout(grid)

        # --- Brightness slider ---
        brightness_row = QHBoxLayout()
        brightness_row.addWidget(QLabel("Default Brightness:"))
        self.brightness_slider = QSlider(Qt.Horizontal)
        self.brightness_slider.setMinimum(0)
        self.brightness_slider.setMaximum(255)
        self.brightness_value_label = QLabel("200")
        self.brightness_slider.valueChanged.connect(
            lambda v: self.brightness_value_label.setText(str(v))
        )
        brightness_row.addWidget(self.brightness_slider)
        brightness_row.addWidget(self.brightness_value_label)
        save_brightness_btn = QPushButton("Save to led.json")
        save_brightness_btn.clicked.connect(self.save_brightness)
        brightness_row.addWidget(save_brightness_btn)
        layout.addLayout(brightness_row)

        note = QLabel(
            "Note: brightness here updates config/led.json (used as the firmware's\n"
            "default on next flash). Live brightness push requires adding a\n"
            "'brightness' field to the ESP32 /command endpoint - ask if you want that added."
        )
        note.setStyleSheet("color: gray; font-size: 11px;")
        layout.addWidget(note)

        # --- Stop effect ---
        stop_btn = QPushButton("Stop / Clear Effect")
        stop_btn.clicked.connect(lambda: self.trigger_effect("NONE"))
        layout.addWidget(stop_btn)

        layout.addStretch()
        self.setLayout(layout)

        self.load_brightness()

    def refresh_devices(self):
        session = get_session()
        try:
            devices = session.query(Device).all()
            self.device_combo.clear()
            self._device_ips = []
            for d in devices:
                self.device_combo.addItem(f"{d.device_name} ({d.ip})")
                self._device_ips.append(d.ip)
        finally:
            session.close()

    def _selected_ip(self):
        idx = self.device_combo.currentIndex()
        if idx < 0 or idx >= len(self._device_ips):
            return None
        return self._device_ips[idx]

    def trigger_effect(self, effect_name: str):
        ip = self._selected_ip()
        if not ip:
            QMessageBox.warning(self, "No device", "Add a device on the Devices tab first.")
            return

        result = ESP32Service(ip, {"effect": effect_name})
        if result is not None:
            logger.info(f"Triggered {effect_name} on {ip}")
        else:
            QMessageBox.warning(self, "Failed", f"Could not reach device at {ip}")

    def load_brightness(self):
        cfg = load_config("led")
        self.brightness_slider.setValue(cfg.get("brightness", 200))

    def save_brightness(self):
        cfg = load_config("led")
        cfg["brightness"] = self.brightness_slider.value()
        save_config("led", cfg)
        QMessageBox.information(self, "Saved", "Brightness saved to config/led.json")