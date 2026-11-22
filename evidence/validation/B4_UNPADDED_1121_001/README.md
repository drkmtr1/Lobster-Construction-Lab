# B4-UNPADDED-1121-001 validation

The [symbolic proof](../../../research/B4_UNPADDED_1121.md) covers
integer K>=1 on exactly `[[1],[1],[2],[1]]+[[]]*(K+1)`. The files
here record bounded checks of its implementation.

## Original targets and arithmetic audit

`config.json` fixes the 12 path lengths and limits. The regression uses
one worker, a 78-vertex cap, and 2,000,000 bytes per result. K=64 reaches
78 vertices. `regression_result.json` holds each caller-retained original
graph, exact prefix, adjacent boundary check, both inventories, original
crossing edge, K completion steps, complete labels, alpha classes and
original-target checker result. Each case passed. The unchanged checker
consumes the retained original graph. The regressions verify that both
named leaves of the third branch stay on their original center and
carry their prescribed labels.

`independent_audit.py` uses no LCL imports. It reconstructs each named
target and compares vertex and undirected edge collections with
multiplicity, independently of storage order. It checks the exact
named assignments, both inventories, preserved prefix, original path
incidences, label and difference bijections, and alpha classes.
`independent_audit_result.json` binds to the same 12 saved target
certificates. It passed on the first attempt and adds zero targets.

## Separately checked component and seed

`left_component_result.json` records one original 10-vertex component
certificate, its alpha cut, actual witness path and the distance of each
vertex from it. `seed_result.json` records one independent 14-vertex
fixed-prefix certificate with low-class size 6 and the two returned
physical ports. Neither is included in the 12 completed-target count.
The other R241/L008 ingredients were checked symbolically in the proof.

## Implementation checks and custody

`commands.json` records exact commands and outputs. 57 targeted
test methods passed, including four new methods and compatibility
checks of B4, B3, B2 and the retained nonadjacent consumer. The K=1
CLI run repeats a declared target. The H010 demo is a compatibility gate.
Admission tests exercise the 78/77 case cap and the default graph
ceiling using the size preflight at K=9986 and K=9987. The 10,000-vertex
ceiling and the inherited record-size cap remain distinct. Solver
search, enumeration and solution counting were outside the run.

The intake-only `lcl context` command needed `PYTHONUTF8=1` on Windows
because its default code page could not encode the state file's U+2265.
It was rerun successfully with UTF-8. All validation commands use
`PYTHONUTF8=1`.

`source/` freezes implementation, dependency and focused-test bytes.
Retained test modules are identified by the starting commit and exact
command paths. CLI and demo runs retain their own configs and source
snapshots. `REVIEWS.md` records the two separate AI dispositions.
`MANIFEST.json` hashes the raw bytes of this package and
`.gitattributes` preserves those bytes.
