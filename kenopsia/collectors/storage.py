"""Storage collector for Kenopsia Core v0.2.0."""

from __future__ import annotations

import shutil
from pathlib import Path
from typing import Any


def _read_mounts() -> list[dict[str, str]]:
    mounts: list[dict[str, str]] = []
    proc_mounts = Path("/proc/mounts")
    if not proc_mounts.exists():
        return mounts

    for line in proc_mounts.read_text(encoding="utf-8", errors="replace").splitlines():
        parts = line.split()
        if len(parts) < 3:
            continue
        source, target, fstype = parts[:3]
        if fstype in {"proc", "sysfs", "devtmpfs", "devpts", "tmpfs", "cgroup", "cgroup2", "overlay", "squashfs"}:
            continue
        mounts.append({"source": source, "mount": target.replace("\\040", " "), "fstype": fstype})
    return mounts


def collect() -> dict[str, Any]:
    """Collect local filesystem capacity details."""

    filesystems: list[dict[str, Any]] = []
    seen: set[str] = set()

    for mount in _read_mounts():
        target = mount["mount"]
        if target in seen:
            continue
        seen.add(target)
        try:
            usage = shutil.disk_usage(target)
        except OSError:
            continue
        used = usage.total - usage.free
        used_percent = round((used / usage.total) * 100, 2) if usage.total else 0.0
        filesystems.append(
            {
                "source": mount["source"],
                "mount": target,
                "fstype": mount["fstype"],
                "total_bytes": usage.total,
                "used_bytes": used,
                "free_bytes": usage.free,
                "used_percent": used_percent,
            }
        )

    return {"filesystems": filesystems}
