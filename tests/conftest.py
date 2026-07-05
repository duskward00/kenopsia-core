"""
Test path bootstrap.

Some local development environments invoke pytest in ways that do not add the
repository root to sys.path consistently. Keep tests independent from whether
the package has been installed in editable mode.
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
