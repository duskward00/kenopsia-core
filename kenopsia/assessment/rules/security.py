from __future__ import annotations

from ..findings import Finding, Severity
from ..inventory import Inventory


def ssh_root_login_rule(inventory: Inventory) -> list[Finding]:
    security = inventory.data_for("security", {})
    ssh = security.get("ssh", {})
    permit_root_login = str(ssh.get("PermitRootLogin", "")).lower()

    if permit_root_login not in {"yes", "without-password", "prohibit-password"}:
        return []

    return [
        Finding(
            id="security.ssh.root_login",
            category="security",
            severity=Severity.HIGH,
            title="SSH root login is enabled or partially enabled",
            description="The SSH daemon configuration allows direct root login behavior.",
            recommendation="Set PermitRootLogin no in sshd_config and restart the SSH service after validating administrative access.",
            evidence={"PermitRootLogin": ssh.get("PermitRootLogin")},
            source="ssh_root_login_rule",
        )
    ]


def ssh_password_auth_rule(inventory: Inventory) -> list[Finding]:
    security = inventory.data_for("security", {})
    ssh = security.get("ssh", {})
    password_auth = str(ssh.get("PasswordAuthentication", "")).lower()

    if password_auth != "yes":
        return []

    return [
        Finding(
            id="security.ssh.password_auth",
            category="security",
            severity=Severity.MEDIUM,
            title="SSH password authentication is enabled",
            description="SSH allows password-based authentication.",
            recommendation="Consider using key-based authentication and disabling PasswordAuthentication where operationally appropriate.",
            evidence={"PasswordAuthentication": ssh.get("PasswordAuthentication")},
            source="ssh_password_auth_rule",
        )
    ]


security_rules = [ssh_root_login_rule, ssh_password_auth_rule]
