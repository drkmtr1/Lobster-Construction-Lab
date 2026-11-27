# D220 — Direct joint allocation with six fixed marks

**Disposition: PROVED WITHIN EXACT SCOPE.** The exact 30-edge folded source admits the six registered marks inside the retained D219 slot bands. Independently, the D218 seed and host order exclude sequential difference-preserving transfers even with arbitrary nested terminal sets, on the all-quota-two family for every h ≥ 5. [Named original, folded source and hand control](../evidence/validation/D220_DIRECT_JOINT_FIXED_MARK_ALLOCATION/HAND_CONTROLS.md).

## 1. Registered question

Fix the original T with profile `[[2],[2,2],[2,2,2,2,2],[2]]`. Its four spine vertices, nine centers and eighteen terminals give 31 vertices and 30 edges. Form S by changing only the two exterior center attachments inward as in D217. Both are trees: each original branch component is attached by one edge to a retained spine, and each terminal stays at its actual center. The hand record specifies both named incidence sets before assigning labels.

In the order (s:1, s:2, s:0, s:3, b:0:0, b:3:0), the registered labels are (0,30,29,5,2,3). The two replaced source weights are 2 and 27, and their restored weights are 27 and 2. This is the D217 joint exchange with every label fixed. Ordinary gracefulness of T follows from a marked positive on S. The fixed marks are an additional supply condition.

## 2. Arbitrary nested subsets in the D218 transfer order

In the all-quota-two D218 family there are 2h−1 positive hosts and 4h−2 terminals. The two reserved spine-end leaves carry no terminals. Hence m=6h and the initial active terminal palette is P₀=[h+2,5h−1]. Every host in the prescribed order lies outside P₀. The first nine hosts are 1, m−2, 2, m−3, 3, m−4, 4, m−5, 6. For h=5 the last of these is the final host, and for h>5 it begins the remaining alternating pairs. Consecutive hosts in the eight steps alternate sides of P₀.

At a step from v to w, each moved terminal keeps its label z, loses its edge to v and gains an edge to w. All other edges and labels are unchanged. With v below P₀ and w above it, the old moved weights are z−v and the new ones are w−z, each injective on the moved set X. Equality of the two multisets is equivalent to X=(v+w)−X. When v is high and w is low, the same equivalence follows by interchanging the old and new expressions. In a graceful intermediate tree these weights must agree because the complement of the moved edges is unchanged. Thus the moved set lies in the invariant intersection J=P ∩ ((v+w)−P), and must have cardinality |P|−2 to meet the departing quota. These constraints apply to arbitrary subsets of P.

The sums in the first seven steps alternate m−1,m, starting with m−1. The eighth sum is m+1. The table uses closed integer intervals with reversed endpoints denoting the empty set. Each row uses the preceding moved palette as P.

| Move | Intersection J | Forced movement |
|---|---|---|
| 1 → m−2 | [h+2,5h−3] | All of J |
| m−2 → 2 | [h+3,5h−3] | J minus 3h |
| 2 → m−3 | [h+3,3h−2] ∪ [3h+1,5h−4] | All of J |
| m−3 → 3 | [h+4,3h−2] ∪ [3h+2,5h−4] | All of J |
| 3 → m−4 | [h+4,3h−3] ∪ [3h+2,5h−5] | All of J |
| m−4 → 4 | [h+5,3h−3] ∪ [3h+3,5h−5] | All of J |
| 4 → m−5 | [h+5,3h−4] ∪ [3h+3,5h−6] | All of J |
| m−5 → 6 | [h+7,3h−4] ∪ [3h+5,5h−6] | Impossible |

For an interval [l,u], reflection in sum s gives [s−u,s−l]. After the first step the reflection in sum m has intersection [h+3,5h−3], losing only one label of P. Exactly one more must be omitted from this invariant intersection. Its only singleton orbit is the midpoint 3h, so the omission is forced. From then on the two bands straddle half the relevant reflection sum, and the reflected bands exchange sides. The intersections in rows 3 through 7 therefore come from pairing opposite bands under reflection. Each of these rows, and the first row, loses exactly two labels of P. At h=5 the first seven palettes are still nonempty. In the eighth row the reflected high and low bands are respectively [h+7,3h−2] and [3h+5,5h−4]. The incoming bands each have length 2h−8. Each intersection band has length 2h−10, so four labels must stay behind, exceeding the quota of two. At h=5 the eighth intersection is empty and the final host still requires two labels.

This excludes the specified sequential architecture with the D218 initialization, marks, host order and per-step weight preservation. It holds for arbitrary choices of nested terminal sets in that architecture. It leaves direct joint allocation available. The Director’s flexible-mark observation for even h≥6, with marks (0,m,m−1,h+1,h/2,h/2+1) and reserved leaves m−1 and h+1, remains held and untested here.

## 3. Full fixed-mark skeleton reduction

For m=30, let C_L and C_R be the distinct numerical labels at the slots attached to the spine roots 0 and m in S. Slots include the respective spine-end leaves as well as branch centers. Their fixed memberships include 29 and 2 in C_L, and 5 and 3 in C_R. The seven remaining slots are the two left and five right interior centers. The central spine edge has weight m. The other skeleton weights are the labels in C_L and the values m−z for z in C_R. The separate maps are injective and all weights lie in [1,m−1]. Distinctness across the two maps is therefore equivalent to C_L ∩ (m−C_R)=∅. With W=C_L ∪ (m−C_R), the remaining labels and weights are respectively

```text
R = [1,m−1] minus (C_L union C_R)
D = [1,m−1] minus W
```

Each has size eighteen on the registered skeleton. This criterion is sufficient for an injectively labeled skeleton with distinct weights. Full gracefulness also requires the residual allocation.

For any orbit {z,z′}, where z′=m−z and z′≠z, choosing both as slot labels on opposite sides collides at one weight. Choosing both on the same side consumes both coordinates in both inventories. Choosing neither leaves both coordinates in both inventories. Choosing only z on the left leaves z′ as both a label and a difference. Choosing only z on the right leaves z′ as a label and z as a difference. The midpoint m/2, when integral, uses its own coordinate in both inventories on either side if selected. Otherwise that coordinate remains in both inventories.

The pins leave 25 possible slot labels for the interior centers. Before collision pruning, the number of unordered side assignments is binom(25,2) binom(23,5)=300 × 33,649=10,094,700. Each permutation of complete quota-two interior arms within the same physical section acts as an automorphism of S and T and fixes all marks. The map takes the actual center and its two leaves to the corresponding named vertices of the destination arm. Interchanging the two leaves at any center also fixes the graph. Thus any lawful labeled witness can be transported to assign the interior center labels in increasing order within each section and the two leaves in increasing label order at each center. This preserves existence and gives a lift to actual names. The skeleton-choice bound is separate from the number of named labelings.

## 4. Nested domains and the fixed-band moment

Arm A selects the retained slot bands [1,6] ∪ [25,29]. With 29 and 2 on the left, their complementary labels 1 and 28 must also be on the left. This fills all four left slots. Accordingly the unique side assignment in this band gives

```text
C_L = {1,2,28,29}
C_R = {3,4,5,6,25,26,27}
W   = [1,5] union [24,29]
R   = [7,24]
D   = [6,23]
```

Arm B contains every other lawful skeleton. Excluding the exact pair (C_L,C_R) of Arm A from Arm B makes these disjoint and exhaustive over the registered skeleton domain. An interrupted allocation or skeleton traversal alone cannot establish exhaustion. The positive below settles existence without entering Arm B.

Write i=z−7 for a terminal label and w=d−6 for its weight. Both alphabets are [0,17]. The five lower hosts k=1,2,3,4,6 give w=i−(k−1), because they are below every terminal. The four upper hosts 30−k for k=2,3,4,5 give w=17−k−i, because they are above every terminal. Each host needs two terminals. The sum of the low-host offsets is 2(0+1+2+3+5)=22. The sum of the high-host intercepts is 2(15+14+13+12)=108. If B is the sum of the eight high-host terminal indices, then summing w over all terminals gives 153−B−22+108−B. Its required value is 153, so B=43. This necessary identity is specific to Arm A's bands and host quotas. The constructive control verifies the entire inventory in addition to this identity.

## 5. Exact joint-allocation representation

For a supplied lawful skeleton, use one tagged column per actual terminal host, each unused label, and each unused difference. The 9, 18 and 18 columns are disjoint even when a numerical label equals a numerical difference. For each named host with label a and each pair z₁<z₂ in R, form a row on the host, both labels and both actual differences |z₁−a| and |z₂−a| if the differences are distinct members of D. No host or support symmetry is required. There are at most 9 binom(18,2)=1,377 row attempts per skeleton.

A completion partitions its terminal edges by host. Each pair yields a legal row, and bijection and gracefulness cover each tagged column once. Conversely, a cover chooses exactly one row at each host, partitions R and D, and installs the two labels in increasing order at the two original terminal indices. This yields a graceful labeling of S with all six marks. The two-edge exchange then recovers a graceful T.

An exact finite traversal, if needed, represents each row by the bits for its five columns. From the currently uncovered column set, choose a column with the fewest compatible rows whose masks are contained in the uncovered set. With no compatible row this branch is impossible. Otherwise branch over exactly those rows and remove the chosen mask. Every cover must choose one such row, and every complete descendant extends that choice without overlap. Empty uncovered set is success. Every branch removes a host, so the induction terminates after at most nine chosen rows. This describes the equivalence and a complete algorithm mathematically. The symbolic positive required neither an implementation nor any traversal.

## 6. Direct allocation and scope

In normalized coordinates, weight 17 forces index 17 at host 1. Then weight 16 forces index 16 there. Weight 15 now forces index 0 at host 28. Assign the pair of smallest weights 0,1 to host 6 using indices 5,6. Use indices 3,4 at host 25, and place indices 15,1,2 at hosts 2,27,26 respectively. This accounts for weights 14,13,11 at the last three placements and reserves the smaller unused differences for the joint allocation.

The remaining indices 7 through 14 can be placed together in the order 14,13,12,11,10,7,9,8 at hosts 3,4,27,28,26,2,3,4 respectively. They realize weights 12,10,2,4,3,6,7,5, exactly the unused weights. The hand record gives the full named result and separate actual spectra. The eight high-host indices sum to 43. The construction keeps the skeleton and completes both inventories simultaneously. For example, host 1 retains labels 23 and 24 in the joint certificate. The first forced sequential departure would retain 23 and 24 as well, but its next departure would retain 7 and 15 at host 28, whereas the joint certificate gives host 28 labels 7 and 18. The decisive difference is that a final joint assignment need not honor any sequence of intermediate per-step invariants. The fixed-band positive and the sequential exclusion concern different solution sets.

Retained [R226](../references/upstream/mdl/N226_R226_two_host_completion.md) starts with an independent labeled core and two actual hosts, and uses difference-graph balance and forced choices with reflected pairs and a possible midpoint to characterize attainable quotas. [R232](../references/upstream/mdl/N232_R232_joint_allocation.md) coordinates physical quotas across supplied disjoint paired palettes, subject to local balance and its singleton-forest premise. Here all nine hosts compete for the same two inventories, without prescribed batches or a two-host factorization. [N240](../references/upstream/mdl/N240_resource_algebra_counting.md) similarly enforces both resource inventories, using square-free label and difference factors indexed by actual vertices and incidences. The tagged rows are an exact support representation for this fixed skeleton and two leaves per host. Support equivalence alone gives no existence guarantee. The actual positive here comes from the displayed arithmetic assignment.

D217 supplies the exact two-edge reconstruction. D218 and D219 supply marked sequential constructions on their retained domains. D220 supplies this one marked original by direct joint allocation and excludes the specified all-quota-two transfer order for all h≥5. The certificate gives no general fixed-band supplier, no general all-quota-two marked existence theorem and no conclusion about alternative architectures from the transfer obstruction. No larger target, dormant diagnostic, solver, scientific module, original-target checker or numerical discovery was used.
