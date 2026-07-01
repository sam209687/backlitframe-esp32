"""
app/models/__init__.py

Import all models here so SQLAlchemy's mapper registry has every class
registered before any query runs. This is required because several
models reference each other by string name in relationship(), e.g.
Device.customer = relationship("Customer"). If a query on one model
runs before the others are imported, SQLAlchemy raises:

    InvalidRequestError: failed to locate a name ('Customer')

Importing this package (or any single model through it) guarantees
all classes are registered together.
"""

from app.models.customer import Customer  # noqa: F401
from app.models.feature import Feature, CustomerFeature  # noqa: F401
from app.models.device import Device  # noqa: F401
from app.models.product import Product  # noqa: F401
from app.models.schedule import Schedule  # noqa: F401