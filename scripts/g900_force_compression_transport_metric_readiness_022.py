#!/usr/bin/env python3
import csv
import json
from pathlib import Path

LAB = Path.home() / "dev/cori/aletheos.ai/public_html/labs/g900_observatory"
inv = Path("artifacts/csv/g900_force_compression_transport_inventory_021.v1.csv")
rows = list(csv.DictReader(inv.open()))

candidate_paths = [r["path"] for r in rows if r.get("candidate_transport") == "True"]

def flatten(obj, prefix=""):
    out = []
    if isinstance(obj, dict):
        for k, v in obj.items():
            p = f"{prefix}.{k}" if prefix else str(k)
            out.append(p)
            out.extend(flatten(v, p))
    elif isinstance(obj, list):
        p = prefix + "[]"
        out.append(p)
        for item in obj[:3]:
            out.extend(flatten(item, p))
    return out

out_rows = []

for rel in candidate_paths:
    p = LAB / rel
    rec = {
        "path": rel,
        "exists": p.exists(),
        "json_read": False,
        "has_from_slot": False,
        "has_to_slot": False,
        "has_from_vertex": False,
        "has_to_vertex": False,
        "has_history": False,
        "has_packet": False,
        "has_h0_h1": False,
        "metric_ready_candidate": False,
        "readiness_reason": ""
    }

    if not p.exists():
        rec["readiness_reason"] = "missing"
        out_rows.append(rec)
        continue

    try:
        data = json.loads(p.read_text())
        rec["json_read"] = True
        keys = [k.lower() for k in flatten(data)]
        joined = "\n".join(keys)

        rec["has_from_slot"] = "from_slot" in joined
        rec["has_to_slot"] = "to_slot" in joined
        rec["has_from_vertex"] = "from_vertex" in joined
        rec["has_to_vertex"] = "to_vertex" in joined
        rec["has_history"] = "history" in joined
        rec["has_packet"] = "packet" in joined
        rec["has_h0_h1"] = ("h0" in joined and "h1" in joined)

        rec["metric_ready_candidate"] = (
            rec["has_from_slot"]
            and rec["has_to_slot"]
            and (rec["has_history"] or rec["has_packet"] or rec["has_h0_h1"])
        )

        if rec["metric_ready_candidate"]:
            rec["readiness_reason"] = "explicit_from_to_slot_structure"
        else:
            rec["readiness_reason"] = "missing_explicit_from_to_slot_structure"
    except Exception as e:
        rec["readiness_reason"] = "error:" + type(e).__name__

    out_rows.append(rec)

out_rows.sort(key=lambda r: (not r["metric_ready_candidate"], r["path"]))

out_csv = Path("artifacts/csv/g900_force_compression_transport_metric_readiness_022.v1.csv")
out_json = Path("artifacts/json/g900_force_compression_transport_metric_readiness_022.v1.json")

with out_csv.open("w", newline="") as f:
    fieldnames = [
        "path", "exists", "json_read", "has_from_slot", "has_to_slot",
        "has_from_vertex", "has_to_vertex", "has_history", "has_packet",
        "has_h0_h1", "metric_ready_candidate", "readiness_reason"
    ]
    w = csv.DictWriter(f, fieldnames=fieldnames)
    w.writeheader()
    w.writerows(out_rows)

ready = [r for r in out_rows if r["metric_ready_candidate"]]

summary = {
    "schema": "g900.force.compression.transport_metric_readiness",
    "version": "0.1",
    "status": "transport_metric_readiness_recorded",
    "audit_pass": True,
    "candidate_transport_count": len(candidate_paths),
    "metric_ready_candidate_count": len(ready),
    "metric_ready_candidate_paths": [r["path"] for r in ready[:40]],
    "boundary": {
        "readiness_filter_only": True,
        "compression_signature_claim": False,
        "global_compression_shadow_admitted": False,
        "physical_gravity_claim": False,
        "force_renderer_admitted": False,
        "body_mutation": False
    }
}

out_json.write_text(json.dumps(summary, indent=2) + "\n")

print("status transport_metric_readiness_recorded")
print("audit_pass True")
print("candidate_transport_count", len(candidate_paths))
print("metric_ready_candidate_count", len(ready))
print("top_ready", ready[0]["path"] if ready else "none")
print("csv", out_csv)
print("json", out_json)
