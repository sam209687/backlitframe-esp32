"""
dashboard_page.py

Live mission-control dashboard for Smart Showroom AI.
Shows ESP32, voice, microphone, media, database and runtime status.
"""

from datetime import datetime

from PySide6.QtCore import QTimer, Qt
from PySide6.QtWidgets import QLabel, QHBoxLayout, QVBoxLayout

from app.core.database import get_session
from app.models.device import Device

from app.ui_comp.base import (
    BasePage,
    BaseCard,
    BaseButton,
    BaseTable,
)

from app.ui_comp.indicators import StatusIndicator


class DashboardPage(BasePage):

    def __init__(self, runtime=None):
        super().__init__(
            title="Dashboard",
            subtitle="Live showroom controller status",
        )

        self.runtime = runtime

        self.build_page()
        self.setup_timer()
        self.refresh_dashboard()

    # -------------------------------------------------
    # UI
    # -------------------------------------------------

    def build_page(self):
        refresh_btn = BaseButton(
            "Refresh",
            icon="fa5s.sync",
        )
        refresh_btn.clicked.connect(self.refresh_dashboard)

        self.add_toolbar_widget(refresh_btn)

        # ---------------- Hero Status Row ----------------

        status_row = QHBoxLayout()
        status_row.setSpacing(14)

        self.esp32_card = self.indicator_card(
            title="ESP32 Controller",
            subtitle="Network LED controller",
            status_text="Disconnected",
            status=StatusIndicator.DISCONNECTED,
        )

        self.voice_card = self.indicator_card(
            title="Voice Engine",
            subtitle="Wake word and product command",
            status_text="Idle",
            status=StatusIndicator.IDLE,
        )

        self.whisper_card = self.indicator_card(
            title="Whisper AI",
            subtitle="Speech transcription model",
            status_text="Ready",
            status=StatusIndicator.READY,
        )

        self.media_card = self.indicator_card(
            title="TV Media",
            subtitle="HDMI showroom playback",
            status_text="Idle",
            status=StatusIndicator.IDLE,
        )

        status_row.addWidget(self.esp32_card)
        status_row.addWidget(self.voice_card)
        status_row.addWidget(self.whisper_card)
        status_row.addWidget(self.media_card)

        self.add_layout(status_row)

        # ---------------- Second Status Row ----------------

        second_row = QHBoxLayout()
        second_row.setSpacing(14)

        self.mic_card = self.indicator_card(
            title="Microphone",
            subtitle="USB capture device",
            status_text="Ready",
            status=StatusIndicator.READY,
        )

        self.db_card = self.indicator_card(
            title="Database",
            subtitle="SQLite configuration storage",
            status_text="Ready",
            status=StatusIndicator.READY,
        )

        self.runtime_card = self.indicator_card(
            title="Runtime",
            subtitle="Showroom automation engine",
            status_text="Ready",
            status=StatusIndicator.READY,
        )

        self.scheduler_card = self.indicator_card(
            title="Scheduler",
            subtitle="Relay and signboard timer",
            status_text="Idle",
            status=StatusIndicator.IDLE,
        )

        second_row.addWidget(self.mic_card)
        second_row.addWidget(self.db_card)
        second_row.addWidget(self.runtime_card)
        second_row.addWidget(self.scheduler_card)

        self.add_layout(second_row)

        # ---------------- Voice Recognition ----------------

        voice_row = QHBoxLayout()
        voice_row.setSpacing(14)

        self.voice_info = BaseCard(
            "Voice Recognition",
            "Latest recognized command and matching product",
        )

        self.last_text = QLabel("Last Text : -")
        self.keyword_text = QLabel("Matched Keyword : -")
        self.product_text = QLabel("Matched Product : -")
        self.effect_text = QLabel("LED Effect : -")
        self.media_text = QLabel("Media : -")

        for label in [
            self.last_text,
            self.keyword_text,
            self.product_text,
            self.effect_text,
            self.media_text,
        ]:
            label.setWordWrap(True)
            self.voice_info.add_widget(label)

        self.device_card = BaseCard(
            "Connected ESP32",
            "Active controller discovered from network",
        )

        self.device_status_indicator = StatusIndicator(
            "Disconnected",
            StatusIndicator.DISCONNECTED,
        )

        self.device_name = QLabel("Device : -")
        self.device_ip = QLabel("IP : -")
        self.device_status = QLabel("Status : Offline")
        self.last_seen = QLabel("Last Checked : -")

        self.device_card.add_widget(self.device_status_indicator)
        self.device_card.add_widget(self.device_name)
        self.device_card.add_widget(self.device_ip)
        self.device_card.add_widget(self.device_status)
        self.device_card.add_widget(self.last_seen)

        voice_row.addWidget(self.voice_info, 2)
        voice_row.addWidget(self.device_card, 1)

        self.add_layout(voice_row)

        # ---------------- Quick Controls ----------------

        self.quick_card = BaseCard(
            "Quick Actions",
            "Common showroom actions",
        )

        quick_row = QHBoxLayout()
        quick_row.setSpacing(10)

        self.refresh_devices_btn = BaseButton(
            "Check ESP32",
            icon="fa5s.microchip",
        )
        self.refresh_devices_btn.clicked.connect(
            self.refresh_device_status
        )

        self.refresh_runtime_btn = BaseButton(
            "Check Runtime",
            icon="fa5s.server",
        )
        self.refresh_runtime_btn.clicked.connect(
            self.refresh_runtime_status
        )

        self.clear_log_btn = BaseButton(
            "Clear Log View",
            icon="fa5s.broom",
            button_type=BaseButton.SECONDARY,
        )
        self.clear_log_btn.clicked.connect(
            self.clear_logs
        )

        quick_row.addWidget(self.refresh_devices_btn)
        quick_row.addWidget(self.refresh_runtime_btn)
        quick_row.addWidget(self.clear_log_btn)
        quick_row.addStretch()

        self.quick_card.add_layout(quick_row)

        self.add_widget(self.quick_card)

        # ---------------- Runtime Log ----------------

        self.log_card = BaseCard(
            "Runtime Log",
            "Recent showroom events",
        )

        self.log_table = BaseTable()
        self.log_table.set_headers(
            [
                "Time",
                "Event",
                "Details",
            ]
        )

        self.log_card.add_widget(self.log_table)

        self.add_widget(self.log_card)

    def indicator_card(
        self,
        title,
        subtitle,
        status_text,
        status,
    ):
        card = BaseCard(
            title,
            subtitle,
        )

        indicator = StatusIndicator(
            status_text,
            status,
        )

        value = QLabel(status_text)
        value.setAlignment(Qt.AlignLeft)
        value.setStyleSheet("""
            font-size: 24px;
            font-weight: 800;
            background: transparent;
        """)

        card.indicator = indicator
        card.value_label = value

        card.add_widget(indicator)
        card.add_widget(value)

        return card

    # -------------------------------------------------
    # Timer
    # -------------------------------------------------

    def setup_timer(self):
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.refresh_dashboard)
        self.timer.start(3000)

    # -------------------------------------------------
    # Refresh
    # -------------------------------------------------

    def refresh_dashboard(self):
        self.refresh_device_status()
        self.refresh_runtime_status()
        self.refresh_logs()

    def refresh_device_status(self):
        session = get_session()

        try:
            device = (
                session.query(Device)
                .filter(Device.status == "connected")
                .first()
            )

            now = datetime.now().strftime("%H:%M:%S")

            if device:
                self.esp32_card.indicator.set_connected("Connected")
                self.esp32_card.value_label.setText("Online")

                self.device_status_indicator.set_connected("Connected")

                self.device_name.setText(
                    f"Device : {device.device_name or 'ESP32'}"
                )
                self.device_ip.setText(
                    f"IP : {device.ip or '-'}"
                )
                self.device_status.setText("Status : Connected")
                self.last_seen.setText(f"Last Checked : {now}")

            else:
                self.esp32_card.indicator.set_disconnected("Disconnected")
                self.esp32_card.value_label.setText("Offline")

                self.device_status_indicator.set_disconnected("Disconnected")

                self.device_name.setText("Device : -")
                self.device_ip.setText("IP : -")
                self.device_status.setText("Status : Offline")
                self.last_seen.setText(f"Last Checked : {now}")

            self.db_card.indicator.set_ready("Ready")
            self.db_card.value_label.setText("Ready")

        except Exception as error:
            self.db_card.indicator.set_error("Error")
            self.db_card.value_label.setText("Error")

            self.add_log(f"Database error: {error}")

        finally:
            session.close()

    def refresh_runtime_status(self):
        if not self.runtime:
            self.runtime_card.indicator.set_idle("No Runtime")
            self.runtime_card.value_label.setText("Idle")

            self.voice_card.indicator.set_idle("Idle")
            self.voice_card.value_label.setText("Idle")
            return

        runtime_state = str(
            getattr(
                self.runtime,
                "state",
                "Ready",
            )
        )

        self.runtime_card.indicator.set_ready("Ready")
        self.runtime_card.value_label.setText(runtime_state)

        monitor = getattr(
            self.runtime,
            "monitor",
            None,
        )

        if monitor:
            voice_text = getattr(
                monitor,
                "voice_text",
                "",
            )

            if voice_text:
                self.voice_card.indicator.set_listening("Detected")
                self.voice_card.value_label.setText("Active")
            else:
                self.voice_card.indicator.set_idle("Idle")
                self.voice_card.value_label.setText("Idle")

            self.last_text.setText(
                f"Last Text : {voice_text or '-'}"
            )

            product = getattr(
                monitor,
                "product",
                None,
            )

            if product:
                self.product_text.setText(
                    f"Matched Product : {getattr(product, 'name', '-')}"
                )
                self.effect_text.setText(
                    f"LED Effect : {getattr(product, 'led_effect', '-')}"
                )
                self.media_text.setText(
                    f"Media : {getattr(product, 'media_path', '-')}"
                )
            else:
                self.product_text.setText("Matched Product : -")
                self.effect_text.setText("LED Effect : -")
                self.media_text.setText("Media : -")

        current_media = None

        try:
            media_engine = getattr(
                self.runtime,
                "media_engine",
                None,
            )

            if media_engine:
                current_media = media_engine.current_media()

        except Exception:
            current_media = None

        if current_media:
            self.media_card.indicator.set_playing("Playing")
            self.media_card.value_label.setText("Playing")
        else:
            self.media_card.indicator.set_idle("Idle")
            self.media_card.value_label.setText("Idle")

    def refresh_logs(self):
        logger = getattr(
            self.runtime,
            "logger",
            None,
        ) if self.runtime else None

        if not logger:
            return

        self.log_table.clear_rows()

        for log in logger.latest(20):
            self.log_table.add_row(
                [
                    log.get("time", ""),
                    log.get("event", ""),
                    str(log.get("data", "")),
                ]
            )

    # -------------------------------------------------
    # Helpers
    # -------------------------------------------------

    def clear_logs(self):
        self.log_table.clear_rows()

    def refresh_customers(self):
        self.refresh_dashboard()

    def update_voice_status(self, status):
        self.voice_card.value_label.setText(status)

        if str(status).lower() in ["listening", "active", "detected"]:
            self.voice_card.indicator.set_listening(status)
        else:
            self.voice_card.indicator.set_idle(status)

    def update_esp32_status(self, status):
        status_text = str(status)

        self.esp32_card.value_label.setText(status_text)

        if status_text.lower() in ["online", "connected", "ready"]:
            self.esp32_card.indicator.set_connected("Connected")
        else:
            self.esp32_card.indicator.set_disconnected("Disconnected")

    def update_hdmi_status(self, status):
        status_text = str(status)

        self.media_card.value_label.setText(status_text)

        if status_text.lower() in ["playing", "online", "active"]:
            self.media_card.indicator.set_playing("Playing")
        else:
            self.media_card.indicator.set_idle(status_text)

    def update_last_product(self, product):
        self.product_text.setText(
            f"Matched Product : {product}"
        )

    def add_log(self, message):
        self.log_table.add_row(
            [
                datetime.now().strftime("%H:%M:%S"),
                "Log",
                message,
            ]
        )