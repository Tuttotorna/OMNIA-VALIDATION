# Temporal Collapse Critical Horizon Corrected v0 — Result

## Status

Status: PASS  
Version: 0.1.0  
Claim level: Level 2 — Critical Temporal Horizon Rule

---

## Purpose

This experiment corrects and validates the critical temporal horizon rule.

The previous experiment found a stable offset error:

    mean_horizon_error = -1

That showed the original rule was almost correct, but off by one because of zero-based temporal indexing.

This experiment tests the corrected rule:

    critical_horizon =
    first_raw_collapse + confirmation_window + persistence_window - 2

Core question:

    can the critical temporal horizon be predicted exactly
    from raw collapse onset, confirmation window, and persistence window?

Core boundary:

    measurement != arbitration != decision

This experiment does not evaluate semantic truth.

It evaluates temporal observability structure.

---

## Experiment File

    examples/temporal_collapse_critical_horizon_corrected_v0.py

Result file:

    results/temporal_collapse_critical_horizon_corrected_v0.json

Reproduction command:

    python examples/temporal_collapse_critical_horizon_corrected_v0.py

---

## Summary Result

    Status: PASS
    Version: 0.1.0

    confirmation_windows = [2, 3, 4, 5, 6, 7, 8]
    persistence_windows = [2, 3, 4, 5, 6, 7, 8]
    trajectory_lengths = [8, 10, 12, 14, 16]

    pair_count = 49

    observable_pair_count = 43
    unobservable_pair_count = 6
    observable_rate = 0.8775510204081632

    exact_corrected_match_count = 43
    exact_corrected_match_rate = 1.0

    mean_corrected_horizon_error = 0
    mean_minimum_observed_length = 12.837209302325581

    raw_collapse_onset_reference = 4

Corrected rule:

    critical_horizon =
    first_raw_collapse + confirmation_window + persistence_window - 2

The experiment passed.

The corrected critical horizon rule matched every observable pair.

---

## Main Finding

The central result is:

    exact_corrected_match_rate = 1.0

and:

    mean_corrected_horizon_error = 0

This means the corrected horizon rule perfectly matched all observable cases.

The temporal horizon is not just empirical.

It is structurally predictable under the tested rule.

---

## Corrected Rule

The corrected rule is:

    critical_horizon =
    first_raw_collapse + confirmation_window + persistence_window - 2

Where:

    first_raw_collapse = first raw COLLAPSE index
    confirmation_window = number of raw collapse frames required
    persistence_window = number of temporal collapse frames required

The minus 2 appears because both confirmation and persistence are counted inclusively under zero-based indexing.

---

## Why The Previous Rule Was Off

The previous estimated rule was:

    critical_horizon =
    first_raw_collapse + confirmation_window + persistence_window - 1

The observed error was:

    mean_horizon_error = -1

That means observed persistence appeared one step earlier than the estimated rule.

The corrected rule subtracts 2 instead of 1.

This exactly removes the offset.

---

## Indexing Explanation

Example:

    first_raw_collapse = 4
    confirmation_window = 2
    persistence_window = 2

Raw collapse sequence:

    step 4 = raw COLLAPSE
    step 5 = raw COLLAPSE

Temporal confirmation:

    step 4 = ESCALATE
    step 5 = temporal COLLAPSE

Persistence confirmation:

    step 5 = temporal COLLAPSE
    step 6 = temporal COLLAPSE

Therefore persistent collapse appears at:

    step 6

Formula:

    4 + 2 + 2 - 2 = 6

So the corrected rule matches the observed temporal horizon.

---

## Observability Result

    observable_pair_count = 43
    unobservable_pair_count = 6
    observable_rate = 0.8775510204081632

43 of 49 window pairs were observable within the tested trajectory lengths.

6 pairs were not observable because their corrected expected horizon was beyond the tested maximum trajectory length.

The tested maximum was:

    trajectory_length = 16

Therefore pairs requiring horizon beyond the available sequence remain unobservable.

---

## Exact Match Result

    exact_corrected_match_count = 43
    exact_corrected_match_rate = 1.0

Every observable pair matched the corrected rule.

This is the strongest result in the experiment.

It means the horizon rule is exact for all observable tested pairs.

---

## Horizon Error

    mean_corrected_horizon_error = 0

The average error is zero.

No observable pair deviated from the corrected prediction.

This converts the previous CHECK into a PASS.

---

## Minimum Observed Length

    mean_minimum_observed_length = 12.837209302325581

This is the average minimum trajectory length required to observe persistent collapse across observable window pairs.

This value is not the critical horizon itself.

It is the smallest tested trajectory length that was long enough to contain the critical horizon.

Because trajectory lengths were sampled discretely:

    8, 10, 12, 14, 16

the minimum observed length is rounded upward to the nearest tested length.

---

## Observable Versus Unobservable

A pair is observable when the tested trajectory length is long enough to include the corrected critical horizon.

A pair is unobservable when no tested trajectory length is long enough.

The 6 unobservable pairs are not contradictions.

They require longer trajectories.

The corrected expected horizons for those pairs were at the edge or beyond the tested limit.

---

## Unobservable Pairs

The unobservable pairs were:

    cw6_pw8
    cw7_pw7
    cw7_pw8
    cw8_pw6
    cw8_pw7
    cw8_pw8

These are the strictest temporal-window combinations.

They require longer observation horizons than the available tested lengths.

---

## Structural Meaning

This experiment shows that persistent collapse observability has an exact temporal horizon under the tested synthetic dynamics.

The horizon depends on three quantities:

    raw collapse onset
    confirmation window
    persistence window

This is a strong result because it converts temporal collapse from a label into a predictable timing relation.

---

## Relation To Phase Diagram v0

The previous phase diagram showed:

    safety_rate = 1.0
    pass_rate = 0.4266666666666667
    persistent_confirmed_rate = 0.4266666666666667

That experiment mapped the PASS/CHECK boundary.

This corrected horizon experiment explains the boundary.

The boundary exists because persistence becomes observable only after:

    first_raw_collapse + confirmation_window + persistence_window - 2

If the trajectory ends before that point, persistence is not observable.

---

## Relation To OMNIATEMPO

This experiment directly supports the OMNIATEMPO direction.

It shows that temporal structural collapse is governed by an observability horizon.

Collapse is not only:

    present

or:

    absent

It is also:

    temporally observable
    not yet temporally observable

depending on the available observation window.

This is precisely temporal structural measurement.

---

## Relation To TDelta

This experiment gives a concrete early proxy for TDelta-style reasoning.

The corrected critical horizon behaves like:

    a predicted divergence observability time

It answers:

    when does persistent collapse become observable?

The rule:

    critical_horizon =
    first_raw_collapse + confirmation_window + persistence_window - 2

is a simple temporal divergence-time law inside this controlled setup.

This is not full TDelta.

But it is an operational step toward measuring structural divergence over time.

---

## What This Confirms

This experiment supports:

    corrected critical horizon rule
    exact temporal observability prediction
    zero mean horizon error
    full exact match across observable pairs
    temporal persistence depends on finite observation horizon
    unobservable strict-window pairs require longer sequences
    phase diagram boundary is explainable by horizon length
    temporal collapse can be described by a timing rule

---

## What This Does Not Prove

This experiment does not prove:

    universal critical horizon law
    real-world temporal validity
    semantic correctness
    causal correctness
    optimal confirmation-window choice
    optimal persistence-window choice
    full TDelta
    full OMNIATEMPO correctness
    full OMNIA correctness

It validates a controlled synthetic temporal observability rule.

---

## Boundary Statement

This experiment does not evaluate:

    truth
    meaning
    semantic correctness
    intelligence
    causality
    real-world reliability
    full OMNIA correctness

It evaluates:

    corrected critical horizon of persistent temporal collapse

---

## Limitations

    The trajectories are synthetic.
    The raw collapse onset is stable in the tested trajectory.
    The confirmation rule is hand-defined.
    The persistence rule is hand-defined.
    Only trajectory lengths 8, 10, 12, 14, and 16 were tested.
    Only confirmation windows 2 through 8 were tested.
    Only persistence windows 2 through 8 were tested.
    No external temporal dataset was used.
    No semantic ground truth exists.

---

## Result Classification

Recommended classification:

    PASS

Evidence level:

    Level 2 — Critical Temporal Horizon Rule

Reason:

    49 window pairs tested
    43 observable pairs
    6 unobservable pairs
    exact corrected match rate = 1.0
    mean corrected horizon error = 0
    corrected rule validated on all observable pairs
    unobservable pairs explained by insufficient trajectory length

This is a successful controlled temporal-rule validation.

---

## Relation To Previous Results

Validation path:

    Effective Observer Count v0
    -> raw_count != effective_count

    Recoverability Effective Observer v0
    -> flawed recoverability proxy exposed

    Recoverability Effective Observer v1
    -> proxy corrected

    Correlation Analysis v0
    -> effective_count beats raw_count

    Correlation Stability v0
    -> correlation stability verified

    Correlation Adversarial v0
    -> adversarial boundary exposed

    Recoverability Gate v0
    -> multi-signal gate detects instability

    Recoverability Gate Stability v0
    -> threshold stability verified

    Recoverability Gate Adversarial v0
    -> adversarial resistance improved

    Recoverability Gate Randomized v0
    -> coherent randomized behavior

    Recoverability Gate Randomized Stability v0
    -> stable randomized behavior

    Recoverability Gate External Proxy v0
    -> external-style shift exposes mismatch

    Cross-Gate Disagreement Analysis v0
    -> signal conflict regimes measured

    Cross-Gate Disagreement Stability v0
    -> conflict remains stable across populations

    Cross-Gate Real Dataset Proxy v0
    -> mild proxy dataset under-stressed

    Cross-Gate Real Dataset Proxy Stressed v0
    -> stronger disagreement achieved without confirmed collapse

    Cross-Gate Real Dataset Proxy Collapse v0
    -> arbitration COLLAPSE appears under multi-gate confirmed pressure

    Collapse Confirmation Stability v0
    -> collapse remains present, but confirmation-source identity is perturbation-sensitive

    Collapse Confirmation Source Swap v0
    -> collapse remains stable when confirmation source changes

    Temporal Collapse Degradation v0
    -> temporal degradation is measurable, but single-frame collapse requires confirmation

    Temporal Collapse Confirmation v0
    -> transient collapse is filtered, but persistence requires longer trajectories

    Temporal Collapse Persistence v0
    -> temporal collapse persistence is confirmed while transient collapse is filtered

    Temporal Collapse Persistence Stability v0
    -> persistence is stable under mild window variation, but scale-sensitive under stricter windows

    Temporal Collapse Phase Diagram v0
    -> temporal observability boundary is mapped across trajectory length, confirmation window, and persistence window

    Temporal Collapse Critical Horizon v0
    -> first critical horizon rule was off by one

    Temporal Collapse Critical Horizon Corrected v0
    -> corrected critical horizon rule matches all observable pairs

---

## Required Next Step

Recommended next experiment:

    examples/temporal_collapse_critical_horizon_extended_v0.py

Purpose:

    test the corrected critical horizon rule over longer trajectory lengths
    and stricter temporal windows

Main question:

    does the corrected horizon rule remain exact
    when all strict-window pairs become observable?

Recommended design:

    trajectory_length = 8, 10, 12, 14, 16, 18, 20
    confirmation_window = 2, 3, 4, 5, 6, 7, 8, 9, 10
    persistence_window = 2, 3, 4, 5, 6, 7, 8, 9, 10

Required checks:

    observable rate increases with maximum trajectory length
    exact corrected match rate remains 1.0
    mean corrected horizon error remains 0
    previously unobservable pairs become observable
    no contradiction appears in strict-window regimes

Expected output:

    extended critical horizon map
    exact-horizon validation across wider window space
    clearer critical temporal horizon law

---

## Final Result

    PASS — corrected critical temporal horizon matched the observability rule.

Correct final conclusion:

    persistent temporal collapse becomes observable exactly at the corrected critical horizon:
    first_raw_collapse + confirmation_window + persistence_window - 2.