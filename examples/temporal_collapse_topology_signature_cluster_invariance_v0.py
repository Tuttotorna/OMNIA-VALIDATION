import json
from pathlib import Path
from statistics import mean, pstdev

VERSION = "0.1.0"

RESULTS_PATH = Path(
    "results/temporal_collapse_topology_signature_cluster_invariance_v0.json"
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


def cluster_invariance_specs():
    return [
        {
            "family": "single_run",
            "name": "single_run_len_1",
            "run_lengths": [1],
        },
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
            "name": "two_runs_len_1_1",
            "run_lengths": [1, 1],
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
            "family": "three_equal_runs",
            "name": "three_runs_len_1_1_1",
            "run_lengths": [1, 1, 1],
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
            "family": "mixed_same_cost",
            "name": "mixed_1_2_3",
            "run_lengths": [1, 2, 3],
        },
        {
            "family": "mixed_same_cost",
            "name": "mixed_1_1_4",
            "run_lengths": [1, 1, 4],
        },
        {
            "family": "mixed_same_cost",
            "name": "mixed_2_2_2",
            "run_lengths": [2, 2, 2],
        },
        {
            "family": "mixed_same_cost",
            "name": "mixed_1_3_2",
            "run_lengths": [1, 3, 2],
        },
        {
            "family": "staircase",
            "name": "staircase_1_2_3_4",
            "run_lengths": [1, 2, 3, 4],
        },
        {
            "family": "staircase",
            "name": "staircase_1_2_3_4_5",
            "run_lengths": [1, 2, 3, 4, 5],
        },
        {
            "family": "staircase",
            "name": "staircase_2_3_4_5",
            "run_lengths": [2, 3, 4, 5],
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


def build_cluster_id(
    transition_cost,
    remaining_run_count,
    destination_class,
):
    return (
        f"cost={transition_cost}"
        f"|remaining={remaining_run_count}"
        f"|dest={destination_class}"
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


def build_records():
    records = []

    for variant_index, spec in enumerate(cluster_invariance_specs()):
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

            cluster_id = build_cluster_id(
                transition_cost=transition_cost,
                remaining_run_count=remaining_run_count,
                destination_class=observed_destination,
            )

            signature_core = build_signature_core(
                transition_cost=transition_cost,
                remaining_run_count=remaining_run_count,
                destination_class=observed_destination,
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
                "destination_metrics": destination_metrics,
                "cluster_id": cluster_id,
                "signature_core": signature_core,
                "transition_signature": transition_signature,
                "destination_matches_rule": (
                    predicted_destination == observed_destination
                ),
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
            "method": "signature_cluster_invariance",
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
                "predicted_destination_class": (
                    item["predicted_destination_class"]
                ),
                "destination_matches_rule": (
                    item["destination_matches_rule"]
                ),
                "cluster_id": item["cluster_id"],
                "signature_core": item["signature_core"],
                "transition_signature": item["transition_signature"],
            })

    return flat


def summarize_clusters(flat_records):
    clusters = {}

    for item in flat_records:
        cluster_id = item["cluster_id"]

        if cluster_id not in clusters:
            clusters[cluster_id] = {
                "cluster_id": cluster_id,
                "record_count": 0,
                "families": [],
                "geometry_names": [],
                "confirmation_windows": [],
                "source_classes": [],
                "transition_costs": [],
                "remaining_run_counts": [],
                "destination_classes": [],
                "signature_cores": [],
                "transition_signatures": [],
            }

        clusters[cluster_id]["record_count"] += 1
        clusters[cluster_id]["families"].append(item["family"])
        clusters[cluster_id]["geometry_names"].append(
            item["geometry_name"]
        )
        clusters[cluster_id]["confirmation_windows"].append(
            item["confirmation_window"]
        )
        clusters[cluster_id]["source_classes"].append(
            item["source_class"]
        )
        clusters[cluster_id]["transition_costs"].append(
            item["transition_cost"]
        )
        clusters[cluster_id]["remaining_run_counts"].append(
            item["remaining_run_count"]
        )
        clusters[cluster_id]["destination_classes"].append(
            item["observed_destination_class"]
        )
        clusters[cluster_id]["signature_cores"].append(
            item["signature_core"]
        )
        clusters[cluster_id]["transition_signatures"].append(
            item["transition_signature"]
        )

    for cluster_id, item in clusters.items():
        item["family_values"] = sorted(set(item["families"]))
        item["geometry_name_values"] = sorted(
            set(item["geometry_names"])
        )
        item["confirmation_window_values"] = sorted(
            set(item["confirmation_windows"])
        )
        item["source_class_values"] = sorted(
            set(item["source_classes"])
        )
        item["transition_cost_values"] = sorted(
            set(item["transition_costs"])
        )
        item["remaining_run_count_values"] = sorted(
            set(item["remaining_run_counts"])
        )
        item["destination_class_values"] = sorted(
            set(item["destination_classes"])
        )
        item["signature_core_values"] = sorted(
            set(item["signature_cores"])
        )
        item["transition_signature_values"] = sorted(
            set(item["transition_signatures"])
        )

        item["signature_core_consistent"] = (
            len(item["signature_core_values"]) == 1
        )

        item["cluster_id_invariant"] = (
            len(item["transition_cost_values"]) == 1
            and len(item["remaining_run_count_values"]) == 1
            and len(item["destination_class_values"]) == 1
            and item["signature_core_consistent"]
        )

        item["family_crossing"] = len(item["family_values"]) > 1
        item["source_class_variation"] = (
            len(item["source_class_values"]) > 1
        )
        item["threshold_crossing"] = (
            len(item["confirmation_window_values"]) > 1
        )

    return clusters


def summarize_by_family(flat_records):
    summary = {}

    for item in flat_records:
        family = item["family"]

        if family not in summary:
            summary[family] = {
                "family": family,
                "record_count": 0,
                "geometry_names": [],
                "cluster_ids": [],
                "signature_cores": [],
                "transition_costs": [],
                "remaining_run_counts": [],
                "destination_classes": [],
            }

        summary[family]["record_count"] += 1
        summary[family]["geometry_names"].append(item["geometry_name"])
        summary[family]["cluster_ids"].append(item["cluster_id"])
        summary[family]["signature_cores"].append(item["signature_core"])
        summary[family]["transition_costs"].append(
            item["transition_cost"]
        )
        summary[family]["remaining_run_counts"].append(
            item["remaining_run_count"]
        )
        summary[family]["destination_classes"].append(
            item["observed_destination_class"]
        )

    for family, item in summary.items():
        item["geometry_name_values"] = sorted(
            set(item["geometry_names"])
        )
        item["cluster_id_values"] = sorted(set(item["cluster_ids"]))
        item["signature_core_values"] = sorted(
            set(item["signature_cores"])
        )
        item["transition_cost_values"] = sorted(
            set(item["transition_costs"])
        )
        item["remaining_run_count_values"] = sorted(
            set(item["remaining_run_counts"])
        )
        item["destination_class_values"] = sorted(
            set(item["destination_classes"])
        )
        item["cluster_count"] = len(item["cluster_id_values"])
        item["signature_core_count"] = len(
            item["signature_core_values"]
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

        cluster_ids = [
            item["cluster_id"]
            for item in items
        ]

        signature_cores = [
            item["signature_core"]
            for item in items
        ]

        costs = [
            item["transition_cost"]
            for item in items
        ]

        remaining_counts = [
            item["remaining_run_count"]
            for item in items
        ]

        destination_counts = {}

        for item in items:
            destination = item["observed_destination_class"]
            destination_counts[destination] = (
                destination_counts.get(destination, 0) + 1
            )

        match_values = [
            item["destination_matches_rule"]
            for item in items
        ]

        summary[str(confirmation_window)] = {
            "confirmation_window": confirmation_window,
            "record_count": len(items),
            "cluster_count": len(set(cluster_ids)),
            "signature_core_count": len(set(signature_cores)),
            "transition_cost_values": sorted(set(costs)),
            "transition_cost_mean": safe_mean(costs),
            "transition_cost_std": safe_std(costs),
            "remaining_run_count_values": sorted(
                set(remaining_counts)
            ),
            "destination_class_counts": destination_counts,
            "destination_match_rate": (
                sum(1 for value in match_values if value)
                / max(len(match_values), 1)
            ),
        }

    return summary


def validate_cluster_invariance(clusters):
    failures = []
    collisions = []

    for cluster_id, item in clusters.items():
        if not item["signature_core_consistent"]:
            failures.append({
                "cluster_id": cluster_id,
                "reason": "multiple_signature_cores",
                "signature_core_values": (
                    item["signature_core_values"]
                ),
            })

        if not item["cluster_id_invariant"]:
            failures.append({
                "cluster_id": cluster_id,
                "reason": "cluster_components_not_invariant",
                "transition_cost_values": (
                    item["transition_cost_values"]
                ),
                "remaining_run_count_values": (
                    item["remaining_run_count_values"]
                ),
                "destination_class_values": (
                    item["destination_class_values"]
                ),
            })

        if (
            len(item["signature_core_values"]) == 1
            and item["signature_core_values"][0].replace("/", "|")
            .replace("--> ", "dest=")
            != cluster_id
        ):
            collisions.append({
                "cluster_id": cluster_id,
                "signature_core": item["signature_core_values"][0],
            })

    return {
        "cluster_invariance_holds": (
            len(failures) == 0
        ),
        "failure_count": len(failures),
        "failures": failures,
        "cluster_collision_count": len(collisions),
        "cluster_collisions": collisions,
        "cluster_rule": (
            "cluster_id = transition_cost "
            "+ remaining_run_count + destination_class"
        ),
        "signature_core_rule": (
            "same transition_cost + same remaining_run_count "
            "+ same destination_class -> same signature_core"
        ),
    }


def validate_destination_rule(flat_records):
    failures = []

    for item in flat_records:
        expected_destination = (
            destination_class_from_remaining_run_count(
                item["remaining_run_count"]
            )
        )

        if item["observed_destination_class"] != expected_destination:
            failures.append({
                "geometry_name": item["geometry_name"],
                "confirmation_window": item["confirmation_window"],
                "remaining_run_count": item["remaining_run_count"],
                "expected_destination": expected_destination,
                "observed_destination": (
                    item["observed_destination_class"]
                ),
            })

    return {
        "destination_rule_holds": len(failures) == 0,
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

    clusters = summarize_clusters(flat)
    by_family = summarize_by_family(flat)
    by_threshold = summarize_by_threshold(flat)

    cluster_validation = validate_cluster_invariance(clusters)
    destination_validation = validate_destination_rule(flat)

    family_crossing_clusters = {
        cluster_id: item
        for cluster_id, item in clusters.items()
        if item["family_crossing"]
    }

    source_variation_clusters = {
        cluster_id: item
        for cluster_id, item in clusters.items()
        if item["source_class_variation"]
    }

    threshold_crossing_clusters = {
        cluster_id: item
        for cluster_id, item in clusters.items()
        if item["threshold_crossing"]
    }

    multi_record_clusters = {
        cluster_id: item
        for cluster_id, item in clusters.items()
        if item["record_count"] > 1
    }

    signature_core_values = sorted(
        set(item["signature_core"] for item in flat)
    )

    cluster_id_values = sorted(
        set(item["cluster_id"] for item in flat)
    )

    cluster_invariance_map_detected = (
        cluster_validation["cluster_invariance_holds"]
        and destination_validation["destination_rule_holds"]
        and len(clusters) == len(signature_core_values)
    )

    return {
        "record_count": len(records),
        "flat_record_count": len(flat),
        "thresholds": CONFIRMATION_WINDOWS,
        "cluster_count": len(clusters),
        "signature_core_count": len(signature_core_values),
        "cluster_id_count": len(cluster_id_values),
        "family_count": len(by_family),
        "family_values": sorted(by_family.keys()),
        "multi_record_cluster_count": len(multi_record_clusters),
        "family_crossing_cluster_count": len(
            family_crossing_clusters
        ),
        "source_variation_cluster_count": len(
            source_variation_clusters
        ),
        "threshold_crossing_cluster_count": len(
            threshold_crossing_clusters
        ),
        "cluster_invariance_map_detected": (
            cluster_invariance_map_detected
        ),
        "clusters": clusters,
        "family_crossing_clusters": family_crossing_clusters,
        "source_variation_clusters": source_variation_clusters,
        "threshold_crossing_clusters": threshold_crossing_clusters,
        "multi_record_clusters": multi_record_clusters,
        "by_family": by_family,
        "by_threshold": by_threshold,
        "cluster_invariance_validation": cluster_validation,
        "destination_rule_validation": destination_validation,
        "cluster_definition": (
            "cluster_id = transition_cost "
            "+ remaining_run_count + destination_class"
        ),
        "invariance_claim": (
            "same transition_cost + same remaining_run_count "
            "+ same destination_class -> same signature_core"
        ),
    }


def compact_cluster(cluster):
    return {
        "cluster_id": cluster["cluster_id"],
        "record_count": cluster["record_count"],
        "family_values": cluster["family_values"],
        "geometry_name_values": cluster["geometry_name_values"],
        "confirmation_window_values": (
            cluster["confirmation_window_values"]
        ),
        "source_class_values": cluster["source_class_values"],
        "transition_cost_values": cluster["transition_cost_values"],
        "remaining_run_count_values": (
            cluster["remaining_run_count_values"]
        ),
        "destination_class_values": (
            cluster["destination_class_values"]
        ),
        "signature_core_values": cluster["signature_core_values"],
        "signature_core_consistent": (
            cluster["signature_core_consistent"]
        ),
        "cluster_id_invariant": cluster["cluster_id_invariant"],
        "family_crossing": cluster["family_crossing"],
        "source_class_variation": cluster["source_class_variation"],
        "threshold_crossing": cluster["threshold_crossing"],
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
                "cluster_id": item["cluster_id"],
                "signature_core": item["signature_core"],
                "transition_signature": (
                    item["transition_signature"]
                ),
                "destination_matches_rule": (
                    item["destination_matches_rule"]
                ),
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
        if analysis["cluster_invariance_map_detected"]
        else "CHECK"
    )

    compact_clusters = {
        cluster_id: compact_cluster(cluster)
        for cluster_id, cluster in analysis["clusters"].items()
    }

    summary = {
        "variant_count": len(records),
        "flat_record_count": analysis["flat_record_count"],
        "node_count": len(SUPPORTED_CLASSES),
        "confirmation_windows": CONFIRMATION_WINDOWS,
        "persistence_window": PERSISTENCE_WINDOW,
        "family_count": analysis["family_count"],
        "family_values": analysis["family_values"],
        "cluster_count": analysis["cluster_count"],
        "signature_core_count": analysis["signature_core_count"],
        "cluster_id_count": analysis["cluster_id_count"],
        "multi_record_cluster_count": (
            analysis["multi_record_cluster_count"]
        ),
        "family_crossing_cluster_count": (
            analysis["family_crossing_cluster_count"]
        ),
        "source_variation_cluster_count": (
            analysis["source_variation_cluster_count"]
        ),
        "threshold_crossing_cluster_count": (
            analysis["threshold_crossing_cluster_count"]
        ),
        "cluster_invariance_holds": (
            analysis["cluster_invariance_validation"][
                "cluster_invariance_holds"
            ]
        ),
        "cluster_collision_count": (
            analysis["cluster_invariance_validation"][
                "cluster_collision_count"
            ]
        ),
        "destination_rule_holds": (
            analysis["destination_rule_validation"][
                "destination_rule_holds"
            ]
        ),
        "cluster_invariance_map_detected": (
            analysis["cluster_invariance_map_detected"]
        ),
        "cluster_definition": analysis["cluster_definition"],
        "invariance_claim": analysis["invariance_claim"],
        "method": "signature_cluster_invariance",
    }

    payload = {
        "experiment": (
            "temporal_collapse_topology_signature_cluster_invariance_v0"
        ),
        "version": VERSION,
        "status": status,
        "summary": summary,
        "signature_cluster_invariance_summary": {
            "record_count": analysis["record_count"],
            "flat_record_count": analysis["flat_record_count"],
            "thresholds": analysis["thresholds"],
            "cluster_count": analysis["cluster_count"],
            "signature_core_count": analysis["signature_core_count"],
            "cluster_id_count": analysis["cluster_id_count"],
            "family_count": analysis["family_count"],
            "family_values": analysis["family_values"],
            "multi_record_cluster_count": (
                analysis["multi_record_cluster_count"]
            ),
            "family_crossing_cluster_count": (
                analysis["family_crossing_cluster_count"]
            ),
            "source_variation_cluster_count": (
                analysis["source_variation_cluster_count"]
            ),
            "threshold_crossing_cluster_count": (
                analysis["threshold_crossing_cluster_count"]
            ),
            "cluster_invariance_map_detected": (
                analysis["cluster_invariance_map_detected"]
            ),
            "cluster_definition": analysis["cluster_definition"],
            "invariance_claim": analysis["invariance_claim"],
            "cluster_invariance_validation": (
                analysis["cluster_invariance_validation"]
            ),
            "destination_rule_validation": (
                analysis["destination_rule_validation"]
            ),
            "clusters": compact_clusters,
            "by_family": analysis["by_family"],
            "by_threshold": analysis["by_threshold"],
        },
        "geometry_records": [
            compact_record(record)
            for record in records
        ],
        "interpretation": (
            "This experiment tests whether signature clusters are "
            "invariant objects defined by transition cost, remaining "
            "run count, and destination class, even when geometry "
            "family and source class vary."
        ),
        "reproduction_command": (
            "python examples/"
            "temporal_collapse_topology_signature_cluster_invariance_v0.py"
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
        "Temporal Collapse Topology Signature Cluster Invariance v0"
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
            f"clusters={values['cluster_count']} "
            f"cores={values['signature_core_count']} "
            f"costs={values['transition_cost_values']} "
            f"remaining={values['remaining_run_count_values']} "
            f"destinations={values['destination_class_counts']} "
            f"destination_match={values['destination_match_rate']}"
        )

    print()
    print("By family")
    print("-" * 80)

    for family, values in analysis["by_family"].items():
        print(
            f"family={family:<24} "
            f"records={values['record_count']} "
            f"clusters={values['cluster_count']} "
            f"cores={values['signature_core_count']} "
            f"costs={values['transition_cost_values']} "
            f"remaining={values['remaining_run_count_values']} "
            f"destinations={values['destination_class_values']}"
        )

    print()
    print("Clusters")
    print("-" * 80)

    for cluster_id, cluster in compact_clusters.items():
        print(
            f"cluster={cluster_id:<64} "
            f"records={cluster['record_count']} "
            f"families={cluster['family_values']} "
            f"C={cluster['confirmation_window_values']} "
            f"sources={cluster['source_class_values']} "
            f"core_ok={cluster['signature_core_consistent']} "
            f"invariant={cluster['cluster_id_invariant']}"
        )

    print()
    print("Family-crossing clusters")
    print("-" * 80)

    for cluster_id, cluster in (
        analysis["family_crossing_clusters"].items()
    ):
        print(
            f"cluster={cluster_id:<64} "
            f"records={cluster['record_count']} "
            f"families={cluster['family_values']} "
            f"sources={cluster['source_class_values']} "
            f"C={cluster['confirmation_window_values']}"
        )

    print()
    print("Source-variation clusters")
    print("-" * 80)

    for cluster_id, cluster in (
        analysis["source_variation_clusters"].items()
    ):
        print(
            f"cluster={cluster_id:<64} "
            f"records={cluster['record_count']} "
            f"sources={cluster['source_class_values']} "
            f"families={cluster['family_values']}"
        )

    print()
    print("Rule validation")
    print("-" * 80)

    cluster_validation = analysis["cluster_invariance_validation"]
    destination_validation = analysis["destination_rule_validation"]

    print(
        "cluster_invariance_holds:",
        cluster_validation["cluster_invariance_holds"],
    )
    print(
        "cluster_failure_count:",
        cluster_validation["failure_count"],
    )
    print(
        "cluster_collision_count:",
        cluster_validation["cluster_collision_count"],
    )
    print(
        "destination_rule_holds:",
        destination_validation["destination_rule_holds"],
    )
    print(
        "destination_failure_count:",
        destination_validation["failure_count"],
    )

    if cluster_validation["failures"]:
        print("cluster_failures:", cluster_validation["failures"])

    if destination_validation["failures"]:
        print(
            "destination_failures:",
            destination_validation["failures"],
        )

    print()
    print("=" * 80)
    print("FINAL CHECK")
    print("=" * 80)

    if status == "PASS":
        print(
            "PASS - signature-cluster invariance detected: "
            "same transition cost + same remaining run count + same "
            "destination class produced the same signature core, even "
            "across family and source-class variation."
        )
    else:
        print(
            "CHECK - signature-cluster invariance was not fully "
            "confirmed under tested cluster mappings."
        )

    print()
    print("=" * 80)
    print("Result saved to:", RESULTS_PATH)
    print("=" * 80)


if __name__ == "__main__":
    main()