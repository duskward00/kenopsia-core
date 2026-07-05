from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from typing import Any, Iterable

from .findings import Finding
from .inventory import Inventory
from .recommendations import Recommendation, recommendations_from_findings
from .registry import RuleRegistry
from .scoring import AssessmentScore, calculate_score


# ---------------------------------------------------------------------------
# Legacy v0.2.x compatibility interface
# ---------------------------------------------------------------------------

@dataclass(slots=True)
class AssessmentFinding:
    """
    Legacy finding object used by the current CLI/reporting path.

    This remains available until the CLI is migrated to the new Finding model.
    """

    id: str
    title: str
    severity: str
    category: str
    summary: str
    recommendation: str
    evidence: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(slots=True)
class LegacyAssessmentResult:
    """
    Legacy assessment result returned by run_assessment().

    The current CLI expects `.score`, `.grade`, `.findings`, and `.to_dict()`.
    """

    score: int
    grade: str
    findings: list[AssessmentFinding]

    def to_dict(self) -> dict[str, Any]:
        return {
            "score": self.score,
            "grade": self.grade,
            "findings": [finding.to_dict() for finding in self.findings],
        }


def _legacy_grade(score: int) -> str:
    if score >= 90:
        return "A"
    if score >= 80:
        return "B"
    if score >= 70:
        return "C"
    if score >= 60:
        return "D"
    return "F"


def _legacy_penalty(severity: str) -> int:
    return {
        "critical": 20,
        "high": 12,
        "medium": 7,
        "low": 3,
        "info": 0,
    }.get(severity.lower(), 0)


def _as_list(value: Any) -> list[Any]:
    if value is None:
        return []
    if isinstance(value, list):
        return value
    if isinstance(value, tuple):
        return list(value)
    return [value]


_IGNORED_STORAGE_FS_TYPES = {
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


def _collect_storage_findings(data: dict[str, Any]) -> Iterable[AssessmentFinding]:
    filesystems = _as_list(data.get("filesystems") or data.get("storage", {}).get("filesystems"))

    for fs in filesystems:
        fs_type = str(fs.get("type", fs.get("fstype", ""))).lower()
        mount = fs.get("mount") or fs.get("mounted_on") or fs.get("target") or "unknown"

        if fs_type in _IGNORED_STORAGE_FS_TYPES:
            continue

        try:
            used_pct = float(fs.get("used_percent", fs.get("use_percent", 0)))
        except (TypeError, ValueError):
            continue

        if used_pct >= 90:
            yield AssessmentFinding(
                id=f"storage.filesystem.high_usage.{mount}",
                title=f"Filesystem {mount} is critically full",
                severity="high",
                category="storage",
                summary=f"Filesystem {mount} is at {used_pct:.1f}% used.",
                recommendation="Free space, expand the filesystem, or move data before services become unstable.",
                evidence={"mount": mount, "type": fs_type, "used_percent": used_pct},
            )
        elif used_pct >= 80:
            yield AssessmentFinding(
                id=f"storage.filesystem.warning_usage.{mount}",
                title=f"Filesystem {mount} is above 80% used",
                severity="medium",
                category="storage",
                summary=f"Filesystem {mount} is at {used_pct:.1f}% used.",
                recommendation="Review growth trends and plan cleanup or expansion.",
                evidence={"mount": mount, "type": fs_type, "used_percent": used_pct},
            )


def _collect_security_findings(data: dict[str, Any]) -> Iterable[AssessmentFinding]:
    services = _as_list(data.get("services") or data.get("security", {}).get("services"))

    for svc in services:
        name = str(svc.get("name", ""))
        state = str(svc.get("state", svc.get("active_state", ""))).lower()
        enabled = str(svc.get("enabled", svc.get("unit_file_state", ""))).lower()
        if name in {"telnet.service", "rsh.service", "rexec.service"} and (state == "active" or enabled == "enabled"):
            yield AssessmentFinding(
                id=f"security.legacy_service.{name}",
                title=f"Legacy remote access service detected: {name}",
                severity="high",
                category="security",
                summary=f"{name} appears to be active or enabled.",
                recommendation="Disable legacy clear-text remote access services and use SSH or a managed access platform.",
                evidence={"service": svc},
            )

    ssh = data.get("ssh") or data.get("security", {}).get("ssh") or {}

    # Accept both legacy lower-case collector keys and newer sshd_config style.
    permit_root = str(
        ssh.get("permit_root_login", ssh.get("PermitRootLogin", ""))
    ).lower()
    password_auth = str(
        ssh.get("password_authentication", ssh.get("PasswordAuthentication", ""))
    ).lower()

    if permit_root in {"yes", "without-password", "prohibit-password"}:
        yield AssessmentFinding(
            id="security.ssh.root_login",
            title="SSH root login is permitted",
            severity="medium",
            category="security",
            summary=f"SSH PermitRootLogin is set to {permit_root}.",
            recommendation="Disable direct root SSH login and require named administrative accounts with sudo.",
            evidence={"permit_root_login": permit_root},
        )

    if password_auth == "yes":
        yield AssessmentFinding(
            id="security.ssh.password_authentication",
            title="SSH password authentication is enabled",
            severity="low",
            category="security",
            summary="SSH PasswordAuthentication is enabled.",
            recommendation="Prefer key-based or SSO-backed access where practical, especially for Internet-facing hosts.",
            evidence={"password_authentication": password_auth},
        )


def _collect_platform_findings(data: dict[str, Any]) -> Iterable[AssessmentFinding]:
    os_data = data.get("os") or data.get("platform") or {}
    distro = str(os_data.get("id", os_data.get("distro", ""))).lower()
    version = str(os_data.get("version_id", os_data.get("version", "")))

    if distro in {"ubuntu", "debian", "fedora", "centos", "rhel", "rocky", "almalinux"} and not version:
        yield AssessmentFinding(
            id="platform.missing_version",
            title="Operating system version could not be determined",
            severity="info",
            category="platform",
            summary="The collector identified the Linux family but not the exact version.",
            recommendation="Verify /etc/os-release parsing and collector permissions.",
            evidence={"os": os_data},
        )


def run_assessment(data: dict[str, Any]) -> LegacyAssessmentResult:
    """
    Run the legacy assessment checks against collected host data.

    This function is intentionally retained until the main CLI is migrated to
    the new normalized inventory pipeline in a later milestone.
    """

    findings: list[AssessmentFinding] = []
    findings.extend(_collect_platform_findings(data))
    findings.extend(_collect_storage_findings(data))
    findings.extend(_collect_security_findings(data))

    score = max(0, 100 - sum(_legacy_penalty(f.severity) for f in findings))
    return LegacyAssessmentResult(score=score, grade=_legacy_grade(score), findings=findings)


# ---------------------------------------------------------------------------
# Sprint 1 assessment framework
# ---------------------------------------------------------------------------

@dataclass
class AssessmentResult:
    """Complete assessment result produced by the new framework."""

    inventory: Inventory
    findings: list[Finding]
    recommendations: list[Recommendation]
    score: AssessmentScore
    generated_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    def as_dict(self) -> dict[str, Any]:
        return {
            "generated_at": self.generated_at,
            "inventory": self.inventory.as_dict(),
            "findings": [finding.as_dict() for finding in self.findings],
            "recommendations": [rec.as_dict() for rec in self.recommendations],
            "score": self.score.as_dict(),
        }


class AssessmentEngine:
    """Runs registered assessment rules against normalized inventory."""

    def __init__(self, registry: RuleRegistry | None = None) -> None:
        self.registry = registry or RuleRegistry()

    def assess(self, inventory: Inventory) -> AssessmentResult:
        findings = self.registry.run(inventory)
        score = calculate_score(findings)
        recommendations = recommendations_from_findings(findings)

        return AssessmentResult(
            inventory=inventory,
            findings=findings,
            recommendations=recommendations,
            score=score,
        )
