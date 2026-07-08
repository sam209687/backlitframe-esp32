"""
voice_page.py

Live microphone -> faster-whisper transcription.

Flow:
    Microphone
    -> Faster Whisper
    -> Transcript
    -> Wakeup check
    -> Product match
    -> ESP32 LED command
    -> Media action through runtime

Runs in a background thread so the UI does not freeze.
"""

import queue
import numpy as np

from PySide6.QtCore import QThread, Signal
from PySide6.QtWidgets import (
    QCheckBox,
    QComboBox,
    QHBoxLayout,
    QLabel,
    QMessageBox,
    QTextEdit,
    QVBoxLayout,
)

from app.core.database import get_session
from app.core.logger import get_logger
from app.core.config_manager import load as load_config
from app.models.device import Device
from app.modules.showroom.voice_actions import handle_transcript

from app.ui_comp.base import (
    BaseButton,
    BaseCard,
    BasePage,
)

logger = get_logger(__name__)

SAMPLE_RATE = 16000
CHUNK_SECONDS = 4


# ==========================================================
# Transcription Worker
# ==========================================================


class TranscriptionWorker(QThread):

    transcript_ready = Signal(str)
    error = Signal(str)
    status_changed = Signal(str)

    def __init__(self, runtime=None):
        super().__init__()

        self.runtime = runtime
        self._running = False
        self._model = None

    def stop(self):
        self._running = False

    def run(self):
        try:
            import sounddevice as sd
            from faster_whisper import WhisperModel

        except ImportError as error:
            self.error.emit(f"Missing dependency:\n{error}")
            return

        cfg = load_config("voice")

        model_size = cfg.get("model", "small")
        language = cfg.get("language", "auto")
        language = None if language == "auto" else language

        self.status_changed.emit(f"Loading Whisper ({model_size})...")

        try:
            self._model = WhisperModel(
                model_size,
                compute_type="int8",
            )

        except Exception as error:
            self.error.emit(f"Unable to load model:\n{error}")
            return

        self.status_changed.emit("Listening...")
        self._running = True

        audio_queue = queue.Queue()

        def audio_callback(indata, frames, time_info, status):
            if status:
                logger.warning(status)

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

                    buffer = np.concatenate(
                        [
                            buffer,
                            data,
                        ],
                        axis=0,
                    )

                    if len(buffer) < chunk_samples:
                        continue

                    audio = buffer[:chunk_samples, 0]
                    buffer = buffer[chunk_samples:]

                    segments, _ = self._model.transcribe(
                        audio,
                        language=language,
                        beam_size=1,
                    )

                    text = " ".join(
                        segment.text.strip()
                        for segment in segments
                    ).strip()

                    if text:
                        self.transcript_ready.emit(text)

        except Exception as error:
            self.error.emit(f"Audio Error:\n{error}")

        finally:
            self.status_changed.emit("Stopped")


# ==========================================================
# Voice Page
# ==========================================================


class VoicePage(BasePage):

    def __init__(self, runtime=None):
        super().__init__()

        self.runtime = runtime
        self.worker = None
        self._device_ips = []

        self.build_ui()
        self.refresh_devices()

    # ------------------------------------------------------
    # UI
    # ------------------------------------------------------

    def build_ui(self):
        main_layout = self.layout()

        if main_layout is None:
            main_layout = QVBoxLayout()
            self.setLayout(main_layout)

        main_layout.setContentsMargins(24, 24, 24, 24)
        main_layout.setSpacing(16)

        # ---------------- Header ----------------

        header_layout = QHBoxLayout()

        title_box = QVBoxLayout()
        title_box.setSpacing(4)

        title = QLabel("Voice Control")
        title.setObjectName("PageTitle")

        subtitle = QLabel(
            "Test wakeup commands, product keywords, LED trigger and media playback"
        )
        subtitle.setObjectName("PageSubtitle")

        title_box.addWidget(title)
        title_box.addWidget(subtitle)

        header_layout.addLayout(title_box)
        header_layout.addStretch()

        self.refresh_btn = BaseButton("Refresh Devices")
        self.refresh_btn.clicked.connect(self.refresh_devices)

        header_layout.addWidget(self.refresh_btn)

        main_layout.addLayout(header_layout)

        # ---------------- Device Card ----------------

        device_card = BaseCard(
            "Target ESP32",
            "Select the controller that should receive LED commands",
        )

        device_layout = QVBoxLayout()
        device_layout.setSpacing(12)

        device_row = QHBoxLayout()
        device_row.setSpacing(12)

        device_row.addWidget(QLabel("Target Device"))

        self.device_combo = QComboBox()
        device_row.addWidget(self.device_combo, 1)

        device_layout.addLayout(device_row)

        self.auto_trigger_checkbox = QCheckBox(
            "Automatically trigger product actions"
        )
        self.auto_trigger_checkbox.setChecked(True)

        device_layout.addWidget(self.auto_trigger_checkbox)

        help_text = QLabel(
            "Test flow: say 'Hello' or 'Vanga Sir' first, then say "
            "'show sesame oil', 'show groundnut oil', 'show coconut oil', or 'show mustard oil'."
        )
        help_text.setWordWrap(True)
        help_text.setObjectName("MutedText")

        device_layout.addWidget(help_text)

        device_card.add_layout(device_layout)
        main_layout.addWidget(device_card)

        # ---------------- Controls Card ----------------

        controls_card = BaseCard(
            "Listening Control",
            "Start or stop live microphone transcription",
        )

        controls_layout = QVBoxLayout()
        controls_layout.setSpacing(12)

        button_row = QHBoxLayout()
        button_row.setSpacing(10)

        self.start_btn = BaseButton("Start Listening")
        self.stop_btn = BaseButton("Stop")
        self.clear_btn = BaseButton("Clear Transcript")

        self.stop_btn.setEnabled(False)

        self.start_btn.clicked.connect(self.start_listening)
        self.stop_btn.clicked.connect(self.stop_listening)
        self.clear_btn.clicked.connect(self.clear_transcript)

        button_row.addWidget(self.start_btn)
        button_row.addWidget(self.stop_btn)
        button_row.addWidget(self.clear_btn)
        button_row.addStretch()

        controls_layout.addLayout(button_row)

        self.status_label = QLabel("Idle")
        self.status_label.setObjectName("MutedText")

        controls_layout.addWidget(self.status_label)

        controls_card.add_layout(controls_layout)
        main_layout.addWidget(controls_card)

        # ---------------- Transcript Card ----------------

        transcript_card = BaseCard(
            "Live Transcript",
            "Recognized speech and action result",
        )

        transcript_layout = QVBoxLayout()
        transcript_layout.setSpacing(12)

        self.transcript_log = QTextEdit()
        self.transcript_log.setReadOnly(True)

        transcript_layout.addWidget(self.transcript_log)

        transcript_card.add_layout(transcript_layout)
        main_layout.addWidget(transcript_card, 1)

    # ------------------------------------------------------
    # Device
    # ------------------------------------------------------

    def refresh_devices(self):
        session = get_session()

        try:
            devices = (
                session.query(Device)
                .order_by(Device.id.asc())
                .all()
            )

            self.device_combo.clear()
            self._device_ips.clear()

            for device in devices:
                ip = device.ip or ""
                name = device.device_name or "ESP32"
                status = device.status or "unknown"

                label = f"{name} ({ip})"

                if status.lower() == "connected":
                    label += " ✓"

                self.device_combo.addItem(label)
                self._device_ips.append(ip)

        finally:
            session.close()

    def selected_ip(self):
        index = self.device_combo.currentIndex()

        if index < 0:
            return None

        if index >= len(self._device_ips):
            return None

        ip = self._device_ips[index]

        if not ip:
            return None

        return ip

    # ------------------------------------------------------
    # Listening
    # ------------------------------------------------------

    def start_listening(self):
        if self.worker and self.worker.isRunning():
            return

        self.worker = TranscriptionWorker(self.runtime)

        self.worker.transcript_ready.connect(self.on_transcript)
        self.worker.status_changed.connect(self.on_status)
        self.worker.error.connect(self.on_error)

        self.worker.start()

        self.start_btn.setEnabled(False)
        self.stop_btn.setEnabled(True)

        self.log("🎙 Starting microphone...")

    def stop_listening(self):
        if self.worker:
            self.worker.stop()

        self.start_btn.setEnabled(True)
        self.stop_btn.setEnabled(False)

        self.status_label.setText("Stopping...")
        self.log("🛑 Stopping listener...")

    def on_status(self, status):
        self.status_label.setText(status)

        if status == "Listening...":
            self.log("✅ Listening started. Say wakeup command.")

        if status == "Stopped":
            self.start_btn.setEnabled(True)
            self.stop_btn.setEnabled(False)
            self.log("🛑 Listening stopped.")

    def on_error(self, message):
        QMessageBox.critical(
            self,
            "Voice Error",
            message,
        )

        self.start_btn.setEnabled(True)
        self.stop_btn.setEnabled(False)

        self.status_label.setText("Error")
        self.log(f"❌ {message}")

    # ------------------------------------------------------
    # Transcript Handling
    # ------------------------------------------------------

    def on_transcript(self, text):
        self.log(f"> {text}")

        if not self.auto_trigger_checkbox.isChecked():
            self.log("Auto trigger disabled.")
            return

        ip = self.selected_ip()

        if not ip:
            self.log("⚠ No ESP32 selected.")
            return

        result = handle_transcript(
            text,
            ip,
            runtime=self.runtime,
        )

        if not result:
            return

        status = result.get("status")
        message = result.get("message", "")

        if status == "wakeup":
            self.log("✅ Wakeup detected. Say product name now.")

        elif status == "waiting_wakeup":
            self.log("⏳ Waiting for wakeup command.")

        elif status == "product_matched":
            self.log(f"✅ Product: {result.get('product')}")
            self.log(f"💡 LED Effect: {result.get('effect')}")
            self.log(f"📺 Media: {result.get('media')}")

            if result.get("led_ok"):
                self.log("✅ LED command sent.")
            else:
                self.log("⚠ LED command failed.")

            if result.get("media_ok"):
                self.log("✅ Media playback started.")
            else:
                self.log("⚠ Media playback not started.")

        elif status == "no_product":
            self.log(f"❌ {message}")

        elif status == "empty":
            self.log("No speech detected.")

        else:
            self.log(message)

    # ------------------------------------------------------
    # Helpers
    # ------------------------------------------------------

    def log(self, message):
        self.transcript_log.append(message)
        self.transcript_log.ensureCursorVisible()

    def clear_transcript(self):
        self.transcript_log.clear()

    def closeEvent(self, event):
        if self.worker and self.worker.isRunning():
            self.worker.stop()
            self.worker.wait(1500)

        event.accept()