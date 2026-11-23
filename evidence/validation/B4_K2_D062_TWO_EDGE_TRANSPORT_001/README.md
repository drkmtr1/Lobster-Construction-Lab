# B4-K2-D062-TWO-EDGE-TRANSPORT-001 evidence

**EXHAUSTED RESTRICTED NEGATIVE.** One frozen named original, 19 thresholds,
and both orders at each threshold. Eleven prefixes repeat a difference.
The two suffix orders miss the required inventory on each of the remaining
eight. Every full case uses the complete label alphabet. The named proof
and result table are in [the task proof](../../../research/B4_K2_D062_TWO_EDGE_TRANSPORT.md).

## Records and custody

- `config.json` fixes the exact original profile, model, limits and archive
  identities. `target_original.json` and `freeze.json` were written before
  any certificate check for the target. The freeze receipt binds the
  original, task source, unchanged verifier, runtime and archive bytes.
- `controls.json` records the independently supplied D061/D062 seed and the
  D062 (K=1,t=2) labeling on the reused archived original. It records the
  frozen-prefix failure and the wrong-digest control. The digest probe
  used empty labels to isolate its additional checker error without
  a 39th full assignment.
- `candidates.jsonl` has one raw row per threshold with both ordered
  assignments, all named edges, full inventories and original-bound
  checker receipts. `result.json` binds these rows and records completion.
- `audit_result.json` independently reconstructs the named original and
  verifies those same saved candidates. It records both missing and
  repeated weights for each order. This audit adds zero cases.
- `command_receipts.json`, `REVIEWS.md`, and `MANIFEST.json` record the
  exact invocations, separate reviews, and raw-byte identities.

The sole new graph has 19 vertices and 18 edges. Both retained originals
were reused. Each of the 38 cases was evaluated as prescribed, including
both end cuts and c=11. There were 26 elementary control assertions
across checker and independent audit, 0.140625 combined process-CPU
seconds, zero solver queries, and no rerun or additional parameter.

The assigned old weight (w) gains one precisely when its original label
endpoints straddle the cut. The assigned-edge spectrum is distinct if
and only if the shifted old weights form a final segment of (2..17).
The missed target weights are then ({1,d}), where (d) is the start
of that segment and (d=18) for an empty segment. Compute the suffix
differences on the actual original edges with both orders. This is a
test of the fixed transport operation.

## Reproduction

Use a disposable checkout at parent `2e558bc9f13c2437e381272360452e9ff2de3646`. Copy exact
Git blob bytes for `config.json`, `commands.json`, `validate.py` and
`audit.py` from the commit containing this bundle, at their recorded paths,
without advancing HEAD. The archived sources are already present at the
parent. Leave all generated output paths absent in the disposable checkout.
Use project-local Python 3.12 or 3.13 and execute the three commands in
[commands.json](commands.json) once, in order, from the repository root.
The commands first freeze the target, then check it, then audit the saved
rows. Runtime timings can differ. Preserve the archived bundle.
Occupied output paths stop execution. A partial JSONL log or a missing
final result or audit receipt is incomplete evidence for exhaustion.
Preserve it and stop without relaunching the task.
