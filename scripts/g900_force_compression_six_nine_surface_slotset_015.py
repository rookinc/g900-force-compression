#!/usr/bin/env python3
import csv
import json
from pathlib import Path

SRC = Path("artifacts/json/g900_force_compression_six_nine_bridge_inspect_014.v1.json")
data = json.loads(SRC.read_text())

slot_sets = data.get("top_slot_sets", [])

# Treat 6_9 as the obstruction pair and 12 as return/summit-root candidate
# only as labels from source field names. No metric claim.
records = []
for rec in slot_sets:
    slots_text = rec["slot_set"]
    slots = [int(x) for x in slots_text.split()] if slots_text else []
    slot_set = set(slots)

    has_pair_6_9 = 6 in slot_set and 9 in slot_set
    has_slot_12 = 12 in slot_set
    has_gap_11 = 11 in slot_set
    has_source_3 = 3 in slot_set

    if not slots:
        surface_class = "empty_unparsed"
    elif slots == [6, 9]:
        surface_class = "bare_six_nine_pair"
    elif has_pair_6_9 and has_slot_12 and has_source_3 and has_gap_11:
        surface_class = "expanded_surface_with_gap"
    elif has_pair_6_9 and has_slot_12 and has_source_3:
        surface_class = "expanded_surface_without_gap"
    else:
        surface_class = "other"

    records.append({
        "slot_set": slots_text,
        "count": rec["count"],
        "slot_count": len(slots),
        "has_pair_6_9": has_pair_6_9,
        "has_slot_12": has_slot_12,
        "has_gap_11": has_gap_11,
        "has_source_3": has_source_3,
        "surface_class": surface_class
    })

class_counts = {}
for r in records:
    class_counts[r["surface_class"]] = class_counts.get(r["surface_class"], 0) + int(r["count"])

out_csv = Path("artifacts/csv/g900_force_compression_six_nine_surface_slotset_015.v1.csv")
out_json = Path("artifacts/json/g900_force_compression_six_nine_surface_slotset_015.v1.json")

with out_csv.open("w", newline="") as f:
    fieldnames = [
        "slot_set", "count", "slot_count", "has_pair_6_9",
        "has_slot_12", "has_gap_11", "has_source_3", "surface_class"
    ]
    w = csv.DictWriter(f, fieldnames=fieldnames)
    w.writeheader()
    w.writerows(records)

summary = {
    "schema": "g900.force.compression.six_nine.surface_slotset",
    "version": "0.1",
    "status": "six_nine_surface_slotset_classified",
    "audit_pass": True,
    "source_artifact": str(SRC),
    "slotset_class_count": len(records),
    "class_counts": class_counts,
    "dominant_class": max(class_counts, key=class_counts.get) if class_counts else None,
    "metric_ready": False,
    "interpretation": {
        "six_nine_surface_shape_present": True,
        "directed_transport_history_present": False,
        "surface_rowset_not_transport_history": True
    },
    "boundary": {
        "surface_slotset_classification_only": True,
        "slot_history_constructed": False,
        "compression_signature_claim": False,
        "compression_shadow_admitted": False,
        "physical_gravity_claim": False,
        "force_renderer_admitted": False,
        "body_mutation": False
    }
}

out_json.write_text(json.dumps(summary, indent=2) + "\n")

print("status six_nine_surface_slotset_classified")
print("audit_pass True")
print("slotset_class_count", len(records))
print("class_counts", class_counts)
print("dominant_class", summary["dominant_class"])
print("metric_ready False")
print("csv", out_csv)
print("json", out_json)
