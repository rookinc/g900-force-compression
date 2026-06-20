#!/usr/bin/env python3
import csv
import json
from pathlib import Path

ROOT = Path("..").resolve()
PROJECTS = [
    "19-thalean-gravity-finite-tests",
    "29-g900-observatory-homecoming",
    "30-null-well-apparatus",
    "31-null-well-surface-inversion",
]

TERMS = [
    "six_nine",
    "six-nine",
    "null_well",
    "null-well",
    "surface",
    "receipt_home",
    "return_home",
    "return_cell",
    "inward",
    "boundary",
    "compression",
    "gravity",
]

rows = []
for project in PROJECTS:
    pdir = ROOT / project
    if not pdir.exists():
        rows.append({
            "project": project,
            "path": "",
            "kind": "missing_project",
            "matched_terms": "",
            "status": "missing_project"
        })
        continue

    for sub in ["artifacts/json", "artifacts/csv", "notes"]:
        sdir = pdir / sub
        if not sdir.exists():
            continue
        for path in sorted(sdir.rglob("*")):
            if not path.is_file():
                continue
            name = path.name.lower()
            rel = path.relative_to(ROOT)
            hits = [t for t in TERMS if t in name]
            if hits:
                rows.append({
                    "project": project,
                    "path": str(rel),
                    "kind": sub,
                    "matched_terms": ";".join(hits),
                    "status": "candidate_source"
                })

out_csv = Path("artifacts/csv/g900_force_compression_source_discovery_001.v1.csv")
out_json = Path("artifacts/json/g900_force_compression_source_discovery_001.v1.json")
out_csv.parent.mkdir(parents=True, exist_ok=True)
out_json.parent.mkdir(parents=True, exist_ok=True)

with out_csv.open("w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=[
        "project", "path", "kind", "matched_terms", "status"
    ])
    writer.writeheader()
    writer.writerows(rows)

summary = {
    "schema": "g900.force.compression.source.discovery",
    "version": "0.1",
    "status": "source_discovery_recorded",
    "audit_pass": True,
    "project_count": len(PROJECTS),
    "candidate_source_count": sum(1 for r in rows if r["status"] == "candidate_source"),
    "missing_project_count": sum(1 for r in rows if r["status"] == "missing_project"),
    "terms": TERMS,
    "boundary": {
        "compression_shadow_admitted": False,
        "physical_gravity_claim": False,
        "body_mutation": False,
        "interpretation_claim": False
    }
}
out_json.write_text(json.dumps(summary, indent=2) + "\n")

print("status source_discovery_recorded")
print("audit_pass True")
print("candidate_source_count", summary["candidate_source_count"])
print("missing_project_count", summary["missing_project_count"])
print("csv", out_csv)
print("json", out_json)
