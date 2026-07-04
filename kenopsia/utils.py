from __future__ import annotations
import subprocess
from pathlib import Path


def run(cmd: list[str], timeout: int = 15) -> str:
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
        return (r.stdout or r.stderr or "").strip()
    except Exception as exc:
        return f"Unavailable: {exc}"


def read(path: str, default: str = "Unavailable") -> str:
    try:
        return Path(path).read_text(errors="ignore").strip()
    except Exception:
        return default


def gb(value: float | int | None) -> float | None:
    if value is None:
        return None
    return round(float(value) / (1024 ** 3), 2)


def pct_label(value: float | int | None) -> str:
    if value is None:
        return "unknown"
    return f"{float(value):.1f}%"
