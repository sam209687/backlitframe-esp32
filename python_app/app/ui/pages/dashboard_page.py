"""
dashboard_page.py
Placeholder page - build out real widgets here.
"""

from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel


class DashboardPage(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Dashboard page - coming soon"))
        self.setLayout(layout)
