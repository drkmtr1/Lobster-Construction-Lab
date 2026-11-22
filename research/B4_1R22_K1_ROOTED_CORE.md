# B4-1R22-K1-ROOTED-CORE-001

## Exact core and construction

The core C has ordered original profile `[[1],[],[2],[2],[],[]]`.
Its six spine vertices s:0 through s:5 retain their five consecutive
edges. The centers b:i:0 for i=0,2,3 attach to their own s:i. Their
respective terminal counts are 1,2,2, with original names l:i:0:j.
This is a tree with 14 vertices and 13 edges. Section 1 has no
branch and s:1 remains present. The only prescribed label is
a(s:1)=0.

Choose s:0=13 and s:2=10 at the neighbors of zero. Give the first
center and leaf labels 1 and 12, realizing weights 12 and 11.
The third center at 2 and its leaves at 9 and 11 supply 8,7,9
on their attachment and leaf edges. Thus the weights from 7
through 13 are accounted for. The unassigned right side has
labels 3,4,5,6,7,8 available and needs weights 1 through 6.
Choose s:3=4 for weight 6 at s:2 and s:4=8 for weight 4 at
s:3. Then s:5=3 gives weight 5 and the center b:3:0=7 with
leaves 5 and 6 gives weights 3,2,1. The ledger is direct
arithmetic on the exact core. It uses no target solution,
isomorphism or computational enumeration.

| Named vertices in order | Core labels a | Original-edge weights |
|---|---|---|
| s:0,s:1,s:2,s:3,s:4,s:5 | 13,0,10,4,8,3 | 13,10,6,4,5 |
| b:0:0,l:0:0:0 | 1,12 | 12,11 |
| b:2:0,l:2:0:0,l:2:0:1 | 2,9,11 | 8,7,9 |
| b:3:0,l:3:0:0,l:3:0:1 | 7,5,6 | 3,2,1 |

The first row lists spine weights in spine order. Each branch row
lists its attachment followed by the terminal weights in name
order. The fourteen displayed labels exhaust [0,13] once, and
the thirteen displayed weights exhaust [1,13] once. This proves
the sole root pin and a graceful bijection on the named core.

For comparison, the [earlier rooted-core task](B4_Q1T2_K1_ROOTED_CORE.md)
deletes section 2 and uses a maximum at its attachment spine
vertex. Here the deleted section is 1 and the lift needs zero
at its physical spine vertex. The [normalized 1R22 construction](B4_UNPADDED_1R22_SUPPLIER.md)
has only the spine through s:4. Its r=1 arithmetic base, after
deleting the second center and leaf of weights 13 and 14 and
subtracting one from each remaining label, gives a 13-vertex
alpha prefix of the present core with s:1=0 and exit s:4=7.
Its low size is 6. The one-step high shift leaves label 6
and difference 1 at exit 8, whose distance to 6 is two.
That particular prefix transport fails at K=1. The full
14-vertex ledger above supplies a different direct route.

## Conditional lift and application

Suppose the exact core C is independently supplied with any
graceful labeling a and a(s:1)=0. Let r be an exact integer
r>=2, excluding Boolean values. Keep every original core
incidence and add b:1:0 at s:1, then r named leaves
l:1:0:j for 0<=j<r at b:1:0. These are exactly the missing
vertices and edges in `[[1],[r],[2],[2],[],[]]`. They
preserve connectivity and acyclicity. The full graph has
r+15 vertices and m=r+14 edges.

Use f(v)=a(v)+r on every core vertex. Assign r+14 to b:1:0,
0 to l:1:0:0, and r-j to l:1:0:j for 1<=j<r. The labels
on the second leaves are exactly [0,r-1], those on the
translated core are [r,r+13], and the second center alone
takes r+14. These disjoint bands give every label in [0,m]
once on an original vertex.

Each core edge keeps its difference, giving [1,13].
The actual s:1 has label r, so its attachment to b:1:0
has weight (r+14)-r=14. Each nonzero second terminal of
index j gives (r+14)-(r-j)=14+j, hence [15,r+13].
The original second terminal at zero has edge weight r+14.
These disjoint bands exhaust [1,m] once each on the actual
edges. At r=2 the second leaves take 0 and 1, the core
takes [2,15], and the center takes 16. The added weights
are 14,15,16, with just the single nonzero terminal weight
15. Neither the lift nor its premise requires an alpha
cut. The explicit core above discharges the premise and
makes the lift a supplier for every r>=2.

## Direct singleton and physical witness

In the partial construction use the fixed ledger directly
on C without s:5, translating by r, then supply the
second branch by the stated formulas. There is no call
to a full-target labeling procedure. The only unassigned
vertex is s:5. The last two sections are empty, and s:5
has only its original spine neighbor s:4. Thus the sole
pending edge and sole crossing edge are s:4--s:5.

In the full alphabet [0,r+14], the supplied labels are
[0,r+14] minus {r+a(s:5)} by the label partition. The
assigned-edge weights are [1,r+14] minus
{|a(s:4)-a(s:5)|} by the difference partition. With the
fixed ledger this gives R={r+3}, D={5}, and physical
s:4=r+8. Assign the single label r+3 to s:5. Its original
edge has weight |(r+8)-(r+3)|=5 and consumes both resources
while preserving all prefix labels. That weight follows
from the ledger. There is no interval consumer or prescribed
edge weight in the core premise.

The actual path s:0--s:1--s:2--s:3--s:4--s:5 witnesses
the full topology. Every center is one edge from its own
spine vertex and every terminal is two edges from the
spine through its own center. These original incidences
persist for every r. Prefix supply requires only the
fixed ledger entries and r prescribed terminal labels.
Completion makes one further assignment.

## Repeatable second-branch growth

Given the supplied labeling for r and a nonnegative integer h,
keep the original zero terminal l:1:0:0 fixed and add h to
every other old label. Attach precisely the new names
l:1:0:(r+i), for 0<=i<h, at the same physical b:1:0 and assign
h-i. These new labels [1,h] lie between zero and the shifted
positives [h+1,r+h+14]. All old edges keep their difference
except the unique edge to the zero terminal. Its difference
becomes the new maximum r+h+14. The new terminal differences
are (r+h+14)-(h-i)=r+14+i, filling [r+14,r+h+13] between
the unchanged old [1,r+13] and the maximum. For h=0 the new
band is empty and the operation is the identity.

The physical maximum remains at b:1:0, the original terminal
remains zero, and each added vertex is a leaf at that center,
two edges from the same spine. Every old incidence stays.
The translated old core acquires shift r+h. An old positive
second terminal j gets (r-j)+h, and each new one at j=r+i
gets h-i=(r+h)-j. These are exactly the direct formulas
at r+h. In particular, after a later batch each earlier
nonzero new leaf is raised by that batch size, giving its
final direct-formula label. Induction proves pointwise
agreement for any finite batch partition in prescribed name
order. Each batch terminates after adding its h named leaves
and a finite number of assignments to the old vertices.

The finite check compares r=4 directly, r=2 followed by
one batch of two, and r=2 through the declared r=3 by
two batches of one. All are comparisons on the same declared
r=4 original. No intermediate original beyond the declared
four cases is required.

## Exact all-positive selection rule

For integer r,K>=1 on the ordered profile
`[[1],[r],[2],[2]]+[[]]*(K+1)`, choose the following cases.

| Case | Source and interface |
|---|---|
| r=1, K>=1 | At K=1 use the [retained direct singleton at t=2](B4_THIRD_ZERO_HOST_K1_DIRECT.md), R={5}, D={6}, s:4=11. At K>=2 use the [retained nonadjacent third zero-host supply at t=2](B4_THIRD_ZERO_HOST_NONADJACENT.md), R=[7,K+6], D=[1,K], s:4=K+8. |
| r>=2, K>=2 | [Retained normalized 1R22 supplier](B4_UNPADDED_1R22_SUPPLIER.md), R=[r+6,r+K+5], D=[1,K], s:4=r+K+7, followed by its original-path completion. |
| r>=2, K=1 | Present direct singleton, R={r+3}, D={5}, s:4=r+8. |

The first row uses the two retained interfaces for the exact
r=1 family. The three outer cases are disjoint and exhaustive,
so they establish ordinary gracefulness of this exact ordered
family for all positive integers r,K. Growth of the third
branch with r>=2 and general B4 coverage remain separate.

[Bounded evidence](../evidence/validation/B4_1R22_K1_ROOTED_CORE_001/README.md)
covers the one auxiliary core and four declared completed
targets. The same-certificate audit and batch comparisons
add no cases. The proof supplies the parameter quantifiers,
and no search, enumeration or historical replay is used.
