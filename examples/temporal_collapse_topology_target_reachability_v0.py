import json
from pathlib import Path
from statistics import mean, pstdev

VERSION = "0.1.0"

RESULTS_PATH = Path(
    "results/temporal_collapse_topology_target_reachability_v0.json"
)

CONFIRMATION_WINDOWS = [2, 3, 4]
PERSISTENCE_WINDOW = 2

SUPPORTED_CLASSES = [
    "GLOBAL_PERSISTENT_COLLAPSE",
    "RECOVERY_RELAPSE_COLLAPSE",
    "FRAGMENTED_LOCAL_COLLAPSE",
    "OSCILLATING_NONPERSISTENT",
    "SPIKE_FILTERED",
    "CLEAN_PASS",
]

FRAME_VALUES = [
    "PASS",
    "ESCALATE",
    "COLLAPSE",
]


def compute_runs(sequence):
    runs = []
    start = None

    for index, value in enumerate(sequence):
        if value == "COLLAPSE":
            if start is None:
                start = index
        else:
            if start is not None:
                runs.append((start, index - 1))
                start = None

    if start is not None:
        runs.append((start, len(sequence) - 1))

    return runs


def classify(sequence, confirmation_window):
    persistence_threshold = confirmation_window + PERSISTENCE_WINDOW

    runs = compute_runs(sequence)

    collapse_run_count = len(runs)

    run_lengths = [
        end - start + 1
        for start, end in runs
    ]

    max_run_length = max(run_lengths) if run_lengths else 0

    local_confirmation_count = sum(
        1
        for length in run_lengths
        if length >= confirmation_window
    )

    persistence_reset_count = max(
        collapse_run_count - 1,
        0,
    )

    fragmentation_index = (
        persistence_reset_count / max(collapse_run_count, 1)
    )

    global_persistence_detected = any(
        length >= persistence_threshold
        for length in run_lengths
    )

    if collapse_run_count == 0:
        label = "CLEAN_PASS"

    elif (
        collapse_run_count == 1
        and max_run_length < confirmation_window
    ):
        label = "SPIKE_FILTERED"

    elif (
        global_persistence_detected
        and persistence_reset_count == 0
    ):
        label = "GLOBAL_PERSISTENT_COLLAPSE"

    elif (
        global_persistence_detected
        and persistence_reset_count > 0
    ):
        label = "RECOVERY_RELAPSE_COLLAPSE"

    elif (
        local_confirmation_count > 0
        and not global_persistence_detected
    ):
        label = "FRAGMENTED_LOCAL_COLLAPSE"

    else:
        label = "OSCILLATING_NONPERSISTENT"

    return {
        "classification": label,
        "confirmation_window": confirmation_window,
        "persistence_window": PERSISTENCE_WINDOW,
        "global_persistence_threshold": persistence_threshold,
        "collapse_run_count": collapse_run_count,
        "run_lengths": run_lengths,
        "max_temporal_collapse_run_length": max_run_length,
        "temporal_collapse_run_count": local_confirmation_count,
        "persistence_reset_count": persistence_reset_count,
        "fragmentation_index": round(fragmentation_index, 4),
        "global_persistence_detected": global_persistence_detected,
        "local_confirmation_count": local_confirmation_count,
        "collapse_runs": runs,
    }


def make_sequence(length, runs):
    sequence = ["PASS"] * length

    for start, run_length in runs:
        end = min(length, start + run_length)

        for index in range(start, end):
            sequence[index] = "COLLAPSE"

        if start > 0:
            sequence[start - 1] = "ESCALATE"

    return sequence


def make_sequence_from_lengths(run_lengths, spacing=5, start_offset=4):
    if not run_lengths:
        return 10, []

    runs = []
    cursor = start_offset

    for run_length in run_lengths:
        runs.append((cursor, run_length))
        cursor += run_length + spacing

    length = cursor + start_offset

    return length, runs


def target_reachability_specs():
    raw_specs = [
        {
            "name": "zero_run_clean",
            "run_lengths": [],
        },
        {
            "name": "single_spike_len_1",
            "run_lengths": [1],
        },
        {
            "name": "single_run_len_2",
            "run_lengths": [2],
        },
        {
            "name": "single_run_len_3",
            "run_lengths": [3],
        },
        {
            "name": "single_run_len_4",
            "run_lengths": [4],
        },
        {
            "name": "single_run_len_7",
            "run_lengths": [7],
        },
        {
            "name": "two_spikes_len_1_1",
            "run_lengths": [1, 1],
        },
        {
            "name": "two_runs_len_2_2",
            "run_lengths": [2, 2],
        },
        {
            "name": "two_runs_len_3_3",
            "run_lengths": [3, 3],
        },
        {
            "name": "two_runs_len_5_5",
            "run_lengths": [5, 5],
        },
        {
            "name": "three_spikes_len_1_1_1",
            "run_lengths": [1, 1, 1],
        },
        {
            "name": "three_runs_len_2_2_2",
            "run_lengths": [2, 2, 2],
        },
        {
            "name": "three_runs_len_3_3_3",
            "run_lengths": [3, 3, 3],
        },
        {
            "name": "three_runs_len_4_4_4",
            "run_lengths": [4, 4, 4],
        },
        {
            "name": "four_spikes_len_1_1_1_1",
            "run_lengths": [1, 1, 1, 1],
        },
        {
            "name": "four_runs_len_2_2_2_2",
            "run_lengths": [2, 2, 2, 2],
        },
        {
            "name": "mixed_1_2_3_4",
            "run_lengths": [1, 2, 3, 4],
        },
        {
            "name": "mixed_2_3_4_5",
            "run_lengths": [2, 3, 4, 5],
        },
        {
            "name": "mixed_single_confirmed_plus_spikes",
            "run_lengths": [1, 1, 4, 1],
        },
        {
            "name": "mixed_two_confirmed_plus_spikes",
            "run_lengths": [1, 3, 1, 4],
        },
    ]

    specs = []

    for item in raw_specs:
        length, runs = make_sequence_from_lengths(item["run_lengths"])

        specs.append({
            "name": item["name"],
            "length": length,
            "runs": runs,
            "run_lengths": item["run_lengths"],
        })

    return specs


def safe_mean(values):
    return mean(values) if values else None


def safe_std(values):
    return pstdev(values) if len(values) > 1 else 0.0


def thresholded_reducible_mass(run_lengths, confirmation_window):
    threshold_below_confirmation = confirmation_window - 1

    return sum(
        max(0, run_length - threshold_below_confirmation)
        for run_length in run_lengths
    )


def post_reduction_lengths(run_lengths, confirmation_window):
    threshold_below_confirmation = confirmation_window - 1

    return [
        min(run_length, threshold_below_confirmation)
        for run_length in run_lengths
        if min(run_length, threshold_below_confirmation) > 0
    ]


def build_reduced_sequence(original_runs, reduced_lengths):
    if not reduced_lengths:
        return ["PASS"] * 10

    spacing = 5
    start_offset = 4
    cursor = start_offset

    reduced_runs = []

    for length in reduced_lengths:
        reduced_runs.append((cursor, length))
        cursor += length + spacing

    sequence_length = cursor + start_offset

    return make_sequence(sequence_length, reduced_runs)


def predicted_target_class_from_remaining_runs(
    remaining_lengths,
    confirmation_window,
):
    if len(remaining_lengths) == 0:
        return "CLEAN_PASS"

    if len(remaining_lengths) == 1:
        if remaining_lengths[0] < confirmation_window:
            return "SPIKE_FILTERED"

    if all(length < confirmation_window for length in remaining_lengths):
        return "OSCILLATING_NONPERSISTENT"

    return "UNRESOLVED"


def geometry_features(run_lengths):
    return {
        "collapse_run_count": len(run_lengths),
        "run_lengths": run_lengths,
        "run_length_mean": safe_mean(run_lengths),
        "run_length_std": safe_std(run_lengths),
        "max_run_length": max(run_lengths) if run_lengths else 0,
        "min_run_length": min(run_lengths) if run_lengths else 0,
        "total_collapse_frames": sum(run_lengths),
        "confirmed_run_count_by_threshold": {
            str(confirmation_window): sum(
                1
                for length in run_lengths
                if length >= confirmation_window
            )
            for confirmation_window in CONFIRMATION_WINDOWS
        },
    }


def build_records():
    records = []

    for variant_index, spec in enumerate(target_reachability_specs()):
        sequence = make_sequence(
            spec["length"],
            spec["runs"],
        )

        features = geometry_features(spec["run_lengths"])

        threshold_results = []

        for confirmation_window in CONFIRMATION_WINDOWS:
            source_metrics = classify(
                sequence,
                confirmation_window,
            )

            minimum_depth = thresholded_reducible_mass(
                spec["run_lengths"],
                confirmation_window,
            )

            remaining_lengths = post_reduction_lengths(
                spec["run_lengths"],
                confirmation_window,
            )

            predicted_target = predicted_target_class_from_remaining_runs(
                remaining_lengths,
                confirmation_window,
            )

            reduced_sequence = build_reduced_sequence(
                spec["runs"],
                remaining_lengths,
            )

            reduced_metrics = classify(
                reduced_sequence,
                confirmation_window,
            )

            observed_reduced_class = reduced_metrics["classification"]

            prediction_matches_observed = (
                predicted_target == observed_reduced_class
            )

            threshold_results.append({
                "confirmation_window": confirmation_window,
                "global_persistence_threshold": (
                    confirmation_window + PERSISTENCE_WINDOW
                ),
                "source_class": source_metrics["classification"],
                "source_metrics": source_metrics,
                "minimum_target_depth": minimum_depth,
                "remaining_run_count": len(remaining_lengths),
                "remaining_run_lengths": remaining_lengths,
                "predicted_target_class": predicted_target,
                "observed_reduced_class": observed_reduced_class,
                "prediction_matches_observed": (
                    prediction_matches_observed
                ),
                "reduced_metrics": reduced_metrics,
                "target_reachability_rule": (
                    "0 remaining runs -> CLEAN_PASS; "
                    "1 remaining run -> SPIKE_FILTERED; "
                    "2+ remaining sub-threshold runs -> "
                    "OSCILLATING_NONPERSISTENT"
                ),
            })

        records.append({
            "variant_index": variant_index,
            "geometry_name": spec["name"],
            "trajectory_length": spec["length"],
            "runs": spec["runs"],
            "run_lengths": spec["run_lengths"],
            "raw_action_sequence": sequence,
            "features": features,
            "threshold_results": threshold_results,
            "method": "post_reduction_target_class_law",
        })

    return records


def flatten_records(records):
    flat = []

    for record in records:
        for item in record["threshold_results"]:
            flat.append({
                "variant_index": record["variant_index"],
                "geometry_name": record["geometry_name"],
                "run_lengths": record["run_lengths"],
                "features": record["features"],
                "confirmation_window": item["confirmation_window"],
                "source_class": item["source_class"],
                "minimum_target_depth": item["minimum_target_depth"],
                "remaining_run_count": item["remaining_run_count"],
                "remaining_run_lengths": item["remaining_run_lengths"],
                "predicted_target_class": item["predicted_target_class"],
                "observed_reduced_class": item["observed_reduced_class"],
                "prediction_matches_observed": (
                    item["prediction_matches_observed"]
                ),
            })

    return flat


def summarize_by_target(flat_records):
    summary = {}

    for item in flat_records:
        target_class = item["observed_reduced_class"]

        if target_class not in summary:
            summary[target_class] = {
                "record_count": 0,
                "geometry_names": [],
                "confirmation_windows": [],
                "remaining_run_counts": [],
                "minimum_target_depths": [],
            }

        summary[target_class]["record_count"] += 1
        summary[target_class]["geometry_names"].append(
            item["geometry_name"]
        )
        summary[target_class]["confirmation_windows"].append(
            item["confirmation_window"]
        )
        summary[target_class]["remaining_run_counts"].append(
            item["remaining_run_count"]
        )
        summary[target_class]["minimum_target_depths"].append(
            item["minimum_target_depth"]
        )

    for target_class, item in summary.items():
        item["remaining_run_count_values"] = sorted(
            set(item["remaining_run_counts"])
        )
        item["minimum_target_depth_values"] = sorted(
            set(item["minimum_target_depths"])
        )
        item["minimum_target_depth_mean"] = safe_mean(
            item["minimum_target_depths"]
        )
        item["minimum_target_depth_std"] = safe_std(
            item["minimum_target_depths"]
        )

    return summary


def summarize_by_remaining_run_count(flat_records):
    summary = {}

    for item in flat_records:
        count = item["remaining_run_count"]
        key = str(count)

        if key not in summary:
            summary[key] = {
                "remaining_run_count": count,
                "record_count": 0,
                "observed_classes": [],
                "predicted_classes": [],
                "geometry_names": [],
                "confirmation_windows": [],
            }

        summary[key]["record_count"] += 1
        summary[key]["observed_classes"].append(
            item["observed_reduced_class"]
        )
        summary[key]["predicted_classes"].append(
            item["predicted_target_class"]
        )
        summary[key]["geometry_names"].append(
            item["geometry_name"]
        )
        summary[key]["confirmation_windows"].append(
            item["confirmation_window"]
        )

    for key, item in summary.items():
        item["observed_class_values"] = sorted(
            set(item["observed_classes"])
        )
        item["predicted_class_values"] = sorted(
            set(item["predicted_classes"])
        )
        item["class_stable_for_remaining_count"] = (
            len(item["observed_class_values"]) == 1
        )

    return summary


def summarize_by_threshold(flat_records):
    summary = {}

    for confirmation_window in CONFIRMATION_WINDOWS:
        items = [
            item
            for item in flat_records
            if item["confirmation_window"] == confirmation_window
        ]

        class_counts = {}

        for item in items:
            target_class = item["observed_reduced_class"]
            class_counts[target_class] = (
                class_counts.get(target_class, 0) + 1
            )

        prediction_matches = [
            item["prediction_matches_observed"]
            for item in items
        ]

        summary[str(confirmation_window)] = {
            "confirmation_window": confirmation_window,
            "record_count": len(items),
            "class_counts": class_counts,
            "prediction_match_count": sum(
                1 for value in prediction_matches if value
            ),
            "prediction_match_rate": (
                sum(1 for value in prediction_matches if value)
                / max(len(prediction_matches), 1)
            ),
            "remaining_run_count_values": sorted(
                set(item["remaining_run_count"] for item in items)
            ),
            "minimum_target_depth_values": sorted(
                set(item["minimum_target_depth"] for item in items)
            ),
        }

    return summary


def validate_reachability_rule(flat_records):
    failures = []

    for item in flat_records:
        remaining_count = item["remaining_run_count"]
        observed = item["observed_reduced_class"]

        if remaining_count == 0:
            expected = "CLEAN_PASS"
        elif remaining_count == 1:
            expected = "SPIKE_FILTERED"
        else:
            expected = "OSCILLATING_NONPERSISTENT"

        if observed != expected:
            failures.append({
                "geometry_name": item["geometry_name"],
                "confirmation_window": item["confirmation_window"],
                "remaining_run_count": remaining_count,
                "expected": expected,
                "observed": observed,
            })

    return {
        "target_reachability_rule_holds": len(failures) == 0,
        "failure_count": len(failures),
        "failures": failures,
        "rule": (
            "0 remaining runs -> CLEAN_PASS; "
            "1 remaining run -> SPIKE_FILTERED; "
            "2+ remaining runs -> OSCILLATING_NONPERSISTENT"
        ),
    }


def summarize(records):
    flat = flatten_records(records)

    by_target = summarize_by_target(flat)
    by_remaining_run_count = summarize_by_remaining_run_count(flat)
    by_threshold = summarize_by_threshold(flat)
    rule_validation = validate_reachability_rule(flat)

    prediction_match_count = sum(
        1
        for item in flat
        if item["prediction_matches_observed"]
    )

    target_class_values = sorted(
        set(item["observed_reduced_class"] for item in flat)
    )

    remaining_count_values = sorted(
        set(item["remaining_run_count"] for item in flat)
    )

    return {
        "record_count": len(records),
        "flat_record_count": len(flat),
        "thresholds": CONFIRMATION_WINDOWS,
        "target_class_values": target_class_values,
        "remaining_run_count_values": remaining_count_values,
        "prediction_match_count": prediction_match_count,
        "prediction_match_rate": (
            prediction_match_count / max(len(flat), 1)
        ),
        "by_target": by_target,
        "by_remaining_run_count": by_remaining_run_count,
        "by_threshold": by_threshold,
        "target_reachability_rule_validation": rule_validation,
        "post_reduction_target_class_law_detected": (
            rule_validation["target_reachability_rule_holds"]
            and prediction_match_count == len(flat)
        ),
        "depth_law": (
            "minimum_target_depth = "
            "sum(max(0, run_length - "
            "(confirmation_window - 1)))"
        ),
        "target_class_law": rule_validation["rule"],
    }


def compact_record(record):
    return {
        "variant_index": record["variant_index"],
        "geometry_name": record["geometry_name"],
        "run_lengths": record["run_lengths"],
        "features": record["features"],
        "threshold_results": [
            {
                "confirmation_window": item["confirmation_window"],
                "global_persistence_threshold": (
                    item["global_persistence_threshold"]
                ),
                "source_class": item["source_class"],
                "minimum_target_depth": item["minimum_target_depth"],
                "remaining_run_count": item["remaining_run_count"],
                "remaining_run_lengths": item["remaining_run_lengths"],
                "predicted_target_class": item["predicted_target_class"],
                "observed_reduced_class": item["observed_reduced_class"],
                "prediction_matches_observed": (
                    item["prediction_matches_observed"]
                ),
            }
            for item in record["threshold_results"]
        ],
        "method": record["method"],
    }


def main():
    records = build_records()
    analysis = summarize(records)

    status = (
        "PASS"
        if analysis["post_reduction_target_class_law_detected"]
        else "CHECK"
    )

    summary = {
        "variant_count": len(records),
        "flat_record_count": analysis["flat_record_count"],
        "node_count": len(SUPPORTED_CLASSES),
        "confirmation_windows": CONFIRMATION_WINDOWS,
        "persistence_window": PERSISTENCE_WINDOW,
        "target_class_values": analysis["target_class_values"],
        "remaining_run_count_values": (
            analysis["remaining_run_count_values"]
        ),
        "prediction_match_rate": analysis["prediction_match_rate"],
        "target_reachability_rule_holds": (
            analysis["target_reachability_rule_validation"][
                "target_reachability_rule_holds"
            ]
        ),
        "post_reduction_target_class_law_detected": (
            analysis["post_reduction_target_class_law_detected"]
        ),
        "depth_law": analysis["depth_law"],
        "target_class_law": analysis["target_class_law"],
        "method": "post_reduction_target_class_law",
    }

    payload = {
        "experiment": (
            "temporal_collapse_topology_target_reachability_v0"
        ),
        "version": VERSION,
        "status": status,
        "summary": summary,
        "target_reachability_summary": analysis,
        "geometry_records": [
            compact_record(record)
            for record in records
        ],
        "interpretation": (
            "This experiment separates the depth law from the "
            "post-reduction target-class law."
        ),
        "reproduction_command": (
            "python examples/"
            "temporal_collapse_topology_target_reachability_v0.py"
        ),
    }

    RESULTS_PATH.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    RESULTS_PATH.write_text(
        json.dumps(payload, indent=2),
        encoding="utf-8",
    )

    print("=" * 80)
    print(
        "OMNIA-VALIDATION - "
        "Temporal Collapse Topology Target Reachability v0"
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
    print("By remaining run count")
    print("-" * 80)

    for count, values in (
        analysis["by_remaining_run_count"].items()
    ):
        print(
            f"remaining_run_count={count} "
            f"records={values['record_count']} "
            f"observed_classes={values['observed_class_values']} "
            f"stable={values['class_stable_for_remaining_count']}"
        )

    print()
    print("By target")
    print("-" * 80)

    for target_class, values in analysis["by_target"].items():
        print(
            f"target={target_class:<32} "
            f"records={values['record_count']} "
            f"remaining_counts={values['remaining_run_count_values']} "
            f"depth_values={values['minimum_target_depth_values']}"
        )

    print()
    print("By threshold")
    print("-" * 80)

    for threshold, values in analysis["by_threshold"].items():
        print(
            f"confirmation_window={threshold} "
            f"class_counts={values['class_counts']} "
            f"prediction_match_rate={values['prediction_match_rate']} "
            f"remaining_counts={values['remaining_run_count_values']}"
        )

    print()
    print("Geometry records")
    print("-" * 80)

    for record in records:
        compact_thresholds = []

        for item in record["threshold_results"]:
            compact_thresholds.append(
                {
                    "C": item["confirmation_window"],
                    "depth": item["minimum_target_depth"],
                    "remaining": item["remaining_run_count"],
                    "target": item["observed_reduced_class"],
                }
            )

        print(
            f"variant={record['variant_index']} "
            f"geometry={record['geometry_name']} "
            f"runs={record['run_lengths']} "
            f"results={compact_thresholds}"
        )

    print()
    print("Rule validation")
    print("-" * 80)

    rule_validation = analysis["target_reachability_rule_validation"]

    print(
        "target_reachability_rule_holds:",
        rule_validation["target_reachability_rule_holds"],
    )
    print("failure_count:", rule_validation["failure_count"])

    if rule_validation["failures"]:
        print("failures:", rule_validation["failures"])

    print()
    print("=" * 80)
    print("FINAL CHECK")
    print("=" * 80)

    if status == "PASS":
        print(
            "PASS - post-reduction target-class law detected: "
            "remaining run count determines CLEAN_PASS, "
            "SPIKE_FILTERED, or OSCILLATING_NONPERSISTENT."
        )
    else:
        print(
            "CHECK - post-reduction target-class law was not "
            "fully confirmed under tested cases."
        )

    print()
    print("=" * 80)
    print("Result saved to:", RESULTS_PATH)
    print("=" * 80)


if __name__ == "__main__":
    main()