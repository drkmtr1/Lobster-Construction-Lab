# Release validation — Lobster Construction Lab v0.1.0

**Disposition: PASSED for the stated bounded software checks.** This report covers the delivered starter implementation and finite evidence, not a proof of universal lobster gracefulness.

## Executed environment and identity

| Item | Observed value |
|---|---|
| Python | CPython 3.12.14 |
| Platform | Linux 6.18.57, x86_64, glibc2.41 |
| NetworkX | 3.7 |
| SymPy / mpmath | 1.14.0 / 1.3.0 |
| z3-solver | 5.4.1.0 |
| Final mathematical/CLI source inventory SHA-256 | `2dfe3231007a18f4a74e4c4b49fd4a112ebbb66ef439e711ff59ac11fde7bbfd` |
| Unit tests | 110 methods, all passed, no optional-engine skips in this environment |
| Recorded unit-test duration | 12.103 seconds in the final run |

Dependencies were installed only in an isolated build environment. Python3.13, Windows11 and Will's physical hardware were **not** executed. Package compatibility research and static launcher review are separate evidence, not Windows validation. No Lean build was performed.

The complete source/config/environment inventory and semantic check summary are in [release_final/summary.json](release_final/summary.json). Every constructive/solver record contains its original graph, restrictions, witness where present, independent checker result, exact configuration and a source snapshot. Source hashes cover executable Python/dependency declarations; the release manifest separately covers packaged documents and evidence.

## What was tested

The suite checks exact original topology/roles, invalid labels, repeated differences, nonlobsters, domain boundaries, restriction scope, incomplete counts, DP state requirements, optional dependency absence, malformed/oversized input admission, immutable attempts, cancellation/caps, source/config/environment mismatch, record tampering and quarantine on bad witnesses.

Independent finite comparisons include **all 125 named trees on five vertices** across DFS/DP/direct permutations, and **120 fixed-core R226 cases across nine tiny targets**. These totals describe those exact test sets, not lobster isomorphism-class coverage. Constructor tests include parameter grids, positive domain boundaries, unsupported inputs, shifted/reflected intervals and independently checked partial/full witnesses. The balanced family has a symbolic proof in addition to finite implementation checks.

The independent reviewer inspected search completeness, DP state sufficiency, original-target/restriction checking and resume integrity. Its reports are `docs/VERIFIER_REVIEW.md`, `docs/SEARCH_REVIEW.md` and `docs/RUN_REVIEW.md`. These are separate AI-assisted mathematical/software reviews, not human peer review or formal proof-assistant certification.

## End-to-end command outcomes

The final `scripts/validate_release.py` invocation ran 14 bounded subprocess commands successfully, followed by the independent B2 negative-control enumeration and semantic assertions. Full command arguments, exit codes and elapsed times are in the summary; raw output is preserved in the adjacent `.log` files.

| Operation | Result and original target | Evidence |
|---|---|---|
| Load H010 example → formula → independent check → save | 14 vertices / 13 edges; valid complete labeling | [demo record](release_final/demo/record.json) |
| Padded two-section composition | 22 vertices / 21 edges; valid complete labeling and supplied interval trace | [composition record](release_final/composed/record.json) |
| Zero-padding balanced supplier, q=2,K=3 | 12 vertices / 11 edges; valid complete labeling, exact prefix state | [balanced record](release_final/balanced/record.json) |
| R226 positive fixed core | Four-vertex path, core labels0,2; constructive valid completion | [allocation record](release_final/allocation/record.json) |
| Unrestricted P4, DFS / DP / permutation oracle | Exact named count4 in all three methods | [DFS](release_final/p4_dfs/record.json), [DP](release_final/p4_dp/record.json), [oracle](release_final/p4_oracle/record.json) |
| P4 with middle labels0,3 | Exact restricted count0; unchanged unrestricted count4 | [restricted record](release_final/p4_restricted/record.json) |
| Six-vertex path | Exact named count24 | [P6 record](release_final/p6_dfs/record.json) |
| Six-vertex spider, legs2,2,1 | Exact named count16 | [spider record](release_final/spider_dfs/record.json) |
| Optional Z3 on P4 | SAT model independently verified; no exact count claimed | [Z3 record](release_final/p4_z3/record.json) |
| Optional NetworkX/SymPy diagnostics | P4 tree structure confirmed; two exact polynomial residuals zero | [diagnostic output](release_final/diagnostics.log) |

## Four B2 finite controls

All four use no direct leaves, K=1, above-side boundaries and **no root-label restriction**. Each uses the original declared physical graph.

| q,r | ell | Forced active/suffix labels | Final finite result |
|---|---:|---|---|
| 1,1 | 1 | `s:2=2`, `s:3=1` | Exhausted restricted negative |
| 1,1 | 2 | `s:2=3`, `s:3=2` | SAT, full witness independently checked |
| 1,2 | 1 | `s:2=2`, `s:3=1` | SAT, full witness independently checked |
| 2,1 | 1 | `s:2=2`, `s:3=1` | Exhausted restricted negative |

The [pilot checkpoint](release_final/pilot/checkpoint.json) identifies the four immutable case records; its [manifest](release_final/pilot/manifest.json) fixes parameters, limits and source/environment identity. The initial limits were four cases, one worker, 50,000 attempted assignments and two seconds per case, 16 vertices, 20 seconds per invocation and 2 MB per attempt. All four decisions completed within those bounds.

The first negative was independently reproduced by the [direct permutation oracle](release_final/b2_negative_oracle/record.json), using at most 40,320 permutations and five seconds. The last negative is finite DFS exhaustion under its declared restriction; it is not advertised as a formal or independently certified nongraceful tree. The first two rows alone demonstrate why a failed fixed return interval cannot be treated as failure of the graph.

Extracted prefixes retain `independent_supplier=false`. The separate balanced constructor's infinite-domain proof comes from its explicit label/difference partition, not from this table.

## Preserved development correction

The first release attempt selected core labels0,1 for an intended positive R226 example. R226 correctly found that fixed core infeasible; the report aggregator then incorrectly assumed a certificate existed. The original evidence and [disposition](release_run/ATTEMPT_DISPOSITION.md) remain preserved. The positive example was changed to core0,2, and the aggregator now handles absent certificates. No checker or mathematical target was weakened.

`release_verified/` records the corrected pre-balanced build. `release_final/` includes the final balanced implementation and is definitive for this release. Earlier evidence is retained with its own source identity.

## Reproduce and limits

From the project root, using its Python environment:

```text
python scripts/validate_release.py --output runs/my_validation_001
```

Choose a new output directory. The script uses a 30-second subprocess stop for each validation command in addition to the engines' own smaller mathematical budgets. Missing optional libraries skip their dedicated unit checks or report unavailable diagnostics; core mathematics remains usable.

Timing/state/output controls are cooperative or structural, not hard OS process containment. Resume is at case boundaries. Hashes detect changed content but are not signatures. Solver exhaustion/UNSAT lacks a separately checked negative proof object. Independent reviews and finite tests can expose defects; they do not certify all future modifications.

The next unequal-prefix seed task is deliberately **not executed** by this validation script. Its inputs and proof duties are ready in `research/NEXT_TASK.md`.

## Fresh-extraction standard-library smoke check

The packaged source was extracted into a separate directory and run with `python -S`, disabling site packages. The H010 demo constructed and independently verified its witness, frontier DP returned the exact P4 count4, and optional NetworkX/SymPy diagnostics correctly reported `UNAVAILABLE`. This verifies that the usable core does not accidentally depend on the installed optional engines. Details are in [EXTRACTION_SMOKE.json](EXTRACTION_SMOKE.json). The extracted executable/dependency source identity matches the final full validation inventory above.
