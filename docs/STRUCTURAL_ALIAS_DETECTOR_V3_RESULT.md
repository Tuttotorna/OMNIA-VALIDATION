Nome file:

docs/STRUCTURAL_ALIAS_DETECTOR_V3_RESULT.md

Contenuto completo:

# Structural Alias Detector v3 — Result

## Status

```text
Status: FAIL
Version: 0.3.0


---

Purpose

This experiment tested whether structural aliasing can be detected by comparing transition topology instead of lexical token overlap.

The goal was to move beyond token identity.

Core boundary:

measurement != inference != decision


---

Dataset

Dataset file:

data/structural_benchmark_dataset_v0.jsonl

Result file:

results/structural_alias_detector_v3.json

Total records:

32


---

Global Result

Record count:    32
Success count:   12
Success rate:    0.375

Final classification:

FAIL


---

Pair-Type Results

STRUCTURAL_EQUIVALENT

count=6
success_rate=1.0

Clean structural equivalence was detected correctly.

All structurally identical clean representations produced high alias evidence:

alias_evidence = 0.95
transition_score = 1.0
structural_bonus = 0.25

Result:

PASS


---

STRUCTURAL_DIFFERENT

count=6
success_rate=1.0

Clean structural differences were separated correctly.

This is the strongest positive result of v3.

The detector successfully distinguished different structural families when the structures were clean.

Result:

PASS


---

STRUCTURAL_NEAR_EQUIVALENT

count=6
success_rate=0.0

All near-equivalent cases failed.

The detector treated small perturbations as major topological changes.

Typical values:

transition_score = 0.0
alias_evidence ≈ 0.09

Interpretation:

the graph signature is too rigid.

Result:

FAIL


---

FALSE_MERGE_TRAP

count=4
success_rate=0.0

All false-merge traps failed.

These cases produced very high structural similarity:

alias_evidence = 0.95
transition_score = 1.0

But their expected relation was separation.

This confirms a hard boundary:

pure structure cannot separate cases
when the projected transition topology is identical

Result:

FAIL


---

FALSE_SPLIT_TRAP

count=4
success_rate=0.0

All false-split traps failed.

The detector did not recognize alias-inflated structures as equivalent.

Observed values:

fs_001_alias_inflation_binary      alias_evidence = 0.1
fs_002_cardinality_inflation_cycle alias_evidence = 0.233333333333
fs_003_separator_attack            alias_evidence = 0.0
fs_004_nested_alias_split          alias_evidence = 0.0

Interpretation:

the detector compares graph signatures too literally.

Alias inflation changes the graph form enough to break exact matching.

Result:

FAIL


---

PARTIAL_DRIFT

count=6
success_rate=0.0

All partial-drift cases failed.

Most cases showed high lexical overlap but low transition topology similarity.

Example pattern:

lexical_score ≈ 0.95
transition_score = 0.0
alias_evidence ≈ 0.095

Interpretation:

token overlap remains high, but the exact transition signature fails to capture gradual degradation.

Result:

FAIL


---

Main Positive Finding

v3 proves one useful thing:

transition topology works well on clean cases

Specifically:

STRUCTURAL_EQUIVALENT = 1.0
STRUCTURAL_DIFFERENT  = 1.0

So transition topology is a stronger structural signal than lexical overlap for clean structural comparison.


---

Main Negative Finding

v3 fails under perturbation.

The failure mode is clear:

exact graph signature matching is too brittle

Small local changes cause the transition signature to change sharply.

This collapses the detector on:

STRUCTURAL_NEAR_EQUIVALENT
PARTIAL_DRIFT
FALSE_SPLIT_TRAP


---

Hard Boundary Finding

False-merge traps remain unresolved.

When two different intended structures produce identical transition topology, a structure-only detector cannot separate them.

This is not a bug.

It is a boundary.

same transition topology
same projected structure
no semantic signal

Therefore:

no structural-only recovery is possible at this layer


---

Interpretation

v3 is not a valid final detector.

But it validates the direction:

alias detection must be structural,
not lexical

The current implementation is just too exact.

The next step is not to return to token overlap.

The next step is:

fuzzy transition topology


---

Why v3 Failed

v3 used exact graph-signature overlap.

That means:

small transition perturbation
→ changed graph signature
→ low similarity
→ failed alias detection

This is too brittle for real structural measurement.

A robust detector must compare:

transition distributions

edge-weight similarity

local motif similarity

normalized graph distance

tolerated perturbation bands

edit distance between transition traces


not exact signature equality.


---

Requirements for v4

v4 should introduce fuzzy transition topology.

Minimum requirements:

compare transition distributions probabilistically

tolerate sparse local perturbations

preserve clean structural separation

detect alias-inflated equivalent structures

keep false-merge traps marked as hard boundaries

separate partial drift from full equivalence

avoid relying on lexical token overlap


Core design rule:

do not ask whether transition graphs are identical;
ask how much structure survives under perturbation


---

Operational Conclusion

v3 is a failed detector, but a useful experiment.

It establishes:

clean topology is useful
exact topology is brittle

Therefore v4 must measure fuzzy structural similarity rather than exact structural identity.


---

Limitations

This is not the full OMNIA engine.

This is a toy alias detector.

No semantic truth is evaluated.

Graph signatures remain simplified.

No universal robustness claim is made.


---

Reproduction

python examples/structural_alias_detector_v3.py


---

Final Result

FAIL — structural alias detector v3 did not satisfy pass condition.

But the failure is informative:

transition topology is directionally correct,
but exact graph matching is too fragile.