# B4-UNPADDED-111T-001 validation

The audited theorem concerns the exact original profile
`[[1],[1],[1],[t]]+[[]]*(K+1)` for integers `t>=2,K>=1`. Its proof is
[the project corollary of R241 and L008](../../../research/B4_UNPADDED_111T.md).

## Completed original targets

`config.json` declares the 12 pairs in order, four with K=1 and eight
with K>=2. The regression runs serially, with one worker, a 75-vertex
target cap and 2,000,000 bytes per JSON result. It retains each original
graph before calling the constructor. `regression_result.json` contains
the target, digest, named prefix, interface, partial certificate, adjacent
predicate result, original unfinished and crossing edges, full labeling,
tail differences, singleton alpha cut when applicable, and unchanged
original-target certificate. All 12 passed. The largest target was 75
vertices, on (31,32). `components_result.json` records two certificates
on the same nine-vertex left component, one per construction. They are
separate from the completed targets.

## Independent arithmetic audit

The first `independent_audit.py` attempt exited on target-list ordering.
It listed all spine vertices first, while the builder interleaves their
branches, so an order-sensitive array comparison refused the first
record. The script and failure output are preserved. No construction
record was regenerated. `independent_audit_retry.py` instead compares
sorted named vertices, retaining multiplicity. It reconstructs named
incidences, the exact arithmetic assignments and remaining resources,
and checks all label and difference bijections against the same 12
certificates. The retry passed 12/12. The audit uses no LCL imports and
reports zero additional completed targets.

## Implementation checks and custody

`commands.json` preserves the exact commands and outputs, including
53 passing targeted test methods, both verified CLI examples (2,1) and
(2,2) drawn from the declared set, the retained H010 demo, and the first
audit failure and successful retry. The tests cover the 75/74-vertex
admission boundary and the 10,000/10,001 parameter size preflight.
The 10,000-vertex CLI graph limit gives t+K<=9988. The inherited record
size cap applies separately. The standalone constructor has no CLI size
preflight cap. Solver search, seed enumeration, and solution counting
were outside the task.

`source/` holds raw source and dependency snapshots. Retained test
modules are identified by the starting commit and their commands.
The CLI and demo directories contain their own configurations, source
snapshots and run records. `regression_result.json` records runtime,
source and config hashes, and the audit binds to that original result.
`REVIEWS.md` records the separate AI reviews. `MANIFEST.json` hashes
raw files in this package and `.gitattributes` preserves their bytes.
Finite checks corroborate the quantified symbolic proof.
