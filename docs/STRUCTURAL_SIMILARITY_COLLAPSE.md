# STRUCTURAL SIMILARITY COLLAPSE

## Core Observation

The progression from rigid structural matching to fuzzy structural matching exposes a fundamental instability:

```text
exact similarity  -> brittle separation
fuzzy similarity  -> permissive collapse

This is not merely an implementation issue.

It appears to be a deeper structural tradeoff.


---

The Problem

A similarity system attempts to balance two opposite pressures:

1. tolerance
2. discrimination

If the system is too rigid:

small perturbations
→ false splits

If the system is too tolerant:

structural compression
→ false merges

The collapse emerges when:

high similarity
!=
safe equivalence


---

Observed Experimental Progression

v1 — Exact Structural Matching

Characteristics:

- strict boundaries
- low tolerance
- strong separation
- fragile equivalence detection

Behavior:

equivalent structures:
PASS

near-equivalent structures:
often FAIL

different structures:
mostly separated

Main failure mode:

false split


---

v4 — Fuzzy Structural Similarity

Characteristics:

- soft boundaries
- high tolerance
- improved near-equivalence detection
- degraded structural separation

Behavior:

equivalent structures:
PASS

near-equivalent structures:
PASS

different structures:
partially collapse

projection collisions:
catastrophic merges

Main failure mode:

false merge


---

Structural Similarity Collapse

The collapse occurs when fuzzy compression removes enough structural distinction that different systems become observationally indistinguishable.

Formally:

distinct generators
→ similar projections
→ compressed representation
→ merge instability

This creates:

projection collapse

where:

multiple structurally different origins
share the same observable topology


---

Critical Insight

The experiments suggest:

similarity alone
cannot guarantee separation

and:

invariance alone
cannot guarantee identity

This is important because many systems implicitly assume:

high similarity
≈
same structure

The benchmark results contradict this assumption.


---

Failure Geometry

The benchmark series begins to expose a geometry of failure:

False Split Region

same structure
→ representation perturbation
→ artificial separation

False Merge Region

different structure
→ projection compression
→ artificial equivalence

Drift Ambiguity Region

partial structural deformation
→ unstable classification

Projection Boundary Region

structure exceeds observable projection capacity


---

Important Consequence

The main output of the benchmark is not accuracy.

The important output is:

failure topology

Meaning:

where structure becomes unrecoverable

This includes:

irreversible compression

projection ambiguity

topology collision

indistinguishability zones

unstable equivalence boundaries



---

Structural Interpretation

The experiments increasingly suggest:

there may exist regions where
perfect structural discrimination
and
perfect structural tolerance
cannot coexist simultaneously

Meaning:

robust equivalence detection
may inherently trade against
safe structural separation


---

OMNIA Boundary Alignment

This aligns with the OMNIA boundary:

measurement != inference != decision

The detector measures observable structural behavior.

It does not prove:

identity
truth
semantic equivalence
causal equivalence


---

Experimental Implication

The benchmark evolves from:

"Can we measure similarity?"

to:

"What information is destroyed during projection?"

This reframes the problem from classification into:

structural observability limits


---

Current Experimental State

The project now contains:

- structural benchmark dataset
- boundary traps
- drift regions
- alias detectors
- resilience layers
- fuzzy topology experiments
- projection-collapse examples
- failure taxonomies

This forms an initial experimental framework for studying:

structural similarity collapse


---

Limitations

- This is not the full OMNIA engine.
- These are toy experimental detectors.
- Thresholds remain heuristic.
- No semantic truth is evaluated.
- No universal robustness claim is made.
- Results are exploratory.