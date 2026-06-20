# G900 force compression return-cell robustness profile 008

Status: robustness profile recorded

Result

The return-cell homeward-alignment compression signature is robust but not
absolute.

Perturbation summary

- perturbation cases: 24
- signature pass count: 23
- exact-home-after count: 14
- baseline passed: true
- baseline exact: true

Robust under

- source-slot rotation
- row-order replay
- unique-support replay
- one-row deletion
- moderate target displacement
- moderate receipt-home displacement

Failure observed

The compression signature fails under target_rot_plus_5.

Interpretation

The return-cell compression signature is not a generic artifact of any
perturbation. It has a finite tolerance band.

Compression subtype

bounded homeward alignment compression

Boundary

Robustness profile only.
No global compression shadow admitted.
No physical gravity claim.
No force renderer admitted.
No body mutation.
