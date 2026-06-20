#!/usr/bin/env python3
import csv
import json
from pathlib import Path

LAB = Path.home() / "dev/cori/aletheos.ai/public_html/labs/g900_observatory"

sources = [
    LAB / "receipts",
    LAB / "artifacts/json",
]

rows = []

for root in sources:
    if not root.exists():
        continue

    for p in sorted(root.rglob("*.json")):
        try:
            obj = json.loads(p.read_text())
        except Exception:
            continue

        text = json.dumps(obj).lower()

        has_transport = "transport" in text
        has_information = "information" in text
        has_return_cell = "return_cell" in text
        has_receipt = "receipt" in text
        has_admitted = "admitted" in text

        candidate = (
            has_transport and
            has_information and
            has_receipt
        )

        rows.append({
            "path": str(p.relative_to(LAB)),
            "candidate_transport": candidate,
            "has_transport": has_transport,
            "has_information": has_information,
            "has_return_cell": has_return_cell,
            "has_receipt": has_receipt,
            "has_admitted": has_admitted
        })

candidates = [r for r in rows if r["candidate_transport"]]

out_csv = Path(
    "artifacts/csv/"
    "g900_force_compression_transport_inventory_021.v1.csv"
)
out_json = Path(
    "artifacts/json/"
    "g900_force_compression_transport_inventory_021.v1.json"
)

with out_csv.open("w", newline="") as f:
    fieldnames = list(rows[0].keys()) if rows else [
        "path",
        "candidate_transport",
        "has_transport",
        "has_information",
        "has_return_cell",
        "has_receipt",
        "has_admitted"
    ]
    w = csv.DictWriter(f, fieldnames=fieldnames)
    w.writeheader()
    w.writerows(rows)

summary = {
    "schema": "g900.force.compression.transport_inventory",
    "version": "0.1",
    "status": "transport_inventory_recorded",
    "audit_pass": True,
    "artifact_count": len(rows),
    "candidate_transport_count": len(candidates),
    "candidate_transport_paths":
        [r["path"] for r in candidates[:50]],
    "next_step":
        "determine whether additional transports are "
        "metric-ready for compression testing",
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

print("status transport_inventory_recorded")
print("audit_pass True")
print("artifact_count", len(rows))
print("candidate_transport_count", len(candidates))
print(
    "top_candidate",
    candidates[0]["path"] if candidates else "none"
)
print("json", out_json)
print("csv", out_csv)
