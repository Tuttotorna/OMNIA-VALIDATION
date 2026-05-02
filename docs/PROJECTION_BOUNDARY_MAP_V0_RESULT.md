# PROJECTION BOUNDARY MAP v0

## Status

```text
PASS
```

## Operational Classification

```text
BOUNDARY_MAP_BUILT
```

## Claim Level

```text
Level 1 — Toy Demonstration
```

---

# Purpose

This experiment maps structural failure boundaries of a first-seen canonical projection layer.

The goal is not to prove universal invariance.

The goal is to identify:

- which projection assumptions fail,
- how they fail,
- what observable effects they produce,
- and whether those effects are measurable in a reproducible way.

This experiment extends:

```text
cross_domain_invariance_v0_2
adversarial_representation_v0
```

toward:

```text
structured boundary taxonomy
```

---

# Core Boundary

```text
measurement != inference != decision
```

---

# Experiment Logic

The experiment evaluates multiple attack families against a canonical projection system.

Each attack intentionally breaks one structural assumption.

The experiment then measures:

```text
projection behavior
distance behavior
observed structural effect
severity
```

Expected outcomes:

| Intended relation | Observed failure |
|---|---|
| different structures collapse | false_merge |
| same structures separate | false_split |
| partial degradation | partial_split |

---

# Attack Families

## MANY_TO_ONE_COLLAPSE

Broken assumption:

```text
token_identity_is_disposable
```

Observed effect:

```text
false_merge
```

Meaning:

Different intended structures collapse into the same projected form.

Example:

```text
hot/cold alternation
buy/sell alternation
```

Both become:

```text
010101010101...
```

Result:

```text
combined_distance = 0.0
```

---

## ALIAS_INFLATION

Broken assumption:

```text
stable_symbol_identity
```

Observed effect:

```text
false_split
```

Meaning:

Equivalent structures are separated by adversarial alias expansion.

Example:

```text
binary alternation
```

becomes:

```text
012345012345...
```

instead of:

```text
010101010101...
```

Result:

```text
combined_distance = 1.263691235877
```

---

## CARDINALITY_INFLATION

Broken assumption:

```text
state_cardinality_is_stable
```

Observed effect:

```text
false_split
```

Meaning:

Equivalent cyclic systems become separated by artificial state inflation.

Example:

```text
01230123...
```

vs

```text
01234567...
```

Result:

```text
combined_distance = 0.826827245531
```

---

## SEPARATOR_ATTACK

Broken assumption:

```text
token_boundaries_are_reliable
```

Observed effect:

```text
false_split
```

Meaning:

Changing separators changes projected topology.

Result:

```text
combined_distance = 0.827486195701
```

---

## PERIODICITY_SPOOFING

Broken assumption:

```text
periodicity_implies_structural_equivalence
```

Observed effect:

```text
false_merge
```

Meaning:

Different systems sharing the same period collapse together.

Result:

```text
combined_distance = 0.0
```

---

## LOCAL_SWAP_DRIFT

Broken assumption:

```text
local_order_is_stable
```

Observed effect:

```text
partial_split
```

Meaning:

Small local permutations degrade structural similarity without complete collapse.

Result:

```text
projected_edit_distance = 0.09375
combined_distance       = 0.233612057667
```

This is the weakest detected attack in the experiment.

---

## JSON_FIELD_ERASURE

Broken assumption:

```text
ignored_fields_are_irrelevant
```

Observed effect:

```text
false_merge
```

Meaning:

Metadata erasure causes structurally different systems to collapse together.

Result:

```text
combined_distance = 0.0
```

---

# Controls

## Equivalent Control

Expected:

```text
correct_merge
```

Observed:

```text
correct_merge
```

Result:

```text
combined_distance = 0.0
```

---

## Separate Control

Expected:

```text
correct_split
```

Observed:

```text
correct_split
```

Result:

```text
combined_distance = 0.827486195701
```

---

# Boundary Summary

## Attack Families

```text
7
```

```text
ALIAS_INFLATION
CARDINALITY_INFLATION
JSON_FIELD_ERASURE
LOCAL_SWAP_DRIFT
MANY_TO_ONE_COLLAPSE
PERIODICITY_SPOOFING
SEPARATOR_ATTACK
```

---

## Observed Effects

```text
3
```

```text
false_merge
false_split
partial_split
```

---

## Broken Assumptions

```text
7
```

```text
ignored_fields_are_irrelevant
local_order_is_stable
periodicity_implies_structural_equivalence
stable_symbol_identity
state_cardinality_is_stable
token_boundaries_are_reliable
token_identity_is_disposable
```

---

## Detection Summary

```text
detected_boundary_count   = 7
undetected_boundary_count = 0
control_ok                = True
```

---

## Severity

```text
average_severity = 0.821151920176
max_severity     = 1.0
```

---

# Main Insight

Projection robustness is not a single property.

Different attack families break different assumptions and produce different measurable failure signatures.

This means:

```text
"invariance"
```

is not binary.

It is conditional on:

```text
projection assumptions
token stability
cardinality stability
boundary stability
ordering stability
field preservation
```

---

# Interpretation

PASS means:

- multiple projection boundaries were successfully identified,
- multiple failure effects were reproduced,
- controls remained valid,
- and a minimal structural boundary map was built.

This experiment does not prove robust invariance.

It demonstrates:

```text
measurable projection fragility topology
```

---

# Pass Condition

```text
attack_family_count >= 4
and observed_effect_count >= 3
and detected_boundary_count >= 5
and control_ok == true
```

Observed:

```text
attack_family_count       = 7
observed_effect_count     = 3
detected_boundary_count   = 7
control_ok                = True
```

Result:

```text
PASS
```

---

# Limitations

```text
This is not the full OMNIA engine.
This is a toy projection boundary map.
The canonical projection is hand-built.
Attack families are synthetic and manually designed.
Severity is a toy proxy.
No semantic truth is evaluated.
No universal robustness claim is made.
No external reproduction is included yet.
```

---

# Reproduction

```bash
python examples/projection_boundary_map_v0.py
```

---

# Final Conclusion

This experiment shows that projection systems possess:

```text
detectable structural boundaries
```

and that these boundaries can be:

```text
classified
mapped
measured
grouped by assumption
grouped by effect
```

The result is not universal robustness.

The result is:

```text
a measurable topology of projection fragility
```