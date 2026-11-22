# B4-UNPADDED-Q1T2-001

## Retained named seed and full premise

Use the [accepted 1122 seed](B4_THIRD_ZERO_HOST_NONADJACENT.md#explicit-seed-and-witness)
on the original `[[1],[1],[2],[2],[]]`, with the unchanged
15-vertex graph and its 14 actual edges.

| Named vertices in order | Seed labels | Edge weights in original order |
|---|---|---|
| s:0,s:1,s:2,s:3,s:4 | 9,1,12,5,8 | 8,11,7,3 |
| b:0:0,l:0:0:0 | 4,10 | 5,6 |
| b:1:0,l:1:0:0 | 11,2 | 10,9 |
| b:2:0,l:2:0:0,l:2:0:1 | 0,13,14 | 12,13,14 |
| b:3:0,l:3:0:0,l:3:0:1 | 7,3,6 | 2,4,1 |

The branch rows put the original attachment before the terminals.
The full ledger gives 0..14 and edge weights 1..14 once each, and
every edge crosses the cut at p=7. Take actual L=H=b:0:0 of
label 4 and U=s:4 of label 8 and let
W=b:0:0--s:0--s:1--s:2--s:3--s:4. The first leaf has distance
one from W. Other centers have distance one and their leaves
have distance two. Hence H is on W and Z=b:2:0=0 is at distance
one. This supplies A(15,7;4,1).

Take c=9>8 and a=4. The selected vertices, in increasing
order, are s:0, l:0:0:0, b:1:0, s:2, l:2:0:0, l:2:0:1.
The complete incident list is:

| Selected incidence group | Differences |
|---|---|
| s:0--s:1, s:1--s:2, s:2--s:3 | 8,11,7 |
| s:0--b:0:0, b:0:0--l:0:0:0 | 5,6 |
| s:1--b:1:0, b:1:0--l:1:0:0 | 10,9 |
| s:2--b:2:0, b:2:0--l:2:0:0, b:2:0--l:2:0:1 | 12,13,14 |

These are all edges meeting the selected highs. The four
remaining edges are s:3--s:4, s:3--b:3:0 and both fourth
terminal edges, of weights 3,2,4,1. Thus the complete premise
is [c-a,14]=[5,14]. The evidence rechecks the already retained
seed and this predicate without rerunning its historical search.

## Exact normalized prefix

Fix exact integers q>=1, t>=2 and K>=2, excluding Booleans.
Apply the [general-host insertion theorem and compatibility](ALPHA_UPPER_BLOCK_GENERAL_HOST.md)
with h=q-1 first leaves named l:0:0:j for 1<=j<q and k=t-2
third leaves named l:2:0:j for 2<=j<t. By the named compatibility
proof either order gives the following labels, before any high
shift.

| Named vertices | Normalized labels |
|---|---|
| s:0,s:1,s:2,s:3,s:4 | q+8,1,q+11,5,8 |
| b:0:0,l:0:0:0 | 4,q+9 |
| l:0:0:j, 1<=j<q | 8+j |
| b:1:0,l:1:0:0 | q+10,2 |
| b:2:0 | 0 |
| l:2:0:j, 0<=j<t | q+12+j |
| b:3:0,l:3:0:0,l:3:0:1 | 7,3,6 |

In particular the original first terminal is shifted from 10.
The additional first names get 8+j from the insertion band.
The old third terminals rise from 13,14 by h, and their new
neighbors continue in that same label band from q+14.
The old lows occupy [0,6] and the two unselected highs are 7,8.
The new first terminals fill [9,q+7], the six translated old
highs fill [q+8,q+13], and the additional third terminals
fill [q+14,q+t+11]. These are consecutive disjoint blocks.

The four old unselected edges keep [1,4]. The fresh first
edges have weights [5,q+3], the old selected incidences
gain h and give [q+4,q+13], and the fresh third edges have
weights [q+14,q+t+11]. All weights are attained once on
the exact original incidences, with each edge crossing
the same cut. At q=1 the new first bands are empty. At
t=2 zero-host growth is the identity. The physical
ports, hosts and W stay as above. Thus on the exact
prefix `[[q],[1],[t],[2],[]]` of order q+t+12 we have
A(q+t+12,7;4,1) with threshold q+8. Exactly the old
six selected highs and the fresh third leaves meet the
threshold, with complete incident spectrum [q+4,q+t+11].

## High shift, original suffix, and scope

The full exact target `[[q],[1],[t],[2]]+[[]]*(K+1)`
has order K+q+t+12 and m=K+q+t+11 edges. The only
unassigned vertices after the prefix are s:5 through
s:(K+4). They have only the consecutive original path
incidences from s:4, with sole crossing s:4--s:5.

Raise every normalized high by K. The used labels are
[0,6] and [K+7,m]. Each prefix edge gains K on its high
endpoint, so the used differences are exactly [K+1,m].
Hence R=[7,K+6], D=[1,K], and physical s:4=K+8, two
above the maximum of R.

The retained [C_K recurrence](B2_NONADJACENT_CONSUMER.md#construction-and-proof)
has first entry K+1, suffix entries 0..K-1 once each
and all K differences 1..K, including its recursive
bridge. It terminates by decreasing K by three to 2,
3 or 4. Translate by 7 so its first label is the
already assigned K+8. Apply the remaining entries
in order to s:5 through s:(K+4). This makes K assignments,
preserves the prefix, fills R, and consumes D on those
original edges. The evidence first checks the actual
B4 boundary and calls only the unchanged numeric helper,
because the public B2 completion helper uses s:2.

This proves ordinary gracefulness on the stated domain.
At K=2 the path labels (10,8,7) have endpoints in one
bipartition class bracketing the middle label, so a
threshold cannot separate the classes for this labeling.
At K=1 the exact interface would leave R={7}, D={1} and
s:4=9, giving difference 2 on the sole unfinished edge.
This only excludes that interface. The
[direct q=1 singleton](B4_THIRD_ZERO_HOST_K1_DIRECT.md)
and [t=1 Q112 branch](B4_FOURTH_2_SUPPLY.md) retain their
own resource contracts. At q=1 the normalized formula
and physical completion agree pointwise with the retained
(1,1,t,2) nonadjacent construction.

The proof gives the unbounded quantifiers. The
[bounded executable evidence](../evidence/validation/B4_UNPADDED_Q1T2_001/README.md)
covers the six declared new targets, one retained seed
recheck, one retained completed control, and same-target
comparisons. No historical search is replayed or new
public route introduced. Broader second-branch growth
and q>1,K=1 with varying third branch remain separate.
