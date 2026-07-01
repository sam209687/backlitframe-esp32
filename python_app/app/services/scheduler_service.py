"""
scheduler_service.py
Handles signboard on/off timing and other scheduled events, based on
the schedules table.
"""

from app.core.database import get_session
from app.core.logger import get_logger
from app.models.schedule import Schedule
from app.services.esp32_service import send_command

logger = get_logger(__name__)


def start_scheduler():
    logger.info("Scheduler service started.")
    # TODO: hook into APScheduler or a background thread that polls
    # the schedules table and fires send_command() at on_time/off_time.


def run_schedule(schedule: Schedule, device_ip: str):
    logger.info(f"Running schedule {schedule.id} for device {device_ip}")
    send_command(device_ip, {"schedule_type": schedule.type})
