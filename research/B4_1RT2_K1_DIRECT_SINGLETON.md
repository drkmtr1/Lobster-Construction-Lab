# B4-1RT2-K1-DIRECT-SINGLETON-001

## Independently supplied maximum-rooted core

Let r>=3 be an exact integer. The
[retained ordinary core proof](B4_1R32_K1_ROOTED_CORE.md#parameterized-core-and-finite-closure)
supplies `C_r=[[1],[r],[],[2],[],[]]`, with r+12 vertices,
r+11 edges, and the following labels. There is no center or
terminal at section 2. Its physical spine vertex s:2 is present.

| Named vertices in order | Core labels a_r |
|---|---|
| s:0,s:1,s:2,s:3,s:4,s:5 | r+6,0,r+11,1,r+9,r+3 |
| b:0:0,l:0:0:0 | r+2,r+1 |
| b:1:0,l:1:0:0 | r+7,r+4 |
| l:1:0:j, 1<=j<r | j+1 |
| b:3:0,l:3:0:0,l:3:0:1 | r+10,r+8,r+5 |

The proof grows the [retained r=2 core](B4_12T2_K1_ROOTED_CORE.md#retained-original-and-a-single-ordinary-insertion)
using the [ordinary crossing-cut rule](ORDINARY_CUT_LEAF_INSERTION.md)
with cut 3 at b:1:0=9 and a batch of r-2 leaves.
The old labels below 3 occupy [0,2]; the new leaves occupy [3,r];
the old upper labels move to [r+1,r+11]. In particular the maximum
is at physical s:2. The six old noncrossing weights stay [1,6].
New second-terminal edges have weights r+6-j for 2<=j<r,
giving [7,r+4]. The seven original crossings gain r-2 and give
[r+5,r+11]. The disjoint bands give a graceful core with
complete crossing spectrum [7,r+11] at c_r=r+1. All names
and incidences at sections 0, 1 and 3 stay with their centers.
The proof supplies the cores symbolically. The saved cores for
r=3,4,5 and their original identities are examined as retained
controls.

## Direct formula and exact singleton

Fix an exact integer t>=4. Translate the core labels by one.
Restore just the original attachment s:2--b:2:0, label b:2:0
by zero, and attach the t original leaves l:2:0:j only to
that center, using r+13+j for 0<=j<t. One edge connects the
new center to the core, and its new terminals have degree
one. The graph is connected and acyclic with all original
named incidences, n=r+t+13 vertices and m=r+t+12 edges.
The construction gives these labels, including the final
assignment for reference.

| Named vertices in order | Full labels f |
|---|---|
| s:0,s:1,s:2,s:3,s:4,s:5 | r+7,1,r+12,2,r+10,r+4 |
| b:0:0,l:0:0:0 | r+3,r+2 |
| b:1:0,l:1:0:0 | r+8,r+5 |
| l:1:0:j, 1<=j<r | j+2 |
| b:2:0 | 0 |
| l:2:0:j, 0<=j<t | r+13+j |
| b:3:0,l:3:0:0,l:3:0:1 | r+11,r+9,r+6 |

The center uses {0}, the translated core uses [1,r+12],
and the third terminals use [r+13,r+t+12]. These partition
[0,m]. Translation preserves every original core difference
[1,r+11]. Physical s:2 now has label r+12, so its attachment
to zero supplies r+12. Each third terminal's weight is its
label, giving [r+13,r+t+12]. These partition [1,m].

To supply the prefix, evaluate the core formula on the
vertices other than s:5, translate those labels by one, then
assign the third center and its terminal labels directly.
The only unassigned vertex is physical s:5, whose only
original neighbor is s:4. Thus s:4--s:5 is the sole pending
and crossing edge of the assigned vertex set. The partition
calculations exclude exactly a_r(s:5)+1=r+4 from the label
alphabet and |a_r(s:4)-a_r(s:5)|=6 from the difference
alphabet. At physical s:4 the label is r+10. Hence the
singleton contract is R={r+4}, D={6}, and the only assignment
f(s:5)=r+4 consumes both on the actual edge, preserving
every earlier assignment.

The original spine through s:4 witnesses the prefix.
Appending s:5 witnesses the full graph. Every center is
one edge from its spine attachment, and every terminal
is two edges away through its original center. The formula
uses finitely many assignments for every finite r,t. It
establishes ordinary gracefulness. In this exhibited labeling
the endpoints of l:0:0:0--b:0:0--s:0 have labels r+2 and r+7,
with the opposite-class r+3 between them, so there is no
alpha threshold for this labeling.

## Smallest new original

For r=3,t=4 the following ledger accounts for six spine
vertices, four centers and ten terminals. The rows list
the consecutive spine differences or the original attachment
followed by terminal edges in name order.

| Named vertices in order | Labels | Edge differences in this order |
|---|---|---|
| s:0,s:1,s:2,s:3,s:4,s:5 | 10,1,15,2,13,7 | 9,14,13,11,6 |
| b:0:0,l:0:0:0 | 6,5 | 4,1 |
| b:1:0,l:1:0:0,l:1:0:1,l:1:0:2 | 11,8,3,4 | 10,3,8,7 |
| b:2:0,l:2:0:0,l:2:0:1,l:2:0:2,l:2:0:3 | 0,16,17,18,19 | 15,16,17,18,19 |
| b:3:0,l:3:0:0,l:3:0:1 | 14,12,9 | 12,2,5 |

The labels are exactly 0..19 once. The nineteen listed
differences are exactly 1..19 once, on all five spine
edges, four attachments and ten terminal edges.
Physical s:4=13 leaves R={7} and D={6} before completion.

## Ordinary third-host growth

The [accepted t=3 completion](B4_1R32_K1_ROOTED_CORE.md#fixed-size-lift-and-original-singleton)
has order r+16, zero at Z=b:2:0, and the same labels as the
formula on all existing named vertices. Apply the
[ordinary zero-host extension](B4_THIRD_ZERO_HOST_K1.md#conditional-ordinary-zero-host-extension),
whose premise is a graceful tree and a supplied zero host.
The first fresh leaf l:2:0:3 receives r+16, its current
order. After a finite batch, the next index j receives
r+13+j, again the current order and the next maximum
difference. All previous labels, differences, original
spine vertices and adjacencies stay. Each addition is a
pendant edge at the same Z, preserving connectivity and
acyclicity. Thus any finite subdivision assigns exactly
the same labels in prescribed index order. The empty batch
is the identity. The new label and difference bands occupy
the newly added maxima, so the old singleton resources
and physical s:4 remain as proved when the direct prefix is
supplied. The zero-host lemma is applied to completed trees.

## Restricted ordinary two-host compatibility

Use H=b:1:0, Z=b:2:0 and d=r+2 on the completed labeling.
The translation makes a core label a_r(v) at least c_r
exactly when a_r(v)+1 is at least d. The translated core
crossings remain [7,r+11]. The third attachment and all
third terminal edges cross d, from Z=0 to labels r+12 and
[r+13,r+t+12]. The complete crossing spectrum is therefore
[7,r+t+12] and the noncrossing spectrum stays [1,6].
In particular the original final edge s:4--s:5 has both
endpoints at least d and retains weight six. The host has
f(H)=r+8, and f(H)-d+1=7 agrees with the lower crossing
bound. H remains one edge from the unchanged spine.
This supplies the full ordinary cut premise. Counting
all edges incident above the cut would also count
same-side edges such as the final edge.

For a batch of h>=0 fresh second terminals at H, the
ordinary crossing-cut rule raises labels at least d by h
and gives local leaf i the label d+i-1. At global
j=r+i-1 this is j+2. Previously inserted second terminals
with indices j>=1 stay below the cut. The original
l:1:0:0 is an upper-side vertex and moves with its center,
so their edge keeps weight three. All other old labels
change exactly as in the formula with r replaced by r+h.
This includes each of the third terminal labels and s:4
and s:5, while Z stays zero. The returned cut is r+h+2,
the host label is r+h+8 and the required crossing spectrum
again starts at 7. A Z batch of k>=0 from any such state
keeps the host and cut and assigns labels starting at the
current order. Its new edges cross and extend the top of
the crossing spectrum. It is exactly substitution t->t+k.

After any finite interleaving with totals h,k, induction
on the batches now gives the stated formula and cut at
(r+h,t+k) on the same named graph with its prescribed
additional leaves. Each step preserves both premises,
the physical hosts and the spine, so the result is
pointwise independent of subdivision or order, provided
each host uses its own increasing leaf-name order. This
is a restricted result on these completed ordinary
states and also applies at their accepted t=3 boundary.
For the resulting direct singleton, second growth raises
both the label in R and the label at s:4 by h. Third growth
preserves both. The edge uses D={6} throughout.

The [alpha compatibility result](ALPHA_MINIMUM_HIGH_ZERO_HOST_COMPATIBILITY.md)
acts on a supplied alpha state with H at its minimum-high
label. Here H is six above the ordinary cut and same-side
edges are present. The [normalized K>=2 supplier](B4_1RT2_TWO_HOST_COMPATIBILITY.md)
uses a different third-terminal ledger and a different suffix
contract. The present proof uses only the ordinary rules
on complete graceful states and the direct formula for the
partial singleton.

## Selection for all positive r,t,K

The exact ordered profile is `[[1],[r],[t],[2]]+[[]]*(K+1)`.
In the following rows s:4 is always the original physical port.
The domains are pairwise disjoint and exhaustive. First separate
K>=2 from K=1. At K=1 separate t=1 and t=2, then for t>=3
separate r=1, r=2 and r>=3. The last subgroup is split at t=3.

| Domain | Supplier and physical interface |
|---|---|
| K>=2, all r,t>=1 | [Retained six-case selection](B4_1RT2_TWO_HOST_COMPATIBILITY.md#exact-selection-for-k2). All use D=[1,K]. For t=1 its adjacent interface has R=[r+6,r+K+5], s:4=r+K+6. For t>=2 the nonadjacent interface has R=[r+6,r+K+5], s:4=r+K+7. |
| K=1,t=1, all r>=1 | [QR12 at q=1](B4_UNPADDED_QR12.md) gives R={r+6}, D={1}, s:4=r+7. Its retained Q112 branch gives exactly this interface at r=1. |
| K=1,t=2, all r>=1 | [1R22 selector](B4_1R22_K1_ROOTED_CORE.md#exact-all-positive-selection-rule) gives R={5}, D={6}, s:4=11 for r=1; R={r+3}, D={5}, s:4=r+8 for r>=2. |
| K=1,t>=3,r=1 | [11T2 direct singleton](B4_THIRD_ZERO_HOST_K1_DIRECT.md#all-positive-t-at-k1) gives R={5}, D={6}, s:4=11. |
| K=1,t>=3,r=2 | [12T2 rooted-core singleton](B4_12T2_K1_ROOTED_CORE.md#direct-singleton-and-witnesses) gives R={6}, D={6}, s:4=12. |
| K=1,t=3,r>=3 | [1R32 rooted-core singleton](B4_1R32_K1_ROOTED_CORE.md#fixed-size-lift-and-original-singleton) gives R={r+4}, D={6}, s:4=r+10. |
| K=1,t>=4,r>=3 | The direct singleton above gives R={r+4}, D={6}, s:4=r+10. |

Each branch consumes its own resources on the original target.
These constructions prove ordinary gracefulness for all positive
integers r,t,K on this exact ordered family. Other first or fourth
sizes, additional sections and more general profiles remain
separate obligations. The [bounded evidence](../evidence/validation/B4_1RT2_K1_DIRECT_SINGLETON_001/README.md)
checks only the declared records, without search.
