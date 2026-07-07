"""
style.py

Generates the global stylesheet.
"""

from .manager import ThemeManager


class Style:

    @staticmethod
    def build():

        t = ThemeManager.current()

        return f"""

        QWidget{{
            background:{t.background};
            color:{t.text};
            font-family:"{t.font_family}";
            font-size:{t.body_size}px;
        }}

        QLabel{{
            color:{t.text};
            background:transparent;
        }}

        QFrame{{
            background:{t.card};
            border:1px solid {t.border};
            border-radius:{t.radius_md}px;
        }}

        QPushButton{{
            background:{t.primary};
            color:white;
            border:none;
            border-radius:{t.radius_md}px;
            padding:8px 18px;
        }}

        QPushButton:hover{{
            background:{t.primary_hover};
        }}

        QPushButton:pressed{{
            background:{t.primary_pressed};
        }}

        QLineEdit,
        QTextEdit,
        QPlainTextEdit,
        QComboBox{{
            background:{t.surface};
            border:1px solid {t.border};
            border-radius:{t.radius_md}px;
            padding:8px;
        }}

        QHeaderView::section{{
            background:{t.surface_alt};
            border:none;
            padding:8px;
        }}

        QTableWidget{{
            gridline-color:{t.divider};
            border:1px solid {t.border};
            border-radius:{t.radius_md}px;
        }}

        QScrollBar:vertical{{
            width:10px;
            background:transparent;
        }}

        QScrollBar::handle:vertical{{
            background:{t.primary};
            border-radius:5px;
        }}

        """