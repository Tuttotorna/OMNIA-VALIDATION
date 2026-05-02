# Adversarial Representation v0 — Result

## Status

```text
PASS

Operational Classification

BOUNDARY_DETECTED

Evidence Level

Level 1 — Toy Demonstration

Experiment

adversarial_representation_v0

Repository

OMNIA-VALIDATION


---

Purpose

This experiment tests whether a minimal first-seen canonical projection can be broken by adversarial representation design.

The goal is not to prove robustness.

The goal is to detect measurable boundaries.

Core question:

can adversarial representations cause false merges
or false splits after canonical projection?

Observed result:

yes


---

Core Boundary

measurement != inference != decision

The experiment measures structural behavior only.

It does not:

infer semantic truth

decide meaning

validate the full OMNIA engine

prove universal adversarial robustness

prove representation-free mathematics



---

Background

Previous cross-domain invariance chain:

cross_domain_invariance_v0:
raw representation dominated structure
FAIL / NEGATIVE_RESULT

cross_domain_invariance_v0_1:
clean canonical projection recovered structure
PASS

cross_domain_invariance_v0_2:
canonical projection survived deterministic noise
PASS

This experiment tests the next boundary:

can canonical projection be deliberately fooled?


---

Projection Under Test

The projection under test is:

first-seen canonical projection

Example:

A B A B
->
0 1 0 1

and:

hot cold hot cold
->
0 1 0 1

and:

buy sell buy sell
->
0 1 0 1

This projection removes token identity and preserves order of first appearance.

That is useful for representation invariance.

It is also fragile.


---

Failure Modes Tested

Two adversarial failure modes were tested.

1. False Merge

different intended structures
->
same / near-same canonical projection

This happens when different meanings or domains share the same surface pattern.

2. False Split

same intended structure
->
different canonical projection

This happens when aliases or token-boundary tricks cause one conceptual state to appear as multiple states.


---

PASS Meaning

In this experiment, PASS does not mean the projection resisted attack.

It means:

adversarial boundaries were detected and documented
while clean controls remained valid

This repository is falsification-oriented.

Finding a controlled weakness is a useful result.


---

Observed Summary

Observed output:

Status: PASS
Operational classification: BOUNDARY_DETECTED
Claim level: Level 1 — Toy Demonstration

Attack count:

8

Expected failure cases:

8

Controls:

equivalent_controls_ok = True
separate_controls_ok   = True
controls_ok            = True

This means the attack cases exposed boundaries while the clean controls behaved as expected.


---

False Merge Results

False merge attacks detected:

6

All detected false merges had:

projected_edit_distance = 0.0
combined_distance       = 0.0

This means different intended structures collapsed into identical canonical projections.


---

False Merge Examples

Temperature vs Finance

false_merge_A_temperature
<->
false_merge_B_finance

Observed:

projected_edit_distance = 0.0
combined_distance       = 0.0

Interpretation:

hot/cold alternation
and
buy/sell alternation
collapsed into the same projection

Both became:

010101010101...


---

Temperature vs Low/High

false_merge_A_temperature
<->
false_merge_C_low_high

Observed:

projected_edit_distance = 0.0
combined_distance       = 0.0

Interpretation:

different intended structures
became indistinguishable
under first-seen projection


---

Finance vs Zero/Extreme

false_merge_B_finance
<->
false_merge_D_zero_extreme

Observed:

projected_edit_distance = 0.0
combined_distance       = 0.0

Interpretation:

token meaning was erased
and only alternation remained


---

False Merge Insight

Main false merge insight:

first-seen projection preserves formal alternation
but destroys token identity

Therefore:

different intended structures
can collapse into the same canonical structure

This is not a bug only.

It is a boundary.

It shows exactly what this lens can and cannot see.


---

False Split Results

False split attacks detected:

2

Detected cases:

false_split_A_clean
<->
false_split_B_aliases

and:

false_split_C_clean_cycle
<->
false_split_D_alias_cycle


---

False Split Example 1

Clean binary alternation:

left right left right ...

Projection:

010101010101...

Alias-based binary alternation:

left_a right_a left_b right_b left_c right_c ...

Projection:

012345012345...

Observed:

projected_edit_distance = 0.65625
combined_distance       = 1.263691235877

Interpretation:

same intended binary alternation
was split into a higher-cardinality projected structure


---

False Split Example 2

Clean four-cycle:

north east south west ...

Projection:

012301230123...

Alias-based four-cycle:

north_a east_a south_a west_a north_b east_b south_b west_b ...

Projection:

0123456701234567...

Observed:

projected_edit_distance = 0.5
combined_distance       = 0.826827245531

Interpretation:

same intended four-state cycle
was split into an eight-state projected structure


---

False Split Insight

Main false split insight:

aliasing can inflate apparent structural state count

Therefore:

same intended structure
can become artificially distant
under first-seen projection

This exposes a real weakness of naive canonicalization.


---

Control Results

Clean controls behaved correctly.

Equivalent binary controls:

control_binary_clean_1
<->
control_binary_clean_2

Observed:

projected_edit_distance = 0.0
combined_distance       = 0.0

Equivalent four-cycle controls:

control_four_cycle_1
<->
control_four_cycle_2

Observed:

projected_edit_distance = 0.0
combined_distance       = 0.0

Different controls remained separated:

binary_alternation
vs
four_cycle

Observed:

projected_edit_distance = 0.5
combined_distance       = 0.827486195701

Control status:

controls_ok = True


---

Why Controls Matter

Controls show that the projection was not simply broken everywhere.

It behaved as intended on clean cases.

The adversarial cases exposed specific boundaries:

false merge through token-identity erasure

and:

false split through alias inflation

This makes the result more useful than a generic failure.


---

Main Result

The main result is:

first-seen canonical projection is useful
but adversarially fragile

More precisely:

it can recover clean invariance
and survive deterministic noise,
but it can be broken by adversarial token design


---

Main Insight

Main insight:

canonical projection is a lens,
not a universal truth function

It measures structure under a specific transformation rule.

It cannot preserve everything.

It loses token identity by design.

That design choice creates both power and vulnerability.


---

Why This Matters For OMNIA

This result strengthens the OMNIA boundary discipline.

It shows that a structural measurement layer must explicitly state:

what transformations are allowed

what information is discarded

what equivalences are created

what attacks can exploit the projection

where the lens becomes unreliable


This directly supports the principle:

measurement != inference != decision

The measurement can expose a structural behavior.

It cannot decide whether two projected structures are semantically equivalent.


---

Failure-Recovery-Boundary Chain

The validation chain now has four stages.

v0

raw signatures
->
representation dominates structure
->
FAIL / NEGATIVE_RESULT

v0.1

clean canonical projection
->
structure recovered
->
PASS

v0.2

noisy canonical projection
->
structure preserved with degradation
->
PASS

adversarial_representation_v0

adversarial representation
->
projection boundaries detected
->
PASS / BOUNDARY_DETECTED

This is a strong methodological chain.

It does not claim invincibility.

It documents capability and limits.


---

What This Experiment Does NOT Prove

This experiment does NOT prove:

OMNIA is adversarially robust

canonical projection is universally valid

semantic identity can be inferred

false merges are always wrong

false splits are always wrong

all adversarial attacks are covered

the full OMNIA engine has the same weakness

representation-free mathematics is achieved


It only proves:

this toy canonical projection has measurable adversarial boundaries


---

Important Constraint

Correct claim:

the first-seen canonical projection has detectable false-merge
and false-split boundaries under synthetic adversarial cases

Incorrect claim:

OMNIA is broken

Incorrect claim:

OMNIA is adversarially robust

Incorrect claim:

canonical projection proves semantic equivalence


---

JSON Result

Generated file:

results/adversarial_representation_v0.json

Key fields:

{
  "status": "PASS",
  "operational_classification": "BOUNDARY_DETECTED",
  "attack_count": 8,
  "expected_failure_case_count": 8,
  "control_analysis": {
    "equivalent_controls_ok": true,
    "separate_controls_ok": true,
    "controls_ok": true
  }
}


---

Reproduction Command

Run from repository root:

python examples/adversarial_representation_v0.py

Expected classification:

PASS

Expected operational classification:

BOUNDARY_DETECTED

Expected attack count:

8


---

Colab Reproduction

The experiment was reproduced in a clean Colab environment.

Observed summary:

Status: PASS
Operational classification: BOUNDARY_DETECTED

Attack count:
8

Expected failure cases:
8

Controls:
equivalent_controls_ok = True
separate_controls_ok   = True
controls_ok            = True

Return code:

0

The experiment executed correctly.


---

Result Classification

Operational classification:

BOUNDARY_DETECTED

Reason:

false merge and false split attacks were detected
while clean controls remained valid

Evidence level:

Level 1 — Toy Demonstration


---

Main Conclusion

Main conclusion:

first-seen canonical projection is useful for clean invariance,
but fragile under adversarial token design

More compressed:

normalization helps,
but normalization itself must be validated


---

Recommended Next Step

Recommended next experiment:

examples/projection_boundary_map_v0.py

Goal:

map which attacks break which projection assumptions

Recommended dimensions:

token identity loss

alias inflation

boundary ambiguity

reordered labels

fake periodicity

separator abuse

many-to-one collapse

one-to-many split


Core next question:

can projection failure modes be classified systematically?