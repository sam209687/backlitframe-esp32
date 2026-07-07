"""
products_page.py

Product CRUD UI

Add:
- name
- voice keywords
- LED effect
- media path

Edit/Delete products
"""

from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QMessageBox,
    QComboBox
)


from app.core.database import get_session
from app.models.product import Product


LED_EFFECTS = [
    "NONE",
    "SESAME",
    "GROUNDNUT",
    "MUSTARD",
    "COCONUT"
]



class ProductsPage(QWidget):

    def __init__(self, runtime = None):

        super().__init__()

        self.selected_id = None

        self.build_ui()

        self.refresh_table()



    def build_ui(self):

        layout = QVBoxLayout()


        title = QLabel(
            "Products Management"
        )

        title.setStyleSheet(
            "font-size:18px;font-weight:bold"
        )

        layout.addWidget(title)



        # Inputs

        self.name_input = QLineEdit()

        self.keyword_input = QLineEdit()

        self.media_input = QLineEdit()


        self.effect_combo = QComboBox()

        self.effect_combo.addItems(
            LED_EFFECTS
        )



        layout.addWidget(
            QLabel("Product Name")
        )

        layout.addWidget(
            self.name_input
        )



        layout.addWidget(
            QLabel("Voice Keywords (comma separated)")
        )

        layout.addWidget(
            self.keyword_input
        )



        layout.addWidget(
            QLabel("LED Effect")
        )

        layout.addWidget(
            self.effect_combo
        )



        layout.addWidget(
            QLabel("Media Path")
        )

        layout.addWidget(
            self.media_input
        )



        # Buttons

        btn_row = QHBoxLayout()


        save_btn = QPushButton(
            "Save Product"
        )

        save_btn.clicked.connect(
            self.save_product
        )



        delete_btn = QPushButton(
            "Delete Selected"
        )

        delete_btn.clicked.connect(
            self.delete_product
        )


        clear_btn = QPushButton(
            "Clear"
        )

        clear_btn.clicked.connect(
            self.clear_form
        )



        btn_row.addWidget(save_btn)

        btn_row.addWidget(delete_btn)

        btn_row.addWidget(clear_btn)


        layout.addLayout(
            btn_row
        )



        # Table


        self.table = QTableWidget()

        self.table.setColumnCount(5)


        self.table.setHorizontalHeaderLabels(
            [
                "ID",
                "Name",
                "Keywords",
                "LED",
                "Media"
            ]
        )


        self.table.cellClicked.connect(
            self.load_selected
        )


        layout.addWidget(
            self.table
        )



        self.setLayout(
            layout
        )




    def refresh_table(self):

        session = get_session()


        try:

            products = session.query(
                Product
            ).all()


            self.table.setRowCount(
                len(products)
            )


            for row,p in enumerate(products):

                self.table.setItem(
                    row,0,
                    QTableWidgetItem(str(p.id))
                )


                self.table.setItem(
                    row,1,
                    QTableWidgetItem(p.name)
                )


                self.table.setItem(
                    row,2,
                    QTableWidgetItem(
                        p.voice_keywords or ""
                    )
                )


                self.table.setItem(
                    row,3,
                    QTableWidgetItem(
                        p.led_effect or ""
                    )
                )


                self.table.setItem(
                    row,4,
                    QTableWidgetItem(
                        p.media_path or ""
                    )
                )


        finally:

            session.close()




    def save_product(self):

        session = get_session()


        try:

            if self.selected_id:


                product = session.query(
                    Product
                ).get(
                    self.selected_id
                )


            else:

                product = Product()

                session.add(
                    product
                )



            product.name = (
                self.name_input.text()
            )


            product.voice_keywords = (
                self.keyword_input.text()
            )


            product.led_effect = (
                self.effect_combo.currentText()
            )


            product.media_path = (
                self.media_input.text()
            )



            session.commit()


        finally:

            session.close()



        self.clear_form()

        self.refresh_table()




    def load_selected(self,row,column):

        self.selected_id = int(
            self.table.item(row,0).text()
        )


        self.name_input.setText(
            self.table.item(row,1).text()
        )


        self.keyword_input.setText(
            self.table.item(row,2).text()
        )


        self.effect_combo.setCurrentText(
            self.table.item(row,3).text()
        )


        self.media_input.setText(
            self.table.item(row,4).text()
        )




    def delete_product(self):

        if not self.selected_id:

            QMessageBox.warning(
                self,
                "Select",
                "Select a product first"
            )

            return



        session = get_session()


        try:

            product = session.query(
                Product
            ).get(
                self.selected_id
            )


            session.delete(
                product
            )


            session.commit()


        finally:

            session.close()



        self.clear_form()

        self.refresh_table()




    def clear_form(self):

        self.selected_id = None

        self.name_input.clear()

        self.keyword_input.clear()

        self.media_input.clear()

        self.effect_combo.setCurrentIndex(0)