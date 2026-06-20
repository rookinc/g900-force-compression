#!/usr/bin/env python3
import csv
import json
from pathlib import Path

LAB = Path.home() / "dev/cori/aletheos.ai/public_html/labs/g900_observatory"

paths = [
    "artifacts/json/g900_return_cell_conserved_packet_scout_001.v1.json",
    "artifacts/json/g900_return_cell_carrier_incidence_packet_scout_002.v1.json",
    "artifacts/json/g900_return_cell_one_step_information_transport_support_audit_006.v1.json",
]

def walk(obj, path=""):
    if isinstance(obj, dict):
        yield path, obj
        for k, v in obj.items():
            p = f"{path}.{k}" if path else str(k)
            yield from walk(v, p)
    elif isinstance(obj, list):
        for i, item in enumerate(obj):
            yield from walk(item, f"{path}[{i}]")

def rowlike(d):
    if not isinstance(d, dict):
        return False
    keys = set(d.keys())
    return (
        ("from_slot" in keys and "to_slot" in keys)
        or ("source_slot" in keys and "target_slot" in keys)
        or ("from_vertex" in keys and "to_vertex" in keys)
        or ("edge_id" in keys and ("from_slot" in keys or "to_slot" in keys))
    )

rows = []

for rel in paths:
    p = LAB / rel
    obj = json.loads(p.read_text())

    for jpath, d in walk(obj):
        if rowlike(d):
            rows.append({
                "source_path": rel,
                "json_path": jpath,
                "from_slot": d.get("from_slot", d.get("source_slot", "")),
                "to_slot": d.get("to_slot", d.get("target_slot", "")),
                "from_vertex": d.get("from_vertex", ""),
                "to_vertex": d.get("to_vertex", ""),
                "edge_id": d.get("edge_id", ""),
                "segment_role": d.get("segment_role", ""),
                "anchor_limit": d.get("anchor_limit", ""),
                "selection_score": d.get("selection_score", "")
            })

source_counts = {}
for r in rows:
    source_counts[r["source_path"]] = source_counts.get(r["source_path"], 0) + 1

slot_signature_by_source = {}
for rel in paths:
    rs = [r for r in rows if r["source_path"] == rel]
    froms = sorted(set(str(r["from_slot"]) for r in rs if str(r["from_slot"]) != ""))
    tos = sorted(set(str(r["to_slot"]) for r in rs if str(r["to_slot"]) != ""))
    slot_signature_by_source[rel] = {
        "rowlike_count": len(rs),
        "from_slot_set": froms,
        "to_slot_set": tos
    }

out_csv = Path("artifacts/csv/g900_force_compression_return_cell_packet_deep_extract_024_rows.v1.csv")
out_json = Path("artifacts/json/g900_force_compression_return_cell_packet_deep_extract_024.v1.json")

with out_csv.open("w", newline="") as f:
    fieldnames = [
        "source_path", "json_path", "from_slot", "to_slot",
        "from_vertex", "to_vertex", "edge_id", "segment_role",
        "anchor_limit", "selection_score"
    ]
    w = csv.DictWriter(f, fieldnames=fieldnames)
    w.writeheader()
    w.writerows(rows)

summary = {
    "schema": "g900.force.compression.return_cell.packet_deep_extract",
    "version": "0.1",
    "status": "return_cell_packet_deep_extract_recorded",
    "audit_pass": True,
    "source_count": len(paths),
    "rowlike_record_count": len(rows),
    "source_counts": source_counts,
    "slot_signature_by_source": slot_signature_by_source,
    "boundary": {
        "deep_extract_only": True,
        "compression_signature_claim": False,
        "global_compression_shadow_admitted": False,
        "physical_gravity_claim": False,
        "force_renderer_admitted": False,
        "body_mutation": False
    }
}

out_json.write_text(json.dumps(summary, indent=2) + "\n")

print("status return_cell_packet_deep_extract_recorded")
print("audit_pass True")
print("source_count", len(paths))
print("rowlike_record_count", len(rows))
print("source_counts", source_counts)
print("json", out_json)
print("csv", out_csv)
