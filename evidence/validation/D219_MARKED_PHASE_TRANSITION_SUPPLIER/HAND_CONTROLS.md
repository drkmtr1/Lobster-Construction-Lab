# D219 named hand controls

The spine labels are in the actual order `s:0,s:1,s:2,s:3`. Each row `b:i:u` gives every terminal at the actual index `l:i:u:e` in order. The source S folds only `b:0:0` and `b:3:0` inward to the adjacent interior roots. The original T restores those two attachments outward. In all edge tables, each terminal weight is the direct absolute subtraction of its own listed parent label, in terminal index order.

## 1. Mixed-phase positive

The exact original is `[[1],[2,1,2,2],[1,2,1,1,2],[1]]`. It has ℓ=4, j=5, R=13, h=6, F=16 and m=30. The initial terminal interval is [8,23], the spine-end reserves are 29 and 5, and the roots are 0 and 30. The slots have bands [1,7] and [24,29]. At the initial root 30 their weights are [23,29] and [1,6]. Together with the root edge 30 and the terminals initially at 1, of weights [7,22], they fill [1,30].

| Single-interval host → next | Input interval | Δ | Retained at current host | Output interval |
|---|---|---:|---|---|
| 1 → 28 | [8,23] | −2 | (22,23) | [8,21] |
| 28 → 2 | [8,21] | +1 | (8) | [9,21] |
| 2 → 27 | [9,21] | −1 | (21) | [9,20] |
| 27 → 3 | [9,20] | +1 | (9) | [10,20] |
| 3 → 26 | [10,20] | −1 | (20) | [10,19] |
| 26 → 4 | [10,19] | +1 | (10) | [11,19] |
| 4 → 25 | [11,19] | −1 | (19) | [11,18] |
| 25 → 6 | [11,18] | +2 | (11,12) | [13,18] |

Each output endpoint sum is the sum of its two actual host labels. Split [13,18] into [13,15] and [16,18] before 6. The starting cross-sum is 31.

| Two-interval host → next | Input intervals | Δ | (a,λ,ν) | Retained | Moved intervals | New cross-sum |
|---|---|---:|---|---|---|---:|
| 6 → 24 | [13,15], [16,18] | −1 | (1,0,0) | (15,18) | [13,14], [16,17] | 30 |
| 24 → 7 | [13,14], [16,17] | +1 | (1,1,1) | (13,16) | [14,14], [17,17] | 31 |
| 7 final | [14,14], [17,17] | — | — | (14,17) | — | — |

The left pairs are (1,29), (2,28) and (6,24). The right pairs are (3,27), (4,26) and (5,25), and final slot 7 stays right. Moving the left actual pairs to root 0 swaps their initial weights pair by pair. This gives the actual fold.

Both graphs have spine labels (29,0,30,5), giving spine weights (29,30,25). They retain the following named branch and terminal labels. The two attachment columns are computed independently with the actual parent of each graph.

| Named branch | Center | Indexed terminal labels | Terminal weights | S parent and weight | T parent and weight |
|---|---:|---|---|---|---|
| `b:0:0` | 2 | (21) | (19) | `s:1`, 2 | `s:0`, 27 |
| `b:1:0` | 1 | (22,23) | (21,22) | `s:1`, 1 | `s:1`, 1 |
| `b:1:1` | 28 | (8) | (20) | `s:1`, 28 | `s:1`, 28 |
| `b:1:2` | 6 | (15,18) | (9,12) | `s:1`, 6 | `s:1`, 6 |
| `b:1:3` | 24 | (13,16) | (11,8) | `s:1`, 24 | `s:1`, 24 |
| `b:2:0` | 27 | (9) | (18) | `s:2`, 3 | `s:2`, 3 |
| `b:2:1` | 25 | (11,12) | (14,13) | `s:2`, 5 | `s:2`, 5 |
| `b:2:2` | 26 | (10) | (16) | `s:2`, 4 | `s:2`, 4 |
| `b:2:3` | 4 | (19) | (15) | `s:2`, 26 | `s:2`, 26 |
| `b:2:4` | 7 | (14,17) | (7,10) | `s:2`, 23 | `s:2`, 23 |
| `b:3:0` | 3 | (20) | (17) | `s:2`, 27 | `s:3`, 2 |

The transfer retentions cover [8,23] once. The spine and centers use its exact complement in [0,30]. The attachment list in S is (2,1,28,6,24,3,5,4,26,23,27) and in T is (27,1,28,6,24,3,5,4,26,23,2). Each list with the spine weights is [1,6]∪[23,30] once. The common terminal weights read (19,21,22,20,9,12,11,8,18,14,13,16,15,7,10,17), exactly [7,22] once. Thus the complete S and T spectra are [1,30] with the actual weights 2 and 27 exchanged. There are 31 named vertex labels in each graph.

## 2. All-even positive

The exact original is `[[2],[2,2],[2,4,2,2,2],[2]]`. It has ℓ=2, j=5, R=11, h=5, F=20 and m=32. The initial terminal interval is [7,26] and its initial weight band at 1 is [6,25]. The slots [1,6] and [27,31] give [26,31] and [1,5] at root 32, and the root edge has weight 32. The two reserves are 31 and 5.

In the one-interval phase the move 1→30 has Δ=−2. Retain (25,26) at 1 and move [7,24], of endpoint sum 31, to 30. Splitting this interval gives [7,15] and [16,24], both length nine and cross-sum 31. Since h=5, 27=m−5 transfers directly to the final host 6.

| Two-interval host → next | Input intervals | Δ | (a,λ,ν) | Retained | Moved intervals | New cross-sum |
|---|---|---:|---|---|---|---:|
| 30 → 2 | [7,15], [16,24] | +1 | (1,1,1) | (7,16) | [8,15], [17,24] | 32 |
| 2 → 29 | [8,15], [17,24] | −1 | (1,0,0) | (15,24) | [8,14], [17,23] | 31 |
| 29 → 3 | [8,14], [17,23] | +1 | (1,1,1) | (8,17) | [9,14], [18,23] | 32 |
| 3 → 28 | [9,14], [18,23] | −1 | (1,0,0) | (14,23) | [9,13], [18,22] | 31 |
| 28 → 4 | [9,13], [18,22] | +1 | (1,1,1) | (9,18) | [10,13], [19,22] | 32 |
| 4 → 27 | [10,13], [19,22] | −1 | (1,0,0) | (13,22) | [10,12], [19,21] | 31 |
| 27 → 6 | [10,12], [19,21] | +2 | (2,2,2) | (10,11,19,20) | [12,12], [21,21] | 33 |
| 6 final | [12,12], [21,21] | — | — | (12,21) | — | — |

The left pairs (1,31) and (2,30) move to root 0. The right pairs (3,29), (4,28) and (5,27) and final slot 6 stay right. This gives the exact folded incidences. The actual spine labels are (31,0,32,5) with weights (31,32,27).

| Named branch | Center | Indexed terminal labels | Terminal weights | S parent and weight | T parent and weight |
|---|---:|---|---|---|---|
| `b:0:0` | 2 | (15,24) | (13,22) | `s:1`, 2 | `s:0`, 29 |
| `b:1:0` | 1 | (25,26) | (24,25) | `s:1`, 1 | `s:1`, 1 |
| `b:1:1` | 30 | (7,16) | (23,14) | `s:1`, 30 | `s:1`, 30 |
| `b:2:0` | 29 | (8,17) | (21,12) | `s:2`, 3 | `s:2`, 3 |
| `b:2:1` | 27 | (10,11,19,20) | (17,16,8,7) | `s:2`, 5 | `s:2`, 5 |
| `b:2:2` | 28 | (9,18) | (19,10) | `s:2`, 4 | `s:2`, 4 |
| `b:2:3` | 4 | (13,22) | (9,18) | `s:2`, 28 | `s:2`, 28 |
| `b:2:4` | 6 | (12,21) | (6,15) | `s:2`, 26 | `s:2`, 26 |
| `b:3:0` | 3 | (14,23) | (11,20) | `s:2`, 29 | `s:3`, 2 |

The terminal retentions cover [7,26] once. The spine and centers give all other labels in [0,32]. The attachment list in S is (2,1,30,3,5,4,28,26,29) and in T is (29,1,30,3,5,4,28,26,2). Each list with the spine weights partitions [1,5]∪[26,32]. The common terminal weights are (13,22,24,25,23,14,21,12,17,16,8,7,19,10,9,18,6,15,11,20), exactly [6,25]. This verifies each actual full spectrum [1,32] and the exchange 2 with 29. There are 33 named vertex labels in each graph.

## 3. Adverse boundary for the fixed recipe

For entirely quota-two originals, a split at the first host 1 would require a≥2 for |Δ|=2. The supplied quota Q=2 gives a=1. The first departure must therefore use one interval. The second departure m−2 has Δ=+1 and cannot retain an even quota in one interval, so the split must occur between these two departures. The later departure m−5 has Δ=+2 and needs a≥2 in the two-interval phase. Again Q=2 gives a=1. This failure holds for both h=5 size splits and for larger h. It excludes only this order and declared single-switch trimming regime. There is no inference about other marked certificates, other geometric moves or ordinary existence.

All control arithmetic was done by hand. No diagnostic, solver, original-target checker or scientific module ran.

[Primary mathematical manuscript](../../../research/INDEPENDENT_MARKED_PHASE_TRANSITION_SUPPLIER.md)
