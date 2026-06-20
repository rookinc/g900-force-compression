#!/usr/bin/env python3
import json
from pathlib import Path

deps = [
    Path("artifacts/json/g900_force_compression_phase_checkpoint_v2_030.v1.json"),
    Path("artifacts/json/g900_force_compression_transport_history_surface_inventory_032.v1.json"),
    Path("artifacts/json/g900_force_compression_metric_constructible_uniqueness_033.v1.json")
]

loaded = {p.name: json.loads(p.read_text()) for p in deps}

checks = {
    "030_phase_v2_pass": loaded[deps[0].name].get("audit_pass") is True,
    "032_inventory_pass": loaded[deps[1].name].get("audit_pass") is True,
    "032_candidate_transport_count_80": loaded[deps[1].name].get("candidate_transport_count") == 80,
    "032_metric_constructible_count_3": loaded[deps[1].name].get("metric_constructible_count") == 3,
    "033_uniqueness_pass": loaded[deps[2].name].get("audit_pass") is True,
    "033_candidate_transport_count_80": loaded[deps[2].name].get("candidate_transport_count") == 80,
    "033_metric_constructible_count_3": loaded[deps[2].name].get("metric_constructible_count") == 3,
    "033_failed_zero": loaded[deps[2].name].get("failed_check_count") == 0
}

failed = [k for k, v in checks.items() if not v]

summary = {
    "schema": "g900.force.compression.phase_checkpoint_v3",
    "version": "0.1",
    "status": "compression_phase_checkpoint_v3_passed" if not failed else "compression_phase_checkpoint_v3_failed",
    "audit_pass": not failed,
    "phase_statement": "Project 32 has verified a local lineage-stable finite homeward-alignment compression theorem and a tested-family uniqueness result for metric-constructible transport histories.",
    "closed_results": [
        "return_cell_lineage_compression_theorem_verified",
        "tested_family_metric_constructible_uniqueness_recorded"
    ],
    "uniqueness_scope": {
        "candidate_transport_count": 80,
        "metric_constructible_count": 3,
        "all_metric_constructible_histories_are_return_cell_lineage": True,
        "global_uniqueness_claim": False
    },
    "current_taxonomy": {
        "return_cell": "verified local lineage-stable transport compression",
        "six_nine": "receipt-strong surface compression candidate not metric-ready",
        "non_return_cell_transport_family": "not metric-constructible in tested transport-labeled artifacts"
    },
    "next_allowed_steps": [
        "write uniqueness section into paper",
        "define six_nine_surface_metric",
        "search for non_transport compression surfaces",
        "prepare overleaf build"
    ],
    "closed_boundaries": {
        "global_compression_shadow_admitted": False,
        "physical_gravity_claim": False,
        "force_renderer_admitted": False,
        "body_mutation": False,
        "global_uniqueness_claim": False
    },
    "dependency_count": len(deps),
    "check_count": len(checks),
    "failed_check_count": len(failed),
    "failed_checks": failed,
    "checks": checks,
    "source_artifacts": [str(p) for p in deps]
}

out = Path("artifacts/json/g900_force_compression_phase_checkpoint_v3_034.v1.json")
out.write_text(json.dumps(summary, indent=2) + "\n")

print("status", summary["status"])
print("audit_pass", summary["audit_pass"])
print("dependency_count", summary["dependency_count"])
print("check_count", summary["check_count"])
print("failed_check_count", summary["failed_check_count"])
print("phase_statement", summary["phase_statement"])
print("json", out)
