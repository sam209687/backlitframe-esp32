"""
init_db.py
Run this once to create smartshowroom.db and seed default features.

Usage (from python_app/ with venv activated):
    python -m database.init_db
or simply:
    python database/init_db.py
"""

import os
import sys

# Make sure python_app/ is on the path so `import app...` works
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, os.path.join(BASE_DIR, "python_app"))

from app.core.database import init_db, get_session  # noqa: E402
from app.models.feature import Feature  # noqa: E402

DEFAULT_FEATURES = ["voice", "display", "led", "signboard"]


def seed_features():
    session = get_session()
    try:
        for name in DEFAULT_FEATURES:
            exists = session.query(Feature).filter_by(name=name).first()
            if not exists:
                session.add(Feature(name=name, enabled=True))
                print(f"Seeded feature: {name}")
        session.commit()
    finally:
        session.close()


if __name__ == "__main__":
    init_db()
    seed_features()
    print("Database ready.")
