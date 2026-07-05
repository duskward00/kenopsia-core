from __future__ import annotations

from typing import Any

from kenopsia.assessment import InventorySection


def normalize_ssh(raw_ssh: dict[str, Any]) -> dict[str, Any]:
    normalized: dict[str, Any] = {}

    aliases = {
        "PermitRootLogin": ["PermitRootLogin", "permit_root_login"],
        "PasswordAuthentication": ["PasswordAuthentication", "password_authentication"],
        "PubkeyAuthentication": ["PubkeyAuthentication", "pubkey_authentication"],
        "X11Forwarding": ["X11Forwarding", "x11_forwarding"],
        "status": ["status"],
        "path": ["path"],
        "error": ["error"],
    }

    for target, keys in aliases.items():
        for key in keys:
            if key in raw_ssh:
                normalized[target] = raw_ssh[key]
                break

    normalized["raw"] = raw_ssh
    return normalized


def normalize_security(payload: dict[str, Any]) -> InventorySection:
    security = payload.get("security", payload)
    raw_ssh = security.get("ssh", {})

    return InventorySection(
        name="security",
        data={
            "ssh": normalize_ssh(raw_ssh) if isinstance(raw_ssh, dict) else {},
            "firewall": security.get("firewall", {}),
            "selinux": security.get("selinux", {}),
            "raw": security,
        },
        source="normalization.security",
    )
