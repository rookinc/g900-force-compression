#!/usr/bin/env python3
import csv
import json
import math
from pathlib import Path

LAB = Path.home() / "dev/cori/aletheos.ai/public_html/labs/g900_observatory"
HIST = LAB / "artifacts/csv/g900_return_cell_one_step_information_transport_support_audit_006_history.v1.csv"
SRC_JSON = LAB / "artifacts/json/g900_return_cell_one_step_information_transport_support_audit_006.v1.json"

rows = list(csv.DictReader(HIST.open()))
src = json.loads(SRC_JSON.read_text())

def slot_dist(a, b, n=15):
    a = int(a)
    b = int(b)
    d = abs(a - b) % n
    return min(d, n - d)

# Conservative receipt-home proxy:
# target slots appearing in the admitted h1 packet.
home_slots = sorted({int(r["to_slot"]) for r in rows if r.get("to_slot", "") != ""})
from_slots = [int(r["from_slot"]) for r in rows if r.get("from_slot", "") != ""]
to_slots = [int(r["to_slot"]) for r in rows if r.get("to_slot", "") != ""]

def min_dist_to_home(slot):
    return min(slot_dist(slot, h) for h in home_slots) if home_slots else None

from_distances = [min_dist_to_home(s) for s in from_slots]
to_distances = [min_dist_to_home(s) for s in to_slots]

def mean(xs):
    return sum(xs) / len(xs) if xs else None

def entropy(values):
    if not values:
        return None
    counts = {}
    for v in values:
        counts[v] = counts.get(v, 0) + 1
    total = len(values)
    return -sum((c / total) * math.log2(c / total) for c in counts.values())

support_before = sorted(set(from_slots))
support_after = sorted(set(to_slots))

metrics = {
    "support_size_before": len(support_before),
    "support_size_after": len(support_after),
    "support_radius_before": max(from_distances) if from_distances else None,
    "support_radius_after": max(to_distances) if to_distances else None,
    "mean_distance_to_receipt_home_before": mean(from_distances),
    "mean_distance_to_receipt_home_after": mean(to_distances),
    "maximum_distance_to_receipt_home_before": max(from_distances) if from_distances else None,
    "maximum_distance_to_receipt_home_after": max(to_distances) if to_distances else None,
    "support_entropy_before": entropy(from_slots),
    "support_entropy_after": entropy(to_slots),
}

before_radius = metrics["support_radius_before"] or 0
after_radius = metrics["support_radius_after"] or 0
metrics["concentration_ratio_before"] = (
    metrics["support_size_before"] / before_radius if before_radius else None
)
metrics["concentration_ratio_after"] = (
    metrics["support_size_after"] / after_radius if after_radius else None
)

checks = {
    "history_exists": HIST.exists(),
    "source_json_exists": SRC_JSON.exists(),
    "row_count_is_positive": len(rows) > 0,
    "receipt_pass_source": bool(src.get("audit_pass", False)),
    "boundary_no_force_claim": src.get("boundary", {}).get("force_claim") is False,
    "boundary_no_physical_claim": src.get("boundary", {}).get("physics_claim") is False,
    "boundary_no_body_mutation": src.get("boundary", {}).get("mutates_body") is False,
    "mean_distance_nonincreasing": (
        metrics["mean_distance_to_receipt_home_after"]
        <= metrics["mean_distance_to_receipt_home_before"]
    ),
    "radius_nonincreasing": (
        metrics["support_radius_after"] <= metrics["support_radius_before"]
    ),
}

compression_signature = (
    checks["mean_distance_nonincreasing"]
    and checks["radius_nonincreasing"]
)

out_rows = []
for i, r in enumerate(rows):
    fs = int(r["from_slot"])
    ts = int(r["to_slot"])
    out_rows.append({
        "row_index": i,
        "state_id": r.get("state_id", ""),
        "segment_role": r.get("segment_role", ""),
        "from_slot": fs,
        "to_slot": ts,
        "from_dist_to_home": min_dist_to_home(fs),
        "to_dist_to_home": min_dist_to_home(ts),
        "distance_delta": min_dist_to_home(ts) - min_dist_to_home(fs),
        "edge_id": r.get("edge_id", ""),
        "selection_score": r.get("selection_score", "")
    })

out_csv = Path("artifacts/csv/g900_force_compression_return_cell_metric_probe_001_rows.v1.csv")
out_json = Path("artifacts/json/g900_force_compression_return_cell_metric_probe_001.v1.json")

with out_csv.open("w", newline="") as f:
    fieldnames = [
        "row_index", "state_id", "segment_role", "from_slot", "to_slot",
        "from_dist_to_home", "to_dist_to_home", "distance_delta",
        "edge_id", "selection_score"
    ]
    w = csv.DictWriter(f, fieldnames=fieldnames)
    w.writeheader()
    w.writerows(out_rows)

summary = {
    "schema": "g900.force.compression.return_cell.metric_probe",
    "version": "0.1",
    "status": "return_cell_metric_probe_recorded",
    "audit_pass": all(checks.values()),
    "compression_signature": compression_signature,
    "row_count": len(rows),
    "receipt_home_proxy": {
        "kind": "target_slots_of_admitted_h1_packet",
        "home_slots": home_slots
    },
    "metrics": metrics,
    "checks": checks,
    "boundary": {
        "metric_probe_only": True,
        "compression_shadow_admitted": False,
        "force_renderer_admitted": False,
        "physical_gravity_claim": False,
        "body_mutation": False
    }
}
out_json.write_text(json.dumps(summary, indent=2) + "\n")

print("status return_cell_metric_probe_recorded")
print("audit_pass", summary["audit_pass"])
print("compression_signature", compression_signature)
print("row_count", len(rows))
print("home_slots", home_slots)
print("mean_before", metrics["mean_distance_to_receipt_home_before"])
print("mean_after", metrics["mean_distance_to_receipt_home_after"])
print("radius_before", metrics["support_radius_before"])
print("radius_after", metrics["support_radius_after"])
print("csv", out_csv)
print("json", out_json)
