#!/usr/bin/env python3
import csv
import json
from pathlib import Path

LAB = Path.home() / "dev/cori/aletheos.ai/public_html/labs/g900_observatory"

terms = [
    "058", "059", "060", "061", "062", "063", "064", "065", "066", "067",
    "six_nine", "return_home", "route", "slot", "pair", "target", "union"
]

rows = []

for sub in ["artifacts/csv", "artifacts/json"]:
    d = LAB / sub
    if not d.exists():
        continue
    for p in sorted(d.rglob("*")):
        if not p.is_file():
            continue
        low = str(p.relative_to(LAB)).lower()
        score = sum(1 for t in terms if t in low)
        if score == 0:
            continue

        rec = {
            "path": str(p.relative_to(LAB)),
            "kind": p.suffix.lstrip("."),
            "filename_score": score,
            "read_status": "",
            "fieldnames": "",
            "row_count": "",
            "slot_like_fields": "",
            "pair_like_fields": "",
            "route_like_fields": "",
            "candidate_bridge": False
        }

        try:
            if p.suffix == ".csv":
                with p.open(newline="") as f:
                    reader = csv.DictReader(f)
                    data = list(reader)
                    fields = reader.fieldnames or []
                rec["read_status"] = "csv_read"
                rec["fieldnames"] = ";".join(fields)
                rec["row_count"] = len(data)
                rec["slot_like_fields"] = ";".join([x for x in fields if "slot" in x.lower()])
                rec["pair_like_fields"] = ";".join([x for x in fields if "pair" in x.lower()])
                rec["route_like_fields"] = ";".join([x for x in fields if "route" in x.lower() or "hold" in x.lower() or "step" in x.lower()])
                rec["candidate_bridge"] = bool(rec["slot_like_fields"] or rec["pair_like_fields"])
            elif p.suffix == ".json":
                obj = json.loads(p.read_text())
                if isinstance(obj, dict):
                    fields = sorted(obj.keys())
                else:
                    fields = []
                rec["read_status"] = "json_read"
                rec["fieldnames"] = ";".join(fields)
                rec["row_count"] = ""
                rec["slot_like_fields"] = ";".join([x for x in fields if "slot" in x.lower()])
                rec["pair_like_fields"] = ";".join([x for x in fields if "pair" in x.lower()])
                rec["route_like_fields"] = ";".join([x for x in fields if "route" in x.lower() or "hold" in x.lower() or "step" in x.lower()])
                rec["candidate_bridge"] = bool(rec["slot_like_fields"] or rec["pair_like_fields"] or rec["route_like_fields"])
            else:
                rec["read_status"] = "skipped"
        except Exception as e:
            rec["read_status"] = "error:" + type(e).__name__

        rows.append(rec)

rows.sort(key=lambda r: (not r["candidate_bridge"], -int(r["filename_score"]), r["path"]))

out_csv = Path("artifacts/csv/g900_force_compression_six_nine_slot_history_bridge_012_sources.v1.csv")
out_json = Path("artifacts/json/g900_force_compression_six_nine_slot_history_bridge_012.v1.json")

with out_csv.open("w", newline="") as f:
    fieldnames = [
        "path", "kind", "filename_score", "read_status", "fieldnames",
        "row_count", "slot_like_fields", "pair_like_fields",
        "route_like_fields", "candidate_bridge"
    ]
    w = csv.DictWriter(f, fieldnames=fieldnames)
    w.writeheader()
    w.writerows(rows)

bridge_candidates = [r for r in rows if r["candidate_bridge"]]

summary = {
    "schema": "g900.force.compression.six_nine.slot_history_bridge",
    "version": "0.1",
    "status": "six_nine_slot_history_bridge_sources_recorded",
    "audit_pass": True,
    "source_count": len(rows),
    "candidate_bridge_count": len(bridge_candidates),
    "top_candidates": bridge_candidates[:20],
    "metric_ready": False,
    "next_step": "inspect top bridge candidates for explicit source-to-target slot history",
    "boundary": {
        "bridge_source_search_only": True,
        "slot_history_constructed": False,
        "compression_signature_claim": False,
        "compression_shadow_admitted": False,
        "physical_gravity_claim": False,
        "force_renderer_admitted": False,
        "body_mutation": False
    }
}

out_json.write_text(json.dumps(summary, indent=2) + "\n")

print("status six_nine_slot_history_bridge_sources_recorded")
print("audit_pass True")
print("source_count", len(rows))
print("candidate_bridge_count", len(bridge_candidates))
print("top_candidate", bridge_candidates[0]["path"] if bridge_candidates else "none")
print("metric_ready False")
print("csv", out_csv)
print("json", out_json)
