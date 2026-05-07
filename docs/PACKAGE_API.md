# OMNIA-VALIDATION — Package API

## Purpose

This document describes the reusable Python package layer added to OMNIA-VALIDATION.

The package layer is located in:

```text
omnia_validation/
```

It provides small reusable utilities for:

```text
hashing
JSON/JSONL IO
simple structural metrics
artifact metadata
result schema validation
CLI validation checks
```

Core boundary:

```text
measurement != inference != decision
```

The package layer does not replace the experimental scripts.

It only reduces duplicated logic and improves reproducibility.

---

## 1. Package Modules

Current modules:

```text
omnia_validation.hashing
omnia_validation.io
omnia_validation.metrics
omnia_validation.metadata
omnia_validation.schemas
omnia_validation.cli
```

Package entry point:

```text
omnia_validation/__init__.py
```

CLI entry point:

```text
omnia-validation
```

Configured in:

```text
pyproject.toml
```

---

## 2. Installation

Install in editable development mode:

```bash
python -m pip install -e ".[dev]"
```

Verify import:

```bash
python -c "import omnia_validation; print('OK')"
```

Expected output:

```text
OK
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

## 3. omnia_validation.hashing

Source file:

```text
omnia_validation/hashing.py
```

Purpose:

```text
compute SHA-256 hashes
validate SHA-256 hexadecimal strings
support artifact traceability
```

Available functions:

```text
sha256_bytes
sha256_text
sha256_file
is_sha256_hex
```

---

### sha256_bytes

```python
sha256_bytes(data: bytes) -> str
```

Returns the SHA-256 hexadecimal digest for raw bytes.

Example:

```python
from omnia_validation.hashing import sha256_bytes

digest = sha256_bytes(b"omnia")
print(digest)
```

---

### sha256_text

```python
sha256_text(text: str, *, encoding: str = "utf-8") -> str
```

Returns the SHA-256 hexadecimal digest for text.

Example:

```python
from omnia_validation.hashing import sha256_text

digest = sha256_text("omnia")
print(digest)
```

---

### sha256_file

```python
sha256_file(path: str | Path, *, chunk_size: int = 1024 * 1024) -> str
```

Returns the SHA-256 hexadecimal digest for a file.

The file is read in chunks.

This avoids loading large artifacts fully in memory.

Example:

```python
from omnia_validation.hashing import sha256_file

digest = sha256_file("data/example.jsonl")
print(digest)
```

Raises:

```text
FileNotFoundError
IsADirectoryError
```

---

### is_sha256_hex

```python
is_sha256_hex(value: str) -> bool
```

Returns `True` when a string is a valid SHA-256 hexadecimal digest.

Example:

```python
from omnia_validation.hashing import is_sha256_hex

assert is_sha256_hex("a" * 64)
assert not is_sha256_hex("g" * 64)
```

---

## 4. omnia_validation.io

Source file:

```text
omnia_validation/io.py
```

Purpose:

```text
read JSON
write JSON
read JSONL
write JSONL
preserve deterministic formatting where practical
```

Available functions:

```text
read_json
write_json
read_jsonl
write_jsonl
```

---

### read_json

```python
read_json(path: str | Path) -> Any
```

Reads a JSON file.

Example:

```python
from omnia_validation.io import read_json

data = read_json("results/example.json")
```

---

### write_json

```python
write_json(path: str | Path, data: Any, *, indent: int = 2) -> None
```

Writes JSON with deterministic formatting.

Behavior:

```text
creates parent directories when needed
uses UTF-8
uses ensure_ascii=False
uses sort_keys=True
adds final newline
```

Example:

```python
from omnia_validation.io import write_json

result = {
    "status": "PASS",
    "payload": {
        "record_count": 10
    }
}

write_json("results/example.json", result)
```

---

### read_jsonl

```python
read_jsonl(path: str | Path) -> list[dict[str, Any]]
```

Reads a JSONL file as a list of dictionaries.

Rules:

```text
blank lines are ignored
each non-empty line must be a JSON object
```

Example:

```python
from omnia_validation.io import read_jsonl

records = read_jsonl("data/example.jsonl")
print(len(records))
```

Raises:

```text
ValueError
```

when a JSONL line is not an object.

---

### write_jsonl

```python
write_jsonl(path: str | Path, records: list[dict[str, Any]]) -> None
```

Writes dictionaries to a JSONL file.

Behavior:

```text
creates parent directories when needed
uses UTF-8
uses ensure_ascii=False
uses sort_keys=True
writes one JSON object per line
```

Example:

```python
from omnia_validation.io import write_jsonl

records = [
    {"id": "a", "value": 1},
    {"id": "b", "value": 2}
]

write_jsonl("data/example.jsonl", records)
```

Raises:

```text
TypeError
```

when an item is not a dictionary.

---

## 5. omnia_validation.metrics

Source file:

```text
omnia_validation/metrics.py
```

Purpose:

```text
provide small semantics-free structural signals
```

Available functions:

```text
shannon_entropy
compression_ratio
normalized_repetition_score
```

Important boundary:

```text
These are not semantic metrics.
They do not determine correctness.
They only expose simple structural behavior.
```

---

### shannon_entropy

```python
shannon_entropy(text: str) -> float
```

Returns Shannon entropy over characters.

Empty text returns:

```text
0.0
```

Example:

```python
from omnia_validation.metrics import shannon_entropy

score = shannon_entropy("abcabcabc")
print(score)
```

Interpretation:

```text
lower entropy  -> more repeated/simple character distribution
higher entropy -> more varied character distribution
```

Boundary:

```text
entropy is not truth
entropy is not correctness
entropy is not intelligence
```

---

### compression_ratio

```python
compression_ratio(text: str, *, encoding: str = "utf-8") -> float
```

Returns:

```text
compressed_size / raw_size
```

using `zlib`.

Empty text returns:

```text
0.0
```

Example:

```python
from omnia_validation.metrics import compression_ratio

ratio = compression_ratio("abcabcabcabcabcabc")
print(ratio)
```

Interpretation:

```text
lower ratio  -> more compressible structure
higher ratio -> less compressible structure
```

Boundary:

```text
compression ratio is not semantic correctness
```

---

### normalized_repetition_score

```python
normalized_repetition_score(text: str) -> float
```

Returns a simple normalized repetition score.

Range:

```text
0.0 -> no repeated character mass
1.0 -> all characters are the same
```

Empty text returns:

```text
0.0
```

Single-character text returns:

```text
1.0
```

Example:

```python
from omnia_validation.metrics import normalized_repetition_score

score = normalized_repetition_score("aaaaab")
print(score)
```

---

## 6. omnia_validation.metadata

Source file:

```text
omnia_validation/metadata.py
```

Purpose:

```text
create reproducibility metadata
create standard result envelopes
attach visible epistemic boundary
```

Available functions:

```text
utc_now_iso
file_metadata
result_envelope
```

---

### utc_now_iso

```python
utc_now_iso() -> str
```

Returns the current UTC timestamp in ISO-8601 format.

Example:

```python
from omnia_validation.metadata import utc_now_iso

timestamp = utc_now_iso()
print(timestamp)
```

---

### file_metadata

```python
file_metadata(path: str | Path) -> dict[str, Any]
```

Returns basic reproducibility metadata for a file.

Returned fields:

```text
path
size_bytes
sha256
```

Example:

```python
from omnia_validation.metadata import file_metadata

metadata = file_metadata("data/example.jsonl")
print(metadata)
```

Raises:

```text
FileNotFoundError
```

when the file does not exist.

---

### result_envelope

```python
result_envelope(
    *,
    experiment: str,
    status: str,
    payload: dict[str, Any],
    boundary: str = "measurement != inference != decision",
) -> dict[str, Any]
```

Builds a standard result envelope.

Returned structure:

```json
{
  "experiment": "example_validator_v0",
  "status": "PASS",
  "created_at_utc": "2026-05-07T00:00:00+00:00",
  "boundary": "measurement != inference != decision",
  "payload": {}
}
```

Example:

```python
from omnia_validation.io import write_json
from omnia_validation.metadata import result_envelope

payload = {
    "record_count": 10,
    "main_signal": "record_presence",
    "decision_reason": "Input records were present."
}

result = result_envelope(
    experiment="example_validator_v0",
    status="PASS",
    payload=payload,
)

write_json("results/example_validator_v0.json", result)
```

---

## 7. omnia_validation.schemas

Source file:

```text
omnia_validation/schemas.py
```

Purpose:

```text
validate the structural shape of OMNIA-VALIDATION result artifacts
check canonical result envelope fields
check allowed result statuses
check visible boundary preservation
```

Important boundary:

```text
schema validation checks structure only
schema validation does not check semantic truth
schema validation does not make final decisions
```

Available constants:

```text
ALLOWED_RESULT_STATUSES
REQUIRED_RESULT_FIELDS
DEFAULT_BOUNDARY
```

Available functions:

```text
validate_result_envelope
is_valid_result_envelope
require_valid_result_envelope
```

---

### ALLOWED_RESULT_STATUSES

```python
ALLOWED_RESULT_STATUSES = frozenset({"PASS", "CHECK", "FAIL"})
```

Allowed top-level result statuses.

Meaning:

```text
PASS  -> tested structural condition survived this validation step
CHECK -> partial instability, ambiguity, or boundary condition detected
FAIL  -> collapse, mismatch, invalid artifact, or validation failure detected
```

---

### REQUIRED_RESULT_FIELDS

```python
REQUIRED_RESULT_FIELDS = frozenset(
    {
        "experiment",
        "status",
        "created_at_utc",
        "boundary",
        "payload",
    }
)
```

Required top-level fields for a canonical result envelope.

---

### DEFAULT_BOUNDARY

```python
DEFAULT_BOUNDARY = "measurement != inference != decision"
```

Default epistemic boundary used by OMNIA-VALIDATION result artifacts.

---

### validate_result_envelope

```python
validate_result_envelope(result: Mapping[str, Any]) -> list[str]
```

Validates the canonical OMNIA-VALIDATION result envelope.

Returns a list of error messages.

An empty list means the envelope passed the structural schema check.

Example:

```python
from omnia_validation.schemas import validate_result_envelope

result = {
    "experiment": "example_validator_v0",
    "status": "PASS",
    "created_at_utc": "2026-05-07T00:00:00+00:00",
    "boundary": "measurement != inference != decision",
    "payload": {
        "record_count": 10
    },
}

errors = validate_result_envelope(result)

if errors:
    print(errors)
else:
    print("PASS")
```

Checks:

```text
result is a mapping/object
required fields are present
experiment is a non-empty string
status is PASS, CHECK, or FAIL
created_at_utc is a UTC-like ISO-8601 string
boundary matches measurement != inference != decision
payload is a mapping/object
```

---

### is_valid_result_envelope

```python
is_valid_result_envelope(result: Mapping[str, Any]) -> bool
```

Returns `True` when a result envelope passes the structural schema check.

Example:

```python
from omnia_validation.schemas import is_valid_result_envelope

if is_valid_result_envelope(result):
    print("valid")
else:
    print("invalid")
```

---

### require_valid_result_envelope

```python
require_valid_result_envelope(result: Mapping[str, Any]) -> None
```

Raises `ValueError` if a result envelope fails the structural schema check.

Example:

```python
from omnia_validation.schemas import require_valid_result_envelope

require_valid_result_envelope(result)
```

Useful inside validators when a script must stop on invalid output.

Example:

```python
from omnia_validation.io import write_json
from omnia_validation.metadata import result_envelope
from omnia_validation.schemas import require_valid_result_envelope

payload = {
    "record_count": 10,
    "main_signal": "record_presence",
    "decision_reason": "Input records were present.",
}

result = result_envelope(
    experiment="example_validator_v0",
    status="PASS",
    payload=payload,
)

require_valid_result_envelope(result)
write_json("results/example_validator_v0.json", result)
```

---

## 8. omnia_validation.cli

Source file:

```text
omnia_validation/cli.py
```

CLI command:

```text
omnia-validation
```

Purpose:

```text
small command-line checks for validation artifacts
```

Available commands:

```text
hash-file
validate-sha256
validate-json
validate-result
```

---

### hash-file

```bash
omnia-validation hash-file <path>
```

Computes SHA-256 for a file.

Example:

```bash
omnia-validation hash-file data/example.jsonl
```

Output:

```text
<sha256_digest>
```

---

### validate-sha256

```bash
omnia-validation validate-sha256 <value>
```

Validates whether a string is a SHA-256 hexadecimal digest.

Example:

```bash
omnia-validation validate-sha256 aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
```

Expected output:

```text
PASS
```

Invalid example:

```bash
omnia-validation validate-sha256 not-a-hash
```

Expected output:

```text
FAIL
```

---

### validate-json

```bash
omnia-validation validate-json <path>
```

Validates whether a `.json` or `.jsonl` file is parseable.

For `.jsonl`, it also reports the number of records.

Example:

```bash
omnia-validation validate-json results/example.json
```

Example output:

```json
{
  "status": "PASS"
}
```

JSONL example:

```bash
omnia-validation validate-json data/example.jsonl
```

Example output:

```json
{
  "status": "PASS",
  "records": 10
}
```

Failure output:

```json
{
  "status": "FAIL",
  "error": "..."
}
```

---

### validate-result

```bash
omnia-validation validate-result <path>
```

Validates a result JSON file against the canonical OMNIA-VALIDATION result envelope schema.

It checks:

```text
experiment
status
created_at_utc
boundary
payload
```

Valid example:

```bash
omnia-validation validate-result results/example_validator_v0.json
```

Expected output:

```json
{
  "status": "PASS",
  "schema": "result_envelope"
}
```

Invalid result example:

```json
{
  "experiment": "example_validator_v0",
  "status": "UNKNOWN",
  "payload": []
}
```

Expected output shape:

```json
{
  "status": "FAIL",
  "errors": [
    "missing required field: boundary",
    "missing required field: created_at_utc",
    "status must be one of: CHECK, FAIL, PASS",
    "payload must be a mapping/object"
  ]
}
```

Boundary:

```text
validate-result checks structural schema only
validate-result does not check semantic truth
validate-result does not certify production safety
```

---

## 9. Public Imports

The package exposes common utilities from:

```text
omnia_validation/__init__.py
```

Current public imports:

```python
from omnia_validation import (
    ALLOWED_RESULT_STATUSES,
    DEFAULT_BOUNDARY,
    REQUIRED_RESULT_FIELDS,
    compression_ratio,
    is_sha256_hex,
    is_valid_result_envelope,
    normalized_repetition_score,
    read_json,
    read_jsonl,
    require_valid_result_envelope,
    sha256_bytes,
    sha256_file,
    sha256_text,
    shannon_entropy,
    validate_result_envelope,
    write_json,
    write_jsonl,
)
```

Example:

```python
from omnia_validation import (
    is_valid_result_envelope,
    sha256_text,
    shannon_entropy,
)

digest = sha256_text("omnia")
entropy = shannon_entropy("omnia")

result = {
    "experiment": "example_validator_v0",
    "status": "PASS",
    "created_at_utc": "2026-05-07T00:00:00+00:00",
    "boundary": "measurement != inference != decision",
    "payload": {
        "record_count": 1
    },
}

print(digest)
print(entropy)
print(is_valid_result_envelope(result))
```

---

## 10. Recommended Use Inside Validators

Recommended validator pattern:

```python
from __future__ import annotations

from pathlib import Path

from omnia_validation.io import read_jsonl, write_json
from omnia_validation.metadata import result_envelope
from omnia_validation.schemas import require_valid_result_envelope

VALIDATOR_NAME = "example_validator_v0"
INPUT_PATH = Path("data/example_input_v0.jsonl")
RESULT_PATH = Path("results/example_validator_v0.json")


def main() -> int:
    records = read_jsonl(INPUT_PATH)

    payload = {
        "record_count": len(records),
        "input_path": str(INPUT_PATH),
        "output_path": str(RESULT_PATH),
        "main_signal": "record_presence",
        "decision_reason": "Input records were present.",
    }

    result = result_envelope(
        experiment=VALIDATOR_NAME,
        status="PASS" if records else "FAIL",
        payload=payload,
    )

    require_valid_result_envelope(result)
    write_json(RESULT_PATH, result)

    return 0 if records else 1


if __name__ == "__main__":
    raise SystemExit(main())
```

After generating a result, validate it from the command line:

```bash
omnia-validation validate-result results/example_validator_v0.json
```

---

## 11. Testing The Package Layer

Run:

```bash
pytest -q
```

Current test files:

```text
tests/test_hashing.py
tests/test_io.py
tests/test_metrics.py
tests/test_metadata.py
tests/test_cli.py
tests/test_schemas.py
```

The tests verify:

```text
hash determinism
file hashing
SHA-256 format validation
JSON roundtrip
JSONL roundtrip
entropy behavior
compression behavior
repetition score behavior
metadata generation
result envelope construction
CLI command behavior
validate-result CLI behavior
schema constants
schema validation
schema error reporting
schema failure raising
```

---

## 12. CI Coverage

The GitHub Actions workflow runs on:

```text
push
pull_request
```

Python versions:

```text
3.10
3.11
3.12
```

Checks:

```text
package installation
ruff check
pytest
CLI smoke test
```

Workflow file:

```text
.github/workflows/ci.yml
```

Current CLI smoke test checks:

```text
validate-sha256
```

The pytest suite checks:

```text
validate-json
validate-result
hash-file
validate-sha256
```

---

## 13. Design Rules

The package layer should remain:

```text
small
explicit
standard-library-first
semantics-free
reproducibility-oriented
validator-supportive
```

Avoid adding heavy dependencies unless necessary.

Avoid embedding experimental logic directly into generic utilities.

Keep experimental behavior in:

```text
examples/
```

Keep reusable support behavior in:

```text
omnia_validation/
```

---

## 14. Non-Goals

The package API does not provide:

```text
semantic truth detection
model intelligence evaluation
production-safety certification
domain-independent correctness guarantees
final decision logic
```

It provides reusable support utilities for structural validation artifacts.

Final boundary:

```text
measurement != inference != decision
```