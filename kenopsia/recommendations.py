from __future__ import annotations
from .findings import dedupe


def merge(collectors: list[dict]) -> list[dict]:
    items = []
    for c in collectors:
        items.extend(c.get("recommendations", []))
    return dedupe(items)
