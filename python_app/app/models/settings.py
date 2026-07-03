"""
settings.py

Stores configurable application settings.
Nothing should be hardcoded.
"""

from sqlalchemy import Column, Integer, String

from app.core.database import Base


class Setting(Base):
    __tablename__ = "settings"

    id = Column(Integer, primary_key=True, autoincrement=True)

    category = Column(String(100), nullable=False)

    key = Column(String(100), unique=True, nullable=False)

    value = Column(String(255), nullable=True)

    datatype = Column(String(30), default="string")

    description = Column(String(255), nullable=True)

    editable = Column(Integer, default=1)

    sort_order = Column(Integer, default=0)

    def __repr__(self):
        return f"<Setting {self.key}={self.value}>"