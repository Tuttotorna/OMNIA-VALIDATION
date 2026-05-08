# OMNIA-VALIDATION — Artifact Hash Manifest Policy

## Purpose

This document defines how OMNIA-VALIDATION should handle artifact hashes, hash manifests, source files, datasets, result files, and traceability claims.

The goal is to distinguish:

```text
hash match
hash mismatch
hash presence
artifact traceability
semantic correctness
scientific validation
```

Core boundary:

```text
measurement != inference != decision
```

A hash can prove that a file matches a recorded byte sequence.

A hash cannot prove that the file is semantically true, scientifically correct, or production-safe.

---

## 1. Core Principle

Artifact hashes support traceability.

They do not create truth.

Correct interpretation:

```text
hash match -> artifact identity preserved
hash mismatch -> artifact identity changed or path/content problem exists
hash present -> source traceability improved
hash absent -> source traceability weaker
```

Incorrect interpretation:

```text
hash match -> scientific result is true
hash present -> model output is correct
hash match -> semantic truth is certified
hash present -> production safety is certified
```

Hashing is a reproducibility tool.

It is not a semantic validation tool.

---

## 2. What Is An Artifact

An artifact is any file used, generated, or referenced by a validation process.

Examples:

```text
dataset files
source-output files
JSON result files
JSONL result files
enveloped result files
manifest files
validator scripts
configuration files
benchmark records
external source records
```

Common artifact directories:

```text
data/
data/source_outputs/
results/
results_enveloped/
examples/
docs/
```

---

## 3. What Is A Hash Manifest

A hash manifest is a structured record that stores hashes for artifacts.

A manifest should make it possible to answer:

```text
which file was used?
where was it located?
what hash was recorded?
when was it recorded?
which validator recorded it?
what role did the file play?
```

A future hash manifest may include:

```text
artifact_path
artifact_role
sha256
size_bytes
created_at_utc
recorded_by
validator_id
notes
```

---

## 4. SHA-256 Policy

OMNIA-VALIDATION currently uses SHA-256 for artifact traceability.

SHA-256 format:

```text
64 lowercase hexadecimal characters
```

Example:

```text
24d7177cea63e44e2616c0d4546ed65fd824719f7fc4030b9a52130c1bf4e00c
```

Validate format:

```bash
omnia-validation validate-sha256 24d7177cea63e44e2616c0d4546ed65fd824719f7fc4030b9a52130c1bf4e00c
```

Compute file hash:

```bash
omnia-validation hash-file <path>
```

Hash support is implemented in:

```text
omnia_validation.hashing
omnia_validation.cli
```

---

## 5. Hash Match

A hash match means:

```text
the current file bytes match the recorded SHA-256 value
```

A hash match supports:

```text
artifact identity
source traceability
reproducibility review
regression review
release review
```

A hash match does not prove:

```text
semantic correctness
scientific correctness
model intelligence
production safety
universal validity
final truth
```

Correct claim:

```text
The artifact matches the recorded SHA-256 hash.
```

Incorrect claim:

```text
The result is true because the hash matches.
```

---

## 6. Hash Mismatch

A hash mismatch means:

```text
the current file bytes do not match the recorded SHA-256 value
```

Possible causes:

```text
file content changed intentionally
file content changed accidentally
wrong file path
wrong source file
corrupted file
line-ending change
encoding change
manual edit
untracked regeneration
```

A hash mismatch should be treated seriously.

If hash equality is required by a validator, a mismatch should usually produce:

```text
FAIL
```

If the artifact was intentionally updated, the status may be:

```text
CHECK
```

until the update is documented and reviewed.

---

## 7. Hash Presence

Hash presence means:

```text
a hash value was recorded for an artifact
```

Hash presence improves traceability.

It does not guarantee correctness.

Correct interpretation:

```text
the artifact is traceable to a byte-level identity
```

Incorrect interpretation:

```text
the artifact is semantically correct
```

A result can be fully hash-traceable and still scientifically weak.

A result can lack a hash and still be useful, but with weaker reproducibility evidence.

---

## 8. Hash Absence

Hash absence means:

```text
no recorded hash is available for the artifact
```

This weakens traceability.

It does not automatically invalidate the artifact.

Correct handling:

```text
mark traceability as weaker
compute hash when possible
document missing hash when not possible
avoid overclaiming source verification
```

If a validator requires source hashes and they are missing, the validator may return:

```text
CHECK
```

or:

```text
FAIL
```

depending on the validator rule.

---

## 9. Placeholder Hashes

Placeholder hashes are symbolic values used before real hashes are available.

Examples:

```text
<sha256>
placeholder_hash
pending_hash
source_hash_pending
```

Placeholder hashes are not source verification.

They should be replaced by real computed hashes when the artifact exists.

Temporal Collapse Level 3 V15 explicitly strengthened traceability by replacing symbolic source-file hash placeholders with real computed SHA-256 hashes.

Correct interpretation:

```text
placeholder hash -> weak traceability
real hash        -> stronger traceability
```

Incorrect interpretation:

```text
placeholder hash is equivalent to real hash
```

---

## 10. Manifest Scope

A hash manifest should clearly state its scope.

Possible scopes:

```text
source_outputs
datasets
results
results_enveloped
validator_scripts
release_artifacts
```

A manifest should not imply coverage beyond its declared scope.

Correct:

```text
This manifest covers data/source_outputs/.
```

Incorrect:

```text
This manifest proves the whole repository is verified.
```

---

## 11. Recommended Manifest Fields

Recommended manifest structure:

```json
{
  "experiment": "artifact_hash_manifest_v0",
  "status": "PASS",
  "created_at_utc": "2026-05-07T00:00:00+00:00",
  "boundary": "measurement != inference != decision",
  "payload": {
    "manifest_scope": "source_outputs",
    "artifact_count": 0,
    "artifacts": []
  }
}
```

Recommended artifact entry:

```json
{
  "artifact_path": "data/source_outputs/example.jsonl",
  "artifact_role": "source_output",
  "sha256": "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
  "size_bytes": 1234,
  "recorded_by": "artifact_hash_manifest_v0",
  "notes": "source output used by validator"
}
```

---

## 12. Artifact Roles

Recommended artifact roles:

```text
dataset
source_output
model_output
validator_script
result
enveloped_result
manifest
documentation
configuration
benchmark_input
benchmark_output
```

Artifact roles should be explicit.

This helps distinguish:

```text
input identity
output identity
script identity
documentation identity
```

---

## 13. Source-Output Hashes

Source-output hashes are especially important when validators depend on model output files, external records, or generated traces.

Source-output hashes support:

```text
traceability
rerun comparison
source identity
regression review
```

They do not prove:

```text
the model answer is correct
the benchmark was solved
the output is semantically valid
```

Correct claim:

```text
The source-output file is traceable by SHA-256.
```

Incorrect claim:

```text
The model output is correct because it has a SHA-256 hash.
```

---

## 14. Dataset Hashes

Dataset hashes support:

```text
dataset identity
dataset version control
reproducibility checks
regression checks
```

Dataset hash changes may indicate:

```text
new dataset version
manual edit
corruption
different line endings
different ordering
different serialization
```

If a dataset hash changes, document whether the change is:

```text
expected drift
unexpected regression
schema regression
artifact update
```

See:

```text
docs/RESULT_REGRESSION_POLICY.md
```

---

## 15. Result Hashes

Result hashes may be useful for release freezing and regression review.

However, result files may include timestamps.

If timestamps are regenerated, hashes may change even when substantive payloads do not.

For result hashes, distinguish:

```text
byte-level identity
payload-level identity
semantic interpretation
```

A byte-level result hash is strict.

A payload-level regression comparison may be more useful for generated result artifacts.

Future regression tooling should define which comparison type is being used.

---

## 16. Enveloped Result Hashes

Enveloped results live in:

```text
results_enveloped/
```

They are schema-normalized copies of historical result files.

Hashing enveloped results can verify:

```text
wrapper output identity
manifest identity
release artifact identity
```

It cannot verify:

```text
scientific revalidation of legacy experiments
semantic correctness of original results
```

Remember:

```text
results_enveloped/ is normalization
not revalidation
```

---

## 17. Validator Script Hashes

Hashing validator scripts can support release traceability.

A script hash proves:

```text
this exact script content was recorded
```

It does not prove:

```text
the script is correct
the method is valid
the interpretation is sound
```

Script hashes are useful for:

```text
release archives
reproduction packages
change detection
regression investigations
```

---

## 18. Hash Regression

Hash regression occurs when an artifact hash changes unexpectedly.

Examples:

```text
expected hash no longer matches computed hash
source-output file changed without documentation
dataset changed without version update
manifest changed unexpectedly
```

Hash regression should be classified using:

```text
docs/RESULT_REGRESSION_POLICY.md
```

Possible classifications:

```text
EXPECTED_DRIFT
UNEXPECTED_REGRESSION
HASH_REGRESSION
SCIENTIFIC_BOUNDARY_CHANGE
NO_REGRESSION
```

---

## 19. PASS / CHECK / FAIL Guidance

Use:

```text
PASS
```

when:

```text
all required artifact hashes are present
all required artifact hashes match
manifest schema is valid
artifact paths resolve
```

Use:

```text
CHECK
```

when:

```text
hashes are missing but not strictly required
artifact update is intentional but needs review
manifest scope is partial
traceability is improved but not complete
manual review is needed
```

Use:

```text
FAIL
```

when:

```text
required hash mismatches
required artifact is missing
hash format is invalid
manifest is malformed
validator requires traceability and traceability fails
```

---

## 20. Manifest Validation

A future manifest validator should check:

```text
manifest has canonical result envelope
payload.manifest_scope exists
payload.artifacts is a list
each artifact has artifact_path
each artifact has artifact_role
each artifact has sha256
sha256 format is valid
artifact path exists when required
computed hash matches recorded hash when required
```

Current status:

```text
policy plus generated manifest workflow
not yet automated
```

Future package module:

```text
omnia_validation.manifest
```

Future CLI command:

```bash
omnia-validation validate-manifest <path>
```

This command is not implemented yet.

---

## 21. Recommended Manifest Location

Possible future manifest locations:

```text
manifests/
results/artifact_hash_manifest_v0.json
results_enveloped/artifact_hash_manifest_v0.json
```

Recommended initial location:

```text
results/artifact_hash_manifest_v0.json
```

Reason:

```text
hash manifests are result artifacts
```

If the manifest is canonical-envelope formatted, it may also be wrapped or validated like other canonical results.

---

## 22. Release Use

Before a release, hash manifests can support:

```text
artifact freezing
source-output traceability
dataset identity
result identity
release reproducibility
```

Release notes should not overstate hash meaning.

Correct release language:

```text
This release includes SHA-256 hashes for selected artifacts.
```

Incorrect release language:

```text
This release proves the results are true because the hashes match.
```

See:

```text
docs/RELEASE_POLICY.md
```

---

## 23. Maintenance Use

During maintenance, hashes can help detect:

```text
unexpected file changes
source-output mutation
dataset mutation
result regeneration
manifest drift
```

If hashes change, do not silently replace them.

Correct handling:

```text
identify what changed
classify the change
document the reason
update manifest only when justified
run tests
```

See:

```text
docs/MAINTENANCE.md
```

---

## 24. Relation To Result Regression

Hash changes are one form of result or artifact regression.

See:

```text
docs/RESULT_REGRESSION_POLICY.md
```

A hash mismatch may be:

```text
expected drift
unexpected regression
hash regression
scientific boundary change
```

The classification depends on context.

---

## 25. Relation To Validator Registry

The validator registry should eventually record hash traceability status for validator families.

See:

```text
docs/VALIDATOR_REGISTRY.md
```

Future registry fields may include:

```text
hash_manifest_path
hash_traceability_status
source_output_hash_status
dataset_hash_status
result_hash_status
```

This is not yet implemented.

---

## 26. Relation To V15

Temporal Collapse Level 3 V15 is the strongest current example of hash traceability.

It replaced source-file hash placeholders with real computed SHA-256 hashes.

Current V15 summary:

```text
source_file_count: 4
computed_hash_count: 4
real_hash_count: 4
placeholder_hash_count: 0
hash_format_failure_count: 0
hash_mismatch_failure_count: 0
```

Correct interpretation:

```text
source traceability was strengthened
```

Incorrect interpretation:

```text
semantic correctness was proven
```

---

## 27. What Not To Do

Do not:

```text
treat hash match as semantic truth
treat hash presence as scientific validation
silently replace mismatching hashes
hide hash mismatches
commit placeholder hashes as if they were real hashes
claim full repository verification from partial manifest scope
ignore artifact path changes
ignore dataset mutations
```

---


## Generator Script

The current manifest generator is:

```text
examples/build_artifact_hash_manifest_v0.py
```

It currently scans:

```text
data/source_outputs/
```

It writes:

```text
results/artifact_hash_manifest_v0.json
```

It records:

```text
artifact_path
artifact_role
sha256
size_bytes
source_validator
source_provider
source_run
```

Current limitation:

```text
stable timestamp option still missing
repository-wide artifact coverage still missing
```

## 28. Future Work

Future improvements:

```text
add artifact hash manifest file
add omnia_validation.manifest module
expand validate-manifest CLI coverage
add manifest tests
add manifest schema documentation
add source-output manifest
add dataset manifest
add release artifact manifest
add validator registry hash-traceability fields
add result regression integration
```

Possible future files:

```text
results/artifact_hash_manifest_v0.json
tests/test_manifest.py
docs/ARTIFACT_HASH_MANIFEST_V0_RESULT.md
```

Possible future module:

```text
omnia_validation.manifest
```

---

## 29. Correct Interpretation

Correct interpretation:

```text
hashes support traceability
hashes support reproducibility review
hashes support artifact identity
hash mismatches require classification
hash manifests can strengthen release discipline
```

Incorrect interpretation:

```text
hashes prove semantic truth
hashes prove model correctness
hashes certify production safety
hashes make experiments final
hash manifests replace independent reproduction
```

---

## 30. Non-Goal

This policy does not implement a hash manifest validator.

It defines the policy for future manifest use.

It clarifies what hashes can and cannot prove.

Final boundary:

```text
measurement != inference != decision
```