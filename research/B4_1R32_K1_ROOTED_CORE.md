# B4-1R32-K1-ROOTED-CORE-001

## Retained ordinary core and complete cut premise

The [retained 14-vertex core](B4_12T2_K1_ROOTED_CORE.md#retained-original-and-a-single-ordinary-insertion)
is exactly `[[1],[2],[],[2],[],[]]`. It has six spine
vertices s:0 through s:5, five consecutive spine edges,
centers at sections 0,1,3 and their named terminal leaves
in counts 1,2,2. The empty third section has s:2 and no
branch center. The original graph and certificate are
preserved separately and the bounded run rechecks them
once, without replaying their construction.

| Named vertices in order | Retained labels | Original edges in order, by weight |
|---|---|---|
| s:0,s:1,s:2,s:3,s:4,s:5 | 8,0,13,1,11,5 | 8,13,12,10,6 |
| b:0:0,l:0:0:0 | 4,3 | 4,1 |
| b:1:0,l:1:0:0,l:1:0:1 | 9,6,2 | 9,3,7 |
| b:3:0,l:3:0:0,l:3:0:1 | 12,10,7 | 11,2,5 |

The first weight row gives the spine weights in order.
Each branch row gives its attachment and then terminal
weights in name order. The labels and weights fill
[0,13] and [1,13] once, respectively.

At c=3, the vertices below the cut are exactly s:1=0,
s:3=1 and l:1:0:1=2. They have no edges to one another.
Their entire original incidence ledger is:

| Original crossing edge | Weight |
|---|---:|
| s:0--s:1 | 8 |
| s:1--s:2 | 13 |
| s:1--b:1:0 | 9 |
| s:2--s:3 | 12 |
| s:3--s:4 | 10 |
| s:3--b:3:0 | 11 |
| b:1:0--l:1:0:1 | 7 |

All seven cross. The other six edges are wholly above
the cut. They are s:4--s:5, both first-branch edges,
b:1:0--l:1:0:0, and both fourth terminal edges, with
weights 6,4,1,3,2,5. Counting upper-side incidences
would include all thirteen edges, whereas the required
complete crossing multiset is [7,13].
The original B=b:1:0 has label 9, hence
[b-c+1,m]=[7,13]. The spine s:0--s:1--s:2--s:3--s:4--s:5
witnesses the core, with B one edge away through s:1.
This discharges the premises of the
[ordinary crossing-cut insertion](ORDINARY_CUT_LEAF_INSERTION.md)
at the prescribed physical host.

## Parameterized core and finite closure

Let r>=3 be an exact integer, excluding Booleans. Use
h=r-2 in the retained rule. Labels below three stay,
and those at least three gain h. Add exactly the fresh
l:1:0:j for 2<=j<r at B. For global index j the local
one-based fresh index is j-1, so the rule assigns
3+(j-1)-1=j+1. The name l:1:0:1 retains label 2.
All original core labels in full form are:

| Named vertices in order | Core labels a_r |
|---|---|
| s:0,s:1,s:2,s:3,s:4,s:5 | r+6,0,r+11,1,r+9,r+3 |
| b:0:0,l:0:0:0 | r+2,r+1 |
| b:1:0,l:1:0:0 | r+7,r+4 |
| l:1:0:j for 1<=j<r | j+1 |
| b:3:0,l:3:0:0,l:3:0:1 | r+10,r+8,r+5 |

Each fresh leaf is connected only to the same B and
creates no cycle. All old named incidences remain. The
result is exactly `C_r=[[1],[r],[],[2],[],[]]`, with
r+12 vertices and r+11 edges. In the disjoint label
partition the retained below-cut labels are [0,2], the
new leaves fill [3,r], and the shifted retained labels
fill [r+1,r+11]. In particular the maximum r+11 remains
at physical s:2.

The six old noncrossing weights stay [1,6]. Each new
leaf gives weight (r+7)-(j+1)=r+6-j, covering [7,r+4]
once. The seven old crossings gain r-2 and cover
[r+5,r+11]. These disjoint groups exhaust all core
weights. At r=3 the only new weight is 7. The updated
cut c_r=r+1 has exactly the same original upper vertices
and all new leaves below it. Its crossing set consists
of the seven old crossings and the new leaf edges,
giving [7,r+11] once. Its noncrossing set remains the
six old edges with [1,6], and the actual B label r+7
gives the required lower bound (r+7)-(r+1)+1=7.

At any intermediate r the same witness persists, with
B one edge away and each new leaf two. A further batch
of h>=0 shifts just the values at least c_r, keeping
all already inserted leaves below c_r. The j=r+i-1
fresh name, for local i>=1, receives c_r+i-1=j+1.
The shifted old retained values gain h. Thus the core
formula and returned cut and host are precisely those
at r+h. This also describes the starting core at r=2,
where the fresh range is empty. The ordinary lemma's
finite closure at this cut gives pointwise agreement
for any batches in the specified order. No alpha
state is used.

## Fixed-size lift and original singleton

Translate each core value by one. Add b:2:0=0 at the
original s:2 and its three terminals l:2:0:j at that
center with labels r+13+j for 0<=j<3. A new center with
one attachment and its three leaves preserves the tree.
Only these four incidences are added. The exact full
profile is `[[1],[r],[3],[2],[],[]]`, with n=r+16 and
m=r+15. The disjoint label blocks are {0}, [1,r+12],
and [r+13,r+15]. Each translated core edge keeps its
weight in [1,r+11]. The actual physical s:2 has label
r+12, so its edge to zero gives r+12. The three terminal
edges give [r+13,r+15]. Both alphabets are exhausted
once and all original branch names and incidences stay.

Supply the direct prefix by applying the displayed
core formula only on vertices other than s:5, translating
them by one and then supplying that exact third branch.
This constructs the prefix independently. Its sole
unassigned original vertex is s:5, with only original
neighbor s:4. The full label partition omits exactly
a_r(s:5)+1 and the full difference partition omits exactly
|a_r(s:4)-a_r(s:5)|. Hence R={r+4}, D={6} at physical
s:4=r+10. Assign s:5=r+4. Its original edge has weight
|(r+10)-(r+4)|=6 and consumes both resources without
altering any prefix label.

The original spine through s:4 witnesses the prefix.
Extending it to s:5 witnesses the full graph. Each center
is one edge from its original spine vertex and each
terminal two edges away through its own center. No
terminal attaches beyond s:3. The construction is
finite, with a fixed original ledger, r-2 prescribed
second additions, the fixed third branch and one
singleton assignment.

## Completed-target cut and agreement of both growth orders

Use d_r=c_r+1=r+2 in the completed target. Translating
a core label by one preserves its side of the cut.
The four restored edges cross, since b:2:0 is zero
and s:2=r+12 and the terminal labels r+13 through
r+15 exceed d_r. The complete crossing spectrum is
[7,r+15], from the core crossings [7,r+11] and the
four new weights. The six original noncrossing weights
remain [1,6]. The actual B=r+8 gives
f(B)-d_r+1=7. The host still lies one edge from the
original full spine. Thus the completed graceful target
satisfies the ordinary insertion premise at this cut.

For a further batch h>=0, shift exactly the old labels
at least d_r by h. The freshly named second leaf at
global index j=r+i-1 gets d_r+i-1=j+2. The previously
inserted second terminals have labels below d_r, hence
stay fixed. The ordinary rule returns cut r+h+2 and
host r+h+8, with crossing spectrum [7,r+h+15] and
noncrossing spectrum [1,6]. The resulting labels are
the full formula at r+h. The port at physical s:4 gains
h. Since s:4=r+10 and s:5=r+4 are both above or at d_r,
the old final edge stays noncrossing and its difference
stays six. The direct singleton at r+h has R={r+h+4},
D={6}, s:4=r+h+10. The insertion lemma here acts on
the completed tree, while the prefix uses its separate
formula and independently computed resources.

More explicitly, for an old core vertex v,
a_r(v)>=r+1 exactly when a_r(v)+1>=r+2. Thus either
order shifts exactly the same core labels by h and
translates them by one. The new second terminal's
core label j+1 translates to j+2, its value in direct
full growth. The third center stays zero in either
order, and each of the three third terminal labels
r+13+j gains h in full growth, matching its lifted
value at r+h. Both orders attach the same names at
the same B and restore the same third branch. They
keep the same physical witness and final edge. This
proves pointwise equality on the named original and
all its incidences for one batch. Finite named-batch
closure on both sides gives equality for every finite
subdivision in the same name order.

## Exact selection and evidence scope

For all positive integers r,K on
`[[1],[r],[3],[2]]+[[]]*(K+1)`, the disjoint cases are:

| Range | Source and physical interface |
|---|---|
| r=1,K=1 | [Retained third-zero-host singleton](B4_THIRD_ZERO_HOST_K1_DIRECT.md) at t=3, with R={5}, D={6}, s:4=11. |
| r=2,K=1 | [Retained 12T2 rooted-core singleton](B4_12T2_K1_ROOTED_CORE.md) at t=3, with R={6}, D={6}, s:4=12. |
| r>=3,K=1 | This direct singleton, with R={r+4}, D={6}, s:4=r+10. |
| K>=2 | [Accepted 1R32 selection](B4_1R32_MINIMUM_HIGH_SUPPLIER.md#exact-coverage-and-bounded-evidence). For r=1 use R=[7,K+6], s:4=K+8; for r=2 use R=[8,K+7], s:4=K+9; for r>=3 use R=[r+6,r+K+5], s:4=r+K+7. Each uses D=[1,K] on the original nonadjacent suffix. |

The existing and new cases together prove ordinary gracefulness
for this exact ordered family. The new supplier holds the first,
third and fourth sizes fixed at 1,3,2. Simultaneous arbitrary
second and third sizes and broader profiles remain separate.

[Bounded evidence](../evidence/validation/B4_1R32_K1_ROOTED_CORE_001/README.md)
checks one retained core, three new cores and three completed
targets. Core r=5 comparisons use the retained r=2 core and
the declared r=3,4 stages. Full r=5 comparisons use lifts of
those core routes and completed growth from r=3, with r=4
as the existing intermediate. No completed r=2 case was
reconstructed or checked. The comparisons and independent
audit add zero graph cases.
