# D229 — Fixed named controls

## Independent original declarations

Both V controls use the same h=10 original T, specified before assigning labels:

`[[3],[3,1],[3,3,3,3,3,3,1,1,1,1,1,1,1,1,1],[1]]`

It has (ℓ,j)=(2,15), 35 terminals, 57 edges and 58 vertices. The spine connects `s:0,s:1,s:2,s:3` consecutively. The indexed center `b:i:a` of entry a in section i meets `s:i`. Its indexed terminals `l:i:a:e` attach only to it, one for each index from zero through quota minus one. Both folds S use the same names. Replace only `s:0--b:0:0` and `s:3--b:3:0` by `s:1--b:0:0` and `s:2--b:3:0`. The complete pairs 1,9 are left and pairs 2,…,8 are right. The flanks take L₁,L₁₀ and the left interiors receive (H₁,L₉). The right list in actual branch index order is (L₂,L₃,L₄,H₂,H₃,H₄,L₅,L₆,L₇,L₈,L₁₂,H₅,H₆,H₇,H₈). These roles satisfy the fixed input quotas. The two h=6 unit sources and matched 43-edge X original and fold retain their independently specified names, profiles and role assignments. [D228 named controls](../D228_FINITE_STATE_BINARY_MULTIPLICITY_GROWTH/HAND_CONTROLS.md)

## Exact returning packets

For size F before the step, an upper coordinate below is an offset from F. Each two-letter tag specifies the input block then the weight block. The U packet at S1 is the D225 packet verified in D228 Control A, with residual lower inputs {0,2,3,5}, upper inputs [3,6], no lower weights and upper weights [−1,6]. Its four highs use (3,3),(0,5),(5,−1),(2,1) on LU in offset order H₁,…,H₄, and its upper lows are (4,6),(3,4),(6,2),(5,0) at L₁,L₂,L₇,L₈. The returns are (1,0) at L₄ and (F+7,F+7) at L₃.

At U from S2, before removing the two returns the lower input set is [0,3]∪{6}, the lower weight set {1}, the upper inputs [3,7] and upper weights [−1,7]. Remove L₄ (2,1) and L₃ (F+7,F+7). The remaining lower inputs {0,1,3,6} all use highs, and upper inputs [3,6] all use lows. The UU rows at L₁,L₂,L₇,L₈ are (3,5),(5,6),(6,2),(4,−1), where the differences are +2,+1,−4,−5. The LU rows at H₁,H₂,H₃,H₄ are (6,0),(1,4),(3,1),(0,3), with sums 6,5,4,3. The upper weights from the two lists partition [−1,6]. All eight residual host demands are one. Both anchors have the exact return at S2.

For V, n=12. The returns at L₄ and L₃ are (β,β−1) and (F+23,F+23). The following are all residual rows after those returns.

| Host | Tag | S1 rows | S2 rows |
|---|---|---|---|
| L₁ | LL | (0,2) | (0,2) |
| L₂ | LL | (2,3) | (3,4) |
| L₃ | LL | (4,4) | (5,5) |
| L₄ | LL | (6,5) | (7,6) |
| L₁ | UU | (19,21),(20,22) | (18,20),(16,18) |
| L₂ | UU | (13,14),(17,18) | (20,21),(21,22) |
| L₃ | UU | (15,15) | (12,12) |
| L₄ | UU | (21,20) | (15,14) |
| L₇ | UU | (11,7) | (11,7) |
| L₈ | UU | (22,17) | (22,17) |
| H₁ | LU | (3,19),(10,12) | (14,8),(11,11) |
| H₂ | LU | (5,16),(13,8) | (6,15),(8,13) |
| H₃ | LU | (7,13),(11,9) | (1,19),(4,16) |
| H₄ | LU | (8,11),(9,10) | (9,10),(10,9) |
| H₁ | UL | (16,6) | (13,9) |
| H₂ | UL | (14,7) | (14,7) |
| H₃ | UL | (12,8) | (17,3) |
| H₄ | UL | (18,1) | (19,0) |

In both columns subtraction at each low is 3−k. Adding each of the three rows per high gives 22 at H₁, 21 at H₂, 20 at H₃ and 19 at H₄. Each column has three rows at every new role after returning the two anchors, and one replacement each at L₇ and L₈. The S1 lower input rows partition ([0,11] except 1)∪{13}, and the lower weights [1,8]. S2 partitions ([0,11] except 2)∪{14} and ([0,7] except 1)∪{9}. The UU and UL inputs partition [11,22] in each column, and UU and LU weights partition [7,22]. Thus all tagged alphabets and host counts agree with the full independent vacancies. The U/V closures work from any supplied allocation at the declared state.

## Complete named 57-edge certificates

Start each column from its corresponding h=6 source, F=11, and the V packet above. Move ordinary rows by (i+12,w+8) and roles by +4. Use z=i+13 and actual weight d=w+10 at the final h=10. The spine (48,0,57,11) gives (48,57,46). Both columns use the same center labels and actual edges. Terminal tuples are in increasing index order, with fresh labels sorted per host in this fixed original.

| Actual name | Role | Center | S1 terminal labels | S1 differences | S2 terminal labels | S2 differences |
|---|---|---:|---|---|---|---|
| b:0:0 | L₁ | 1 | 13,43,44 | 12,42,43 | 13,40,42 | 12,39,41 |
| b:1:0 | H₁ | 56 | 16,23,40 | 40,33,16 | 24,27,37 | 32,29,19 |
| b:1:1 | L₉ | 9 | 33 | 24 | 33 | 24 |
| b:2:0 | L₂ | 2 | 15,37,41 | 13,35,39 | 16,44,45 | 14,42,43 |
| b:2:1 | L₃ | 3 | 17,39,47 | 14,36,44 | 18,36,47 | 15,33,44 |
| b:2:2 | L₄ | 4 | 14,19,45 | 10,15,41 | 15,20,39 | 11,16,35 |
| b:2:3 | H₂ | 55 | 18,26,38 | 37,29,17 | 19,21,38 | 36,34,17 |
| b:2:4 | H₃ | 54 | 20,24,36 | 34,30,18 | 14,17,41 | 40,37,13 |
| b:2:5 | H₄ | 53 | 21,22,42 | 32,31,11 | 22,23,43 | 31,30,10 |
| b:2:6 | L₅ | 5 | 30 | 25 | 30 | 25 |
| b:2:7 | L₆ | 6 | 32 | 26 | 32 | 26 |
| b:2:8 | L₇ | 7 | 35 | 28 | 35 | 28 |
| b:2:9 | L₈ | 8 | 46 | 38 | 46 | 38 |
| b:2:10 | L₁₂ | 12 | 34 | 22 | 34 | 22 |
| b:2:11 | H₅ | 52 | 25 | 27 | 25 | 27 |
| b:2:12 | H₆ | 51 | 31 | 20 | 31 | 20 |
| b:2:13 | H₇ | 50 | 27 | 23 | 29 | 21 |
| b:2:14 | H₈ | 49 | 28 | 21 | 26 | 23 |
| b:3:0 | L₁₀ | 10 | 29 | 19 | 28 | 18 |

The terminal label and absolute difference columns in both certificates exhaust [13,47] and [10,44]. The displayed center and spine labels are the exact complement of the terminal labels in [0,57]. Folded attachments in table order have weights (1,56,9,55,54,53,2,3,4,52,51,50,49,45,5,6,7,8,47). Together with the spine they give [1,9]∪[45,57]. The literal outside edges of T have |48−1|=47 and |11−10|=1, so their exchange preserves the full spectrum. Both physical reversals use the same terminal tuples at the corresponding index-preserving reversed names and spine (11,57,0,48). These are complete named original and folded certificates.

## Matched cap control

Use the unchanged h=10, 43-edge original `[[3],[1,1],[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],[1]]` and fold from D228 Control C. Both flanks and all actual index assignments are exactly those in that hand record. With source S2 take the eight new demand rows and the two replacements from D228 C, appending the old return anchors as ordinary cap rows. The same full named labeling works, with terminal inventories [13,33] and [10,30], and literal exchange 1↔33. From S1 this cap is excluded by the independent lower-input sum calculation in the D229 proof, without assuming returned anchors. The two states therefore differ on the same exact terminal cap. [Cap proof](../../../research/HOMOGENEOUS_PAIR_FINITE_KERNEL_SUPPLY.md#2-homogeneous-self-transitions-and-terminal-caps) · [43-edge certificate](../D228_FINITE_STATE_BINARY_MULTIPLICITY_GROWTH/HAND_CONTROLS.md#4-complete-h10-positives-for-a-and-c)
