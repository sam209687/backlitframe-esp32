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

    product_id = Column(
        Integer,
        ForeignKey("products.id"),
        nullable=False
    )

    media_name = Column(String(200), nullable=False)

    media_type = Column(String(20), nullable=False)

    file_path = Column(String(500), nullable=False)

    duration = Column(Integer, default=10)

    display_order = Column(Integer, default=1)

    is_default = Column(Integer, default=1)

    is_active = Column(Integer, default=1)

    description = Column(String(255))

    product = relationship(
        "Product",
        back_populates="media"
    )

    def __repr__(self):
        return (
            f"<Media {self.media_name}>"
        )