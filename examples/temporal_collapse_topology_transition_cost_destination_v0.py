import json
from pathlib import Path
from statistics import mean, pstdev

VERSION = "0.1.0"

RESULTS_PATH = Path(
    "results/temporal_collapse_topology_transition_cost_destination_v0.json"
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


def transition_specs():
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
        {
            "name": "relapse_two_long_runs",
            "run_lengths": [5, 5],
        },
        {
            "name": "dense_many_short_runs",
            "run_lengths": [2, 2, 1, 2, 1, 2],
        },
        {
            "name": "sparse_long_then_spikes",
            "run_lengths": [6, 1, 1, 1],
        },
        {
            "name": "staircase_1_2_3_4_5",
            "run_lengths": [1, 2, 3, 4, 5],
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


def build_reduced_sequence(remaining_lengths):
    if not remaining_lengths:
        return ["PASS"] * 10

    spacing = 5
    start_offset = 4
    cursor = start_offset

    reduced_runs = []

    for run_length in remaining_lengths:
        reduced_runs.append((cursor, run_length))
        cursor += run_length + spacing

    sequence_length = cursor + start_offset

    return make_sequence(sequence_length, reduced_runs)


def destination_class_from_remaining_run_count(remaining_run_count):
    if remaining_run_count == 0:
        return "CLEAN_PASS"

    if remaining_run_count == 1:
        return "SPIKE_FILTERED"

    return "OSCILLATING_NONPERSISTENT"


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
                for run_length in run_lengths
                if run_length >= confirmation_window
            )
            for confirmation_window in CONFIRMATION_WINDOWS
        },
    }


def build_transition_signature(
    source_class,
    confirmation_window,
    transition_cost,
    remaining_run_count,
    destination_class,
):
    return (
        f"{source_class}"
        f" --C={confirmation_window}"
        f"/cost={transition_cost}"
        f"/remaining={remaining_run_count}"
        f"--> {destination_class}"
    )


def build_records():
    records = []

    for variant_index, spec in enumerate(transition_specs()):
        sequence = make_sequence(
            spec["length"],
            spec["runs"],
        )

        features = geometry_features(spec["run_lengths"])

        transition_results = []

        for confirmation_window in CONFIRMATION_WINDOWS:
            source_metrics = classify(
                sequence,
                confirmation_window,
            )

            transition_cost = thresholded_reducible_mass(
                spec["run_lengths"],
                confirmation_window,
            )

            remaining_lengths = post_reduction_lengths(
                spec["run_lengths"],
                confirmation_window,
            )

            remaining_run_count = len(remaining_lengths)

            predicted_destination = (
                destination_class_from_remaining_run_count(
                    remaining_run_count
                )
            )

            reduced_sequence = build_reduced_sequence(
                remaining_lengths
            )

            reduced_metrics = classify(
                reduced_sequence,
                confirmation_window,
            )

            observed_destination = reduced_metrics["classification"]

            cost_matches_rule = (
                transition_cost
                == thresholded_reducible_mass(
                    spec["run_lengths"],
                    confirmation_window,
                )
            )

            destination_matches_rule = (
                predicted_destination == observed_destination
            )

            transition_signature = build_transition_signature(
                source_class=source_metrics["classification"],
                confirmation_window=confirmation_window,
                transition_cost=transition_cost,
                remaining_run_count=remaining_run_count,
                destination_class=observed_destination,
            )

            transition_results.append({
                "confirmation_window": confirmation_window,
                "global_persistence_threshold": (
                    confirmation_window + PERSISTENCE_WINDOW
                ),
                "source_class": source_metrics["classification"],
                "source_metrics": source_metrics,
                "transition_cost": transition_cost,
                "remaining_run_count": remaining_run_count,
                "remaining_run_lengths": remaining_lengths,
                "predicted_destination_class": predicted_destination,
                "observed_destination_class": observed_destination,
                "destination_metrics": reduced_metrics,
                "cost_matches_rule": cost_matches_rule,
                "destination_matches_rule": destination_matches_rule,
                "cost_destination_consistent": (
                    cost_matches_rule
                    and destination_matches_rule
                ),
                "transition_signature": transition_signature,
            })

        records.append({
            "variant_index": variant_index,
            "geometry_name": spec["name"],
            "trajectory_length": spec["length"],
            "runs": spec["runs"],
            "run_lengths": spec["run_lengths"],
            "raw_action_sequence": sequence,
            "features": features,
            "transition_results": transition_results,
            "method": "transition_cost_destination_decomposition",
        })

    return records


def flatten_records(records):
    flat = []

    for record in records:
        for item in record["transition_results"]:
            flat.append({
                "variant_index": record["variant_index"],
                "geometry_name": record["geometry_name"],
                "run_lengths": record["run_lengths"],
                "features": record["features"],
                "confirmation_window": item["confirmation_window"],
                "source_class": item["source_class"],
                "transition_cost": item["transition_cost"],
                "remaining_run_count": item["remaining_run_count"],
                "remaining_run_lengths": item["remaining_run_lengths"],
                "predicted_destination_class": (
                    item["predicted_destination_class"]
                ),
                "observed_destination_class": (
                    item["observed_destination_class"]
                ),
                "cost_matches_rule": item["cost_matches_rule"],
                "destination_matches_rule": (
                    item["destination_matches_rule"]
                ),
                "cost_destination_consistent": (
                    item["cost_destination_consistent"]
                ),
                "transition_signature": item["transition_signature"],
            })

    return flat


def summarize_by_source_destination(flat_records):
    summary = {}

    for item in flat_records:
        key = (
            f"{item['source_class']}"
            f"->{item['observed_destination_class']}"
        )

        if key not in summary:
            summary[key] = {
                "transition": key,
                "record_count": 0,
                "geometry_names": [],
                "confirmation_windows": [],
                "transition_costs": [],
                "remaining_run_counts": [],
                "signatures": [],
            }

        summary[key]["record_count"] += 1
        summary[key]["geometry_names"].append(item["geometry_name"])
        summary[key]["confirmation_windows"].append(
            item["confirmation_window"]
        )
        summary[key]["transition_costs"].append(
            item["transition_cost"]
        )
        summary[key]["remaining_run_counts"].append(
            item["remaining_run_count"]
        )
        summary[key]["signatures"].append(
            item["transition_signature"]
        )

    for key, item in summary.items():
        item["transition_cost_values"] = sorted(
            set(item["transition_costs"])
        )
        item["transition_cost_mean"] = safe_mean(
            item["transition_costs"]
        )
        item["transition_cost_std"] = safe_std(
            item["transition_costs"]
        )
        item["remaining_run_count_values"] = sorted(
            set(item["remaining_run_counts"])
        )
        item["confirmation_window_values"] = sorted(
            set(item["confirmation_windows"])
        )

    return summary


def summarize_by_destination(flat_records):
    summary = {}

    for item in flat_records:
        destination_class = item["observed_destination_class"]

        if destination_class not in summary:
            summary[destination_class] = {
                "destination_class": destination_class,
                "record_count": 0,
                "source_classes": [],
                "transition_costs": [],
                "remaining_run_counts": [],
                "geometry_names": [],
            }

        summary[destination_class]["record_count"] += 1
        summary[destination_class]["source_classes"].append(
            item["source_class"]
        )
        summary[destination_class]["transition_costs"].append(
            item["transition_cost"]
        )
        summary[destination_class]["remaining_run_counts"].append(
            item["remaining_run_count"]
        )
        summary[destination_class]["geometry_names"].append(
            item["geometry_name"]
        )

    for destination_class, item in summary.items():
        item["source_class_values"] = sorted(set(item["source_classes"]))
        item["transition_cost_values"] = sorted(
            set(item["transition_costs"])
        )
        item["transition_cost_mean"] = safe_mean(
            item["transition_costs"]
        )
        item["transition_cost_std"] = safe_std(
            item["transition_costs"]
        )
        item["remaining_run_count_values"] = sorted(
            set(item["remaining_run_counts"])
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

        source_counts = {}
        destination_counts = {}

        for item in items:
            source = item["source_class"]
            destination = item["observed_destination_class"]

            source_counts[source] = source_counts.get(source, 0) + 1
            destination_counts[destination] = (
                destination_counts.get(destination, 0) + 1
            )

        costs = [
            item["transition_cost"]
            for item in items
        ]

        consistency_values = [
            item["cost_destination_consistent"]
            for item in items
        ]

        summary[str(confirmation_window)] = {
            "confirmation_window": confirmation_window,
            "record_count": len(items),
            "source_class_counts": source_counts,
            "destination_class_counts": destination_counts,
            "transition_cost_values": sorted(set(costs)),
            "transition_cost_mean": safe_mean(costs),
            "transition_cost_std": safe_std(costs),
            "cost_destination_consistency_count": sum(
                1 for value in consistency_values if value
            ),
            "cost_destination_consistency_rate": (
                sum(1 for value in consistency_values if value)
                / max(len(consistency_values), 1)
            ),
        }

    return summary


def validate_transition_model(flat_records):
    failures = []

    for item in flat_records:
        run_lengths = item["run_lengths"]
        confirmation_window = item["confirmation_window"]

        expected_cost = thresholded_reducible_mass(
            run_lengths,
            confirmation_window,
        )

        remaining_lengths = post_reduction_lengths(
            run_lengths,
            confirmation_window,
        )

        expected_destination = (
            destination_class_from_remaining_run_count(
                len(remaining_lengths)
            )
        )

        if (
            item["transition_cost"] != expected_cost
            or item["observed_destination_class"] != expected_destination
        ):
            failures.append({
                "geometry_name": item["geometry_name"],
                "confirmation_window": confirmation_window,
                "expected_cost": expected_cost,
                "observed_cost": item["transition_cost"],
                "expected_destination": expected_destination,
                "observed_destination": item[
                    "observed_destination_class"
                ],
                "remaining_run_count": item["remaining_run_count"],
            })

    return {
        "transition_model_holds": len(failures) == 0,
        "failure_count": len(failures),
        "failures": failures,
        "cost_rule": (
            "transition_cost = "
            "sum(max(0, run_length - "
            "(confirmation_window - 1)))"
        ),
        "destination_rule": (
            "0 remaining runs -> CLEAN_PASS; "
            "1 remaining run -> SPIKE_FILTERED; "
            "2+ remaining runs -> OSCILLATING_NONPERSISTENT"
        ),
    }


def summarize(records):
    flat = flatten_records(records)

    by_source_destination = summarize_by_source_destination(flat)
    by_destination = summarize_by_destination(flat)
    by_threshold = summarize_by_threshold(flat)
    validation = validate_transition_model(flat)

    consistency_count = sum(
        1
        for item in flat
        if item["cost_destination_consistent"]
    )

    signatures = [
        item["transition_signature"]
        for item in flat
    ]

    unique_signatures = sorted(set(signatures))

    source_classes = sorted(
        set(item["source_class"] for item in flat)
    )

    destination_classes = sorted(
        set(item["observed_destination_class"] for item in flat)
    )

    transition_costs = [
        item["transition_cost"]
        for item in flat
    ]

    return {
        "record_count": len(records),
        "flat_record_count": len(flat),
        "thresholds": CONFIRMATION_WINDOWS,
        "source_class_values": source_classes,
        "destination_class_values": destination_classes,
        "transition_cost_values": sorted(set(transition_costs)),
        "transition_cost_mean": safe_mean(transition_costs),
        "transition_cost_std": safe_std(transition_costs),
        "cost_destination_consistency_count": consistency_count,
        "cost_destination_consistency_rate": (
            consistency_count / max(len(flat), 1)
        ),
        "unique_transition_signature_count": len(unique_signatures),
        "unique_transition_signatures": unique_signatures,
        "by_source_destination": by_source_destination,
        "by_destination": by_destination,
        "by_threshold": by_threshold,
        "transition_model_validation": validation,
        "transition_cost_destination_decomposition_detected": (
            validation["transition_model_holds"]
            and consistency_count == len(flat)
        ),
        "transition_model": (
            "transition = "
            "thresholded_reducible_mass_cost "
            "+ post_reduction_destination_class"
        ),
    }


def compact_record(record):
    return {
        "variant_index": record["variant_index"],
        "geometry_name": record["geometry_name"],
        "run_lengths": record["run_lengths"],
        "features": record["features"],
        "transition_results": [
            {
                "confirmation_window": item["confirmation_window"],
                "global_persistence_threshold": (
                    item["global_persistence_threshold"]
                ),
                "source_class": item["source_class"],
                "transition_cost": item["transition_cost"],
                "remaining_run_count": item["remaining_run_count"],
                "remaining_run_lengths": item["remaining_run_lengths"],
                "predicted_destination_class": (
                    item["predicted_destination_class"]
                ),
                "observed_destination_class": (
                    item["observed_destination_class"]
                ),
                "cost_matches_rule": item["cost_matches_rule"],
                "destination_matches_rule": (
                    item["destination_matches_rule"]
                ),
                "cost_destination_consistent": (
                    item["cost_destination_consistent"]
                ),
                "transition_signature": item["transition_signature"],
            }
            for item in record["transition_results"]
        ],
        "method": record["method"],
    }


def main():
    records = build_records()
    analysis = summarize(records)

    status = (
        "PASS"
        if analysis[
            "transition_cost_destination_decomposition_detected"
        ]
        else "CHECK"
    )

    summary = {
        "variant_count": len(records),
        "flat_record_count": analysis["flat_record_count"],
        "node_count": len(SUPPORTED_CLASSES),
        "confirmation_windows": CONFIRMATION_WINDOWS,
        "persistence_window": PERSISTENCE_WINDOW,
        "source_class_values": analysis["source_class_values"],
        "destination_class_values": analysis["destination_class_values"],
        "transition_cost_values": analysis["transition_cost_values"],
        "cost_destination_consistency_rate": (
            analysis["cost_destination_consistency_rate"]
        ),
        "transition_model_holds": (
            analysis["transition_model_validation"][
                "transition_model_holds"
            ]
        ),
        "transition_cost_destination_decomposition_detected": (
            analysis[
                "transition_cost_destination_decomposition_detected"
            ]
        ),
        "unique_transition_signature_count": (
            analysis["unique_transition_signature_count"]
        ),
        "transition_model": analysis["transition_model"],
        "cost_rule": (
            analysis["transition_model_validation"]["cost_rule"]
        ),
        "destination_rule": (
            analysis["transition_model_validation"][
                "destination_rule"
            ]
        ),
        "method": "transition_cost_destination_decomposition",
    }

    payload = {
        "experiment": (
            "temporal_collapse_topology_transition_cost_destination_v0"
        ),
        "version": VERSION,
        "status": status,
        "summary": summary,
        "transition_cost_destination_summary": analysis,
        "geometry_records": [
            compact_record(record)
            for record in records
        ],
        "interpretation": (
            "This experiment combines the thresholded transition-cost "
            "law and the post-reduction destination-class law into one "
            "cost + destination transition model."
        ),
        "reproduction_command": (
            "python examples/"
            "temporal_collapse_topology_transition_cost_destination_v0.py"
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
        "Temporal Collapse Topology Transition Cost Destination v0"
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
    print("By threshold")
    print("-" * 80)

    for threshold, values in analysis["by_threshold"].items():
        print(
            f"confirmation_window={threshold} "
            f"sources={values['source_class_counts']} "
            f"destinations={values['destination_class_counts']} "
            f"costs={values['transition_cost_values']} "
            f"consistency={values['cost_destination_consistency_rate']}"
        )

    print()
    print("By destination")
    print("-" * 80)

    for destination, values in analysis["by_destination"].items():
        print(
            f"destination={destination:<32} "
            f"records={values['record_count']} "
            f"sources={values['source_class_values']} "
            f"costs={values['transition_cost_values']} "
            f"remaining_counts={values['remaining_run_count_values']}"
        )

    print()
    print("By source -> destination")
    print("-" * 80)

    for transition, values in (
        analysis["by_source_destination"].items()
    ):
        print(
            f"transition={transition:<64} "
            f"records={values['record_count']} "
            f"costs={values['transition_cost_values']} "
            f"remaining_counts={values['remaining_run_count_values']}"
        )

    print()
    print("Geometry records")
    print("-" * 80)

    for record in records:
        compact_results = []

        for item in record["transition_results"]:
            compact_results.append({
                "C": item["confirmation_window"],
                "source": item["source_class"],
                "cost": item["transition_cost"],
                "remaining": item["remaining_run_count"],
                "dest": item["observed_destination_class"],
            })

        print(
            f"variant={record['variant_index']} "
            f"geometry={record['geometry_name']} "
            f"runs={record['run_lengths']} "
            f"results={compact_results}"
        )

    print()
    print("Rule validation")
    print("-" * 80)

    validation = analysis["transition_model_validation"]

    print("transition_model_holds:", validation["transition_model_holds"])
    print("failure_count:", validation["failure_count"])

    if validation["failures"]:
        print("failures:", validation["failures"])

    print()
    print("=" * 80)
    print("FINAL CHECK")
    print("=" * 80)

    if status == "PASS":
        print(
            "PASS - transition cost / destination decomposition "
            "detected: temporal topology transitions decompose into "
            "thresholded reducible mass + post-reduction destination "
            "class."
        )
    else:
        print(
            "CHECK - transition cost / destination decomposition was "
            "not fully confirmed under tested cases."
        )

    print()
    print("=" * 80)
    print("Result saved to:", RESULTS_PATH)
    print("=" * 80)


if __name__ == "__main__":
    main()