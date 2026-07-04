# Collector API

Collectors expose a single function:

```python
def collect() -> dict:
    ...
```

The returned dictionary is rendered directly into reports and exported to JSON.
