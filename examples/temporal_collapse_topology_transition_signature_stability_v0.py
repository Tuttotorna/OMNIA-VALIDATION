import json
from pathlib import Path
from statistics import mean, pstdev

VERSION = "0.1.0"

RESULTS_PATH = Path(
    "results/temporal_collapse_topology_transition_signature_stability_v0.json"
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


def signature_stability_specs():
    return [
        {
            "family": "single_run",
            "name": "single_run_len_2",
            "run_lengths": [2],
        },
        {
            "family": "single_run",
            "name": "single_run_len_3",
            "run_lengths": [3],
        },
        {
            "family": "single_run",
            "name": "single_run_len_4",
            "run_lengths": [4],
        },
        {
            "family": "single_run",
            "name": "single_run_len_5",
            "run_lengths": [5],
        },
        {
            "family": "two_equal_runs",
            "name": "two_runs_len_2_2",
            "run_lengths": [2, 2],
        },
        {
            "family": "two_equal_runs",
            "name": "two_runs_len_3_3",
            "run_lengths": [3, 3],
        },
        {
            "family": "two_equal_runs",
            "name": "two_runs_len_4_4",
            "run_lengths": [4, 4],
        },
        {
            "family": "two_equal_runs",
            "name": "two_runs_len_5_5",
            "run_lengths": [5, 5],
        },
        {
            "family": "three_equal_runs",
            "name": "three_runs_len_2_2_2",
            "run_lengths": [2, 2, 2],
        },
        {
            "family": "three_equal_runs",
            "name": "three_runs_len_3_3_3",
            "run_lengths": [3, 3, 3],
        },
        {
            "family": "three_equal_runs",
            "name": "three_runs_len_4_4_4",
            "run_lengths": [4, 4, 4],
        },
        {
            "family": "three_equal_runs",
            "name": "three_runs_len_5_5_5",
            "run_lengths": [5, 5, 5],
        },
        {
            "family": "mixed_staircase",
            "name": "staircase_1_2_3_4",
            "run_lengths": [1, 2, 3, 4],
        },
        {
            "family": "mixed_staircase",
            "name": "staircase_1_2_3_4_5",
            "run_lengths": [1, 2, 3, 4, 5],
        },
        {
            "family": "mixed_staircase",
            "name": "staircase_2_3_4_5",
            "run_lengths": [2, 3, 4, 5],
        },
        {
            "family": "mixed_staircase",
            "name": "staircase_2_3_4_5_6",
            "run_lengths": [2, 3, 4, 5, 6],
        },
        {
            "family": "spike_plus_long",
            "name": "long_then_spikes_4_1_1",
            "run_lengths": [4, 1, 1],
        },
        {
            "family": "spike_plus_long",
            "name": "long_then_spikes_5_1_1",
            "run_lengths": [5, 1, 1],
        },
        {
            "family": "spike_plus_long",
            "name": "long_then_spikes_6_1_1_1",
            "run_lengths": [6, 1, 1, 1],
        },
        {
            "family": "spike_plus_long",
            "name": "long_then_spikes_7_1_1_1",
            "run_lengths": [7, 1, 1, 1],
        },
        {
            "family": "dense_short",
            "name": "dense_short_2_1_2_1",
            "run_lengths": [2, 1, 2, 1],
        },
        {
            "family": "dense_short",
            "name": "dense_short_2_2_1_2_1",
            "run_lengths": [2, 2, 1, 2, 1],
        },
        {
            "family": "dense_short",
            "name": "dense_short_2_2_1_2_1_2",
            "run_lengths": [2, 2, 1, 2, 1, 2],
        },
        {
            "family": "dense_short",
            "name": "dense_short_3_2_1_2_1_2",
            "run_lengths": [3, 2, 1, 2, 1, 2],
        },
    ]


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
    collapse_run_count = len(run_lengths)
    total_collapse_frames = sum(run_lengths)

    return {
        "collapse_run_count": collapse_run_count,
        "run_lengths": run_lengths,
        "run_length_mean": safe_mean(run_lengths),
        "run_length_std": safe_std(run_lengths),
        "max_run_length": max(run_lengths) if run_lengths else 0,
        "min_run_length": min(run_lengths) if run_lengths else 0,
        "total_collapse_frames": total_collapse_frames,
        "mass_per_run": (
            total_collapse_frames / max(collapse_run_count, 1)
        ),
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


def build_signature_core(
    transition_cost,
    remaining_run_count,
    destination_class,
):
    return (
        f"cost={transition_cost}"
        f"/remaining={remaining_run_count}"
        f"--> {destination_class}"
    )


def build_records():
    records = []

    for variant_index, spec in enumerate(signature_stability_specs()):
        length, runs = make_sequence_from_lengths(spec["run_lengths"])
        sequence = make_sequence(length, runs)

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

            destination_metrics = classify(
                reduced_sequence,
                confirmation_window,
            )

            observed_destination = destination_metrics["classification"]

            transition_signature = build_transition_signature(
                source_class=source_metrics["classification"],
                confirmation_window=confirmation_window,
                transition_cost=transition_cost,
                remaining_run_count=remaining_run_count,
                destination_class=observed_destination,
            )

            signature_core = build_signature_core(
                transition_cost=transition_cost,
                remaining_run_count=remaining_run_count,
                destination_class=observed_destination,
            )

            cost_destination_consistent = (
                observed_destination == predicted_destination
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
                "destination_metrics": destination_metrics,
                "cost_destination_consistent": (
                    cost_destination_consistent
                ),
                "transition_signature": transition_signature,
                "signature_core": signature_core,
            })

        records.append({
            "variant_index": variant_index,
            "family": spec["family"],
            "geometry_name": spec["name"],
            "run_lengths": spec["run_lengths"],
            "trajectory_length": length,
            "runs": runs,
            "raw_action_sequence": sequence,
            "features": features,
            "transition_results": transition_results,
            "method": "transition_signature_stability_map",
        })

    return records


def flatten_records(records):
    flat = []

    for record in records:
        for item in record["transition_results"]:
            flat.append({
                "variant_index": record["variant_index"],
                "family": record["family"],
                "geometry_name": record["geometry_name"],
                "run_lengths": record["run_lengths"],
                "features": record["features"],
                "confirmation_window": item["confirmation_window"],
                "source_class": item["source_class"],
                "transition_cost": item["transition_cost"],
                "remaining_run_count": item["remaining_run_count"],
                "remaining_run_lengths": item["remaining_run_lengths"],
                "observed_destination_class": (
                    item["observed_destination_class"]
                ),
                "cost_destination_consistent": (
                    item["cost_destination_consistent"]
                ),
                "transition_signature": item["transition_signature"],
                "signature_core": item["signature_core"],
            })

    return flat


def summarize_by_family(records):
    summary = {}

    for record in records:
        family = record["family"]

        if family not in summary:
            summary[family] = {
                "family": family,
                "variant_count": 0,
                "geometry_names": [],
                "signatures_by_threshold": {
                    str(confirmation_window): []
                    for confirmation_window in CONFIRMATION_WINDOWS
                },
                "signature_cores_by_threshold": {
                    str(confirmation_window): []
                    for confirmation_window in CONFIRMATION_WINDOWS
                },
                "costs_by_threshold": {
                    str(confirmation_window): []
                    for confirmation_window in CONFIRMATION_WINDOWS
                },
                "destinations_by_threshold": {
                    str(confirmation_window): []
                    for confirmation_window in CONFIRMATION_WINDOWS
                },
                "remaining_counts_by_threshold": {
                    str(confirmation_window): []
                    for confirmation_window in CONFIRMATION_WINDOWS
                },
            }

        summary[family]["variant_count"] += 1
        summary[family]["geometry_names"].append(
            record["geometry_name"]
        )

        for item in record["transition_results"]:
            threshold_key = str(item["confirmation_window"])

            summary[family]["signatures_by_threshold"][
                threshold_key
            ].append(item["transition_signature"])

            summary[family]["signature_cores_by_threshold"][
                threshold_key
            ].append(item["signature_core"])

            summary[family]["costs_by_threshold"][
                threshold_key
            ].append(item["transition_cost"])

            summary[family]["destinations_by_threshold"][
                threshold_key
            ].append(item["observed_destination_class"])

            summary[family]["remaining_counts_by_threshold"][
                threshold_key
            ].append(item["remaining_run_count"])

    for family, item in summary.items():
        signature_stability_by_threshold = {}
        core_stability_by_threshold = {}
        destination_stability_by_threshold = {}
        remaining_count_stability_by_threshold = {}
        cost_stats_by_threshold = {}

        for confirmation_window in CONFIRMATION_WINDOWS:
            threshold_key = str(confirmation_window)

            signatures = item["signatures_by_threshold"][threshold_key]
            cores = item["signature_cores_by_threshold"][threshold_key]
            destinations = item["destinations_by_threshold"][threshold_key]
            remaining_counts = item["remaining_counts_by_threshold"][
                threshold_key
            ]
            costs = item["costs_by_threshold"][threshold_key]

            signature_stability_by_threshold[threshold_key] = {
                "unique_count": len(set(signatures)),
                "stable": len(set(signatures)) == 1,
                "unique_values": sorted(set(signatures)),
            }

            core_stability_by_threshold[threshold_key] = {
                "unique_count": len(set(cores)),
                "stable": len(set(cores)) == 1,
                "unique_values": sorted(set(cores)),
            }

            destination_stability_by_threshold[threshold_key] = {
                "unique_count": len(set(destinations)),
                "stable": len(set(destinations)) == 1,
                "unique_values": sorted(set(destinations)),
            }

            remaining_count_stability_by_threshold[threshold_key] = {
                "unique_count": len(set(remaining_counts)),
                "stable": len(set(remaining_counts)) == 1,
                "unique_values": sorted(set(remaining_counts)),
            }

            cost_stats_by_threshold[threshold_key] = {
                "cost_values": sorted(set(costs)),
                "cost_mean": safe_mean(costs),
                "cost_std": safe_std(costs),
                "cost_stable": len(set(costs)) == 1,
            }

        full_signatures = [
            signature
            for signatures in item["signatures_by_threshold"].values()
            for signature in signatures
        ]

        full_cores = [
            core
            for cores in item["signature_cores_by_threshold"].values()
            for core in cores
        ]

        item["signature_stability_by_threshold"] = (
            signature_stability_by_threshold
        )
        item["core_stability_by_threshold"] = core_stability_by_threshold
        item["destination_stability_by_threshold"] = (
            destination_stability_by_threshold
        )
        item["remaining_count_stability_by_threshold"] = (
            remaining_count_stability_by_threshold
        )
        item["cost_stats_by_threshold"] = cost_stats_by_threshold
        item["family_unique_signature_count"] = len(set(full_signatures))
        item["family_unique_core_count"] = len(set(full_cores))

        stable_thresholds = sum(
            1
            for value in core_stability_by_threshold.values()
            if value["stable"]
        )

        item["stable_core_threshold_count"] = stable_thresholds
        item["core_stability_rate"] = (
            stable_thresholds / max(len(CONFIRMATION_WINDOWS), 1)
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

        signatures = [
            item["transition_signature"]
            for item in items
        ]

        cores = [
            item["signature_core"]
            for item in items
        ]

        costs = [
            item["transition_cost"]
            for item in items
        ]

        destinations = [
            item["observed_destination_class"]
            for item in items
        ]

        consistency_values = [
            item["cost_destination_consistent"]
            for item in items
        ]

        destination_counts = {}

        for destination in destinations:
            destination_counts[destination] = (
                destination_counts.get(destination, 0) + 1
            )

        summary[str(confirmation_window)] = {
            "confirmation_window": confirmation_window,
            "record_count": len(items),
            "unique_transition_signature_count": len(set(signatures)),
            "unique_signature_core_count": len(set(cores)),
            "transition_cost_values": sorted(set(costs)),
            "transition_cost_mean": safe_mean(costs),
            "transition_cost_std": safe_std(costs),
            "destination_class_counts": destination_counts,
            "cost_destination_consistency_rate": (
                sum(1 for value in consistency_values if value)
                / max(len(consistency_values), 1)
            ),
        }

    return summary


def summarize_signature_clusters(flat_records):
    clusters = {}

    for item in flat_records:
        signature_core = item["signature_core"]

        if signature_core not in clusters:
            clusters[signature_core] = {
                "signature_core": signature_core,
                "record_count": 0,
                "families": [],
                "geometry_names": [],
                "confirmation_windows": [],
                "source_classes": [],
                "transition_costs": [],
                "remaining_run_counts": [],
                "destination_classes": [],
            }

        clusters[signature_core]["record_count"] += 1
        clusters[signature_core]["families"].append(item["family"])
        clusters[signature_core]["geometry_names"].append(
            item["geometry_name"]
        )
        clusters[signature_core]["confirmation_windows"].append(
            item["confirmation_window"]
        )
        clusters[signature_core]["source_classes"].append(
            item["source_class"]
        )
        clusters[signature_core]["transition_costs"].append(
            item["transition_cost"]
        )
        clusters[signature_core]["remaining_run_counts"].append(
            item["remaining_run_count"]
        )
        clusters[signature_core]["destination_classes"].append(
            item["observed_destination_class"]
        )

    for signature_core, item in clusters.items():
        item["family_values"] = sorted(set(item["families"]))
        item["confirmation_window_values"] = sorted(
            set(item["confirmation_windows"])
        )
        item["source_class_values"] = sorted(set(item["source_classes"]))
        item["transition_cost_values"] = sorted(
            set(item["transition_costs"])
        )
        item["remaining_run_count_values"] = sorted(
            set(item["remaining_run_counts"])
        )
        item["destination_class_values"] = sorted(
            set(item["destination_classes"])
        )

    return clusters


def validate_signature_consistency(flat_records):
    failures = []

    for item in flat_records:
        expected_cost = thresholded_reducible_mass(
            item["run_lengths"],
            item["confirmation_window"],
        )

        expected_remaining_lengths = post_reduction_lengths(
            item["run_lengths"],
            item["confirmation_window"],
        )

        expected_remaining_count = len(expected_remaining_lengths)

        expected_destination = (
            destination_class_from_remaining_run_count(
                expected_remaining_count
            )
        )

        expected_core = build_signature_core(
            transition_cost=expected_cost,
            remaining_run_count=expected_remaining_count,
            destination_class=expected_destination,
        )

        if (
            item["transition_cost"] != expected_cost
            or item["remaining_run_count"] != expected_remaining_count
            or item["observed_destination_class"] != expected_destination
            or item["signature_core"] != expected_core
        ):
            failures.append({
                "geometry_name": item["geometry_name"],
                "confirmation_window": item["confirmation_window"],
                "expected_cost": expected_cost,
                "observed_cost": item["transition_cost"],
                "expected_remaining_count": expected_remaining_count,
                "observed_remaining_count": item[
                    "remaining_run_count"
                ],
                "expected_destination": expected_destination,
                "observed_destination": item[
                    "observed_destination_class"
                ],
                "expected_core": expected_core,
                "observed_core": item["signature_core"],
            })

    return {
        "signature_consistency_holds": len(failures) == 0,
        "failure_count": len(failures),
        "failures": failures,
        "signature_core_rule": (
            "signature_core = "
            "cost=<thresholded_reducible_mass>/"
            "remaining=<remaining_run_count>--> "
            "<post_reduction_destination_class>"
        ),
    }


def summarize(records):
    flat = flatten_records(records)

    by_family = summarize_by_family(records)
    by_threshold = summarize_by_threshold(flat)
    signature_clusters = summarize_signature_clusters(flat)
    validation = validate_signature_consistency(flat)

    signatures = [
        item["transition_signature"]
        for item in flat
    ]

    cores = [
        item["signature_core"]
        for item in flat
    ]

    families = sorted(
        set(item["family"] for item in flat)
    )

    stable_family_count = sum(
        1
        for item in by_family.values()
        if item["core_stability_rate"] == 1.0
    )

    partially_stable_family_count = sum(
        1
        for item in by_family.values()
        if 0 < item["core_stability_rate"] < 1.0
    )

    unstable_family_count = sum(
        1
        for item in by_family.values()
        if item["core_stability_rate"] == 0.0
    )

    consistency_count = sum(
        1
        for item in flat
        if item["cost_destination_consistent"]
    )

    transition_signature_stability_map_detected = (
        validation["signature_consistency_holds"]
        and consistency_count == len(flat)
        and len(signature_clusters) > 0
    )

    return {
        "record_count": len(records),
        "flat_record_count": len(flat),
        "thresholds": CONFIRMATION_WINDOWS,
        "family_values": families,
        "family_count": len(families),
        "unique_transition_signature_count": len(set(signatures)),
        "unique_signature_core_count": len(set(cores)),
        "signature_cluster_count": len(signature_clusters),
        "stable_family_count": stable_family_count,
        "partially_stable_family_count": partially_stable_family_count,
        "unstable_family_count": unstable_family_count,
        "cost_destination_consistency_count": consistency_count,
        "cost_destination_consistency_rate": (
            consistency_count / max(len(flat), 1)
        ),
        "by_family": by_family,
        "by_threshold": by_threshold,
        "signature_clusters": signature_clusters,
        "signature_consistency_validation": validation,
        "transition_signature_stability_map_detected": (
            transition_signature_stability_map_detected
        ),
        "signature_definition": (
            "SOURCE_CLASS --C=<confirmation_window>/"
            "cost=<transition_cost>/"
            "remaining=<remaining_run_count>--> DESTINATION_CLASS"
        ),
        "signature_core_definition": (
            "cost=<transition_cost>/"
            "remaining=<remaining_run_count>--> DESTINATION_CLASS"
        ),
    }


def compact_record(record):
    return {
        "variant_index": record["variant_index"],
        "family": record["family"],
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
                "observed_destination_class": (
                    item["observed_destination_class"]
                ),
                "cost_destination_consistent": (
                    item["cost_destination_consistent"]
                ),
                "transition_signature": item["transition_signature"],
                "signature_core": item["signature_core"],
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
            "transition_signature_stability_map_detected"
        ]
        else "CHECK"
    )

    summary = {
        "variant_count": len(records),
        "flat_record_count": analysis["flat_record_count"],
        "node_count": len(SUPPORTED_CLASSES),
        "confirmation_windows": CONFIRMATION_WINDOWS,
        "persistence_window": PERSISTENCE_WINDOW,
        "family_count": analysis["family_count"],
        "family_values": analysis["family_values"],
        "unique_transition_signature_count": (
            analysis["unique_transition_signature_count"]
        ),
        "unique_signature_core_count": (
            analysis["unique_signature_core_count"]
        ),
        "signature_cluster_count": analysis["signature_cluster_count"],
        "stable_family_count": analysis["stable_family_count"],
        "partially_stable_family_count": (
            analysis["partially_stable_family_count"]
        ),
        "unstable_family_count": analysis["unstable_family_count"],
        "cost_destination_consistency_rate": (
            analysis["cost_destination_consistency_rate"]
        ),
        "signature_consistency_holds": (
            analysis["signature_consistency_validation"][
                "signature_consistency_holds"
            ]
        ),
        "transition_signature_stability_map_detected": (
            analysis[
                "transition_signature_stability_map_detected"
            ]
        ),
        "signature_definition": analysis["signature_definition"],
        "signature_core_definition": (
            analysis["signature_core_definition"]
        ),
        "method": "transition_signature_stability_map",
    }

    payload = {
        "experiment": (
            "temporal_collapse_topology_transition_signature_stability_v0"
        ),
        "version": VERSION,
        "status": status,
        "summary": summary,
        "transition_signature_stability_summary": analysis,
        "geometry_records": [
            compact_record(record)
            for record in records
        ],
        "interpretation": (
            "This experiment tests whether transition signatures and "
            "signature cores remain structurally consistent under "
            "controlled run-length geometry perturbations."
        ),
        "reproduction_command": (
            "python examples/"
            "temporal_collapse_topology_transition_signature_stability_v0.py"
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
        "Temporal Collapse Topology Transition Signature Stability v0"
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
            f"records={values['record_count']} "
            f"unique_signatures={values['unique_transition_signature_count']} "
            f"unique_cores={values['unique_signature_core_count']} "
            f"costs={values['transition_cost_values']} "
            f"destinations={values['destination_class_counts']} "
            f"consistency={values['cost_destination_consistency_rate']}"
        )

    print()
    print("By family")
    print("-" * 80)

    for family, values in analysis["by_family"].items():
        print(
            f"family={family:<24} "
            f"variants={values['variant_count']} "
            f"unique_signatures={values['family_unique_signature_count']} "
            f"unique_cores={values['family_unique_core_count']} "
            f"core_stability_rate={values['core_stability_rate']}"
        )

        for threshold, core_values in (
            values["core_stability_by_threshold"].items()
        ):
            print(
                f"  C={threshold} "
                f"core_unique={core_values['unique_count']} "
                f"stable={core_values['stable']} "
                f"cores={core_values['unique_values']}"
            )

    print()
    print("Signature clusters")
    print("-" * 80)

    for signature_core, values in analysis["signature_clusters"].items():
        print(
            f"core={signature_core:<52} "
            f"records={values['record_count']} "
            f"families={values['family_values']} "
            f"C={values['confirmation_window_values']} "
            f"sources={values['source_class_values']}"
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
                "core": item["signature_core"],
            })

        print(
            f"variant={record['variant_index']} "
            f"family={record['family']} "
            f"geometry={record['geometry_name']} "
            f"runs={record['run_lengths']} "
            f"results={compact_results}"
        )

    print()
    print("Rule validation")
    print("-" * 80)

    validation = analysis["signature_consistency_validation"]

    print(
        "signature_consistency_holds:",
        validation["signature_consistency_holds"],
    )
    print("failure_count:", validation["failure_count"])

    if validation["failures"]:
        print("failures:", validation["failures"])

    print()
    print("=" * 80)
    print("FINAL CHECK")
    print("=" * 80)

    if status == "PASS":
        print(
            "PASS - transition-signature stability map detected: "
            "signature cores remained internally consistent while "
            "family-level stability exposed perturbation-sensitive "
            "signature clusters."
        )
    else:
        print(
            "CHECK - transition-signature stability map was not fully "
            "confirmed under tested geometry perturbations."
        )

    print()
    print("=" * 80)
    print("Result saved to:", RESULTS_PATH)
    print("=" * 80)


if __name__ == "__main__":
    main()