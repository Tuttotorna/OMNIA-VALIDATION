import itertools
import json
from collections import defaultdict, deque
from pathlib import Path
from statistics import mean, pstdev

VERSION = "0.1.0"

RESULTS_PATH = Path(
    "results/temporal_collapse_topology_bridge_stability_v0.json"
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

NOISE_COMPONENT = [
    "CLEAN_PASS",
    "SPIKE_FILTERED",
    "OSCILLATING_NONPERSISTENT",
]

COLLAPSE_COMPONENT = [
    "FRAGMENTED_LOCAL_COLLAPSE",
    "GLOBAL_PERSISTENT_COLLAPSE",
    "RECOVERY_RELAPSE_COLLAPSE",
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


def transition_edges_from_sequence(sequence, max_depth=2):
    source = classify(sequence)["classification"]

    edges = {}

    for depth in range(1, max_depth + 1):
        for mutations in candidate_mutations(sequence, depth):
            mutated = mutate_sequence(sequence, mutations)
            target = classify(mutated)["classification"]

            if target == source:
                continue

            key = (source, target)

            if key not in edges:
                edges[key] = {
                    "from_class": source,
                    "to_class": target,
                    "minimum_mutation_depth": depth,
                    "example_count": 1,
                }
            else:
                edges[key]["example_count"] += 1

    return list(edges.values())


def build_transition_graph_for_variant(variant_index, variants_by_case):
    edge_map = {}

    for case_name, sequences in variants_by_case.items():
        sequence = sequences[variant_index]

        for edge in transition_edges_from_sequence(
            sequence,
            max_depth=2,
        ):
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
                edge_map[key]["example_count"] += edge["example_count"]

                if (
                    edge["minimum_mutation_depth"]
                    < edge_map[key]["minimum_mutation_depth"]
                ):
                    edge_map[key]["minimum_mutation_depth"] = (
                        edge["minimum_mutation_depth"]
                    )

                if case_name not in edge_map[key]["source_case_names"]:
                    edge_map[key]["source_case_names"].append(case_name)

    return list(edge_map.values())


def build_graph(edges):
    graph = {
        class_name: set()
        for class_name in SUPPORTED_CLASSES
    }

    reverse = {
        class_name: set()
        for class_name in SUPPORTED_CLASSES
    }

    for edge in edges:
        source = edge["from_class"]
        target = edge["to_class"]

        graph[source].add(target)
        reverse[target].add(source)

    return graph, reverse


def shortest_paths_from(source, graph):
    distances = {
        class_name: None
        for class_name in SUPPORTED_CLASSES
    }

    distances[source] = 0

    queue = deque([source])

    while queue:
        current = queue.popleft()

        for neighbor in graph[current]:
            if distances[neighbor] is None:
                distances[neighbor] = distances[current] + 1
                queue.append(neighbor)

    return distances


def reachability_matrix(graph):
    return {
        source: shortest_paths_from(source, graph)
        for source in SUPPORTED_CLASSES
    }


def strongly_connected_components(graph):
    nodes = list(graph.keys())

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
                reverse_dfs(node, component)

    for node in reversed(order):
        if node not in visited:
            component = []
            reverse_dfs(node, component)
            components.append(sorted(component))

    return components


def component_for_class(class_name):
    if class_name in NOISE_COMPONENT:
        return "NOISE_COMPONENT"

    if class_name in COLLAPSE_COMPONENT:
        return "COLLAPSE_COMPONENT"

    return "UNKNOWN_COMPONENT"


def compute_bridge_metrics(edges):
    graph, reverse = build_graph(edges)
    reachability = reachability_matrix(graph)
    sccs = strongly_connected_components(graph)

    incoming_reach = defaultdict(int)
    outgoing_reach = defaultdict(int)

    for source, distances in reachability.items():
        for target, distance in distances.items():
            if distance is not None and source != target:
                outgoing_reach[source] += 1
                incoming_reach[target] += 1

    node_metrics = {}

    for class_name in SUPPORTED_CLASSES:
        direct_outgoing = graph[class_name]
        direct_incoming = reverse[class_name]

        cross_component_outgoing = [
            target
            for target in direct_outgoing
            if component_for_class(target)
            != component_for_class(class_name)
        ]

        cross_component_incoming = [
            source
            for source in direct_incoming
            if component_for_class(source)
            != component_for_class(class_name)
        ]

        outgoing_depths = [
            edge["minimum_mutation_depth"]
            for edge in edges
            if edge["from_class"] == class_name
        ]

        cross_depths = [
            edge["minimum_mutation_depth"]
            for edge in edges
            if (
                edge["from_class"] == class_name
                and component_for_class(edge["to_class"])
                != component_for_class(class_name)
            )
        ]

        bridge_score = (
            len(cross_component_outgoing) * 3
            + len(cross_component_incoming) * 2
            + len(direct_incoming)
            + len(direct_outgoing)
        )

        component_crossing_score = (
            len(cross_component_outgoing)
            + len(cross_component_incoming)
        )

        node_metrics[class_name] = {
            "component": component_for_class(class_name),
            "direct_incoming_count": len(direct_incoming),
            "direct_outgoing_count": len(direct_outgoing),
            "reachable_incoming_count": incoming_reach[class_name],
            "reachable_outgoing_count": outgoing_reach[class_name],
            "cross_component_outgoing_count": len(
                cross_component_outgoing
            ),
            "cross_component_incoming_count": len(
                cross_component_incoming
            ),
            "cross_component_outgoing_targets": sorted(
                cross_component_outgoing
            ),
            "cross_component_incoming_sources": sorted(
                cross_component_incoming
            ),
            "component_crossing_score": component_crossing_score,
            "bridge_score": bridge_score,
            "minimum_outgoing_depth": (
                min(outgoing_depths)
                if outgoing_depths
                else None
            ),
            "minimum_cross_component_depth": (
                min(cross_depths)
                if cross_depths
                else None
            ),
        }

    ranked_bridge_candidates = sorted(
        SUPPORTED_CLASSES,
        key=lambda item: (
            node_metrics[item]["bridge_score"],
            node_metrics[item]["component_crossing_score"],
            node_metrics[item]["reachable_outgoing_count"],
            -(
                node_metrics[item]["minimum_cross_component_depth"]
                if node_metrics[item]["minimum_cross_component_depth"]
                is not None
                else 99
            ),
        ),
        reverse=True,
    )

    top_score = (
        node_metrics[ranked_bridge_candidates[0]]["bridge_score"]
        if ranked_bridge_candidates
        else None
    )

    tied_top_bridge_candidates = [
        class_name
        for class_name in ranked_bridge_candidates
        if node_metrics[class_name]["bridge_score"] == top_score
    ]

    component_results = []

    for component in sccs:
        external_incoming = set()
        external_outgoing = set()

        for node in component:
            for source in reverse[node]:
                if source not in component:
                    external_incoming.add(source)

            for target in graph[node]:
                if target not in component:
                    external_outgoing.add(target)

        component_results.append({
            "nodes": component,
            "size": len(component),
            "external_incoming_count": len(external_incoming),
            "external_outgoing_count": len(external_outgoing),
            "external_incoming_nodes": sorted(external_incoming),
            "external_outgoing_nodes": sorted(external_outgoing),
        })

    return {
        "graph": {
            key: sorted(value)
            for key, value in graph.items()
        },
        "reverse_graph": {
            key: sorted(value)
            for key, value in reverse.items()
        },
        "strongly_connected_components": sccs,
        "component_results": component_results,
        "node_metrics": node_metrics,
        "ranked_bridge_candidates": ranked_bridge_candidates,
        "top_bridge_score": top_score,
        "tied_top_bridge_candidates": tied_top_bridge_candidates,
    }


def summarize_variant(variant_index, edges):
    metrics = compute_bridge_metrics(edges)

    return {
        "variant_index": variant_index,
        "edge_count": len(edges),
        "edges": edges,
        "ranked_bridge_candidates": (
            metrics["ranked_bridge_candidates"]
        ),
        "top_bridge_score": metrics["top_bridge_score"],
        "tied_top_bridge_candidates": (
            metrics["tied_top_bridge_candidates"]
        ),
        "node_metrics": metrics["node_metrics"],
        "component_results": metrics["component_results"],
        "strongly_connected_components": (
            metrics["strongly_connected_components"]
        ),
    }


def summarize_stability(variant_results):
    top_bridge_sets = [
        tuple(item["tied_top_bridge_candidates"])
        for item in variant_results
    ]

    ranked_first_values = [
        item["ranked_bridge_candidates"][0]
        for item in variant_results
    ]

    candidate_frequency = defaultdict(int)

    for item in variant_results:
        for candidate in item["tied_top_bridge_candidates"]:
            candidate_frequency[candidate] += 1

    node_metric_stability = {}

    for class_name in SUPPORTED_CLASSES:
        bridge_scores = [
            item["node_metrics"][class_name]["bridge_score"]
            for item in variant_results
        ]

        crossing_scores = [
            item["node_metrics"][class_name][
                "component_crossing_score"
            ]
            for item in variant_results
        ]

        cross_out_counts = [
            item["node_metrics"][class_name][
                "cross_component_outgoing_count"
            ]
            for item in variant_results
        ]

        cross_in_counts = [
            item["node_metrics"][class_name][
                "cross_component_incoming_count"
            ]
            for item in variant_results
        ]

        node_metric_stability[class_name] = {
            "bridge_scores": bridge_scores,
            "component_crossing_scores": crossing_scores,
            "cross_component_outgoing_counts": cross_out_counts,
            "cross_component_incoming_counts": cross_in_counts,
            "bridge_score_mean": mean(bridge_scores),
            "component_crossing_score_mean": mean(
                crossing_scores
            ),
            "bridge_score_std": (
                pstdev(bridge_scores)
                if len(bridge_scores) > 1
                else 0.0
            ),
            "component_crossing_score_std": (
                pstdev(crossing_scores)
                if len(crossing_scores) > 1
                else 0.0
            ),
        }

    stable_top_bridge_set = (
        len(set(top_bridge_sets)) == 1
    )

    stable_ranked_first = (
        len(set(ranked_first_values)) == 1
    )

    return {
        "top_bridge_sets": [
            list(item)
            for item in top_bridge_sets
        ],
        "ranked_first_values": ranked_first_values,
        "stable_top_bridge_set": stable_top_bridge_set,
        "stable_ranked_first": stable_ranked_first,
        "candidate_frequency": dict(candidate_frequency),
        "node_metric_stability": node_metric_stability,
    }


def main():
    variants_by_case = base_case_variants()

    variant_count = min(
        len(items)
        for items in variants_by_case.values()
    )

    variant_results = []

    for variant_index in range(variant_count):
        edges = build_transition_graph_for_variant(
            variant_index,
            variants_by_case,
        )

        variant_results.append(
            summarize_variant(
                variant_index,
                edges,
            )
        )

    stability = summarize_stability(variant_results)

    edge_counts = [
        item["edge_count"]
        for item in variant_results
    ]

    bridge_score_leaders = stability["ranked_first_values"]

    bridge_equivalence_candidates = sorted(
        [
            candidate
            for candidate, count in stability[
                "candidate_frequency"
            ].items()
            if count > 0
        ]
    )

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
        "ranked_first_bridge_values": bridge_score_leaders,
        "stable_ranked_first_bridge": (
            stability["stable_ranked_first"]
        ),
        "stable_top_bridge_set": (
            stability["stable_top_bridge_set"]
        ),
        "bridge_equivalence_candidates": (
            bridge_equivalence_candidates
        ),
        "candidate_frequency": stability["candidate_frequency"],
    }

    status = (
        "PASS"
        if (
            "OSCILLATING_NONPERSISTENT"
            in bridge_equivalence_candidates
            and "SPIKE_FILTERED"
            in bridge_equivalence_candidates
            and not summary["stable_ranked_first_bridge"]
        )
        else "CHECK"
    )

    payload = {
        "experiment": (
            "temporal_collapse_topology_bridge_stability_v0"
        ),
        "version": VERSION,
        "status": status,
        "summary": summary,
        "stability": stability,
        "variant_results": variant_results,
        "interpretation": (
            "PASS means bridge identity is not singular: "
            "multiple topology classes can act as legitimate "
            "bridge candidates under shifted variants."
        ),
        "reproduction_command": (
            "python examples/"
            "temporal_collapse_topology_bridge_stability_v0.py"
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
        "Temporal Collapse Topology Bridge Stability v0"
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
    print("Bridge metric stability")
    print("-" * 80)

    for class_name, values in stability[
        "node_metric_stability"
    ].items():
        print(
            f"{class_name:<32} "
            f"bridge_scores={values['bridge_scores']} "
            f"crossing_scores={values['component_crossing_scores']} "
            f"bridge_std={values['bridge_score_std']} "
            f"crossing_std={values['component_crossing_score_std']}"
        )

    print()
    print("Variant bridge summaries")
    print("-" * 80)

    for item in variant_results:
        print(
            f"variant={item['variant_index']} "
            f"edge_count={item['edge_count']} "
            f"top_bridge_score={item['top_bridge_score']} "
            f"ranked_first={item['ranked_bridge_candidates'][0]} "
            f"tied_top={item['tied_top_bridge_candidates']}"
        )

    print()
    print("Component results")
    print("-" * 80)

    for item in variant_results:
        print("variant_index:", item["variant_index"])

        for component in item["component_results"]:
            print(component)

    print()
    print("=" * 80)
    print("FINAL CHECK")
    print("=" * 80)

    if status == "PASS":
        print(
            "PASS - bridge role is not singular; "
            "multiple topology classes can act as bridge candidates "
            "under shifted variants."
        )
    else:
        print(
            "CHECK - bridge role did not expose the expected "
            "multi-candidate structure."
        )

    print()
    print("=" * 80)
    print("Result saved to:", RESULTS_PATH)
    print("=" * 80)


if __name__ == "__main__":
    main()