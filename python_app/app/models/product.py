"""
product.py
Represents a showroom product (e.g. sesame oil), its voice keywords,
LED effect, and media folder path.
"""

from sqlalchemy import Column, Integer, String

from app.core.database import Base
from sqlalchemy.orm import relationship

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)  # e.g. sesame
    voice_keywords = Column(String(500), nullable=True)  # comma separated: "sesame,gingelly,nallennai"
    led_effect = Column(String(100), nullable=True)  # e.g. SESAME
    media_path = Column(String(255), nullable=True)  # e.g. media/sesame
    media = relationship("Media",back_populates="product",cascade="all, delete-orphan")

    def keywords_list(self) -> list[str]:
        if not self.voice_keywords:
            return []
        return [k.strip() for k in self.voice_keywords.split(",") if k.strip()]

    def __repr__(self):
        return f"<Product id={self.id} name='{self.name}' led_effect='{self.led_effect}'>"
