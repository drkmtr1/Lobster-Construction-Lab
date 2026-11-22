# B4-UNPADDED-3111-001 validation

The [conditional zero-port lemma and symbolic family proof](../../../research/ALPHA_ZERO_PORT_LEAF_EXTENSION.md)
and the [concrete 3111 proof](../../../research/B4_UNPADDED_3111.md)
are reviewed separately from the finite executable campaign.

## Completed original targets and same-certificate audit

The configuration fixes 12 lengths for the exact 3111 profile, one
worker, 79 target vertices and 2,000,000 bytes per result. K=64
reaches the vertex cap. The regression retains each original graph
before invoking the constructor. Its records include all three first
leaf attachments, exact prefix labels, both resource inventories,
the physical port, original crossing and suffix, completion trace,
full labels, alpha partition and unchanged verifier results. The
checker passed on all 12 originals.

The standard-library audit independently reconstructs named vertices,
edges and roles, comparing vertex and undirected-edge multiplicities
without requiring storage order. It verifies the exact assignments,
prefix, trace, both inventories and full alpha cut. It passed on
the same 12 saved certificates on its first attempt and adds zero
completed targets. The general-q corollary is symbolic only.

## Separate arithmetic seed

The single 15-vertex prefix certificate uses the exact
`[[3],[1],[1],[1],[]]` graph with labels 0..14, differences 1..14,
low-class size 6, and physical ports b:0:0=0 and s:4=6.
It verifies the witness path, distance at most two and both new
original leaf edges. It is separate from the 12 completed targets.

## Commands and custody

`commands.json` preserves the exact invocations and outputs of 23
passing test methods in four targeted modules, the bounded regression,
its separate audit, the actual K=1 CLI run and the retained H010 demo.
The CLI repeats a declared target. The tests include false certificates,
altered named leaf incidence, different same-size profiles, invalid
parameters, the 79/78 campaign cap and the 10,000/10,001 ceiling
using size preflight for the latter. The inherited byte cap applies
separately. No solver or enumeration campaign ran.

The project-local Windows runtime used `PYTHONUTF8=1`. Versions and
source/configuration identities are in the results. `source/`
freezes implementation, focused-test and dependency declarations.
The CLI/demo retain their own configs and source snapshots.
`REVIEWS.md` records both AI dispositions. `MANIFEST.json` hashes
raw bytes, preserved by `.gitattributes`.
