#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
python -m py_compile kenopsia.py kenopsia/*.py collectors/*.py
echo "Validation passed."
