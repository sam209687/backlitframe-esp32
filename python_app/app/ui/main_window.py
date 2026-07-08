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
from app.ui.pages.voice_page import VoicePage
from app.ui.pages.led_page import LedPage
from app.ui.pages.media_page import MediaPage
from app.ui.pages.settings_page import SettingsPage

from app.ui_comp.layout.sidebar import Sidebar
from app.ui_comp.layout.topbar import TopBar
from app.ui_comp.layout.statusbar import StatusBar


class MainWindow(QMainWindow):

    def __init__(self, runtime=None):
        super().__init__()

        self.runtime = runtime
        self.pages = {}

        self.setWindowTitle("Smart Showroom AI")
        self.resize(1400, 850)

        self.build_ui()
        self.register_pages()

        self.goto_page("Dashboard")

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
        self.sidebar.page_changed.connect(self.goto_page)

        body.addWidget(self.sidebar)

        self.stack = QStackedWidget()
        body.addWidget(self.stack, 1)

        self.statusbar = StatusBar()
        root.addWidget(self.statusbar)

    def register_pages(self):
        self.add_page("Dashboard", DashboardPage(self.runtime))
        self.add_page("Products", ProductsPage(self.runtime))
        self.add_page("Devices", DevicesPage(self.runtime))
        self.add_page("LED Effects", LedPage(self.runtime))
        self.add_page("Media", MediaPage(self.runtime))
        self.add_page("Voice", VoicePage(self.runtime))
        self.add_page("Settings", SettingsPage(self.runtime))

        print("Registered pages:")
        for name in self.pages:
            print("-", name)

    def add_page(self, name, widget):
        self.pages[name] = widget
        self.stack.addWidget(widget)

    def goto_page(self, name):
        print("Goto page:", name)

        page = self.pages.get(name)

        if not page:
            print("PAGE NOT FOUND:", name)
            return

        self.stack.setCurrentWidget(page)

        if hasattr(self.statusbar, "set_status"):
            self.statusbar.set_status(f"Current Page : {name}")

        self.refresh_page(page)

    def refresh_page(self, page):
        refresh_methods = [
            "refresh_dashboard",
            "refresh_table",
            "refresh_devices",
            "refresh_customers",
            "load_products",
        ]

        for method_name in refresh_methods:
            if hasattr(page, method_name):
                try:
                    getattr(page, method_name)()
                except Exception as error:
                    print(f"{method_name} error:", error)

    def closeEvent(self, event):
        try:
            if self.runtime and hasattr(self.runtime, "stop"):
                self.runtime.stop()
        except Exception as error:
            print("Runtime stop error:", error)

        event.accept()