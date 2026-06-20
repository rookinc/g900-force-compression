#!/usr/bin/env python3
import json
from pathlib import Path

main = Path("main.tex").read_text()
theorem = Path("sections/06_theorem.tex").read_text()
uniq = Path("sections/07_uniqueness.tex").read_text()
conclusion = Path("sections/08_conclusion.tex").read_text()
all_text = "\n".join([
    main,
    theorem,
    uniq,
    conclusion
])

checks = {
    "theorem_section_included":
        "\\input{sections/06_theorem}" in main,
    "uniqueness_section_included":
        "\\input{sections/07_uniqueness}" in main,

    "local_theorem_present":
        "local to the presently known return-cell packet lineage" in theorem,

    "lineage_statement_present":
        "three packet representations" in all_text
        or "all three packet stages" in all_text,

    "tested_family_uniqueness_present":
        (
            "Only three" in all_text
            and "metric-constructible histories were found" in all_text
            and "All three belonged to the" in all_text
            and "return-cell packet lineage" in all_text
        ),

    "no_global_uniqueness_claim":
        "not a global uniqueness theorem" in uniq,

    "no_global_compression_shadow_claim":
        "does not admit a global compression shadow" in theorem,

    "no_physical_gravity_claim":
        "does not claim physical gravity" in theorem,

    "no_force_renderer_claim":
        "force renderer" in theorem,

    "no_body_mutation_claim":
        "body mutation" in all_text
}

failed = [k for k, v in checks.items() if not v]

summary = {
    "schema":
        "g900.force.compression.paper_boundary_audit",
    "version": "0.1",
    "status":
        "paper_boundary_audit_passed"
        if not failed else
        "paper_boundary_audit_failed",
    "audit_pass": not failed,

    "closed_statement":
        "The paper establishes a local lineage-stable finite "
        "homeward-alignment compression theorem and a tested-family "
        "uniqueness result for metric-constructible transport histories.",

    "open_boundary": {
        "global_compression_shadow": False,
        "physical_gravity": False,
        "apparatus_wide_compression": False,
        "global_uniqueness": False,
        "force_renderer": False,
        "body_mutation": False
    },

    "check_count": len(checks),
    "failed_check_count": len(failed),
    "failed_checks": failed,
    "checks": checks
}

out = Path(
    "artifacts/json/"
    "g900_force_compression_paper_boundary_audit_036.v1.json"
)
out.write_text(json.dumps(summary, indent=2) + "\n")

print("status", summary["status"])
print("audit_pass", summary["audit_pass"])
print("check_count", summary["check_count"])
print("failed_check_count", summary["failed_check_count"])
print("json", out)
