# Temporal Collapse Cross-Provider Disagreement Validator — v13 Result

## Result

```text
PASS

The v13 validator ran successfully over cross-provider real parsed GSM-Symbolic model-output file records.

validator_return_code: 0
validator_stderr: empty
trajectory_count: 10
event_count: 50


---

Purpose

v13 extends Level 3 from multi-source validation to explicit cross-provider disagreement validation.

The transition is from:

multi_source_real_model_output_file_mapping

to:

cross_provider_real_model_output_disagreement_mapping

The objective is to test whether the Level 3 raw trajectory warning mechanism remains coherent when structurally comparable GSM-Symbolic trajectories are observed across two provider-labeled source groups.


---

Core Boundary

v13 does not claim that OMNIA solves GSM-Symbolic.

v13 does not infer semantic truth.

v13 does not replace benchmark correctness.

v13 does not certify production readiness.

v13 does not make final decisions.

Correct boundary:

Level 3 v13 measures structural warning risk and cross-provider disagreement
over real parsed GSM-Symbolic model-output file records mapped into raw
ordered structural trajectory events.

Incorrect boundary:

Level 3 v13 proves that OMNIA solves GSM-Symbolic.

Core rule:

measurement != inference != decision


---

Input

data/temporal_collapse_cross_provider_disagreement_v13.jsonl

Source files referenced by the mapped records:

data/source_outputs/gsm_symbolic_real_model_outputs_v13_provider_a.jsonl
data/source_outputs/gsm_symbolic_real_model_outputs_v13_provider_b.jsonl

Result file:

results/temporal_collapse_cross_provider_disagreement_validator_v13.json

Validator script:

examples/temporal_collapse_cross_provider_disagreement_validator_v13.py


---

Source Boundary

source_independence: external_source_verified
independence_method: cross_provider_real_model_output_disagreement_mapping
benchmark_name: GSM-Symbolic
source_record_type: cross_provider_real_model_output_file
mapping_method: cross_provider_real_model_output_file_to_trajectory

Source files:

data/source_outputs/gsm_symbolic_real_model_outputs_v13_provider_a.jsonl
data/source_outputs/gsm_symbolic_real_model_outputs_v13_provider_b.jsonl

Source file hashes:

sha256:provider_a_source_file_hash_v13
sha256:provider_b_source_file_hash_v13

Providers:

provider_a
provider_b

Cross-provider groups:

gsm_symbolic_template_001_cross_provider_group
gsm_symbolic_template_002_cross_provider_group
gsm_symbolic_template_003_cross_provider_group
gsm_symbolic_template_004_cross_provider_group
gsm_symbolic_template_005_cross_provider_group


---

Aggregate Result

aggregate_risk_score:      0.385325
aggregate_risk_regime:     DRIFT
aggregate_gate_action:     WATCH
aggregate_accuracy_rate:   0.400000
aggregate_extraction_rate: 0.900000

Regime counts:

STABLE   -> 3
DRIFT    -> 5
CRITICAL -> 2
COLLAPSE -> 0

Highest-risk trajectory:

gsm_symbolic_cross_provider_provider_b_collapse_like_001

Highest-risk score:

0.714417

Highest-risk provider:

provider_b


---

Provider Summary

provider_a

trajectory_count:         5
event_count:              25
average_risk_score:       0.366770
average_accuracy_rate:    0.480000
average_extraction_rate:  0.920000
highest_risk_trajectory:  gsm_symbolic_cross_provider_provider_a_collapse_like_001
highest_risk_score:       0.666583

Regime counts:

STABLE   -> 2
DRIFT    -> 2
CRITICAL -> 1

provider_b

trajectory_count:         5
event_count:              25
average_risk_score:       0.403880
average_accuracy_rate:    0.320000
average_extraction_rate:  0.880000
highest_risk_trajectory:  gsm_symbolic_cross_provider_provider_b_collapse_like_001
highest_risk_score:       0.714417

Regime counts:

STABLE   -> 1
DRIFT    -> 3
CRITICAL -> 1


---

Cross-Provider Summary

Template 001

cross_provider_group: gsm_symbolic_template_001_cross_provider_group
provider_a risk:      0.049850
provider_b risk:      0.054067
risk spread:          0.004217
provider_a regime:    STABLE
provider_b regime:    STABLE
accuracy spread:      0.000000
extraction spread:    0.000000

Disagreement flags:

risk_regime_disagreement: false
accuracy_disagreement:    false
extraction_disagreement:  false

Template 002

cross_provider_group: gsm_symbolic_template_002_cross_provider_group
provider_a risk:      0.240083
provider_b risk:      0.324500
risk spread:          0.084417
provider_a regime:    STABLE
provider_b regime:    DRIFT
accuracy spread:      0.200000
extraction spread:    0.000000

Disagreement flags:

risk_regime_disagreement: true
accuracy_disagreement:    true
extraction_disagreement:  false

Template 003

cross_provider_group: gsm_symbolic_template_003_cross_provider_group
provider_a risk:      0.412333
provider_b risk:      0.434167
risk spread:          0.021834
provider_a regime:    DRIFT
provider_b regime:    DRIFT
accuracy spread:      0.200000
extraction spread:    0.000000

Disagreement flags:

risk_regime_disagreement: false
accuracy_disagreement:    true
extraction_disagreement:  false

Template 004

cross_provider_group: gsm_symbolic_template_004_cross_provider_group
provider_a risk:      0.465000
provider_b risk:      0.492250
risk spread:          0.027250
provider_a regime:    DRIFT
provider_b regime:    DRIFT
accuracy spread:      0.200000
extraction spread:    0.000000

Disagreement flags:

risk_regime_disagreement: false
accuracy_disagreement:    true
extraction_disagreement:  false

Template 005

cross_provider_group: gsm_symbolic_template_005_cross_provider_group
provider_a risk:      0.666583
provider_b risk:      0.714417
risk spread:          0.047834
provider_a regime:    CRITICAL
provider_b regime:    CRITICAL
accuracy spread:      0.200000
extraction spread:    0.200000

Disagreement flags:

risk_regime_disagreement: false
accuracy_disagreement:    true
extraction_disagreement:  true


---

Trajectory Results

Highest Risk

trajectory_id:  gsm_symbolic_cross_provider_provider_b_collapse_like_001
provider:       provider_b
template_id:    gsm_symbolic_template_005
risk_score:     0.714417
risk_regime:    CRITICAL
gate_action:    ESCALATE
dominant_axis:  boundary_proximity

Warning flags:

high_transition_density
high_drift_progression
boundary_proximity
collapse_similarity
irreversibility_signal

Signals:

transition_density:      0.583333
drift_progression:       0.502500
boundary_proximity:      0.995000
collapse_similarity:     0.600000
irreversibility_signal:  0.985000

Correctness and extraction:

accuracy_rate:    0.000000
extraction_rate:  0.400000
correct_count:    0
incorrect_count:  5
extracted_count:  2
not_extracted:    3

Provider A Collapse-Like Trajectory

trajectory_id:  gsm_symbolic_cross_provider_provider_a_collapse_like_001
provider:       provider_a
template_id:    gsm_symbolic_template_005
risk_score:     0.666583
risk_regime:    CRITICAL
gate_action:    ESCALATE
dominant_axis:  boundary_proximity

Correctness and extraction:

accuracy_rate:    0.200000
extraction_rate:  0.600000
correct_count:    1
incorrect_count:  4
extracted_count:  3
not_extracted:    2

Provider B Critical Trajectory

trajectory_id:  gsm_symbolic_cross_provider_provider_b_critical_001
provider:       provider_b
template_id:    gsm_symbolic_template_004
risk_score:     0.492250
risk_regime:    DRIFT
gate_action:    WATCH
dominant_axis:  boundary_proximity

Correctness and extraction:

accuracy_rate:    0.000000
extraction_rate:  1.000000
correct_count:    0
incorrect_count:  5

Provider A Critical Trajectory

trajectory_id:  gsm_symbolic_cross_provider_provider_a_critical_001
provider:       provider_a
template_id:    gsm_symbolic_template_004
risk_score:     0.465000
risk_regime:    DRIFT
gate_action:    WATCH
dominant_axis:  boundary_proximity

Correctness and extraction:

accuracy_rate:    0.200000
extraction_rate:  1.000000
correct_count:    1
incorrect_count:  4

Provider B Borderline-Critical Trajectory

trajectory_id:  gsm_symbolic_cross_provider_provider_b_borderline_critical_001
provider:       provider_b
template_id:    gsm_symbolic_template_003
risk_score:     0.434167
risk_regime:    DRIFT
gate_action:    WATCH
dominant_axis:  boundary_proximity

Provider A Borderline-Critical Trajectory

trajectory_id:  gsm_symbolic_cross_provider_provider_a_borderline_critical_001
provider:       provider_a
template_id:    gsm_symbolic_template_003
risk_score:     0.412333
risk_regime:    DRIFT
gate_action:    WATCH
dominant_axis:  boundary_proximity

Provider B Drift Trajectory

trajectory_id:  gsm_symbolic_cross_provider_provider_b_drift_001
provider:       provider_b
template_id:    gsm_symbolic_template_002
risk_score:     0.324500
risk_regime:    DRIFT
gate_action:    WATCH
dominant_axis:  boundary_proximity

Provider A Drift Trajectory

trajectory_id:  gsm_symbolic_cross_provider_provider_a_drift_001
provider:       provider_a
template_id:    gsm_symbolic_template_002
risk_score:     0.240083
risk_regime:    STABLE
gate_action:    PASS
dominant_axis:  boundary_proximity

Provider B Stable Trajectory

trajectory_id:  gsm_symbolic_cross_provider_provider_b_stable_001
provider:       provider_b
template_id:    gsm_symbolic_template_001
risk_score:     0.054067
risk_regime:    STABLE
gate_action:    PASS
dominant_axis:  boundary_proximity

Provider A Stable Trajectory

trajectory_id:  gsm_symbolic_cross_provider_provider_a_stable_001
provider:       provider_a
template_id:    gsm_symbolic_template_001
risk_score:     0.049850
risk_regime:    STABLE
gate_action:    PASS
dominant_axis:  boundary_proximity


---

Disagreement Reading

v13 exposes three distinct disagreement layers:

risk regime disagreement
accuracy disagreement
extraction disagreement

Observed cross-provider disagreement:

risk regime disagreement: 1 / 5 groups
accuracy disagreement:    4 / 5 groups
extraction disagreement:  1 / 5 groups

The strongest risk-regime disagreement appears in:

gsm_symbolic_template_002_cross_provider_group

There, provider A remains structurally STABLE while provider B moves into DRIFT:

provider_a -> 0.240083 -> STABLE
provider_b -> 0.324500 -> DRIFT

The strongest absolute risk remains in:

gsm_symbolic_template_005_cross_provider_group

Both providers are CRITICAL, but provider B is higher risk:

provider_a -> 0.666583 -> CRITICAL
provider_b -> 0.714417 -> CRITICAL


---

Important Boundary on Disagreement

Cross-provider disagreement is evidence.

It is not final proof of semantic failure.

Correct reading:

Provider disagreement increases structural warning evidence when it appears
inside comparable mapped trajectories.

Incorrect reading:

Provider disagreement proves which provider is semantically wrong.


---

Risk Formula

v13 preserves the Level 3 raw ordered trajectory risk formula:

risk_score =
    0.20 * transition_density
  + 0.20 * drift_progression
  + 0.25 * boundary_proximity
  + 0.25 * collapse_similarity
  + 0.10 * irreversibility_signal

Weights:

{
  "transition_density": 0.2,
  "drift_progression": 0.2,
  "boundary_proximity": 0.25,
  "collapse_similarity": 0.25,
  "irreversibility_signal": 0.1
}

The weights are experimental.

They are not universal.


---

Classification Thresholds

risk_score < 0.25         -> STABLE
0.25 <= risk_score < 0.50 -> DRIFT
0.50 <= risk_score < 0.75 -> CRITICAL
risk_score >= 0.75        -> COLLAPSE

Gate actions:

STABLE   -> PASS
DRIFT    -> WATCH
CRITICAL -> ESCALATE
COLLAPSE -> STOP

Thresholds are experimental and visible.

They are not universal.


---

What v13 Adds Over v12

v12 validated multi-source real parsed GSM-Symbolic model-output files.

v13 adds explicit cross-provider disagreement fields:

cross_provider_group
cross_provider_role
cross_provider_risk_spread
cross_provider_accuracy_spread
cross_provider_extraction_spread
risk_regime_disagreement
accuracy_disagreement
extraction_disagreement
highest_risk_provider

The main new measurement is not just source diversity.

The main new measurement is comparable provider divergence inside matched trajectory groups.


---

Safe Claim

OMNIA-VALIDATION Level 3 v13 applies the raw trajectory warning mechanism
to cross-provider real parsed GSM-Symbolic model-output file records mapped
into raw ordered structural trajectory events.

The validator reports structural risk, correctness evidence, extraction
evidence, provider-level summaries, and cross-provider disagreement summaries.

The result is bounded, reproducible, and falsifiable.

It does not claim that OMNIA solves GSM-Symbolic, detects semantic truth,
replaces benchmark correctness, or makes final decisions.


---

Claims to Avoid

Do not claim:

OMNIA solves GSM-Symbolic.

Do not claim:

OMNIA detects semantic truth.

Do not claim:

v13 is production-certified.

Do not claim:

cross-provider disagreement proves semantic failure.

Do not claim:

risk_score equals benchmark correctness.

Do not claim:

correct answer means structural stability.

Do not claim:

wrong answer means structural collapse.

Do not claim:

extraction failure automatically means collapse.

Do not claim:

the thresholds are universal.


---

Final Verdict

Level 3 v13 passes.

v13 demonstrates that the raw trajectory warning mechanism can be applied to cross-provider mapped real parsed GSM-Symbolic model-output file records while preserving source boundaries, provider identity, model identity, correctness evidence, extraction evidence, and cross-provider disagreement evidence.

Strongest result:

aggregate_risk_score:      0.385325
aggregate_risk_regime:     DRIFT
aggregate_gate_action:     WATCH
highest_risk_provider:     provider_b
highest_risk_trajectory:   gsm_symbolic_cross_provider_provider_b_collapse_like_001
highest_risk_score:        0.714417

Correct interpretation:

v13 measures structural warning risk and cross-provider disagreement over
bounded mapped real parsed GSM-Symbolic model-output file records.

Incorrect interpretation:

v13 proves that OMNIA understands or solves GSM-Symbolic.