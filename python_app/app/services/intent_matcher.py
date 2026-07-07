"""
intent_matcher.py

Determines what the customer is trying to do.

This module does NOT execute anything.

It only classifies the spoken sentence.

Examples

"Hello"

    -> GREETING

"Show me sesame oil"

    -> PRODUCT_SEARCH

"Repeat"

    -> REPEAT

"Stop"

    -> STOP

"What do you have?"

    -> HELP

Author:
Smart Showroom AI
"""

from enum import Enum

from app.services.text_normalizer import TextNormalizer


class Intent(Enum):

    UNKNOWN = "unknown"

    GREETING = "greeting"

    PRODUCT_SEARCH = "product_search"

    HELP = "help"

    REPEAT = "repeat"

    STOP = "stop"


class IntentMatcher:

    GREETING = {

        "hello",

        "hi",

        "welcome",

        "good morning",

        "good evening",

        "vanga sir",

        "வாங்க சார்",

        "enna venum",

        "how can i help you",

    }

    HELP = {

        "help",

        "what do you have",

        "show products",

        "products",

        "catalog",

        "available",

    }

    STOP = {

        "stop",

        "cancel",

        "exit",

        "close",

        "bye",

    }

    REPEAT = {

        "repeat",

        "again",

        "once more",

    }

    # ----------------------------------------------------

    @staticmethod
    def classify(text: str):

        text = TextNormalizer.normalize(text)

        if not text:

            return Intent.UNKNOWN

        for phrase in IntentMatcher.GREETING:

            if phrase in text:

                return Intent.GREETING

        for phrase in IntentMatcher.HELP:

            if phrase in text:

                return Intent.HELP

        for phrase in IntentMatcher.REPEAT:

            if phrase in text:

                return Intent.REPEAT

        for phrase in IntentMatcher.STOP:

            if phrase in text:

                return Intent.STOP

        #
        # Everything else
        # is assumed to be
        # a product request.
        #

        return Intent.PRODUCT_SEARCH

    # ----------------------------------------------------

    @staticmethod
    def debug(text):

        print()

        print("==============================")

        print("Input :")

        print(text)

        print()

        print("Normalized :")

        print(TextNormalizer.normalize(text))

        print()

        print("Intent :")

        print(IntentMatcher.classify(text))

        print("==============================")