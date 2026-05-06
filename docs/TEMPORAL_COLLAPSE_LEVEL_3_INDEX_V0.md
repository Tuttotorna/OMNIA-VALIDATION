# Temporal Collapse Level 3 Index v0

## Purpose

This document indexes the Level 3 early-warning layer of OMNIA-VALIDATION.

Level 1 detected temporal-collapse signatures.

Level 2 mapped temporal-collapse topology, control-plane behavior, dependency boundaries, and phase regimes.

Level 3 introduces operational early-warning classification.

The purpose is to move from:

```text
after-the-fact collapse mapping
```

to:

```text
pre-collapse structural warning
```

---

## Core Boundary

Level 3 does not predict universal AI collapse.

Level 3 does not detect semantic truth.

Level 3 does not make final decisions.

Level 3 measures structural warning conditions only.

```text
measurement != inference != decision
```

---

## Level 3 Function

Given a trajectory or trajectory-like sequence, Level 3 computes structural warning signals and classifies the trajectory into a risk regime.

Target regimes:

```text
STABLE
DRIFT
CRITICAL
COLLAPSE
```

Gate actions:

```text
STABLE   -> PASS
DRIFT    -> WATCH
CRITICAL -> ESCALATE
COLLAPSE -> STOP
```

The gate action is not a final decision.

It is a measurement-derived warning signal for an external decision layer.

---

## Level 3 Progression

Level 3 currently has nine validation steps:

```text
Level 3 v0
  -> synthetic reference trajectories

Level 3 v1
  -> Level 2-derived result snapshots

Level 3 v2
  -> ordered Level 2 stage trajectory

Level 3 v3
  -> raw ordered reference trajectories

Level 3 v4
  -> external-style raw trajectory validation

Level 3 v5
  -> separate-generator raw trajectory validation

Level 3 v6
  -> declared external-source raw trajectory validation

Level 3 v7
  -> verified external-source raw trajectory validation

Level 3 v8
  -> direct public benchmark record mapping
```

This progression moves from:

```text
synthetic warning
```

to:

```text
snapshot-derived warning
```

to:

```text
ordered stage-trajectory warning
```

to:

```text
raw trajectory warning
```

to:

```text
external-style raw trajectory validation
```

to:

```text
separate-generator raw trajectory validation
```

to:

```text
declared external-source raw trajectory validation
```

to:

```text
verified external-source raw trajectory validation
```

to:

```text
direct public benchmark record mapping
```

The current strongest internal raw result is v3.

The current strongest external-style result is v4.

The current strongest separate-generator result is v5.

The current strongest declared external-source result is v6.

The current strongest verified external-source result is v7.

The current strongest direct public benchmark mapping result is v8.

v8 is stronger than v7 because it adds direct benchmark-record fields.

v8 does not claim that OMNIA solves GSM-Symbolic.

v8 measures structural warning risk over direct GSM-Symbolic public benchmark record mappings.

---

## Canonical Level 3 Files

### Concept document

```text
docs/TEMPORAL_COLLAPSE_EARLY_WARNING_LEVEL_3_V0.md
```

Defines the Level 3 purpose, risk regimes, warning principles, formula, thresholds, and boundaries.

---

## Level 3 v0 Files

### Level 3 v0 prototype script

```text
examples/temporal_collapse_early_warning_level_3_v0.py
```

Implements the minimal Level 3 early-warning prototype.

The script computes:

```text
transition_density
drift_score
boundary_proximity
collapse_similarity
irreversibility_signal
risk_score
risk_regime
gate_action
```

### Level 3 v0 result JSON

```text
results/temporal_collapse_early_warning_level_3_v0.json
```

Stores the reproducible output of the Level 3 v0 prototype.

### Level 3 v0 result document

```text
docs/TEMPORAL_COLLAPSE_EARLY_WARNING_LEVEL_3_V0_RESULT.md
```

Documents the Level 3 v0 result, interpretation, tested boundary, ordered risk progression, and safe claim.

---

## Level 3 v0 Result Status

Current status:

```text
PASS
```

The v0 prototype executed successfully.

The script produced the expected ordered risk progression:

```text
stable_reference_001    -> 0.038
drift_reference_001     -> 0.283
critical_reference_001  -> 0.565
collapse_reference_001  -> 0.8685
```

This progression correctly separates:

```text
STABLE
DRIFT
CRITICAL
COLLAPSE
```

inside the bounded synthetic v0 setup.

Correct interpretation:

```text
Level 3 v0 validates the minimal early-warning mechanism
on synthetic reference trajectories only.
```

---

## Level 3 v1 Files

### Level 2-derived bridge script

```text
examples/temporal_collapse_early_warning_from_level_2_v1.py
```

Applies the Level 3 early-warning layer to trajectory-like snapshots derived from existing Level 2 temporal-collapse result files.

This script reads:

```text
results/temporal_collapse_topology_cluster_adjacency_graph_v0.json
results/temporal_collapse_topology_cluster_graph_centrality_v0.json
results/temporal_collapse_topology_cluster_graph_control_plane_v0.json
results/temporal_collapse_topology_control_plane_robustness_v0.json
results/temporal_collapse_topology_dependency_map_v0.json
results/temporal_collapse_topology_dependency_boundary_v0.json
results/temporal_collapse_topology_boundary_phase_diagram_v0.json
```

Then emits:

```text
results/temporal_collapse_early_warning_from_level_2_v1.json
```

### Level 3 v1 result JSON

```text
results/temporal_collapse_early_warning_from_level_2_v1.json
```

Stores the reproducible output of the Level 3 v1 bridge.

### Level 3 v1 result document

```text
docs/TEMPORAL_COLLAPSE_EARLY_WARNING_FROM_LEVEL_2_V1_RESULT.md
```

Documents the Level 3 v1 bridge result.

---

## Level 3 v1 Result Status

Current status:

```text
PASS
```

Aggregate result:

```text
aggregate_risk_score:  0.300373
aggregate_risk_regime: DRIFT
aggregate_gate_action: WATCH
```

Regime counts:

```text
STABLE   -> 4
DRIFT    -> 2
CRITICAL -> 1
COLLAPSE -> 0
```

Strongest local warning:

```text
dependency_boundary_v0 -> CRITICAL -> ESCALATE
```

Correct interpretation:

```text
Level 3 v1 did not detect global collapse.

It detected aggregate structural drift inside the Level 2-derived chain,
with a critical local warning at the dependency-boundary layer.
```

Important limitation:

```text
Level 3 v1 is a heuristic bridge.

It converts Level 2 result files into trajectory-like risk snapshots.

It is not yet a direct trajectory-native validator.
```

---

## Level 3 v2 Files

### Ordered trajectory validator script

```text
examples/temporal_collapse_trajectory_native_validator_v2.py
```

Builds an ordered Level 2 stage trajectory and evaluates Level 3 warning risk across the chain.

The script moves from:

```text
file -> snapshot -> risk
```

to:

```text
ordered chain -> trajectory -> risk
```

It reads the ordered stage chain:

```text
1 -> cluster_adjacency_graph
2 -> cluster_graph_centrality
3 -> cluster_graph_control_plane
4 -> control_plane_robustness
5 -> dependency_map
6 -> dependency_boundary
7 -> boundary_phase_diagram
```

Then emits:

```text
results/temporal_collapse_trajectory_native_validator_v2.json
```

### Level 3 v2 result JSON

```text
results/temporal_collapse_trajectory_native_validator_v2.json
```

Stores the reproducible output of the Level 3 v2 trajectory-native validator.

### Level 3 v2 result document

```text
docs/TEMPORAL_COLLAPSE_TRAJECTORY_NATIVE_VALIDATOR_V2_RESULT.md
```

Documents the ordered trajectory result, structural sequence, dominant warning axis, tested boundary, and safe claim.

---

## Level 3 v2 Result Status

Current status:

```text
PASS
```

Current v2 result:

```text
risk_regime:    DRIFT
risk_score:     0.35722
gate_action:    WATCH
dominant_axis:  boundary_proximity
warning_flags:
  - boundary_proximity
```

Observed ordered status-signature trajectory:

```text
PASS_DOMINANT
PASS_DOMINANT
PASS_DOMINANT
CHECK_PRESSURE
CHECK_PRESSURE
CHECK_PRESSURE
PASS_DOMINANT
```

Compact form:

```text
PASS -> PASS -> PASS -> CHECK -> CHECK -> CHECK -> PASS
```

Strongest local pressure:

```text
dependency_boundary
  check_ratio:      0.625
  boundary_signal:  0.7375
  collapse_signal:  0.1875
```

Correct interpretation:

```text
Level 3 v2 did not detect terminal collapse.

It detected ordered trajectory drift,
driven mainly by boundary proximity.

The strongest local pressure appears at the dependency-boundary stage.
```

Important limitation:

```text
Level 3 v2 is trajectory-native relative to the ordered Level 2 stage chain.

It is not yet raw runtime trajectory validation.
```

---

## Level 3 v3 Files

### Raw trajectory concept document

```text
docs/TEMPORAL_COLLAPSE_RAW_TRAJECTORY_VALIDATOR_V3.md
```

Defines the v3 raw ordered trajectory validator.

It specifies:

```text
raw trajectory schema
required event fields
warning signals
risk formula
classification thresholds
gate actions
transition evidence
aggregate output
safe claims
limitations
```

### Raw trajectory input JSONL

```text
data/temporal_collapse_raw_trajectories_v3.jsonl
```

Stores the bounded raw ordered trajectory records used by v3.

The dataset contains four reference trajectories:

```text
raw_stable_001
raw_drift_001
raw_critical_001
raw_collapse_like_001
```

Each event contains:

```text
trajectory_id
step
signature
cluster
delta
iri
boundary_distance
phase
```

### Raw trajectory validator script

```text
examples/temporal_collapse_raw_trajectory_validator_v3.py
```

Reads raw ordered trajectory events directly from JSONL.

The script groups events by `trajectory_id`, sorts them by `step`, computes visible warning signals, classifies risk regimes, emits gate actions, and preserves transition evidence.

It moves from:

```text
stage-summary trajectory warning
```

to:

```text
raw trajectory warning
```

### Level 3 v3 result JSON

```text
results/temporal_collapse_raw_trajectory_validator_v3.json
```

Stores the reproducible output of the Level 3 v3 raw trajectory validator.

### Level 3 v3 result document

```text
docs/TEMPORAL_COLLAPSE_RAW_TRAJECTORY_VALIDATOR_V3_RESULT.md
```

Documents the v3 result, ordered risk progression, per-trajectory evidence, aggregate result, safe claim, and limitations.

---

## Level 3 v3 Result Status

Current status:

```text
PASS
```

The v3 validator executed successfully.

The validator separated all four bounded reference trajectories into the expected regimes:

```text
raw_stable_001         -> STABLE    -> 0.033417 -> PASS
raw_drift_001          -> DRIFT     -> 0.277833 -> WATCH
raw_critical_001       -> CRITICAL  -> 0.568722 -> ESCALATE
raw_collapse_like_001  -> COLLAPSE  -> 0.817056 -> STOP
```

Risk score progression:

```text
0.033417 -> 0.277833 -> 0.568722 -> 0.817056
```

Aggregate result:

```text
aggregate_risk_score:  0.424257
aggregate_risk_regime: DRIFT
aggregate_gate_action: WATCH
```

Regime counts:

```text
STABLE   -> 1
DRIFT    -> 1
CRITICAL -> 1
COLLAPSE -> 1
```

Highest-risk trajectory:

```text
raw_collapse_like_001 -> 0.817056
```

Correct interpretation:

```text
Level 3 v3 validates the raw ordered trajectory warning mechanism
on bounded reference trajectories.

It does not prove universal collapse prediction.

It shows that the warning layer can separate STABLE, DRIFT, CRITICAL,
and COLLAPSE regimes over raw ordered trajectory records.
```

---

## Level 3 v4 Files

### External raw trajectory concept document

```text
docs/TEMPORAL_COLLAPSE_EXTERNAL_RAW_TRAJECTORY_VALIDATOR_V4.md
```

Defines the v4 external-style raw trajectory validation direction.

It specifies:

```text
external raw trajectory schema
required source field
source independence tracking
warning signals
risk formula
classification thresholds
source summary
aggregate output
safe claims
limitations
```

### External-style raw trajectory input JSONL

```text
data/temporal_collapse_external_raw_trajectories_v4.jsonl
```

Stores the external-style raw ordered trajectory records used by v4.

The dataset contains five trajectories:

```text
external_stable_001
external_drift_001
external_borderline_critical_001
external_critical_001
external_collapse_like_001
```

Each event contains:

```text
trajectory_id
step
signature
cluster
delta
iri
boundary_distance
phase
source
source_independence
```

The current source is:

```text
external_style_generator_v4
```

The current source independence status is:

```text
not_verified
```

### External raw trajectory validator script

```text
examples/temporal_collapse_external_raw_trajectory_validator_v4.py
```

Applies the v3 raw trajectory warning mechanism to external-style raw ordered trajectory records.

The script groups events by `trajectory_id`, sorts by `step`, computes warning signals, emits gate actions, preserves transition evidence, and builds source summaries.

It moves from:

```text
raw reference trajectory warning
```

to:

```text
external-style raw trajectory validation
```

### Level 3 v4 result JSON

```text
results/temporal_collapse_external_raw_trajectory_validator_v4.json
```

Stores the reproducible output of the Level 3 v4 external-style raw trajectory validator.

### Level 3 v4 result document

```text
docs/TEMPORAL_COLLAPSE_EXTERNAL_RAW_TRAJECTORY_VALIDATOR_V4_RESULT.md
```

Documents the v4 result, source summary, ordered risk progression, aggregate result, per-trajectory evidence, safe claim, and source-independence limitation.

---

## Level 3 v4 Result Status

Current status:

```text
PASS
```

Source summary:

```text
source:              external_style_generator_v4
source_independence: not_verified
trajectory_count:    5
average_risk_score:  0.468439
```

Aggregate result:

```text
aggregate_risk_score:  0.468439
aggregate_risk_regime: DRIFT
aggregate_gate_action: WATCH
source_count:          1
```

Regime counts:

```text
STABLE   -> 1
DRIFT    -> 1
CRITICAL -> 2
COLLAPSE -> 1
```

Highest-risk trajectory:

```text
external_collapse_like_001 -> 0.824306
```

Observed risk progression:

```text
external_stable_001               -> STABLE    -> 0.040583 -> PASS
external_drift_001                -> DRIFT     -> 0.321306 -> WATCH
external_borderline_critical_001  -> CRITICAL  -> 0.536222 -> ESCALATE
external_critical_001             -> CRITICAL  -> 0.619778 -> ESCALATE
external_collapse_like_001        -> COLLAPSE  -> 0.824306 -> STOP
```

Correct interpretation:

```text
Level 3 v4 applied the v3 raw trajectory warning mechanism
to external-style raw ordered trajectory records.

The validator separated STABLE, DRIFT, CRITICAL, and COLLAPSE-like regimes,
while explicitly marking source independence as not verified.
```

Important limitation:

```text
Level 3 v4 is external-style validation.

It is not verified independent validation.

A source label alone does not prove independence.
```

---

## Level 3 v5 Files

### Separate generator script

```text
examples/generate_independent_raw_trajectories_v5.py
```

Generates raw ordered trajectory records through a separate generator script.

The generator emits:

```text
data/temporal_collapse_verified_independent_raw_trajectories_v5.jsonl
```

It preserves:

```text
source
source_independence
independence_method
```

The current source is:

```text
independent_generator_script_v5
```

The current source independence status is:

```text
generated_by_independent_script
```

The current independence method is:

```text
separate_generator_script
```

### Separate-generator raw trajectory input JSONL

```text
data/temporal_collapse_verified_independent_raw_trajectories_v5.jsonl
```

Stores the raw ordered trajectory records generated by the separate v5 generator.

The dataset contains five trajectories:

```text
independent_stable_001
independent_drift_001
independent_borderline_critical_001
independent_critical_001
independent_collapse_like_001
```

Each event contains:

```text
trajectory_id
step
signature
cluster
delta
iri
boundary_distance
phase
source
source_independence
independence_method
```

### Verified independent raw trajectory validator script

```text
examples/temporal_collapse_verified_independent_raw_trajectory_validator_v5.py
```

Applies the raw trajectory warning mechanism to records generated by the separate v5 generator script.

The script groups events by `trajectory_id`, sorts by `step`, computes warning signals, emits gate actions, preserves transition evidence, and builds source summaries.

It moves from:

```text
external-style validation
```

to:

```text
separate-generator validation
```

### Level 3 v5 result JSON

```text
results/temporal_collapse_verified_independent_raw_trajectory_validator_v5.json
```

Stores the reproducible output of the Level 3 v5 validator.

### Level 3 v5 result document

```text
docs/TEMPORAL_COLLAPSE_VERIFIED_INDEPENDENT_RAW_TRAJECTORY_VALIDATOR_V5_RESULT.md
```

Documents the v5 result, generator boundary, source summary, ordered risk progression, aggregate result, per-trajectory evidence, safe claim, and independence limitation.

---

## Level 3 v5 Result Status

Current status:

```text
PASS
```

The v5 generator executed successfully.

The v5 validator executed successfully.

No runtime error was produced.

Source summary:

```text
source:              independent_generator_script_v5
source_independence: generated_by_independent_script
independence_method: separate_generator_script
trajectory_count:    5
average_risk_score:  0.444451
```

Aggregate result:

```text
aggregate_risk_score:  0.444451
aggregate_risk_regime: DRIFT
aggregate_gate_action: WATCH
source_count:          1
```

Regime counts:

```text
STABLE   -> 1
DRIFT    -> 2
CRITICAL -> 1
COLLAPSE -> 1
```

Highest-risk trajectory:

```text
independent_collapse_like_001 -> 0.808922
```

Observed risk progression:

```text
independent_stable_001               -> STABLE   -> 0.037367 -> PASS
independent_drift_001                -> DRIFT    -> 0.285528 -> WATCH
independent_borderline_critical_001  -> DRIFT    -> 0.495100 -> WATCH
independent_critical_001             -> CRITICAL -> 0.595339 -> ESCALATE
independent_collapse_like_001        -> COLLAPSE -> 0.808922 -> STOP
```

Important borderline result:

```text
independent_borderline_critical_001 -> 0.495100
CRITICAL threshold                  -> 0.500000
```

Correct interpretation:

```text
Level 3 v5 applied the raw trajectory warning mechanism
to raw ordered trajectory records generated by a separate generator script.

The validator separated STABLE, DRIFT, CRITICAL, and COLLAPSE regimes,
with one borderline near-critical trajectory preserved below the CRITICAL threshold.
```

Important limitation:

```text
Level 3 v5 is stronger than v4.

It is not absolute external validation.

The source independence label means generated_by_independent_script,
not independently verified external source.
```

---

## Level 3 v6 Files

### External-source concept document

```text
docs/TEMPORAL_COLLAPSE_EXTERNAL_SOURCE_RAW_TRAJECTORY_VALIDATOR_V6.md
```

Defines the v6 declared external-source raw trajectory validation direction.

It specifies:

```text
external-source raw trajectory schema
source independence levels
required source field
required independence method
warning signals
risk formula
classification thresholds
source summary
aggregate output
safe claims
limitations
```

### Declared external-source raw trajectory input JSONL

```text
data/temporal_collapse_external_source_raw_trajectories_v6.jsonl
```

Stores the declared external-source raw ordered trajectory records used by v6.

The dataset contains five trajectories:

```text
external_source_stable_001
external_source_drift_001
external_source_borderline_critical_001
external_source_critical_001
external_source_collapse_like_001
```

Each event contains:

```text
trajectory_id
step
signature
cluster
delta
iri
boundary_distance
phase
source
source_independence
independence_method
```

The current source is:

```text
benchmark_prompt_perturbation_v6
```

The current source independence status is:

```text
external_source_declared
```

The current independence method is:

```text
prompt_perturbation_trace
```

This is not:

```text
external_source_verified
```

### External-source raw trajectory validator script

```text
examples/temporal_collapse_external_source_raw_trajectory_validator_v6.py
```

Applies the raw trajectory warning mechanism to declared external-source raw ordered trajectory records.

The script groups events by `trajectory_id`, sorts by `step`, computes warning signals, emits gate actions, preserves transition evidence, and builds source summaries.

It moves from:

```text
separate-generator validation
```

to:

```text
declared external-source validation
```

### Level 3 v6 result JSON

```text
results/temporal_collapse_external_source_raw_trajectory_validator_v6.json
```

Stores the reproducible output of the Level 3 v6 validator.

### Level 3 v6 result document

```text
docs/TEMPORAL_COLLAPSE_EXTERNAL_SOURCE_RAW_TRAJECTORY_VALIDATOR_V6_RESULT.md
```

Documents the v6 result, source boundary, source summary, ordered risk progression, aggregate result, per-trajectory evidence, safe claim, and external-source limitation.

---

## Level 3 v6 Result Status

Current status:

```text
PASS
```

The v6 validator executed successfully.

No runtime error was produced.

Source summary:

```text
source:              benchmark_prompt_perturbation_v6
source_independence: external_source_declared
independence_method: prompt_perturbation_trace
trajectory_count:    5
average_risk_score:  0.451667
```

Aggregate result:

```text
aggregate_risk_score:  0.451667
aggregate_risk_regime: DRIFT
aggregate_gate_action: WATCH
source_count:          1
```

Regime counts:

```text
STABLE   -> 1
DRIFT    -> 1
CRITICAL -> 2
COLLAPSE -> 1
```

Highest-risk trajectory:

```text
external_source_collapse_like_001 -> 0.813406
```

Observed risk progression:

```text
external_source_stable_001               -> STABLE   -> 0.040000 -> PASS
external_source_drift_001                -> DRIFT    -> 0.294956 -> WATCH
external_source_borderline_critical_001  -> CRITICAL -> 0.503233 -> ESCALATE
external_source_critical_001             -> CRITICAL -> 0.606739 -> ESCALATE
external_source_collapse_like_001        -> COLLAPSE -> 0.813406 -> STOP
```

Important borderline result:

```text
external_source_borderline_critical_001 -> 0.503233
CRITICAL threshold                      -> 0.500000
margin above threshold                  -> 0.003233
```

Correct interpretation:

```text
Level 3 v6 applied the raw trajectory warning mechanism
to declared external-source raw ordered trajectory records.

The validator separated STABLE, DRIFT, CRITICAL, and COLLAPSE regimes,
with the borderline trajectory crossing the CRITICAL threshold by a narrow margin.
```

Important limitation:

```text
Level 3 v6 is stronger than v5 as a declared source-boundary step.

It is not external_source_verified.

The source independence label means external_source_declared,
not absolute independent verification.
```

---

## Level 3 v7 Files

### Verified external-source concept document

```text
docs/TEMPORAL_COLLAPSE_VERIFIED_EXTERNAL_SOURCE_RAW_TRAJECTORY_VALIDATOR_V7.md
```

Defines the v7 verified external-source raw trajectory validation direction.

It specifies:

```text
verified external-source raw trajectory schema
required external source reference
required mapping notes
source independence levels
warning signals
risk formula
classification thresholds
source summary
aggregate output
safe claims
limitations
```

### Verified external-source raw trajectory input JSONL

```text
data/temporal_collapse_verified_external_source_raw_trajectories_v7.jsonl
```

Stores the GSM-Symbolic-derived verified external-source raw ordered trajectory records used by v7.

The dataset contains five trajectories:

```text
gsm_symbolic_stable_001
gsm_symbolic_drift_001
gsm_symbolic_borderline_critical_001
gsm_symbolic_critical_001
gsm_symbolic_collapse_like_001
```

Each event contains:

```text
trajectory_id
step
signature
cluster
delta
iri
boundary_distance
phase
source
source_independence
independence_method
external_source_reference
mapping_notes
```

The current source is:

```text
gsm_symbolic_public_benchmark_v7
```

The current source independence status is:

```text
external_source_verified
```

The current independence method is:

```text
public_benchmark_mapping
```

The current external source reference is:

```text
GSM-Symbolic public benchmark / Apple ml-gsm-symbolic repository
```

Important boundary:

```text
v7 does not claim that OMNIA solves GSM-Symbolic.

v7 uses GSM-Symbolic as a public/documentable benchmark boundary
for mapped raw structural trajectory records.
```

### Verified external-source raw trajectory validator script

```text
examples/temporal_collapse_verified_external_source_raw_trajectory_validator_v7.py
```

Applies the raw trajectory warning mechanism to verified external-source raw ordered trajectory records mapped from GSM-Symbolic.

The script groups events by `trajectory_id`, sorts by `step`, computes warning signals, emits gate actions, preserves transition evidence, and builds source summaries.

It moves from:

```text
declared external-source validation
```

to:

```text
verified external-source validation
```

### Level 3 v7 result JSON

```text
results/temporal_collapse_verified_external_source_raw_trajectory_validator_v7.json
```

Stores the reproducible output of the Level 3 v7 validator.

### Level 3 v7 result document

```text
docs/TEMPORAL_COLLAPSE_VERIFIED_EXTERNAL_SOURCE_RAW_TRAJECTORY_VALIDATOR_V7_RESULT.md
```

Documents the v7 result, public benchmark boundary, source summary, ordered risk progression, aggregate result, per-trajectory evidence, safe claim, and GSM-Symbolic limitation.

---

## Level 3 v7 Result Status

Current status:

```text
PASS
```

The v7 validator executed successfully.

No runtime error was produced.

Source summary:

```text
source:                    gsm_symbolic_public_benchmark_v7
source_independence:       external_source_verified
independence_method:       public_benchmark_mapping
external_source_reference: GSM-Symbolic public benchmark / Apple ml-gsm-symbolic repository
trajectory_count:          5
average_risk_score:        0.464700
```

Aggregate result:

```text
aggregate_risk_score:  0.464700
aggregate_risk_regime: DRIFT
aggregate_gate_action: WATCH
source_count:          1
```

Regime counts:

```text
STABLE   -> 1
DRIFT    -> 1
CRITICAL -> 2
COLLAPSE -> 1
```

Highest-risk trajectory:

```text
gsm_symbolic_collapse_like_001 -> 0.817794
```

Observed risk progression:

```text
gsm_symbolic_stable_001               -> STABLE   -> 0.106344 -> PASS
gsm_symbolic_drift_001                -> DRIFT    -> 0.306183 -> WATCH
gsm_symbolic_borderline_critical_001  -> CRITICAL -> 0.508467 -> ESCALATE
gsm_symbolic_critical_001             -> CRITICAL -> 0.584711 -> ESCALATE
gsm_symbolic_collapse_like_001        -> COLLAPSE -> 0.817794 -> STOP
```

Important borderline result:

```text
gsm_symbolic_borderline_critical_001 -> 0.508467
CRITICAL threshold                   -> 0.500000
margin above threshold               -> 0.008467
```

Correct interpretation:

```text
Level 3 v7 applied the raw trajectory warning mechanism
to GSM-Symbolic-derived verified external-source raw ordered trajectory records.

The validator separated STABLE, DRIFT, CRITICAL, and COLLAPSE regimes,
with the borderline trajectory crossing the CRITICAL threshold by a narrow margin.
```

Important limitation:

```text
Level 3 v7 is stronger than v6 because it uses a public/documentable benchmark boundary.

It does not claim that OMNIA solves GSM-Symbolic.

It does not directly evaluate official GSM-Symbolic model answers.

It maps GSM-Symbolic-derived structural trajectory records into the Level 3 raw warning mechanism.
```

---

## Level 3 v8 Files

### Direct GSM-Symbolic record concept document

```text
docs/TEMPORAL_COLLAPSE_DIRECT_GSM_SYMBOLIC_RECORD_VALIDATOR_V8.md
```

Defines the v8 direct public benchmark record mapping direction.

It specifies:

```text
direct GSM-Symbolic record schema
required template id
required question id
required variant type
required benchmark name
required source record type
required source record reference
required mapping method
warning signals
risk formula
classification thresholds
source summary
aggregate output
safe claims
limitations
```

### Direct GSM-Symbolic record input JSONL

```text
data/temporal_collapse_direct_gsm_symbolic_records_v8.jsonl
```

Stores the direct GSM-Symbolic public benchmark record mappings used by v8.

The dataset contains five trajectories:

```text
gsm_symbolic_direct_stable_001
gsm_symbolic_direct_drift_001
gsm_symbolic_direct_borderline_critical_001
gsm_symbolic_direct_critical_001
gsm_symbolic_direct_collapse_like_001
```

Each event contains:

```text
trajectory_id
step
template_id
question_id
variant_type
signature
cluster
delta
iri
boundary_distance
phase
source
source_independence
independence_method
external_source_reference
benchmark_name
source_record_type
source_record_reference
mapping_method
mapping_notes
```

The current source is:

```text
gsm_symbolic_public_benchmark_v8
```

The current source independence status is:

```text
external_source_verified
```

The current independence method is:

```text
direct_public_benchmark_record_mapping
```

The current benchmark name is:

```text
GSM-Symbolic
```

The current source record type is:

```text
template_variant
```

The current mapping method is:

```text
template_variant_to_trajectory
```

Important boundary:

```text
v8 does not claim that OMNIA solves GSM-Symbolic.

v8 does not evaluate semantic correctness.

v8 measures structural warning risk over direct GSM-Symbolic public benchmark
record mappings.
```

### Direct GSM-Symbolic record validator script

```text
examples/temporal_collapse_direct_gsm_symbolic_record_validator_v8.py
```

Applies the raw trajectory warning mechanism to direct GSM-Symbolic public benchmark records mapped into raw ordered structural trajectory events.

The script groups events by `trajectory_id`, sorts by `step`, computes warning signals, emits gate actions, preserves transition evidence, and builds source summaries.

It moves from:

```text
verified external-source mapped trajectory records
```

to:

```text
direct public benchmark record mapping
```

### Level 3 v8 result JSON

```text
results/temporal_collapse_direct_gsm_symbolic_record_validator_v8.json
```

Stores the reproducible output of the Level 3 v8 validator.

### Level 3 v8 result document

```text
docs/TEMPORAL_COLLAPSE_DIRECT_GSM_SYMBOLIC_RECORD_VALIDATOR_V8_RESULT.md
```

Documents the v8 result, direct benchmark-record boundary, source summary, ordered risk progression, aggregate result, per-trajectory evidence, safe claim, limitation, and technical note.

---

## Level 3 v8 Result Status

Current status:

```text
PASS
```

The v8 validator executed successfully.

No runtime error was produced.

Source summary:

```text
source:                    gsm_symbolic_public_benchmark_v8
source_independence:       external_source_verified
independence_method:       direct_public_benchmark_record_mapping
external_source_reference: GSM-Symbolic public benchmark / Apple ml-gsm-symbolic repository
benchmark_name:            GSM-Symbolic
source_record_type:        template_variant
mapping_method:            template_variant_to_trajectory
trajectory_count:          5
average_risk_score:        0.465463
```

Aggregate result:

```text
aggregate_risk_score:  0.465463
aggregate_risk_regime: DRIFT
aggregate_gate_action: WATCH
source_count:          1
```

Regime counts:

```text
STABLE   -> 1
DRIFT    -> 1
CRITICAL -> 2
COLLAPSE -> 1
```

Highest-risk trajectory:

```text
gsm_symbolic_direct_collapse_like_001 -> 0.820378
```

Observed risk progression:

```text
gsm_symbolic_direct_stable_001               -> STABLE   -> 0.104128 -> PASS
gsm_symbolic_direct_drift_001                -> DRIFT    -> 0.303100 -> WATCH
gsm_symbolic_direct_borderline_critical_001  -> CRITICAL -> 0.511733 -> ESCALATE
gsm_symbolic_direct_critical_001             -> CRITICAL -> 0.587978 -> ESCALATE
gsm_symbolic_direct_collapse_like_001        -> COLLAPSE -> 0.820378 -> STOP
```

Important borderline result:

```text
gsm_symbolic_direct_borderline_critical_001 -> 0.511733
CRITICAL threshold                          -> 0.500000
margin above threshold                      -> 0.011733
```

Correct interpretation:

```text
Level 3 v8 applied the raw trajectory warning mechanism
to direct GSM-Symbolic public benchmark records mapped into raw ordered
structural trajectory events.

The validator separated STABLE, DRIFT, CRITICAL, and COLLAPSE regimes,
with the borderline trajectory crossing the CRITICAL threshold by a narrow margin.
```

Important limitation:

```text
Level 3 v8 is stronger than v7 because it adds direct benchmark-record fields.

It does not claim that OMNIA solves GSM-Symbolic.

It does not evaluate semantic correctness.

It does not directly evaluate official GSM-Symbolic model answers.

It maps direct GSM-Symbolic public benchmark record fields into the Level 3 raw warning mechanism.
```

Technical note:

```text
The current v8 output contains the label multiple_mapping_notess.

This is a harmless formatting issue caused by pluralizing mapping_notes by appending s.

The intended clean label is multiple_mapping_notes.

The measurement result is not affected.
```

---

## Risk Formula v0/v1

Level 3 v0 and v1 use:

```text
risk_score =
    0.20 * transition_density
  + 0.20 * drift_score
  + 0.25 * boundary_proximity
  + 0.25 * collapse_similarity
  + 0.10 * irreversibility_signal
```

All weights are visible.

No hidden interpretation layer is used.

---

## Risk Formula v2

Level 3 v2 uses the trajectory-native stage-chain variant:

```text
risk_score =
    0.20 * transition_density
  + 0.20 * drift_progression
  + 0.25 * boundary_proximity
  + 0.25 * collapse_similarity
  + 0.10 * irreversibility_proxy
```

The v2 formula preserves the same structural intent while replacing snapshot signals with ordered-stage signals.

---

## Risk Formula v3/v4/v5/v6/v7/v8

Level 3 v3, v4, v5, v6, v7, and v8 use the raw ordered trajectory variant:

```text
risk_score =
    0.20 * transition_density
  + 0.20 * drift_progression
  + 0.25 * boundary_proximity
  + 0.25 * collapse_similarity
  + 0.10 * irreversibility_signal
```

The v3/v4/v5/v6/v7/v8 formula measures directly over raw ordered trajectory events.

It uses:

```text
signature transitions
cluster transitions
phase transitions
delta progression
iri progression
boundary distance
collapse phase count
broken signature markers
```

v4 additionally tracks:

```text
source
source_independence
source_summary
```

v5 additionally tracks:

```text
source
source_independence
independence_method
source_summary
```

v6 additionally tracks:

```text
declared external-source boundary
source
source_independence
independence_method
source_summary
external_source_note
```

v7 additionally tracks:

```text
verified external-source boundary
source
source_independence
independence_method
external_source_reference
mapping_notes
source_summary
external_source_note
```

v8 additionally tracks:

```text
direct public benchmark record mapping
template_id
question_id
variant_type
benchmark_name
source_record_type
source_record_reference
mapping_method
mapping_notes
source_summary
external_source_note
```

---

## Classification Thresholds

Current thresholds:

```text
risk_score < 0.25         -> STABLE
0.25 <= risk_score < 0.50 -> DRIFT
0.50 <= risk_score < 0.75 -> CRITICAL
risk_score >= 0.75        -> COLLAPSE
```

These thresholds are experimental.

They are not universal.

They are valid only inside the tested construction unless expanded by later validation.

---

## Structural Path

The Level 3 chain depends on the Level 2 chain.

Logical dependency:

```text
temporal-collapse signatures
  -> cluster structure
  -> directed graph topology
  -> centrality behavior
  -> control-plane behavior
  -> robustness CHECK
  -> dependency map
  -> boundary map
  -> phase diagram
  -> early-warning classification
  -> raw trajectory warning
  -> external-style raw trajectory validation
  -> separate-generator raw trajectory validation
  -> declared external-source raw trajectory validation
  -> verified external-source raw trajectory validation
  -> direct public benchmark record mapping
```

The Level 3 warning layer exists because Level 2 mapped structural boundaries.

Without the Level 2 boundary map, Level 3 would only be arbitrary scoring.

With the Level 2 boundary map, Level 3 becomes bounded structural navigation.

With v3, the warning layer begins operating directly over raw ordered trajectory events.

With v4, the same mechanism is applied to external-style raw ordered trajectory records while tracking source independence.

With v5, the same mechanism is applied to raw ordered trajectory records generated by a separate generator script.

With v6, the same mechanism is applied to declared external-source raw ordered trajectory records.

With v7, the same mechanism is applied to GSM-Symbolic-derived verified external-source raw ordered trajectory records.

With v8, the same mechanism is applied to direct GSM-Symbolic public benchmark record mappings.

---

## Meaning of the CHECK Result

The Level 2 robustness CHECK remains central.

The CHECK result showed that the control plane was not universally invariant.

That instability was not hidden.

It became the reason to map dependency boundaries and phase regimes.

Level 3 inherits this principle:

```text
failure is boundary information
```

A warning system becomes stronger when it knows where the measurement becomes unstable.

---

## Structural Reading Across v0 to v8

### v0

```text
synthetic reference trajectories
  -> STABLE / DRIFT / CRITICAL / COLLAPSE separated correctly
```

v0 proves only that the minimal warning machine works on controlled synthetic examples.

### v1

```text
Level 2-derived snapshots
  -> aggregate DRIFT
  -> dependency_boundary CRITICAL
```

v1 shows that warning pressure appears in Level 2-derived result snapshots.

Its strongest local warning appears at the dependency-boundary layer.

### v2

```text
ordered Level 2 stage trajectory
  -> DRIFT
  -> WATCH
  -> boundary_proximity dominant
```

v2 shows that the ordered chain does not collapse globally.

It enters a drift regime driven by boundary proximity.

The structural sequence is:

```text
PASS -> PASS -> PASS -> CHECK -> CHECK -> CHECK -> PASS
```

This indicates a localized boundary-pressure zone, not terminal collapse.

### v3

```text
raw ordered reference trajectory records
  -> STABLE / DRIFT / CRITICAL / COLLAPSE separated correctly
```

v3 validates the raw trajectory warning mechanism on bounded reference trajectories.

The ordered risk progression is:

```text
0.033417 -> 0.277833 -> 0.568722 -> 0.817056
```

This is the strongest internal raw Level 3 result because the warning layer operates directly over raw ordered events.

### v4

```text
external-style raw trajectory records
  -> STABLE / DRIFT / CRITICAL / COLLAPSE-like regimes separated
```

v4 applies the v3 mechanism to external-style raw ordered trajectory records.

The observed risk progression is:

```text
0.040583 -> 0.321306 -> 0.536222 -> 0.619778 -> 0.824306
```

The decisive boundary condition is:

```text
source_independence: not_verified
```

Therefore v4 is not verified independent validation.

It is external-style validation with source independence explicitly tracked.

### v5

```text
separate-generator raw trajectory records
  -> STABLE / DRIFT / CRITICAL / COLLAPSE regimes separated
```

v5 applies the raw trajectory warning mechanism to records produced by a separate generator script.

The observed risk progression is:

```text
0.037367 -> 0.285528 -> 0.495100 -> 0.595339 -> 0.808922
```

The decisive boundary condition is:

```text
source_independence: generated_by_independent_script
independence_method: separate_generator_script
```

Therefore v5 is stronger than v4, but it is not absolute external validation.

### v6

```text
declared external-source raw trajectory records
  -> STABLE / DRIFT / CRITICAL / COLLAPSE regimes separated
```

v6 applies the raw trajectory warning mechanism to records under a declared external-source boundary.

The observed risk progression is:

```text
0.040000 -> 0.294956 -> 0.503233 -> 0.606739 -> 0.813406
```

The decisive boundary condition is:

```text
source_independence: external_source_declared
independence_method: prompt_perturbation_trace
```

Therefore v6 is stronger than v5 as a declared source-boundary step.

It is not `external_source_verified`.

### v7

```text
GSM-Symbolic-derived verified external-source raw trajectory records
  -> STABLE / DRIFT / CRITICAL / COLLAPSE regimes separated
```

v7 applies the raw trajectory warning mechanism to records mapped from a public/documentable benchmark boundary.

The observed risk progression is:

```text
0.106344 -> 0.306183 -> 0.508467 -> 0.584711 -> 0.817794
```

The decisive boundary condition is:

```text
source_independence: external_source_verified
independence_method: public_benchmark_mapping
external_source_reference: GSM-Symbolic public benchmark / Apple ml-gsm-symbolic repository
```

Therefore v7 is stronger than v6.

It does not claim that OMNIA solves GSM-Symbolic.

It maps GSM-Symbolic-derived structural trajectory records into the Level 3 raw warning mechanism.

### v8

```text
direct GSM-Symbolic public benchmark record mappings
  -> STABLE / DRIFT / CRITICAL / COLLAPSE regimes separated
```

v8 applies the raw trajectory warning mechanism to direct GSM-Symbolic public benchmark record fields mapped into raw ordered structural trajectory events.

The observed risk progression is:

```text
0.104128 -> 0.303100 -> 0.511733 -> 0.587978 -> 0.820378
```

The decisive boundary condition is:

```text
source_independence: external_source_verified
independence_method: direct_public_benchmark_record_mapping
benchmark_name: GSM-Symbolic
source_record_type: template_variant
mapping_method: template_variant_to_trajectory
```

Therefore v8 is stronger than v7 as a direct benchmark-record mapping step.

It does not claim that OMNIA solves GSM-Symbolic.

It does not evaluate semantic correctness.

It measures structural warning risk over direct GSM-Symbolic public benchmark record mappings.

---

## Current Structural Verdict

Safe verdict:

```text
Level 3 has moved from synthetic warning,
to snapshot-derived warning,
to ordered stage-trajectory warning,
to raw ordered trajectory warning,
to external-style raw trajectory validation,
to separate-generator raw trajectory validation,
to declared external-source raw trajectory validation,
to verified external-source raw trajectory validation,
to direct public benchmark record mapping.

The current strongest internal raw result is v3.

The current strongest external-style result is v4.

The current strongest separate-generator result is v5.

The current strongest declared external-source result is v6.

The current strongest verified external-source result is v7.

The current strongest direct public benchmark mapping result is v8.

Level 3 v8 separated STABLE, DRIFT, CRITICAL, and COLLAPSE regimes
over direct GSM-Symbolic public benchmark record mappings using visible signals,
explicit thresholds, source labels, independence method labels, benchmark fields,
source-record fields, mapping methods, and inspectable transition evidence.

v8 is stronger than v7 because it adds direct benchmark-record fields.

v8 does not claim that OMNIA solves GSM-Symbolic.

v8 does not evaluate semantic correctness.
```

This is bounded, reproducible, and falsifiable.

---

## Safe Claim

```text
OMNIA-VALIDATION Level 3 v0 introduced a bounded early-warning layer
for temporal-collapse trajectories.

Level 3 v1 applied that warning layer to Level 2-derived result snapshots.

Level 3 v2 evaluated the Level 2 temporal-collapse chain
as an ordered stage trajectory.

Level 3 v3 evaluated raw ordered reference trajectory records directly.

Level 3 v4 applied the same raw trajectory warning mechanism
to external-style raw ordered trajectory records.

Level 3 v5 applied the raw trajectory warning mechanism to records generated
by a separate generator script.

Level 3 v6 applied the raw trajectory warning mechanism to declared
external-source raw ordered trajectory records.

Level 3 v7 applied the raw trajectory warning mechanism to GSM-Symbolic-derived
verified external-source raw ordered trajectory records.

Level 3 v8 applied the raw trajectory warning mechanism to direct GSM-Symbolic
public benchmark records mapped into raw ordered structural trajectory events.

The v8 validator separated STABLE, DRIFT, CRITICAL, and COLLAPSE regimes,
with the borderline trajectory crossing the CRITICAL threshold by a narrow margin.
```

---

## Claims to Avoid

Do not claim:

```text
OMNIA predicts AI collapse universally.
```

Do not claim:

```text
OMNIA detects semantic truth.
```

Do not claim:

```text
Level 3 is production-certified.
```

Do not claim:

```text
The thresholds are universal.
```

Do not claim:

```text
Level 3 v4 is verified independent validation.
```

Do not claim:

```text
Level 3 v5 proves absolute external independence.
```

Do not claim:

```text
Level 3 v6 proves external_source_verified validation.
```

Do not claim:

```text
Level 3 v7 proves that OMNIA solves GSM-Symbolic.
```

Do not claim:

```text
Level 3 v8 proves that OMNIA solves GSM-Symbolic.
```

Do not claim:

```text
Level 3 v8 evaluates semantic correctness.
```

Do not claim:

```text
External-style, separate-generator, declared external-source, verified external-source,
or direct public benchmark mapping validation proves model cognition.
```

Correct boundary:

```text
Level 3 v0 measures structural warning conditions
inside a bounded synthetic validation setup.

Level 3 v1 measures structural warning pressure
over Level 2-derived result snapshots.

Level 3 v2 measures warning risk across an ordered Level 2 stage trajectory.

Level 3 v3 measures warning risk directly over bounded raw ordered
reference trajectory records.

Level 3 v4 measures warning risk over external-style raw ordered trajectory
records with source independence explicitly marked as not_verified.

Level 3 v5 measures warning risk over raw ordered trajectory records generated
by a separate generator script, with independence_method recorded as
separate_generator_script.

Level 3 v6 measures warning risk over declared external-source raw ordered
trajectory records, with source_independence recorded as external_source_declared
and independence_method recorded as prompt_perturbation_trace.

Level 3 v7 measures warning risk over GSM-Symbolic-derived verified external-source
raw ordered trajectory records, with source_independence recorded as
external_source_verified and independence_method recorded as public_benchmark_mapping.

Level 3 v8 measures warning risk over direct GSM-Symbolic public benchmark record
mappings, with source_independence recorded as external_source_verified and
independence_method recorded as direct_public_benchmark_record_mapping.
```

---

## Current Level 3 Status

```text
Level 3 v0
  -> synthetic early-warning prototype
  -> PASS

Level 3 v1
  -> Level 2-derived bridge
  -> PASS
  -> aggregate DRIFT
  -> strongest local warning: dependency_boundary_v0 CRITICAL

Level 3 v2
  -> ordered Level 2 stage trajectory
  -> PASS
  -> trajectory DRIFT
  -> WATCH
  -> dominant axis: boundary_proximity

Level 3 v3
  -> raw ordered reference trajectories
  -> PASS
  -> STABLE / DRIFT / CRITICAL / COLLAPSE separated
  -> highest risk: raw_collapse_like_001

Level 3 v4
  -> external-style raw trajectory validation
  -> PASS
  -> STABLE / DRIFT / CRITICAL / COLLAPSE-like regimes separated
  -> highest risk: external_collapse_like_001
  -> source independence: not_verified

Level 3 v5
  -> separate-generator raw trajectory validation
  -> PASS
  -> STABLE / DRIFT / CRITICAL / COLLAPSE regimes separated
  -> highest risk: independent_collapse_like_001
  -> source independence: generated_by_independent_script
  -> independence method: separate_generator_script

Level 3 v6
  -> declared external-source raw trajectory validation
  -> PASS
  -> STABLE / DRIFT / CRITICAL / COLLAPSE regimes separated
  -> highest risk: external_source_collapse_like_001
  -> source independence: external_source_declared
  -> independence method: prompt_perturbation_trace
  -> not external_source_verified

Level 3 v7
  -> verified external-source raw trajectory validation
  -> PASS
  -> STABLE / DRIFT / CRITICAL / COLLAPSE regimes separated
  -> highest risk: gsm_symbolic_collapse_like_001
  -> source independence: external_source_verified
  -> independence method: public_benchmark_mapping
  -> external source: GSM-Symbolic public benchmark / Apple ml-gsm-symbolic repository
  -> does not claim GSM-Symbolic solving

Level 3 v8
  -> direct public benchmark record mapping
  -> PASS
  -> STABLE / DRIFT / CRITICAL / COLLAPSE regimes separated
  -> highest risk: gsm_symbolic_direct_collapse_like_001
  -> source independence: external_source_verified
  -> independence method: direct_public_benchmark_record_mapping
  -> benchmark: GSM-Symbolic
  -> source record type: template_variant
  -> mapping method: template_variant_to_trajectory
  -> does not claim GSM-Symbolic solving
  -> does not evaluate semantic correctness
```

---

## Next Step

The next validation step is to move from direct template-variant benchmark mapping to actual model-output or answer-correctness trace mapping.

Target direction:

```text
Level 3 v0 synthetic reference
  -> Level 3 v1 Level-2-derived snapshots
  -> Level 3 v2 ordered Level 2 stage trajectory
  -> Level 3 v3 raw ordered reference trajectories
  -> Level 3 v4 external-style raw trajectory validation
  -> Level 3 v5 separate-generator raw trajectory validation
  -> Level 3 v6 declared external-source raw trajectory validation
  -> Level 3 v7 verified external-source raw trajectory validation
  -> Level 3 v8 direct public benchmark record mapping
  -> Level 3 v9 direct answer-trace / model-output mapping
```

The next script should test the raw trajectory warning mechanism against actual GSM-Symbolic model outputs, answer correctness traces, or benchmark files parsed directly from source.

Possible v9 source classes:

```text
actual GSM-Symbolic generated records
official GSM-Symbolic template variants parsed from source
model outputs over GSM-Symbolic variants
answer correctness traces over symbolic perturbations
public benchmark files transformed into raw trajectory records
```

It should preserve:

```text
time order
variant order
template id
question id
variant type
model name
run id
response id
expected answer
model final answer
is_correct
signature transitions
cluster transitions
delta progression
boundary crossings
irreversibility progression
phase-regime changes
raw trajectory events
source labels
source independence status
independence method
external-source documentation
mapping notes
```

Target file:

```text
examples/temporal_collapse_direct_gsm_symbolic_answer_trace_validator_v9.py
```

The v9 objective is to test whether the raw trajectory warning mechanism remains coherent when the records include answer traces or model outputs.

This is the move from:

```text
direct public benchmark record mapping
```

to:

```text
direct answer-trace / model-output mapping
```