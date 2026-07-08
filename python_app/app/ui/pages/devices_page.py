"""
devices_page.py

ESP32 Devices page using ui_comp.
Shows discovered devices and live status.
"""

from PySide6.QtCore import QTimer, Qt
from PySide6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QMessageBox,
)

from app.core.database import get_session
from app.models.device import Device
from app.services.esp32_service import ESP32Service

from app.ui_comp.base import (
    BasePage,
    BaseCard,
    BaseButton,
    BaseTable,
)


class DevicesPage(BasePage):

    def __init__(self, runtime=None):

        super().__init__(
            title="ESP32 Devices",
            subtitle="Discovered showroom controllers and relay devices"
        )

        self.runtime = runtime

        self.build_page()
        self.setup_timer()
        self.refresh_table()

    # -------------------------------------------------

    def build_page(self):

        refresh_btn = BaseButton(
            "Refresh",
            icon="fa5s.sync"
        )
        refresh_btn.clicked.connect(self.refresh_table)

        ping_btn = BaseButton(
            "Ping Selected",
            icon="fa5s.wifi",
            button_type=BaseButton.SECONDARY
        )
        ping_btn.clicked.connect(self.ping_selected)

        test_btn = BaseButton(
            "Test LED",
            icon="fa5s.lightbulb"
        )
        test_btn.clicked.connect(self.test_led)

        self.add_toolbar_widget(refresh_btn)
        self.add_toolbar_widget(ping_btn)
        self.add_toolbar_widget(test_btn)

        # ---------------- Summary Cards ----------------

        row = QHBoxLayout()

        self.total_card = self.status_card("Devices", "0")
        self.online_card = self.status_card("Online", "0")
        self.ip_card = self.status_card("Active IP", "-")
        self.relay_card = self.status_card("Relay", "Ready")

        row.addWidget(self.total_card)
        row.addWidget(self.online_card)
        row.addWidget(self.ip_card)
        row.addWidget(self.relay_card)

        self.add_layout(row)

        # ---------------- Device Table ----------------

        card = BaseCard(
            "Device List",
            "ESP32 devices discovered from the network"
        )

        self.table = BaseTable()
        self.table.set_headers([
            "ID",
            "Device Name",
            "IP Address",
            "Status",
            "Last Seen",
        ])

        card.add_widget(self.table)

        self.add_widget(card)

    # -------------------------------------------------

    def status_card(self, title, value):

        card = BaseCard(title)

        label = QLabel(value)
        label.setAlignment(Qt.AlignLeft)

        label.setStyleSheet(
            f"""
            font-size:26px;
            font-weight:700;
            color:{self.theme.primary};
            background:transparent;
            """
        )

        card.value_label = label
        card.add_widget(label)

        return card

    # -------------------------------------------------

    def setup_timer(self):

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.refresh_table)
        self.timer.start(3000)

    # -------------------------------------------------

    def refresh_table(self):

        session = get_session()

        try:

            devices = (
                session.query(Device)
                .order_by(Device.id.asc())
                .all()
            )

            self.table.clear_rows()

            online = 0
            active_ip = "-"

            for device in devices:

                status = device.status or "Unknown"

                if status.lower() == "connected":
                    online += 1
                    active_ip = device.ip or "-"

                self.table.add_row([
                    device.id,
                    device.device_name or "ESP32",
                    device.ip or "",
                    status,
                    getattr(device, "last_seen", "") or "-",
                ])

            self.total_card.value_label.setText(str(len(devices)))
            self.online_card.value_label.setText(str(online))
            self.ip_card.value_label.setText(active_ip)

        finally:

            session.close()

    # -------------------------------------------------

    def selected_ip(self):

        row = self.table.currentRow()

        if row < 0:
            return None

        item = self.table.item(row, 2)

        if not item:
            return None

        return item.text().strip()

    # -------------------------------------------------

    def ping_selected(self):

        ip = self.selected_ip()

        if not ip:

            QMessageBox.warning(
                self,
                "No Device",
                "Select a device first."
            )
            return

        ok = ESP32Service.send_effect(
            "PING",
            ip
        )

        QMessageBox.information(
            self,
            "Ping",
            "Ping sent successfully." if ok else "Ping failed."
        )

    # -------------------------------------------------

    def test_led(self):

        ip = self.selected_ip()

        if not ip:

            QMessageBox.warning(
                self,
                "No Device",
                "Select a device first."
            )
            return

        ok = ESP32Service.send_effect(
            "RAINBOW",
            ip
        )

        QMessageBox.information(
            self,
            "LED Test",
            "LED test sent." if ok else "LED test failed."
        )