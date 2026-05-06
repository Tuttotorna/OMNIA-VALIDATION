import json
from pathlib import Path
from statistics import mean, pstdev

VERSION = "0.1.0"

RESULTS_PATH = Path(
    "results/temporal_collapse_topology_cluster_graph_control_plane_v0.json"
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
        1 for length in run_lengths if length >= confirmation_window
    )

    persistence_reset_count = max(collapse_run_count - 1, 0)

    fragmentation_index = (
        persistence_reset_count / max(collapse_run_count, 1)
    )

    global_persistence_detected = any(
        length >= persistence_threshold for length in run_lengths
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


def cluster_specs():
    return [
        {"family": "single_run", "name": "single_run_len_1", "run_lengths": [1]},
        {"family": "single_run", "name": "single_run_len_2", "run_lengths": [2]},
        {"family": "single_run", "name": "single_run_len_3", "run_lengths": [3]},
        {"family": "single_run", "name": "single_run_len_4", "run_lengths": [4]},
        {"family": "single_run", "name": "single_run_len_5", "run_lengths": [5]},

        {"family": "two_equal_runs", "name": "two_runs_len_1_1", "run_lengths": [1, 1]},
        {"family": "two_equal_runs", "name": "two_runs_len_2_2", "run_lengths": [2, 2]},
        {"family": "two_equal_runs", "name": "two_runs_len_3_3", "run_lengths": [3, 3]},
        {"family": "two_equal_runs", "name": "two_runs_len_4_4", "run_lengths": [4, 4]},

        {"family": "three_equal_runs", "name": "three_runs_len_1_1_1", "run_lengths": [1, 1, 1]},
        {"family": "three_equal_runs", "name": "three_runs_len_2_2_2", "run_lengths": [2, 2, 2]},
        {"family": "three_equal_runs", "name": "three_runs_len_3_3_3", "run_lengths": [3, 3, 3]},
        {"family": "three_equal_runs", "name": "three_runs_len_4_4_4", "run_lengths": [4, 4, 4]},

        {"family": "mixed_same_cost", "name": "mixed_1_2_3", "run_lengths": [1, 2, 3]},
        {"family": "mixed_same_cost", "name": "mixed_1_1_4", "run_lengths": [1, 1, 4]},
        {"family": "mixed_same_cost", "name": "mixed_2_2_2", "run_lengths": [2, 2, 2]},
        {"family": "mixed_same_cost", "name": "mixed_1_3_2", "run_lengths": [1, 3, 2]},

        {"family": "staircase", "name": "staircase_1_2_3_4", "run_lengths": [1, 2, 3, 4]},
        {"family": "staircase", "name": "staircase_1_2_3_4_5", "run_lengths": [1, 2, 3, 4, 5]},
        {"family": "staircase", "name": "staircase_2_3_4_5", "run_lengths": [2, 3, 4, 5]},

        {"family": "spike_plus_long", "name": "long_then_spikes_4_1_1", "run_lengths": [4, 1, 1]},
        {"family": "spike_plus_long", "name": "long_then_spikes_5_1_1", "run_lengths": [5, 1, 1]},
        {"family": "spike_plus_long", "name": "long_then_spikes_6_1_1_1", "run_lengths": [6, 1, 1, 1]},
        {"family": "spike_plus_long", "name": "long_then_spikes_7_1_1_1", "run_lengths": [7, 1, 1, 1]},

        {"family": "dense_short", "name": "dense_short_2_1_2_1", "run_lengths": [2, 1, 2, 1]},
        {"family": "dense_short", "name": "dense_short_2_2_1_2_1", "run_lengths": [2, 2, 1, 2, 1]},
        {"family": "dense_short", "name": "dense_short_2_2_1_2_1_2", "run_lengths": [2, 2, 1, 2, 1, 2]},
        {"family": "dense_short", "name": "dense_short_3_2_1_2_1_2", "run_lengths": [3, 2, 1, 2, 1, 2]},
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

    for variant_index, spec in enumerate(cluster_specs()):
        length, runs = make_sequence_from_lengths(spec["run_lengths"])
        sequence = make_sequence(length, runs)
        features = geometry_features(spec["run_lengths"])
        transition_results = []

        for confirmation_window in CONFIRMATION_WINDOWS:
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

            transition_results.append({
                "confirmation_window": confirmation_window,
                "source_class": source_metrics["classification"],
                "transition_cost": transition_cost,
                "remaining_run_count": remaining_run_count,
                "remaining_run_lengths": remaining_lengths,
                "predicted_destination_class": predicted_destination,
                "observed_destination_class": observed_destination,
                "cluster_id": cluster_id,
                "signature_core": signature_core,
                "destination_matches_rule": predicted_destination == observed_destination,
            })

        records.append({
            "variant_index": variant_index,
            "family": spec["family"],
            "geometry_name": spec["name"],
            "run_lengths": spec["run_lengths"],
            "trajectory_length": length,
            "runs": runs,
            "features": features,
            "transition_results": transition_results,
            "method": "cluster_graph_control_plane",
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
                "observed_destination_class": item["observed_destination_class"],
                "cluster_id": item["cluster_id"],
                "signature_core": item["signature_core"],
                "destination_matches_rule": item["destination_matches_rule"],
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
        cluster["source_class_variation"] = len(cluster["source_class_values"]) > 1
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
                    "from_confirmation_window": left["confirmation_window"],
                    "to_confirmation_window": right["confirmation_window"],
                    "confirmation_window": right["confirmation_window"],
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

        for left_record, right_record in zip(ordered_records, ordered_records[1:]):
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
            value for value in set(edge["families"]) if value is not None
        )
        edge["geometry_name_values"] = sorted(
            value for value in set(edge["geometry_names"]) if value is not None
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

        item["control_balance_score"] = 1.0 / (
            1.0 + abs(item["weighted_in_degree"] - item["weighted_out_degree"])
        )

        item["control_signature"] = (
            f"control={item['control_plane_score']}"
            f"|centrality={item['centrality_score']}"
            f"|bridge={item['bridge_score']}"
            f"|family_cross={item['family_crossing_edge_total_weight']}"
            f"|self={item['self_loop_weight']}"
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
    return {
        "cluster_id": item["cluster_id"],
        "signature_core": item["signature_core"],
        "control_plane_rank": item.get("control_plane_rank"),
        "control_plane_score": item["control_plane_score"],
        "centrality_score": item["centrality_score"],
        "weighted_total_degree": item["weighted_total_degree"],
        "weighted_in_degree": item["weighted_in_degree"],
        "weighted_out_degree": item["weighted_out_degree"],
        "in_degree": item["in_degree"],
        "out_degree": item["out_degree"],
        "bridge_score": item["bridge_score"],
        "self_loop_weight": item["self_loop_weight"],
        "threshold_edge_total_weight": item["threshold_edge_total_weight"],
        "geometry_edge_total_weight": item["geometry_edge_total_weight"],
        "family_crossing_edge_total_weight": (
            item["family_crossing_edge_total_weight"]
        ),
        "neighbor_count": item["neighbor_count"],
        "control_balance_score": item["control_balance_score"],
        "is_bridge": item["is_bridge"],
        "is_source": item["is_source"],
        "is_attractor": item["is_attractor"],
        "is_isolated": item["is_isolated"],
        "family_values": item["family_values"],
        "source_class_values": item["source_class_values"],
    }


def select_control_plane_members(ranked):
    if not ranked:
        return []

    top_score = ranked[0]["control_plane_score"]
    cutoff = top_score * 0.30

    members = [
        item
        for item in ranked
        if (
            item["control_plane_score"] >= cutoff
            or item["family_crossing_edge_total_weight"] > 0
        )
    ]

    return members


def summarize_by_remaining_count(metrics):
    grouped = {}

    for item in metrics.values():
        remaining = str(item["remaining_run_count"])

        if remaining not in grouped:
            grouped[remaining] = {
                "remaining_run_count": item["remaining_run_count"],
                "cluster_count": 0,
                "control_plane_scores": [],
                "centrality_scores": [],
                "bridge_scores": [],
                "family_crossing_weights": [],
                "clusters": [],
            }

        grouped[remaining]["cluster_count"] += 1
        grouped[remaining]["control_plane_scores"].append(
            item["control_plane_score"]
        )
        grouped[remaining]["centrality_scores"].append(
            item["centrality_score"]
        )
        grouped[remaining]["bridge_scores"].append(item["bridge_score"])
        grouped[remaining]["family_crossing_weights"].append(
            item["family_crossing_edge_total_weight"]
        )
        grouped[remaining]["clusters"].append(item["cluster_id"])

    for item in grouped.values():
        item["control_plane_score_mean"] = safe_mean(
            item["control_plane_scores"]
        )
        item["centrality_score_mean"] = safe_mean(item["centrality_scores"])
        item["bridge_score_mean"] = safe_mean(item["bridge_scores"])
        item["family_crossing_weight_mean"] = safe_mean(
            item["family_crossing_weights"]
        )
        item["clusters"] = sorted(item["clusters"])

    return grouped


def summarize_by_destination(metrics):
    grouped = {}

    for item in metrics.values():
        destination = item["destination_class"]

        if destination not in grouped:
            grouped[destination] = {
                "destination_class": destination,
                "cluster_count": 0,
                "control_plane_scores": [],
                "centrality_scores": [],
                "bridge_scores": [],
                "family_crossing_weights": [],
                "clusters": [],
            }

        grouped[destination]["cluster_count"] += 1
        grouped[destination]["control_plane_scores"].append(
            item["control_plane_score"]
        )
        grouped[destination]["centrality_scores"].append(
            item["centrality_score"]
        )
        grouped[destination]["bridge_scores"].append(item["bridge_score"])
        grouped[destination]["family_crossing_weights"].append(
            item["family_crossing_edge_total_weight"]
        )
        grouped[destination]["clusters"].append(item["cluster_id"])

    for item in grouped.values():
        item["control_plane_score_mean"] = safe_mean(
            item["control_plane_scores"]
        )
        item["centrality_score_mean"] = safe_mean(item["centrality_scores"])
        item["bridge_score_mean"] = safe_mean(item["bridge_scores"])
        item["family_crossing_weight_mean"] = safe_mean(
            item["family_crossing_weights"]
        )
        item["clusters"] = sorted(item["clusters"])

    return grouped


def validate_control_plane(
    validation,
    ranked,
    control_plane_members,
    expected_dominant,
    expected_second,
):
    failures = []

    if not validation["graph_validation_holds"]:
        failures.append({
            "reason": "graph_validation_failed",
            "graph_failures": validation["failures"],
        })

    if not ranked:
        failures.append({"reason": "empty_control_plane_ranking"})

    if ranked and ranked[0]["cluster_id"] != expected_dominant:
        failures.append({
            "reason": "dominant_control_cluster_mismatch",
            "expected": expected_dominant,
            "observed": ranked[0]["cluster_id"],
        })

    if len(ranked) > 1 and ranked[1]["cluster_id"] != expected_second:
        failures.append({
            "reason": "second_control_cluster_mismatch",
            "expected": expected_second,
            "observed": ranked[1]["cluster_id"],
        })

    member_ids = {item["cluster_id"] for item in control_plane_members}

    if expected_dominant not in member_ids:
        failures.append({
            "reason": "dominant_control_cluster_missing_from_control_plane",
            "expected": expected_dominant,
        })

    if expected_second not in member_ids:
        failures.append({
            "reason": "second_control_cluster_missing_from_control_plane",
            "expected": expected_second,
        })

    return {
        "control_plane_validation_holds": len(failures) == 0,
        "failure_count": len(failures),
        "failures": failures,
    }


def summarize(records):
    flat = flatten_records(records)
    clusters = summarize_clusters(flat)

    threshold_edges = build_threshold_edges(records)
    geometry_edges = build_geometry_edges(records)
    edges = merge_edges(threshold_edges, geometry_edges)

    graph_validation = validate_graph(clusters, edges)

    metrics = compute_graph_metrics(clusters, edges)
    ranked = rank_control_plane(metrics)
    control_plane_members = select_control_plane_members(ranked)

    expected_dominant = (
        "cost=0|remaining=3|dest=OSCILLATING_NONPERSISTENT"
    )
    expected_second = (
        "cost=3|remaining=3|dest=OSCILLATING_NONPERSISTENT"
    )

    control_validation = validate_control_plane(
        graph_validation,
        ranked,
        control_plane_members,
        expected_dominant,
        expected_second,
    )

    dominant = ranked[0] if ranked else None
    second = ranked[1] if len(ranked) > 1 else None

    source_clusters = {
        cluster_id: item
        for cluster_id, item in metrics.items()
        if item["is_source"]
    }

    attractor_clusters = {
        cluster_id: item
        for cluster_id, item in metrics.items()
        if item["is_attractor"]
    }

    bridge_clusters = {
        cluster_id: item
        for cluster_id, item in metrics.items()
        if item["is_bridge"]
    }

    isolated_clusters = {
        cluster_id: item
        for cluster_id, item in metrics.items()
        if item["is_isolated"]
    }

    control_plane_detected = (
        graph_validation["graph_validation_holds"]
        and control_validation["control_plane_validation_holds"]
    )

    return {
        "record_count": len(records),
        "flat_record_count": len(flat),
        "cluster_count": len(clusters),
        "edge_count": len(edges),
        "threshold_edge_count": len(threshold_edges),
        "geometry_edge_count": len(geometry_edges),
        "clusters": clusters,
        "edges": edges,
        "graph_validation": graph_validation,
        "metrics": metrics,
        "control_plane_ranking": ranked,
        "control_plane_members": control_plane_members,
        "dominant_control_cluster": dominant,
        "second_control_cluster": second,
        "expected_dominant_control_cluster": expected_dominant,
        "expected_second_control_cluster": expected_second,
        "control_plane_validation": control_validation,
        "control_plane_detected": control_plane_detected,
        "source_clusters": source_clusters,
        "attractor_clusters": attractor_clusters,
        "bridge_clusters": bridge_clusters,
        "isolated_clusters": isolated_clusters,
        "remaining_count_summary": summarize_by_remaining_count(metrics),
        "destination_summary": summarize_by_destination(metrics),
    }


def compact_record(record):
    return {
        "variant_index": record["variant_index"],
        "family": record["family"],
        "geometry_name": record["geometry_name"],
        "run_lengths": record["run_lengths"],
        "features": record["features"],
        "transition_results": record["transition_results"],
        "method": record["method"],
    }


def main():
    records = build_records()
    analysis = summarize(records)

    status = "PASS" if analysis["control_plane_detected"] else "CHECK"

    ranking_compact = [
        compact_metric(item)
        for item in analysis["control_plane_ranking"]
    ]

    members_compact = [
        compact_metric(item)
        for item in analysis["control_plane_members"]
    ]

    dominant = (
        compact_metric(analysis["dominant_control_cluster"])
        if analysis["dominant_control_cluster"]
        else None
    )

    second = (
        compact_metric(analysis["second_control_cluster"])
        if analysis["second_control_cluster"]
        else None
    )

    control_plane_member_ids = [
        item["cluster_id"]
        for item in members_compact
    ]

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
        "source_cluster_count": len(analysis["source_clusters"]),
        "attractor_cluster_count": len(analysis["attractor_clusters"]),
        "bridge_cluster_count": len(analysis["bridge_clusters"]),
        "isolated_cluster_count": len(analysis["isolated_clusters"]),
        "control_plane_member_count": len(members_compact),
        "dominant_control_cluster": (
            dominant["cluster_id"] if dominant else None
        ),
        "dominant_control_plane_score": (
            dominant["control_plane_score"] if dominant else None
        ),
        "dominant_centrality_score": (
            dominant["centrality_score"] if dominant else None
        ),
        "second_control_cluster": (
            second["cluster_id"] if second else None
        ),
        "second_control_plane_score": (
            second["control_plane_score"] if second else None
        ),
        "second_centrality_score": (
            second["centrality_score"] if second else None
        ),
        "expected_dominant_control_cluster": (
            analysis["expected_dominant_control_cluster"]
        ),
        "expected_second_control_cluster": (
            analysis["expected_second_control_cluster"]
        ),
        "dominant_control_cluster_matches_expected": (
            dominant is not None
            and dominant["cluster_id"]
            == analysis["expected_dominant_control_cluster"]
        ),
        "second_control_cluster_matches_expected": (
            second is not None
            and second["cluster_id"]
            == analysis["expected_second_control_cluster"]
        ),
        "graph_validation_holds": (
            analysis["graph_validation"]["graph_validation_holds"]
        ),
        "graph_failure_count": (
            analysis["graph_validation"]["failure_count"]
        ),
        "control_plane_validation_holds": (
            analysis["control_plane_validation"][
                "control_plane_validation_holds"
            ]
        ),
        "control_plane_failure_count": (
            analysis["control_plane_validation"]["failure_count"]
        ),
        "control_plane_detected": analysis["control_plane_detected"],
        "method": "cluster_graph_control_plane",
    }

    payload = {
        "experiment": (
            "temporal_collapse_topology_cluster_graph_control_plane_v0"
        ),
        "version": VERSION,
        "status": status,
        "summary": summary,
        "cluster_graph_control_plane_summary": {
            "record_count": analysis["record_count"],
            "flat_record_count": analysis["flat_record_count"],
            "cluster_count": analysis["cluster_count"],
            "edge_count": analysis["edge_count"],
            "threshold_edge_count": analysis["threshold_edge_count"],
            "geometry_edge_count": analysis["geometry_edge_count"],
            "graph_validation": analysis["graph_validation"],
            "control_plane_validation": analysis["control_plane_validation"],
            "control_plane_detected": analysis["control_plane_detected"],
            "control_plane_score_definition": (
                "control_plane_score = centrality_score "
                "+ 1.50*family_crossing_edge_total_weight "
                "+ 1.25*bridge_score "
                "+ 1.00*self_loop_weight "
                "+ 0.50*threshold_edge_total_weight "
                "+ 0.50*geometry_edge_total_weight "
                "+ 0.50*weighted_total_degree"
            ),
            "expected_dominant_control_cluster": (
                analysis["expected_dominant_control_cluster"]
            ),
            "expected_second_control_cluster": (
                analysis["expected_second_control_cluster"]
            ),
            "dominant_control_cluster": dominant,
            "second_control_cluster": second,
            "control_plane_member_ids": control_plane_member_ids,
            "control_plane_members": members_compact,
            "control_plane_ranking": ranking_compact,
            "source_clusters": {
                cluster_id: compact_metric(item)
                for cluster_id, item in analysis["source_clusters"].items()
            },
            "attractor_clusters": {
                cluster_id: compact_metric(item)
                for cluster_id, item in analysis["attractor_clusters"].items()
            },
            "bridge_clusters": {
                cluster_id: compact_metric(item)
                for cluster_id, item in analysis["bridge_clusters"].items()
            },
            "isolated_clusters": {
                cluster_id: compact_metric(item)
                for cluster_id, item in analysis["isolated_clusters"].items()
            },
            "remaining_count_summary": analysis["remaining_count_summary"],
            "destination_summary": analysis["destination_summary"],
        },
        "geometry_records": [
            compact_record(record)
            for record in records
        ],
        "interpretation": (
            "This experiment separates control-plane clusters from ordinary "
            "bridge clusters inside the invariant signature-cluster graph. "
            "It weights graph centrality, bridge load, family-crossing "
            "evidence, threshold participation, geometry participation, "
            "and self-loop persistence."
        ),
        "reproduction_command": (
            "python examples/"
            "temporal_collapse_topology_cluster_graph_control_plane_v0.py"
        ),
    }

    RESULTS_PATH.parent.mkdir(parents=True, exist_ok=True)
    RESULTS_PATH.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    print("=" * 80)
    print(
        "OMNIA-VALIDATION - "
        "Temporal Collapse Topology Cluster Graph Control Plane v0"
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
    print("Control-plane ranking")
    print("-" * 80)

    for item in ranking_compact:
        print(
            f"rank={item['control_plane_rank']:<2} "
            f"cluster={item['cluster_id']:<64} "
            f"control={item['control_plane_score']} "
            f"centrality={item['centrality_score']} "
            f"wdeg={item['weighted_total_degree']} "
            f"win={item['weighted_in_degree']} "
            f"wout={item['weighted_out_degree']} "
            f"bridge={item['bridge_score']} "
            f"self={item['self_loop_weight']} "
            f"threshold={item['threshold_edge_total_weight']} "
            f"geometry={item['geometry_edge_total_weight']} "
            f"family_cross={item['family_crossing_edge_total_weight']}"
        )

    print()
    print("Control-plane members")
    print("-" * 80)

    for item in members_compact:
        print(
            f"rank={item['control_plane_rank']:<2} "
            f"cluster={item['cluster_id']:<64} "
            f"control={item['control_plane_score']} "
            f"centrality={item['centrality_score']} "
            f"family_cross={item['family_crossing_edge_total_weight']} "
            f"bridge={item['bridge_score']}"
        )

    print()
    print("Dominant control cluster")
    print("-" * 80)

    if dominant:
        for key in [
            "cluster_id",
            "control_plane_score",
            "centrality_score",
            "weighted_total_degree",
            "weighted_in_degree",
            "weighted_out_degree",
            "bridge_score",
            "self_loop_weight",
            "threshold_edge_total_weight",
            "geometry_edge_total_weight",
            "family_crossing_edge_total_weight",
        ]:
            print(f"{key}: {dominant.get(key)}")

    print()
    print("Second control cluster")
    print("-" * 80)

    if second:
        for key in [
            "cluster_id",
            "control_plane_score",
            "centrality_score",
            "weighted_total_degree",
            "weighted_in_degree",
            "weighted_out_degree",
            "bridge_score",
            "self_loop_weight",
            "threshold_edge_total_weight",
            "geometry_edge_total_weight",
            "family_crossing_edge_total_weight",
        ]:
            print(f"{key}: {second.get(key)}")

    print()
    print("By remaining run count")
    print("-" * 80)

    for remaining, item in analysis["remaining_count_summary"].items():
        print(
            f"remaining={remaining:<2} "
            f"clusters={item['cluster_count']} "
            f"control_mean={item['control_plane_score_mean']} "
            f"centrality_mean={item['centrality_score_mean']} "
            f"bridge_mean={item['bridge_score_mean']} "
            f"family_cross_mean={item['family_crossing_weight_mean']}"
        )

    print()
    print("By destination")
    print("-" * 80)

    for destination, item in analysis["destination_summary"].items():
        print(
            f"destination={destination:<28} "
            f"clusters={item['cluster_count']} "
            f"control_mean={item['control_plane_score_mean']} "
            f"centrality_mean={item['centrality_score_mean']} "
            f"bridge_mean={item['bridge_score_mean']} "
            f"family_cross_mean={item['family_crossing_weight_mean']}"
        )

    print()
    print("Graph validation")
    print("-" * 80)

    graph_validation = analysis["graph_validation"]

    print(
        "graph_validation_holds:",
        graph_validation["graph_validation_holds"],
    )
    print("failure_count:", graph_validation["failure_count"])

    if graph_validation["failures"]:
        print("failures:", graph_validation["failures"])

    print()
    print("Control-plane validation")
    print("-" * 80)

    control_validation = analysis["control_plane_validation"]

    print(
        "control_plane_validation_holds:",
        control_validation["control_plane_validation_holds"],
    )
    print("failure_count:", control_validation["failure_count"])

    if control_validation["failures"]:
        print("failures:", control_validation["failures"])

    print()
    print("=" * 80)
    print("FINAL CHECK")
    print("=" * 80)

    if status == "PASS":
        print(
            "PASS - signature-cluster control plane detected: "
            "dominant and second control clusters matched the expected "
            "remaining=3 OSCILLATING_NONPERSISTENT control layer."
        )
    else:
        print(
            "CHECK - signature-cluster control plane was not fully "
            "confirmed under the expected dominance criteria."
        )

    print()
    print("=" * 80)
    print("Result saved to:", RESULTS_PATH)
    print("=" * 80)


if __name__ == "__main__":
    main()