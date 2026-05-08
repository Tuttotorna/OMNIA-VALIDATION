# OMNIA-VALIDATION — Validator Registry

## Purpose

This document provides a structured registry of validators and validation-related scripts in OMNIA-VALIDATION.

The goal is to make the repository easier to inspect, reproduce, extend, and audit.

Core boundary:

```text
measurement != inference != decision
```

This registry does not declare all validators final.

It maps what exists, what each validator is meant to test, and how it should be interpreted.

---

## 1. Registry Principle

A validator is not a truth oracle.

A validator is a controlled structural test.

It should answer questions such as:

```text
what remained stable?
what drifted?
what collapsed?
what boundary was exposed?
what artifact became invalid?
what requires CHECK rather than PASS?
```

A validator should not claim:

```text
semantic truth
model intelligence
production safety
universal validity
final correctness
```

---

## 2. Status Vocabulary

Canonical validator statuses:

```text
PASS
CHECK
FAIL
```

Meaning:

```text
PASS  -> tested structural condition survived this validation step
CHECK -> partial instability, ambiguity, boundary condition, or normalization state
FAIL  -> collapse, mismatch, invalid artifact, or validation failure
```

Important:

```text
CHECK is not cosmetic failure.
CHECK often means a boundary was exposed.
```

---

## 3. Result Layers

The repository contains two result layers:

```text
results/
results_enveloped/
```

Meaning:

```text
results/           -> historical raw result artifacts
results_enveloped/ -> schema-normalized copies of legacy results
```

The legacy wrapper uses:

```text
status: CHECK
```

because:

```text
wrapping is normalization
wrapping is not scientific revalidation
```

---

## 4. Registry Categories

Current registry categories:

```text
schema and package validators
legacy normalization validators
Temporal Collapse Level 3 validators
Temporal Collapse Topology validators
observer and recoverability validators
cross-domain and perturbation validators
structural benchmark validators
future validator families
```

---

## 5. Schema And Package Validators

### Result Envelope Validator

Purpose:

```text
validate canonical OMNIA-VALIDATION result envelopes
```

Code:

```text
omnia_validation/schemas.py
```

CLI:

```bash
omnia-validation validate-result <path>
```

Canonical fields:

```text
experiment
status
created_at_utc
boundary
payload
```

Tests:

```text
tests/test_schemas.py
tests/test_cli.py
tests/test_enveloped_results.py
```

Status:

```text
present
tested
top-level only
not payload-specific yet
```

Boundary:

```text
schema validation checks structure
schema validation does not prove scientific correctness
```

---

### JSON Artifact Validator

Purpose:

```text
validate JSON / JSONL parseability
```

Code:

```text
omnia_validation/io.py
omnia_validation/cli.py
```

CLI:

```bash
omnia-validation validate-json <path>
```

Tests:

```text
tests/test_io.py
tests/test_cli.py
tests/test_existing_results.py
```

Status:

```text
present
tested
used for historical results
```

Boundary:

```text
parseable JSON does not imply canonical result schema
parseable JSON does not imply scientific correctness
```

---

### SHA-256 Validator

Purpose:

```text
validate SHA-256 format
compute file hashes
```

Code:

```text
omnia_validation/hashing.py
omnia_validation/cli.py
```

CLI:

```bash
omnia-validation validate-sha256 <sha256>
omnia-validation hash-file <path>
```

Tests:

```text
tests/test_hashing.py
tests/test_cli.py
```

Status:

```text
present
tested
```

Boundary:

```text
hash validity checks traceability
hash validity does not interpret experiment meaning
```

---

## 6. Legacy Normalization Validators

### Legacy Result Envelope Wrapper

Purpose:

```text
wrap historical result files into canonical result envelopes
without modifying original result files
```

Script:

```text
examples/wrap_legacy_results_in_envelope.py
```

Input:

```text
results/*.json
```

Output:

```text
results_enveloped/*.json
results_enveloped/legacy_result_envelope_manifest_v0.json
```

Tests:

```text
tests/test_wrap_legacy_results.py
tests/test_enveloped_results.py
tests/test_existing_results.py
```

Current result:

```text
legacy results wrapped: 97
schema-valid enveloped files: 98
wrapping failures: 0
```

Wrapper status:

```text
CHECK
```

Reason:

```text
wrapping is format normalization
wrapping is not scientific revalidation
```

Status:

```text
present
tested
CI-guarded
non-destructive
```

Documentation:

```text
docs/LEGACY_RESULT_NORMALIZATION.md
docs/LEGACY_STATUS_MAPPING.md
```

Boundary:

```text
results_enveloped/ does not scientifically revalidate all legacy experiments
```

---

### Legacy Status Preservation

Purpose:

```text
preserve older status values inside canonical wrappers
without automatically reinterpreting them
```

Preserved field:

```text
payload.legacy_status
```

Full legacy payload:

```text
payload.legacy_result
```

Policy:

```text
docs/LEGACY_STATUS_MAPPING.md
```

Tests:

```text
tests/test_wrap_legacy_results.py
```

Status:

```text
present
tested
not yet mapped into validator-specific canonical statuses
```

Boundary:

```text
legacy PASS does not automatically become wrapper PASS
legacy CRITICAL does not automatically become wrapper FAIL
legacy DRIFT does not automatically become wrapper FAIL
```

---

## 7. Temporal Collapse Level 3 Validators

Current Level 3 chain:

```text
V13 -> V14 -> V15
```

Canonical entry point:

```text
docs/TEMPORAL_COLLAPSE_LEVEL_3_INDEX_V0.md
```

Human-readable summary:

```text
docs/TEMPORAL_COLLAPSE_LEVEL_3_FINAL_SUMMARY_V0.md
```

---

### V13 — Cross-Provider Disagreement Validator

Purpose:

```text
detect cross-provider structural disagreement
```

Result:

```text
results/temporal_collapse_cross_provider_disagreement_validator_v13.json
```

Documentation:

```text
docs/TEMPORAL_COLLAPSE_CROSS_PROVIDER_DISAGREEMENT_VALIDATOR_V13.md
docs/TEMPORAL_COLLAPSE_CROSS_PROVIDER_DISAGREEMENT_VALIDATOR_V13_RESULT.md
```

Interpretation:

```text
cross-provider disagreement is structural evidence
not a semantic truth judgment
```

Status:

```text
historical result present
legacy result enveloped
```

Boundary:

```text
provider disagreement does not automatically prove model failure
```

---

### V14 — Repeated-Run Cross-Provider Stability Validator

Purpose:

```text
map repeated-run cross-provider records into raw ordered structural trajectories
```

Script:

```text
examples/temporal_collapse_repeated_run_cross_provider_stability_validator_v14.py
```

Data:

```text
data/temporal_collapse_repeated_run_cross_provider_stability_v14.jsonl
```

Result:

```text
results/temporal_collapse_repeated_run_cross_provider_stability_validator_v14.json
```

Documentation:

```text
docs/TEMPORAL_COLLAPSE_REPEATED_RUN_CROSS_PROVIDER_STABILITY_VALIDATOR_V14.md
docs/TEMPORAL_COLLAPSE_REPEATED_RUN_CROSS_PROVIDER_STABILITY_VALIDATOR_V14_RESULT.md
```

Preserved aggregate result:

```text
aggregate_risk_score: 0.379255
aggregate_risk_regime: DRIFT
aggregate_gate_action: WATCH
aggregate_accuracy_rate: 0.42
aggregate_extraction_rate: 0.9
```

Status:

```text
historical result present
legacy result enveloped
```

Boundary:

```text
DRIFT is a measured regime
not automatic failure
```

---

### V15 — External Source Hash Strengthening Validator

Purpose:

```text
replace symbolic source-file hash placeholders with real computed SHA-256 hashes
```

Script:

```text
examples/temporal_collapse_external_source_hash_strengthening_validator_v15.py
```

Data:

```text
data/temporal_collapse_external_source_hash_strengthened_v15.jsonl
```

Result:

```text
results/temporal_collapse_external_source_hash_strengthening_validator_v15.json
```

Documentation:

```text
docs/TEMPORAL_COLLAPSE_EXTERNAL_SOURCE_HASH_STRENGTHENING_VALIDATOR_V15.md
docs/TEMPORAL_COLLAPSE_EXTERNAL_SOURCE_HASH_STRENGTHENING_VALIDATOR_V15_RESULT.md
```

Current summary:

```text
trajectory_count: 20
event_count: 100
source_file_count: 4
computed_hash_count: 4
real_hash_count: 4
placeholder_hash_count: 0
hash_format_failure_count: 0
hash_mismatch_failure_count: 0
```

Source-output hashes:

```text
data/source_outputs/gsm_symbolic_real_model_outputs_v14_provider_a_run_001.jsonl
sha256:24d7177cea63e44e2616c0d4546ed65fd824719f7fc4030b9a52130c1bf4e00c
```

```text
data/source_outputs/gsm_symbolic_real_model_outputs_v14_provider_a_run_002.jsonl
sha256:602676324b4335e7cb670d6884cbe5e978dacac59889dbc362252440d706dc2e
```

```text
data/source_outputs/gsm_symbolic_real_model_outputs_v14_provider_b_run_001.jsonl
sha256:5ab1f8a6bf24f266a8dbf4e4e952be749db66ae66156bff0835d44088bb8ac5a
```

```text
data/source_outputs/gsm_symbolic_real_model_outputs_v14_provider_b_run_002.jsonl
sha256:5399edf34ba661ece7b6f0855df09ecad7d895a74951bd8bec56ad8074dd9010
```

Status:

```text
historical result present
legacy result enveloped
hash traceability strengthened
```

Boundary:

```text
hash strengthening improves source traceability
it does not prove semantic correctness
```

---

## 8. Temporal Collapse Topology Validators

Canonical entry point:

```text
docs/TEMPORAL_COLLAPSE_TOPOLOGY_INDEX_V0.md
```

Main chain document:

```text
docs/TEMPORAL_COLLAPSE_TOPOLOGY_EXPERIMENT_CHAIN_V0.md
```

Final phase result:

```text
docs/TEMPORAL_COLLAPSE_TOPOLOGY_BOUNDARY_PHASE_DIAGRAM_V0_RESULT.md
```

Current v0 status:

```text
cluster adjacency graph        PASS
cluster graph centrality       PASS
cluster graph control plane    PASS
control-plane robustness       CHECK
dependency map                 PASS
dependency boundary            PASS
boundary phase diagram         PASS
```

Correct reading:

```text
detect structure
test structure
find instability
map instability
classify boundary regimes
```

Incorrect reading:

```text
force every result to PASS
```

---

### Cluster Adjacency Graph Validator

Script:

```text
examples/temporal_collapse_topology_cluster_adjacency_graph_v0.py
```

Result:

```text
results/temporal_collapse_topology_cluster_adjacency_graph_v0.json
```

Purpose:

```text
detect directed adjacency between temporal-collapse signature clusters
```

Status:

```text
PASS in v0 chain
legacy result enveloped
```

---

### Cluster Graph Centrality Validator

Script:

```text
examples/temporal_collapse_topology_cluster_graph_centrality_v0.py
```

Result:

```text
results/temporal_collapse_topology_cluster_graph_centrality_v0.json
```

Purpose:

```text
measure centrality structure in the temporal-collapse cluster graph
```

Status:

```text
PASS in v0 chain
legacy result enveloped
```

---

### Cluster Graph Control Plane Validator

Script:

```text
examples/temporal_collapse_topology_cluster_graph_control_plane_v0.py
```

Result:

```text
results/temporal_collapse_topology_cluster_graph_control_plane_v0.json
```

Purpose:

```text
detect a measurable control plane in the cluster graph
```

Status:

```text
PASS in v0 chain
legacy result enveloped
```

Boundary:

```text
control plane detection does not imply universal invariance
```

---

### Control-Plane Robustness Validator

Script:

```text
examples/temporal_collapse_topology_control_plane_robustness_v0.py
```

Result:

```text
results/temporal_collapse_topology_control_plane_robustness_v0.json
```

Purpose:

```text
test robustness of the detected control plane under perturbation
```

Status:

```text
CHECK in v0 chain
legacy result enveloped
```

Interpretation:

```text
the control plane is not fully robust under all tested perturbations
```

Boundary:

```text
CHECK is the measured boundary
not something to hide
```

---

### Dependency Map Validator

Script:

```text
examples/temporal_collapse_topology_dependency_map_v0.py
```

Result:

```text
results/temporal_collapse_topology_dependency_map_v0.json
```

Purpose:

```text
map dependency structure after control-plane instability is exposed
```

Status:

```text
PASS in v0 chain
legacy result enveloped
```

---

### Dependency Boundary Validator

Script:

```text
examples/temporal_collapse_topology_dependency_boundary_v0.py
```

Result:

```text
results/temporal_collapse_topology_dependency_boundary_v0.json
```

Purpose:

```text
detect dependency boundaries in temporal-collapse topology
```

Status:

```text
PASS in v0 chain
legacy result enveloped
```

---

### Boundary Phase Diagram Validator

Script:

```text
examples/temporal_collapse_topology_boundary_phase_diagram_v0.py
```

Result:

```text
results/temporal_collapse_topology_boundary_phase_diagram_v0.json
```

Purpose:

```text
classify boundary regimes after dependency-boundary mapping
```

Status:

```text
PASS in v0 chain
legacy result enveloped
```

Safe canonical claim:

```text
OMNIA-VALIDATION detected a directed temporal-collapse signature topology
with a measurable control plane and a dependency boundary phase diagram.

The tested variant axis remained stable, while family and threshold axes
exposed drift and critical boundaries.
```

Boundary:

```text
the control plane is not universally invariant
```

---

## 9. Additional Temporal Collapse Topology Scripts

The repository also contains additional temporal-collapse topology result families.

Examples include:

```text
temporal_collapse_topology_absorption_depth_v0
temporal_collapse_topology_attractor_v0
temporal_collapse_topology_attractor_stability_v0
temporal_collapse_topology_basin_entry_v0
temporal_collapse_topology_basin_escape_v0
temporal_collapse_topology_boundary_cycle_v0
temporal_collapse_topology_escape_depth_stability_v0
temporal_collapse_topology_geometry_sensitivity_v0
temporal_collapse_topology_noise_robustness_v0
temporal_collapse_topology_phase_transition_v0
temporal_collapse_topology_reversibility_index_v0
temporal_collapse_topology_signature_cluster_invariance_v0
temporal_collapse_topology_stability_v0
temporal_collapse_topology_target_reachability_v0
temporal_collapse_topology_threshold_boundary_v0
temporal_collapse_topology_threshold_sensitivity_v0
temporal_collapse_topology_transition_graph_v0
temporal_collapse_topology_transition_graph_stability_v0
temporal_collapse_topology_transition_signature_stability_v0
temporal_collapse_topology_variable_run_length_v0
temporal_collapse_topology_window_sensitivity_v0
```

Status:

```text
historical results present
legacy results enveloped
not all individually documented in this registry yet
```

Future work:

```text
add per-validator entries
add reproduction order
add payload-specific schema expectations
add regression tests
```

---

## 10. Observer And Recoverability Validators

Existing result families include:

```text
effective_observer_count_v0
effective_observer_recoverability_gate_v0
effective_observer_recoverability_gate_stability_v0
effective_observer_recoverability_gate_adversarial_v0
effective_observer_recoverability_gate_external_proxy_v0
effective_observer_recoverability_gate_randomized_v0
effective_observer_recoverability_gate_randomized_stability_v0
recoverability_effective_observer_v0
recoverability_effective_observer_v1
observer_family_geometry_v0
observer_family_geometry_v1
observer_family_geometry_v2
observer_family_geometry_v3
observer_family_geometry_adversarial_v0
```

Purpose family:

```text
measure observer sensitivity
measure effective observer behavior
measure recoverability under structural variation
measure observer-family geometry
```

Status:

```text
historical results present
legacy results enveloped
payload-specific schemas not yet enforced
```

Boundary:

```text
observer-structure measurement is not consciousness detection
observer sensitivity is not semantic truth
```

---

## 11. Cross-Domain And Perturbation Validators

Existing result families include:

```text
perturbation_consistency_v0
adversarial_representation_v0
cross_domain_invariance_v0
cross_domain_invariance_v0_1
cross_domain_invariance_v0_2
semantic_vs_structural_separation_v0
trajectory_geometry_v0
projection_boundary_map_v0
projection_resilience_layer_v0
structural_boundary_resilience_v1
structural_boundary_resilience_v2
resilience_regression_suite_v0
resilience_regression_negative_control_v0
```

Purpose family:

```text
test perturbation consistency
test representation dependence
test cross-domain invariance claims
test semantic-vs-structural separation
test trajectory geometry
test projection boundaries
test resilience behavior
```

Status:

```text
historical results present
legacy results enveloped
not all payloads have family-specific validators yet
```

Boundary:

```text
cross-domain structural similarity is not universal validity
semantic separation tests are not semantic truth detectors
```

---

## 12. Cross-Gate Validators

Existing result families include:

```text
cross_gate_disagreement_analysis_v0
cross_gate_disagreement_stability_v0
cross_gate_real_dataset_proxy_v0
cross_gate_real_dataset_proxy_stressed_v0
cross_gate_real_dataset_proxy_collapse_v0
```

Purpose family:

```text
measure disagreement and stability across gate-like validation structures
test proxy real-dataset behavior
test collapse under stress
```

Status:

```text
historical results present
legacy results enveloped
```

Boundary:

```text
gate disagreement is a structural signal
not automatic production rejection
```

---

## 13. Structural Benchmark Validators

Existing result families include:

```text
structural_benchmark_dataset_v0_summary
structural_benchmark_runner_v0
structural_alias_detector_v3
structural_alias_detector_v4
```

Purpose family:

```text
summarize structural benchmark datasets
run structural benchmark checks
detect structural aliasing behavior
```

Status:

```text
historical results present
legacy results enveloped
```

Boundary:

```text
benchmark structure does not imply universal benchmark validity
```

---

## 14. Collapse Confirmation Validators

Existing result families include:

```text
collapse_confirmation_stability_v0
collapse_confirmation_source_swap_v0
temporal_collapse_confirmation_v0
temporal_collapse_critical_horizon_corrected_v0
temporal_collapse_dynamic_horizon_v0
temporal_collapse_fragmentation_classification_v0
temporal_collapse_persistence_v0
temporal_collapse_persistence_stability_v0
temporal_collapse_phase_diagram_v0
temporal_collapse_regime_reset_v0
```

Purpose family:

```text
test collapse confirmation behavior
test source swaps
test dynamic and corrected horizons
test persistence and fragmentation
test phase diagrams and regime resets
```

Status:

```text
historical results present
legacy results enveloped
```

Boundary:

```text
collapse-like structural behavior is not automatically semantic failure
```

---

## 15. Current Registry Status

Current registry status:

```text
partial registry
major validator families mapped
Level 3 chain mapped
Topology v0 chain mapped
legacy normalization mapped
schema/package validators mapped
additional families listed
not yet full per-file registry
```

This registry is useful for navigation.

It is not yet a complete formal validator registry.

---

## 16. Future Registry Work

Future improvements:

```text
add every validator script with exact input/output paths
add payload schema expectation per validator
add PASS/CHECK/FAIL rule per validator
add reproducibility command per validator
add linked result documentation per validator
add regression-test status per validator
add hash traceability status per validator
add external reproduction status per validator
```

Possible future structure:

```text
validator_id
script_path
input_paths
output_paths
docs_paths
status_rule
payload_schema
test_status
CI_status
known_boundary
```

---

## 17. Correct Interpretation

Correct interpretation:

```text
this registry maps validators and validation-related scripts
this registry helps reproduction and maintenance
this registry separates families of validation work
this registry preserves boundaries and non-claims
```

Incorrect interpretation:

```text
every listed validator is final
every listed result is universally validated
a registry entry proves semantic truth
a registry entry certifies production safety
```

---

## 18. Non-Goal

This registry does not make OMNIA-VALIDATION complete.

It does not certify all experiments.

It does not replace the validator documentation.

It does not replace independent reproduction.

It provides a structured map of the validation layer.

Final boundary:

```text
measurement != inference != decision
```