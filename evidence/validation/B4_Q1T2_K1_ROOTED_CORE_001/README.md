# B4-Q1T2-K1-ROOTED-CORE-001 evidence

[Proof](../../../research/B4_Q1T2_K1_ROOTED_CORE.md) · [Configuration](config.json) · [Measured identity](validation/identity.json) · [Commands](commands.json) · [Reviews](REVIEWS.md) · [Byte manifest](MANIFEST.json)

The deterministic harness separately retained each exact original named
graph, including its digest, before assigning any labels. The unchanged
original-target verifier checked every saved certificate and the
physical singleton was checked against the actual original s:4--s:5.
The [independent standard-library audit](audit_result.json) rebuilt all
seven named originals and recomputed their spectra, root pins, lift,
both singleton complements and completion. It added zero cases.

| Kind | Parameters | Orders | Outcome |
|---|---|---|---|
| Completed K=1 targets | (2,2), (2,3), (3,2), (4,3) in (q,t) order | 17, 18, 18, 20 | All four passed |
| Auxiliary rooted cores | q=2,3,4 | 14, 15, 16 | All three passed |
| Domain rejection probes | Boolean, float, string, 1, negative for each of q,t | No graph | All ten rejected |

One worker, maximum 20 vertices, maximum 2,000,000 bytes per result,
zero solver queries and zero search enumeration. The largest completed
certificate is 6,149 bytes. The [summary](validation/summary.json)
binds the four certificates to their exact original graphs. Its
auxiliary list is counted independently. The old q=1 ledger is a
comparison source only. The rejected single-cut template is recorded
analytically in the proof. No old campaign or partial run was replayed,
and the prior raw and original-bound DFS records remain INCOMPLETE.

The validator imports only the existing model and checker and snapshots
their exact working bytes, the package initializer and core dependency
metadata. The audit imports neither the validator nor LCL. The raw Git
attributes preserve the frozen evidence and the measured proof.
For a fresh reproduction, start from the recorded parent in a separate
checkout with the project-local Python. Copy in the frozen config, both
scripts and the exact proof, with an unused output directory. Run the
validation and audit commands in that order from the checkout root.
Do not rerun into this archived evidence directory; its outputs are
exclusive. The reproducibility checks add no mathematical quantifiers
to those established by the proof.
