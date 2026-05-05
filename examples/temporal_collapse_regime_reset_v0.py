import json
import os
from statistics import mean

VERSION = "0.1.0"

RESULTS_DIR = "results"

RESULTS_PATH = os.path.join(
    RESULTS_DIR,
    "temporal_collapse_regime_reset_v0.json",
)

CONFIRMATION_WINDOW = 2
PERSISTENCE_WINDOW = 2
RESET_WINDOW = 2
TRAJECTORY_LENGTH = 16


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


def evaluate_state(state, previous_raw_actions):
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
        normalized_effective,
        recoverability_score,
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
        confirmation_window=CONFIRMATION_WINDOW,
    )

    return {
        "raw_action": raw_action,
        "temporal_action": temporal_action,
        "signal_actions": signal_actions,
    }


def stable_state():
    return build_state(100, 0.88, 0.82, 0.70, 0.88, 0.86)


def warning_state():
    return build_state(100, 0.42, 0.38, 0.57, 0.43, 0.40)


def collapse_state():
    return build_state(100, 0.14, 0.13, 0.44, 0.08, 0.07)


def hard_collapse_state():
    return build_state(100, 0.08, 0.07, 0.36, 0.04, 0.04)


def recovery_state():
    return build_state(100, 0.74, 0.70, 0.68, 0.76, 0.74)


def partial_recovery_state():
    return build_state(100, 0.58, 0.55, 0.63, 0.61, 0.58)


def generate_trajectories():
    trajectories = {}

    trajectories["clean_monotonic"] = [
        stable_state(),
        recovery_state(),
        partial_recovery_state(),
        warning_state(),
        collapse_state(),
        hard_collapse_state(),
        hard_collapse_state(),
        hard_collapse_state(),
        hard_collapse_state(),
        hard_collapse_state(),
        hard_collapse_state(),
        hard_collapse_state(),
        hard_collapse_state(),
        hard_collapse_state(),
        hard_collapse_state(),
        hard_collapse_state(),
    ]

    trajectories["drifting_onset"] = [
        stable_state(),
        recovery_state(),
        recovery_state(),
        partial_recovery_state(),
        warning_state(),
        warning_state(),
        collapse_state(),
        hard_collapse_state(),
        hard_collapse_state(),
        hard_collapse_state(),
        hard_collapse_state(),
        hard_collapse_state(),
        hard_collapse_state(),
        hard_collapse_state(),
        hard_collapse_state(),
        hard_collapse_state(),
    ]

    trajectories["instant_spike_recovery"] = [
        stable_state(),
        collapse_state(),
        stable_state(),
        recovery_state(),
        stable_state(),
        recovery_state(),
        stable_state(),
        recovery_state(),
        stable_state(),
        recovery_state(),
        stable_state(),
        recovery_state(),
        stable_state(),
        recovery_state(),
        stable_state(),
        recovery_state(),
    ]

    trajectories["oscillating_collapse"] = [
        stable_state(),
        warning_state(),
        collapse_state(),
        recovery_state(),
        collapse_state(),
        recovery_state(),
        collapse_state(),
        recovery_state(),
        collapse_state(),
        recovery_state(),
        collapse_state(),
        recovery_state(),
        collapse_state(),
        recovery_state(),
        collapse_state(),
        recovery_state(),
    ]

    trajectories["recovery_then_relapse"] = [
        stable_state(),
        warning_state(),
        collapse_state(),
        hard_collapse_state(),
        recovery_state(),
        partial_recovery_state(),
        recovery_state(),
        warning_state(),
        collapse_state(),
        hard_collapse_state(),
        hard_collapse_state(),
        hard_collapse_state(),
        hard_collapse_state(),
        hard_collapse_state(),
        hard_collapse_state(),
        hard_collapse_state(),
    ]

    trajectories["fragmented_persistence"] = [
        stable_state(),
        warning_state(),
        collapse_state(),
        hard_collapse_state(),
        recovery_state(),
        collapse_state(),
        hard_collapse_state(),
        recovery_state(),
        collapse_state(),
        hard_collapse_state(),
        recovery_state(),
        collapse_state(),
        hard_collapse_state(),
        recovery_state(),
        collapse_state(),
        hard_collapse_state(),
    ]

    trajectories["dual_regime_collapse"] = [
        stable_state(),
        recovery_state(),
        warning_state(),
        collapse_state(),
        hard_collapse_state(),
        hard_collapse_state(),
        recovery_state(),
        recovery_state(),
        warning_state(),
        collapse_state(),
        hard_collapse_state(),
        hard_collapse_state(),
        hard_collapse_state(),
        hard_collapse_state(),
        hard_collapse_state(),
        hard_collapse_state(),
    ]

    trajectories["delayed_secondary_collapse"] = [
        stable_state(),
        recovery_state(),
        warning_state(),
        collapse_state(),
        recovery_state(),
        recovery_state(),
        recovery_state(),
        warning_state(),
        warning_state(),
        collapse_state(),
        hard_collapse_state(),
        hard_collapse_state(),
        hard_collapse_state(),
        hard_collapse_state(),
        hard_collapse_state(),
        hard_collapse_state(),
    ]

    return trajectories


def find_runs(actions, target):
    runs = []
    start = None

    for index, action in enumerate(actions):
        if action == target and start is None:
            start = index

        if action != target and start is not None:
            runs.append(
                {
                    "start": start,
                    "end": index - 1,
                    "length": index - start,
                }
            )
            start = None

    if start is not None:
        runs.append(
            {
                "start": start,
                "end": len(actions) - 1,
                "length": len(actions) - start,
            }
        )

    return runs


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


def has_recovery_window_between(actions, start, end, reset_window):
    if start is None or end is None:
        return False

    if end <= start:
        return False

    gap = actions[start:end]

    non_collapse_run = 0

    for action in gap:
        if action != "COLLAPSE":
            non_collapse_run += 1
        else:
            non_collapse_run = 0

        if non_collapse_run >= reset_window:
            return True

    return False


def find_valid_regime_starts(raw_actions):
    raw_collapse_runs = find_runs(raw_actions, "COLLAPSE")

    valid_runs = [
        run
        for run in raw_collapse_runs
        if run["length"] >= CONFIRMATION_WINDOW
    ]

    regime_starts = []

    for run in valid_runs:
        candidate_start = run["start"]

        if not regime_starts:
            regime_starts.append(candidate_start)
            continue

        previous_start = regime_starts[-1]

        recovered = has_recovery_window_between(
            actions=raw_actions,
            start=previous_start,
            end=candidate_start,
            reset_window=RESET_WINDOW,
        )

        if recovered:
            regime_starts.append(candidate_start)

    return {
        "raw_collapse_runs": raw_collapse_runs,
        "valid_runs": valid_runs,
        "regime_starts": regime_starts,
    }


def predict_dynamic_horizons(regime_starts):
    return [
        start
        + CONFIRMATION_WINDOW
        + PERSISTENCE_WINDOW
        - 2
        for start in regime_starts
    ]


def first_dynamic_horizon_that_matches(
    predicted_horizons,
    observed_persistent,
):
    if observed_persistent is None:
        return None

    for horizon in predicted_horizons:
        if horizon == observed_persistent:
            return horizon

    return None


def evaluate_trajectory(name, states):
    previous_raw_actions = []
    raw_actions = []
    temporal_actions = []
    state_results = []

    for step, state in enumerate(states):
        result = evaluate_state(
            state=state,
            previous_raw_actions=previous_raw_actions,
        )

        raw_actions.append(result["raw_action"])
        temporal_actions.append(result["temporal_action"])
        previous_raw_actions.append(result["raw_action"])

        state_results.append(
            {
                "step": step,
                "raw_action": result["raw_action"],
                "temporal_action": result["temporal_action"],
                "signal_actions": result["signal_actions"],
            }
        )

    regime_data = find_valid_regime_starts(raw_actions)

    predicted_horizons = predict_dynamic_horizons(
        regime_data["regime_starts"]
    )

    observed_persistent = first_persistent_index(
        temporal_actions,
        PERSISTENCE_WINDOW,
    )

    matched_horizon = first_dynamic_horizon_that_matches(
        predicted_horizons,
        observed_persistent,
    )

    dynamic_horizon_error = (
        observed_persistent - matched_horizon
        if observed_persistent is not None
        and matched_horizon is not None
        else None
    )

    temporal_collapse_runs = find_runs(
        temporal_actions,
        "COLLAPSE",
    )

    persistence_reset_count = max(
        0,
        len(temporal_collapse_runs) - 1,
    )

    horizon_fragmentation = len(regime_data["regime_starts"])

    raw_first_collapse = first_index(raw_actions, "COLLAPSE")
    temporal_first_collapse = first_index(
        temporal_actions,
        "COLLAPSE",
    )

    status = "PASS"

    if name in {
        "instant_spike_recovery",
        "oscillating_collapse",
    }:
        if observed_persistent is not None:
            status = "CHECK"

    elif name == "fragmented_persistence":
        if observed_persistent is not None:
            status = "CHECK"

        if horizon_fragmentation < 2:
            status = "CHECK"

    else:
        if observed_persistent is None:
            status = "CHECK"

        if matched_horizon is None:
            status = "CHECK"

        if dynamic_horizon_error != 0:
            status = "CHECK"

    return {
        "trajectory_name": name,
        "status": status,
        "raw_first_collapse": raw_first_collapse,
        "temporal_first_collapse": temporal_first_collapse,
        "observed_persistent": observed_persistent,
        "matched_dynamic_horizon": matched_horizon,
        "dynamic_horizon_error": dynamic_horizon_error,
        "raw_collapse_runs": regime_data["raw_collapse_runs"],
        "valid_raw_runs": regime_data["valid_runs"],
        "regime_starts": regime_data["regime_starts"],
        "predicted_dynamic_horizons": predicted_horizons,
        "horizon_fragmentation": horizon_fragmentation,
        "persistence_reset_count": persistence_reset_count,
        "raw_action_sequence": raw_actions,
        "temporal_action_sequence": temporal_actions,
        "states": state_results,
    }


def main():
    os.makedirs(RESULTS_DIR, exist_ok=True)

    trajectories = generate_trajectories()

    trajectory_results = [
        evaluate_trajectory(name, states)
        for name, states in trajectories.items()
    ]

    pass_trajectory_count = sum(
        1
        for item in trajectory_results
        if item["status"] == "PASS"
    )

    check_trajectory_count = (
        len(trajectory_results) - pass_trajectory_count
    )

    observable_results = [
        item
        for item in trajectory_results
        if item["observed_persistent"] is not None
    ]

    error_values = [
        item["dynamic_horizon_error"]
        for item in trajectory_results
        if item["dynamic_horizon_error"] is not None
    ]

    reset_counts = [
        item["persistence_reset_count"]
        for item in trajectory_results
    ]

    fragmentation_counts = [
        item["horizon_fragmentation"]
        for item in trajectory_results
    ]

    summary = {
        "trajectory_count": len(trajectory_results),
        "trajectory_length": TRAJECTORY_LENGTH,
        "confirmation_window": CONFIRMATION_WINDOW,
        "persistence_window": PERSISTENCE_WINDOW,
        "reset_window": RESET_WINDOW,
        "pass_trajectory_count": pass_trajectory_count,
        "check_trajectory_count": check_trajectory_count,
        "observable_persistence_count": len(observable_results),
        "mean_dynamic_horizon_error": (
            mean(error_values)
            if error_values
            else None
        ),
        "max_abs_dynamic_horizon_error": (
            max(abs(value) for value in error_values)
            if error_values
            else None
        ),
        "mean_persistence_reset_count": mean(reset_counts),
        "max_persistence_reset_count": max(reset_counts),
        "mean_horizon_fragmentation": mean(fragmentation_counts),
        "max_horizon_fragmentation": max(fragmentation_counts),
        "dynamic_rule": (
            "dynamic_critical_horizon = "
            "valid_regime_start + "
            "confirmation_window + "
            "persistence_window - 2"
        ),
        "reset_rule": (
            "a regime is reset when raw_action is not COLLAPSE "
            "for reset_window consecutive frames before persistence"
        ),
        "tested_dynamic_families": [
            "clean_monotonic",
            "drifting_onset",
            "instant_spike_recovery",
            "oscillating_collapse",
            "recovery_then_relapse",
            "fragmented_persistence",
            "dual_regime_collapse",
            "delayed_secondary_collapse",
        ],
    }

    status = (
        "PASS"
        if (
            pass_trajectory_count == len(trajectory_results)
            and summary["mean_dynamic_horizon_error"] == 0
            and summary["max_abs_dynamic_horizon_error"] == 0
            and summary["max_horizon_fragmentation"] >= 2
        )
        else "CHECK"
    )

    payload = {
        "status": status,
        "version": VERSION,
        "summary": summary,
        "trajectory_results": trajectory_results,
        "reproduction_command": (
            "python examples/temporal_collapse_regime_reset_v0.py"
        ),
    }

    with open(RESULTS_PATH, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2)

    print("=" * 80)
    print("OMNIA-VALIDATION - Temporal Collapse Regime Reset v0")
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
    print("Trajectory summaries")
    print("-" * 80)

    for item in trajectory_results:
        print(
            f"{item['trajectory_name']:<30} "
            f"status={item['status']:<5} "
            f"raw_first={item['raw_first_collapse']} "
            f"temporal_first={item['temporal_first_collapse']} "
            f"observed={item['observed_persistent']} "
            f"matched={item['matched_dynamic_horizon']} "
            f"error={item['dynamic_horizon_error']} "
            f"regimes={item['regime_starts']} "
            f"horizons={item['predicted_dynamic_horizons']} "
            f"fragments={item['horizon_fragmentation']} "
            f"resets={item['persistence_reset_count']} "
            f"raw={' -> '.join(item['raw_action_sequence'])} "
            f"temporal={' -> '.join(item['temporal_action_sequence'])}"
        )

    print()
    print("=" * 80)
    print("FINAL CHECK")
    print("=" * 80)

    if status == "PASS":
        print(
            "PASS - reset-aware dynamic horizon restored "
            "predictability under regime changes."
        )
    else:
        print(
            "CHECK - reset-aware dynamic horizon did not fully "
            "restore predictability."
        )

    print()
    print("=" * 80)
    print("Result saved to:", RESULTS_PATH)
    print("=" * 80)


if __name__ == "__main__":
    main()