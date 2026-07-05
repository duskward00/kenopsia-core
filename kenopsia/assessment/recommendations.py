from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from .findings import Finding, Severity


@dataclass(frozen=True)
class Recommendation:
    """Actionable remediation guidance derived from one or more findings."""

    id: str
    title: str
    priority: Severity
    description: str
    actions: list[str] = field(default_factory=list)
    related_findings: list[str] = field(default_factory=list)
    evidence: dict[str, Any] = field(default_factory=dict)

    def as_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "title": self.title,
            "priority": self.priority.value,
            "description": self.description,
            "actions": self.actions,
            "related_findings": self.related_findings,
            "evidence": self.evidence,
        }


def recommendations_from_findings(findings: list[Finding]) -> list[Recommendation]:
    """
    Create a simple recommendation list from findings.

    Future milestones can replace this with a richer recommendation catalog.
    """

    recommendations: list[Recommendation] = []

    for finding in findings:
        recommendations.append(
            Recommendation(
                id=f"rec.{finding.id}",
                title=finding.title,
                priority=finding.severity,
                description=finding.recommendation,
                actions=[finding.recommendation],
                related_findings=[finding.id],
                evidence=finding.evidence,
            )
        )

    return recommendations
