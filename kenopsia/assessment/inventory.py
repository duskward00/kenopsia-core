from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class InventorySection:
    """
    A normalized inventory section.

    Collector output should eventually be adapted into sections like storage,
    security, services, packages, networking, hardware, and operating_system.
    """

    name: str
    data: dict[str, Any] = field(default_factory=dict)
    source: str = "collector"
    status: str = "ok"
    errors: list[str] = field(default_factory=list)

    def as_dict(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "data": self.data,
            "source": self.source,
            "status": self.status,
            "errors": self.errors,
        }


@dataclass
class Inventory:
    """Normalized inventory container used by the assessment engine."""

    host: str = "unknown"
    sections: dict[str, InventorySection] = field(default_factory=dict)

    def add_section(self, section: InventorySection) -> None:
        self.sections[section.name] = section

    def get(self, name: str) -> InventorySection | None:
        return self.sections.get(name)

    def data_for(self, name: str, default: Any = None) -> Any:
        section = self.get(name)
        if section is None:
            return default
        return section.data

    def as_dict(self) -> dict[str, Any]:
        return {
            "host": self.host,
            "sections": {name: section.as_dict() for name, section in self.sections.items()},
        }
