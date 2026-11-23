# The strict R241 port pair on original `[[2,2],[2]]`

[Task specification](../tasks/LCL_Codex_D082_222_Strict_Return_2026-11-22.md) · [Verified intake](../evidence/validation/LCL_R241_222_STRICT_RETURN_001/INTAKE.md) · [Bounded evidence](../evidence/validation/LCL_R241_222_STRICT_RETURN_001/README.md)

## Original topology and pinned orientation

The original tree has the spine s:0–s:1, the two distinct centers b:0:0 and b:0:1 at s:0, and the center b:1:0 at s:1. Each center has its own terminal indices 0 and 1. It has 11 vertices and 10 original edges. The only path between the two physical spine ports is their actual edge. Every center is one edge from that path and every terminal two.

With s:0 low, connectivity and alternate classes along every edge force lows s:0, b:1:0 and the four terminals at section zero. The highs are s:1, both centers at section zero and the two terminals at section one. The exact cut is therefore `P=6`. The required offsets (1,0) prescribe s:0=1 and s:1=6. This leaves {0,2,3,4,5} on the five unpinned low names and {7,8,9,10} on the four unpinned high names.

## Analytic obstruction

Write A and B for the labels of b:0:0 and b:0:1, respectively, and z for the low label of b:1:0. Every edge difference is high minus low. The total is the high degree-weighted label sum minus the low degree-weighted label sum. The high alphabet sums to 40. Relative to assigning degree one to every high vertex, s:1 contributes an additional 6 and the two centers of degree three contribute an additional `2(A+B)`. The low alphabet sums to 15. The only low vertices with degree above one are s:0 and b:1:0, both of degree three. Their additional contribution is `2+2z`. Consequently gracefulness would require

```text
55 = 1+...+10 = (40+6+2(A+B)) − (15+2+2z) = 29+2(A+B−z)
z = A+B−13.
```

Since A and B are distinct in {7,8,9,10}, the possible unordered numerical pairs and their forced z are:

| {A,B} | z |
|---|---:|
| {7,8} | 2 |
| {7,9} | 3 |
| {7,10} | 4 |
| {8,9} | 4 |
| {8,10} | 5 |
| {9,10} | 6, outside the free low alphabet |

This table is a necessary condition on the center labels. The following contradictions apply to both orders of each admissible pair, without identifying named centers or terminals.

Weight 10 requires the actual adjacent pair 0 and 10. If 10 is at a second-section terminal, its only neighbor is z≥2, which is impossible. Therefore 10 is at one of the two first-section centers, and one of its own terminals carries 0. The table leaves only two cases.

- If the other first-section center is labeled 7, then z=4. The two terminals at z carry 8 and 9 in either order. The edge from z=4 to the terminal labeled 9 has weight 5, repeating the actual spine weight `6−1=5`.
- If the other first-section center is labeled 8, then z=5. The right terminal labels are 7 and 9, giving weights 2 and 4. The spine weighs 5, the three center attachments weigh 9, 7 and 1, and the zero terminal edge weighs 10. Each remaining edge goes from a first-section center of label at least 8 to a terminal of label at most 4. Its weight is at least 4. Thus no edge has weight 3.

Every possible center placement is excluded. This rules out `A(11,6;1,0)` at the prescribed physical ports on the exact original. The proof establishes no obstruction to other ports or to ordinary gracefulness.

## Diagnostic and composition scope

The finite diagnostic visits every ordered pair of permutations on the two original classes with the pins above, exactly `5!·4!=2,880` visits. Both branch names and every terminal index are distinct. The implementation uses no weighted-degree pruning or symmetry quotient. Each searched assignment is an alpha bijection, so its ten edge weights all lie in [1,10]. If they fail the required bijection, a pair of distinct original edges with equal weight witnesses the failure. The independent auditor verifies coverage by factorial ranks and checks the saved pair for each failed assignment.

The adopted R241 placement requires an already supplied old B state with its actual exit offset equal to the next block's actual entrance offset. D080's H(a) supplies entrance zero, but this pinned B cannot supply the required exit state under the simultaneous entrance pin. Thus the proposed J(a) route using this exact B state is rejected at its premise. The retained H(a), R241 join, D078–D081 constructions and path consumer keep their accepted scopes. No J(a) original, repeated assembly, or suffix from this seed is evaluated. [Pinned R241](https://github.com/drkmtr1/Math-Discovery-Lab/blob/858a8c1fcfda87ba40bb1adee498a6131504a803/research/candidates/volume-010.md#L4364-L4405) · [D080 bridge](R241_ZERO_TO_ONE_BRIDGE.md)
