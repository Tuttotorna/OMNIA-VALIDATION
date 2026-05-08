# OMNIA-VALIDATION Results Index

## Purpose

This file gives a public entrypoint into the result artifacts and validation reports.

The repository contains many result files.

This index explains the major families.

## Main directories

```text
data/              source inputs and datasets
results/           raw result artifacts
results_enveloped/ result artifacts wrapped in canonical envelopes
docs/              reports, validator notes, and result interpretations
examples/          scripts that generate or analyze results
tests/             package and regression tests
```

## Major result families

### Artifact traceability

Relevant files:

- `results/artifact_hash_manifest_v0.json`
- `docs/ARTIFACT_HASH_MANIFEST_POLICY.md`

Purpose:

- preserve artifact byte identity
- validate source-output hashes
- expose artifact drift

### Result regression

Relevant files:

- `omnia_validation/regression.py`
- `docs/RESULT_REGRESSION_POLICY.md`
- `examples/compare_result_regression_v0.py`

Purpose:

- classify whether result artifacts changed structurally
- separate no-regression from drift or structural regression

### Result schema / envelope validation

Relevant files:

- `docs/RESULT_SCHEMA.md`
- `examples/wrap_legacy_results_in_envelope.py`
- `tests/test_enveloped_results.py`

Purpose:

- normalize legacy results
- validate canonical result envelopes

### Temporal-collapse experiments

Relevant files:

- `docs/TEMPORAL_COLLAPSE_LEVEL_3_INDEX_V0.md`
- `docs/TEMPORAL_COLLAPSE_LEVEL_3_FINAL_SUMMARY_V0.md`
- `results/temporal_collapse_*.json`

Purpose:

- record trajectory behavior
- expose collapse regimes
- analyze stability, reversibility, topology, and transition behavior

### Invariance / cross-domain experiments

Relevant files:

- `docs/CROSS_DOMAIN_INVARIANCE_V0_RESULT.md`
- `docs/CROSS_DOMAIN_INVARIANCE_V0_1_RESULT.md`
- `docs/CROSS_DOMAIN_INVARIANCE_V0_2_RESULT.md`
- `results/cross_domain_invariance_*.json`

Purpose:

- test whether structural signals survive across domain shifts or representation changes

### Observer / recoverability experiments

Relevant files:

- `docs/OBSERVER_FAMILY_GEOMETRY_*.md`
- `docs/EFFECTIVE_OBSERVER_*.md`
- `docs/RECOVERABILITY_*.md`

Purpose:

- analyze observer dependence
- test recoverability
- measure structural indistinguishability and projection limits

## Important reading rule

A result artifact is evidence for a defined structural check.

It is not a universal proof.

```text
result evidence != semantic truth
validation pass != final decision
```
