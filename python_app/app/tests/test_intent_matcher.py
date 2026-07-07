from app.services.intent_matcher import IntentMatcher

tests = [

    "Hello",

    "Hi",

    "Vanga Sir",

    "Show me sesame oil",

    "Groundnut Oil",

    "Help",

    "What products do you have",

    "Repeat",

    "Again",

    "Stop",

    "Cancel",

]

for t in tests:

    IntentMatcher.debug(t)