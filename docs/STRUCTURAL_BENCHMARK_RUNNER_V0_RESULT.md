# Structural Benchmark Runner v0 — Result

## Status

```text
Status: FAIL
Claim level: Level 1 — Benchmark Runner


---

Purpose

This experiment runs the OMNIA-native structural benchmark dataset and measures how the current projection-based structural layer behaves across:

structural equivalence

near-equivalence

structural difference

false-merge traps

false-split traps

partial structural drift


Core boundary:

measurement != inference != decision


---

Dataset

Dataset file:

data/structural_benchmark_dataset_v0.jsonl

Result file:

results/structural_benchmark_runner_v0.json

Total records:

32


---

Global Result

Summary

Record count:             32
Success count:            19
Success rate:             0.59375

False merge count:        4
False split count:        4
Partial mismatch count:   5


---

Pair-Type Performance

STRUCTURAL_EQUIVALENT

count=6
success_rate=1.0
avg_distance=0.0

Observed behavior:

all equivalent structures merged correctly

representation renaming preserved structural identity

canonical projection remained stable


Result:

PASS


---

STRUCTURAL_NEAR_EQUIVALENT

count=6
success_rate=1.0
avg_distance=0.053218276863

Observed behavior:

sparse perturbations remained structurally close

local noise did not destroy equivalence detection

near-equivalent sequences remained mergeable


Result:

PASS


---

STRUCTURAL_DIFFERENT

count=6
success_rate=1.0
avg_distance=0.673722414857

Observed behavior:

structurally different families separated correctly

projection layer maintained large inter-family distance

cyclic, nested, mirror, and run-gradient structures remained distinguishable


Result:

PASS


---

FALSE_MERGE_TRAP

count=4
success_rate=0.0
avg_distance=0.0

Observed behavior:

all false-merge traps collapsed

structurally different semantic domains projected identically

projection erased distinctions required for separation


Examples:

temperature vs finance
periodicity spoofing
metadata erasure
low-high vs zero-extreme

Interpretation:

the current projection layer cannot distinguish some structurally distinct systems once projection collapses them into the same canonical form.

Result:

FAIL


---

FALSE_SPLIT_TRAP

count=4
success_rate=0.0
avg_distance=0.834204659118

Observed behavior:

equivalent systems split incorrectly

alias inflation and cardinality inflation fragmented equivalent structure

separator instability produced catastrophic split behavior


Examples:

alias inflation
cardinality inflation
separator attack
nested alias split

Interpretation:

the current projection layer remains highly sensitive to representational fragmentation.

Result:

FAIL


---

PARTIAL_DRIFT

count=6
success_rate=0.166666666667
avg_distance=0.207587893742

Observed behavior:

most partial-drift cases collapsed into merge

one case separated into split

only one case remained classified as partial


Interpretation:

the current threshold regime poorly models gradual structural degradation.

Result:

FAIL


---

Important Structural Observation

The benchmark exposes a critical asymmetry:

clean equivalence detection is strong
clean difference detection is strong

boundary behavior remains weak

Specifically:

equivalent            -> stable
near-equivalent       -> stable
different             -> stable

false-merge traps     -> unstable
false-split traps     -> unstable
partial drift          -> unstable

This means:

the projection layer behaves correctly
inside clean regions

but behaves poorly near structural boundaries


---

Structural Interpretation

This benchmark is useful precisely because it fails.

The benchmark demonstrates:

where projection collapses information

where alias inflation destabilizes identity

where structural drift becomes ambiguous

where partial degradation cannot yet be modeled correctly


The benchmark therefore acts as:

a structural stress map

rather than a success showcase.


---

Main Insight

Current projection-only structural comparison is sufficient for:

clean equivalence
clean separation

but insufficient for:

boundary-sensitive structural reasoning

especially under:

projection collapse

alias inflation

separator instability

partial drift

cardinality distortion



---

Operational Meaning

The FAIL result does not invalidate the benchmark.

Instead:

the benchmark successfully exposes
known projection fragilities

This is operationally valuable because the benchmark now becomes:

a reproducible structural failure harness

for future resilience layers and mitigation systems.


---

Limitations

This is not the full OMNIA engine.

This is a toy benchmark runner.

Thresholds are manually chosen.

No semantic truth is evaluated.

The dataset is synthetic.

No universal robustness claim is made.


---

Reproduction

python examples/structural_benchmark_runner_v0.py


---

Final Classification

FAIL — structural benchmark runner v0 did not satisfy pass condition.

Pass condition:

success_rate >= 0.60
and false_merge_count <= 4
and false_split_count <= 4

Measured result:

success_rate = 0.59375

The system therefore failed the benchmark threshold by:

0.00625

while simultaneously exposing multiple unresolved projection-boundary instabilities.