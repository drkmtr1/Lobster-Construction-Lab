# Ordinary crossing-cut leaf insertion

## Supplied state and construction

Let a named tree have an ordinary graceful labeling g with
alphabet [0,m] and difference multiset [1,m]. Supply an actual
vertex B of label b and an integer cut 1<=c<=b<=m. Define E
to be exactly the original edges with one endpoint below c
and the other at least c. Require the complete multiset of
differences on E to be [b-c+1,m], each once.

For an exact integer h>=0, take distinct, prescribed fresh
names u_i for 1<=i<=h. Add them as leaves at the same
physical B. Keep old labels below c, increase old labels
at least c by h, and assign u_i=c+i-1. Leaf attachment
preserves connectivity, acyclicity and every old named
incidence. The label bands are

| Vertices | Label band |
|---|---|
| Unchanged old vertices | [0,c-1] |
| New leaves | [c,c+h-1] |
| Shifted old vertices | [c+h,m+h] |

The bands give all labels [0,m+h] once. For an old crossing
edge, only the larger label rises, so its difference grows by
h. For an old edge below the cut, neither endpoint moves.
For an edge wholly at or above the cut, both endpoints
move by h, and subtracting them cancels the shifts.
Since the supplied old crossing spectrum is complete, the
old noncrossing spectrum is its complement in [1,m].
A new leaf has difference b+h-(c+i-1), since the host has
label b+h>=c+h above all fresh labels. These give

| Edges | Difference band |
|---|---|
| Old noncrossing | [1,b-c] |
| New leaves at B | [b-c+1,b-c+h] |
| Old crossing | [b-c+h+1,m+h] |

Each weight in the three contiguous disjoint bands occurs
once. This is an ordinary graceful labeling. The fresh
bands are empty if h=0, giving the identity. At b=c the old
noncrossing band is empty and the new differences are [1,h].

## Updated cut and finite closure

Return c'=c+h and b'=b+h at physical B. At the new cut the
upper set consists of exactly the same old vertices as
before. Every new leaf lies below c' and the host is above
or at it. Thus the new crossing set consists of E and the
new edges, with spectrum [b'-c'+1,m+h]=[b-c+1,m+h].
The inequalities 1<=c'<=b'<=m+h and the complete crossing
premise persist.

For batches of sizes h_1 and h_2, each originally shifted
label gains h_1+h_2 and every original label below c is
fixed. A first-batch name u_i keeps c+i-1 because it is
below c+h_1. A second-batch name of local index j gets
c+h_1+j-1, the label for global index h_1+j in the
combined batch. The same names attach at the same physical
host and the resulting cut and host labels agree. Induction
on the number of batches gives finite pointwise closure in
the prescribed order. Each operation takes finitely many
old assignments and exactly h new leaf assignments.

Any retained physical port v keeps its identity and old
incidences. Its label remains g(v) if g(v)<c and becomes
g(v)+h otherwise. This rule places no numerical preservation
condition on the ports. If an actual path W witnesses
distance at most two for the old tree and dist(B,W)<=1,
the same W witnesses the enlarged tree. The old paths
stay, and every new leaf is at distance at most two via B.
The host stays within distance one of W for further batches.

## Scope and comparison

The hypothesis is about cut-crossing edges. A same-side
upper edge belongs to upper-side incidence but its difference
stays fixed. No alpha split is assumed. In the retained
[alpha lower-block insertion](ALPHA_LOWER_BLOCK_LEAF_INSERTION.md)
the alpha cut and c<=p ensure that all incidences to vertices
below c cross the selected threshold. That rule puts the
new leaves in descending order, keeps the same cut for
further insertion, and supplies a separate alpha-state
conclusion. The present rule uses ascending name order and
returns the raised cut. The one-batch difference arithmetic
has the same bands when the complete crossing premise holds.
For its use on an actual named core with edges wholly above
the cut, see [the 12T2 rooted-core proof](B4_12T2_K1_ROOTED_CORE.md).
