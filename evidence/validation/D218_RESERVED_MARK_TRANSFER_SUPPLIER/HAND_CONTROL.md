# D218 exact named hand control

The prescribed original is `[[1],[2,1],[1,2,1,1,1],[1]]`. It has ℓ=2, j=5, R=11, h=5, F=11 and m=23. The two spine-end leaves in the fold have labels 22 and 5. The roots have labels 0 and 23. The initial positive hosts are the other nine slots.

## Initial graceful inventory and terminal transfers

The root edge has weight 23. The low slots 1,…,6 attached to 23 give weights 17,…,22, and the high slots 18,…,22 attached to 23 give weights 1,…,5. With terminals 7,…,17 all at 1, their weights are 6,…,16. These partitions give labels [0,23] and weights [1,23] once each. The active host sequence is (1,21,2,20,3,19,4,18,6); neither spine-end leaf participates.

| Current host | Next host | Active interval before retention | Q | Δ | (λ,μ) | Retained labels | Moved interval |
|---:|---:|---|---:|---:|---|---|---|
| 1 | 21 | [7,17] | 2 | −2 | (0,2) | (16,17) | [7,15] |
| 21 | 2 | [7,15] | 1 | +1 | (1,0) | (7) | [8,15] |
| 2 | 20 | [8,15] | 1 | −1 | (0,1) | (15) | [8,14] |
| 20 | 3 | [8,14] | 1 | +1 | (1,0) | (8) | [9,14] |
| 3 | 19 | [9,14] | 1 | −1 | (0,1) | (14) | [9,13] |
| 19 | 4 | [9,13] | 1 | +1 | (1,0) | (9) | [10,13] |
| 4 | 18 | [10,13] | 1 | −1 | (0,1) | (13) | [10,12] |
| 18 | 6 | [10,12] | 2 | +2 | (2,0) | (10,11) | [12,12] |
| 6 | — | [12,12] | 1 | — | — | (12) | — |

The moved interval endpoint sums are 22,23,22,23,22,23,22,24, equal to the actual two host labels at each step. The retained tuples in increasing order give the original terminal indices at the final hosts. The left pairs (1,22) and (2,21) move to root 0. In that label order their root differences change (22,1)→(1,22) and (21,2)→(2,21). Every other slot stays at root 23. This places all original spine incidences and both interior groups at their folded positions.

## Separate actual spectra

Both S and T have spine labels (22,0,23,5) on `s:0,s:1,s:2,s:3`, so the actual spine weights are (22,23,18). In the table, a terminal tuple lists exactly `l:i:j:0,l:i:j:1,…` for its indexed branch `b:i:j`. All terminal edges are common. The columns for S and T give separate endpoint subtractions for the branch attachments.

| Named branch | Center | Indexed terminals | Terminal weights by subtraction | Actual folded parent, difference | Actual original parent, difference |
|---|---:|---|---|---|---|
| `b:0:0` | 2 | (15) | (15−2) = (13) | `s:1`, 2−0=2 | `s:0`, 22−2=20 |
| `b:1:0` | 1 | (16,17) | (16−1,17−1) = (15,16) | `s:1`, 1−0=1 | `s:1`, 1−0=1 |
| `b:1:1` | 21 | (7) | (21−7) = (14) | `s:1`, 21−0=21 | `s:1`, 21−0=21 |
| `b:2:0` | 20 | (8) | (20−8) = (12) | `s:2`, 23−20=3 | `s:2`, 23−20=3 |
| `b:2:1` | 18 | (10,11) | (18−10,18−11) = (8,7) | `s:2`, 23−18=5 | `s:2`, 23−18=5 |
| `b:2:2` | 19 | (9) | (19−9) = (10) | `s:2`, 23−19=4 | `s:2`, 23−19=4 |
| `b:2:3` | 4 | (13) | (13−4) = (9) | `s:2`, 23−4=19 | `s:2`, 23−4=19 |
| `b:2:4` | 6 | (12) | (12−6) = (6) | `s:2`, 23−6=17 | `s:2`, 23−6=17 |
| `b:3:0` | 3 | (14) | (14−3) = (11) | `s:2`, 23−3=20 | `s:3`, 5−3=2 |

The spine uses {0,5,22,23}, branch vertices {1,2,3,4,6,18,19,20,21} and terminals [7,17]. They exhaust [0,23] once. The complete named weight lists are:

- **S.** Spine (22,23,18). Branch attachments (2,1,21,3,5,4,19,17,20). Terminal edges (13,15,16,14,12,8,7,10,9,6,11).
- **T.** Spine (22,23,18). Branch attachments (20,1,21,3,5,4,19,17,2). Terminal edges (13,15,16,14,12,8,7,10,9,6,11).

In each list the spine and branch bands together are [1,5] and [17,23]. The terminal band is [6,16]. Each graph has 23 actual differences of multiplicity one, and its full alphabet is [1,23]. The actual restoration replaces `s:1--b:0:0` and `s:2--b:3:0` by `s:0--b:0:0` and `s:3--b:3:0`. Their differences exchange 2 and 20. No diagnostic, solver or protected checker ran.

[Primary mathematical manuscript](../../../research/INDEPENDENT_RESERVED_MARK_TRANSFER_SUPPLIER.md)
