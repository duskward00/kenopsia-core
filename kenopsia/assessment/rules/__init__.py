"""
Built-in assessment rules.
"""

from .security import security_rules
from .services import services_rules
from .storage import storage_rules

__all__ = ["security_rules", "services_rules", "storage_rules"]
