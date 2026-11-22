# B4-1RT2-TWO-HOST-COMPATIBILITY-001

## Original seed and supplied hosts

The [independent 1232 seed](B4_12T2_ZERO_HOST_SUPPLIER.md#original-seed-and-direct-ledger)
on `[[1],[2],[3],[2],[]]` has five spine vertices, four
original centers at s:0 through s:3, and eight terminals at
their prescribed centers. The complete ledger, rechecked
against the [retained certificate](../evidence/validation/B4_12T2_ZERO_HOST_SUPPLIER_001/validation/normalized-t3.json)
and its [original](../evidence/validation/B4_12T2_ZERO_HOST_SUPPLIER_001/validation/originals/normalized-t3.json),
is as follows. Within each branch row, the attachment comes first,
then the terminal edges by name index.

| Named vertices | Labels | Actual original differences |
|---|---|---|
| s:0,s:1,s:2,s:3,s:4 | 11,7,16,4,9 | 4,9,12,5 |
| b:0:0,l:0:0:0 | 1,12 | 10,11 |
| b:1:0,l:1:0:0,l:1:0:1 | 8,6,5 | 1,2,3 |
| b:2:0,l:2:0:0,l:2:0:1,l:2:0:2 | 0,13,14,15 | 16,13,14,15 |
| b:3:0,l:3:0:0,l:3:0:1 | 10,2,3 | 6,8,7 |

The labels exhaust 0..16 and the differences exhaust 1..16, each
once. The lows are s:1,s:3,b:0:0,b:2:0 and the four second and
fourth terminals, using 0..7. Every listed edge crosses to a high.
Thus the seed supplies `A(17,8;1,1)` with `L=b:0:0=1`,
`U=s:4=9`, `H=b:1:0=8`, and `Z=b:2:0=0`.
All four anchors are distinct. The original path
`b:0:0--s:0--s:1--s:2--s:3--s:4` is W.
The first terminal is one step from W. Centers 1, 2 and 3
are one step from W through their spine attachments, and
their terminals are two steps away. In particular both hosts
meet their distance-one premise.

## Named normalized formula

For exact integers r>=3,t>=4 apply the
[two-host lemma](ALPHA_MINIMUM_HIGH_ZERO_HOST_COMPATIBILITY.md)
with h=r-2 and k=t-3. At H use the names l:1:0:j for
2<=j<r, whose one-based new-name index is j-1.
At Z use l:2:0:j for 3<=j<t, whose one-based new-name
index is j-2. A leaf attaches only to its named center.
The exact enlarged prefix is `[[1],[r],[t],[2],[]]` with
the following direct formula.

| Named vertices | Normalized labels in the same order |
|---|---|
| s:0,s:1,s:2,s:3,s:4 | r+9,7,r+14,4,r+7 |
| b:0:0,l:0:0:0 | 1,r+10 |
| b:1:0,l:1:0:0,l:1:0:1 | r+6,6,5 |
| l:1:0:j, 2<=j<r | j+6 |
| b:2:0 | 0 |
| l:2:0:j, 0<=j<3 | r+11+j |
| l:2:0:j, 3<=j<t | r+12+j |
| b:3:0,l:3:0:0,l:3:0:1 | r+8,2,3 |

The original s:2 carries r+14. Continuing the old third-terminal
formula at j=3 would duplicate it, so the new indices begin at
r+15. The two original second-terminal labels remain 6,5
in their original name order.

The new order is r+t+12. The old lows use [0,7], followed by
the new H leaves [8,r+5], the shifted old highs [r+6,r+14],
and the fresh Z leaves [r+15,r+t+11]. These disjoint consecutive
bands give both the full bijection and the low and high sizes
r+6 and t+6. The new H edges have weights r-j for 2<=j<r,
using [1,r-2]. The original 16 weights increase by r-2 to
[r-1,r+14]. The new Z edges have weights equal to their labels,
using [r+15,r+t+11]. This partitions the edge alphabet.
All these edges cross the cut p=r+6 by the lemma.

The resulting state is `A(r+t+12,r+6;1,1)` at the same
physical L=1 and U=r+7. H=r+6 is minimum high, and Z stays
zero. The same W witnesses every vertex, including the new
leaves at distance two. Neither host nor any old incidence moves.
The zero-addition boundary states are retained controls in the
finite checks. They are outside the new executable domain.

## Original nonadjacent suffix

For exact integer K>=2 the full named original is
`[[1],[r],[t],[2]]+[[]]*(K+1)`, with K+r+t+12 vertices and
m=K+r+t+11 edges. Raise all high labels by K at the updated
cut p=r+6. Every original prefix edge has one low and one high
endpoint, so all its weights rise by K. Its used label and
difference sets are exactly
`[0,r+5] union [K+r+6,m]` and `[K+1,m]`.
Their complements in `[0,m]` and `[1,m]` are
`R=[r+6,r+K+5]` and `D=[1,K]`. The physical port s:4
now has label r+K+7. The only unassigned vertices are
s:5,...,s:(K+4). All those sections are empty of branch
vertices, so their entire incidence set is the original K-edge
spine suffix from s:4. The sole crossing is s:4--s:5.

Use the retained [numeric recurrence](B2_NONADJACENT_CONSUMER.md#construction-and-proof)
with translation p. Its bases C_2=(3,1,0), C_3=(4,1,0,2),
C_4=(5,1,2,0,3) have suffix entries [0,K-1] once each and
successive differences (2,1), (3,1,2), (4,1,2,3) respectively.
For K>=5, write C_(K-3)=(K-2,x_1,...,x_(K-3)). The recurrence
uses (K+1,1,K-1,0) followed by the reflected entries K-2-x_i.
By induction the reflected labels are [2,K-2], completing the
suffix alphabet with 1,K-1,0. The first three edge weights are
K,K-2,K-1. The reflected shorter port is 0, so the bridge
from that 0 and the remaining reflected-tail edges retain
all shorter differences [1,K-3]. Each recursive argument
decreases by three to one of the three bases.

Mapping p+C_K in order onto the actual s:4 through s:(K+4)
matches the existing port p+K+1, uses R exactly once on the
remaining K vertices and uses D exactly once on the original
edges. The prefix is preserved and this finite construction
gives ordinary gracefulness. The harness checks the physical
B4 boundary before calling the unchanged numeric helper.
The public B2 wrapper remains scoped to physical s:2.

At K=1 this interface gives R={r+6}, D={1} and port r+8.
The sole finishing edge would have difference 2, so this
interface fails there. At K=2 the three path labels
r+9,r+7,r+6 preclude an alpha threshold for this labeling.
The opposite-class middle label lies strictly between two
same-class endpoints. The alpha claim is for the normalized
prefix.

## Exact selection for K>=2

In every row K>=2 and D=[1,K]. The boundary is physical s:4.
The first row is adjacent and every other row is nonadjacent.

| Disjoint range | Supplier | R and physical s:4 |
|---|---|---|
| t=1, all r>=1 | [QR12 at q=1](B4_UNPADDED_QR12.md), including its Q112 branch for r=1 | [r+6,r+K+5], r+K+6 |
| t=2, all r>=1 | [1R22 selection](B4_1R22_K1_ROOTED_CORE.md) | r=1 gives [7,K+6], K+8; r>=2 gives [r+6,r+K+5], r+K+7 |
| t=3, all r>=1 | [1R32 selection](B4_1R32_K1_ROOTED_CORE.md#exact-selection-and-evidence-scope) | r=1 gives [7,K+6], K+8; r=2 gives [8,K+7], K+9; r>=3 gives [r+6,r+K+5], r+K+7 |
| t>=4,r=1 | [Q1T2 at q=1](B4_UNPADDED_Q1T2.md) | [7,K+6], K+8 |
| t>=4,r=2 | [12T2 supplier](B4_12T2_ZERO_HOST_SUPPLIER.md) | [8,K+7], K+9 |
| t>=4,r>=3 | This construction | [r+6,r+K+5], r+K+7 |

This proves ordinary gracefulness for all positive r,t and K>=2
on the exact ordered (1,r,t,2) family. The new formula discharges
the last row. The K=1 corner with r>=3,t>=4 remains a separate
obligation, along with coverage for broader profiles. The
[declared evidence](../evidence/validation/B4_1RT2_TWO_HOST_COMPATIBILITY_001/README.md)
checks four retained controls, three new prefixes, and four
new completed targets.

The [prior reproduction erratum](../docs/REPRODUCTION_ERRATA.md#b4-1r32-k1-rooted-core-001)
corrects checkout instructions for the archived K=1 evidence.
