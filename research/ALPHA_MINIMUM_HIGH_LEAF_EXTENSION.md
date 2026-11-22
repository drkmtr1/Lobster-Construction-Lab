# Conditional minimum-high leaf extension

## Supplied state and finite closure

Let G be an independently supplied named tree with an alpha graceful
labeling g onto 0..n-1, where n>=2. The low interval is [0,p-1] and the
high interval is [p,n-1], with 1<=p<n. The actual distinct ports L,U
have g(L)=x and g(U)=p+y, with 0<=x<p and 0<=y<n-p. The supplied
L-to-U path W is within distance two of every old vertex. Suppose the
designated actual host z has g(z)=p and distance at most one from W.

For integer h>=0 take pairwise distinct names a_1,...,a_h outside G
and add exactly the leaf edges z--a_i. All old vertices and incidences
remain. Each new vertex has degree one and is connected through z,
so the result is a tree of order n+h. Keep every old low label,
raise every old high label by h, and assign a_i the label p+i-1.
The disjoint label blocks are [0,p-1] on old lows, [p,p+h-1]
on new leaves, and [p+h,n+h-1] on old highs. They give a bijection
onto 0..n+h-1. Each old edge crossed the original cut, so its
difference increases by h and the old spectrum becomes [h+1,n+h-1].
The host now has p+h, giving each new edge difference h-i+1.
Those differences exhaust [1,h] once.

The new low class is [0,p+h-1]. Every old edge crosses that cut,
as does each new edge from a new low leaf to high z. The same
physical L keeps x and U has p+h+y. Thus x and y are unchanged and
in range, since the high-class size n-p stays fixed and the low
class grows. The same actual z stays minimum high at p+h.
Old paths remain and each new leaf is at distance
1+dist(z,W)<=2 via its only incident edge. The same actual witness
therefore suffices and the output is A(n+h,p+h;x,y).

At h=0 both new ranges are empty and the operation is the identity.
After j additions all hypotheses hold at the same z, with order n+j
and low-class size p+j. One more addition raises only the old high
class by one and gives the next name label p+j. This gives exactly
h additions and terminates. In two successive batches of sizes
h_1,h_2, old highs gain h_1+h_2 and leaves of the first batch
keep their low labels. The next batch begins at p+h_1, so
the result agrees pointwise with the single batch of h_1+h_2
in the same concatenated name order. Induction covers all finite
batches at that same supplied host.

## Scope and source comparison

At distance two from W a fresh leaf is at distance three from
the same W. The distance-one hypothesis concerns this witnessing
path and the label arithmetic is unaffected by the distances.
The rule requires an independently supplied minimum-high host.
For a high host of label p+c with c>0, the same one-leaf placement
would give c+1, already present in the shifted old spectrum 2..n.
This obstruction concerns that placement only.

The [1211 proof](B4_UNPADDED_1211.md#r241-derivation-on-the-original-cut)
already contains this insertion for h=1 in its relabeled left
component. In that proof the high exit and low size increase
together and keep offset one. The [1121 proof](B4_UNPADDED_1121.md)
inserts a high leaf at a largest-low host, keeping its low size
and moving its exit offset. The [zero-port proof](ALPHA_ZERO_PORT_LEAF_EXTENSION.md)
used in [3111](B4_UNPADDED_3111.md) appends maximum labels at its
actual zero host with every old label fixed. The present rule
raises old high labels and increases the low-class size.
R241 is a separate composition of two supplied nontrivial states,
with its own matching-offset and witness hypotheses. No historical
novelty, arbitrary-host supply or universal-lobster claim is made.

## Independent left supply and original R241 join

Use the actual nine-vertex left component from 1211 after its
within-class relabeling of the [B4-unit component](B4_UNPADDED_UNIT.md).
The local labels are:

| Named vertices | Local labels |
|---|---|
| s:0,s:1,s:2 | 8,2,5 |
| b:0:0,l:0:0:0 | 0,7 |
| b:1:0,l:1:0:0 | 4,3 |
| b:2:0,l:2:0:0 | 1,6 |

These use 0..8 once. The spine differences are (6,3).
The attachment/leaf pairs are (8,7),(2,1),(4,5), filling 1..8.
Every edge crosses [0,3] and [4,8]. The actual ports are
L_B=b:0:0=0 and U_B=s:2=5, with offsets (0,1).
Along W_B=b:0:0--s:0--s:1--s:2, the first leaf is one step away,
the second and third centers are one step away, and their leaves
are two steps away. In particular z=b:1:0=4 is the minimum high
and one step from W_B.

Apply h=r-1 for each integer r>=1, using names l:1:0:j with
1<=j<r at z. The resulting labels on s:0,s:1,s:2 are
(r+7,2,r+4). On b:0:0,l:0:0:0 they are (0,r+6), on b:1:0
and l:1:0:j they are r+3 and 3+j for 0<=j<r, and on
b:2:0,l:2:0:0 they are (1,r+5). This is B_r=A(r+8,r+3;0,1)
with the same ports and W_B.

The retained right component is reflected L008 at size one
and zero padding. On s:3,s:4,b:3:0,l:3:0:0 the original
L008 labels are (0,3,2,1). Reflecting the low interval by
u -> 1-u and the high interval by v -> 5-v gives (1,2,3,0).
Each original difference d becomes 4-d, preserving 1..3.
With ports L_A=s:3 and U_A=s:4 this is A(4,2;1,0).
The edge s:3--s:4 is its witness, and the center and leaf lie
one and two edges away. [Retained L008](../references/upstream/bounded/research__LEMMAS.md.archive.md)
· MDL_Bounded_Search `e48b94eec4091b4fe189e325cab2eda464409943`,
`research/LEMMAS.md`, line 21

Use R241 with right A and left B_r at x_A=y_B=1, restoring
exactly s:2--s:3. Add r+3 to A, keep B_r lows, and add 4 to
B_r highs. The label blocks are B_r low [0,r+2], A low
[r+3,r+4], A high [r+5,r+6], and B_r high [r+7,r+11].
Every edge still crosses the cut, including the join from B_r
high to A low. A supplies differences 1..3, the connector
has difference (r+8)-(r+4)=4, and B_r supplies [5,r+11].
The witnesses concatenate on the original connector,
preserving distance at most two. The result is A(r+12,r+5;0,0)
with the actual ports b:0:0=0 and s:4=r+5.

The minimum-high extension takes place inside B_r's left
precursor before joining. In the composed seed b:1:0=r+7
lies two labels above the minimum high r+5. The minimum-high
rule therefore does not apply there in the composed 1211 seed.
[Adopted R241](../references/upstream/mdl/N241_relational_ports.md)
· MDL `858a8c1fcfda87ba40bb1adee498a6131504a803`,
`research/candidates/volume-010.md`, lines 4364–4405 and 4488–4505

## Symbolic unpadded family (q,r,1,1)

For integer q>=1 apply the accepted
[zero-port extension](ALPHA_ZERO_PORT_LEAF_EXTENSION.md#supplied-state-and-finite-closure)
to the composed seed at its actual L=b:0:0. Add the names
l:0:0:j for 1<=j<q with labels r+11+j. This leaves the
other labels and all old incidences intact. The exact profile
through s:4 is `[[q],[r],[1],[1],[]]` and the new normalized
state is A(q+r+11,r+5;0,0). Its witness is
b:0:0--s:0--s:1--s:2--s:3--s:4.

For each integer K>=1 use the exact original target
`[[q],[r],[1],[1]]+[[]]*(K+1)`. Its order is K+q+r+11 and its
edge count is m=K+q+r+10. Only s:5,...,s:(K+4) lie outside
the prefix. They lie on the original K-edge path starting
at s:4 and have no other unfinished incidences. Raising
every high seed label by K gives the direct prefix:

| Named vertices | Shifted labels |
|---|---|
| s:0,s:1,s:2,s:3,s:4 | K+r+11,2,K+r+8,r+4,K+r+5 |
| b:0:0,l:0:0:0 | 0,K+r+10 |
| l:0:0:j (1<=j<q) | K+r+11+j |
| b:1:0 | K+r+7 |
| l:1:0:j (0<=j<r) | 3+j |
| b:2:0,l:2:0:0 | 1,K+r+9 |
| b:3:0,l:3:0:0 | K+r+6,r+3 |

The low labels consist of 0,1,2, the r second-branch leaf
labels 3..r+2, and r+3,r+4. The original seven highs use
K+r+5..K+r+11, with additional first leaves extending
this block through m. The following differences group
all original prefix incidences:

| Original edges | Differences in the given order |
|---|---|
| s:3--s:4, s:3--b:3:0, b:3:0--l:3:0:0, s:2--s:3 | K+1, K+2, K+3, K+4 |
| b:1:0--l:1:0:j (0<=j<r) | K+r+4-j, using [K+5,K+r+4] |
| s:1--b:1:0, s:1--s:2, s:2--b:2:0, b:2:0--l:2:0:0, s:0--s:1, b:0:0--l:0:0:0, s:0--b:0:0 | K+r+5 through K+r+11 |
| b:0:0--l:0:0:j (1<=j<q) | K+r+11+j, using [K+r+12,K+r+q+10] |

The last block is empty at q=1. The used labels are
[0,r+4] and [K+r+5,m], and the differences fill [K+1,m].
Let a=r+5. Thus R=[a,a+K-1], D=[1,K], and actual s:4=a+K.

On the original path beginning at s:4, use the retained
[above-side adjacent completion](PROOF_OBLIGATIONS.md#active-endpoint-above-the-interval).
Odd position j=2i+1 uses a+i, and positive even position
j=2i uses a+K-i. They give [a,a+ceil(K/2)-1] and
[a+ceil(K/2),a+K-1], partitioning R. The successive edge
differences are K-2i and K-2i+1 on odd and even steps,
respectively. Both equal K-j+1, exhausting D in descending
order. There are K assignments to just the original suffix
vertices. Prefix lows and odd suffix labels fill 0..p-1
for p=a+ceil(K/2). Prefix highs and even suffix labels fill
p..m. Every prefix edge crosses the cut, and the suffix
alternates across it from high s:4. Thus the complete alpha
low-class size is r+5+ceil(K/2), with cutoff one less.
For lobster topology extend the prefix witness along the
suffix to s:(K+4). No further exported relational state is
claimed for the completed graph.

The relabeled seed at r=1 can differ from the existing unit
and q111 constructors. At q=1,r=2 the displayed formula
is the retained 1211 formula. Both old routes and their
certificates retain their accepted behavior. The proof
quantifies q,r,K by finite construction and algebra.
Only the [1311 specialization](B4_UNPADDED_1311.md) has new
executable coverage. Other branch placements, padding,
additional sections and arbitrary topology require separate supply.
