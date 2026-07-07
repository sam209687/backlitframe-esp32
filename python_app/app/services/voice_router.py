"""
voice_router.py

Central routing engine for Smart Showroom AI.

This module decides which service should handle the
customer's speech.

Author:
Smart Showroom AI
"""

from app.services.intent_matcher import IntentMatcher, Intent


class VoiceRouter:

    @staticmethod
    def route(text: str):

        intent = IntentMatcher.classify(text)

        print("\n================================")
        print("VOICE ROUTER")
        print("================================")
        print("Input  :", text)
        print("Intent :", intent.value)
        print("================================")

        return {

            "intent": intent,

            "text": text,

            "continue": True,

            "search_product": intent == Intent.PRODUCT_SEARCH,

            "greeting": intent == Intent.GREETING,

            "help": intent == Intent.HELP,

            "repeat": intent == Intent.REPEAT,

            "stop": intent == Intent.STOP,

        }