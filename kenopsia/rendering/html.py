"""Simple HTML report renderer for Kenopsia Core."""
from __future__ import annotations

from html import escape
from typing import Any


def render_html_report(payload: dict[str, Any]) -> str:
    collected = payload.get("collected", {})
    assessment = payload.get("assessment", {})
    meta = collected.get("metadata", {})
    findings = assessment.get("findings", [])
    rows = []
    for finding in findings:
        rows.append(
            "<tr>"
            f"<td>{escape(str(finding.get('severity','')))}</td>"
            f"<td>{escape(str(finding.get('category','')))}</td>"
            f"<td>{escape(str(finding.get('title','')))}</td>"
            f"<td>{escape(str(finding.get('recommendation','')))}</td>"
            "</tr>"
        )
    if not rows:
        rows.append('<tr><td colspan="4">No findings detected.</td></tr>')

    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>Kenopsia Core Assessment</title>
  <style>
    body {{ font-family: system-ui, sans-serif; margin: 2rem; line-height: 1.45; }}
    .card {{ border: 1px solid #ddd; border-radius: 12px; padding: 1rem; margin-bottom: 1rem; }}
    table {{ border-collapse: collapse; width: 100%; }}
    th, td {{ border-bottom: 1px solid #ddd; padding: .6rem; text-align: left; vertical-align: top; }}
    th {{ background: #f6f6f6; }}
    .score {{ font-size: 2rem; font-weight: 700; }}
  </style>
</head>
<body>
  <h1>Kenopsia Core Assessment</h1>
  <div class="card">
    <div><strong>Host:</strong> {escape(str(meta.get('hostname', 'unknown')))}</div>
    <div><strong>Collected:</strong> {escape(str(meta.get('collected_at', 'unknown')))}</div>
    <div><strong>Version:</strong> {escape(str(meta.get('kenopsia_version', 'unknown')))}</div>
  </div>
  <div class="card">
    <div class="score">Score: {escape(str(assessment.get('score', 'n/a')))} / Grade: {escape(str(assessment.get('grade', 'n/a')))}</div>
  </div>
  <h2>Findings</h2>
  <table>
    <thead><tr><th>Severity</th><th>Category</th><th>Finding</th><th>Recommendation</th></tr></thead>
    <tbody>{''.join(rows)}</tbody>
  </table>
</body>
</html>
"""
