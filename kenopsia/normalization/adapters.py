from __future__ import annotations

from typing import Any

from kenopsia.assessment import Inventory, InventorySection

from .security import normalize_security
from .services import normalize_services
from .storage import normalize_storage


def _host_from_payload(payload: dict[str, Any]) -> str:
    candidates = [
        payload.get("hostname"),
        payload.get("host"),
        payload.get("system", {}).get("hostname") if isinstance(payload.get("system"), dict) else None,
        payload.get("platform", {}).get("hostname") if isinstance(payload.get("platform"), dict) else None,
    ]

    for candidate in candidates:
        if candidate:
            return str(candidate)

    return "unknown"


def inventory_from_payload(payload: dict[str, Any]) -> Inventory:
    """
    Convert the current collector payload into normalized Inventory.

    This is intentionally tolerant of mixed legacy structures so the project can
    migrate collectors gradually instead of all at once.
    """

    inventory = Inventory(host=_host_from_payload(payload))

    inventory.add_section(normalize_storage(payload))
    inventory.add_section(normalize_security(payload))
    inventory.add_section(normalize_services(payload))

    for name in ("system", "hardware", "memory", "networking", "packages", "fedora", "virtualization"):
        value = payload.get(name)
        if isinstance(value, dict):
            inventory.add_section(
                InventorySection(
                    name=name,
                    data=value,
                    source=f"normalization.{name}",
                )
            )

    return inventory
