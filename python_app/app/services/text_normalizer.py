"""
text_normalizer.py

Universal text normalization for Smart Showroom AI.

This module prepares Whisper output before any
matching is performed.

Used by:
    - WelcomeService
    - ProductService
    - IntentMatcher
    - VoiceRouter
    - Future AI modules

Author:
    Smart Showroom AI
"""

import re
import unicodedata


class TextNormalizer:

    # ---------------------------------------------

    @staticmethod
    def remove_accents(text: str) -> str:
        """
        Removes unicode accents.

        café -> cafe
        naïve -> naive
        """

        return "".join(

            c for c in unicodedata.normalize("NFKD", text)

            if not unicodedata.combining(c)

        )

    # ---------------------------------------------

    @staticmethod
    def remove_punctuation(text: str) -> str:
        """
        Keep:
            English letters
            Numbers
            Tamil Unicode block
            Spaces
        """

        return re.sub(

            r"[^a-zA-Z0-9\u0B80-\u0BFF ]",

            " ",

            text

        )

    # ---------------------------------------------

    @staticmethod
    def remove_extra_spaces(text: str) -> str:

        return " ".join(text.split())

    # ---------------------------------------------

    @staticmethod
    def normalize(text: str) -> str:
        """
        Complete normalization pipeline.
        """

        if text is None:
            return ""

        text = str(text)

        text = text.strip()

        text = TextNormalizer.remove_accents(text)

        text = text.lower()

        text = TextNormalizer.remove_punctuation(text)

        text = TextNormalizer.remove_extra_spaces(text)

        return text

    # ---------------------------------------------

    @staticmethod
    def tokenize(text: str):
        """
        Converts text into tokens.

        Example

        "Cold Press Groundnut Oil"

        →

        ["cold","press","groundnut","oil"]
        """

        text = TextNormalizer.normalize(text)

        if not text:

            return []

        return text.split()

    # ---------------------------------------------

    @staticmethod
    def contains(source: str, target: str) -> bool:
        """
        Case-insensitive contains.
        """

        source = TextNormalizer.normalize(source)

        target = TextNormalizer.normalize(target)

        return target in source

    # ---------------------------------------------

    @staticmethod
    def starts_with(source: str, target: str) -> bool:

        source = TextNormalizer.normalize(source)

        target = TextNormalizer.normalize(target)

        return source.startswith(target)

    # ---------------------------------------------

    @staticmethod
    def ends_with(source: str, target: str) -> bool:

        source = TextNormalizer.normalize(source)

        target = TextNormalizer.normalize(target)

        return source.endswith(target)

    # ---------------------------------------------

    @staticmethod
    def word_set(text: str):
        """
        Returns unique normalized words.

        Useful for fuzzy comparison.
        """

        return set(TextNormalizer.tokenize(text))

    # ---------------------------------------------

    @staticmethod
    def common_word_count(a: str, b: str):
        """
        Number of common words.

        Example

        Ground Nut Oil

        Groundnut Oil

        -> 1
        """

        return len(

            TextNormalizer.word_set(a)

            &

            TextNormalizer.word_set(b)

        )

    # ---------------------------------------------

    @staticmethod
    def debug(text: str):

        print()

        print("========== TEXT NORMALIZER ==========")

        print("Original   :", repr(text))

        print("Normalized :", repr(TextNormalizer.normalize(text)))

        print("Tokens     :", TextNormalizer.tokenize(text))

        print("=====================================")