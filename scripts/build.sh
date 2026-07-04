#!/usr/bin/env bash
set -euo pipefail
./scripts/validate.sh
python kenopsia.py
