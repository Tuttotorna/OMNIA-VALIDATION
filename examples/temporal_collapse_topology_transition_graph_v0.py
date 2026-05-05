import itertools
import json
from pathlib import Path
from statistics import mean

VERSION = "0.1.0"

RESULTS_PATH = Path(
    "results/temporal_collapse_topology_transition_graph_v0.json"
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


def base_cases():
    return {
        "clean_pass": {
            "sequence": make_sequence(12, []),
        },
        "spike_filtered": {
            "sequence": make_sequence(12, [(5, 1)]),
        },
        "oscillating_nonpersistent": {
            "sequence": make_sequence(
                14,
                [
                    (3, 1),
                    (6, 1),
                    (9, 1),
                ],
            ),
        },
        "fragmented_local_collapse": {
            "sequence": make_sequence(
                18,
                [
                    (3, 2),
                    (7, 2),
                    (11, 2),
                ],
            ),
        },
        "global_persistent_collapse": {
            "sequence": make_sequence(
                18,
                [
                    (6, 8),
                ],
            ),
        },
        "recovery_relapse_collapse": {
            "sequence": make_sequence(
                20,
                [
                    (3, 2),
                    (10, 6),
                ],
            ),
        },
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

            edge_key = (source_class, target_class)

            if edge_key not in edges:
                edges[edge_key] = {
                    "from_class": source_class,
                    "to_class": target_class,
                    "minimum_mutation_depth": depth,
                    "example_mutations": mutations,
                    "example_sequence": mutated,
                    "example_metrics": mutated_result,
                    "example_count": 1,
                }

            else:
                edges[edge_key]["example_count"] += 1

    return {
        "source_class": source_class,
        "source_metrics": base_result,
        "checked_by_depth": checked_by_depth,
        "edges": list(edges.values()),
    }


def build_transition_graph():
    cases = base_cases()

    case_results = []
    edge_map = {}

    for case_name, case_data in cases.items():
        transition_result = find_transitions_from_sequence(
            case_data["sequence"],
            max_depth=2,
        )

        source_class = transition_result["source_class"]

        case_results.append({
            "case_name": case_name,
            "source_class": source_class,
            "sequence_length": len(case_data["sequence"]),
            "raw_action_sequence": case_data["sequence"],
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
                    "example_mutations": edge["example_mutations"],
                    "example_sequence": edge["example_sequence"],
                    "example_metrics": edge["example_metrics"],
                    "example_count": edge["example_count"],
                    "source_case_names": [case_name],
                }

            else:
                edge_map[key]["example_count"] += (
                    edge["example_count"]
                )

                if case_name not in edge_map[key]["source_case_names"]:
                    edge_map[key]["source_case_names"].append(case_name)

                if (
                    edge["minimum_mutation_depth"]
                    < edge_map[key]["minimum_mutation_depth"]
                ):
                    edge_map[key]["minimum_mutation_depth"] = (
                        edge["minimum_mutation_depth"]
                    )
                    edge_map[key]["example_mutations"] = (
                        edge["example_mutations"]
                    )
                    edge_map[key]["example_sequence"] = (
                        edge["example_sequence"]
                    )
                    edge_map[key]["example_metrics"] = (
                        edge["example_metrics"]
                    )

    edges = list(edge_map.values())

    return case_results, edges


def build_adjacency(edges):
    adjacency = {
        class_name: {}
        for class_name in SUPPORTED_CLASSES
    }

    for edge in edges:
        source = edge["from_class"]
        target = edge["to_class"]

        adjacency[source][target] = {
            "minimum_mutation_depth": edge["minimum_mutation_depth"],
            "example_count": edge["example_count"],
        }

    return adjacency


def compute_node_metrics(edges):
    metrics = {
        class_name: {
            "outgoing_count": 0,
            "incoming_count": 0,
            "outgoing_targets": [],
            "incoming_sources": [],
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
        metrics[source]["outgoing_targets"].append(target)

        metrics[target]["incoming_count"] += 1
        metrics[target]["incoming_sources"].append(source)

        outgoing_depths[source].append(depth)

    for class_name, depths in outgoing_depths.items():
        if depths:
            metrics[class_name]["min_outgoing_depth"] = min(depths)
            metrics[class_name]["mean_outgoing_depth"] = mean(depths)

    return metrics


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


def main():
    case_results, edges = build_transition_graph()

    adjacency = build_adjacency(edges)
    node_metrics = compute_node_metrics(edges)
    sccs = strongly_connected_components(adjacency)

    edge_depths = [
        edge["minimum_mutation_depth"]
        for edge in edges
    ]

    outgoing_counts = [
        values["outgoing_count"]
        for values in node_metrics.values()
    ]

    incoming_counts = [
        values["incoming_count"]
        for values in node_metrics.values()
    ]

    strongly_connected_component_count = len(sccs)

    largest_scc_size = (
        max(len(component) for component in sccs)
        if sccs
        else 0
    )

    classes_with_no_outgoing = [
        class_name
        for class_name, values in node_metrics.items()
        if values["outgoing_count"] == 0
    ]

    classes_with_no_incoming = [
        class_name
        for class_name, values in node_metrics.items()
        if values["incoming_count"] == 0
    ]

    summary = {
        "node_count": len(SUPPORTED_CLASSES),
        "edge_count": len(edges),
        "confirmation_window": CONFIRMATION_WINDOW,
        "persistence_window": PERSISTENCE_WINDOW,
        "global_persistence_threshold": GLOBAL_PERSISTENCE_THRESHOLD,
        "max_mutation_depth": 2,
        "supported_classes": SUPPORTED_CLASSES,
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
        "mean_outgoing_count": (
            mean(outgoing_counts)
            if outgoing_counts
            else None
        ),
        "mean_incoming_count": (
            mean(incoming_counts)
            if incoming_counts
            else None
        ),
        "strongly_connected_component_count": (
            strongly_connected_component_count
        ),
        "largest_strongly_connected_component_size": (
            largest_scc_size
        ),
        "classes_with_no_outgoing_edges": classes_with_no_outgoing,
        "classes_with_no_incoming_edges": classes_with_no_incoming,
    }

    status = (
        "PASS"
        if (
            edges
            and not classes_with_no_outgoing
            and largest_scc_size >= 3
        )
        else "CHECK"
    )

    payload = {
        "experiment": (
            "temporal_collapse_topology_transition_graph_v0"
        ),
        "version": VERSION,
        "status": status,
        "summary": summary,
        "adjacency": adjacency,
        "node_metrics": node_metrics,
        "strongly_connected_components": sccs,
        "edges": edges,
        "case_results": case_results,
        "reproduction_command": (
            "python examples/"
            "temporal_collapse_topology_transition_graph_v0.py"
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
        "Temporal Collapse Topology Transition Graph v0"
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
    print("Node metrics")
    print("-" * 80)

    for class_name, values in node_metrics.items():
        print(
            f"{class_name:<32} "
            f"out={values['outgoing_count']} "
            f"in={values['incoming_count']} "
            f"min_out_depth={values['min_outgoing_depth']} "
            f"mean_out_depth={values['mean_outgoing_depth']}"
        )

    print()
    print("Edges")
    print("-" * 80)

    for edge in edges:
        print(
            f"{edge['from_class']:<32} "
            f"-> {edge['to_class']:<32} "
            f"depth={edge['minimum_mutation_depth']} "
            f"examples={edge['example_count']} "
            f"sources={edge['source_case_names']}"
        )

    print()
    print("Strongly connected components")
    print("-" * 80)

    for component in sccs:
        print(component)

    print()
    print("=" * 80)
    print("FINAL CHECK")
    print("=" * 80)

    if status == "PASS":
        print(
            "PASS - temporal topology transition graph "
            "exposed a connected mutation phase space."
        )
    else:
        print(
            "CHECK - temporal topology transition graph "
            "did not expose enough connected transition structure."
        )

    print()
    print("=" * 80)
    print("Result saved to:", RESULTS_PATH)
    print("=" * 80)


if __name__ == "__main__":
    main()