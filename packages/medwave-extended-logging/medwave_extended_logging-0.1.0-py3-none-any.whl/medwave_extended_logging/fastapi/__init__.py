"""
Module for logging fastapi requests and responses.

Inspiration from https://github.com/azhig/fastapi-logging

Modified in many places and kept as minimal.
Included logging to database and excluded extensive console log support.
"""

from .utils import register_middleware  # noqa F401
from .utils import setup_logger  # noqa F401
