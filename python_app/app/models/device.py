"""
device.py
Represents a physical ESP32 device (LED frame, signboard, etc.) belonging
to a customer.
"""

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from app.core.database import Base


class Device(Base):
    __tablename__ = "devices"

    id = Column(Integer, primary_key=True, autoincrement=True)
    customer_id = Column(Integer, ForeignKey("customers.id"), nullable=True)
    device_name = Column(String(100), nullable=False)  # e.g. SMART_SHOWROOM_FRAME_01
    ip = Column(String(45), nullable=True)
    location = Column(String(255), nullable=True)
    status = Column(String(50), default="disconnected")  # connected/disconnected

    customer = relationship("Customer", back_populates="devices")
    schedules = relationship("Schedule", back_populates="device", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Device id={self.id} name='{self.device_name}' status='{self.status}'>"
