# B4-Q1T2-K1-ROOTED-CORE-001

## Exact core and the retained comparison

For an integer q>=2 let C_q have profile
`[[q],[1],[],[2],[],[]]`. The original spine has vertices s:0
through s:5 and its five consecutive edges. Three original centers
b:0:0, b:1:0 and b:3:0 attach at s:0, s:1 and s:3. Their terminal
leaves have original names l:i:0:j with counts q, 1 and 2,
respectively. Thus the core has q+12 vertices and q+11 edges.
It has no branch center at section 2. All notation below uses these
physical names.

The [retained q=1 core](B4_THIRD_ZERO_HOST_K1_DIRECT.md#fixed-rooted-core-and-lift)
gives b:0:0 label 3, s:2 label 12, and zero to s:1. Appending a
fresh maximum label 13 while holding those old labels would give
difference 10, already present. More generally, a graceful
rooted core with s:2 maximal must put zero at one of its two
neighbors, s:1 or s:3, to realize the maximum difference. The
ordinary [zero-host extension](B4_THIRD_ZERO_HOST_K1.md#conditional-ordinary-zero-host-extension)
therefore cannot grow the first branch by appending fresh maxima
with this root already maximal. Neither observation constrains
other graceful relabelings.

The upper-block arithmetic can apply to an ordinary graceful
labeling if the edges with exactly one endpoint at or above c
already use [c-a,m], where m is the old maximum and a<c is the
host label. With a shift of h on that block, each of those
differences grows by h and every other old difference stays.
The h fresh labels [c,c+h-1] give edge differences
[c-a,c-a+h-1] at the unshifted host. Together these give the
label and difference bijections for the larger tree. Here the
condition concerns crossing edges, since an edge with both
vertices above the cut keeps its difference. The retained
[general low-host upper insertion](ALPHA_UPPER_BLOCK_GENERAL_HOST.md)
uses alpha separation to make the complete incident set to its
selected highs the crossing set, and additionally preserves
witnessed alpha ports. The [lower-block rule](ALPHA_LOWER_BLOCK_LEAF_INSERTION.md)
also assumes alpha separation and uses an incident spectrum with
a different cut and host. The retained [R241](../references/upstream/mdl/N241_relational_ports.md)
joins two supplied compatible witnessed alpha states along a
stipulated physical edge. The ordinary core proof needs none of
these alpha-state hypotheses or an application of R241.

Here is why the single-cut extension with the retained labels
and fixed host 3 fails already for one added leaf. Put its label
at c and raise by one all old labels at least c. For each old
difference j in [1,12], let S(j) be 1 if it crosses the cut
and 0 otherwise, and set S(0)=0. The multiplicity of j after
insertion is 1-S(j)+S(j-1)+1_{j=c-3}. For gracefulness it must
be 1, forcing the crossing spectrum to be [c-3,12].
Every possible integer c with 3<c<=13 violates that condition:

| c | Required crossing spectrum failure on the retained core |
|---|---|
| 4, 5 | Weight 2 is required but both labels 9 and 11 are at or above c. |
| 6 | Weight 5 is required but both labels 6 and 11 are at or above c. |
| 7 | Weight 3 is outside the required band but the edge with labels 5 and 8 crosses. |
| 8, 9 | Weight 7 is required but both labels 0 and 7 are below c. |
| 10, 11 | Weight 2 is outside the required band but the edge with labels 9 and 11 crosses. |
| 12, 13 | Weight 10 is required but both labels 1 and 11 are below c. |

This rejects that retained-label template only. It follows
from the fixed edge ledger and uses no labeling search.

## Relabeled core and formula

A different ledger on the same q=1 topology is obtained by
reserving the largest two labels for s:2 and s:0. Set
s:3=0, s:1=1, b:0:0=2, s:2=12 and s:0=11. These two
selected vertices have four incident edges with differences
12,11 and 10,9, respectively. The cut c=11 has host a=2,
so the desired crossing band starts at 9. The remaining
entries in the table supply the other differences directly.
In particular the old first terminal receives 10 for
difference 8 and the second center receives 8 for difference 7.

| Named vertices in order | Labels r_q |
|---|---|
| s:0, s:1, s:2, s:3, s:4, s:5 | q+10, 1, q+11, 0, 5, 4 |
| b:0:0, l:0:0:0 | 2, 10 |
| l:0:0:j for 1<=j<q | 10+j |
| b:1:0, l:1:0:0 | 8, 6 |
| b:3:0, l:3:0:0, l:3:0:1 | 3, 9, 7 |

At q=1 the row of additional first leaves is empty. The fixed
labels outside s:0 and s:2 use [0,10] once. The new first
terminals fill [11,q+9] and the two shifted vertices carry
q+10 and q+11. These blocks have sizes 11, q-1 and 2 and form
a bijection on all q+12 named vertices. In particular the
maximum is at physical s:2 for every q>=2.

The table accounts for all actual edges. The eight fixed
edges and the four edges crossing the selected cut are
listed explicitly.

| Original edge or group | Difference |
|---|---|
| s:4--s:5 | 1 |
| b:1:0--l:1:0:0 | 2 |
| s:3--b:3:0 | 3 |
| b:3:0--l:3:0:1 | 4 |
| s:3--s:4 | 5 |
| b:3:0--l:3:0:0 | 6 |
| s:1--b:1:0 | 7 |
| b:0:0--l:0:0:0 | 8 |
| b:0:0--l:0:0:j for 1<=j<q | 8+j |
| s:0--b:0:0 | q+8 |
| s:0--s:1 | q+9 |
| s:1--s:2 | q+10 |
| s:2--s:3 | q+11 |

The partition is [1,8], [9,q+7] and [q+8,q+11], each
weight once. For q=2 the middle band is the singleton {9}.
At q=1 it is empty and the old crossing band is [9,12].
Thus shifting the two vertices by q-1 and adding exactly
q-1 named first leaves produces the formula from the new
fixed arithmetic ledger. There is no full-target input,
canonical relabeling of the graph, or additional edge.
The assignment terminates after the fixed core entries and
the prescribed finite number of first-leaf entries.

## Lift and physical singleton

For exact integers q,t>=2, the original
`[[q],[1],[t],[2],[],[]]` adds the vertex b:2:0 and its t
terminal leaves to C_q. Retain every core vertex and incidence,
including the physical s:5. Translate each old label by one,
put b:2:0=0, and assign the prescribed names by
f(l:2:0:j)=q+13+j for 0<=j<t. The only new edges are the actual
s:2--b:2:0 attachment and the t terminal edges at that center.
All centers remain one edge from the same physical spine and
all leaves remain two edges away. This is a tree on q+t+13
vertices with m=q+t+12 edges.

The new zero, the translated core labels [1,q+12], and the
third terminal labels [q+13,m] give all labels [0,m] once.
Translation keeps the core spectrum [1,q+11]. The attachment
has weight q+12 because r_q(s:2)=q+11. The terminal
differences are precisely the t labels [q+13,m] at host zero.
These disjoint bands prove ordinary gracefulness. For example,
the path s:3--b:3:0--l:3:0:0 has lifted labels 1,4,10.
The endpoints lie in the same bipartition class and bracket
the center label, ruling out an alpha cut for this labeling.

Supply the prefix by giving these formulas only for vertices
other than s:5. The exact original target is part of the state.
The sole pending original incidence is s:4--s:5, and the
frontier consists only of physical s:4. The label complement is
R={r_q(s:5)+1}={5}. The difference complement is
D={|r_q(s:4)-r_q(s:5)|}={1}. The physical port has value
f(s:4)=r_q(s:4)+1=6. Assign s:5=5; the original edge has
weight |6-5|=1 and consumes both resources. The value 1
is a consequence of the exhibited core rather than an input
constraint. Every prefix label stays at its assigned value.

## Family coverage and validation scope

Together with the retained [direct q=1 singleton](B4_THIRD_ZERO_HOST_K1_DIRECT.md),
[Q112 at t=1](B4_FOURTH_2_SUPPLY.md), and
[Q1T2 at t>=2,K>=2](B4_UNPADDED_Q1T2.md), the result gives
ordinary gracefulness of `[[q],[1],[t],[2]]+[[]]*(K+1)`
for all positive integers q,t,K. Use Q112 when t=1,
the retained direct singleton when t>=2,K=1,q=1,
the new singleton when t>=2,K=1,q>=2, and the nonadjacent
Q1T2 supplier when t>=2,K>=2. Each case has its own
physical interface. Second-branch growth with third-branch
size at least two remains a separate proof obligation.

The [bounded evidence](../evidence/validation/B4_Q1T2_K1_ROOTED_CORE_001/README.md)
covers the four specified completed targets and the three
specified auxiliary cores. It corroborates the symbolic proof.
There is no new executable production route, solver call,
labeling enumeration or historical replay.
