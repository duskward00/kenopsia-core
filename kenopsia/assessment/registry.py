from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass, field

from .findings import Finding
from .inventory import Inventory

AssessmentRule = Callable[[Inventory], list[Finding]]


@dataclass
class RuleRegistry:
    """Simple registry for assessment rules."""

    rules: list[AssessmentRule] = field(default_factory=list)

    def register(self, rule: AssessmentRule) -> AssessmentRule:
        self.rules.append(rule)
        return rule

    def extend(self, rules: list[AssessmentRule]) -> None:
        self.rules.extend(rules)

    def run(self, inventory: Inventory) -> list[Finding]:
        findings: list[Finding] = []

        for rule in self.rules:
            findings.extend(rule(inventory))

        return findings
