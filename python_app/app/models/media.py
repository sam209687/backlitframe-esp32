from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey
)

from sqlalchemy.orm import relationship

from app.core.database import Base


class Media(Base):
    __tablename__ = "media"

    id = Column(Integer, primary_key=True)

    product_id = Column(Integer, ForeignKey("products.id"))

    media_name = Column(String(200))

    media_type = Column(String(20))

    file_path = Column(String(500))

    duration = Column(Integer)

    display_order = Column(Integer)

    is_default = Column(Integer)

    is_active = Column(Integer)

    description = Column(String(255))

    product = relationship(
        "Product",
        back_populates="media"
    )