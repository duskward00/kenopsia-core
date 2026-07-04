from __future__ import annotations


def overall_score(collectors: list[dict]) -> int:
    scores = [int(c.get("health", 0)) for c in collectors if c.get("health") is not None]
    if not scores:
        return 0
    return round(sum(scores) / len(scores))


def label(score: int) -> str:
    if score >= 90:
        return "Excellent"
    if score >= 75:
        return "Good"
    if score >= 60:
        return "Needs attention"
    return "At risk"


def score_class(score: int) -> str:
    if score >= 90:
        return "score-good"
    if score >= 75:
        return "score-warn"
    return "score-bad"
