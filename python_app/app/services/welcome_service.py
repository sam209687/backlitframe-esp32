"""
welcome_service.py

Loads welcome keywords from database.
"""

from app.core.database import get_session
from app.models.welcome_keyword import WelcomeKeyword


class WelcomeService:

    @staticmethod
    def get_keywords():

        session = get_session()

        try:

            rows = (
                session.query(WelcomeKeyword)
                .filter(WelcomeKeyword.enabled == 1)
                .all()
            )

            return rows

        finally:
            session.close()

    @staticmethod
    def match(text: str):
        """
        Returns matching WelcomeKeyword object
        if spoken text contains one.
        """

        session = get_session()

        try:

            rows = (
                session.query(WelcomeKeyword)
                .filter(WelcomeKeyword.enabled == 1)
                .all()
            )

            text = text.lower()

            for row in rows:

                if row.keyword.lower() in text:
                    return row

            return None

        finally:
            session.close()