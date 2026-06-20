#!/usr/bin/env python3
import json
from pathlib import Path

deps = [
    Path("artifacts/json/g900_force_compression_return_cell_checkpoint_009.v1.json"),
    Path("artifacts/json/g900_force_compression_return_cell_packet_deep_extract_024.v1.json"),
    Path("artifacts/json/g900_force_compression_return_cell_deep_extract_reconciliation_025.v1.json"),
    Path("artifacts/json/g900_force_compression_return_cell_lineage_compression_026.v1.json"),
]

loaded = {p.name: json.loads(p.read_text()) for p in deps}

checks = {
    "009_local_checkpoint_pass": loaded[deps[0].name].get("audit_pass") is True,
    "024_deep_extract_pass": loaded[deps[1].name].get("audit_pass") is True,
    "024_three_sources": loaded[deps[1].name].get("source_count") == 3,
    "025_reconciliation_pass": loaded[deps[2].name].get("audit_pass") is True,
    "025_same_signature_all_three": loaded[deps[2].name].get("result", {}).get("same_slot_signature_all_three") is True,
    "026_lineage_pass": loaded[deps[3].name].get("audit_pass") is True,
    "026_all_stages_signature": loaded[deps[3].name].get("all_stages_preserve_signature") is True,
    "026_all_stages_exact": loaded[deps[3].name].get("all_stages_exact_after") is True,
    "026_shared_from": loaded[deps[3].name].get("shared_from_slot_set") is True,
    "026_shared_to": loaded[deps[3].name].get("shared_to_slot_set") is True,
}

failed = [k for k, v in checks.items() if not v]

summary = {
    "schema": "g900.force.compression.return_cell.lineage_checkpoint",
    "version": "0.1",
    "status": "return_cell_lineage_compression_checkpoint_passed" if not failed else "return_cell_lineage_compression_checkpoint_failed",
    "audit_pass": not failed,
    "checkpoint_statement": "A three-stage return-cell packet lineage preserves the same local replay-stable bounded homeward-alignment compression signature.",
    "lineage_stages": [
        "g900_return_cell_conserved_packet_scout_001",
        "g900_return_cell_carrier_incidence_packet_scout_002",
        "g900_return_cell_one_step_information_transport_support_audit_006"
    ],
    "shared_signature": {
        "from_slot_set": [3, 6, 9],
        "to_slot_set": [9, 12, 13],
        "mean_distance_to_home": {
            "before": 2.75,
            "after": 0.0
        },
        "support_radius": {
            "before": 5,
            "after": 0
        },
        "exact_after": True
    },
    "upgrade_over_009": "009 verified the admitted transport; 027 verifies the same compression signature across the scout, carrier-incidence, and admitted transport lineage.",
    "dependency_count": len(deps),
    "check_count": len(checks),
    "failed_check_count": len(failed),
    "failed_checks": failed,
    "checks": checks,
    "boundary": {
        "lineage_checkpoint_only": True,
        "global_compression_shadow_admitted": False,
        "physical_gravity_claim": False,
        "force_renderer_admitted": False,
        "body_mutation": False
    }
}

out = Path("artifacts/json/g900_force_compression_return_cell_lineage_checkpoint_027.v1.json")
out.write_text(json.dumps(summary, indent=2) + "\n")

print("status", summary["status"])
print("audit_pass", summary["audit_pass"])
print("dependency_count", summary["dependency_count"])
print("check_count", summary["check_count"])
print("failed_check_count", summary["failed_check_count"])
print("checkpoint_statement", summary["checkpoint_statement"])
print("json", out)
