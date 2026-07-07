from app.services.fuzzy_match import FuzzyMatch

tests = [

    ("Vanga Sir", "Vronga sir"),

    ("Groundnut Oil", "Ground Nut Oil"),

    ("Groundnut Oil", "Ground nut"),

    ("Sesame Oil", "Gingelly Oil"),

    ("Hello", "hello"),

    ("Cold Press Sesame Oil", "Sesame Oil"),

    ("வாங்க சார்", "வாங்க சார்"),

]

for a, b in tests:

    FuzzyMatch.debug(a, b)