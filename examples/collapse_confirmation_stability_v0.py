import csv
import json
import math
import os
from copy import deepcopy
from statistics import mean

VERSION = "0.1.0"

DATA_DIR = "data"
RESULTS_DIR = "results"

DATA_PATH = os.path.join(
    DATA_DIR,
    "collapse_confirmation_stability_v0.csv",
)

RESULTS_PATH = os.path.join(
    RESULTS_DIR,
    "collapse_confirmation_stability_v0.json",
)


PERTURBATION_CONFIGS = [
    {
        "name": "baseline",
        "duplicate_delta": 0,
        "dominant_delta": 0,
        "failure_delta": 0,
        "instability_delta": 0,
        "projection_loss_delta": 0.0,
        "signal_delta": 0.0,
    },
    {
        "name": "mild_relief",
        "duplicate_delta": -2,
        "dominant_delta": -2,
        "failure_delta": -2,
        "instability_delta": -2,
        "projection_loss_delta": -0.03,
        "signal_delta": 0.02,
    },
    {
        "name": "mild_stress",
        "duplicate_delta": 2,
        "dominant_delta": 2,
        "failure_delta": 2,
        "instability_delta": 2,
        "projection_loss_delta": 0.03,
        "signal_delta": -0.02,
    },
    {
        "name": "projection_relief",
        "duplicate_delta": 0,
        "dominant_delta": 0,
        "failure_delta": 0,
        "instability_delta": 0,
        "projection_loss_delta": -0.08,
        "signal_delta": 0.00,
    },
    {
        "name": "projection_stress",
        "duplicate_delta": 0,
        "dominant_delta": 0,
        "failure_delta": 0,
        "instability_delta": 0,
        "projection_loss_delta": 0.08,
        "signal_delta": 0.00,
    },
    {
        "name": "collapse_relief",
        "duplicate_delta": 0,
        "dominant_delta": 0,
        "failure_delta": -6,
        "instability_delta": -6,
        "projection_loss_delta": 0.00,
        "signal_delta": 0.01,
    },
    {
        "name": "collapse_stress",
        "duplicate_delta": 0,
        "dominant_delta": 0,
        "failure_delta": 6,
        "instability_delta": 6,
        "projection_loss_delta": 0.00,
        "signal_delta": -0.01,
    },
    {
        "name": "redundancy_relief",
        "duplicate_delta": -8,
        "dominant_delta": -8,
        "failure_delta": 0,
        "instability_delta": 0,
        "projection_loss_delta": 0.00,
        "signal_delta": 0.02,
    },
    {
        "name": "redundancy_stress",
        "duplicate_delta": 8,
        "dominant_delta": 8,
        "failure_delta": 0,
        "instability_delta": 0,
        "projection_loss_delta": 0.00,
        "signal_delta": -0.02,
    },
]


def clamp(x, lo=0.0, hi=1.0):
    return max(lo, min(hi, x))


def clamp_int(x, lo, hi):
    return max(lo, min(hi, int(x)))


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


def base_rows():
    return [
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
            "record_id": "effective_only_collapse",
            "source_family": "effective",
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
            "record_id": "recoverability_near_failure",
            "source_family": "recoverability",
            "raw_count": 96,
            "duplicate_count": 72,
            "family_count": 3,
            "dominant_family_count": 81,
            "signal_a": 0.46,
            "signal_b": 0.44,
            "signal_c": 0.43,
            "failure_count": 19,
            "instability_count": 36,
            "projection_loss": 0.32,
        },
        {
            "record_id": "projection_confirmed_collapse",
            "source_family": "projection",
            "raw_count": 88,
            "duplicate_count": 22,
            "family_count": 5,
            "dominant_family_count": 51,
            "signal_a": 0.61,
            "signal_b": 0.59,
            "signal_c": 0.57,
            "failure_count": 18,
            "instability_count": 52,
            "projection_loss": 0.91,
        },
        {
            "record_id": "collapse_resistance_confirmed",
            "source_family": "collapse",
            "raw_count": 110,
            "duplicate_count": 31,
            "family_count": 4,
            "dominant_family_count": 72,
            "signal_a": 0.55,
            "signal_b": 0.52,
            "signal_c": 0.50,
            "failure_count": 91,
            "instability_count": 104,
            "projection_loss": 0.48,
        },
        {
            "record_id": "dual_confirmed_collapse",
            "source_family": "collapse",
            "raw_count": 104,
            "duplicate_count": 38,
            "family_count": 4,
            "dominant_family_count": 69,
            "signal_a": 0.63,
            "signal_b": 0.60,
            "signal_c": 0.58,
            "failure_count": 84,
            "instability_count": 99,
            "projection_loss": 0.88,
        },
        {
            "record_id": "surface_stable_deep_collapse",
            "source_family": "mixed",
            "raw_count": 130,
            "duplicate_count": 98,
            "family_count": 4,
            "dominant_family_count": 103,
            "signal_a": 0.88,
            "signal_b": 0.86,
            "signal_c": 0.83,
            "failure_count": 66,
            "instability_count": 91,
            "projection_loss": 0.74,
        },
        {
            "record_id": "projection_last_to_fail",
            "source_family": "mixed",
            "raw_count": 92,
            "duplicate_count": 65,
            "family_count": 4,
            "dominant_family_count": 72,
            "signal_a": 0.74,
            "signal_b": 0.72,
            "signal_c": 0.70,
            "failure_count": 52,
            "instability_count": 68,
            "projection_loss": 0.43,
        },
        {
            "record_id": "recoverability_last_to_fail",
            "source_family": "mixed",
            "raw_count": 78,
            "duplicate_count": 18,
            "family_count": 5,
            "dominant_family_count": 41,
            "signal_a": 0.92,
            "signal_b": 0.89,
            "signal_c": 0.87,
            "failure_count": 64,
            "instability_count": 73,
            "projection_loss": 0.89,
        },
        {
            "record_id": "distributed_irrecoverable_loss",
            "source_family": "support",
            "raw_count": 120,
            "duplicate_count": 76,
            "family_count": 4,
            "dominant_family_count": 92,
            "signal_a": 0.39,
            "signal_b": 0.37,
            "signal_c": 0.35,
            "failure_count": 78,
            "instability_count": 102,
            "projection_loss": 0.71,
        },
        {
            "record_id": "observer_alias_total_failure",
            "source_family": "observer",
            "raw_count": 87,
            "duplicate_count": 66,
            "family_count": 3,
            "dominant_family_count": 71,
            "signal_a": 0.96,
            "signal_b": 0.08,
            "signal_c": 0.91,
            "failure_count": 41,
            "instability_count": 69,
            "projection_loss": 0.86,
        },
        {
            "record_id": "redundancy_hides_collapse",
            "source_family": "logs",
            "raw_count": 180,
            "duplicate_count": 157,
            "family_count": 2,
            "dominant_family_count": 164,
            "signal_a": 0.67,
            "signal_b": 0.65,
            "signal_c": 0.62,
            "failure_count": 73,
            "instability_count": 131,
            "projection_loss": 0.67,
        },
        {
            "record_id": "collapse_with_entropy_preserved",
            "source_family": "sensor",
            "raw_count": 102,
            "duplicate_count": 21,
            "family_count": 5,
            "dominant_family_count": 61,
            "signal_a": 0.91,
            "signal_b": 0.42,
            "signal_c": 0.86,
            "failure_count": 79,
            "instability_count": 96,
            "projection_loss": 0.84,
        },
        {
            "record_id": "hard_collapse_low_everything",
            "source_family": "collapse",
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
            "record_id": "borderline_should_escalate",
            "source_family": "borderline",
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
            "record_id": "clean_but_high_divergence",
            "source_family": "borderline",
            "raw_count": 66,
            "duplicate_count": 5,
            "family_count": 8,
            "dominant_family_count": 12,
            "signal_a": 0.99,
            "signal_b": 0.05,
            "signal_c": 0.96,
            "failure_count": 1,
            "instability_count": 4,
            "projection_loss": 0.08,
        },
        {
            "record_id": "partial_collapse_recoverable",
            "source_family": "support",
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
        {
            "record_id": "projection_only_failure",
            "source_family": "projection",
            "raw_count": 76,
            "duplicate_count": 6,
            "family_count": 7,
            "dominant_family_count": 18,
            "signal_a": 0.81,
            "signal_b": 0.79,
            "signal_c": 0.78,
            "failure_count": 2,
            "instability_count": 7,
            "projection_loss": 0.94,
        },
        {
            "record_id": "collapse_only_failure",
            "source_family": "collapse",
            "raw_count": 95,
            "duplicate_count": 8,
            "family_count": 8,
            "dominant_family_count": 19,
            "signal_a": 0.82,
            "signal_b": 0.80,
            "signal_c": 0.77,
            "failure_count": 88,
            "instability_count": 94,
            "projection_loss": 0.12,
        },
        {
            "record_id": "multi_gate_confirmed_collapse",
            "source_family": "collapse",
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
    ]


def write_default_dataset():
    os.makedirs(DATA_DIR, exist_ok=True)

    rows = base_rows()

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


def perturb_row(row, config):
    out = deepcopy(row)
    raw_count = out["raw_count"]

    out["duplicate_count"] = clamp_int(
        out["duplicate_count"] + config["duplicate_delta"],
        0,
        raw_count,
    )

    out["dominant_family_count"] = clamp_int(
        out["dominant_family_count"] + config["dominant_delta"],
        0,
        raw_count,
    )

    out["failure_count"] = clamp_int(
        out["failure_count"] + config["failure_delta"],
        0,
        raw_count,
    )

    out["instability_count"] = clamp_int(
        out["instability_count"] + config["instability_delta"],
        0,
        raw_count,
    )

    out["projection_loss"] = clamp(
        out["projection_loss"] + config["projection_loss_delta"]
    )

    out["signal_a"] = clamp(out["signal_a"] + config["signal_delta"])
    out["signal_b"] = clamp(out["signal_b"] + config["signal_delta"])
    out["signal_c"] = clamp(out["signal_c"] + config["signal_delta"])

    return out


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


def safe_count(counts, key):
    return counts.get(key, 0)


def summarize_config(config_name, evaluated):
    arbitration_counts = count_by_key(evaluated, "arbitration_action")

    multi_gate_collapse_count = sum(
        1
        for item in evaluated
        if list(item["signal_actions"].values()).count("COLLAPSE") >= 2
    )

    collapse_with_projection_count = sum(
        1
        for item in evaluated
        if item["signal_actions"]["projection_gate"] == "COLLAPSE"
    )

    collapse_with_resistance_count = sum(
        1
        for item in evaluated
        if item["signal_actions"]["collapse_gate"] == "COLLAPSE"
    )

    isolated_effective_auto_collapse_count = sum(
        1
        for item in evaluated
        if item["record_id"] == "effective_only_collapse"
        and item["arbitration_action"] == "COLLAPSE"
    )

    clean_control_pass_count = sum(
        1
        for item in evaluated
        if item["record_id"] == "clean_control_reference"
        and item["arbitration_action"] == "PASS"
    )

    ambiguous_escalate_count = sum(
        1
        for item in evaluated
        if item["record_id"] in {
            "effective_only_collapse",
            "recoverability_near_failure",
            "borderline_should_escalate",
        }
        and item["arbitration_action"] == "ESCALATE"
    )

    high_disagreement_count = sum(
        1
        for item in evaluated
        if item["severity_spread"] >= 3
    )

    contradiction_count = sum(
        1
        for item in evaluated
        if "PASS" in item["signal_actions"].values()
        and "COLLAPSE" in item["signal_actions"].values()
    )

    mean_spread = mean(
        item["severity_spread"]
        for item in evaluated
    )

    config_status = (
        "PASS"
        if (
            safe_count(arbitration_counts, "COLLAPSE") >= 3
            and multi_gate_collapse_count >= 3
            and collapse_with_projection_count >= 2
            and collapse_with_resistance_count >= 2
            and isolated_effective_auto_collapse_count == 0
            and clean_control_pass_count == 1
            and high_disagreement_count >= 6
            and contradiction_count >= 4
        )
        else "CHECK"
    )

    return {
        "config_name": config_name,
        "status": config_status,
        "arbitration_action_distribution": arbitration_counts,
        "collapse_count": safe_count(arbitration_counts, "COLLAPSE"),
        "escalate_count": safe_count(arbitration_counts, "ESCALATE"),
        "pass_count": safe_count(arbitration_counts, "PASS"),
        "retry_count": safe_count(arbitration_counts, "RETRY"),
        "flag_count": safe_count(arbitration_counts, "FLAG"),
        "multi_gate_collapse_count": multi_gate_collapse_count,
        "collapse_with_projection_count": collapse_with_projection_count,
        "collapse_with_resistance_count": collapse_with_resistance_count,
        "isolated_effective_auto_collapse_count": (
            isolated_effective_auto_collapse_count
        ),
        "clean_control_pass_count": clean_control_pass_count,
        "ambiguous_escalate_count": ambiguous_escalate_count,
        "high_disagreement_count": high_disagreement_count,
        "contradiction_count": contradiction_count,
        "mean_severity_spread": mean_spread,
        "sample_results": evaluated[:5],
    }


def main():
    os.makedirs(RESULTS_DIR, exist_ok=True)

    rows = read_dataset()

    config_runs = []

    for config in PERTURBATION_CONFIGS:
        perturbed_rows = [
            perturb_row(row, config)
            for row in rows
        ]

        evaluated = [
            evaluate_record(row)
            for row in perturbed_rows
        ]

        config_runs.append(
            summarize_config(
                config_name=config["name"],
                evaluated=evaluated,
            )
        )

    pass_config_count = sum(
        1 for run in config_runs if run["status"] == "PASS"
    )

    check_config_count = len(config_runs) - pass_config_count

    collapse_counts = [
        run["collapse_count"]
        for run in config_runs
    ]

    multi_gate_counts = [
        run["multi_gate_collapse_count"]
        for run in config_runs
    ]

    projection_counts = [
        run["collapse_with_projection_count"]
        for run in config_runs
    ]

    resistance_counts = [
        run["collapse_with_resistance_count"]
        for run in config_runs
    ]

    isolated_auto_counts = [
        run["isolated_effective_auto_collapse_count"]
        for run in config_runs
    ]

    clean_control_counts = [
        run["clean_control_pass_count"]
        for run in config_runs
    ]

    escalate_counts = [
        run["escalate_count"]
        for run in config_runs
    ]

    high_disagreement_counts = [
        run["high_disagreement_count"]
        for run in config_runs
    ]

    contradiction_counts = [
        run["contradiction_count"]
        for run in config_runs
    ]

    mean_spreads = [
        run["mean_severity_spread"]
        for run in config_runs
    ]

    summary = {
        "config_count": len(config_runs),
        "record_count_per_config": len(rows),
        "total_evaluated_records": len(rows) * len(config_runs),
        "pass_config_count": pass_config_count,
        "check_config_count": check_config_count,
        "mean_collapse_count": mean(collapse_counts),
        "min_collapse_count": min(collapse_counts),
        "max_collapse_count": max(collapse_counts),
        "mean_multi_gate_collapse_count": mean(multi_gate_counts),
        "min_multi_gate_collapse_count": min(multi_gate_counts),
        "max_multi_gate_collapse_count": max(multi_gate_counts),
        "mean_projection_confirmed_count": mean(projection_counts),
        "min_projection_confirmed_count": min(projection_counts),
        "mean_resistance_confirmed_count": mean(resistance_counts),
        "min_resistance_confirmed_count": min(resistance_counts),
        "max_isolated_effective_auto_collapse_count": max(
            isolated_auto_counts
        ),
        "min_clean_control_pass_count": min(clean_control_counts),
        "mean_escalate_count": mean(escalate_counts),
        "min_escalate_count": min(escalate_counts),
        "mean_high_disagreement_count": mean(high_disagreement_counts),
        "min_high_disagreement_count": min(high_disagreement_counts),
        "mean_contradiction_count": mean(contradiction_counts),
        "min_contradiction_count": min(contradiction_counts),
        "mean_severity_spread": mean(mean_spreads),
        "min_mean_severity_spread": min(mean_spreads),
    }

    status = (
        "PASS"
        if (
            pass_config_count == len(config_runs)
            and summary["min_collapse_count"] >= 3
            and summary["min_multi_gate_collapse_count"] >= 3
            and summary["min_projection_confirmed_count"] >= 2
            and summary["min_resistance_confirmed_count"] >= 2
            and summary["max_isolated_effective_auto_collapse_count"] == 0
            and summary["min_clean_control_pass_count"] == 1
            and summary["min_high_disagreement_count"] >= 6
            and summary["min_contradiction_count"] >= 4
        )
        else "CHECK"
    )

    payload = {
        "status": status,
        "version": VERSION,
        "summary": summary,
        "config_runs": config_runs,
        "reproduction_command": (
            "python examples/collapse_confirmation_stability_v0.py"
        ),
    }

    with open(RESULTS_PATH, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2)

    print("=" * 80)
    print("OMNIA-VALIDATION - Collapse Confirmation Stability v0")
    print("=" * 80)
    print()

    print("Status:", status)
    print("Version:", VERSION)
    print("Config count:", len(config_runs))
    print("Record count per config:", len(rows))

    print()
    print("Summary")
    print("-" * 80)

    for key, value in summary.items():
        print(f"{key}: {value}")

    print()
    print("Config summaries")
    print("-" * 80)

    for run in config_runs:
        print(
            f"{run['config_name']:<22} "
            f"status={run['status']:<5} "
            f"collapse={run['collapse_count']} "
            f"multi={run['multi_gate_collapse_count']} "
            f"projection={run['collapse_with_projection_count']} "
            f"resistance={run['collapse_with_resistance_count']} "
            f"isolated_auto={run['isolated_effective_auto_collapse_count']} "
            f"control_pass={run['clean_control_pass_count']} "
            f"high={run['high_disagreement_count']} "
            f"contradiction={run['contradiction_count']} "
            f"mean_spread={run['mean_severity_spread']:.12f}"
        )

    print()
    print("=" * 80)
    print("FINAL CHECK")
    print("=" * 80)

    if status == "PASS":
        print(
            "PASS - multi-gate collapse confirmation remained stable "
            "under perturbation."
        )
    else:
        print(
            "CHECK - multi-gate collapse confirmation showed instability "
            "under perturbation."
        )

    print()
    print("=" * 80)
    print("Result saved to:", RESULTS_PATH)
    print("=" * 80)


if __name__ == "__main__":
    main()