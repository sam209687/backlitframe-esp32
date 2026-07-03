"""
wakeword_service.py

Detect showroom activation phrases.
"""

from app.core.database import get_session
from sqlalchemy import text


class WakeWordService:

    def __init__(self):
        self.reload()

    def reload(self):

        session = get_session()

        rows = session.execute(text("""
            SELECT keyword
            FROM welcome_keywords
            WHERE enabled=1
        """))

        self.keywords = [
            r[0].lower()
            for r in rows
        ]

        session.close()

    def activated(self, text_value: str):

        text_value = text_value.lower()

        for keyword in self.keywords:

            if keyword in text_value:
                return True

        return False