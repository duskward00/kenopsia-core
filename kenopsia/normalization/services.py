from __future__ import annotations

from typing import Any

from kenopsia.assessment import InventorySection


def normalize_service(raw: dict[str, Any]) -> dict[str, Any]:
    return {
        "name": raw.get("name") or raw.get("unit") or raw.get("service"),
        "description": raw.get("description") or raw.get("loaded"),
        "state": raw.get("state") or raw.get("active_state") or raw.get("active"),
        "enabled": raw.get("enabled") or raw.get("unit_file_state") or raw.get("startup"),
        "raw": raw,
    }


def normalize_services(payload: dict[str, Any]) -> InventorySection:
    raw_services = payload.get("services", [])

    if isinstance(raw_services, dict):
        raw_services = raw_services.get("services", [])

    services = [
        normalize_service(service)
        for service in raw_services
        if isinstance(service, dict)
    ]

    failed = [
        service for service in services
        if str(service.get("state", "")).lower() == "failed"
    ]

    return InventorySection(
        name="services",
        data={
            "services": services,
            "failed": failed,
        },
        source="normalization.services",
    )
