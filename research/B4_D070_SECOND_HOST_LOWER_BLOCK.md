# Restricted second-host lower-block obstruction on the D070 family

## Supplied states and exact cuts

Use only the [D070 supplied normalized maps](B4_D069_ALT_ALPHA_FIRST_HOST.md) on `P(q,t)=[[q],[2],[t],[2],[]]` for exact q,t≥2. Let h=q−2 and k=t−2. The seed P(2,2) uses the retained [D066 named original](../evidence/validation/B4_K2_ALPHA_PREFIX_S4_9_001/prefix_original.json) (digest `35c75a93573720212045e5dedb66a0d5ccfd5a09900ea12b791ec900938ea4f4`) and the distinct [D070 labeling ledger](../evidence/validation/B4_D069_ALT_ALPHA_FIRST_HOST_001/seed.json) (ID `1082f21587d2efc147336fde7d2b5696bb37ff984166140cfb2b0bb2a3408b37`). In D070 the seed is directly supplied on these incidences.

The seed spine labels are (10,2,15,6,9). The center and two terminal labels in each branch are (5,11,12), (13,1,3), (0,16,14), (8,7,4). The spine is high, low, high, low, high. Each branch center is opposite its spine attachment and each terminal opposite its center. The classes use [0,7] and [8,16] respectively. Grouping all actual edges by their unique low endpoint gives the following exhaustive partition.

| Low label | Physical low endpoint | Its original high neighbors with differences |
|---:|---|---|
| 0 | b:2:0 | s:2 (15), l:2:0:0 (16), l:2:0:1 (14) |
| 1 | l:1:0:0 | b:1:0 (12) |
| 2 | s:1 | s:0 (8), s:2 (13), b:1:0 (11) |
| 3 | l:1:0:1 | b:1:0 (10) |
| 4 | l:3:0:1 | b:3:0 (4) |
| 5 | b:0:0 | s:0 (5), l:0:0:0 (6), l:0:0:1 (7) |
| 6 | s:3 | s:2 (9), s:4 (3), b:3:0 (2) |
| 7 | l:3:0:0 | b:3:0 (1) |

The differences exhaust [1,16] once each. The physical witness W=b:0:0–s:0–s:1–s:2–s:3–s:4 stays on the same names. Each center is on W or adjacent to its attachment on W. Each terminal is within distance two, and B=b:1:0 is at distance one from W through s:1. The actual ports L=b:0:0=5 and U=s:4=9, and the distinct zero host Z=b:2:0=0, retain their labels on all supplied P(q,t).

For the [lower-block rule](ALPHA_LOWER_BLOCK_LEAF_INSERTION.md#supplied-state-and-hypotheses) the threshold inequality is x<c≤p with x=5, p=8, giving exactly c=6,7,8. Write S_c for the physical vertices with labels below c and E_c for their original incident edges. All such vertices are low, every high is at or above c, and every edge has precisely one low endpoint. Thus E_c counts each crossing exactly once. Its required difference multiset for a high host with current label B is [B−c+1,m], of length m−B+c.

## Complete spectra and counts

The table of low incidences yields these seed spectra. The archived P(3,3) adds one first and one third terminal with h=k=1. Its old weights 5 through 16 rise by one because their unique high endpoints are precisely the selected highs of the D070 cut at 10. Weights 1 through 4 stay, the fresh first edge has weight 5, and the fresh third edge has weight 18. For each c the low endpoints select the same old edges and both new ones.

| Prefix | c | Actual difference multiset (each once) | Required interval | Actual / required count |
|---|---:|---|---|---|
| P(2,2) | 6 | 4,5,6,7,8,10,11,12,13,14,15,16 | [8,16] | 12 / 9 |
| P(2,2) | 7 | [2,16] | [7,16] | 15 / 10 |
| P(2,2) | 8 | [1,16] | [6,16] | 16 / 11 |
| P(3,3) | 6 | 4,5,6,7,8,9,11,12,13,14,15,16,17,18 | [9,18] | 14 / 10 |
| P(3,3) | 7 | [2,18] | [8,18] | 17 / 11 |
| P(3,3) | 8 | [1,18] | [7,18] | 18 / 12 |

In all D070 states only old labels at least ten shift by h. Each fresh first terminal l:0:0:u, 2≤u<q, has label u+8 and meets low port 5. Each fresh third terminal l:2:0:u, 2≤u<t, has label 15+h+u and meets zero. Both lists consist entirely of high leaves. No old name switches sides at any lower cut. Every new edge meets an unchanged low vertex below all three cuts, so |E_c| grows by exactly h+k. The high host B=b:1:0, initially 13, has current label 13+h. The edge count is m=16+h+k. Therefore the required interval length is c+k+3, and the actual counts are 12+h+k, 15+h+k and 16+h+k. Their surpluses are h+3, h+5 and h+5 for c=6,7,8 in order.

These normalized maps themselves exhaust their label and difference alphabets. As a numerical resource check on their accepted r=2 continuations, shifting every high by K gives R=[8,K+7], D=[1,K], and physical s:4=K+9 as in D070. The finite audit records this at K=2 using the same two prefixes. No new original or suffix completion is required for this obstruction.

## Difference-sum necessity for every positive batch

Fix any supplied D070 state, any of its three cuts, and an exact integer batch size j≥1. In the prescribed operation the old labels below c stay fixed and the others gain j. The i-th new second terminal l:1:0:(i+1) receives c+j−i for 1≤i≤j, and attaches only to B. The old named incidences remain. All these pendant additions produce the exact original `[[q],[2+j],[t],[2],[]]`, with m+j edges and the same witness W. The label bands [0,c−1], [c,c+j−1] and [c+j,m+j] partition the enlarged alphabet, so the transformation yields a bijection. Its low class has size 8+j, the low port and zero host stay at 5 and 0, and the same physical exit and host rise to 9+j and B+j.

Every old high moves. The selected low endpoints stay, so exactly the weights of E_c gain j. Both endpoints on the other old edges move equally and keep their differences. The new weights at the shifted host B+j are B−c+i for i=1,…,j. If M=m(m+1)/2, the actual total difference sum is M+j|E_c|+j(B−c)+j(j+1)/2. The graceful required total is M+jm+j(j+1)/2. Their difference is

```
actual − required = j (|E_c| − (m − B + c)).
```

The actual sum is larger by j(h+3) at cut 6 and j(h+5) at cuts 7 and 8, for every h,k≥0 and j≥1. This rules out gracefulness under the specified insertion operation across the supplied D070 q,t family even though the original graph and label bijection are correct. At j=0 there are no new terminals or shifts, and the accepted D070 labeling is the identity output.

**ACCEPT the restricted obstruction.** Its scope is the given D070 maps, lower-block operation, physical second host and port-admissible cuts. Other suppliers and second-host transitions remain open. The [bounded evidence](../evidence/validation/B4_D070_SECOND_HOST_LOWER_BLOCK_001/README.md) verifies six complete spectra and the symbolic coefficients by independent arithmetic. The positive D070 theorem keeps its scope.
