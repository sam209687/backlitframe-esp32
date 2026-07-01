"""
license_service.py
Validates a customer's license_key and resolves their plan/features.
"""

from app.core.database import get_session
from app.core.logger import get_logger
from app.models.customer import Customer

logger = get_logger(__name__)


def validate_license(license_key: str) -> Customer | None:
    session = get_session()
    try:
        customer = session.query(Customer).filter_by(license_key=license_key).first()
        if not customer:
            logger.warning(f"Invalid license key: {license_key}")
        return customer
    finally:
        session.close()
