"""
fuzzy_match.py

Universal fuzzy string matching engine.

Used by:

- WelcomeService
- ProductService
- IntentMatcher
- VoiceRouter

Author:
Smart Showroom AI
"""

from difflib import SequenceMatcher

from app.services.text_normalizer import TextNormalizer


class FuzzyMatch:

    DEFAULT_THRESHOLD = 0.70

    # ---------------------------------------------------------

    @staticmethod
    def similarity(a: str, b: str) -> float:
        """
        Returns similarity score between 0 and 1.
        """

        a = TextNormalizer.normalize(a)
        b = TextNormalizer.normalize(b)

        if not a or not b:
            return 0.0

        return SequenceMatcher(
            None,
            a,
            b
        ).ratio()

    # ---------------------------------------------------------

    @staticmethod
    def word_similarity(a: str, b: str) -> float:
        """
        Word overlap score.
        """

        wa = TextNormalizer.word_set(a)
        wb = TextNormalizer.word_set(b)

        if not wa or not wb:
            return 0.0

        common = len(wa & wb)

        largest = max(len(wa), len(wb))

        return common / largest

    # ---------------------------------------------------------

    @staticmethod
    def score(a: str, b: str) -> float:
        """
        Combined score.

        60% character similarity
        40% word similarity
        """

        char_score = FuzzyMatch.similarity(a, b)

        word_score = FuzzyMatch.word_similarity(a, b)

        return round(

            (char_score * 0.60)

            +

            (word_score * 0.40),

            3

        )

    # ---------------------------------------------------------

    @staticmethod
    def match(a: str,
              b: str,
              threshold=None):

        if threshold is None:
            threshold = FuzzyMatch.DEFAULT_THRESHOLD

        score = FuzzyMatch.score(a, b)

        return score >= threshold

    # ---------------------------------------------------------

    @staticmethod
    def best_match(text,
                   candidates,
                   threshold=None):
        """
        Finds best string.

        Returns

        (
            candidate,
            score
        )
        """

        if threshold is None:
            threshold = FuzzyMatch.DEFAULT_THRESHOLD

        best_item = None
        best_score = 0.0

        for item in candidates:

            score = FuzzyMatch.score(
                text,
                item
            )

            if score > best_score:

                best_item = item

                best_score = score

        if best_score < threshold:
            return None, best_score

        return best_item, best_score

    # ---------------------------------------------------------

    @staticmethod
    def best_object(text,
                    objects,
                    getter,
                    threshold=None):
        """
        Finds best object.

        getter(obj) returns string.
        """

        if threshold is None:
            threshold = FuzzyMatch.DEFAULT_THRESHOLD

        best = None
        best_score = 0.0

        for obj in objects:

            phrase = getter(obj)

            score = FuzzyMatch.score(
                text,
                phrase
            )

            if score > best_score:

                best = obj

                best_score = score

        if best_score < threshold:
            return None, best_score

        return best, best_score

    # ---------------------------------------------------------

    @staticmethod
    def debug(a, b):

        print()

        print("===============================")

        print("A :", a)

        print("B :", b)

        print()

        print("Normalized")

        print(TextNormalizer.normalize(a))

        print(TextNormalizer.normalize(b))

        print()

        print(
            "Character Score :",
            FuzzyMatch.similarity(a, b)
        )

        print(
            "Word Score      :",
            FuzzyMatch.word_similarity(a, b)
        )

        print(
            "Final Score     :",
            FuzzyMatch.score(a, b)
        )

        print(
            "Matched         :",
            FuzzyMatch.match(a, b)
        )

        print("===============================")