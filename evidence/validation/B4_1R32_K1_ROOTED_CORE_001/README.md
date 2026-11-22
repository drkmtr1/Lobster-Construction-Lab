# 1R32 K=1 rooted core validation

Run identity: B4-1R32-K1-ROOTED-CORE-001-20261121

Accepted parent: 648ec01f4eaca4a8f71aa162f057a870485dd93c

## Bounds and results

The search-free harness passed one retained 14-vertex core recheck,
three new auxiliary cores of orders 15, 16, 17, and three completed
original K=1 targets of orders 19, 20, 21. Each completed target binds
the core for its own r by hash. The six new records use r=3, 4, 5.
The four invalid inputs were rejected before any graph was built.
One worker, at most 21 vertices and 2,000,000 bytes per result were
declared. No solver, labeling enumeration or historical replay ran.

The independent audit rechecks the seven same records and the four
rejection records. Both r=5 batch comparisons reuse the declared
records and their intermediate cut states. The audit, comparisons and
reviews add zero cases.

## Reproduction and custody

From the repository root in PowerShell using the documented
project-local Python, run the commands in
[commands.json](commands.json). Use a disposable checkout of the
published source with the new output paths free. The validator and
audit write fresh outputs, preserving these saved results. The
configuration freezes the declared cases and limits.

The [validation summary](validation/summary.json) links exact saved
certificates. The [identity record](validation/identity.json)
identifies the runtime, runner, audit, configuration, proof, production
source snapshots, retained input and historical receipts by raw SHA-256.
New evidence and the new proof have explicit Git byte-preservation
attributes. Audit comparisons to retained Markdown allow solely uniform
LF or CRLF variation and keep those comparisons distinct from raw hash
matches. The saved retained JSON and evidence manifest use raw bytes.
See the [audit](audit_result.json), [growth records](validation/growth_comparison.json),
[AI reviews](REVIEWS.md) and [manifest](MANIFEST.json).

The quantified argument and the six-case selector are in the
[proof](../../../research/B4_1R32_K1_ROOTED_CORE.md). Executable evidence
instantiates the three declared r values only. The distinct historical
DFS receipt remains INCOMPLETE with reason max_nodes.
