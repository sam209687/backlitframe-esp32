"""
settings_service.py

Central settings cache.
Nothing should read the database directly.
"""

from app.core.database import get_session
from app.models.settings import Setting


class SettingsService:

    _settings = {}

    @classmethod
    def load(cls):
        """Load all settings from database."""

        session = get_session()

        try:

            cls._settings.clear()

            rows = session.query(Setting).all()

            for row in rows:
                cls._settings[row.key] = row.value

            print(f"Loaded {len(cls._settings)} settings")

        finally:
            session.close()

    @classmethod
    def get(cls, key, default=None):

        return cls._settings.get(key, default)

    @classmethod
    def set(cls, key, value):

        cls._settings[key] = value

        session = get_session()

        try:

            row = session.query(Setting).filter_by(key=key).first()

            if row:

                row.value = str(value)

                session.commit()

        finally:
            session.close()

    @classmethod
    def reload(cls):

        cls.load()