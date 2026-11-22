# Conditional lower-block leaf insertion

## Supplied state and hypotheses

Let a named tree of order n have an alpha graceful bijection g
onto [0,n-1], with low class [0,p-1] and high class [p,n-1],
where n>=2 and 1<=p<n. Let its actual distinct ports L,U have
g(L)=x and g(U)=p+y, with 0<=x<p and 0<=y<n-p. Supply an actual
L-to-U path W at distance at most two from every vertex.
Supply an actual high host z with b=g(z) in [p,n-1] and
dist(z,W)<=1. Choose an integer c with 1<=c<=p and x<c.

Let S_c contain all original vertices with label below c, and
E_c all original edges incident to S_c. The complete difference
multiset on E_c must be [b-c+1,n-1], each once. This is an
additional hypothesis on the supplied labeling and incidences.

For integer h>=0, supply fresh pairwise distinct names
a_1,...,a_h and add precisely z--a_i. All old names and edges
stay. Adding degree-one vertices keeps the graph connected
and cannot create a cycle, so the enlarged graph is a tree
of order n+h.

## Transformation and edge partition

Keep old labels below c, raise all other old labels by h,
and assign g_h(a_i)=c+h-i for 1<=i<=h. In ascending order the
label blocks are:

| Vertices | Labels |
|---|---|
| Old low vertices below c | [0,c-1] |
| Fresh low leaves | [c,c+h-1] |
| Old low vertices at or above c | [c+h,p+h-1] |
| Old high vertices | [p+h,n+h-1] |

Contiguous disjoint blocks give the full bijection. An old
edge has one low endpoint and one high endpoint. Its high
endpoint always moves, since c<=p. On E_c the low endpoint
stays and the difference grows by h. Outside E_c both endpoints
move equally. The old graceful spectrum and the full E_c
hypothesis give the following partition:

| Edge group | Differences |
|---|---|
| Old edges outside E_c | [1,b-c] |
| Fresh edges at z | [b-c+1,b-c+h] |
| Old edges in E_c | [b-c+h+1,n+h-1] |

Indeed z now has label b+h, and its edge to a_i has weight
b-c+i. Each block has multiplicity one and together they fill
[1,n+h-1]. The low-class size is p+h. All old edges retain their
class orientation, and every new low leaf attaches to the old
high z. Empty intervals are used when their lower bound exceeds
their upper bound, including b=c, c=p, or h=0 as applicable.

## Returned state and ordered repetition

The low port stays at x because x<c. The high port moves to
p+h+y and the host to b+h. The actual ports and both offsets
stay; the high-class size n-p stays as well. The old W still
has its edges and old distances. Each fresh leaf has distance
1+dist(z,W)<=2. The output is A(n+h,p+h;x,y), with the same
actual host and witness.

Return the same c. The vertices below c are exactly S_c.
Fresh leaves and all previously shifted vertices are at least c.
No new edge meets S_c, since its host and fresh leaf are both
above or at c. The complete incident spectrum becomes
[b+h-c+1,n+h-1]. Thus the full hypothesis persists, with the
updated host label b+h and unchanged c.

For h=0 the labels and graph are identical. For two batches of
sizes h_1,h_2, the old vertices at or above c gain h_1+h_2.
The first batch's i-th leaf is at or above c, so after the
second batch its label is c+h_1+h_2-i. The second batch's j-th
leaf gets c+h_2-j, equal to c+h_1+h_2-(h_1+j). Hence the
two batches agree pointwise with one batch in concatenated name
order. Induction gives the same result for any finite batches,
including chronological single additions. There are exactly h
prescribed leaf additions. The labeling and incidence work is
finite on each supplied finite tree.

## Comparisons and limits

At c=p=b the host is minimum high and S_c is the entire old
low class. Every old edge meets S_c, and
the one-batch arithmetic is the
[minimum-high extension](ALPHA_MINIMUM_HIGH_LEAF_EXTENSION.md)
with its fresh-name assignment reversed. Repeatedly resetting
the threshold to the growing p keeps earlier fresh low labels
fixed and assigns fresh labels in ascending order. Holding c
fixed shifts the earlier fresh lows and agrees with the stated
descending convention.

At the actual 1212 host label 10 with p=8, applying the
minimum-high recipe anyway with one fresh label 8 raises all
old highs by one. Its new difference is |11-8|=3, already in
the shifted old spectrum [2,15]. This specific placement
fails. The supplied lower-block premise permits the different
cut at c=4 for this host.

The [upper-block rule](ALPHA_UPPER_BLOCK_LEAF_INSERTION.md)
moves selected high vertices, adds high leaves at a label-one
host, and returns a raised threshold. This lower-block rule
moves every old high and some old lows, adds low leaves at a
supplied high host, and returns the same threshold. [R241](../references/upstream/mdl/N241_relational_ports.md)
joins two supplied compatible port states. The
[QR12 application](B4_UNPADDED_QR12.md) supplies one original
prefix directly. These constructions make no arbitrary-host,
arbitrary-topology, or historical-novelty claim.
