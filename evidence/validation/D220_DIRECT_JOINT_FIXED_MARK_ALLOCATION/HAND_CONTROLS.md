# D220 named originals and hand arithmetic

## Original incidence definitions

The independently specified profile is `[[2],[2,2],[2,2,2,2,2],[2]]`. The definition below fixes both graphs without using certificate labels.

- The spine vertices are s:0, s:1, s:2 and s:3. Include s:0--s:1, s:1--s:2 and s:2--s:3 in both graphs.
- The nine centers are b:0:0, b:1:0, b:1:1, b:2:0, b:2:1, b:2:2, b:2:3, b:2:4 and b:3:0. For each b:i:j there are exactly two terminals l:i:j:0 and l:i:j:1. Include exactly the two edges from the center to those terminals in both graphs.
- In the original T, attach each b:i:j to s:i. In the folded source S, attach b:0:0 to s:1 and b:3:0 to s:2. All seven interior attachments remain b:i:j--s:i.

These exhaust the incidence sets. Each graph has 4+9+18=31 distinct named vertices and 3+9+18=30 edges. Since the branch subtrees attach singly to the spine, both are connected and acyclic. In particular, folding does not reconstruct the original by merging or renaming vertices.

## Fixed-mark Arm A positive

The spine labels in original order are (29,0,30,5). The actual weights of its three common edges in order are (29,30,25). Each terminal tuple below is in increasing original terminal index order. The attachment columns independently subtract the labels on the actual parent edges in each graph.

| Center | Label | Terminal labels | Actual terminal differences | S attachment | T attachment |
|---|---:|---|---|---|---|
| b:0:0 | 2 | (14,22) | (12,20) | s:1, 2 | s:0, 27 |
| b:1:0 | 1 | (23,24) | (22,23) | s:1, 1 | s:1, 1 |
| b:1:1 | 28 | (7,18) | (21,10) | s:1, 28 | s:1, 28 |
| b:2:0 | 4 | (15,20) | (11,16) | s:2, 26 | s:2, 26 |
| b:2:1 | 6 | (12,13) | (6,7) | s:2, 24 | s:2, 24 |
| b:2:2 | 25 | (10,11) | (15,14) | s:2, 5 | s:2, 5 |
| b:2:3 | 26 | (9,17) | (17,9) | s:2, 4 | s:2, 4 |
| b:2:4 | 27 | (8,19) | (19,8) | s:2, 3 | s:2, 3 |
| b:3:0 | 3 | (16,21) | (13,18) | s:2, 27 | s:3, 2 |

The label blocks in both graphs are the two inner roots {0,30}, the eleven slots [1,6] ∪ [25,29], and eighteen terminals [7,24]. Their union is [0,30], with each coordinate used once. The physical marks in order (s:1,s:2,s:0,s:3,b:0:0,b:3:0) are (0,30,29,5,2,3).

The S attachment column in table order gives (2,1,28,26,24,5,4,3,27). With the three spine edges the S skeleton spectrum is [1,5] ∪ [24,30]. The T attachment column gives (27,1,28,26,24,5,4,3,2), which gives the same spectrum with the three spine edges. The eighteen displayed terminal differences sort to [6,23]. Thus each graph has spectrum [1,30] with multiplicity one. In particular the roots are the original physical roots, the restored edges have weights |29−2|=27 and |5−3|=2, and the terminal incidences stay intact.

The high hosts 25,26,27,28 have normalized terminal index pairs (3,4), (2,10), (1,12), (0,11). Their sum is 7+12+13+11=43. The allocation preserves both complete resource inventories by direct assignments on the fixed skeleton.

## Sequential all-quota-two control at h=5

The initial palette at host 1 is [7,24]. At each departure two labels must stay at the actual departing host. This is the separately calculated h=5 instance of the proof's invariant intersections.

| Move | Reflection sum | Retained at departing host | Moved palette, or obstruction |
|---|---:|---|---|
| 1 → 28 | 29 | 23,24 | [7,22] |
| 28 → 2 | 30 | 7,15 | [8,14] ∪ [16,22] |
| 2 → 27 | 29 | 14,22 | [8,13] ∪ [16,21] |
| 27 → 3 | 30 | 8,16 | [9,13] ∪ [17,21] |
| 3 → 26 | 29 | 13,21 | [9,12] ∪ [17,20] |
| 26 → 4 | 30 | 9,17 | [10,12] ∪ [18,20] |
| 4 → 25 | 29 | 12,20 | {10,11,18,19} |
| 25 → 6 | 31 | Two required | Reflection gives {12,13,20,21}, disjoint from the active palette |

Host 6 still needs two terminals in the last row. The forced sequence therefore fails even when the moved subsets need not have a prescribed shape. The Arm A assignment above is joint and meets this original's nine quotas.

## Retained D219 controls

These inventories come from the actual D219 named controls and apply the skeleton rule to their own quotas. Neither graph extends the registered D220 domain. [D219 hand controls](../D219_MARKED_PHASE_TRANSITION_SUPPLIER/HAND_CONTROLS.md).

| D219 control | Left slots | Right slots | Skeleton slot weights W | Remaining labels | Remaining differences |
|---|---|---|---|---|---|
| 30-edge mixed | {1,2,6,24,28,29} | {3,4,5,7,25,26,27} | [1,6] ∪ [23,29] | [8,23] | [7,22] |
| 32-edge all-even | {1,2,30,31} | {3,4,5,6,27,28,29} | [1,5] ∪ [26,31] | [7,26] | [6,25] |

For the mixed control, reflecting the right slots in 30 gives {27,26,25,23,5,4,3}. For the all-even control, reflecting the right slots in 32 gives {29,28,27,26,5,4,3}. Each reflected set is disjoint from its left slots. The restored edges exchange respectively 2 with 27 and 2 with 29. Their actual terminal differences fill their corresponding remaining difference intervals as recorded in D219. Some quotas differ from two, so the nine quota-two row classes of D220 do not apply to either control.

All D220 arithmetic above is hand work. There were no protected checker calls, scientific module executions, diagnostic preparations or solver invocations.
