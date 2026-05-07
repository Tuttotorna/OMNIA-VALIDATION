# OMNIA-VALIDATION — Quickstart

## Purpose

This document gives a minimal operational path for using OMNIA-VALIDATION from a clean environment.

It is for users who want to:

```text
clone the repository
install the package layer
run tests
validate artifacts
understand results/
understand results_enveloped/
run the legacy wrapper
```

Core boundary:

```text
measurement != inference != decision
```

---

## 1. Clone The Repository

```bash
git clone https://github.com/Tuttotorna/OMNIA-VALIDATION.git
cd OMNIA-VALIDATION
```

---

## 2. Install In Editable Mode

Python requirement:

```text
Python >= 3.10
```

Install:

```bash
python -m pip install --upgrade pip
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

---

## 3. Run Tests

```bash
pytest -q
```

Run linting:

```bash
ruff check omnia_validation tests
```

Expected state:

```text
tests pass
ruff passes
CI should remain green
```

---

## 4. Run Basic CLI Checks

Validate a SHA-256 string:

```bash
omnia-validation validate-sha256 aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
```

Expected output:

```text
PASS
```

Validate JSON:

```bash
omnia-validation validate-json results/temporal_collapse_external_source_hash_strengthening_validator_v15.json
```

Expected output:

```json
{
  "status": "PASS"
}
```

Validate a canonical result envelope:

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

---

## 5. Understand Result Directories

OMNIA-VALIDATION intentionally has two result layers.

```text
results/
```

Historical result artifacts.

These preserve original experiment output.

They may not follow the current canonical result envelope.

```text
results_enveloped/
```

Schema-normalized copies of legacy results.

These follow the canonical result envelope:

```text
experiment
status
created_at_utc
boundary
payload
```

Correct interpretation:

```text
results/ preserves historical evidence.
results_enveloped/ provides schema-valid wrappers.
```

Incorrect interpretation:

```text
results_enveloped/ scientifically revalidates all legacy experiments.
results/ should be deleted.
```

---

## 6. Regenerate Enveloped Results

Run:

```bash
python examples/wrap_legacy_results_in_envelope.py
```

Then run:

```bash
pytest -q
```

This checks:

```text
historical results are parseable JSON
enveloped results follow the canonical schema
the wrapper preserves legacy payloads
the wrapper preserves legacy statuses
the wrapper uses CHECK because wrapping is not revalidation
```

---

## 7. Validate A Result File

For a historical result:

```bash
omnia-validation validate-json results/<result_file>.json
```

For an enveloped result:

```bash
omnia-validation validate-result results_enveloped/<result_file>.json
```

Meaning:

```text
validate-json   -> file is parseable JSON or JSONL
validate-result -> file follows the canonical OMNIA-VALIDATION result envelope
```

---

## 8. Run Temporal Collapse Topology Chain

Run:

```bash
python examples/temporal_collapse_topology_cluster_adjacency_graph_v0.py
python examples/temporal_collapse_topology_cluster_graph_centrality_v0.py
python examples/temporal_collapse_topology_cluster_graph_control_plane_v0.py
python examples/temporal_collapse_topology_control_plane_robustness_v0.py
python examples/temporal_collapse_topology_dependency_map_v0.py
python examples/temporal_collapse_topology_dependency_boundary_v0.py
python examples/temporal_collapse_topology_boundary_phase_diagram_v0.py
```

Then validate generated result JSON:

```bash
omnia-validation validate-json results/temporal_collapse_topology_boundary_phase_diagram_v0.json
```

If a result is canonical-envelope formatted, also run:

```bash
omnia-validation validate-result results/temporal_collapse_topology_boundary_phase_diagram_v0.json
```

---

## 9. Run Temporal Collapse Level 3 Chain

Current chain:

```text
V13 -> V14 -> V15
```

Run:

```bash
python examples/temporal_collapse_cross_provider_disagreement_validator_v13.py
python examples/temporal_collapse_repeated_run_cross_provider_stability_validator_v14.py
python examples/temporal_collapse_external_source_hash_strengthening_validator_v15.py
```

Then validate:

```bash
omnia-validation validate-json results/temporal_collapse_external_source_hash_strengthening_validator_v15.json
```

---

## 10. Read Results Correctly

Correct reading:

```text
What remained stable?
What drifted?
What collapsed?
What boundary was exposed?
What needs CHECK instead of PASS?
```

Incorrect reading:

```text
This proves semantic truth.
This certifies model intelligence.
This guarantees production safety.
This proves universal validity.
```

OMNIA-VALIDATION measures structural behavior under controlled validation pressure.

It does not make final decisions.

---

## 11. Minimal Maintenance Loop

Before pushing changes:

```bash
pytest -q
ruff check omnia_validation tests
git status --short
```

If result files changed:

```bash
omnia-validation validate-json results/<result_file>.json
python examples/wrap_legacy_results_in_envelope.py
pytest -q
```

If enveloped results changed:

```bash
omnia-validation validate-result results_enveloped/legacy_result_envelope_manifest_v0.json
pytest -q
```

---

## 12. Key Documents

Start here:

```text
README.md
docs/INDEX.md
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

## 13. Non-Goal

This quickstart does not certify scientific correctness.

It gives the minimal operational path for running, testing, and validating the repository structure.

Final boundary:

```text
measurement != inference != decision
```