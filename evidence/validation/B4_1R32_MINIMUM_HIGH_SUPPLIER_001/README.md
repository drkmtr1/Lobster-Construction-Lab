# B4-1R32-MINIMUM-HIGH-SUPPLIER-001 evidence

[Proof](../../../research/B4_1R32_MINIMUM_HIGH_SUPPLIER.md) · [Configuration](config.json) · [Identity](validation/identity.json) · [Commands](commands.json) · [Reviews](REVIEWS.md) · [Byte manifest](MANIFEST.json)

| Check | Exact scope | Orders | Outcome |
|---|---|---|---|
| Retained seed recheck | 1232 seed, r=2 at third size three | 17 | Passed |
| New normalized prefixes | r=3,4,5 | 18,19,20 | All three passed |
| New completed originals | (r,K)=(3,2),(3,3),(4,4),(5,5) | 20,21,23,25 | All four passed |
| Invalid probes | The eight declared typed pairs | No graph | All eight rejected |

Both completed r=3 originals reference the same normalized
certificate. The validator saves the exact original profile,
names, incidences and digest before applying any labeling.
The unchanged checker verifies each completion. Before
using the unchanged numeric helper, the harness checks both
inventory complements, the updated cut p=r+6, physical s:4
and the only unfinished original path from s:4.

The [normalized batch comparison](validation/batch_comparison.json)
uses the retained r=2 seed, the saved r=3 and r=4 intermediate
prefixes, and the same saved r=5 final prefix. Direct labels,
one batch of three and three unit batches agree, including labels
8,9,10 on the new names. Each saved intermediate checks its
updated alpha cut, both physical hosts and the witness.
No additional target or prefix is created.

The [independent standard-library audit](audit_result.json)
imports neither production LCL nor the validator. It reconstructs
the exact named graphs, checks edge multiplicities before using
edge-key dictionaries, and verifies the spectra, alpha predicates,
physical anchors, witness distances, both complements, the
original suffix and the same comparison. The audit adds zero
graph cases. [Run summary](validation/summary.json)

One worker ran under a 25-vertex limit and 2,000,000-byte result
cap in project-local CPython 3.13.17 on Windows. The largest
completed record was 7,671 bytes. No solver, computational
labeling enumeration, historical search replay or production
edit occurred. The historical limited DFS retains its
INCOMPLETE status and raw bytes.

Proof, configuration, scripts, snapshots and generated evidence
bind raw bytes. Retained JSON matches as raw bytes; only retained
Markdown can be compared with uniform LF or CRLF in another
checkout. Publication checks separately compare the exact snapshot
to working source and normalized text to the parent Git source.

To reproduce, start at the recorded parent in a separate checkout
with project-local Python. Copy in the exact proof, scripts and
configuration. Leave the output directory unused and run the
recorded commands in order from the project root. The archived
outputs are exclusive and remain immutable.
