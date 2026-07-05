# Kenopsia Core Architecture

## Vision

Kenopsia Core separates data collection from assessment.

    Linux Host
        │
    Collectors
        │
    Normalized Inventory
        │
    Assessment Engine
        │
    Rule Engine
        │
    Finding Engine
        │
    Recommendation Engine
        │
    Scoring Engine
        │
    Renderers (HTML / JSON / Markdown)

## Design Principles

-   Collect once, assess many times.
-   Collectors never make judgments.
-   Rules produce findings.
-   Findings produce recommendations.
-   Scores are derived from evidence.
-   Every assessment is explainable and traceable.
