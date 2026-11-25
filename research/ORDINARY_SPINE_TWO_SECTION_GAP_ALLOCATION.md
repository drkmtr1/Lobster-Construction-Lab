# D144 — Physical gap-leaf quotas for the D143 two-section return

Task `LCL-ORDINARY-SPINE-TWO-SECTION-GAP-ALLOCATION-001`. All sizes, labels and quotas are exact integers, excluding booleans. All intervals are inclusive, with reversed intervals empty. Write ⊔ for disjoint union.

## 1. Scope

Use the accepted [D143 construction and reduction](ORDINARY_SPINE_TWO_SECTION_CUT_STATE.md), including its exact D134 p=1 incoming state, witnessing spine, and named original prefix. Orient its actual extreme frontier v to zero, set n=2c+2 and d=c+2, and require the crossing spectrum [d,n] at cut c. Two actual sections add spine vertices u,w, with H=2K new vertices and edges and n≥2K. Fix lower and upper exterior sizes A≥2, B≥1 and gap size s≥K, with A+B+s=2K. Prescribe the reduced exterior tree and its graceful labeling as in D143 Section 3, independently of gap allocation. The old frontier v at reduced label A is ineligible as a gap host. Each fresh exterior vertex has a fixed numerical role and a prescribed quota of named gap leaves, zero when ineligible. The quota vector is given before allocation and sums to s. Each supplied leaf is an actual direct leaf or terminal with its declared physical host. Its section, branch and terminal indices are part of the input. No graph, incidence or exterior label changes during allocation.

Write k=K−A and g=s−K, so that K=A+B+g, k=B+g and s−k=A+g. The gap source alphabet is [0,s−1] split at k, and each source i takes the full label A+c+i. The required difference coordinates partition [0,s−1] at K. At lower exterior host j∈[0,A−1] let a_j=A−2−j; its image is i+a_j. At upper exterior host of reduced label A+b with b∈[1,B], the image is s+b−i. The absolute edge weight in either case is d plus the image. D143 requires one use of each source and image, with image at least K exactly on an actual crossing.

Sections 2–3 give necessary conditions throughout this declared class. Sections 4–6 give a deterministic sufficient quota rule, including a standalone family of suitable named exteriors for arbitrary A≥2 and B≥2. Rejection by the sufficient rule alone leaves other allocations open.

## 2. Aggregate crossing balance

Let L and U sum the supplied lower and upper host quotas. Let x count lower sources assigned to upper hosts, and y count upper sources assigned to lower hosts. These are exactly the two types of crossing incidence, because exterior sides are fixed and gap endpoints are split at k. Hence x+y=g. In a successful allocation the k lower sources supply k−x lower hosts, and the s−k upper sources supply y lower hosts. They also supply x and s−k−y upper hosts, respectively. Thus

    L=k−x+y=B+2y,
    U=s−k−y+x=A+2x.

In particular 0≤x,y≤g, B≤L≤B+2g and A≤U≤A+2g. The respective parities are those of B and A. Conversely, for nonnegative aggregate quotas summing to s, the lower bounds and parities give unique nonnegative integers x=(U−A)/2 and y=(L−B)/2 with x+y=g. They respect the source capacities k=B+g and s−k=A+g. This converse establishes only aggregate counts.

## 3. Physical constraints and adverse control

The exact source windows for an individual host and incidence type are below. Denote a_j by a in the lower-host rows.

| Physical host | Source side | Eligible i |
|---|---|---|
| Lower j | Lower | [max(0,−a),k−1] |
| Lower j | Upper | [K−a,min(s−1,s−1−a)] |
| Upper A+b | Lower | [b+1,min(k−1,g+b)] |
| Upper A+b | Upper | [max(k,g+b+1),s−1] |

For a lower source at a lower host, the maximum image is k−1+A−2=K−3. A valid such image is noncrossing and its lower bound is attained exactly when i+a≥0. On the upper side a lower host must reach K and stay below s; K−a≥k+2 so the stated window already lies entirely on that side. At an upper host, s+b−i≤s−1 requires i≥b+1, and its value is always at least b+1 for i≤s−1. For a lower source crossing requires i≤g+b, and for an upper source noncrossing requires i≥g+b+1, which already implies i≥b+1. These arguments prove every endpoint, including g=0.

In particular i=k has no eligible lower host. At an upper host it can be noncrossing only for b≤B−1, since k=B+g. Therefore B=1 is impossible, regardless of quotas or the supplied exterior. The top-index upper host b=B and the lower host j=A−1 each have at most max(0,g−1) crossing assignments. Every other host has at most g crossing assignments. These bounds follow by taking the lengths of the crossing windows. They do not guarantee compatible joint use of named hosts.

There is also a necessary parity test beyond the aggregates. Let l_j and u_b denote the given host quotas and let T be the sum of coordinates of sources assigned to upper hosts. A bijection has sum of image minus source equal to zero, so

    sum_j a_j l_j + sum_b (s+b) u_b = 2T.

The left side must be even. The source windows impose further constraints on T.

At A=2 the lower hosts are w at j=0, with zero translation, and the host at j=1, with translation −1. Since no upper host admits either i=0 or i=1, i=0 must use w. Assigning i=1 to j=1 would then repeat image zero, so i=1 must also use w. Thus l_0≥2 throughout this A=2 class.

For an adverse symbolic quota family use the actual five-vertex D143 exterior at A=2, B=3, with K≥5 and s=2K−5. Supply l_0=1 and l_1=s−3, with upper quotas (1,0,1) at u,b_2,b_3. These are nonnegative quotas of actual direct leaves and terminals, on the same predeclared exterior tree. Their total is s. They meet the aggregate identities with x=0 and y=g, and meet the parity test since s is odd and (s+1)+(s+3)−(s−3)=s+7 is even. The forced first two sources make completion impossible. This proves that aggregate feasibility, even with the global parity test, fails to settle physical compatibility in this embedding.

## 4. A deterministic sufficient rule for prescribed quotas

Take B≥2 and let j_0=A−2 be the zero-translation host and j_−=A−1 the host of translation −1. Reserve the low exterior part of the source alphabet

    I_0=[0,1] ⊔ [g+2,k−1]

for j_0, supplying the same differences. Here exterior part refers to the part outside the paired intervals of gap coordinates. The set I_0 has B coordinates. The A middle sources in M=[k,K−1] are upper, with noncrossing weights still needed. Choose either of these explicit boundary rules before allocation.

1. Put every source in M at upper host b=B−1. Its image is s+B−1−i and reverses M because s+B−1=k+K−1.
2. If A=2 and B≥3, put i=k at upper host b=B−2 and i=k+1 at b=B. Each source is fixed because its chosen b satisfies s+b=2i.

Both rules use M bijectively as images. Their quotas are h_b, with sum A. Require l_(j_0)≥B and put v_b=u_b−h_b, requiring all v_b≥0.

The remaining source and image coordinates form two equal intervals: [2,g+1] and [K,s−1]. Pair column p in [2,g+1] with coordinate R(p)=s+1−p, so R maps to [K,s−1] bijectively. The low row is below k, and the high row is above or at K and hence above or at k. The four reserved parts I_0, M and the two rows partition [0,s−1], including g=0. A lower host must keep the row and an upper host must switch rows for each packet below. These directions are exactly the D143 crossing test on these rows. In column coordinates an upper host with index b sends a low source p to high column p−(b−1), or a high source R(p) to low column p+(b−1). A lower host with translation a sends p to p+a in the low row, and R(p) to R(p−a) in the high row. All unused cells in a reserved packet or the row remainder take the fixed image at j_0.

Use three types of packets, each operating on both row coordinates of its consecutive column interval starting at p.

| Packet | Width in columns | Non-neutral host usage |
|---|---:|---|
| Lower rotation for a∈[1,A−2] | a+1 | One +a lower host and a uses of j_− |
| Reflection pair for b∈[1,B] | b | Two uses of upper host b |
| Mixed cycle for b∈[2,B] | b | One use of upper b=1, one of upper b, and b−1 of j_− |

For a lower rotation, the low source p maps to p+a at translation +a. Each p+j with 1≤j≤a maps to p+j−1 at translation −1. This cycles the whole low interval and leaves the high row fixed. At a reflection pair, p+b−1 and R(p) exchange images through upper host b in both directions. Both coordinates are in the packet and all its other cells are fixed. For a mixed cycle, p maps to R(p) at upper b=1. The high source R(p) maps to p+b−1 at upper b, after which each low source p+j maps to p+j−1 at translation −1 for j=b−1 down to 1. This closes the actual directed cycle, with distinct cells and the remaining ones fixed. All three proofs track the exact host formulas. A low row upper-host assignment reaches a high image and crosses. A high row upper-host assignment reaches a low image and is noncrossing. A lower host stays within the row, with a high row edge crossing and a low row edge noncrossing. The fixed middle and low boundary assignments also meet the incidence test.

Compute packet counts directly from the input quotas, with no assignment trial. Set P_a=l_(A−2−a) for a∈[1,A−2], and D=l_(j_−)−sum_a a P_a. For b≥3 set M_b to the residue of v_b modulo 2 in {0,1}. Put

    M_2=D−sum_(b≥3)(b−1) M_b.

Require 0≤M_2≤v_2 and v_2−M_2 even. Treat the empty sum at B=2 as zero. Require v_1≥sum_(b≥2)M_b and their difference even. Define

    P'_1=(v_1−sum_(b≥2)M_b)/2,
    P'_b=(v_b−M_b)/2 for b≥2.

These are nonnegative integers. Require the single width bound

    W=sum_a (a+1)P_a + sum_b b P'_b + sum_(b≥2) b M_b ≤ g.

Use M_b mixed packets in order of increasing b first, then P_a rotations in increasing a, then P'_b reflection pairs in increasing b. Place them consecutively on [2,g+1] and fix both row coordinates in any columns left over. This is a single deterministic choice of counts and order. At g=0 it permits exactly zero packets. The tests settle the specified recipe, and other choices of allocations remain open when a test fails.

Every packet permutes its own cells. Column reservations are disjoint and both boundary regions use their own coordinates. Hence each source is labeled once and each required difference coordinate is used once. The physical counts at positive translations are precisely the P_a. The count at translation −1 is sum_a aP_a+sum_(b≥2)(b−1)M_b=l_(j_−). The upper counts are h_b+v_b by the packet equations. All remaining cells are at j_0 and equal its quota since the declared quotas sum to s. Thus the method preserves every prescribed individual host count, along with differences [d,d+K−1] on actual noncrossing gap edges and [d+K,d+s−1] on actual crossing gap edges. In particular the construction works for supplied physically eligible hosts of zero quota without placing any named leaf there.

## 5. Exact completion, intermediate state and finite repetition

Assign the gap source labels for each host to its actual declared leaves in increasing coordinate order, using the fixed order of branch indices for direct leaves and of terminal indices for each center. Exterior names and labels are supplied independently. Keep the D143 old labels in [A,A+c−1]⊔[A+c+s,A+n+s], and expand the exterior upper labels by n+s. The supplied exterior tree uses the exterior labels and consumes [n+s+1,m] on actual crossing edges. The construction uses the gap labels [A+c,A+c+s−1] and differences [d,d+s−1]. The old spectrum is [1,d−1]⊔[d+s,n+s]. These complements give the complete label and weight bijections. The exact crossing spectrum at C=c+K is [d+K,m] from the old crossing interval, the crossing gap interval and the full high exterior interval. The actual final vertex w returns at the oriented extreme zero, with exact D134 p=1 data n'=n+2K, c'=c+K and d'=d+K. For an actual maximum-frontier input use the simultaneous label complements n−G and m−F of D143 Section 3, preserving all weights and physical membership under the complementary cuts. The actual lower shift is A for minimum polarity and B for maximum polarity, and the upper shift adds s in either case.

The first section's independent gap source set I_1 consists of the packet and boundary sources whose actual host belongs to that section. Its difference coordinate set J_1 is the union of just their explicitly computed images. Let E_1 and D_1 be the first section's expanded exterior labels and its actual exterior differences, including the connector vu. From the supplied labeling these are known before either section is emitted. The used first-boundary labels are the old label bands, E_1 and A+c+I_1, disjointly. The used weights are the old weight bands, D_1 and d+J_1, disjointly. Their remaining inventories are the exact full alphabet complements. The first-boundary crossing weights are [d+s,n+s], D_1 and d+(J_1∩[K,s−1]), disjointly. The new frontier is the expanded label of u and the only edge between this completed prefix and the second section is the declared uw. Its actual difference is given by the two supplied exterior labels. The second section uses exactly the complementary reservations; no intermediate rank or half-spectrum assumption enters.

All quota tests and placements depend on the declared block, not on n or c. A finite list of independently supplied blocks obeying the tests and the size premise at each step therefore closes by the D143 return, including repetitions of one admitted block. The D134 symbolic initializer at p=1 supplies arbitrarily large admissible initial size, with its actual declared path and branch section preserved as parts of the original input. Subsequent per-side shifts sum because old membership is preserved at every actual cut. At each completed boundary every already emitted label gets the sum of later actual lower shifts plus, exactly on its upper side, the sum of later gaps. Each already emitted difference gains just that gap sum when crossing. At a first-section boundary use the crossing set above, with its noncrossing complement in the used weights. This gives immutable final labels and both exact final-alphabet inventories by the D143 composition. The block selection and count tests take O(A+B) indexed operations. Filling the disjoint packets and remainder, then emitting fixed ordered leaf names, takes O(s+A+B) indexed operations per block, including the expanded exterior tree. This is an arithmetic operation count. No search or placement sweep is needed. All finite preparations and emissions terminate.

## 6. Independent exterior supply, recovery and strict enlargement

For arbitrary A≥2, B≥2 the following independently labeled exterior family meets D143 Section 3. Give v,u,w the reduced labels A,A+1,0. Place one named branch of the first section at each label j∈[1,A−1], with actual attachment to u. Place one named branch of the second at each label A+b with b∈[2,B], with actual attachment to w. Each branch is a direct leaf at quota zero, or an actual center with the independently prescribed named terminals at positive quota. Direct gap leaves at u and w occupy their own distinct prescribed indices. The actual connector vu weighs 1, the edges from u to w and the first exterior branches weigh [2,A+1], and the edges from w to the second exterior branches weigh [A+2,A+B]. All are distinct and join the specified sides. This supplies the labeled exterior without use of a complete target labeling. Other independently supplied named exteriors satisfying the input hypotheses can use the same allocation rule.

There are unbounded quota parameters even with this exterior supplied. Choose independent nonnegative rotation and pair counts and M_2, with M_b∈{0,1} for b≥3. Choose an integer g≥W. The packet usages and the chosen boundary rule specify all non-neutral counts before allocation. Prescribe the remaining count at j_0 from the total s=A+B+2g. It is at least B, as each interval has room for its prescribed non-neutral cells. These vectors pass the deterministic tests. This parameterization supplies one domain of quotas. The theorem itself reads an independently prescribed vector and checks it by the displayed arithmetic.

For the D143 control let A=2, B=3, k=K−2, s=2K−5 and use boundary rule 2. The exterior is exactly v,u,w,a,b_2,b_3 with respective reduced labels 2,3,0,1,4,5. For the original quotas l_a=t, l_w=s−2−2r−3t and (u_1,u_2,u_3)=(1+2r+t,t,1), the rule gives M_2=t, P'_1=r and all other counts zero. The width bound is 2t+r≤g=K−5. The middle sources k and k+1 are fixed at u and b_3. The mixed cycles start at the even columns 2 through 2t, and the b=1 pairs use the next r columns. Thus the rule recovers precisely the D143 allocation, including its named first and second profiles, crossing incidences, and Section 5 inventories. In particular, the first sources are {k} together with the b=1 pair cells, the low mixed starts and their successors. Their images replace every low mixed successor by the high partner of the corresponding start, exactly as in D143. The control includes empty cycle sets and equality in the width bound.

For a strict enlargement on those same exterior names and labels, prescribe two additional independent nonnegative parameters p,q and the full quotas

    l_a=t,  l_w=s−2−2r−3t−2p−2q,
    u_1=1+2r+t,  u_2=t+2p,  u_3=1+2q.

Take g≥2t+r+2p+3q, with r,t,p,q≥0. The new capacities yield M_2=t, P'_1=r, P'_2=p and P'_3=q. The neutral count is nonnegative and at least B by the packet count, or by substituting the displayed bound on g. Both actual profiles are formed before placement. The first is (t,0^(1+2r+t)); the second is (t+2p,1+2q,0^(s−2−2r−3t−2p−2q)). The first-section size is still 3+2r+2t and odd. The total is 2K, so the second-section size is also odd. Either p>0 or q>0 yields a strictly new physical quota vector for the same fixed exterior. At p=q=0 the vectors and placement agree with D143. The arbitrary-width rule additionally permits actual positive-translation hosts when A≥3 and mixed cycles longer than three when B≥3 and their specified counts are positive.

## 7. Retained methods and open scope

R226 classifies fixed-core completion for two hosts from given label and difference palettes, via actual forced components and reflected pairs. R232 combines supplied disjoint two-host palettes with a specified singleton forest, parity and endpoint capacity conditions. Here the boundary and packet palettes arise directly from the D143 consecutive gap and physical host formulas, with a prescribed crossing split. Their generation does not use a two-host extraction or a singleton-forest assumption. The retained R226 and R232 conclusions remain valid under their own premises. [R226](../references/upstream/mdl/N226_R226_two_host_completion.md#n226-closeout) · [R232](../references/upstream/mdl/N232_R232_joint_allocation.md)

D135 and D136 use translation displacements with a zero moment inside invariant source and target bands, and construct cycles or rotation packets. The lower-only rotations here are proved directly for the available positive shifts and the common −1 shift. Mixed host reflections interleave the two rows, so the gap as a whole does not have those invariant source and target bands. The actual crossing rule is checked at every arrow. The exact R226, R232, D135, D136 and D143 scopes remain separate. [D135](ORDINARY_SPINE_GENERAL_DISPLACEMENT_CYCLE_ALLOCATION.md) · [D136](ORDINARY_SPINE_INTERLEAVED_ROTATION_PACKET_ALLOCATION.md)

The balance, parity, exact per-host windows, B=1 exclusion and forced A=2 endpoints apply to all completions in the stated D143 class. The constructive quota and width conditions give a sufficient domain with independent supply. They leave unresolved exact feasibility outside this domain, more efficient or different allocations of the available coordinates, and general supply of named exteriors for arbitrary physical profiles. These results concern the declared embedding with fixed exterior roles and gap quotas.
