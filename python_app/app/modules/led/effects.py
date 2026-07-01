"""
effects.py
Placeholder for any Python-side effect metadata (durations, colors, etc.)
that the dashboard UI needs to display/edit. Actual rendering happens
on the ESP32 firmware side.
"""

EFFECT_META = {
    "SESAME": {"label": "Sesame Oil", "color": "#E8C39E", "default_duration": 30},
    "GROUNDNUT": {"label": "Groundnut Oil", "color": "#C68E3F", "default_duration": 30},
    "COCONUT": {"label": "Coconut Oil", "color": "#F5F5DC", "default_duration": 30},
    "MUSTARD": {"label": "Mustard Oil", "color": "#B5A642", "default_duration": 30},
    "PC_MODE": {"label": "PC Mode", "color": "#00A8FF", "default_duration": None},
    "COZY_READING": {"label": "Cozy Reading", "color": "#FFB877", "default_duration": None},
    "FILLING_OIL": {"label": "Filling Oil", "color": "#FFD700", "default_duration": 10},
}
