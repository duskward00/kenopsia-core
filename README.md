# Kenopsia Core

**Professional Linux System Assessment Platform**

Kenopsia Core inventories, audits, scores, and explains a Linux system through a static HTML report and structured JSON output.

> Every system has a story.

## Quick Start

```bash
cd ~/Git/kenopsia-core
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
./scripts/validate.sh
./scripts/run.sh
xdg-open reports/kenopsia-report.html
```

## Generated Output

```text
reports/kenopsia-report.html
reports/kenopsia-report.json
history/<timestamp>.json
```

## Current Scope

- System inventory
- Hardware inventory
- Memory inventory
- Network inventory
- Services and listening socket summary
- Security audit
- Storage and SMART summary
- Fedora package intelligence
- Health scoring
- Findings and recommendations

## CLI

```bash
python kenopsia.py
python -m kenopsia.cli
```

Future installable CLI target:

```bash
kenopsia
```
