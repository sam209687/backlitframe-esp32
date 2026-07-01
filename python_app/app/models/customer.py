"""
customer.py
Represents a shop/customer using the Smart Showroom system.
"""

import datetime
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship

from app.core.database import Base


class Customer(Base):
    __tablename__ = "customers"

    id = Column(Integer, primary_key=True, autoincrement=True)
    shop_name = Column(String(255), nullable=False)
    owner = Column(String(255), nullable=True)
    plan = Column(String(50), nullable=False, default="basic")  # basic/premium/etc
    license_key = Column(String(255), unique=True, nullable=True)
    created_date = Column(DateTime, default=datetime.datetime.utcnow)

    features = relationship(
        "CustomerFeature", back_populates="customer", cascade="all, delete-orphan"
    )
    devices = relationship("Device", back_populates="customer", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Customer id={self.id} shop_name='{self.shop_name}' plan='{self.plan}'>"
