"""
feature_manager.py
Checks whether a feature (voice, led, display, signboard, etc.) is enabled
for a given customer, based on the customer_features table.

Usage:
    from app.core.feature_manager import feature_enabled

    if feature_enabled(customer_id=1, feature_name="voice"):
        start_voice()
"""

from app.core.database import get_session
from app.models.customer import Customer
from app.models.feature import Feature, CustomerFeature


def feature_enabled(customer_id: int, feature_name: str) -> bool:
    session = get_session()
    try:
        row = (
            session.query(CustomerFeature)
            .join(Feature, Feature.id == CustomerFeature.feature_id)
            .filter(
                CustomerFeature.customer_id == customer_id,
                Feature.name == feature_name,
            )
            .first()
        )
        return bool(row and row.enabled)
    finally:
        session.close()


def enabled_features(customer_id: int) -> list[str]:
    """Return a list of feature names enabled for a customer."""
    session = get_session()
    try:
        rows = (
            session.query(Feature.name)
            .join(CustomerFeature, CustomerFeature.feature_id == Feature.id)
            .filter(
                CustomerFeature.customer_id == customer_id,
                CustomerFeature.enabled.is_(True),
            )
            .all()
        )
        return [r[0] for r in rows]
    finally:
        session.close()


def set_feature(customer_id: int, feature_name: str, enabled: bool):
    """Enable/disable a feature for a customer (creates the row if missing)."""
    session = get_session()
    try:
        feature = session.query(Feature).filter_by(name=feature_name).first()
        if not feature:
            raise ValueError(f"Unknown feature: {feature_name}")

        cf = (
            session.query(CustomerFeature)
            .filter_by(customer_id=customer_id, feature_id=feature.id)
            .first()
        )
        if cf:
            cf.enabled = enabled
        else:
            cf = CustomerFeature(
                customer_id=customer_id, feature_id=feature.id, enabled=enabled
            )
            session.add(cf)
        session.commit()
    finally:
        session.close()
