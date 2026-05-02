# Structural Alias Detector v4 — Result

## Status

```text
Status: FAIL
Version: 0.4.0


---

Purpose

This experiment tested fuzzy transition-topology similarity.

The goal was to improve v3, which used exact graph-signature matching and failed under small perturbations.

Core boundary:

measurement != inference != decision


---

Dataset

Dataset file:

data/structural_benchmark_dataset_v0.jsonl

Result file:

results/structural_alias_detector_v4.json

Total records:

32


---

Global Result

Record count:    32
Success count:   15
Success rate:    0.46875

Final classification:

FAIL


---

Pair-Type Results

STRUCTURAL_EQUIVALENT

count=6
success_rate=1.0
avg_fuzzy_similarity=1.0
avg_transition_overlap=1.0
avg_motif3_overlap=1.0

Clean structural equivalence was detected correctly.

Result:

PASS


---

STRUCTURAL_NEAR_EQUIVALENT

count=6
success_rate=1.0
avg_fuzzy_similarity=0.875887796375
avg_transition_overlap=0.905218260538
avg_motif3_overlap=0.85553855051

This is the main improvement over v3.

v3 result:

STRUCTURAL_NEAR_EQUIVALENT success_rate = 0.0

v4 result:

STRUCTURAL_NEAR_EQUIVALENT success_rate = 1.0

Fuzzy topology correctly tolerated small perturbations.

Result:

PASS


---

STRUCTURAL_DIFFERENT

count=6
success_rate=0.333333333333
avg_fuzzy_similarity=0.398812986671
avg_transition_overlap=0.274508949491
avg_motif3_overlap=0.033990147783

This is the main regression.

v3 result:

STRUCTURAL_DIFFERENT success_rate = 1.0

v4 result:

STRUCTURAL_DIFFERENT success_rate = 0.333333333333

The detector became too permissive.

Several genuinely different structures were classified as medium_similarity instead of low_similarity.

Failed cases:

diff_001_binary_alternation_vs_four_cycle
diff_004_triple_cycle_vs_mirror_sequence
diff_005_nested_blocks_vs_mirror_sequence
diff_006_run_length_gradient_vs_binary_alternation

Result:

FAIL


---

FALSE_MERGE_TRAP

count=4
success_rate=0.0
avg_fuzzy_similarity=1.0
avg_transition_overlap=1.0
avg_motif3_overlap=1.0

False-merge traps remained unresolved.

These cases are structurally indistinguishable under this layer.

They produce maximum similarity:

fuzzy_similarity = 1.0
transition_overlap = 1.0
motif3_overlap = 1.0

But their expected relation is separation.

This confirms the hard boundary:

same projected transition topology
same measured structure
no structural-only recovery

Result:

FAIL


---

FALSE_SPLIT_TRAP

count=4
success_rate=0.0
avg_fuzzy_similarity=0.306381490303
avg_transition_overlap=0.202380952381
avg_motif3_overlap=0.064516129032

False-split traps remained unresolved.

The fuzzy detector improved some scores relative to exact matching, but not enough to classify them as high similarity.

Failed cases:

fs_001_alias_inflation_binary
fs_002_cardinality_inflation_cycle
fs_003_separator_attack
fs_004_nested_alias_split

Interpretation:

alias inflation still changes the observed topology too much for this detector.

Result:

FAIL


---

PARTIAL_DRIFT

count=6
success_rate=0.166666666667
avg_fuzzy_similarity=0.880146650131
avg_transition_overlap=0.873275070194
avg_motif3_overlap=0.777960141246

Partial drift improved only minimally.

Correct case:

drift_006_mirror_sequence

Failed cases:

drift_001_binary_alternation
drift_002_four_cycle
drift_003_triple_cycle
drift_004_nested_blocks
drift_005_run_length_gradient

Most partial-drift cases were classified as high_similarity, not medium_similarity.

Interpretation:

v4 is too tolerant of mild local drift.

Result:

FAIL


---

Comparison With v3

v3

success_rate = 0.375

STRUCTURAL_EQUIVALENT      = 1.0
STRUCTURAL_NEAR_EQUIVALENT = 0.0
STRUCTURAL_DIFFERENT       = 1.0
PARTIAL_DRIFT              = 0.0
FALSE_SPLIT_TRAP           = 0.0
FALSE_MERGE_TRAP           = 0.0

v4

success_rate = 0.46875

STRUCTURAL_EQUIVALENT      = 1.0
STRUCTURAL_NEAR_EQUIVALENT = 1.0
STRUCTURAL_DIFFERENT       = 0.333333333333
PARTIAL_DRIFT              = 0.166666666667
FALSE_SPLIT_TRAP           = 0.0
FALSE_MERGE_TRAP           = 0.0

v4 improves perturbation tolerance.

But it weakens separation.


---

Main Positive Finding

v4 validates fuzzy transition topology for near-equivalence.

The detector now preserves structural similarity under small perturbations:

STRUCTURAL_NEAR_EQUIVALENT success_rate = 1.0

This fixes the main brittleness of v3.


---

Main Negative Finding

v4 is too permissive.

It turns too many truly different structures into medium_similarity.

The key regression is:

STRUCTURAL_DIFFERENT success_rate = 0.333333333333

This means the detector cannot be accepted as a robust alias detector.


---

Technical Diagnosis

v3 failed because it was too rigid.

v4 failed because it is too permissive.

v3 = exact topology, brittle
v4 = fuzzy topology, over-tolerant

The missing component is a second signal:

dissimilarity risk

A single fuzzy similarity score is not enough.


---

Hard Boundary Finding

False-merge traps remain impossible for this layer.

When two cases produce identical structural projections, structural-only measurement cannot separate them.

This remains true in v4.

FALSE_MERGE_TRAP avg_fuzzy_similarity = 1.0

Therefore these cases should be classified as hard boundaries, not ordinary detector failures.


---

Requirements for v5

v5 should not simply tune thresholds.

It needs dual scoring:

similarity_score
dissimilarity_risk

A case should be classified as high similarity only if:

similarity_score is high
and dissimilarity_risk is low

Minimum v5 requirements:

preserve STRUCTURAL_NEAR_EQUIVALENT

recover STRUCTURAL_DIFFERENT

keep false-merge traps marked as hard boundaries

improve partial drift separation

avoid global permissiveness

separate alias evidence from true similarity

add risk features based on motif loss, cardinality inflation, and transition mismatch


Core v5 rule:

do not trust high similarity alone


---

Operational Conclusion

v4 is a failed detector, but it proves an important direction:

fuzzy topology solves perturbation brittleness

However:

fuzzy topology alone weakens true structural separation

The correct next step is not more fuzziness.

The correct next step is controlled fuzziness with a dissimilarity-risk gate.


---

Limitations

This is not the full OMNIA engine.

This is a toy fuzzy topology detector.

Thresholds are manually chosen.

No semantic truth is evaluated.

False-merge traps remain hard boundaries.

No universal robustness claim is made.


---

Reproduction

python examples/structural_alias_detector_v4.py


---

Final Result

FAIL — structural alias detector v4 did not satisfy pass condition.

But relative to v3:

v4 is better for perturbation tolerance
and worse for structural separation.