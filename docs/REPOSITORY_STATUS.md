# OMNIA-VALIDATION Repository Status

Generated / updated: 2026-05-08T18:32:07.987594+00:00

## Status

OMNIA-VALIDATION is an operational validation repository.

Clean-environment audit:

```text
import omnia_validation   OK
pip install -e .          OK
pytest                    254 passed
```

## Repository role

```text
OMNIA-VALIDATION = evidence / falsification / reproducibility layer
```

It is not the OMNIA measurement core.

It is not a truth oracle.

It is not a semantic judge.

It is not a final decision system.

Decision remains external.

## Existing strengths

The repository already contains:

- installable package metadata
- CLI commands
- test suite
- CI workflow
- MIT LICENSE
- data artifacts
- result artifacts
- many validation reports
- artifact manifest logic
- result-regression logic
- reviewer guide
- release notes

## Cleanup performed

This cleanup strengthens public presentation:

- README.md rewritten as validation evidence hub
- DOI badge corrected
- CITATION.cff added
- docs/VALIDATION_SCOPE.md added
- docs/RESULTS_INDEX.md added
- docs/FAILURE_CASES.md added
- docs/REPOSITORY_STATUS.md added
- GitHub About / Homepage / Topics aligned
- GitHub Release updated or created

## Known documentation issue

Several legacy result documents may contain unclosed Markdown fences.

The core public entrypoints are now clean, but legacy result documents should be repaired gradually only when needed.

Do not bulk-rewrite all legacy result files without checking content preservation.

## DOI

```text
10.5281/zenodo.20083830
https://doi.org/10.5281/zenodo.20083830
```

## Safe interpretation

```text
OMNIA measures.
OMNIA-VALIDATION tests evidence, limits, failures, and reproducibility.
Decision remains external.
```
