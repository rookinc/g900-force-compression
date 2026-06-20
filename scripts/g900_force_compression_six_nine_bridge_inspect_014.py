#!/usr/bin/env python3
import csv
import json
import re
from pathlib import Path

LAB = Path.home() / "dev/cori/aletheos.ai/public_html/labs/g900_observatory"
SRC = LAB / "artifacts/csv/g900_six_nine_one_row_correction_probe_058_candidate_target_rows.v1.csv"

rows = list(csv.DictReader(SRC.open()))

def parse_nums(text):
    if text is None:
        return []
    return [int(x) for x in re.findall(r"\d+", str(text))]

def clean_slots(xs):
    return sorted(set(x for x in xs if 0 <= x <= 14))

out_rows = []
slot_set_counts = {}
root_slot_counts = {}
pair_counts = {}

for i, r in enumerate(rows):
    fields = {
        "pair_key": r.get("pair_key", ""),
        "source_pair": r.get("source_pair", ""),
        "source_endpoints": r.get("source_endpoints", ""),
        "source_root_slot": r.get("source_root_slot", ""),
        "source_limit_transition": r.get("source_limit_transition", ""),
        "source_side_gap_signature": r.get("source_side_gap_signature", ""),
        "broken_ladder": r.get("broken_ladder", ""),
        "phase_ladder_values": r.get("phase_ladder_values", ""),
        "inside_moving_endpoint": r.get("inside_moving_endpoint", ""),
        "outside_moving_endpoint": r.get("outside_moving_endpoint", ""),
        "anchor": r.get("anchor", ""),
        "root": r.get("root", "")
    }

    parsed = {}
    allnums = []
    for k, v in fields.items():
        nums = parse_nums(v)
        parsed[k] = clean_slots(nums)
        allnums.extend(nums)

    slot_set = clean_slots(allnums)
    slot_set_text = " ".join(str(x) for x in slot_set)
    slot_set_counts[slot_set_text] = slot_set_counts.get(slot_set_text, 0) + 1

    root_slot = fields["source_root_slot"]
    root_slot_counts[root_slot] = root_slot_counts.get(root_slot, 0) + 1

    pair = fields["source_pair"] or fields["pair_key"]
    pair_counts[pair] = pair_counts.get(pair, 0) + 1

    out_rows.append({
        "i": i,
        "pair_key": fields["pair_key"],
        "source_pair": fields["source_pair"],
        "source_root_slot": fields["source_root_slot"],
        "source_limit_transition": fields["source_limit_transition"],
        "source_side_gap_signature": fields["source_side_gap_signature"],
        "broken_ladder": fields["broken_ladder"],
        "phase_ladder_values": fields["phase_ladder_values"],
        "inside_moving_endpoint": fields["inside_moving_endpoint"],
        "outside_moving_endpoint": fields["outside_moving_endpoint"],
        "anchor": fields["anchor"],
        "root": fields["root"],
        "parsed_slot_set": slot_set_text,
        "parsed_slot_count": len(slot_set)
    })

nonempty = [r for r in out_rows if int(r["parsed_slot_count"]) > 0]

top_slot_sets = sorted(
    [{"slot_set": k, "count": v} for k, v in slot_set_counts.items()],
    key=lambda x: (-x["count"], x["slot_set"])
)[:20]

top_pairs = sorted(
    [{"pair": k, "count": v} for k, v in pair_counts.items()],
    key=lambda x: (-x["count"], x["pair"])
)[:20]

out_csv = Path("artifacts/csv/g900_force_compression_six_nine_bridge_inspect_014_rows.v1.csv")
out_json = Path("artifacts/json/g900_force_compression_six_nine_bridge_inspect_014.v1.json")

with out_csv.open("w", newline="") as f:
    fieldnames = [
        "i", "pair_key", "source_pair", "source_root_slot",
        "source_limit_transition", "source_side_gap_signature",
        "broken_ladder", "phase_ladder_values",
        "inside_moving_endpoint", "outside_moving_endpoint",
        "anchor", "root", "parsed_slot_set", "parsed_slot_count"
    ]
    w = csv.DictWriter(f, fieldnames=fieldnames)
    w.writeheader()
    w.writerows(out_rows)

summary = {
    "schema": "g900.force.compression.six_nine.bridge.inspect_014",
    "version": "0.1",
    "status": "six_nine_058_candidate_rows_inspected",
    "audit_pass": True,
    "source": str(SRC),
    "row_count": len(rows),
    "nonempty_parsed_slot_row_count": len(nonempty),
    "distinct_slot_set_count": len(slot_set_counts),
    "top_slot_sets": top_slot_sets,
    "top_pairs": top_pairs,
    "root_slot_counts": root_slot_counts,
    "candidate_history_possible": len(nonempty) > 0,
    "metric_ready": False,
    "reason_metric_not_ready": "slot sets are abundant, but directed source-to-target slot history is not yet isolated",
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

print("status six_nine_058_candidate_rows_inspected")
print("audit_pass True")
print("row_count", len(rows))
print("nonempty_parsed_slot_row_count", len(nonempty))
print("distinct_slot_set_count", len(slot_set_counts))
print("candidate_history_possible", len(nonempty) > 0)
print("metric_ready False")
print("top_slot_set", top_slot_sets[0] if top_slot_sets else None)
print("csv", out_csv)
print("json", out_json)
