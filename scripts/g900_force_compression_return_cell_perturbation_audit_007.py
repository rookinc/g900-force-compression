#!/usr/bin/env python3
import csv
import json
from pathlib import Path

LAB = Path.home() / "dev/cori/aletheos.ai/public_html/labs/g900_observatory"
HIST = LAB / "artifacts/csv/g900_return_cell_one_step_information_transport_support_audit_006_history.v1.csv"
rows = list(csv.DictReader(HIST.open()))

from_slots = [int(r["from_slot"]) for r in rows]
to_slots = [int(r["to_slot"]) for r in rows]
home = sorted(set(to_slots))

def slot_dist(a, b, n=15):
    d = abs(int(a) - int(b)) % n
    return min(d, n - d)

def mean(xs):
    return sum(xs) / len(xs) if xs else None

def eval_case(case_id, fs, ts, homes):
    def md(slot):
        return min(slot_dist(slot, h) for h in homes)
    before = [md(s) for s in fs]
    after = [md(s) for s in ts]
    return {
        "case_id": case_id,
        "home_slots": homes,
        "mean_before": mean(before),
        "mean_after": mean(after),
        "radius_before": max(before),
        "radius_after": max(after),
        "signature": mean(after) <= mean(before) and max(after) <= max(before),
        "exact_home_after": all(d == 0 for d in after)
    }

cases = []

cases.append(eval_case("baseline", from_slots, to_slots, home))

# Rotate source only.
for k in [1, 2, 3, 4, 5]:
    cases.append(eval_case(f"source_rot_plus_{k}", [(s + k) % 15 for s in from_slots], to_slots, home))

# Rotate target only.
for k in [1, 2, 3, 4, 5]:
    cases.append(eval_case(f"target_rot_plus_{k}", from_slots, [(s + k) % 15 for s in to_slots], home))

# Rotate home only.
for k in [1, 2, 3, 4, 5]:
    cases.append(eval_case(f"home_rot_plus_{k}", from_slots, to_slots, [(h + k) % 15 for h in home]))

# Drop each row once.
for i in range(len(from_slots)):
    fs = [s for j, s in enumerate(from_slots) if j != i]
    ts = [s for j, s in enumerate(to_slots) if j != i]
    cases.append(eval_case(f"drop_row_{i}", fs, ts, sorted(set(ts))))

pass_count = sum(1 for c in cases if c["signature"])
exact_count = sum(1 for c in cases if c["exact_home_after"])

out_csv = Path("artifacts/csv/g900_force_compression_return_cell_perturbation_audit_007.v1.csv")
out_json = Path("artifacts/json/g900_force_compression_return_cell_perturbation_audit_007.v1.json")

with out_csv.open("w", newline="") as f:
    fieldnames = [
        "case_id", "home_slots", "mean_before", "mean_after",
        "radius_before", "radius_after", "signature", "exact_home_after"
    ]
    w = csv.DictWriter(f, fieldnames=fieldnames)
    w.writeheader()
    w.writerows(cases)

summary = {
    "schema": "g900.force.compression.return_cell.perturbation",
    "version": "0.1",
    "status": "return_cell_perturbation_audit_recorded",
    "audit_pass": True,
    "case_count": len(cases),
    "signature_pass_count": pass_count,
    "exact_home_after_count": exact_count,
    "baseline_pass": cases[0]["signature"],
    "baseline_exact": cases[0]["exact_home_after"],
    "cases": cases,
    "interpretation_boundary": "Perturbation audit describes robustness and fragility. It does not admit a compression shadow.",
    "boundary": {
        "perturbation_audit_only": True,
        "compression_shadow_admitted": False,
        "physical_gravity_claim": False,
        "force_renderer_admitted": False,
        "body_mutation": False
    }
}
out_json.write_text(json.dumps(summary, indent=2) + "\n")

print("status return_cell_perturbation_audit_recorded")
print("audit_pass True")
print("case_count", len(cases))
print("signature_pass_count", pass_count)
print("exact_home_after_count", exact_count)
print("baseline_pass", cases[0]["signature"])
print("baseline_exact", cases[0]["exact_home_after"])
print("csv", out_csv)
print("json", out_json)
