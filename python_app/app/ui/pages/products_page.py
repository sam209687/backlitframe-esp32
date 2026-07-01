"""
products_page.py
Manage products: name, voice keywords, LED effect, media folder path.
"""

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton,
    QTableWidget, QTableWidgetItem, QHeaderView, QMessageBox, QComboBox
)

from app.core.database import get_session
from app.core.logger import get_logger
from app.models.product import Product
from app.modules.led.presets import EFFECT_PRESETS

logger = get_logger(__name__)


class ProductsPage(QWidget):
    def __init__(self):
        super().__init__()
        self._build_ui()
        self.refresh_table()

    def _build_ui(self):
        layout = QVBoxLayout()

        title = QLabel("Products")
        title.setStyleSheet("font-size: 18px; font-weight: bold;")
        layout.addWidget(title)

        # --- Add product form ---
        form_row = QHBoxLayout()
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Product name (e.g. sesame)")

        self.keywords_input = QLineEdit()
        self.keywords_input.setPlaceholderText("Voice keywords, comma separated (sesame,gingelly,nallennai)")

        self.effect_combo = QComboBox()
        self.effect_combo.addItems(sorted(EFFECT_PRESETS.values()))

        self.media_input = QLineEdit()
        self.media_input.setPlaceholderText("Media path (e.g. media/sesame)")

        add_btn = QPushButton("Add Product")
        add_btn.clicked.connect(self.add_product)

        form_row.addWidget(self.name_input)
        form_row.addWidget(self.keywords_input)
        form_row.addWidget(self.effect_combo)
        form_row.addWidget(self.media_input)
        form_row.addWidget(add_btn)
        layout.addLayout(form_row)

        # --- Product table ---
        self.table = QTableWidget(0, 4)
        self.table.setHorizontalHeaderLabels(["Name", "Voice Keywords", "LED Effect", "Media Path"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setSelectionMode(QTableWidget.SingleSelection)
        layout.addWidget(self.table)

        # --- Actions ---
        action_row = QHBoxLayout()
        delete_btn = QPushButton("Delete Selected")
        delete_btn.clicked.connect(self.delete_selected)
        refresh_btn = QPushButton("Refresh")
        refresh_btn.clicked.connect(self.refresh_table)
        action_row.addWidget(delete_btn)
        action_row.addStretch()
        action_row.addWidget(refresh_btn)
        layout.addLayout(action_row)

        self.setLayout(layout)

    def refresh_table(self):
        session = get_session()
        try:
            products = session.query(Product).all()
            self.table.setRowCount(len(products))
            self._product_ids = []
            for row, product in enumerate(products):
                self.table.setItem(row, 0, QTableWidgetItem(product.name))
                self.table.setItem(row, 1, QTableWidgetItem(product.voice_keywords or ""))
                self.table.setItem(row, 2, QTableWidgetItem(product.led_effect or ""))
                self.table.setItem(row, 3, QTableWidgetItem(product.media_path or ""))
                self._product_ids.append(product.id)
        finally:
            session.close()

    def add_product(self):
        name = self.name_input.text().strip()
        keywords = self.keywords_input.text().strip()
        effect = self.effect_combo.currentText()
        media_path = self.media_input.text().strip() or f"media/{name}"

        if not name:
            QMessageBox.warning(self, "Missing info", "Product name is required.")
            return

        session = get_session()
        try:
            product = Product(
                name=name,
                voice_keywords=keywords,
                led_effect=effect,
                media_path=media_path,
            )
            session.add(product)
            session.commit()
            logger.info(f"Added product {name}")
        finally:
            session.close()

        self.name_input.clear()
        self.keywords_input.clear()
        self.media_input.clear()
        self.refresh_table()

    def delete_selected(self):
        row = self.table.currentRow()
        if row < 0:
            QMessageBox.information(self, "No selection", "Select a product row first.")
            return

        product_id = self._product_ids[row]
        session = get_session()
        try:
            product = session.query(Product).filter_by(id=product_id).first()
            if product:
                session.delete(product)
                session.commit()
                logger.info(f"Deleted product id={product_id}")
        finally:
            session.close()

        self.refresh_table()