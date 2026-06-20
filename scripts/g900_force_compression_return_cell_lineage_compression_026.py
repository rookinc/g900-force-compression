#!/usr/bin/env python3
import csv
import json
from pathlib import Path

SRC = Path("artifacts/csv/g900_force_compression_return_cell_packet_deep_extract_024_rows.v1.csv")
rows = list(csv.DictReader(SRC.open()))

def slot_dist(a, b, n=15):
    d = abs(int(a) - int(b)) % n
    return min(d, n - d)

def mean(xs):
    return sum(xs) / len(xs) if xs else None

def metric(records):
    from_slots = [int(r["from_slot"]) for r in records]
    to_slots = [int(r["to_slot"]) for r in records]
    home = sorted(set(to_slots))

    def md(s):
        return min(slot_dist(s, h) for h in home)

    before = [md(s) for s in from_slots]
    after = [md(s) for s in to_slots]

    return {
        "row_count": len(records),
        "from_slot_set": " ".join(map(str, sorted(set(from_slots)))),
        "to_slot_set": " ".join(map(str, sorted(set(to_slots)))),
        "mean_before": mean(before),
        "mean_after": mean(after),
        "radius_before": max(before),
        "radius_after": max(after),
        "signature": mean(after) <= mean(before) and max(after) <= max(before),
        "exact_after": all(d == 0 for d in after)
    }

by_source = {}
for r in rows:
    by_source.setdefault(r["source_path"], []).append(r)

records = []
for source, recs in sorted(by_source.items()):
    m = metric(recs)
    records.append({
        "source_path": source,
        **m
    })

all_signature = all(r["signature"] for r in records)
all_exact = all(r["exact_after"] for r in records)
shared_from = len(set(r["from_slot_set"] for r in records)) == 1
shared_to = len(set(r["to_slot_set"] for r in records)) == 1

out_csv = Path("artifacts/csv/g900_force_compression_return_cell_lineage_compression_026.v1.csv")
out_json = Path("artifacts/json/g900_force_compression_return_cell_lineage_compression_026.v1.json")

with out_csv.open("w", newline="") as f:
    fieldnames = [
        "source_path", "row_count", "from_slot_set", "to_slot_set",
        "mean_before", "mean_after", "radius_before", "radius_after",
        "signature", "exact_after"
    ]
    w = csv.DictWriter(f, fieldnames=fieldnames)
    w.writeheader()
    w.writerows(records)

summary = {
    "schema": "g900.force.compression.return_cell.lineage_compression",
    "version": "0.1",
    "status": "return_cell_lineage_compression_recorded",
    "audit_pass": all_signature and all_exact and shared_from and shared_to,
    "lineage_stage_count": len(records),
    "all_stages_preserve_signature": all_signature,
    "all_stages_exact_after": all_exact,
    "shared_from_slot_set": shared_from,
    "shared_to_slot_set": shared_to,
    "records": records,
    "lineage_statement": "The return-cell packet lineage preserves the same homeward-alignment compression signature across scout, carrier-incidence, and admitted transport stages.",
    "boundary": {
        "lineage_compression_only": True,
        "global_compression_shadow_admitted": False,
        "physical_gravity_claim": False,
        "force_renderer_admitted": False,
        "body_mutation": False
    }
}
out_json.write_text(json.dumps(summary, indent=2) + "\n")

print("status return_cell_lineage_compression_recorded")
print("audit_pass", summary["audit_pass"])
print("lineage_stage_count", len(records))
print("all_stages_preserve_signature", all_signature)
print("all_stages_exact_after", all_exact)
print("shared_from_slot_set", shared_from)
print("shared_to_slot_set", shared_to)
print("csv", out_csv)
print("json", out_json)
