"""
page_router.py

Central page navigation.

Usage
-----
router.register("dashboard", DashboardPage())
router.register("products", ProductPage())

router.goto("products")
"""

from PySide6.QtWidgets import QStackedWidget


class PageRouter:

    def __init__(self, stack: QStackedWidget):

        self.stack = stack

        self.pages = {}

    # -------------------------------------------------

    def register(
        self,
        name: str,
        widget
    ):

        name = name.lower()

        if name in self.pages:
            return

        self.pages[name] = widget

        self.stack.addWidget(widget)

    # -------------------------------------------------

    def goto(
        self,
        name: str
    ):

        name = name.lower()

        if name not in self.pages:

            print(f"Unknown page : {name}")

            return

        self.stack.setCurrentWidget(

            self.pages[name]

        )

    # -------------------------------------------------

    def current(self):

        return self.stack.currentWidget()

    # -------------------------------------------------

    def page(self, name):

        return self.pages.get(name.lower())

    # -------------------------------------------------

    def names(self):

        return list(self.pages.keys())