"""
voice_page.py
Live microphone -> faster-whisper transcription, feeding recognized
phrases into the showroom voice_actions pipeline.

Runs the record+transcribe loop in a background QThread so the UI
never freezes. Start/Stop button controls the loop.
"""

import queue
import numpy as np

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QTextEdit,
    QComboBox, QCheckBox, QMessageBox
)
from PySide6.QtCore import QThread, Signal

from app.core.database import get_session
from app.core.logger import get_logger
from app.core.config_manager import load as load_config
from app.models.device import Device
from app.modules.showroom.voice_actions import handle_transcript

logger = get_logger(__name__)

SAMPLE_RATE = 16000
CHUNK_SECONDS = 4  # length of each audio segment sent to whisper


class TranscriptionWorker(QThread):
    transcript_ready = Signal(str)
    error = Signal(str)
    status_changed = Signal(str)

    def __init__(self):
        super().__init__()
        self._running = False
        self._model = None

    def stop(self):
        self._running = False

    def run(self):
        try:
            import sounddevice as sd
            from faster_whisper import WhisperModel
        except ImportError as e:
            self.error.emit(
                f"Missing dependency: {e}. Run: pip install sounddevice faster-whisper"
            )
            return

        cfg = load_config("voice")
        model_size = cfg.get("model", "small")
        language = cfg.get("language", "auto")
        language = None if language == "auto" else language

        self.status_changed.emit(f"Loading whisper model '{model_size}'...")
        try:
            self._model = WhisperModel(model_size, compute_type="int8")
        except Exception as e:
            self.error.emit(f"Failed to load model: {e}")
            return

        self.status_changed.emit("Listening...")
        self._running = True

        audio_queue = queue.Queue()

        def audio_callback(indata, frames, time_info, status):
            if status:
                logger.warning(f"Audio status: {status}")
            audio_queue.put(indata.copy())

        try:
            with sd.InputStream(
                samplerate=SAMPLE_RATE,
                channels=1,
                dtype="float32",
                callback=audio_callback,
            ):
                buffer = np.zeros((0, 1), dtype="float32")
                chunk_samples = SAMPLE_RATE * CHUNK_SECONDS

                while self._running:
                    try:
                        data = audio_queue.get(timeout=0.5)
                    except queue.Empty:
                        continue

                    buffer = np.concatenate([buffer, data], axis=0)

                    if len(buffer) >= chunk_samples:
                        segment = buffer[:chunk_samples, 0]
                        buffer = buffer[chunk_samples:]

                        segments, _ = self._model.transcribe(
                            segment, language=language, beam_size=1
                        )
                        text = " ".join(s.text.strip() for s in segments).strip()
                        if text:
                            self.transcript_ready.emit(text)
        except Exception as e:
            self.error.emit(f"Audio stream error: {e}")
        finally:
            self.status_changed.emit("Stopped")


class VoicePage(QWidget):
    def __init__(self):
        super().__init__()
        self.worker = None
        self._build_ui()
        self.refresh_devices()

    def _build_ui(self):
        layout = QVBoxLayout()

        title = QLabel("Voice Control")
        title.setStyleSheet("font-size: 18px; font-weight: bold;")
        layout.addWidget(title)

        # --- Device selector + auto-trigger toggle ---
        device_row = QHBoxLayout()
        device_row.addWidget(QLabel("Target device:"))
        self.device_combo = QComboBox()
        device_row.addWidget(self.device_combo)
        refresh_btn = QPushButton("Refresh Devices")
        refresh_btn.clicked.connect(self.refresh_devices)
        device_row.addWidget(refresh_btn)
        device_row.addStretch()
        layout.addLayout(device_row)

        self.auto_trigger_checkbox = QCheckBox(
            "Auto-trigger product LED/display when a keyword is heard"
        )
        self.auto_trigger_checkbox.setChecked(True)
        layout.addWidget(self.auto_trigger_checkbox)

        # --- Start/Stop ---
        control_row = QHBoxLayout()
        self.start_btn = QPushButton("Start Listening")
        self.start_btn.clicked.connect(self.start_listening)
        self.stop_btn = QPushButton("Stop")
        self.stop_btn.clicked.connect(self.stop_listening)
        self.stop_btn.setEnabled(False)
        control_row.addWidget(self.start_btn)
        control_row.addWidget(self.stop_btn)
        control_row.addStretch()
        layout.addLayout(control_row)

        self.status_label = QLabel("Idle")
        self.status_label.setStyleSheet("color: gray;")
        layout.addWidget(self.status_label)

        # --- Transcript log ---
        layout.addWidget(QLabel("Transcript:"))
        self.transcript_log = QTextEdit()
        self.transcript_log.setReadOnly(True)
        layout.addWidget(self.transcript_log)

        self.setLayout(layout)

    def refresh_devices(self):
        session = get_session()
        try:
            devices = session.query(Device).all()
            self.device_combo.clear()
            self._device_ips = []
            for d in devices:
                self.device_combo.addItem(f"{d.device_name} ({d.ip})")
                self._device_ips.append(d.ip)
        finally:
            session.close()

    def _selected_ip(self):
        idx = self.device_combo.currentIndex()
        if idx < 0 or idx >= len(self._device_ips):
            return None
        return self._device_ips[idx]

    def start_listening(self):
        if self.worker and self.worker.isRunning():
            return

        self.worker = TranscriptionWorker()
        self.worker.transcript_ready.connect(self.on_transcript)
        self.worker.error.connect(self.on_error)
        self.worker.status_changed.connect(self.on_status)
        self.worker.start()

        self.start_btn.setEnabled(False)
        self.stop_btn.setEnabled(True)

    def stop_listening(self):
        if self.worker:
            self.worker.stop()
        self.start_btn.setEnabled(True)
        self.stop_btn.setEnabled(False)
        self.status_label.setText("Stopping...")

    def on_status(self, status: str):
        self.status_label.setText(status)

    def on_error(self, message: str):
        QMessageBox.critical(self, "Voice error", message)
        self.start_btn.setEnabled(True)
        self.stop_btn.setEnabled(False)
        self.status_label.setText("Error")

    def on_transcript(self, text: str):
        self.transcript_log.append(f"> {text}")

        if self.auto_trigger_checkbox.isChecked():
            ip = self._selected_ip()
            if ip:
                handle_transcript(text, ip)
            else:
                self.transcript_log.append("  (no device selected - skipped trigger)")