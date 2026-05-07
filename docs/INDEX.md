# OMNIA-VALIDATION — Documentation Index

## Purpose

This index provides a stable entry point for the OMNIA-VALIDATION documentation.

OMNIA-VALIDATION is a structural validation, falsification, perturbation testing, and reproducibility layer for the OMNIA ecosystem.

Core boundary:

```text
measurement != inference != decision
```

---

## Main Repository Files

```text
README.md
pyproject.toml
requirements-dev.txt
CONTRIBUTING.md
SECURITY.md
```

---

## Package Layer

Reusable utilities are located in:

```text
omnia_validation/
```

Current modules:

```text
omnia_validation.hashing
omnia_validation.io
omnia_validation.metrics
omnia_validation.metadata
omnia_validation.cli
```

---

## Tests

The current test suite is located in:

```text
tests/
```

Current test files:

```text
tests/test_hashing.py
tests/test_io.py
tests/test_metrics.py
```

---

## Continuous Integration

The CI workflow is located in:

```text
.github/workflows/ci.yml
```

It checks:

```text
Python 3.10
Python 3.11
Python 3.12
ruff
pytest
CLI smoke test
```

---

## Running Experiments

Clean execution guide:

```text
docs/RUNNING_EXPERIMENTS.md
```

---

## Validator Authoring Guide

Guide for adding new validators:

```text
docs/VALIDATOR_AUTHORING_GUIDE.md
```

---

## Result Schema

Common schema for JSON result files:

```text
docs/RESULT_SCHEMA.md
```

This document defines the recommended result envelope, status vocabulary, payload fields, hash traceability fields, trajectory fields, topology fields, and failure/boundary reporting rules.

---

## Consolidation Roadmap

The engineering consolidation roadmap is located in:

```text
docs/CONSOLIDATION_ROADMAP_V0.md
```

---

## Temporal Collapse Topology

Canonical entry point:

```text
docs/TEMPORAL_COLLAPSE_TOPOLOGY_INDEX_V0.md
```

Main chain document:

```text
docs/TEMPORAL_COLLAPSE_TOPOLOGY_EXPERIMENT_CHAIN_V0.md
```

Final phase result:

```text
docs/TEMPORAL_COLLAPSE_TOPOLOGY_BOUNDARY_PHASE_DIAGRAM_V0_RESULT.md
```

---

## Temporal Collapse Level 3

Canonical entry point:

```text
docs/TEMPORAL_COLLAPSE_LEVEL_3_INDEX_V0.md
```

Human-readable summary:

```text
docs/TEMPORAL_COLLAPSE_LEVEL_3_FINAL_SUMMARY_V0.md
```

Current chain:

```text
V13 -> V14 -> V15
```

---

## Result Directories

Experimental artifacts are organized under:

```text
data/
examples/
results/
docs/
```

---

## Reading Order

Suggested reading order for new visitors:

```text
README.md
docs/INDEX.md
docs/RUNNING_EXPERIMENTS.md
docs/VALIDATOR_AUTHORING_GUIDE.md
docs/RESULT_SCHEMA.md
docs/CONSOLIDATION_ROADMAP_V0.md
docs/TEMPORAL_COLLAPSE_LEVEL_3_INDEX_V0.md
docs/TEMPORAL_COLLAPSE_TOPOLOGY_INDEX_V0.md
CONTRIBUTING.md
SECURITY.md
```

---

## Engineering Documents

Current engineering/consolidation documents:

```text
docs/RUNNING_EXPERIMENTS.md
docs/VALIDATOR_AUTHORING_GUIDE.md
docs/RESULT_SCHEMA.md
docs/CONSOLIDATION_ROADMAP_V0.md
```

Purpose:

```text
make experiments runnable
make validators authorable
make result files comparable
make repository structure maintainable
```

---

## Non-Goal

This repository does not claim to detect semantic truth, intelligence, consciousness, or final correctness.

It measures structural behavior under controlled validation pressure.

```text
measurement != inference != decision
```