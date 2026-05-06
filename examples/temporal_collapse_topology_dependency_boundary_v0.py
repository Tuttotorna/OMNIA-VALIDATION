import json
from itertools import combinations
from pathlib import Path
from statistics import mean, pstdev

VERSION = "0.1.0"

RESULTS_PATH = Path(
    "results/temporal_collapse_topology_dependency_boundary_v0.json"
)

CONFIRMATION_WINDOWS = [2, 3, 4]
PERSISTENCE_WINDOW = 2

EXPECTED_DOMINANT = (
    "cost=0|remaining=3|dest=OSCILLATING_NONPERSISTENT"
)

EXPECTED_SECOND = (
    "cost=3|remaining=3|dest=OSCILLATING_NONPERSISTENT"
)


def safe_mean(values):
    return mean(values) if values else None


def safe_std(values):
    return pstdev(values) if len(values) > 1 else 0.0


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
    run_lengths = [end - start + 1 for start, end in runs]
    max_run_length = max(run_lengths) if run_lengths else 0

    local_confirmation_count = sum(
        1
        for run_length in run_lengths
        if run_length >= confirmation_window
    )

    persistence_reset_count = max(collapse_run_count - 1, 0)

    global_persistence_detected = any(
        run_length >= persistence_threshold
        for run_length in run_lengths
    )

    if collapse_run_count == 0:
        label = "CLEAN_PASS"

    elif collapse_run_count == 1 and max_run_length < confirmation_window:
        label = "SPIKE_FILTERED"

    elif global_persistence_detected and persistence_reset_count == 0:
        label = "GLOBAL_PERSISTENT_COLLAPSE"

    elif global_persistence_detected and persistence_reset_count > 0:
        label = "RECOVERY_RELAPSE_COLLAPSE"

    elif local_confirmation_count > 0 and not global_persistence_detected:
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
        "global_persistence_detected": global_persistence_detected,
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


def cluster_specs():
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
        "mass_per_run": total_collapse_frames / max(collapse_run_count, 1),
    }


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


def destination_class_from_remaining_run_count(remaining_run_count):
    if remaining_run_count == 0:
        return "CLEAN_PASS"

    if remaining_run_count == 1:
        return "SPIKE_FILTERED"

    return "OSCILLATING_NONPERSISTENT"


def build_reduced_sequence(remaining_lengths):
    if not remaining_lengths:
        return ["PASS"] * 10

    length, runs = make_sequence_from_lengths(remaining_lengths)
    return make_sequence(length, runs)


def build_cluster_id(transition_cost, remaining_run_count, destination_class):
    return (
        f"cost={transition_cost}"
        f"|remaining={remaining_run_count}"
        f"|dest={destination_class}"
    )


def build_signature_core(transition_cost, remaining_run_count, destination_class):
    return (
        f"cost={transition_cost}"
        f"/remaining={remaining_run_count}"
        f"--> {destination_class}"
    )


def parse_cluster_id(cluster_id):
    parts = cluster_id.split("|")

    return {
        "transition_cost": int(parts[0].split("=")[1]),
        "remaining_run_count": int(parts[1].split("=")[1]),
        "destination_class": parts[2].split("=")[1],
    }


def build_records(specs=None, confirmation_windows=None):
    specs = specs if specs is not None else cluster_specs()

    confirmation_windows = (
        confirmation_windows
        if confirmation_windows is not None
        else CONFIRMATION_WINDOWS
    )

    records = []

    for variant_index, spec in enumerate(specs):
        length, runs = make_sequence_from_lengths(spec["run_lengths"])
        sequence = make_sequence(length, runs)
        features = geometry_features(spec["run_lengths"])
        transition_results = []

        for confirmation_window in confirmation_windows:
            source_metrics = classify(sequence, confirmation_window)

            transition_cost = thresholded_reducible_mass(
                spec["run_lengths"],
                confirmation_window,
            )

            remaining_lengths = post_reduction_lengths(
                spec["run_lengths"],
                confirmation_window,
            )

            remaining_run_count = len(remaining_lengths)

            predicted_destination = destination_class_from_remaining_run_count(
                remaining_run_count
            )

            reduced_sequence = build_reduced_sequence(remaining_lengths)
            destination_metrics = classify(reduced_sequence, confirmation_window)
            observed_destination = destination_metrics["classification"]

            cluster_id = build_cluster_id(
                transition_cost,
                remaining_run_count,
                observed_destination,
            )

            signature_core = build_signature_core(
                transition_cost,
                remaining_run_count,
                observed_destination,
            )

            transition_results.append(
                {
                    "confirmation_window": confirmation_window,
                    "source_class": source_metrics["classification"],
                    "transition_cost": transition_cost,
                    "remaining_run_count": remaining_run_count,
                    "remaining_run_lengths": remaining_lengths,
                    "predicted_destination_class": predicted_destination,
                    "observed_destination_class": observed_destination,
                    "cluster_id": cluster_id,
                    "signature_core": signature_core,
                    "destination_matches_rule": (
                        predicted_destination == observed_destination
                    ),
                }
            )

        records.append(
            {
                "variant_index": variant_index,
                "family": spec["family"],
                "geometry_name": spec["name"],
                "run_lengths": spec["run_lengths"],
                "trajectory_length": length,
                "runs": runs,
                "features": features,
                "transition_results": transition_results,
            }
        )

    return records


def flatten_records(records):
    flat = []

    for record in records:
        for item in record["transition_results"]:
            flat.append(
                {
                    "variant_index": record["variant_index"],
                    "family": record["family"],
                    "geometry_name": record["geometry_name"],
                    "run_lengths": record["run_lengths"],
                    "features": record["features"],
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
            )

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
            }

        clusters[cluster_id]["record_count"] += 1
        clusters[cluster_id]["families"].append(item["family"])
        clusters[cluster_id]["geometry_names"].append(item["geometry_name"])
        clusters[cluster_id]["confirmation_windows"].append(
            item["confirmation_window"]
        )
        clusters[cluster_id]["source_classes"].append(item["source_class"])

    for cluster in clusters.values():
        cluster["family_values"] = sorted(set(cluster["families"]))
        cluster["geometry_name_values"] = sorted(set(cluster["geometry_names"]))
        cluster["confirmation_window_values"] = sorted(
            set(cluster["confirmation_windows"])
        )
        cluster["source_class_values"] = sorted(set(cluster["source_classes"]))
        cluster["family_crossing"] = len(cluster["family_values"]) > 1
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
            add_edge(
                edges,
                left["cluster_id"],
                right["cluster_id"],
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
                    "confirmation_window": right["confirmation_window"],
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
            left_windows = {
                item["confirmation_window"]
                for item in left_record["transition_results"]
            }

            right_windows = {
                item["confirmation_window"]
                for item in right_record["transition_results"]
            }

            common_windows = sorted(left_windows.intersection(right_windows))

            for confirmation_window in common_windows:
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
        edge["is_self_edge"] = edge["source_cluster"] == edge["target_cluster"]

    return merged


def validate_graph(clusters, edges):
    failures = []

    for edge_id, edge in edges.items():
        if edge["source_cluster"] not in clusters:
            failures.append(
                {
                    "edge_id": edge_id,
                    "reason": "missing_source_cluster",
                    "source_cluster": edge["source_cluster"],
                }
            )

        if edge["target_cluster"] not in clusters:
            failures.append(
                {
                    "edge_id": edge_id,
                    "reason": "missing_target_cluster",
                    "target_cluster": edge["target_cluster"],
                }
            )

        if edge["weight"] <= 0:
            failures.append(
                {
                    "edge_id": edge_id,
                    "reason": "non_positive_edge_weight",
                    "weight": edge["weight"],
                }
            )

    return {
        "graph_validation_holds": len(failures) == 0,
        "failure_count": len(failures),
        "failures": failures,
    }


def initialize_metrics(clusters):
    metrics = {}

    for cluster_id, cluster in clusters.items():
        metrics[cluster_id] = {
            "cluster_id": cluster_id,
            "signature_core": cluster["signature_core"],
            "record_count": cluster["record_count"],
            "transition_cost": cluster["transition_cost"],
            "remaining_run_count": cluster["remaining_run_count"],
            "destination_class": cluster["destination_class"],
            "family_values": cluster["family_values"],
            "source_class_values": cluster["source_class_values"],
            "in_degree": 0,
            "out_degree": 0,
            "weighted_in_degree": 0,
            "weighted_out_degree": 0,
            "self_loop_count": 0,
            "self_loop_weight": 0,
            "threshold_edge_in_weight": 0,
            "threshold_edge_out_weight": 0,
            "geometry_edge_in_weight": 0,
            "geometry_edge_out_weight": 0,
            "family_crossing_edge_in_weight": 0,
            "family_crossing_edge_out_weight": 0,
            "incoming_neighbors": [],
            "outgoing_neighbors": [],
        }

    return metrics


def compute_graph_metrics(clusters, edges):
    metrics = initialize_metrics(clusters)

    for edge in edges.values():
        source = edge["source_cluster"]
        target = edge["target_cluster"]
        weight = edge["weight"]
        edge_type = edge["edge_type"]

        metrics[source]["out_degree"] += 1
        metrics[source]["weighted_out_degree"] += weight
        metrics[source]["outgoing_neighbors"].append(target)

        metrics[target]["in_degree"] += 1
        metrics[target]["weighted_in_degree"] += weight
        metrics[target]["incoming_neighbors"].append(source)

        if edge["is_self_edge"]:
            metrics[source]["self_loop_count"] += 1
            metrics[source]["self_loop_weight"] += weight

        if edge_type == "threshold_transition":
            metrics[source]["threshold_edge_out_weight"] += weight
            metrics[target]["threshold_edge_in_weight"] += weight

        if edge_type == "geometry_transition":
            metrics[source]["geometry_edge_out_weight"] += weight
            metrics[target]["geometry_edge_in_weight"] += weight

        if edge["family_crossing"]:
            metrics[source]["family_crossing_edge_out_weight"] += weight
            metrics[target]["family_crossing_edge_in_weight"] += weight

    for item in metrics.values():
        item["incoming_neighbors"] = sorted(set(item["incoming_neighbors"]))
        item["outgoing_neighbors"] = sorted(set(item["outgoing_neighbors"]))

        item["total_degree"] = item["in_degree"] + item["out_degree"]

        item["weighted_total_degree"] = (
            item["weighted_in_degree"] + item["weighted_out_degree"]
        )

        item["threshold_edge_total_weight"] = (
            item["threshold_edge_in_weight"]
            + item["threshold_edge_out_weight"]
        )

        item["geometry_edge_total_weight"] = (
            item["geometry_edge_in_weight"]
            + item["geometry_edge_out_weight"]
        )

        item["family_crossing_edge_total_weight"] = (
            item["family_crossing_edge_in_weight"]
            + item["family_crossing_edge_out_weight"]
        )

        item["neighbor_count"] = len(
            set(item["incoming_neighbors"] + item["outgoing_neighbors"])
        )

        item["is_bridge"] = (
            item["weighted_in_degree"] > 0
            and item["weighted_out_degree"] > 0
        )

        item["is_source"] = (
            item["weighted_in_degree"] == 0
            and item["weighted_out_degree"] > 0
        )

        item["is_attractor"] = (
            item["weighted_in_degree"] > 0
            and item["weighted_out_degree"] == 0
        )

        item["is_isolated"] = (
            item["weighted_in_degree"] == 0
            and item["weighted_out_degree"] == 0
        )

        item["bridge_score"] = (
            min(item["weighted_in_degree"], item["weighted_out_degree"])
            + item["neighbor_count"]
            + item["family_crossing_edge_total_weight"]
            + item["self_loop_weight"]
        )

        item["centrality_score"] = (
            item["weighted_total_degree"]
            + item["bridge_score"]
            + item["threshold_edge_total_weight"] * 0.25
            + item["geometry_edge_total_weight"] * 0.25
            + item["family_crossing_edge_total_weight"] * 0.50
            + item["self_loop_weight"] * 0.50
        )

        item["control_plane_score"] = (
            item["centrality_score"]
            + item["family_crossing_edge_total_weight"] * 1.50
            + item["bridge_score"] * 1.25
            + item["self_loop_weight"] * 1.00
            + item["threshold_edge_total_weight"] * 0.50
            + item["geometry_edge_total_weight"] * 0.50
            + item["weighted_total_degree"] * 0.50
        )

    return metrics


def rank_control_plane(metrics):
    ranked = sorted(
        metrics.values(),
        key=lambda item: (
            item["control_plane_score"],
            item["centrality_score"],
            item["family_crossing_edge_total_weight"],
            item["bridge_score"],
            item["self_loop_weight"],
            item["weighted_total_degree"],
            item["cluster_id"],
        ),
        reverse=True,
    )

    for index, item in enumerate(ranked, start=1):
        item["control_plane_rank"] = index

    return ranked


def compact_metric(item):
    if item is None:
        return None

    return {
        "cluster_id": item["cluster_id"],
        "signature_core": item["signature_core"],
        "control_plane_rank": item.get("control_plane_rank"),
        "control_plane_score": item["control_plane_score"],
        "centrality_score": item["centrality_score"],
        "weighted_total_degree": item["weighted_total_degree"],
        "weighted_in_degree": item["weighted_in_degree"],
        "weighted_out_degree": item["weighted_out_degree"],
        "bridge_score": item["bridge_score"],
        "self_loop_weight": item["self_loop_weight"],
        "threshold_edge_total_weight": item["threshold_edge_total_weight"],
        "geometry_edge_total_weight": item["geometry_edge_total_weight"],
        "family_crossing_edge_total_weight": (
            item["family_crossing_edge_total_weight"]
        ),
        "is_bridge": item["is_bridge"],
        "is_source": item["is_source"],
        "is_attractor": item["is_attractor"],
        "is_isolated": item["is_isolated"],
    }


def evaluate_control_plane(records, scenario_name, scenario_type, boundary_axis):
    flat = flatten_records(records)
    clusters = summarize_clusters(flat)

    threshold_edges = build_threshold_edges(records)
    geometry_edges = build_geometry_edges(records)
    edges = merge_edges(threshold_edges, geometry_edges)

    validation = validate_graph(clusters, edges)
    metrics = compute_graph_metrics(clusters, edges)
    ranked = rank_control_plane(metrics)

    dominant = ranked[0] if ranked else None
    second = ranked[1] if len(ranked) > 1 else None

    dominant_id = dominant["cluster_id"] if dominant else None
    second_id = second["cluster_id"] if second else None

    top6 = ranked[:6]
    top6_ids = [item["cluster_id"] for item in top6]

    expected_dominant_rank = None
    expected_second_rank = None

    for item in ranked:
        if item["cluster_id"] == EXPECTED_DOMINANT:
            expected_dominant_rank = item["control_plane_rank"]

        if item["cluster_id"] == EXPECTED_SECOND:
            expected_second_rank = item["control_plane_rank"]

    expected_dominant_present = EXPECTED_DOMINANT in metrics
    expected_second_present = EXPECTED_SECOND in metrics

    expected_pair_present = (
        expected_dominant_present and expected_second_present
    )

    expected_pair_order_preserved = (
        expected_dominant_rank is not None
        and expected_second_rank is not None
        and expected_dominant_rank < expected_second_rank
    )

    top6_contains_expected_pair = (
        EXPECTED_DOMINANT in top6_ids
        and EXPECTED_SECOND in top6_ids
    )

    dominant_top1 = dominant_id == EXPECTED_DOMINANT
    second_top2 = second_id == EXPECTED_SECOND

    robustness_pass = (
        validation["graph_validation_holds"]
        and expected_pair_present
        and expected_pair_order_preserved
        and top6_contains_expected_pair
    )

    strict_pass = robustness_pass and dominant_top1 and second_top2

    dependency_class = classify_boundary_dependency(
        expected_dominant_present=expected_dominant_present,
        expected_second_present=expected_second_present,
        top6_contains_expected_pair=top6_contains_expected_pair,
        expected_pair_order_preserved=expected_pair_order_preserved,
        dominant_top1=dominant_top1,
        second_top2=second_top2,
    )

    return {
        "scenario_name": scenario_name,
        "scenario_type": scenario_type,
        "boundary_axis": boundary_axis,
        "status": "PASS" if robustness_pass else "CHECK",
        "strict_status": "PASS" if strict_pass else "CHECK",
        "dependency_class": dependency_class,
        "record_count": len(records),
        "flat_record_count": len(flat),
        "cluster_count": len(clusters),
        "edge_count": len(edges),
        "threshold_edge_count": len(threshold_edges),
        "geometry_edge_count": len(geometry_edges),
        "graph_validation_holds": validation["graph_validation_holds"],
        "graph_failure_count": validation["failure_count"],
        "dominant_cluster": compact_metric(dominant),
        "second_cluster": compact_metric(second),
        "dominant_cluster_id": dominant_id,
        "second_cluster_id": second_id,
        "expected_dominant_present": expected_dominant_present,
        "expected_second_present": expected_second_present,
        "expected_dominant_rank": expected_dominant_rank,
        "expected_second_rank": expected_second_rank,
        "expected_pair_present": expected_pair_present,
        "expected_pair_order_preserved": expected_pair_order_preserved,
        "top6_contains_expected_pair": top6_contains_expected_pair,
        "dominant_top1": dominant_top1,
        "second_top2": second_top2,
        "top6_cluster_ids": top6_ids,
        "top6_clusters": [compact_metric(item) for item in top6],
        "graph_validation": validation,
    }


def classify_boundary_dependency(
    expected_dominant_present,
    expected_second_present,
    top6_contains_expected_pair,
    expected_pair_order_preserved,
    dominant_top1,
    second_top2,
):
    if not expected_dominant_present or not expected_second_present:
        return "CRITICAL_ABSENCE"

    if not top6_contains_expected_pair:
        return "CRITICAL_TOP6_LOSS"

    if not expected_pair_order_preserved:
        return "CRITICAL_ORDER_INVERSION"

    if not dominant_top1 or not second_top2:
        return "MODERATE_RANK_DRIFT"

    return "STABLE_SUPPORT"


def impact_score(result):
    score = 0.0

    if not result["expected_dominant_present"]:
        score += 100.0

    if not result["expected_second_present"]:
        score += 100.0

    if not result["top6_contains_expected_pair"]:
        score += 50.0

    if not result["expected_pair_order_preserved"]:
        score += 40.0

    if result["expected_dominant_rank"] is not None:
        score += abs(result["expected_dominant_rank"] - 1) * 10.0

    if result["expected_second_rank"] is not None:
        score += abs(result["expected_second_rank"] - 2) * 8.0

    return score


def all_family_values(specs):
    return sorted(set(spec["family"] for spec in specs))


def all_variant_names(specs):
    return sorted(set(spec["name"] for spec in specs))


def filter_specs_by_families(specs, kept_families):
    kept = set(kept_families)

    return [
        spec
        for spec in specs
        if spec["family"] in kept
    ]


def remove_specs_by_families(specs, removed_families):
    removed = set(removed_families)

    return [
        spec
        for spec in specs
        if spec["family"] not in removed
    ]


def remove_specs_by_variants(specs, removed_variants):
    removed = set(removed_variants)

    return [
        spec
        for spec in specs
        if spec["name"] not in removed
    ]


def build_boundary_scenarios():
    specs = cluster_specs()
    families = all_family_values(specs)
    variants = all_variant_names(specs)

    scenarios = [
        {
            "scenario_name": "baseline",
            "scenario_type": "baseline",
            "boundary_axis": "baseline",
            "distance": 0,
            "removed": [],
            "kept": families,
            "specs": specs,
            "confirmation_windows": CONFIRMATION_WINDOWS,
        }
    ]

    for size in [1, 2]:
        for removed in combinations(families, size):
            scenarios.append(
                {
                    "scenario_name": (
                        "remove_family_boundary__"
                        + "__".join(removed)
                    ),
                    "scenario_type": "remove_family_boundary",
                    "boundary_axis": "family",
                    "distance": size,
                    "removed": list(removed),
                    "kept": [
                        family
                        for family in families
                        if family not in removed
                    ],
                    "specs": remove_specs_by_families(specs, removed),
                    "confirmation_windows": CONFIRMATION_WINDOWS,
                }
            )

    for size in [1, 2]:
        for kept in combinations(families, size):
            scenarios.append(
                {
                    "scenario_name": (
                        "keep_family_boundary__"
                        + "__".join(kept)
                    ),
                    "scenario_type": "keep_family_boundary",
                    "boundary_axis": "family",
                    "distance": len(families) - size,
                    "removed": [
                        family
                        for family in families
                        if family not in kept
                    ],
                    "kept": list(kept),
                    "specs": filter_specs_by_families(specs, kept),
                    "confirmation_windows": CONFIRMATION_WINDOWS,
                }
            )

    for size in [1, 2]:
        for removed in combinations(CONFIRMATION_WINDOWS, size):
            kept_thresholds = [
                threshold
                for threshold in CONFIRMATION_WINDOWS
                if threshold not in removed
            ]

            scenarios.append(
                {
                    "scenario_name": (
                        "remove_threshold_boundary__"
                        + "__".join(f"C{item}" for item in removed)
                    ),
                    "scenario_type": "remove_threshold_boundary",
                    "boundary_axis": "threshold",
                    "distance": size,
                    "removed": [f"C{item}" for item in removed],
                    "kept": [f"C{item}" for item in kept_thresholds],
                    "specs": specs,
                    "confirmation_windows": kept_thresholds,
                }
            )

    for size in [1, 2]:
        for kept in combinations(CONFIRMATION_WINDOWS, size):
            scenarios.append(
                {
                    "scenario_name": (
                        "keep_threshold_boundary__"
                        + "__".join(f"C{item}" for item in kept)
                    ),
                    "scenario_type": "keep_threshold_boundary",
                    "boundary_axis": "threshold",
                    "distance": len(CONFIRMATION_WINDOWS) - size,
                    "removed": [
                        f"C{threshold}"
                        for threshold in CONFIRMATION_WINDOWS
                        if threshold not in kept
                    ],
                    "kept": [f"C{item}" for item in kept],
                    "specs": specs,
                    "confirmation_windows": list(kept),
                }
            )

    variant_probe_names = [
        "single_run_len_5",
        "two_runs_len_4_4",
        "three_runs_len_4_4_4",
        "mixed_1_2_3",
        "mixed_1_1_4",
        "staircase_1_2_3_4",
        "long_then_spikes_4_1_1",
        "dense_short_2_2_1_2_1_2",
    ]

    for size in [1, 2]:
        for removed in combinations(variant_probe_names, size):
            scenarios.append(
                {
                    "scenario_name": (
                        "remove_variant_boundary__"
                        + "__".join(removed)
                    ),
                    "scenario_type": "remove_variant_boundary",
                    "boundary_axis": "variant",
                    "distance": size,
                    "removed": list(removed),
                    "kept": [
                        name
                        for name in variants
                        if name not in removed
                    ],
                    "specs": remove_specs_by_variants(specs, removed),
                    "confirmation_windows": CONFIRMATION_WINDOWS,
                }
            )

    return scenarios


def evaluate_boundary_scenarios():
    scenario_definitions = build_boundary_scenarios()
    scenario_results = []

    for scenario in scenario_definitions:
        records = build_records(
            specs=scenario["specs"],
            confirmation_windows=scenario["confirmation_windows"],
        )

        result = evaluate_control_plane(
            records=records,
            scenario_name=scenario["scenario_name"],
            scenario_type=scenario["scenario_type"],
            boundary_axis=scenario["boundary_axis"],
        )

        result["boundary_distance"] = scenario["distance"]
        result["removed"] = scenario["removed"]
        result["kept"] = scenario["kept"]
        result["impact_score"] = impact_score(result)

        scenario_results.append(result)

    return scenario_results


def summarize_boundary_by_axis(scenario_results):
    by_axis = {}

    for result in scenario_results:
        axis = result["boundary_axis"]

        if axis not in by_axis:
            by_axis[axis] = {
                "boundary_axis": axis,
                "scenario_count": 0,
                "pass_count": 0,
                "check_count": 0,
                "strict_pass_count": 0,
                "critical_count": 0,
                "moderate_count": 0,
                "stable_count": 0,
                "impact_scores": [],
                "critical_distances": [],
                "moderate_distances": [],
                "stable_distances": [],
                "critical_scenarios": [],
                "moderate_scenarios": [],
                "stable_scenarios": [],
            }

        item = by_axis[axis]
        item["scenario_count"] += 1
        item["impact_scores"].append(result["impact_score"])

        if result["status"] == "PASS":
            item["pass_count"] += 1
        else:
            item["check_count"] += 1

        if result["strict_status"] == "PASS":
            item["strict_pass_count"] += 1

        dependency_class = result["dependency_class"]

        if dependency_class.startswith("CRITICAL"):
            item["critical_count"] += 1
            item["critical_distances"].append(result["boundary_distance"])
            item["critical_scenarios"].append(result["scenario_name"])

        elif dependency_class.startswith("MODERATE"):
            item["moderate_count"] += 1
            item["moderate_distances"].append(result["boundary_distance"])
            item["moderate_scenarios"].append(result["scenario_name"])

        else:
            item["stable_count"] += 1
            item["stable_distances"].append(result["boundary_distance"])
            item["stable_scenarios"].append(result["scenario_name"])

    for item in by_axis.values():
        scenario_count = item["scenario_count"]

        item["pass_rate"] = item["pass_count"] / scenario_count
        item["check_rate"] = item["check_count"] / scenario_count
        item["strict_pass_rate"] = item["strict_pass_count"] / scenario_count
        item["critical_rate"] = item["critical_count"] / scenario_count
        item["moderate_rate"] = item["moderate_count"] / scenario_count
        item["stable_rate"] = item["stable_count"] / scenario_count
        item["impact_score_mean"] = safe_mean(item["impact_scores"])
        item["impact_score_max"] = (
            max(item["impact_scores"])
            if item["impact_scores"]
            else None
        )
        item["minimum_critical_distance"] = (
            min(item["critical_distances"])
            if item["critical_distances"]
            else None
        )
        item["minimum_moderate_distance"] = (
            min(item["moderate_distances"])
            if item["moderate_distances"]
            else None
        )
        item["minimum_stable_distance"] = (
            min(item["stable_distances"])
            if item["stable_distances"]
            else None
        )

    return by_axis


def summarize_boundary(scenario_results):
    baseline = next(
        result
        for result in scenario_results
        if result["scenario_name"] == "baseline"
    )

    non_baseline_results = [
        result
        for result in scenario_results
        if result["scenario_name"] != "baseline"
    ]

    by_axis = summarize_boundary_by_axis(non_baseline_results)

    critical_results = [
        result
        for result in non_baseline_results
        if result["dependency_class"].startswith("CRITICAL")
    ]

    moderate_results = [
        result
        for result in non_baseline_results
        if result["dependency_class"].startswith("MODERATE")
    ]

    stable_results = [
        result
        for result in non_baseline_results
        if result["dependency_class"] == "STABLE_SUPPORT"
    ]

    sorted_critical = sorted(
        critical_results,
        key=lambda result: (
            result["boundary_distance"],
            -result["impact_score"],
            result["scenario_name"],
        ),
    )

    sorted_moderate = sorted(
        moderate_results,
        key=lambda result: (
            result["boundary_distance"],
            -result["impact_score"],
            result["scenario_name"],
        ),
    )

    sorted_stable = sorted(
        stable_results,
        key=lambda result: (
            result["boundary_distance"],
            result["scenario_name"],
        ),
    )

    minimum_critical_distance = (
        sorted_critical[0]["boundary_distance"]
        if sorted_critical
        else None
    )

    minimum_moderate_distance = (
        sorted_moderate[0]["boundary_distance"]
        if sorted_moderate
        else None
    )

    minimum_critical_scenarios = [
        result
        for result in sorted_critical
        if result["boundary_distance"] == minimum_critical_distance
    ]

    boundary_detected = (
        baseline["status"] == "PASS"
        and baseline["strict_status"] == "PASS"
        and len(critical_results) > 0
        and len(moderate_results) > 0
        and len(stable_results) > 0
        and by_axis.get("threshold", {}).get("minimum_critical_distance")
        is not None
        and by_axis.get("family", {}).get("minimum_critical_distance")
        is not None
    )

    return {
        "baseline_status": baseline["status"],
        "baseline_strict_status": baseline["strict_status"],
        "boundary_scenario_count": len(non_baseline_results),
        "critical_boundary_count": len(critical_results),
        "moderate_boundary_count": len(moderate_results),
        "stable_boundary_count": len(stable_results),
        "minimum_critical_distance": minimum_critical_distance,
        "minimum_moderate_distance": minimum_moderate_distance,
        "minimum_critical_scenario_names": [
            result["scenario_name"]
            for result in minimum_critical_scenarios
        ],
        "minimum_critical_scenarios": [
            compact_boundary_record(result)
            for result in minimum_critical_scenarios
        ],
        "top_critical_boundaries": [
            compact_boundary_record(result)
            for result in sorted_critical[:12]
        ],
        "top_moderate_boundaries": [
            compact_boundary_record(result)
            for result in sorted_moderate[:12]
        ],
        "top_stable_boundaries": [
            compact_boundary_record(result)
            for result in sorted_stable[:12]
        ],
        "by_axis": by_axis,
        "dependency_boundary_detected": boundary_detected,
        "boundary_rule": (
            "Boundary distance is the perturbation size required to move "
            "the expected control-plane pair from stable support into "
            "moderate rank drift or critical failure."
        ),
    }


def compact_boundary_record(result):
    return {
        "scenario_name": result["scenario_name"],
        "scenario_type": result["scenario_type"],
        "boundary_axis": result["boundary_axis"],
        "boundary_distance": result["boundary_distance"],
        "removed": result["removed"],
        "kept": result["kept"],
        "status": result["status"],
        "strict_status": result["strict_status"],
        "dependency_class": result["dependency_class"],
        "impact_score": result["impact_score"],
        "expected_dominant_rank": result["expected_dominant_rank"],
        "expected_second_rank": result["expected_second_rank"],
        "dominant_cluster_id": result["dominant_cluster_id"],
        "second_cluster_id": result["second_cluster_id"],
        "top6_contains_expected_pair": result["top6_contains_expected_pair"],
        "expected_pair_order_preserved": (
            result["expected_pair_order_preserved"]
        ),
    }


def main():
    scenario_results = evaluate_boundary_scenarios()
    boundary_summary = summarize_boundary(scenario_results)

    status = (
        "PASS"
        if boundary_summary["dependency_boundary_detected"]
        else "CHECK"
    )

    payload = {
        "experiment": (
            "temporal_collapse_topology_dependency_boundary_v0"
        ),
        "version": VERSION,
        "status": status,
        "summary": {
            "baseline_status": boundary_summary["baseline_status"],
            "baseline_strict_status": (
                boundary_summary["baseline_strict_status"]
            ),
            "boundary_scenario_count": (
                boundary_summary["boundary_scenario_count"]
            ),
            "critical_boundary_count": (
                boundary_summary["critical_boundary_count"]
            ),
            "moderate_boundary_count": (
                boundary_summary["moderate_boundary_count"]
            ),
            "stable_boundary_count": (
                boundary_summary["stable_boundary_count"]
            ),
            "minimum_critical_distance": (
                boundary_summary["minimum_critical_distance"]
            ),
            "minimum_moderate_distance": (
                boundary_summary["minimum_moderate_distance"]
            ),
            "minimum_critical_scenario_names": (
                boundary_summary["minimum_critical_scenario_names"]
            ),
            "expected_dominant_control_cluster": EXPECTED_DOMINANT,
            "expected_second_control_cluster": EXPECTED_SECOND,
            "dependency_boundary_detected": (
                boundary_summary["dependency_boundary_detected"]
            ),
            "method": "dependency_boundary",
        },
        "dependency_boundary_summary": boundary_summary,
        "scenario_results": [
            compact_boundary_record(result)
            for result in scenario_results
        ],
        "interpretation": {
            "main_result": "dependency boundary detected",
            "structural_conclusion": (
                "The control plane has a measurable perturbation boundary. "
                "Some one-step perturbations remain stable, some cause "
                "moderate rank drift, and some produce critical loss or "
                "order inversion."
            ),
            "important_boundary": (
                "This experiment measures structural boundary behavior. "
                "It does not claim semantic causality or external model "
                "correctness."
            ),
        },
        "final_check": {
            "status": status,
            "message": (
                "dependency boundary detected"
                if status == "PASS"
                else "dependency boundary was not fully confirmed"
            ),
        },
        "reproduction_command": (
            "python examples/"
            "temporal_collapse_topology_dependency_boundary_v0.py"
        ),
    }

    RESULTS_PATH.parent.mkdir(parents=True, exist_ok=True)
    RESULTS_PATH.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    print("=" * 80)
    print(
        "OMNIA-VALIDATION - "
        "Temporal Collapse Topology Dependency Boundary v0"
    )
    print("=" * 80)
    print()

    print("Status:", status)
    print("Version:", VERSION)

    print()
    print("Summary")
    print("-" * 80)

    for key, value in payload["summary"].items():
        print(f"{key}: {value}")

    print()
    print("By boundary axis")
    print("-" * 80)

    for axis, item in boundary_summary["by_axis"].items():
        print(
            f"axis={axis:<10} "
            f"scenarios={item['scenario_count']} "
            f"pass={item['pass_count']} "
            f"check={item['check_count']} "
            f"strict={item['strict_pass_count']} "
            f"critical={item['critical_count']} "
            f"moderate={item['moderate_count']} "
            f"stable={item['stable_count']} "
            f"min_critical={item['minimum_critical_distance']} "
            f"min_moderate={item['minimum_moderate_distance']} "
            f"impact_mean={item['impact_score_mean']} "
            f"impact_max={item['impact_score_max']}"
        )

    print()
    print("Minimum critical boundaries")
    print("-" * 80)

    for item in boundary_summary["minimum_critical_scenarios"]:
        print(
            f"scenario={item['scenario_name']:<64} "
            f"axis={item['boundary_axis']:<10} "
            f"distance={item['boundary_distance']} "
            f"class={item['dependency_class']} "
            f"impact={item['impact_score']} "
            f"dom_rank={item['expected_dominant_rank']} "
            f"sec_rank={item['expected_second_rank']}"
        )

    print()
    print("Top critical boundaries")
    print("-" * 80)

    for item in boundary_summary["top_critical_boundaries"]:
        print(
            f"scenario={item['scenario_name']:<64} "
            f"axis={item['boundary_axis']:<10} "
            f"distance={item['boundary_distance']} "
            f"class={item['dependency_class']} "
            f"impact={item['impact_score']} "
            f"dom_rank={item['expected_dominant_rank']} "
            f"sec_rank={item['expected_second_rank']}"
        )

    print()
    print("Top moderate boundaries")
    print("-" * 80)

    for item in boundary_summary["top_moderate_boundaries"]:
        print(
            f"scenario={item['scenario_name']:<64} "
            f"axis={item['boundary_axis']:<10} "
            f"distance={item['boundary_distance']} "
            f"class={item['dependency_class']} "
            f"impact={item['impact_score']} "
            f"dom_rank={item['expected_dominant_rank']} "
            f"sec_rank={item['expected_second_rank']}"
        )

    print()
    print("Top stable boundaries")
    print("-" * 80)

    for item in boundary_summary["top_stable_boundaries"]:
        print(
            f"scenario={item['scenario_name']:<64} "
            f"axis={item['boundary_axis']:<10} "
            f"distance={item['boundary_distance']} "
            f"class={item['dependency_class']} "
            f"dom_rank={item['expected_dominant_rank']} "
            f"sec_rank={item['expected_second_rank']}"
        )

    print()
    print("Final validation")
    print("-" * 80)

    print(
        "dependency_boundary_detected:",
        boundary_summary["dependency_boundary_detected"],
    )

    print()
    print("=" * 80)
    print("FINAL CHECK")
    print("=" * 80)

    if status == "PASS":
        print(
            "PASS - dependency boundary detected: the control plane has "
            "measurable stable, moderate, and critical perturbation "
            "boundaries."
        )
    else:
        print(
            "CHECK - dependency boundary was not fully confirmed under "
            "the tested perturbation scenarios."
        )

    print()
    print("=" * 80)
    print("Result saved to:", RESULTS_PATH)
    print("=" * 80)


if __name__ == "__main__":
    main()