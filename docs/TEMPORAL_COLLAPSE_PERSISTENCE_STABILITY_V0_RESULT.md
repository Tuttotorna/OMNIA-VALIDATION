# Temporal Collapse Persistence Stability v0 — Result

## Status

Status: CHECK  
Version: 0.1.0  
Claim level: Level 2 — Temporal Persistence Window Stability

---

## Purpose

This experiment tests whether temporal collapse persistence remains stable under different confirmation and persistence window settings.

The previous experiment confirmed that temporal persistence works with:

    confirmation_window = 2
    persistence_window = 2

This experiment perturbs those temporal windows.

Core question:

    does temporal collapse persistence survive window variation?

Core boundary:

    measurement != arbitration != decision

This experiment does not evaluate semantic truth.

It evaluates sensitivity of temporal persistence to observation-window parameters.

---

## Experiment File

    examples/temporal_collapse_persistence_stability_v0.py

Result file:

    results/temporal_collapse_persistence_stability_v0.json

Reproduction command:

    python examples/temporal_collapse_persistence_stability_v0.py

---

## Summary Result

    Status: CHECK
    Version: 0.1.0

    configuration_count = 5
    pass_configuration_count = 3
    check_configuration_count = 2
    mean_persistent_delay = 5.8

The result is CHECK.

Temporal persistence remained stable under mild window variation, but not under stricter confirmation and persistence settings.

---

## Configuration Results

### cw2_pw2

Status: PASS

    confirmation_window = 2
    persistence_window = 2
    stable_pass = True
    persistent_confirmed = True
    spike_filtered = True
    oscillating_filtered = True
    persistent_delay = 5

This is the baseline configuration.

It confirms the previous result:

    transient collapse is filtered
    persistent collapse is preserved

---

### cw2_pw3

Status: PASS

    confirmation_window = 2
    persistence_window = 3
    stable_pass = True
    persistent_confirmed = True
    spike_filtered = True
    oscillating_filtered = True
    persistent_delay = 5

Increasing the persistence window from 2 to 3 does not break the result when confirmation remains fast.

This shows that mild persistence strictness is tolerated.

---

### cw3_pw2

Status: PASS

    confirmation_window = 3
    persistence_window = 2
    stable_pass = True
    persistent_confirmed = True
    spike_filtered = True
    oscillating_filtered = True
    persistent_delay = 6

Increasing the confirmation window from 2 to 3 delays collapse detection.

The result still passes.

This shows that moderate confirmation strictness is tolerated.

---

### cw3_pw3

Status: CHECK

    confirmation_window = 3
    persistence_window = 3
    stable_pass = True
    persistent_confirmed = False
    spike_filtered = True
    oscillating_filtered = True
    persistent_delay = 6

This configuration filters transient collapse correctly.

It also keeps stable and oscillating trajectories safe.

But it fails to confirm persistence.

Interpretation:

    the trajectory is too short
    for both confirmation_window = 3
    and persistence_window = 3

The system does not panic.

It simply lacks enough post-confirmation time to prove persistence.

---

### cw4_pw2

Status: CHECK

    confirmation_window = 4
    persistence_window = 2
    stable_pass = True
    persistent_confirmed = False
    spike_filtered = True
    oscillating_filtered = True
    persistent_delay = 7

This configuration also filters transient collapse correctly.

But confirmation is too delayed.

Temporal collapse appears too late to prove persistent collapse inside an 8-state trajectory.

This is not random failure.

It is temporal-horizon sensitivity.

---

## Main Finding

The main finding is:

    temporal collapse persistence is scale-sensitive

The experiment shows that persistence survives mild temporal-window perturbation:

    cw2_pw2 = PASS
    cw2_pw3 = PASS
    cw3_pw2 = PASS

but fails under stricter windows:

    cw3_pw3 = CHECK
    cw4_pw2 = CHECK

This means collapse persistence depends on the relation between:

    confirmation window
    persistence window
    trajectory length
    post-collapse duration

---

## Important Structural Pattern

The result pattern is coherent:

    cw2_pw2 -> PASS
    cw2_pw3 -> PASS
    cw3_pw2 -> PASS
    cw3_pw3 -> CHECK
    cw4_pw2 -> CHECK

This is not noisy behavior.

It shows a threshold-like transition.

As confirmation and persistence windows become stricter, persistence becomes harder to observe inside the fixed trajectory length.

---

## Persistent Delay

    mean_persistent_delay = 5.8

Persistent delay increases as confirmation becomes stricter.

Observed delays:

    cw2_pw2 -> 5
    cw2_pw3 -> 5
    cw3_pw2 -> 6
    cw3_pw3 -> 6
    cw4_pw2 -> 7

This confirms the expected temporal behavior:

    larger confirmation windows delay collapse observability

The stricter the temporal rule, the later persistence can be detected.

---

## Why The Result Is CHECK

The result is CHECK because only 3 out of 5 configurations passed.

    pass_configuration_count = 3
    check_configuration_count = 2

The failing configurations did not fail because of false collapse.

They failed because persistent collapse was not confirmed within the available trajectory length.

Critical point:

    stable_pass = True
    spike_filtered = True
    oscillating_filtered = True

for all configurations.

So the safety properties remained stable.

The instability appears only in persistence confirmation under stricter windows.

---

## What Remained Stable

Across all configurations:

    stable control remained safe
    instant spike remained filtered
    oscillating nonpersistent trajectory remained nonpersistent

This is important.

The temporal filter did not become unsafe under window perturbation.

It became more conservative.

---

## What Became Unstable

The unstable property was:

    persistent_confirmed

Specifically:

    cw3_pw3 -> persistent_confirmed = False
    cw4_pw2 -> persistent_confirmed = False

This means the system became too strict relative to the trajectory length.

The collapse regime may exist, but the experiment window is too short to prove it.

---

## Relation To OMNIATEMPO

This experiment directly supports the OMNIATEMPO direction.

It shows that temporal collapse is not only a state.

It is also dependent on observation scale.

The measured result implies:

    collapse visibility depends on temporal resolution

and:

    persistence depends on the chosen observation window

This is a temporal-structure result, not a static gate result.

---

## Relation To TDelta

This experiment relates naturally to TDelta as structural divergence time.

The important measured behavior is:

    persistence detection moves later as confirmation windows grow

This introduces a practical temporal quantity:

    detection delay

The larger the confirmation window, the later collapse can be confirmed.

In simplified form:

    TDelta is affected by confirmation scale

This does not yet measure full TDelta.

But it begins to expose a critical temporal horizon:

    how much time is needed to observe persistent structural collapse?

---

## Interpretation

The correct interpretation is not:

    temporal persistence failed

The correct interpretation is:

    temporal persistence has a detectable scale boundary

The experiment exposed a boundary where the observation window is too short for the requested confirmation strength.

This is a useful CHECK.

It tells us the temporal layer is conservative under stricter windows.

---

## What This Confirms

This experiment supports:

    temporal persistence is measurable
    temporal persistence is window-sensitive
    mild window variation preserves persistence
    stricter window variation delays detection
    transient collapse remains filtered
    stable control remains safe
    oscillating instability remains nonpersistent
    persistence confirmation requires enough post-collapse time

---

## What This Does Not Prove

This experiment does not prove:

    universal temporal persistence stability
    optimal confirmation-window choice
    optimal persistence-window choice
    real-world temporal validity
    semantic correctness
    causal correctness
    full OMNIATEMPO correctness
    full OMNIA correctness

It exposes controlled temporal-window sensitivity.

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

    stability of temporal collapse persistence under window perturbation

---

## Limitations

    Only 5 temporal configurations were tested.
    Only one trajectory set was used.
    Each trajectory has 8 states.
    The trajectories are synthetic.
    Larger windows require longer trajectories.
    No external temporal dataset was used.
    No semantic ground truth exists.
    The persistence rule is hand-defined.

---

## Result Classification

Recommended classification:

    CHECK

Evidence level:

    Level 2 — Temporal Persistence Window Stability

Reason:

    5 configurations tested
    3 configurations passed
    2 configurations checked
    transient spike remained filtered
    stable control remained safe
    oscillating instability remained nonpersistent
    persistence failed only under stricter windows
    mean persistent delay was measured

This is not a failure.

It is a boundary diagnosis.

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

---

## Required Next Step

Recommended next experiment:

    examples/temporal_collapse_phase_diagram_v0.py

Purpose:

    map the temporal phase boundary across confirmation and persistence windows

Main question:

    for which (confirmation_window, persistence_window) pairs
    does persistent collapse remain observable?

Required design:

    test a grid of confirmation_window values
    test a grid of persistence_window values
    extend trajectories to 10 or 12 states
    measure PASS/CHECK regions
    measure persistent delay
    measure filtered spike preservation
    measure oscillation safety

Expected output:

    temporal phase diagram

or, in simple file form:

    table of window pairs
    pass/check status
    delay
    persistent_confirmed
    spike_filtered
    oscillating_filtered

---

## Final Result

    CHECK — temporal persistence was unstable under confirmation-window perturbation.

More precise conclusion:

    temporal persistence remained safe,
    but persistence confirmation is scale-sensitive under stricter temporal windows.