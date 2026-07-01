"""
schedule.py
Represents an on/off (or event) schedule for a device, e.g. signboard
timing.
"""

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from app.core.database import Base


class Schedule(Base):
    __tablename__ = "schedules"

    id = Column(Integer, primary_key=True, autoincrement=True)
    device_id = Column(Integer, ForeignKey("devices.id"), nullable=False)
    type = Column(String(50), nullable=False)  # e.g. "daily_on_off"
    on_time = Column(String(10), nullable=True)  # "HH:MM"
    off_time = Column(String(10), nullable=True)  # "HH:MM"

    device = relationship("Device", back_populates="schedules")

    def __repr__(self):
        return f"<Schedule id={self.id} device_id={self.device_id} on='{self.on_time}' off='{self.off_time}'>"
