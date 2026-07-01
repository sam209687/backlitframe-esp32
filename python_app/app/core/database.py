"""
database.py
Central SQLite connection + session factory using SQLAlchemy.
All models import Base from here.
"""

import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# database/smartshowroom.db lives two levels up from app/core/
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
DB_PATH = os.path.join(BASE_DIR, "database", "smartshowroom.db")

engine = create_engine(f"sqlite:///{DB_PATH}", echo=False, future=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
Base = declarative_base()


def get_session():
    """Return a new SQLAlchemy session. Caller is responsible for closing it."""
    return SessionLocal()


def init_db():
    """Create all tables. Import models first so they register with Base.metadata."""
    import app.models  # noqa: F401 - registers all model classes
    Base.metadata.create_all(bind=engine)
    print(f"Database initialized at {DB_PATH}")


# Import all models as soon as this module is loaded. Several models use
# string-based relationship() references (e.g. relationship("Customer")),
# which SQLAlchemy only resolves once every referenced class has been
# imported somewhere. Since almost all app code imports get_session/Base
# from this module, importing app.models here guarantees the full mapper
# registry is populated before any query runs, regardless of which page
# or script happens to run first.
import app.models  # noqa: E402, F401


if __name__ == "__main__":
    init_db()