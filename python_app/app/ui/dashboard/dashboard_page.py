"""
dashboard_page.py
Overview page: pick a customer, see/toggle their enabled features,
and see quick counts (devices, products).
"""

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QComboBox, QPushButton,
    QCheckBox, QGroupBox, QMessageBox, QLineEdit, QFormLayout
)

from app.core.database import get_session
from app.core.logger import get_logger
from app.models.customer import Customer
from app.models.device import Device
from app.models.product import Product
from app.models.feature import Feature
from app.core.feature_manager import set_feature, enabled_features

logger = get_logger(__name__)


class DashboardPage(QWidget):
    def __init__(self):
        super().__init__()
        self._build_ui()
        self.refresh_customers()

    def _build_ui(self):
        layout = QVBoxLayout()

        title = QLabel("Dashboard")
        title.setStyleSheet("font-size: 18px; font-weight: bold;")
        layout.addWidget(title)

        # --- Add customer form ---
        add_box = QGroupBox("Add Customer")
        form = QFormLayout()
        self.shop_name_input = QLineEdit()
        self.owner_input = QLineEdit()
        self.plan_input = QComboBox()
        self.plan_input.addItems(["basic", "premium"])
        form.addRow("Shop name:", self.shop_name_input)
        form.addRow("Owner:", self.owner_input)
        form.addRow("Plan:", self.plan_input)
        add_customer_btn = QPushButton("Add Customer")
        add_customer_btn.clicked.connect(self.add_customer)
        form.addRow(add_customer_btn)
        add_box.setLayout(form)
        layout.addWidget(add_box)

        # --- Customer selector ---
        selector_row = QHBoxLayout()
        selector_row.addWidget(QLabel("Customer:"))
        self.customer_combo = QComboBox()
        self.customer_combo.currentIndexChanged.connect(self.load_features)
        selector_row.addWidget(self.customer_combo)
        selector_row.addStretch()
        layout.addLayout(selector_row)

        # --- Feature toggles ---
        self.feature_box = QGroupBox("Enabled Features")
        self.feature_layout = QVBoxLayout()
        self.feature_box.setLayout(self.feature_layout)
        layout.addWidget(self.feature_box)

        save_btn = QPushButton("Save Feature Changes")
        save_btn.clicked.connect(self.save_features)
        layout.addWidget(save_btn)

        # --- Quick stats ---
        self.stats_label = QLabel("")
        layout.addWidget(self.stats_label)

        layout.addStretch()
        self.setLayout(layout)
        self._feature_checkboxes = {}

    def refresh_customers(self):
        session = get_session()
        try:
            customers = session.query(Customer).all()
            self.customer_combo.blockSignals(True)
            self.customer_combo.clear()
            self._customer_ids = []
            for c in customers:
                self.customer_combo.addItem(f"{c.shop_name} ({c.plan})")
                self._customer_ids.append(c.id)
            self.customer_combo.blockSignals(False)
        finally:
            session.close()

        self.load_features()
        self.load_stats()

    def add_customer(self):
        shop_name = self.shop_name_input.text().strip()
        owner = self.owner_input.text().strip()
        plan = self.plan_input.currentText()

        if not shop_name:
            QMessageBox.warning(self, "Missing info", "Shop name is required.")
            return

        session = get_session()
        try:
            customer = Customer(shop_name=shop_name, owner=owner or None, plan=plan)
            session.add(customer)
            session.commit()
            logger.info(f"Added customer {shop_name} ({plan})")
        finally:
            session.close()

        self.shop_name_input.clear()
        self.owner_input.clear()
        self.refresh_customers()

    def _current_customer_id(self):
        idx = self.customer_combo.currentIndex()
        if idx < 0 or idx >= len(getattr(self, "_customer_ids", [])):
            return None
        return self._customer_ids[idx]

    def load_features(self):
        # clear existing checkboxes
        while self.feature_layout.count():
            item = self.feature_layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()
        self._feature_checkboxes = {}

        customer_id = self._current_customer_id()
        if customer_id is None:
            self.feature_layout.addWidget(QLabel("No customer selected."))
            return

        session = get_session()
        try:
            all_features = [f.name for f in session.query(Feature).all()]
        finally:
            session.close()

        active = set(enabled_features(customer_id))

        for name in all_features:
            cb = QCheckBox(name)
            cb.setChecked(name in active)
            self.feature_layout.addWidget(cb)
            self._feature_checkboxes[name] = cb

    def save_features(self):
        customer_id = self._current_customer_id()
        if customer_id is None:
            QMessageBox.warning(self, "No customer", "Select or add a customer first.")
            return

        for name, cb in self._feature_checkboxes.items():
            set_feature(customer_id, name, cb.isChecked())

        QMessageBox.information(self, "Saved", "Feature settings updated.")
        self.load_features()

    def load_stats(self):
        session = get_session()
        try:
            device_count = session.query(Device).count()
            product_count = session.query(Product).count()
            customer_count = session.query(Customer).count()
        finally:
            session.close()

        self.stats_label.setText(
            f"Customers: {customer_count}   |   Devices: {device_count}   |   Products: {product_count}"
        )