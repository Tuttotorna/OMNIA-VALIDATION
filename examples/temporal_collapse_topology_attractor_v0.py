import itertools
import json
from collections import defaultdict, deque
from pathlib import Path
from statistics import mean

VERSION = "0.1.0"

RESULTS_PATH = Path(
    "results/temporal_collapse_topology_attractor_v0.json"
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


def base_sequences():
    return {
        "clean_pass": make_sequence(12, []),
        "spike_filtered": make_sequence(12, [(5, 1)]),
        "oscillating_nonpersistent": make_sequence(
            14,
            [
                (3, 1),
                (6, 1),
                (9, 1),
            ],
        ),
        "fragmented_local_collapse": make_sequence(
            18,
            [
                (3, 2),
                (7, 2),
                (11, 2),
            ],
        ),
        "global_persistent_collapse": make_sequence(
            18,
            [
                (6, 8),
            ],
        ),
        "recovery_relapse_collapse": make_sequence(
            20,
            [
                (3, 2),
                (10, 6),
            ],
        ),
    }


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
                for value_j in itertools.product(
                    possible_j,
                    repeat=1,
                ):
                    yield [
                        (i, value_i),
                        (j, value_j[0]),
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
                    "example_mutations": mutations,
                    "example_count": 1,
                }
            else:
                edges[key]["example_count"] += 1

    return list(edges.values())


def build_transition_graph():
    edge_map = {}

    for case_name, sequence in base_sequences().items():
        edges = transition_edges_from_sequence(
            sequence,
            max_depth=2,
        )

        for edge in edges:
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


def build_adjacency(edges):
    adjacency = {
        class_name: []
        for class_name in SUPPORTED_CLASSES
    }

    for edge in edges:
        adjacency[edge["from_class"]].append({
            "to_class": edge["to_class"],
            "depth": edge["minimum_mutation_depth"],
            "example_count": edge["example_count"],
        })

    return adjacency


def build_unweighted_graph(edges):
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
    matrix = {}

    for source in SUPPORTED_CLASSES:
        distances = shortest_paths_from(
            source,
            graph,
        )

        matrix[source] = distances

    return matrix


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

    components = []

    visited.clear()

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


def basin_metrics(edges):
    graph, reverse = build_unweighted_graph(edges)

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
        out_edges = graph[class_name]
        in_edges = reverse[class_name]

        node_metrics[class_name] = {
            "direct_outgoing_count": len(out_edges),
            "direct_incoming_count": len(in_edges),
            "reachable_outgoing_count": outgoing_reach[class_name],
            "reachable_incoming_count": incoming_reach[class_name],
            "is_sink_like": len(out_edges) == 0,
            "is_source_like": len(in_edges) == 0,
            "attractor_score": incoming_reach[class_name] - outgoing_reach[class_name],
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
            node_metrics[item]["direct_outgoing_count"]
            * node_metrics[item]["direct_incoming_count"],
            node_metrics[item]["reachable_outgoing_count"],
        ),
        reverse=True,
    )

    component_results = []

    for component in sccs:
        component_incoming = set()
        component_outgoing = set()

        for node in component:
            for source in reverse[node]:
                if source not in component:
                    component_incoming.add(source)

            for target in graph[node]:
                if target not in component:
                    component_outgoing.add(target)

        component_results.append({
            "nodes": component,
            "size": len(component),
            "external_incoming_count": len(component_incoming),
            "external_outgoing_count": len(component_outgoing),
            "external_incoming_nodes": sorted(component_incoming),
            "external_outgoing_nodes": sorted(component_outgoing),
            "component_attractor_score": (
                len(component_incoming) - len(component_outgoing)
            ),
        })

    return {
        "reachability": reachability,
        "strongly_connected_components": sccs,
        "node_metrics": node_metrics,
        "attractor_candidates": attractor_candidates,
        "basin_candidates": basin_candidates,
        "bridge_candidates": bridge_candidates,
        "component_results": component_results,
    }


def main():
    edges = build_transition_graph()
    adjacency = build_adjacency(edges)
    metrics = basin_metrics(edges)

    attractor_scores = [
        item["attractor_score"]
        for item in metrics["node_metrics"].values()
    ]

    basin_scores = [
        item["basin_score"]
        for item in metrics["node_metrics"].values()
    ]

    escape_scores = [
        item["escape_score"]
        for item in metrics["node_metrics"].values()
    ]

    strongest_attractor = (
        metrics["attractor_candidates"][0]
        if metrics["attractor_candidates"]
        else None
    )

    strongest_basin = (
        metrics["basin_candidates"][0]
        if metrics["basin_candidates"]
        else None
    )

    strongest_bridge = (
        metrics["bridge_candidates"][0]
        if metrics["bridge_candidates"]
        else None
    )

    summary = {
        "node_count": len(SUPPORTED_CLASSES),
        "edge_count": len(edges),
        "confirmation_window": CONFIRMATION_WINDOW,
        "persistence_window": PERSISTENCE_WINDOW,
        "global_persistence_threshold": GLOBAL_PERSISTENCE_THRESHOLD,
        "max_mutation_depth": 2,
        "supported_classes": SUPPORTED_CLASSES,
        "strongly_connected_component_count": len(
            metrics["strongly_connected_components"]
        ),
        "largest_scc_size": (
            max(
                len(component)
                for component in metrics[
                    "strongly_connected_components"
                ]
            )
            if metrics["strongly_connected_components"]
            else 0
        ),
        "strongest_attractor_candidate": strongest_attractor,
        "strongest_basin_candidate": strongest_basin,
        "strongest_bridge_candidate": strongest_bridge,
        "mean_attractor_score": mean(attractor_scores),
        "mean_basin_score": mean(basin_scores),
        "mean_escape_score": mean(escape_scores),
    }

    status = (
        "PASS"
        if (
            strongest_attractor is not None
            and strongest_basin is not None
            and strongest_bridge is not None
            and len(metrics["strongly_connected_components"]) >= 2
        )
        else "CHECK"
    )

    payload = {
        "experiment": (
            "temporal_collapse_topology_attractor_v0"
        ),
        "version": VERSION,
        "status": status,
        "summary": summary,
        "adjacency": adjacency,
        "edges": edges,
        "reachability": metrics["reachability"],
        "node_metrics": metrics["node_metrics"],
        "attractor_candidates": (
            metrics["attractor_candidates"]
        ),
        "basin_candidates": metrics["basin_candidates"],
        "bridge_candidates": metrics["bridge_candidates"],
        "component_results": metrics["component_results"],
        "strongly_connected_components": (
            metrics["strongly_connected_components"]
        ),
        "reproduction_command": (
            "python examples/"
            "temporal_collapse_topology_attractor_v0.py"
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
        "Temporal Collapse Topology Attractor v0"
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
    print("Node attractor metrics")
    print("-" * 80)

    for class_name, values in metrics["node_metrics"].items():
        print(
            f"{class_name:<32} "
            f"direct_in={values['direct_incoming_count']} "
            f"direct_out={values['direct_outgoing_count']} "
            f"reach_in={values['reachable_incoming_count']} "
            f"reach_out={values['reachable_outgoing_count']} "
            f"attractor={values['attractor_score']} "
            f"basin={values['basin_score']} "
            f"escape={values['escape_score']}"
        )

    print()
    print("Attractor candidates")
    print("-" * 80)

    for item in metrics["attractor_candidates"]:
        print(item)

    print()
    print("Basin candidates")
    print("-" * 80)

    for item in metrics["basin_candidates"]:
        print(item)

    print()
    print("Bridge candidates")
    print("-" * 80)

    for item in metrics["bridge_candidates"]:
        print(item)

    print()
    print("Component results")
    print("-" * 80)

    for component in metrics["component_results"]:
        print(component)

    print()
    print("=" * 80)
    print("FINAL CHECK")
    print("=" * 80)

    if status == "PASS":
        print(
            "PASS - attractor and basin structure was detected "
            "inside the temporal topology transition graph."
        )
    else:
        print(
            "CHECK - attractor and basin structure was not "
            "sufficiently detected."
        )

    print()
    print("=" * 80)
    print("Result saved to:", RESULTS_PATH)
    print("=" * 80)


if __name__ == "__main__":
    main()