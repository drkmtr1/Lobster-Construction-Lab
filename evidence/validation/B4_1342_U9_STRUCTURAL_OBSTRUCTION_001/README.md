# 1342 adjacent-exit structural obstruction evidence

Run identity `B4-1342-U9-STRUCTURAL-OBSTRUCTION-001-20261122`

[Claim A and Claim B](../../../research/B4_1342_U9_STRUCTURAL_OBSTRUCTION.md) are analytic.
The arithmetic harness uses only two distinct retained originals.
The U=10 1342 certificate is an identity and previous-result
control. The 1122 control at a=4, U=8, c=9 still supplies [5,14].
Both rechecks use the unchanged original-target verifier. The
separate arithmetic audit reconstructs their named incidences.

The [structural receipt](validation/structural.json) records all
63 pairs, the full degree and neighborhood census and each
of the six residual named contradictions. The harness visits
512 subsets of nine eligible physical highs once, recording
57 exclusions and one selected set for each surviving pair.
The audit checks these results analytically from the mandatory
and optional highs. It also records 45 arithmetic checks of
the difference-count recurrence, including batches whose new
difference interval extends above 18. Those checks exercise
the arithmetic without creating any graph or labeling.

The [summary](validation/summary.json) records one worker,
order at most 19, and 2,000,000 bytes per result. Fifteen typed
and range [rejections](validation/invalid_inputs.json) all stop
before evaluation. There were zero new graph records, solver
queries, graceful-label enumeration, historical search replays,
new graceful certificates, or insertion attempts.

## Reproduce in a disposable parent checkout

1. Locate the commit introducing this bundle with
   `git log --diff-filter=A --format=%H -- <this-README-path>`.
2. Create a disposable checkout at `3ac2ccc91d28063e89ebd21bf3ec5bf525f72992`.
   Copy the exact Git blobs for `research/B4_1342_U9_STRUCTURAL_OBSTRUCTION.md` and this directory's
   `config.json`, `commands.json`, `validate.py` and `audit.py` to
   their recorded paths with a byte-capable extraction. Keep HEAD
   at the recorded parent. Leave this task's `validation/` and
   `audit_result.json` absent.
3. From the repository root, use the [project-local
   Python](../../../docs/OPERATIONS.md) and execute the
   [recorded commands](commands.json) in order in separate
   PowerShell processes. The first command checks the parent
   and creates an exclusive output directory. The second reads
   those outputs and writes its audit receipt exclusively.
4. Preserve the archived evidence unchanged. The
   [parent-checkout erratum](../../../docs/REPRODUCTION_ERRATA.md)
   explains the distinction between source and execution checkout.

[Source and runtime identity](validation/identity.json) ·
[Command receipts](command_receipts.json) · [Audit](audit_result.json) ·
[Separate AI reviews](REVIEWS.md) · [Raw-byte manifest](MANIFEST.json)

Retained control and task-input comparisons use raw bytes.
Production source snapshots retain raw execution hashes. Their
separate comparisons to the parent normalize CRLF to LF.
