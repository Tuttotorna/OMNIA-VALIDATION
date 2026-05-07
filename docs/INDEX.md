# OMNIA-VALIDATION — Documentation Index

## Purpose

This index provides a stable entry point for the OMNIA-VALIDATION documentation.

OMNIA-VALIDATION is a structural validation, falsification, perturbation testing, and reproducibility layer for the OMNIA ecosystem.

Core boundary:

```text
measurement != inference != decision

Main Repository Files

README.md
pyproject.toml
requirements-dev.txt
CONTRIBUTING.md
SECURITY.md

Package Layer

Reusable utilities are located in:

omnia_validation/

Current modules:

omnia_validation.hashing
omnia_validation.io
omnia_validation.metrics
omnia_validation.metadata
omnia_validation.cli

Tests

The current test suite is located in:

tests/

Current test files:

tests/test_hashing.py
tests/test_io.py
tests/test_metrics.py

Continuous Integration

The CI workflow is located in:

.github/workflows/ci.yml

It checks:

Python 3.10
Python 3.11
Python 3.12
ruff
pytest
CLI smoke test

Consolidation Roadmap

The engineering consolidation roadmap is located in:

docs/CONSOLIDATION_ROADMAP_V0.md

Temporal Collapse Topology

Canonical entry point:

docs/TEMPORAL_COLLAPSE_TOPOLOGY_INDEX_V0.md

Main chain document:

docs/TEMPORAL_COLLAPSE_TOPOLOGY_EXPERIMENT_CHAIN_V0.md

Final phase result:

docs/TEMPORAL_COLLAPSE_TOPOLOGY_BOUNDARY_PHASE_DIAGRAM_V0_RESULT.md

Temporal Collapse Level 3

Canonical entry point:

docs/TEMPORAL_COLLAPSE_LEVEL_3_INDEX_V0.md

Human-readable summary:

docs/TEMPORAL_COLLAPSE_LEVEL_3_FINAL_SUMMARY_V0.md

Current chain:

V13 -> V14 -> V15

Result Directories

Experimental artifacts are organized under:

data/
examples/
results/
docs/

Reading Order

Suggested reading order for new visitors:

README.md
docs/INDEX.md
docs/CONSOLIDATION_ROADMAP_V0.md
docs/TEMPORAL_COLLAPSE_LEVEL_3_INDEX_V0.md
docs/TEMPORAL_COLLAPSE_TOPOLOGY_INDEX_V0.md
CONTRIBUTING.md
SECURITY.md

Non-Goal

This repository does not claim to detect semantic truth, intelligence, consciousness, or final correctness.

It measures structural behavior under controlled validation pressure.

measurement != inference != decision