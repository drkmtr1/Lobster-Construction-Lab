# Symbolic physical (4,5) supplier on original `[[3,b],[3]]`

[Evidence and reproduction](../evidence/validation/LCL_R241_3B3_PORT45_SYMBOLIC_001/README.md) · [D088 obstruction](R241_3B2_PORT44_SYMBOLIC.md) · [D087 supplier](R241_2B2_SYMBOLIC_PORT34.md) · [Adopted R241](../references/upstream/mdl/N241_relational_ports.md)

**Theorem.** For every exact integer b≥2, the exact named original T_b=`[[3,b],[3]]` independently supplies A(b+11,b+5;4,5), with the original s:0–s:1 spine as witness.

## A. Exact graph

The two spine names s:0 and s:1 have their one original edge. Attach b:0:0 and b:0:1 to s:0 and attach b:1:0 to s:1. The terminal groups l:0:0:j, l:0:1:j and l:1:0:j have index ranges 0≤j<3, 0≤j<b and 0≤j<3, respectively. In each case the corresponding named center is the terminal's sole neighbor. The section, branch and terminal indices keep each group and each incidence distinct. There are two spine vertices, three centers and b+6 terminals, giving N=b+11. The spine edge, three attachments and b+6 terminal edges give m=b+10. Starting from the spine, each center and then each terminal is attached by a single edge to an existing vertex. Thus the graph is connected and acyclic and every named incidence has multiplicity one.

## B. Vertex-label partition

Use the candidate in its exact indexed form.

| Named vertices | Labels |
|---|---|
| s:0, s:1 | 4, b+10 |
| b:0:0 and l:0:0:j with 0≤j<3 | b+6 and 1+j, respectively |
| b:0:1 and l:0:1:j with 0≤j<b | b+5 and 5+j, respectively |
| b:1:0 and l:1:0:j with 0≤j<3 | 0 and b+7+j, respectively |

The low side consists of s:0, b:1:0 and the two first-section terminal groups. These names get {0,1,2,3,4} and [5,b+4] disjointly. The interval has b elements and endpoints at j=0 and j=b−1. Thus the lows exhaust [0,b+4] exactly once and have size P=b+5. The six remaining names are s:1, both first-section centers and the three right terminals. They get [b+5,b+10] once each. Together the disjoint sides cover [0,m]. At b=2 the ranges reduce to [0,6] and [7,12], and the variable terminal labels are 5 and 6. The same endpoint bounds hold for every larger integer b.

## C. Actual differences and right capacity

| Actual edges | High-minus-low arithmetic |
|---|---|
| b:0:1–l:0:1:j | (b+5)−(5+j)=b−j, descending from b to 1 |
| s:0–b:0:1 | (b+5)−4=b+1 |
| s:0–b:0:0 | (b+6)−4=b+2 |
| b:0:0–l:0:0:j | (b+6)−(1+j)=b+5−j, descending from b+5 to b+3 |
| s:0–s:1 | (b+10)−4=b+6 |
| b:1:0–l:1:0:j | (b+7+j)−0=b+7+j, ascending from b+7 to b+9 |
| s:1–b:1:0 | (b+10)−0=b+10 |

The groups exhaust the original edges with 1+3 attachments/spine and b+6 distinct terminal incidences. The b variable-terminal differences give [1,b] exactly once. The other ten differences are b+1 through b+10, each once. Hence the complete spectrum is [1,m] with no repeated or omitted difference.

For this original, the three right-terminal positions are l:1:0:0, l:1:0:1 and l:1:0:2. Their edges to zero supply m−3,m−2,m−1, and the right attachment supplies m. At the same b, the two right-terminal weights forced in D088 were b+7 and b+8. D089 assigns those two values at indices 0 and 1, respectively. The added index 2 supplies b+9, while the right attachment increases from b+9 to b+10. This provides enough right-edge positions for the top four weights. The new original has a different order and normalization from the two-terminal original in D088. D088's exclusion remains scoped to `[[3,b],[2]]` at its prescribed (4,4) state.

## D. Alpha state and physical witness

Every edge crosses cut P=b+5. The spine crosses between its low and high endpoints, the two first attachments join low s:0 to high centers with low leaves, and the right attachment joins high s:1 to low b:1:0 with high leaves. The physical spine labels are 4 and b+10=P+5, giving offsets (4,5). Each center is distance one from the spine and each terminal distance two along its own center edge. This proves the asserted normalized state.

## E. Direct terminating supply

Check that b is an integer at least two. Emit the two spine names, three center names and their four edges, with the corresponding labels above. Emit the two fixed terminal groups with indices 0,1,2 and their one center edge per leaf. Emit the variable terminal group in the loop j=0,…,b−1, giving each name its own edge to b:0:1 and its label 5+j. The index ranges are finite and disjoint as name groups. The algorithm terminates after O(b) indexed operations and output records, determined by b and the displayed formulas.

## F. Signed-degree consistency

Write A, B and z for the labels of b:0:0, b:0:1 and b:1:0. Counting degree one per vertex first, the high alphabet sums to 6b+45 and the low alphabet to (b+4)(b+5)/2. The actual degrees of s:0, s:1, b:0:0, b:0:1 and b:1:0 are 3,2,4,b+1,4, respectively. The ports add (b+10)−2·4=b+2 to the degree-one contribution, and the centers contribute the other signed corrections. Thus any graceful labeling at these ports satisfies
```text
(b+10)(b+11)/2 = 6b+45 − (b+4)(b+5)/2 + (b+2) + 3A+bB−3z
3A+bB−3z = b²+8b+18.
```
The candidate gives 3(b+6)+b(b+5)=b²+8b+18 at z=0. This consistency check is supplementary to the exact original-edge spectrum.

## Boundary certificate and potential compatibility

The one new b=2 original has 13 vertices, 12 edges and cut seven. The formula gives physical labels 4 and 12 and original-order weights 8,4,7,6,5,3,2,1,12,9,10,11. The retained D087 b=5 and D086 b=4 positives have their own named originals. D088 is a retained scoped negative. These checks corroborate the implementation. The proof above supplies the quantifier.

D087's outgoing offset four agrees with this module's actual incoming offset four. R241 would further require the designated connector in the original target, both component witnesses, joint vertex-label and edge-difference partitions, the physical returned port and quantified closure. The present theorem supplies only the one-component family with the two constant quotas fixed at three.
