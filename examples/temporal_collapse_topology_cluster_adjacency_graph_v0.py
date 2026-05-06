import json
from pathlib import Path
from statistics import mean, pstdev

VERSION = "0.1.0"

RESULTS_PATH = Path(
    "results/temporal_collapse_topology_cluster_adjacency_graph_v0.json"
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


def cluster_adjacency_specs():
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


def parse_cluster_id(cluster_id):
    parts = cluster_id.split("|")
    cost = int(parts[0].split("=")[1])
    remaining = int(parts[1].split("=")[1])
    destination = parts[2].split("=")[1]

    return {
        "transition_cost": cost,
        "remaining_run_count": remaining,
        "destination_class": destination,
    }


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

    for variant_index, spec in enumerate(cluster_adjacency_specs()):
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
            "method": "cluster_adjacency_graph",
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
            parsed = parse_cluster_id(cluster_id)

            clusters[cluster_id] = {
                "cluster_id": cluster_id,
                "signature_core": item["signature_core"],
                "record_count": 0,
                "transition_cost": parsed["transition_cost"],
                "remaining_run_count": parsed["remaining_run_count"],
                "destination_class": parsed["destination_class"],
                "families": [],
                "geometry_names": [],
                "confirmation_windows": [],
                "source_classes": [],
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
        clusters[cluster_id]["transition_signatures"].append(
            item["transition_signature"]
        )

    for cluster_id, cluster in clusters.items():
        cluster["family_values"] = sorted(set(cluster["families"]))
        cluster["geometry_name_values"] = sorted(
            set(cluster["geometry_names"])
        )
        cluster["confirmation_window_values"] = sorted(
            set(cluster["confirmation_windows"])
        )
        cluster["source_class_values"] = sorted(
            set(cluster["source_classes"])
        )
        cluster["family_crossing"] = (
            len(cluster["family_values"]) > 1
        )
        cluster["source_class_variation"] = (
            len(cluster["source_class_values"]) > 1
        )
        cluster["threshold_crossing"] = (
            len(cluster["confirmation_window_values"]) > 1
        )

    return clusters


def add_edge(edges, source, target, edge_type, evidence):
    key = f"{source} -> {target} [{edge_type}]"

    if key not in edges:
        edges[key] = {
            "edge_id": key,
            "source_cluster": source,
            "target_cluster": target,
            "edge_type": edge_type,
            "weight": 0,
            "families": [],
            "geometry_names": [],
            "confirmation_windows": [],
            "evidence": [],
        }

    edges[key]["weight"] += 1
    edges[key]["families"].append(evidence.get("family"))
    edges[key]["geometry_names"].append(evidence.get("geometry_name"))

    if evidence.get("confirmation_window") is not None:
        edges[key]["confirmation_windows"].append(
            evidence.get("confirmation_window")
        )

    edges[key]["evidence"].append(evidence)


def build_threshold_edges(records):
    edges = {}

    for record in records:
        ordered = sorted(
            record["transition_results"],
            key=lambda item: item["confirmation_window"],
        )

        for left, right in zip(ordered, ordered[1:]):
            source = left["cluster_id"]
            target = right["cluster_id"]

            add_edge(
                edges,
                source,
                target,
                "threshold_transition",
                {
                    "family": record["family"],
                    "geometry_name": record["geometry_name"],
                    "from_confirmation_window": (
                        left["confirmation_window"]
                    ),
                    "to_confirmation_window": (
                        right["confirmation_window"]
                    ),
                    "confirmation_window": (
                        right["confirmation_window"]
                    ),
                    "from_core": left["signature_core"],
                    "to_core": right["signature_core"],
                },
            )

    return edges


def build_geometry_edges(records):
    edges = {}

    grouped = {}

    for record in records:
        grouped.setdefault(record["family"], []).append(record)

    for family, family_records in grouped.items():
        ordered_records = sorted(
            family_records,
            key=lambda record: (
                record["features"]["total_collapse_frames"],
                record["features"]["collapse_run_count"],
                record["geometry_name"],
            ),
        )

        for left_record, right_record in zip(
            ordered_records,
            ordered_records[1:],
        ):
            for confirmation_window in CONFIRMATION_WINDOWS:
                left_item = next(
                    item
                    for item in left_record["transition_results"]
                    if item["confirmation_window"] == confirmation_window
                )
                right_item = next(
                    item
                    for item in right_record["transition_results"]
                    if item["confirmation_window"] == confirmation_window
                )

                add_edge(
                    edges,
                    left_item["cluster_id"],
                    right_item["cluster_id"],
                    "geometry_transition",
                    {
                        "family": family,
                        "geometry_name": (
                            f"{left_record['geometry_name']} -> "
                            f"{right_record['geometry_name']}"
                        ),
                        "confirmation_window": confirmation_window,
                        "from_geometry": left_record["geometry_name"],
                        "to_geometry": right_record["geometry_name"],
                        "from_run_lengths": left_record["run_lengths"],
                        "to_run_lengths": right_record["run_lengths"],
                        "from_core": left_item["signature_core"],
                        "to_core": right_item["signature_core"],
                    },
                )

    return edges


def merge_edges(*edge_maps):
    merged = {}

    for edge_map in edge_maps:
        for key, edge in edge_map.items():
            if key not in merged:
                merged[key] = {
                    "edge_id": edge["edge_id"],
                    "source_cluster": edge["source_cluster"],
                    "target_cluster": edge["target_cluster"],
                    "edge_type": edge["edge_type"],
                    "weight": 0,
                    "families": [],
                    "geometry_names": [],
                    "confirmation_windows": [],
                    "evidence": [],
                }

            merged[key]["weight"] += edge["weight"]
            merged[key]["families"].extend(edge["families"])
            merged[key]["geometry_names"].extend(edge["geometry_names"])
            merged[key]["confirmation_windows"].extend(
                edge["confirmation_windows"]
            )
            merged[key]["evidence"].extend(edge["evidence"])

    for edge in merged.values():
        edge["family_values"] = sorted(
            value
            for value in set(edge["families"])
            if value is not None
        )
        edge["geometry_name_values"] = sorted(
            value
            for value in set(edge["geometry_names"])
            if value is not None
        )
        edge["confirmation_window_values"] = sorted(
            value
            for value in set(edge["confirmation_windows"])
            if value is not None
        )
        edge["family_crossing"] = len(edge["family_values"]) > 1

    return merged


def compute_graph_metrics(clusters, edges):
    degree = {}

    for cluster_id in clusters:
        degree[cluster_id] = {
            "cluster_id": cluster_id,
            "in_degree": 0,
            "out_degree": 0,
            "weighted_in_degree": 0,
            "weighted_out_degree": 0,
            "neighbors_in": [],
            "neighbors_out": [],
            "edge_types_in": [],
            "edge_types_out": [],
        }

    for edge in edges.values():
        source = edge["source_cluster"]
        target = edge["target_cluster"]
        weight = edge["weight"]
        edge_type = edge["edge_type"]

        degree[source]["out_degree"] += 1
        degree[source]["weighted_out_degree"] += weight
        degree[source]["neighbors_out"].append(target)
        degree[source]["edge_types_out"].append(edge_type)

        degree[target]["in_degree"] += 1
        degree[target]["weighted_in_degree"] += weight
        degree[target]["neighbors_in"].append(source)
        degree[target]["edge_types_in"].append(edge_type)

    for cluster_id, item in degree.items():
        item["neighbors_in"] = sorted(set(item["neighbors_in"]))
        item["neighbors_out"] = sorted(set(item["neighbors_out"]))
        item["edge_types_in"] = sorted(set(item["edge_types_in"]))
        item["edge_types_out"] = sorted(set(item["edge_types_out"]))
        item["total_degree"] = (
            item["in_degree"] + item["out_degree"]
        )
        item["weighted_total_degree"] = (
            item["weighted_in_degree"]
            + item["weighted_out_degree"]
        )

    attractors = {
        cluster_id: item
        for cluster_id, item in degree.items()
        if item["out_degree"] == 0 and item["in_degree"] > 0
    }

    sources = {
        cluster_id: item
        for cluster_id, item in degree.items()
        if item["in_degree"] == 0 and item["out_degree"] > 0
    }

    bridges = {
        cluster_id: item
        for cluster_id, item in degree.items()
        if item["in_degree"] > 0 and item["out_degree"] > 0
    }

    isolated = {
        cluster_id: item
        for cluster_id, item in degree.items()
        if item["in_degree"] == 0 and item["out_degree"] == 0
    }

    top_by_total_degree = sorted(
        degree.values(),
        key=lambda item: (
            item["weighted_total_degree"],
            item["total_degree"],
            item["cluster_id"],
        ),
        reverse=True,
    )

    return {
        "degree_by_cluster": degree,
        "attractor_clusters": attractors,
        "source_clusters": sources,
        "bridge_clusters": bridges,
        "isolated_clusters": isolated,
        "top_clusters_by_weighted_degree": top_by_total_degree[:10],
        "cluster_count": len(clusters),
        "edge_count": len(edges),
        "attractor_count": len(attractors),
        "source_count": len(sources),
        "bridge_count": len(bridges),
        "isolated_count": len(isolated),
    }


def summarize_by_edge_type(edges):
    summary = {}

    for edge in edges.values():
        edge_type = edge["edge_type"]

        if edge_type not in summary:
            summary[edge_type] = {
                "edge_type": edge_type,
                "edge_count": 0,
                "total_weight": 0,
                "source_clusters": [],
                "target_clusters": [],
                "families": [],
            }

        summary[edge_type]["edge_count"] += 1
        summary[edge_type]["total_weight"] += edge["weight"]
        summary[edge_type]["source_clusters"].append(
            edge["source_cluster"]
        )
        summary[edge_type]["target_clusters"].append(
            edge["target_cluster"]
        )
        summary[edge_type]["families"].extend(edge["family_values"])

    for edge_type, item in summary.items():
        item["source_cluster_count"] = len(
            set(item["source_clusters"])
        )
        item["target_cluster_count"] = len(
            set(item["target_clusters"])
        )
        item["family_values"] = sorted(set(item["families"]))

    return summary


def validate_graph(clusters, edges):
    failures = []

    for edge_id, edge in edges.items():
        if edge["source_cluster"] not in clusters:
            failures.append({
                "edge_id": edge_id,
                "reason": "missing_source_cluster",
                "source_cluster": edge["source_cluster"],
            })

        if edge["target_cluster"] not in clusters:
            failures.append({
                "edge_id": edge_id,
                "reason": "missing_target_cluster",
                "target_cluster": edge["target_cluster"],
            })

        if edge["weight"] <= 0:
            failures.append({
                "edge_id": edge_id,
                "reason": "non_positive_edge_weight",
                "weight": edge["weight"],
            })

    return {
        "graph_validation_holds": len(failures) == 0,
        "failure_count": len(failures),
        "failures": failures,
    }


def compact_cluster(cluster):
    return {
        "cluster_id": cluster["cluster_id"],
        "signature_core": cluster["signature_core"],
        "record_count": cluster["record_count"],
        "transition_cost": cluster["transition_cost"],
        "remaining_run_count": cluster["remaining_run_count"],
        "destination_class": cluster["destination_class"],
        "family_values": cluster["family_values"],
        "geometry_name_values": cluster["geometry_name_values"],
        "confirmation_window_values": (
            cluster["confirmation_window_values"]
        ),
        "source_class_values": cluster["source_class_values"],
        "family_crossing": cluster["family_crossing"],
        "source_class_variation": cluster["source_class_variation"],
        "threshold_crossing": cluster["threshold_crossing"],
    }


def compact_edge(edge):
    return {
        "edge_id": edge["edge_id"],
        "source_cluster": edge["source_cluster"],
        "target_cluster": edge["target_cluster"],
        "edge_type": edge["edge_type"],
        "weight": edge["weight"],
        "family_values": edge["family_values"],
        "confirmation_window_values": (
            edge["confirmation_window_values"]
        ),
        "family_crossing": edge["family_crossing"],
        "evidence_count": len(edge["evidence"]),
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
                "source_class": item["source_class"],
                "transition_cost": item["transition_cost"],
                "remaining_run_count": item["remaining_run_count"],
                "observed_destination_class": (
                    item["observed_destination_class"]
                ),
                "cluster_id": item["cluster_id"],
                "signature_core": item["signature_core"],
                "destination_matches_rule": (
                    item["destination_matches_rule"]
                ),
            }
            for item in record["transition_results"]
        ],
        "method": record["method"],
    }


def summarize(records):
    flat = flatten_records(records)

    clusters = summarize_clusters(flat)

    threshold_edges = build_threshold_edges(records)
    geometry_edges = build_geometry_edges(records)

    edges = merge_edges(
        threshold_edges,
        geometry_edges,
    )

    graph_metrics = compute_graph_metrics(
        clusters,
        edges,
    )

    by_edge_type = summarize_by_edge_type(edges)

    graph_validation = validate_graph(
        clusters,
        edges,
    )

    family_crossing_edges = {
        edge_id: edge
        for edge_id, edge in edges.items()
        if edge["family_crossing"]
    }

    self_edges = {
        edge_id: edge
        for edge_id, edge in edges.items()
        if edge["source_cluster"] == edge["target_cluster"]
    }

    non_self_edges = {
        edge_id: edge
        for edge_id, edge in edges.items()
        if edge["source_cluster"] != edge["target_cluster"]
    }

    graph_detected = (
        graph_validation["graph_validation_holds"]
        and len(clusters) > 0
        and len(edges) > 0
        and graph_metrics["bridge_count"] > 0
    )

    return {
        "record_count": len(records),
        "flat_record_count": len(flat),
        "thresholds": CONFIRMATION_WINDOWS,
        "cluster_count": len(clusters),
        "threshold_edge_count": len(threshold_edges),
        "geometry_edge_count": len(geometry_edges),
        "edge_count": len(edges),
        "self_edge_count": len(self_edges),
        "non_self_edge_count": len(non_self_edges),
        "family_crossing_edge_count": len(family_crossing_edges),
        "clusters": clusters,
        "edges": edges,
        "threshold_edges": threshold_edges,
        "geometry_edges": geometry_edges,
        "self_edges": self_edges,
        "non_self_edges": non_self_edges,
        "family_crossing_edges": family_crossing_edges,
        "graph_metrics": graph_metrics,
        "by_edge_type": by_edge_type,
        "graph_validation": graph_validation,
        "cluster_adjacency_graph_detected": graph_detected,
        "graph_definition": (
            "nodes = invariant signature clusters; "
            "edges = threshold transitions + geometry transitions"
        ),
    }


def main():
    records = build_records()
    analysis = summarize(records)

    status = (
        "PASS"
        if analysis["cluster_adjacency_graph_detected"]
        else "CHECK"
    )

    compact_clusters = {
        cluster_id: compact_cluster(cluster)
        for cluster_id, cluster in analysis["clusters"].items()
    }

    compact_edges = {
        edge_id: compact_edge(edge)
        for edge_id, edge in analysis["edges"].items()
    }

    summary = {
        "variant_count": len(records),
        "flat_record_count": analysis["flat_record_count"],
        "node_count": len(SUPPORTED_CLASSES),
        "confirmation_windows": CONFIRMATION_WINDOWS,
        "persistence_window": PERSISTENCE_WINDOW,
        "cluster_count": analysis["cluster_count"],
        "edge_count": analysis["edge_count"],
        "threshold_edge_count": analysis["threshold_edge_count"],
        "geometry_edge_count": analysis["geometry_edge_count"],
        "self_edge_count": analysis["self_edge_count"],
        "non_self_edge_count": analysis["non_self_edge_count"],
        "family_crossing_edge_count": (
            analysis["family_crossing_edge_count"]
        ),
        "attractor_cluster_count": (
            analysis["graph_metrics"]["attractor_count"]
        ),
        "source_cluster_count": (
            analysis["graph_metrics"]["source_count"]
        ),
        "bridge_cluster_count": (
            analysis["graph_metrics"]["bridge_count"]
        ),
        "isolated_cluster_count": (
            analysis["graph_metrics"]["isolated_count"]
        ),
        "graph_validation_holds": (
            analysis["graph_validation"]["graph_validation_holds"]
        ),
        "graph_failure_count": (
            analysis["graph_validation"]["failure_count"]
        ),
        "cluster_adjacency_graph_detected": (
            analysis["cluster_adjacency_graph_detected"]
        ),
        "graph_definition": analysis["graph_definition"],
        "method": "cluster_adjacency_graph",
    }

    payload = {
        "experiment": (
            "temporal_collapse_topology_cluster_adjacency_graph_v0"
        ),
        "version": VERSION,
        "status": status,
        "summary": summary,
        "cluster_adjacency_graph_summary": {
            "record_count": analysis["record_count"],
            "flat_record_count": analysis["flat_record_count"],
            "thresholds": analysis["thresholds"],
            "cluster_count": analysis["cluster_count"],
            "edge_count": analysis["edge_count"],
            "threshold_edge_count": analysis["threshold_edge_count"],
            "geometry_edge_count": analysis["geometry_edge_count"],
            "self_edge_count": analysis["self_edge_count"],
            "non_self_edge_count": analysis["non_self_edge_count"],
            "family_crossing_edge_count": (
                analysis["family_crossing_edge_count"]
            ),
            "cluster_adjacency_graph_detected": (
                analysis["cluster_adjacency_graph_detected"]
            ),
            "graph_definition": analysis["graph_definition"],
            "graph_validation": analysis["graph_validation"],
            "by_edge_type": analysis["by_edge_type"],
            "graph_metrics": analysis["graph_metrics"],
            "clusters": compact_clusters,
            "edges": compact_edges,
        },
        "geometry_records": [
            compact_record(record)
            for record in records
        ],
        "interpretation": (
            "This experiment builds a directed graph over invariant "
            "signature clusters. Nodes are cluster IDs. Edges represent "
            "threshold transitions and geometry transitions between "
            "clusters."
        ),
        "reproduction_command": (
            "python examples/"
            "temporal_collapse_topology_cluster_adjacency_graph_v0.py"
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
        "Temporal Collapse Topology Cluster Adjacency Graph v0"
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
    print("By edge type")
    print("-" * 80)

    for edge_type, values in analysis["by_edge_type"].items():
        print(
            f"edge_type={edge_type:<24} "
            f"edges={values['edge_count']} "
            f"weight={values['total_weight']} "
            f"sources={values['source_cluster_count']} "
            f"targets={values['target_cluster_count']} "
            f"families={values['family_values']}"
        )

    print()
    print("Top clusters by weighted degree")
    print("-" * 80)

    for item in analysis["graph_metrics"][
        "top_clusters_by_weighted_degree"
    ]:
        print(
            f"cluster={item['cluster_id']:<64} "
            f"in={item['in_degree']} "
            f"out={item['out_degree']} "
            f"win={item['weighted_in_degree']} "
            f"wout={item['weighted_out_degree']} "
            f"total={item['weighted_total_degree']}"
        )

    print()
    print("Attractor clusters")
    print("-" * 80)

    for cluster_id, item in analysis["graph_metrics"][
        "attractor_clusters"
    ].items():
        print(
            f"cluster={cluster_id:<64} "
            f"in={item['in_degree']} "
            f"win={item['weighted_in_degree']} "
            f"neighbors_in={item['neighbors_in']}"
        )

    print()
    print("Bridge clusters")
    print("-" * 80)

    for cluster_id, item in analysis["graph_metrics"][
        "bridge_clusters"
    ].items():
        print(
            f"cluster={cluster_id:<64} "
            f"in={item['in_degree']} "
            f"out={item['out_degree']} "
            f"win={item['weighted_in_degree']} "
            f"wout={item['weighted_out_degree']}"
        )

    print()
    print("Edges")
    print("-" * 80)

    for edge_id, edge in compact_edges.items():
        print(
            f"edge={edge_id} "
            f"weight={edge['weight']} "
            f"families={edge['family_values']} "
            f"C={edge['confirmation_window_values']}"
        )

    print()
    print("Family-crossing edges")
    print("-" * 80)

    for edge_id, edge in analysis["family_crossing_edges"].items():
        print(
            f"edge={edge_id} "
            f"weight={edge['weight']} "
            f"families={edge['family_values']}"
        )

    print()
    print("Rule validation")
    print("-" * 80)

    validation = analysis["graph_validation"]

    print(
        "graph_validation_holds:",
        validation["graph_validation_holds"],
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
            "PASS - signature-cluster adjacency graph detected: "
            "invariant clusters form a directed transition topology "
            "under threshold and geometry transitions."
        )
    else:
        print(
            "CHECK - signature-cluster adjacency graph was not fully "
            "confirmed under tested transitions."
        )

    print()
    print("=" * 80)
    print("Result saved to:", RESULTS_PATH)
    print("=" * 80)


if __name__ == "__main__":
    main()