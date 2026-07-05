"""Markdown rendering helpers for v0.2.0 assessment output."""

from __future__ import annotations

from typing import Any


def render_assessment_markdown(hostname: str, assessment: dict[str, Any]) -> str:
    findings = assessment.get("findings", [])
    lines = [
        f"# Kenopsia Core Assessment — {hostname}",
        "",
        f"**Score:** {assessment.get('score', 'n/a')}/100  ",
        f"**Grade:** {assessment.get('grade', 'n/a')}",
        "",
        "## Findings",
        "",
    ]
    if not findings:
        lines.append("No assessment findings were generated.")
        return "\n".join(lines) + "\n"

    for finding in findings:
        lines.extend(
            [
                f"### {finding.get('title', 'Untitled finding')}",
                "",
                f"- **Severity:** {finding.get('severity', 'unknown')}",
                f"- **Category:** {finding.get('category', 'unknown')}",
                f"- **Summary:** {finding.get('summary', '')}",
                f"- **Recommendation:** {finding.get('recommendation', '')}",
                "",
            ]
        )
    return "\n".join(lines)
