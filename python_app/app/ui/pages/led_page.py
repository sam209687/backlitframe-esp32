"""
led_page.py

LED control page.
"""

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QComboBox,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QMessageBox,
    QSlider,
    QVBoxLayout,
)

from app.core.database import get_session
from app.core.logger import get_logger
from app.core.config_manager import load as load_config, save as save_config
from app.models.device import Device
from app.modules.led.presets import EFFECT_PRESETS
from app.modules.led.effects import EFFECT_META
from app.services.esp32_service import ESP32Service

from app.ui_comp.base import (
    BasePage,
    BaseCard,
    BaseButton,
)

logger = get_logger(__name__)


class LedPage(BasePage):

    def __init__(self, runtime=None):

        super().__init__(
            title="LED Control",
            subtitle="Trigger ESP32 LED effects and manage default brightness"
        )

        self.runtime = runtime
        self._device_ips = []

        self.build_page()
        self.refresh_devices()
        self.load_brightness()

    def build_page(self):

        refresh_btn = BaseButton(
            "Refresh Devices",
            icon="fa5s.sync"
        )
        refresh_btn.clicked.connect(self.refresh_devices)

        self.add_toolbar_widget(refresh_btn)

        # Device card

        device_card = BaseCard(
            "ESP32 Device",
            "Select the ESP32 device to send LED commands"
        )

        row = QHBoxLayout()

        row.addWidget(QLabel("Device"))

        self.device_combo = QComboBox()

        row.addWidget(self.device_combo, 1)

        device_card.add_layout(row)

        self.add_widget(device_card)

        # Effects card

        effects_card = BaseCard(
            "LED Effects",
            "Click an effect to test it live on ESP32"
        )

        grid = QGridLayout()
        grid.setSpacing(10)

        row = 0
        col = 0

        effects = sorted(set(EFFECT_PRESETS.values()))

        for effect_name in effects:

            label = EFFECT_META.get(
                effect_name,
                {}
            ).get(
                "label",
                effect_name
            )

            btn = BaseButton(label)

            btn.clicked.connect(
                lambda checked=False, effect=effect_name:
                self.trigger_effect(effect)
            )

            grid.addWidget(btn, row, col)

            col += 1

            if col >= 3:
                col = 0
                row += 1

        effects_card.add_layout(grid)

        stop_btn = BaseButton(
            "Stop / Clear Effect",
            button_type=BaseButton.DANGER
        )
        stop_btn.clicked.connect(
            lambda: self.trigger_effect("NONE")
        )

        effects_card.add_widget(stop_btn)

        self.add_widget(effects_card)

        # Brightness card

        brightness_card = BaseCard(
            "Default Brightness",
            "Saved to config/led.json"
        )

        brightness_row = QHBoxLayout()

        self.brightness_slider = QSlider(Qt.Horizontal)
        self.brightness_slider.setMinimum(0)
        self.brightness_slider.setMaximum(255)

        self.brightness_value_label = QLabel("200")
        self.brightness_value_label.setMinimumWidth(50)
        self.brightness_value_label.setAlignment(Qt.AlignCenter)

        self.brightness_slider.valueChanged.connect(
            lambda value:
            self.brightness_value_label.setText(str(value))
        )

        save_btn = BaseButton(
            "Save",
            icon="fa5s.save"
        )
        save_btn.clicked.connect(self.save_brightness)

        brightness_row.addWidget(self.brightness_slider, 1)
        brightness_row.addWidget(self.brightness_value_label)
        brightness_row.addWidget(save_btn)

        brightness_card.add_layout(brightness_row)

        note = QLabel(
            "Live brightness needs ESP32 firmware support. "
            "This saves the default value only."
        )
        note.setWordWrap(True)

        brightness_card.add_widget(note)

        self.add_widget(brightness_card)

    def refresh_devices(self):

        session = get_session()

        try:
            devices = (
                session.query(Device)
                .order_by(Device.id.asc())
                .all()
            )

            self.device_combo.clear()
            self._device_ips.clear()

            for device in devices:

                ip = device.ip or ""

                label = f"{device.device_name or 'ESP32'} ({ip})"

                if getattr(device, "status", "") == "connected":
                    label += " ✓"

                self.device_combo.addItem(label)
                self._device_ips.append(ip)

        finally:
            session.close()

    def selected_ip(self):

        index = self.device_combo.currentIndex()

        if index < 0:
            return None

        if index >= len(self._device_ips):
            return None

        return self._device_ips[index]

    def trigger_effect(self, effect_name):

        ip = self.selected_ip()

        if not ip:

            QMessageBox.warning(
                self,
                "No ESP32",
                "No ESP32 device selected."
            )
            return

        ok = ESP32Service.send_effect(
            effect_name,
            ip
        )

        if ok:

            logger.info(
                f"Triggered {effect_name} on {ip}"
            )

        else:

            QMessageBox.warning(
                self,
                "Failed",
                f"Could not send effect to {ip}"
            )

    def load_brightness(self):

        cfg = load_config("led")

        value = cfg.get("brightness", 200)

        self.brightness_slider.setValue(value)

        self.brightness_value_label.setText(
            str(value)
        )

    def save_brightness(self):

        cfg = load_config("led")

        cfg["brightness"] = self.brightness_slider.value()

        save_config("led", cfg)

        QMessageBox.information(
            self,
            "Saved",
            "Brightness saved to config/led.json"
        )