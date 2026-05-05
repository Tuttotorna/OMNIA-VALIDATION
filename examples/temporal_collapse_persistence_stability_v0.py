import json
import os
from statistics import mean

VERSION = "0.1.0"

RESULTS_DIR = "results"

RESULTS_PATH = os.path.join(
    RESULTS_DIR,
    "temporal_collapse_persistence_stability_v0.json",
)


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
    severity = {
        "PASS": 0,
        "RETRY": 1,
        "FLAG": 2,
        "ESCALATE": 3,
        "COLLAPSE": 4,
    }

    return severity[action]


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


def generate_trajectories():
    trajectories = {}

    trajectories["stable_control"] = [
        build_state(60, 0.93, 0.88, 0.72, 0.96, 0.95),
        build_state(60, 0.92, 0.88, 0.72, 0.95, 0.94),
        build_state(60, 0.92, 0.87, 0.71, 0.95, 0.94),
        build_state(60, 0.91, 0.87, 0.71, 0.94, 0.93),
        build_state(60, 0.91, 0.86, 0.70, 0.94, 0.93),
        build_state(60, 0.90, 0.86, 0.70, 0.93, 0.92),
        build_state(60, 0.90, 0.85, 0.69, 0.92, 0.91),
        build_state(60, 0.89, 0.85, 0.69, 0.92, 0.91),
    ]

    persistent = [
        build_state(100, 0.88, 0.82, 0.70, 0.88, 0.86),
        build_state(100, 0.74, 0.70, 0.68, 0.76, 0.74),
        build_state(100, 0.58, 0.55, 0.63, 0.61, 0.58),
        build_state(100, 0.42, 0.38, 0.57, 0.43, 0.40),
        build_state(100, 0.26, 0.24, 0.50, 0.22, 0.18),
        build_state(100, 0.14, 0.13, 0.44, 0.08, 0.07),
        build_state(100, 0.10, 0.09, 0.40, 0.05, 0.05),
        build_state(100, 0.08, 0.07, 0.36, 0.04, 0.04),
    ]

    trajectories["persistent_collapse"] = persistent

    trajectories["instant_noise_spike"] = [
        build_state(75, 0.86, 0.82, 0.70, 0.88, 0.86),
        build_state(75, 0.18, 0.15, 0.42, 0.12, 0.10),
        build_state(75, 0.82, 0.78, 0.68, 0.84, 0.82),
        build_state(75, 0.80, 0.76, 0.67, 0.82, 0.80),
        build_state(75, 0.78, 0.74, 0.66, 0.80, 0.78),
        build_state(75, 0.76, 0.72, 0.65, 0.78, 0.76),
        build_state(75, 0.74, 0.70, 0.64, 0.76, 0.74),
        build_state(75, 0.72, 0.68, 0.63, 0.74, 0.72),
    ]

    trajectories["oscillating_nonpersistent"] = [
        build_state(95, 0.80, 0.76, 0.70, 0.82, 0.80),
        build_state(95, 0.34, 0.30, 0.58, 0.38, 0.35),
        build_state(95, 0.70, 0.66, 0.67, 0.72, 0.70),
        build_state(95, 0.28, 0.24, 0.55, 0.30, 0.28),
        build_state(95, 0.62, 0.58, 0.63, 0.64, 0.60),
        build_state(95, 0.12, 0.10, 0.42, 0.08, 0.07),
        build_state(95, 0.58, 0.54, 0.60, 0.58, 0.56),
        build_state(95, 0.56, 0.52, 0.58, 0.56, 0.54),
    ]

    return trajectories


def first_temporal_collapse(actions):
    for index, action in enumerate(actions):
        if action == "COLLAPSE":
            return index
    return None


def has_persistent_collapse(actions, persistence_window):
    for index in range(len(actions) - persistence_window + 1):
        window = actions[index:index + persistence_window]

        if all(action == "COLLAPSE" for action in window):
            return True

    return False


def evaluate_configuration(
    config_name,
    confirmation_window,
    persistence_window,
):
    trajectories = generate_trajectories()

    trajectory_results = []

    for name, states in trajectories.items():
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

        persistent = has_persistent_collapse(
            temporal_actions,
            persistence_window,
        )

        first_collapse = first_temporal_collapse(
            temporal_actions
        )

        trajectory_results.append({
            "trajectory_name": name,
            "raw_actions": raw_actions,
            "temporal_actions": temporal_actions,
            "persistent_collapse": persistent,
            "first_temporal_collapse": first_collapse,
        })

    stable_ok = next(
        item
        for item in trajectory_results
        if item["trajectory_name"] == "stable_control"
    )

    persistent_ok = next(
        item
        for item in trajectory_results
        if item["trajectory_name"] == "persistent_collapse"
    )

    spike_ok = next(
        item
        for item in trajectory_results
        if item["trajectory_name"] == "instant_noise_spike"
    )

    oscillating_ok = next(
        item
        for item in trajectory_results
        if item["trajectory_name"] == "oscillating_nonpersistent"
    )

    stable_pass = (
        "COLLAPSE"
        not in stable_ok["temporal_actions"]
    )

    persistent_confirmed = (
        persistent_ok["persistent_collapse"]
    )

    spike_filtered = (
        "COLLAPSE"
        not in spike_ok["temporal_actions"]
    )

    oscillating_filtered = (
        not oscillating_ok["persistent_collapse"]
    )

    status = (
        "PASS"
        if (
            stable_pass
            and persistent_confirmed
            and spike_filtered
            and oscillating_filtered
        )
        else "CHECK"
    )

    return {
        "config_name": config_name,
        "status": status,
        "confirmation_window": confirmation_window,
        "persistence_window": persistence_window,
        "stable_pass": stable_pass,
        "persistent_confirmed": persistent_confirmed,
        "spike_filtered": spike_filtered,
        "oscillating_filtered": oscillating_filtered,
        "persistent_delay": (
            persistent_ok["first_temporal_collapse"]
        ),
        "trajectory_results": trajectory_results,
    }


def main():
    os.makedirs(RESULTS_DIR, exist_ok=True)

    configurations = [
        ("cw2_pw2", 2, 2),
        ("cw2_pw3", 2, 3),
        ("cw3_pw2", 3, 2),
        ("cw3_pw3", 3, 3),
        ("cw4_pw2", 4, 2),
    ]

    config_results = []

    for name, cw, pw in configurations:
        config_results.append(
            evaluate_configuration(
                config_name=name,
                confirmation_window=cw,
                persistence_window=pw,
            )
        )

    pass_count = sum(
        1
        for item in config_results
        if item["status"] == "PASS"
    )

    check_count = len(config_results) - pass_count

    persistent_delays = [
        item["persistent_delay"]
        for item in config_results
        if item["persistent_delay"] is not None
    ]

    summary = {
        "configuration_count": len(configurations),
        "pass_configuration_count": pass_count,
        "check_configuration_count": check_count,
        "mean_persistent_delay": (
            mean(persistent_delays)
            if persistent_delays
            else None
        ),
    }

    status = (
        "PASS"
        if pass_count >= 4
        else "CHECK"
    )

    payload = {
        "status": status,
        "version": VERSION,
        "summary": summary,
        "configuration_results": config_results,
        "reproduction_command": (
            "python examples/"
            "temporal_collapse_persistence_stability_v0.py"
        ),
    }

    with open(
        RESULTS_PATH,
        "w",
        encoding="utf-8",
    ) as f:
        json.dump(payload, f, indent=2)

    print("=" * 80)
    print(
        "OMNIA-VALIDATION - "
        "Temporal Collapse Persistence Stability v0"
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
    print("Configuration summaries")
    print("-" * 80)

    for item in config_results:
        print(
            f"{item['config_name']:<12} "
            f"status={item['status']:<5} "
            f"cw={item['confirmation_window']} "
            f"pw={item['persistence_window']} "
            f"stable={item['stable_pass']} "
            f"persistent={item['persistent_confirmed']} "
            f"spike_filtered={item['spike_filtered']} "
            f"oscillation_filtered={item['oscillating_filtered']} "
            f"delay={item['persistent_delay']}"
        )

    print()
    print("=" * 80)
    print("FINAL CHECK")
    print("=" * 80)

    if status == "PASS":
        print(
            "PASS - temporal persistence remained stable "
            "under confirmation-window perturbation."
        )
    else:
        print(
            "CHECK - temporal persistence was unstable "
            "under confirmation-window perturbation."
        )

    print()
    print("=" * 80)
    print("Result saved to:", RESULTS_PATH)
    print("=" * 80)


if __name__ == "__main__":
    main()