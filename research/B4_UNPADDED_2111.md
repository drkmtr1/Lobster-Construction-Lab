# B4-UNPADDED-2111-001

For every integer K >= 1, excluding booleans, the exact unpadded
profile `[[2],[1],[1],[1]]+[[]]*(K+1)` admits an explicit alpha
graceful labeling.

## Original graph and prefix inventories

There are K+5 consecutive spine vertices `s:0,...,s:(K+4)`, four
centers `b:i:0` attached to the respective `s:i`, and five terminal
leaves. The two leaves `l:0:0:0` and `l:0:0:1` both attach to
`b:0:0`. The order is K+14 and the K+4 spine edges, four attachments
and five terminal edges give m=K+13. The prefix contains all four
branches and spine indices 0 through 4, hence 14 vertices and 13
edges. Only `s:5,...,s:(K+4)` remain unassigned. Their incident edges
are exactly the K original consecutive spine edges from `s:4`,
with sole prefix-crossing edge `s:4--s:5`.

| Named vertices, in order | Supplied labels, in order |
|---|---|
| `s:0,s:1,s:2,s:3,s:4` | K+12,2,K+9,5,K+6 |
| `b:0:0,l:0:0:0,l:0:0:1` | 0,K+11,K+13 |
| `b:1:0,l:1:0:0` | K+10,1 |
| `b:2:0,l:2:0:0` | 3,K+8 |
| `b:3:0,l:3:0:0` | K+7,4 |

The low vertices in order of label are `b:0:0,l:1:0:0,s:1,b:2:0,l:3:0:0,s:3`,
using 0..5. The eight high vertices in order are
`s:4,b:3:0,l:2:0:0,s:2,b:1:0,l:0:0:0,s:0,l:0:0:1`, using K+6..K+13.
The classes are disjoint and exhaust the prefix. In particular the root
has label m-1 and the second first-branch leaf has label m.
The spine alternates classes, each attachment joins opposite classes,
and all terminal leaves are opposite their centers. Subtraction on the
actual prefix edges gives the following differences.

| Original edge | Difference |
|---|---:|
| `s:3--s:4` | K+1 |
| `s:3--b:3:0` | K+2 |
| `b:3:0--l:3:0:0` | K+3 |
| `s:2--s:3` | K+4 |
| `b:2:0--l:2:0:0` | K+5 |
| `s:2--b:2:0` | K+6 |
| `s:1--s:2` | K+7 |
| `s:1--b:1:0` | K+8 |
| `b:1:0--l:1:0:0` | K+9 |
| `s:0--s:1` | K+10 |
| `b:0:0--l:0:0:0` | K+11 |
| `s:0--b:0:0` | K+12 |
| `b:0:0--l:0:0:1` | K+13 |

The table counts four spine, four attachment and five terminal edges,
each once. Subtracting the used labels from 0..m and the used differences
from 1..m gives R=[6,K+5] and D=[1,K]. The active vertex is physical
`s:4=K+6`, one above the upper endpoint.

## Unit skeleton and the prescribed leaf

Use the accepted [B4-unit fixed prefix](B4_UNPADDED_UNIT.md#retained-r241l008-derivation-of-the-fixed-seed).
This skeleton stops at `s:4` and has no unfinished suffix vertices.
To derive it, cut its original `s:2--s:3` edge. The left component B
has spine labels (8,2,5) and center/leaf pairs (0,7), (6,1), (3,4).
These cover 0..8, with low class 0..3. The two spine differences are
6,3 and the branch pairs are (8,7), (4,5), (2,1). Every edge crosses
the cut and the spectrum is 1..8. Its actual ports
`L_B=b:0:0=0` and `U_B=s:2=5` have offsets (0,1) since n_B=9 and
p_B=4. The path `b:0:0--s:0--s:1--s:2` witnesses B. Its first leaf
and other centers are one edge away and the other terminal leaves
are two edges away.

Right component A starts with L008 at branch size one and zero
padding, with `s:3,l:3:0:0,b:3:0,s:4` labeled 0,1,2,3.
Reflect the low class by x -> 1-x and the high class by x -> 5-x.
Each high-minus-low difference d becomes 4-d, so 1..3 is
preserved. On `s:3,s:4,b:3:0,l:3:0:0` this gives (1,2,3,0).
The original `s:3--s:4` edge witnesses A, with center and leaf at
distances one and two. With n_A=4 and p_A=2, its actual ports
`L_A=s:3`, `U_A=s:4` have offsets (1,0).
[L008 archive](../references/upstream/bounded/research__LEMMAS.md.archive.md)
· MDL_Bounded_Search `e48b94eec4091b4fe189e325cab2eda464409943`,
`research/LEMMAS.md`, line 21

R241 applies at x_A=y_B=1, restoring exactly `s:2--s:3`. Adding
p_B=4 to A and n_A=4 to B highs, with B lows fixed, gives label
blocks [0,3], [4,5], [6,7], [8,12]. The differences are A's 1..3,
connector (5+4)-(1+4)=4, and B's 5..12. The output spine is
(12,2,9,5,6) and center/leaf pairs are (0,11), (10,1), (3,8),
(7,4). The returned physical ports are `b:0:0=0` and `s:4=6`.
The witnesses concatenate to `b:0:0--s:0--s:1--s:2--s:3--s:4`,
which keeps every vertex within distance two.
[R241 and disposition](../references/upstream/mdl/N241_relational_ports.md)
· MDL `858a8c1fcfda87ba40bb1adee498a6131504a803`,
`research/candidates/volume-010.md`, lines 4364–4405 and 4488–4505

On this skeleton add exactly the required terminal `l:0:0:1` at
the original center `b:0:0=0` and assign label 13. This adds
difference 13 on that edge and keeps all old labels, incidences
and differences. The new high label preserves low-class size 6
and the physical port. The new leaf is one edge from the witness
because its center is on the path. The resulting 14-vertex
arithmetic seed uses 0..13 and differences 1..13. Raising its
eight high labels by K increases every original prefix difference
by K and gives the displayed formula.

## Adjacent path and alpha cut

For the original suffix write `w_j=s:(4+j)`, 0<=j<=K. The retained
[above-side adjacent consumer](PROOF_OBLIGATIONS.md#active-endpoint-above-the-interval)
starts at the given high port and uses the lowest remaining label
first, then the highest, alternating. Taking a low endpoint leaves
the new port immediately below the remaining interval, and taking
a high endpoint leaves it immediately above. The existing
`_consume_suffix` starts at index 4 on the branch-free suffix.

Odd steps j=2i+1 assign 6+i, using [6,5+ceil(K/2)] in increasing
order. Positive even steps j=2i assign K+6-i, using
[6+ceil(K/2),K+5] in decreasing order. These disjoint ranges exhaust
R, with the second empty at K=1. An odd step follows label K+6-i
(including the given port at i=0), so its difference is K-2i.
An even step follows label 6+i-1, so its difference is K-2i+1.
Each equals K-j+1, using D exactly once in descending order. There
are exactly K suffix assignments to the previously unassigned
vertices, and every prefix label is preserved.

The prefix lows and odd suffix positions use 0..p-1, with
p=6+ceil(K/2). The prefix highs and even suffix positions use
p..K+13. The prefix crosses the cut and the suffix alternates
across it from high `s:4`. Thus every original edge crosses and
the labeling is alpha. Its numerical alpha cutoff is p-1.
At K=1, R={6}, D={1}, `s:4=7`, and `s:5=6`. The fixed seed has
low-class size 6 and the completed labeling has low-class size 7
(cutoff 6).

## Scope

This is a project corollary on the exact ordered profile with zero
padding and integer K >= 1. The fixed prefix seed is an auxiliary
arithmetic object. The public constructor starts at K=1. The proof
uses the label-zero extension of the unit skeleton. The [discarded
port template](FAILED_HYPOTHESES.md#f-b4-2111-port-template) has a
separate, narrow obstruction. The bounded certificates corroborate
the implementation. Historical novelty, other profiles and arbitrary
repetition are outside the claim.
