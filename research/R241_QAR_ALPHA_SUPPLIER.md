# D097 parameterized three-quota alpha supplier

[Evidence](../evidence/validation/LCL_R241_QAR_ALPHA_SUPPLIER_001/README.md) · [D087](R241_2B2_SYMBOLIC_PORT34.md) · [D089](R241_3B3_PORT45_SYMBOLIC.md) · [D096](R241_2AR_ZERO_HOST.md) · [Retained zero-host extension](ALPHA_ZERO_HOST_LEAF_EXTENSION.md)

**Theorem.** For exact integers q,a≥2 and r≥q, the ordered original profile [[q,a],[r]] supplies \(A(q+a+r+5,q+a+2;q+1,q+2)\). The physical ports are the endpoints of the original spine s:0–s:1. The inequality r≥q is part of the domain.

## Named graph and indexed labels

The original has the spine edge s:0–s:1 and the three attachments s:0–b:0:0, s:0–b:0:1 and s:1–b:1:0. Give each center its designated q, a or r indexed terminals, each adjacent solely to that center. Section, branch and terminal indices distinguish all names. Starting from the spine, each center and each terminal enters by one edge, so the graph is connected and acyclic. There are N=q+a+r+5 vertices and N−1 original edges. The spine witnesses every center at distance one and every terminal at distance two.

Set P=q+a+2. The complete assignment is as follows.

| Original name | Label |
| --- | --- |
| s:0, s:1 | q+1, P+q+2 |
| b:0:0, b:0:1, b:1:0 | P+1, P, 0 |
| l:0:0:j, 0≤j<q | 1+j |
| l:0:1:j, 0≤j<a | q+2+j |
| l:1:0:k, 0≤k<q | P+2+k |
| l:1:0:k, q≤k<r | P+3+k |

## Direct proof at r=q

Write N₀=2q+a+5=P+q+3. The low names are b:1:0, the first left terminal group, s:0 and the second left terminal group. Their labels respectively occupy the disjoint consecutive groups {0}, [1,q], {q+1} and [q+2,q+a+1], giving [0,P−1]. The distinct high groups b:0:1, b:0:0, the q right terminals and s:1 use {P}, {P+1}, [P+2,P+q+1] and {P+q+2}. They exhaust [P,N₀−1]. Every indexed band has step one on its full index domain. Thus each label in [0,N₀−1] occurs exactly once.

The spine and all three attachments cross the cut P. Each left terminal is low with a high center, and each right terminal is high with a low center. On every original edge the high endpoint minus the low endpoint gives the following weights.

| Actual original edges | Computation | Inventory |
| --- | --- | --- |
| b:0:1–l:0:1:j, 0≤j<a | P−(q+2+j)=a−j | [1,a] |
| s:0–b:0:1 | P−(q+1) | {a+1} |
| s:0–b:0:0 | (P+1)−(q+1) | {a+2} |
| b:0:0–l:0:0:j, 0≤j<q | (P+1)−(1+j)=P−j | [a+3,a+q+2] |
| s:0–s:1 | (P+q+2)−(q+1)=P+1 | {a+q+3} |
| b:1:0–l:1:0:k, 0≤k<q | P+2+k | [a+q+4,a+2q+3] |
| s:1–b:1:0 | P+q+2 | {a+2q+4} |

The terminal weights advance by one in magnitude between successive indices, and each row accounts for a distinct named edge group. The seven groups run consecutively from 1 to a+2q+4=N₀−1 with neither gaps nor overlaps. Every actual edge is listed once. The boundary labeling is therefore graceful and alpha. The actual s:0 has low label q+1 and s:1 has high label P+q+2, giving offsets (q+1,q+2). In particular q+1<P and q+2=N₀−P−1.

## Right extension and exact capacity

At capacity the supplied right host b:1:0 is zero and one edge from the physical spine. The retained zero-host theorem applies to the witnessed normalized state just proved, with h=r−q fresh named leaves and no changes to old names, labels or edges. For k≥q the new leaf l:1:0:k is addition number k−q+1. Its label is N₀+(k−q)=P+3+k. Its edge at b:1:0 has the same difference. Both fresh inventories are exactly [N₀,N−1]=[a+2q+5,N−1], disjoint from their old inventories. Their unions give the full label and difference alphabets, with both unused inventories empty. For r=q the final index range and inventories are empty and this step is the identity.

All new labels are high and all new edges cross to the same zero host. The low class, cut, physical ports and original spine remain in place. The number of high vertices is N−P=r+3. Offset q+2 is in [0,r+2] precisely when r≥q. For smaller r the prescribed exit label \(P+q+2\) lies above N−1. That arithmetic excludes this particular exit offset outside the domain and leaves other interfaces open.

## Retained cases and termination

At q=2 we have P=a+4 and N=a+r+7. The spine and center labels, both indexed left palettes and the initial and fresh right palettes specialize pointwise to D096. The subcase r=2 is exactly D087. At q=r=3 we have P=a+5, N=a+11, ports (4,5) and the exact D089 assignment with its parameter b=a, including terminal indices. D088's restriction on `[[3,b],[2]]` at its distinct offsets (4,4) is preserved.

Check exact integer types and the inequalities first. Then emit the spine and centers with their four edges and run the indexed terminal loops in the table, each with its single original attachment. The loops emit q+a+r terminals and terminate after O(q+a+r) indexed operations. This is a direct symbolic supplier whose capacity-boundary proof covers every allowed q,a. The retained theorem handles the extra right terminals. Its scope is the given two-section original and offsets.
