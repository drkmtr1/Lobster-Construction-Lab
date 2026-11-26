# D201 — Expanded-exterior multi-host residue-packet classification

Task LCL-ORDINARY-SPINE-EXPANDED-EXTERIOR-MULTI-HOST-RESIDUE-PACKETS-001. The general expanded shell preserves the exact D200 palettes after normalization. The step-four, step-six and relocated cases have necessary and sufficient packet-capacity tests on the prescribed original parents. In these cases, the surplus-source residue contributes a forced path, and every other nonidentity component is a consecutive cycle packet. The criterion supports arbitrary finite additional-host multiplicity with independently prescribed additional quotas.

Intervals below are inclusive integer intervals. All sizes, labels, indices, quotas and packet counts are exact integers.

## 1. Expanded shell and physical resources

Take an independently supplied graceful N-edge named prefix in minimum orientation at frontier 0. Retain its actual witnessing spine. Use D200's independently admitted three cut coordinates r<t<N−1, distinct safe thresholds D_r,D_t≤N−2, and D_(N−1)=N−1. Let u=min(D_r,D_t), v*=max(D_r,D_t)+1, and let the numerical D200 lower roles {h,J0}={r+1,t+2} satisfy 4≤h,J0≤K0−1. Choose {α,β}={u,v*} and σ in {−1,+1} as in D200. With M0=N+K0, require c0=M0−α and l0=c0+σβ in [N+2,M0−3]. Here “admitted shell” means these geometric premises. Its base residual allocation is still to be supplied with the expanded host menu.

Let A≥1, d=A−1, K=K0+d and M=M0+d. The upper exterior has width one. The increasing old map is

    E(x)=A+x+1_(x≥r)+1_(x≥t)+(K0−4)1_(x≥N−1).

Its old labels are ([A,N+A] minus {d+r+1,d+t+2}) union {M−2,M−1}. Its old weights are ([1,N] minus {u,v*}) union {M0−3,M0−2}. The former is D200's exact label partition shifted by d. The latter follows from the safe-supported old rank formula and is independent of d, because translation leaves every endpoint subtraction unchanged. The fresh label palette is [0,A−1] together with the two low unit gaps, the long gap [N+A+1,M−3], and {M}. The fresh weight palette is {u,v*}, [N+1,M0−4] and [M0−1,M]. The ranges are disjoint, including the cases A=1 and empty additional-host menu.

Put the actual new spine vertex at M. The first four original children in order are at d+h,d,d+J0,d+c0, with the designated original terminal of the fourth child at d+l0. The connector uses actual frontier E(0)=A and weight M−A=M0−1. The four child weights in order are M0−h,M0,M0−J0,α. The designated terminal weight is β. Put the A−1 actual additional children at 0,...,A−2 in increasing order of physical label. Their actual attachments have weights M,M−1,...,M0+1, and intersect no other weight family. With A=1 the exact D200 order remains.

For a finite set J of distinct positive indices, set max J=0 if empty, require A≥1+h max J, and assign additional child j at d−hj the actual quota t_j≥1. These labels are distinct in [0,A−2]. Every other additional child is an actual direct leaf. Set T=Σ_j t_j. The actual quotas at the first two children are p,q≥1 and the third child is a direct leaf. There are A+3 actual children and p+q+T+1 terminals. Including the connector gives K=p+q+T+A+5, so K0=p+q+T+6. No original ancestry or ordering changes.

At C=N+A+1, the old lower vertices are exactly those with original labels x<N−1, and the old crossing weights are M0−3,M0−2. All lower child attachments, every additional child attachment and the connector cross. The upper child's attachment and its one terminal are noncrossing with weights α,β. All residual parents are strictly lower and all residual terminal labels are upper. For an actual terminal label x, write y=x−d. Its differences to the actual neutral, principal and additional parent j are respectively y, y−h, y+hj. Each is positive by actual endpoint order. In particular the actual weight is the indicated normalized target coordinate, with no translation of weights. The two remaining palettes are

    R=[N+2,M0−3] minus {c0,l0},
    Q=[N+1,M0−4] minus {M0−h,M0−J0}.

Actual free labels are d+R, and actual free weights are Q. They each have size K0−6=p+q+T. The designation of residual parents and all crossing flags are now fixed. A bijection into Q gives exactly the correct differences and consumes every used and free resource. Old and fresh labels split physically by C as above, with the unused labels all upper. Old and fixed fresh weights split at N+1, and the unused weights all belong to the crossing band. Completion therefore gives crossing [N+1,M], noncrossing [1,N], frontier M and physical cut C. Complement at M to get frontier 0, cut M+1−C=K0−1, all sides reversed and identical actual weights and crossing flags. The returned state is P(M,K0−1,N+1). Under the D157 strict definition this is strict precisely for A=1 and K0=N, since D−c=2 then requires K0=N and the even-size relation then forces A=1.

## 2. Directed components and exact packet extraction

Use vertices R union Q and one arrow y→f(y) for each residual source. Any completed allocation has indegree 1 exactly on Q and outdegree 1 exactly on R, including identity loops. Hence distinct components of this finite directed graph are paths or cycles. With one unmatched source and one unmatched target there is exactly one path, oriented from R minus Q to Q minus R. All other components are cycles. This follows by following the unique outgoing arrow from the unmatched source: a repeat would give a previously visited vertex a second incoming arrow, or return to the source with its forbidden incoming arrow. The resulting path must end at the unmatched target. Any remaining vertex has both degrees one.

All arrows preserve residue modulo h. In that residue scale differences by h, so allowable increments are 0,−1,+j. If the unmatched source is the largest available coordinate in its residue and the target the smallest, the first step cannot go upward or stay in place. Inductively the visited coordinates form a consecutive upper interval whose current position is its bottom. Every positive jump lands in that interval or beyond the available maximum. An identity would repeat the current coordinate. Thus only the next down-step is possible until the target is reached. In this assertion, a missing intermediate coordinate would preclude a successful path. The cases below have every such coordinate present. The forced path occupies that entire residue in the two templates.

For a nonidentity simple cycle, begin at its maximum. The first arrow is −1. All arrows before the first positive jump are consecutive unit descents, since an identity cannot occur in a longer cycle. The first positive jump lands at or below the maximum and above the current coordinate, so it hits a visited vertex. Simplicity permits this only at the starting maximum, closing the cycle. A cycle with positive increment +j has exactly j negative steps and j+1 consecutive positions. Conversely on any j+1 consecutive available positions in a residue, assign the lowest source to host j (the positive jump to the top) and every other source to the principal host (the preceding coordinate). This is the exact packet. Identity loops at the neutral host account for every available position outside the path and these packets.

Both templates have each nondistinguished residue equal in sources and targets and contiguous in its residue coordinates, including the possible top truncation in the relocated shell. Thus their capacity criterion holds in both directions. For each spare residue k of capacity c_k, let u_(j,k) be its number of type j packets. Then

    u_(j,k)≥0 integral; Σ_k u_(j,k)=t_j; Σ_j (j+1)u_(j,k)≤c_k.

Necessity follows from vertex disjointness and the exact cycle classification. For sufficiency, order residues and host indices increasingly, and consecutively place the prescribed number of packets starting at each residue's lowest coordinate. A capacity inequality fits the whole block of each type. The rest of the common coordinates are identities. Saturation leaves zero identities in that residue. Empty capacities, empty J and sparse host indices require no separate shift types. An exact deterministic finite count allocator can order the entries by residue then host index, enumerate the finite integer intervals [0,t_j], and return the first matrix satisfying the displayed equations and inequalities, or prove the fixed test fails if all matrices are rejected. This defines an arithmetic extraction; no packet search or solver was executed. The frozen positive controls provide their given matrices explicitly. Sorting actual labels within each physical host gives exact distinct terminal indices. Each packet contributes one actual terminal at host j and j at the principal host. The global quota moment, obtained by summing source minus target, is h(p−Σ_j j t_j).

## 3. Size-independent step-four and step-six placements

Use cuts 3,4 with thresholds 1,2 in either order, and the safe top cut N−1. Let (h,J0) be (4,6) or (6,4). Put c0=M0−3,l0=M0−4, with α=3, β=1, σ=−1. The shell leaves

    R=[N+2,M0−5],
    Q=[N+1,M0−5] minus {M0−6}.

In this range the geometric lower bound K0≥7 is satisfied, and the actual quotas require K0≥8. The sum difference is (M0−6)−(N+1)=K0−7. Write P=p−Σ_j j t_j. Equality requires P≥1, K0=hP+7, and gives

    p=P+Σ_j j t_j,
    q=(h−1)P+1−Σ_j (j+1)t_j.

Below, identify the base N+1 as coordinate 0. Then R occupies 1,...,hP+1, Q occupies 0,...,hP+1 except hP. The unique distinct source is hP and distinct target is 0. This residue is exhausted by the P-step descending path of §2. Relative residue 1 has capacity P+1, and residues 2,...,h−1 have capacity P. Their sum is (h−1)P+1. The packet inequalities are thus exact, including the independent positivity of q: the unused total capacity equals q, and the negative-arrow total is precisely p. Distinct assignments yielding the same counts need not coincide, and no named-labeling count is claimed.

A simple sufficient condition is Σ_j (j+1)t_j≤P+1 and q≥1. All packets then fit in residue 1. For any finite J and independently given positive t_j choose P large enough for this inequality and q≥1, and choose any integer A≥1+h max J. This determines the coupled p,q and actual fresh child/terminal inventory. At A=1 and J empty, the exact D200 step-four and step-six roles are recovered. At N=K0 as well, the step-four case is D199.

## 4. Expanded relocated placement

Set h≥4, N≥h+3, and assume actual safe coordinates (r,D_r)=(h−1,h−3), (t,D_t)=(h+1,h−1) and (N−1,N−1). The roles are h,J0=h+3. Take α=h, β=h−3 and σ=+1, giving c0=M0−h and l0=M0−3. The geometry requires K0≥h+4, from J0≤K0−1, and this bound admits both upper designated labels and child roles. The exact residues are

    R=[N+2,M0−4] minus {M0−h},
    Q=[N+1,M0−4] minus {M0−h,M0−h−3}.

At K0=h+4 the weight omission M0−h−3 equals N+1. The sets agree, and relative to N+1 the coordinates are 1,...,h−1 with 3 absent. Each residue has at most one point. Hence all arrows are identities at that boundary, excluding p≥1 even if positive-shift quota could have balanced the global moment. For the remaining geometric range the sum difference is K0−h−4. Equality to hP with P=p−Σ_j j t_j gives

    P≥1, K0=h(P+1)+4,
    p=P+Σ_j j t_j,
    q=(h−1)P+h−2−Σ_j (j+1)t_j.

Relative to N+1, sources are 1,...,hP+h−1 except hP+3. Targets add 0 and omit hP. The unique zero-residue path again consists of P consecutive descending steps. Residue 3 lacks its top position, yielding capacity P. Residues 1,...,h−1 other than 3 have capacity P+1. The proof includes h=4, where residue 3 is the last nonzero residue and its top is the last possible source. These capacities sum to (h−1)P+h−2. The test of §2 with these capacities and the displayed equations is necessary and sufficient within this exact placement. This includes empty J, saturated individual residues and both physical polarities. One can again choose a sufficiently large P and place all packets in residue 1 when an admitted relocated prefix is fixed.

## 5. Independent supply and source comparison

The reversed-threshold D199 one-center seed supplies the step-four and step-six cuts for N=4P_seed+7, P_seed≥1, by putting its actual root at zero, center at 4, its three terminals at 1,2,3 and actual direct leaves at [5,N]. D199's independent nonnested Family C also supplies those cuts at the same N, with spine (2,4,1,7,0), first children at 3,6, last children at {5} union [8,N] and three empty interior sections. For Family C, the internal edge weights 1,2,3,4,5,6,7 are all used once by those original spine and low-leaf edges. For N=11 the actual thresholds at cuts 3,4,10 are 1,2,10; the first two cross all old ranks or all except 1 as stated. This fixed eleven-edge graph can be used for an unbounded number of additional positive receiving centers and any independently prescribed collection of their positive quotas. The old cut conditions and original ordered receiving roles stay fixed, while the required actual direct leaves, A and the coupled p,q belong to each respective new original. No bound comparing old size and fresh size is needed.

[R226](../references/upstream/mdl/N226_R226_two_host_completion.md) gives exact forced components, reflected pairs and quota accounting for two supplied hosts. In the one-sided zero/−h restriction it is the same forced residue allocation as D200. [R232](../references/upstream/mdl/N232_R232_joint_allocation.md) combines already reserved two-host palettes using singleton-forest parity and pair capacities. Its physical-host quota custody is directly relevant. The present capacities are sizes of coordinate residues, and a type j cycle uses one +hj token and j actual −h tokens within one residue. They are derived from a single global pair of palettes and differ from R232's orientation and incidence conditions on preassigned two-host batches.

[D136 §2](ORDINARY_SPINE_INTERLEAVED_ROTATION_PACKET_ALLOCATION.md) gives exactly the same packet on scaled coordinates at a=j,b=1, namely the bottom jump by j and each other coordinate stepping down by one. Its residue decomposition and physical token bookkeeping are applicable comparisons, as are the signed unit-sided sufficient packets and per-band moment in [D196 §3](ORDINARY_SPINE_GENERALIZED_ONE_SECTION_CUT_SPECTRUM.md). The simple-cycle necessity here uses the specific one-unit negative direction and the declared one-sided alphabets. [D165](ORDINARY_SPINE_EXCEPTIONAL_FOUR_FIRST_CENTER_PARITY_CHAIN.md) supplies step-two hole paths, [D166](ORDINARY_SPINE_EXCEPTIONAL_FOUR_FIRST_CENTER_EIGHT_DEFECT.md) gives their exact directional recurrence, [D167](ORDINARY_SPINE_EXCEPTIONAL_RESERVATION_SEMILINEAR.md) gives anchored finite types and reversible path growth, and [D168](ORDINARY_SPINE_EXCEPTIONAL_TWO_UPPER_HOST_RESIDUE_COMPRESSION.md) gives arbitrary-step residue paths and compression. Those two-host path similarities apply to the distinguished residue. Extra positive arrows in D201 are accounted for by all the cycles proved in §2. The literature obligations and prior pinned shell proposal retain their existing scopes. No historical novelty is asserted.

## 6. Inheritance and immutable composition

For a physical maximum-output cut C' in [A+max(h,J0),N+A+1], let b be the number of old labels E(x) below C'. All fresh lower attachment roles and the connector's old endpoint lie below C'; all residual terminals, upper center and its terminal, and the new frontier lie at or above C'. Thus fresh crossing weights are exactly [N+1,M] minus {M0−3,M0−2}. The induced b is a proper old cut. The two omitted old high weights must cross, and the two supplied low holes u,v* cannot cross. Among the other old ranks, the old increasing weight map adds 2 at and after max(D_r,D_t), up through N−2. It has weight v*+1 at max(D_r,D_t). Therefore C' is safe exactly if b is old-safe with max(D_r,D_t)≤D_b≤N−1. The threshold is D_b+2 for D_b≤N−2 and N+1 for D_b=N−1. Conversely these conditions supply the missing high weights and an exact consecutive tail above v*. This is D200's inheritance test with the physical cut corridor translated by A−1. It holds independently of the placement of the packets within their residues. Cuts outside this corridor can depend on individual packet placement. The proof gives no universal renewal or decomposition.

The increasing old map is E for a minimum input and M−E(N−x) for its complementary actual input. The latter gives physical minimum output with cut M+1−C. These maps preserve each old vertex and literal incidence and use the actual old-side split x<N−1 in minimum coordinates for this step. Compare each endpoint's new side to its actual stored incoming cut. The exact added weight of any old edge with original ordered labels a<b is Σ_(a<r_i≤b) g_(r_i), for the three local thresholds r_i and widths g_(r_i); the offset A cancels. The physical complementary orientation has the same weights. In particular, edges whose actual cut memberships change are handled by named endpoint subtraction. One common increment for old crossing edges would lose information when the cut repartitions.

For consecutive admitted steps, compose the actual increasing integer maps. A step threshold pulls back to the least earlier input coordinate where the preceding map meets it, if such a coordinate exists. Coincident pullbacks add widths, and thresholds already satisfied at the minimum coordinate contribute to the offset. This is the finite D198 transport. Freeze the topology and the local coordinates at each vertex's birth. Apply all subsequent maps to those coordinates when making the final write-once label assignment. For any original boundary use the image of its named vertex set and subtract its named edge endpoints in the final alphabet. Its complement supplies remaining label and weight inventories, including both physical cut partitions and actual literal connectors. Finite boundary count and finite local extraction give termination.

For F, retain the exact D200 strict control ending at maximum 86, physical cut 45. Its 43-edge incoming prefix has actual safe direct-tail cuts h_old=32,34 with thresholds equal to their coordinates. D200's corridor gives physical maximum cuts h_old+3 with thresholds h_old+2, respectively (35,34),(37,36). The actual terminal-free section with two direct leaves takes maximum input to minimum output by shifting old labels by 1, placing its actual new frontier at 0 and actual leaves at 89,88 in original child-index order. The safe-cut update yields (36,34),(38,36),(88,88), with N=89. The transported working cut is 46 and threshold 44. Thus the next shell uses h=37, A=38, P=1, K0=78, p=2, q=69. Its chain is 127→90 and its residue-1 packet is 91→128→91. The final physical maximum cut is 128, the crossing spectrum is [90,204], and its complementary cut is 77. It returns P(204,77,90).

Let E_1,E_2 be the exact D200 maps of its first and second multi-gap lifts, and E_3(x)=38+x+1_(x≥36)+1_(x≥38)+74·1_(x≥88) be the expanded map in F. In actual original boundary coordinates at sizes 15,30,43,86,89,204, the maps to the final maximum output are respectively

    x ↦ E_3(E_2(E_1(x)+1)+1),
    x ↦ E_3(E_2(x+1)+1),
    x ↦ E_3(E_2(x)+1),
    x ↦ E_3(x+1),
    x ↦ E_3(x),
    x ↦ x.

For the initial prefix and first shell's boundary the two new low thresholds and the new large threshold are above all inputs of E_3, so these two final maps equal their D200 final maps plus 39. At the 43-edge boundary the new low thresholds pull back to 32 and 34 in that boundary's labels. At size 86 they pull back to 35 and 37, with no large-gap pullback there. At size 89 both last actual direct leaves cross the large threshold. The initial prefix's final map is 42+x with D200's steps at 3,4,8,10,14 of widths 1,1,1,1,11. The complementary map for each size m0 is x↦204−F_m0(m0−x) for the listed maximum-side F_m0. The five final maximum connector pairs are (42,73),(73,40),(40,127),(127,38),(38,204). The frozen evidence records exact final incidence weights and used/remaining label and weight cuts at every original boundary.

## 7. Fixed original controls and scope

| Control | Exact result |
| --- | --- |
| A. Retained D199/D200, N=15 | A=1, h=4, P=2 and J empty. Exact 30-edge original, all old and outgoing named labels and actual edge rows retained. |
| B. Family C, N=11 | The path is 24→20→16→12. Residue-1 packets at 13,17 and 21,25 and a residue-2 packet at 14,18,22 use lengths 2,2,3. No capacity exceeds 4, so these packets cannot all occupy one residue. Maximum cut 21, crossing [12,38], return P(38,18,12). |
| C. Family C, N=11 | The valid fixed partial placement has A=13 and K0=15. R=[13,21], Q=[12,21] minus {20}. Both sides of the moment equal 8. Capacities (3,2,2) exclude the one required length-four packet. |
| D. Swapped role, N=11 | Path 18→12 and packet 13→19→13. Maximum cut 19, crossing [12,30], return P(30,12,12). |
| E. Small relocated, N=8 | The independent actual (2),(),(),(0,0) prefix supplies the three cuts. Capacities (2,2,1), path 13→9 and packet 10→14→10 give maximum cut 14, crossing [9,24], return P(24,11,9). |
| F. D200 composition plus an actual terminal-free section and expanded shell | 15→30→43→86→89→204. Final maximum cut 128, crossing [90,204], noncrossing [1,89], return P(204,77,90). |

The fixed partial C palettes and incidence cuts are verified in both orientations. Its negative concerns this shell and these fixed roles. The relocated P=0 exclusion also concerns its exact geometric boundary. General compatible fresh-parent supply with arbitrary quotas, arbitrary positive-terminal closure, and original-spine decomposition remain open. Closed D191, D197 and D198 numerical lanes, D198's unclassified fixed minimum-input branch and all historical dispositions are preserved. The proof and evidence use symbolic reasoning and prescribed named arithmetic with zero labeling search, solver states, original-checker invocations, campaign execution and historical replay.
