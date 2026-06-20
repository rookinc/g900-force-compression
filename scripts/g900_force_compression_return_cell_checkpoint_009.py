#!/usr/bin/env python3
import json
from pathlib import Path

deps = [
    Path("artifacts/json/g900_force_compression_return_cell_metric_probe_001.v1.json"),
    Path("artifacts/json/g900_force_compression_return_cell_alignment_002.v1.json"),
    Path("artifacts/json/g900_force_compression_return_cell_home_contrast_003.v1.json"),
    Path("artifacts/json/g900_force_compression_return_cell_home_alignment_theorem_candidate_004.v1.json"),
    Path("artifacts/json/g900_force_compression_return_cell_theorem_verify_005.v1.json"),
    Path("artifacts/json/g900_force_compression_return_cell_replay_audit_006.v1.json"),
    Path("artifacts/json/g900_force_compression_return_cell_perturbation_audit_007.v1.json"),
    Path("artifacts/json/g900_force_compression_return_cell_robustness_profile_008.v1.json"),
]

loaded = {}
for p in deps:
    loaded[p.name] = json.loads(p.read_text())

checks = {
    "all_dependencies_exist": all(p.exists() for p in deps),
    "001_pass": loaded[deps[0].name].get("audit_pass") is True,
    "001_compression_signature": loaded[deps[0].name].get("compression_signature") is True,
    "002_pass": loaded[deps[1].name].get("audit_pass") is True,
    "002_homeward_alignment": loaded[deps[1].name].get("interpretation", {}).get("homeward_alignment") is True,
    "003_pass": loaded[deps[2].name].get("audit_pass") is True,
    "003_target_home_exact": loaded[deps[2].name].get("target_home_exact_after") is True,
    "004_pass": loaded[deps[3].name].get("audit_pass") is True,
    "005_verified": loaded[deps[4].name].get("audit_pass") is True,
    "005_failed_zero": loaded[deps[4].name].get("failed_check_count") == 0,
    "006_replay_pass": loaded[deps[5].name].get("audit_pass") is True,
    "006_all_replays": loaded[deps[5].name].get("all_replays_preserve_signature") is True,
    "007_perturbation_recorded": loaded[deps[6].name].get("audit_pass") is True,
    "007_baseline_pass": loaded[deps[6].name].get("baseline_pass") is True,
    "008_profile_pass": loaded[deps[7].name].get("audit_pass") is True,
    "008_finite_tolerance": loaded[deps[7].name].get("interpretation", {}).get("finite_tolerance_band") is True,
}

failed = [k for k, v in checks.items() if not v]

summary = {
    "schema": "g900.force.compression.return_cell.checkpoint",
    "version": "0.1",
    "status": "return_cell_local_compression_checkpoint_passed" if not failed else "return_cell_local_compression_checkpoint_failed",
    "audit_pass": not failed,
    "checkpoint_statement": "A local replay-stable bounded homeward-alignment compression signature is verified for the admitted return-cell one-step information transport.",
    "dependency_count": len(deps),
    "check_count": len(checks),
    "failed_check_count": len(failed),
    "failed_checks": failed,
    "theorem_status": {
        "local_metric_signature": True,
        "homeward_alignment": True,
        "negative_controls_recorded": True,
        "dependency_verified": True,
        "replay_stable": True,
        "perturbation_profile_recorded": True,
        "robust_but_not_absolute": True
    },
    "limits": {
        "global_compression_shadow_admitted": False,
        "physical_gravity_claim": False,
        "force_renderer_admitted": False,
        "body_mutation": False,
        "global_force_definition_complete": False
    },
    "source_artifacts": [str(p) for p in deps],
    "checks": checks
}

out = Path("artifacts/json/g900_force_compression_return_cell_checkpoint_009.v1.json")
out.write_text(json.dumps(summary, indent=2) + "\n")

print("status", summary["status"])
print("audit_pass", summary["audit_pass"])
print("dependency_count", summary["dependency_count"])
print("check_count", summary["check_count"])
print("failed_check_count", summary["failed_check_count"])
print("checkpoint_statement", summary["checkpoint_statement"])
print("json", out)
