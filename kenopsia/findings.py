from __future__ import annotations

SEVERITY_ORDER = {"critical": 0, "high": 1, "medium": 2, "low": 3, "info": 4}


def dedupe(items: list[dict]) -> list[dict]:
    seen = set()
    out = []
    for item in items:
        key = (item.get("severity"), item.get("title"), item.get("detail"))
        if key not in seen:
            seen.add(key)
            out.append(item)
    return sorted(out, key=lambda x: SEVERITY_ORDER.get(x.get("severity", "info"), 9))


def risk_counts(findings: list[dict]) -> dict:
    counts = {"critical": 0, "high": 0, "medium": 0, "low": 0, "info": 0}
    for f in findings:
        sev = f.get("severity", "info")
        counts[sev] = counts.get(sev, 0) + 1
    return counts
