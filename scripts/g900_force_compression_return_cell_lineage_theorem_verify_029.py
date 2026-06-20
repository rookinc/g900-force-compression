#!/usr/bin/env python3
import json
from pathlib import Path

p026 = Path("artifacts/json/g900_force_compression_return_cell_lineage_compression_026.v1.json")
p027 = Path("artifacts/json/g900_force_compression_return_cell_lineage_checkpoint_027.v1.json")
p028 = Path("artifacts/json/g900_force_compression_return_cell_lineage_theorem_candidate_028.v1.json")

a026 = json.loads(p026.read_text())
a027 = json.loads(p027.read_text())
a028 = json.loads(p028.read_text())

checks = {
    "026_audit_pass": a026.get("audit_pass") is True,
    "026_lineage_stage_count_3": a026.get("lineage_stage_count") == 3,
    "026_all_stages_preserve_signature": a026.get("all_stages_preserve_signature") is True,
    "026_all_stages_exact_after": a026.get("all_stages_exact_after") is True,
    "026_shared_from_slot_set": a026.get("shared_from_slot_set") is True,
    "026_shared_to_slot_set": a026.get("shared_to_slot_set") is True,
    "027_audit_pass": a027.get("audit_pass") is True,
    "027_failed_zero": a027.get("failed_check_count") == 0,
    "028_candidate_pass": a028.get("audit_pass") is True,
    "028_boundary_no_global_shadow": a028.get("boundary", {}).get("global_compression_shadow_admitted") is False,
    "028_boundary_no_physics": a028.get("boundary", {}).get("physical_gravity_claim") is False,
    "028_boundary_no_renderer": a028.get("boundary", {}).get("force_renderer_admitted") is False,
    "028_boundary_no_mutation": a028.get("boundary", {}).get("body_mutation") is False,
    "028_boundary_no_future_uniqueness": a028.get("boundary", {}).get("future_lineage_uniqueness_claim") is False
}

# Verify exact metric records in 026.
records = a026.get("records", [])
for idx, r in enumerate(records):
    checks[f"026_record_{idx}_from_slot_set"] = r.get("from_slot_set") == "3 6 9"
    checks[f"026_record_{idx}_to_slot_set"] = r.get("to_slot_set") == "9 12 13"
    checks[f"026_record_{idx}_mean_before"] = r.get("mean_before") == 2.75
    checks[f"026_record_{idx}_mean_after"] = r.get("mean_after") == 0.0
    checks[f"026_record_{idx}_radius_before"] = r.get("radius_before") == 5
    checks[f"026_record_{idx}_radius_after"] = r.get("radius_after") == 0
    checks[f"026_record_{idx}_signature"] = r.get("signature") is True
    checks[f"026_record_{idx}_exact_after"] = r.get("exact_after") is True

failed = [k for k, v in checks.items() if not v]

summary = {
    "schema": "g900.force.compression.return_cell.lineage_theorem_verify",
    "version": "0.1",
    "status": "return_cell_lineage_theorem_verified" if not failed else "return_cell_lineage_theorem_failed",
    "audit_pass": not failed,
    "verified_statement": "For the presently known return-cell packet lineage, all three packet stages preserve the same finite homeward-alignment compression signature.",
    "source_artifacts": [str(p026), str(p027), str(p028)],
    "check_count": len(checks),
    "failed_check_count": len(failed),
    "failed_checks": failed,
    "checks": checks,
    "boundary": {
        "local_lineage_theorem_verified_only": True,
        "global_compression_shadow_admitted": False,
        "physical_gravity_claim": False,
        "force_renderer_admitted": False,
        "body_mutation": False,
        "future_lineage_uniqueness_claim": False
    }
}

out = Path("artifacts/json/g900_force_compression_return_cell_lineage_theorem_verify_029.v1.json")
out.write_text(json.dumps(summary, indent=2) + "\n")

print("status", summary["status"])
print("audit_pass", summary["audit_pass"])
print("check_count", summary["check_count"])
print("failed_check_count", summary["failed_check_count"])
print("verified_statement", summary["verified_statement"])
print("json", out)
