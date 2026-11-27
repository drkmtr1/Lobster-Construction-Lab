# D216 joint pooled-cluster reflection and two-interior-cluster supply

**PROVED WITHIN EXACT SCOPE.** The specified pooled-source reconstruction is graceful exactly when its two stated palettes are reflection invariant. An independent common-quota supplier gives the stated parameterized plain-transfer domain and covers every two-interior-group unit-quota original with unit flanks. The selected 26-edge mixed-quota original also has an independently supplied compatible pool, constructed symbolically below. No dormant diagnostic was prepared. [Exact named hand controls](../evidence/validation/D216_JOINT_POOLED_CLUSTER_REFLECTION/HAND_CONTROLS.md)

## 1. Exterior shell and actual ports

Use the fixed spine `s:0--s:1--s:2--s:3`. In section i each indexed center `b:i:j` has precisely its listed terminals `l:i:j:e`, in original index order. A listed quota zero keeps the branch vertex as a direct leaf. All quotas are nonnegative integers and all lists are finite. An interval with reversed endpoints is empty.

For p,t≥0 start from [D215](INDEPENDENT_NONNEGATIVE_EXTERIOR_SHELL.md) with b=0 and delete only its direct leaf `b:2:0` of label zero and its actual attachment of maximal weight p+t+6. Subtract one from every remaining label. The result is the exact shell `[[p],[],[],[t]]`, with k=p+t+5 edges and graceful labels [0,k]. All retained edge weights are unchanged. Its exact labels and differences are also immediate by endpoint subtraction.

| Actual vertices | g-values in order | Actual edge weights |
|---|---|---|
| Spine | (t+3,t+2,p+t+5,0) | (1,p+3,p+t+5) |
| Left and right branch vertices | (t+1,p+t+4) | (2,p+t+4) at their spine attachments |
| Left terminals | [t+4,p+t+3] | [3,p+2] |
| Right terminals | [1,t] | [p+4,p+t+3], in reverse order |

Cut t+3 puts {0}, [1,t], {t+1}, {t+2} below it and {t+3}, [t+4,p+t+3], {p+t+4}, {p+t+5} at or above it. These are disjoint consecutive pieces. The spine alternates upper, lower, upper, lower. The exterior hosts have opposite sides to their own spine parents, and their terminal intervals are on the sides opposite those hosts. Thus all actual edges cross. The weight columns partition [1,k], with p=0 or t=0 simply removing the corresponding empty terminal band. Both exterior branch attachments remain even when both quotas are zero.

In this orientation the donor `s:1` has maximum lower label A=t+2 and the actual receiver `s:2` has alpha label A+δ for δ=p+3. Read the path in reverse, exchange p and t in the formula and retain the actual branch and terminal names at their physical slots to supply the opposite donor orientation. Then the donor is actual `s:2`, A=p+2, and the receiver is actual `s:1`, with δ=t+3.

## 2. Exact two-palette theorem for fixed whole-branch reflection

Use one supplied graceful pool of N edges with the actual donor at zero. Its indexed off-spine stars, including one-vertex direct leaves, are exactly both requested interior lists temporarily attached to the donor. They keep their final branch and terminal names. The pool and shell share exactly that donor, so the D214/D215 canonical-amalgamation formula supplies the pooled intermediate tree. The shell weights are [N+1,N+k], and each pooled nonroot coordinate x=f(v) is installed at A+x for x∈[1,N]. The donor is A and the receiver is A+N+δ. The complement of the fixed shell's labels in [0,N+k] is precisely [A+1,A+N].

Let R be the branch identities whose final parent is the receiver. For a set E of actual branch identities reflect the coordinates of **every** vertex of each branch in E by ρ(x)=N+δ−x, retaining all other vertex coordinates. Then attach every center in R to the receiver and every other center to the donor. In particular, E may include branches remaining at the donor. Let P(E) be the set of all original normalized coordinates in the branches of E and S(I) the original center coordinates for any branch set I. Write M=E△R.

The fixed labels and unchanged coordinates already occupy exactly the complement of A+P(E) in [0,N+k]. Reflection is injective on P(E), so the output is a label bijection if and only if ρ(P(E))=P(E). This necessity also addresses a reflected coordinate outside [1,N], since it would be outside the target alphabet or collide with an unchanged label. The eligible interval is [δ,N]. Indeed a coordinate x∈[1,N] satisfies 1≤ρ(x)≤N exactly when δ≤x≤N. If δ>N, the eligible interval is empty. The general involution has two-element pairs and, exactly when N+δ is even and the midpoint belongs to the eligible interval, a singleton midpoint.

Each shell edge keeps its installed endpoints, including the literal `s:1--s:2` edge of weight N+δ. Each internal terminal edge has both endpoints reflected or neither, which keeps its absolute weight. For a center of original coordinate a, the actual attachment difference is:

| Final parent and label choice | Difference |
|---|---|
| Donor, unreflected | a |
| Donor, reflected | ρ(a) |
| Receiver, unreflected | ρ(a) |
| Receiver, reflected | a |

These are actual endpoint differences, since a and ρ(a) are positive, the receiver coordinate is N+δ, and subtracting ρ(a) from it returns a. Thus the only changes in the attachment-weight multiset are replacement of S(M) by ρ(S(M)). All complementary weight occurrences, including each unchanged attachment, are distinct in the original graceful intermediate tree. The new weights exhaust [1,N+k] exactly when ρ(S(M))=S(M). The originals of both partitions are ordinary sets because the source is graceful. Combining the two equivalences proves the claimed if and only if for this **fixed source, shell, parent map and whole-branch reflection**.

A direct leaf has one coordinate and no internal edge. Empty palettes impose vacuous equalities. If E is empty, the vertex condition is automatic and the exact criterion is ρ(S(R))=S(R). If N=0, R and E are empty and only H remains. On the final names, the shell edge set and every branch's internal edge set persist. The attachment edge at each center uses its required original parent. The four spine vertices witness lobster membership as every off-spine vertex is at distance at most two from its spine parent. The argument supplies no necessity for other source labelings, partial relabelings, other shells, or ordinary gracefulness itself.

## 3. Independently supplied equal terminal quotas

Let every branch have the same positive terminal quota q, let s=q+1 and L=ℓ+j, and let N=sL. When L=0 use the singleton pool. For L>0 give the root zero, center i label si, and its e-th terminal label s(L−i)+e for 1≤i≤L and 1≤e≤s−1. The centers use all positive multiples of s through N. The terminal labels are exactly all other positive integers through N, partitioned by the distinct quotients L−i.

The signed label difference from center to terminal is s(L−2i)+e. If L−2i≥0 its absolute values give the block [sd+1,sd+s−1] with d=L−2i. If L−2i<0 they give the same type of block with d=2i−L−1, since the residue becomes s−e. The first set of quotients is L−2,L−4,… down to 0 or 1, matching the parity of L. The second set runs up to L−1 and has the opposite parity. Together they are exactly [0,L−1], including L=1. Therefore every nonmultiple weight is used once and the attachments use all multiples.

If δ=sh for h≥1, reflection on center indices sends i to L+h−i. For a positive receiver branch count j, an invariant index set of size j exists in [h,L] exactly when j≤L−h+1 and an odd j has an available midpoint, namely L+h even. Indeed all pairs can be selected independently, and the single midpoint, when integral, is inside [h,L] for h≤L. A size zero selection works irrespective of h. Assign the selected indices to receiver names and all others to donor names, with their indexed terminal order as specified. This gives the sufficient conditions using E=empty. There is no requirement to change assigned final parent identities.

For p=t=q=1 the orientations both give δ=4 and h=2. Then L≥2 and each possible receiver count is at most L−1. If L is even, a midpoint exists and either orientation works. If L is odd, one group has even size, so taking that group as receiver works. This proves ordinary gracefulness for every independently positive ℓ,j on `[[1],[1]*ell,[1]*j,[1]]`. The common quota is essential to this supplied formula. No independently variable quota theorem follows from it.

## 4. Unit-flank shell classification and plain-transfer exclusion

For p=t=1 the shell is the eight-vertex path in physical order from the left terminal to the right terminal. Denote its path label sequence by (x₀,…,x₇). With the actual donor at position 3 normalized to the maximum lower label 3, highs occur at 0,2,4,6 and lows at 1,3,5,7. The signed sum of all weights equals twice the difference of the high and low label sums minus the endpoint difference x₀−x₇, since both endpoints have degree one. Therefore 28=2(22−6)−(x₀−x₇), giving x₀−x₇=4. As x₃=3, x₇∈{0,1,2}. The weight-7 edge must join 0 and 7.

- **x₇=0.** Then x₀=4 and x₆=7. The two high labels at x₂ and x₄ are 5 and 6, so the two weights incident to x₃=3 are 2 and 3. The first edge repeats one of them, as x₁∈{1,2}.
- **x₇=1.** Then x₀=5. If x₁=0, then x₂=7 and x₂−x₃=4. With x₅=2 and {x₄,x₆}={4,6}, the high 6 repeats weight 4 at x₅. Otherwise x₁=2, x₅=0 and 7 occurs at x₄ or x₆. If x₆=7 and x₄=6, weight x₄−3=3 repeats x₀−x₁. If x₆=7 and x₄=4, x₂=6 and weight x₂−x₁=4 repeats x₄−x₅. If x₄=7, x₂=6 again repeats weight 3 or 4, and x₂=4 gives the actual valid sequence (5,2,4,3,7,0,6,1) of weights (3,2,1,4,7,6,5).
- **x₇=2.** Then x₀=6. If x₁=0, x₂=7, x₅=1 and {x₄,x₆}={4,5}. The high 5 repeats weight 4 at x₅, already used by x₂−x₃. Otherwise x₁=1 and x₅=0. If x₆=7, the last weight 5 repeats the first. If x₄=7, x₂=5 repeats 4 on the donor edge, and x₂=4 forces x₆=5 to repeat the first weight 5 on x₅--x₆.

These are all possibilities, so the displayed labeling is unique in the declared normalization. Reversing the path gives the same assertion in the opposite physical orientation. The receiver label is 7 and δ=4 is forced. When N is odd, ρ(x)=N+4−x has no integer midpoint. If both branch counts are odd, either orientation has an odd number of receiver center coordinates, so plain transfer cannot have an invariant center palette. This excludes the declared plain-transfer operation only. The 20-edge control explicitly succeeds by joint reflection. [Named controls and adverse selections](../evidence/validation/D216_JOINT_POOLED_CLUSTER_REFLECTION/HAND_CONTROLS.md)

## 5. The selected mixed-quota 26-edge original

The selected named target is `[[1],[2,2,2],[2,2,3],[1]]`. The isolated interior clusters have 9 and 10 edges respectively, each with three positive branches. The pooled cluster has N=19 edges and six positive branches. All three are diameter-four rooted trees within the D215 application of Van Bussel's Theorem 4.5. Bare rooted existence supplies no compatible palettes by itself.

Here δ=4, so ρ(x)=23−x has only pairs. Since |M| is even and |R|=3 in either orientation, |E| is odd by the parity of symmetric difference. The reflected vertex palette must be even in size. Each quota-two branch contributes three vertices and the one quota-three branch contributes four. Any odd-size E without the quota-three branch has an odd-size palette, so every successful E contains that unique branch.

For a symbolic supply use donor `s:1` and reflect all three receiving branches. Thus E=R and M is empty. Reserve donor center labels 19,18 and c, with their partner coordinates 4,5,23−c as donor terminals along with 1,2,3. Take c≥12, distinct from 18 and 19, so the three partners are distinct and below all donor centers. All other eligible pairs belong wholly to the receiver. If C=19+18+c, the sum of the six donor terminal labels is 75−C and the sum of the nine donor differences is C+2C−(75−C)=4C−75. The pool weight sum is 190, so the receiver's ten distinct differences have sum 265−4C≥55. This forces C≤52 and c≤15 in this choice of donor pattern. Choose the largest such c=15. The receiver's sum is 57, and [1,9]∪{12} gives the desired total. For this choice the donor terminal difference palette must be {10,11,13,14,16,17}, after reserving its center weights 19,18,15.

The donor terminal labels are {1,2,3,4,5,8}. Use 19→8 for weight 11, and then 15→5,2 for weights 10,13. Use 19→3 for 16, and the remaining labels 1,4 at 18 for 17,14. This gives each donor host exactly two terminals.

The receiver alphabet is {6,7,9,10,11,12,13,14,16,17}. Use centers 6,7,12. Weight 12 is larger than the receiver alphabet span 11, so it is reserved at the root attachment. Take 12→17 for weight 5 at the quota-three host. Use 7→16 and 6→14 for 9 and 8. The four remaining labels 9,10,11,13 must realize {1,2,3,4} at 6,7,12,12. The label 13 realizes weight 1 at 12, and 6→9, 7→11, 12→10 then give 3,4,2. This supplies the required counts and difference set. The full center/terminal assignments and their actual named transports are recorded as the second positive hand control.

The receiver labels form pairs (6,17), (7,16), (9,14), (10,13), (11,12), and M=∅. Thus both conditions hold. Reflect all three actual receiving components and give them their final parent `s:2`. The literal shell edges fill [20,26] and the pool edges fill [1,19] after reconstruction. This hand construction decides the selected compatibility question positively. It is a specific mixed-quota witness, with no claim of independent arbitrary-quota supply. No scientific numerical consumer, dormant diagnostic, or future budget freeze is needed.

## 6. Retained mechanisms and strategic gate

[R248](../references/upstream/mdl/N248_component_palette_reflection.md) requires reflecting the whole selected component and moving it to the partner of its original host, using an invariant union of component labels. Within this two-port operation it is exactly the E=R specialization, with actual reflection sum 2A+N+δ. The selected 26-edge control in fact uses that specialization, whereas the 20-edge control also uses moves with unchanged coordinates and exchanges their attachment weights. Allowing arbitrary E and R requires the separate invariant palette at E△R. [D211](ORDINARY_SPINE_COORDINATED_FOUR_HOST_SUPPLIER.md) already balances weights jointly across host changes, and [D210](ORDINARY_SPINE_SIMULTANEOUS_ORDINARY_SUPPLIER.md) uses reflected terminal transfers. They allocate against independently supplied partial whole-original resources. The present proof balances whole branch label palettes and attachment weights around a separately supplied pool, with all internal differences fixed.

For E=∅ the partner condition on centers recovers the established pair and midpoint transfers at the two hosts. Mishra and Panigrahi's 2010 paper, Section 2, Definition 2.2 and Lemma 2.3, documents the component moves with unchanged labels and requires the new host to lie outside the moved components. Here both hosts are shell vertices outside the pool's off-spine components. [Mishra and Panigrahi, pp. 259–260](https://mbpapers.math.cas.cz/full/135/3/mb135_3_3.pdf)

The two conditions also give a sequential interpretation of the joint operation. First reflect and move all E by R248. Each original center pair of M lies entirely in E or entirely outside E, since invariance of P(E) pairs all selected labels inside P(E). Thus the corrective moves E∖R back to the donor and R∖E forward to the receiver each admit unchanged-label pair or midpoint transfers in their own direction. The first group is still invariant after its labels have been reflected. The joint operation and this composition agree on every final name and edge. This comparison makes no priority claim.

The alternative diameter-five-core route would retain both interior groups on their distinct actual parents and the literal edge between them. When both groups contain positive quotas, that core has diameter five and is ordinary graceful by the Hrnčiar–Haviar theorem. This gives core existence but does not specify the two attachment labels needed to reconstruct the exterior. [N145](../references/upstream/mdl/N145_retained_record.md) records the difference between the general theorem and its particular port-supplying case. A joint whole-original allocation like D210/D211 could avoid that independent port requirement, but its retained quota domains do not imply the present unbounded pair of interior lists. The relevant comparison is between these unproved supply or exterior-reconstruction premises and the present two-palette premise, beyond the common-quota family and the two fixed mixed-quota controls. [Hrnčiar and Haviar, primary publication](https://www.sciencedirect.com/science/article/pii/S0012365X00002338)

D214 and D215 establish a single-cluster composition. D216 resolves the selected compatibility question by supplying a pool. The held two-cluster obligation remains open for arbitrary independent quota lists. The 26-edge witness establishes that larger reflected components are feasible, and uses the established R248 specialization. The 20-edge witness separately exercises the extra freedom of E△R. Further isolated witnesses would leave independent variable-quota supply unproved. A future strategic choice should weigh that specific supply gap against the two-port exterior condition of the diameter-five route and the need for a comparable parameterized palette in the whole-original route. This is the third related rooted-cluster investigation since D214. Strategic reassessment is mandatory before selecting any subsequent task. None is selected here.

D212's theorem, all three INCOMPLETE D212 certificate questions, the held D212 closure, D213's structural bound and held insertion obligation, and deferred D207 remain unchanged.
