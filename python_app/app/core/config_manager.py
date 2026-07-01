"""
config_manager.py
Loads and caches JSON files from the config/ directory.
"""

import os
import json

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
CONFIG_DIR = os.path.join(BASE_DIR, "config")

_cache = {}


def load(name: str) -> dict:
    """
    Load a config file by name, e.g. load("voice") -> config/voice.json
    Results are cached; call reload() to force a re-read.
    """
    if name in _cache:
        return _cache[name]

    path = os.path.join(CONFIG_DIR, f"{name}.json")
    if not os.path.exists(path):
        raise FileNotFoundError(f"Config file not found: {path}")

    with open(path, "r") as f:
        data = json.load(f)

    _cache[name] = data
    return data


def reload(name: str) -> dict:
    """Force reload a config file, bypassing the cache."""
    _cache.pop(name, None)
    return load(name)


def save(name: str, data: dict):
    """Write updated config back to disk and refresh cache."""
    path = os.path.join(CONFIG_DIR, f"{name}.json")
    with open(path, "w") as f:
        json.dump(data, f, indent=2)
    _cache[name] = data


if __name__ == "__main__":
    print(load("app"))
    print(load("voice"))
