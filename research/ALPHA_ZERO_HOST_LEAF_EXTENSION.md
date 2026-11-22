# Conditional alpha leaf extension at a supplied zero host

Let a named tree on n vertices carry a witnessed alpha state
A(n,p;x,y). Thus n>=2, 1<=p<n, and g bijects the old vertices
onto [0,n-1] with differences [1,n-1] on the original edges.
Every edge crosses the cut between [0,p-1] and [p,n-1].
The actual distinct ports L and U have labels x and p+y,
where 0<=x<p and 0<=y<n-p. The supplied actual L-to-U path W
is within distance two of every vertex.

Assume a prescribed actual host z has g(z)=0 and dist(z,W)<=1.
The host may be off W and may differ from L. For integer h>=0,
take pairwise distinct fresh names a_1,...,a_h and add just those
vertices and the edges z--a_i. All old vertices and incidences
stay. Each new vertex connects as a leaf at z, so the result is
connected and has no new cycle. Its order is n+h.

Keep every old label and set g_h(a_i)=n+i-1. Old labels are
[0,n-1] and fresh labels [n,n+h-1], giving the full bijection.
Old edges keep [1,n-1]. The actual host stays at zero, so the new
edge z--a_i has difference n+i-1. These give [n,n+h-1] once
each, hence the enlarged original edges use [1,n+h-1] once each.
The new leaves are high because n>p. Their edges cross to the
low host. Old edges still cross the cut, and p stays unchanged.

The physical L,U keep labels x,p+y and offsets x,y. The range of
valid high offsets grows, so y remains valid. Every old path to
W remains, and each new leaf lies at distance 1+dist(z,W)<=2
from W. In fact paths among old vertices are unchanged, as no
path between old vertices can pass through a fresh leaf.
The output is A(n+h,p;x,y) with the same actual L,U,W and z.
There is no change of port to z.

For h=0 the new ranges are empty and the operation is the identity.
After k additions every hypothesis holds for order n+k at the
same zero host, and the next named leaf receives n+k. Induction
gives finite closure and exactly h additions. For successive
batches of sizes h_1 and h_2 the j-th leaf of the second batch
receives n+h_1+j-1, the label of leaf h_1+j in the concatenated
order. First-batch labels are unchanged, and induction gives
pointwise agreement for any finite batch partition.

This is the arithmetic of the [retained zero-port extension](ALPHA_ZERO_PORT_LEAF_EXTENSION.md#supplied-state-and-finite-closure)
with the label-zero host tracked separately from the two physical
ports. A host at distance two would place a new leaf at distance
three from this W. The statement assumes that the given state
supplies zero at the prescribed host. It gives no relabeling
rule to move zero or make a different host satisfy the hypotheses.
