# D098 named center-role transport for ordered three-quota originals

[Evidence](../evidence/validation/LCL_R241_NAMED_CENTER_ROLE_TRANSPORT_001/README.md) · [D097 supplier](R241_QAR_ALPHA_SUPPLIER.md) · [Retained boundary source](R241_242_PORT_34.md)

**Theorem.** For exact integers q>r≥a≥2, the ordered original `[[q,a],[r]]` supplies A(N,P;a+1,a+2), where N=q+a+r+5 and P=q+a+2.

## Named source, target and incidence correspondence

The source S has profile `[[a,q],[r]]`, and the target T has profile `[[q,a],[r]]`. Each has the common spine s:0–s:1 and attachment edges s:0–b:0:0, s:0–b:0:1 and s:1–b:1:0. In each original, l:i:j:k is adjacent only to b:i:j, with k from zero through the corresponding quota minus one. In S the first two terminal index ranges have lengths a and q, respectively. In T they have lengths q and a. Both right groups have length r. Attaching each center and terminal by its one edge to a previously present vertex gives a tree. There are five spine or center vertices and q+a+r terminals. The spine edge and the three center attachments together with the terminal edges give exactly N−1 edges in each original.

Define the source-to-target map φ by fixing s:0, s:1, b:1:0 and every l:1:0:k, sending b:0:j to b:0:(1−j), and sending l:0:j:k to l:0:(1−j):k. Source b:0:0 and its a leaves therefore map to target b:0:1 and its a leaves, and source b:0:1 and its q leaves map to target b:0:0 and its q leaves. Each range of k is identical at its mapped group. The same branch-index rule with the graphs exchanged is the inverse, proving a bijection between the named vertex sets.

The spine and right attachment and terminal edges are fixed. Each left attachment maps to the other left attachment, and each left terminal edge maps to the edge between the translated terminal and its corresponding translated center, with its terminal index preserved. Applying the inverse gives every target edge exactly once. Thus the actual incidences and their multiplicities are preserved in both directions. The two ordered profiles have distinct named original identities.

## Source hypothesis and transported labels

Since r≥a, D097 applies to S with first quota a and second quota q, returning normalized offsets (a+1,a+2) at the actual spine endpoints. Write its complete source labeling as F and set G(v)=F(φ⁻¹(v)) for each target vertex v. Substituting a for D097's first quota and q for its second quota, then applying the inverse name map, gives these target values.

| Named target vertex | Label |
| --- | --- |
| s:0, s:1 | a+1, P+a+2 |
| b:0:0, b:0:1, b:1:0 | P, P+1, 0 |
| l:0:0:j, 0≤j<q | a+2+j |
| l:0:1:j, 0≤j<a | 1+j |
| l:1:0:k, 0≤k<a | P+2+k |
| l:1:0:k, a≤k<r | P+3+k |

The low labels on the right center, second left terminals, entrance and first left terminals respectively give {0}, [1,a], {a+1} and [a+2,a+q+1]. These are disjoint and give [0,P−1]. The remaining vertices take {P,P+1}, [P+2,P+a+1], {P+a+2} and [P+a+3,N−1] on the two left centers, initial right terminals, exit and additional right terminals, respectively. Each interval is filled once by the stated index ranges. The final interval has r−a entries and is empty at r=a. These consecutive bands give [P,N−1] and complete the label bijection. The spine and all attachments cross the cut, as do the edges from high left centers to low terminals and the edges from the low right center to high terminals.

## Target difference inventory and physical witness

For each source edge uv, the corresponding target edge φ(u)φ(v) has weight |F(u)−F(v)|. The inverse verifies this pointwise equality across the complete target edge set. Independently, subtraction on the target yields the following bands.

| Actual target edges | Weights |
| --- | --- |
| b:0:0–l:0:0:j | q−j, giving [1,q] |
| s:0–b:0:0 | P−(a+1)=q+1 |
| s:0–b:0:1 | (P+1)−(a+1)=q+2 |
| b:0:1–l:0:1:j | P−j, giving [q+3,q+a+2] |
| s:0–s:1 | P+1=q+a+3 |
| b:1:0–l:1:0:k for 0≤k<a | P+2+k, giving [P+2,P+a+1] |
| s:1–b:1:0 | P+a+2 |
| b:1:0–l:1:0:k for a≤k<r | P+3+k, giving [P+a+3,N−1] |

All bands are disjoint, and their consecutive union is [1,N−1]. At r=a the last line has no incidences, with the right attachment already giving N−1. Both unused inventories are empty. The actual spine stays s:0–s:1, and each center and terminal lies at distance one or two from its original designated spine vertex, respectively. Its physical labels a+1 and P+a+2 return offsets (a+1,a+2).

## Direct construction and combined coverage

Check exact integer types and the inequalities q>r≥a≥2. Emit the two spine names and three centers with their four edges. Emit the indexed terminal names, edges and labels using the table. These loops take O(q+a+r) indexed operations and use the original target as specified. Equivalently, evaluate D097 on S and transfer each name and its label in one pass. The proof is an incidence-preserving transport of the existing D097 labeling.

For exact integers q,a≥2, D097 covers r≥q at offsets (q+1,q+2). The complementary D098 slice q>r≥a uses offsets (a+1,a+2). The union is exactly r≥min(q,a). Supply when r<min(q,a) remains open for these constructions. For those profiles the two returned exit offsets exceed the available high range 0 through r+2. Other physical states remain a separate question.
