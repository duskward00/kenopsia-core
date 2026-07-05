from __future__ import annotations

from typing import Any

from kenopsia.assessment import InventorySection

IGNORED_FILESYSTEM_TYPES = {
    "autofs",
    "binfmt_misc",
    "bpf",
    "cgroup",
    "cgroup2",
    "configfs",
    "debugfs",
    "devpts",
    "devtmpfs",
    "efivarfs",
    "fusectl",
    "hugetlbfs",
    "mqueue",
    "nsfs",
    "overlay",
    "proc",
    "pstore",
    "ramfs",
    "rpc_pipefs",
    "securityfs",
    "squashfs",
    "sysfs",
    "tmpfs",
    "tracefs",
}


def _safe_percent(value: Any) -> float | None:
    if value is None:
        return None

    if isinstance(value, str):
        value = value.strip().replace("%", "")

    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def normalize_filesystem(raw: dict[str, Any]) -> dict[str, Any]:
    fs_type = str(raw.get("type", raw.get("fstype", ""))).lower()
    mount = raw.get("mount") or raw.get("mounted_on") or raw.get("target") or "unknown"

    used_percent = _safe_percent(
        raw.get("used_percent")
        or raw.get("use_percent")
        or raw.get("pcent")
        or raw.get("capacity")
    )

    return {
        "device": raw.get("device") or raw.get("filesystem") or raw.get("source"),
        "mount": mount,
        "type": fs_type,
        "size": raw.get("size"),
        "used": raw.get("used"),
        "available": raw.get("available") or raw.get("avail"),
        "used_percent": used_percent,
        "assess": fs_type not in IGNORED_FILESYSTEM_TYPES,
        "ignored_reason": "virtual_or_pseudo_filesystem" if fs_type in IGNORED_FILESYSTEM_TYPES else None,
        "raw": raw,
    }


def normalize_storage(payload: dict[str, Any]) -> InventorySection:
    storage = payload.get("storage", payload)
    raw_filesystems = storage.get("filesystems", [])

    filesystems = [
        normalize_filesystem(fs)
        for fs in raw_filesystems
        if isinstance(fs, dict)
    ]

    return InventorySection(
        name="storage",
        data={
            "filesystems": filesystems,
            "assessed_filesystems": [fs for fs in filesystems if fs["assess"]],
            "ignored_filesystems": [fs for fs in filesystems if not fs["assess"]],
        },
        source="normalization.storage",
    )
