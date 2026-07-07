"""
voice_page.py

Live microphone -> faster-whisper transcription.

The recognized speech is displayed in the UI and can be forwarded
to the Showroom Runtime.

Runs completely in a background thread so the UI never freezes.
"""

import queue
import numpy as np

from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QTextEdit,
    QComboBox,
    QCheckBox,
    QMessageBox,
)

from PySide6.QtCore import (
    QThread,
    Signal,
)

from app.core.database import get_session
from app.core.logger import get_logger
from app.core.config_manager import load as load_config
from app.models.device import Device
from app.modules.showroom.voice_actions import handle_transcript

logger = get_logger(__name__)

SAMPLE_RATE = 16000
CHUNK_SECONDS = 4


# ==========================================================
# Whisper Worker
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

    # -----------------------------------------------------

    def stop(self):

        self._running = False

    # -----------------------------------------------------

    def run(self):

        try:

            import sounddevice as sd

            from faster_whisper import WhisperModel

        except ImportError as e:

            self.error.emit(
                f"Missing dependency:\n{e}"
            )

            return

        cfg = load_config("voice")

        model_size = cfg.get(
            "model",
            "small"
        )

        language = cfg.get(
            "language",
            "auto"
        )

        language = None if language == "auto" else language

        self.status_changed.emit(
            f"Loading Whisper ({model_size})..."
        )

        try:

            self._model = WhisperModel(
                model_size,
                compute_type="int8"
            )

        except Exception as e:

            self.error.emit(
                f"Unable to load model:\n{e}"
            )

            return

        self.status_changed.emit(
            "Listening..."
        )

        self._running = True

        audio_queue = queue.Queue()

        def audio_callback(indata, frames, time_info, status):

            if status:

                logger.warning(status)

            audio_queue.put(
                indata.copy()
            )

        try:

            with sd.InputStream(

                samplerate=SAMPLE_RATE,

                channels=1,

                dtype="float32",

                callback=audio_callback,

            ):

                buffer = np.zeros(
                    (0, 1),
                    dtype="float32"
                )

                chunk_samples = SAMPLE_RATE * CHUNK_SECONDS

                while self._running:

                    try:

                        data = audio_queue.get(
                            timeout=0.5
                        )

                    except queue.Empty:

                        continue

                    buffer = np.concatenate(
                        [buffer, data],
                        axis=0
                    )

                    if len(buffer) < chunk_samples:

                        continue

                    audio = buffer[:chunk_samples, 0]

                    buffer = buffer[chunk_samples:]

                    segments, _ = self._model.transcribe(

                        audio,

                        language=language,

                        beam_size=1

                    )

                    text = " ".join(
                        s.text.strip()
                        for s in segments
                    ).strip()

                    if text:

                        self.transcript_ready.emit(
                            text
                        )

        except Exception as e:

            self.error.emit(
                f"Audio Error:\n{e}"
            )

        finally:

            self.status_changed.emit(
                "Stopped"
            )


# ==========================================================
# Voice Page
# ==========================================================


class VoicePage(QWidget):

    def __init__(self, runtime=None):

        super().__init__()

        self.runtime = runtime

        self.worker = None

        self._device_ips = []

        self.build_ui()

        self.refresh_devices()

    # -----------------------------------------------------

    def build_ui(self):

        layout = QVBoxLayout()

        title = QLabel("Voice Control")

        title.setStyleSheet("""
            font-size:20px;
            font-weight:bold;
        """)

        layout.addWidget(title)

        # ---------------- Device ----------------

        row = QHBoxLayout()

        row.addWidget(
            QLabel("Target Device")
        )

        self.device_combo = QComboBox()

        row.addWidget(
            self.device_combo
        )

        refresh = QPushButton(
            "Refresh"
        )

        refresh.clicked.connect(
            self.refresh_devices
        )

        row.addWidget(
            refresh
        )

        row.addStretch()

        layout.addLayout(row)

        # ---------------- Checkbox ----------------

        self.auto_trigger_checkbox = QCheckBox(
            "Automatically trigger product actions"
        )

        self.auto_trigger_checkbox.setChecked(
            True
        )

        layout.addWidget(
            self.auto_trigger_checkbox
        )

        # ---------------- Buttons ----------------

        row = QHBoxLayout()

        self.start_btn = QPushButton(
            "Start Listening"
        )

        self.stop_btn = QPushButton(
            "Stop"
        )

        self.stop_btn.setEnabled(False)

        self.start_btn.clicked.connect(
            self.start_listening
        )

        self.stop_btn.clicked.connect(
            self.stop_listening
        )

        row.addWidget(
            self.start_btn
        )

        row.addWidget(
            self.stop_btn
        )

        row.addStretch()

        layout.addLayout(row)

        # ---------------- Status ----------------

        self.status_label = QLabel(
            "Idle"
        )

        layout.addWidget(
            self.status_label
        )

        # ---------------- Transcript ----------------

        layout.addWidget(
            QLabel("Transcript")
        )

        self.transcript_log = QTextEdit()

        self.transcript_log.setReadOnly(True)

        layout.addWidget(
            self.transcript_log
        )

        self.setLayout(layout)

    # -----------------------------------------------------

    def refresh_devices(self):

        session = get_session()

        try:

            devices = session.query(
                Device
            ).all()

            self.device_combo.clear()

            self._device_ips.clear()

            for device in devices:

                self.device_combo.addItem(
                    f"{device.device_name} ({device.ip})"
                )

                self._device_ips.append(
                    device.ip
                )

        finally:

            session.close()

    # -----------------------------------------------------

    def selected_ip(self):

        index = self.device_combo.currentIndex()

        if index < 0:

            return None

        if index >= len(self._device_ips):

            return None

        return self._device_ips[index]

    # -----------------------------------------------------

    def start_listening(self):

        if self.worker and self.worker.isRunning():

            return

        self.worker = TranscriptionWorker(
            self.runtime
        )

        self.worker.transcript_ready.connect(
            self.on_transcript
        )

        self.worker.status_changed.connect(
            self.on_status
        )

        self.worker.error.connect(
            self.on_error
        )

        self.worker.start()

        self.start_btn.setEnabled(False)

        self.stop_btn.setEnabled(True)

    # -----------------------------------------------------

    def stop_listening(self):

        if self.worker:

            self.worker.stop()

        self.start_btn.setEnabled(True)

        self.stop_btn.setEnabled(False)

        self.status_label.setText(
            "Stopping..."
        )

    # -----------------------------------------------------

    def on_status(self, status):

        self.status_label.setText(
            status
        )

    # -----------------------------------------------------

    def on_error(self, message):

        QMessageBox.critical(
            self,
            "Voice Error",
            message
        )

        self.start_btn.setEnabled(True)

        self.stop_btn.setEnabled(False)

        self.status_label.setText(
            "Error"
        )

    # -----------------------------------------------------

    def on_transcript(self, text):

        self.transcript_log.append(
            f"> {text}"
        )

        # Future Runtime Integration
        if (
            self.runtime
            and hasattr(self.runtime, "manager")
            and hasattr(self.runtime.manager, "on_wakeup")
        ):
            pass

        if self.auto_trigger_checkbox.isChecked():

            ip = self.selected_ip()

            if ip:

                handle_transcript(
                    text,
                    ip
                )

            else:

                self.transcript_log.append(
                    "No ESP32 selected."
                )