from __future__ import annotations

from html import escape
from pathlib import Path
from typing import Any


def render_normalized_html(result: Any, output_path: str | Path) -> Path:
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)

    category_rows = ""
    if result.score.categories:
        category_rows = "\n".join(
            f"<tr><td>{escape(category)}</td><td>{score}</td></tr>"
            for category, score in result.score.categories.items()
        )
    else:
        category_rows = "<tr><td colspan='2'>No findings detected.</td></tr>"

    finding_rows = ""
    if result.findings:
        finding_rows = "\n".join(
            "<tr>"
            f"<td>{escape(finding.severity.value)}</td>"
            f"<td>{escape(finding.category)}</td>"
            f"<td>{escape(finding.title)}</td>"
            f"<td>{escape(finding.recommendation)}</td>"
            "</tr>"
            for finding in result.findings
        )
    else:
        finding_rows = "<tr><td colspan='4'>No findings detected.</td></tr>"

    html = f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>Kenopsia Core Normalized Assessment</title>
  <style>
    body {{ font-family: system-ui, sans-serif; margin: 2rem; line-height: 1.45; }}
    .card {{ border: 1px solid #ddd; border-radius: 12px; padding: 1rem; margin-bottom: 1rem; }}
    .score {{ font-size: 2rem; font-weight: 700; }}
    table {{ border-collapse: collapse; width: 100%; margin-bottom: 1.5rem; }}
    th, td {{ border-bottom: 1px solid #ddd; padding: .6rem; text-align: left; vertical-align: top; }}
    th {{ background: #f6f6f6; }}
  </style>
</head>
<body>
  <h1>Kenopsia Core Normalized Assessment</h1>

  <div class="card">
    <div><strong>Host:</strong> {escape(result.inventory.host)}</div>
    <div><strong>Generated:</strong> {escape(result.generated_at)}</div>
  </div>

  <div class="card">
    <div class="score">Score: {result.score.overall} / Grade: {escape(result.score.grade)}</div>
    <div>Status: {escape(result.score.label)}</div>
  </div>

  <h2>Category Scores</h2>
  <table>
    <thead><tr><th>Category</th><th>Score</th></tr></thead>
    <tbody>{category_rows}</tbody>
  </table>

  <h2>Findings</h2>
  <table>
    <thead><tr><th>Severity</th><th>Category</th><th>Finding</th><th>Recommendation</th></tr></thead>
    <tbody>{finding_rows}</tbody>
  </table>
</body>
</html>
"""

    path.write_text(html, encoding="utf-8")
    return path
