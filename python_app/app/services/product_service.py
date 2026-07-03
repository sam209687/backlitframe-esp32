"""
product_service.py

Provides product lookup services.
Voice engine and UI should use this service instead of querying
the database directly.
"""

from app.core.database import get_session
from app.models.product import Product


class ProductService:

    @staticmethod
    def get_all_products():
        session = get_session()
        try:
            return session.query(Product).all()
        finally:
            session.close()

    @staticmethod
    def get_product_by_name(name: str):
        session = get_session()

        try:
            return (
                session.query(Product)
                .filter(Product.name == name)
                .first()
            )

        finally:
            session.close()

    @staticmethod
    def find_product_from_text(text: str):
        """
        Finds product whose voice keyword appears
        inside spoken text.
        """

        session = get_session()

        try:

            products = session.query(Product).all()

            text = text.lower()

            for product in products:

                if not product.voice_keywords:
                    continue

                keywords = [
                    k.strip().lower()
                    for k in product.voice_keywords.split(",")
                ]

                for keyword in keywords:

                    if keyword in text:
                        return product

            return None

        finally:
            session.close()