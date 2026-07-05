#!/usr/bin/env bash
set -euo pipefail
export PYTHONPATH="${PWD}:${PYTHONPATH:-}"
python -m kenopsia.cli assess --out reports
