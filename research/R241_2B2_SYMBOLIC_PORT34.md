# Symbolic physical (3,4) supplier on original `[[2,b],[2]]`

[Evidence and reproduction](../evidence/validation/LCL_R241_2B2_SYMBOLIC_PORT34_001/README.md) · [D086 motivation](R241_242_PORT_34.md) · [Adopted R241](../references/upstream/mdl/N241_relational_ports.md)

**Theorem.** For every integer b≥2 the exact named original `T_b=[[2,b],[2]]` independently supplies A(b+9,b+4;3,4). The specified witness is the actual spine s:0–s:1.

## A. Named graph and incidences

Use the spine vertices s:0 and s:1 and their one edge. Attach b:0:0 and b:0:1 to s:0, and b:1:0 to s:1. At the first and right centers, use terminal indices 0 and 1 at their respective section and branch names. At b:0:1 use the names l:0:1:j with 0≤j<b. Each terminal has just its own center as neighbor. Section, branch and terminal indices distinguish all names. The graph is connected and acyclic since each attached vertex adds exactly one edge to the graph already built. The five spine/center vertices and b+4 terminals give N=b+9. The spine edge, three attachments and b+4 terminal edges give m=b+8. Each edge belongs to exactly one of these groups, and within a terminal group its index determines a distinct endpoint.

## B. Label bijection

Give the following labels directly on those names.

| Named vertices | Labels |
|---|---|
| s:0, s:1 | 3, b+8 |
| b:0:0 and l:0:0:0, l:0:0:1 | b+5 and 1, 2 respectively |
| b:0:1 and l:0:1:j, 0≤j<b | b+4 and 4+j respectively |
| b:1:0 and l:1:0:0, l:1:0:1 | 0 and b+6, b+7 respectively |

The low names are s:0, b:1:0 and all b+2 first-section terminals. Their labels are the disjoint singleton group {0,1,2,3} and interval [4,b+3]. The latter has b elements since j=0 gives 4 and j=b−1 gives b+3. Their union is [0,b+3], of size P=b+4. The five high names s:1, b:0:0, b:0:1 and the right terminals receive [b+4,b+8] bijectively. These consecutive disjoint classes cover [0,b+8] once each.

## C. Original-edge difference partition

Every right-hand subtraction uses the high endpoint minus the low endpoint at the named edge.

| Original edge group | Difference calculation |
|---|---|
| s:0–s:1 | (b+8)−3=b+5 |
| s:0–b:0:0 | (b+5)−3=b+2 |
| b:0:0–l:0:0:0 and b:0:0–l:0:0:1 | (b+5)−1=b+4 and (b+5)−2=b+3 |
| s:0–b:0:1 | (b+4)−3=b+1 |
| b:0:1–l:0:1:j, 0≤j<b | (b+4)−(4+j)=b−j |
| s:1–b:1:0 | (b+8)−0=b+8 |
| b:1:0–l:1:0:0 and b:1:0–l:1:0:1 | (b+6)−0=b+6 and (b+7)−0=b+7 |

The indexed family decreases by one from b to 1 as j runs from 0 to b−1. The other eight edges supply b+1 through b+8 as distinct singletons, disjoint from [1,b]. These listed edges account for every original incidence once, hence all differences [1,m] occur exactly once.

## D. Alpha cut, ports and witness

The spine joins a low to a high. Each first attachment joins the low s:0 to a high center, and their terminal edges reach lows. The right attachment joins high s:1 to low b:1:0, and the right terminal edges reach highs. Thus every edge crosses P=b+4. The actual entrance has label 3 and the actual exit has label b+8=P+4. Each center is distance one from the spine and each terminal distance two through its original center. These data give the claimed state with physical offsets (3,4).

## E. Direct supply and boundary

Given an integer b≥2, emit the spine, center and fixed terminal names, their prescribed incidences and their constant-number label formulas. For j=0,1,…,b−1 emit l:0:1:j, its one edge at b:0:1 and label 4+j. The distinct named groups make the labeling total and unambiguous. The finite loop advances j by one and stops at b. It uses O(b) indexed operations and output records, with no existing solution as an input.

At b=2 the variable labels are 4 and 5 and their edge weights are 2 and 1. The low and high alphabets become [0,5] and [6,10], with the eight singleton differences 3 through 10. In particular the smallest allowed b keeps all endpoints disjoint. The symbolic partitions apply unchanged for every larger b.

## F. Supplementary signed sum

Let A and B denote the two ordered first-center labels and z the right-center label for any graceful alpha labeling at these prescribed ports. The degrees at s:0, s:1, b:0:0, b:0:1 and b:1:0 are 3, 2, 3, b+1 and 3. All terminals have degree one. The degree-one high sum is 5b+30 and the low sum is (b+3)(b+4)/2. The excess-degree port contribution is (b+8)−2·3=b+2, with center contribution 2A+bB−2z. Equating the signed edge sum to (b+8)(b+9)/2 and rearranging gives 2A+bB−2z=b²+6b+10. The formula gives 2(b+5)+b(b+4)=b²+6b+10 at z=0. This is a consistency check for the fixed ports. The difference partition above proves gracefulness.

## Retained controls and physical compatibility

D084, D085 and D086 already supply (3,4) on b=2, 3 and 4. At b=2 the retained variable indices 0 and 1 have labels 5 and 4, and the right indices 0 and 1 have labels 9 and 8. The formula orders each of those same two palettes increasingly. At b=3 the retained variable indices have labels 6,5,4 and the formula assigns them 4,5,6. At b=4 the retained D086 ledger matches the formula at every index. These comparisons keep the actual graphs and port predicates fixed. Within each named center the label multiset and incident terminal-weight multiset agree, while individual values can differ at particular indices. The optional b=5 regression checks one additional instantiation. The finite records serve as controls for the implementation.

Exit offset four conditionally matches the R212-B.1 designated entrance Z at u=5 when the actual connector and both witnessing paths satisfy R241. The D080 H(a) entrance is zero. The theorem varies one terminal quota with the other two fixed at two. It supplies one component at a time with the indicated physical ports.
