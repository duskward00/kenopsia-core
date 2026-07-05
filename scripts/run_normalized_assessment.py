#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path

from kenopsia.runtime import run_normalized_assessment
from kenopsia.rendering.normalized_html import render_normalized_html
from kenopsia.rendering.normalized_json import render_normalized_json
from kenopsia.rendering.normalized_markdown import render_normalized_markdown


def _load_payload(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    parser = argparse.ArgumentParser(description="Run the Kenopsia normalized assessment pipeline.")
    parser.add_argument(
        "--input",
        type=Path,
        required=True,
        help="Path to a collected legacy payload JSON file.",
    )
    parser.add_argument(
        "--reports-dir",
        type=Path,
        default=Path("reports"),
        help="Directory where normalized reports should be written.",
    )

    args = parser.parse_args()

    payload = _load_payload(args.input)
    result = run_normalized_assessment(payload)

    args.reports_dir.mkdir(parents=True, exist_ok=True)

    json_path = render_normalized_json(result, args.reports_dir / "kenopsia-normalized-report.json")
    md_path = render_normalized_markdown(result, args.reports_dir / "kenopsia-normalized-report.md")
    html_path = render_normalized_html(result, args.reports_dir / "kenopsia-normalized-report.html")

    print(f"Normalized assessment score: {result.score.overall} ({result.score.grade})")
    print(f"JSON report: {json_path}")
    print(f"Markdown report: {md_path}")
    print(f"HTML report: {html_path}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
