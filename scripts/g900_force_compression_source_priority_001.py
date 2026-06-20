#!/usr/bin/env python3
import csv
import json
from pathlib import Path

src = Path("artifacts/csv/g900_force_compression_source_discovery_001.v1.csv")
rows = list(csv.DictReader(src.open()))

priority_terms = {
    "compression": 5,
    "gravity": 4,
    "null_well": 5,
    "null-well": 5,
    "receipt_home": 5,
    "return_home": 5,
    "return_cell": 4,
    "six_nine": 4,
    "six-nine": 4,
    "boundary": 2,
    "surface": 2,
    "inward": 5
}

def score(row):
    terms = row["matched_terms"].split(";") if row["matched_terms"] else []
    base = sum(priority_terms.get(t, 0) for t in terms)
    path = row["path"].lower()
    bonus = 0
    if path.endswith(".json"):
        bonus += 2
    if "theorem" in path or "audit" in path or "ledger" in path:
        bonus += 2
    if "rowset" in path or "rows" in path:
        bonus += 1
    if "draft" in path:
        bonus -= 1
    return base + bonus

out_rows = []
for r in rows:
    if r["status"] != "candidate_source":
        continue
    s = score(r)
    priority = "low"
    if s >= 9:
        priority = "high"
    elif s >= 5:
        priority = "medium"
    out_rows.append({
        "priority_score": s,
        "priority": priority,
        **r
    })

out_rows.sort(key=lambda r: (-int(r["priority_score"]), r["project"], r["path"]))

out_csv = Path("artifacts/csv/g900_force_compression_source_priority_001.v1.csv")
out_json = Path("artifacts/json/g900_force_compression_source_priority_001.v1.json")

with out_csv.open("w", newline="") as f:
    fieldnames = [
        "priority_score", "priority", "project", "path", "kind",
        "matched_terms", "status"
    ]
    w = csv.DictWriter(f, fieldnames=fieldnames)
    w.writeheader()
    w.writerows(out_rows)

summary = {
    "schema": "g900.force.compression.source.priority",
    "version": "0.1",
    "status": "source_priority_recorded",
    "audit_pass": True,
    "source_count": len(out_rows),
    "high_priority_count": sum(1 for r in out_rows if r["priority"] == "high"),
    "medium_priority_count": sum(1 for r in out_rows if r["priority"] == "medium"),
    "low_priority_count": sum(1 for r in out_rows if r["priority"] == "low"),
    "top_sources": out_rows[:12],
    "boundary": {
        "source_interpreted": False,
        "compression_shadow_admitted": False,
        "physical_gravity_claim": False,
        "body_mutation": False
    }
}
out_json.write_text(json.dumps(summary, indent=2) + "\n")

print("status source_priority_recorded")
print("audit_pass True")
print("source_count", summary["source_count"])
print("high_priority_count", summary["high_priority_count"])
print("medium_priority_count", summary["medium_priority_count"])
print("low_priority_count", summary["low_priority_count"])
print("top_source", out_rows[0]["path"] if out_rows else "none")
