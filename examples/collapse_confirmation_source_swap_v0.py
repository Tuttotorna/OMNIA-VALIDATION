import csv
import json
import math
import os
from statistics import mean

VERSION = "0.1.0"

DATA_DIR = "data"
RESULTS_DIR = "results"

DATA_PATH = os.path.join(
    DATA_DIR,
    "collapse_confirmation_source_swap_v0.csv",
)

RESULTS_PATH = os.path.join(
    RESULTS_DIR,
    "collapse_confirmation_source_swap_v0.json",
)


def clamp(x, lo=0.0, hi=1.0):
    return max(lo, min(hi, x))


def safe_div(a, b):
    if b == 0:
        return 0.0
    return a / b


def entropy_from_values(values):
    total = sum(values)

    if total <= 0:
        return 0.0

    entropy = 0.0

    for value in values:
        if value <= 0:
            continue

        p = value / total
        entropy -= p * math.log(p)

    max_entropy = math.log(len(values)) if len(values) > 1 else 1.0

    return clamp(safe_div(entropy, max_entropy))


def write_default_dataset():
    os.makedirs(DATA_DIR, exist_ok=True)

    rows = [
        {
            "record_id": "clean_control_reference",
            "source_family": "control",
            "raw_count": 48,
            "duplicate_count": 2,
            "family_count": 8,
            "dominant_family_count": 8,
            "signal_a": 0.84,
            "signal_b": 0.82,
            "signal_c": 0.80,
            "failure_count": 0,
            "instability_count": 2,
            "projection_loss": 0.04,
        },
        {
            "record_id": "isolated_effective_collapse",
            "source_family": "effective_only",
            "raw_count": 140,
            "duplicate_count": 121,
            "family_count": 3,
            "dominant_family_count": 118,
            "signal_a": 0.72,
            "signal_b": 0.70,
            "signal_c": 0.68,
            "failure_count": 3,
            "instability_count": 7,
            "projection_loss": 0.08,
        },
        {
            "record_id": "projection_strong_resistance_weak",
            "source_family": "projection_swap",
            "raw_count": 88,
            "duplicate_count": 24,
            "family_count": 5,
            "dominant_family_count": 54,
            "signal_a": 0.61,
            "signal_b": 0.59,
            "signal_c": 0.57,
            "failure_count": 17,
            "instability_count": 46,
            "projection_loss": 0.93,
        },
        {
            "record_id": "projection_weak_resistance_strong",
            "source_family": "resistance_swap",
            "raw_count": 110,
            "duplicate_count": 33,
            "family_count": 4,
            "dominant_family_count": 74,
            "signal_a": 0.55,
            "signal_b": 0.52,
            "signal_c": 0.50,
            "failure_count": 93,
            "instability_count": 106,
            "projection_loss": 0.34,
        },
        {
            "record_id": "projection_flag_resistance_collapse",
            "source_family": "resistance_swap",
            "raw_count": 104,
            "duplicate_count": 39,
            "family_count": 4,
            "dominant_family_count": 70,
            "signal_a": 0.63,
            "signal_b": 0.60,
            "signal_c": 0.58,
            "failure_count": 87,
            "instability_count": 101,
            "projection_loss": 0.83,
        },
        {
            "record_id": "projection_collapse_resistance_flag",
            "source_family": "projection_swap",
            "raw_count": 102,
            "duplicate_count": 22,
            "family_count": 5,
            "dominant_family_count": 61,
            "signal_a": 0.91,
            "signal_b": 0.42,
            "signal_c": 0.86,
            "failure_count": 76,
            "instability_count": 90,
            "projection_loss": 0.94,
        },
        {
            "record_id": "recoverability_weak_projection_strong",
            "source_family": "recoverability_swap",
            "raw_count": 130,
            "duplicate_count": 101,
            "family_count": 4,
            "dominant_family_count": 107,
            "signal_a": 0.88,
            "signal_b": 0.86,
            "signal_c": 0.83,
            "failure_count": 64,
            "instability_count": 89,
            "projection_loss": 0.86,
        },
        {
            "record_id": "recoverability_weak_resistance_strong",
            "source_family": "recoverability_swap",
            "raw_count": 96,
            "duplicate_count": 75,
            "family_count": 3,
            "dominant_family_count": 83,
            "signal_a": 0.46,
            "signal_b": 0.44,
            "signal_c": 0.43,
            "failure_count": 83,
            "instability_count": 92,
            "projection_loss": 0.38,
        },
        {
            "record_id": "divergence_dominant_projection_weak",
            "source_family": "divergence_swap",
            "raw_count": 76,
            "duplicate_count": 6,
            "family_count": 7,
            "dominant_family_count": 18,
            "signal_a": 0.99,
            "signal_b": 0.04,
            "signal_c": 0.96,
            "failure_count": 2,
            "instability_count": 7,
            "projection_loss": 0.94,
        },
        {
            "record_id": "divergence_dominant_resistance_weak",
            "source_family": "divergence_swap",
            "raw_count": 95,
            "duplicate_count": 8,
            "family_count": 8,
            "dominant_family_count": 19,
            "signal_a": 0.99,
            "signal_b": 0.05,
            "signal_c": 0.96,
            "failure_count": 88,
            "instability_count": 94,
            "projection_loss": 0.12,
        },
        {
            "record_id": "triple_confirmed_collapse",
            "source_family": "triple_confirmed",
            "raw_count": 100,
            "duplicate_count": 61,
            "family_count": 3,
            "dominant_family_count": 82,
            "signal_a": 0.34,
            "signal_b": 0.31,
            "signal_c": 0.29,
            "failure_count": 89,
            "instability_count": 98,
            "projection_loss": 0.93,
        },
        {
            "record_id": "quad_confirmed_collapse",
            "source_family": "triple_confirmed",
            "raw_count": 70,
            "duplicate_count": 63,
            "family_count": 2,
            "dominant_family_count": 66,
            "signal_a": 0.12,
            "signal_b": 0.10,
            "signal_c": 0.09,
            "failure_count": 68,
            "instability_count": 70,
            "projection_loss": 0.97,
        },
        {
            "record_id": "resistance_relief_projection_takeover",
            "source_family": "source_swap",
            "raw_count": 90,
            "duplicate_count": 33,
            "family_count": 5,
            "dominant_family_count": 54,
            "signal_a": 0.74,
            "signal_b": 0.72,
            "signal_c": 0.70,
            "failure_count": 26,
            "instability_count": 41,
            "projection_loss": 0.95,
        },
        {
            "record_id": "projection_relief_resistance_takeover",
            "source_family": "source_swap",
            "raw_count": 112,
            "duplicate_count": 37,
            "family_count": 4,
            "dominant_family_count": 73,
            "signal_a": 0.57,
            "signal_b": 0.55,
            "signal_c": 0.53,
            "failure_count": 97,
            "instability_count": 108,
            "projection_loss": 0.28,
        },
        {
            "record_id": "ambiguous_should_escalate",
            "source_family": "ambiguous",
            "raw_count": 84,
            "duplicate_count": 46,
            "family_count": 4,
            "dominant_family_count": 54,
            "signal_a": 0.58,
            "signal_b": 0.57,
            "signal_c": 0.56,
            "failure_count": 31,
            "instability_count": 54,
            "projection_loss": 0.46,
        },
        {
            "record_id": "partial_collapse_recoverable",
            "source_family": "ambiguous",
            "raw_count": 91,
            "duplicate_count": 25,
            "family_count": 5,
            "dominant_family_count": 49,
            "signal_a": 0.73,
            "signal_b": 0.71,
            "signal_c": 0.68,
            "failure_count": 43,
            "instability_count": 59,
            "projection_loss": 0.36,
        },
    ]

    fieldnames = [
        "record_id",
        "source_family",
        "raw_count",
        "duplicate_count",
        "family_count",
        "dominant_family_count",
        "signal_a",
        "signal_b",
        "signal_c",
        "failure_count",
        "instability_count",
        "projection_loss",
    ]

    with open(DATA_PATH, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def read_dataset():
    write_default_dataset()

    rows = []

    with open(DATA_PATH, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)

        for row in reader:
            rows.append(
                {
                    "record_id": row["record_id"],
                    "source_family": row["source_family"],
                    "raw_count": int(row["raw_count"]),
                    "duplicate_count": int(row["duplicate_count"]),
                    "family_count": int(row["family_count"]),
                    "dominant_family_count": int(row["dominant_family_count"]),
                    "signal_a": float(row["signal_a"]),
                    "signal_b": float(row["signal_b"]),
                    "signal_c": float(row["signal_c"]),
                    "failure_count": int(row["failure_count"]),
                    "instability_count": int(row["instability_count"]),
                    "projection_loss": float(row["projection_loss"]),
                }
            )

    return rows


def derive_features(row):
    raw_count = row["raw_count"]

    duplicate_ratio = clamp(safe_div(row["duplicate_count"], raw_count))
    non_redundancy = clamp(1.0 - duplicate_ratio)

    family_balance = clamp(
        1.0 - safe_div(row["dominant_family_count"], raw_count)
    )

    relation_entropy = entropy_from_values(
        [
            row["signal_a"],
            row["signal_b"],
            row["signal_c"],
        ]
    )

    failure_ratio = clamp(safe_div(row["failure_count"], raw_count))
    instability_ratio = clamp(safe_div(row["instability_count"], raw_count))

    collapse_resistance = clamp(
        1.0
        - 0.55 * failure_ratio
        - 0.45 * instability_ratio
    )

    projection_stability = clamp(1.0 - row["projection_loss"])

    return {
        "raw_count": raw_count,
        "non_redundancy": non_redundancy,
        "family_balance": family_balance,
        "relation_entropy": relation_entropy,
        "collapse_resistance": collapse_resistance,
        "projection_stability": projection_stability,
        "failure_ratio": failure_ratio,
        "instability_ratio": instability_ratio,
        "duplicate_ratio": duplicate_ratio,
    }


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


def compute_divergence(
    normalized_effective,
    recoverability_score,
):
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
        1 for action in signal_actions.values()
        if action == "COLLAPSE"
    )

    escalate_votes = sum(
        1 for action in signal_actions.values()
        if action == "ESCALATE"
    )

    pass_votes = sum(
        1 for action in signal_actions.values()
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


def compute_disagreement(signal_actions):
    severities = [
        action_severity(action)
        for action in signal_actions.values()
    ]

    unique_actions = len(set(signal_actions.values()))
    spread = max(severities) - min(severities)
    mean_severity = mean(severities)

    variance = mean(
        (value - mean_severity) ** 2
        for value in severities
    )

    return {
        "unique_action_count": unique_actions,
        "severity_spread": spread,
        "severity_variance": variance,
        "mean_severity": mean_severity,
    }


def evaluate_record(row):
    features = derive_features(row)

    effective_count = compute_effective_count(
        raw_count=features["raw_count"],
        non_redundancy=features["non_redundancy"],
        family_balance=features["family_balance"],
        relation_entropy=features["relation_entropy"],
        collapse_resistance=features["collapse_resistance"],
        projection_stability=features["projection_stability"],
    )

    normalized_effective = safe_div(
        effective_count,
        features["raw_count"],
    )

    recoverability_score = compute_recoverability_score(
        non_redundancy=features["non_redundancy"],
        family_balance=features["family_balance"],
        relation_entropy=features["relation_entropy"],
        collapse_resistance=features["collapse_resistance"],
        projection_stability=features["projection_stability"],
    )

    divergence = compute_divergence(
        normalized_effective=normalized_effective,
        recoverability_score=recoverability_score,
    )

    signal_actions = {
        "effective_signal_gate": effective_signal_gate(normalized_effective),
        "recoverability_gate": recoverability_gate(recoverability_score),
        "divergence_gate": divergence_gate(divergence),
        "collapse_gate": collapse_gate(
            features["collapse_resistance"],
        ),
        "projection_gate": projection_gate(
            features["projection_stability"],
        ),
    }

    disagreement = compute_disagreement(signal_actions)
    arbitration_action = structural_arbitration(signal_actions)

    collapse_sources = [
        key
        for key, value in signal_actions.items()
        if value == "COLLAPSE"
    ]

    return {
        "record_id": row["record_id"],
        "source_family": row["source_family"],
        "raw_count": features["raw_count"],
        "effective_count": effective_count,
        "normalized_effective": normalized_effective,
        "recoverability_score": recoverability_score,
        "divergence": divergence,
        "non_redundancy": features["non_redundancy"],
        "family_balance": features["family_balance"],
        "relation_entropy": features["relation_entropy"],
        "collapse_resistance": features["collapse_resistance"],
        "projection_stability": features["projection_stability"],
        "failure_ratio": features["failure_ratio"],
        "instability_ratio": features["instability_ratio"],
        "duplicate_ratio": features["duplicate_ratio"],
        "signal_actions": signal_actions,
        "collapse_sources": collapse_sources,
        "arbitration_action": arbitration_action,
        "unique_action_count": disagreement["unique_action_count"],
        "severity_spread": disagreement["severity_spread"],
        "severity_variance": disagreement["severity_variance"],
        "mean_severity": disagreement["mean_severity"],
    }


def count_by_key(results, key):
    counts = {}

    for item in results:
        value = item[key]
        counts[value] = counts.get(value, 0) + 1

    return counts


def count_nested_action(results, gate_name):
    counts = {}

    for item in results:
        action = item["signal_actions"][gate_name]
        counts[action] = counts.get(action, 0) + 1

    return counts


def mean_by_key(results, key):
    values = [item[key] for item in results]
    return mean(values) if values else 0.0


def has_collapse_source(item, source_name):
    return source_name in item["collapse_sources"]


def main():
    os.makedirs(RESULTS_DIR, exist_ok=True)

    rows = read_dataset()

    results = [
        evaluate_record(row)
        for row in rows
    ]

    arbitration_counts = count_by_key(results, "arbitration_action")
    family_counts = count_by_key(results, "source_family")

    collapse_records = [
        item
        for item in results
        if item["arbitration_action"] == "COLLAPSE"
    ]

    escalate_records = [
        item
        for item in results
        if item["arbitration_action"] == "ESCALATE"
    ]

    multi_source_collapse_records = [
        item
        for item in collapse_records
        if len(item["collapse_sources"]) >= 2
    ]

    projection_confirmed_records = [
        item
        for item in collapse_records
        if has_collapse_source(item, "projection_gate")
    ]

    resistance_confirmed_records = [
        item
        for item in collapse_records
        if has_collapse_source(item, "collapse_gate")
    ]

    recoverability_confirmed_records = [
        item
        for item in collapse_records
        if has_collapse_source(item, "recoverability_gate")
    ]

    source_swap_records = [
        item
        for item in collapse_records
        if (
            has_collapse_source(item, "projection_gate")
            or has_collapse_source(item, "collapse_gate")
        )
    ]

    projection_only_confirmation_count = sum(
        1
        for item in collapse_records
        if has_collapse_source(item, "projection_gate")
        and not has_collapse_source(item, "collapse_gate")
    )

    resistance_only_confirmation_count = sum(
        1
        for item in collapse_records
        if has_collapse_source(item, "collapse_gate")
        and not has_collapse_source(item, "projection_gate")
    )

    joint_projection_resistance_count = sum(
        1
        for item in collapse_records
        if has_collapse_source(item, "projection_gate")
        and has_collapse_source(item, "collapse_gate")
    )

    isolated_effective_auto_collapse_count = sum(
        1
        for item in results
        if item["record_id"] == "isolated_effective_collapse"
        and item["arbitration_action"] == "COLLAPSE"
    )

    clean_control_pass_count = sum(
        1
        for item in results
        if item["record_id"] == "clean_control_reference"
        and item["arbitration_action"] == "PASS"
    )

    escalation_recovery_count = sum(
        1
        for item in escalate_records
        if len(item["collapse_sources"]) == 1
    )

    high_disagreement_count = sum(
        1
        for item in results
        if item["severity_spread"] >= 3
    )

    contradiction_count = sum(
        1
        for item in results
        if "PASS" in item["signal_actions"].values()
        and "COLLAPSE" in item["signal_actions"].values()
    )

    confirmation_source_families = sorted(
        set(
            source
            for item in collapse_records
            for source in item["collapse_sources"]
        )
    )

    summary = {
        "record_count": len(results),
        "dataset_path": DATA_PATH,
        "arbitration_action_distribution": arbitration_counts,
        "source_family_distribution": family_counts,
        "collapse_count": len(collapse_records),
        "escalate_count": len(escalate_records),
        "multi_source_collapse_count": len(multi_source_collapse_records),
        "projection_confirmed_collapse_count": len(projection_confirmed_records),
        "resistance_confirmed_collapse_count": len(resistance_confirmed_records),
        "recoverability_confirmed_collapse_count": len(
            recoverability_confirmed_records
        ),
        "confirmation_source_families": confirmation_source_families,
        "confirmation_swap_count": (
            projection_only_confirmation_count
            + resistance_only_confirmation_count
        ),
        "projection_only_confirmation_count": projection_only_confirmation_count,
        "resistance_only_confirmation_count": resistance_only_confirmation_count,
        "joint_projection_resistance_count": joint_projection_resistance_count,
        "source_swap_collapse_count": len(source_swap_records),
        "isolated_effective_auto_collapse_count": (
            isolated_effective_auto_collapse_count
        ),
        "clean_control_pass_count": clean_control_pass_count,
        "escalation_recovery_count": escalation_recovery_count,
        "high_disagreement_count": high_disagreement_count,
        "contradiction_count": contradiction_count,
        "mean_unique_action_count": mean_by_key(
            results,
            "unique_action_count",
        ),
        "mean_severity_spread": mean_by_key(results, "severity_spread"),
        "mean_severity_variance": mean_by_key(
            results,
            "severity_variance",
        ),
        "gate_action_distributions": {
            "effective_signal_gate": count_nested_action(
                results,
                "effective_signal_gate",
            ),
            "recoverability_gate": count_nested_action(
                results,
                "recoverability_gate",
            ),
            "divergence_gate": count_nested_action(
                results,
                "divergence_gate",
            ),
            "collapse_gate": count_nested_action(
                results,
                "collapse_gate",
            ),
            "projection_gate": count_nested_action(
                results,
                "projection_gate",
            ),
        },
    }

    status = (
        "PASS"
        if (
            len(collapse_records) >= 4
            and len(multi_source_collapse_records) >= 4
            and projection_only_confirmation_count >= 1
            and resistance_only_confirmation_count >= 1
            and joint_projection_resistance_count >= 1
            and len(confirmation_source_families) >= 3
            and isolated_effective_auto_collapse_count == 0
            and clean_control_pass_count == 1
            and escalation_recovery_count >= 2
            and high_disagreement_count >= 8
            and contradiction_count >= 5
        )
        else "CHECK"
    )

    payload = {
        "status": status,
        "version": VERSION,
        "summary": summary,
        "results": results,
        "reproduction_command": (
            "python examples/collapse_confirmation_source_swap_v0.py"
        ),
    }

    with open(RESULTS_PATH, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2)

    print("=" * 80)
    print("OMNIA-VALIDATION - Collapse Confirmation Source Swap v0")
    print("=" * 80)
    print()

    print("Status:", status)
    print("Version:", VERSION)
    print("Dataset path:", DATA_PATH)
    print("Record count:", len(results))

    print()
    print("Summary")
    print("-" * 80)

    for key, value in summary.items():
        if isinstance(value, dict):
            print(f"{key}:")
            for sub_key, sub_value in sorted(value.items()):
                print(f"  {sub_key}: {sub_value}")
        elif isinstance(value, list):
            print(f"{key}: {', '.join(value)}")
        else:
            print(f"{key}: {value}")

    print()
    print("Records")
    print("-" * 80)

    for item in results:
        sig = item["signal_actions"]
        sources = ",".join(item["collapse_sources"])
        if not sources:
            sources = "-"

        print(
            f"{item['record_id']:<42} "
            f"family={item['source_family']:<18} "
            f"arb={item['arbitration_action']:<9} "
            f"sources={sources:<45} "
            f"spread={item['severity_spread']} "
            f"var={item['severity_variance']:.6f} "
            f"eff={sig['effective_signal_gate']:<9} "
            f"rec={sig['recoverability_gate']:<9} "
            f"div={sig['divergence_gate']:<9} "
            f"col={sig['collapse_gate']:<9} "
            f"proj={sig['projection_gate']:<9}"
        )

    print()
    print("=" * 80)
    print("FINAL CHECK")
    print("=" * 80)

    if status == "PASS":
        print(
            "PASS - collapse confirmation remained stable under source swap."
        )
    else:
        print(
            "CHECK - collapse confirmation showed source dependency."
        )

    print()
    print("=" * 80)
    print("Result saved to:", RESULTS_PATH)
    print("=" * 80)


if __name__ == "__main__":
    main()