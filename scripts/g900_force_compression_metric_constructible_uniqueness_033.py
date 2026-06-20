#!/usr/bin/env python3
import csv
import json
from pathlib import Path

src = Path("artifacts/csv/g900_force_compression_transport_history_surface_inventory_032.v1.csv")
rows = list(csv.DictReader(src.open()))

constructible = [r for r in rows if r["metric_constructible"] == "True"]

all_return_cell = all("g900_return_cell_" in r["transport_path"] for r in constructible)
all_same_signature = (
    len(set(r["from_slot_set"] for r in constructible)) == 1
    and len(set(r["to_slot_set"] for r in constructible)) == 1
)

checks = {
    "source_rows_present": len(rows) == 80,
    "constructible_count_3": len(constructible) == 3,
    "all_constructible_return_cell": all_return_cell,
    "all_constructible_same_signature": all_same_signature,
    "shared_from_slot_set_3_6_9": all(r["from_slot_set"] == "3 6 9" for r in constructible),
    "shared_to_slot_set_12_13_9": all(r["to_slot_set"] == "12 13 9" for r in constructible)
}

failed = [k for k, v in checks.items() if not v]

summary = {
    "schema": "g900.force.compression.metric_constructible_uniqueness",
    "version": "0.1",
    "status": "metric_constructible_uniqueness_recorded" if not failed else "metric_constructible_uniqueness_failed",
    "audit_pass": not failed,
    "candidate_transport_count": len(rows),
    "metric_constructible_count": len(constructible),
    "constructible_paths": [r["transport_path"] for r in constructible],
    "uniqueness_statement": "In the tested transport-labeled candidate family, only the return-cell packet lineage is metric-constructible for homeward-alignment compression testing.",
    "shared_signature": {
        "from_slot_set": [3, 6, 9],
        "to_slot_set": [9, 12, 13]
    },
    "check_count": len(checks),
    "failed_check_count": len(failed),
    "failed_checks": failed,
    "checks": checks,
    "boundary": {
        "tested_family_uniqueness_only": True,
        "global_uniqueness_claim": False,
        "compression_signature_claim_beyond_return_cell": False,
        "global_compression_shadow_admitted": False,
        "physical_gravity_claim": False,
        "force_renderer_admitted": False,
        "body_mutation": False
    }
}

out = Path("artifacts/json/g900_force_compression_metric_constructible_uniqueness_033.v1.json")
out.write_text(json.dumps(summary, indent=2) + "\n")

print("status", summary["status"])
print("audit_pass", summary["audit_pass"])
print("candidate_transport_count", len(rows))
print("metric_constructible_count", len(constructible))
print("failed_check_count", len(failed))
print("uniqueness_statement", summary["uniqueness_statement"])
print("json", out)
