# An unequal two-center return on the original spine

[Authorized task](../tasks/LCL_Codex_D081_Unequal_TwoCenter_R241_Return_2026-11-22.md) · [Verified intake](../evidence/validation/LCL_R241_UNEQUAL_TWO_CENTER_RETURN_001/INTAKE.md) · [Evidence](../evidence/validation/LCL_R241_UNEQUAL_TWO_CENTER_RETURN_001/README.md)

## The selected fixed-port question

Let G be the exact original `[[1,2],[1]]`. Its physical spine is s:0–s:1. At section zero b:0:0 has one indexed terminal and b:0:1 has two. At section one b:1:0 has one terminal. Each center is adjacent only to its own spine vertex and its own terminals. Connectivity and s:0 low force the low class to be s:0, b:1:0 and the three first-section terminals. The other four names are high. The original order is nine, the low size is five and the edge count is eight. The spine witnesses all names with center distance one and terminal distance two.

Fix `s:0=1, s:1=5`, the required physical offsets (1,0). Write A and B for the labels of b:0:0 and b:0:1, and z for the label of b:1:0. All weights are high minus low. Summing signed degree times label gives the following two contributions.

| Class | Alphabet sum | Extra contributions from degree above one |
| --- | ---: | --- |
| High | 26 | `5+A+2B`, from s:1 and the two first centers |
| Low | 10 | `2+z`, from s:0 of degree three and b:1:0 of degree two |

The resulting sum is `19+A+2B−z`. Gracefulness requires 36, so `z=A+2B−17`. The six ordered distinct choices for (A,B) from {6,7,8} yield:

| (A,B) | Forced z | z belongs to the free low set {0,2,3,4} |
| --- | ---: | --- |
| (6,7) | 3 | yes |
| (6,8) | 5 | no |
| (7,6) | 2 | yes |
| (7,8) | 6 | no |
| (8,6) | 3 | yes |
| (8,7) | 5 | no |

In the first and third table rows, 8 is at the only second-section terminal. Its only neighbor has label 3 or 2. Since the only label pair with weight 8 is (0,8), the required weight is absent. In the fifth row, 8 is at b:0:0. Its spine neighbor already has label 1, so its indexed terminal must carry 0 to realize weight 8. The indexed terminals at b:0:1=6 must then carry 2 and 4. Its edge to the terminal labeled 2 repeats weight 4 already on s:0–s:1. Therefore no assignment satisfies the exact (1,0) interface.

The alternate and neighboring controls have the following original label and weight ledgers. For the weights, read the spine first, then each center attachment followed by its terminal edges in their original index order.

| Original names in order | G at (2,0) | `[[1,2],[2]]` at (1,0) |
| --- | --- | --- |
| s:0, s:1 | 2, 5 | 1, 5 |
| b:0:0, l:0:0:0 | 7, 3 | 9, 0 |
| b:0:1, l:0:1:0, l:0:1:1 | 8, 0, 1 | 8, 2, 3 |
| b:1:0 and terminals by index | 4, 6 | 4, 6, 7 |
| Original weights | 3, 5, 4, 6, 8, 7, 1, 2 | 4, 8, 9, 7, 6, 5, 1, 2, 3 |

Both cases use exactly [0,4] and the full complementary high band with each original edge crossing. They are witnessed alpha states on their own named originals. The exact obstruction is therefore a failure of prescribed ports. The diagnostic domains fix the two actual ports. On G each pinning leaves four lows and three highs free, giving `4!·3!=144` ordered named assignments. The neighbor leaves four free on each side, giving `4!·4!=576`. The two G domains have different labels at s:0 and are disjoint, though they share the same named original.

## Direct supply for F(b)

For every exact integer b≥0 take the original profile `F(b)=[[1,b],[b]]`, with all three named centers present. Its order is `N_B=2b+6`, low size `P_B=b+3` and edge count `2b+5`. Assign:

| Original vertex or group | Label |
| --- | --- |
| s:0, s:1 | 1, b+3 |
| b:0:0, l:0:0:0 | 2b+5, 0 |
| b:0:1 | 2b+4 |
| l:0:1:j, 0≤j<b | 2+j |
| b:1:0 | b+2 |
| l:1:0:j, 0≤j<b | b+4+j |

The low labels occur once as {0}, {1}, [2,b+1], {b+2}. The highs occur once as {b+3}, [b+4,2b+3], {2b+4}, {2b+5}. Every edge crosses the cut. On all actual edges the weights are:

| Original edge group | Absolute difference |
| --- | --- |
| s:1–b:1:0 | 1 |
| b:1:0–l:1:0:j | `2+j`, spanning [2,b+1] |
| s:0–s:1 | b+2 |
| b:0:1–l:0:1:j | `2b+2−j`, spanning [b+3,2b+2] |
| s:0–b:0:1 | 2b+3 |
| s:0–b:0:0 | 2b+4 |
| b:0:0–l:0:0:0 | 2b+5 |

The bands partition the whole weight alphabet [1,2b+5] once each. At b=0 both variable terminal families are empty, but b:0:1 and b:1:0 retain their attachments as actual direct leaves. In that case the five fixed weights are 1,2,3,4,5 and the six labels are distinct. For every b the two actual spine ports witness distance at most two and have labels 1 and P_B. This gives `A(2b+6,b+3;1,0)` by finite assignments on the original. At b=1 the formula is exactly D079's retained named (1,0) ledger, including each indexed leaf. At b=2 it is the neighboring strict control above.

## The joined macro R(b,a)

For exact b≥0 and a≥1 place F(b) at sections 0,1 as old B. Place the [D080 bridge H(a)](R241_ZERO_TO_ONE_BRIDGE.md#independent-replacement-ha), with `N_A=2a+5, p_A=a+2` and offsets (0,1), as new A at sections 2,3. Renumber the section field only, preserving every branch and terminal index. The unique original crossing between these disjoint blocks is s:1–s:2. R241's actual offset equality is `y_B=0=x_A`. Keep B lows, add N_A to B highs and P_B to all of A.

| Label group | Interval after placement |
| --- | --- |
| B lows | [0,b+2] |
| A lows | [b+3,a+b+4] |
| A highs | [a+b+5,2a+b+7] |
| B highs | [2a+b+8,2a+2b+10] |

These partition the full labels at cut `P_R=a+b+5`. The actual connector joins s:1 at `b+3+N_A` to s:2 at `b+3`, giving `N_A=2a+5`. A's old differences are [1,2a+4]. B's old differences each gain N_A since only their high endpoint moves, giving [2a+6,2a+2b+10]. Together with the connector these exhaust the full weights once. The physical entrance remains s:0 at 1 and the physical exit s:3 becomes `P_B+a+3=P_R+1`. Each old edge and the connector cross the new cut. The original joined spine is a witness. Every center still has distance one and every terminal two. The joined graph is precisely `R(b,a)=[[1,b],[b],[a],[a+1]]`, a tree on the disjoint blocks with the original connector. It supplies `A(2a+2b+11,a+b+5;1,1)`. [Pinned R241 proof](https://github.com/drkmtr1/Math-Discovery-Lab/blob/858a8c1fcfda87ba40bb1adee498a6131504a803/research/candidates/volume-010.md#L4364-L4405)

## Finite repetition and exact suffix

Take any finite nonempty list of these blocks with independent integers b_i≥0 and a_i≥1, placed on their original successive four-section groups. Start with the first R. At each further step the preceding aggregate B and the next A are disjoint, the previous high exit and new low entrance are consecutive physical spine vertices, and `y_B=x_A=1`. Only their actual connector edge is used. With component orders N_B,N_A and low sizes P_B,p_A the R241 label bands are `[0,P_B−1]`, `[P_B,P_B+p_A−1]`, `[P_B+p_A,P_B+N_A−1]`, `[P_B+N_A,N_B+N_A−1]`. The weight bands are `[1,N_A−1]`, `{N_A}`, `[N_A+1,N_A+N_B−1]`. They establish exact normalization and return the old physical entrance at 1 and the actual last spine vertex at `P_B+p_A+1`. The two old witness paths adjoin via the connector, giving the original longer spine. This proves the next premise and finishes by finite induction, after one within-macro join per block and one across-block join per adjacent pair.

The resulting original has `P=Σ_i(a_i+b_i+5)`, `N=Σ_i(2a_i+2b_i+11)`, and for k blocks its exit is physical s:(4k−1) at P+1. At L=0 this already labels the full original as alpha graceful. For L≥2, shift by L only the prefix high labels. The used labels are [0,P−1] and [P+L,N+L−1]. Each original assigned-edge weight gains L and the used weights are [L+1,N+L−1]. Taking complements in the full alphabets gives R=[P,P+L−1], D=[1,L] at physical exit P+L+1. The only unassigned vertices are the appended empty spine sections. Their incident edges are exactly the consecutive L-edge path from that exit, with its first edge the sole crossing.

The [retained recurrence](B2_NONADJACENT_CONSUMER.md#construction-and-proof) translated by P supplies exactly that path after checking both inventories. Its bases at L=2,3,4 are (3,1,0), (4,1,0,2), (5,1,2,0,3). For L≥5 prepend (L+1,1,L−1) to all of C_(L−3) reflected under `u↦L−2−u`. The reflection begins at 0 and its subsequent labels give precisely [2,L−2]. With 1 and L−1 these exhaust the suffix labels. Edges down to the reflected zero give L,L−2,L−1. The edge from that zero to the next entry is the first smaller edge reflected, so with later reflected edges it gives [1,L−3] once each. The recursion decreases by three to a base. This proves ordinary gracefulness on the stated original at L≥2. The prescribed shift at L=1 instead leaves R={P}, D={1} at P+2, whose sole possible continuation edge would weigh 2.

## Optional symbolic compatibility with D078

For a finite nonempty list of independently supplied R(b,a) blocks and [D078 M(c,d) blocks](R241_PAIRED_BRANCHED_SPINE.md#independently-supplied-modules), with the latter's exact nonnegative quotas, every block has actual offsets (1,1). Place each block on its specified consecutive original sections. Then each adjacent equality and witness condition in the preceding induction still holds, including when the new block has two sections instead of four. N and P are the sums of the actual block orders and low sizes and the final exit remains at P+1. The same L=0 and L≥2 proof applies with the exit at the last supplied spine vertex. This is a symbolic consequence using only the two already described independent suppliers and adds no finite test cases. It covers precisely original concatenations of those blocks.

The exact unequal original G remains excluded for (1,0). The proved repeatable pattern has tied quotas within each F and H. Arbitrary multiple-center sections, empty interior sections and general non-alpha supply remain open.
