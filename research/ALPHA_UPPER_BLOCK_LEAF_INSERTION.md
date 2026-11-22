# Conditional upper-block leaf insertion

## Exact state and operation

Supply a named tree of order n and an alpha labeling g onto 0..n-1,
with low class [0,p-1] and high class [p,n-1], where 2<=p<n.
Its actual distinct ports L and U have labels x and p+y, respectively,
with 0<=x<p and 0<=y<n-p. Supply an actual L-to-U path W within
distance two of every vertex. The designated actual host z has
g(z)=1 and distance at most one from W.

Choose integer c with p+y<c<=n-1. Let H_c consist of every original
vertex with label at least c, and E_c of every original edge incident
to H_c. Require the multiset of differences on E_c to consist of each
weight c-1 through n-1 exactly once. This is part of the input, in
addition to A(n,p;x,y), the physical host and the witness.

For integer h>=0 prescribe distinct fresh names a_1,...,a_h and
attach only z--a_i. Every original vertex and edge stays. The enlarged
graph remains connected, and a new leaf cannot lie on a cycle, so it is
a tree on n+h vertices. Raise the labels in H_c by h, keep all other
old labels and set g_h(a_i)=c+i-1. The label blocks are [0,c-1],
[c,c+h-1], [c+h,n+h-1]. They partition 0..n+h-1.

Since c>p+y>=p, all changed old labels are high. Every edge of E_c
has one changed high endpoint and an unchanged low endpoint, as each
original edge crosses the alpha cut. It follows that the unaffected
edges keep [1,c-2] and E_c changes to [c+h-1,n+h-1]. The fresh high
leaves attach to low z=1 and give differences c+i-2, exactly
[c-1,c+h-2]. The three ranges partition 1..n+h-1 with multiplicity
one. The low class is still [0,p-1] and every edge crosses. Thus the
result is alpha graceful with low-class size p.

The two port labels x and p+y are below c, as is label one. The
actual ports, offsets and host label therefore stay. All old paths
to W remain, and each new leaf is within two steps of W via z. The
same witness suffices for A(n+h,p;x,y).

## Output invariant and finite closure

Return c'=c+h along with the new state. The vertices at least c'
are exactly the original H_c. Unshifted old labels were below c,
and every new leaf is below c'. No new edge meets the selected set,
so the complete incident-edge multiset at c' is [c'-1,n+h-1].
The threshold bounds still hold, since p+y<c'<=n+h-1. The
host and witness hypotheses still hold as well.

For h=0 the operation is the identity, with an empty new block.
After j additions the threshold is c+j and the selected vertex
set remains H_c. The next prescribed leaf takes label c+j,
and the selected old vertices rise by one. Thus exactly h
additions terminate with the batch formula. More generally,
successive batches of sizes h_1,h_2 shift only H_c in both
steps. Old and first-batch labels outside H_c stay fixed in
the second step, which starts assigning at c+h_1. The batches
therefore agree with one batch in the concatenated name order.
This gives finite closure at the same actual host, with the
updated threshold and incident predicate retained at every step.

## Independent base on the original left graph

Use the [relabeled nine-vertex 1211 component](B4_UNPADDED_1211.md#r241-derivation-on-the-original-cut),
also used in [1311](B4_UNPADDED_1311.md). Its original profile
is `[[1],[1],[1]]`. Its spine labels are (8,2,5). The named
center/leaf pairs in branch order are (0,7), (4,3), (1,6).
They label 0..8 once. The spine differences are (6,3) and
branch attachment/terminal pairs are (8,7), (2,1), (4,5).
All edges cross the cut of low size 4 and the differences are
1..8. The actual ports b:0:0=0 and s:2=5 give offsets (0,1).
The path b:0:0--s:0--s:1--s:2 witnesses the component: the
first leaf and the other centers are one step from the path,
and the remaining terminal leaves are two steps from it.

Take z=b:2:0=1, one step from the witness, and c=7>5. The
selected vertices s:0 and l:0:0:0 have exactly the following
incident edges.

| Original edge | Difference |
|---|---:|
| s:0--s:1 | 6 |
| b:0:0--l:0:0:0 | 7 |
| s:0--b:0:0 | 8 |

These are all incidences because s:0 is the initial spine
vertex, and l:0:0:0 is a terminal. Thus this seed independently
supplies the entire predicate. The predicate is additional:
on this same witnessed alpha state, c=8 also meets the numerical
threshold bounds, but selects s:0 alone and gives {6,8} in place
of {7,8}. One prescribed insertion at c=8 would duplicate
difference 7 and miss difference 6. This concerns that placement.

For each integer t>=1 insert h=t-1 leaves named l:2:0:j,
1<=j<t, at b:2:0. The resulting spine is (t+7,2,5).
The first and second center/leaf pairs are (0,t+6) and (4,3).
The third center is 1 and its t terminals are 6+j, 0<=j<t.
The state is A(t+8,4;0,1) on `[[1],[1],[t]]`, and the updated
threshold is t+6. The second leaf, second attachment, edge
s:1--s:2 and third attachment give 1,2,3,4 respectively.
The third terminal edges give 5..t+4. The first spine edge,
first terminal and first attachment give t+5,t+6,t+7.
The last three are the updated upper incident spectrum.
The first center remains zero and the second center remains
minimum high at 4, one edge from the witness. The actual exit
s:2 stays 5, preserving offset one.

The [1121 largest-low insertion](B4_UNPADDED_1121.md)
shifts all old highs and supplies a new smallest difference.
This upper-block operation leaves the minimum high and both
port labels fixed, and inserts a middle band of differences
at the different host with label one.

## Composition in the supplied order

First perform the upper-block insertion just proved, then use
the [minimum-high extension](ALPHA_MINIMUM_HIGH_LEAF_EXTENSION.md)
with r-1 fresh leaves at the actual second center b:1:0. This
raises all highs by r-1 and supplies the left state
A(r+t+7,r+3;0,1). Its spine is (r+t+6,2,r+4).
The first pair is (0,r+t+5), the second center is r+3 with
leaves 3+j for 0<=j<r, and the third center is 1 with
leaves r+5+j for 0<=j<t. The original witness and actual
ports of the left component stay, and its exit now has label
r+4. The upper-block predicate was used for the first step.
No preservation of that predicate through the second step or
commutativity of the operations is required.

The right component is the [reflected L008 state](B4_UNPADDED_UNIT.md)
A(4,2;1,0). On s:3,s:4,b:3:0,l:3:0:0 its labels are (1,2,3,0).
L008 at size one and no padding supplies (0,3,2,1) before reflecting
the low class by u -> 1-u and the high class by v -> 5-v.
The map sends difference d to 4-d, preserving 1..3. The
actual ports are s:3 and s:4, and the original edge witnesses
the right component with its center and leaf within distance two.
[L008](../references/upstream/bounded/research__LEMMAS.md.archive.md)
· MDL_Bounded_Search `e48b94eec4091b4fe189e325cab2eda464409943`,
`research/LEMMAS.md` line 21

Apply R241 with right as A and left as B, matching x_A=y_B=1.
Add r+3 to A, keep left lows, and add 4 to left highs.
The four vertex blocks are left low [0,r+2], right low
[r+3,r+4], right high [r+5,r+6], and left high [r+7,r+t+10].
Restore exactly the original s:2--s:3 edge, giving difference
(r+8)-(r+4)=4. The right spectrum remains 1..3 and the left
spectrum gains 4 to give 5..r+t+10. The two witnesses concatenate
along the original connector and all vertices remain within
distance two. This supplies A(r+t+11,r+5;0,0) with returned
physical b:0:0=0 and s:4=r+5.
[R241 and adopted scope](../references/upstream/mdl/N241_relational_ports.md)
· MDL `858a8c1fcfda87ba40bb1adee498a6131504a803`,
`research/candidates/volume-010.md` lines 4364–4405 and 4488–4505

Then use the accepted [zero-port extension](ALPHA_ZERO_PORT_LEAF_EXTENSION.md)
at the returned physical first center with q-1 leaves named
l:0:0:j for 1<=j<q. Their seed labels are r+t+10+j. This keeps
the two actual ports and the concatenated witness of the prefix.
The resulting normalized state is A(q+r+t+10,r+5;0,0) on
`[[q],[r],[t],[1],[]]`.

## Exact symbolic (q,r,t,1) family

Fix positive integers q,r,t,K. The full original target
`[[q],[r],[t],[1]]+[[]]*(K+1)` has q+r+t+10 prefix vertices,
K+q+r+t+10 total vertices and m=K+q+r+t+9 edges. The four
branches and spine through s:4 are in the prefix. Exactly the
K vertices s:5,...,s:(K+4) remain. Their incidences form the
original consecutive path from s:4, with sole crossing s:4--s:5.
The high shift by K gives the direct named formula:

| Named vertices | Shifted labels |
|---|---|
| s:0,s:1,s:2,s:3,s:4 | K+r+t+10,2,K+r+8,r+4,K+r+5 |
| b:0:0,l:0:0:0 | 0,K+r+t+9 |
| l:0:0:j (1<=j<q) | K+r+t+10+j |
| b:1:0 | K+r+7 |
| l:1:0:j (0<=j<r) | 3+j |
| b:2:0 | 1 |
| l:2:0:j (0<=j<t) | K+r+9+j |
| b:3:0,l:3:0:0 | K+r+6,r+3 |

The lows give 0,1,2, then 3..r+2, then r+3,r+4.
The sorted highs give K+r+5..K+r+8, the third leaves
K+r+9..K+r+t+8, the first leaf and root K+r+t+9 and
K+r+t+10, and the added first leaves through m. Thus the
two used label intervals are [0,r+4] and [K+r+5,m].

| Original edges, in order within each group | Absolute differences |
|---|---|
| s:3--s:4, s:3--b:3:0, b:3:0--l:3:0:0, s:2--s:3 | K+1, K+2, K+3, K+4 |
| b:1:0--l:1:0:j (0<=j<r) | K+r+4-j, using [K+5,K+r+4] |
| s:1--b:1:0, s:1--s:2, s:2--b:2:0 | K+r+5, K+r+6, K+r+7 |
| b:2:0--l:2:0:j (0<=j<t) | K+r+8+j, using [K+r+8,K+r+t+7] |
| s:0--s:1, b:0:0--l:0:0:0, s:0--b:0:0 | K+r+t+8, K+r+t+9, K+r+t+10 |
| b:0:0--l:0:0:j (1<=j<q) | K+r+t+10+j, using [K+r+t+11,m] |

Each original prefix edge occurs once. The last interval is empty
at q=1. The differences exhaust [K+1,m] and the two complements
are R=[r+5,K+r+4] and D=[1,K]. The physical port s:4=K+r+5
is immediately above R.

Write a=r+5. The [adjacent consumer](PROOF_OBLIGATIONS.md#active-endpoint-above-the-interval)
assigns a+i at odd j=2i+1 and a+K-i at even j=2i>0.
The respective label sets are [a,a+ceil(K/2)-1] and
[a+ceil(K/2),a+K-1], partitioning R. Subtraction from the
previous path label, including the port for the first step,
gives K-2i and K-2i+1 for odd and even steps. Both are K-j+1.
Exactly K assignments to the original suffix consume D and
preserve the prefix. With p=a+ceil(K/2), the prefix lows plus
odd positions fill 0..p-1 and the prefix highs plus even
positions fill p..m. All original prefix edges cross, and the
suffix alternates across the cut from high s:4. The complete
labeling is alpha with cutoff p-1. At K=1, R={r+5}, D={1},
s:4=r+6, s:5=r+5 and p=r+6. Extend the concatenated witness
along the suffix to witness the full topology. An additional
completed relational state would require a separate proof.

At t=1 the formula agrees with the accepted (q,r,1,1) result.
The positive integer quantifiers use the algebra and finite
constructions above. Only the [QR21 specialization](B4_UNPADDED_QR21.md)
is newly executable. Other fourth-branch sizes, padding, multiple
branches per section, more sections and arbitrary host or topology
supply are outside this result.
