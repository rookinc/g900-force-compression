#!/usr/bin/env python3
import json
from pathlib import Path

deps = [
    Path("artifacts/json/g900_force_compression_phase_checkpoint_017.v1.json"),
    Path("artifacts/json/g900_force_compression_transport_inventory_021.v1.json"),
    Path("artifacts/json/g900_force_compression_transport_metric_readiness_022.v1.json"),
    Path("artifacts/json/g900_force_compression_return_cell_packet_deep_extract_024.v1.json"),
    Path("artifacts/json/g900_force_compression_return_cell_deep_extract_reconciliation_025.v1.json"),
    Path("artifacts/json/g900_force_compression_return_cell_lineage_compression_026.v1.json"),
    Path("artifacts/json/g900_force_compression_return_cell_lineage_checkpoint_027.v1.json"),
    Path("artifacts/json/g900_force_compression_return_cell_lineage_theorem_candidate_028.v1.json"),
    Path("artifacts/json/g900_force_compression_return_cell_lineage_theorem_verify_029.v1.json"),
]

loaded = {p.name: json.loads(p.read_text()) for p in deps}

checks = {
    "017_phase_checkpoint_pass": loaded[deps[0].name].get("audit_pass") is True,
    "021_transport_inventory_pass": loaded[deps[1].name].get("audit_pass") is True,
    "021_candidate_transport_count_80": loaded[deps[1].name].get("candidate_transport_count") == 80,
    "022_metric_readiness_pass": loaded[deps[2].name].get("audit_pass") is True,
    "022_field_scan_ready_count_3": loaded[deps[2].name].get("metric_ready_candidate_count") == 3,
    "024_deep_extract_pass": loaded[deps[3].name].get("audit_pass") is True,
    "024_source_count_3": loaded[deps[3].name].get("source_count") == 3,
    "024_rowlike_count_32": loaded[deps[3].name].get("rowlike_record_count") == 32,
    "025_reconciliation_pass": loaded[deps[4].name].get("audit_pass") is True,
    "025_same_signature_all_three": loaded[deps[4].name].get("result", {}).get("same_slot_signature_all_three") is True,
    "026_lineage_compression_pass": loaded[deps[5].name].get("audit_pass") is True,
    "027_lineage_checkpoint_pass": loaded[deps[6].name].get("audit_pass") is True,
    "028_theorem_candidate_pass": loaded[deps[7].name].get("audit_pass") is True,
    "029_theorem_verified": loaded[deps[8].name].get("audit_pass") is True,
    "029_failed_zero": loaded[deps[8].name].get("failed_check_count") == 0,
}

failed = [k for k, v in checks.items() if not v]

summary = {
    "schema": "g900.force.compression.phase_checkpoint_v2",
    "version": "0.1",
    "status": "compression_phase_checkpoint_v2_passed" if not failed else "compression_phase_checkpoint_v2_failed",
    "audit_pass": not failed,
    "phase_statement": "Project 32 has verified a local lineage-stable finite homeward-alignment compression theorem for the presently known return-cell packet lineage.",
    "theorem_statement": "For the presently known return-cell packet lineage, all three packet stages preserve the same finite homeward-alignment compression signature.",
    "lineage_stages": [
        "conserved_packet_scout_001",
        "carrier_incidence_packet_scout_002",
        "one_step_information_transport_support_audit_006"
    ],
    "shared_signature": {
        "from_slot_set": [3, 6, 9],
        "to_slot_set": [9, 12, 13],
        "mean_distance_to_home_before": 2.75,
        "mean_distance_to_home_after": 0.0,
        "support_radius_before": 5,
        "support_radius_after": 0,
        "exact_after": True
    },
    "current_taxonomy": {
        "return_cell": "verified_local_lineage_stable_transport_compression",
        "six_nine": "receipt_strong_surface_compression_candidate_not_metric_ready"
    },
    "next_allowed_steps": [
        "write theorem section into paper",
        "define six_nine_surface_metric",
        "search for non_return_cell_metric_ready_transport_family",
        "update appliance copy to mention local lineage-stable compression only"
    ],
    "closed_boundaries": {
        "global_compression_shadow_admitted": False,
        "physical_gravity_claim": False,
        "force_renderer_admitted": False,
        "body_mutation": False,
        "future_lineage_uniqueness_claim": False
    },
    "dependency_count": len(deps),
    "check_count": len(checks),
    "failed_check_count": len(failed),
    "failed_checks": failed,
    "checks": checks,
    "source_artifacts": [str(p) for p in deps]
}

out = Path("artifacts/json/g900_force_compression_phase_checkpoint_v2_030.v1.json")
out.write_text(json.dumps(summary, indent=2) + "\n")

print("status", summary["status"])
print("audit_pass", summary["audit_pass"])
print("dependency_count", summary["dependency_count"])
print("check_count", summary["check_count"])
print("failed_check_count", summary["failed_check_count"])
print("phase_statement", summary["phase_statement"])
print("json", out)
