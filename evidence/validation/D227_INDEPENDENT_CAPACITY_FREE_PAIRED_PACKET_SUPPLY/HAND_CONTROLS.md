# D227 — Named arithmetic and structural controls

## Original definitions and roles

Each profile listed below defines its own T before labels are assigned. The four named spine vertices `s:0,s:1,s:2,s:3` are linked consecutively. For entry a of section i the actual indexed center `b:i:a` attaches to `s:i` and has exactly the listed number of index-ordered terminals `l:i:a:e`, all attached to that same center. The graphs S on the same names change only `s:0--b:0:0` and `s:3--b:3:0` to `s:1--b:0:0` and `s:2--b:3:0`. Use the corresponding unit subgraphs by keeping terminal index zero at each center. These definitions depend solely on the profiles, never on labels.

For all h=6 controls use (ℓ,j)=(2,7), left pairs 1,5 and right pairs 2,3,4. The named role order is L₁ for the left flank, (H₁,L₅) for the even-side list, (L₂,L₃,L₄,L₈,H₄,H₃,H₂) for the odd-side list, and L₆ for the right flank. In the h=9 control use (2,13), pairs 1,8 left and 2,3,4,5,6,7 right. Use L₁ for the left flank, (H₁,L₈) on the left interior, (L₂,L₃,L₄,L₅,L₆,L₇,H₂,H₃,H₄,H₅,H₆,H₇,L₁₁) on the right interior, and L₉ for the right flank. These names bind the controls to the prescribed original slots. Each terminal table uses actual index order, with index zero transported from the unit seed. Every physical reversal uses the same labels on the correspondingly reversed names, retaining index order inside sections.

## 1. All-three 47-edge control

Fix `[[3],[3,3],[3,3,3,3,3,3,3],[3]]`, with F=33 and m=47. Multiply the h=6 unit allocation at F₀=11 by three. For low hosts the successive normalized input and output increments are 0,11,22. For high hosts the successive input increments are 0,11,22 and the output increments are 22,11,0. The low unit rows for L₁,L₂,L₃,L₄,L₅,L₆,L₈ are (5,7),(7,8),(10,10),(1,0),(8,6),(4,1),(9,4). The high rows for H₁,H₂,H₃,H₄ are (0,9),(6,2),(2,5),(3,3). Both unit inventories are [0,10]. Each multiplied block contains all 11 residues.

| Actual name | Role | Center | Terminal labels | Actual terminal differences |
|---|---:|---:|---|---|
| b:0:0 | L₁ | 1 | 14,25,36 | 13,24,35 |
| b:1:0 | H₁ | 46 | 9,20,31 | 37,26,15 |
| b:1:1 | L₅ | 5 | 17,28,39 | 12,23,34 |
| b:2:0 | L₂ | 2 | 16,27,38 | 14,25,36 |
| b:2:1 | L₃ | 3 | 19,30,41 | 16,27,38 |
| b:2:2 | L₄ | 4 | 10,21,32 | 6,17,28 |
| b:2:3 | L₈ | 8 | 18,29,40 | 10,21,32 |
| b:2:4 | H₄ | 43 | 12,23,34 | 31,20,9 |
| b:2:5 | H₃ | 44 | 11,22,33 | 33,22,11 |
| b:2:6 | H₂ | 45 | 15,26,37 | 30,19,8 |
| b:3:0 | L₆ | 6 | 13,24,35 | 7,18,29 |

The spine is (42,0,47,7) with differences (42,47,40). The table's folded center attachment weights are (1,46,5,45,44,43,39,4,3,2,41). They and the spine give [1,5]∪[39,47]. Only the two exterior weights change in T, to |42−1|=41 and |7−6|=1. The terminal labels and differences in the table exhaust [9,41] and [6,38]. Together with skeleton and spine these give both full alphabets.

## 2. Nonuniform 63-edge control

Fix `[[3],[3,1],[3,3,3,3,3,3,3,3,3,3,1,1,1],[3]]`. There are 17 hosts, including 13 at quota three and four at quota one. The 43 terminals give 63 edges and 64 vertices. Use the h=9 F₀=17 unit seed and an independent h₀=7 packet of G=13. All its numerical rows are indicated below. A dash indicates zero auxiliary quota, with the unit original terminal still carried. For a low row, the resulting actual label tuple is (i+25,u+12,u+42), with differences (w+22,v+9,v+39). For a high row the label tuple is the same and the differences are (w+22,v+39,v+9). The auxiliary and carried normalized blocks are [0,12], [13,29] and [30,42], on both sides.

| Actual name | Role | Unit (i,w) | Packet (u,v) | Center | Terminal labels | Actual terminal differences |
|---|---:|---|---|---:|---|---|
| b:0:0 | L₁ | (13,15) | (8,10) | 1 | 38,20,50 | 37,19,49 |
| b:1:0 | H₁ | (4,11) | (0,11) | 62 | 29,12,42 | 33,50,20 |
| b:1:1 | L₈ | (10,5) | — | 8 | 35 | 27 |
| b:2:0 | L₂ | (11,12) | (6,7) | 2 | 36,18,48 | 34,16,46 |
| b:2:1 | L₃ | (16,16) | (12,12) | 3 | 41,24,54 | 38,21,51 |
| b:2:2 | L₄ | (1,0) | (1,0) | 4 | 26,13,43 | 22,9,39 |
| b:2:3 | L₅ | (15,13) | (11,9) | 5 | 40,23,53 | 35,18,48 |
| b:2:4 | L₆ | (12,9) | (9,6) | 6 | 37,21,51 | 31,15,45 |
| b:2:5 | L₇ | (8,4) | (5,1) | 7 | 33,17,47 | 26,10,40 |
| b:2:6 | H₂ | (0,14) | (2,8) | 61 | 25,14,44 | 36,47,17 |
| b:2:7 | H₃ | (5,8) | (7,2) | 60 | 30,19,49 | 30,41,11 |
| b:2:8 | H₄ | (2,10) | (3,5) | 59 | 27,15,45 | 32,44,14 |
| b:2:9 | H₅ | (9,2) | (4,3) | 58 | 34,16,46 | 24,42,12 |
| b:2:10 | H₆ | (3,7) | — | 57 | 28 | 29 |
| b:2:11 | H₇ | (6,3) | — | 56 | 31 | 25 |
| b:2:12 | L₁₁ | (14,6) | — | 11 | 39 | 28 |
| b:3:0 | L₉ | (7,1) | (10,4) | 9 | 32,22,52 | 23,13,43 |

The two source coordinate columns separately exhaust [0,16] and [0,12] for inputs and weights. The final labels and endpoint differences in the table give [12,54] and [9,51]. The spine (55,0,63,10) gives differences (55,63,53). The actual folded center attachments in order have weights (1,62,8,61,60,59,58,57,56,2,3,4,5,6,7,52,54). Together they give the skeleton [1,8]∪[52,63]. Restoring the literal outward attachments exchanges 1 and 54 by |55−1|=54 and |10−9|=1. All other incidences coincide. The actual reflected graph has spine (10,63,0,55) and the opposite indexed section order, with the same transported weights. Four unit quotas and seven high slots force at least three high grows in any D226 role assignment to these lists.

## 3. Sparse centered obstruction and direct marked positive

Fix `[[1],[3,3],[1,1,1,1,1,1,1],[1]]`. It has F=15 and m=29. In this marking every lawful assignment gives support U={H₁,L₅}, independent of which of the two actual left centers occupies each role. Any centered packet, joint or repeated, has total width G=2. At normalized input u=1, H₁ would give v=−1 and L₅ also v=−1. Neither is admissible even for degree one there, ruling out a centered completion for this support.

For a general allocation, start from the h=6 unit rows in Section 1. D225's shared cut (5,3) with width 2 gives both fresh rows to L₅ and grows it to three. Then grow H₁ by two using D225's single movable maximum. In the second step the old maximum at L₃, (12,12), moves to (14,14). H₁'s fresh normalized rows are (0,13) and (13,0), while the ordinary old coordinates each grow by one. The resulting complete named original and fold follow.

| Actual name | Center | Terminal labels | Actual terminal differences |
|---|---:|---|---|
| b:0:0 | 1 | 17 | 16 |
| b:1:0 | 28 | 10,9,22 | 18,19,6 |
| b:1:1 | 5 | 20,15,16 | 15,10,11 |
| b:2:0 | 2 | 19 | 17 |
| b:2:1 | 3 | 23 | 20 |
| b:2:2 | 4 | 11 | 7 |
| b:2:3 | 8 | 21 | 13 |
| b:2:4 | 25 | 13 | 12 |
| b:2:5 | 26 | 12 | 14 |
| b:2:6 | 27 | 18 | 9 |
| b:3:0 | 6 | 14 | 8 |

The actual alphabets of the terminal columns are [9,23] and [6,20]. The spine (24,0,29,7) has weights (24,29,22), and the folded attachments (1,28,5,27,26,25,21,4,3,2,23) give with the spine [1,5]∪[21,29]. Restoration gives |24−1|=23 and |7−6|=1, leaving the full weight alphabet for T. Thus the centered obstruction holds in the exact same marking as the direct positive.

## 4. Joint lift, parallels and width zero

At h=6 and old F=11, use support {L₂,L₃,L₅,H₁}. Mark these in the original role order above by profile `[[1],[3,3],[3,3,1,1,1,1,1],[1]]`, F=19 and m=33. The G=4 lift in the proof has upper start 15. A concrete lift installs L₂ rows (0,1),(16,17), L₃ rows (3,3),(18,18), L₅ rows (2,0),(17,15), and H₁ rows (15,2),(1,16). The vacant alphabets are [0,3]∪[15,18] in both coordinates. At H₁ the two sums are 17=F′−2. At the lows the shifts are +1,0,−2. Translating the explicitly named unit rows of Section 1 by (4,4) and appending these rows at the named hosts gives the full marked allocation and exchange 1↔27. The four-cycle has two high edges. A different example at G=3 with parallel edges at (1,0), one L₄ and one H₁, obeys both projected row equations. Its odd-high two-cycle fails the bit test because the two distinct input bits would yield equal output bits. This is a local cycle check and asserts no complete multigraph on that example. The zero-width shift gives neither block and all old rows and original counts remain.

The same joint positive is the matched control in Section 6. Its actual spine (28,0,33,7) gives weights (28,33,26). The complete named terminal tuples, with center and actual terminal differences, follow.

| Actual name | Center | Terminal labels | Actual terminal differences |
|---|---:|---|---|
| b:0:0 | 1 | 18 | 17 |
| b:1:0 | 32 | 13,10,24 | 19,22,8 |
| b:1:1 | 5 | 21,11,26 | 16,6,21 |
| b:2:0 | 2 | 20,9,25 | 18,7,23 |
| b:2:1 | 3 | 23,12,27 | 20,9,24 |
| b:2:2 | 4 | 14 | 10 |
| b:2:3 | 8 | 22 | 14 |
| b:2:4 | 29 | 16 | 13 |
| b:2:5 | 30 | 15 | 15 |
| b:2:6 | 31 | 19 | 12 |
| b:3:0 | 6 | 17 | 11 |

The terminal labels and weights cover [9,27] and [6,24]. The folded center attachment weights in order are (1,32,5,31,30,29,25,4,3,2,27). The two literal exterior weights are |28−1|=27 and |7−6|=1. Thus S and T have both complete alphabets.

## 5. Direct 31-edge positive with a bank already present

Fix `[[1],[3,3],[1,1,1,1,1,1,1],[3]]` using the roles above. This was the initial candidate for a diagnostic. Its three grown roles H₁,L₅,L₆ require centered width G=3, where the L₆ shift −3 cannot occur at any projected input. A direct positive was supplied symbolically during mathematical review.

In the subgraph with L₆ still unit, use F=15 and assign the H₁ rows (0,13),(1,12),(2,11). Set L₃ to (14,14). The remaining highs H₂,H₃,H₄ are (8,4),(9,2),(10,0). The low rows at L₁,L₂,L₄,L₆,L₈ are respectively (5,7),(4,5),(7,6),(6,3),(13,8). Use (3,1),(11,9),(12,10) at L₅. These satisfy the actual affine equations and fill both alphabets [0,14], with exact quotas. This independent allocation has a deeper H₁ bank than the D226 quota-funded schedule guarantees at this quota.

Apply the D226 negative-shift operation directly with d=3,u=1 to L₆. Move the three fixed-input H₁ weights to 15,14,13, move the top identity to (16,16), and shift the other rows by (1,1). The fresh L₆ rows (3,0),(15,12) complete [0,16] in both coordinates. The following labels, in actual index order, use the original graph at F=17 and m=31.

| Actual name | Center | Terminal labels | Actual terminal differences |
|---|---:|---|---|
| b:0:0 | 1 | 15 | 14 |
| b:1:0 | 30 | 9,10,11 | 21,20,19 |
| b:1:1 | 5 | 13,21,22 | 8,16,17 |
| b:2:0 | 2 | 14 | 12 |
| b:2:1 | 3 | 25 | 22 |
| b:2:2 | 4 | 17 | 13 |
| b:2:3 | 8 | 23 | 15 |
| b:2:4 | 27 | 20 | 7 |
| b:2:5 | 28 | 19 | 9 |
| b:2:6 | 29 | 18 | 11 |
| b:3:0 | 6 | 16,12,24 | 10,6,18 |

The terminal alphabets are [9,25] and [6,22]. The spine (26,0,31,7) gives weights (26,31,24). The folded center attachment weights in order are (1,30,5,29,28,27,23,4,3,2,25). The two actual exterior endpoints give |26−1|=25 and |7−6|=1. Both named labelings therefore have complete edge and vertex inventories.

## 6. One proposed matched discriminator for separate authorization

**Proposal only.** The sole unresolved target in this proposal is `[[3],[3,3],[1,1,1,1,1,1,1],[3]]` with m=33, F=19 and h=6. Fix T, S and the marks and names as declared at the start, with left pairs 1,5 and right pairs 2,3,4. All equal-quota name changes within each side preserve arithmetic feasibility and lift by permuting the corresponding actual branch and terminal groups, keeping terminal indices. This target has just the numerical support {L₁,H₁,L₅,L₆}. Its two growing sides and both flanks are fixed. The two controls are Section 4 (equal order, equal number of grows and both arms positive), and Section 5 (centered negative with general allocation positive). The 29-edge control remains additional archival hand evidence.

**Arm A.** Exact centered joint-packet feasibility is excluded symbolically for the target. The total width is G=4. The two L₆ rows must both use the sole admissible projected edge (3,0). They consume both uses of input 3 and output 0. The L₅ rows can only project to (2,0) and (3,1). Both are blocked, so there is no degree-two graph, before any cycle parity or bit choice. This exclusion includes a sequence of centered additions.

**Arm B.** Decide existence of a complete allocation at F=19 on the same marked skeleton, with every admissible affine row and the exact final quotas. No old row or unit-seed cut is fixed. The smaller direct certificate in Section 5 exercises a way to supply Arm B even when Arm A and the D226 bank-admission conditions fail. It does not decide this new target. A positive or a proved exhaustive negative decides only the declared fixed-mark question for the target.

Proposed finite ceilings are one worker, one target, the two controls, and a single shared allowance of 16 distinct certificate or status records and 131,072 evidence bytes. The Arm A endpoint reasoning and the explicit control lifts can be checked directly without enumerating multigraphs. At F=19 and 11 hosts there are at most 209 candidate host-input rows per profile before discarding invalid weights. The F=17 control has at most 187, so initial row generation for the three profiles needs at most 605 attempts. A finite exact branch procedure consumes a remaining input, its chosen unused weight and one quota at the chosen host. It terminates at at most 19 selected rows, with 20 live recursion frames including the root. Propose 1,000,000 total branch nodes, 60 measured CPU seconds and 120 seconds foreground elapsed for the entire comparison including independent certificate verification. These are limits for separate review, with no automatic escalation. An interrupted traversal remains incomplete.

Any later authorized comparison must record the exact originals, marks, residual rules, visited or exhausted scope, distinct labels and weights, quotas and the literal exterior restoration. Require an independent audit of actual endpoint differences on both named graphs and every terminal index. No software, run manifest or execution artifact has been prepared.
