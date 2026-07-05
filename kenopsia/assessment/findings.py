from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any


class Severity(str, Enum):
    """Supported finding severity levels."""

    INFO = "info"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


SEVERITY_WEIGHTS: dict[Severity, int] = {
    Severity.INFO: 0,
    Severity.LOW: 2,
    Severity.MEDIUM: 5,
    Severity.HIGH: 10,
    Severity.CRITICAL: 20,
}


@dataclass(frozen=True)
class Finding:
    """
    A normalized assessment finding.

    Findings are the core evidence objects in Kenopsia Core. Collectors gather
    facts; rules evaluate those facts; findings describe what was discovered.
    """

    id: str
    category: str
    severity: Severity
    title: str
    description: str
    recommendation: str
    evidence: dict[str, Any] = field(default_factory=dict)
    confidence: float = 1.0
    source: str = "kenopsia"

    def penalty(self) -> int:
        """Return the score penalty associated with this finding."""
        return SEVERITY_WEIGHTS[self.severity]

    def as_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "category": self.category,
            "severity": self.severity.value,
            "title": self.title,
            "description": self.description,
            "recommendation": self.recommendation,
            "evidence": self.evidence,
            "confidence": self.confidence,
            "source": self.source,
            "penalty": self.penalty(),
        }
