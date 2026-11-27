# D209 fixed hand-arithmetic controls

Each original is specified by the profile in its heading. The four spine names are `s:0` through `s:3` in order; the three consecutive spine edges are retained. In section i, the j-th listed quota is at `b:i:j`, attached to `s:i`, and owns exactly the terminals `l:i:j:k` in increasing zero-based index order. No other edges occur. The tables use this fixed indexing, with each terminal tuple in its actual parent’s index order. The core is sections 1 and 2. The computations below are hand arithmetic; no search or executable verification was used.

## A. D105, equal unit flanks, [[1],[4,3],[2],[1]]

The core has 13 edges. Its ordered spine labels are (13,12), ordered center labels (1,0,2), and terminal tuples (3,4,5,6), (7,9,11), (8,10). The path is 10→8→6→5→4→3→2. Its spine difference is 1, its three center-attachment differences are (12,13,10), and its terminal differences are (2,3,4,5), (7,9,11), (6,8). These use exactly [0,13] and [1,13].

Attach the right quota-one section at deficit 1. The 16-edge state has its other original core port at 1; complement that state and attach left at deficit 1. The final core map is 15−f.

| Original section | Spine label | Centers | Terminals | Center-attachment differences | Terminal differences |
|---|---:|---|---|---|---|
| 0 | 19 | (0) | (18) | (19) | (18) |
| 1 | 2 | (14,15) | (12,11,10,9); (8,6,4) | (12,13) | (2,3,4,5); (7,9,11) |
| 2 | 3 | (13) | (7,5) | (10) | (6,8) |
| 3 | 17 | (1) | (16) | (16) | (15) |

The actual spine differences in original order are (17,1,14). Final label bands by birth are core [2,15], first right {1,16,17}, last left {0,18,19}. Thus the first two final label groups use [1,17], and the full alphabet is [0,19]. The difference bands by birth are [1,13], [14,16], [17,19].

## B. D117, independently varying unequal flanks, [[2],[6,5],[4],[3]]

The core has 19 edges. In the size-17 D117 seed with right quota two, the actual low and high left centers have labels 2 and 15, and the right center has label 1. The even alternating source assignment uses pairs (7,10), (8,9). After right growth to quota four, the core has spine labels (0,19), center labels (2,15,1), terminal tuples (3,7,8,9,10,16), (4,5,6,11,12), (13,14,17,18). Its spine difference is 19, center-attachment differences are (2,15,18), and terminal differences are (1,5,6,7,8,14), (11,10,9,4,3), (12,13,16,17). The alphabets are [0,19] and [1,19].

First use the complemented core and add the smaller left quota two from its actual maximum, at deficit 0. At size 23 the unused right port has deficit 3; add the original right quota three there. The final core map from the displayed labeling is 23−f.

| Original section | Spine label | Centers | Terminals | Center-attachment differences | Terminal differences |
|---|---:|---|---|---|---|
| 0 | 3 | (24) | (2,1) | (21) | (22,23) |
| 1 | 23 | (21,8) | (20,16,15,14,13,7); (19,18,17,12,11) | (2,15) | (1,5,6,7,8,14); (11,10,9,4,3) |
| 2 | 4 | (22) | (10,9,6,5) | (18) | (12,13,16,17) |
| 3 | 28 | (0) | (25,26,27) | (28) | (25,26,27) |

The actual spine differences are (20,19,24). Final label groups are core [4,23], left {1,2,3,24}, right {0}∪[25,28], composing [0,28]. Difference bands by birth are [1,19], [20,23], [24,28].

## C. Complementary descending paths, [[4],[6,4],[6],[4]]

Here z=4, u=6, b=6, c=4, n=20. The core spine is (20,16), and the centers are (1,0,2) in actual order. The decreasing paths are

- 19→17→16,
- 14→12→10→9→8→7→6→5→3→1,
- 4→2.

The sources assigned to label 1 are (6,7,8,9,10,17); the zero-center identities are (11,13,15,18); and the sources assigned to label 2 are (3,4,5,12,14,19). The four fixed differences are (4,19,20,14). The respective terminal differences (5,6,7,8,9,16), (11,13,15,18), (1,2,3,10,12,17) complete [1,20] and the vertex alphabet is [0,20].

Attach right at deficit 4 and size 26, complement the result, then attach left at deficit 1. The final core map is 22−f.

| Original section | Spine label | Centers | Terminals | Center-attachment differences | Terminal differences |
|---|---:|---|---|---|---|
| 0 | 29 | (0) | (28,30,31,32) | (29) | (28,30,31,32) |
| 1 | 2 | (21,22) | (16,15,14,13,12,5); (11,9,7,4) | (19,20) | (5,6,7,8,9,16); (11,13,15,18) |
| 2 | 6 | (20) | (19,18,17,10,8,3) | (14) | (1,2,3,10,12,17) |
| 3 | 27 | (1) | (23,24,25,26) | (26) | (22,23,24,25) |

The actual spine differences are (27,4,21). Final label groups are core [2,22], right {1}∪[23,27], left {0,28,29,30,31,32}, composing [0,32]. Difference bands by birth are [1,20], [21,26], [27,32].

## D. All-even adverse port control, [[1],[6,4],[2],[1]]

The core has n=16 edges and the full original has 22. The actual core spine degrees are 3 and 2; the center degrees are 7,5,3; the terminals have degree 1. If the actual right port had label 15, the sum of the actual edge differences would be odd, since the sum of labels is 136 and the even-degree port is the unique omitted label modulo 2. The required difference sum 136 is even. For the reverse pins, the 16-labeled right port forces its actual center to have label 0. Neither the pair {0,15} nor {1,16} is then an actual edge, eliminating difference 15. Global complement gives the analogous two exclusions at the adjacent bottom.

For this concrete original the unit-flank two-step D131 and translated-core necessary conditions therefore fail. This is an adverse control for those interfaces. Ordinary gracefulness of this target is unresolved by the present construction.
