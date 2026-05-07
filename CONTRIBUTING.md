# Contributing to OMNIA-VALIDATION

OMNIA-VALIDATION is a structural validation, falsification, perturbation testing, and reproducibility layer.

Contributions should preserve the core boundary:

```text
measurement != inference != decision

Acceptable Contributions

Useful contributions include:

new validators
new falsification cases
negative results
reproducibility improvements
test fixtures
schema validation
documentation cleanup
CI improvements

Experimental Discipline

A validator should include:

script or package entry point
bounded input data
deterministic output when possible
explicit result file
clear pass/check/fail logic
documented boundary

Negative Results

Negative results are allowed.

A failed experiment should not be hidden if it exposes a real boundary.

Pull Request Checklist

Before opening a pull request:

pytest -q
ruff check omnia_validation tests

If the contribution changes result files, explain why.

