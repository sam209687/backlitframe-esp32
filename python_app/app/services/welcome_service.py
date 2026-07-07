"""
welcome_service.py

Loads welcome keywords from the database and
matches spoken text against the configured phrases.
"""

from app.core.database import get_session
from app.models.welcome_keyword import WelcomeKeyword


class WelcomeService:

    @staticmethod
    def get_keywords():
        """
        Returns all enabled welcome phrases.
        """

        session = get_session()

        try:

            return (
                session.query(WelcomeKeyword)
                .filter(WelcomeKeyword.enabled == True)
                .all()
            )

        finally:
            session.close()

    # -------------------------------------------------

    @staticmethod
    def match(text: str):
        """
        Returns the matching WelcomeKeyword object
        if the spoken text contains one of the configured phrases.
        """

        if not text:
            return None

        session = get_session()

        try:

            rows = (
                session.query(WelcomeKeyword)
                .filter(WelcomeKeyword.enabled == True)
                .all()
            )

            spoken = text.lower().strip()

            print("\nConfigured Welcome Phrases")
            print("--------------------------------")

            for row in rows:

                phrase = (row.phrase or "").lower().strip()

                print(f"Checking : '{phrase}'")

                if phrase and phrase in spoken:

                    print(f"Matched  : '{row.phrase}'")

                    return row

            print("No welcome phrase matched")

            return None

        finally:
            session.close()