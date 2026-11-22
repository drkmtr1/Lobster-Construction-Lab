# B4-12T2-K1-ROOTED-CORE-001

## Retained original and a single ordinary insertion

Use the named core `[[1],[1],[],[2],[],[]]` from the
[retained direct proof](B4_THIRD_ZERO_HOST_K1_DIRECT.md#fixed-rooted-core-and-lift)
and its [certificate](../evidence/validation/B4_THIRD_ZERO_HOST_K1_DIRECT_001/validation/core_certificate.json).
It has six spine vertices, three centers and four terminals,
hence 13 vertices and 12 edges. The spine s:0 through s:5
has only its consecutive spine edges, with centers at
sections 0,1,3 and their original l:i:0:j attached there.

The retained spine labels are 7,0,12,1,10,4. The three
branch rows in name order are (3,2), (8,5) and (11,9,6).
These occupy [0,12] and their spine differences
(7,12,11,9,6) and attachment-then-terminal differences
(4,1), (8,3) and (10,2,5) occupy [1,12] once each.

Take B=b:1:0, b=8, c=2 and m=12. Exactly s:1=0 and
s:3=1 lie below the cut. Neither has a neighbor below the
cut. Their complete original incidences are the following
six distinct crossing edges.

| Actual edge | Difference |
|---|---:|
| s:0--s:1 | 7 |
| s:1--s:2 | 12 |
| s:1--b:1:0 | 8 |
| s:2--s:3 | 11 |
| s:3--s:4 | 9 |
| s:3--b:3:0 | 10 |

This is exactly [7,12]=[b-c+1,m]. At this threshold the
other six original edges are wholly above the cut. For
example, b:0:0--l:0:0:0 has labels 3,2 and weight 1.
Counting upper-side incidence would include that edge as
well, and shifting both endpoints leaves its weight 1.
The retained labeling is ordinary. For example, the
physical path with labels 2,3,7 rules out an alpha
separation since its same-class endpoints bracket 3.
Thus the [ordinary crossing-cut rule](ORDINARY_CUT_LEAF_INSERTION.md)
applies directly under its verified premise.

Set h=1 and add only l:1:0:1 at b:1:0 with label 2.
Each old label at least 2 rises by one. The new graph
is exactly `[[1],[2],[],[2],[],[]]`, with the prescribed
new leaf in section 1 and the empty section 2 unchanged.
The original three branch centers are at sections 0,1,3,
and s:2 is still an original spine vertex.

| Named vertices in order | New core labels a | Original edge differences |
|---|---|---|
| s:0,s:1,s:2,s:3,s:4,s:5 | 8,0,13,1,11,5 | 8,13,12,10,6 |
| b:0:0,l:0:0:0 | 4,3 | 4,1 |
| b:1:0,l:1:0:0,l:1:0:1 | 9,6,2 | 9,3,7 |
| b:3:0,l:3:0:0,l:3:0:1 | 12,10,7 | 11,2,5 |

The rows list consecutive spine weights and attachment-then-
terminal weights at each branch. The fourteen labels fill
[0,13] once and the thirteen original differences fill
[1,13] once. In particular the actual a(s:2)=13. At the
returned cut c'=3, the below-cut vertices are s:1,s:3 and
the fresh leaf. The six old crossing weights become
8,13,9,12,10,11 in the earlier table order. The new edge
has weight 7, so the full spectrum is [7,13] with updated
host 9. The same original spine witnesses the old and new
core, with the host one edge away. The label at physical
s:4 moves from 10 to 11, and s:5 from 4 to 5. Only one
core insertion is executed in the declared checks.

## Conditional lift from the maximum-rooted core

Suppose the exact 14-vertex deleted-third core above is
independently supplied with any graceful ledger a having
actual a(s:2)=13. For each exact integer t>=3, exclude
Boolean values and translate all core labels by one. Put
zero at the restored actual b:2:0. Assign l:2:0:j label 15+j
for 0<=j<t. Add precisely s:2--b:2:0 and b:2:0--l:2:0:j.
The new center attaches to the connected acyclic core by
one edge and the new terminals are leaves at that center.
All core incidences and section indices stay. This is the
exact `[[1],[2],[t],[2],[],[]]`, with t+15 vertices and
m=t+14 edges.

The center alone has label zero. The core uses [1,14] and
the third terminals use [15,t+14], giving a complete
bijection on [0,m]. The old weights stay [1,13]. Because
the actual original s:2 now has label 14, its new
attachment gives weight 14. Each third terminal edge has
the label of its terminal as difference, giving [15,t+14].
These three disjoint weight bands exhaust [1,m].
The displayed new core discharges this conditional premise.
The same translation used for the [earlier first-growth
rooted core](B4_Q1T2_K1_ROOTED_CORE.md) had a different
deleted-third profile. The [second-growth rooted core](B4_1R22_K1_ROOTED_CORE.md)
instead deletes section 1 and supplies a root zero. Here
neither the lift nor its supplied core requires an alpha cut.

## Direct singleton and witnesses

Use the fixed core ledger restricted to vertices other
than s:5. Translate those labels by one and assign the
third branch directly as above. This assigns exactly
the original vertices other than s:5, without running a
full-target construction first. Only s:4 is adjacent
to s:5, so the sole pending and crossing edge is s:4--s:5.

The label partition omits just a(s:5)+1 from [0,m],
and the difference partition omits just the original
weight |a(s:4)-a(s:5)| from [1,m]. Hence the general
interface uses those respective singleton values at
physical s:4=a(s:4)+1. With the exhibited core these are
R={6}, D={6} and actual s:4=12, independent of t.
Assign s:5=6. Its original edge uses |12-6|=6 and
every prefix assignment stays fixed.

The original spine s:0--s:1--s:2--s:3--s:4 witnesses
the prefix. Appending s:5 gives the full witness.
All centers remain one edge from the appropriate
spine vertex and all terminals two edges away through
their center. The construction terminates after the
fixed core-prefix assignments, the center and t leaves,
and one final assignment. No interval consumer is
needed for this singleton.

## Third-branch finite growth

In the completed labeling at t the maximum is t+14.
The next terminal l:2:0:t receives 15+t, the next
maximum. Its edge from the same original b:2:0=0
has that difference and all old labels and weights
stay. The new graph just attaches that leaf to the
same center and preserves the full spine witness.
Induction for a finite batch assigns each next name
its unique value 15+j, without moving previous labels.
Any finite subdivision into successive batches
therefore gives the same labeling and incidences
pointwise in the prescribed name order. The empty
batch is the identity.

On the declared t=5 target, the direct formula, one
batch of two from t=3, and two batches through the
declared t=4 give the same named labels and incidences,
including labels 18,19 for l:2:0:3 and l:2:0:4. This
comparison adds zero cases.

## Exact all-positive selection rule

For positive integers t,K on the exact ordered
`[[1],[2],[t],[2]]+[[]]*(K+1)`, select the following.

| Range | Supplier and interface |
|---|---|
| t=1, all K>=1 | [Retained QR12](B4_UNPADDED_QR12.md) at q=1,r=2, with R=[8,K+7], D=[1,K], s:4=K+8, adjacent. |
| t=2, all K>=1 | At K=1 use [the retained direct singleton](B4_1R22_K1_ROOTED_CORE.md) at r=2 with R={5}, D={5}, s:4=10. At K>=2 use [the retained 1R22 supplier](B4_UNPADDED_1R22_SUPPLIER.md) at r=2 with R=[8,K+7], D=[1,K], s:4=K+9, nonadjacent. |
| t>=3, K>=2 | [Retained 12T2 zero-host construction](B4_12T2_ZERO_HOST_SUPPLIER.md) with R=[8,K+7], D=[1,K], s:4=K+9, nonadjacent. |
| t>=3, K=1 | The direct singleton proved here, R={6}, D={6}, s:4=12. |

These disjoint cases exhaust all positive integers t,K for
the exact ordered family and prove ordinary gracefulness.
Broader second-branch growth with the third branch varying,
arbitrary B4 and universal coverage remain separate.

[Bounded evidence](../evidence/validation/B4_12T2_K1_ROOTED_CORE_001/README.md)
rechecks the one retained core, supplies one new core
certificate and checks the four declared targets. The
arithmetic audit and batch comparison add no cases.
