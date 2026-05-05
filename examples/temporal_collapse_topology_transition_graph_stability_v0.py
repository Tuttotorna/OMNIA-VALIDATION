import itertools
import json
from pathlib import Path
from statistics import mean, pstdev

VERSION = "0.1.0"

RESULTS_PATH = Path(
    "results/temporal_collapse_topology_transition_graph_stability_v0.json"
)

CONFIRMATION_WINDOW = 2
PERSISTENCE_WINDOW = 2
GLOBAL_PERSISTENCE_THRESHOLD = (
    CONFIRMATION_WINDOW + PERSISTENCE_WINDOW
)

SUPPORTED_CLASSES = [
    "GLOBAL_PERSISTENT_COLLAPSE",
    "RECOVERY_RELAPSE_COLLAPSE",
    "FRAGMENTED_LOCAL_COLLAPSE",
    "OSCILLATING_NONPERSISTENT",
    "SPIKE_FILTERED",
    "CLEAN_PASS",
]

MUTATION_VALUES = [
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


def classify(sequence):
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
        if length >= CONFIRMATION_WINDOW
    )

    persistence_reset_count = max(
        collapse_run_count - 1,
        0,
    )

    fragmentation_index = (
        persistence_reset_count / max(collapse_run_count, 1)
    )

    global_persistence_detected = any(
        length >= GLOBAL_PERSISTENCE_THRESHOLD
        for length in run_lengths
    )

    if collapse_run_count == 0:
        label = "CLEAN_PASS"

    elif (
        collapse_run_count == 1
        and max_run_length < CONFIRMATION_WINDOW
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
        "collapse_run_count": collapse_run_count,
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


def base_case_variants():
    variants = {}

    variants["clean_pass"] = [
        make_sequence(12, []),
        make_sequence(16, []),
        make_sequence(20, []),
    ]

    variants["spike_filtered"] = [
        make_sequence(12, [(4, 1)]),
        make_sequence(16, [(7, 1)]),
        make_sequence(20, [(10, 1)]),
    ]

    variants["oscillating_nonpersistent"] = [
        make_sequence(14, [(3, 1), (6, 1), (9, 1)]),
        make_sequence(18, [(4, 1), (8, 1), (12, 1)]),
        make_sequence(22, [(5, 1), (10, 1), (15, 1)]),
    ]

    variants["fragmented_local_collapse"] = [
        make_sequence(18, [(3, 2), (7, 2), (11, 2)]),
        make_sequence(22, [(4, 2), (9, 2), (14, 2)]),
        make_sequence(26, [(5, 2), (11, 2), (17, 2)]),
    ]

    variants["global_persistent_collapse"] = [
        make_sequence(18, [(6, 8)]),
        make_sequence(22, [(8, 8)]),
        make_sequence(26, [(10, 8)]),
    ]

    variants["recovery_relapse_collapse"] = [
        make_sequence(20, [(3, 2), (10, 6)]),
        make_sequence(24, [(4, 2), (12, 6)]),
        make_sequence(28, [(5, 2), (14, 6)]),
    ]

    return variants


def mutate_sequence(sequence, mutations):
    mutated = list(sequence)

    for index, new_value in mutations:
        if 0 <= index < len(mutated):
            mutated[index] = new_value

    return mutated


def candidate_mutations(sequence, depth):
    indices = list(range(len(sequence)))

    if depth == 1:
        for index in indices:
            old_value = sequence[index]

            for new_value in MUTATION_VALUES:
                if new_value != old_value:
                    yield [(index, new_value)]

    elif depth == 2:
        for i, j in itertools.combinations(indices, 2):
            old_i = sequence[i]
            old_j = sequence[j]

            possible_i = [
                value
                for value in MUTATION_VALUES
                if value != old_i
            ]

            possible_j = [
                value
                for value in MUTATION_VALUES
                if value != old_j
            ]

            for value_i in possible_i:
                for value_j in possible_j:
                    yield [
                        (i, value_i),
                        (j, value_j),
                    ]

    else:
        raise ValueError(
            "Only mutation depths 1 and 2 are supported."
        )


def find_transitions_from_sequence(sequence, max_depth=2):
    base_result = classify(sequence)
    source_class = base_result["classification"]

    edges = {}
    checked_by_depth = {
        "1": 0,
        "2": 0,
    }

    for depth in range(1, max_depth + 1):
        for mutations in candidate_mutations(sequence, depth):
            checked_by_depth[str(depth)] += 1

            mutated = mutate_sequence(sequence, mutations)
            mutated_result = classify(mutated)
            target_class = mutated_result["classification"]

            if target_class == source_class:
                continue

            key = (
                source_class,
                target_class,
            )

            if key not in edges:
                edges[key] = {
                    "from_class": source_class,
                    "to_class": target_class,
                    "minimum_mutation_depth": depth,
                    "example_mutations": mutations,
                    "example_sequence": mutated,
                    "example_metrics": mutated_result,
                    "example_count": 1,
                }
            else:
                edges[key]["example_count"] += 1

    return {
        "source_class": source_class,
        "source_metrics": base_result,
        "checked_by_depth": checked_by_depth,
        "edges": list(edges.values()),
    }


def build_graph_for_variant_set(variant_index, variants_by_case):
    case_results = []
    edge_map = {}

    for case_name, variant_sequences in variants_by_case.items():
        sequence = variant_sequences[variant_index]

        transition_result = find_transitions_from_sequence(
            sequence,
            max_depth=2,
        )

        case_results.append({
            "case_name": case_name,
            "variant_index": variant_index,
            "source_class": transition_result["source_class"],
            "sequence_length": len(sequence),
            "raw_action_sequence": sequence,
            "source_metrics": transition_result["source_metrics"],
            "checked_by_depth": transition_result["checked_by_depth"],
            "edge_count": len(transition_result["edges"]),
            "edges": transition_result["edges"],
        })

        for edge in transition_result["edges"]:
            key = (
                edge["from_class"],
                edge["to_class"],
            )

            if key not in edge_map:
                edge_map[key] = {
                    "from_class": edge["from_class"],
                    "to_class": edge["to_class"],
                    "minimum_mutation_depth": (
                        edge["minimum_mutation_depth"]
                    ),
                    "example_count": edge["example_count"],
                    "source_case_names": [case_name],
                }
            else:
                edge_map[key]["example_count"] += (
                    edge["example_count"]
                )

                if (
                    edge["minimum_mutation_depth"]
                    < edge_map[key]["minimum_mutation_depth"]
                ):
                    edge_map[key]["minimum_mutation_depth"] = (
                        edge["minimum_mutation_depth"]
                    )

                if case_name not in edge_map[key]["source_case_names"]:
                    edge_map[key]["source_case_names"].append(case_name)

    edges = list(edge_map.values())

    return {
        "variant_index": variant_index,
        "case_results": case_results,
        "edges": edges,
    }


def build_adjacency(edges):
    adjacency = {
        class_name: {}
        for class_name in SUPPORTED_CLASSES
    }

    for edge in edges:
        adjacency[edge["from_class"]][edge["to_class"]] = {
            "minimum_mutation_depth": edge["minimum_mutation_depth"],
            "example_count": edge["example_count"],
        }

    return adjacency


def strongly_connected_components(adjacency):
    nodes = list(adjacency.keys())
    graph = {
        node: set(adjacency[node].keys())
        for node in nodes
    }

    visited = set()
    order = []

    def dfs(node):
        visited.add(node)

        for neighbor in graph[node]:
            if neighbor not in visited:
                dfs(neighbor)

        order.append(node)

    for node in nodes:
        if node not in visited:
            dfs(node)

    reverse_graph = {
        node: set()
        for node in nodes
    }

    for source, targets in graph.items():
        for target in targets:
            reverse_graph[target].add(source)

    visited.clear()
    components = []

    def reverse_dfs(node, component):
        visited.add(node)
        component.append(node)

        for neighbor in reverse_graph[node]:
            if neighbor not in visited:
                reverse_dfs(neighbor, component)

    for node in reversed(order):
        if node not in visited:
            component = []
            reverse_dfs(node, component)
            components.append(sorted(component))

    return components


def node_metrics(edges):
    metrics = {
        class_name: {
            "outgoing_count": 0,
            "incoming_count": 0,
            "min_outgoing_depth": None,
            "mean_outgoing_depth": None,
        }
        for class_name in SUPPORTED_CLASSES
    }

    outgoing_depths = {
        class_name: []
        for class_name in SUPPORTED_CLASSES
    }

    for edge in edges:
        source = edge["from_class"]
        target = edge["to_class"]
        depth = edge["minimum_mutation_depth"]

        metrics[source]["outgoing_count"] += 1
        metrics[target]["incoming_count"] += 1

        outgoing_depths[source].append(depth)

    for class_name, depths in outgoing_depths.items():
        if depths:
            metrics[class_name]["min_outgoing_depth"] = min(depths)
            metrics[class_name]["mean_outgoing_depth"] = mean(depths)

    return metrics


def edge_key(edge):
    return f"{edge['from_class']}->{edge['to_class']}"


def summarize_graph(graph):
    edges = graph["edges"]
    adjacency = build_adjacency(edges)
    sccs = strongly_connected_components(adjacency)
    metrics = node_metrics(edges)

    edge_depths = [
        edge["minimum_mutation_depth"]
        for edge in edges
    ]

    classes_with_no_outgoing = [
        class_name
        for class_name, values in metrics.items()
        if values["outgoing_count"] == 0
    ]

    classes_with_no_incoming = [
        class_name
        for class_name, values in metrics.items()
        if values["incoming_count"] == 0
    ]

    return {
        "variant_index": graph["variant_index"],
        "edge_count": len(edges),
        "edges": edges,
        "edge_keys": sorted(edge_key(edge) for edge in edges),
        "adjacency": adjacency,
        "node_metrics": metrics,
        "strongly_connected_components": sccs,
        "strongly_connected_component_count": len(sccs),
        "largest_strongly_connected_component_size": (
            max(len(component) for component in sccs)
            if sccs
            else 0
        ),
        "classes_with_no_outgoing_edges": classes_with_no_outgoing,
        "classes_with_no_incoming_edges": classes_with_no_incoming,
        "mean_edge_depth": (
            mean(edge_depths)
            if edge_depths
            else None
        ),
        "min_edge_depth": (
            min(edge_depths)
            if edge_depths
            else None
        ),
        "max_edge_depth": (
            max(edge_depths)
            if edge_depths
            else None
        ),
        "case_results": graph["case_results"],
    }


def summarize_edge_stability(graph_summaries):
    all_edges = sorted({
        key
        for graph in graph_summaries
        for key in graph["edge_keys"]
    })

    edge_stability = {}

    for key in all_edges:
        present_variants = []
        depths = []

        for graph in graph_summaries:
            edge_lookup = {
                edge_key(edge): edge
                for edge in graph["edges"]
            }

            if key in edge_lookup:
                present_variants.append(graph["variant_index"])
                depths.append(
                    edge_lookup[key]["minimum_mutation_depth"]
                )

        edge_stability[key] = {
            "present_variant_count": len(present_variants),
            "present_variants": present_variants,
            "persistence_rate": (
                len(present_variants) / len(graph_summaries)
                if graph_summaries
                else 0.0
            ),
            "minimum_depths": depths,
            "mean_depth": (
                mean(depths)
                if depths
                else None
            ),
            "depth_std": (
                pstdev(depths)
                if len(depths) > 1
                else 0.0
            ),
        }

    return edge_stability


def summarize_component_stability(graph_summaries):
    component_signatures = [
        sorted(
            [
                tuple(component)
                for component in graph[
                    "strongly_connected_components"
                ]
            ]
        )
        for graph in graph_summaries
    ]

    first_signature = (
        component_signatures[0]
        if component_signatures
        else []
    )

    matching_count = sum(
        1
        for signature in component_signatures
        if signature == first_signature
    )

    return {
        "baseline_component_signature": first_signature,
        "matching_component_signature_count": matching_count,
        "component_signature_stability_rate": (
            matching_count / len(component_signatures)
            if component_signatures
            else 0.0
        ),
        "component_signatures": component_signatures,
    }


def summarize_node_metric_stability(graph_summaries):
    node_summary = {}

    for class_name in SUPPORTED_CLASSES:
        outgoing_values = [
            graph["node_metrics"][class_name]["outgoing_count"]
            for graph in graph_summaries
        ]

        incoming_values = [
            graph["node_metrics"][class_name]["incoming_count"]
            for graph in graph_summaries
        ]

        min_depth_values = [
            graph["node_metrics"][class_name]["min_outgoing_depth"]
            for graph in graph_summaries
            if graph["node_metrics"][class_name]["min_outgoing_depth"]
            is not None
        ]

        node_summary[class_name] = {
            "outgoing_counts": outgoing_values,
            "incoming_counts": incoming_values,
            "outgoing_count_mean": mean(outgoing_values),
            "incoming_count_mean": mean(incoming_values),
            "outgoing_count_std": (
                pstdev(outgoing_values)
                if len(outgoing_values) > 1
                else 0.0
            ),
            "incoming_count_std": (
                pstdev(incoming_values)
                if len(incoming_values) > 1
                else 0.0
            ),
            "min_outgoing_depth_values": min_depth_values,
            "min_outgoing_depth_mean": (
                mean(min_depth_values)
                if min_depth_values
                else None
            ),
            "min_outgoing_depth_std": (
                pstdev(min_depth_values)
                if len(min_depth_values) > 1
                else 0.0
            ),
        }

    return node_summary


def main():
    variants_by_case = base_case_variants()

    variant_count = min(
        len(items)
        for items in variants_by_case.values()
    )

    graph_summaries = []

    for variant_index in range(variant_count):
        graph = build_graph_for_variant_set(
            variant_index,
            variants_by_case,
        )

        graph_summaries.append(
            summarize_graph(graph)
        )

    edge_stability = summarize_edge_stability(graph_summaries)
    component_stability = summarize_component_stability(graph_summaries)
    node_metric_stability = summarize_node_metric_stability(
        graph_summaries
    )

    edge_persistence_rates = [
        item["persistence_rate"]
        for item in edge_stability.values()
    ]

    fully_persistent_edges = [
        key
        for key, item in edge_stability.items()
        if item["persistence_rate"] == 1.0
    ]

    partial_edges = [
        key
        for key, item in edge_stability.items()
        if item["persistence_rate"] < 1.0
    ]

    edge_counts = [
        graph["edge_count"]
        for graph in graph_summaries
    ]

    largest_scc_sizes = [
        graph["largest_strongly_connected_component_size"]
        for graph in graph_summaries
    ]

    summary = {
        "variant_count": variant_count,
        "node_count": len(SUPPORTED_CLASSES),
        "confirmation_window": CONFIRMATION_WINDOW,
        "persistence_window": PERSISTENCE_WINDOW,
        "global_persistence_threshold": GLOBAL_PERSISTENCE_THRESHOLD,
        "max_mutation_depth": 2,
        "supported_classes": SUPPORTED_CLASSES,
        "edge_count_values": edge_counts,
        "mean_edge_count": mean(edge_counts),
        "edge_count_std": (
            pstdev(edge_counts)
            if len(edge_counts) > 1
            else 0.0
        ),
        "mean_edge_persistence_rate": (
            mean(edge_persistence_rates)
            if edge_persistence_rates
            else None
        ),
        "fully_persistent_edge_count": len(fully_persistent_edges),
        "partial_edge_count": len(partial_edges),
        "fully_persistent_edges": fully_persistent_edges,
        "partial_edges": partial_edges,
        "component_signature_stability_rate": (
            component_stability[
                "component_signature_stability_rate"
            ]
        ),
        "largest_scc_size_values": largest_scc_sizes,
        "largest_scc_size_std": (
            pstdev(largest_scc_sizes)
            if len(largest_scc_sizes) > 1
            else 0.0
        ),
    }

    status = (
        "PASS"
        if (
            summary["component_signature_stability_rate"] == 1.0
            and summary["fully_persistent_edge_count"] >= 8
            and summary["largest_scc_size_std"] == 0.0
        )
        else "CHECK"
    )

    payload = {
        "experiment": (
            "temporal_collapse_topology_transition_graph_"
            "stability_v0"
        ),
        "version": VERSION,
        "status": status,
        "summary": summary,
        "edge_stability": edge_stability,
        "component_stability": component_stability,
        "node_metric_stability": node_metric_stability,
        "graph_summaries": graph_summaries,
        "reproduction_command": (
            "python examples/"
            "temporal_collapse_topology_transition_graph_"
            "stability_v0.py"
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
        "Temporal Collapse Topology Transition Graph Stability v0"
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
    print("Edge stability")
    print("-" * 80)

    for key, values in edge_stability.items():
        print(
            f"{key:<75} "
            f"present={values['present_variant_count']} "
            f"rate={values['persistence_rate']} "
            f"depths={values['minimum_depths']} "
            f"depth_std={values['depth_std']}"
        )

    print()
    print("Component stability")
    print("-" * 80)

    for key, value in component_stability.items():
        print(f"{key}: {value}")

    print()
    print("Node metric stability")
    print("-" * 80)

    for class_name, values in node_metric_stability.items():
        print(
            f"{class_name:<32} "
            f"out={values['outgoing_counts']} "
            f"in={values['incoming_counts']} "
            f"out_std={values['outgoing_count_std']} "
            f"in_std={values['incoming_count_std']} "
            f"min_depths={values['min_outgoing_depth_values']} "
            f"min_depth_std={values['min_outgoing_depth_std']}"
        )

    print()
    print("=" * 80)
    print("FINAL CHECK")
    print("=" * 80)

    if status == "PASS":
        print(
            "PASS - transition graph structure remained stable "
            "across shifted base trajectory variants."
        )
    else:
        print(
            "CHECK - transition graph structure changed under "
            "shifted base trajectory variants."
        )

    print()
    print("=" * 80)
    print("Result saved to:", RESULTS_PATH)
    print("=" * 80)


if __name__ == "__main__":
    main()