"""
devices_page.py

Shows discovered ESP32 devices
"""


from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QTableWidget,
    QTableWidgetItem,
    QPushButton
)


from PySide6.QtCore import QTimer


from app.core.database import get_session
from app.models.device import Device



class DevicesPage(QWidget):


    def __init__(self):

        super().__init__()


        self.build_ui()


        self.timer = QTimer()


        self.timer.timeout.connect(
            self.refresh_table
        )


        self.timer.start(
            3000
        )


        self.refresh_table()




    def build_ui(self):

        layout = QVBoxLayout()


        title = QLabel(
            "ESP32 Devices"
        )


        title.setStyleSheet(
            "font-size:18px;font-weight:bold;"
        )


        layout.addWidget(
            title
        )



        refresh_btn = QPushButton(
            "Refresh"
        )


        refresh_btn.clicked.connect(
            self.refresh_table
        )


        layout.addWidget(
            refresh_btn
        )



        self.table = QTableWidget()


        self.table.setColumnCount(
            4
        )


        self.table.setHorizontalHeaderLabels(
            [
                "ID",
                "Device Name",
                "IP Address",
                "Status"
            ]
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


            devices = session.query(
                Device
            ).all()



            self.table.setRowCount(
                len(devices)
            )



            for row,d in enumerate(devices):


                self.table.setItem(
                    row,
                    0,
                    QTableWidgetItem(
                        str(d.id)
                    )
                )


                self.table.setItem(
                    row,
                    1,
                    QTableWidgetItem(
                        d.device_name
                    )
                )


                self.table.setItem(
                    row,
                    2,
                    QTableWidgetItem(
                        d.ip or ""
                    )
                )


                self.table.setItem(
                    row,
                    3,
                    QTableWidgetItem(
                        d.status
                    )
                )


        finally:

            session.close()