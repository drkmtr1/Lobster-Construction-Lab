# B4-1342-UPPER-BLOCK-OBSTRUCTION-001

## Exact retained 1342 state

Use the accepted [normalized formula](B4_1RT2_TWO_HOST_COMPATIBILITY.md#named-normalized-formula)
at r=3,t=4 and the separately saved
[certificate](../evidence/validation/B4_1RT2_TWO_HOST_COMPATIBILITY_001/validation/normalized-r3-t4.json)
and [original](../evidence/validation/B4_1RT2_TWO_HOST_COMPATIBILITY_001/validation/originals/normalized-r3-t4.json).
The ordered profile is `[[1],[3],[4],[2],[]]`. The original
has the five named spine vertices, one center at each of
s:0 through s:3, and ten terminals at those four centers.
Its 18 edges are the four consecutive spine edges, four
attachments, and ten terminal edges. The ledger gives the
spine weights in order and each attachment before its
terminal edges in name-index order.

| Named vertices in order | Labels | Original differences |
|---|---|---|
| s:0,s:1,s:2,s:3,s:4 | 12,7,17,4,10 | 5,10,13,6 |
| b:0:0,l:0:0:0 | 1,13 | 11,12 |
| b:1:0,l:1:0:0,l:1:0:1,l:1:0:2 | 9,6,5,8 | 2,3,4,1 |
| b:2:0,l:2:0:0,l:2:0:1,l:2:0:2,l:2:0:3 | 0,14,15,16,18 | 17,14,15,16,18 |
| b:3:0,l:3:0:0,l:3:0:1 | 11,2,3 | 7,9,8 |

These are precisely the labels 0..18 and differences 1..18,
each once. Every edge has a low endpoint in [0,8] and a
high endpoint in [9,18]. The actual host in this task is
H=L=b:0:0=1. The physical high exit is U=s:4=10, and the
third zero host is Z=b:2:0=0. Thus the state is A(19,9;1,1).
The first host lies on the original witness
b:0:0--s:0--s:1--s:2--s:3--s:4. The first terminal is a
step away. The other centers are one step away via their
spine attachments, with their terminals two steps away.

The [general-host rule](ALPHA_UPPER_BLOCK_GENERAL_HOST.md)
with host label a=1 specializes to the
[label-one rule](ALPHA_UPPER_BLOCK_LEAF_INSERTION.md).
Its strict threshold inequality p+y<c<=n-1 gives exactly
c=11 through 18. In this domain every selected vertex is
high, so no selected edge can meet two selected vertices.
The exit s:4=10 and both low anchors lie below each permitted
threshold. They stay numerically fixed under the operation,
the low class stays of size nine, and the physical exit
keeps offset one.

## Complete selected incidences

For each c take all original edges incident to a vertex
with label at least c. Inspect the complete incidence list
at each high vertex that can be selected:

| Label | Selected high vertex when c is at most the label | Complete incident original edges with weights |
|---:|---|---|
| 11 | b:3:0 | s:3--b:3:0 (7), b:3:0--l:3:0:0 (9), b:3:0--l:3:0:1 (8) |
| 12 | s:0 | s:0--s:1 (5), s:0--b:0:0 (11) |
| 13 | l:0:0:0 | b:0:0--l:0:0:0 (12) |
| 14 | l:2:0:0 | b:2:0--l:2:0:0 (14) |
| 15 | l:2:0:1 | b:2:0--l:2:0:1 (15) |
| 16 | l:2:0:2 | b:2:0--l:2:0:2 (16) |
| 17 | s:2 | s:1--s:2 (10), s:2--s:3 (13), s:2--b:2:0 (17) |
| 18 | l:2:0:3 | b:2:0--l:2:0:3 (18) |

This accounts for all possible incidences by physical
degree and the named graph. At c the selected vertex and
edge lists are exactly the rows labeled c through 18.
Their lists are disjoint because each edge has one high
endpoint. The five incidences always left out are the
four edges at high b:1:0=9 (weights 1,2,3,4) and the
exit edge s:3--s:4 at high s:4=10 (weight 6). Thus every
original edge is classified and none is counted twice.

| c | Complete selected multiset | Actual count | Required multiset | Required count | Match |
|---:|---|---:|---|---:|---|
| 11 | {5} union [7,18] | 13 | [10,18] | 9 | No |
| 12 | {5} union [10,18] | 10 | [11,18] | 8 | No |
| 13 | {10} union [12,18] | 8 | [12,18] | 7 | No |
| 14 | {10} union [13,18] | 7 | [13,18] | 6 | No |
| 15 | {10,13} union [15,18] | 6 | [14,18] | 5 | No |
| 16 | {10,13} union [16,18] | 5 | [15,18] | 4 | No |
| 17 | {10,13,17,18} | 4 | [16,18] | 3 | No |
| 18 | {18} | 1 | [17,18] | 2 | No |

Every entry within a displayed band has multiplicity one.
The evidence gives an explicit named edge ledger for every
threshold. No allowed threshold supplies the rule's complete
incidence premise.

## Obstruction for every positive batch size

Fix any exact integer h>=1. The prescribed operation keeps
old labels below c, shifts old labels at least c by h, and
attaches only l:0:0:j at b:0:0, assigning c+j-1 for
1<=j<=h. The original names and incidences remain, and
adding pendant leaves gives a tree with 18+h edges.
The vertex label bands [0,c-1], [c,c+h-1], and
[c+h,18+h] show that the obstacle is in the edge spectrum.

Each selected old edge has a single shifted high endpoint,
so its difference increases by exactly h. Every other old
difference stays. At the unchanged host label one the fresh
edge weights are c+j-2, with sum h(c-1)+h(h-1)/2.
Write s_c for the actual selected-edge cardinality. The
difference sum after the operation is

```text
171 + h*s_c + h*(c-1) + h*(h-1)/2.
```

A graceful result on the enlarged tree requires total
weight 1+...+(18+h), namely 171+19h+h(h-1)/2.
Subtracting gives the signed discrepancy h*(s_c+c-20).
As h is positive, equality would require s_c=20-c,
the cardinality of [c-1,18]. The signed discrepancy per
unit h is 4,2,1,1,1,1,1,-1 in threshold order.
Each is nonzero. This proves failure of the exact
operation for every positive batch, including operations
attempted without the rule's sufficient hypothesis.

The obstruction concerns this retained ledger, physical
label-one host, operation, thresholds and unchanged exit.
Gracefulness of the enlarged named graph under some other
labeling remains outside this result. The eight h=1
adverse attempts reuse the same original 2342 graph.
They confirm the label alphabet and record the missing and
repeated edge differences. The symbolic sum supplies the
quantifier over h. Prior ordinary coverage for exact
(1,r,t,2) remains as proved by the
[seven-case selector](B4_1RT2_K1_DIRECT_SINGLETON.md#selection-for-all-positive-rtk).

## Positive 1122 control

On the retained original `[[1],[1],[2],[2],[]]`, use the
[retained Q1T2 seed calculation](B4_UNPADDED_Q1T2.md#retained-named-seed-and-full-premise)
and its [saved recheck](../evidence/validation/B4_UNPADDED_Q1T2_001/validation/retained_seed.json).
The state is A(15,7;4,1), with H=L=b:0:0=4 and U=s:4=8
on the same named witness. The eight high vertices have
labels 7..14, the seven lows have 0..6, and the actual
differences are 1..14 once each. Choose c=9. The selected
highs and all their original incidences are:

| Selected high, label | Complete original incidences with weights |
|---|---|
| s:0, 9 | s:0--s:1 (8), s:0--b:0:0 (5) |
| l:0:0:0, 10 | b:0:0--l:0:0:0 (6) |
| b:1:0, 11 | s:1--b:1:0 (10), b:1:0--l:1:0:0 (9) |
| s:2, 12 | s:1--s:2 (11), s:2--s:3 (7), s:2--b:2:0 (12) |
| l:2:0:0, 13 | b:2:0--l:2:0:0 (13) |
| l:2:0:1, 14 | b:2:0--l:2:0:1 (14) |

The four remaining weights are 1,2,3,4, on the fourth
terminal and attachment edges and the exit edge. Thus the
ten selected weights are exactly [c-a,14]=[5,14]. This
one retained recheck verifies the rule can have a complete
premise on a different supplied state. No seed search or
new graceful target is needed.

## Remaining first-branch obligation

A different alpha labeling on the same named 1342
original could supply the missing incidence band while
preserving the host, zero anchor and numerical exit.
That changes only the supplied ledger. A different
insertion interface would also need a new proof of its
shift, full difference partition and suffix resources.
The smaller change is to seek a relabeling of the same
original under the existing interface. This task leaves
that supply question open.

[Bounded evidence](../evidence/validation/B4_1342_UPPER_BLOCK_OBSTRUCTION_001/README.md)
checks the two retained graphs and one new attempted
original without solver calls or labeling enumeration.
