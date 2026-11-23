# B4-K2-D062-S4-ADJACENT-RANK-001 evidence

**EXHAUSTED RESTRICTED NEGATIVE** on templates L and R for the one
retained D063 original. Each template has 171 hole pairs and both
physical suffix orders, giving 684 distinct full maps. The sole valid
prefix belongs to L with R={11,12}, D={1,7}, and s:4=9. Its two orders
give (2,1) and (3,1). R repeats an assigned difference at every pair.
[Proof, including the named-edge obstruction for R](../../../research/B4_K2_D062_S4_ADJACENT_RANK.md)

## Raw records

- [pre-run.md](pre-run.md) states the exact named restriction and derives
  the 18/17 conditions before numerical execution. No case was pruned.
- `config.json` fixes the unchanged original, both rank exchanges,
  sole parameter tuple, hard limits, attachment hash, 27 pinned
  archive inputs, and production source hashes. `freeze.json` binds
  these inputs, pre-run proof, commands, scripts, and runtime before
  evaluation. The original stays in the D063 archive.
- `controls.json` records the D061 seed and derived D062 lift, as well
  as D063 and D064 receipts without replay. It gives the two named
  template orders and actual original edge orders. The wrong-digest
  control uses the retained target with an empty label map to isolate
  the digest error. The malformed label control duplicates s:4's label
  at s:5 on the retained K=1 source, producing a zero-weight edge.
  Neither control adds a model case.
- `cases-L.jsonl` and `cases-R.jsonl` each contain 171 flushed rows.
  A row combines the exact prefix map, port, R, D, prefix edge weights
  and repetitions with both suffix orders, their full checker difference
  receipts in original edge order, and missing and repeated weights.
  The full named map is the recorded prefix plus the two suffix values.
  `result.json` seals both logs and records complete case coverage.
- [audit_result.json](audit_result.json) independently reconstructs
  the original incidences and digest, both rank exchanges, the same
  full maps, and both inventories. It corroborates 51 extreme-hole
  failures per template and adds zero cases or graph identities.
- The command receipts, separate AI reviews and raw-byte manifest
  preserve exact execution and evidence provenance.

One official run used one CPU worker and 0.296875 combined
process-CPU seconds. No solver, graph generation, base grid replay,
early exit, or additional cases occurred.

## Reproduction

Use a disposable checkout at parent `af9077e17bb720fb9da268d4dcb72f801ea41ccf`. Copy
exact Git blob bytes of `config.json`, `commands.json`, `pre-run.md`,
`validate.py` and `audit.py` from the published task into their recorded
paths without advancing HEAD. The retained inputs are already present
at the parent. Leave generated output paths absent. Run the commands
in [commands.json](commands.json) once in order from the repository root
with project-local Python 3.12 or 3.13. Stop on any failure. A partial
JSONL or missing final result or audit receipt is **INCOMPLETE**. Preserve
the partial evidence without retrying. Runtime timings may differ.
