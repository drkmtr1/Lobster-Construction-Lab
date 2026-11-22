# Pinned 1342 all-ledger obstruction evidence

Run identity `B4-1342-ALL-LEDGER-PINNED-OBSTRUCTION-001-20261122`

The recheck uses exactly two distinct graph records, the retained
19-vertex 1342 and retained 15-vertex 1122 originals. The unchanged
original-target verifier accepted both inherited certificates.
Both originals and their complete source chains are retained
by reference, with their raw-file hashes and canonical graph
digests. The associated receipts carry their exact original-edge
ledgers, witnesses, alpha classes and pins. The 1122 positive
control at c=9 has ten selected weights, exactly [5,14].

The [structural receipt](validation/structural.json) gives the
named high-vertex degree and incidence census, the two degree
bounds and all six later hypothetical degree patterns. It also
records the descending premises and the signed all-batch
sum identity. The [proof](../../../research/B4_1342_ALL_LEDGER_PINNED_OBSTRUCTION.md)
covers every candidate ledger and positive batch under the
stated pins. Threshold calculations use only the original
named topology and the three pin values.

One worker, 19 vertices, and 2,000,000 bytes per result bounded
the recheck. Five invalid threshold inputs were rejected before
evaluation. The independent audit adds zero cases. There were
zero solver queries, labeling enumerations, historical replays,
new graphs, new graceful targets, or newly attempted enlarged
graphs. The preceding 2342 assignments remain archived evidence.

## Reproduction in a disposable parent checkout

1. Identify the commit containing this bundle, for example
   with `git log --diff-filter=A --format=%H -- <this-README-path>`
   from a checkout on or after publication.
2. Create a disposable checkout at the recorded parent
   `41f4e42fb73ab87a93abe1f7c348e8442fdd47b7`. Copy the exact Git blobs for
   `research/B4_1342_ALL_LEDGER_PINNED_OBSTRUCTION.md`, and this directory's
   `config.json`, `validate.py` and `audit.py` to their
   original paths, keeping HEAD at the parent. For byte-preserving
   extraction, use Python subprocess to capture `git show <commit>:<path>`
   and pathlib to write the bytes.
3. Leave this task's `validation/` and `audit_result.json`
   absent in that checkout. Preserve archived results intact.
4. From the checkout root use the [documented project-local Python](../../../docs/OPERATIONS.md)
   and run the saved [commands](commands.json) in order, each in its own
   PowerShell process because each ends in `exit $LASTEXITCODE`. The
   validator checks the parent and creates its output directory exclusively.
   The audit reads those outputs and writes its own receipt exclusively.

The [parent-checkout erratum](../../../docs/REPRODUCTION_ERRATA.md)
explains the reproduction distinction. The [identity](validation/identity.json)
and [manifest](MANIFEST.json) bind actual bytes. Production source
comparisons to the parent allow CRLF-to-LF normalization and
are separate from raw hashes of the execution snapshots.

[Summary](validation/summary.json) · [Arithmetic audit](audit_result.json) ·
[Separate reviews](REVIEWS.md)
