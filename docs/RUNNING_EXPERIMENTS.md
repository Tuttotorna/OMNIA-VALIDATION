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

## 5. Run Temporal Collapse Topology Chain

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

## 6. Run Temporal Collapse Level 3 Chain

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

## 7. Validate JSON and JSONL Artifacts

Use the package CLI:

```bash
omnia-validation validate-json results/temporal_collapse_external_source_hash_strengthening_validator_v15.json
```

For JSONL files:

```bash
omnia-validation validate-json data/temporal_collapse_external_source_hash_strengthened_v15.jsonl
```

---

## 8. Compute a File Hash

```bash
omnia-validation hash-file data/temporal_collapse_external_source_hash_strengthened_v15.jsonl
```

This returns a SHA-256 digest.

Use it for reproducibility checks and artifact traceability.

---

## 9. How To Read Results

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

## 10. Negative Results

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

## 11. Clean Execution Rule

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

## 12. Non-Goal

OMNIA-VALIDATION does not certify production safety.

It does not prove semantic correctness.

It does not replace external interpretation.

Final boundary:

```text
measurement != inference != decision
```