"""Security posture collector for Kenopsia Core v0.2.1."""

from __future__ import annotations

import configparser
import subprocess
from pathlib import Path
from typing import Any


def _run(command: list[str]) -> str:
    try:
        completed = subprocess.run(command, check=False, capture_output=True, text=True, timeout=10)
    except (OSError, subprocess.TimeoutExpired):
        return ""
    return completed.stdout.strip()


def _collect_services() -> list[dict[str, str]]:
    output = _run(["systemctl", "list-unit-files", "--type=service", "--no-legend", "--no-pager"])
    services: list[dict[str, str]] = []
    for line in output.splitlines():
        parts = line.split()
        if len(parts) >= 2:
            services.append({"name": parts[0], "enabled": parts[1]})
    return services


def _collect_ssh_config() -> dict[str, str]:
    sshd_config = Path("/etc/ssh/sshd_config")
    result: dict[str, str] = {}
    if not sshd_config.exists():
        return result

    try:
        lines = sshd_config.read_text(encoding="utf-8", errors="replace").splitlines()
    except PermissionError:
        return {"status": "permission_denied", "path": str(sshd_config)}
    except OSError as exc:
        return {"status": "unavailable", "path": str(sshd_config), "error": exc.__class__.__name__}

    for raw_line in lines:
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        parts = line.split(None, 1)
        if len(parts) != 2:
            continue
        key, value = parts[0].lower(), parts[1].strip()
        if key == "permitrootlogin":
            result["permit_root_login"] = value
        elif key == "passwordauthentication":
            result["password_authentication"] = value
    return result


def _collect_os_release() -> dict[str, str]:
    path = Path("/etc/os-release")
    if not path.exists():
        return {}
    parser = configparser.ConfigParser()
    parser.optionxform = str
    parser.read_string("[os]\n" + path.read_text(encoding="utf-8", errors="replace"))
    return {k.lower(): v.strip('"') for k, v in parser["os"].items()}


def collect() -> dict[str, Any]:
    """Collect conservative local security posture signals."""

    return {
        "os": _collect_os_release(),
        "services": _collect_services(),
        "ssh": _collect_ssh_config(),
    }
