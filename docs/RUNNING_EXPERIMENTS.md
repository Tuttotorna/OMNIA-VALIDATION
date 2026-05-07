# Running OMNIA-VALIDATION Experiments

## Purpose

This document explains how to run OMNIA-VALIDATION experiments from a clean environment.

OMNIA-VALIDATION is not a semantic evaluator.

It is a structural validation, falsification, perturbation testing, and reproducibility layer.

Core boundary:

```text
measurement != inference != decision
```

---

## 1. Clone the Repository

```bash
git clone https://github.com/Tuttotorna/OMNIA-VALIDATION.git
cd OMNIA-VALIDATION
```

---

## 2. Create a Python Environment

Python requirement:

```text
Python >= 3.10
```

Recommended setup:

```bash
python -m venv .venv
source .venv/bin/activate
```

On Windows PowerShell:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

---

## 3. Install Development Dependencies

```bash
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
```

This installs the package layer in editable mode and includes:

```text
pytest
ruff
hatchling
```

---

## 4. Verify the Package Layer

Run:

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

Run a CLI smoke test:

```bash
omnia-validation validate-sha256 aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
```

Expected output:

```text
PASS
```

---

## 5. Artifact Validation Commands

OMNIA-VALIDATION currently provides these CLI checks:

```text
omnia-validation hash-file <path>
omnia-validation validate-sha256 <value>
omnia-validation validate-json <path>
omnia-validation validate-result <path>
```

Purpose:

```text
hash-file       -> compute SHA-256 for an artifact
validate-sha256 -> check SHA-256 hexadecimal format
validate-json   -> check JSON / JSONL parseability
validate-result -> check canonical OMNIA-VALIDATION result envelope
```

Important distinction:

```text
validate-json checks that a file is readable JSON or JSONL.
validate-result checks that a JSON result has the required OMNIA-VALIDATION envelope.
```

The canonical result envelope requires:

```text
experiment
status
created_at_utc
boundary
payload
```

Allowed result statuses:

```text
PASS
CHECK
FAIL
```

Boundary:

```text
validate-result checks structure only.
It does not validate semantic truth.
It does not certify production safety.
It does not decide whether the scientific interpretation is correct.
```

---

## 6. Run Temporal Collapse Topology Chain

Run the topology scripts in this order:

```bash
python examples/temporal_collapse_topology_cluster_adjacency_graph_v0.py
python examples/temporal_collapse_topology_cluster_graph_centrality_v0.py
python examples/temporal_collapse_topology_cluster_graph_control_plane_v0.py
python examples/temporal_collapse_topology_control_plane_robustness_v0.py
python examples/temporal_collapse_topology_dependency_map_v0.py
python examples/temporal_collapse_topology_dependency_boundary_v0.py
python examples/temporal_collapse_topology_boundary_phase_diagram_v0.py
```

Expected result files:

```text
results/temporal_collapse_topology_cluster_adjacency_graph_v0.json
results/temporal_collapse_topology_cluster_graph_centrality_v0.json
results/temporal_collapse_topology_cluster_graph_control_plane_v0.json
results/temporal_collapse_topology_control_plane_robustness_v0.json
results/temporal_collapse_topology_dependency_map_v0.json
results/temporal_collapse_topology_dependency_boundary_v0.json
results/temporal_collapse_topology_boundary_phase_diagram_v0.json
```

Important interpretation:

```text
PASS  -> measured behavior survived this validation step
CHECK -> partial instability or boundary condition detected
FAIL  -> collapse, mismatch, or validation failure detected
```

A `CHECK` or `FAIL` result is not automatically a repository failure.

It may be the measured boundary of the system.

---

## 7. Validate Temporal Collapse Topology Results

After running the topology chain, validate that the result files are parseable JSON:

```bash
omnia-validation validate-json results/temporal_collapse_topology_cluster_adjacency_graph_v0.json
omnia-validation validate-json results/temporal_collapse_topology_cluster_graph_centrality_v0.json
omnia-validation validate-json results/temporal_collapse_topology_cluster_graph_control_plane_v0.json
omnia-validation validate-json results/temporal_collapse_topology_control_plane_robustness_v0.json
omnia-validation validate-json results/temporal_collapse_topology_dependency_map_v0.json
omnia-validation validate-json results/temporal_collapse_topology_dependency_boundary_v0.json
omnia-validation validate-json results/temporal_collapse_topology_boundary_phase_diagram_v0.json
```

If the files use the canonical OMNIA-VALIDATION result envelope, also run:

```bash
omnia-validation validate-result results/temporal_collapse_topology_cluster_adjacency_graph_v0.json
omnia-validation validate-result results/temporal_collapse_topology_cluster_graph_centrality_v0.json
omnia-validation validate-result results/temporal_collapse_topology_cluster_graph_control_plane_v0.json
omnia-validation validate-result results/temporal_collapse_topology_control_plane_robustness_v0.json
omnia-validation validate-result results/temporal_collapse_topology_dependency_map_v0.json
omnia-validation validate-result results/temporal_collapse_topology_dependency_boundary_v0.json
omnia-validation validate-result results/temporal_collapse_topology_boundary_phase_diagram_v0.json
```

Expected valid schema output:

```json
{
  "status": "PASS",
  "schema": "result_envelope"
}
```

If `validate-json` passes but `validate-result` fails, the file is valid JSON but does not yet follow the canonical result envelope.

That is an engineering/schema issue, not automatically a scientific failure.

---

## 8. Run Temporal Collapse Level 3 Chain

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

Expected result files:

```text
results/temporal_collapse_cross_provider_disagreement_validator_v13.json
results/temporal_collapse_repeated_run_cross_provider_stability_validator_v14.json
results/temporal_collapse_external_source_hash_strengthening_validator_v15.json
```

V15 should preserve real SHA-256 source traceability.

Expected important fields:

```text
real_hash_count
placeholder_hash_count
hash_format_failure_count
hash_mismatch_failure_count
```

A strong traceability result should show:

```text
placeholder_hash_count: 0
hash_format_failure_count: 0
hash_mismatch_failure_count: 0
```

---

## 9. Validate Temporal Collapse Level 3 Results

First validate parseability:

```bash
omnia-validation validate-json results/temporal_collapse_cross_provider_disagreement_validator_v13.json
omnia-validation validate-json results/temporal_collapse_repeated_run_cross_provider_stability_validator_v14.json
omnia-validation validate-json results/temporal_collapse_external_source_hash_strengthening_validator_v15.json
```

Then validate the OMNIA-VALIDATION result envelope if the files are expected to follow the canonical schema:

```bash
omnia-validation validate-result results/temporal_collapse_cross_provider_disagreement_validator_v13.json
omnia-validation validate-result results/temporal_collapse_repeated_run_cross_provider_stability_validator_v14.json
omnia-validation validate-result results/temporal_collapse_external_source_hash_strengthening_validator_v15.json
```

Expected valid schema output:

```json
{
  "status": "PASS",
  "schema": "result_envelope"
}
```

If validation fails, inspect the reported errors.

Typical schema errors:

```text
missing required field: experiment
missing required field: status
missing required field: created_at_utc
missing required field: boundary
missing required field: payload
status must be one of: CHECK, FAIL, PASS
boundary should be: measurement != inference != decision
payload must be a mapping/object
```

---

## 10. Validate JSON and JSONL Artifacts

Use the package CLI:

```bash
omnia-validation validate-json results/temporal_collapse_external_source_hash_strengthening_validator_v15.json
```

For JSONL files:

```bash
omnia-validation validate-json data/temporal_collapse_external_source_hash_strengthened_v15.jsonl
```

For result JSON files using the canonical envelope:

```bash
omnia-validation validate-result results/temporal_collapse_external_source_hash_strengthening_validator_v15.json
```

Correct validation sequence:

```text
1. validate-json
2. validate-result
```

Meaning:

```text
validate-json   -> file is parseable
validate-result -> file has canonical result envelope
```

---

## 11. Compute a File Hash

```bash
omnia-validation hash-file data/temporal_collapse_external_source_hash_strengthened_v15.jsonl
```

This returns a SHA-256 digest.

Use it for reproducibility checks and artifact traceability.

Validate a SHA-256 digest:

```bash
omnia-validation validate-sha256 aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
```

Expected output:

```text
PASS
```

---

## 12. How To Read Results

Do not read results as semantic truth.

Read them as structural measurements under controlled validation pressure.

Correct reading:

```text
What remained stable?
What became unstable?
What collapsed?
What boundary was exposed?
What condition produced drift?
What condition produced critical behavior?
```

Incorrect reading:

```text
The model is intelligent.
The answer is semantically true.
The benchmark is solved.
The system is production-safe.
The framework is universally valid.
```

---

## 13. Negative Results

Negative results are part of OMNIA-VALIDATION.

They should not be hidden.

A failed or weak result can expose:

```text
threshold instability
representation dependence
observer sensitivity
measurement collapse
dependency boundary
false-positive behavior
semantic/structural separation
```

This is scientifically useful.

---

## 14. Clean Execution Rule

For reproducibility, prefer a clean run:

```bash
git status
pytest -q
ruff check omnia_validation tests
```

Then run the experiment chain.

If files are generated or modified, inspect:

```bash
git status
git diff
```

Commit only intentional changes.

---

## 15. Minimal Result Validation Workflow

For any result file:

```bash
omnia-validation validate-json results/<result_file>.json
omnia-validation validate-result results/<result_file>.json
```

Expected output for valid JSON:

```json
{
  "status": "PASS"
}
```

Expected output for a valid OMNIA-VALIDATION result envelope:

```json
{
  "status": "PASS",
  "schema": "result_envelope"
}
```

If the first command fails:

```text
The file is not valid JSON.
Fix parseability first.
```

If the first command passes but the second fails:

```text
The file is valid JSON but not a canonical OMNIA-VALIDATION result envelope.
Fix experiment/status/created_at_utc/boundary/payload structure.
```

---

## 16. Non-Goal

OMNIA-VALIDATION does not certify production safety.

It does not prove semantic correctness.

It does not replace external interpretation.

Final boundary:

```text
measurement != inference != decision
```