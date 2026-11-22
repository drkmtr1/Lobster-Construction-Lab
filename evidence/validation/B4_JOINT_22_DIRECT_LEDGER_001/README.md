# Direct named joint-core ledger evidence

Two complete, explicitly constructed candidates are checked
on one frozen [15-vertex original](validation/core_original.json).
[Case A](validation/candidate_A.json) repeats difference 2
and omits 6, and [Case B](validation/candidate_B.json) is
graceful with maximum 14 at physical s:2. The separate
[digest adverse check](validation/adverse.json) reuses B
with a deliberately wrong expected original digest.

The unchanged checker verifies the exact [t=2 original](validation/lift_original.json).
Its [lift receipt](validation/lift.json) records the direct
prefix, both complements, pending original edge, completion,
and four invalid integer inputs. The two [comparison controls](validation/controls.json)
were independently checked without repeating the prior cut
comparisons. There are four graph records, two complete
candidate ledgers, zero solver queries, and zero enumeration
nodes. The prior DFS remains INCOMPLETE.

The [standalone arithmetic audit](audit_result.json) reconstructs
every original and confirms raw custody and the joint CPU total.
The recorded shared arithmetic CPU budget is 30 seconds, with
one worker and 2,000,000 bytes per result. Process CPU excludes
subprocess Git custody operations. Both commands are bounded and
create their output paths exclusively. The [proof](../../../research/B4_JOINT_22_DIRECT_LEDGER.md)
establishes the symbolic lift for fixed q=r=2, K=1 and all exact
integers t>=1.

## Reproduction

1. Locate the commit introducing this bundle by Git history.
2. In a disposable checkout at `e3138ed2804883396fb548f824316155fc859974`,
   copy exact Git blobs for `research/B4_JOINT_22_DIRECT_LEDGER.md` and this directory's
   `validate.py`, `audit.py`, `config.json` and `commands.json`
   to their original paths. Keep HEAD at the recorded parent.
3. Leave `validation/` and `audit_result.json` absent. Run the
   [saved PowerShell commands](commands.json) in order, each
   in a separate process from the repository root with the
   [project-local Python](../../../docs/OPERATIONS.md).
   A reproduction has its own timing receipts.
4. Preserve the published records. Raw retained and runtime
   source hashes are recorded in [identity.json](validation/identity.json).
   Source snapshot comparisons to the parent only normalize CRLF to LF.

[Command receipts](command_receipts.json) ·
[Separate AI reviews](REVIEWS.md) · [Raw-byte manifest](MANIFEST.json)
