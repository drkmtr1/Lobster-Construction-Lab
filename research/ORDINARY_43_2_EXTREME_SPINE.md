# D105 — Ordinary graceful labeling with extreme physical spine labels

The target is the frozen named [D099 original](../evidence/validation/LCL_R241_43_2_LOWER_BLOCK_001/original.json) with ordered quotas `[[4,3],[2]]` and graph digest `2060a4e5a7d8f8ebc1906499facea2730250938d4550bb4c6ca34582a1f5b6e6`. The spine is `s:0--s:1`. Its left endpoint has centers `b:0:0` and `b:0:1`, with four and three indexed terminals. Its right endpoint has center `b:1:0` with two indexed terminals. Each indexed terminal is adjacent only to its own center. This gives two spine vertices, three centers and nine terminals. The spine and the three attachments together with the nine terminal edges exhaust the 13 original incidences. Each center is adjacent to its spine vertex, so all vertices have distance at most two from the spine.

## Direct assignment and exact inventories

Give `s:0` label 0 and `s:1` label 13. Give `b:0:0`, `b:0:1` and `b:1:0` labels 10, 9 and 1, respectively. At those three centers give the increasing terminal indices the lists `(2,3,8,11)`, `(4,5,6)` and `(7,12)`, respectively. The lists follow the frozen branch roles and contain one label per actual terminal. Writing the two spine labels, three center labels and three fixed indexed lists terminates after 14 label assignments and needs no search.

The spine and centers use {0,1,9,10,13}. The three terminal lists give {2,3,4,5,6,7,8,11,12} with no repeated entries. Hence all labels [0,13] occur exactly once. Both physical spine pins hold.

| Original edge, in frozen order | Signed difference from the class containing s:0 | Absolute difference |
| --- | ---: | ---: |
| s:0--s:1 | 13−0 = 13 | 13 |
| s:0--b:0:0 | 10−0 = 10 | 10 |
| b:0:0--l:0:0:0 | 10−2 = 8 | 8 |
| b:0:0--l:0:0:1 | 10−3 = 7 | 7 |
| b:0:0--l:0:0:2 | 10−8 = 2 | 2 |
| b:0:0--l:0:0:3 | 10−11 = −1 | 1 |
| s:0--b:0:1 | 9−0 = 9 | 9 |
| b:0:1--l:0:1:0 | 9−4 = 5 | 5 |
| b:0:1--l:0:1:1 | 9−5 = 4 | 4 |
| b:0:1--l:0:1:2 | 9−6 = 3 | 3 |
| s:1--b:1:0 | 13−1 = 12 | 12 |
| b:1:0--l:1:0:0 | 7−1 = 6 | 6 |
| b:1:0--l:1:0:1 | 12−1 = 11 | 11 |

The four spine and attachment weights are {9,10,12,13}. The right-terminal weights are {6,11}; the corresponding left-terminal groups fill the remaining {1,2,3,4,5,7,8}. These are disjoint and give every value in [1,13] once. Both unused inventories are empty, so this is an ordinary graceful labeling on precisely the prescribed original.

## Bipartition and the single negative signed edge

Traversing from `s:0`, the vertices at even distance are `s:0`, `b:1:0` and the seven left terminals. Their labels are L={0,1,2,3,4,5,6,8,11}. The odd-distance vertices are `s:1`, both left centers and the two right terminals. Their labels are H={7,9,10,12,13}. A separation with L below H would require 11<7. A separation with H below L would require 13<0. Both fail.

Orient each edge from the even-distance class to the odd-distance class. The table computes its signed difference as the head label minus the tail label. The only negative value is −1 at the actual edge `l:0:0:3--b:0:0`, running from label 11 to 10. The signed degree sum agrees independently. The odd-distance sum is 2·13+5·10+4·9+7+12=131. The even-distance sum is 3·0+3·1+2+3+8+11+4+5+6=42. Their difference is 89. The absolute differences sum to 91, and replacing the single absolute weight 1 by −1 decreases the sum by 2, giving 91−2·1=89.

[D104](R241_43_2_LEFT_TERMINAL_ZERO.md) excludes both alpha orientations on the same frozen original. The explicit certificate establishes ordinary gracefulness with physical labels (0,13) and has no separating cut. The single negative signed edge is a property of this certificate. General composition and additional profiles are outside this result. [Evidence](../evidence/validation/LCL_ORDINARY_43_2_EXTREME_SPINE_001/README.md).
