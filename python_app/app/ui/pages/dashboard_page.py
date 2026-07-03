"""
dashboard_page.py

Main dashboard page for Smart Showroom AI.
This page displays the current showroom status and will be updated
live by other services (Voice Engine, ESP32, HDMI Player, etc.).
"""

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QFrame,
    QTextEdit,
)


class DashboardPage(QWidget):

    def __init__(self):
        super().__init__()

        self.build_ui()

        self.refresh()

    # --------------------------------------------------------
    # UI
    # --------------------------------------------------------

    def build_ui(self):

        main_layout = QVBoxLayout()
        main_layout.setSpacing(15)

        title = QLabel("Smart Showroom Dashboard")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("""
            font-size:22px;
            font-weight:bold;
            padding:10px;
        """)

        main_layout.addWidget(title)

        # ---------------- Status Card ----------------

        card = QFrame()
        card.setFrameShape(QFrame.StyledPanel)

        card_layout = QVBoxLayout(card)

        self.lbl_esp32 = QLabel()
        self.lbl_voice = QLabel()
        self.lbl_hdmi = QLabel()
        self.lbl_customer = QLabel()
        self.lbl_timer = QLabel()

        card_layout.addWidget(self.lbl_esp32)
        card_layout.addWidget(self.lbl_voice)
        card_layout.addWidget(self.lbl_hdmi)
        card_layout.addWidget(self.lbl_customer)
        card_layout.addWidget(self.lbl_timer)

        main_layout.addWidget(card)

        # ---------------- Last Voice ----------------

        voice_card = QFrame()
        voice_card.setFrameShape(QFrame.StyledPanel)

        voice_layout = QVBoxLayout(voice_card)

        voice_title = QLabel("Last Voice Command")

        self.lbl_last_voice = QLabel("-")

        voice_layout.addWidget(voice_title)
        voice_layout.addWidget(self.lbl_last_voice)

        main_layout.addWidget(voice_card)

        # ---------------- Last Product ----------------

        product_card = QFrame()
        product_card.setFrameShape(QFrame.StyledPanel)

        product_layout = QVBoxLayout(product_card)

        product_title = QLabel("Last Product")

        self.lbl_last_product = QLabel("-")

        product_layout.addWidget(product_title)
        product_layout.addWidget(self.lbl_last_product)

        main_layout.addWidget(product_card)

        # ---------------- Logs ----------------

        log_title = QLabel("System Log")

        self.log_box = QTextEdit()
        self.log_box.setReadOnly(True)
        self.log_box.setMinimumHeight(180)

        main_layout.addWidget(log_title)
        main_layout.addWidget(self.log_box)

        self.setLayout(main_layout)

    # --------------------------------------------------------
    # Refresh
    # --------------------------------------------------------

    def refresh(self):
        """
        Refresh all dashboard values.
        Later these values will come from services/database.
        """

        self.lbl_esp32.setText("ESP32 Status : Connected")

        self.lbl_voice.setText("Voice Engine : Idle")

        self.lbl_hdmi.setText("HDMI Display : Waiting")

        self.lbl_customer.setText("Current Customer : None")

        self.lbl_timer.setText("Welcome Timeout : 10 sec")

    # --------------------------------------------------------
    # Compatibility
    # --------------------------------------------------------

    def refresh_customers(self):
        """
        Temporary compatibility function.

        Existing MainWindow calls this method.
        Internally it simply refreshes the dashboard.
        """

        self.refresh()

    # --------------------------------------------------------
    # Update Methods
    # --------------------------------------------------------

    def update_voice_status(self, status):

        self.lbl_voice.setText(f"Voice Engine : {status}")

    def update_esp32_status(self, status):

        self.lbl_esp32.setText(f"ESP32 Status : {status}")

    def update_hdmi_status(self, status):

        self.lbl_hdmi.setText(f"HDMI Display : {status}")

    def update_customer(self, customer):

        self.lbl_customer.setText(
            f"Current Customer : {customer}"
        )

    def update_last_voice(self, text):

        self.lbl_last_voice.setText(text)

    def update_last_product(self, product):

        self.lbl_last_product.setText(product)

    def add_log(self, message):

        self.log_box.append(message)

    # --------------------------------------------------------
    # Reset
    # --------------------------------------------------------

    def clear_dashboard(self):

        self.lbl_last_voice.setText("-")

        self.lbl_last_product.setText("-")

        self.log_box.clear()

        self.refresh()