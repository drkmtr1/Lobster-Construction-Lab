# Alternative alpha supply at the original first host

## Exact domain and structural prefilter

Use the [retained D066 original](../evidence/validation/B4_K2_ALPHA_PREFIX_S4_9_001/prefix_original.json), with profile `[[2],[2],[2],[2],[]]`. The spine has edges s:i–s:(i+1) for 0≤i<4. For 0≤i<4 the center b:i:0 attaches to s:i and its two named terminals attach only to that center. Orientation from high s:4 forces lows s:1, s:3, b:0:0, b:2:0 and the four terminals at sections 1 and 3. They use [0,7], and the complementary nine highs use [8,16]. Fix s:4=9, b:2:0=0 and H=b:0:0 with low label a≥1, and use c∈[10,16] so the exit remains below the shift.

Each original edge has exactly one high endpoint, so selecting the high vertices with labels at least c counts their degrees once per original edge. There are k=17−c such highs. The required complete incidence spectrum [c−a,16] has k+a weights, so the selected excess degrees (degree minus one) must sum to a. Excluding the fixed exit leaves s:0 of excess one, s:2, b:1:0 and b:3:0 of excess two, and the four first and third terminals of excess zero. The coefficient of x^k in `(1+xy)(1+xy²)^3(1+x)^4` records exactly these possible sums by powers of y. For a∈[1,7] the surviving sets are:

| c | Necessary host labels a |
|---:|---|
| 10 | 5,6,7 |
| 11 | 3,4,5,6,7 |
| 12 | 1,2,3,4,5,6,7 |
| 13 | 1,2,3,4,5,6,7 |
| 14 | 1,2,3,4,5,6 |
| 15 | 1,2,3,4 |
| 16 | 1,2 |

This excludes 15 of the 49 numerical pairs by cardinality. The 34 others still require the complete spectrum. The audit records the reason for each excluded pair. The construction uses one of the admitted pairs.

## Analytic construction on the named original

Choose c=10, a=5. The required unselected spectrum is [1,4]. The unselected highs have labels 8 and 9. Since s:4=9 contributes a single edge, put 8 on the degree-three b:3:0 so these highs contribute four edges in total. Put s:3=6 to give weights 2 and 3 against those two highs, and put 7 and 4 on the fourth terminals to supply 1 and 4. The remaining low labels {1,2,3} go on s:1 and the two second terminals.

Write x=f(s:0), y=f(s:2), z=f(b:1:0), and u=f(s:1). Summing weights as high labels minus low labels with their degree multiplicities gives the [D066 weighted degree identity](B4_K2_ALPHA_PREFIX_S4_9.md#direct-analytic-supply-on-p). The degree-one contributions give 108−28=80. The excess contributions are x+2(y+z+8−u−6−5), which must equal 136−80=56. Equivalently y+z=31+u−x/2. The zero-host neighbors are the possible positions for label 16, by difference 16. Choose the high leaf for 16 and y=15 for another zero edge. Take u=2 and x=10, forcing z=13. The edge s:2–s:1 then has weight 13, leaving weight 14 to be supplied by the remaining zero leaf at 14. The first terminals use the remaining high labels 11 and 12. Use original terminal index order as displayed:

| Original named vertices in order | Labels | Original differences |
|---|---|---|
| s:0,s:1,s:2,s:3,s:4 | 10,2,15,6,9 | 8,13,9,3 |
| b:0:0,l:0:0:0,l:0:0:1 | 5,11,12 | 5,6,7 |
| b:1:0,l:1:0:0,l:1:0:1 | 13,1,3 | 11,12,10 |
| b:2:0,l:2:0:0,l:2:0:1 | 0,16,14 | 15,16,14 |
| b:3:0,l:3:0:0,l:3:0:1 | 8,7,4 | 2,1,4 |

The difference rows give consecutive spine weights or branch attachment then the two terminal weights. The labels exhaust [0,16] and the original differences exhaust [1,16]. The eight lows use [0,7], every edge crosses that cut, and the two high vertices below c have exactly the four weights 1,2,3,4. Thus the complete selected spectrum is [5,16]=[c−a,16]. The 17 labels were determined on the prefix before any larger original was labeled. The original digest is `35c75a93573720212045e5dedb66a0d5ccfd5a09900ea12b791ec900938ea4f4`. The [certificate](../evidence/validation/B4_D069_ALT_ALPHA_FIRST_HOST_001/certificates.json) separately binds the new ledger to that digest.

The physical ports are L=H=b:0:0 and U=s:4 on W=b:0:0–s:0–s:1–s:2–s:3–s:4. All original centers are on W or adjacent to their spine vertices on W, and every terminal is within distance two. The distinct low host Z=b:2:0 is one edge from W at s:2. This supplies normalized A(17,8;5,1) and the required fixed ports and hosts.

## Pointwise growth and finite interleavings

Use the [upper-block rule and its compatibility lemma](ALPHA_UPPER_BLOCK_GENERAL_HOST.md#compatibility-with-a-distinct-zero-host) with the [zero-host extension](ALPHA_ZERO_HOST_LEAF_EXTENSION.md). For q=2+h and t=2+k with h,k≥0, the fresh first names l:0:0:j for 2≤j<q attach only to H and get c+j−2. The fresh third names l:2:0:j for 2≤j<t attach only to Z and get 15+h+j. The original names at or above c shift by h, and the other original names keep their labels. The witness and the low class remain fixed.

For clarity about arbitrary finite interleavings, after i first and j third additions the order is 17+i+j and the active cut is c+i. Precisely the original selected highs and the already added third terminals are at or above that cut. A first-host batch shifts these and increases the active cut by its size. Old first leaves remain below the cut and the batch fills its next consecutive first labels. A zero-host batch appends labels starting at 17+i+j above the active cut, keeps the cut fixed, and extends the complete selected edge spectrum by exactly its weights at the zero host. Inductively the selected spectrum is [c+i−a,16+i+j], and the invariant yields precisely the formulas above on every named vertex in either order and every finite interleaving in index order. Each addition is pendant at its own physical center, preserving all old incidences and distances from W. This returns `[[q],[2],[t],[2],[]]`, A(17+h+k,8;5,1), with physical s:4=9. Empty batches are identities.

## Original suffix and ordinary gracefulness

For exact q,t,K≥2 adjoin K empty sections after s:4 on the full original `[[q],[2],[t],[2]]+[[]]*(K+1)`. Its size is m=16+h+k+K. The pending edges are exactly the consecutive K-edge suffix from s:4, with sole crossing s:4–s:5. Shifting every high label by K leaves used labels [0,7]∪[K+8,m]. Each assigned original edge gains K since it crosses the normalized alpha cut. Its assigned difference inventory is [K+1,m]. Thus R=[8,K+7], D=[1,K], and the physical port s:4 has label K+9.

Use the [numerical recurrence](B2_NONADJACENT_CONSUMER.md#construction-and-proof) and [D067's original B4 path argument](B4_2222_NONADJACENT_ALL_K.md#recurrence-and-the-physical-path). Its bases C₂,C₃,C₄ respectively have first entries 3,4,5, tail permutations of [0,K−1], and edge weights 2,1 and 3,1,2 and 4,1,2,3. For K≥5 prepend (K+1,1,K−1) to the reflection of the entire C_(K−3) under x↦K−2−x. The reflected sequence begins at 0, and the other reflected entries use [2,K−2]. The three edges up to 0 use K,K−2,K−1. The bridge from 0 to the next entry and all later reflected edges retain exactly the smaller sequence's [1,K−3] weights. Decreasing K by three terminates at a base. Assign 8+C_K along the actual suffix starting at physical s:4, whose initial value agrees. This uses R and D exactly once and proves ordinary gracefulness for all exact q,t,K≥2 at r=2 and fourth size two. The public B2 wrapper remains scoped to physical s:2. The K=1, q=1 and t=1 boundaries use retained separate constructions. Claim scope and the finite validation procedures are recorded in the [evidence bundle](../evidence/validation/B4_D069_ALT_ALPHA_FIRST_HOST_001/README.md).
