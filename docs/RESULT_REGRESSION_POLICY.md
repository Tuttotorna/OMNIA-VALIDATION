# OMNIA-VALIDATION — Result Regression Policy

## Purpose


## Executable Regression Layer

The first executable result-regression layer is implemented in:

```text
omnia_validation/regression.py
```

It is exercised by:

```text
tests/test_regression.py
examples/compare_result_regression_v0.py
```

Current classifications:

```text
NO_REGRESSION
EXPECTED_DRIFT
SCHEMA_REGRESSION
STATUS_REGRESSION
BOUNDARY_REGRESSION
PAYLOAD_REGRESSION
HASH_REGRESSION
```

Correct interpretation:

```text
the module classifies structural result differences
the module does not decide semantic truth
```


This document defines how OMNIA-VALIDATION should treat changes between old result artifacts and newly generated result artifacts.

The goal is to distinguish:

```text
expected drift
unexpected regression
schema regression
hash regression
payload regression
scientific boundary change
```

Core boundary:

```text
measurement != inference != decision
```

A result difference is not automatically an error.

A result difference is evidence that must be classified.

---

## 1. Regression Principle

OMNIA-VALIDATION is a falsification-oriented repository.

Therefore, result changes should not be hidden.

A result change may indicate:

```text
a real structural difference
a changed input
a changed parameter
a changed validator
a changed dependency
a changed schema
a reproducibility problem
an artifact corruption
a boundary refinement
```

The purpose of regression review is not to force all outputs to remain identical.

The purpose is to identify what changed and why.

---

## 2. What Counts As A Result Regression

A result regression is a meaningful difference between:

```text
a previous result artifact
```

and:

```text
a newly generated result artifact
```

Possible regression targets:

```text
results/
results_enveloped/
data/
source_outputs/
hash manifests
schema envelopes
validator payloads
status fields
boundary statements
```

A regression may be harmless, expected, suspicious, or invalid.

---

## 3. Regression Categories

Regression categories:

```text
expected drift
unexpected regression
schema regression
hash regression
payload regression
status regression
boundary regression
documentation regression
scientific boundary change
```

Each category must be treated differently.

---

## 4. Expected Drift

Expected drift means the result changed because the tested system or input conditions changed in a documented way.

Examples:

```text
new dataset version
new perturbation family
new threshold
new validator version
new source-output file
new controlled parameter
new random seed explicitly documented
```

Expected drift should be recorded.

It should not be hidden.

It should not automatically become `FAIL`.

Correct handling:

```text
document input change
document validator change
preserve old result
write new result
explain drift reason
```

---

## 5. Unexpected Regression

Unexpected regression means the result changed without a known cause.

Examples:

```text
same input
same validator
same parameters
same environment expectation
different output
```

This requires review.

Correct handling:

```text
do not overwrite old evidence silently
compare old and new payloads
check environment
check dependency versions
check input hashes
check validator code
mark as CHECK until explained
```

Unexpected regression does not automatically mean the framework failed.

It means the reproducibility boundary was exposed.

---

## 6. Schema Regression

Schema regression occurs when a result expected to follow the canonical envelope no longer validates.

Canonical envelope fields:

```text
experiment
status
created_at_utc
boundary
payload
```

Allowed canonical statuses:

```text
PASS
CHECK
FAIL
```

Check with:

```bash
omnia-validation validate-result <path>
```

A schema regression is serious when it affects:

```text
new canonical results
results_enveloped/
manifest files
CI-validated outputs
```

Correct handling:

```text
treat as FAIL for schema compliance
fix result writer
fix schema if schema changed intentionally
update docs if schema changed intentionally
add or update tests
```

Historical files in `results/` may remain legacy-format.

They are checked for JSON parseability, not necessarily canonical envelope compliance.

---

## 7. Hash Regression

Hash regression occurs when an expected artifact hash changes.

Examples:

```text
source-output SHA-256 changes
data file SHA-256 changes
manifest hash changes
expected hash no longer matches computed hash
```

Hash regression may indicate:

```text
intentional artifact update
accidental file change
corruption
wrong source file
wrong path
uncommitted change
```

Correct handling:

```text
recompute hash
verify file path
verify file content
document artifact change
preserve old hash record if historically relevant
do not silently replace hashes
```

Hash mismatch should usually be treated as:

```text
FAIL
```

when the validator explicitly requires hash equality.

It may be treated as:

```text
CHECK
```

when the hash difference is part of a documented artifact update.

---

## 8. Payload Regression

Payload regression occurs when the result payload changes.

Examples:

```text
score changed
regime changed
trajectory count changed
event count changed
risk score changed
cluster count changed
dependency map changed
```

Payload regression requires context.

A payload change may be:

```text
expected drift
bug fix
parameter change
real structural change
unexpected reproducibility failure
```

Correct handling:

```text
compare payload fields
identify changed inputs
identify changed code
identify changed thresholds
document whether change is expected
```

Do not treat every payload difference as `FAIL`.

Some payload differences are exactly what OMNIA-VALIDATION is designed to expose.

---

## 9. Status Regression

Status regression occurs when canonical status changes.

Examples:

```text
PASS -> CHECK
CHECK -> FAIL
FAIL -> CHECK
CHECK -> PASS
```

Status regression must be reviewed carefully.

A move from:

```text
PASS -> CHECK
```

may mean:

```text
new boundary discovered
stricter validation added
partial instability exposed
```

A move from:

```text
CHECK -> PASS
```

may mean:

```text
stronger evidence added
bug fixed
overly strict condition corrected
```

But it may also be overclaiming.

Correct handling:

```text
verify PASS/CHECK/FAIL rule
check validator documentation
check result schema
check input changes
check boundary statement
```

Never convert `CHECK` to `PASS` only for cosmetic reasons.

---

## 10. Boundary Regression

Boundary regression occurs when a result or document loses the project boundary:

```text
measurement != inference != decision
```

or starts implying unsupported claims.

Examples:

```text
semantic truth detection
model intelligence certification
production safety certification
universal validity
final correctness
```

Boundary regression is serious.

Correct handling:

```text
restore boundary statement
remove overclaiming language
document correct interpretation
update tests or templates if needed
```

Boundary regression may occur in:

```text
README.md
docs/
result docs
release notes
issue templates
pull request templates
validator output
```

---

## 11. Documentation Regression

Documentation regression occurs when docs no longer match repository behavior.

Examples:

```text
README mentions missing file
docs/INDEX.md omits important file
CLI command in docs does not run
schema docs disagree with schemas.py
package API docs disagree with code
maintenance docs disagree with wrapper behavior
```

Correct handling:

```text
update docs
or update code
or explicitly document the difference
```

Documentation regression is important because OMNIA-VALIDATION depends on reproducibility.

---

## 12. Scientific Boundary Change

A scientific boundary change occurs when new evidence changes the valid interpretation of an experiment.

Examples:

```text
control plane no longer robust
threshold axis exposes critical boundary
new source hashes invalidate old traceability
cross-provider disagreement changes regime
payload-specific schema reveals malformed result family
```

A scientific boundary change should not be hidden.

Correct handling:

```text
preserve previous result
write new result
document changed interpretation
update result docs
update project status if important
mark CHECK when appropriate
```

Scientific boundary changes are part of the value of the repository.

They show where claims become weaker, stronger, or more precise.

---

## 13. Historical Results

Historical results live in:

```text
results/
```

They preserve old experimental outputs.

They may not follow the canonical envelope.

They should not be rewritten casually.

If historical results need schema-compatible wrappers, use:

```text
results_enveloped/
```

not in-place mutation of:

```text
results/
```

Correct policy:

```text
preserve historical result
add new result if needed
wrap legacy result if schema compatibility is needed
document the change
```

---

## 14. Enveloped Results

Enveloped results live in:

```text
results_enveloped/
```

They are canonical wrappers around legacy results.

They should validate with:

```bash
omnia-validation validate-result results_enveloped/<file>.json
```

The wrapper preserves:

```text
payload.legacy_result
payload.legacy_status
payload.legacy_result_path
```

Wrapper status remains:

```text
CHECK
```

because:

```text
wrapping is normalization
wrapping is not scientific revalidation
```

Any regression in `results_enveloped/` should be reviewed.

Schema regressions in `results_enveloped/` should fail tests.

---

## 15. Regression Review Procedure

When a result changes, follow this procedure:

```text
identify changed files
identify whether files are historical or canonical
run JSON validation
run result-envelope validation if applicable
compare payloads
compare statuses
compare hashes if applicable
check validator code changes
check input data changes
check documentation changes
classify regression category
document the conclusion
```

Recommended commands:

```bash
git status --short
git diff --stat
pytest -q
ruff check omnia_validation tests
```

For historical results:

```bash
omnia-validation validate-json results/<file>.json
```

For enveloped results:

```bash
omnia-validation validate-result results_enveloped/<file>.json
```

For hash-sensitive artifacts:

```bash
omnia-validation hash-file <path>
```

---

## 16. Regression Classification

Recommended classification labels:

```text
EXPECTED_DRIFT
UNEXPECTED_REGRESSION
SCHEMA_REGRESSION
HASH_REGRESSION
PAYLOAD_REGRESSION
STATUS_REGRESSION
BOUNDARY_REGRESSION
DOCUMENTATION_REGRESSION
SCIENTIFIC_BOUNDARY_CHANGE
NO_REGRESSION
```

These labels are not yet enforced by code.

They are recommended review categories.

---

## 17. PASS / CHECK / FAIL Guidance

Use:

```text
PASS
```

when:

```text
the tested structural condition survived
schema passed when schema was the tested condition
hash matched when hash equality was required
regression was expected and documented
```

Use:

```text
CHECK
```

when:

```text
result changed but meaning is not fully resolved
drift is observed
boundary condition is exposed
legacy normalization occurred
manual review is needed
scientific interpretation changed
```

Use:

```text
FAIL
```

when:

```text
schema required but invalid
hash required but mismatched
required artifact missing
validator cannot reproduce required output
JSON is unreadable
boundary statement is dangerously overclaimed
```

---

## 18. What Not To Do

Do not:

```text
delete old results to hide regression
rewrite historical artifacts silently
convert CHECK to PASS for appearance
treat every drift as failure
treat every instability as semantic incorrectness
ignore hash mismatches
ignore schema failures
remove boundary statements
overstate release meaning
```

This repository becomes stronger when regressions are visible and classified.

---

## 19. Relation To Release Policy

Before a release, regression review should check:

```text
unexpected result changes
schema regressions
hash regressions
documentation regressions
boundary regressions
```

See:

```text
docs/RELEASE_POLICY.md
```

A release should freeze a known state.

It should not hide unresolved regressions.

---

## 20. Relation To Maintenance

Maintenance should preserve evidence while improving reproducibility.

See:

```text
docs/MAINTENANCE.md
```

When result files change, run:

```bash
omnia-validation validate-json results/<result_file>.json
python examples/wrap_legacy_results_in_envelope.py
pytest -q
```

When enveloped results change, run:

```bash
omnia-validation validate-result results_enveloped/legacy_result_envelope_manifest_v0.json
pytest -q
```

---

## 21. Relation To Validator Registry

The validator registry should eventually record regression status for validators.

See:

```text
docs/VALIDATOR_REGISTRY.md
```

Future registry fields may include:

```text
baseline_result_path
latest_result_path
regression_status
last_regression_review
hash_traceability_status
schema_status
payload_schema_status
```

This is not yet implemented.

---

## 22. Future Work

Future improvements:

```text
add result regression test helpers
add frozen baseline manifests
add artifact hash manifests
add payload-specific schema validators
add regression classification output
add validator registry consistency tests
add regression review issue template
add per-family regression policies
```

Possible future files:

```text
docs/ARTIFACT_HASH_MANIFEST_POLICY.md
docs/VALIDATOR_STATUS_VOCABULARY.md
```

Possible future package modules:

```text
omnia_validation.regression
omnia_validation.manifest
```

---

## 23. Correct Interpretation

Correct interpretation:

```text
a result change is evidence to classify
expected drift is not automatically failure
unexpected regression requires review
schema regression is serious for canonical results
hash regression is serious when hash equality is required
boundary regression must be corrected
```

Incorrect interpretation:

```text
all result differences are errors
all drift means failure
all instability means semantic incorrectness
old results should be rewritten to match new schemas
CHECK should be hidden
```

---

## 24. Non-Goal

This policy does not force every result to remain identical forever.

It defines how to classify result changes without hiding evidence or overclaiming certainty.

Final boundary:

```text
measurement != inference != decision
```