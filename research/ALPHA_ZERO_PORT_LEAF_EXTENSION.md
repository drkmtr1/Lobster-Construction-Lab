# Conditional zero-port leaf extension

## Supplied state and finite closure

Let G be an independently supplied named tree on n>=2 vertices with an
alpha graceful labeling g onto 0..n-1. Its low class is 0..p0-1 and its
high class is p0..n-1, with 1<=p0<n. The actual distinct ports L,U have
g(L)=0 and g(U)=p0+y for 0<=y<n-p0. Supply an L-to-U path in G whose
distance from every vertex is at most two. These data form a state
A(n,p0;0,y).

For an integer h>=0 prescribe pairwise distinct new names a_1,...,a_h
outside G. Add just these vertices and the edges L--a_i. The resulting
graph keeps every old vertex and edge. It is connected because each new
vertex is adjacent to L, and is acyclic because a new vertex has degree
one and the old graph is a tree. It has n+h vertices and n+h-1 edges.

Keep every old label and give a_i the label n+i-1. The old and new
vertex labels partition 0..n+h-1. The old differences remain 1..n-1.
Each new edge has difference n+i-1 because its actual host still has
label 0. The new differences are exactly n..n+h-1, each once. Each
new vertex lies in the high class and each new edge crosses to the
low host. The low class remains 0..p0-1. Both original ports keep their
labels, so their offsets remain (0,y), and y<n+h-p0. All old witness
distances remain at most two along the old paths, and each new leaf is
one edge from L on the same witness.

This gives A(n+h,p0;0,y). After j additions the same premises hold
with n replaced by n+j. The next prescribed leaf at L takes label
n+j and supplies that difference. Induction proves closure for any
finite number of additions at this same actual host. For successive
batches, numbering the leaves in their prescribed concatenated order
gives the same labels as a single batch. The operation makes exactly
h additions and stops. For h=0 the new blocks are empty and the map
and state are the identity.

## Host restriction and source comparison

This rule supplies leaves at an existing label-zero vertex. With
the old labels fixed, a new leaf with fresh label n at a host with
label c>0 gives n-c in 1..n-1, already an old difference. That
duplicate obstructs this fixed-label extension at such a host.
The rule gives neither a way to move label zero nor a
nongracefulness result for the enlarged tree.

The adopted [R241 binary rule](../references/upstream/mdl/N241_relational_ports.md)
takes two independently supplied states of order at least two and
requires matching offsets at the actual joined ports. The present
operation uses one supplied state and attaches prescribed leaves.
It needs no singleton R241 operand. Its output is another nontrivial
state with the same ports and offsets, which remain available to
the R241 contract where its own hypotheses hold. The retained source
is MDL commit `858a8c1fcfda87ba40bb1adee498a6131504a803`,
`research/candidates/volume-010.md`, lines 4364–4405 and 4488–4505.

The [2111 proof](B4_UNPADDED_2111.md) is the h=1 instance on the unit
seed. The [B2 unpadded supplier](B2_UNPADDED_ALL_QR.md) also has a
label-zero first center and a terminal block ending at m. Increasing
q there with K,r fixed appends new maximum labels and differences at
that host. Its normalized low size r+2 and exit label r+3 give
y=1, so its high-shift exit is nonadjacent. The [1121 extension](B4_UNPADDED_1121.md)
uses a largest-low center, raises old highs, and inserts a high leaf
to take difference 1. Its low size stays four while its high exit
label increases from four to five, changing the exit offset from zero
to one. The [1211 extension](B4_UNPADDED_1211.md)
uses a minimum-high center after a relabeling, raises old highs, and
inserts a low leaf to take difference 1. In 1211 the low size and high
exit label both increase by one, retaining exit offset one. Neither
transformation is needed to append maximum labels at label zero.

## High shift and conditional adjacent completion

Set N=n+h. For integer K>=1 suppose the target consists of this
enlarged prefix and exactly the original K-edge path from actual U
with K additional fresh vertices and no other unfinished incidence.
Its edge count is m=N+K-1. Raise every high seed label by K and keep
the low labels fixed. The used labels are [0,p0-1] and [p0+K,m].
Each prefix edge crosses classes, so its absolute difference
increases by K and the used differences are [K+1,m]. Therefore
R=[p0,p0+K-1] and D=[1,K], and actual U now has label p0+K+y.
The shifted labeling is a partial labeling with a gap in its label
set. The normalized alpha state is the seed before shifting.

For y=0 the actual U is immediately above R, so the retained
[adjacent consumer](PROOF_OBLIGATIONS.md#active-endpoint-above-the-interval)
applies. Write the original path as w_0=U,w_1,...,w_K. It chooses
the remaining low endpoint first, then the high endpoint, alternating.
Odd positions w_(2i+1) receive p0+i, and positive even positions
w_(2i) receive p0+K-i. With p=p0+ceil(K/2), the two label sets are
[p0,p-1] and [p,p0+K-1]. They partition R, including the empty
even set for K=1. Odd and positive even steps have respective
differences K-2i and K-2i+1 by subtracting the consecutive labels.
Both equal K-j+1 at step j. The consumer makes K assignments to the
fresh path vertices and preserves every prefix label. Prefix lows
and odd suffix labels give 0..p-1, and prefix highs and even suffix
labels give p..m. The prefix edges still cross the cut and the
suffix alternates across it from high U. The complete labeling is
alpha with low-class size p and numerical cutoff p-1. For y>0
the above-side adjacent hypothesis does not hold.

## Immediate symbolic (q,1,1,1) corollary

Use the independently supplied [B4-unit R241/L008 seed](B4_UNPADDED_UNIT.md#retained-r241l008-derivation-of-the-fixed-seed)
on the four unit branches and spine through s:4. Its spine labels
are (12,2,9,5,6), and its center/leaf pairs are
(0,11),(10,1),(3,8),(7,4). The retained construction uses R241 at
x_A=y_B=1 to restore the original s:2--s:3 edge and returns
L=b:0:0=0 and U=s:4=6, with n=13, p0=6 and offsets (0,0).
The original path b:0:0--s:0--s:1--s:2--s:3--s:4 witnesses it.
The reflected right component uses [L008](../references/upstream/bounded/research__LEMMAS.md.archive.md)
at q=1 and zero padding, from MDL_Bounded_Search commit
`e48b94eec4091b4fe189e325cab2eda464409943`, `research/LEMMAS.md`,
line 21.

For each integer q>=1 add h=q-1 prescribed leaves with original
names l:0:0:j, 1<=j<q, at b:0:0. Their seed labels are 12+j.
The seed has 13+(q-1)=q+12 vertices and q+11 edges. None of the
old branches or incidences change. The actual remaining vertices
in the target are exactly s:5,...,s:(K+4), with the original path
edges beginning at U=s:4. After shifting the highs by K the new
leaves have labels K+12+j. The full graph has m=K+q+11 edges
and K+q+12 vertices. Its unused labels remain [6,K+5], its unused
differences remain [1,K], and actual s:4=K+6. The adjacent completion
therefore gives an alpha labeling on exactly
`[[q],[1],[1],[1]]+[[]]*(K+1)` for all integers q,K>=1, with
low-class size 6+ceil(K/2) and cutoff one less.

This supplies the family symbolically once the fixed seed is given.
The new implementation and campaign concern only the exact
[3111 profile](B4_UNPADDED_3111.md). Supplying arbitrary hosts,
other branch placements, additional sections or arbitrary topologies
remains a separate obligation. No historical novelty, formal
verification or universal-lobster result is asserted.
