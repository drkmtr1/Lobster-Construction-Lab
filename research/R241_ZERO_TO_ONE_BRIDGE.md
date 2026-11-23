# A zero-to-one R241 bridge and a repeatable four-section macro

[Authorized task](../tasks/LCL_Codex_D080_Zero_To_One_R241_Bridge_2026-11-22.md) · [Roadmap](../docs/strategy/LCL_Branched_Spine_Research_Roadmap_2026-11-22.md) · [Evidence](../evidence/validation/LCL_R241_ZERO_TO_ONE_BRIDGE_001/README.md)

## The selected `[[1],[1]]` interface fails

The original six-vertex tree has spine edge s:0–s:1, attachments s:0–b:0:0 and s:1–b:1:0, and one indexed terminal edge at each center. With s:0 low and s:1 high, every edge must cross the alpha cut. Connectivity forces low names s:0, b:1:0, l:0:0:0 and high names s:1, b:0:0, l:1:0:0. Their alphabets are [0,2] and [3,5]. The original spine edge witnesses the module. Each center is one edge away and each terminal two.

Offsets (0,1) require s:0=0 and s:1=4. Difference 5 must join labels 0 and 5. The neighbors of s:0 are s:1, already pinned to 4, and its center b:0:0. The center must therefore carry 5. The first terminal has label 1 or 2. At 1 its edge has difference 4, repeating the spine weight. At 2 its edge has difference 3, leaving 1 for b:1:0. The edge from s:1 to b:1:0 then also has difference 3. This exhausts the original possibilities and rejects the specified interface. The four pinned assignments are a separate finite check.

For the same graph, s:0=0 and s:1=3 with first center and terminal 5,1 and second center and terminal 2,4 give weights (3,5,4,1,2) when read spine first, then each attachment and terminal edge. Both vertex alphabets occur exactly once on the proper side. This supplies `A(6,3;0,0)` at the actual spine ports.

## Independent replacement H(a)

For every exact integer a≥1 let `H(a)=[[a],[a+1]]` in the original names. Write `p=a+2` and `N_A=2a+5`. The low names are s:0, b:1:0 and the a first-section terminals. The high names are s:1, b:0:0 and the a+1 second-section terminals. Give them the following labels.

| Actual vertex or group | Label |
| --- | --- |
| s:0 | 0 |
| s:1 | a+3 |
| b:0:0 | 2a+4 |
| b:1:0 | a+1 |
| l:0:0:j, 0≤j<a | j+1 |
| l:1:0:0 | a+2 |
| l:1:0:j, 1≤j≤a | a+3+j |

The lows partition [0,a+1] as {0}, [1,a], {a+1}. The highs partition [a+2,2a+4] as {a+2}, {a+3}, [a+4,2a+3], {2a+4}. Every original edge crosses that cut. Its differences are

| Actual edge group | Difference |
| --- | --- |
| b:1:0–l:1:0:0 | `(a+2)−(a+1)=1` |
| s:1–b:1:0 | `(a+3)−(a+1)=2` |
| b:1:0–l:1:0:j, 1≤j≤a | `j+2`, giving [3,a+2] |
| s:0–s:1 | a+3 |
| b:0:0–l:0:0:j, 0≤j<a | `2a+3−j`, giving [a+4,2a+3] |
| s:0–b:0:0 | 2a+4 |

The disjoint bands give every difference in [1,2a+4] once. At a=1 the second-section terminals have indices 0 and 1 and both are used. As above, all vertices are within distance two of the original spine edge. The exact low and high ports s:0 and s:1 have labels 0 and p+1, so this gives `A(2a+5,a+2;0,1)` directly. The finite indexed assignments terminate for each a.

## The original four-section macro Q(a)

Take D079's exact B=`[[1,1],[1]]` at sections 0 and 1. Its retained named ledger gives s:0=1, s:1=4, first-section center/terminal pairs (7,0) and (6,2), and second-section center/terminal (3,5). It uses differences (3,6,7,5,4,1,2) on its original spine, attachments and terminals in that order, with cut 4. Thus B has state `A(8,4;1,0)` and physical high exit s:1. Embed H(a) as A at sections 2 and 3 by increasing only the section field of every name by 2, preserving branch and terminal indices. The components are disjoint. Their only connecting edge in Q(a)=`[[1,1],[1],[a],[a+1]]` is s:1–s:2.

In adopted R241.1 the old aggregate B precedes the new A. For old B lows keep the label, for old B highs add N_A, and for all A labels add p_B. Here the old B exit offset is zero and the new A entrance offset is zero. Under placement the actual connector goes from `4+N_A` at s:1 to 4 at s:2, giving weight `N_A=2a+5`. The label groups B low, A low, A high, B high are respectively

`[0,3], [4,a+5], [a+6,2a+8], [2a+9,2a+12]`.

They are disjoint and cover [0,2a+12] at cut a+6. A's internal weights [1,2a+4] stay unchanged. B's internal weights all gain 2a+5 because only their high ends move and give [2a+6,2a+12]. The connector fills the precise missing singleton {2a+5}. Every original edge crosses the new cut. The original s:0 remains 1, and s:3 receives `4+(a+3)=a+7`, one above the low size. Thus Q(a) supplies `A(2a+13,a+6;1,1)`. Its original spine is the concatenation of the two disjoint witnesses and the actual connecting edge. Within-module distances to the witness remain at most two. One edge joins the two trees into a tree. [Pinned original R241](https://github.com/drkmtr1/Math-Discovery-Lab/blob/858a8c1fcfda87ba40bb1adee498a6131504a803/research/candidates/volume-010.md#L4364-L4405) · [D079 certificate and evidence](../evidence/validation/LCL_R241_TWO_CENTER_PORT_001/README.md)

## Repetition on the original spine

For any integer k≥1 and any exact positive integers a_1,…,a_k, concatenate the four original sections of each Q(a_i). At each step embed the next Q(a_i) by increasing its section indices by `4(i−1)`. Keep the aggregate B as the preceding prefix and the next Q as A. The old physical high exit is at the last processed spine position, with offset 1. The new first physical spine vertex has entrance offset 1. Their only join is their consecutive original spine edge, from s:(4i−5) to s:(4i−4) for i≥2. The new entrance is shifted by `P_B` and equals `P_B+1`. The old exit becomes `P_B+1+N_A`. Their difference is exactly N_A.

For a join with component orders N_B,N_A and low sizes P_B,p_A, the assigned label bands are `[0,P_B−1]`, `[P_B,P_B+p_A−1]`, `[P_B+p_A,P_B+N_A−1]`, and `[P_B+N_A,N_B+N_A−1]`. The exact ordered weight bands of the new block, connector and old prefix are `[1,N_A−1]`, `{N_A}`, and `[N_A+1,N_A+N_B−1]`. This returns the old entrance at 1 and the new physical exit at `P_B+p_A+1`, preserving the next join premise. The joined witness is the exact longer spine. Induction starts at one Q with no external join, and each further step adds exactly four original sections and their single connecting edge. The procedure terminates after k−1 such joins and the finitely many within-macro constructions.

The final prefix has `N=Σ_i(2a_i+13)`, `P=Σ_i(a_i+6)`, physical s:0 at 1 and physical s:(4k−1) at P+1. Its label and weight alphabets are [0,N−1] and [1,N−1]. It is alpha graceful and already complete for L=0.

## Continuation on the exact suffix

Append L≥2 empty original sections. Keep the lows and raise each high by L. The actual used label bands are `[0,P−1] ∪ [P+L,N+L−1]` and the assigned-edge weights are `[L+1,N+L−1]`, since every assigned edge crosses the old cut. Thus in the full original alphabets the exact complements are `R=[P,P+L−1]` and `D=[1,L]`, and physical exit s:(4k−1) carries P+L+1. The only unassigned vertices are s:4k through s:(4k+L−1), with no branch incidences. The original pending edges are the L spine edges along that suffix, with a single crossing from the active physical exit.

Use the retained numerical recurrence on this exact path after translating by P. Its three bases are `C_2=(3,1,0)`, `C_3=(4,1,0,2)`, `C_4=(5,1,2,0,3)`. For L≥5 prepend `(L+1,1,L−1)` to all of C_(L−3) reflected by `u↦L−2−u`. The reflected list starts at 0 and has the other values [2,L−2]. Along with 1 and L−1 the suffix labels exhaust [0,L−1]. The first three weights are L, L−2, L−1. The edge from reflected zero to the next entry is the first old edge after reflection, so with the remaining reflected edges it accounts for [1,L−3]. Reducing L by three terminates at a base. The translated start agrees with the active port. The remaining entries consume R and the actual suffix differences consume D once each, proving ordinary gracefulness. The narrow production B2 graph wrapper retains its s:2 scope. [Retained numerical proof](B2_NONADJACENT_CONSUMER.md#construction-and-proof)

At L=1 the same placement leaves only label P at distance two from port P+2, whereas D={1}. This only excludes that suffix interface. At Q(1), L=2 gives P=7, actual path (10,8,7) from s:3. For Q(1),Q(2) and L=5 there are N=32 prefix vertices, P=15, and 37 vertices in all. The actual path from s:7 has labels (21,16,19,15,17,18) and weights (5,3,4,2,1), with weight 2 the reflected first smaller edge. The theorem covers exactly repetitions of these four-section profiles with fixed first pair B and H quotas (a,a+1). Arbitrary multiple-center sections and interior empty sections remain outside the supplied domain.
