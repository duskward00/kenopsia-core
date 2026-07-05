"""
Normalization helpers for Kenopsia Core.

Milestone 3 introduces adapter functions that convert existing collector
payloads into the normalized Inventory model introduced in Milestone 2.
"""

from .adapters import inventory_from_payload
from .storage import normalize_storage
from .security import normalize_security
from .services import normalize_services

__all__ = [
    "inventory_from_payload",
    "normalize_security",
    "normalize_services",
    "normalize_storage",
]
