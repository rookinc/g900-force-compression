#!/usr/bin/env python3
import csv
import json
import re
from pathlib import Path

LAB = Path.home() / "dev/cori/aletheos.ai/public_html/labs/g900_observatory"

SRC = LAB / "artifacts/csv/g900_six_nine_corrected_target_union_compare_059_nearest_diff_rows.v1.csv"
rows = list(csv.DictReader(SRC.open()))

def parse_pair(text):
    if text is None:
        return []
    nums = [int(x) for x in re.findall(r"\d+", str(text))]
    return nums

out_rows = []
for i, r in enumerate(rows):
    source_pair = parse_pair(r.get("source_pair", ""))
    pair_key = parse_pair(r.get("pair_key", ""))
    endpoints = parse_pair(r.get("source_endpoints", ""))
    transition = parse_pair(r.get("source_limit_transition", ""))
    gap = parse_pair(r.get("source_side_gap_signature", ""))
    ladder = parse_pair(r.get("broken_ladder", ""))

    candidate_slots = []
    for xs in [source_pair, pair_key, endpoints, transition, gap, ladder]:
        candidate_slots.extend(xs)

    candidate_slots = [x for x in candidate_slots if 0 <= x <= 14]
    unique_slots = sorted(set(candidate_slots))

    out_rows.append({
        "i": i,
        "membership": r.get("membership", ""),
        "pair_key": r.get("pair_key", ""),
        "source_pair": r.get("source_pair", ""),
        "source_root_slot": r.get("source_root_slot", ""),
        "source_limit_transition": r.get("source_limit_transition", ""),
        "source_side_gap_signature": r.get("source_side_gap_signature", ""),
        "broken_ladder": r.get("broken_ladder", ""),
        "inside_moving_endpoint": r.get("inside_moving_endpoint", ""),
        "outside_moving_endpoint": r.get("outside_moving_endpoint", ""),
        "anchor": r.get("anchor", ""),
        "root": r.get("root", ""),
        "parsed_slot_set": " ".join(str(x) for x in unique_slots),
        "parsed_slot_count": len(unique_slots)
    })

membership_counts = {}
slot_sets = {}
for r in out_rows:
    membership_counts[r["membership"]] = membership_counts.get(r["membership"], 0) + 1
    slot_sets[r["parsed_slot_set"]] = slot_sets.get(r["parsed_slot_set"], 0) + 1

candidate_history_possible = any(int(r["parsed_slot_count"]) > 0 for r in out_rows)

out_csv = Path("artifacts/csv/g900_force_compression_six_nine_bridge_inspect_013_rows.v1.csv")
out_json = Path("artifacts/json/g900_force_compression_six_nine_bridge_inspect_013.v1.json")

with out_csv.open("w", newline="") as f:
    fieldnames = [
        "i", "membership", "pair_key", "source_pair", "source_root_slot",
        "source_limit_transition", "source_side_gap_signature", "broken_ladder",
        "inside_moving_endpoint", "outside_moving_endpoint", "anchor", "root",
        "parsed_slot_set", "parsed_slot_count"
    ]
    w = csv.DictWriter(f, fieldnames=fieldnames)
    w.writeheader()
    w.writerows(out_rows)

summary = {
    "schema": "g900.force.compression.six_nine.bridge.inspect",
    "version": "0.1",
    "status": "six_nine_bridge_source_inspected",
    "audit_pass": True,
    "source": str(SRC),
    "row_count": len(rows),
    "membership_counts": membership_counts,
    "distinct_parsed_slot_set_count": len(slot_sets),
    "slot_sets": slot_sets,
    "candidate_history_possible": candidate_history_possible,
    "metric_ready": False,
    "reason_metric_not_ready": "parsed slot sets exist, but this artifact does not yet identify directed source-to-target slot history",
    "boundary": {
        "bridge_inspection_only": True,
        "slot_history_constructed": False,
        "compression_signature_claim": False,
        "compression_shadow_admitted": False,
        "physical_gravity_claim": False,
        "force_renderer_admitted": False,
        "body_mutation": False
    }
}
out_json.write_text(json.dumps(summary, indent=2) + "\n")

print("status six_nine_bridge_source_inspected")
print("audit_pass True")
print("row_count", len(rows))
print("membership_counts", membership_counts)
print("distinct_parsed_slot_set_count", len(slot_sets))
print("candidate_history_possible", candidate_history_possible)
print("metric_ready False")
print("csv", out_csv)
print("json", out_json)
