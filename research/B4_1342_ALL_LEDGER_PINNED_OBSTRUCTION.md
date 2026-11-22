# B4-1342-ALL-LEDGER-PINNED-OBSTRUCTION-001

## Quantified claim and fixed physical graph

Let T be the original named tree with ordered profile
`[[1],[3],[4],[2],[]]`. It has five spine vertices, four original
centers and ten terminal leaves. Its edges are the four consecutive
spine edges, the four attachments s:i--b:i:0 for 0<=i<=3, and
the ten terminal edges b:i:0--l:i:0:j for the appropriate indices.
It has order 19 and 18 edges. Use the separately retained
[named original](../evidence/validation/B4_1342_UPPER_BLOCK_OBSTRUCTION_001/validation/originals/1342.json).

Let g be **any** normalized graceful alpha labeling of T with
low labels [0,8], high labels [9,18], and pins
`g(b:0:0)=1`, `g(b:2:0)=0`, and `g(s:4)=10`.
For each integer c in [11,18], let E_c consist of all original
edges meeting a vertex with label at least c and put s_c=|E_c|.

- **A.** For every such g and c, s_c differs from 20-c.
- **B.** For every such g and c and every integer h>=1, the prescribed
  upper-block shift and first-host insertion fails gracefulness.

The physical ports are L=H=b:0:0 and U=s:4. Their labels are 1 and
10, with y=1. The third zero host is Z=b:2:0. The named path
b:0:0--s:0--s:1--s:2--s:3--s:4 witnesses the tree within distance
two, with H on the path and Z one edge from s:2. Gracefulness
and the pins are consistent: the [retained normalized certificate](../evidence/validation/B4_1RT2_TWO_HOST_COMPATIBILITY_001/validation/normalized-r3-t4.json)
gives one such labeling. The argument below uses none of its
unpinned values.

## Forced physical alpha classes and degree counts

Starting from high s:4 and alternating along the original spine
forces s:0,s:2 high and s:1,s:3 low. At each branch the center is
opposite its spine vertex, and every terminal is opposite its own
center. Hence the exact high vertices and their full neighbor
lists are:

| High vertex | Original neighbors | Degree |
|---|---|---:|
| s:0 | s:1, b:0:0 | 2 |
| s:2 | s:1, s:3, b:2:0 | 3 |
| s:4 | s:3 | 1 |
| b:1:0 | s:1, l:1:0:0, l:1:0:1, l:1:0:2 | 4 |
| b:3:0 | s:3, l:3:0:0, l:3:0:1 | 3 |
| l:0:0:0 | b:0:0 | 1 |
| l:2:0:j, 0<=j<4 | b:2:0 | 1 each |

These are ten original named vertices. The nine lows are s:1,
s:3, b:0:0, b:2:0, the three terminals at b:1:0 and the two
at b:3:0. Every original edge has exactly one high endpoint.
The strict bound in the [general-host rule](ALPHA_UPPER_BLOCK_GENERAL_HOST.md#exact-state-and-incident-edge-hypothesis)
is p+y=10<c<=18. All selected vertices are high, and physical
s:4 cannot be selected. Their incident edge sets are disjoint
because an edge cannot meet two highs. Thus s_c is the sum
of the degrees of the selected high vertices, drawn from the
nine eligible physical vertices with degrees 1,1,1,1,1,2,3,3,4.

The vertex bijection selects k=19-c vertices. With host label
one, the rule's required multiset [c-1,18] has k+1=20-c
weights. The degree census separates the thresholds as follows.

| Threshold | k | Required count | Necessary degree calculation |
|---:|---:|---:|---|
| 11 | 8 | 9 | The eight smallest eligible degrees sum to 13. |
| 12 | 7 | 8 | The seven smallest eligible degrees sum to 10. |
| 13 | 6 | 7 | Count equality forces s:0 and five degree-one vertices. |
| 14 | 5 | 6 | Count equality forces s:0 and four degree-one vertices. |
| 15 | 4 | 5 | Count equality forces s:0 and three degree-one vertices. |
| 16 | 3 | 4 | Count equality forces s:0 and two degree-one vertices. |
| 17 | 2 | 3 | Count equality forces s:0 and one degree-one vertex. |
| 18 | 1 | 2 | Count equality forces s:0 alone. |

The first two rows already contradict equality. In every later
row, each selected degree is at least one, and equality leaves
one extra unit beyond k. Exactly one selected vertex must have
degree two, and every other selected vertex must have degree one.
The only high vertex of degree two is s:0. Hence s:0 is selected,
while s:2, b:1:0 and b:3:0 cannot be selected.

## Descending differences contradict the forced pattern

Fix a threshold 13<=c<=18 and suppose the count is k+1. The
unique vertex of label zero is Z. Its full named neighbor list
is s:2 and the four third terminals l:2:0:j for 0<=j<4.

Difference 18 occurs, and in [0,18] the only label pair realizing
it is (0,18). Label 18 is selected. Its vertex is adjacent to Z
and cannot be s:2, which the degree pattern excluded. Therefore
it is one of those third terminals and its sole edge contributes
difference 18.

Now let c<=j<=17 and assume every vertex of label j+1 through
18 is such a third terminal. Every original edge crosses the
fixed alpha cut, so an edge with difference j has a high endpoint
with label at least j and a nonnegative low endpoint. Any high
endpoint with label strictly larger than j is one of the already
forced terminals. Its only neighbor is Z=0, so its unique edge
has strictly larger difference. Thus the high endpoint of the
edge of difference j must have label j. Its other endpoint is
zero, and the only selected neighbors of zero can be third
terminals, since s:2 is excluded. The vertex of label j is
therefore another degree-one third terminal. The induction
terminates at c, with the base alone sufficient at c=18.

Every selected vertex is now forced to be a third terminal.
This contradicts the required selected s:0 of degree two.
The argument also applies when the number of forced terminals
would exceed the four available: the assumed labeling would
have to supply the vertex for each distinct selected label.
This proves A for every permitted threshold and every candidate
g. Gracefulness of the original labeling supplies each
difference used in the induction. No incidence-spectrum
assumption on E_c enters that argument.

## The prescribed operation for every positive batch

For an exact integer h>=1, shift each old label at least c by h,
keep each old label below c, and assign the prescribed fresh
l:0:0:j the label c+j-1 for 1<=j<=h. Attach each only at H.
The original incidences and physical exit stay, and the
label intervals [0,c-1], [c,c+h-1] and [c+h,18+h] still give
a bijection. The resulting tree has 18+h edges.

Each edge of E_c gains exactly h in its difference because its
high endpoint is the only shifted endpoint. The other old
differences remain. At H=1 the new weights start at c-1 and run
through c+h-2. Therefore the resulting sum and the sum required
by gracefulness are

```text
actual:    171 + h*s_c + h*(c-1) + h*(h-1)/2
required:  171 + 19*h           + h*(h-1)/2
difference: h*(s_c+c-20)
```

A makes this difference nonzero for every positive h. This proves
B even for direct use of the operation without the sufficient
incidence hypothesis. Both claims are restricted to the original
graph, alpha orientation, the three numerical pins, exact
threshold range, prescribed host and operation. They impose no
obstruction on gracefulness by another construction. The
[earlier fixed-ledger result](B4_1342_FIXED_LEDGER_UPPER_BLOCK_OBSTRUCTION.md)
and its eight attempted assignments remain separate archived
evidence. The [all-positive (1,r,t,2) theorem](B4_1RT2_K1_DIRECT_SINGLETON.md#selection-for-all-positive-rtk)
is unchanged.

## Bounded evidence and next supply question

The [evidence](../evidence/validation/B4_1342_ALL_LEDGER_PINNED_OBSTRUCTION_001/README.md) rechecks using the retained
1342 certificate and the [retained 1122 positive control](../evidence/validation/B4_UNPADDED_Q1T2_001/validation/retained_seed.json).
The 1122 control with H=4, U=8 and c=9 gives the ten selected
weights [5,14]. It demonstrates a valid premise for the retained
rule on that supplied state. There are no new graphs or
assignments in the bounded evidence.

Seeking a different ledger with all three original pins can no
longer supply this transition. The next proposed obligation
would change only the first-host label, asking for a in [2,8]
and a permitted c as outputs, with the zero host, physical exit,
and oriented alphabet retained. Its required multiset would be
[c-a,18]. That obligation was not executed here.
