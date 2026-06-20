#!/usr/bin/env python3
import json
from pathlib import Path

p001 = Path("artifacts/json/g900_force_compression_return_cell_metric_probe_001.v1.json")
p002 = Path("artifacts/json/g900_force_compression_return_cell_alignment_002.v1.json")
p003 = Path("artifacts/json/g900_force_compression_return_cell_home_contrast_003.v1.json")
p004 = Path("artifacts/json/g900_force_compression_return_cell_home_alignment_theorem_candidate_004.v1.json")

a001 = json.loads(p001.read_text())
a002 = json.loads(p002.read_text())
a003 = json.loads(p003.read_text())
a004 = json.loads(p004.read_text())

checks = {}

checks["001_audit_pass"] = a001.get("audit_pass") is True
checks["001_compression_signature_true"] = a001.get("compression_signature") is True
checks["001_boundary_no_shadow"] = a001.get("boundary", {}).get("compression_shadow_admitted") is False
checks["001_boundary_no_physics"] = a001.get("boundary", {}).get("physical_gravity_claim") is False
checks["001_boundary_no_mutation"] = a001.get("boundary", {}).get("body_mutation") is False

m001 = a001.get("metrics", {})
checks["metric_mean_2_75_to_0"] = (
    m001.get("mean_distance_to_receipt_home_before") == 2.75
    and m001.get("mean_distance_to_receipt_home_after") == 0.0
)
checks["metric_radius_5_to_0"] = (
    m001.get("support_radius_before") == 5
    and m001.get("support_radius_after") == 0
)
checks["metric_size_preserved_3"] = (
    m001.get("support_size_before") == 3
    and m001.get("support_size_after") == 3
)
checks["metric_entropy_preserved_1_5"] = (
    m001.get("support_entropy_before") == 1.5
    and m001.get("support_entropy_after") == 1.5
)

checks["002_audit_pass"] = a002.get("audit_pass") is True
checks["002_homeward_alignment_true"] = a002.get("interpretation", {}).get("homeward_alignment") is True
checks["002_support_shrinkage_false"] = a002.get("interpretation", {}).get("support_shrinkage") is False

checks["003_audit_pass"] = a003.get("audit_pass") is True
checks["003_target_home_exact_after"] = a003.get("target_home_exact_after") is True
checks["003_target_minimal_tested"] = a003.get("target_home_mean_after_minimal_in_tested_set") is True

records = {r["home_id"]: r for r in a003.get("records", [])}
checks["003_source_home_fails"] = records.get("source_home", {}).get("mean_nonincreasing") is False
checks["003_six_nine_pair_fails"] = records.get("six_nine_pair", {}).get("mean_nonincreasing") is False
checks["003_full_return_cell_exact_but_nondiscriminating"] = (
    records.get("return_cell_full", {}).get("exact_home_after") is True
    and records.get("return_cell_full", {}).get("mean_before") == 0.0
)

checks["004_audit_pass"] = a004.get("audit_pass") is True
checks["004_local_only_boundary"] = a004.get("boundary", {}).get("local_theorem_candidate_only") is True
checks["004_no_global_shadow"] = a004.get("boundary", {}).get("global_compression_shadow_admitted") is False
checks["004_no_physics"] = a004.get("boundary", {}).get("physical_gravity_claim") is False
checks["004_no_renderer"] = a004.get("boundary", {}).get("force_renderer_admitted") is False
checks["004_no_mutation"] = a004.get("boundary", {}).get("body_mutation") is False

failed = [k for k, v in checks.items() if not v]

summary = {
    "schema": "g900.force.compression.return_cell.theorem_verify",
    "version": "0.1",
    "status": "return_cell_home_alignment_theorem_verified" if not failed else "return_cell_home_alignment_theorem_not_verified",
    "audit_pass": not failed,
    "verified_statement": "For the admitted return-cell one-step information transport, the source support maps exactly into the admitted target-home slot set under the tested finite slot-distance metric.",
    "source_artifacts": [str(p001), str(p002), str(p003), str(p004)],
    "check_count": len(checks),
    "failed_check_count": len(failed),
    "failed_checks": failed,
    "checks": checks,
    "boundary": {
        "local_theorem_verified_only": not failed,
        "global_compression_shadow_admitted": False,
        "physical_gravity_claim": False,
        "force_renderer_admitted": False,
        "body_mutation": False
    }
}

out = Path("artifacts/json/g900_force_compression_return_cell_theorem_verify_005.v1.json")
out.write_text(json.dumps(summary, indent=2) + "\n")

print("status", summary["status"])
print("audit_pass", summary["audit_pass"])
print("check_count", summary["check_count"])
print("failed_check_count", summary["failed_check_count"])
if failed:
    print("failed_checks", ",".join(failed))
print("json", out)
