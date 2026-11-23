# Fixed-ledger upper-block obstruction on the D066 prefix

## Original and admissible cuts

Use only the independently supplied [D066 original and ledger](../evidence/validation/B4_K2_ALPHA_PREFIX_S4_9_001/README.md) on `[[2],[2],[2],[2],[]]`. The original graph digest is `35c75a93573720212045e5dedb66a0d5ccfd5a09900ea12b791ec900938ea4f4`. Its separate named ledger ID is `a84d6183c8a6f97aa0a8d5aed6efb6122ed8029c7526e9fefd8bb242f0d108be`. The five consecutive spine vertices have labels 10,2,16,7,9 in order. The four center/terminal triples in section order are (6,12,13), (14,1,4), (0,15,11), and (8,3,5). Every center attaches to its own spine section and every terminal to its own center. The spine weights in order are 8,14,9,2. The attachment and two terminal weights by branch are (4,6,7), (12,13,10), (16,15,11), and (1,5,3). The labels exhaust [0,16] and these 16 weights exhaust [1,16].

The spine is high, low, high, low, high at the cut between 7 and 8. Centers lie opposite their own spine vertices and terminals opposite their centers. The eight lows use [0,7] and the nine highs use [8,16]. The original witness W is b:0:0–s:0–s:1–s:2–s:3–s:4. Every vertex is within distance two of W by its original attachment. Its low end and first insertion host are the same physical b:0:0=6. Its high exit is s:4=9, and the third zero host b:2:0=0 is one edge from W at s:2.

The [general-host rule](ALPHA_UPPER_BLOCK_GENERAL_HOST.md#exact-state-and-incident-edge-hypothesis) requires c strictly above the exit and at most the highest old label. These conditions give exactly c=10,…,16. Each selected vertex with label at least c is high, and every low lies below c. Therefore every original edge incident to a selected high crosses c and has a single selected endpoint. The selected original weight multiset must be [c−6,16], of size 23−c.

## Complete incidence calculation

Each row below includes all the weights at the indicated high endpoint. The two below-threshold high endpoints, s:4=9 and b:3:0=8, contribute weights (2) and (1,5,3) respectively. Together the high endpoint groups partition all 16 original edges.

| High name | Label | Original low neighbors with weights |
|---|---:|---|
| s:0 | 10 | s:1 (8), b:0:0 (4) |
| l:2:0:1 | 11 | b:2:0 (11) |
| l:0:0:0 | 12 | b:0:0 (6) |
| l:0:0:1 | 13 | b:0:0 (7) |
| b:1:0 | 14 | s:1 (12), l:1:0:0 (13), l:1:0:1 (10) |
| l:2:0:0 | 15 | b:2:0 (15) |
| s:2 | 16 | s:1 (14), s:3 (9), b:2:0 (16) |

For each cut, take the union of the groups whose labels are at least c. Each listed weight occurs once. The independent receipts retain every named selected edge and endpoints.

| c | Selected weight multiset | Actual / required count | Deficit | Missing weights | Excess weights |
|---:|---|---:|---:|---|---|
| 10 | 4,6,7,8,9,10,11,12,13,14,15,16 | 12 / 13 | 1 | 5 | ∅ |
| 11 | 6,7,9,10,11,12,13,14,15,16 | 10 / 12 | 2 | 5,8 | ∅ |
| 12 | 6,7,9,10,12,13,14,15,16 | 9 / 11 | 2 | 8,11 | ∅ |
| 13 | 7,9,10,12,13,14,15,16 | 8 / 10 | 2 | 8,11 | ∅ |
| 14 | 9,10,12,13,14,15,16 | 7 / 9 | 2 | 8,11 | ∅ |
| 15 | 9,14,15,16 | 4 / 8 | 4 | 10,11,12,13 | ∅ |
| 16 | 9,14,16 | 3 / 7 | 4 | 10,11,12,13,15 | 9 |

## Necessary edge sum for every positive batch

Fix any admissible c and integer h≥1. Raise the old labels at least c by h, keep those below c, and give the h fresh first terminals l:0:0:j, j=2,…,h+1, labels c+j−2. Each terminal attaches only to the same original b:0:0. All old incidences are retained, s:4 stays at 9, and the new graph is exactly `[[2+h],[2],[2],[2],[]]`. Pendant additions give a tree with 16+h edges, and the three label bands [0,c−1], [c,c+h−1], [c+h,16+h] partition its full alphabet. The same witness remains valid.

Each of the |E_c| selected original edges gains exactly h because its single shifted endpoint was already the larger endpoint. The other original edges retain their weights. The unchanged host 6 gives new weights c−6,…,c+h−7. The old weight sum is 136, so the sum of the resulting multiset is

```
136 + h*|E_c| + h*(c−6) + h*(h−1)/2.
```

Gracefulness requires the sum of [1,16+h], or 136+17h+h(h−1)/2. Subtracting the actual sum from this required sum gives h(23−c−|E_c|). Every deficit in the table is positive. The edge sum therefore rules out every positive batch, independently of whether the sufficient spectrum hypothesis of the general-host theorem is invoked. This is the same edge-by-edge obstruction method as the [fixed 1342 proof](B4_1342_FIXED_LEDGER_UPPER_BLOCK_OBSTRUCTION.md) applied to these different named incidences, host value and alphabet. At h=0 both sums equal 136 and the operation returns the D066 ledger unchanged.

**EXHAUSTED RESTRICTED NEGATIVE.** All seven admissible cuts fail on this fixed ledger, at this host and exit, for the prescribed operation. The result leaves other labelings and insertion rules open. The established [D067 suffix continuation](B4_2222_NONADJACENT_ALL_K.md) and [D068 third-host growth and selector](B4_22T2_ZERO_HOST_ALL_TK.md) retain their domains. The [bounded evidence](../evidence/validation/B4_D068_FIRST_HOST_UPPER_BLOCK_001/README.md) includes a retained D068 positive completion and the independently reconstructed receipts.
