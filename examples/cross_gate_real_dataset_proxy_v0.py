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
    "cross_gate_real_dataset_proxy_v0.csv",
)

RESULTS_PATH = os.path.join(
    RESULTS_DIR,
    "cross_gate_real_dataset_proxy_v0.json",
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

    if os.path.exists(DATA_PATH):
        return

    rows = [
        {
            "record_id": "open_issue_tracker",
            "source_family": "software",
            "raw_count": 82,
            "duplicate_count": 41,
            "family_count": 3,
            "dominant_family_count": 61,
            "signal_a": 0.82,
            "signal_b": 0.77,
            "signal_c": 0.69,
            "failure_count": 7,
            "instability_count": 12,
            "projection_loss": 0.18,
        },
        {
            "record_id": "release_notes_patchset",
            "source_family": "software",
            "raw_count": 37,
            "duplicate_count": 4,
            "family_count": 6,
            "dominant_family_count": 12,
            "signal_a": 0.68,
            "signal_b": 0.71,
            "signal_c": 0.66,
            "failure_count": 2,
            "instability_count": 5,
            "projection_loss": 0.11,
        },
        {
            "record_id": "support_ticket_cluster",
            "source_family": "support",
            "raw_count": 126,
            "duplicate_count": 76,
            "family_count": 4,
            "dominant_family_count": 88,
            "signal_a": 0.74,
            "signal_b": 0.33,
            "signal_c": 0.58,
            "failure_count": 22,
            "instability_count": 39,
            "projection_loss": 0.42,
        },
        {
            "record_id": "refund_request_batch",
            "source_family": "support",
            "raw_count": 58,
            "duplicate_count": 9,
            "family_count": 8,
            "dominant_family_count": 14,
            "signal_a": 0.44,
            "signal_b": 0.48,
            "signal_c": 0.50,
            "failure_count": 3,
            "instability_count": 9,
            "projection_loss": 0.16,
        },
        {
            "record_id": "sensor_fault_window",
            "source_family": "sensor",
            "raw_count": 94,
            "duplicate_count": 13,
            "family_count": 5,
            "dominant_family_count": 37,
            "signal_a": 0.15,
            "signal_b": 0.91,
            "signal_c": 0.83,
            "failure_count": 34,
            "instability_count": 51,
            "projection_loss": 0.71,
        },
        {
            "record_id": "telemetry_baseline_window",
            "source_family": "sensor",
            "raw_count": 120,
            "duplicate_count": 7,
            "family_count": 9,
            "dominant_family_count": 21,
            "signal_a": 0.72,
            "signal_b": 0.75,
            "signal_c": 0.78,
            "failure_count": 4,
            "instability_count": 8,
            "projection_loss": 0.08,
        },
        {
            "record_id": "log_anomaly_burst",
            "source_family": "logs",
            "raw_count": 210,
            "duplicate_count": 124,
            "family_count": 3,
            "dominant_family_count": 162,
            "signal_a": 0.36,
            "signal_b": 0.39,
            "signal_c": 0.94,
            "failure_count": 55,
            "instability_count": 88,
            "projection_loss": 0.62,
        },
        {
            "record_id": "documentation_revision_set",
            "source_family": "docs",
            "raw_count": 45,
            "duplicate_count": 6,
            "family_count": 7,
            "dominant_family_count": 11,
            "signal_a": 0.81,
            "signal_b": 0.73,
            "signal_c": 0.70,
            "failure_count": 1,
            "instability_count": 6,
            "projection_loss": 0.10,
        },
        {
            "record_id": "research_claim_group",
            "source_family": "research",
            "raw_count": 33,
            "duplicate_count": 3,
            "family_count": 5,
            "dominant_family_count": 10,
            "signal_a": 0.92,
            "signal_b": 0.41,
            "signal_c": 0.88,
            "failure_count": 7,
            "instability_count": 12,
            "projection_loss": 0.27,
        },
        {
            "record_id": "benchmark_result_matrix",
            "source_family": "research",
            "raw_count": 64,
            "duplicate_count": 8,
            "family_count": 8,
            "dominant_family_count": 16,
            "signal_a": 0.66,
            "signal_b": 0.64,
            "signal_c": 0.61,
            "failure_count": 4,
            "instability_count": 10,
            "projection_loss": 0.15,
        },
        {
            "record_id": "customer_feedback_topic_set",
            "source_family": "support",
            "raw_count": 89,
            "duplicate_count": 29,
            "family_count": 6,
            "dominant_family_count": 44,
            "signal_a": 0.58,
            "signal_b": 0.52,
            "signal_c": 0.69,
            "failure_count": 11,
            "instability_count": 25,
            "projection_loss": 0.31,
        },
        {
            "record_id": "dependency_graph_snapshot",
            "source_family": "software",
            "raw_count": 144,
            "duplicate_count": 18,
            "family_count": 10,
            "dominant_family_count": 29,
            "signal_a": 0.84,
            "signal_b": 0.82,
            "signal_c": 0.77,
            "failure_count": 9,
            "instability_count": 17,
            "projection_loss": 0.14,
        },
        {
            "record_id": "incident_report_bundle",
            "source_family": "logs",
            "raw_count": 76,
            "duplicate_count": 24,
            "family_count": 4,
            "dominant_family_count": 47,
            "signal_a": 0.28,
            "signal_b": 0.88,
            "signal_c": 0.44,
            "failure_count": 19,
            "instability_count": 31,
            "projection_loss": 0.55,
        },
        {
            "record_id": "stable_validation_subset",
            "source_family": "research",
            "raw_count": 52,
            "duplicate_count": 2,
            "family_count": 9,
            "dominant_family_count": 9,
            "signal_a": 0.86,
            "signal_b": 0.87,
            "signal_c": 0.84,
            "failure_count": 0,
            "instability_count": 3,
            "projection_loss": 0.05,
        },
        {
            "record_id": "ambiguous_evaluation_pack",
            "source_family": "research",
            "raw_count": 48,
            "duplicate_count": 11,
            "family_count": 5,
            "dominant_family_count": 24,
            "signal_a": 0.49,
            "signal_b": 0.91,
            "signal_c": 0.22,
            "failure_count": 8,
            "instability_count": 17,
            "projection_loss": 0.39,
        },
        {
            "record_id": "redundant_policy_corpus",
            "source_family": "docs",
            "raw_count": 132,
            "duplicate_count": 84,
            "family_count": 3,
            "dominant_family_count": 101,
            "signal_a": 0.63,
            "signal_b": 0.60,
            "signal_c": 0.57,
            "failure_count": 12,
            "instability_count": 28,
            "projection_loss": 0.29,
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


def mean_by_family(results, key):
    output = {}

    for family in sorted(set(item["source_family"] for item in results)):
        values = [
            item[key]
            for item in results
            if item["source_family"] == family
        ]

        output[family] = mean(values) if values else 0.0

    return output


def main():
    os.makedirs(RESULTS_DIR, exist_ok=True)

    rows = read_dataset()

    results = [
        evaluate_record(row)
        for row in rows
    ]

    arbitration_counts = count_by_key(results, "arbitration_action")
    family_counts = count_by_key(results, "source_family")

    high_disagreement_count = sum(
        1
        for item in results
        if item["severity_spread"] >= 3
    )

    medium_disagreement_count = sum(
        1
        for item in results
        if item["severity_spread"] == 2
    )

    low_disagreement_count = sum(
        1
        for item in results
        if item["severity_spread"] <= 1
    )

    contradiction_count = sum(
        1
        for item in results
        if "PASS" in item["signal_actions"].values()
        and "COLLAPSE" in item["signal_actions"].values()
    )

    unanimous_count = sum(
        1
        for item in results
        if item["unique_action_count"] == 1
    )

    summary = {
        "record_count": len(results),
        "dataset_path": DATA_PATH,
        "arbitration_action_distribution": arbitration_counts,
        "source_family_distribution": family_counts,
        "high_disagreement_count": high_disagreement_count,
        "medium_disagreement_count": medium_disagreement_count,
        "low_disagreement_count": low_disagreement_count,
        "contradiction_count": contradiction_count,
        "unanimous_count": unanimous_count,
        "mean_unique_action_count": mean_by_key(
            results,
            "unique_action_count",
        ),
        "mean_severity_spread": mean_by_key(results, "severity_spread"),
        "mean_severity_variance": mean_by_key(
            results,
            "severity_variance",
        ),
        "mean_spread_by_family": mean_by_family(
            results,
            "severity_spread",
        ),
        "mean_variance_by_family": mean_by_family(
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
            len(results) >= 10
            and high_disagreement_count > 0
            and contradiction_count > 0
            and "ESCALATE" in arbitration_counts
            and "COLLAPSE" in arbitration_counts
        )
        else "CHECK"
    )

    payload = {
        "status": status,
        "version": VERSION,
        "summary": summary,
        "results": results,
        "reproduction_command": (
            "python examples/cross_gate_real_dataset_proxy_v0.py"
        ),
    }

    with open(RESULTS_PATH, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2)

    print("=" * 80)
    print("OMNIA-VALIDATION - Cross-Gate Real Dataset Proxy v0")
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
        else:
            print(f"{key}: {value}")

    print()
    print("Records")
    print("-" * 80)

    for item in results:
        sig = item["signal_actions"]

        print(
            f"{item['record_id']:<32} "
            f"family={item['source_family']:<9} "
            f"arb={item['arbitration_action']:<9} "
            f"unique={item['unique_action_count']} "
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
            "PASS - real-dataset proxy exposed measurable cross-gate conflict."
        )
    else:
        print(
            "CHECK - real-dataset proxy did not expose enough cross-gate conflict."
        )

    print()
    print("=" * 80)
    print("Result saved to:", RESULTS_PATH)
    print("=" * 80)


if __name__ == "__main__":
    main()