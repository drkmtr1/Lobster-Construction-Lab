# Joint-core crossing-cut compatibility evidence

[Proof](../../../research/B4_JOINT_22_CUT_COMPAT.md) gives the complete cut criterion,
the repeatable c=11 first-center formula and the K=1 lift
for q>=2, fixed r=2 and t>=1. The retained Case A and
Case B controls share one exact named original. The first
is correctly rejected, the second accepted, and a separate
wrong-digest check on B is rejected by the unchanged checker.

The four fixed new graphs are cores q=3 and q=4 and
completed originals (q,t)=(3,1),(4,2). Each original is
saved before its certificate. The batch receipt compares
one first-leaf addition, a batch of two and two successive
unit batches using the same declared cores. Both lifts
return R={6}, D={2} at physical s:4=8, with sole pending
edge s:4--s:5.

The [independent arithmetic audit](audit_result.json) contains
the full named crossing ledger and both the actual and required
spectra at each threshold. It is the sole executable threshold
pass. There are 16 rows for each host on the seed and 17 rows
for the second host on q=3, giving 49 total. First-host cuts
11,12,13 match. No second-host threshold matches on either
tested ledger. These are fixed-ledger results. The recorded
validator and audit used 0.171875 process-CPU seconds combined.
The 2,000,000-byte per-record and 10,000,000-byte total caps
were checked, with zero search queries and zero enumeration.

## Reproduction in a disposable parent checkout

1. Identify the commit introducing this bundle by Git history.
2. Create a disposable checkout at `2d9eb76ea59155a0cfb68b7441dd778467bf475c`.
   Extract the exact Git blobs for `research/B4_JOINT_22_CUT_COMPAT.md`, and this
   directory's `config.json`, `validate.py`, `audit.py`,
   and `commands.json` without advancing HEAD.
3. Leave `validation/` and `audit_result.json` absent.
   Run the [saved commands](commands.json) in order in separate
   PowerShell processes from the repository root using
   [project-local Python](../../../docs/OPERATIONS.md).
   The validator creates its output directory exclusively.
4. Preserve the published evidence. A reproduction has its own
   CPU receipt. The parent source comparison alone normalizes
   CRLF to LF. Execution inputs and snapshots have raw hashes.

[Identity](validation/identity.json) · [Command receipts](command_receipts.json) ·
[Separate reviews](REVIEWS.md) · [Manifest](MANIFEST.json)
