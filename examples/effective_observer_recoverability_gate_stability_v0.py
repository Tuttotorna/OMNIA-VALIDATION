import json
import os
from statistics import mean

VERSION = "0.1.0"

RESULTS_DIR = "results"
RESULTS_PATH = os.path.join(
    RESULTS_DIR,
    "effective_observer_recoverability_gate_stability_v0.json",
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


def compute_adversarial_divergence(
    normalized_effective,
    recoverability_score,
):
    return abs(normalized_effective - recoverability_score)


def gate_action(
    normalized_effective,
    recoverability_score,
    projection_stability,
    collapse_resistance,
    family_balance,
    non_redundancy,
    adversarial_divergence,
    thresholds,
):
    collapse_threshold = thresholds["collapse_threshold"]
    divergence_escalate = thresholds["divergence_escalate"]
    divergence_flag = thresholds["divergence_flag"]
    recoverability_retry = thresholds["recoverability_retry"]
    family_flag = thresholds["family_flag"]
    non_redundancy_flag = thresholds["non_redundancy_flag"]
    normalized_effective_low = thresholds["normalized_effective_low"]

    if collapse_resistance < collapse_threshold:
        return "COLLAPSE"

    if projection_stability < collapse_threshold:
        return "COLLAPSE"

    if adversarial_divergence >= divergence_escalate:
        return "ESCALATE"

    if recoverability_score < recoverability_retry:
        return "RETRY"

    if family_balance < family_flag:
        return "FLAG"

    if non_redundancy < non_redundancy_flag:
        return "FLAG"

    if (
        normalized_effective < normalized_effective_low
        and recoverability_score >= 0.50
    ):
        return "FLAG"

    if adversarial_divergence >= divergence_flag:
        return "FLAG"

    return "PASS"


def build_case_parameters(case_name):
    if case_name == "clean_balanced":
        return {
            "raw": 40,
            "non_red": 0.95,
            "family": 0.95,
            "entropy": 0.55,
            "collapse": 0.90,
            "stability": 0.90,
        }

    if case_name == "high_raw_duplicate":
        return {
            "raw": 80,
            "non_red": 0.15,
            "family": 0.25,
            "entropy": 0.85,
            "collapse": 0.20,
            "stability": 0.30,
        }

    if case_name == "projection_collapse":
        return {
            "raw": 60,
            "non_red": 0.95,
            "family": 0.95,
            "entropy": 0.80,
            "collapse": 0.95,
            "stability": 0.05,
        }

    if case_name == "collapse_resistance_failure":
        return {
            "raw": 52,
            "non_red": 0.90,
            "family": 0.90,
            "entropy": 0.60,
            "collapse": 0.05,
            "stability": 0.75,
        }

    if case_name == "balanced_but_dependent":
        return {
            "raw": 50,
            "non_red": 0.35,
            "family": 1.00,
            "entropy": 0.45,
            "collapse": 0.25,
            "stability": 0.40,
        }

    if case_name == "sparse_but_independent":
        return {
            "raw": 8,
            "non_red": 1.00,
            "family": 0.80,
            "entropy": 0.20,
            "collapse": 0.90,
            "stability": 0.95,
        }

    if case_name == "entropy_inflation":
        return {
            "raw": 55,
            "non_red": 0.50,
            "family": 0.50,
            "entropy": 1.00,
            "collapse": 0.20,
            "stability": 0.25,
        }

    if case_name == "observer_alias_attack":
        return {
            "raw": 48,
            "non_red": 0.25,
            "family": 0.40,
            "entropy": 0.75,
            "collapse": 0.35,
            "stability": 0.30,
        }

    if case_name == "partial_collapse":
        return {
            "raw": 45,
            "non_red": 0.60,
            "family": 0.70,
            "entropy": 0.55,
            "collapse": 0.15,
            "stability": 0.20,
        }

    if case_name == "hidden_single_point_failure":
        return {
            "raw": 52,
            "non_red": 0.90,
            "family": 0.90,
            "entropy": 0.60,
            "collapse": 0.05,
            "stability": 0.10,
        }

    raise ValueError(f"unknown case: {case_name}")


def evaluate_case(case_name, thresholds):
    params = build_case_parameters(case_name)

    raw = params["raw"]
    non_red = params["non_red"]
    family = params["family"]
    entropy = params["entropy"]
    collapse = params["collapse"]
    stability = params["stability"]

    effective_count = compute_effective_count(
        raw_count=raw,
        non_redundancy=non_red,
        family_balance=family,
        relation_entropy=entropy,
        collapse_resistance=collapse,
        projection_stability=stability,
    )

    normalized_effective = safe_div(effective_count, raw)

    recoverability_score = compute_recoverability_score(
        non_redundancy=non_red,
        family_balance=family,
        relation_entropy=entropy,
        collapse_resistance=collapse,
        projection_stability=stability,
    )

    adversarial_divergence = compute_adversarial_divergence(
        normalized_effective=normalized_effective,
        recoverability_score=recoverability_score,
    )

    action = gate_action(
        normalized_effective=normalized_effective,
        recoverability_score=recoverability_score,
        projection_stability=stability,
        collapse_resistance=collapse,
        family_balance=family,
        non_redundancy=non_red,
        adversarial_divergence=adversarial_divergence,
        thresholds=thresholds,
    )

    return {
        "case": case_name,
        "raw_count": raw,
        "effective_count": effective_count,
        "normalized_effective": normalized_effective,
        "recoverability_score": recoverability_score,
        "projection_stability": stability,
        "collapse_resistance": collapse,
        "family_balance": family,
        "non_redundancy": non_red,
        "relation_entropy": entropy,
        "adversarial_divergence": adversarial_divergence,
        "gate_action": action,
    }


def evaluate_config(config_name, thresholds):
    cases = [
        "clean_balanced",
        "high_raw_duplicate",
        "projection_collapse",
        "collapse_resistance_failure",
        "balanced_but_dependent",
        "sparse_but_independent",
        "entropy_inflation",
        "observer_alias_attack",
        "partial_collapse",
        "hidden_single_point_failure",
    ]

    results = [
        evaluate_case(case_name=case, thresholds=thresholds)
        for case in cases
    ]

    action_counts = {}

    for item in results:
        action = item["gate_action"]
        action_counts[action] = action_counts.get(action, 0) + 1

    pass_count = action_counts.get("PASS", 0)

    flagged_count = sum(
        1
        for item in results
        if item["gate_action"]
        in {"FLAG", "RETRY", "ESCALATE", "COLLAPSE"}
    )

    collapse_count = action_counts.get("COLLAPSE", 0)

    critical_cases = {
        "projection_collapse",
        "collapse_resistance_failure",
        "hidden_single_point_failure",
    }

    critical_collapse_count = sum(
        1
        for item in results
        if item["case"] in critical_cases
        and item["gate_action"] == "COLLAPSE"
    )

    clean_action = next(
        item["gate_action"]
        for item in results
        if item["case"] == "clean_balanced"
    )

    clean_pass = clean_action == "PASS"

    divergence_values = [
        item["adversarial_divergence"]
        for item in results
    ]

    config_pass = (
        clean_pass
        and critical_collapse_count == 3
        and flagged_count >= 8
        and pass_count >= 1
    )

    return {
        "config_name": config_name,
        "thresholds": thresholds,
        "status": "PASS" if config_pass else "CHECK",
        "summary": {
            "case_count": len(results),
            "pass_count": pass_count,
            "flagged_count": flagged_count,
            "collapse_count": collapse_count,
            "critical_collapse_count": critical_collapse_count,
            "clean_balanced_action": clean_action,
            "mean_adversarial_divergence": mean(divergence_values),
            "max_adversarial_divergence": max(divergence_values),
        },
        "results": results,
    }


def build_threshold_configs():
    base = {
        "collapse_threshold": 0.10,
        "divergence_escalate": 0.60,
        "divergence_flag": 0.35,
        "recoverability_retry": 0.30,
        "family_flag": 0.35,
        "non_redundancy_flag": 0.35,
        "normalized_effective_low": 0.05,
    }

    configs = [
        ("base_thresholds", base),
        (
            "tighter_divergence_threshold",
            {
                **base,
                "divergence_flag": 0.32,
                "divergence_escalate": 0.56,
            },
        ),
        (
            "looser_divergence_threshold",
            {
                **base,
                "divergence_flag": 0.40,
                "divergence_escalate": 0.65,
            },
        ),
        (
            "tighter_collapse_threshold",
            {
                **base,
                "collapse_threshold": 0.12,
            },
        ),
        (
            "looser_collapse_threshold",
            {
                **base,
                "collapse_threshold": 0.08,
            },
        ),
        (
            "tighter_balance_thresholds",
            {
                **base,
                "family_flag": 0.40,
                "non_redundancy_flag": 0.40,
            },
        ),
        (
            "looser_balance_thresholds",
            {
                **base,
                "family_flag": 0.30,
                "non_redundancy_flag": 0.30,
            },
        ),
        (
            "combined_threshold_shift",
            {
                **base,
                "collapse_threshold": 0.09,
                "divergence_flag": 0.38,
                "divergence_escalate": 0.63,
                "recoverability_retry": 0.28,
                "family_flag": 0.32,
                "non_redundancy_flag": 0.32,
                "normalized_effective_low": 0.06,
            },
        ),
    ]

    return configs


def compare_to_base(base_run, run):
    base_actions = {
        item["case"]: item["gate_action"]
        for item in base_run["results"]
    }

    run_actions = {
        item["case"]: item["gate_action"]
        for item in run["results"]
    }

    shared_cases = sorted(set(base_actions) & set(run_actions))

    same_count = sum(
        1
        for case in shared_cases
        if base_actions[case] == run_actions[case]
    )

    action_persistence = safe_div(same_count, len(shared_cases))

    changed_cases = [
        {
            "case": case,
            "base_action": base_actions[case],
            "current_action": run_actions[case],
        }
        for case in shared_cases
        if base_actions[case] != run_actions[case]
    ]

    return {
        "config_name": run["config_name"],
        "shared_case_count": len(shared_cases),
        "action_persistence": action_persistence,
        "changed_case_count": len(changed_cases),
        "changed_cases": changed_cases,
    }


def main():
    os.makedirs(RESULTS_DIR, exist_ok=True)

    configs = build_threshold_configs()

    runs = [
        evaluate_config(config_name=name, thresholds=thresholds)
        for name, thresholds in configs
    ]

    base_run = runs[0]

    comparisons = [
        compare_to_base(base_run, run)
        for run in runs[1:]
    ]

    pass_config_count = sum(
        1
        for run in runs
        if run["status"] == "PASS"
    )

    check_config_count = len(runs) - pass_config_count

    action_persistence_values = [
        item["action_persistence"]
        for item in comparisons
    ]

    clean_pass_count = sum(
        1
        for run in runs
        if run["summary"]["clean_balanced_action"] == "PASS"
    )

    critical_collapse_full_count = sum(
        1
        for run in runs
        if run["summary"]["critical_collapse_count"] == 3
    )

    summary = {
        "config_count": len(runs),
        "pass_config_count": pass_config_count,
        "check_config_count": check_config_count,
        "clean_pass_count": clean_pass_count,
        "critical_collapse_full_count": critical_collapse_full_count,
        "mean_action_persistence": mean(action_persistence_values),
        "min_action_persistence": min(action_persistence_values),
        "max_action_persistence": max(action_persistence_values),
    }

    status = (
        "PASS"
        if pass_config_count >= 6
        and clean_pass_count >= 6
        and critical_collapse_full_count >= 6
        and summary["min_action_persistence"] >= 0.80
        else "CHECK"
    )

    payload = {
        "status": status,
        "version": VERSION,
        "summary": summary,
        "runs": runs,
        "comparisons_to_base": comparisons,
        "reproduction_command": (
            "python examples/"
            "effective_observer_recoverability_gate_stability_v0.py"
        ),
    }

    with open(RESULTS_PATH, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2)

    print("=" * 80)
    print(
        "OMNIA-VALIDATION - "
        "Effective Observer Recoverability Gate Stability v0"
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
    print("Runs")
    print("-" * 80)

    for run in runs:
        s = run["summary"]
        print(
            f"{run['config_name']:<32} "
            f"status={run['status']:<5} "
            f"pass={s['pass_count']} "
            f"flagged={s['flagged_count']} "
            f"collapse={s['collapse_count']} "
            f"critical_collapse={s['critical_collapse_count']} "
            f"clean={s['clean_balanced_action']}"
        )

    print()
    print("Comparisons to base")
    print("-" * 80)

    for item in comparisons:
        print(
            f"{item['config_name']:<32} "
            f"persistence={item['action_persistence']:.12f} "
            f"changed={item['changed_case_count']}"
        )

    print()
    print("=" * 80)
    print("FINAL CHECK")
    print("=" * 80)

    if status == "PASS":
        print(
            "PASS - recoverability gate remained stable under threshold perturbation."
        )
    else:
        print(
            "CHECK - recoverability gate showed threshold fragility."
        )

    print()
    print("=" * 80)
    print("Result saved to:", RESULTS_PATH)
    print("=" * 80)


if __name__ == "__main__":
    main()