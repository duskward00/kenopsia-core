from __future__ import annotations

from typing import Any

from kenopsia.assessment.engine import AssessmentEngine, AssessmentResult
from kenopsia.assessment.registry import RuleRegistry
from kenopsia.assessment.rules.security import security_rules
from kenopsia.assessment.rules.services import services_rules
from kenopsia.assessment.rules.storage import storage_rules
from kenopsia.normalization import inventory_from_payload


def default_rule_registry() -> RuleRegistry:
    registry = RuleRegistry()
    registry.extend(storage_rules)
    registry.extend(security_rules)
    registry.extend(services_rules)
    return registry


def run_normalized_assessment(payload: dict[str, Any]) -> AssessmentResult:
    """
    Run the Sprint 1 normalized assessment pipeline.

    Current path:

    legacy collector payload -> normalized Inventory -> rules -> findings -> score
    """

    inventory = inventory_from_payload(payload)
    engine = AssessmentEngine(default_rule_registry())
    return engine.assess(inventory)
