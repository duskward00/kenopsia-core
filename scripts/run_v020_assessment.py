#!/usr/bin/env python3
"""Run Kenopsia Core v0.2.0 local assessment and write JSON/Markdown output."""

from __future__ import annotations

import argparse
import json
import socket
from datetime import datetime, timezone
from pathlib import Path

from kenopsia.assessment import run_assessment
from kenopsia.collectors import security, storage
from kenopsia.rendering.assessment_markdown import render_assessment_markdown


def main() -> int:
    parser = argparse.ArgumentParser(description="Run Kenopsia Core v0.2.0 assessment")
    parser.add_argument("--out", default="output", help="Output directory")
    args = parser.parse_args()

    out_dir = Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)

    hostname = socket.gethostname()
    collected = {
        "metadata": {
            "hostname": hostname,
            "collected_at": datetime.now(timezone.utc).isoformat(),
            "kenopsia_version": "0.2.0",
        },
        **storage.collect(),
        **security.collect(),
    }
    assessment = run_assessment(collected).to_dict()
    payload = {"collected": collected, "assessment": assessment}

    json_path = out_dir / f"kenopsia-assessment-{hostname}.json"
    md_path = out_dir / f"kenopsia-assessment-{hostname}.md"
    json_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    md_path.write_text(render_assessment_markdown(hostname, assessment), encoding="utf-8")

    print(f"Wrote {json_path}")
    print(f"Wrote {md_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
