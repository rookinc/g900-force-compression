#!/usr/bin/env python3
import csv
import json
from pathlib import Path

LAB = Path.home() / "dev/cori/aletheos.ai/public_html/labs/g900_observatory"
priority_csv = Path("artifacts/csv/g900_force_compression_appliance_source_priority_001.v1.csv")

priority_rows = list(csv.DictReader(priority_csv.open()))
top = [r for r in priority_rows if r["priority"] == "high"][:12]

def flatten_keys(obj, prefix=""):
    keys = []
    if isinstance(obj, dict):
        for k, v in obj.items():
            p = f"{prefix}.{k}" if prefix else str(k)
            keys.append(p)
            keys.extend(flatten_keys(v, p))
    elif isinstance(obj, list):
        keys.append(prefix + "[]")
        for item in obj[:3]:
            keys.extend(flatten_keys(item, prefix + "[]"))
    return keys

rows = []
for r in top:
    rel = r["path"]
    path = LAB / rel
    rec = {
        "path": rel,
        "exists": path.exists(),
        "kind": r["kind"],
        "priority_score": r["priority_score"],
        "read_status": "",
        "top_level_keys": "",
        "interesting_keys": "",
        "row_count": "",
        "field_count": "",
    }

    if not path.exists():
        rec["read_status"] = "missing"
        rows.append(rec)
        continue

    try:
        if path.suffix == ".json":
            data = json.loads(path.read_text())
            if isinstance(data, dict):
                rec["top_level_keys"] = ";".join(sorted(data.keys()))
            flat = sorted(set(flatten_keys(data)))
            interesting = [
                k for k in flat
                if any(t in k.lower() for t in [
                    "audit_pass", "verdict", "status", "transport", "permission",
                    "receipt", "support", "edge", "route", "history",
                    "obligation", "claim", "boundary", "mutates", "physical",
                    "force", "body"
                ])
            ]
            rec["interesting_keys"] = ";".join(interesting[:80])
            rec["field_count"] = len(flat)
            rec["read_status"] = "json_read"
        elif path.suffix == ".csv":
            with path.open(newline="") as f:
                reader = csv.DictReader(f)
                rows_list = list(reader)
                rec["row_count"] = len(rows_list)
                rec["top_level_keys"] = ";".join(reader.fieldnames or [])
                rec["field_count"] = len(reader.fieldnames or [])
                rec["read_status"] = "csv_read"
        else:
            text = path.read_text(errors="replace")
            rec["row_count"] = len(text.splitlines())
            rec["read_status"] = "text_read"
    except Exception as e:
        rec["read_status"] = "error:" + type(e).__name__

    rows.append(rec)

out_csv = Path("artifacts/csv/g900_force_compression_appliance_field_inventory_001.v1.csv")
out_json = Path("artifacts/json/g900_force_compression_appliance_field_inventory_001.v1.json")

with out_csv.open("w", newline="") as f:
    fieldnames = [
        "path", "exists", "kind", "priority_score", "read_status",
        "top_level_keys", "interesting_keys", "row_count", "field_count"
    ]
    w = csv.DictWriter(f, fieldnames=fieldnames)
    w.writeheader()
    w.writerows(rows)

summary = {
    "schema": "g900.force.compression.appliance.field.inventory",
    "version": "0.1",
    "status": "appliance_field_inventory_recorded",
    "audit_pass": True,
    "inspected_source_count": len(rows),
    "json_read_count": sum(1 for r in rows if r["read_status"] == "json_read"),
    "csv_read_count": sum(1 for r in rows if r["read_status"] == "csv_read"),
    "missing_count": sum(1 for r in rows if r["read_status"] == "missing"),
    "error_count": sum(1 for r in rows if r["read_status"].startswith("error")),
    "sources": rows,
    "boundary": {
        "field_inventory_only": True,
        "source_interpreted": False,
        "compression_shadow_admitted": False,
        "force_renderer_admitted": False,
        "physical_gravity_claim": False,
        "body_mutation": False
    }
}
out_json.write_text(json.dumps(summary, indent=2) + "\n")

print("status appliance_field_inventory_recorded")
print("audit_pass True")
print("inspected_source_count", summary["inspected_source_count"])
print("json_read_count", summary["json_read_count"])
print("csv_read_count", summary["csv_read_count"])
print("missing_count", summary["missing_count"])
print("error_count", summary["error_count"])
print("csv", out_csv)
print("json", out_json)
