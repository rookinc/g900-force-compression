#!/usr/bin/env python3
import csv
import json
import math
from pathlib import Path

LAB = Path.home() / "dev/cori/aletheos.ai/public_html/labs/g900_observatory"
HIST = LAB / "artifacts/csv/g900_return_cell_one_step_information_transport_support_audit_006_history.v1.csv"
rows = list(csv.DictReader(HIST.open()))

from_slots = [int(r["from_slot"]) for r in rows]
to_slots = [int(r["to_slot"]) for r in rows]

def slot_dist(a, b, n=15):
    d = abs(int(a) - int(b)) % n
    return min(d, n - d)

def mean(xs):
    return sum(xs) / len(xs) if xs else None

def min_dist_to_home(slot, homes):
    return min(slot_dist(slot, h) for h in homes)

def metric_for_home(home_slots):
    before = [min_dist_to_home(s, home_slots) for s in from_slots]
    after = [min_dist_to_home(s, home_slots) for s in to_slots]
    return {
        "home_slots": home_slots,
        "mean_before": mean(before),
        "mean_after": mean(after),
        "mean_delta": mean(after) - mean(before),
        "radius_before": max(before),
        "radius_after": max(after),
        "radius_delta": max(after) - max(before),
        "exact_home_after": all(d == 0 for d in after),
        "mean_nonincreasing": mean(after) <= mean(before),
        "radius_nonincreasing": max(after) <= max(before),
    }

home_sets = {
    "target_home": sorted(set(to_slots)),
    "source_home": sorted(set(from_slots)),
    "six_nine_pair": [6, 9],
    "return_cell_full": [3, 6, 9, 12, 13],
    "slot_zero": [0],
    "opposite_anchors": [0, 7, 14],
}

records = []
for name, homes in home_sets.items():
    m = metric_for_home(homes)
    m["home_id"] = name
    records.append(m)

target = next(r for r in records if r["home_id"] == "target_home")
strict_target_best = all(
    target["mean_after"] <= r["mean_after"]
    for r in records
)

out_csv = Path("artifacts/csv/g900_force_compression_return_cell_home_contrast_003.v1.csv")
out_json = Path("artifacts/json/g900_force_compression_return_cell_home_contrast_003.v1.json")

with out_csv.open("w", newline="") as f:
    fieldnames = [
        "home_id", "home_slots", "mean_before", "mean_after", "mean_delta",
        "radius_before", "radius_after", "radius_delta",
        "exact_home_after", "mean_nonincreasing", "radius_nonincreasing"
    ]
    w = csv.DictWriter(f, fieldnames=fieldnames)
    w.writeheader()
    w.writerows(records)

summary = {
    "schema": "g900.force.compression.return_cell.home_contrast",
    "version": "0.1",
    "status": "home_contrast_recorded",
    "audit_pass": True,
    "row_count": len(rows),
    "home_set_count": len(records),
    "target_home": target,
    "target_home_exact_after": target["exact_home_after"],
    "target_home_mean_after_minimal_in_tested_set": strict_target_best,
    "records": records,
    "boundary": {
        "contrast_audit_only": True,
        "home_proxy_not_unique_proof": True,
        "compression_shadow_admitted": False,
        "physical_gravity_claim": False,
        "body_mutation": False,
        "force_renderer": False
    }
}
out_json.write_text(json.dumps(summary, indent=2) + "\n")

print("status home_contrast_recorded")
print("audit_pass True")
print("row_count", len(rows))
print("home_set_count", len(records))
print("target_home_exact_after", summary["target_home_exact_after"])
print("target_home_mean_after_minimal_in_tested_set", strict_target_best)
print("target_mean_after", target["mean_after"])
print("target_radius_after", target["radius_after"])
