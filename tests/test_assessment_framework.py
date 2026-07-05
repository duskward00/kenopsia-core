from kenopsia.assessment import (
    Finding,
    Inventory,
    InventorySection,
    RuleRegistry,
    Severity,
    calculate_score,
)
from kenopsia.assessment.engine import AssessmentEngine
from kenopsia.assessment.rules.storage import storage_capacity_rule


def test_score_without_findings_is_healthy():
    score = calculate_score([])
    assert score.overall == 100
    assert score.grade == "A+"
    assert score.label == "Healthy"


def test_finding_penalty_uses_severity_weight():
    finding = Finding(
        id="test.high",
        category="test",
        severity=Severity.HIGH,
        title="High test finding",
        description="Example",
        recommendation="Fix it",
    )
    assert finding.penalty() == 10


def test_rule_registry_runs_registered_rules():
    inventory = Inventory(host="test-host")

    def sample_rule(inv):
        return [
            Finding(
                id="sample.rule",
                category="sample",
                severity=Severity.LOW,
                title="Sample",
                description="Sample finding",
                recommendation="Sample recommendation",
            )
        ]

    registry = RuleRegistry()
    registry.register(sample_rule)

    findings = registry.run(inventory)
    assert len(findings) == 1
    assert findings[0].id == "sample.rule"


def test_assessment_engine_generates_result():
    inventory = Inventory(host="test-host")
    registry = RuleRegistry()

    def sample_rule(inv):
        return [
            Finding(
                id="sample.medium",
                category="sample",
                severity=Severity.MEDIUM,
                title="Sample medium finding",
                description="Sample",
                recommendation="Resolve sample",
            )
        ]

    registry.register(sample_rule)
    result = AssessmentEngine(registry).assess(inventory)

    assert result.score.overall == 95
    assert result.recommendations[0].related_findings == ["sample.medium"]


def test_storage_rule_ignores_efivarfs_false_positive():
    inventory = Inventory(host="test-host")
    inventory.add_section(
        InventorySection(
            name="storage",
            data={
                "filesystems": [
                    {
                        "mount": "/sys/firmware/efi/efivars",
                        "type": "efivarfs",
                        "used_percent": 100,
                    }
                ]
            },
        )
    )

    assert storage_capacity_rule(inventory) == []


def test_storage_rule_flags_real_full_filesystem():
    inventory = Inventory(host="test-host")
    inventory.add_section(
        InventorySection(
            name="storage",
            data={
                "filesystems": [
                    {
                        "mount": "/",
                        "type": "ext4",
                        "used_percent": 96,
                    }
                ]
            },
        )
    )

    findings = storage_capacity_rule(inventory)
    assert len(findings) == 1
    assert findings[0].severity == Severity.CRITICAL
