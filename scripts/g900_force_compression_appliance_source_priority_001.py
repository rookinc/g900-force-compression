#!/usr/bin/env python3
import csv
import json
from pathlib import Path

src = Path("artifacts/csv/g900_force_compression_appliance_source_discovery_001.v1.csv")
rows = list(csv.DictReader(src.open()))

weights = {
    "six_nine_return_home_receipt": 12,
    "return_home": 10,
    "return_cell_one_step_information_transport": 10,
    "bounded_information_transport": 9,
    "permission_channel": 8,
    "information_flux_witness": 8,
    "support_audit": 7,
    "carrier_incidence": 6,
    "packet_successor_rule": 6,
    "receipt": 5,
    "transport": 4,
    "information": 3,
    "return_cell": 4,
    "channel": 2,
    "candidate": 1,
    "force": 1,
}

def score(row):
    path = row["path"].lower()
    s = 0
    for term, w in weights.items():
        if term in path:
            s += w
    if path.endswith(".json"):
        s += 3
    if path.endswith(".csv"):
        s += 2
    if "backup" in row["kind"]:
        s -= 5
    if "bak" in path:
        s -= 5
    return s

out_rows = []
for r in rows:
    if r["status"] != "candidate_appliance_source":
        continue
    s = score(r)
    priority = "low"
    if s >= 14:
        priority = "high"
    elif s >= 8:
        priority = "medium"
    out_rows.append({
        "priority_score": s,
        "priority": priority,
        **r
    })

out_rows.sort(key=lambda r: (-int(r["priority_score"]), r["path"]))

out_csv = Path("artifacts/csv/g900_force_compression_appliance_source_priority_001.v1.csv")
out_json = Path("artifacts/json/g900_force_compression_appliance_source_priority_001.v1.json")

with out_csv.open("w", newline="") as f:
    fieldnames = ["priority_score", "priority", "path", "kind", "matched_terms", "status"]
    w = csv.DictWriter(f, fieldnames=fieldnames)
    w.writeheader()
    w.writerows(out_rows)

summary = {
    "schema": "g900.force.compression.appliance.source.priority",
    "version": "0.1",
    "status": "appliance_source_priority_recorded",
    "audit_pass": True,
    "source_count": len(out_rows),
    "high_priority_count": sum(1 for r in out_rows if r["priority"] == "high"),
    "medium_priority_count": sum(1 for r in out_rows if r["priority"] == "medium"),
    "low_priority_count": sum(1 for r in out_rows if r["priority"] == "low"),
    "top_sources": out_rows[:20],
    "boundary": {
        "source_interpreted": False,
        "compression_shadow_admitted": False,
        "force_renderer_admitted": False,
        "physical_gravity_claim": False,
        "body_mutation": False
    }
}
out_json.write_text(json.dumps(summary, indent=2) + "\n")

print("status appliance_source_priority_recorded")
print("audit_pass True")
print("source_count", summary["source_count"])
print("high_priority_count", summary["high_priority_count"])
print("medium_priority_count", summary["medium_priority_count"])
print("low_priority_count", summary["low_priority_count"])
print("top_source", out_rows[0]["path"] if out_rows else "none")
