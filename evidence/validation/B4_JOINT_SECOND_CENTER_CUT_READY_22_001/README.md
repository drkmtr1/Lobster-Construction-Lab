# Cut-ready alternative C(2,2) evidence

The [proof](../../../research/B4_JOINT_SECOND_CENTER_CUT_READY_22.md) directly supplies an
alternative ledger on the retained named C(2,2) original.
The [seed receipt](validation/alternative-r2.json) verifies
physical s:2=14, s:1=0 and second host b:1:0=2. The
[adverse test](validation/adverse.json) reuses this ledger
with a deliberately wrong original digest and is rejected.

The [independent audit](audit_result.json) records the
complete actual and required spectra at all 16 thresholds
0..15, including the endpoint comparisons. Only c=13
matches. It also checks the updated cuts 14 and 15 on
the distinct r=3 ledger and r=4 output. The independent
C(2,3) control and one-leaf second-growth output share the
same original. [Batch data](validation/batches.json) compare
one two-leaf batch with two unit batches in the named
terminal order.

Only the [r=4 core](validation/r4-original.json) and
[r=4,t=2 lift](validation/r4-t2-original.json) are new
named original graph records. Their orders are 17 and
20. The [lift receipt](validation/r4-t2.json) preserves
R={11}, D={1}, the actual exit s:4=10 and sole pending
edge s:4--s:5. The [retained controls](validation/controls.json)
verify two positives and bind the D059 fixed-ledger
negative without replay. The separate r=3 first-growth
corollary uses a symbolic proof and contributes no graph.

The two scripts used one worker and 0.171875 process-CPU
seconds. Zero queries, labeling enumeration, retries or
new dependencies. The per-result 2,000,000-byte and total
10,000,000-byte caps apply. [Runtime and source
identity](validation/identity.json) binds the execution.

## Reproduce in a disposable parent checkout

1. Locate the introducing commit in Git history.
2. Create a disposable checkout at `ea444f9ae68505596fc3cc84dbdb2e848eeec446`.
   Copy exact Git blobs for `research/B4_JOINT_SECOND_CENTER_CUT_READY_22.md` and this directory's
   `config.json`, `commands.json`, `validate.py` and
   `audit.py` to the recorded paths without advancing HEAD.
3. Leave `validation/` and `audit_result.json` absent.
   From the repository root run the [saved commands](commands.json)
   in order, each in a separate PowerShell process with
   [project-local Python](../../../docs/OPERATIONS.md).
4. Keep the historical evidence frozen. Production snapshot
   comparisons to the parent alone normalize CRLF to LF.
   Task inputs, snapshots and retained evidence use raw hashes.
   Reproduction has its own timings.

[Command receipts](command_receipts.json) ·
[Separate AI reviews](REVIEWS.md) · [Raw-byte manifest](MANIFEST.json)
