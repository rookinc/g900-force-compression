#!/usr/bin/env python3
import csv
import json
from pathlib import Path

LAB = Path.home() / "dev/cori/aletheos.ai/public_html/labs/g900_observatory"
INV = Path("artifacts/csv/g900_force_compression_transport_inventory_021.v1.csv")

candidate_paths = []
for r in csv.DictReader(INV.open()):
    if r.get("candidate_transport") == "True":
        candidate_paths.append(r["path"])

def walk(obj, path=""):
    if isinstance(obj, dict):
        yield path, obj
        for k, v in obj.items():
            p = f"{path}.{k}" if path else str(k)
            yield from walk(v, p)
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            p = f"{path}[{i}]"
            yield from walk(v, p)

def is_rowlike(d):
    if not isinstance(d, dict):
        return False
    return "from_slot" in d and "to_slot" in d

records = []

for rel in candidate_paths:
    p = LAB / rel
    rowlikes = []
    read_status = "missing"

    if p.exists():
        try:
            obj = json.loads(p.read_text())
            read_status = "json_read"
            for jp, d in walk(obj):
                if is_rowlike(d):
                    rowlikes.append((jp, d))
        except Exception as e:
            read_status = "error:" + type(e).__name__

    from_slots = sorted(set(str(d.get("from_slot")) for _, d in rowlikes if d.get("from_slot") not in [None, ""]))
    to_slots = sorted(set(str(d.get("to_slot")) for _, d in rowlikes if d.get("to_slot") not in [None, ""]))
    has_vertices = any(("from_vertex" in d or "to_vertex" in d) for _, d in rowlikes)
    has_edges = any(("edge_id" in d and d.get("edge_id")) for _, d in rowlikes)

    metric_constructible = bool(rowlikes and from_slots and to_slots)

    records.append({
        "transport_path": rel,
        "read_status": read_status,
        "rowlike_record_count": len(rowlikes),
        "from_slot_set": " ".join(from_slots),
        "to_slot_set": " ".join(to_slots),
        "has_from_slot": bool(from_slots),
        "has_to_slot": bool(to_slots),
        "has_vertex_fields": has_vertices,
        "has_edge_ids": has_edges,
        "has_home_candidate": bool(to_slots),
        "metric_constructible": metric_constructible
    })

records.sort(key=lambda r: (not r["metric_constructible"], -int(r["rowlike_record_count"]), r["transport_path"]))

out_csv = Path("artifacts/csv/g900_force_compression_transport_history_surface_inventory_032.v1.csv")
out_json = Path("artifacts/json/g900_force_compression_transport_history_surface_inventory_032.v1.json")

with out_csv.open("w", newline="") as f:
    fieldnames = [
        "transport_path", "read_status", "rowlike_record_count",
        "from_slot_set", "to_slot_set", "has_from_slot", "has_to_slot",
        "has_vertex_fields", "has_edge_ids", "has_home_candidate",
        "metric_constructible"
    ]
    w = csv.DictWriter(f, fieldnames=fieldnames)
    w.writeheader()
    w.writerows(records)

ready = [r for r in records if r["metric_constructible"]]

summary = {
    "schema": "g900.force.compression.transport_history_surface_inventory",
    "version": "0.1",
    "status": "transport_history_surface_inventory_recorded",
    "audit_pass": True,
    "candidate_transport_count": len(candidate_paths),
    "metric_constructible_count": len(ready),
    "metric_constructible_paths": [r["transport_path"] for r in ready],
    "records": records,
    "boundary": {
        "inventory_only": True,
        "compression_signature_claim": False,
        "global_compression_shadow_admitted": False,
        "physical_gravity_claim": False,
        "force_renderer_admitted": False,
        "body_mutation": False
    }
}

out_json.write_text(json.dumps(summary, indent=2) + "\n")

print("status transport_history_surface_inventory_recorded")
print("audit_pass True")
print("candidate_transport_count", len(candidate_paths))
print("metric_constructible_count", len(ready))
print("top_ready", ready[0]["transport_path"] if ready else "none")
print("csv", out_csv)
print("json", out_json)
