"""
voice_service.py
Wraps the speech-to-text engine configured in config/voice.json.
Currently targets faster-whisper; can be swapped to Vosk by changing
config only (no code change needed in callers).
"""

from app.core.config_manager import load as load_config
from app.core.logger import get_logger

logger = get_logger(__name__)


def start_voice():
    cfg = load_config("voice")
    engine = cfg.get("engine", "faster-whisper")
    logger.info(f"Starting voice engine: {engine} (model={cfg.get('model')})")

    if engine == "faster-whisper":
        _start_faster_whisper(cfg)
    elif engine == "vosk":
        _start_vosk(cfg)
    else:
        raise ValueError(f"Unsupported voice engine: {engine}")


def _start_faster_whisper(cfg: dict):
    # from faster_whisper import WhisperModel
    # model = WhisperModel(cfg["model"])
    logger.info("faster-whisper engine placeholder - implement transcription loop here")


def _start_vosk(cfg: dict):
    logger.info("Vosk engine placeholder - implement transcription loop here")
