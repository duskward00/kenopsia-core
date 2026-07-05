"""Kenopsia Core command line interface."""
from __future__ import annotations

import argparse
import json
import socket
from datetime import datetime, timezone
from pathlib import Path

from kenopsia import __version__
from kenopsia.assessment import run_assessment
from kenopsia.collectors import security, storage
from kenopsia.rendering.assessment_markdown import render_assessment_markdown
from kenopsia.rendering.html import render_html_report


def collect_payload() -> dict:
    hostname = socket.gethostname()
    collected = {
        "metadata": {
            "hostname": hostname,
            "collected_at": datetime.now(timezone.utc).isoformat(),
            "kenopsia_version": __version__,
        },
        **storage.collect(),
        **security.collect(),
    }
    assessment = run_assessment(collected).to_dict()
    return {"collected": collected, "assessment": assessment}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="kenopsia", description="Kenopsia Core Linux assessment platform")
    parser.add_argument("--version", action="store_true", help="Show version and exit")
    subparsers = parser.add_subparsers(dest="command")
    assess = subparsers.add_parser("assess", help="Run local assessment")
    assess.add_argument("--out", default="reports", help="Output directory")
    args = parser.parse_args(argv)

    if args.version:
        print(f"Kenopsia Core v{__version__}")
        return 0

    if args.command in {None, "assess"}:
        out_dir = Path(getattr(args, "out", "reports"))
        out_dir.mkdir(parents=True, exist_ok=True)
        payload = collect_payload()
        hostname = payload["collected"]["metadata"]["hostname"]
        (out_dir / f"kenopsia-assessment-{hostname}.json").write_text(json.dumps(payload, indent=2), encoding="utf-8")
        (out_dir / f"kenopsia-assessment-{hostname}.md").write_text(render_assessment_markdown(hostname, payload["assessment"]), encoding="utf-8")
        (out_dir / "kenopsia-report.html").write_text(render_html_report(payload), encoding="utf-8")
        print(f"Kenopsia Core v{__version__}")
        print(f"Assessment score: {payload['assessment']['score']} ({payload['assessment']['grade']})")
        print(f"Report: {out_dir / 'kenopsia-report.html'}")
        return 0

    parser.print_help()
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
