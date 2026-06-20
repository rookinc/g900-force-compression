#!/usr/bin/env python3
import csv
import json
from pathlib import Path

LAB = Path.home() / "dev/cori/aletheos.ai/public_html/labs/g900_observatory"
JSON_PATH = LAB / "artifacts/json/g900_six_nine_return_home_receipt_ledger_068.v1.json"
CSV_PATH = LAB / "artifacts/csv/g900_six_nine_return_home_receipt_ledger_068_route_holds.v1.csv"

data = json.loads(JSON_PATH.read_text())
rows = list(csv.DictReader(CSV_PATH.open()))

holds = data.get("route_holds", [])
csv_holds = rows

checks = {
    "json_exists": JSON_PATH.exists(),
    "csv_exists": CSV_PATH.exists(),
    "audit_pass": data.get("audit_pass") is True,
    "holds_verified": data.get("holds_verified") is True,
    "summit_supported": data.get("summit_supported") is True,
    "boundaries_intact": data.get("boundaries_intact") is True,
    "force_claim_false": data.get("boundary", {}).get("force_claim") is False,
    "physics_claim_false": data.get("boundary", {}).get("physics_claim") is False,
    "viewer_or_body_mutation_false": data.get("boundary", {}).get("viewer_or_body_mutation") is False,
    "route_holds_present": len(holds) > 0,
    "csv_rows_present": len(csv_holds) > 0,
}

role_counts = {}
status_counts = {}
load_bearing_values = []

for r in csv_holds:
    role = r.get("role", "")
    status = r.get("status", "")
    lb = r.get("load_bearing_value", "")
    role_counts[role] = role_counts.get(role, 0) + 1
    status_counts[status] = status_counts.get(status, 0) + 1
    if lb:
        load_bearing_values.append(lb)

summary = {
    "schema": "g900.force.compression.six_nine.return_home_probe",
    "version": "0.1",
    "status": "six_nine_return_home_probe_recorded",
    "audit_pass": all(checks.values()),
    "source_json": str(JSON_PATH),
    "source_csv": str(CSV_PATH),
    "source_verdict": data.get("verdict"),
    "arrival_status": data.get("arrival_status"),
    "closed_claim": data.get("closed_claim"),
    "open_boundary": data.get("open_boundary"),
    "route_hold_count": len(csv_holds),
    "role_counts": role_counts,
    "status_counts": status_counts,
    "load_bearing_values": load_bearing_values,
    "checks": checks,
    "compression_relevance": {
        "return_home_receipt_present": checks["holds_verified"],
        "summit_supported": checks["summit_supported"],
        "candidate_surface": "six_nine_return_home",
        "metric_ready": False,
        "reason_metric_not_ready": "route-hold ledger has roles and load-bearing values but no explicit source-to-target slot history in this probe"
    },
    "boundary": {
        "source_probe_only": True,
        "compression_signature_claim": False,
        "compression_shadow_admitted": False,
        "physical_gravity_claim": False,
        "force_renderer_admitted": False,
        "body_mutation": False
    }
}

out_json = Path("artifacts/json/g900_force_compression_six_nine_return_home_probe_010.v1.json")
out_csv = Path("artifacts/csv/g900_force_compression_six_nine_return_home_probe_010_holds.v1.csv")

out_json.write_text(json.dumps(summary, indent=2) + "\n")

with out_csv.open("w", newline="") as f:
    fieldnames = ["hold", "role", "status", "load_bearing_value"]
    w = csv.DictWriter(f, fieldnames=fieldnames)
    w.writeheader()
    for r in csv_holds:
        w.writerow({k: r.get(k, "") for k in fieldnames})

print("status six_nine_return_home_probe_recorded")
print("audit_pass", summary["audit_pass"])
print("route_hold_count", summary["route_hold_count"])
print("arrival_status", summary["arrival_status"])
print("metric_ready", summary["compression_relevance"]["metric_ready"])
print("json", out_json)
print("csv", out_csv)
