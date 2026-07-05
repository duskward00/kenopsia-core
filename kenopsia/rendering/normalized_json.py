from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def render_normalized_json(result: Any, output_path: str | Path) -> Path:
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(result.as_dict(), indent=2, sort_keys=True), encoding="utf-8")
    return path
