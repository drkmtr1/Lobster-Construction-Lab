# B4-1342-RELAXED-HOST-SEED-001 result and completeness argument

## Restricted result

The [reviewed prefilter and predicate proof](B4_1342_RELAXED_HOST_SEED.md)
applies on the exact original named `[[1],[3],[4],[2],[]]`.
For a=2..8 and c=11..18, with physical Z=b:2:0=0 and U=s:4=10,
33 pairs fail the necessary structural tests. One task-local
first-witness run exhausted all 23 survivors. This is an
**EXHAUSTED RESTRICTED NEGATIVE** for the exact normalized
alpha domain with the complete incidence spectrum [c-a,18].
It is implementation-level evidence with a reviewed
completeness argument. Other pins, thresholds, operations
and ordinary labelings of the lobster remain outside the
conclusion. The prior label-one obstruction is separate.

## Why exhaustion covers the admitted domain

The [task-local DFS](../evidence/validation/B4_1342_RELAXED_HOST_SEED_001/seed_search.py)
tries thresholds in descending order and a in ascending order
within each threshold. For each pair it tries every surviving
subset in lexicographic named order. The structural tests are
necessary on any qualifying labeling, whose selected high set
appears exactly once in that pair's subset list.

For a subset, selected named highs have domain [c,18] and
the other highs have [9,c-1]. Each low has [0,8]. The three
starting assignments are exactly Z=0, U=10 and H=a. The DFS
starts with any already closed edges checked in the appropriate
band. It checks label uniqueness, and whenever assigning a
vertex closes an edge to a labeled neighbor, it checks the
positive difference, edge band, and difference uniqueness
both against previous closed edges and within that step.
These are necessary conditions for every completion. An
empty legal domain at a vertex cannot extend to a completion:
its assigned neighbors and used labels and differences
remain fixed down that branch. No condition restricts the
ordering of terminal labels or removes a named symmetry.

The next variable minimizes the number of current legal
values, ties going to more assigned neighbors, higher original
degree, then lexicographic vertex name. Every legal value is
visited in increasing order. This changes only branch order.
Each descent introduces one named vertex, each original edge
is checked once when both endpoints are fixed, and rollback
removes just the label and edge differences added by that step.
At a complete assignment, the 19 distinct labels and 18
distinct legal edge differences fill the required alphabets.
The edge-band equivalence in the presearch proof then gives
the full selected multiset. If no complete assignment is
reached and each allowed choice is examined or excluded by
one of the necessary checks, the named subset is exhausted.
Exhausting all stored subsets exhausts the pair.

One shared budget counts each recursive non-pin assignment trial
immediately before descent. Domain checks that exclude a value
before assignment do not increment that count. Cooperative polling
occurs before search recursion, before each assignment trial and
at subset boundaries. Any reached limit propagates, yielding
INCOMPLETE for the active pair. Later pairs remain unstarted after
a terminal outcome. The run retains exclusive start, subset and
terminal receipts. The checker and edge-band verifier would bind
a candidate to the untouched original before marking it SAT.

## Recorded run

The 23 pair receipts are all EXHAUSTED. Total attempted
assignment nodes were 13,171 with 1.109 seconds elapsed
(to three decimal places). Neither the 200,000 node cap nor
the 20-second cooperative time cap was reached. The c=11,a=8
branch has zero trials: U=10 is unselected, and its neighbor
s:3 would need an unselected edge of difference below c-a=3.
The only low label available in the alphabet for that
inequality is 8, already pinned to H for that pair. No
complete witness was found and the exact-count mode was off.

Only the retained 1342 original and the retained 1122
positive control were checked. The former satisfies its
historical alpha conditions with a=1 and was excluded
from the search domain. The latter gives [5,14] at a=4,c=9.
With no new seed, the two conditional validation graphs
were not created and the proposed parameterized construction
was not promoted. Detailed pair and subset receipts and the
independent arithmetic audit are linked from the
[bounded evidence](../evidence/validation/B4_1342_RELAXED_HOST_SEED_001/README.md).
