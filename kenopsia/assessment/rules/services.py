from __future__ import annotations

from ..findings import Finding, Severity
from ..inventory import Inventory


def failed_services_rule(inventory: Inventory) -> list[Finding]:
    services = inventory.data_for("services", {})
    failed = services.get("failed", [])

    findings: list[Finding] = []

    for service in failed:
        name = service.get("name") or "unknown.service"
        findings.append(
            Finding(
                id=f"services.failed.{name}",
                category="services",
                severity=Severity.MEDIUM,
                title=f"Service is failed: {name}",
                description=f"The service {name} is currently in a failed state.",
                recommendation="Review journalctl and systemctl status output for the failed service, then restart or disable it as appropriate.",
                evidence=service,
                source="failed_services_rule",
            )
        )

    return findings


services_rules = [failed_services_rule]
