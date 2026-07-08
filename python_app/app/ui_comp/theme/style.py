"""
style.py

Global stylesheet generator.
"""

from .manager import ThemeManager


class Style:

    @staticmethod
    def build():

        t = ThemeManager.current()

        return f"""
        QWidget {{
            background: {t.background};
            color: {t.text};
            font-family: "{t.font_family}";
            font-size: {t.body_size}px;
        }}

        QLabel {{
            background: transparent;
            color: {t.text};
        }}

        QPushButton {{
            background: {t.primary};
            color: white;
            border: none;
            border-radius: {t.radius_md}px;
            padding: 8px 18px;
            font-weight: 600;
        }}

        QPushButton:hover {{
            background: {t.primary_hover};
        }}

        QPushButton:pressed {{
            background: {t.primary_pressed};
        }}

        QPushButton:disabled {{
            background: {t.surface_alt};
            color: {t.text_secondary};
        }}

        QLineEdit,
        QTextEdit,
        QPlainTextEdit,
        QComboBox {{
            background: {t.surface};
            color: {t.text};
            border: 1px solid {t.border};
            border-radius: {t.radius_md}px;
            padding: 8px;
        }}

        QTableWidget {{
            background: {t.card};
            color: {t.text};
            border: 1px solid {t.border};
            border-radius: {t.radius_md}px;
            gridline-color: {t.divider};
        }}

        QHeaderView::section {{
            background: {t.surface_alt};
            color: {t.text};
            padding: 8px;
            border: none;
            font-weight: bold;
        }}

        QScrollBar:vertical {{
            width: 10px;
            background: transparent;
        }}

        QScrollBar::handle:vertical {{
            background: {t.border};
            border-radius: 5px;
        }}

        QScrollBar::handle:vertical:hover {{
            background: {t.primary};
        }}
        """
