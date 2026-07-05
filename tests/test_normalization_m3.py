from kenopsia.assessment import InventorySection
from kenopsia.assessment.rules.services import failed_services_rule
from kenopsia.normalization import inventory_from_payload, normalize_storage


def test_inventory_from_payload_creates_expected_sections():
    payload = {
        "hostname": "test-host",
        "storage": {"filesystems": []},
        "security": {"ssh": {"PermitRootLogin": "no"}},
        "services": [],
    }

    inventory = inventory_from_payload(payload)

    assert inventory.host == "test-host"
    assert inventory.get("storage") is not None
    assert inventory.get("security") is not None
    assert inventory.get("services") is not None


def test_storage_normalization_marks_efivarfs_ignored():
    section = normalize_storage(
        {
            "filesystems": [
                {
                    "mount": "/sys/firmware/efi/efivars",
                    "type": "efivarfs",
                    "used_percent": "100%",
                }
            ]
        }
    )

    fs = section.data["filesystems"][0]

    assert fs["assess"] is False
    assert fs["ignored_reason"] == "virtual_or_pseudo_filesystem"
    assert section.data["ignored_filesystems"][0]["type"] == "efivarfs"


def test_storage_normalization_keeps_ext4_assessable():
    section = normalize_storage(
        {
            "filesystems": [
                {
                    "mount": "/",
                    "type": "ext4",
                    "used_percent": "81%",
                }
            ]
        }
    )

    fs = section.data["filesystems"][0]

    assert fs["assess"] is True
    assert fs["used_percent"] == 81.0


def test_failed_services_rule_uses_normalized_services():
    inventory = inventory_from_payload(
        {
            "hostname": "test-host",
            "services": [
                {
                    "name": "example.service",
                    "state": "failed",
                    "enabled": "enabled",
                }
            ],
        }
    )

    findings = failed_services_rule(inventory)

    assert len(findings) == 1
    assert findings[0].id == "services.failed.example.service"
