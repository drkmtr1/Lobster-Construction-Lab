# D215 exact named hand controls

These are the six prescribed originals, with a fixed four-vertex spine and every indexed parent incidence. The entry in section i at index j is the actual vertex `b:i:j`. Its terminal tuple lists labels at `l:i:j:0,l:i:j:1,…` in order, with () for a direct leaf. A central dash for the empty section means there are no central branch vertices. The four labels in a spine tuple are at `s:0,s:1,s:2,s:3`, and the three spine weights are in consecutive edge order.

| Control | Exact profile | n | k | A | N=n+k |
|---:|---|---:|---:|---:|---:|
| 1 | `[[1],[1,1,1],[1],[1]]` | 6 | 9 | 4 | 15 |
| 2 | `[[2],[1,2,1],[3],[4]]` | 7 | 15 | 7 | 22 |
| 3 | `[[0],[1,0,2],[2],[0]]` | 6 | 8 | 3 | 14 |
| 4 | `[[0],[],[0],[0]]` | 0 | 6 | 3 | 6 |
| 5 | `[[3],[2,0,0],[0],[2]]` | 5 | 11 | 5 | 16 |
| 6 | `[[1],[1,1],[1],[1]]` | 4 | 9 | 4 | 13 |

## Independent isolated cluster certificates

All six use f(`s:1`)=0. Each row specifies every listed `b:1:j` and its terminals independently of H. Attachments from the root have the displayed branch labels as weights. Subtracting the terminal labels from their named parent labels in absolute value gives the last column.

| Control | Branch labels by j | Terminal tuples by j | Terminal weights by j |
|---:|---|---|---|
| 1 | (6,2,4) | (1), (5), (3) | (5), (3), (1) |
| 2 | (1,6,7) | (5), (3,4), (2) | (4), (3,2), (5) |
| 3 | (4,2,6) | (5), (), (1,3) | (1), (), (5,3) |
| 4 | — | — | — |
| 5 | (3,4,5) | (1,2), (), () | (2,1), (), () |
| 6 | (4,2) | (1), (3) | (3), (1) |

In control 1 the root weights are {2,4,6} and the terminal weights {1,3,5}. Control 2 uses the retained independent seven-edge D214 cluster with root weights {1,6,7} and terminal weights {2,3,4,5}. Control 3 has root weights {2,4,6} including its actual direct leaf `b:1:1`, and terminal weights {1,3,5}. Control 4 is the single vertex with empty weights. Control 5 has root weights {3,4,5} and terminal weights {1,2}. In control 6 the literal four differences are 4, 2 at the root and |4−1|=3, |2−3|=1 at the terminals. Each central row contains all labels [0,n] once and realizes [1,n] once. In particular the B2 root-zero labeling was established before using the shell.

## Complete named assignments

The exterior branch columns are in physical section order 0,2,3. All branch and terminal slots of section 1 are in actual index order. These rows give the entire F on the original with `s:1` appearing only in the spine column.

| Control | Spine labels | Exterior branch labels | Exterior terminal tuples | Central branch labels | Central terminal tuples |
|---:|---|---|---|---|---|
| 1 | (11,4,14,1) | (3,0,13) | (12), (15), (2) | (10,6,8) | (5), (9), (7) |
| 2 | (15,7,19,1) | (6,0,18) | (16,17), (20,21,22), (2,3,4,5) | (8,13,14) | (12), (10,11), (9) |
| 3 | (10,3,12,1) | (2,0,11) | (), (13,14), () | (7,5,9) | (8), (), (4,6) |
| 4 | (4,3,6,1) | (2,0,5) | (), (), () | — | — |
| 5 | (11,5,16,1) | (4,0,15) | (12,13,14), (), (2,3) | (8,9,10) | (6,7), (), () |
| 6 | (9,4,12,1) | (3,0,11) | (10), (13), (2) | (8,6) | (5), (7) |

By reading labels from the displayed names the fresh lower, central and fresh upper bands are respectively as follows. The shared root is the first label of the central band in each row.

| Control | Fresh lower | Central | Fresh upper | Physical cut |
|---:|---|---|---|---:|
| 1 | [0,3] | [4,10] | [11,15] | 11 |
| 2 | [0,6] | [7,14] | [15,22] | 15 |
| 3 | [0,2] | [3,9] | [10,14] | 10 |
| 4 | [0,2] | [3,3] | [4,6] | 4 |
| 5 | [0,4] | [5,10] | [11,16] | 11 |
| 6 | [0,3] | [4,8] | [9,13] | 9 |

## Actual edge differences

These are the absolute subtractions of the endpoints in the preceding rows. Branch attachments use their physical spine parents, and each terminal weight uses its own branch parent.

| Control | Spine weights | Exterior branch attachments | Exterior terminal weights | Central branch attachments | Central terminal weights |
|---:|---|---|---|---|---|
| 1 | (7,10,13) | (8,14,12) | (9), (15), (11) | (6,2,4) | (5), (3), (1) |
| 2 | (8,12,18) | (9,19,17) | (10,11), (20,21,22), (16,15,14,13) | (1,6,7) | (4), (3,2), (5) |
| 3 | (7,9,11) | (8,12,10) | (), (13,14), () | (4,2,6) | (1), (), (5,3) |
| 4 | (1,3,5) | (2,6,4) | (), (), () | — | — |
| 5 | (6,11,15) | (7,16,14) | (8,9,10), (), (13,12) | (3,4,5) | (2,1), (), () |
| 6 | (5,8,11) | (6,12,10) | (7), (13), (9) | (4,2) | (3), (1) |

The central columns give [1,n], with no crossing at the listed cut. The spine and exterior columns give [n+1,N], with all those edges crossing. In control 3 both flanks are direct leaves and the opposite interior branch has two terminals. In control 4 all three exterior branch attachments remain, although the central list and all exterior terminal lists are empty. In control 5 the opposite interior branch and the two listed central zeros are direct leaves with their own edges. Counts across the six hand tables are 86 original edge differences and 92 named vertex assignments. No diagnostic, solver, checker or executable enumeration was used.

Control 6 proves ordinary existence for B2. It makes no matched-gap claim at any center of B2. B2, B3 and B4 remain INCOMPLETE and undecided under their exact D212 all-center certificate questions.

[Primary manuscript](../../../research/INDEPENDENT_NONNEGATIVE_EXTERIOR_SHELL.md)
