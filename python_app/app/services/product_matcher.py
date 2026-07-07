"""
product_matcher.py

Smart product matcher for Smart Showroom AI.
"""

from app.services.product_service import ProductService
from app.services.text_normalizer import TextNormalizer
from app.services.fuzzy_match import FuzzyMatch


class ProductMatcher:

    SCORE_THRESHOLD = 0.55

    # -------------------------------------------------

    @staticmethod
    def match(text: str):

        if not text:
            return None

        spoken = TextNormalizer.normalize(text)

        products = ProductService.get_all()

        best_product = None
        best_score = 0.0
        best_keyword = ""

        print("\n================================")
        print("PRODUCT MATCHER")
        print("================================")
        print("Input :", spoken)
        print()

        for product in products:

            candidates = [product.name]

            if product.voice_keywords:

                candidates.extend(
                    [
                        k.strip()
                        for k in product.voice_keywords.split(",")
                        if k.strip()
                    ]
                )

            for keyword in candidates:

                keyword = TextNormalizer.normalize(keyword)

                score = FuzzyMatch.score(
                    spoken,
                    keyword
                )

                print(
                    f"{product.name:<25}"
                    f"{keyword:<25}"
                    f"{score:.3f}"
                )

                if score > best_score:

                    best_score = score
                    best_product = product
                    best_keyword = keyword

        print("--------------------------------")

        if (
            best_product is None
            or best_score < ProductMatcher.SCORE_THRESHOLD
        ):

            print("No Product Matched")
            print("--------------------------------")

            return None

        print(
            f"Matched : {best_product.name}"
        )

        print(
            f"Keyword : {best_keyword}"
        )

        print(
            f"Score   : {best_score:.3f}"
        )

        print("--------------------------------")

        return {
            "product": best_product,
            "score": round(best_score, 3),
            "keyword": best_keyword,
        }