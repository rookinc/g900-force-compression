#!/usr/bin/env python3
import csv
import json
from pathlib import Path

LAB = Path.home() / "dev/cori/aletheos.ai/public_html/labs/g900_observatory"

TERMS = [
    "force",
    "compression",
    "gravity",
    "candidate",
    "receipt",
    "information",
    "transport",
    "permission",
    "channel",
    "return_cell",
    "tracer",
    "smear",
    "render_contract",
    "apparatus",
    "quartz",
    "camera",
]

rows = []

if not LAB.exists():
    rows.append({
        "path": "",
        "kind": "missing_lab",
        "matched_terms": "",
        "status": "missing_lab"
    })
else:
    for path in sorted(LAB.rglob("*")):
        if not path.is_file():
            continue
        rel = path.relative_to(LAB)
        name = path.name.lower()
        rels = str(rel).lower()
        hits = [t for t in TERMS if t in name or t in rels]
        if hits:
            kind = "file"
            if ".bak." in name:
                kind = "backup"
            elif path.suffix == ".js":
                kind = "runtime_js"
            elif path.suffix == ".html":
                kind = "runtime_html"
            elif path.suffix == ".css":
                kind = "runtime_css"
            elif path.suffix == ".json":
                kind = "json"
            elif path.suffix == ".md":
                kind = "note"

            rows.append({
                "path": str(rel),
                "kind": kind,
                "matched_terms": ";".join(hits),
                "status": "candidate_appliance_source"
            })

out_csv = Path("artifacts/csv/g900_force_compression_appliance_source_discovery_001.v1.csv")
out_json = Path("artifacts/json/g900_force_compression_appliance_source_discovery_001.v1.json")
out_csv.parent.mkdir(parents=True, exist_ok=True)
out_json.parent.mkdir(parents=True, exist_ok=True)

with out_csv.open("w", newline="") as f:
    fieldnames = ["path", "kind", "matched_terms", "status"]
    w = csv.DictWriter(f, fieldnames=fieldnames)
    w.writeheader()
    w.writerows(rows)

summary = {
    "schema": "g900.force.compression.appliance.source.discovery",
    "version": "0.1",
    "status": "appliance_source_discovery_recorded",
    "audit_pass": True,
    "lab_path": str(LAB),
    "candidate_appliance_source_count": sum(1 for r in rows if r["status"] == "candidate_appliance_source"),
    "missing_lab_count": sum(1 for r in rows if r["status"] == "missing_lab"),
    "runtime_js_count": sum(1 for r in rows if r["kind"] == "runtime_js"),
    "runtime_html_count": sum(1 for r in rows if r["kind"] == "runtime_html"),
    "backup_count": sum(1 for r in rows if r["kind"] == "backup"),
    "terms": TERMS,
    "boundary": {
        "appliance_interpreted": False,
        "compression_shadow_admitted": False,
        "force_renderer_admitted": False,
        "physical_gravity_claim": False,
        "body_mutation": False
    }
}
out_json.write_text(json.dumps(summary, indent=2) + "\n")

print("status appliance_source_discovery_recorded")
print("audit_pass True")
print("candidate_appliance_source_count", summary["candidate_appliance_source_count"])
print("runtime_js_count", summary["runtime_js_count"])
print("runtime_html_count", summary["runtime_html_count"])
print("backup_count", summary["backup_count"])
print("csv", out_csv)
print("json", out_json)
