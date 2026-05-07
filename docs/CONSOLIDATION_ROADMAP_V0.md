# OMNIA-VALIDATION — Consolidation Roadmap V0

## Purpose

This roadmap turns OMNIA-VALIDATION from a research-script archive into a reproducible, installable, testable validation layer.

It does not change the epistemic boundary of the project.

```text
measurement != inference != decision

Current Status

OMNIA-VALIDATION is currently research-first.

Its strengths are:

structural validation
falsification pressure
negative-result preservation
frozen JSON/JSONL artifacts
experiment/result traceability

Its engineering gaps are:

no package layer
no formal runtime declaration
no centralized reusable utilities
no visible test suite
no visible CI workflow
many versioned monolithic scripts

Phase 1 — Industrialization

Add:

pyproject.toml
requirements-dev.txt
omnia_validation/
tests/
.github/workflows/ci.yml

Goal:

pip-installable package
declared Python >= 3.10
minimal CLI
pytest suite
GitHub Actions CI

Phase 2 — Modularization

Extract reusable utilities from experimental scripts into:

omnia_validation.hashing
omnia_validation.io
omnia_validation.metrics
omnia_validation.metadata

Future modules may include:

omnia_validation.trajectories
omnia_validation.schemas
omnia_validation.topology
omnia_validation.benchmarks
omnia_validation.runners

Phase 3 — Test and Automation

Convert embedded script checks into external tests.

Required test families:

unit tests
fixture tests
result-regression tests
JSON/JSONL parse tests
hash-integrity tests
CLI smoke tests

Phase 4 — Documentation Cleanup

Keep research snapshots, but create stable indexes:

docs/INDEX.md
docs/RUNNING_EXPERIMENTS.md
docs/RESULT_SCHEMA.md
docs/VALIDATOR_AUTHORING_GUIDE.md

Phase 5 — Community Activation

Add:

CONTRIBUTING.md
SECURITY.md
CODE_OF_CONDUCT.md
issue templates
pull request template

Non-Goal

This roadmap does not turn OMNIA-VALIDATION into a semantic truth detector.

It remains a structural validation and falsification layer.

measurement != inference != decision

