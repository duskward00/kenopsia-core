# Sprint 1 / Milestone 2: Assessment Framework Foundation

This milestone introduces the new internal assessment framework for Kenopsia Core.

It does **not** replace the existing v0.1.0 runtime yet. Instead, it adds the core foundation that future milestones will integrate into the CLI, collectors, and renderers.

## Added

```text
kenopsia/assessment/
├── __init__.py
├── engine.py
├── findings.py
├── inventory.py
├── recommendations.py
├── registry.py
├── scoring.py
└── rules/
    ├── __init__.py
    ├── security.py
    └── storage.py
```

## Architecture Introduced

```text
Collectors
    │
Normalized Inventory
    │
Rules
    │
Findings
    │
Recommendations
    │
Scoring
    │
Renderers
```

## Why This Matters

The original v0.1.0 engine relies heavily on collectors producing opinionated output.

This milestone begins moving Kenopsia toward a cleaner model:

- Collectors collect facts.
- Rules assess facts.
- Findings explain risks.
- Recommendations provide action.
- Scoring is derived from findings.

## Notable Behavior

The initial storage rule explicitly ignores virtual and pseudo filesystems such as:

- `efivarfs`
- `proc`
- `sysfs`
- `tmpfs`
- `squashfs`
- `overlay`

This prevents the false positive discovered when `/sys/firmware/efi/efivars` appeared full during early v0.2.x testing.

## Validation

After applying the overlay, run:

```bash
cd ~/Git/kenopsia-core

python3 -m venv .venv
source .venv/bin/activate

pip install -r requirements.txt
pip install pytest

pytest
./scripts/validate.sh
./scripts/run.sh
```

## Next Milestone

Sprint 1 / Milestone 3 will begin connecting existing collectors to the normalized inventory model.
