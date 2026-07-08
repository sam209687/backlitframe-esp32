import os

from PySide6.QtWidgets import (
    QHBoxLayout,
    QMessageBox,
    QFileDialog,
)

from app.ui_comp.base import (
    BasePage,
    BaseCard,
    BaseButton,
    BaseLineEdit,
    BaseComboBox,
    BaseTable,
)

from app.services.product_service import ProductService
from app.modules.led.presets import EFFECT_PRESETS
from app.modules.led.effects import EFFECT_META


class ProductsPage(BasePage):

    def __init__(self, runtime=None):
        super().__init__(
            title="Products",
            subtitle="Manage product keywords, LED effects and media folder",
        )

        self.runtime = runtime
        self.selected_id = None

        self.build_page()
        self.load_effects()
        self.refresh_table()

    def build_page(self):
        self.new_btn = BaseButton(
            "New",
            icon="fa5s.plus",
            button_type=BaseButton.SECONDARY,
        )
        self.new_btn.clicked.connect(self.clear_form)

        self.refresh_btn = BaseButton(
            "Refresh",
            icon="fa5s.sync",
        )
        self.refresh_btn.clicked.connect(self.refresh_table)

        self.add_toolbar_widget(self.new_btn)
        self.add_toolbar_widget(self.refresh_btn)

        self.form_card = BaseCard(
            "Product Details",
            "Add or edit showroom product configuration",
        )

        self.name_input = BaseLineEdit(
            label="Product Name",
            placeholder="Sesame Premium",
            icon="fa5s.box",
        )

        self.keywords_input = BaseLineEdit(
            label="Voice Keywords",
            placeholder="sesame, gingelly, nallennai",
            icon="fa5s.microphone",
        )

        self.effect_combo = BaseComboBox(
            label="LED Effect",
            placeholder="Select LED effect",
            icon="fa5s.lightbulb",
        )

        self.media_input = BaseLineEdit(
            label="Media Folder",
            placeholder="media/sesame",
            icon="fa5s.folder",
        )

        browse_btn = BaseButton(
            "Browse Media Folder",
            icon="fa5s.folder-open",
            button_type=BaseButton.SECONDARY,
        )
        browse_btn.clicked.connect(self.browse_media_folder)

        self.form_card.add_widget(self.name_input)
        self.form_card.add_widget(self.keywords_input)
        self.form_card.add_widget(self.effect_combo)
        self.form_card.add_widget(self.media_input)
        self.form_card.add_widget(browse_btn)

        btn_row = QHBoxLayout()

        self.save_btn = BaseButton(
            "Save Product",
            icon="fa5s.save",
        )
        self.save_btn.clicked.connect(self.save_product)

        self.delete_btn = BaseButton(
            "Delete",
            icon="fa5s.trash",
            button_type=BaseButton.DANGER,
        )
        self.delete_btn.clicked.connect(self.delete_product)

        btn_row.addWidget(self.save_btn)
        btn_row.addWidget(self.delete_btn)
        btn_row.addStretch()

        self.form_card.add_layout(btn_row)
        self.add_widget(self.form_card)

        self.table_card = BaseCard(
            "Product List",
            "Click a row to edit",
        )

        self.table = BaseTable()
        self.table.set_headers(
            [
                "ID",
                "Name",
                "Keywords",
                "LED Effect",
                "Media Path",
            ]
        )

        self.table.cellClicked.connect(self.load_selected_row)

        self.table_card.add_widget(self.table)
        self.add_widget(self.table_card)

    def load_effects(self):
        self.effect_combo.clear()

        effects = ["NONE"]

        for effect in sorted(set(EFFECT_PRESETS.values())):
            if effect and effect not in effects:
                effects.append(effect)

        for effect in sorted(EFFECT_META.keys()):
            if effect and effect not in effects:
                effects.append(effect)

        for effect_code in effects:
            if effect_code == "NONE":
                label = "None"
            else:
                label = EFFECT_META.get(
                    effect_code,
                    {},
                ).get(
                    "label",
                    effect_code.replace("_", " ").title(),
                )

            self.effect_combo.add_item(label, effect_code)

        print("LED effects loaded:", effects)

    def browse_media_folder(self):
        folder = QFileDialog.getExistingDirectory(
            self,
            "Select Media Folder",
            os.getcwd(),
        )

        if folder:
            self.media_input.setText(folder)

    def refresh_table(self):
        self.table.clear_rows()

        for product in ProductService.get_all():
            self.table.add_row(
                [
                    product.id,
                    product.name,
                    product.voice_keywords or "",
                    product.led_effect or "",
                    product.media_path or "",
                ]
            )

    def load_selected_row(self, row, column):
        self.selected_id = int(self.table.item(row, 0).text())

        self.name_input.setText(self.table.item(row, 1).text())
        self.keywords_input.setText(self.table.item(row, 2).text())
        self.media_input.setText(self.table.item(row, 4).text())

        effect_code = self.table.item(row, 3).text()
        self.set_effect_value(effect_code)

    def set_effect_value(self, effect_code):
        for index in range(self.effect_combo.combo.count()):
            if self.effect_combo.combo.itemData(index) == effect_code:
                self.effect_combo.set_current_index(index)
                return

        if self.effect_combo.combo.count() > 0:
            self.effect_combo.set_current_index(0)

    def selected_effect(self):
        data = self.effect_combo.current_data()

        if data:
            return str(data)

        return self.effect_combo.current_text().strip()

    def save_product(self):
        name = self.name_input.text().strip()

        if not name:
            QMessageBox.warning(
                self,
                "Missing Name",
                "Product name is required.",
            )
            return

        if self.selected_id:
            product = ProductService.get_by_id(self.selected_id)

            if not product:
                QMessageBox.warning(
                    self,
                    "Not Found",
                    "Selected product no longer exists.",
                )
                return

            product.name = name
            product.voice_keywords = self.keywords_input.text().strip()
            product.led_effect = self.selected_effect()
            product.media_path = self.media_input.text().strip()

            ProductService.update(product)

        else:
            ProductService.create(
                name=name,
                voice_keywords=self.keywords_input.text().strip(),
                led_effect=self.selected_effect(),
                media_path=self.media_input.text().strip(),
            )

        self.clear_form()
        self.refresh_table()

    def delete_product(self):
        if not self.selected_id:
            QMessageBox.warning(
                self,
                "No Product",
                "Select a product to delete.",
            )
            return

        confirm = QMessageBox.question(
            self,
            "Delete Product",
            "Delete selected product?",
        )

        if confirm == QMessageBox.Yes:
            ProductService.delete(self.selected_id)
            self.clear_form()
            self.refresh_table()

    def clear_form(self):
        self.selected_id = None

        self.name_input.clear()
        self.keywords_input.clear()
        self.media_input.clear()

        if self.effect_combo.combo.count() > 0:
            self.effect_combo.set_current_index(0)