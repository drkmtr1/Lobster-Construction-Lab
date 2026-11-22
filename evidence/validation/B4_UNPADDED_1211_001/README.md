# B4-UNPADDED-1211-001 validation

The [symbolic proof](../../../research/B4_UNPADDED_1211.md) establishes the
result for integer K>=1 on exactly `[[1],[2],[1],[1]]+[[]]*(K+1)`.

## Completed targets and independent audit

The configuration fixes the 12 declared lengths, one worker, a
78-vertex cap, and 2,000,000 bytes per result. K=64 reaches the cap.
`regression_result.json` preserves each original target retained before
construction, both middle-leaf incidences and exact labels, the checked
prefix and its two inventories, the physical port and crossing edge,
each path step, the completed labels, the alpha classes, and the
result from the unchanged original-target checker. All 12 passed.

`independent_audit.py` uses only the standard library. It reconstructs
the named graph and compares named vertex and undirected-edge
collections with multiplicity, independently of storage order. It
checks each label, original incidence, both inventories, and the full
alpha cut. Its saved result binds to the original regression and
covers the same 12 certificates. It passed on the first attempt and
adds zero completed targets.

## Separate auxiliary certificates

- `relabelled_component_result.json` certifies one nine-vertex
  left component and records the two within-class exchanges and
  before/after edge differences.
- `left_component_result.json` certifies one expanded ten-vertex
  left component, the new leaf edge and the physical ports and
  witness distances.
- `seed_result.json` certifies one fourteen-vertex fixed seed with
  low-class size 7 and the two returned ports.

The three are separate from the 12 completed targets. The reflected
L008 right component is checked algebraically in the proof.

## Commands, environment and custody

The project-local Python ran with `PYTHONUTF8=1`. Runtime identity and
raw source and configuration hashes are in the result records.
`commands.json` preserves exact commands and outputs from 61
passing targeted test methods in 13 modules, the completed-target
regression, the arithmetic audit, the K=1 CLI case and the retained
H010 demo. The CLI case repeats a declared target. Targeted tests
cover the retained B4/B3/B2 and consumer behavior, and exercise
admission at the 78/77-vertex campaign cap and the 10,000/10,001
default ceiling using size preflight for the latter. The record
byte cap applies separately. No solver, enumeration or solution
counting campaign ran.

`source/` freezes the implementation, focused test and dependency
declarations. Retained tests are identified by the accepted base
and their command paths. The CLI and demo save separate configs and
source snapshots. `REVIEWS.md` records both AI dispositions.
`MANIFEST.json` hashes raw file bytes, preserved by `.gitattributes`.
