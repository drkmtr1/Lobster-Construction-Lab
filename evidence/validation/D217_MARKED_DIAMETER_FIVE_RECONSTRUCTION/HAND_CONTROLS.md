# D217 named hand controls

The physical spine in every row is `s:0--s:1--s:2--s:3`. The j-th entry of section i is the named branch vertex `b:i:j`. Its terminal tuple lists labels at `l:i:j:0,l:i:j:1,…` in original index order. The folded source changes only the two exterior branch attachment edges stated in the manuscript. In a zero-quota group the listed branch vertex is a direct leaf with its own attachment edge.

## 1. Five-edge joint-exchange positive

On `[[0],[],[],[0]]` give the spine labels (4,0,5,3), and give the exterior branch vertices `b:0:0,b:3:0` labels (1,2). These are all labels [0,5]. There are no other vertices or edges. The source spine weights are (4,5,2), the inward exterior attachment weights are (1,3), and the original outward attachment weights are (3,1).

| Affected original branch | Actual folded endpoints by name | Folded weight | Actual original endpoints by name | Original weight |
|---|---|---:|---|---:|
| `b:0:0` | `s:1--b:0:0` = (0,1) | 1 | `s:0--b:0:0` = (4,1) | 3 |
| `b:3:0` | `s:2--b:3:0` = (5,2) | 3 | `s:3--b:3:0` = (3,2) | 1 |

Both use [1,5]. The left midpoint test would require label 2 at `s:0` and the right would require −1 at `s:3`. The actual original path reads (1,4,0,5,3,2) in order, with differences (3,4,5,2,1).

## 2. Adverse fold of the retained D216 original

On `[[1],[2,2,2],[2,2,3],[1]]`, the retained certificate has spine labels (23,3,26,0), exterior branch labels (2,25) and their terminal labels (24,1). The original attachment weights are |23−2|=21 and |0−25|=25. The fold gives |3−2|=1 and |26−25|=1. The unchanged difference 1 at `b:2:2--l:2:2:1` comes from labels 14 and 13. Thus under this fixed assignment the folded spectrum repeats 1 and loses 21 and 25. The D216 original remains graceful under that assignment. [Retained D216 full certificate](../D216_JOINT_POOLED_CLUSTER_REFLECTION/HAND_CONTROLS.md#2-symbolic-supplier-for-the-selected-26-edge-mixed-quota-original)

## 3. Selected 26-edge marked source and reconstructed original

Original T is `[[1],[1,2,3],[1,2,4],[1]]`. Folded source S has all the same 27 named vertices. In S the actual `b:0:0` parent is `s:1`, and the actual `b:3:0` parent is `s:2`. All other original incidences are shared. The spine labels in both graphs are (25,0,26,3) in original order. The actual spine weights are (25,26,23).

| Named branch | Center | Indexed terminal labels | Terminal differences | Parent in S and its weight | Parent in T and its weight |
|---|---:|---|---|---|---|
| `b:0:0` | 1 | (13) | (12) | `s:1`, 1 | `s:0`, 24 |
| `b:1:0` | 11 | (14) | (3) | `s:1`, 11 | `s:1`, 11 |
| `b:1:1` | 19 | (23,10) | (4,9) | `s:1`, 19 | `s:1`, 19 |
| `b:1:2` | 16 | (18,8,9) | (2,8,7) | `s:1`, 16 | `s:1`, 16 |
| `b:2:0` | 4 | (17) | (13) | `s:2`, 22 | `s:2`, 22 |
| `b:2:1` | 5 | (22,15) | (17,10) | `s:2`, 21 | `s:2`, 21 |
| `b:2:2` | 6 | (24,21,20,12) | (18,15,14,6) | `s:2`, 20 | `s:2`, 20 |
| `b:3:0` | 2 | (7) | (5) | `s:2`, 24 | `s:3`, 1 |

The six marked labels are {0,1,2,3,25,26}, the remaining six center labels are {4,5,6,11,16,19}, and the fifteen terminal labels are {7,8,9,10,12,13,14,15,17,18,20,21,22,23,24}. These disjoint sets fill [0,26]. The table gives the actual changed attachments and every unchanged named edge together with the spine. Below, all endpoints are sorted numerically within their edge. The columns for cuts use the predicate low < cut ≤ high in both graphs. Differences have multiplicity one.

| Weight | S endpoint labels | T endpoint labels if changed | Crosses 11 in both | Crosses 25 in both |
|---:|---|---|---|---|
| 1 | (0,1) | (2,3) | no | no |
| 2 | (16,18) | — | no | no |
| 3 | (11,14) | — | no | no |
| 4 | (19,23) | — | no | no |
| 5 | (2,7) | — | no | no |
| 6 | (6,12) | — | yes | no |
| 7 | (9,16) | — | yes | no |
| 8 | (8,16) | — | yes | no |
| 9 | (10,19) | — | yes | no |
| 10 | (5,15) | — | yes | no |
| 11 | (0,11) | — | yes | no |
| 12 | (1,13) | — | yes | no |
| 13 | (4,17) | — | yes | no |
| 14 | (6,20) | — | yes | no |
| 15 | (6,21) | — | yes | no |
| 16 | (0,16) | — | yes | no |
| 17 | (5,22) | — | yes | no |
| 18 | (6,24) | — | yes | no |
| 19 | (0,19) | — | yes | no |
| 20 | (6,26) | — | yes | yes |
| 21 | (5,26) | — | yes | yes |
| 22 | (4,26) | — | yes | yes |
| 23 | (3,26) | — | yes | yes |
| 24 | (2,26) | (1,25) | yes | yes |
| 25 | (0,25) | — | yes | yes |
| 26 | (0,26) | — | yes | yes |

This verifies [1,26] on each exact graph and the common safe spectra [6,26] and [20,26]. The restoration exchanges only weights 1 and 24, without moving either interior branch group or its terminal indices. The marks have extreme roots by this choice of constructive supply, while the theorem in Section 2 and the scientific question allow any ordinary graceful folded source. The fixed certificate and its parametric safe-gap transport were developed by hand. Diagnostic, solver and protected-checker counts are zero.

[Primary manuscript](../../../research/MARKED_DIAMETER_FIVE_EXTERIOR_RECONSTRUCTION.md)
