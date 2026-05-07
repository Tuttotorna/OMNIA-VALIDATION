# Pull Request

## Summary

Describe the change.

```text
What changed?
Why was it needed?
What files were affected?
```

Core boundary:

```text
measurement != inference != decision
```

---

## Change Type

Select the change type:

```text
package utility
CLI
schema validation
test
experiment script
result artifact
legacy normalization
documentation
maintenance
release policy
other
```

---

## Files Changed

List important files:

```text
path/to/file
path/to/file
path/to/file
```

---

## Validation Performed

Run:

```bash
pytest -q
```

Run:

```bash
ruff check omnia_validation tests
```

If result files changed, run:

```bash
omnia-validation validate-json results/<result_file>.json
python examples/wrap_legacy_results_in_envelope.py
pytest -q
```

If enveloped result files changed, run:

```bash
omnia-validation validate-result results_enveloped/legacy_result_envelope_manifest_v0.json
pytest -q
```

Paste output:

```text
<validation output here>
```

---

## Result Artifact Impact

Does this PR affect result artifacts?

```text
yes/no
```

If yes, specify:

```text
results/
results_enveloped/
data/
examples/
docs/
```

---

## Legacy Result Impact

Does this PR modify historical files in `results/`?

```text
yes/no
```

If yes, explain why.

```text
<explanation>
```

Historical result files should not be rewritten casually.

Prefer schema-normalized wrappers in:

```text
results_enveloped/
```

---

## Schema Impact

Does this PR affect the canonical result envelope?

```text
yes/no
```

Current canonical fields:

```text
experiment
status
created_at_utc
boundary
payload
```

If yes, update:

```text
omnia_validation/schemas.py
tests/test_schemas.py
tests/test_cli.py
docs/RESULT_SCHEMA.md
docs/PACKAGE_API.md
docs/PROJECT_STATUS.md
```

---

## Documentation Impact

If public behavior changed, update relevant docs:

```text
README.md
docs/INDEX.md
docs/QUICKSTART.md
docs/PROJECT_STATUS.md
docs/MAINTENANCE.md
docs/RELEASE_POLICY.md
docs/RUNNING_EXPERIMENTS.md
docs/VALIDATOR_AUTHORING_GUIDE.md
docs/RESULT_SCHEMA.md
docs/PACKAGE_API.md
docs/LEGACY_RESULT_NORMALIZATION.md
docs/LEGACY_STATUS_MAPPING.md
```

---

## Non-Claim Check

This PR does not claim:

```text
semantic truth
model intelligence
production safety
universal validity
final correctness
```

This PR preserves the boundary:

```text
measurement != inference != decision
```

---

## Checklist

```text
[ ] pytest -q passes
[ ] ruff check omnia_validation tests passes
[ ] README updated if needed
[ ] docs/INDEX.md updated if needed
[ ] docs/PROJECT_STATUS.md updated if status changed
[ ] docs/PACKAGE_API.md updated if package API changed
[ ] docs/RESULT_SCHEMA.md updated if schema changed
[ ] legacy results were not rewritten silently
[ ] negative or CHECK results were not hidden
[ ] no credentials or tokens were committed
```