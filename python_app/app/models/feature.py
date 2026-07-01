"""
feature.py
Feature = a capability the system supports (voice, display, led, signboard...)
CustomerFeature = join table: which features are ON/OFF for which customer.
"""

from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship

from app.core.database import Base


class Feature(Base):
    __tablename__ = "features"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), unique=True, nullable=False)  # voice, display, led, signboard
    enabled = Column(Boolean, default=True)  # globally available or not

    def __repr__(self):
        return f"<Feature id={self.id} name='{self.name}'>"


class CustomerFeature(Base):
    __tablename__ = "customer_features"

    id = Column(Integer, primary_key=True, autoincrement=True)
    customer_id = Column(Integer, ForeignKey("customers.id"), nullable=False)
    feature_id = Column(Integer, ForeignKey("features.id"), nullable=False)
    enabled = Column(Boolean, default=False)

    customer = relationship("Customer", back_populates="features")
    feature = relationship("Feature")

    def __repr__(self):
        return f"<CustomerFeature customer_id={self.customer_id} feature_id={self.feature_id} enabled={self.enabled}>"
