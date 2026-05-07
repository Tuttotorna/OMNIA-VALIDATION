# OMNIA-VALIDATION

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.20068812.svg)](https://doi.org/10.5281/zenodo.20068812)

Structural validation, falsification, perturbation testing, and reproducibility layer for the OMNIA ecosystem.

OMNIA-VALIDATION exists to pressure-test structural measurements.

Its purpose is not to defend OMNIA.

Its purpose is to expose what survives controlled validation, and what collapses under perturbation, falsification, threshold changes, observer variation, and reproducibility checks.

```text
measurement != inference != decision
```

---

## Documentation Index

Canonical documentation index:

```text
docs/INDEX.md
```

Current project status:

```text
docs/PROJECT_STATUS.md
```

Maintenance guide:

```text
docs/MAINTENANCE.md
```

Clean execution guide:

```text
docs/RUNNING_EXPERIMENTS.md
```

Validator authoring guide:

```text
docs/VALIDATOR_AUTHORING_GUIDE.md
```

Common result schema:

```text
docs/RESULT_SCHEMA.md
```

Package API reference:

```text
docs/PACKAGE_API.md
```

Legacy result normalization:

```text
docs/LEGACY_RESULT_NORMALIZATION.md
```

Legacy status mapping:

```text
docs/LEGACY_STATUS_MAPPING.md
```

Engineering consolidation roadmap:

```text
docs/CONSOLIDATION_ROADMAP_V0.md
```

Contribution guide:

```text
CONTRIBUTING.md
```

Security policy:

```text
SECURITY.md
```

---

## Package Layer

OMNIA-VALIDATION now includes a minimal installable Python package layer:

```text
omnia_validation/
```

Current reusable modules:

```text
omnia_validation.hashing
omnia_validation.io
omnia_validation.metrics
omnia_validation.metadata
omnia_validation.schemas
omnia_validation.cli
```

The package API is documented in:

```text
docs/PACKAGE_API.md
```

This package layer does not replace the experimental scripts.

It provides reusable support utilities for reproducibility, hashing, JSON/JSONL handling, metadata envelopes, simple structural metrics, result schema validation, and command-line artifact checks.

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

Example CLI checks:

```bash
omnia-validation validate-sha256 aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
omnia-validation validate-json results/example.json
omnia-validation validate-result results/example.json
omnia-validation hash-file data/example.jsonl
```

CLI command meaning:

```text
validate-sha256 -> check SHA-256 hexadecimal format
validate-json   -> check JSON / JSONL parseability
validate-result -> check canonical OMNIA-VALIDATION result envelope
hash-file       -> compute SHA-256 for an artifact
```

Important distinction:

```text
validate-json checks whether the file is parseable.
validate-result checks whether the result follows the OMNIA-VALIDATION envelope.
```

Current canonical result envelope:

```text
experiment
status
created_at_utc
boundary
payload
```

Boundary:

```text
validate-result checks structural schema only.
It does not validate semantic truth.
It does not certify production safety.
It does not decide whether the scientific interpretation is correct.
```

---

## Continuous Integration

The repository includes a GitHub Actions workflow:

```text
.github/workflows/ci.yml
```

The CI checks:

```text
Python 3.10
Python 3.11
Python 3.12
package installation
ruff
pytest
CLI smoke test
```

This makes the repository more reproducible without changing the research boundary.

---

## Maintenance

Maintenance rules are defined in:

```text
docs/MAINTENANCE.md
```

Before pushing changes, run:

```bash
pytest -q
ruff check omnia_validation tests
```

If result files change, validate the changed file and regenerate enveloped results when needed:

```bash
omnia-validation validate-json results/<result_file>.json
python examples/wrap_legacy_results_in_envelope.py
pytest -q
```

Maintenance must preserve evidence while improving reproducibility.

It must not:

```text
rewrite old results silently
delete negative results
convert CHECK to PASS without revalidation
hide failures
remove boundary statements
treat normalization as scientific proof
```

---

## Purpose

OMNIA-VALIDATION tests whether structural measurements remain meaningful under controlled pressure.

The repository studies:

```text
perturbation behavior
adversarial pressure
representation changes
synthetic stress
cross-run reproducibility
observer variation
threshold sensitivity
falsification attempts
structural collapse
boundary instability
```

This repository is intentionally pressure-oriented.

A failed experiment is not hidden.

A weak result is not rewritten as a strong result.

A structural collapse is preserved as evidence.

The purpose is not to protect OMNIA from failure.

The purpose is to expose failure when failure exists.

---

## Core Position

OMNIA-VALIDATION does not assume that OMNIA is universally correct.

It tests two things:

```text
what survives structured criticism
```

and:

```text
what collapses under controlled validation
```

This distinction is fundamental.

A measurement framework becomes stronger when its failure boundaries become clearer.

---

## Core Boundary

OMNIA-VALIDATION validates structural measurements only.

It does not validate:

```text
semantic truth
intelligence
consciousness
correctness guarantees
universal scientific laws
final decisions
domain-independent truth
```

Interpretation remains external.

Decision remains external.

```text
measurement != inference != decision
```

---

## What This Repository Tests

Current validation directions include:

```text
perturbation consistency
cross-run reproducibility
observer sensitivity
representation dependence
structural persistence
instability emergence
threshold robustness
metric collapse behavior
false-positive generation
semantic-vs-structural separation
trajectory reproducibility
adversarial perturbation behavior
saturation stability
irreversibility consistency
dependency-boundary behavior
phase-like structural regimes
```

The objective is to determine where a measurement remains stable, where it becomes unstable, where it becomes misleading, and where it collapses entirely.

---

## Validation Philosophy

The repository is built around a falsification-oriented philosophy.

The objective is not:

```text
prove OMNIA correct
```

The objective is:

```text
attempt to break OMNIA measurements
under controlled conditions
```

If a measurement collapses under validation:

```text
the collapse is preserved
the limitation is documented
the negative result remains public
the boundary becomes part of the measured system
```

Negative results are considered part of the system.

---

## Structural Validation Principle

Core principle:

```text
a measurement framework becomes stronger
when its failure boundaries become clearer
```

OMNIA-VALIDATION therefore preserves:

```text
failed experiments
weak correlations
unstable thresholds
broken assumptions
reproducibility failures
semantic contradictions
metric instability
dependency failures
boundary collapses
```

This is intentional.

The repository is not designed to produce only positive results.

It is designed to make structural behavior harder to fake.

---

## Current Validation Domains

Validation currently includes experiments involving:

```text
LLM perturbation behavior
structural drift
symbolic reasoning
software transformations
trajectory geometry
observer variation
cryptographic perturbation
chaotic dynamics
representation-sensitive instability
synthetic perturbation families
temporal-collapse topology
dependency-boundary phase behavior
```

The repository may expand toward additional domains over time.

---

## Current Validation Targets

The repository currently stress-tests measurements such as:

```text
Ω      -> structural coherence
IRI    -> irreversibility
SEI    -> saturation / exhaustion
TΔ     -> divergence timing
R      -> resilience
Ω̂      -> residual invariant structure
```

The objective is to determine:

```text
where these measurements remain stable
where they become unstable
where they become misleading
where they collapse entirely
```

---

## Temporal Collapse Topology

One current validation line studies temporal-collapse behavior as a structural topology.

This line asks:

```text
Does temporal-collapse behavior expose a stable structural topology,
or is it only a collection of isolated trajectory labels?
```

The v0 chain detected:

```text
directed signature-cluster topology
centrality structure
control plane
dependency map
dependency boundary map
boundary phase diagram
```

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

Safe canonical claim:

```text
OMNIA-VALIDATION detected a directed temporal-collapse signature topology
with a measurable control plane and a dependency boundary phase diagram.

The tested variant axis remained stable, while family and threshold axes
exposed drift and critical boundaries.
```

Important limitation:

```text
The control plane is not universally invariant.
```

This is not a failure of the chain.

It is the measured boundary of the chain.

---

## Temporal Collapse Topology — V0 Results

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

The `CHECK` result in the robustness test is important.

It shows that the control plane is not fully robust under all tested perturbations.

That instability is then mapped by the dependency-map, dependency-boundary, and phase-diagram experiments.

The correct reading is:

```text
detect structure
test structure
find instability
map instability
classify boundary regimes
```

Not:

```text
force every result to PASS
```

---

## Temporal Collapse Topology — Reproduction Order

Run the temporal-collapse topology scripts in this order:

```bash
python examples/temporal_collapse_topology_cluster_adjacency_graph_v0.py
python examples/temporal_collapse_topology_cluster_graph_centrality_v0.py
python examples/temporal_collapse_topology_cluster_graph_control_plane_v0.py
python examples/temporal_collapse_topology_control_plane_robustness_v0.py
python examples/temporal_collapse_topology_dependency_map_v0.py
python examples/temporal_collapse_topology_dependency_boundary_v0.py
python examples/temporal_collapse_topology_boundary_phase_diagram_v0.py
```

Result files:

```text
results/temporal_collapse_topology_cluster_adjacency_graph_v0.json
results/temporal_collapse_topology_cluster_graph_centrality_v0.json
results/temporal_collapse_topology_cluster_graph_control_plane_v0.json
results/temporal_collapse_topology_control_plane_robustness_v0.json
results/temporal_collapse_topology_dependency_map_v0.json
results/temporal_collapse_topology_dependency_boundary_v0.json
results/temporal_collapse_topology_boundary_phase_diagram_v0.json
```

---

## Temporal Collapse Level 3

Another current validation line studies Level 3 temporal-collapse behavior.

Level 3 focuses on raw ordered structural trajectories, repeated-run behavior, cross-provider behavior, collapse-like boundary proximity, and external-source traceability.

Current Level 3 chain:

```text
V13 -> V14 -> V15
```

Current strongest result:

```text
V15 HASH STRENGTHENING PASSED
```

Canonical Level 3 entry point:

```text
docs/TEMPORAL_COLLAPSE_LEVEL_3_INDEX_V0.md
```

Human-readable summary:

```text
docs/TEMPORAL_COLLAPSE_LEVEL_3_FINAL_SUMMARY_V0.md
```

---

## Temporal Collapse Level 3 — Current Chain

### V13

```text
V13: cross-provider disagreement validator
```

V13 detects cross-provider structural disagreement.

Relevant files:

```text
docs/TEMPORAL_COLLAPSE_CROSS_PROVIDER_DISAGREEMENT_VALIDATOR_V13.md
docs/TEMPORAL_COLLAPSE_CROSS_PROVIDER_DISAGREEMENT_VALIDATOR_V13_RESULT.md
results/temporal_collapse_cross_provider_disagreement_validator_v13.json
```

### V14

```text
V14: repeated-run cross-provider stability validator
```

V14 maps repeated-run cross-provider GSM-Symbolic model-output records into raw ordered structural trajectories.

Relevant files:

```text
docs/TEMPORAL_COLLAPSE_REPEATED_RUN_CROSS_PROVIDER_STABILITY_VALIDATOR_V14.md
docs/TEMPORAL_COLLAPSE_REPEATED_RUN_CROSS_PROVIDER_STABILITY_VALIDATOR_V14_RESULT.md
examples/temporal_collapse_repeated_run_cross_provider_stability_validator_v14.py
data/temporal_collapse_repeated_run_cross_provider_stability_v14.jsonl
results/temporal_collapse_repeated_run_cross_provider_stability_validator_v14.json
```

### V15

```text
V15: external source hash strengthening validator
```

V15 replaces symbolic source-file hash placeholders with real computed SHA-256 hashes.

Relevant files:

```text
docs/TEMPORAL_COLLAPSE_EXTERNAL_SOURCE_HASH_STRENGTHENING_VALIDATOR_V15.md
docs/TEMPORAL_COLLAPSE_EXTERNAL_SOURCE_HASH_STRENGTHENING_VALIDATOR_V15_RESULT.md
examples/temporal_collapse_external_source_hash_strengthening_validator_v15.py
data/temporal_collapse_external_source_hash_strengthened_v15.jsonl
results/temporal_collapse_external_source_hash_strengthening_validator_v15.json
```

---

## Temporal Collapse Level 3 — V15 Result

V15 validation summary:

```text
experiment: temporal_collapse_external_source_hash_strengthening_validator_v15
status: v15_external_source_hash_strengthened
trajectory_count: 20
event_count: 100
source_file_count: 4
computed_hash_count: 4
real_hash_count: 4
placeholder_hash_count: 0
hash_format_failure_count: 0
hash_mismatch_failure_count: 0
```

Aggregate structural result preserved from V14:

```text
aggregate_risk_score: 0.379255
aggregate_risk_regime: DRIFT
aggregate_gate_action: WATCH
aggregate_accuracy_rate: 0.42
aggregate_extraction_rate: 0.9
```

Regime counts:

```text
CRITICAL: 4
DRIFT: 10
STABLE: 6
```

Highest-risk local trajectory:

```text
gsm_symbolic_repeated_run_provider_b_run_002_collapse_like_001
```

Highest-risk score:

```text
0.7096
```

Highest-risk provider:

```text
provider_b
```

Highest-risk run:

```text
provider_b_run_v14_002
```

Correct reading:

```text
aggregate condition: DRIFT
aggregate gate action: WATCH
highest local risk: CRITICAL
strongest local behavior: collapse-like trajectory
source traceability: strengthened with real SHA-256 hashes
```

---

## Temporal Collapse Level 3 — Source Hashes

V15 computed real SHA-256 hashes for the source-output files:

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

The important result is:

```text
real_hash_count: 4
placeholder_hash_count: 0
hash_format_failure_count: 0
hash_mismatch_failure_count: 0
```

This means the source-file trace is no longer only symbolic.

---

## Legacy Result Normalization

The repository intentionally contains both:

```text
results/
results_enveloped/
```

They are not duplicates in purpose.

They represent two different layers.

```text
results/
```

contains historical result artifacts in their original format.

```text
results_enveloped/
```

contains schema-normalized copies of those historical artifacts.

The original results were not rewritten.

The normalized copies are wrapped into the canonical OMNIA-VALIDATION result envelope:

```text
experiment
status
created_at_utc
boundary
payload
```

The legacy result is preserved inside:

```text
payload.legacy_result
```

The legacy result path is preserved inside:

```text
payload.legacy_result_path
```

The legacy status, when present, is preserved inside:

```text
payload.legacy_status
```

The wrapping process was generated by:

```text
examples/wrap_legacy_results_in_envelope.py
```

The normalization manifest is located at:

```text
results_enveloped/legacy_result_envelope_manifest_v0.json
```

Current normalization status:

```text
legacy results wrapped: 97
schema-valid enveloped files: 98
wrapping failures: 0
```

Correct interpretation:

```text
results/ preserves historical evidence.
results_enveloped/ provides schema-valid wrappers.
```

Incorrect interpretation:

```text
results_enveloped/ scientifically revalidates every legacy experiment.
results_enveloped/ replaces the original results.
results/ should be deleted.
```

Legacy normalization is format normalization only.

It is not semantic validation.

It is not scientific revalidation.

Documentation:

```text
docs/LEGACY_RESULT_NORMALIZATION.md
```

---

## Legacy Status Mapping

Historical results may contain legacy status values created before the canonical schema existed.

Examples:

```text
DRIFT
STABLE
CRITICAL
WATCH
passed
stable
collapse-like
v15_external_source_hash_strengthened
```

The current canonical schema allows only:

```text
PASS
CHECK
FAIL
```

Current policy:

```text
legacy status values are preserved
legacy status values are not erased
legacy status values are stored inside payload.legacy_status
wrapped legacy files use canonical status CHECK
automatic scientific reinterpretation is not applied
```

Reason:

```text
wrapping is normalization
wrapping is not revalidation
```

This prevents a format conversion from being falsely presented as a scientific rerun.

Documentation:

```text
docs/LEGACY_STATUS_MAPPING.md
```

---

## Temporal Collapse Level 3 — Boundary

Level 3 does not claim:

```text
OMNIA solves GSM-Symbolic
OMNIA replaces benchmark correctness
OMNIA detects semantic truth
OMNIA proves model intelligence
OMNIA proves model failure
OMNIA certifies production safety
OMNIA makes final decisions
```

Level 3 claims only:

```text
OMNIA measures structural behavior under ordered transformations,
repeated-run variation,
cross-provider variation,
and source-traceable validation conditions.
```

Boundary:

```text
measurement != inference != decision
```

---

## What This Repository Does Not Claim

OMNIA-VALIDATION does not claim:

```text
universal validity
universal invariance
semantic correctness detection
truth detection
mathematical completeness
scientific finality
production certification
domain-independent guarantees
decision authority
```

The repository is exploratory and adversarial by design.

A result is valid only inside its tested construction unless later validation expands the boundary.

---

## Reproducibility Policy

All validation experiments should aim to include:

```text
executable scripts
bounded datasets
deterministic settings when possible
parameter visibility
transformation visibility
reproducible execution paths
environment notes
result files
negative outcomes when relevant
```

Validation without reproducibility is considered weak evidence.

A result should be readable, runnable, and falsifiable.

---

## Negative Result Policy

Negative results are preserved intentionally.

This repository does not hide:

```text
failed hypotheses
weak correlations
threshold instability
contradictory outcomes
unexpected behavior
measurement collapse
boundary sensitivity
partial robustness
```

Negative evidence defines what the framework is not measuring.

This is considered scientifically valuable.

---

## Semantic Separation Policy

OMNIA measurements are structural.

They are not semantic truth guarantees.

Example:

```text
a semantically wrong answer
may remain structurally stable
```

and:

```text
a semantically correct answer
may become structurally unstable
```

OMNIA-VALIDATION actively studies this separation.

Structural stability is not semantic correctness.

Structural instability is not semantic incorrectness.

The two domains must not be confused.

---

## Validation Categories

### Reproducibility Validation

Tests whether measurements remain stable across repeated runs.

Focus areas:

```text
run consistency
threshold stability
parameter sensitivity
reproducible trajectories
```

---

### Perturbation Validation

Tests how measurements react under controlled transformations.

Focus areas:

```text
noise injection
representation changes
structural drift
adversarial perturbations
trajectory degradation
```

---

### Falsification Validation

Attempts to reduce measurements to simpler explanations.

Examples:

```text
churn-only explanations
entropy-only explanations
syntax-only explanations
representation-only explanations
topology-only explanations
threshold-only explanations
```

The objective is to determine whether the measurement survives reduction attempts.

---

### Cross-Domain Validation

Tests whether structurally similar behaviors emerge across heterogeneous systems.

Current directions include:

```text
LLM behavior
software systems
chaotic trajectories
cryptographic systems
synthetic perturbation spaces
temporal-collapse trajectories
```

---

### Boundary Validation

Studies where measurements fail.

Focus areas:

```text
saturation collapse
irreversibility ambiguity
observer instability
metric degeneracy
structural exhaustion
dependency boundaries
phase-like structural zones
```

---

## Repository Structure

Current important directories:

```text
docs/              -> technical documentation and result reports
examples/          -> runnable validation scripts
results/           -> historical generated JSON result files
results_enveloped/ -> schema-normalized copies of legacy result files
data/              -> bounded datasets and source-output records
omnia_validation/  -> reusable Python package utilities
tests/             -> pytest suite
.github/workflows/ -> CI workflow
```

Typical experimental structure may include:

```text
docs/
examples/
benchmarks/
results/
results_enveloped/
negative_results/
reproducibility/
synthetic/
stress_tests/
cross_domain/
```

---

## Relationship To OMNIA

OMNIA provides the structural measurement layer.

OMNIA-VALIDATION pressure-tests that layer.

Simplified relationship:

```text
OMNIA
  -> measurement generation

OMNIA-VALIDATION
  -> measurement stress testing
```

The repositories are complementary.

They are not interchangeable.

OMNIA-VALIDATION does not replace OMNIA.

It tests whether OMNIA-related measurements remain stable, reproducible, falsifiable, and bounded under pressure.

---

## Relationship To OMNIA-CONSTANT

OMNIA-CONSTANT focuses specifically on Ω-region interpretation and falsification.

OMNIA-VALIDATION is broader.

It validates:

```text
measurements
thresholds
perturbation behavior
reproducibility
failure boundaries
adversarial stability
dependency behavior
structural phase zones
```

across the ecosystem.

---

## Current Status

Current status:

```text
experimental
falsification-oriented
pressure-driven
non-final
partially industrialized
installable package layer added
CI-enabled
maintenance guide added
clean execution guide added
validator authoring guide added
result schema added
package API documented
project status documented
schema validator added
validate-result CLI added
legacy result normalization added
legacy status mapping documented
```

Current status document:

```text
docs/PROJECT_STATUS.md
```

This status is intentional.

The repository should not be interpreted as:

```text
finalized science
universal proof
production certification
semantic authority
correctness oracle
```

The correct interpretation is:

```text
a growing validation layer for structural measurement behavior
```

---

## Why This Repository Exists

Without validation pressure:

```text
metrics drift into narrative
thresholds become arbitrary
frameworks become unfalsifiable
failures disappear from visibility
structural claims become too easy to overstate
```

OMNIA-VALIDATION exists to prevent this.

Its function is to make the measurement layer face controlled criticism.

---

## Final Position

OMNIA-VALIDATION is the pressure-testing layer of the OMNIA ecosystem.

Its role is not to defend the framework.

Its role is to expose:

```text
instability
ambiguity
failure
weak assumptions
false interpretations
reproducibility problems
dependency boundaries
structural collapse
```

under controlled structural validation.

Core principle:

```text
a framework becomes more trustworthy
when its failure boundaries become measurable
```

Final boundary:

```text
measurement != inference != decision
```

---

## Author: Brighindi Massimiliano

Contact: brighissimo@gmail.com