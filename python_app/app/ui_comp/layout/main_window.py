"""
main_window.py

Main application window.
Every desktop page loads here.
"""

from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QStackedWidget,
)

from app.ui.pages.dashboard_page import DashboardPage
from app.ui.pages.products_page import ProductsPage
from app.ui.pages.devices_page import DevicesPage
from app.ui.pages.led_page import LedPage
from app.ui.pages.media_page import MediaPage
from app.ui.pages.voice_page import VoicePage
from app.ui.pages.settings_page import SettingsPage

from app.ui_comp.base import BasePage
from app.ui_comp.layout.sidebar import Sidebar
from app.ui_comp.layout.topbar import TopBar
from app.ui_comp.layout.statusbar import StatusBar
from app.ui_comp.layout.page_router import PageRouter


class MainWindow(QMainWindow):

    def __init__(self, runtime=None):
        super().__init__()

        self.runtime = runtime

        self.setWindowTitle("Smart Showroom AI")
        self.resize(1600, 900)

        self.build_ui()
        self.register_pages()

        self.sidebar.page_changed.connect(self.change_page)

        self.change_page("Dashboard")

    def build_ui(self):
        central = QWidget()
        self.setCentralWidget(central)

        root = QVBoxLayout(central)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        self.topbar = TopBar()
        root.addWidget(self.topbar)

        body = QHBoxLayout()
        body.setContentsMargins(0, 0, 0, 0)
        body.setSpacing(0)

        root.addLayout(body, 1)

        self.sidebar = Sidebar()
        body.addWidget(self.sidebar)

        self.stack = QStackedWidget()
        body.addWidget(self.stack, 1)

        self.statusbar = StatusBar()
        root.addWidget(self.statusbar)

        self.router = PageRouter(self.stack)

    def register_pages(self):
        self.router.register("dashboard", DashboardPage(self.runtime))
        self.router.register("products", ProductsPage(self.runtime))
        self.router.register("devices", DevicesPage(self.runtime))
        self.router.register("led effects", LedPage(self.runtime))
        self.router.register("media", MediaPage(self.runtime))
        self.router.register("voice", VoicePage(self.runtime))
        self.router.register("settings", SettingsPage(self.runtime))

        self.router.register(
            "scheduler",
            self.placeholder_page(
                "Scheduler",
                "Schedule automation is not connected yet.",
            ),
        )

        self.router.register(
            "relay",
            self.placeholder_page(
                "Relay Manager",
                "Relay manager is not connected yet.",
            ),
        )

    def change_page(self, name):
        key = str(name).strip().lower()

        print("Goto page:", key)

        page = self.router.page(key)

        if page is None:
            print("PAGE NOT FOUND:", key)
            return

        self.router.goto(key)
        self.refresh_page(page)

        if hasattr(self.statusbar, "set_status"):
            self.statusbar.set_status(f"Current Page : {name}")

    def refresh_page(self, page):
        methods = [
            "refresh_dashboard",
            "refresh_table",
            "refresh_devices",
            "load_products",
        ]

        for method in methods:
            if hasattr(page, method):
                try:
                    getattr(page, method)()
                except Exception as error:
                    print(f"{method} error:", error)

    def placeholder_page(self, title, subtitle):
        return BasePage(
            title=title,
            subtitle=subtitle,
        )

    def closeEvent(self, event):
        try:
            if self.runtime and hasattr(self.runtime, "stop"):
                self.runtime.stop()
        except Exception as error:
            print("Runtime stop error:", error)

        event.accept()