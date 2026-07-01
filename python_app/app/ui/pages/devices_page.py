"""
devices_page.py
Manage ESP32 devices: list, add, test connection, send a quick effect command.
"""

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton,
    QTableWidget, QTableWidgetItem, QHeaderView, QMessageBox, QComboBox
)
from PySide6.QtCore import Qt

from app.core.database import get_session
from app.core.logger import get_logger
from app.models.device import Device
from app.services.esp32_service import send_command, get_status
from app.modules.led.presets import EFFECT_PRESETS

logger = get_logger(__name__)


class DevicesPage(QWidget):
    def __init__(self):
        super().__init__()
        self._build_ui()
        self.refresh_table()

    def _build_ui(self):
        layout = QVBoxLayout()

        title = QLabel("Devices")
        title.setStyleSheet("font-size: 18px; font-weight: bold;")
        layout.addWidget(title)

        # --- Add device form ---
        form_row = QHBoxLayout()
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Device name (e.g. SMART_SHOWROOM_FRAME_01)")
        self.ip_input = QLineEdit()
        self.ip_input.setPlaceholderText("IP address (e.g. 192.168.1.50)")
        self.location_input = QLineEdit()
        self.location_input.setPlaceholderText("Location (optional)")
        add_btn = QPushButton("Add Device")
        add_btn.clicked.connect(self.add_device)

        form_row.addWidget(self.name_input)
        form_row.addWidget(self.ip_input)
        form_row.addWidget(self.location_input)
        form_row.addWidget(add_btn)
        layout.addLayout(form_row)

        # --- Device table ---
        self.table = QTableWidget(0, 4)
        self.table.setHorizontalHeaderLabels(["Name", "IP", "Location", "Status"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setSelectionMode(QTableWidget.SingleSelection)
        layout.addWidget(self.table)

        # --- Actions for selected device ---
        action_row = QHBoxLayout()
        test_btn = QPushButton("Test Connection")
        test_btn.clicked.connect(self.test_connection)

        self.effect_combo = QComboBox()
        self.effect_combo.addItems(sorted(EFFECT_PRESETS.values()))
        send_btn = QPushButton("Send Effect")
        send_btn.clicked.connect(self.send_effect)

        refresh_btn = QPushButton("Refresh")
        refresh_btn.clicked.connect(self.refresh_table)

        action_row.addWidget(test_btn)
        action_row.addWidget(self.effect_combo)
        action_row.addWidget(send_btn)
        action_row.addStretch()
        action_row.addWidget(refresh_btn)
        layout.addLayout(action_row)

        self.setLayout(layout)

    def refresh_table(self):
        session = get_session()
        try:
            devices = session.query(Device).all()
            self.table.setRowCount(len(devices))
            self._device_ids = []
            for row, device in enumerate(devices):
                self.table.setItem(row, 0, QTableWidgetItem(device.device_name))
                self.table.setItem(row, 1, QTableWidgetItem(device.ip or ""))
                self.table.setItem(row, 2, QTableWidgetItem(device.location or ""))
                self.table.setItem(row, 3, QTableWidgetItem(device.status or "unknown"))
                self._device_ids.append(device.id)
        finally:
            session.close()

    def add_device(self):
        name = self.name_input.text().strip()
        ip = self.ip_input.text().strip()
        location = self.location_input.text().strip()

        if not name or not ip:
            QMessageBox.warning(self, "Missing info", "Device name and IP are required.")
            return

        session = get_session()
        try:
            device = Device(device_name=name, ip=ip, location=location or None, status="unknown")
            session.add(device)
            session.commit()
            logger.info(f"Added device {name} ({ip})")
        finally:
            session.close()

        self.name_input.clear()
        self.ip_input.clear()
        self.location_input.clear()
        self.refresh_table()

    def _selected_device_ip(self):
        row = self.table.currentRow()
        if row < 0:
            QMessageBox.information(self, "No selection", "Select a device row first.")
            return None, None
        device_id = self._device_ids[row]
        ip_item = self.table.item(row, 1)
        return device_id, ip_item.text() if ip_item else None

    def test_connection(self):
        device_id, ip = self._selected_device_ip()
        if not ip:
            return

        status = get_status(ip)
        new_status = "connected" if status else "disconnected"

        session = get_session()
        try:
            device = session.query(Device).filter_by(id=device_id).first()
            if device:
                device.status = new_status
                session.commit()
        finally:
            session.close()

        self.refresh_table()

        if status:
            QMessageBox.information(self, "Connected", f"Device responded: {status}")
        else:
            QMessageBox.warning(self, "No response", f"Could not reach device at {ip}")

    def send_effect(self):
        _, ip = self._selected_device_ip()
        if not ip:
            return

        effect = self.effect_combo.currentText()
        result = send_command(ip, {"effect": effect})
        if result is not None:
            QMessageBox.information(self, "Sent", f"Sent effect '{effect}' to {ip}")
        else:
            QMessageBox.warning(self, "Failed", f"Could not send command to {ip}")