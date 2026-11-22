# B4-1342-RELAXED-HOST-SEED-001

## Exact named seed question

On the separately retained [named original](../evidence/validation/B4_1342_UPPER_BLOCK_OBSTRUCTION_001/validation/originals/1342.json),
the profile is `[[1],[3],[4],[2],[]]`, with 19 vertices and 18
edges. The normalized labels are 0..18, with low band 0..8
and high band 9..18. The physical zero host is Z=b:2:0=0,
the physical exit is U=s:4=10, and the physical first host
and low port are H=L=b:0:0. Its label a ranges over 2..8.
The threshold c ranges over 11..18 and the required original
incidence multiset is [c-a,18]. These are the only numerical
pins or parameter restrictions. The same named witness
b:0:0--s:0--s:1--s:2--s:3--s:4 lies within two edges of
every vertex. H is on it and Z is one edge away.

The [pinned obstruction](B4_1342_ALL_LEDGER_PINNED_OBSTRUCTION.md)
excludes a=1 under the other retained pins. The
[fixed-ledger obstruction](B4_1342_FIXED_LEDGER_UPPER_BLOCK_OBSTRUCTION.md)
and its earlier 2342 attempts concern that one original labeling
and are preserved separately.

## Necessary prefilter and all 56 pairs

Alternating the original incidences from high s:4 forces
s:0,s:2,s:4,b:1:0,b:3:0,l:0:0:0 and all four third
terminals onto the high side. Their degrees are respectively
2,3,1,4,3 and five degrees one. No original edge touches
two high vertices. The selected vertices form a subset S of
the nine highs other than U, whose label 10 excludes it.
Exactly k=19-c vertices are selected. The required interval
has k+a weights, so its complete incidence count demands

```text
sum(deg(v)-1 for v in S) = a.
```

The physical s:2 is in S. If it were not, difference 18
would force label 18 at a third terminal adjacent only to
Z=0. If all larger labels have been so forced, the next
required difference d>=c cannot use any such larger label:
its only edge has a larger difference. A high label below
d cannot realize d against a nonnegative low. The high
endpoint therefore has label d and touches zero. The only
selected options are again degree-one third terminals.
This descends through c, forcing all selected degrees to
be one and contradicting the positive excess a.

Every unselected neighbor of Z has its own label as its edge
difference. This edge is unselected, so its difference is
strictly below c-a. Those labels must be distinct and high.
The available slots are [9,c-a-1] with label 10 removed,
as 10 is pinned to U and U is not a neighbor of Z. All four
third terminals are the possible unselected neighbors once
s:2 is selected. Thus the third necessary test is
`|N(Z) - S| <= |[9,c-a-1] - {10}|`, taking an empty interval
when its upper endpoint is less than 9.

For each (c,a) the frozen prefilter checks every size-k named
subset of the nine eligible highs, without enumerating
labelings. First require s:2. Then require excess a. Finally
require enough slots for the unselected zero neighbors.
Reject a pair if no subset passes all three tests. The
record preserves the count of subsets after each test and
all surviving subsets. This accounts for every pair in the
full a=2..8, c=11..18 product.

| c | Surviving a |
|---:|---|
| 11 | 5,6,7,8 |
| 12 | 3,4,5,6,7 |
| 13 | 2,3,4,5 |
| 14 | 2,3,4 |
| 15 | 2,3 |
| 16 | 2,3 |
| 17 | 2,3 |
| 18 | 2 |

There are 56 pairs, 33 necessary-condition exclusions, and
23 survivors. Survival only establishes that a named subset
passes these three necessary checks.

## Exact edge constraint

For each original edge let v be its forced high endpoint and
u its forced low endpoint. It is selected exactly when
g(v)>=c. Put d=g(v)-g(u). In a graceful labeling the original
differences are a bijection onto [1,18]. If the complete
selected spectrum is [c-a,18], all other differences are
[1,c-a-1], so each edge belongs to its respective band.
Conversely, if every edge is assigned to the specified band
by its high endpoint, disjointness and the difference
bijection force every value of [c-a,18] to occur on a
selected edge and every lower value on an unselected edge,
each once. Hence the band constraints are equivalent to the
full predicate under the graceful and alpha conditions.

The retained [1122 control](../evidence/validation/B4_UNPADDED_Q1T2_001/validation/retained_seed.json) at a=4,c=9 supplies
[5,14] under its own pins. The prior [1342 certificate](../evidence/validation/B4_1RT2_TWO_HOST_COMPATIBILITY_001/validation/normalized-r3-t4.json)
is checked as a retained graceful alpha labeling with a=1,
outside the new host domain. Neither control adds a pair to
the admitted search.

[Bounded search and outcome](../evidence/validation/B4_1342_RELAXED_HOST_SEED_001/README.md)
