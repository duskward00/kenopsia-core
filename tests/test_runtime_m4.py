import json
from pathlib import Path

from kenopsia.rendering.normalized_html import render_normalized_html
from kenopsia.rendering.normalized_json import render_normalized_json
from kenopsia.rendering.normalized_markdown import render_normalized_markdown
from kenopsia.runtime import run_normalized_assessment


def test_normalized_runtime_scores_payload():
    payload = {
        "hostname": "test-host",
        "storage": {
            "filesystems": [
                {"mount": "/", "type": "ext4", "used_percent": 96},
                {"mount": "/sys/firmware/efi/efivars", "type": "efivarfs", "used_percent": 100},
            ]
        },
        "security": {"ssh": {"PermitRootLogin": "no", "PasswordAuthentication": "no"}},
        "services": [{"name": "bad.service", "state": "failed", "enabled": "enabled"}],
    }

    result = run_normalized_assessment(payload)

    ids = [finding.id for finding in result.findings]

    assert "storage.capacity" in ids[0] or any(id.startswith("storage.capacity") for id in ids)
    assert "services.failed.bad.service" in ids
    assert result.score.overall < 100


def test_normalized_renderers_write_files(tmp_path: Path):
    payload = {
        "hostname": "test-host",
        "storage": {"filesystems": []},
        "security": {"ssh": {"PermitRootLogin": "no"}},
        "services": [],
    }

    result = run_normalized_assessment(payload)

    json_path = render_normalized_json(result, tmp_path / "report.json")
    md_path = render_normalized_markdown(result, tmp_path / "report.md")
    html_path = render_normalized_html(result, tmp_path / "report.html")

    assert json_path.exists()
    assert md_path.exists()
    assert html_path.exists()

    loaded = json.loads(json_path.read_text(encoding="utf-8"))
    assert loaded["score"]["overall"] == 100
    assert "Kenopsia Core Normalized Assessment" in md_path.read_text(encoding="utf-8")
    assert "<html" in html_path.read_text(encoding="utf-8")
