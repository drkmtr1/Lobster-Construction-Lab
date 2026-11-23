# B4-K2-D062-TWO-GAP-ORDER-PRESERVING-001 evidence

**EXHAUSTED RESTRICTED NEGATIVE.** All 171 hole pairs and both physical
suffix orders were checked, giving 342 distinct full maps. Of the
171 prefixes, 161 repeat a difference. The remaining ten supply
two unused differences, and neither order consumes both.
The retained original was reused with zero new graph identities.
[Named proof and exact resource table](../../../research/B4_K2_D062_TWO_GAP_ORDER_PRESERVING.md)

## Evidence and interpretation

- `config.json` fixes the model, parent checkpoint, retained target,
  source hashes, and limits. `freeze.json` binds the existing target and
  exact task, archive, production and runtime identities before any
  candidate check. The target is read from D063, leaving its bytes in
  that archive.
- `controls.json` rechecks the D061 seed and independently derived D062
  K=1 labeling against their retained originals. It records the adverse
  digest check, using empty labels to isolate the extra digest error
  without an extra full candidate, and the retained D063 outcome without
  replay. It also gives the original edge order and assigned-edge order.
- `cases.jsonl` has one flushed row per unordered pair. Each contains
  the assigned name-to-label map, assigned weights in the saved edge
  order, physical port, R/D, and both suffix assignments with their
  differences and unchanged checker receipts. Combining the prefix
  map with an ordered suffix yields the full map. Each checker exposes
  the complete difference list in original edge order, and each case
  records missing and repeated weights with multiplicities.
- `result.json` seals the finished case log. The separate standard-library
  `audit.py` reconstructs the named incidences and digest, derives the
  gap labels by successive insertions in rank space, and rechecks the
  same 342 receipts. `audit_result.json` includes the ten valid prefixes
  and the 51 pairs ruled out by weights 18 or 17 as a separate mathematical
  deduction. It skips no cases from the grid.
- `command_receipts.json`, `REVIEWS.md` and `MANIFEST.json` preserve the
  actual commands, independent reviews, and raw-byte identities.

The completed freeze/check/audit sequence used one CPU worker and
0.1875 combined process-CPU seconds. No solver, additional cases,
new graph generation, reruns, or historical replay occurred.
This result applies to the fixed D062 prefix rank order on the
one named original.

## Reproduction

Use a disposable checkout at parent `b0303b9be3ba70de0936e9b942f8044c70a49938`. Copy the
exact Git blob bytes of `config.json`, `commands.json`, `validate.py`
and `audit.py` from the published task to this bundle path with HEAD
still at the parent. The retained target and all archive inputs are
already present at the parent. Leave generated output paths absent.
Use project-local Python 3.12 or 3.13. Run the three commands in
[commands.json](commands.json) once, in order, from the repository root.
Stop on a failure. Occupied output paths stop the scripts. A partial
case log or missing final result or audit is **INCOMPLETE** and must
be preserved without replay. Timings may differ on reproduction.
