# Independent C(2,3) core and finite checks

The [proof](../../../research/B4_JOINT_23_MAX_ROOTED_CORE.md) derives both zero-neighbor
cases and supplies the fixed Case B ledger directly,
with s:2=15 and s:3=0. The [core original](validation/core-original.json)
was frozen before its [certificate](validation/core.json)
was checked. The [wrong-digest receipt](validation/adverse.json)
records rejection of the deliberately altered binding.

The only other new originals are the two exact lifts,
[order 18](validation/lift-t1-original.json) and
[order 19](validation/lift-t2-original.json). Their
[certificates](validation/lift-t1.json) and
[second-lift receipt](validation/lift-t2.json) retain
the actual singleton R={4}, D={4}, s:4=8 and every
original edge. The [control receipts](validation/controls.json)
recheck C(2,2), C(3,2) and bind the D059 negative to
its prior raw audit. The 49 D059 cut comparisons were
preserved without replay.

The [independent audit](audit_result.json) reconstructs
the named originals and accounts for the scoped Case A
partial failure and 34 host/threshold rows on the new
core. First cuts 6,12,13,14 match and no second cut
matches. The c=12 repeatability proof adds no graph.
Three new graphs, one worker, 0.234375 process-CPU
seconds, zero search queries and zero enumeration nodes.
The 2,000,000-byte record and 10,000,000-byte total caps
were checked. Source and runtime hashes are in
[identity.json](validation/identity.json).

## Reproduction in a disposable parent checkout

1. Identify the commit adding this bundle using Git history.
2. Create a disposable checkout at `98ae0ee75b5afedfd6019a2f79c5da7c9d40c99c`.
   Extract the exact Git blobs for `research/B4_JOINT_23_MAX_ROOTED_CORE.md`,
   `config.json`, `validate.py`, `audit.py` and `commands.json`
   at their recorded paths without advancing HEAD.
3. Leave `validation/` and `audit_result.json` absent.
   From the checkout root, run the [saved commands](commands.json)
   in separate PowerShell processes in the recorded order
   using the [project-local interpreter](../../../docs/OPERATIONS.md).
   A reproduction has its own timing receipts.
4. Preserve the frozen evidence. Parent comparisons of production
   sources normalize CRLF to LF. Runtime snapshots, new inputs,
   and retained source evidence use raw-byte hashes.

[Command receipts](command_receipts.json) ·
[Separate AI reviews](REVIEWS.md) · [Raw-byte manifest](MANIFEST.json)
