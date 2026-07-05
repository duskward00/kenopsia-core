# Sprint 1 / Milestone 4: Runtime Integration

Milestone 4 adds the first runnable normalized assessment path.

## Added

```text
kenopsia/runtime/
├── __init__.py
└── normalized.py

kenopsia/rendering/
├── normalized_html.py
├── normalized_json.py
└── normalized_markdown.py

scripts/run_normalized_assessment.py
```

## What It Does

This milestone runs:

```text
legacy payload JSON
    ↓
normalized Inventory
    ↓
assessment rules
    ↓
findings
    ↓
score
    ↓
HTML / JSON / Markdown reports
```

The existing CLI remains unchanged for now.
