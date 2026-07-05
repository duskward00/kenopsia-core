from __future__ import annotations

from pathlib import Path
from typing import Any


def render_normalized_markdown(result: Any, output_path: str | Path) -> Path:
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)

    score = result.score
    lines: list[str] = [
        "# Kenopsia Core Normalized Assessment",
        "",
        f"Generated: `{result.generated_at}`",
        f"Host: `{result.inventory.host}`",
        "",
        f"## Overall Score: {score.overall} ({score.grade})",
        "",
        f"Status: **{score.label}**",
        "",
        "## Category Scores",
        "",
    ]

    if score.categories:
        for category, category_score in score.categories.items():
            lines.append(f"- **{category}**: {category_score}")
    else:
        lines.append("- No findings detected.")

    lines.extend(["", "## Findings", ""])

    if result.findings:
        for finding in result.findings:
            lines.extend(
                [
                    f"### {finding.title}",
                    "",
                    f"- **Severity:** {finding.severity.value}",
                    f"- **Category:** {finding.category}",
                    f"- **Description:** {finding.description}",
                    f"- **Recommendation:** {finding.recommendation}",
                    "",
                ]
            )
    else:
        lines.append("No findings detected.")

    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return path
