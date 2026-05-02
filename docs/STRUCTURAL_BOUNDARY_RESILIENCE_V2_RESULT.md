# Structural Boundary Resilience v2 — Result

## Status

```text
Status: FAIL
Claim level: Level 1 — Boundary-Aware Resilience


---

Purpose

This experiment tested a selective alias-aware resilience layer.

Unlike v1, this version does not globally reduce distance.

The goal was:

apply compression only when alias evidence is detected

Core boundary:

measurement != inference != decision


---

Dataset

Dataset file:

data/structural_benchmark_dataset_v0.jsonl

Result file:

results/structural_boundary_resilience_v2.json

Total records:

32


---

Global Result

Record count:              32
Success count:             19
Success rate:              0.59375
Boundary failure count:    12

Pass condition:

success_rate >= 0.65
and STRUCTURAL_DIFFERENT success_rate >= 0.80

Measured result:

success_rate = 0.59375
STRUCTURAL_DIFFERENT success_rate = 0.833333333333

Final classification:

FAIL


---

Pair-Type Results

STRUCTURAL_EQUIVALENT

count=6
success_rate=1.0
avg_alias_evidence=0.3
avg_baseline_distance=0.0
avg_resilient_distance=0.0

Equivalent structures remained stable.

Result:

PASS


---

STRUCTURAL_NEAR_EQUIVALENT

count=6
success_rate=1.0
avg_alias_evidence=0.81448657381
avg_baseline_distance=0.046651785714
avg_resilient_distance=0.042528118298

Near-equivalent structures remained correctly merged.

The resilience layer slightly reduced already-small distances without damaging these cases.

Result:

PASS


---

STRUCTURAL_DIFFERENT

count=6
success_rate=0.833333333333
avg_alias_evidence=0.354166666667
avg_baseline_distance=0.550471230158
avg_resilient_distance=0.54439484127

This is the main improvement over v1.

v1 result:

STRUCTURAL_DIFFERENT success_rate = 0.5

v2 result:

STRUCTURAL_DIFFERENT success_rate = 0.833333333333

The selective gate preserved true structural separation much better than global compression.

One case still failed:

diff_006_run_length_gradient_vs_binary_alternation

It remained classified as partial instead of split.

Result:

PARTIAL PASS


---

FALSE_MERGE_TRAP

count=4
success_rate=0.0
avg_alias_evidence=0.3
avg_baseline_distance=0.0
avg_resilient_distance=0.0

False-merge traps remained unresolved.

The reason is structural:

baseline_distance = 0.0

Once projection collapses two distinct cases into the same projected form, this layer has no signal to recover the distinction.

Failed cases:

fm_001_temperature_vs_finance
fm_002_periodicity_spoofing
fm_003_json_field_erasure
fm_004_low_high_vs_zero_extreme

Result:

FAIL


---

FALSE_SPLIT_TRAP

count=4
success_rate=0.0
avg_alias_evidence=0.1375
avg_baseline_distance=0.7265625
avg_resilient_distance=0.7265625

This is the main failure of v2.

The detector did not recognize false-split alias patterns.

Because alias evidence remained too low, the compression gate did not activate.

Failed cases:

fs_001_alias_inflation_binary
fs_002_cardinality_inflation_cycle
fs_003_separator_attack
fs_004_nested_alias_split

Interpretation:

the alias detector is too weak

The resilience mechanism exists, but it is not triggered where it is needed.

Result:

FAIL


---

PARTIAL_DRIFT

count=6
success_rate=0.333333333333
avg_alias_evidence=0.986534916667
avg_baseline_distance=0.17328042328
avg_resilient_distance=0.148125881297

Partial drift improved compared with v1.

v1 result:

PARTIAL_DRIFT success_rate = 0.166666666667

v2 result:

PARTIAL_DRIFT success_rate = 0.333333333333

Correct cases:

drift_005_run_length_gradient
drift_006_mirror_sequence

Failed cases:

drift_001_binary_alternation
drift_002_four_cycle
drift_003_triple_cycle
drift_004_nested_blocks

Interpretation:

the system still over-merges mild drift, but less badly than v1.

Result:

FAIL


---

Comparison With v1

v1

success_rate = 0.5
STRUCTURAL_DIFFERENT success_rate = 0.5
PARTIAL_DRIFT success_rate = 0.166666666667

v2

success_rate = 0.59375
STRUCTURAL_DIFFERENT success_rate = 0.833333333333
PARTIAL_DRIFT success_rate = 0.333333333333

v2 is not a full success.

But it is structurally safer than v1.

The key improvement is:

selective compression preserved true separation better than global compression


---

Main Finding

Structural Boundary Resilience v2 fails the benchmark, but validates one important design principle:

global distance compression is structurally unsafe

and:

selective gated compression is safer

The failure is not in the idea of selective resilience.

The failure is in the alias-evidence detector.


---

Main Failure Mechanism

The alias detector used token-frequency overlap.

That was insufficient.

False-split traps had:

avg_alias_evidence = 0.1375

So the gate stayed closed.

But those are exactly the cases where alias-aware compression should activate.

Therefore:

frequency overlap is not enough to detect structural aliasing

A better detector must compare transformation structure, not token identity.


---

Operational Interpretation

The v2 layer separates three outcomes.

Stable

STRUCTURAL_EQUIVALENT
STRUCTURAL_NEAR_EQUIVALENT

These remain correct.

Improved

STRUCTURAL_DIFFERENT
PARTIAL_DRIFT

These improved compared with v1.

Still Failed

FALSE_MERGE_TRAP
FALSE_SPLIT_TRAP

False merges are hard projection-collapse boundaries.

False splits require better alias detection.


---

Requirements for v3

A valid v3 should not simply lower thresholds.

It should improve the detector.

Required changes:

detect alias inflation by transition-pattern similarity

compare periodic structure after symbol renaming

separate token-frequency similarity from structural similarity

preserve STRUCTURAL_DIFFERENT separation

avoid global compression

keep false-merge traps marked as hard boundaries

treat partial drift separately from alias inflation


Core v3 rule:

compress only when two sequences differ in symbols
but preserve transition topology


---

Why The FAIL Is Useful

This FAIL is not noise.

It shows:

the gate works
but the evidence function is incomplete

The experiment therefore identifies the next technical target:

alias evidence must be structural,
not lexical


---

Limitations

This is not the full OMNIA engine.

This is a toy resilience layer.

Alias evidence is heuristic.

No semantic truth is evaluated.

False merges may remain unresolved.

No universal robustness claim is made.


---

Reproduction

python examples/structural_boundary_resilience_v2.py


---

Final Result

FAIL — structural boundary resilience v2 did not satisfy pass condition.

But relative to v1:

v2 is a safer failed mitigation.

It preserves true structural separation better and exposes the need for a genuinely structural alias detector.