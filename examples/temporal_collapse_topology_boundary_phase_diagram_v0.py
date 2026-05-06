import json
from pathlib import Path
from statistics import mean, pstdev

VERSION = "0.1.3"

INPUT_RESULTS_PATH = Path(
    "results/temporal_collapse_topology_dependency_boundary_v0.json"
)

RESULTS_PATH = Path(
    "results/temporal_collapse_topology_boundary_phase_diagram_v0.json"
)

PHASE_ORDER = [
    "STABLE_ZONE",
    "DRIFT_ZONE",
    "CRITICAL_ZONE",
]

PHASE_FROM_CLASS = {
    "STABLE_SUPPORT": "STABLE_ZONE",
    "MODERATE_RANK_DRIFT": "DRIFT_ZONE",
    "CRITICAL_TOP6_LOSS": "CRITICAL_ZONE",
    "CRITICAL_ORDER_INVERSION": "CRITICAL_ZONE",
    "CRITICAL_ABSENCE": "CRITICAL_ZONE",
}


def safe_mean(values):
    return mean(values) if values else None


def safe_std(values):
    return pstdev(values) if len(values) > 1 else 0.0


def load_json(path):
    if not path.exists():
        raise FileNotFoundError(f"Missing input result file: {path}")

    return json.loads(path.read_text(encoding="utf-8"))


def extract_boundary_records(payload):
    """
    Extract the full dependency-boundary scenario list.

    The input JSON can contain several short summary lists:
    - minimum critical boundaries
    - top critical boundaries
    - top moderate boundaries
    - top stable boundaries

    The correct source is the largest scenario-like list.
    Therefore this function never returns the first matching list.
    It scans the whole payload and selects the largest valid candidate.
    """

    candidates = []

    def score_record_list(records):
        if not records:
            return 0

        sample_keys = set()

        for item in records[:50]:
            if isinstance(item, dict):
                sample_keys.update(item.keys())

        scenario_like_keys = {
            "scenario_name",
            "scenario_type",
            "boundary_axis",
            "axis",
            "dependency_axis",
            "dependency_class",
            "boundary_class",
            "impact_score",
            "impact",
            "boundary_distance",
            "distance",
            "expected_dominant_rank",
            "dominant_rank",
            "expected_second_rank",
            "second_rank",
            "status",
            "strict_status",
        }

        return len(sample_keys.intersection(scenario_like_keys))

    def walk(obj, path=None):
        path = path or []

        if isinstance(obj, dict):
            for key, value in obj.items():
                walk(value, path + [key])

        elif isinstance(obj, list):
            if obj and all(isinstance(item, dict) for item in obj):
                score = score_record_list(obj)

                if score >= 4:
                    candidates.append({
                        "path": path,
                        "length": len(obj),
                        "score": score,
                        "records": obj,
                    })

            for index, value in enumerate(obj):
                walk(value, path + [str(index)])

    walk(payload)

    if not candidates:
        return []

    candidates.sort(
        key=lambda item: (
            item["length"],
            item["score"],
        ),
        reverse=True,
    )

    return candidates[0]["records"]


def get_value(record, *keys, default=None):
    for key in keys:
        if key in record:
            return record[key]

    return default


def normalize_boundary_record(record):
    dependency_class = get_value(
        record,
        "dependency_class",
        "boundary_class",
        "class",
        "classification",
    )

    phase_zone = PHASE_FROM_CLASS.get(dependency_class, "UNKNOWN_ZONE")

    boundary_axis = get_value(
        record,
        "boundary_axis",
        "axis",
        "dependency_axis",
    )

    boundary_distance = get_value(
        record,
        "boundary_distance",
        "distance",
        "perturbation_distance",
    )

    impact_score = get_value(
        record,
        "impact_score",
        "impact",
        "boundary_impact",
        default=0.0,
    )

    return {
        "scenario_name": get_value(record, "scenario_name", "name"),
        "scenario_type": get_value(record, "scenario_type", "type"),
        "boundary_axis": boundary_axis,
        "boundary_distance": boundary_distance,
        "status": get_value(record, "status"),
        "strict_status": get_value(record, "strict_status"),
        "dependency_class": dependency_class,
        "phase_zone": phase_zone,
        "impact_score": impact_score,
        "expected_dominant_rank": get_value(
            record,
            "expected_dominant_rank",
            "dominant_rank",
        ),
        "expected_second_rank": get_value(
            record,
            "expected_second_rank",
            "second_rank",
        ),
        "dominant_cluster_id": get_value(
            record,
            "dominant_cluster_id",
            "dominant_cluster",
        ),
        "second_cluster_id": get_value(
            record,
            "second_cluster_id",
            "second_cluster",
        ),
    }


def phase_severity(phase):
    if phase == "STABLE_ZONE":
        return 0

    if phase == "DRIFT_ZONE":
        return 1

    if phase == "CRITICAL_ZONE":
        return 2

    return 99


def summarize_by_phase(records):
    summary = {}

    for phase in PHASE_ORDER + ["UNKNOWN_ZONE"]:
        phase_records = [
            record for record in records
            if record["phase_zone"] == phase
        ]

        if not phase_records:
            continue

        distances = [
            record["boundary_distance"]
            for record in phase_records
            if record["boundary_distance"] is not None
        ]

        impacts = [
            record["impact_score"]
            for record in phase_records
            if record["impact_score"] is not None
        ]

        dominant_ranks = [
            record["expected_dominant_rank"]
            for record in phase_records
            if record["expected_dominant_rank"] is not None
        ]

        second_ranks = [
            record["expected_second_rank"]
            for record in phase_records
            if record["expected_second_rank"] is not None
        ]

        summary[phase] = {
            "phase_zone": phase,
            "record_count": len(phase_records),
            "boundary_axis_values": sorted(
                set(
                    record["boundary_axis"]
                    for record in phase_records
                    if record["boundary_axis"] is not None
                )
            ),
            "scenario_type_values": sorted(
                set(
                    record["scenario_type"]
                    for record in phase_records
                    if record["scenario_type"] is not None
                )
            ),
            "dependency_class_values": sorted(
                set(
                    record["dependency_class"]
                    for record in phase_records
                    if record["dependency_class"] is not None
                )
            ),
            "minimum_boundary_distance": min(distances) if distances else None,
            "maximum_boundary_distance": max(distances) if distances else None,
            "impact_score_mean": safe_mean(impacts),
            "impact_score_std": safe_std(impacts),
            "impact_score_max": max(impacts) if impacts else None,
            "dominant_rank_mean": safe_mean(dominant_ranks),
            "second_rank_mean": safe_mean(second_ranks),
            "scenario_names": [
                record["scenario_name"]
                for record in phase_records
            ],
        }

    return summary


def summarize_axis_phase_matrix(records):
    matrix = {}

    for record in records:
        axis = record["boundary_axis"] or "unknown"
        phase = record["phase_zone"]

        matrix.setdefault(axis, {})
        matrix[axis].setdefault(
            phase,
            {
                "boundary_axis": axis,
                "phase_zone": phase,
                "record_count": 0,
                "dependency_class_values": [],
                "boundary_distances": [],
                "impact_scores": [],
                "scenario_names": [],
            },
        )

        item = matrix[axis][phase]
        item["record_count"] += 1
        item["scenario_names"].append(record["scenario_name"])

        if record["dependency_class"] is not None:
            item["dependency_class_values"].append(record["dependency_class"])

        if record["boundary_distance"] is not None:
            item["boundary_distances"].append(record["boundary_distance"])

        if record["impact_score"] is not None:
            item["impact_scores"].append(record["impact_score"])

    for axis_items in matrix.values():
        for item in axis_items.values():
            item["dependency_class_values"] = sorted(
                set(item["dependency_class_values"])
            )

            item["minimum_boundary_distance"] = (
                min(item["boundary_distances"])
                if item["boundary_distances"]
                else None
            )

            item["maximum_boundary_distance"] = (
                max(item["boundary_distances"])
                if item["boundary_distances"]
                else None
            )

            item["impact_score_mean"] = safe_mean(item["impact_scores"])

            item["impact_score_max"] = (
                max(item["impact_scores"])
                if item["impact_scores"]
                else None
            )

    return matrix


def summarize_distance_phase_map(records):
    distance_map = {}

    for record in records:
        axis = record["boundary_axis"] or "unknown"
        distance = record["boundary_distance"]
        phase = record["phase_zone"]

        if distance is None:
            continue

        distance_key = str(distance)

        distance_map.setdefault(axis, {})
        distance_map[axis].setdefault(
            distance_key,
            {
                "boundary_axis": axis,
                "boundary_distance": distance,
                "record_count": 0,
                "phase_counts": {
                    "STABLE_ZONE": 0,
                    "DRIFT_ZONE": 0,
                    "CRITICAL_ZONE": 0,
                    "UNKNOWN_ZONE": 0,
                },
                "dominant_phase": None,
                "scenario_names": [],
                "impact_scores": [],
            },
        )

        item = distance_map[axis][distance_key]
        item["record_count"] += 1
        item["phase_counts"][phase] = item["phase_counts"].get(phase, 0) + 1
        item["scenario_names"].append(record["scenario_name"])

        if record["impact_score"] is not None:
            item["impact_scores"].append(record["impact_score"])

    for axis_items in distance_map.values():
        for item in axis_items.values():
            ordered = sorted(
                item["phase_counts"].items(),
                key=lambda pair: (
                    pair[1],
                    phase_severity(pair[0]),
                    pair[0],
                ),
                reverse=True,
            )

            item["dominant_phase"] = ordered[0][0] if ordered else None
            item["impact_score_mean"] = safe_mean(item["impact_scores"])

            item["impact_score_max"] = (
                max(item["impact_scores"])
                if item["impact_scores"]
                else None
            )

    return distance_map


def compute_phase_boundaries(records):
    boundaries = {}

    axes = sorted(
        set(
            record["boundary_axis"]
            for record in records
            if record["boundary_axis"] is not None
        )
    )

    for axis in axes:
        axis_records = [
            record for record in records
            if record["boundary_axis"] == axis
        ]

        stable = [
            record for record in axis_records
            if record["phase_zone"] == "STABLE_ZONE"
        ]

        drift = [
            record for record in axis_records
            if record["phase_zone"] == "DRIFT_ZONE"
        ]

        critical = [
            record for record in axis_records
            if record["phase_zone"] == "CRITICAL_ZONE"
        ]

        def min_distance(items):
            values = [
                item["boundary_distance"]
                for item in items
                if item["boundary_distance"] is not None
            ]

            return min(values) if values else None

        sequence = []

        distances = sorted(
            set(
                record["boundary_distance"]
                for record in axis_records
                if record["boundary_distance"] is not None
            )
        )

        for distance in distances:
            distance_records = [
                record for record in axis_records
                if record["boundary_distance"] == distance
            ]

            phase_counts = {
                "STABLE_ZONE": sum(
                    1 for record in distance_records
                    if record["phase_zone"] == "STABLE_ZONE"
                ),
                "DRIFT_ZONE": sum(
                    1 for record in distance_records
                    if record["phase_zone"] == "DRIFT_ZONE"
                ),
                "CRITICAL_ZONE": sum(
                    1 for record in distance_records
                    if record["phase_zone"] == "CRITICAL_ZONE"
                ),
            }

            dominant_phase = sorted(
                phase_counts.items(),
                key=lambda pair: (
                    pair[1],
                    phase_severity(pair[0]),
                    pair[0],
                ),
                reverse=True,
            )[0][0]

            sequence.append({
                "boundary_distance": distance,
                "phase_counts": phase_counts,
                "dominant_phase": dominant_phase,
            })

        boundaries[axis] = {
            "boundary_axis": axis,
            "stable_count": len(stable),
            "drift_count": len(drift),
            "critical_count": len(critical),
            "stable_min_distance": min_distance(stable),
            "drift_min_distance": min_distance(drift),
            "critical_min_distance": min_distance(critical),
            "transition_boundary_detected": (
                len(stable) > 0
                and (len(drift) > 0 or len(critical) > 0)
            ),
            "phase_sequence_by_distance": sequence,
        }

    return boundaries


def select_extremes(records):
    stable = [
        record for record in records
        if record["phase_zone"] == "STABLE_ZONE"
    ]

    drift = [
        record for record in records
        if record["phase_zone"] == "DRIFT_ZONE"
    ]

    critical = [
        record for record in records
        if record["phase_zone"] == "CRITICAL_ZONE"
    ]

    minimum_critical = sorted(
        critical,
        key=lambda record: (
            record["boundary_distance"]
            if record["boundary_distance"] is not None
            else 999999,
            -record["impact_score"],
            record["scenario_name"] or "",
        ),
    )

    maximum_critical = sorted(
        critical,
        key=lambda record: (
            record["impact_score"],
            -(
                record["boundary_distance"]
                if record["boundary_distance"] is not None
                else 0
            ),
            record["scenario_name"] or "",
        ),
        reverse=True,
    )

    minimum_drift = sorted(
        drift,
        key=lambda record: (
            record["boundary_distance"]
            if record["boundary_distance"] is not None
            else 999999,
            -record["impact_score"],
            record["scenario_name"] or "",
        ),
    )

    minimum_stable = sorted(
        stable,
        key=lambda record: (
            record["boundary_distance"]
            if record["boundary_distance"] is not None
            else 999999,
            record["scenario_name"] or "",
        ),
    )

    return {
        "minimum_critical_boundaries": minimum_critical[:12],
        "maximum_impact_critical_boundaries": maximum_critical[:12],
        "minimum_drift_boundaries": minimum_drift[:12],
        "minimum_distance_stable_boundaries": minimum_stable[:12],
    }


def build_ascii_phase_diagram(distance_phase_map):
    lines = []

    for axis in sorted(distance_phase_map):
        lines.append(f"{axis}:")

        for distance_key in sorted(
            distance_phase_map[axis],
            key=lambda value: int(value),
        ):
            item = distance_phase_map[axis][distance_key]
            counts = item["phase_counts"]

            lines.append(
                "  "
                f"d={distance_key} "
                f"stable={counts.get('STABLE_ZONE', 0)} "
                f"drift={counts.get('DRIFT_ZONE', 0)} "
                f"critical={counts.get('CRITICAL_ZONE', 0)} "
                f"dominant={item['dominant_phase']}"
            )

    return "\n".join(lines)


def validate_phase_diagram(phase_summary, phase_boundaries):
    failures = []

    for phase in PHASE_ORDER:
        if phase not in phase_summary:
            failures.append({
                "reason": f"missing_{phase.lower()}",
            })

    for axis, item in phase_boundaries.items():
        if axis in {"family", "threshold"}:
            if item["critical_count"] <= 0:
                failures.append({
                    "reason": "expected_critical_zone_missing",
                    "boundary_axis": axis,
                })

        if axis == "variant":
            if item["critical_count"] != 0:
                failures.append({
                    "reason": "unexpected_variant_critical_zone",
                    "boundary_axis": axis,
                    "critical_count": item["critical_count"],
                })

    return {
        "phase_diagram_validation_holds": len(failures) == 0,
        "failure_count": len(failures),
        "failures": failures,
    }


def main():
    dependency_payload = load_json(INPUT_RESULTS_PATH)

    raw_records = extract_boundary_records(dependency_payload)

    phase_records = [
        normalize_boundary_record(record)
        for record in raw_records
    ]

    phase_summary = summarize_by_phase(phase_records)
    axis_phase_summary = summarize_axis_phase_matrix(phase_records)
    distance_phase_map = summarize_distance_phase_map(phase_records)
    phase_boundaries = compute_phase_boundaries(phase_records)
    boundary_extremes = select_extremes(phase_records)
    ascii_phase_diagram = build_ascii_phase_diagram(distance_phase_map)

    validation = validate_phase_diagram(
        phase_summary,
        phase_boundaries,
    )

    input_detected = dependency_payload.get(
        "summary",
        {},
    ).get("dependency_boundary_detected", False)

    phase_diagram_detected = (
        input_detected
        and len(phase_records) > 0
        and validation["phase_diagram_validation_holds"]
        and "STABLE_ZONE" in phase_summary
        and "DRIFT_ZONE" in phase_summary
        and "CRITICAL_ZONE" in phase_summary
    )

    status = "PASS" if phase_diagram_detected else "CHECK"

    minimum_critical_distances = [
        item["critical_min_distance"]
        for item in phase_boundaries.values()
        if item["critical_min_distance"] is not None
    ]

    minimum_drift_distances = [
        item["drift_min_distance"]
        for item in phase_boundaries.values()
        if item["drift_min_distance"] is not None
    ]

    payload = {
        "experiment": (
            "temporal_collapse_topology_boundary_phase_diagram_v0"
        ),
        "version": VERSION,
        "status": status,
        "summary": {
            "input_result_file": str(INPUT_RESULTS_PATH),
            "boundary_scenario_count": len(phase_records),
            "phase_zone_count": len(phase_summary),
            "stable_zone_count": phase_summary.get(
                "STABLE_ZONE",
                {},
            ).get("record_count", 0),
            "drift_zone_count": phase_summary.get(
                "DRIFT_ZONE",
                {},
            ).get("record_count", 0),
            "critical_zone_count": phase_summary.get(
                "CRITICAL_ZONE",
                {},
            ).get("record_count", 0),
            "family_transition_boundary_detected": (
                phase_boundaries.get(
                    "family",
                    {},
                ).get("transition_boundary_detected", False)
            ),
            "threshold_transition_boundary_detected": (
                phase_boundaries.get(
                    "threshold",
                    {},
                ).get("transition_boundary_detected", False)
            ),
            "variant_transition_boundary_detected": (
                phase_boundaries.get(
                    "variant",
                    {},
                ).get("transition_boundary_detected", False)
            ),
            "minimum_critical_distance": (
                min(minimum_critical_distances)
                if minimum_critical_distances
                else None
            ),
            "minimum_drift_distance": (
                min(minimum_drift_distances)
                if minimum_drift_distances
                else None
            ),
            "phase_diagram_validation_holds": (
                validation["phase_diagram_validation_holds"]
            ),
            "phase_diagram_detected": phase_diagram_detected,
            "method": "boundary_phase_diagram",
        },
        "boundary_phase_diagram_summary": {
            "phase_summary": phase_summary,
            "axis_phase_summary": axis_phase_summary,
            "distance_phase_map": distance_phase_map,
            "phase_boundaries": phase_boundaries,
            "boundary_extremes": boundary_extremes,
            "ascii_phase_diagram": ascii_phase_diagram,
            "phase_diagram_validation": validation,
            "phase_diagram_detected": phase_diagram_detected,
            "phase_rule": (
                "STABLE_SUPPORT -> STABLE_ZONE; "
                "MODERATE_RANK_DRIFT -> DRIFT_ZONE; "
                "CRITICAL_TOP6_LOSS, CRITICAL_ORDER_INVERSION, "
                "and CRITICAL_ABSENCE -> CRITICAL_ZONE."
            ),
        },
        "phase_records": phase_records,
        "interpretation": {
            "main_result": (
                "boundary phase diagram detected"
                if status == "PASS"
                else "boundary phase diagram not fully confirmed"
            ),
            "structural_conclusion": (
                "The dependency-boundary landscape separates into "
                "stable, drift, and critical zones. Family and threshold "
                "axes expose transition boundaries; the variant axis remains "
                "stable under tested perturbations."
            ),
            "important_boundary": (
                "This is a structural phase map of boundary behavior, "
                "not a semantic judgment or decision layer."
            ),
        },
        "final_check": {
            "status": status,
            "message": (
                "boundary phase diagram detected"
                if status == "PASS"
                else "boundary phase diagram was not fully confirmed"
            ),
        },
        "reproduction_command": (
            "python examples/"
            "temporal_collapse_topology_boundary_phase_diagram_v0.py"
        ),
    }

    RESULTS_PATH.parent.mkdir(parents=True, exist_ok=True)
    RESULTS_PATH.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    print("=" * 80)
    print(
        "OMNIA-VALIDATION - "
        "Temporal Collapse Topology Boundary Phase Diagram v0"
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
    print("Phase zones")
    print("-" * 80)

    for phase in PHASE_ORDER:
        item = phase_summary.get(phase)

        if not item:
            continue

        print(
            f"phase={phase:<16} "
            f"records={item['record_count']} "
            f"axes={item['boundary_axis_values']} "
            f"classes={item['dependency_class_values']} "
            f"min_distance={item['minimum_boundary_distance']} "
            f"max_distance={item['maximum_boundary_distance']} "
            f"impact_mean={item['impact_score_mean']} "
            f"impact_max={item['impact_score_max']}"
        )

    print()
    print("Axis / phase matrix")
    print("-" * 80)

    for axis, axis_items in axis_phase_summary.items():
        for phase in PHASE_ORDER:
            item = axis_items.get(phase)

            if not item:
                continue

            print(
                f"axis={axis:<10} "
                f"phase={phase:<16} "
                f"records={item['record_count']} "
                f"min_distance={item['minimum_boundary_distance']} "
                f"max_distance={item['maximum_boundary_distance']} "
                f"impact_mean={item['impact_score_mean']} "
                f"impact_max={item['impact_score_max']}"
            )

    print()
    print("Distance phase map")
    print("-" * 80)

    print(ascii_phase_diagram if ascii_phase_diagram else "(empty)")

    print()
    print("Phase boundaries")
    print("-" * 80)

    for axis, item in phase_boundaries.items():
        print(
            f"axis={axis:<10} "
            f"stable={item['stable_count']} "
            f"drift={item['drift_count']} "
            f"critical={item['critical_count']} "
            f"stable_min={item['stable_min_distance']} "
            f"drift_min={item['drift_min_distance']} "
            f"critical_min={item['critical_min_distance']} "
            f"transition_boundary={item['transition_boundary_detected']}"
        )

    print()
    print("Minimum critical boundaries")
    print("-" * 80)

    for record in boundary_extremes["minimum_critical_boundaries"]:
        print(
            f"scenario={record['scenario_name']:<64} "
            f"axis={record['boundary_axis']:<10} "
            f"distance={record['boundary_distance']} "
            f"class={record['dependency_class']} "
            f"impact={record['impact_score']} "
            f"dom_rank={record['expected_dominant_rank']} "
            f"sec_rank={record['expected_second_rank']}"
        )

    print()
    print("Maximum-impact critical boundaries")
    print("-" * 80)

    for record in boundary_extremes["maximum_impact_critical_boundaries"]:
        print(
            f"scenario={record['scenario_name']:<64} "
            f"axis={record['boundary_axis']:<10} "
            f"distance={record['boundary_distance']} "
            f"class={record['dependency_class']} "
            f"impact={record['impact_score']} "
            f"dom_rank={record['expected_dominant_rank']} "
            f"sec_rank={record['expected_second_rank']}"
        )

    print()
    print("Minimum drift boundaries")
    print("-" * 80)

    for record in boundary_extremes["minimum_drift_boundaries"]:
        print(
            f"scenario={record['scenario_name']:<64} "
            f"axis={record['boundary_axis']:<10} "
            f"distance={record['boundary_distance']} "
            f"class={record['dependency_class']} "
            f"impact={record['impact_score']} "
            f"dom_rank={record['expected_dominant_rank']} "
            f"sec_rank={record['expected_second_rank']}"
        )

    print()
    print("Minimum stable boundaries")
    print("-" * 80)

    for record in boundary_extremes["minimum_distance_stable_boundaries"]:
        print(
            f"scenario={record['scenario_name']:<64} "
            f"axis={record['boundary_axis']:<10} "
            f"distance={record['boundary_distance']} "
            f"class={record['dependency_class']} "
            f"impact={record['impact_score']} "
            f"dom_rank={record['expected_dominant_rank']} "
            f"sec_rank={record['expected_second_rank']}"
        )

    print()
    print("Validation")
    print("-" * 80)

    print(
        "phase_diagram_validation_holds:",
        validation["phase_diagram_validation_holds"],
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
            "PASS - boundary phase diagram detected: dependency boundaries "
            "separate into stable, drift, and critical zones."
        )
    else:
        print(
            "CHECK - boundary phase diagram was not fully confirmed under "
            "the tested dependency-boundary records."
        )

    print()
    print("=" * 80)
    print("Result saved to:", RESULTS_PATH)
    print("=" * 80)


if __name__ == "__main__":
    main()