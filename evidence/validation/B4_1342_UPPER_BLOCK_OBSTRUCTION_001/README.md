# 1342 fixed-ledger upper-block obstruction evidence

Run identity `B4-1342-UPPER-BLOCK-OBSTRUCTION-001-20261122`

## Scope and outcome

The run checks three distinct named originals. They are the
retained 19-vertex 1342 negative control, retained 15-vertex
1122 positive control, and one new attempted 20-vertex 2342
original. The expanded original and digest were saved before
assigning any attempted labels. Its only new vertex and edge
are l:0:0:1 and its attachment to b:0:0.

The positive control supplies ten selected incidences with
multiset [5,14]. Every one of the eight permitted 1342
thresholds fails its selected-incidence premise. The
[all-batch proof](../../../research/B4_1342_FIXED_LEDGER_UPPER_BLOCK_OBSTRUCTION.md)
proves the exact operation fails for every positive batch.
Every h=1 attempt uses the complete vertex alphabet 0..19
and keeps both physical anchor labels and the zero host. The
unchanged checker rejects all eight attempts.

| Threshold | Missing weights, each of multiplicity zero | Repeated weights with multiplicities | Difference sum |
|---:|---|---|---:|
| 11 | 5,7 | 6×2, 10×2 | 194 |
| 12 | 5,10 | 6×2, 11×2 | 192 |
| 13 | 10 | 11×2 | 191 |
| 14 | 10 | 11×2 | 191 |
| 15 | 10,13,15 | 11×2, 14×3 | 191 |
| 16 | 10,13,16 | 11×2, 14×2, 15×2 | 191 |
| 17 | 10,13,17 | 11×2, 14×2, 16×2 | 191 |
| 18 | 18 | 17×2 | 189 |

The required sum for h=1 is 190. The five invalid thresholds
were rejected before evaluating any incidence. The independent
audit reconstructs and checks the same three originals, all
eight thresholds and assignments, the positive control, input
guards, and the symbolic sum coefficients. It adds zero graph
records. The campaign used one worker, 20 vertices and
2,000,000 bytes per result as caps, with zero solver queries,
labeling enumeration or historical replay. It supplies zero
new graceful targets.

## Reproduction in a disposable parent checkout

1. Identify the commit containing this bundle, for example
   by running `git log --diff-filter=A --format=%H -- <this-README-path>`
   from a checkout on or after publication.
2. Create a disposable checkout at the recorded parent
   `c83ae3b11a6bc03189dc44653881137fc014c72a`. Copy the exact Git blobs
   for `research/B4_1342_FIXED_LEDGER_UPPER_BLOCK_OBSTRUCTION.md`
   and this directory's `config.json`, `validate.py` and
   `audit.py` to their original paths without advancing HEAD.
   A byte-capable extraction uses Python subprocess to capture
   `git show <checkpoint>:<path>` and pathlib to write the bytes.
3. Leave this task's `validation/` and `audit_result.json`
   absent in that checkout. Keep the archived evidence intact.
4. Use the [documented project-local Python](../../../docs/OPERATIONS.md)
   from the checkout root and run the saved [commands](commands.json)
   in order, each in its own PowerShell process because each ends in
   `exit $LASTEXITCODE`. The validator checks the parent and creates
   its output directory exclusively. The audit also writes exclusively.

See the [reproduction erratum](../../../docs/REPRODUCTION_ERRATA.md)
for the parent-checkout distinction. The raw
[manifest](MANIFEST.json) and [identity](validation/identity.json)
identify the saved files and execution source snapshots.
Raw hashes use exact bytes. Comparison of production
snapshots to the Git parent permits only CRLF-to-LF normalization.

[Summary](validation/summary.json) ·
[Complete threshold ledgers](validation/thresholds.json) ·
[All-batch coefficients](validation/all_batch_sum.json) ·
[All one-leaf attempts](validation/one_leaf_attempts.json) ·
[Independent audit](audit_result.json) · [AI reviews](REVIEWS.md)
