"""
showroom_state.py

Defines all runtime states used by Smart Showroom AI.
"""


from enum import Enum


class ShowroomState(str, Enum):

    STARTING = "STARTING"

    IDLE = "IDLE"

    WAITING_WAKEWORD = "WAITING_WAKEWORD"

    LISTENING = "LISTENING"

    PROCESSING = "PROCESSING"

    PRODUCT_FOUND = "PRODUCT_FOUND"

    PRODUCT_NOT_FOUND = "PRODUCT_NOT_FOUND"

    PLAYING_MEDIA = "PLAYING_MEDIA"

    PAUSED = "PAUSED"

    STOPPED = "STOPPED"

    ERROR = "ERROR"