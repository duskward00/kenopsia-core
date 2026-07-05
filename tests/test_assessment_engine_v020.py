from kenopsia.assessment import run_assessment


def test_empty_assessment_scores_clean():
    result = run_assessment({})
    assert result.score == 100
    assert result.grade == "A"
    assert result.findings == []


def test_storage_medium_and_high_findings_affect_score():
    data = {
        "filesystems": [
            {"mount": "/", "used_percent": 85},
            {"mount": "/var", "used_percent": 93},
        ]
    }
    result = run_assessment(data)
    assert result.score == 81
    assert result.grade == "B"
    assert [finding.category for finding in result.findings] == ["storage", "storage"]


def test_ssh_password_auth_low_finding():
    data = {"ssh": {"password_authentication": "yes", "permit_root_login": "no"}}
    result = run_assessment(data)
    assert result.score == 97
    assert result.grade == "A"
    assert result.findings[0].id == "security.ssh.password_authentication"
