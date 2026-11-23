# Direct normalized alpha supply on the named 2322 prefix

## Conditional consumer on the original target

Let P be the exact named `[[2],[3],[2],[2],[]]`, with four consecutive spine edges from s:0 to s:4, a center b:i:0 joined to s:i for i=0,1,2,3, and the (2,3,2,2) named terminal leaves joined only to their respective centers. Its 18 vertices and 17 edges are all original. Starting with physical s:4 on the high side, the alpha low names are s:1, s:3, b:0:0, b:2:0, l:1:0:0, l:1:0:1, l:1:0:2, l:3:0:0 and l:3:0:1. All nine remaining names are high. W=b:0:0–s:0–s:1–s:2–s:3–s:4 is an actual path. Every center is on W or adjacent to it. Every terminal is within two edges of W.

Suppose an independently supplied alpha labeling f has low alphabet [0,8], high alphabet [9,17], original weight multiset [1,17] and physical f(s:4)=10. For exact K≥2 the full original `T_K=[[2],[3],[2],[2]]+[[]]*(K+1)` adds just s:5 through s:(K+4), their consecutive spine edges from s:4, and no branches. The only crossing between assigned and unassigned vertices is s:4–s:5. The full order and size are 18+K and 17+K.

Shift the high labels by K and keep the lows. The used labels are [0,8] and [K+9,K+17]. Every original prefix difference gains K, because exactly its larger endpoint moves, so the used differences are [K+1,K+17]. In the full original alphabets this leaves exactly R=[9,K+8] and D=[1,K]. The assigned physical port s:4 has K+10, two above max(R).

Use the numerical [retained nonadjacent recurrence](B2_NONADJACENT_CONSUMER.md#construction-and-proof) as in the [B4 transfer](B4_2222_NONADJACENT_ALL_K.md#recurrence-and-the-physical-path). The bases (3,1,0), (4,1,0,2), (5,1,2,0,3) for K=2,3,4 have starts K+1, tails [0,K−1] once each, and respective weight orders (2,1), (3,1,2), (4,1,2,3). For K≥5 prepend (K+1,1,K−1) to the reflection of all of C_(K−3) under x↦K−2−x. The reflected sequence begins at 0, and the rest of its labels are [2,K−2] once each by induction. Along with 1,K−1,0 this gives the complete tail [0,K−1]. The three edges to the reflected 0 use K,K−2,K−1. The bridge from 0 into the reflected tail is the first edge of the reflected smaller sequence. Together with the later edges it supplies [1,K−3] once each. Decreasing K by three terminates at a base.

Translate by 9 and assign the entries in order to physical s:4,…,s:(K+4). The initial entry agrees with K+10 at s:4. The remaining entries use R and the actual K suffix edges use D exactly, with no changed prefix label. This establishes the conditional fixed-profile theorem. The production B2 wrapper retains its s:2 scope. At K=2 the full path is (12,10,9) with differences (2,1). Its R={9,10} reflects low size 9. D075's offset-three obstruction has low size eight and keeps its scope. At K=1 this interface would use label 9 against port 11, giving weight 2 against D={1}. K=1 lies outside the conditional theorem.

## Direct alpha supplier

Construct the ledger on P itself. To place the large weights, choose b:1:0=17 with terminal labels (0,1,2) and adjacent low s:1=3. Its four original edges then consume [14,17]. At the exit choose s:3=8, b:3:0=9, and fourth-terminal labels (5,6). With s:4=10 the edges from s:3 to s:4 and to b:3:0 have weights 2 and 1, while the fourth-terminal edges have weights 4 and 3. These are construction choices, not extra feasibility conditions.

The unassigned lows b:0:0 and b:2:0 now have labels 4 and 7 in some order. The other six highs have labels [11,16]. Write X=f(s:0) and Y=f(s:2). The remaining nine edges have required total 5+…+13=81. Their signed high-minus-low sum is
`(11+…+16)+X+2Y−(2·3+8+3·(4+7))=34+X+2Y`.
Indeed their high degrees are 2 at s:0, 3 at s:2 and 1 at each of the four remaining terminals. Their low incidences are two at s:1, one at s:3 and three at each of the first and third centers. Thus X+2Y=47. Weight 13 can only join high 16 to low 3, whose remaining high neighbors are s:0 and s:2. X=16 would make Y nonintegral, so Y=16 and X=15. The edge s:2–s:3 already has weight 8. Assigning label 7 to b:0:0 would duplicate that weight on s:0–b:0:0, so b:0:0=4 and b:2:0=7. The remaining original terminal edges need {5,6,7,10}. For the first center 4, only available terminal labels 11 and 14 produce weights in that set. Give those labels to the two first terminals in index order, and give 12 and 13 to the two third terminals in index order.

| Original vertices in order | Labels |
| --- | --- |
| s:0, s:1, s:2, s:3, s:4 | 15, 3, 16, 8, 10 |
| b:0:0, l:0:0:0, l:0:0:1 | 4, 11, 14 |
| b:1:0, l:1:0:0, l:1:0:1, l:1:0:2 | 17, 0, 1, 2 |
| b:2:0, l:2:0:0, l:2:0:1 | 7, 12, 13 |
| b:3:0, l:3:0:0, l:3:0:1 | 9, 5, 6 |

| Original incidence group | Weights in order |
| --- | --- |
| Consecutive spine edges | 12, 13, 8, 2 |
| First attachment, then terminals by index | 11, 7, 10 |
| Second attachment, then terminals by index | 14, 17, 16, 15 |
| Third attachment, then terminals by index | 9, 5, 6 |
| Fourth attachment, then terminals by index | 1, 4, 3 |

The labels in the two physical classes are exactly [0,8] and [9,17], and the displayed weights exhaust [1,17] once each. The first host b:0:0 is the physical low port of label 4 and s:4 is the high port of label 10, yielding A(18,9;4,1) on W. This supplies the hypothesis of the conditional consumer and proves ordinary gracefulness of the exact ordered 2322 profile for every exact integer K≥2. The third center has label 7 and the second center has label 17. This ledger therefore supplies neither the zero-host nor the minimum-high host premise. The theorem is for the fixed branch sizes.
