"""
Kenopsia Core assessment framework.

This package now exposes both:

1. The legacy v0.2.x `run_assessment()` interface used by the current CLI.
2. The Sprint 1 framework foundation used by the new assessment architecture.

This compatibility layer prevents Milestone 2 from breaking the existing
runtime while the project is being refactored in pieces.
"""

from .engine import (
    AssessmentEngine,
    AssessmentFinding,
    AssessmentResult,
    LegacyAssessmentResult,
    run_assessment,
)
from .findings import Finding, Severity
from .inventory import Inventory, InventorySection
from .recommendations import Recommendation
from .registry import RuleRegistry
from .scoring import AssessmentScore, calculate_score

__all__ = [
    "AssessmentEngine",
    "AssessmentFinding",
    "AssessmentResult",
    "AssessmentScore",
    "Finding",
    "Inventory",
    "InventorySection",
    "LegacyAssessmentResult",
    "Recommendation",
    "RuleRegistry",
    "Severity",
    "calculate_score",
    "run_assessment",
]
