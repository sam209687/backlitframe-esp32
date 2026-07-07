"""
dashboard_page.py

Live Dashboard for Smart Showroom AI.
Displays runtime information received from RuntimeMonitor.
"""

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QFrame,
    QTextEdit,
)


class DashboardPage(QWidget):

    def __init__(self, runtime = None):

        super().__init__()

        self.runtime = runtime

        self.monitor = runtime.monitor

        self.build_ui()

        self.monitor.subscribe(
            self.update_runtime
        )

        self.refresh()

    # -------------------------------------------------

    def build_ui(self):

        layout = QVBoxLayout()

        title = QLabel("Smart Showroom Dashboard")

        title.setAlignment(Qt.AlignCenter)

        title.setStyleSheet("""
            font-size:24px;
            font-weight:bold;
            padding:10px;
        """)

        layout.addWidget(title)

        # -------------------------------------------------

        status_card = QFrame()

        status_card.setFrameShape(QFrame.StyledPanel)

        status_layout = QVBoxLayout(status_card)

        self.lbl_runtime = QLabel()

        self.lbl_voice = QLabel()

        self.lbl_product = QLabel()

        self.lbl_media = QLabel()

        self.lbl_session = QLabel()

        self.lbl_error = QLabel()

        status_layout.addWidget(self.lbl_runtime)

        status_layout.addWidget(self.lbl_voice)

        status_layout.addWidget(self.lbl_product)

        status_layout.addWidget(self.lbl_media)

        status_layout.addWidget(self.lbl_session)

        status_layout.addWidget(self.lbl_error)

        layout.addWidget(status_card)

        # -------------------------------------------------

        voice_card = QFrame()

        voice_card.setFrameShape(QFrame.StyledPanel)

        voice_layout = QVBoxLayout(voice_card)

        voice_layout.addWidget(
            QLabel("Last Voice")
        )

        self.lbl_last_voice = QLabel("-")

        voice_layout.addWidget(
            self.lbl_last_voice
        )

        layout.addWidget(voice_card)

        # -------------------------------------------------

        product_card = QFrame()

        product_card.setFrameShape(QFrame.StyledPanel)

        product_layout = QVBoxLayout(product_card)

        product_layout.addWidget(
            QLabel("Current Product")
        )

        self.lbl_last_product = QLabel("-")

        product_layout.addWidget(
            self.lbl_last_product
        )

        layout.addWidget(product_card)

        # -------------------------------------------------

        log_title = QLabel("Runtime Log")

        layout.addWidget(log_title)

        self.log_box = QTextEdit()

        self.log_box.setReadOnly(True)

        self.log_box.setMinimumHeight(180)

        layout.addWidget(self.log_box)

        self.setLayout(layout)

    # -------------------------------------------------

    def refresh(self):

        self.update_runtime()

    # -------------------------------------------------

    def refresh_customers(self):

        self.refresh()

    # -------------------------------------------------

    def update_runtime(self):

        monitor = self.monitor

        self.lbl_runtime.setText(
            f"Runtime State : {monitor.state}"
        )

        self.lbl_voice.setText(
            f"Voice : {monitor.voice_text}"
        )

        if monitor.product:

            product_name = getattr(
                monitor.product,
                "product_name",
                getattr(
                    monitor.product,
                    "name",
                    "-"
                )
            )

            self.lbl_product.setText(
                f"Product : {product_name}"
            )

            self.lbl_last_product.setText(
                product_name
            )

        else:

            self.lbl_product.setText(
                "Product : -"
            )

            self.lbl_last_product.setText(
                "-"
            )

        if monitor.media:

            self.lbl_media.setText(
                f"Media : {monitor.media.media_name}"
            )

        else:

            self.lbl_media.setText(
                "Media : -"
            )

        session_product = "-"

        if self.runtime.session.product:

            session_product = getattr(
                self.runtime.session.product,
                "product_name",
                getattr(
                    self.runtime.session.product,
                    "name",
                    "-"
                )
            )

        self.lbl_session.setText(
            f"Session : {session_product}"
        )

        self.lbl_error.setText(
            f"Error : {monitor.error}"
        )

        self.lbl_last_voice.setText(
            monitor.voice_text or "-"
        )

    # -------------------------------------------------

    def update_voice_status(self, status):

        self.lbl_voice.setText(
            f"Voice : {status}"
        )

    # -------------------------------------------------

    def update_last_voice(self, text):

        self.lbl_last_voice.setText(text)

    # -------------------------------------------------

    def update_last_product(self, product):

        self.lbl_last_product.setText(product)

    # -------------------------------------------------

    def add_log(self, message):

        self.log_box.append(message)

    # -------------------------------------------------

    def clear_dashboard(self):

        self.log_box.clear()

        self.refresh()