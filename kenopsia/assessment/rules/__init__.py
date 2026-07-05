"""
Built-in assessment rules.

Milestone 2 only introduces the rule structure and a small starter set.
Future milestones will expand these rules and connect them to real collectors.
"""

from .storage import storage_rules
from .security import security_rules

__all__ = ["storage_rules", "security_rules"]
