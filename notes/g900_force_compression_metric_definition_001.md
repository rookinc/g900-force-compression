# G900 force compression metric definition 001

Question

How should compression be measured inside the G900 apparatus?

Principle

Compression is treated as a finite receipt grammar.
Metrics must be:

- finite
- reproducible
- replayable
- body-preserving
- physics-neutral

Compression metrics

support_size

The number of support elements participating in the receipt.

Interpretation

Smaller support may indicate greater concentration.

support_radius

Maximum graph distance from receipt home to any support element.

Interpretation

Smaller radius may indicate greater concentration.

mean_distance_to_receipt_home

Mean graph distance from receipt home to support elements.

Interpretation

Lower values indicate inward bias.

maximum_distance_to_receipt_home

Largest graph distance from receipt home.

Interpretation

Measures spread boundary.

support_entropy

Entropy of support occupancy across admissible regions.

Interpretation

Lower entropy may indicate concentration.

concentration_ratio

concentration_ratio =
    support_size /
    support_radius

Interpretation

Larger values may indicate denser concentration.

Boundary

Metrics are descriptive only.

Metrics do not imply:

- mass
- energy
- spacetime curvature
- physical gravity
- force generation
