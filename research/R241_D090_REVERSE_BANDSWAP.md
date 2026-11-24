# Section reversal and alpha-band exchange of D090

[Evidence and reproduction](../evidence/validation/LCL_R241_D090_REVERSE_BANDSWAP_001/README.md) · [D090 supplier](R241_2B2_3B3_JOINT.md) · [Adopted R241.1](../references/upstream/mdl/N241_relational_ports.md)

**Theorem.** For all integers a,b≥2, the exact named original R(a,b)=`[[3],[3,b],[2],[2,a]]` independently supplies A(a+b+20,11;5,3), witnessed by the original spine s:0–s:1–s:2–s:3.

## Exact original graph correspondence

Construct the target with four spine vertices s:0 through s:3, successive spine edges, and the following exact rows of terminal quotas. For each displayed row, attach b:i:j to s:i and attach exactly l:i:j:k for 0≤k below that quota to b:i:j.

| Target section i | Ordered quotas at its centers | Source section in D090 |
| --- | --- | --- |
| 0 | 3 | 3 |
| 1 | 3,b | 2 |
| 2 | 2 | 1 |
| 3 | 2,a | 0 |

There are four spine vertices, six centers and a+b+10 terminals. The three spine edges, six attachments and a+b+10 terminal edges are all distinct. Thus N=a+b+20, with N−1 edges. The graph is a tree because each center or terminal was attached once to a tree, starting with the spine.

Define ρ by replacing section i by 3−i in each vertex name. Preserve the role and every branch and terminal index. The quota rows show that this is defined on every source vertex, and the inverse replaces the section index in the same way. Every source spine edge at i,i+1 maps to the target spine edge at 2−i,3−i as an undirected incidence. Each attachment maps to the exact attachment at the reversed section with the same center index. Each terminal edge maps to that terminal's exact center edge at the reversed section with both indices unchanged. The inverse has the same property in each edge group. Thus the edge map is bijective with every original incidence counted once. In particular the source connector s:1–s:2 maps to the same undirected named edge in the target, and is the only edge between its two pairs of sections.

## Label bands, differences and ports

D090 gives a direct alpha map f on T(a,b)=`[[2,a],[2],[3,b],[3]]`. Its cut is P=a+b+9, and H=N−P=11. Give target vertex ρ(v) the label f(v)−P when f(v)≥P, and f(v)+H when f(v)<P. Translation carries the old [P,N−1] bijectively to [0,H−1]=[0,10]. The old [0,P−1] translates bijectively to [H,H+P−1]=[11,N−1]. The intervals are consecutive and disjoint, and ρ is bijective on names, so g covers each vertex and label once. The two translated bands exchange the alpha classes, with each internal order preserved.

On an arbitrary source edge let h be its high endpoint and l its low endpoint. Their images are respectively low and high. For d=f(h)−f(l) the new difference is positive and calculated on the corresponding actual edge:
```text
g(ρ(l)) − g(ρ(h)) = f(l)+H − (f(h)−P) = N−d.
```
Since 1≤d≤N−1, the new difference also lies in this interval. Applying the numerical map twice returns d, so it is bijective on the whole required spectrum. By the original-edge bijection, all target differences occur once. Independently, the old D090 edge bands and their images are as follows.

| Old edge group and spectrum | Target sections or incidence | New spectrum |
| --- | --- | --- |
| D087 internal, [b+12,a+b+19] | 2 and 3 | [1,a+8] |
| Original connector, {b+11} | s:1–s:2 | {a+9} |
| D089 internal, [1,b+10] | 0 and 1 | [a+10,a+b+19] |

The bands are consecutive, disjoint and exhaustive. The spine labels follow directly from the D090 formulas in reversed order.

| Target vertex | Source label on its preimage | Translated label |
| --- | --- | --- |
| s:0 | a+b+14 | 5 |
| s:1 | a+8 | a+19 |
| s:2 | a+b+19 | 10 |
| s:3 | 3 | 14 |

The actual connector weight is (a+19)−10=a+9. The original path s:0–s:1–s:2–s:3 is the reversed source witness. Each center is one edge from it and each terminal reaches it in two edges through the actual center. The new low size is 11, so the actual entrance is 5 and the actual high exit is 11+3=14. Both unused inventories are empty.

## Independent supply and scope

Require exact integers a,b≥2. Emit the exact target by its four ordered quota rows. Compute the explicit named D090 labels from its formula, reverse each section index, and translate the labels by their old band as above. Each vertex and edge takes a bounded number of indexed operations per output record. There are O(a+b) records and both variable-length terminal loops terminate at their prescribed quotas. This directly supplies the entire reversed state from the parameters. For each allowed a,b the proof uses only the accepted explicit D090 family and the verified band exchange.

At a=b=2 the new original has 24 vertices, 23 edges and cut 11, and the physical spine labels are (5,21,10,14). This boundary certificate corroborates the formula. D091 and D092 concern different exact originals and retain their separate obstructions.

D090 has offsets (3,5) and this theorem supplies (5,3). Their actual physical outgoing and incoming offsets meet the numerical R241 condition in either order. An actual composed original, its connector and witness, joint inventories and any repeated construction remain separate proof obligations. The present theorem supplies the single reversed component.
