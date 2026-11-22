# B4-THIRD-ZERO-HOST-NONADJACENT-001

## Exact seed question and outcome

The original prefix `[[1],[1],[2],[2],[]]` has spine s:0 through
s:4, four centers b:i:0 on their original s:i, and terminals at
those centers in counts 1,1,2,2. The four spine, four attachment
and six terminal edges give 15 named vertices and 14 edges. Its
canonical digest is
`a8fc14f45ba08e88fb3c53ce0611b2886c5cc0250dcc0985070e92de804595dc`.

The low vertices are s:1, s:3, b:0:0, b:2:0, l:1:0:0,
l:3:0:0 and l:3:0:1, each initially allowed 0..6.
The high vertices are s:0, s:2, s:4, b:1:0, b:3:0,
l:0:0:0, l:2:0:0 and l:2:0:1, each initially allowed 7..14.
The only pins are b:2:0=0 and s:4=8. The saved query used
the unchanged first-witness DFS once with one worker, 15 vertices,
100,000 assignment nodes, five cooperative seconds and a separate
2,000,000-byte result cap. The optional generic max_states field
is 20,000 and unused by DFS. There is no root pin, fixed-low
inheritance, terminal-order convention or symmetry quotient.

The [retained nonadjacent control](../evidence/validation/B4_FOURTH_2_SUPPLY_001/diagnostic_results/1122-nonadjacent.json) on
the same original was rechecked without search. It uses all labels
0..14 and weights 1..14, crosses the same cut, and puts 8 at the
actual exit. Its b:2:0=1 is the only mismatch to the new
pins. It is a control for the graph and exit.

The [new original-bound query](../evidence/validation/B4_THIRD_ZERO_HOST_NONADJACENT_001/query_record.json)
returned SAT after 2,368 nodes and 0.020261199999367818 s.
It reports exhausted=false, count=null, count_lower_bound=1.
Both the original-target checker and independent arithmetic audit
verify the new witness on the exact original. An exact count of
solutions remains unknown.

## Explicit seed and witness

The following fixed ledger supplies a seed independently of
running a solver. In each branch row, the differences are listed
in attachment-then-terminal order, and the terminal names are
in increasing index order.

| Named vertices in order | Labels | Original-edge differences |
|---|---|---|
| s:0, s:1, s:2, s:3, s:4 | 9,1,12,5,8 | 8,11,7,3 |
| b:0:0, l:0:0:0 | 4,10 | 5,6 |
| b:1:0, l:1:0:0 | 11,2 | 10,9 |
| b:2:0, l:2:0:0, l:2:0:1 | 0,13,14 | 12,13,14 |
| b:3:0, l:3:0:0, l:3:0:1 | 7,3,6 | 2,4,1 |

The entries on the seven named lows give 0..6 once. The other
eight give 7..14 once. All fourteen original edges are in the
ledger, each crosses the cut, and their displayed differences
are exactly 1..14 once. Thus the fixed labels give an alpha
graceful bijection on this named seed.

Take L=b:0:0=4, U=s:4=8 and actual W given by
b:0:0--s:0--s:1--s:2--s:3--s:4. The first terminal
is one edge from W. Each other center is one edge away,
and each of its terminals is two edges away. In particular
the zero host z=b:2:0 is exactly one edge from W through
its actual neighbor s:2. The shorter path beginning at the
third center would leave the first terminal four edges
from its closest vertex s:2. The specified W is used.

The supplied state is A(15,7;4,1) in the
[retained relation notation](../references/upstream/mdl/N241_relational_ports.md).
The returned low offset x=4 comes from the ledger
and was free in the search. The host is distinct from L.
No relational join is required for this construction.

## Symbolic extension and both inventories

Fix integers t>=2 and K>=2. Apply the accepted
[zero-host extension](ALPHA_ZERO_HOST_LEAF_EXTENSION.md)
with h=t-2. Its fresh names are l:2:0:j, 2<=j<t,
attached only at z=b:2:0. The order index is i=j-1,
so label 15+i-1 is 13+j. All original labels and
edges stay. The new high labels and their weights
are 15..t+12 once each because the host is zero.
For t=2 the list is empty. The exact enlarged normalized
prefix is `[[1],[1],[t],[2],[]]` with order t+13 and
state A(t+13,7;4,1). The original cut, actual ports,
zero host and W persist; each fresh leaf is two edges
from W through the third center.

The full target has profile
`[[1],[1],[t],[2]]+[[]]*(K+1)`, order K+t+13 and
edge count m=K+t+12. Once the vertices through s:4 with
all branches are assigned, the pending vertices are precisely
s:5,...,s:(K+4). The empty sections supply no branches or
terminals. The pending incidences are the consecutive original
spine edges on the K-edge path from s:4, with sole prefix
crossing s:4--s:5.

Raise every normalized high by K; keep the seven lows.
The used labels become [0,6] and [K+7,K+t+12].
Each original prefix edge crosses the seed cut, so
its difference rises by K and the used differences
are [K+1,K+t+12] once each. Relative to the original
full alphabet, the unused inventories are R=[7,K+6]
and D=[1,K]. Physical s:4 had label 8 and now has K+8,
two above the top of R. This is the nonadjacent interface.

## Original path completion and scope

The [accepted recurrence](B2_NONADJACENT_CONSUMER.md#construction-and-proof)
uses C_2=(3,1,0), C_3=(4,1,0,2), and C_4=(5,1,2,0,3).
For K>=5 let C_(K-3)=(K-2,x_1,...,x_(K-3)). Then

```text
C_K=(K+1,1,K-1,0,K-2-x_1,...,K-2-x_(K-3)).
```

The three bases use 0..K-1 once in their suffix, with
differences 1..K once. Inductively the smaller suffix
uses 0..K-4; reflection fills 2..K-2, complementary to
1,K-1,0 among 0..K-1. The first three differences
are K,K-2,K-1. The remaining differences, including
the bridge from 0, are those of the reflected smaller
path because its first entry K-2 reflects to 0. They
exhaust 1..K-3. The argument decreases by three to a base.

Translate by 7. Its first label 7+(K+1)=K+8 equals
the existing s:4. For 1<=i<=K assign s:(4+i) the
entry 7+C_K[i], taking the port index as 0. All K
new labels exhaust R, and all original path edges
exhaust D. Prefix labels are unchanged. These
complementary sets prove the full bijection on 0..m
and full original-edge spectrum 1..m. The recurrence
terminates and there are exactly K suffix assignments.
This is the same sequence arithmetic on the physical
B4 path. The B2 public graph helper remains tied to s:2.
The evidence uses the retained 111T pattern of checking
the B4 boundary before calling its sequence generator.

This proves ordinary gracefulness for t>=2,K>=2 on
the exact stated original profile. At K=2, the actual
suffix through the port has labels (10,8,7).
Its two end vertices lie in one bipartition class and
the middle vertex in the other. The extremes 7 and 10
straddle 8, so a threshold cannot separate those classes
in this labeling. At K=1 the prescribed interface
would leave R={7}, D={1}, s:4=9 and only the original
edge of difference |9-7|=2. This excludes only this
interface at K=1. The [retained Q112 construction](B4_FOURTH_2_SUPPLY.md)
at q=1 covers t=1 under its own adjacent contract.
The retained adjacent 1122 control has a different
host label and supplies its own adjacent interface.
Other K=1 coverage for t>=3 and more general branch
sizes remain separate questions.

The fixed ledger, conditional extension and recurrence
give the quantified construction. The finite evidence
checks the four declared cases and weighs no further
supplier claims. No public route is added.
