# Conditional upper-block leaf insertion at a general low host

## Exact state and incident-edge hypothesis

Supply a witnessed normalized alpha state A(n,p;x,y) on a
named tree of order n. Its labeling g is a bijection onto
[0,n-1], and the original differences are [1,n-1] once each.
Every edge crosses the cut between [0,p-1] and [p,n-1].
The distinct actual ports are L of label x in [0,p-1] and
U of label p+y in [p,n-1], joined by an actual path W within
distance two of every vertex.

Supply a physical low host H with g(H)=a, 0<=a<p, and
dist(H,W)<=1. Choose an integer c with p+y<c<=n-1.
Define H_c as the set of all original vertices whose labels
are at least c, and E_c as the set of all original edges
incident to H_c. Require the complete difference multiset
on E_c to be [c-a,n-1], each once. The full incidence
condition is part of the supplied state.

## Insertion and returned state

For an integer h>=0 prescribe distinct fresh names u_i,
1<=i<=h. Add just these vertices and the edges H--u_i.
Each addition attaches a leaf, preserving connectivity,
acyclicity and every old incidence. Raise all labels
in H_c by h, keep all other old labels, and assign
g'(u_i)=c+i-1. The old fixed labels, new labels and
shifted labels form [0,c-1], [c,c+h-1], and [c+h,n+h-1].
These consecutive blocks give the complete bijection.

Because c>p+y>=p, each selected old vertex is high.
Each edge of E_c has one selected high end and one
unshifted low end, so its difference grows by h.
Unselected old edges keep their weights. The new leaf
at c+i-1 has weight c+i-1-a at the actual host H.
The resulting bands are:

| Edge group | Difference multiset |
|---|---|
| Unaffected old edges | [1,c-a-1] |
| New edges | [c-a,c-a+h-1] |
| Shifted old edges | [c-a+h,n+h-1] |

They exhaust [1,n+h-1] once each. The new vertices are high
and the old low set is unchanged, so the alpha low size is
p and every edge crosses its cut. The actual L, U and H
all have labels below c. They retain labels x,p+y,a and
the ports retain offsets x,y. The same witness W still
contains its old edges. New leaves are one edge beyond H,
at distance at most two from W. This gives A(n+h,p;x,y).

Return c'=c+h. The set at or above c' is exactly the same
physical H_c. Old unselected labels and all new leaves
lie below c'. Hence its incident set is exactly E_c and
its spectrum is [c+h-a,n+h-1]. The threshold inequality
p+y<c'<=n+h-1 and host/witness premises persist.

When h=0 the middle label band and new difference band
are empty, giving the original state. In successive batches
of sizes h_1,h_2 the original selected vertices are raised
by h_1+h_2, and the original unselected vertices stay.
The first batch keeps its labels below c+h_1. The second
assigns c+h_1+j-1 to its j-th name, exactly the value for
name h_1+j in one concatenated batch. The incidence set
is the same in both constructions. Induction gives agreement
for any finite sequence of batches in that name order.
Chronological insertion terminates after h leaf additions,
with a finite shift on the supplied finite state at each step.

## Comparison with retained operations

At a=1 the edge premise is [c-1,n-1], and the proof specializes
to the [retained label-one upper-block rule](ALPHA_UPPER_BLOCK_LEAF_INSERTION.md).
That hypothesis already implies p>=2.

For the arithmetic comparison with the
[lower-block rule](ALPHA_LOWER_BLOCK_LEAF_INSERTION.md), complement
the old labels by g*=(n-1)-g. Its low size is n-p, its high host
label is b*=(n-1)-a, and its lower threshold is c*=n-c.
The vertices with g*<c* are precisely H_c, and the lower-block
edge premise starts at b*-c*+1=c-a. With output complement in
the enlarged alphabet, the upper insertion's new labels become
c*+h-i, as in the lower rule. The old upper-selected labels
stay fixed in the complemented coordinates and all other old
ones move by h, again giving the lower-block arithmetic.

The complemented physical low port would be the original U.
Its complemented label is x*=(n-1)-(p+y). The original
c>p+y gives x*>=n-c=c*, whereas the retained lower-block
port inequality requires x*<c*. Equality also fails the strict
requirement. Thus the port conclusion follows from the direct
original-label verification above. In fact the complemented
low port moves by h while its original-coordinate label stays,
because the output complement uses n+h-1. The complement
comparison concerns arithmetic on the same incidences.

[R241](../references/upstream/mdl/N241_relational_ports.md)
requires independently supplied compatible alpha states at the
actual ports and the stipulated connector between them. This
rule keeps the actual ports and enlarges one supplied state by
prescribed leaf edges on its own original target. It supplies
neither arbitrary-host hypotheses nor a new relational join.

## Compatibility with a distinct zero host

Additionally supply a distinct physical vertex Z with label zero
and dist(Z,W)<=1. Prescribe k>=0 fresh zero-host leaves v_j,
1<=j<=k, all distinct from the old and upper-insertion names.
Both hosts are low and remain fixed under either rule. Both
operations preserve W, and the new leaves remain within
distance two of it.

If the upper insertion goes first, it returns c+h and the
selected original vertices H_c. Then the accepted
[zero-host extension](ALPHA_ZERO_HOST_LEAF_EXTENSION.md)
appends labels n+h+j-1. These are at least n+h>c+h,
so at the final threshold the zero-host leaves join H_c.
Their edges contribute weights [n+h,n+h+k-1] to the
selected spectrum. The H leaves remain below the threshold
and no other incidence joins the set.

If the zero extension goes first, it appends labels n+j-1,
all at least n>c. At c the selected vertices are the old H_c
plus these new leaves. Their incident edges are exactly E_c
and the k new edges to Z. The weights [n,n+k-1] extend the
old spectrum to [c-a,n+k-1], so the full upper-block
hypothesis holds on the enlarged original. Applying the
upper insertion shifts the original selected highs and the
zero-host leaves by h. The H leaves again get c+i-1.

In both orders the labels are therefore:

| Named group | Final label |
|---|---|
| Original vertices in H_c | g(v)+h |
| Other original vertices | g(v) |
| Prescribed H leaves u_i | c+i-1 |
| Prescribed zero-host leaves v_j | n+h+j-1 |

The two operations add the same prescribed incidences.
This is pointwise agreement on named vertices. The final
state is A(n+h+k,p;x,y), with threshold c+h and complete
selected spectrum [c+h-a,n+h+k-1]. The selected vertices are
the original H_c plus the zero-host leaves, with all their
final incident edges. Both host identities and labels,
both ports and offsets, W and every original incidence
are preserved. The proofs include h=0 or k=0 by empty bands.
