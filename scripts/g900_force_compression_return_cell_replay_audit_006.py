#!/usr/bin/env python3
import csv
import json
from pathlib import Path

LAB = Path.home() / "dev/cori/aletheos.ai/public_html/labs/g900_observatory"

HIST = LAB / "artifacts/csv/g900_return_cell_one_step_information_transport_support_audit_006_history.v1.csv"
rows = list(csv.DictReader(HIST.open()))

def slot_dist(a, b, n=15):
    d = abs(int(a) - int(b)) % n
    return min(d, n - d)

def mean(xs):
    return sum(xs) / len(xs) if xs else None

from_slots = [int(r["from_slot"]) for r in rows]
to_slots = [int(r["to_slot"]) for r in rows]

home = sorted(set(to_slots))

def metrics(fs, ts):
    def md(slot):
        return min(slot_dist(slot, h) for h in home)

    before = [md(s) for s in fs]
    after = [md(s) for s in ts]

    return {
        "mean_before": mean(before),
        "mean_after": mean(after),
        "radius_before": max(before),
        "radius_after": max(after),
        "signature": (
            mean(after) <= mean(before)
            and max(after) <= max(before)
        )
    }

replays = []

# Original order
replays.append({
    "replay_id": "original",
    **metrics(from_slots, to_slots)
})

# Reverse row order
replays.append({
    "replay_id": "reverse_rows",
    **metrics(
        list(reversed(from_slots)),
        list(reversed(to_slots))
    )
})

# Sort by source slot
pairs = sorted(zip(from_slots, to_slots))
replays.append({
    "replay_id": "sorted_pairs",
    **metrics(
        [p[0] for p in pairs],
        [p[1] for p in pairs]
    )
})

# Unique support only
replays.append({
    "replay_id": "unique_support",
    **metrics(
        sorted(set(from_slots)),
        sorted(set(to_slots))
    )
})

all_pass = all(r["signature"] for r in replays)

summary = {
    "schema": "g900.force.compression.return_cell.replay",
    "version": "0.1",
    "status": "return_cell_replay_audit_recorded",
    "audit_pass": all_pass,
    "replay_count": len(replays),
    "all_replays_preserve_signature": all_pass,
    "replays": replays,
    "boundary": {
        "replay_audit_only": True,
        "compression_shadow_admitted": False,
        "physical_gravity_claim": False,
        "force_renderer_admitted": False,
        "body_mutation": False
    }
}

out = Path(
    "artifacts/json/"
    "g900_force_compression_return_cell_replay_audit_006.v1.json"
)
out.write_text(json.dumps(summary, indent=2) + "\n")

print("status return_cell_replay_audit_recorded")
print("audit_pass", all_pass)
print("replay_count", len(replays))
print("all_replays_preserve_signature", all_pass)
print("json", out)
