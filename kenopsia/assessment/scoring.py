from __future__ import annotations

from dataclasses import dataclass, field

from .findings import Finding


@dataclass(frozen=True)
class AssessmentScore:
    """Assessment score summary."""

    overall: int
    grade: str
    label: str
    categories: dict[str, int] = field(default_factory=dict)

    def as_dict(self) -> dict:
        return {
            "overall": self.overall,
            "grade": self.grade,
            "label": self.label,
            "categories": self.categories,
        }


def grade_for(score: int) -> str:
    if score >= 95:
        return "A+"
    if score >= 90:
        return "A"
    if score >= 80:
        return "B"
    if score >= 70:
        return "C"
    if score >= 60:
        return "D"
    return "F"


def label_for(score: int) -> str:
    if score >= 90:
        return "Healthy"
    if score >= 80:
        return "Good"
    if score >= 70:
        return "Needs Attention"
    if score >= 60:
        return "Degraded"
    return "At Risk"


def calculate_score(findings: list[Finding]) -> AssessmentScore:
    """
    Calculate transparent scores from finding penalties.

    This deliberately starts simple:
    - each category begins at 100
    - findings subtract severity-based penalties
    - category scores cannot drop below zero
    - overall score is the average category score

    Future milestones may add category weighting.
    """

    if not findings:
        return AssessmentScore(overall=100, grade="A+", label="Healthy", categories={})

    categories: dict[str, int] = {}

    for finding in findings:
        categories.setdefault(finding.category, 100)
        categories[finding.category] = max(0, categories[finding.category] - finding.penalty())

    overall = round(sum(categories.values()) / len(categories))
    return AssessmentScore(
        overall=overall,
        grade=grade_for(overall),
        label=label_for(overall),
        categories=dict(sorted(categories.items())),
    )
