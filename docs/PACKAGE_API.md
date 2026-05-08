# OMNIA-VALIDATION — Package API

## Purpose

This document describes the reusable Python package layer in OMNIA-VALIDATION.

The package is located at:

```text
omnia_validation/
```

Core boundary:

```text
measurement != inference != decision
```

The package provides support utilities for validation scripts.

It does not validate semantic truth.

It does not certify production safety.

It does not make final decisions.

---

## Package Import Policy

The package initializer is intentionally minimal:

```text
omnia_validation/__init__.py
```

It exports only:

```text
__version__
```

Current package-level import:

```python
import omnia_validation

print(omnia_validation.__version__)
```

Expected result:

```text
0.1.0
```

Do not rely on importing helper functions directly from the package root.

Use module-specific imports instead.

Correct:

```python
from omnia_validation.hashing import compute_file_sha256
from omnia_validation.manifest import validate_artifact_manifest
from omnia_validation.schemas import validate_result_envelope
```

Avoid:

```python
from omnia_validation import compute_file_sha256
from omnia_validation import validate_artifact_manifest
from omnia_validation import validate_result_envelope
```

Reason:

```text
submodules may evolve independently
package import must remain stable
validation logic should be imported from the module that defines it
```

---

## Current Modules

Current reusable modules:

```text
omnia_validation.hashing
omnia_validation.io
omnia_validation.metrics
omnia_validation.metadata
omnia_validation.schemas
omnia_validation.manifest
omnia_validation.cli
```

---

## Installation

Install in editable development mode:

```bash
python -m pip install -e ".[dev]"
```

Run tests:

```bash
pytest -q
```

Run linting:

```bash
ruff check omnia_validation tests
```

---

## omnia_validation.hashing

### Purpose

Hash utilities for artifact traceability.

Hashing supports byte-level artifact identity.

Hashing does not prove semantic correctness.

Boundary:

```text
hash match -> artifact byte identity preserved
hash match != semantic truth
```

---

### Functions

```python
from omnia_validation.hashing import compute_file_sha256
from omnia_validation.hashing import is_valid_sha256
```

---

### compute_file_sha256

```python
compute_file_sha256(path: object) -> str
```

Computes the SHA-256 digest of a file.

Example:

```python
from omnia_validation.hashing import compute_file_sha256

digest = compute_file_sha256("data/example.jsonl")
print(digest)
```

Returns:

```text
64-character lowercase hexadecimal SHA-256 string
```

---

### is_valid_sha256

```python
is_valid_sha256(value: object) -> bool
```

Returns `True` when the input is a valid lowercase SHA-256 hexadecimal string.

Example:

```python
from omnia_validation.hashing import is_valid_sha256

assert is_valid_sha256("a" * 64)
assert not is_valid_sha256("not-a-hash")
```

---

## omnia_validation.io

### Purpose

JSON and JSONL input/output helpers.

This module supports artifact handling for validators.

It does not interpret semantic correctness.

---

### Recommended Imports

```python
from omnia_validation.io import read_json
from omnia_validation.io import write_json
from omnia_validation.io import read_jsonl
from omnia_validation.io import write_jsonl
```

---

### read_json

Reads a JSON file.

Example:

```python
from omnia_validation.io import read_json

data = read_json("results/example.json")
```

---

### write_json

Writes a JSON file.

Example:

```python
from omnia_validation.io import write_json

write_json("results/example.json", {"status": "CHECK"})
```

---

### read_jsonl

Reads a JSONL file.

Example:

```python
from omnia_validation.io import read_jsonl

records = read_jsonl("data/example.jsonl")
```

---

### write_jsonl

Writes a JSONL file.

Example:

```python
from omnia_validation.io import write_jsonl

write_jsonl("data/example.jsonl", [{"id": 1}, {"id": 2}])
```

---

## omnia_validation.metrics

### Purpose

Simple structural helper metrics.

These metrics are support utilities.

They are not final scientific claims.

---

### Recommended Imports

```python
from omnia_validation.metrics import shannon_entropy
from omnia_validation.metrics import compression_ratio
from omnia_validation.metrics import normalized_repetition_score
```

---

### shannon_entropy

Computes a simple entropy score for a sequence or string.

Example:

```python
from omnia_validation.metrics import shannon_entropy

score = shannon_entropy("abcabcabc")
```

Interpretation:

```text
higher entropy -> more distributional spread
lower entropy  -> more repetition / concentration
```

Boundary:

```text
entropy is a structural proxy
entropy is not semantic truth
```

---

### compression_ratio

Computes a simple compression ratio.

Example:

```python
from omnia_validation.metrics import compression_ratio

ratio = compression_ratio("abcabcabcabc")
```

Interpretation:

```text
lower ratio may indicate higher compressibility
higher ratio may indicate lower compressibility
```

Boundary:

```text
compression behavior is structural evidence
not semantic validation
```

---

### normalized_repetition_score

Computes a normalized repetition score.

Example:

```python
from omnia_validation.metrics import normalized_repetition_score

score = normalized_repetition_score(["A", "A", "B"])
```

Interpretation:

```text
higher score -> more repetition
lower score  -> less repetition
```

---

## omnia_validation.metadata

### Purpose

Metadata helpers for timestamps, file metadata, and result envelopes.

Metadata supports reproducibility.

Metadata does not prove correctness.

---

### Recommended Imports

Use only functions that exist in the current module implementation.

Do not import metadata helpers from the package root.

Recommended pattern:

```python
from omnia_validation import metadata
```

Then inspect or call the current module functions directly.

Example:

```python
from omnia_validation import metadata

print(dir(metadata))
```

Reason:

```text
metadata helper names may evolve
package root does not re-export metadata helpers
```

---

## omnia_validation.schemas

### Purpose

Canonical result-envelope validation.

This module validates the top-level OMNIA-VALIDATION result schema.

It does not validate semantic truth.

It does not validate payload-specific scientific interpretation.

---

### Canonical Result Envelope

Canonical fields:

```text
experiment
status
created_at_utc
boundary
payload
```

Allowed status values:

```text
PASS
CHECK
FAIL
```

Required boundary:

```text
measurement != inference != decision
```

---

### Recommended Imports

```python
from omnia_validation.schemas import validate_result_envelope
from omnia_validation.schemas import is_valid_result_envelope
from omnia_validation.schemas import require_valid_result_envelope
```

---

### validate_result_envelope

```python
validate_result_envelope(result: dict) -> list[str]
```

Returns a list of validation errors.

Empty list means the envelope passed top-level schema validation.

Example:

```python
from omnia_validation.schemas import validate_result_envelope

result = {
    "experiment": "example_v0",
    "status": "CHECK",
    "created_at_utc": "2026-05-07T00:00:00+00:00",
    "boundary": "measurement != inference != decision",
    "payload": {},
}

errors = validate_result_envelope(result)

assert errors == []
```

---

### is_valid_result_envelope

```python
is_valid_result_envelope(result: dict) -> bool
```

Returns `True` if the result envelope is valid.

Example:

```python
from omnia_validation.schemas import is_valid_result_envelope

assert is_valid_result_envelope(result)
```

---

### require_valid_result_envelope

```python
require_valid_result_envelope(result: dict) -> None
```

Raises `ValueError` when the result envelope is invalid.

Example:

```python
from omnia_validation.schemas import require_valid_result_envelope

require_valid_result_envelope(result)
```

---

### Boundary

The schema validator checks:

```text
top-level envelope structure
required fields
allowed canonical status values
required boundary string
payload object presence
```

It does not check:

```text
semantic correctness
scientific correctness
payload-specific meaning
production safety
final validity
```

---

## omnia_validation.manifest


### build_artifact_hash_manifest_v0.py

Generator script:

```text
examples/build_artifact_hash_manifest_v0.py
```

Purpose:

```text
scan data/source_outputs/
compute SHA-256
record size_bytes
write results/artifact_hash_manifest_v0.json
validate generated manifest
```

Run:

```bash
python examples/build_artifact_hash_manifest_v0.py
omnia-validation validate-manifest results/artifact_hash_manifest_v0.json --verify-hashes
```


Deterministic options:

```text
--stable-timestamp
--created-at <ISO-8601 timestamp>
```
Current limitation:

```text
stable timestamp option added
repository-wide manifest generation still missing
```


### Purpose

Artifact hash manifest validation.

This module validates artifact hash manifests.

It supports traceability.

It does not prove semantic truth.

Boundary:

```text
hash match -> artifact byte identity preserved
hash match != semantic correctness
```

---

### Recommended Imports

```python
from omnia_validation.manifest import VALID_ARTIFACT_ROLES
from omnia_validation.manifest import validate_artifact_entry
from omnia_validation.manifest import validate_artifact_manifest
from omnia_validation.manifest import is_valid_artifact_manifest
from omnia_validation.manifest import require_valid_artifact_manifest
```

---

### VALID_ARTIFACT_ROLES

Allowed artifact roles:

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

---

### validate_artifact_entry

```python
validate_artifact_entry(
    entry: dict,
    *,
    base_dir: str | Path = ".",
    require_existing_file: bool = False,
    verify_hash: bool = False,
) -> list[str]
```

Validates one artifact entry.

Required artifact entry fields:

```text
artifact_path
artifact_role
sha256
```

Example:

```python
from omnia_validation.manifest import validate_artifact_entry

entry = {
    "artifact_path": "data/source_outputs/example.jsonl",
    "artifact_role": "source_output",
    "sha256": "a" * 64,
}

errors = validate_artifact_entry(entry)
```

Optional behavior:

```text
require_existing_file=True -> artifact path must exist
verify_hash=True           -> computed hash must match recorded hash
```

Example with hash verification:

```python
from omnia_validation.manifest import validate_artifact_entry

errors = validate_artifact_entry(
    entry,
    base_dir=".",
    verify_hash=True,
)
```

---

### validate_artifact_manifest

```python
validate_artifact_manifest(
    manifest: dict,
    *,
    base_dir: str | Path = ".",
    require_existing_files: bool = False,
    verify_hashes: bool = False,
) -> list[str]
```

Validates a full artifact hash manifest.

The manifest must use the canonical OMNIA-VALIDATION result envelope:

```text
experiment
status
created_at_utc
boundary
payload
```

Required payload fields:

```text
manifest_version
manifest_scope
artifact_count
hash_algorithm
artifacts
```

Required hash algorithm:

```text
sha256
```

Example:

```python
from omnia_validation.io import read_json
from omnia_validation.manifest import validate_artifact_manifest

manifest = read_json("results/artifact_hash_manifest_v0.json")

errors = validate_artifact_manifest(
    manifest,
    base_dir=".",
    verify_hashes=True,
)

assert errors == []
```

---

### is_valid_artifact_manifest

```python
is_valid_artifact_manifest(
    manifest: dict,
    *,
    base_dir: str | Path = ".",
    require_existing_files: bool = False,
    verify_hashes: bool = False,
) -> bool
```

Returns `True` when the artifact manifest passes validation.

Example:

```python
from omnia_validation.manifest import is_valid_artifact_manifest

assert is_valid_artifact_manifest(manifest)
```

---

### require_valid_artifact_manifest

```python
require_valid_artifact_manifest(
    manifest: dict,
    *,
    base_dir: str | Path = ".",
    require_existing_files: bool = False,
    verify_hashes: bool = False,
) -> None
```

Raises `ValueError` if the artifact manifest is invalid.

Example:

```python
from omnia_validation.manifest import require_valid_artifact_manifest

require_valid_artifact_manifest(
    manifest,
    base_dir=".",
    verify_hashes=True,
)
```

---

### Current Manifest

Current artifact hash manifest:

```text
results/artifact_hash_manifest_v0.json
```

Current scope:

```text
data/source_outputs
```

Current purpose:

```text
records source-output hashes from Temporal Collapse Level 3 V15
```

Current status:

```text
CHECK
```

Reason:

```text
first artifact hash manifest
real SHA-256 hashes present
manifest validation helpers present
repository-wide artifact coverage not yet present
```

---

### Correct Hash Interpretation

Correct:

```text
hash match means artifact byte identity is preserved
hash presence improves traceability
hash mismatch requires classification
```

Incorrect:

```text
hash match proves semantic truth
hash presence certifies scientific correctness
hash traceability replaces independent reproduction
```

Policy:

```text
docs/ARTIFACT_HASH_MANIFEST_POLICY.md
```

---

## omnia_validation.cli

### Purpose

Command-line access to validation utilities.

Current CLI command:

```bash
omnia-validation
```

---

### Current CLI Commands

Known commands include:

```text
validate-sha256
hash-file
validate-json
validate-result
```

---

### validate-sha256

Checks whether a value is a valid lowercase SHA-256 hexadecimal string.

Example:

```bash
omnia-validation validate-sha256 aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
```

Expected output:

```text
PASS
```

---

### hash-file

Computes SHA-256 for a file.

Example:

```bash
omnia-validation hash-file data/example.jsonl
```

Expected output:

```text
<sha256>
```

---

### validate-json

Checks whether a JSON or JSONL artifact is parseable.

Example:

```bash
omnia-validation validate-json results/example.json
```

Boundary:

```text
parseable JSON does not imply canonical result schema
parseable JSON does not imply scientific correctness
```

---

### validate-result

Checks whether a result follows the canonical OMNIA-VALIDATION result envelope.

Example:

```bash
omnia-validation validate-result results/artifact_hash_manifest_v0.json
```

Expected schema response:

```json
{
  "status": "PASS",
  "schema": "result_envelope"
}
```

Boundary:

```text
validate-result checks result-envelope structure
validate-result does not validate payload-specific scientific meaning
```

---

### validate-manifest

Validates artifact hash manifests.

Example:

```bash
omnia-validation validate-manifest results/artifact_hash_manifest_v0.json --verify-hashes
```

Expected output:

```json
{
  "status": "PASS",
  "schema": "artifact_manifest"
}
```

Optional flags:

```text
--base-dir
--require-existing-files
--verify-hashes
```

Boundary:

```text
validate-manifest verifies manifest structure and optional hash matches
validate-manifest does not prove semantic correctness
```

### Future CLI Commands

Possible future commands:

```text
validate-manifest
validate-payload
compare-results
build-hash-manifest
validate-registry
```

Not all of these are implemented.

Do not document them as available until the CLI actually supports them.

---

## Recommended Validator Pattern

A validator should import only what it needs from specific modules.

Example:

```python
from __future__ import annotations

from omnia_validation.io import write_json
from omnia_validation.schemas import require_valid_result_envelope


result = {
    "experiment": "example_validator_v0",
    "status": "CHECK",
    "created_at_utc": "2026-05-07T00:00:00+00:00",
    "boundary": "measurement != inference != decision",
    "payload": {
        "note": "example payload",
    },
}

require_valid_result_envelope(result)
write_json("results/example_validator_v0.json", result)
```

For artifact manifests:

```python
from omnia_validation.io import read_json
from omnia_validation.manifest import require_valid_artifact_manifest

manifest = read_json("results/artifact_hash_manifest_v0.json")

require_valid_artifact_manifest(
    manifest,
    base_dir=".",
    verify_hashes=True,
)
```

---

## Testing

Run all tests:

```bash
pytest -q
```

Run linting:

```bash
ruff check omnia_validation tests
```

Current test files include:

```text
tests/test_hashing.py
tests/test_io.py
tests/test_metrics.py
tests/test_metadata.py
tests/test_cli.py
tests/test_schemas.py
tests/test_existing_results.py
tests/test_enveloped_results.py
tests/test_wrap_legacy_results.py
tests/test_manifest.py
```

---

## Current Limitations

Current package limitations:

```text
package root exports only __version__
payload-specific schemas are not yet implemented
manifest validation is exposed through CLI
result regression helpers are not yet implemented
artifact hash manifest generation is not yet automated
validator registry consistency checks are not yet implemented
experiment-chain CI is not yet implemented
```

These limitations are intentional to keep the current package stable.

---

## Correct Interpretation

Correct interpretation:

```text
omnia_validation provides reusable validation utilities
helpers should be imported from specific modules
schema validation checks top-level result envelopes
manifest validation checks artifact manifest structure and optional hash matches
hashing supports artifact traceability
```

Incorrect interpretation:

```text
omnia_validation proves semantic truth
hash validation proves scientific correctness
result schema validation proves model correctness
manifest validation certifies production safety
package import should expose every helper globally
```

---

## Non-Goal

The package API does not make OMNIA-VALIDATION a production certification tool.

It supports reproducible structural validation work.

Final boundary:

```text
measurement != inference != decision
```