# B4-2222-NONADJACENT-ALL-K-001 evidence

**ACCEPT** ordinary gracefulness of the exact named
`[[2],[2],[2],[2]]+[[]]*(K+1)` for every exact integer K≥2.
The [proof](../../../research/B4_2222_NONADJACENT_ALL_K.md) uses the independent D066
alpha prefix and strong induction, including the bridge from the
new zero to the reflected tail. The theorem concerns the physical
B4 port s:4. The unchanged production graph wrapper still checks
the B2 names at s:2.

## Bounded evidence

| K | Original | Order | Physical s:4 | Ordered pending weights |
|---|---|---:|---:|---|
| 2 | Retained D066 control | 19 | 11 | 2,1 |
| 3 | New | 20 | 12 | 3,1,2 |
| 4 | New | 21 | 13 | 4,1,2,3 |
| 5 | New | 22 | 14 | 5,3,4,2,1 |
| 8 | New | 25 | 17 | 8,6,7,5,3,4,2,1 |

The validator checked exactly five complete certificates with the
unchanged verifier. The retained P was rechecked arithmetically
against its archived original, graph and label-ledger identities.
Four new originals were frozen before the full checks. No K=1 target
was generated. The wrong-digest control uses an empty labeling on the
retained original and is separate from the five full certificates.
The wrong path, wrong D and K=1 contract were rejected by actual calls
to the B4 evidence harness. The audit reconstructs both graph families
and the saved suffixes using the standard library alone. Its bottom-up
recurrence reflects the entire smaller path.

The single official sequence used one worker and 0.171875 combined
process-CPU seconds. It used zero feasibility queries, zero enumeration
nodes and no historical replay. The audit rechecked the same five
certificates and added zero cases. The finite table corroborates the
proved recurrence at its three bases and two recursive examples.

## Bundle and reproduction

`INTAKE.md`, `config.json` and `freeze.json` record the authorized
scope, archived provenance, exact original references, runtime and
script identities. `k{K}_original.json` contains each new original.
`k{K}_certificate.json` binds each result to the proper original,
listing assigned labels and inventories, actual suffix and checker
receipt for every named edge. `prefix_control.json`, `adverse.json`,
`result.json`, and [audit_result.json](audit_result.json) preserve the
rechecks and exact counts. Commands, reviews and the raw-byte manifest
are in the same bundle. The retained B2 proof has a declared checkout
CRLF conversion. Its canonical Git and actual raw hashes are both
recorded, and all other pinned input files match their Git blobs
byte for byte.

Use a disposable checkout at parent `c0dc9245616eb5b43dca14af2605473ead1a99d5`. Copy
the exact Git blob bytes of `INTAKE.md`, `config.json`,
`commands.json`, `validate.py`, `audit.py` and the task proof
to their recorded paths without advancing HEAD. The retained input
archives are already present. Leave generated output paths absent.
Run the three commands in [commands.json](commands.json) once, in order,
with project-local Python 3.12 or 3.13 from the repository root.
Stop on a failure and preserve partial evidence as INCOMPLETE.
Runtime timings can differ.
