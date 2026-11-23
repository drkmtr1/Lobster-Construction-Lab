# Unpinned first-host dual-block obstruction on named 2222

## Original and incidence equations

Use the [D066 original](../evidence/validation/B4_K2_ALPHA_PREFIX_S4_9_001/prefix_original.json), `[[2],[2],[2],[2],[]]`. Its graph digest is `35c75a93573720212045e5dedb66a0d5ccfd5a09900ea12b791ec900938ea4f4`. The four spine edges are s:i–s:(i+1). Each actual center b:i:0 attaches to s:i and each of its two original terminals attaches only to it. This gives 17 vertices and 16 edges, with no interchange of terminal names. The original witness is b:0:0–s:0–s:1–s:2–s:3–s:4. Both insertion hosts lie within one edge of it, and all vertices within two.

Write a=f(b:0:0), B=f(b:1:0), X=f(s:0), Y=f(s:2), T=f(b:3:0), x=f(s:1), and y=f(s:3). The physical pins remain b:2:0=0 and s:4=9. The low class [0,7] has degree-three vertices b:0:0,b:2:0,s:1,s:3 and the four degree-one terminals at branches 1 and 3. The high class [8,16] has degree-three vertices s:2,b:1:0,b:3:0, degree-two s:0, and degree-one s:4 and the four terminals at branches 0 and 2. The alternation from high s:4 and the original attachments force these classes.

For the retained [upper block](ALPHA_UPPER_BLOCK_GENERAL_HOST.md#exact-state-and-incident-edge-hypothesis), let E_U be all edges from highs with label ≥u, where 10≤u≤16. For the [lower block](ALPHA_LOWER_BLOCK_LEAF_INSERTION.md#supplied-state-and-hypotheses), let E_L be all edges from lows with label <d, where a<d≤8. Every selected edge at either cut has a unique selected endpoint. The complete tails are [u−a,16] and [B−d+1,16]. Since the original weights 1 through 16 occur once each, selecting either full tail selects exactly its inverse image on original edges. The larger start gives the smaller selected edge set, and equal starts give identical sets. The complement of the upper selection must use exactly [1,u−a−1].

All lower selections include b:0:0 and b:2:0. With k_d of the two spine lows included, their count is d+4+2k_d. The required count is 16−B+d, so B=12−2k_d∈{8,10,12}. The upper selection has 17−u highs and requires 17−u+a edges, so the selected high degree excess above one per vertex is a. The nonzero excesses are one at s:0 and two at each of s:2,b:1:0,b:3:0. These counts alone do not imply either complete tail.

Two further necessary facts use the full graceful spectrum.

- **s:2 is upper-selected.** Otherwise weight 16 must come from a third terminal labeled 16 at the pinned zero. Descend from 16 to u. For each w≥u the weight requires a high label ≥w. All vertices with larger label have already been forced to be third terminals, each incident only to its own larger weight. Thus weight w also requires a third terminal labeled w. If s:2 were excluded, every selected high would be a degree-one third terminal, contrary to positive upper excess a.
- **X is even.** Summing high labels minus low labels over actual edges, the degree-one contributions total 108−28=80. The excess contributions are X+2(Y+B+T−x−y−a), and must equal 136−80=56. Thus X is even and, when B=8,
  ```
  Y+T = 20+a+x+y−X/2.
  ```
  Also label 16 must lie at a neighbor of the zero host, so X≠16.

## Structural reductions across all first-host labels

**B=10.** The lower count gives k_d=1. Since d≥a+1 and u≥10, B−d+1=11−d≤10−a≤u−a. Thus E_U⊆E_L, also at equality. The upper-selected s:2 has both spine lows as neighbors, forcing k_d=2. This excludes B=10 for every a.

**B=12.** Here k_d=0 and d≤6. If E_U⊆E_L, the selected s:2 again forces both spine lows, a contradiction. Otherwise E_L⊆E_U. Both degree-three pinned lows are selected, forcing their six distinct high neighbors into the upper selection. Hence 17−u≥6 and u≤11, so b:1:0 with label 12 is also selected, taking a seventh slot. Thus u=10 and b:3:0 occupies the remaining nonexit high label 8. Here the upper excess is precisely five (s:0,s:2,b:1:0), so a=5. Then a<d≤6 forces d=6. The six selected nonspine lows include both fourth terminals, whose edges meet b:3:0=8 below the upper cut. This violates E_L⊆E_U.

For **a=7**, d=8 forces B=8, while upper excess seven would select all positive-excess highs including b:1:0. For **a=6**, d is 7 or 8. B=8 makes the maximum available upper excess five. Otherwise B=10 by lower counting and the B=12 obstruction. More explicitly, excess six selects the three degree-three highs and excludes s:0, so B=10 forces u=10. The one-spine-low lower count forces d=7, giving equal tails from 4, and s:2 forces both spine lows. For **a=5** use the proved [D072 obstruction](B4_D071_PINNED_DUAL_BLOCK_OBSTRUCTION.md) with exactly these pins, original, cuts and predicates. For **a=1** the forced s:2 already contributes excess two. It remains to treat B=8 and a=2,3,4.

## B=8 and a=2

Only s:2 among the nonzero excesses is selected. The unselected highs include b:1:0=8, s:4=9, s:0 and b:3:0, so u≥12. At u≥14 the selected edges from s:2 to s:1 and s:3 have weights at least 12. Both spine lows then lie in {1,3,4}, since 0 and 2 are pinned elsewhere. They are distinct, so x+y≤7 and Y≥15. Also T≥10 and X≥10. The identity Y+T=22+x+y−X/2 would give Y+T≤24, against ≥25.

At u=12 the two unselected highs 10 and 11 must be X=10, T=11 by parity. The same subcase occurs at u=13 when the extra unselected terminal is a first terminal with label 12, since its weight 10 leaves exactly [1,9] on the four named high vertices. The edge s:0–b:0:0 gives 8. Among these four highs, weight 9 must be s:0–s:1 with x=1 (T=11 is not adjacent to low label 2, and labels 8 and 9 cannot give 9 on their actual edges). Then b:1:0–s:1 gives 7 and weight 1 forces low 7 on a second terminal. The three neighbors of b:3:0=11 must now have labels at least 5 to give their remaining weights ≤6. Only 5 and 6 are free in that range.

For the other u=13 cases the unselected high labels 10,11,12 belong to X,T and exactly one terminal. A third terminal can only be labeled 10, because the complement is [1,10]. Then X=12 by parity and its edge to A also gives 10, a duplicate. If the extra terminal is a first terminal, its weight is its high label minus 2. After the already rejected (X,T,terminal)=(10,11,12), the remaining possibilities are:

| X,T, terminal label | Contradiction in the unselected edges |
|---|---|
| 10,12,11 | The known first edges use 8 and 9. Weight 10 would need high 10 adjacent to zero or high 12 adjacent to low 2. Neither named incidence exists. |
| 12,11,10 | The known first edges use 10 and 8. Weight 9 forces x=3 on s:0–s:1, and the second attachment gives 5. Fourth-center neighbors must come from {1,4,5,6,7}. Only 4,5,7 give weights in the remaining set {1,2,3,4,6,7}. The second terminals then include low 1 and repeat weight 7 at B. |
| 12,10,11 | The known first edges use 10 and 9. Weight 8 would come from s:0–s:1 at x=4 or the exit at y=1 (T cannot touch A). The latter repeats 9 at b:3:0, so x=4 and the second attachment gives 4. The fourth-center neighbors must be 3,5,7 to give weights in the remaining {1,2,3,5,6,7}. Low 1 at a second terminal repeats weight 7. |

## B=8 and a=3

The nonzero selected excesses are s:0 and s:2. Thus T is unselected along with 8 and 9, requiring u≥11. At u≥15 the selected X must be even and different from 16, impossible. At u=14 this forces X=14 and Y≥15. The selected spine edges imply x≤3 and y≤5, and x≠3 because A is pinned there. Thus x+y≤7, so Y+T=23+x+y−7≤23, against ≥25.

For u=11,12,13 every unselected terminal has label at least 10 and cannot attach to zero, because the complement has maximum u−4≤9. So the unselected high labels [10,u−1] other than T are first terminals, each contributing its label minus 3. The remaining edges are the three edges at B=8, three at b:3:0=T, and the one exit edge. Their six named low vertices use {1,2,4,5,6,7}. The residual weights give these cases:

| T and admissible u | Contradiction in the residual edges |
|---|---|
| 10 at u=11,12,13 | The residual weights are [1,7]. Lows 1,2 cannot meet T (weights 9,8). The only source of weight 1 is B with low 7. Thus B's three low neighbors are 1,2,7, leaving 4,5,6 at T. Weight 6 repeats at B and T. |
| 11 at u=12,13 | The residual weights are [1,6] and 8. Weight 8 cannot come from B at zero or T at A=3. The exit requires y=1, which then gives 10 at T, outside the range. |
| 12 at u=13 | The residual weights are [1,6] and 9. Weight 9 at T would require low 3 at A, so all of T's neighbors must have labels ≥6, with only two available. |

## B=8 and a=4

The selected positive excesses are s:2 and b:3:0. Hence X is unselected along with 8 and 9, so 11≤u≤15. At u=14 there are at least three unselected terminal highs besides X, B and the exit. One must be at zero and give at least 10 against complement maximum 9. At u=15 all four high terminals are unselected, including both third terminals with distinct labels ≥10. One gives at least 11 against complement maximum 10.

For u=11,12,13 any unselected terminal must be first, since the complement maximum u−5≤8. By parity X is 10 or 12.

If X=10, subtract the unselected first-terminal weights [7,u−5] (possibly empty). The remaining [1,6] weights occur on the edges at s:0, B and U. The edge s:0–A already uses 6, so x≥5. The exit requires y≥5. Thus x,y are distinct members of {5,6,7}. The two second terminals must have labels ≥3 and cannot use A=4, so they must take 3 and the remaining member of {5,6,7}. The terminal at 3 uses weight 5. If x=5 then s:0 also gives 5. If x=6 then y=5 gives a repeated 4 with s:0–s:1, and y=7 gives a repeated 2 with B–s:1. If x=7 and y=6, then the exit repeats weight 3 from s:0–s:1. The only candidate is x=7,y=5. Now Y+T=24+7+5−5=31, forcing {Y,T}={15,16}. T cannot be 16 since it does not touch zero. For Y=16,T=15, weight 15 requires 16 adjacent to low 1 or 15 adjacent to zero, neither of which holds at the actual endpoints.

If X=12, then u=13. The other unselected labels 10 and 11 are first terminals, giving weights 6 and 7, and s:0–A gives 8. The remaining weights are [1,5]. Thus s:0–s:1 forces x=7 and uses weight 5. The second attachment uses 1. The exit forces y=5 or 6 because it must use one of 2,3,4. Both second terminals must use 2,3 or 4, requiring low labels among {6,5,4}. Low 4 is pinned at A and one of 5,6 is at s:3, leaving too few.

## Disposition

**ACCEPT the structural obstruction for every a=1..7.** Lower counting and named incidence arguments exhaust all B. The local residual weight arguments exhaust the remaining numerical cuts and do not enumerate complete labelings. D070 is graceful and supplies its own upper tail, while its lower predicate fails. D072 remains the separate pinned result for a=5. This proof rejects only joint same-ledger supply with the given exit, zero host, alpha orientation, original graph and retained cut contracts. No seed, compatibility theorem or path completion is established. See the [bounded arithmetic and reviewed evidence](../evidence/validation/B4_D072_UNPIN_FIRST_HOST_DUAL_BLOCK_001/README.md).
