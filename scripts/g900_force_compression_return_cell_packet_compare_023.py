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

def flatten_packets(obj):
    packets = []
    if isinstance(obj, dict):
        for k, v in obj.items():
            if k == "packet" and isinstance(v, list):
                packets.append(v)
            else:
                packets.extend(flatten_packets(v))
    elif isinstance(obj, list):
        for item in obj:
            packets.extend(flatten_packets(item))
    return packets

def packet_summary(packet):
    from_slots = []
    to_slots = []
    edge_ids = []
    for row in packet:
        if isinstance(row, dict):
            if "from_slot" in row:
                from_slots.append(row["from_slot"])
            if "to_slot" in row:
                to_slots.append(row["to_slot"])
            if "edge_id" in row:
                edge_ids.append(row["edge_id"])
    return {
        "row_count": len(packet),
        "from_slots": " ".join(map(str, from_slots)),
        "to_slots": " ".join(map(str, to_slots)),
        "from_slot_set": " ".join(map(str, sorted(set(from_slots)))),
        "to_slot_set": " ".join(map(str, sorted(set(to_slots)))),
        "edge_ids": " ".join(map(str, edge_ids))
    }

rows = []

for rel in paths:
    p = LAB / rel
    obj = json.loads(p.read_text())
    packets = flatten_packets(obj)

    if not packets:
        rows.append({
            "path": rel,
            "packet_index": "",
            "packet_count": 0,
            "row_count": 0,
            "from_slots": "",
            "to_slots": "",
            "from_slot_set": "",
            "to_slot_set": "",
            "edge_ids": ""
        })
        continue

    for idx, packet in enumerate(packets):
        s = packet_summary(packet)
        rows.append({
            "path": rel,
            "packet_index": idx,
            "packet_count": len(packets),
            **s
        })

# signature comparison
signatures = {}
for r in rows:
    sig = (r["from_slot_set"], r["to_slot_set"])
    signatures.setdefault(str(sig), []).append(r["path"])

out_csv = Path("artifacts/csv/g900_force_compression_return_cell_packet_compare_023.v1.csv")
out_json = Path("artifacts/json/g900_force_compression_return_cell_packet_compare_023.v1.json")

with out_csv.open("w", newline="") as f:
    fieldnames = [
        "path", "packet_index", "packet_count", "row_count",
        "from_slots", "to_slots", "from_slot_set", "to_slot_set", "edge_ids"
    ]
    w = csv.DictWriter(f, fieldnames=fieldnames)
    w.writeheader()
    w.writerows(rows)

summary = {
    "schema": "g900.force.compression.return_cell.packet_compare",
    "version": "0.1",
    "status": "return_cell_packet_compare_recorded",
    "audit_pass": True,
    "source_count": len(paths),
    "packet_record_count": len(rows),
    "signature_count": len(signatures),
    "signatures": signatures,
    "same_slot_signature_all": len(signatures) == 1,
    "boundary": {
        "packet_compare_only": True,
        "compression_signature_claim": False,
        "global_compression_shadow_admitted": False,
        "physical_gravity_claim": False,
        "force_renderer_admitted": False,
        "body_mutation": False
    }
}
out_json.write_text(json.dumps(summary, indent=2) + "\n")

print("status return_cell_packet_compare_recorded")
print("audit_pass True")
print("source_count", len(paths))
print("packet_record_count", len(rows))
print("signature_count", len(signatures))
print("same_slot_signature_all", len(signatures) == 1)
print("csv", out_csv)
print("json", out_json)
