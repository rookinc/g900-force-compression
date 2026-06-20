#!/usr/bin/env python3
import json
from pathlib import Path

deps = [
    Path("artifacts/json/g900_force_compression_return_cell_checkpoint_009.v1.json"),
    Path("artifacts/json/g900_force_compression_six_nine_return_home_probe_010.v1.json"),
    Path("artifacts/json/g900_force_compression_metric_readiness_011.v1.json"),
    Path("artifacts/json/g900_force_compression_six_nine_slot_history_bridge_012.v1.json"),
    Path("artifacts/json/g900_force_compression_six_nine_bridge_inspect_013.v1.json"),
    Path("artifacts/json/g900_force_compression_six_nine_bridge_inspect_014.v1.json"),
    Path("artifacts/json/g900_force_compression_six_nine_surface_slotset_015.v1.json"),
    Path("artifacts/json/g900_force_compression_surface_taxonomy_016.v1.json"),
]

loaded = {p.name: json.loads(p.read_text()) for p in deps}

checks = {
    "009_return_cell_checkpoint_pass": loaded[deps[0].name].get("audit_pass") is True,
    "009_local_signature_verified": loaded[deps[0].name].get("theorem_status", {}).get("replay_stable") is True,
    "010_six_nine_probe_pass": loaded[deps[1].name].get("audit_pass") is True,
    "010_six_nine_metric_not_ready": loaded[deps[1].name].get("compression_relevance", {}).get("metric_ready") is False,
    "011_readiness_pass": loaded[deps[2].name].get("audit_pass") is True,
    "011_metric_ready_count_one": loaded[deps[2].name].get("metric_ready_count") == 1,
    "012_bridge_search_pass": loaded[deps[3].name].get("audit_pass") is True,
    "012_candidate_bridge_count_positive": loaded[deps[3].name].get("candidate_bridge_count", 0) > 0,
    "013_sparse_bridge_recorded": loaded[deps[4].name].get("audit_pass") is True,
    "014_candidate_rows_recorded": loaded[deps[5].name].get("audit_pass") is True,
    "014_slot_sets_abundant": loaded[deps[5].name].get("nonempty_parsed_slot_row_count", 0) > 0,
    "015_surface_slotset_pass": loaded[deps[6].name].get("audit_pass") is True,
    "015_dominant_expanded_gap": loaded[deps[6].name].get("dominant_class") == "expanded_surface_with_gap",
    "016_taxonomy_pass": loaded[deps[7].name].get("audit_pass") is True,
}

failed = [k for k, v in checks.items() if not v]

summary = {
    "schema": "g900.force.compression.phase_checkpoint",
    "version": "0.1",
    "status": "compression_phase_checkpoint_passed" if not failed else "compression_phase_checkpoint_failed",
    "audit_pass": not failed,
    "phase_statement": "Project 32 has one local replay-stable bounded homeward-alignment compression result and one distinct six-nine surface compression candidate taxonomy.",
    "local_results": {
        "return_cell_transport": "verified_local_replay_stable_bounded_homeward_alignment_compression_signature",
        "six_nine_return_home": "receipt_strong_surface_rowset_candidate_not_metric_ready"
    },
    "taxonomy": {
        "return_cell": "transport_compression",
        "six_nine": "surface_compression_candidate"
    },
    "next_allowed_steps": [
        "define_surface_metric_for_six_nine",
        "search_other_metric_ready_transports",
        "write_methods_section_from_001_to_017",
        "update_appliance_force_candidate_copy_without_renderer"
    ],
    "closed_boundaries": {
        "global_compression_shadow_admitted": False,
        "physical_gravity_claim": False,
        "force_renderer_admitted": False,
        "body_mutation": False,
        "global_force_definition_complete": False
    },
    "dependency_count": len(deps),
    "check_count": len(checks),
    "failed_check_count": len(failed),
    "failed_checks": failed,
    "checks": checks,
    "source_artifacts": [str(p) for p in deps]
}

out = Path("artifacts/json/g900_force_compression_phase_checkpoint_017.v1.json")
out.write_text(json.dumps(summary, indent=2) + "\n")

print("status", summary["status"])
print("audit_pass", summary["audit_pass"])
print("dependency_count", summary["dependency_count"])
print("check_count", summary["check_count"])
print("failed_check_count", summary["failed_check_count"])
print("phase_statement", summary["phase_statement"])
print("json", out)
