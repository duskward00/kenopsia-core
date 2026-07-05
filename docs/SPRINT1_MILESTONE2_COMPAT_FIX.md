# Sprint 1 / Milestone 2 Compatibility Fix

Milestone 2 introduced the new assessment framework but accidentally replaced
the existing `kenopsia.assessment` public interface.

The current CLI still imports:

```python
from kenopsia.assessment import run_assessment
```

This compatibility fix restores that interface while keeping the new framework.

## Fixes

- Restores `run_assessment()`
- Restores `AssessmentFinding`
- Adds `LegacyAssessmentResult`
- Keeps the new `AssessmentEngine`
- Keeps normalized inventory, findings, scoring, recommendations, and rule registry
- Adds `tests/conftest.py` so local pytest runs can import `kenopsia` reliably

## Apply

```bash
cd ~/Git/kenopsia-core

mkdir -p /tmp/kenopsia-m2-compat
unzip -o ~/Downloads/kenopsia-core-v0.2.2-sprint1-m2-compat.zip -d /tmp/kenopsia-m2-compat

cp -rv /tmp/kenopsia-m2-compat/kenopsia/* kenopsia/
cp -rv /tmp/kenopsia-m2-compat/tests/* tests/
cp -rv /tmp/kenopsia-m2-compat/docs/* docs/

rm -rf /tmp/kenopsia-m2-compat

source .venv/bin/activate

pytest
./scripts/validate.sh
./scripts/run.sh
```
