from PySide6.QtWidgets import QApplication

from app.showroom.showroom_runtime import ShowroomRuntime
from app.services.product_service import ProductService

app = QApplication([])

runtime = ShowroomRuntime()

product = ProductService.get_by_id(1)

runtime.media.show_product(product)

runtime.media.video_widget().show()

app.exec()