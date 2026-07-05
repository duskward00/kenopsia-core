from pathlib import Path

from kenopsia.collectors import security


def test_ssh_config_permission_denied_is_non_fatal(monkeypatch):
    class FakePath:
        def __init__(self, value):
            self.value = value

        def exists(self):
            return True

        def read_text(self, *args, **kwargs):
            raise PermissionError("denied")

        def __str__(self):
            return self.value

    monkeypatch.setattr(security, "Path", lambda value: FakePath(value))

    result = security._collect_ssh_config()

    assert result == {"status": "permission_denied", "path": "/etc/ssh/sshd_config"}
