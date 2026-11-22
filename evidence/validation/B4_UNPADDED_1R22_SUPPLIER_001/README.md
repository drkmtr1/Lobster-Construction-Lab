# B4-UNPADDED-1R22-SUPPLIER-001 evidence

[Proof](../../../research/B4_UNPADDED_1R22_SUPPLIER.md) · [Config](config.json) · [Identity](validation/identity.json) · [Commands](commands.json) · [Reviews](REVIEWS.md) · [Byte manifest](MANIFEST.json)

| Kind | Exact inputs | Orders | Result |
|---|---|---|---|
| Completed original targets | (r,K)=(2,2),(2,3),(3,4),(4,5) | 18,19,21,23 | 4 passed |
| Normalized prefixes | r=2,3,4 | 16,17,18 | 3 passed |
| Retained controls | 1122 adjacent and nonadjacent diagnostic ledgers | 15 each | 2 passed their original certificates; neither supplies the fixed lower-block premise |
| Invalid input probes | True, 2.0, "2", and 1 separately for r and K | No graph | 8 rejected |

The bounded runner holds every new exact named original and digest
before assigning labels. It reuses the same normalized r=2 certificate
in both r=2 completions, checks both complements and the exact physical
s:4 path before calling the retained numeric helper, and verifies
each full certificate with the unchanged original-target checker.

The [independent audit](audit_result.json) reconstructs names, roles
and original edge multiplicities, calculates spectra, checks the
normalized cut, ports and witness, recomputes both complements
and verifies the recurrence on the same completed cases. It adds zero
targets and zero prefixes. The [retained checks](validation/retained.json)
also record the complete incident spectra at every cut on the same
two old certificates. These checks and the intake inspection do not
rerun their original searches or discover any new seed.

One worker, 23 vertices and 2,000,000 bytes per record were the declared
limits. The largest completed certificate was 7,028 bytes. Both
validation programs ran once and passed in project-local CPython
3.13.17. No solver call, labeling enumeration, broad suite or
historical replay ran. The new fixed r=1 ledger is checked
algebraically in the proof and separate review and is outside the
finite campaign. The [summary](validation/summary.json) lists all
completed certificates and their hashes.

For reproduction, use a separate checkout at the frozen parent and
the project-local Python. Copy in the exact proof, config and two
scripts and start with an unused output directory. Run the validation
and audit commands from the repository root. The saved outputs in this
directory are exclusive and remain immutable. The source snapshots
cover the model, original-target checker, numeric consumer, package
initializer and dependency metadata. Production files are unchanged.
