"""
product_matcher.py

Matches recognized speech to a product.
"""

from app.core.database import get_session
from app.models.product import Product


class ProductMatcher:

    def __init__(self):
        self.reload()

    def reload(self):
        session = get_session()

        self.products = session.query(Product).all()

        session.close()

    def match(self, text: str):

        text = text.lower().strip()

        for product in self.products:

            for keyword in product.keywords_list():

                if keyword.lower() in text:
                    return product

        return None