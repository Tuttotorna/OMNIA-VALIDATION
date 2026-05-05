import json
import os
from statistics import mean

VERSION = "0.1.0"

RESULTS_DIR = "results"

RESULTS_PATH = os.path.join(
    RESULTS_DIR,
    "temporal_collapse_critical_horizon_corrected_v0.json",
)

CONFIRMATION_WINDOWS = [2, 3, 4, 5, 6, 7, 8]
PERSISTENCE_WINDOWS = [2, 3, 4, 5, 6, 7, 8]
TRAJECTORY_LENGTHS = [8, 10, 12, 14, 16]

RAW_COLLAPSE_ONSET_REFERENCE = 4


def clamp(x, lo=0.0, hi=1.0):
    return max(lo, min(hi, x))


def safe_div(a, b):
    if b == 0:
        return 0.0
    return a / b


def compute_effective_count(
    raw_count,
    non_redundancy,
    family_balance,
    relation_entropy,
    collapse_resistance,
    projection_stability,
):
    return max(
        0.0,
        raw_count
        * non_redundancy
        * family_balance
        * (0.5 + 0.5 * relation_entropy)
        * collapse_resistance
        * projection_stability,
    )


def compute_recoverability_score(
    non_redundancy,
    family_balance,
    relation_entropy,
    collapse_resistance,
    projection_stability,
):
    return clamp(
        0.25 * non_redundancy
        + 0.20 * family_balance
        + 0.15 * relation_entropy
        + 0.20 * collapse_resistance
        + 0.20 * projection_stability
    )


def compute_divergence(normalized_effective, recoverability_score):
    return abs(normalized_effective - recoverability_score)


def effective_signal_gate(normalized_effective):
    if normalized_effective >= 0.45:
        return "PASS"
    if normalized_effective >= 0.20:
        return "FLAG"
    if normalized_effective >= 0.05:
        return "RETRY"
    return "COLLAPSE"


def recoverability_gate(recoverability_score):
    if recoverability_score >= 0.72:
        return "PASS"
    if recoverability_score >= 0.45:
        return "FLAG"
    if recoverability_score >= 0.30:
        return "RETRY"
    return "COLLAPSE"


def divergence_gate(divergence):
    if divergence >= 0.60:
        return "ESCALATE"
    if divergence >= 0.35:
        return "FLAG"
    if divergence >= 0.20:
        return "RETRY"
    return "PASS"


def collapse_gate(collapse_resistance):
    if collapse_resistance < 0.10:
        return "COLLAPSE"
    if collapse_resistance < 0.20:
        return "FLAG"
    if collapse_resistance < 0.45:
        return "RETRY"
    return "PASS"


def projection_gate(projection_stability):
    if projection_stability < 0.10:
        return "COLLAPSE"
    if projection_stability < 0.20:
        return "FLAG"
    if projection_stability < 0.45:
        return "RETRY"
    return "PASS"


def action_severity(action):
    return {
        "PASS": 0,
        "RETRY": 1,
        "FLAG": 2,
        "ESCALATE": 3,
        "COLLAPSE": 4,
    }[action]


def severity_to_action(severity_value):
    if severity_value >= 3.50:
        return "COLLAPSE"
    if severity_value >= 2.50:
        return "ESCALATE"
    if severity_value >= 1.50:
        return "FLAG"
    if severity_value >= 0.50:
        return "RETRY"
    return "PASS"


def structural_arbitration(signal_actions):
    severities = [
        action_severity(action)
        for action in signal_actions.values()
    ]

    max_severity = max(severities)
    min_severity = min(severities)
    mean_severity = mean(severities)
    spread = max_severity - min_severity

    collapse_votes = sum(
        1
        for action in signal_actions.values()
        if action == "COLLAPSE"
    )

    escalate_votes = sum(
        1
        for action in signal_actions.values()
        if action == "ESCALATE"
    )

    pass_votes = sum(
        1
        for action in signal_actions.values()
        if action == "PASS"
    )

    if collapse_votes >= 2:
        return "COLLAPSE"

    if collapse_votes == 1 and spread >= 3:
        return "ESCALATE"

    if escalate_votes >= 1 and spread >= 2:
        return "ESCALATE"

    if spread >= 3:
        return "ESCALATE"

    if pass_votes >= 3 and max_severity <= 2:
        return "PASS"

    return severity_to_action(mean_severity)


def temporal_confirmation_action(
    raw_action,
    previous_raw_actions,
    confirmation_window,
):
    if raw_action != "COLLAPSE":
        return raw_action

    recent = previous_raw_actions[-(confirmation_window - 1):]
    confirmed = recent + [raw_action]

    if len(confirmed) < confirmation_window:
        return "ESCALATE"

    if all(action == "COLLAPSE" for action in confirmed):
        return "COLLAPSE"

    return "ESCALATE"


def build_state(
    raw_count,
    non_redundancy,
    family_balance,
    relation_entropy,
    collapse_resistance,
    projection_stability,
):
    return {
        "raw_count": raw_count,
        "non_redundancy": clamp(non_redundancy),
        "family_balance": clamp(family_balance),
        "relation_entropy": clamp(relation_entropy),
        "collapse_resistance": clamp(collapse_resistance),
        "projection_stability": clamp(projection_stability),
    }


def evaluate_state(
    state,
    previous_raw_actions,
    confirmation_window,
):
    raw_count = state["raw_count"]

    effective_count = compute_effective_count(
        raw_count=raw_count,
        non_redundancy=state["non_redundancy"],
        family_balance=state["family_balance"],
        relation_entropy=state["relation_entropy"],
        collapse_resistance=state["collapse_resistance"],
        projection_stability=state["projection_stability"],
    )

    normalized_effective = safe_div(
        effective_count,
        raw_count,
    )

    recoverability_score = compute_recoverability_score(
        non_redundancy=state["non_redundancy"],
        family_balance=state["family_balance"],
        relation_entropy=state["relation_entropy"],
        collapse_resistance=state["collapse_resistance"],
        projection_stability=state["projection_stability"],
    )

    divergence = compute_divergence(
        normalized_effective=normalized_effective,
        recoverability_score=recoverability_score,
    )

    signal_actions = {
        "effective_signal_gate": effective_signal_gate(
            normalized_effective
        ),
        "recoverability_gate": recoverability_gate(
            recoverability_score
        ),
        "divergence_gate": divergence_gate(divergence),
        "collapse_gate": collapse_gate(
            state["collapse_resistance"]
        ),
        "projection_gate": projection_gate(
            state["projection_stability"]
        ),
    }

    raw_action = structural_arbitration(signal_actions)

    temporal_action = temporal_confirmation_action(
        raw_action=raw_action,
        previous_raw_actions=previous_raw_actions,
        confirmation_window=confirmation_window,
    )

    return {
        "raw_action": raw_action,
        "temporal_action": temporal_action,
    }


def generate_persistent_seed_trajectory():
    return [
        build_state(100, 0.88, 0.82, 0.70, 0.88, 0.86),
        build_state(100, 0.74, 0.70, 0.68, 0.76, 0.74),
        build_state(100, 0.58, 0.55, 0.63, 0.61, 0.58),
        build_state(100, 0.42, 0.38, 0.57, 0.43, 0.40),
        build_state(100, 0.26, 0.24, 0.50, 0.22, 0.18),
        build_state(100, 0.14, 0.13, 0.44, 0.08, 0.07),
        build_state(100, 0.10, 0.09, 0.40, 0.05, 0.05),
        build_state(100, 0.08, 0.07, 0.36, 0.04, 0.04),
    ]


def extend_sequence(seed_states, target_length):
    if len(seed_states) > target_length:
        return seed_states[:target_length]

    if len(seed_states) == target_length:
        return list(seed_states)

    states = list(seed_states)
    last = states[-1]

    while len(states) < target_length:
        degraded = build_state(
            raw_count=last["raw_count"],
            non_redundancy=last["non_redundancy"] * 0.92,
            family_balance=last["family_balance"] * 0.92,
            relation_entropy=last["relation_entropy"] * 0.94,
            collapse_resistance=last["collapse_resistance"] * 0.80,
            projection_stability=last["projection_stability"] * 0.80,
        )

        states.append(degraded)
        last = degraded

    return states


def first_index(actions, target):
    for index, action in enumerate(actions):
        if action == target:
            return index

    return None


def first_persistent_index(actions, persistence_window):
    for index in range(len(actions) - persistence_window + 1):
        window = actions[index:index + persistence_window]

        if all(action == "COLLAPSE" for action in window):
            return index + persistence_window - 1

    return None


def evaluate_persistent_trajectory(
    trajectory_length,
    confirmation_window,
    persistence_window,
):
    seed = generate_persistent_seed_trajectory()
    states = extend_sequence(seed, trajectory_length)

    previous_raw_actions = []
    raw_actions = []
    temporal_actions = []

    for state in states:
        result = evaluate_state(
            state=state,
            previous_raw_actions=previous_raw_actions,
            confirmation_window=confirmation_window,
        )

        raw_actions.append(result["raw_action"])
        temporal_actions.append(result["temporal_action"])

        previous_raw_actions.append(result["raw_action"])

    first_raw_collapse = first_index(
        raw_actions,
        "COLLAPSE",
    )

    first_temporal_collapse = first_index(
        temporal_actions,
        "COLLAPSE",
    )

    first_persistent_collapse = first_persistent_index(
        temporal_actions,
        persistence_window,
    )

    corrected_expected_horizon = (
        first_raw_collapse
        + confirmation_window
        + persistence_window
        - 2
        if first_raw_collapse is not None
        else None
    )

    corrected_horizon_error = (
        first_persistent_collapse - corrected_expected_horizon
        if first_persistent_collapse is not None
        and corrected_expected_horizon is not None
        else None
    )

    return {
        "trajectory_length": trajectory_length,
        "confirmation_window": confirmation_window,
        "persistence_window": persistence_window,
        "first_raw_collapse": first_raw_collapse,
        "first_temporal_collapse": first_temporal_collapse,
        "first_persistent_collapse": first_persistent_collapse,
        "corrected_expected_horizon": corrected_expected_horizon,
        "corrected_horizon_error": corrected_horizon_error,
        "persistent_confirmed": first_persistent_collapse is not None,
        "raw_action_sequence": raw_actions,
        "temporal_action_sequence": temporal_actions,
    }


def estimate_critical_horizon(
    confirmation_window,
    persistence_window,
):
    observations = [
        evaluate_persistent_trajectory(
            trajectory_length=trajectory_length,
            confirmation_window=confirmation_window,
            persistence_window=persistence_window,
        )
        for trajectory_length in TRAJECTORY_LENGTHS
    ]

    confirmed = [
        item
        for item in observations
        if item["persistent_confirmed"]
    ]

    minimum_observed_length = (
        min(item["trajectory_length"] for item in confirmed)
        if confirmed
        else None
    )

    corrected_expected_horizons = [
        item["corrected_expected_horizon"]
        for item in observations
        if item["corrected_expected_horizon"] is not None
    ]

    corrected_expected_horizon = (
        corrected_expected_horizons[0]
        if corrected_expected_horizons
        else None
    )

    corrected_horizon_errors = [
        item["corrected_horizon_error"]
        for item in confirmed
        if item["corrected_horizon_error"] is not None
    ]

    mean_corrected_horizon_error = (
        mean(corrected_horizon_errors)
        if corrected_horizon_errors
        else None
    )

    exact_corrected_match = (
        mean_corrected_horizon_error == 0
        if mean_corrected_horizon_error is not None
        else False
    )

    return {
        "confirmation_window": confirmation_window,
        "persistence_window": persistence_window,
        "minimum_observed_length": minimum_observed_length,
        "corrected_expected_horizon": corrected_expected_horizon,
        "observable": minimum_observed_length is not None,
        "mean_corrected_horizon_error": mean_corrected_horizon_error,
        "exact_corrected_match": exact_corrected_match,
        "observations": observations,
    }


def main():
    os.makedirs(RESULTS_DIR, exist_ok=True)

    horizon_results = []

    for confirmation_window in CONFIRMATION_WINDOWS:
        for persistence_window in PERSISTENCE_WINDOWS:
            horizon_results.append(
                estimate_critical_horizon(
                    confirmation_window=confirmation_window,
                    persistence_window=persistence_window,
                )
            )

    observable_results = [
        item
        for item in horizon_results
        if item["observable"]
    ]

    unobservable_results = [
        item
        for item in horizon_results
        if not item["observable"]
    ]

    corrected_errors = [
        item["mean_corrected_horizon_error"]
        for item in observable_results
        if item["mean_corrected_horizon_error"] is not None
    ]

    exact_corrected_match_count = sum(
        1
        for item in observable_results
        if item["exact_corrected_match"]
    )

    minimum_lengths = [
        item["minimum_observed_length"]
        for item in observable_results
        if item["minimum_observed_length"] is not None
    ]

    summary = {
        "confirmation_windows": CONFIRMATION_WINDOWS,
        "persistence_windows": PERSISTENCE_WINDOWS,
        "trajectory_lengths": TRAJECTORY_LENGTHS,
        "pair_count": len(horizon_results),
        "observable_pair_count": len(observable_results),
        "unobservable_pair_count": len(unobservable_results),
        "observable_rate": safe_div(
            len(observable_results),
            len(horizon_results),
        ),
        "exact_corrected_match_count": exact_corrected_match_count,
        "exact_corrected_match_rate": safe_div(
            exact_corrected_match_count,
            len(observable_results),
        ),
        "mean_corrected_horizon_error": (
            mean(corrected_errors)
            if corrected_errors
            else None
        ),
        "mean_minimum_observed_length": (
            mean(minimum_lengths)
            if minimum_lengths
            else None
        ),
        "raw_collapse_onset_reference": (
            RAW_COLLAPSE_ONSET_REFERENCE
        ),
        "corrected_estimated_rule": (
            "critical_horizon = "
            "first_raw_collapse + "
            "confirmation_window + "
            "persistence_window - 2"
        ),
    }

    status = (
        "PASS"
        if (
            summary["observable_rate"] >= 0.50
            and summary["exact_corrected_match_rate"] >= 0.90
            and summary["mean_corrected_horizon_error"] == 0
        )
        else "CHECK"
    )

    payload = {
        "status": status,
        "version": VERSION,
        "summary": summary,
        "horizon_results": horizon_results,
        "reproduction_command": (
            "python examples/"
            "temporal_collapse_critical_horizon_corrected_v0.py"
        ),
    }

    with open(RESULTS_PATH, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2)

    print("=" * 80)
    print(
        "OMNIA-VALIDATION - "
        "Temporal Collapse Critical Horizon Corrected v0"
    )
    print("=" * 80)
    print()

    print("Status:", status)
    print("Version:", VERSION)

    print()
    print("Summary")
    print("-" * 80)

    for key, value in summary.items():
        print(f"{key}: {value}")

    print()
    print("Critical horizon estimates")
    print("-" * 80)

    for item in horizon_results:
        print(
            f"cw={item['confirmation_window']} "
            f"pw={item['persistence_window']} "
            f"observable={item['observable']} "
            f"min_length={item['minimum_observed_length']} "
            f"corrected_expected={item['corrected_expected_horizon']} "
            f"mean_corrected_error={item['mean_corrected_horizon_error']}"
        )

    print()
    print("=" * 80)
    print("FINAL CHECK")
    print("=" * 80)

    if status == "PASS":
        print(
            "PASS - corrected critical temporal horizon matched "
            "the observability rule."
        )
    else:
        print(
            "CHECK - corrected critical temporal horizon did not "
            "fully match the observability rule."
        )

    print()
    print("=" * 80)
    print("Result saved to:", RESULTS_PATH)
    print("=" * 80)


if __name__ == "__main__":
    main()