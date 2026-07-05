#!/usr/bin/env bash
set -euo pipefail
export PYTHONPATH="${PWD}:${PYTHONPATH:-}"
python -m compileall kenopsia scripts tests
python -m pytest -q
python -m kenopsia.cli --version
