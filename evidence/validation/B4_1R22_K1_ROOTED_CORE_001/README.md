# B4-1R22-K1-ROOTED-CORE-001 evidence

[Proof](../../../research/B4_1R22_K1_ROOTED_CORE.md) · [Configuration](config.json) · [Identity](validation/identity.json) · [Commands](commands.json) · [Reviews](REVIEWS.md) · [Byte manifest](MANIFEST.json)

| Kind | Exact inputs | Orders | Result |
|---|---|---|---|
| Auxiliary core | [[1],[],[2],[2],[],[]] with s:1=0 | 14 | 1 passed |
| Completed original targets | r=2,3,4,5 with K=1 | 17,18,19,20 | 4 passed |
| Invalid input probes | True, 2.0, "2", 1 | No graph | 4 rejected |
| Named growth comparison | Direct r=4, batch of two from r=2, and two batches through the declared r=3 | Same r=4 original | Pointwise agreement |

The bounded validator saves all five exact original named graphs
and their digests before assigning labels. It uses the unchanged
original-target checker. All four records refer to the same
[fixed core certificate](validation/core.json). The direct prefix
omits only s:5. It records the actual unused complements, physical
port and the sole pending edge before the final assignment.

The [independent standard-library audit](audit_result.json)
reconstructs original names, roles and incidences and recomputes
all spectra, the root condition, the lift, both complements, the
spine witness, and the [batch check](validation/batch_comparison.json).
It imports neither production LCL code nor the validator's formula.
It adds zero cores and zero completed targets. The batch comparison
also adds zero cases. There is no r=1 executable case.

The run used one worker, a 20-vertex cap, and a 2,000,000-byte
result cap in project-local CPython 3.13.17. The largest completed
certificate was 6,734 bytes. There were zero solver queries,
zero computational enumeration, and zero historical search
replays. Production and prior evidence stayed unchanged.

The manifest, proof identity and snapshots bind raw bytes.
For retained Markdown sources only, the audit permits the recorded
digest to match a uniform LF or CRLF version in a differently
configured checkout. It requires raw equality for retained JSON.
The closeout compares snapshots byte-for-byte with the working
source, and to parent source after Git's CRLF-to-LF text comparison
where applicable. The historic raw and bound incomplete-search
records match the parent as raw bytes.

For reproduction, use a separate checkout at the recorded
parent and the project-local Python. Copy the exact active proof,
config, and scripts, leaving the output directory unused. The
[command receipts](commands.json) give the validation and audit
commands. The saved outputs are exclusive and immutable. The
[summary](validation/summary.json) binds the certificates and
batch comparison to their recorded hashes.
