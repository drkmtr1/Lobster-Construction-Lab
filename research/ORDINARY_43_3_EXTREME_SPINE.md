# D106 — Ordinary right-terminal extension from quota two to three

Begin with the exact signed ordinary [D105 certificate](../evidence/validation/LCL_ORDINARY_43_2_EXTREME_SPINE_001/result.json) on the frozen [D099 original](../evidence/validation/LCL_R241_43_2_LOWER_BLOCK_001/original.json). The source graph digest is `2060a4e5a7d8f8ebc1906499facea2730250938d4550bb4c6ca34582a1f5b6e6`, and the source ledger ID is `af0e2be70013710c5b5b64c6c554512adfaad5ae0faa8ab63c146e428ed50a93`.

## Original graph and direct labeling

The exact target profile is ordered `[[4,3],[3]]`. Each profile has the original spine `s:0--s:1`, both left-center attachments to `s:0`, the right-center attachment to `s:1`, and each terminal attached solely to the center determined by its indices. The two left terminal ranges and the two existing right terminals are unchanged. Expanding the target independently adds precisely `l:1:0:2` and its single edge to `b:1:0`. The new terminal has distance two from the existing spine. The target has 15 named vertices and 14 edges, every edge with multiplicity one. The [target original](../evidence/validation/LCL_ORDINARY_43_3_EXTREME_SPINE_001/original.json) and [audit](../evidence/validation/LCL_ORDINARY_43_3_EXTREME_SPINE_001/result.json) bind the exact names and role-preserving delta.

Copy D105's labels, change only the old exit `s:1` from 13 to 14, and give the new terminal 13. This is a finite copy and two fixed assignments.

| Named vertex or group | Target label or ordered labels |
| --- | --- |
| s:0, s:1 | 0,14 |
| b:0:0, b:0:1, b:1:0 | 10,9,1 |
| l:0:0:0 through l:0:0:3 | 2,3,8,11 |
| l:0:1:0 through l:0:1:2 | 4,5,6 |
| l:1:0:0 through l:1:0:2 | 7,12,13 |

The unchanged vertices carry each label in [0,12] once. The new terminal and exit add 13 and 14 at distinct actual vertices. The physical endpoints keep labels (0,14) in the target.

## Exact difference partition

In both graphs the neighbors of `s:1` are exactly `s:0` and `b:1:0`. Thus raising the exit changes just two old differences. The spine weight changes from 13−0=13 to 14−0=14. The right attachment changes from 13−1=12 to 14−1=13. The new right terminal contributes 13−1=12. The other eleven original differences remain [1,11], since D105 was graceful and the edges changed had weights 12 and 13. The retained and replacement difference groups are disjoint and exhaust [1,14]. Both unused inventories are empty.

| Original edge in target order | Signed difference | Absolute difference |
| --- | ---: | ---: |
| s:0--s:1 | 14 | 14 |
| s:0--b:0:0 | 10 | 10 |
| b:0:0--l:0:0:0 | 8 | 8 |
| b:0:0--l:0:0:1 | 7 | 7 |
| b:0:0--l:0:0:2 | 2 | 2 |
| b:0:0--l:0:0:3 | −1 | 1 |
| s:0--b:0:1 | 9 | 9 |
| b:0:1--l:0:1:0 | 5 | 5 |
| b:0:1--l:0:1:1 | 4 | 4 |
| b:0:1--l:0:1:2 | 3 | 3 |
| s:1--b:1:0 | 13 | 13 |
| b:1:0--l:1:0:0 | 6 | 6 |
| b:1:0--l:1:0:1 | 11 | 11 |
| b:1:0--l:1:0:2 | 12 | 12 |

## Physical signed interface and alpha scope

Traversal from `s:0` gives an even class containing `s:0`, the right center and all left terminals. Its labels are {0,1,2,3,4,5,6,8,11}. The odd class contains the two left centers, the exit and the three right terminals, with labels {7,9,10,12,13,14}. Direct every edge from even to odd and take the head label minus the tail label. The changed spine and right attachment stay positive and the new terminal has positive signed difference 12. The unchanged edge `l:0:0:3 → b:0:0` gives 10−11=−1 and is the sole negative edge.

The odd weighted degree sum is 2·14+5·10+4·9+7+12+13=146. The even weighted degree sum is 3·0+4·1+2+3+8+11+4+5+6=43. Their difference is 103, also obtained from 1+⋯+14−2·1=105−2. These sums refer to the exact original incidences.

The even maximum 11 exceeds the odd minimum 7, and the odd maximum 14 exceeds the even minimum 0. This certificate has no alpha separation. [D098](R241_NAMED_CENTER_ROLE_TRANSPORT.md) separately supplies an alpha labeling of this target topology in its covered domain, with q=4, a=3 and r=3 satisfying q>r≥a. [D104](R241_43_2_LEFT_TERMINAL_ZERO.md) remains a result on the two-right-terminal source. D106 establishes the exact extension from `[[4,3],[2]]` to `[[4,3],[3]]`. The signed interface refers to this certificate and this transition.
