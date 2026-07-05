# Kenopsia Core

> **Know your Linux systems. Understand their story.**

Kenopsia Core is an open-source Linux assessment platform that
inventories Linux systems, evaluates their operational health,
identifies security and configuration risks, and produces transparent,
evidence-based recommendations.

Rather than simply listing hardware, packages, or services, Kenopsia
Core is built to answer a more important question:

> **How healthy is this Linux system, and why?**

------------------------------------------------------------------------

# Why "Kenopsia"?

The name **Kenopsia** comes from **The Dictionary of Obscure Sorrows**,
a project by John Koenig that gives names to emotions and experiences
that many people recognize but few languages formally describe.

Kenopsia is defined as:

> *The eerie, forlorn atmosphere of a place that is usually bustling
> with people but is now abandoned and quiet.*

That definition resonates surprisingly well with computers.

Every Linux system has a story.

Even when nobody is logged in, a server quietly carries the history of
the administrators who built it, the services it provides, the updates
it has received, the security decisions that shaped it, and the
workloads it has faithfully supported.

Kenopsia Core exists to read that story.

Its purpose is not merely to inventory a machine, but to understand its
condition and communicate that understanding through clear, explainable
assessments.

------------------------------------------------------------------------

# Philosophy

Kenopsia Core is guided by four principles.

## Collect

Gather meaningful information about a Linux system using modular
collectors.

## Assess

Transform inventory into understanding through transparent assessment
rules.

## Explain

Every finding should clearly describe:

-   what was discovered
-   why it matters
-   the evidence supporting it
-   the potential impact

## Recommend

Every issue should include actionable guidance that helps administrators
improve the system.

------------------------------------------------------------------------

# What Makes Kenopsia Different?

Most inventory tools answer:

> "What is installed?"

Kenopsia Core is designed to answer:

-   Is the system healthy?
-   What risks are present?
-   Which findings deserve immediate attention?
-   What should be fixed first?
-   Why did this system receive its score?

Inventory is only the beginning.

Assessment is the destination.

------------------------------------------------------------------------

# Vision

Kenopsia Core is being built as a platform that evolves through several
stages.

1.  Inventory
2.  Assessment
3.  Recommendations
4.  Historical Analysis
5.  Multi-System Assessment
6.  Enterprise Platform

------------------------------------------------------------------------

# Architecture

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
    Renderers
        ├── HTML
        ├── JSON
        └── Markdown

------------------------------------------------------------------------

# Design Goals

-   Modular architecture
-   Transparent scoring
-   Explainable recommendations
-   Distribution independent
-   Plugin friendly
-   Open and extensible

------------------------------------------------------------------------

# Current Status

Current Development Milestone

**Sprint 1 --- Project Foundation**

The focus of the current sprint is establishing the long-term
architecture that future releases will build upon.

------------------------------------------------------------------------

# Contributing

Contributions are welcome.

Future documentation will include contribution guidelines, coding
standards, testing requirements, and release procedures.

------------------------------------------------------------------------

# License

This project is planned to be released under the Apache License 2.0.

------------------------------------------------------------------------

# Closing Thoughts

Linux already has excellent monitoring tools.

It already has inventory utilities.

It already has security scanners.

Kenopsia Core is different.

It exists to help administrators understand the overall health of a
Linux system through evidence-based assessment.

Every Linux system has a story.

**Kenopsia Core exists to read it.**
