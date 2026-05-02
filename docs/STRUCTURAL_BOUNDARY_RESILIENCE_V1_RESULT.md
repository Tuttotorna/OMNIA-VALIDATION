# Structural Boundary Resilience v1 — Result

## Status

```text
Status: FAIL
Claim level: Level 1 — Boundary Resilience


---

Purpose

This experiment tested whether a lightweight resilience layer could improve projection-boundary behavior on the OMNIA-native structural benchmark dataset.

The layer was applied after canonical projection.

Its goal was not to change the benchmark.

Its goal was to test whether a simple adjustment layer could reduce boundary failures.

Core boundary:

measurement != inference != decision


---

Dataset

Dataset file:

data/structural_benchmark_dataset_v0.jsonl

Result file:

results/structural_boundary_resilience_v1.json

Total records:

32


---

Global Result

Record count:                   32
Success count:                  16
Success rate:                   0.5

Baseline boundary failures:     10
Resilient boundary failures:    9

Pass condition:

success_rate >= 0.65

Measured result:

success_rate = 0.5

Final classification:

FAIL


---

Pair-Type Results

STRUCTURAL_EQUIVALENT

count=6
success_rate=1.0
avg_baseline_distance=0.0
avg_resilient_distance=0.0

Equivalent structures remained stable.

The resilience layer did not damage clean equivalence cases.

Result:

PASS


---

STRUCTURAL_NEAR_EQUIVALENT

count=6
success_rate=1.0
avg_baseline_distance=0.046651785714
avg_resilient_distance=0.039654017857

Near-equivalent structures remained stable.

The resilience layer slightly reduced already-small distances.

Result:

PASS


---

STRUCTURAL_DIFFERENT

count=6
success_rate=0.5
avg_baseline_distance=0.550471230158
avg_resilient_distance=0.461962632275

This is the main negative finding.

The resilience layer reduced distances too aggressively.

Some genuinely different structures were pulled from split into partial.

Failed cases:

diff_004_triple_cycle_vs_mirror_sequence
diff_005_nested_blocks_vs_mirror_sequence
diff_006_run_length_gradient_vs_binary_alternation

Interpretation:

the layer weakened separation between structurally different families.

Result:

FAIL


---

FALSE_MERGE_TRAP

count=4
success_rate=0.0
avg_baseline_distance=0.0
avg_resilient_distance=0.0

False-merge traps remained unresolved.

These cases were already collapsed at projection level.

Because both sides project to the same structure, the resilience layer has no structural signal to recover from.

Failed cases:

fm_001_temperature_vs_finance
fm_002_periodicity_spoofing
fm_003_json_field_erasure
fm_004_low_high_vs_zero_extreme

Interpretation:

false-merge traps remain hard boundaries for this layer.

Result:

FAIL


---

FALSE_SPLIT_TRAP

count=4
success_rate=0.0
avg_baseline_distance=0.7265625
avg_resilient_distance=0.6294921875

The resilience layer reduced distances in some false-split cases, but not enough to restore correct merge behavior.

Failed cases:

fs_001_alias_inflation_binary
fs_002_cardinality_inflation_cycle
fs_003_separator_attack
fs_004_nested_alias_split

Interpretation:

the layer partially reduced split severity, but failed operationally.

Result:

FAIL


---

PARTIAL_DRIFT

count=6
success_rate=0.166666666667
avg_baseline_distance=0.17328042328
avg_resilient_distance=0.119222470238

Partial drift behavior remained weak.

Most partial-drift cases were pulled down into merge.

Only one case remained correctly classified as partial.

Correct case:

drift_006_mirror_sequence

Failed cases:

drift_001_binary_alternation
drift_002_four_cycle
drift_003_triple_cycle
drift_004_nested_blocks
drift_005_run_length_gradient

Interpretation:

the layer over-compressed mild degradation.

Result:

FAIL


---

Main Negative Finding

The resilience layer was intended to reduce boundary failures.

Instead, it introduced a structural side effect:

it reduced distances too broadly

This helped slightly in some false-split and near-equivalent cases, but damaged separation on genuinely different structures.

The most important failure is:

STRUCTURAL_DIFFERENT success_rate = 0.5

A resilience layer that weakens true structural separation is not acceptable.


---

Boundary Interpretation

The experiment separates three classes of behavior.

Stable Region

STRUCTURAL_EQUIVALENT
STRUCTURAL_NEAR_EQUIVALENT

These remained stable.

Hard Boundary Region

FALSE_MERGE_TRAP

These remained unsolved because projection erased the distinction completely.

Over-Compression Region

STRUCTURAL_DIFFERENT
PARTIAL_DRIFT
FALSE_SPLIT_TRAP

These exposed the weakness of the resilience layer.

The layer compressed distances without enough structural discrimination.


---

Why This FAIL Matters

This is a useful negative result.

It shows that:

resilience cannot mean lowering distance everywhere

A valid resilience layer must preserve:

same-structure closeness

while also preserving:

different-structure separation

The v1 layer failed that second requirement.


---

Main Insight

A naive boundary-resilience layer can improve apparent stability while damaging structural separation.

Therefore:

mitigation must be boundary-aware,
not globally distance-reducing.


---

Operational Conclusion

Structural Boundary Resilience v1 is not a valid mitigation layer.

It should be treated as:

negative control / failed mitigation

not as an improvement.

The correct next step is not to tune the pass threshold.

The correct next step is to build a new layer that separates:

compressible false-split noise

from:

true structural difference


---

Requirements for v2

A better version should include:

explicit hard-boundary detection

no global distance compression

preservation of STRUCTURAL_DIFFERENT separation

targeted alias-collapse logic

separate treatment of partial drift

no attempt to solve semantic false merges structurally


The key rule for v2:

never reduce distance unless there is evidence of representation-level aliasing


---

Limitations

This is not the full OMNIA engine.

This is a toy resilience layer.

Thresholds are manually chosen.

False-merge traps remain unresolved.

No semantic truth is evaluated.

No universal robustness claim is made.


---

Reproduction

python examples/structural_boundary_resilience_v1.py


---

Final Result

FAIL — structural boundary resilience v1 did not satisfy pass condition.

This is the correct result.

The experiment exposed that the v1 mitigation is too aggressive and structurally unsafe.