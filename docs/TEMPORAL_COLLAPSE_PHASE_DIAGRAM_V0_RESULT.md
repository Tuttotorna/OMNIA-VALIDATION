# Temporal Collapse Phase Diagram v0 — Result

## Status

Status: CHECK  
Version: 0.1.0  
Claim level: Level 2 — Temporal Observability Phase Diagram

---

## Purpose

This experiment maps the observability boundary of persistent temporal collapse.

Previous experiments showed that temporal collapse persistence is measurable, but also sensitive to confirmation and persistence windows.

This experiment expands the test into a grid:

    trajectory_length = 8, 10, 12
    confirmation_window = 2, 3, 4, 5, 6
    persistence_window = 2, 3, 4, 5, 6

Core question:

    for which temporal-window settings
    does persistent collapse remain observable?

Core boundary:

    measurement != arbitration != decision

This experiment does not evaluate semantic truth.

It evaluates temporal observability of persistent structural collapse.

---

## Experiment File

    examples/temporal_collapse_phase_diagram_v0.py

Result file:

    results/temporal_collapse_phase_diagram_v0.json

Reproduction command:

    python examples/temporal_collapse_phase_diagram_v0.py

---

## Summary Result

    Status: CHECK
    Version: 0.1.0

    trajectory_lengths = [8, 10, 12]
    confirmation_windows = [2, 3, 4, 5, 6]
    persistence_windows = [2, 3, 4, 5, 6]

    total_cell_count = 75

    pass_cell_count = 32
    check_cell_count = 43

    pass_rate = 0.426666666667

    safe_cell_count = 75
    safety_rate = 1.0

    persistent_confirmed_count = 32
    persistent_confirmed_rate = 0.426666666667

    mean_first_persistent_collapse = 8.5625

The result is CHECK.

The important result is not failure.

The important result is that the experiment produced a temporal phase boundary.

Safety remained stable in every tested cell.

Persistence observability depended on trajectory length and temporal-window scale.

---

## Main Finding

The main finding is:

    safety is stable
    persistence observability is scale-sensitive

Every tested cell preserved safety:

    safety_rate = 1.0

But persistence was confirmed only in part of the grid:

    persistent_confirmed_rate = 0.426666666667

This means the system does not become unsafe when temporal windows become stricter.

It becomes more conservative.

---

## Phase Space

The tested phase space is:

    L  = trajectory length
    cw = confirmation window
    pw = persistence window

The full grid contains:

    3 trajectory lengths
    5 confirmation windows
    5 persistence windows

Therefore:

    3 * 5 * 5 = 75 phase cells

Each phase cell checks:

    stable control remains safe
    instant spike remains filtered
    oscillating trajectory remains nonpersistent
    persistent collapse remains observable

---

## Global Phase Result

    total_cell_count = 75
    pass_cell_count = 32
    check_cell_count = 43
    pass_rate = 0.426666666667

This means 32 cells preserved both safety and persistent-collapse observability.

43 cells preserved safety but did not confirm persistent collapse.

Correct interpretation:

    CHECK cells are not unsafe cells

They are cells where persistent collapse was not observable under the selected temporal scale.

---

## Safety Result

    safe_cell_count = 75
    safety_rate = 1.0

This is the strongest result in the experiment.

Across all tested combinations:

    stable control stayed safe
    transient spike stayed filtered
    oscillating instability stayed nonpersistent

So the temporal layer remained safe across the full grid.

The instability appeared only in observability of persistence.

---

## Persistence Observability Result

    persistent_confirmed_count = 32
    persistent_confirmed_rate = 0.426666666667

Persistent collapse was confirmed in 32 of 75 cells.

This shows that persistent collapse is not universally observable for every window configuration.

It depends on whether the observation horizon is long enough relative to:

    confirmation_window
    persistence_window
    collapse onset
    trajectory length

---

## By Trajectory Length

### L = 8

    cell_count = 25
    pass_count = 3
    check_count = 22
    pass_rate = 0.12
    mean_first_persistent_collapse = 6.666666666667

At length 8, persistence is observable only under very small windows.

This confirms that short trajectories do not contain enough post-collapse time for stricter temporal confirmation.

---

### L = 10

    cell_count = 25
    pass_count = 10
    check_count = 15
    pass_rate = 0.4
    mean_first_persistent_collapse = 8

At length 10, the PASS region expands.

More temporal evidence is available, so more window combinations can confirm persistence.

---

### L = 12

    cell_count = 25
    pass_count = 19
    check_count = 6
    pass_rate = 0.76
    mean_first_persistent_collapse = 9.157894736842104

At length 12, most cells pass.

This confirms a key temporal result:

    longer observation horizons make persistent collapse more observable

---

## Trajectory-Length Trend

The pass rate increases with trajectory length:

    L = 8  -> pass_rate = 0.12
    L = 10 -> pass_rate = 0.40
    L = 12 -> pass_rate = 0.76

This is the clearest phase-boundary behavior in the experiment.

The trend is monotonic.

Longer trajectories expose more persistent-collapse evidence.

---

## By Confirmation Window

### cw2

    cell_count = 15
    pass_count = 11
    check_count = 4
    pass_rate = 0.733333333333

A confirmation window of 2 is permissive enough to observe persistence in most settings.

---

### cw3

    cell_count = 15
    pass_count = 9
    check_count = 6
    pass_rate = 0.6

A confirmation window of 3 still preserves a large PASS region.

---

### cw4

    cell_count = 15
    pass_count = 6
    check_count = 9
    pass_rate = 0.4

At cw4, persistence observability becomes significantly harder.

---

### cw5

    cell_count = 15
    pass_count = 4
    check_count = 11
    pass_rate = 0.266666666667

At cw5, most cells no longer confirm persistence.

The temporal layer becomes highly conservative.

---

### cw6

    cell_count = 15
    pass_count = 2
    check_count = 13
    pass_rate = 0.133333333333

At cw6, persistence is observable only under the longest and least demanding persistence settings.

---

## Confirmation-Window Trend

The pass rate decreases as confirmation window increases:

    cw2 -> pass_rate = 0.733333333333
    cw3 -> pass_rate = 0.6
    cw4 -> pass_rate = 0.4
    cw5 -> pass_rate = 0.266666666667
    cw6 -> pass_rate = 0.133333333333

This is a coherent monotonic trend.

The stricter the confirmation window, the harder it becomes to observe persistent collapse inside a finite trajectory.

---

## Phase Boundary

The experiment exposes a phase boundary.

A simplified rule appears:

    persistent collapse is observable
    when trajectory length is large enough
    relative to confirmation_window + persistence_window

A stricter temporal rule needs a longer observation horizon.

This is the key structural result.

---

## Critical Temporal Horizon

This experiment introduces a practical idea:

    critical temporal horizon

That means:

    the minimum observation length required
    to confirm persistent collapse
    under a given pair of temporal windows

For example:

    short horizon + strict windows -> CHECK
    longer horizon + same windows -> PASS

This is exactly what appears across L = 8, L = 10, and L = 12.

---

## Safety Versus Observability

This experiment separates two different properties:

    safety
    observability

Safety remained stable:

    safety_rate = 1.0

Observability was partial:

    pass_rate = 0.426666666667

This is a strong distinction.

The temporal layer does not hallucinate collapse under stricter windows.

It withholds confirmation when evidence is temporally insufficient.

---

## Why The Result Is CHECK

The global status is CHECK because:

    pass_rate = 0.426666666667

The experiment required at least 0.50 pass rate for global PASS.

It did not reach that threshold.

But the CHECK is informative.

It shows a structured boundary, not random instability.

---

## What The CHECK Means

The CHECK means:

    temporal persistence is not universally observable
    across all tested temporal windows and trajectory lengths

It does not mean:

    the temporal layer failed
    the safety logic failed
    transient collapse was accepted
    oscillating instability became collapse

All tested cells remained safe.

The CHECK isolates observability limits.

---

## Phase Cells — Compact Reading

The compact pattern is:

    L = 8:
      only small cw/pw pairs pass

    L = 10:
      middle region begins to pass

    L = 12:
      most of the lower and middle grid passes

This is exactly the expected behavior if temporal persistence depends on observation horizon.

---

## Important Positive Result

The strongest positive result is:

    safe_cell_count = 75
    safety_rate = 1.0

This means the temporal filter remained stable across the full phase grid.

No tested configuration converted stable control, transient spike, or oscillating instability into persistent collapse.

---

## Important Boundary Result

The strongest boundary result is:

    pass_rate increases with trajectory length

and:

    pass_rate decreases with confirmation-window length

This shows that persistence confirmation is not a static binary.

It is a temporal observability property.

---

## Relation To OMNIATEMPO

This experiment directly supports the OMNIATEMPO direction.

It shows that structural collapse has temporal regimes.

The same underlying collapse sequence can be:

    observable

or:

    not observable

depending on the temporal lens.

This matches the idea that temporal structure is not merely a timestamp.

It is part of the measurement.

---

## Relation To TDelta

This experiment gives early operational support to a TDelta-like concept.

The measured quantities:

    first_temporal_collapse
    first_persistent_collapse
    mean_first_persistent_collapse

are simplified proxies for structural divergence timing.

The phase boundary shows:

    divergence detection depends on observation scale

This is not full TDelta yet.

But it is the correct experimental direction.

---

## What This Confirms

This experiment supports:

    temporal phase behavior is measurable
    persistent collapse observability depends on temporal horizon
    longer trajectories expose more persistence
    stricter confirmation windows reduce observability
    safety remains stable under all tested window pairs
    transient collapse remains filtered
    oscillating instability remains nonpersistent
    persistent collapse has a critical observability boundary

---

## What This Does Not Prove

This experiment does not prove:

    universal temporal phase behavior
    optimal temporal-window parameters
    real-world temporal reliability
    semantic correctness
    causal correctness
    full TDelta
    full OMNIATEMPO correctness
    full OMNIA correctness

It maps a controlled synthetic temporal phase diagram.

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

    temporal observability of persistent structural collapse

---

## Limitations

    The trajectories are synthetic.
    Only 3 trajectory lengths were tested.
    Only 5 confirmation windows were tested.
    Only 5 persistence windows were tested.
    The persistent trajectory pattern is hand-defined.
    The temporal rule is hand-defined.
    No external temporal dataset was used.
    No semantic ground truth exists.

---

## Result Classification

Recommended classification:

    CHECK

Evidence level:

    Level 2 — Temporal Observability Phase Diagram

Reason:

    75 phase cells tested
    full safety across all cells
    32 persistent-confirmed cells
    43 non-confirmed cells
    monotonic trajectory-length effect
    monotonic confirmation-window effect
    phase boundary observed
    critical temporal horizon exposed

This is not a failed result.

It is a boundary map.

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

---

## Required Next Step

Recommended next experiment:

    examples/temporal_collapse_phase_diagram_extended_v0.py

Purpose:

    extend the phase diagram to longer trajectories and larger window ranges

Main question:

    does the PASS region expand predictably
    as trajectory length increases?

Recommended design:

    trajectory_length = 8, 10, 12, 14, 16
    confirmation_window = 2, 3, 4, 5, 6, 7, 8
    persistence_window = 2, 3, 4, 5, 6, 7, 8

Required checks:

    safety remains 1.0
    pass rate increases with trajectory length
    pass rate decreases with confirmation window
    pass rate decreases with persistence window
    critical temporal horizon can be estimated
    phase boundary remains coherent

Expected output:

    larger temporal phase diagram
    critical horizon estimate
    pass/check boundary by temporal scale

---

## Final Result

    CHECK — temporal phase diagram did not expose enough stable observability.

More precise conclusion:

    safety remained stable across all phase cells,
    while persistent collapse observability formed a scale-dependent phase boundary.