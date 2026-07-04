"""
product_service.py

Central Product Service.

Responsibilities
----------------
• Load products
• Search products
• Voice lookup
• CRUD helper methods

No UI.
"""

from app.core.database import get_session
from app.models.product import Product


class ProductService:

    # --------------------------------------------------

    @staticmethod
    def get_all():

        session = get_session()

        try:
            return (
                session.query(Product)
                .order_by(Product.id)
                .all()
            )

        finally:
            session.close()

    # --------------------------------------------------

    @staticmethod
    def get_by_id(product_id):

        session = get_session()

        try:
            return (
                session.query(Product)
                .filter(Product.id == product_id)
                .first()
            )

        finally:
            session.close()

    # --------------------------------------------------

    @staticmethod
    def get_by_name(name):

        session = get_session()

        try:
            return (
                session.query(Product)
                .filter(Product.name == name)
                .first()
            )

        finally:
            session.close()

    # --------------------------------------------------

    @staticmethod
    def search(keyword):

        session = get_session()

        try:

            keyword = f"%{keyword}%"

            return (
                session.query(Product)
                .filter(
                    Product.name.ilike(keyword)
                )
                .all()
            )

        finally:
            session.close()

    # --------------------------------------------------

    @staticmethod
    def find_by_voice(text):

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

    # --------------------------------------------------

    @staticmethod
    def create(**kwargs):

        session = get_session()

        try:

            product = Product(**kwargs)

            session.add(product)

            session.commit()

            session.refresh(product)

            return product

        finally:
            session.close()

    # --------------------------------------------------

    @staticmethod
    def update(product):

        session = get_session()

        try:

            session.merge(product)

            session.commit()

        finally:
            session.close()

    # --------------------------------------------------

    @staticmethod
    def delete(product_id):

        session = get_session()

        try:

            product = session.get(Product, product_id)

            if product:

                session.delete(product)

                session.commit()

                return True

            return False

        finally:
            session.close()

    # --------------------------------------------------
    # Backward compatibility
    # --------------------------------------------------

    @staticmethod
    def get_all_products():
        return ProductService.get_all()

    @staticmethod
    def get_product_by_name(name):
        return ProductService.get_by_name(name)

    @staticmethod
    def find_product_from_text(text):
        return ProductService.find_by_voice(text)