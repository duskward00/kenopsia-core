# Sprint 1 / Milestone 3: Collector Normalization

This milestone adds adapter logic that converts the current collector payload into the normalized inventory model.

## Added

```text
kenopsia/normalization/
├── __init__.py
├── adapters.py
├── security.py
├── services.py
└── storage.py
```

## Added Rules

```text
kenopsia/assessment/rules/services.py
```

## Purpose

Collectors still return legacy payloads for now.

The normalization layer converts those payloads into:

```python
Inventory
InventorySection
```

This prepares the project for the Milestone 4 runtime cutover.

## Validation

```bash
pytest
./scripts/validate.sh
./scripts/run.sh
```
