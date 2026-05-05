import itertools
import json
from collections import defaultdict, deque
from pathlib import Path
from statistics import mean, pstdev

VERSION = "0.1.0"

RESULTS_PATH = Path(
    "results/temporal_collapse_topology_attractor_stability_v0.json"
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
                reverse_dfs(neighbor, component)

    for node in reversed(order):
        if node not in visited:
            component = []
            reverse_dfs(node, component)
            components.append(sorted(component))

    return components


def attractor_metrics_from_edges(edges):
    graph, reverse = build_graph(edges)

    reachability = reachability_matrix(graph)

    incoming_reach = defaultdict(int)
    outgoing_reach = defaultdict(int)

    for source, distances in reachability.items():
        for target, distance in distances.items():
            if distance is not None and source != target:
                outgoing_reach[source] += 1
                incoming_reach[target] += 1

    node_metrics = {}

    for class_name in SUPPORTED_CLASSES:
        out_edges = graph[class_name]
        in_edges = reverse[class_name]

        node_metrics[class_name] = {
            "direct_incoming_count": len(in_edges),
            "direct_outgoing_count": len(out_edges),
            "reachable_incoming_count": incoming_reach[class_name],
            "reachable_outgoing_count": outgoing_reach[class_name],
            "attractor_score": (
                incoming_reach[class_name]
                - outgoing_reach[class_name]
            ),
            "basin_score": incoming_reach[class_name],
            "escape_score": outgoing_reach[class_name],
        }

    attractor_candidates = sorted(
        SUPPORTED_CLASSES,
        key=lambda item: (
            node_metrics[item]["attractor_score"],
            node_metrics[item]["direct_incoming_count"],
            -node_metrics[item]["direct_outgoing_count"],
        ),
        reverse=True,
    )

    basin_candidates = sorted(
        SUPPORTED_CLASSES,
        key=lambda item: (
            node_metrics[item]["basin_score"],
            node_metrics[item]["direct_incoming_count"],
        ),
        reverse=True,
    )

    bridge_candidates = sorted(
        SUPPORTED_CLASSES,
        key=lambda item: (
            node_metrics[item]["direct_incoming_count"]
            * node_metrics[item]["direct_outgoing_count"],
            node_metrics[item]["reachable_outgoing_count"],
        ),
        reverse=True,
    )

    sccs = strongly_connected_components(graph)

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
            "component_attractor_score": (
                len(external_incoming)
                - len(external_outgoing)
            ),
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
        "reachability": reachability,
        "node_metrics": node_metrics,
        "attractor_candidates": attractor_candidates,
        "basin_candidates": basin_candidates,
        "bridge_candidates": bridge_candidates,
        "strongly_connected_components": sccs,
        "component_results": component_results,
    }


def summarize_variant(variant_index, edges):
    metrics = attractor_metrics_from_edges(edges)

    strongest_attractor = metrics["attractor_candidates"][0]
    strongest_basin = metrics["basin_candidates"][0]
    strongest_bridge = metrics["bridge_candidates"][0]

    attractor_scores = [
        values["attractor_score"]
        for values in metrics["node_metrics"].values()
    ]

    basin_scores = [
        values["basin_score"]
        for values in metrics["node_metrics"].values()
    ]

    escape_scores = [
        values["escape_score"]
        for values in metrics["node_metrics"].values()
    ]

    return {
        "variant_index": variant_index,
        "edge_count": len(edges),
        "edges": edges,
        "strongest_attractor_candidate": strongest_attractor,
        "strongest_basin_candidate": strongest_basin,
        "strongest_bridge_candidate": strongest_bridge,
        "mean_attractor_score": mean(attractor_scores),
        "mean_basin_score": mean(basin_scores),
        "mean_escape_score": mean(escape_scores),
        "node_metrics": metrics["node_metrics"],
        "component_results": metrics["component_results"],
        "strongly_connected_components": (
            metrics["strongly_connected_components"]
        ),
    }


def summarize_stability(variant_results):
    attractor_values = [
        item["strongest_attractor_candidate"]
        for item in variant_results
    ]

    basin_values = [
        item["strongest_basin_candidate"]
        for item in variant_results
    ]

    bridge_values = [
        item["strongest_bridge_candidate"]
        for item in variant_results
    ]

    scc_signatures = [
        sorted(
            tuple(component)
            for component in item["strongly_connected_components"]
        )
        for item in variant_results
    ]

    baseline_scc_signature = scc_signatures[0]

    scc_match_count = sum(
        1
        for signature in scc_signatures
        if signature == baseline_scc_signature
    )

    node_score_stability = {}

    for class_name in SUPPORTED_CLASSES:
        attractor_scores = [
            item["node_metrics"][class_name]["attractor_score"]
            for item in variant_results
        ]

        basin_scores = [
            item["node_metrics"][class_name]["basin_score"]
            for item in variant_results
        ]

        escape_scores = [
            item["node_metrics"][class_name]["escape_score"]
            for item in variant_results
        ]

        direct_incoming_counts = [
            item["node_metrics"][class_name]["direct_incoming_count"]
            for item in variant_results
        ]

        direct_outgoing_counts = [
            item["node_metrics"][class_name]["direct_outgoing_count"]
            for item in variant_results
        ]

        node_score_stability[class_name] = {
            "attractor_scores": attractor_scores,
            "basin_scores": basin_scores,
            "escape_scores": escape_scores,
            "direct_incoming_counts": direct_incoming_counts,
            "direct_outgoing_counts": direct_outgoing_counts,
            "attractor_score_mean": mean(attractor_scores),
            "basin_score_mean": mean(basin_scores),
            "escape_score_mean": mean(escape_scores),
            "attractor_score_std": (
                pstdev(attractor_scores)
                if len(attractor_scores) > 1
                else 0.0
            ),
            "basin_score_std": (
                pstdev(basin_scores)
                if len(basin_scores) > 1
                else 0.0
            ),
            "escape_score_std": (
                pstdev(escape_scores)
                if len(escape_scores) > 1
                else 0.0
            ),
        }

    component_score_stability = []

    for variant in variant_results:
        component_score_stability.append({
            "variant_index": variant["variant_index"],
            "component_results": variant["component_results"],
        })

    return {
        "strongest_attractor_values": attractor_values,
        "strongest_basin_values": basin_values,
        "strongest_bridge_values": bridge_values,
        "strongest_attractor_stable": (
            len(set(attractor_values)) == 1
        ),
        "strongest_basin_stable": (
            len(set(basin_values)) == 1
        ),
        "strongest_bridge_stable": (
            len(set(bridge_values)) == 1
        ),
        "baseline_scc_signature": baseline_scc_signature,
        "scc_signature_match_count": scc_match_count,
        "scc_signature_stability_rate": (
            scc_match_count / len(variant_results)
            if variant_results
            else 0.0
        ),
        "node_score_stability": node_score_stability,
        "component_score_stability": component_score_stability,
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
        "strongest_attractor_values": (
            stability["strongest_attractor_values"]
        ),
        "strongest_basin_values": (
            stability["strongest_basin_values"]
        ),
        "strongest_bridge_values": (
            stability["strongest_bridge_values"]
        ),
        "strongest_attractor_stable": (
            stability["strongest_attractor_stable"]
        ),
        "strongest_basin_stable": (
            stability["strongest_basin_stable"]
        ),
        "strongest_bridge_stable": (
            stability["strongest_bridge_stable"]
        ),
        "scc_signature_stability_rate": (
            stability["scc_signature_stability_rate"]
        ),
    }

    status = (
        "PASS"
        if (
            summary["strongest_attractor_stable"]
            and summary["strongest_basin_stable"]
            and summary["strongest_bridge_stable"]
            and summary["scc_signature_stability_rate"] == 1.0
        )
        else "CHECK"
    )

    payload = {
        "experiment": (
            "temporal_collapse_topology_attractor_stability_v0"
        ),
        "version": VERSION,
        "status": status,
        "summary": summary,
        "stability": stability,
        "variant_results": variant_results,
        "reproduction_command": (
            "python examples/"
            "temporal_collapse_topology_attractor_stability_v0.py"
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
        "Temporal Collapse Topology Attractor Stability v0"
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
    print("Node score stability")
    print("-" * 80)

    for class_name, values in stability[
        "node_score_stability"
    ].items():
        print(
            f"{class_name:<32} "
            f"attractor={values['attractor_scores']} "
            f"basin={values['basin_scores']} "
            f"escape={values['escape_scores']} "
            f"attr_std={values['attractor_score_std']} "
            f"basin_std={values['basin_score_std']} "
            f"escape_std={values['escape_score_std']}"
        )

    print()
    print("Component score stability")
    print("-" * 80)

    for item in stability["component_score_stability"]:
        print("variant_index:", item["variant_index"])
        for component in item["component_results"]:
            print(component)

    print()
    print("=" * 80)
    print("FINAL CHECK")
    print("=" * 80)

    if status == "PASS":
        print(
            "PASS - attractor and basin identities remained "
            "stable across shifted trajectory variants."
        )
    else:
        print(
            "CHECK - attractor and basin identities changed "
            "across shifted trajectory variants."
        )

    print()
    print("=" * 80)
    print("Result saved to:", RESULTS_PATH)
    print("=" * 80)


if __name__ == "__main__":
    main()