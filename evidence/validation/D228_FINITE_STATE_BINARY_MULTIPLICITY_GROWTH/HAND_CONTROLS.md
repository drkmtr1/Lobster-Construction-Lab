# D228 — Named hand controls

## Fixed originals and named roles

The four profiles below specify their own original T before any labels are assigned. Connect the actual spine vertices `s:0,s:1,s:2,s:3` in order. An entry of quota Q at indexed position a of section i is the branch `b:i:a` adjacent to `s:i`, with precisely the Q terminals `l:i:a:e` for e=0,…,Q−1 adjacent only to `b:i:a`. S has the same names and changes only the exterior attachment edges `s:0--b:0:0` and `s:3--b:3:0` to `s:1--b:0:0` and `s:2--b:3:0`. The name-to-role assignments are declared independently below. Terminal tuples are in index order.

| Original | Profile | Edges |
|---|---|---:|
| Former D227 comparison | `[[3],[3,3],[1,1,1,1,1,1,1],[3]]` | 33 |
| Unit source used by A and C | `[[1],[1,1],[1,1,1,1,1,1,1],[1]]` | 25 |
| Unit target of A | `[[1],[1,1],[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],[1]]` | 41 |
| Common target of B and C | `[[3],[1,1],[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],[1]]` | 43 |

For h=6 use (ℓ,j)=(2,7), left pairs 1,5 and right pairs 2,3,4. At the two flanks take L₁ and L₆. The indexed left interiors take (H₁,L₅) and the indexed right interiors (L₂,L₃,L₄,L₈,H₄,H₃,H₂). These are D227's roles. For h=10 use (2,15), left pairs 1,9 and right pairs 2,…,8. The flanks are L₁,L₁₀ and the indexed left interiors (H₁,L₉). In right interior index order take (L₂,L₃,L₄,L₅,L₆,L₇,L₈,L₁₂,H₂,H₃,H₄,H₅,H₆,H₇,H₈). The marks are D226's for each h and m. All named edge transports under physical reversal send section i to 3−i, with unchanged branch and terminal indices. Auxiliary row transport uses numerical offsets, then these independently declared final names.

## 1. Former D227 comparison, 33 edges

The input 31-edge source is D227's recorded independent F=17 certificate. It has the same skeleton and roles, with only the left flank at quota one instead of three. Translate each normalized row by (1,1) at F′=19. Each low displacement persists and each high sum increases by 2. The four changed translated rows are H₄ (12,2)→(14,0), L₅ (14,12)→(12,10), L₈ (15,10)→(18,13) and L₆ (16,13)→(15,12). The changed high sum is 14=18−4. The changed low shifts are respectively −2,−5,−3. At L₁ add (0,2) and (16,18). The four replacements change the interior input set {12,14,15,16} to {12,14,15,18}, and the weight set {2,10,12,13} to {0,10,12,13}. Thus the two new L₁ rows complete [0,18] in both coordinates. Every changed row remains at the same named terminal index and actual host.

The spine (28,0,33,7) has differences (28,33,26). With z=9+i, actual endpoint subtraction gives the following indexed tuples.

| Actual center | Center label | Terminal labels | Actual terminal differences |
|---|---:|---|---|
| b:0:0 | 1 | 16,9,25 | 15,8,24 |
| b:1:0 | 32 | 10,11,12 | 22,21,20 |
| b:1:1 | 5 | 14,22,21 | 9,17,16 |
| b:2:0 | 2 | 15 | 13 |
| b:2:1 | 3 | 26 | 23 |
| b:2:2 | 4 | 18 | 14 |
| b:2:3 | 8 | 27 | 19 |
| b:2:4 | 29 | 23 | 6 |
| b:2:5 | 30 | 20 | 10 |
| b:2:6 | 31 | 19 | 12 |
| b:3:0 | 6 | 17,13,24 | 11,7,18 |

The terminal labels cover [9,27] and their differences [6,24], each exactly once. The folded attachment weights in the displayed order are (1,32,5,31,30,29,25,4,3,2,27). Together with the spine weights they give [1,5]∪[25,33]. The labels of the spine and centers complement the displayed terminal range in [0,33]. Restoration changes the two actual exterior differences to |28−1|=27 and |7−6|=1, so the full original and fold both have spectrum [1,33]. Reversal has spine (7,33,0,28) and carries these same weights. The D227 centered exclusion remains: G=4 forces both L₆ rows onto (3,0), blocking both legal L₅ rows (2,0) and (3,1) in the projection. The former proposed comparison is now symbolically resolved before any preparation or execution. [D227's 31-edge source](../D227_INDEPENDENT_CAPACITY_FREE_PAIRED_PACKET_SUPPLY/HAND_CONTROLS.md#5-direct-31-edge-positive-with-a-bank-already-present) · [D227 centered obstruction](../D227_INDEPENDENT_CAPACITY_FREE_PAIRED_PACKET_SUPPLY/HAND_CONTROLS.md#6-one-proposed-matched-discriminator-for-separate-authorization)

## 2. The independent 25-edge source in the two states

At F=11, h=6 and m=25, the actual spine is (20,0,25,7). The normalized source rows below give full named certificates via terminal label z=i+9 and difference d=w+6. The center labels give these same differences by direct subtraction. The source of A is the retained D225 seed. The source of C is the Director's separate supplied state.

| Role | Center label | A source (0,1) | C source (0,2) |
|---|---:|---|---|
| L₁ | 1 | (5,7) | (5,7) |
| H₁ | 24 | (0,9) | (0,9) |
| L₅ | 5 | (8,6) | (8,6) |
| L₂ | 2 | (7,8) | (7,8) |
| L₃ | 3 | (10,10) | (10,10) |
| L₄ | 4 | (1,0) | (2,1) |
| L₈ | 8 | (9,4) | (9,4) |
| H₄ | 21 | (3,3) | (1,5) |
| H₃ | 22 | (2,5) | (4,3) |
| H₂ | 23 | (6,2) | (6,2) |
| L₆ | 6 | (4,1) | (3,0) |

Each column uses [0,10] exactly once in both coordinates. At each low row subtract its input from its weight to obtain 3−k. At each high row the sum is 10−k: in order H₁ through H₄ the sums are (9,8,7,6) in each state. Low 3 carries the maximum identity in both states and low 4 has its stated anchor. The folded weights at branches are (1,24,5,23,22,21,17,4,3,2,19), and the spine gives (20,25,18). The terminal labels [9,19] and weights [6,16] complement the corresponding skeleton sets. Outward attachments exchange weights 1 and 19 using the literal endpoints, completing both spectra.

## 3. Packets for Controls A, B and C

**A.** All eight new quotas are one and n=4. From and to (0,1), after the anchors the lower inputs are {0,2,3,5} and no lower weights remain. The upper offset input and weight sets are {3,4,5,6} and [−1,6]. The fresh highs at H₁,H₂,H₃,H₄ use (3,F+3),(0,F+5),(5,F−1),(2,F+1). Their local sums are 6,5,4,3, exactly 7−k. The upper lows at L₁,L₂,L₇,L₈ use offsets (4,6),(3,4),(6,2),(5,0), at shifts +2,+1,−4,−5. The upper outputs in the high and low lists partition [−1,6]. Reinsert L₄ (1,0), L₃ (F+7,F+7). With (i,w)→(i+4,w) on every other old row this is the exact D225 unit packet and the h=10 result below.

**B.** For X and n=5, source and return (0,1), the lower inputs are {0,2,3,4,6} and lower weight 1. Upper input offsets [4,8] and weight offsets [0,8] give 5 and 9 slots. Highs must all travel lower-to-upper by the side counts in the proof. Of the six low rows only L₂ at 0 or L₈ at 6 can use lower weight 1. If L₂ uses it, the high input sum 15 requires weight sum 26−15=11. The upper lows must consume all five upper inputs with shifts summing to −3, leaving weight sum 9 for highs. If L₈ uses the lower weight, L₁ must take upper offsets 4,5,6, using weights 6,7,8. The remaining upper offsets 7 and 8 force L₂ to an already used weight 8 or unavailable 9. This rules out the stated self-transition. Section 4 of the proof extends the argument to both α values and both proposed returns from β=1.

**C.** For X from (0,2) to (0,1), the remaining lower inputs {0,2,3,4,7} and lower weight {2} follow by subtracting (1,0). Upper input offsets are [4,8] and upper weight offsets [0,8]. Use lower L₁ (0,2), upper L₁ offsets (4,6),(5,7), and upper L₂,L₇,L₈ offsets (7,8),(6,2),(8,3). Use the following highs.

| Host | Lower input | Upper weight offset | Sum |
|---|---:|---:|---:|
| H₁ | 3 | 5 | 8 |
| H₂ | 7 | 0 | 7 |
| H₃ | 2 | 4 | 6 |
| H₄ | 4 | 1 | 5 |

These are exactly 9−k. The five upper low weights are 6,7,8,2,3, complementing the four high offsets in [0,8]. The low shifts are the required +2,+2,+2,+1,−4,−5. The ordinary transport is (i+5,w+1) and the returned rows are L₄ (1,0) and L₃ (F+9,F+9). Thus every input, weight and host demand holds separately.

## 4. Complete h=10 positives for A and C

Now z=i+13 and d=w+10. Apply the packets to the distinct sources in Section 2 and assign the final numerical roles to their fixed named vertices. For A the final F′=19, m′=41. The spine (32,0,41,11) gives weights (32,41,30). For C the final F′=21, m′=43. The spine (34,0,43,11) gives weights (34,43,32). Every listed difference is an actual absolute subtraction from its center label.

| Actual center | Role | A center | A terminals | A differences | C center | C terminals | C differences |
|---|---|---:|---|---|---:|---|---|
| b:0:0 | L₁ | 1 | 28 | 27 | 1 | 13,28,29 | 12,27,28 |
| b:1:0 | H₁ | 40 | 16 | 24 | 42 | 16 | 26 |
| b:1:1 | L₉ | 9 | 25 | 16 | 9 | 26 | 17 |
| b:2:0 | L₂ | 2 | 27 | 25 | 2 | 31 | 29 |
| b:2:1 | L₃ | 3 | 31 | 28 | 3 | 33 | 30 |
| b:2:2 | L₄ | 4 | 14 | 10 | 4 | 14 | 10 |
| b:2:3 | L₅ | 5 | 22 | 17 | 5 | 23 | 18 |
| b:2:4 | L₆ | 6 | 24 | 18 | 6 | 25 | 19 |
| b:2:5 | L₇ | 7 | 30 | 23 | 7 | 30 | 23 |
| b:2:6 | L₈ | 8 | 29 | 21 | 8 | 32 | 24 |
| b:2:7 | L₁₂ | 12 | 26 | 14 | 12 | 27 | 15 |
| b:2:8 | H₂ | 39 | 13 | 26 | 41 | 20 | 21 |
| b:2:9 | H₃ | 38 | 18 | 20 | 40 | 15 | 25 |
| b:2:10 | H₄ | 37 | 15 | 22 | 39 | 17 | 22 |
| b:2:11 | H₅ | 36 | 17 | 19 | 38 | 18 | 20 |
| b:2:12 | H₆ | 35 | 23 | 12 | 37 | 24 | 13 |
| b:2:13 | H₇ | 34 | 19 | 15 | 36 | 22 | 14 |
| b:2:14 | H₈ | 33 | 20 | 13 | 35 | 19 | 16 |
| b:3:0 | L₁₀ | 10 | 21 | 11 | 10 | 21 | 11 |

The A terminal columns exhaust [13,31] and [10,28]. Its folded center attachment weights in table order are (1,40,9,39,38,37,36,35,34,33,29,2,3,4,5,6,7,8,31). Alongside the spine these give [1,9]∪[29,41]. Restore the two outward attachments to give |32−1|=31 and |11−10|=1. The C terminal columns exhaust [13,33] and [10,30]. Its folded center attachment weights are (1,42,9,41,40,39,38,37,36,35,31,2,3,4,5,6,7,8,33). With the spine these give [1,9]∪[31,43]. Restore to |34−1|=33 and |11−10|=1. These two literal exchanges preserve their exact spectra and every other edge. In each case the spine and center labels are precisely the complement of the terminal interval in [0,m′]. Physical reversal uses the displayed table on the reversed names with spines (11,41,0,32) and (11,43,0,34); the endpoint weights and all quotas are transported in original terminal order. This gives full positive controls for the transition architecture.
