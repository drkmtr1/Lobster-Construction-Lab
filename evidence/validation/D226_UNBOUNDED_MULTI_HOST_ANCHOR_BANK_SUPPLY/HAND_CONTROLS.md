# D226 — Named arithmetic and boundary controls

## 1. Exact 69-edge original and fold

Specify the profile `[[3],[15,3],[3,7,5,3,5,3,3],[5]]` on the four consecutive spine vertices `s:0,s:1,s:2,s:3`. Use the listed indexed branch vertices `b:i:a` with edge `s:i--b:i:a`, and all terminal names `l:i:a:e` for 0≤e<Q with edge `b:i:a--l:i:a:e`. Define S on the same names with only the two exterior branch edges replaced by `s:1--b:0:0` and `s:2--b:3:0`. Define its auxiliary unit version and the corresponding unit original by retaining exactly terminal index zero everywhere. These graphs are fixed before assigning labels. The final F=55, h=6, m=69 and there are 70 vertices. The unit stage has F=11 and m=25.

Use left pairs 1,5 and right pairs 2,3,4. The six marks are (0,m,m−5,7,1,6). In the unit allocation L₃ has (10,10), L₄ has (1,0), L₆ has (4,1) and H₂ has (6,2). The remaining high rows by offset (1,3,4) are (0,9),(2,5),(3,3). The remaining lows at (1,2,5,8) are (5,7),(7,8),(8,6),(9,4). These use every coordinate 0,…,10 on each side. The host names in the final table below are fixed already at this unit stage. Each row is transferred with the terminal index it has when first installed.

Choose r=3 at L₃, s=7 at H₁. All nonbank hosts grow, so (K,P,D)=(4,2,5), giving r+1=K and s=P+D. First grow L₃, then H₄,H₃,H₂. Give H₁ the first width 2, use positive shifts +2,+1, and give H₁ the second width 5. Finish with negative shifts of magnitudes 5,3,2,1. Each listed interval of fresh inputs and weights is inclusive. The two sets in the last two columns are unordered and their map is the actual host relation.

| Host grown | Old F | New F | Fresh inputs | Fresh weights |
|---|---:|---:|---|---|
| L₃ | 11 | 17 | [0,2], [14,16] | [0,2], [14,16] |
| H₄ | 17 | 21 | [0,1], [15,16] | [0,1], [15,16] |
| H₃ | 21 | 23 | 0,19 | 0,19 |
| H₂ | 23 | 25 | 0,22 | 0,22 |
| H₁, first | 25 | 29 | [0,1], [26,27] | [0,1], [26,27] |
| L₁ | 29 | 31 | 0,27 | 2,29 |
| L₂ | 31 | 33 | 0,30 | 1,31 |
| H₁, second | 33 | 43 | [0,4], [37,41] | [0,4], [37,41] |
| L₈ | 43 | 45 | 5,43 | 0,38 |
| L₆ | 45 | 49 | [3,4], [46,47] | [0,1], [43,44] |
| L₅ | 49 | 51 | 2,49 | 0,47 |
| L₄ | 51 | 55 | [1,2], [52,53] | [0,1], [51,52] |

For clarity the four top identities at F=17 are 13,14,15,16. Their subsequent sets at F=21,23,25 are {17,18,19,20}, {18,20,21,22}, {19,21,23,24}. Thus exactly the needed top portion is still available at each high step. The first H₁ installment gives the transposed bank at inputs 26,27 with respective weights 1,0. The L₁ move returns it at 28,29 with weights 1,0. L₂ uses the row at 29 and returns it at 31 with weight 0, while L₁'s later translated row occupies input 1 and L₂ occupies input 0. At F=33 the whole H₁ input set is {2,3,11,29,31}. The second installment supplies H₁ with inputs 0 through 4 at F=43 and weights 41 through 37 in reverse order. Growth at L₈ returns those five fixed-input rows. L₆, L₅ and L₄ use respectively the required prefixes of lengths three, two and one. Each width uses only the indicated host's final quota.

The final spine labels are (64,0,69,7), giving differences (64,69,62). In the table the terminal labels and their absolute differences appear in increasing **terminal index** order. For example the first H₁ terminal carries normalized input 22 at the end, while the first terminal from its second installment retains normalized input 0. In every row use z=i+9.

| Actual name | Role | Center label | Terminal labels | Actual terminal differences |
|---|---|---:|---|---|
| `b:0:0` | L₁ | 1 | 36,21,48 | 35,20,47 |
| `b:1:0` | H₁ | 68 | 31,22,23,49,51,9,12,14,17,18,52,53,54,55,56 | 37,46,45,19,17,59,56,54,51,50,16,15,14,13,12 |
| `b:1:1` | L₅ | 5 | 39,13,60 | 34,8,55 |
| `b:2:0` | L₂ | 2 | 38,20,50 | 36,18,48 |
| `b:2:1` | L₃ | 3 | 43,28,29,30,45,47,63 | 40,25,26,27,42,44,60 |
| `b:2:2` | L₄ | 4 | 32,10,11,61,62 | 28,6,7,57,58 |
| `b:2:3` | L₈ | 8 | 40,19,57 | 32,11,49 |
| `b:2:4` | H₄ | 65 | 34,26,27,41,42 | 31,39,38,24,23 |
| `b:2:5` | H₃ | 66 | 33,25,44 | 33,41,22 |
| `b:2:6` | H₂ | 67 | 37,24,46 | 30,43,21 |
| `b:3:0` | L₆ | 6 | 35,15,16,58,59 | 29,9,10,52,53 |

The terminal labels in the table, sorted across the named rows, form [9,63] once each. The displayed centers and spine are its complement in [0,69]. The 55 terminal differences form [6,60] once each. In table order the actual folded attachment weights are (1,68,5,67,66,65,61,4,3,2,63). Together with the three spine edges these are [1,5]∪[61,69]. Only the first and last of these attachment weights change in T. The left becomes |64−1|=63 and the right |7−6|=1. Thus both named trees have the full vertex and difference alphabets and every actual terminal quota. The reflected original assigns these same labels to the section-reversed names, so every weight, including those of the restored edges, transports to its reversed original edge.

## 2. Adverse, zero-width and recurrence controls

- Lower only the example's L₃ quota from 7 to 5, retaining its H₄ demand. Now r=2 produces a top block of length exactly three, so the first high offset 4 lacks its required block. If an attempted H₄ growth moves only three identities while keeping all other old rows on the stated uniform translation, its highest fresh input maps to weight −1. This fails the declared transport. Other assignments are outside this control.
- Lower only the example's H₁ quota from 15 to 13. Then s=6 and this order spends 2 on positive shifts, leaving width 4 for a negative-shift bank of required depth 5. At pre-regeneration F=33 the H₁ inputs are still {2,3,11,29,31}. The old H₁ inputs translate by 4 and the four new low inputs are 0,1,2,3. The new upper interval begins at 36, so H₁ does not own input 4. The first negative-shift transport lacks its fifth distinguished row. This is an adverse schedule control within the prescribed allocation.
- For all-unit quotas K=1 and P=D=r=s=0. Both installments and initial growth have width zero. In the identity-block and both low-growth formulas all fresh intervals are empty at zero width and all existing assignments remain fixed. The seed supplies the exact unit original. An empty positive or negative phase can be omitted independently when its width is zero.
- For h=6→10 the D225 recurrence takes F₀=11 to 19. Carry inputs [4,13] except 5 with weights [1,9]. Restore (1,0) at low 4 and (18,18) at low 3. The four high additions at offsets 1,2,3,4 use (3,14),(0,16),(5,10),(2,12). The four low additions at 1,2,7,8 use (15,17),(14,15),(17,13),(16,11). They obey the actual new affine rules and fill exactly inputs {0,2,3,5}∪[14,17] and weights [10,17]. The returned maximum then supplies any requested identity block by the same L₃ manufacture.
- For h=7, j=3, ℓ=8, put only pair 3 on the right. Pairs 1,2,4,5,6 fit on the left. In particular h−3=4 is left, while H₁ remains an even-side interior and L₃ an odd-side interior. The whole-pair attachments and affine rows remain valid, illustrating the absence of the shared-cut recipient-side requirement.

## 3. Singleton at the minimum cross-interior multiplicity

In the D224 auxiliary h=5 seed, use (ℓ,j)=(2,5), F=9, cut (4,3), left pairs 1,4, and right pairs 2,3. The two actual interior recipients are L₄ and H₂. At G=1 the new F is 10 and the sole fresh row is (4,3). Both L₄'s shift −1 and H₂'s new sum F−1−2=7 give this row. Allocating it to either host gives the corresponding mixed-parity choice of quota two there and one at the other. All old rows transport by the established cut under the same side placement. At m=22 the restoration still exchanges 1 and m−5=17. With larger odd G, precisely the same singleton plus whole reflected pairs add the desired positive integer quotas of opposite parity.
