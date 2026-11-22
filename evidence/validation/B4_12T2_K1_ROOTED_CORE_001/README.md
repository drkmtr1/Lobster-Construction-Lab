# B4-12T2-K1-ROOTED-CORE-001 evidence

[Ordinary insertion proof](../../../research/ORDINARY_CUT_LEAF_INSERTION.md) · [Rooted lift proof](../../../research/B4_12T2_K1_ROOTED_CORE.md) · [Configuration](config.json) · [Identity](validation/identity.json) · [Commands](commands.json) · [Reviews](REVIEWS.md) · [Byte manifest](MANIFEST.json)

| Evidence | Inputs | Orders | Result |
|---|---|---|---|
| Retained core-certificate recheck | Exact original [[1],[1],[],[2],[],[]] | 13 | Passed, with crossing spectrum [7,12] at cut 2 |
| New auxiliary core | Exact original [[1],[2],[],[2],[],[]] | 14 | Passed, with s:2=13 and spectrum [7,13] at cut 3 |
| New completed originals | t=3,4,5,6 at K=1 | 18,19,20,21 | All four passed |
| Invalid input probes | True, 3.0, "3", 2 | No graph | Four rejected |

The validator retained each new exact named original and digest
before assigning labels. It rechecked the one retained certificate
against its separately preserved original graph. The actual one-leaf
insertion changes only the second branch of the core, keeps section
2 empty and verifies both cut-crossing spectra. Every target references
the same [new core certificate](validation/core.json). Each direct
partial labeling omits only physical s:5 and has R={6}, D={6}
and actual s:4=12.

The [batch comparison](validation/batch_comparison.json) checks the
same completed t=5 graph by the direct formula, growth in one batch
from t=3, and growth in two batches through the declared t=4.
The two new names have labels 18 and 19. The comparison adds zero
cases. The [independent standard-library audit](audit_result.json)
imports neither production LCL nor the validator. It rebuilds all
the same original graphs and verifies the spectra, physical roots
and witnesses, cut sets, both complements, final edge and growth.
It adds zero cases.

One worker ran the declared campaign with a 21-vertex cap and
2,000,000-byte record cap in CPython 3.13.17 on Windows. The largest
completed record was 7,522 bytes. No solver, computational
enumeration or historical search replay ran. The batch
proof is symbolic; the only cut insertion executed is h=1
on the retained core. [Run summary](validation/summary.json)

The manifest, code identities, proof identities and source snapshots
bind raw bytes. The retained certificate and original require raw
byte equality. The audit allows uniform LF or CRLF comparison only
for retained Markdown. The publication check compares snapshot
bytes exactly to the working source and separately compares the
line-ending-normalized text to the parent Git sources where needed.
Production files and historical evidence stayed unchanged.

For reproduction, use a separate checkout at the recorded parent
and the project-local Python. Copy in the exact current proofs,
config and scripts, leaving the output directory unused. Run the
recorded validation and audit commands from the project root.
The archived outputs are exclusive and remain immutable.
