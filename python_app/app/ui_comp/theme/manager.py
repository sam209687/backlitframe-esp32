from .theme import DARK, LIGHT


class ThemeManager:
    _theme = DARK

    @classmethod
    def current(cls):
        return cls._theme

    @classmethod
    def set_dark(cls):
        cls._theme = DARK

    @classmethod
    def set_light(cls):
        cls._theme = LIGHT

    @classmethod
    def toggle(cls):
        cls._theme = LIGHT if cls._theme == DARK else DARK

    @classmethod
    def is_dark(cls):
        return cls._theme == DARK