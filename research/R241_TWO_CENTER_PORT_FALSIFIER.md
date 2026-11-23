# Fixed R241 offsets fail on the smallest two-center pair

[Authorized task](../tasks/LCL_Codex_D079_TwoCenter_R241_Port_Falsifier_2026-11-22.md) · [Roadmap](../docs/strategy/LCL_Branched_Spine_Research_Roadmap_2026-11-22.md) · [Evidence](../evidence/validation/LCL_R241_TWO_CENTER_PORT_001/README.md)

## Original graph and exact claim

For positive integers a,b,c the profile `[[a,b],[c]]` has spine edge s:0–s:1, two different centers b:0:0 and b:0:1 incident to s:0, and b:1:0 incident to s:1. Each center has exactly the indexed terminals from its own quota. There are `N=a+b+c+5` vertices and `N−1` edges. The spine edge itself is the physical witness. Each center and terminal is respectively one or two edges from it.

If s:0 is the low entrance and s:1 the high exit, connectedness forces the bipartition orientation. Low vertices are s:0, b:1:0 and the terminals of both centers at section zero. They number `P=a+b+2` and carry labels `[0,P−1]`. High vertices are s:1, b:0:0, b:0:1 and the terminals at section one. They carry `[P,N−1]`. The strict D078 replacement interface demands `(x,y)=(1,1)`, so s:0 has label 1 and s:1 has label P+1. We reject that universal supplier claim by the original named pair at a=b=c=1.

## Analytic contradiction on `[[1,1],[1]]`

Here `N=8` and `P=4`. The prescribed labels are s:0=1 and s:1=5, so the original spine edge weighs 4. The remaining lows are `{0,2,3}` and the remaining highs are `{4,6,7}`. Difference 7 requires the pair 0 and 7 on an actual original edge. There are precisely three possible placements for 7, handled below without removing or identifying either named first-section center.

If 7 is at the only second-section terminal l:1:0:0, its sole neighbor b:1:0 must have label 0. The original s:1–b:1:0 edge then weighs 5. One of the two first-section centers carries 6, so its attachment to s:0=1 also weighs 5.

If 7 is at either named first-section center, its attachment to s:0=1 weighs 6. Its only other neighbor is its own terminal, which must carry 0 to realize 7. Now consider the other first-section center.

- If that center carries 4, its attachment weighs 3. The sole second-section terminal must carry 6, and its low neighbor b:1:0 carries 2 or 3. Their edge weighs 4 or 3, repeating the spine edge or the attachment of the center labeled 4.
- If that center carries 6, its terminal must carry 2 or 3. At 2 the terminal edge weighs 4, repeating the spine edge. At 3 the terminal edge weighs 3, leaving 2 at b:1:0. The original edge from s:1=5 to b:1:0=2 then also weighs 3.

Every case repeats an actual edge difference. This proves that no alpha labeling supplies the required physical ports on this one original. It falsifies the universal fixed-port claim for positive a,b,c. The proof uses the maximal difference and original incidences. The finite enumeration is corroboration.

## Two exact positive controls

Both tables use the physical spine witness s:0–s:1, the same named incidence rules and low size four.

| Original names in order | Labels on `[[1,1],[1]]` | Labels on `[[1,1],[2]]` |
| --- | --- | --- |
| s:0, s:1 | 1, 4 | 1, 5 |
| b:0:0, l:0:0:0 | 7, 0 | 8, 0 |
| b:0:1, l:0:1:0 | 6, 2 | 7, 2 |
| b:1:0 and its terminals by index | 3, 5 | 3, 4, 6 |

Every low label 0 through 3 and every high label 4 through N−1 appears once on its physical side. In the order spine, first attachment and terminal, second attachment and terminal, third attachment and terminals, the weights are `(3,6,7,5,4,1,2)` and `(4,7,8,6,5,2,1,3)`, respectively. These are exactly the required spectra. The first control supplies `A(8,4;1,0)` on the same original as the obstruction. The second supplies `A(9,4;1,1)` on a different original. Both are explicit finite states.

## Exact R241 applicability

In adopted R241.1, B is the preceding aggregate and A the new module, on disjoint original vertex sets. The actual connector from U_B to L_A has weight `N_A+y_B−x_A` after the original placement, and its required weight is `N_A`. Hence this placement uses `y_B=x_A`. In particular the `(1,0)` state cannot precede a next state of entrance offset 1 by this placement. It can accept an incoming offset from a predecessor whose high exit offset is 1, subject to the other R241 premises, but its own returned high offset is zero. The two verified controls therefore do not supply a closed arbitrary-length menu or a new suffix theorem. [Pinned original R241](https://github.com/drkmtr1/Math-Discovery-Lab/blob/858a8c1fcfda87ba40bb1adee498a6131504a803/research/candidates/volume-010.md#L4364-L4405) · [Retained adoption](../references/upstream/mdl/N241_relational_ports.md)

## Exact enumeration plan

Use the above forced orientation and distinguish all names. Without explicit port pins on the eight-vertex original, the two class bijections give `4!·4!=576` assignments. With the two pin values fixed, three lows and three highs remain, giving `3!·3!=36` assignments. On the nine-vertex original with the strict pins, there are three free lows and four free highs, giving `3!·4!=144`. Free labels are exactly the alphabets remaining in each class after removing the pinned values. Enumerate the full two-permutation product separately in each declared diagnostic. The 36 assignments also lie in the 576 unpinned class product and are counted on both visits. No quotient or additional pin is used.

Every assigned edge difference lies in `[1,N−1]` by the alpha cut. Thus a rejected row has two original edges of equal weight. Saving such a pair for every rejected row permits an independent audit of the result without a second exhaustive evaluation of full spectra. The positive rows can be checked against all actual original differences. The original's graph digest and the identity of a named label ledger are separate bindings.
