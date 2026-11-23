# B4-K2-D062-TWO-EDGE-TRANSPORT-001

## Exact source and original target

Use the independently supplied alternative D061 core from
[the original](../evidence/validation/B4_JOINT_22_DIRECT_LEDGER_001/validation/core_original.json)
and [its named certificate](../evidence/validation/B4_JOINT_SECOND_CENTER_CUT_READY_22_001/validation/alternative-r2.json).
The [D062 proof](B4_JOINT_NESTED_CUT_TWO_HOST.md#exact-k1-zero-host-lift)
has h=k=0 at q=r=2. Translate the seed by one and restore the
original third center b:2:0 with label zero. Its two terminals
get 16 and 17, with the actual attachment s:2--b:2:0 of
weight 15. The K=1 named original is reused from the
[D058 archive](../evidence/validation/B4_JOINT_22_DIRECT_LEDGER_001/validation/lift_original.json).
The archive supplies its topology. The labels come from the
D062 formula above.

| Named row | F labels | Actual differences |
|---|---|---|
| s:0 through s:5 | 14, 1, 15, 4, 10, 11 | 13, 14, 11, 6, 1 |
| b:0:0 and its terminals | 2, 12, 9 | 12, 10, 7 |
| b:1:0 and its terminals | 3, 6, 7 | 2, 3, 4 |
| b:2:0 and its terminals | 0, 16, 17 | 15, 16, 17 |
| b:3:0 and its terminals | 13, 5, 8 | 9, 8, 5 |

The spine differences follow consecutive edges. Each branch row
lists the attachment first and its terminal incidences in named
order. The two spectra are [0,17] and [1,17]. The K=1 original
digest is `1e9734225ebec5d92882fa276792b21af7abd8142652472fc9daf772b5431495`.

The only target is `[[2],[2],[2],[2],[],[],[]]`. Its seven spine
vertices and four groups of three branch vertices give 19 vertices.
It contains all 17 K=1 edges and the original final edge s:5--s:6.
Withholding s:5 and s:6 leaves 17 assigned vertices and 16 assigned
edges. The exact pending path is s:4--s:5--s:6, with sole
assigned-to-unassigned edge s:4--s:5. All branch edges are assigned.
The original spine witnesses every vertex within distance two.

## Complete model and resource test

For each integer c in [0,18], map every old label x to
x + 1 when x≥c and to x otherwise. This is the strictly
increasing bijection from [0,17] onto [0,18] minus {c}.
Withholding old s:5 and the fresh s:6 leaves label complement
R={c,G_c(s:5)} with two distinct values. Each possible completion
of this fixed prefix has one of two assignments to those named
vertices. Order A places G_c(s:5) at s:5, and order B places c
there. Both use every target label once. These 19 thresholds
times two orders exhaust the prescribed model. There is no
symmetry quotient or early exit.

An observed edge of old weight w gains one exactly when its
old endpoints straddle c. The old prefix weights are [2,17].
Any old crossing weight w with successor w+1 still unshifted
creates a duplicate at w+1. Conversely a duplicate can occur
only when these two consecutive weights receive increments
one and zero respectively. Hence the prefix is valid exactly
when the crossing prefix weights form a final segment [d,17],
where d=18 denotes an empty segment. Its difference inventory
then omits exactly {1,d}. In a rejected prefix the audit also
records the exact set of missing values and the repeated
multiplicities. The two suffix edges cannot repair a repetition
already on the prefix.

With p=G_c(s:4) and a=G_c(s:5), order A gives the two edge weights
(|p-a|,|a-c|) and order B gives (|p-c|,|a-c|). The relevant
complement is in the target alphabet [1,18]. For either order,
a valid prefix completes exactly when the multiset of those
two named weights equals its unused set D. Thus order B receives
its own check even when A fails.

Order A is the named instance of the [accepted one-cut criterion](B4_JOINT_22_CUT_COMPAT.md#named-seed-and-the-complete-cut-condition)
on all of F, with host physical s:5 carrying old label 11.
It retains the original s:4--s:5 edge after the shift and
attaches just s:6 at s:5. The new weight is d0=|a-c|,
equal to c-11 when c>11 and to 12-c otherwise. The full old
crossing spectrum must therefore be [d0,17], with the empty
tail interpreted literally. The auditor checks equivalence
to the A verdict separately on each of the same 19 thresholds.
Order B relocates the old s:5 value to s:6, so the original
s:4--s:5 edge must be recomputed.

The frozen K=1 prefix has p=10, R={11,18} and D={1,18}.
Placing 11 then 18 gives weights (1,7). Placing 18 then 11
gives (8,7). Neither equals D. This is also the unshifted
endpoint c=18 of the grid.

## Exhausted restricted negative

All 38 label bijections fail the difference test. The complete prefix
test below displays repeated values with their multiplicities. For the
eight rows with no repetition, neither suffix weight pair equals D as
a multiset. The other eleven thresholds already repeat a difference
on the assigned original edges. The full case log gives each named
edge and the missing and repeated values for each completed assignment.

| c | Physical s:4 | R | D | Repeated prefix differences | A weights in path order | B weights in path order |
|---:|---:|---|---|---|---|---|
| 0 | 11 | {0,12} | {1,18} | — | (1,12) | (11,12) |
| 1 | 11 | {1,12} | {1,15} | — | (1,11) | (10,11) |
| 2 | 11 | {2,12} | {1,2,13} | 3 (×2) | (1,10) | (9,10) |
| 3 | 11 | {3,12} | {1,2,7,10,12} | 3 (×2), 8 (×2), 11 (×2) | (1,9) | (8,9) |
| 4 | 11 | {4,12} | {1,3,7,10,12} | 5 (×2), 8 (×2), 11 (×2) | (1,8) | (7,8) |
| 5 | 11 | {5,12} | {1,3,6,9} | 5 (×2), 8 (×2) | (1,7) | (6,7) |
| 6 | 11 | {6,12} | {1,3,6} | 5 (×2) | (1,6) | (5,6) |
| 7 | 11 | {7,12} | {1,4,6} | 5 (×2) | (1,5) | (4,5) |
| 8 | 11 | {8,12} | {1,6} | — | (1,4) | (3,4) |
| 9 | 11 | {9,12} | {1,5} | — | (1,3) | (2,3) |
| 10 | 11 | {10,12} | {1,5,8} | 7 (×2) | (1,2) | (1,2) |
| 11 | 10 | {11,12} | {1,5,8} | 6 (×2) | (2,1) | (1,1) |
| 12 | 10 | {11,12} | {1,5,8} | 6 (×2) | (1,1) | (2,1) |
| 13 | 10 | {11,13} | {1,5,8,11} | 6 (×2), 10 (×2) | (1,2) | (3,2) |
| 14 | 10 | {11,14} | {1,11} | — | (1,3) | (4,3) |
| 15 | 10 | {11,15} | {1,11,14} | 12 (×2) | (1,4) | (5,4) |
| 16 | 10 | {11,16} | {1,16} | — | (1,5) | (6,5) |
| 17 | 10 | {11,17} | {1,17} | — | (1,6) | (7,6) |
| 18 | 10 | {11,18} | {1,18} | — | (1,7) | (8,7) |

The weights in this table can be reproduced by testing each old
edge from the named F ledger at its original label endpoints: if the
lower endpoint is x and the higher is y, increase its old weight
precisely at integer c in [x+1,y]. Compute the two suffix weights
separately on s:4--s:5 and s:5--s:6. The [independent arithmetic audit](../evidence/validation/B4_K2_D062_TWO_EDGE_TRANSPORT_001/audit_result.json)
recalculates these increments, the explicit edge-weight multisets, and
the ordinary one-cut equivalence. Thresholds c=11 and c=12 happen to
exchange the same two full label maps, so 38 prescribed cases examine
36 distinct full maps. Both cases were retained in both orders.

The result rejects this exact single-gap transport of the independently
supplied F, with either placement of its two leftover labels. Ordinary
gracefulness for T under a different labeling, or K≥2 continuations
from a different interface, remains open here.
