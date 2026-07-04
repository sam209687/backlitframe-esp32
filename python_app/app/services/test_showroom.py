from PySide6.QtWidgets import QApplication

from app.ui.showroom_window import ShowroomWindow
from app.services.product_service import ProductService

app = QApplication([])

window = ShowroomWindow()

window.show()

product = ProductService.get_by_id(1)

window.show_product(product)

app.exec()