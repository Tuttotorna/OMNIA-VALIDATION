# OMNIA-VALIDATION — Legacy Result Normalization

## Purpose

This document explains why OMNIA-VALIDATION contains both:

```text
results/
results_enveloped/
```

These directories are intentionally different.

They serve different roles.

Core boundary:

```text
measurement != inference != decision
```

---

## 1. Summary

The repository contains historical result artifacts produced before the canonical result envelope was introduced.

Those original artifacts remain in:

```text
results/
```

A normalized, schema-valid copy of each legacy result is stored in:

```text
results_enveloped/
```

This preserves both:

```text
historical evidence
canonical schema compatibility
```

The original results were not rewritten.

---

## 2. Why This Was Needed

A schema audit showed:

```text
total_json_files_checked: 97
compliant_count: 0
non_compliant_count: 97
unreadable_count: 0
```

Interpretation:

```text
all legacy result files were readable JSON
none were corrupted
none followed the new canonical result envelope yet
```

This was expected.

The result schema was introduced after many experiments had already produced result files.

---

## 3. What Was Not Wrong

The audit did not show that the old results were scientifically wrong.

It showed only that the old results did not yet contain the canonical envelope fields:

```text
experiment
status
created_at_utc
boundary
payload
```

This is a formatting and reproducibility issue.

It is not automatically a scientific failure.

---

## 4. Original Results

Original result files remain in:

```text
results/
```

Role:

```text
preserve historical output
avoid rewriting old evidence
keep original experiment artifacts intact
```

These files may use older internal structures, older status names, or direct result payloads without a wrapper.

They should be treated as historical artifacts.

---

## 5. Enveloped Results

Schema-normalized result files are stored in:

```text
results_enveloped/
```

Role:

```text
provide canonical OMNIA-VALIDATION result envelopes
make legacy artifacts schema-checkable
preserve original payloads inside payload.legacy_result
support future automated validation
```

Each wrapped file contains:

```text
experiment
status
created_at_utc
boundary
payload
```

The original legacy result is preserved inside:

```text
payload.legacy_result
```

The original path is preserved inside:

```text
payload.legacy_result_path
```

The original legacy status, when present, is preserved inside:

```text
payload.legacy_status
```

---

## 6. Wrapper Status

Wrapped legacy files use:

```text
status: CHECK
```

Reason:

```text
wrapping is format normalization
wrapping is not scientific revalidation
```

Using `PASS` would overstate what happened.

The wrapper confirms that the result is now structurally valid as an OMNIA-VALIDATION envelope.

It does not confirm that the original experiment has been scientifically revalidated.

This rule applies even if the legacy file itself contains:

```text
status: PASS
```

The original legacy status is preserved separately inside:

```text
payload.legacy_status
```

The wrapper status remains:

```text
CHECK
```

because the wrapper describes the normalization operation, not the scientific result.

---

## 7. Manifest

The wrapping process generates a manifest:

```text
results_enveloped/legacy_result_envelope_manifest_v0.json
```

The manifest records:

```text
source_dir
output_dir
total_source_files
wrapped_count
failed_count
wrapped_files
failed_files
interpretation
```

Current result:

```text
total_source_files: 97
wrapped_count: 97
failed_count: 0
```

The manifest itself follows the canonical result envelope.

---

## 8. Validation Commands

Validate a wrapped result:

```bash
omnia-validation validate-result results_enveloped/<result_file>.json
```

Expected output:

```json
{
  "status": "PASS",
  "schema": "result_envelope"
}
```

Validate the manifest:

```bash
omnia-validation validate-result results_enveloped/legacy_result_envelope_manifest_v0.json
```

Expected output:

```json
{
  "status": "PASS",
  "schema": "result_envelope"
}
```

Validate historical JSON parseability:

```bash
omnia-validation validate-json results/<result_file>.json
```

This confirms the original result is readable JSON.

It does not require the historical file to follow the new envelope.

---

## 9. Generation Script

The normalization script is located at:

```text
examples/wrap_legacy_results_in_envelope.py
```

Run:

```bash
python examples/wrap_legacy_results_in_envelope.py
```

This script:

```text
reads results/*.json
does not modify original files
writes wrapped copies to results_enveloped/
generates a manifest
validates every generated envelope internally
preserves legacy status when present
preserves legacy payload exactly as payload.legacy_result
uses CHECK for wrappers because wrapping is not revalidation
```

---

## 10. Non-Destructive Rule

The script must remain non-destructive.

It must not:

```text
delete results/
rewrite results/
overwrite scientific interpretation
change historical payloads
silently change legacy status values
convert legacy PASS into wrapper PASS
```

It may:

```text
copy legacy results
wrap legacy results
preserve legacy data inside payload.legacy_result
preserve legacy status inside payload.legacy_status
write canonical envelopes to results_enveloped/
generate a manifest
```

---

## 11. Correct Interpretation

Correct interpretation:

```text
results/ contains historical raw result artifacts.
results_enveloped/ contains schema-normalized copies.
The original data was preserved.
The normalized copies are easier to validate automatically.
```

Incorrect interpretation:

```text
results_enveloped/ proves the old experiments are scientifically correct.
results_enveloped/ replaces the original results.
results/ should be deleted.
CHECK means failure.
```

`CHECK` means the wrapper is cautious.

It says:

```text
this legacy artifact was normalized into the canonical envelope
without claiming scientific revalidation
```

---

## 12. Why This Matters

This normalization gives the repository two useful layers:

```text
historical continuity
engineering consistency
```

Historical continuity matters because experimental artifacts should not be rewritten casually.

Engineering consistency matters because future tools need a common schema.

The result is:

```text
old evidence remains intact
new validation tooling can operate cleanly
```

---

## 13. Test Coverage

Legacy normalization is now protected by automated tests.

Current test files:

```text
tests/test_existing_results.py
tests/test_enveloped_results.py
tests/test_wrap_legacy_results.py
```

They check:

```text
historical results are valid JSON
enveloped results follow the canonical result envelope
the wrapping script infers experiment names from filenames
the wrapping script preserves legacy status
the wrapping script preserves missing legacy status as null
the wrapping script preserves nested legacy payloads
the wrapping script always uses CHECK for wrappers
the wrapping script produces schema-valid envelopes
```

This means the normalization layer is not only documented.

It is also checked by CI.

---

## 14. Current Normalization State

Current state:

```text
results/ exists
results_enveloped/ exists
legacy wrapper script exists
legacy wrapper tests exist
historical result parseability test exists
enveloped result schema test exists
CI is green
```

Current counts:

```text
legacy result files wrapped: 97
schema-valid enveloped files: 98
wrapping failures: 0
```

The 98 schema-valid enveloped files are:

```text
97 wrapped legacy result files
1 manifest file
```

---

## 15. Future Work

Possible future steps:

```text
add payload-specific legacy normalization checks
add legacy-status mapping documentation
add per-family normalization summaries
add regression tests for future normalization changes
add payload-specific schema validators
add family-specific legacy wrappers
add manifest hash traceability
```

The next strict check should target:

```text
results_enveloped/
```

not:

```text
results/
```

because `results/` intentionally preserves legacy format.

---

## 16. Non-Goal

Legacy normalization does not prove semantic truth.

It does not certify production safety.

It does not validate model intelligence.

It does not reinterpret historical experiments.

It only creates schema-valid wrappers around historical result artifacts.

Final boundary:

```text
measurement != inference != decision
```