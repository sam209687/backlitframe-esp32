from PySide6.QtWidgets import QMainWindow, QTabWidget

from app.ui.pages.dashboard_page import DashboardPage
from app.ui.pages.products_page import ProductsPage
from app.ui.pages.devices_page import DevicesPage
from app.ui.pages.voice_page import VoicePage
from app.ui.pages.led_page import LedPage
from app.ui.pages.settings_page import SettingsPage


class MainWindow(QMainWindow):

    def __init__(self):

        super().__init__()

        self.setWindowTitle(
            "Smart Showroom AI - Dashboard"
        )

        self.resize(
            1200,
            800
        )


        # Create pages first

        self.dashboard_page = DashboardPage()

        self.products_page = ProductsPage()

        self.devices_page = DevicesPage()

        self.voice_page = VoicePage()

        self.led_page = LedPage()

        self.settings_page = SettingsPage()



        # Create tabs

        self.tabs = QTabWidget()


        self.tabs.addTab(
            self.dashboard_page,
            "Dashboard"
        )


        self.tabs.addTab(
            self.products_page,
            "Products"
        )


        self.tabs.addTab(
            self.devices_page,
            "Devices"
        )


        self.tabs.addTab(
            self.voice_page,
            "Voice"
        )


        self.tabs.addTab(
            self.led_page,
            "LED"
        )


        self.tabs.addTab(
            self.settings_page,
            "Settings"
        )



        self.tabs.currentChanged.connect(
            self.refresh_page
        )


        self.setCentralWidget(
            self.tabs
        )



    def refresh_page(self,index):

        page = self.tabs.widget(index)


        if page == self.dashboard_page:
            self.dashboard_page.refresh_customers()


        elif page == self.products_page:
            self.products_page.refresh_table()


        elif page == self.devices_page:
            self.devices_page.refresh_table()


        elif page == self.voice_page:
            self.voice_page.refresh_devices()


        elif page == self.led_page:
            self.led_page.refresh_devices()