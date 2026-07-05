from __future__ import annotations

from ..findings import Finding, Severity
from ..inventory import Inventory

IGNORED_FILESYSTEM_TYPES = {
    "autofs",
    "cgroup",
    "cgroup2",
    "debugfs",
    "devpts",
    "devtmpfs",
    "efivarfs",
    "fusectl",
    "hugetlbfs",
    "mqueue",
    "overlay",
    "proc",
    "pstore",
    "securityfs",
    "squashfs",
    "sysfs",
    "tmpfs",
    "tracefs",
}

ASSESSED_FILESYSTEM_TYPES = {
    "btrfs",
    "ext2",
    "ext3",
    "ext4",
    "f2fs",
    "ntfs",
    "xfs",
    "zfs",
}


def storage_capacity_rule(inventory: Inventory) -> list[Finding]:
    storage = inventory.data_for("storage", {})
    filesystems = storage.get("filesystems", [])

    findings: list[Finding] = []

    for fs in filesystems:
        fs_type = str(fs.get("type", "")).lower()
        mount = fs.get("mount", "unknown")
        used_percent = fs.get("used_percent")

        if fs_type in IGNORED_FILESYSTEM_TYPES:
            continue

        if fs_type and fs_type not in ASSESSED_FILESYSTEM_TYPES:
            continue

        if used_percent is None:
            continue

        try:
            used = float(used_percent)
        except (TypeError, ValueError):
            continue

        if used >= 95:
            severity = Severity.CRITICAL
            title = f"Filesystem {mount} is critically full"
        elif used >= 90:
            severity = Severity.HIGH
            title = f"Filesystem {mount} is nearly full"
        elif used >= 80:
            severity = Severity.MEDIUM
            title = f"Filesystem {mount} usage is elevated"
        else:
            continue

        findings.append(
            Finding(
                id=f"storage.capacity.{mount}".replace("/", "_").strip("_") or "root",
                category="storage",
                severity=severity,
                title=title,
                description=f"Filesystem {mount} is {used:.1f}% utilized.",
                recommendation="Free space, expand the filesystem, or move data before services become unstable.",
                evidence=fs,
                source="storage_capacity_rule",
            )
        )

    return findings


storage_rules = [storage_capacity_rule]
