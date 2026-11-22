# B4-THIRD-ZERO-HOST-K1-DIRECT-001

## Exact structural reduction

Consider the named complete original `[[1],[1],[2],[2],[],[]]`.
Its six spine vertices are s:0 through s:5. Each center b:i:0
is attached to the original s:i for i=0,1,2,3, and its named
terminals are attached at that center, in counts 1,1,2,2.
The five spine, four attachment, and six terminal edges give
16 vertices and 15 edges. Its graph digest is
`fce6e5676ab825e344c5f217ace9855e4f1e5dc4c88f8a71e9563093daae1a9c`.

Write z=b:2:0, C=s:2, x=l:2:0:0, y=l:2:0:1. In any graceful
labeling of this original with z=0, difference 15 has to pair
labels 0 and 15. The complete neighbor list of z is C,x,y, so
the three placements of 15 are exactly C, x and y.

Exchange the names x and y and fix all other vertices.
The transposition sends z--x to z--y and z--y to z--x.
It fixes all other edges. Composing any labeling with this
transposition therefore preserves the label bijection and
permutes only these two edge weights, while z stays at zero.
It carries the two terminal-maximum cases into each other
and is its own inverse. Both named labelings remain distinct
where the labels are swapped, and no counting quotient is taken.

In the case y=15, difference 14 can only come from the pairs
(0,14) or (1,15). The latter is impossible because the only
neighbor of y is z=0. Thus either C=14 or x=14. If C=14, deleting
y removes only label 15 and weight 15. This leaves the exact
original `[[1],[1],[1],[2],[],[]]` with z=0, C=14, labels
0..14 and differences 1..14. Conversely such a labeling lifts
by attaching the prescribed y at z with label 15, with all
other incidences intact. The feasibility of this additional
condition on C is outside the selected construction.

If x=14 and y=15, the pairs for difference 13 are (0,13),
(1,14), and (2,15). The latter two are impossible because x
and y touch only z=0. Thus C=13. Deleting z,x,y removes
exactly labels 0,14,15 and differences 13,14,15 from the
three edges z--C, z--x, z--y. The remaining named vertices
and edges give the exact original core `[[1],[1],[],[2],[],[]]`.
Subtract 1 from all remaining labels. Translation preserves
every difference and gives 0..12, differences 1..12, and
the physical root value r(s:2)=12. Conversely, take a
graceful labeling of this core with r(s:2)=12 and add 1 to
each core label. This gives labels 1..13 with C=13 and
differences 1..12. Restore z=0, x=14, y=15 and just their
three original edges. They give differences 13,14,15,
recovering the full graceful bijection and both physical
terminal names. These deletion/translation and restoration
maps are inverses in the stated case.

For C=15 and ordered distinct terminal labels a,b in 1..14,
deleting z,x,y removes labels 0,a,b and differences 15,a,b.
The same core keeps labels [1,15] minus {a,b}, differences
[1,14] minus {a,b}, and C=15. These are gapped resource
sets of size 13 and 12, respectively. This residual condition
does not assert an ordinary graceful core. The spine-maximum
case is left open. The supplied terminal case suffices.

## Fixed rooted core and lift

The named core has 13 vertices and 12 edges, with its full
spine and branches at sections 0, 1 and 3. Its own graph
digest is
`aa0e6e159d15dd8aa9003403e47f99bcf7607511fb0ea0accf76b505cf3ebe36`.

| Named vertices in order | Core labels | Original-edge differences |
|---|---|---|
| s:0, s:1, s:2, s:3, s:4, s:5 | 7,0,12,1,10,4 | 7,12,11,9,6 |
| b:0:0, l:0:0:0 | 3,2 | 4,1 |
| b:1:0, l:1:0:0 | 8,5 | 8,3 |
| b:3:0, l:3:0:0, l:3:0:1 | 11,9,6 | 10,2,5 |

The labels use 0..12 once with r(s:2)=12. The differences
listed in spine order and then attachment-then-terminal order
use 1..12 once on the actual original edges. The lift above
gives the following complete 16-vertex fixed seed.

| Named vertices in order | Lifted labels | Original-edge differences |
|---|---|---|
| s:0, s:1, s:2, s:3, s:4, s:5 | 8,1,13,2,11,5 | 7,12,11,9,6 |
| b:0:0, l:0:0:0 | 4,3 | 4,1 |
| b:1:0, l:1:0:0 | 9,6 | 8,3 |
| b:2:0, l:2:0:0, l:2:0:1 | 0,14,15 | 13,14,15 |
| b:3:0, l:3:0:0, l:3:0:1 | 12,10,7 | 10,2,5 |

This is a separate explicit certificate on the complete
original. The earlier [DFS result](../evidence/validation/B4_THIRD_ZERO_HOST_K1_001/query_record.json)
remains INCOMPLETE, reason max_nodes, at 100,000 nodes, with
exhausted=false, count=null, count_lower_bound=0 and no witness.
The ledger does not come from that run or a continuation of it.

## All positive t at K=1

For each exact integer t>=1, excluding Booleans, the original
`[[1],[1],[t],[2],[],[]]` has t+14 vertices and m=t+13 edges.
Its common fixed named subgraph consists of the full six-vertex
spine, all four centers on their original attachments, and just
the four terminals at sections 0, 1 and 3. This is an explicitly
described subgraph on 14 vertices with 13 original edges.
It keeps b:2:0 and its original attachment to s:2. Use the
lifted labels in the table on these vertices. They are exactly
0..13 once, and the 13 non-third-terminal edges exhaust 1..13:
the 12 translated core edge weights and the attachment of weight 13.

Assign f(l:2:0:j)=14+j for 0<=j<t, attaching each prescribed
name only at b:2:0=0. These are exactly the remaining t labels
and weights 14..t+13. The two disjoint partitions establish
ordinary gracefulness for all positive t, including t=1.
The fixed subgraph is not encoded as a t=0 canonical profile.
The original spine, all branch identities and incidences stay.
Every center lies one edge from the spine and each terminal
lies two edges away, including the additional third terminals.

For growth from the complete t=2 seed the same formula gives
fresh labels 16,17,... at j=2,3,..., keeping all old labels.
After k additions the order is 16+k and the same host is zero,
so the next leaf gets 16+k and provides that edge difference.
This is the [ordinary zero-host arithmetic](B4_THIRD_ZERO_HOST_K1.md#conditional-ordinary-zero-host-extension).
A batch of h leaves uses the same labels in the same name
order as h successive leaves: the first label of a later
batch is the new order after earlier additions. Exactly t-2
additions produce the desired target when t>=2, including the
identity at t=2. The partition proof supplies t=1 directly.
The [alpha extension](ALPHA_ZERO_HOST_LEAF_EXTENSION.md)
retains its own alpha and witness hypotheses.

To construct the prefix, make all the stated assignments
except s:5. Only that vertex and its original incident edge
s:4--s:5 remain. The used labels are [0,t+13] minus {5},
and the used differences are [1,t+13] minus {6}, as deleting
the last assignment omits just that label and that edge
weight. Thus R={5}, D={6}, and physical s:4=11. Assigning
s:5=5 consumes both resources, with |11-5|=6. This construction
uses no label shift on a high class, interval predicate,
relational join, or path recurrence. The actual path
l:0:0:0--b:0:0--s:0 has labels 3,4,8. Its ends lie in one
bipartition class and bracket the middle label, so an alpha
threshold cannot separate the classes in this labeling.

## Exhaustive family selection

For every positive integer t,K the exact original family
`[[1],[1],[t],[2]]+[[]]*(K+1)` admits an ordinary graceful
labeling by the following disjoint, exhaustive cases.

| Domain | Source and physical interface |
|---|---|
| K=1, t>=1 | Direct singleton above, R={5}, D={6}, s:4=11 |
| K>=2, t=1 | [Retained Q112 at q=1](B4_FOURTH_2_SUPPLY.md), R=[7,K+6], D=[1,K], s:4=K+7 |
| K>=2, t>=2 | [Retained nonadjacent zero-host construction](B4_THIRD_ZERO_HOST_NONADJACENT.md), R=[7,K+6], D=[1,K], s:4=K+8 |

The existing theorems supply the respective physical suffixes
in the last two rows. The ordinary family theorem concerns only
this ordered unpadded profile. Arbitrary (q,r,t,2), extra branches,
padding and further sections require separate supply. The
bounded [evidence](../evidence/validation/B4_THIRD_ZERO_HOST_K1_DIRECT_001/README.md) checks the fixed construction
at the four declared values and uses zero solver calls.
