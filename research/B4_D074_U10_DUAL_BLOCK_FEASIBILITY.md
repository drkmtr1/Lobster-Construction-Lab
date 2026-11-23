# Exit-ten dual-block feasibility on the named 2222 original

## Original and meaning of the two predicates

Use the [D066 named original](../evidence/validation/B4_K2_ALPHA_PREFIX_S4_9_001/prefix_original.json), `[[2],[2],[2],[2],[]]`, with graph digest `35c75a93573720212045e5dedb66a0d5ccfd5a09900ea12b791ec900938ea4f4`. Its 16 edges are the four consecutive spine edges, the four attachments s:i–b:i:0, and both named terminals at each center for i=0,1,2,3. The witness W=b:0:0–s:0–s:1–s:2–s:3–s:4 lies on these edges. The first host is on W, the second and zero hosts are one edge from it, and all vertices are within distance two. Terminal indices are retained.

Consider a normalized alpha-graceful labeling with physical U=s:4=10 and Z=b:2:0=0. Write a=f(b:0:0), B=f(b:1:0), X=f(s:0), Y=f(s:2), T=f(b:3:0), x=f(s:1), and y=f(s:3). The actual eight lows use [0,7] and consist of the four degree-three vertices b:0:0,b:2:0,s:1,s:3 and the four degree-one second and fourth terminals. The nine highs use [8,16]. Their degree-two vertex is s:0. Their degree-three vertices are s:2,b:1:0,b:3:0. The other highs are degree-one U and the four first and third terminals.

For integer 11≤u≤16, let E_U be all original edges incident to highs labeled at least u. For a<d≤8, let E_L be all original edges incident to lows labeled below d. These are the [upper-block](ALPHA_UPPER_BLOCK_GENERAL_HOST.md#exact-state-and-incident-edge-hypothesis) and [lower-block](ALPHA_LOWER_BLOCK_LEAF_INSERTION.md#supplied-state-and-hypotheses) selections. All selected edges have one selected endpoint by the alpha orientation. On a simultaneous supplier the required complete spectra are [u−a,16] and [B−d+1,16]. The original edge weight map is injective. Thus each selected edge set equals the inverse image of its weight interval, with containment from the larger start to the smaller and equal sets at equal starts. In particular the complement of E_U uses exactly [1,u−a−1].

## B=8 is necessary and yields a lower block

The d lower-selected lows include the first and zero hosts, both of degree three, and some number k_d of the two degree-three spine lows. Thus |E_L|=d+4+2k_d. Its required length 16−B+d forces B=12−2k_d. Of 8,10,12, label 10 is already occupied at the distinct physical exit.

The upper-selected highs have total excess a above one edge per vertex. This follows from their cardinality 17−u and the required weight count 17−u+a. **s:2 must be upper-selected.** Otherwise weight 16, which must come from 16 next to zero, forces the high 16 onto a third terminal. For each successive weight w=15 down to u, any larger high label is already at a third terminal whose only weight is its own larger label. To supply w requires the high label w adjacent to zero on an actual edge. Under the assumed exclusion of s:2 this again forces a third terminal. At u=16 the base suffices. The resulting all-degree-one selection contradicts a≥1.

For B=12 the lower count gives k_d=0. If E_U⊆E_L, including equality, the two actual edges from s:2 to s:1 and s:3 force both spine lows into E_L. In the other direction, A=b:0:0 and Z are lower-selected and force their six distinct high neighbors into E_U. These are s:0, s:2, and both first and both third terminals. At u≥11 this is only possible with u=11, when high B=12 is also selected. It is distinct from all six and would take a seventh slot. This is impossible. Hence any supplier requires B=8. Then d=8 is a valid lower cut for any a=1..7 because it selects all original edges with weights [1,16]. This reduces joint supply to a complete upper tail on that same pinned map.

## All 19 necessary upper count pairs

With exit 10 and B=8 excluded, the eligible highs are s:2 plus s:0, b:3:0 and four leaves. Select s:2 first. Of the remaining vertices, s:0 contributes excess one, b:3:0 contributes excess two, and the four leaves contribute zero. Choosing 16−u of these six gives the following necessary sets, where a equals two plus the excess of that choice:

| Upper cut u | Necessary a values |
|---:|---|
| 11 | 3,4,5 |
| 12 | 2,3,4,5 |
| 13 | 2,3,4,5 |
| 14 | 2,3,4,5 |
| 15 | 2,3,4 |
| 16 | 2 |

These are 19 count pairs. They require a full spectrum check. In these cases the selected positive excesses are determined by a: s:2 alone at 2, also s:0 at 3, also b:3:0 at 4, and all three at 5.

The degree-weighted sum of actual differences is 136. The once-per-vertex part is 108−28=80, leaving
```
X + 2(Y+B+T−x−y−a) = 56 .
```
Thus X is even, and X≠16 since label 16 must be adjacent to zero. At B=8 this gives
```
Y+T = 20+a+x+y−X/2 .
```

## Eliminating a=2

At u=12 the unselected highs other than B=8 and U=10 carry 9 and 11. These must be X and T, impossible by even X. At u≥14 the selected two spine edges at s:2 require weights at least 12, so x,y≤4 and distinct in {1,3,4}. Hence x+y≤7 and Y≥15. We have T≥9 and X≥12, since highs 8 and 10 are occupied and X is even. The sum identity gives Y+T≤22+7−6=23, against at least 24.

At u=13 the additional unselected labels 9,11,12 go to X,T and one terminal, with X=12. The complete complement is [1,10]. If T=11, the sum identity gives Y=5+x+y. The s:2 spine edges require Y−x,Y−y≥11, giving x,y≥6, whereas those same inequalities with Y≤16 give x,y≤5.

If T=9, the unselected terminal has label 11. It must be first because 11 at zero exceeds the complement maximum. The sum identity gives Y=7+x+y. The two selected s:2 spine edges give x,y≥4, and Y≤16 gives x,y≤5. Then {x,y}={4,5} and Y=16. The selected edges at s:2 weigh 11,12,16, leaving weights 13,14,15 for the remaining first terminal and the two third terminals. The three available labels are 13,14,15. The first terminal at A=2 must receive 15 to give a weight as large as 13. The third terminals would then give 13 and 14, repeating 13 and missing 15.

## Eliminating a=3

Here s:0 and s:2 are selected and T is unselected. At u≥15 even X≠16 is impossible. At u=14, X=14, Y≥15, and the selected spine constraints give x≤3 and y≤5. Since A carries 3, x≤2. The sum identity gives Y+T≤23+7−7=23 against Y+T≥24.

For u=11,12,13 the complement is [1,u−4]. After subtracting edges of any unselected first or third terminals, the remaining seven edges are exactly the three at B, the three at b:3:0 and the exit edge. Their six distinct low names use {1,2,4,5,6,7}.

- **T=9.** Any additional unselected highs are from labels 11,12 and must be first terminals since their labels exceed the complement maximum. Subtract their weights to leave [1,7]. Low 1 must meet B because T=9 would give 8 and the exit would give 9. Weight 1 forces low 7 at B. Low 2 then also meets B, because T=9 would repeat weight 7; the exit's low endpoint is among T's neighbors. Thus the lows at B are 1,2,7 and those at T are 4,5,6. The exit gives 6,5 or 4, all already used.
- **T=11.** This occurs at u=12 or 13. At u=13 the unselected terminal 12 must be first and gives 9. The other terminal 9 must be first, since at u=12 its zero weight exceeds the complement and at u=13 it would repeat weight 9. It gives 6. The residual weights are {1,2,3,4,5,7,8}. T's low neighbors must be 4,6,7: the maximum weight is 8, low 3 is occupied at A, and low 5 would repeat 6. Low 2 then meets B and gives the already used 6.
- **T=12.** Here u=13. The terminal 11 must be first and gives 8. If terminal 9 is first, subtract 6 and 8 to leave {1,2,3,4,5,7,9}. Only the two free labels 5 and 7 give incident weights in that set at T, which needs three distinct lows. If terminal 9 is third, subtract 9 and 8 to leave [1,7]. The three lows at T must be 5,6,7, while the remaining lows 1,2,4 meet B. Weight 7 then repeats at B and T.

## Eliminating a=4

Only s:2 and b:3:0 contribute positive selected excess. Thus X is unselected. At u=11 this forces X=9. At u=12 it forces X in {9,11}. Both violate parity.

At u=13, X=12 by parity and the other unselected labels 9,11 must be first terminals because the complement ends at 8. Their weights are 5,7, and s:0–A gives 8. This leaves {1,2,3,4,6} for s:0–s:1, the three edges at B, and the exit edge. As 12−x≥5, x=6 and that edge uses 6. The second attachment uses 2. The exit can now only use 3, giving y=7: weight 1 needs low 9 and weight 4 needs the already used low 6. The remaining weight 1 would need low 7 at a second terminal, but it is at s:3.

At u=14, X=12 by parity and the other unselected labels 9,11,13 go to three terminals. The complement ends at 9, so at least one must be third and only 9 can be third. The first terminal at 13 then also gives 9. At u=15 all four first and third terminals are unselected. Their two zero-host labels come from [9,14] excluding 10, so one is at least 11, above the complement maximum of 10.

## Eliminating a=5

Both s:0 and b:3:0 join s:2. The complement ends at u−6. At u=13 or 14 at least three terminals are unselected, with labels ≥9 other than 10. None can be third because the complement ends at most at 8. There are only two first terminals.

At u=11 the unselected terminal 9 is first and gives 4. At u=12 the unselected terminals 9 and 11 must both be first and give 4 and 6. In either case the residual weights on the three edges at B and the exit are {1,2,3,5}. At B=8 only free lows 3,6,7 can give weights in that set: low 5 is already at A. These give 5,2,1, so the exit must give 3, forcing y=7. But s:3 is distinct from all three low neighbors of B, which already use 7.

## Exact continuation gate and disposition

**EXHAUSTED RESTRICTED NEGATIVE by structural proof.** All 19 necessary upper pairs fail after the B reduction. This excludes the complete simultaneous premises on this exact normalized named original at s:4=10 and b:2:0=0 for all free first-host labels. The proof is independent of a feasibility search. D073 and D074 retain their separate scopes.

Even under a hypothetical normalized exit-ten supplier, shifting every high by K with p=8 would give R=[8,K+7], D=[1,K] and physical exit K+10=max(R)+3. At K=2 the pending original path begins s:4–s:5. The two possible labels at s:5 are 8 and 9, so its first difference from exit 12 is 4 or 3. Neither lies in D={1,2}. A hypothetical lower-block batch of j leaves would change the low size to p=8+j and physical exit to p+2, keeping that offset. The same K=2 calculation gives R={p,p+1}, exit p+4, and possible weights 4 and 3.

The gate concerns the proposed shifted-prefix interface. Other labelings and other continuation mechanisms require separate arguments. There is no new triple-growth compatibility, all-K consumer, or ordinary-nongracefulness result. See the [bounded audit](../evidence/validation/B4_D074_U10_DUAL_BLOCK_FEASIBILITY_001/README.md).
