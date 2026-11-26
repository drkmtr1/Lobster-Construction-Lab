# D202 — Zero-direct-leaf multi-host detour-path supplier

Task LCL-ORDINARY-SPINE-ZERO-DIRECT-LEAF-MULTI-HOST-DETOUR-PATH-001. The prescribed shell admits a receiving section whose every child is a positive center. A descending path made of three-arrow detours and individual negative steps supplies the exact quotas under the stated aggregate condition. The relocated shell allows arbitrarily many additional positive centers with independently prescribed positive quotas.

All coordinates, widths, labels and quotas are exact integers. Intervals are inclusive, with a reversed interval empty. Every parent and terminal below is an actual vertex of the specified ordered original.

## 1. Expanded shell with all positive receiving quotas

Supply an independently graceful N-edge prefix in minimum orientation with its actual frontier v at 0. Use proper old safe cuts r<t<N−1, with distinct thresholds D_r,D_t≤N−2, and cut N−1 safe at threshold N−1. Let u=min(D_r,D_t), v*=max(D_r,D_t)+1. Use the numerical D200 roles {h,J0}={r+1,t+2} with 4≤h,J0≤K0−1, and choose {α,β}={u,v*}, σ in {−1,+1}. Write M0=N+K0 and require c0=M0−α and l0=c0+σβ to lie in [N+2,M0−3]. These are the geometrical D200 premises; the residual allocation is supplied below.

Take lower width A=d+1≥1 and upper width one. The actual new section is (p,q,s,1,t_d,...,t_1), with p,q,s and all t_j positive. The first four physical child labels are d+h,d,d+J0,d+c0, and the actual terminal of the fourth child is d+l0. Each additional child at d−j, j=1,...,d, has the corresponding quota t_j. Those children occur in increasing physical-label order. There are d+4 actual children, all positive, with 1+p+q+s+T actual terminals, where T=Σ_j t_j. The one connector gives K=p+q+s+T+6+d, so K0=p+q+s+T+6. The new frontier w is M=M0+d. The two negative roles have original quotas p and s; there is no direct leaf in this receiving section.

Use the increasing old map E(x)=A+x+1_(x≥r)+1_(x≥t)+(K0−4)1_(x≥N−1). It gives the old label set

    ([A,N+A] minus {d+r+1,d+t+2}) union {M−2,M−1}.

The long missing interval is [N+A+1,M−3]. The partial-safe-cut rank formula adds 1 to old weight d_old at each of the thresholds D_r,D_t at or below d_old, and adds K0−4 at N−1. It therefore gives the old weight set

    ([1,N] minus {u,v*}) union {M0−3,M0−2}.

The fresh label set is [0,d] together with the two deleted low positions, the long missing interval, and {M}. The fresh weight set is {u,v*} together with [N+1,M0−4] and [M0−1,M]. These are exact complements. The two deleted low positions have now become positive lower centers. The difference at the third child incidence is still M0−J0. The first four child weights in their original order are M0−h,M0,M0−J0,α. The actual connector (A,M) has weight M0−1. The designated terminal has weight β. The additional children at 0,...,d−1 have weights M,M−1,...,M0+1. All these incidences follow from the stated physical endpoints.

At physical cut C=N+A+1 in maximum-output orientation, the old lower vertices are precisely those at input labels less than N−1. The two old crossing weights are M0−3,M0−2. The connector and all lower child incidences cross. The designated fourth child and its terminal both remain on the upper side with w, so their weights α,β supply the two noncrossing holes. In normalized residual coordinates the unused labels and weights are

    R=[N+2,M0−3] minus {c0,l0},
    Q=[N+1,M0−4] minus {M0−h,M0−J0}.

Actual unused labels are d+R and actual unused weights are Q. Both have size K0−6. For physical terminal label x=d+y, each residual parent is strictly below x and below C, as h,J0≤N while y≥N+2. Subtraction gives exactly y−h, y, y−J0 or y+j at the first, second, third or additional host j. Every such terminal crosses the cut. Consequently a quota-respecting bijection R→Q uses the entire remaining inventory. The full label and difference alphabets are [0,M] and [1,M], with crossing [N+1,M] and noncrossing [1,N]. Complementing at M gives minimum frontier 0 and cut M+1−C=K0−1. The literal connector becomes (M−A,0); all differences and crossing flags agree. The returned state is P(M,K0−1,N+1). In D157 terminology it is strict exactly when K0=N and d=0.

## 2. Descending detour-path lemma

Let finite palettes R and Q differ by exactly one unmatched source U and one unmatched target L<U. Assume [L+1,U] is contained in R and [L,U−1] in Q; all other coordinates are common or absent in both. Let a,b be available negative step magnitudes, and 0<j<min(a,b) an available positive displacement. For the three-arrow block

    x → x−a → x−a+j → x−a+j−b,

put y=x−a+j−b. Then y<x−a<x−a+j<x. Its two distinct internal vertices lie in the open interval between its endpoints. Viewed as one block from x to y, the entire block descends strictly. A single negative step also descends strictly. Thus in a concatenation every block interior lies strictly between its own two decreasing boundary coordinates, and is disjoint from all other interiors and boundaries. Shared adjoining endpoints occur once in the concatenated path. This proves simplicity even when an individual positive arrow ascends.

Require d<min(h,J0), p,s≥1 and p+s≥2T. Make an ordered list of p negative tokens of magnitude h followed by s negative tokens of magnitude J0. Make a list of t_j positive tokens of magnitude j for each j=1,...,d in increasing order. Use the next two negative tokens for each positive token, in order as a,b of the displayed block. Use every leftover negative token as an individual descending step. By the aggregate inequality the pairing terminates and every token is used once. Total decrease is Δ=hp+J0s−S, with S=Σ_j j t_j. Each block decreases and all remaining negative arrows decrease, so Δ>0 because actual negative quotas are positive. Equivalently, each three-arrow block decreases by a+b−j>0.

If U−L=Δ, start at U. The final coordinate is L by exact summation. Each strictly descending block boundary lies in [L,U] and every intermediate vertex in (L,U). All internal coordinates thus belong to R∩Q. The resulting simple path uses precisely its vertices except L as sources and precisely its vertices except U as images. Use an identity at every other source. These identities occupy exactly the complementary common coordinates, hence the full directed assignment has one image at each point of Q. The positive and negative token counts are exactly the given actual host quotas. Provided the total is |R|=p+q+s+T, the number of identities is exactly q. For a named construction, sort each host's selected actual labels and use its original terminal indices in increasing order. There are p+s+T nonidentity arrows and |R|−p−s−T identities, with no enumeration of alternative assignments.

Across every successful allocation, regardless of its decomposition, summation of actual source minus target gives the necessary moment ΣR−ΣQ=hp+J0s−S. The aggregate inequality is used as a sufficient hypothesis in the detour construction. No necessity for that inequality follows. When d=0 there are only the two strictly descending options and the identity. For the specified unmatched endpoints with complete interval, the necessary moment is sufficient for any given admissible p,q,s: concatenate the p steps of h and s steps of J0 to reach L from U, then use all remaining identities. In fact a nontrivial cycle would have strictly negative total displacement, so any completion in this negative-only geometry uses its nonidentity arrows on the one path. The moment claim is conditional on the geometry and exact available quota total.

## 3. Size-independent standard shell

Take r=3,t=4, thresholds 1,2 in either order, and the high safe cut N−1. Choose (h,J0)=(4,6) or (6,4). Take α=3,β=1,σ=−1, so c0=M0−3,l0=M0−4. The effective geometry allows K0≥7. With the moment-certified sizes below K0≥8, which admits these distinct roles and both designated upper labels. The exact residuals reduce to

    R=[N+2,M0−5],
    Q=[N+1,M0−5] minus {M0−6}.

Their unmatched source is U=M0−6 and unmatched target L=N+1. Their total moment U−L=K0−7, and both full path intervals are available. For any p,s≥1, d≤3, positive t_1,...,t_d and p+s≥2T, set

    Δ=hp+J0s−S,
    K0=Δ+7,
    q=(h−1)p+(J0−1)s−Σ_j (j+1)t_j+1.

These satisfy the exact size and moment. Write m0=min(h,J0)=4. Because d<m0, S+T≤m0 T. The positive part (h−1)p+(J0−1)s is at least (m0−1)(p+s). Hence q≥(m0−2)T+1≥1, even when T=0. As Δ>0, the shell geometry and both interval requirements hold. Section 2 gives a full named allocation and §1 returns P(N+K0+d,K0−1,N+1). No equality of N and either fresh size enters the proof. The reversed-threshold D199 one-center input or D199's independently supplied nonnested Family C provides the required safe coordinates where admitted, including the fixed Family C at N=11. Already at d=0 one obtains four actual positive receiving centers with independently specified p,s≥1.

## 4. Relocated shell and unbounded receiving multiplicity

For h≥4, J0=h+3 and N≥h+3, use safe cuts (r,D_r)=(h−1,h−3), (t,D_t)=(h+1,h−1) and (N−1,N−1). Thus α=h,β=h−3,σ=+1. Put c0=M0−h and l0=M0−3. The geometric bound is K0≥h+4, from J0≤K0−1, which also puts c0 and l0 in the long gap. The palettes are exactly

    R=[N+2,M0−4] minus {M0−h},
    Q=[N+1,M0−4] minus {M0−h,M0−h−3}.

With positive Δ choose K0>h+4. Then U=M0−h−3 is the unmatched source and L=N+1 is the unmatched target. The one common vacancy M0−h=U+3 is strictly above the whole path interval. Therefore every coordinate required by §2 is present, and U−L=K0−h−4. At the geometric boundary K0=h+4 one has U=L and R=Q. It cannot solve the required positive two-host moment at d=0 and is outside the positive Δ domain of the detour construction.

For any d<h, p,s≥1, independently prescribed positive t_1,...,t_d and p+s≥2T choose

    Δ=hp+(h+3)s−S,
    K0=Δ+h+4,
    q=(h−1)p+(h+2)s−Σ_j (j+1)t_j+h−2.

These give the exact size and moment. Now S+T≤hT, and the positive quota part is at least (h−1)(p+s), so q≥(h−2)T+h−2≥1. All geometric inequalities and the complete-path premises hold. Sections 1–2 give the exact actual inventories and both physical polarities.

For every finite d choose any h≥max(4,d+1). Supply the actual prefix (h−2),(),(),(0,0) with N=h+4 by the D199 terminal-free maps underlying its odd-run formula, with initial center quota h−2, a=0 and b=2. Its minimum-oriented spine in actual order is (h+1,1,h+2,0), initial positive center is 2, its actual terminal labels in index order are h,h−1,...,3, and the last direct children in index order are N,N−1. These labels exhaust [0,N]. The initial terminal differences exhaust [1,h−2], the attachment of the positive center weighs h−1, the spine edges weigh h,h+1,h+2 in order, and the final direct-leaf edges weigh N,N−1. Cut h−1 crosses terminal ranks h−3,h−2 and every higher difference, with no lower crossing. Cut h+1 crosses exactly h−1,h,h+1,h+2,N−1,N. Cut N−1 crosses exactly N−1,N. This verifies all safe premises without solving a target. The prefix contains its two actual direct leaves, and the receiving section has d+4 positive centers and zero direct leaves. This family allows N to grow with d. The upper center retains quota one. The principal and third positive quotas p,s can each be chosen subject to positivity and the aggregate condition, and q is coupled by the formula. General arbitrary quotas and safe-state initialization remain open.

## 5. Exact adverse scope and retained mechanisms

Control D has h=10,J0=13,d=6,N=14,p=s=1 and all six t_j=1, with T=6,S=21. Its exact moment is Δ=23−21=2 and K0=16, q=2. The valid fixed shell has M0=30,M=36,C=22, c0=20,l0=27, and

    R={16,17,18,19,21,22,23,24,25,26},
    Q={15,16,18,19,21,22,23,24,25,26}.

Every potential target y−13 at the third host is at most 13, while Q begins at 15. Thus an actual quota-one lower center cannot receive any assigned terminal within this fixed shell. The positive moment alone is insufficient. This direct incidence obstruction does not determine any other placement or ordinary gracefulness of the original. The obstruction follows from the actual host's empty support, independent of the detour method's sufficient aggregate bound.

[D201](ORDINARY_SPINE_EXPANDED_EXTERIOR_MULTI_HOST_RESIDUE_PACKETS.md) derives a forced monotone path and exact one-jump cycles because all shifts share a residue step and its scaled negative shift is −1. In the present proof positive arrows can lie on the main path, two different negative shifts are admitted, and no common residue restriction is needed. [D135](ORDINARY_SPINE_GENERAL_DISPLACEMENT_CYCLE_ALLOCATION.md) likewise uses actual signed tokens and a bounded walk, extracting zero-sum cycles by repeat removal within invariant bands. [D136](ORDINARY_SPINE_INTERLEAVED_ROTATION_PACKET_ALLOCATION.md) uses rotations and weighted token mass to form capacity-controlled cyclic blocks. The D202 blocks have strictly negative net displacement and disjoint interiors on a single unmatched-endpoint path. [D165](ORDINARY_SPINE_EXCEPTIONAL_FOUR_FIRST_CENTER_PARITY_CHAIN.md) uses step-two hole repairs, [D166](ORDINARY_SPINE_EXCEPTIONAL_FOUR_FIRST_CENTER_EIGHT_DEFECT.md) gives exact directional recurrences, and [D167](ORDINARY_SPINE_EXCEPTIONAL_RESERVATION_SEMILINEAR.md) and [D168](ORDINARY_SPINE_EXCEPTIONAL_TWO_UPPER_HOST_RESIDUE_COMPRESSION.md) preserve signed flow and quotas through finite types and reversible anchored compression. These paths share exact hole accounting with D202. Their two-option residue recurrences and common-hole barriers differ from D202's complete integer path interval and multiple host options. [D196](ORDINARY_SPINE_GENERALIZED_ONE_SECTION_CUT_SPECTRUM.md) supplies unit-sided zero-sum cycles on prescribed invariant bands. No historical novelty is asserted.

## 6. Inherited safe cuts and immutable transport

At a physical maximum-output cut C' in [A+max(h,J0),N+A+1], all fresh lower attachment roles and the old connector endpoint are below the cut. All residual terminals, the upper center and its terminal, and the frontier w are at or above it. Thus fresh crossing weights are [N+1,M] minus {M0−3,M0−2}. Write b=|{x:E(x)<C'}| for the induced proper old cut. A safe output requires both old high weights to cross, and every old weight below the noncrossing v* to stay noncrossing. The remaining old crossing ranks must fill a suffix immediately below N+1, possibly empty. Old rank max(D_r,D_t) has image v*+1. The old supported-rank map therefore gives exactly the D201 corridor condition: b must be safe at an old threshold D_b between max(D_r,D_t) and N−1. The output threshold is D_b+2 for D_b≤N−2, and N+1 for D_b=N−1. The converse fills the required crossing suffix. The complementary output cuts are M+1−C'. This direct inherited range gives no general positive-terminal closure or renewal.

The old label maps in actual physical orientations are E for incoming minimum, and x↦M−E(N−x) for incoming maximum. Both are increasing. At a shell step an edge originally between minimum-oriented x<y gains the sum of the local widths on thresholds in (x,y]. Record actual changed sides by comparing the input cut with the output cut at every original vertex. Record changed crossing edges by comparing the two original endpoint predicates. This calculation does not rely on an old edge retaining its crossing status. For any finite admitted sequence, D198's increasing transport composes the maps, with each later threshold pulled back to the first earlier coordinate satisfying it. Offsets absorb thresholds already passed by the least earlier coordinate and coincident gaps add. Assign each actual vertex's birth label once in the final alphabet by its composed remaining map. For each original boundary, transform its assigned vertex labels and subtract its actual transformed edge endpoints; take their complements in the complete alphabets for the two remaining inventories. Split both resources by the final physical cut and crossing predicates. All maps, intervals and paths are finite.

For E, independently retain D200's exact strict original through 15→30→43→86. At its 43-edge prefix, safe cuts 32 and 34 in the direct-leaf tail give D200 maximum-output cuts 35 and 37 with thresholds 34 and 36. Append the actual terminal-free two-child section. Its actual maximum-to-minimum map on older vertices is x↦x+1, its new frontier is zero, and its original children are at 89,88 in index order. The supplied 89-edge state has cut 46, threshold 44. The high cut from the two actual children is 88 at threshold 88, and the two retained cuts become (36,34),(38,36). These formulas and the original graph were fixed independently of the 280-edge continuation.

The third shell uses h=37,J0=40,d=2,p=3,s=1,t_1=t_2=1, Δ=148, K0=189. It gives the prescribed path 238→201→202→165→128→130→90, final maximum cut 93, crossing [90,280] and returned P(280,188,90). At this last step the old cut changes from 46 to the induced old cut 88 in minimum input coordinates. In particular old labels 46 through 87 change physical sides and old crossing ranks 44 through 87 cease to cross. Ranks 88 and 89 still cross.

Write E_1(x)=1+x+1_(x≥3)+1_(x≥4)+11·1_(x≥14) for the first D200 shell and E_2(x)=1+x+1_(x≥12)+1_(x≥14)+39·1_(x≥42) for the second. The final map is E_3(x)=3+x+1_(x≥36)+1_(x≥38)+185·1_(x≥88). In actual boundary coordinates at sizes 15,30,43,86,89,280 the pointwise maps into the final maximum output are respectively

    x ↦ E_3(E_2(E_1(x)+1)+1),
    x ↦ E_3(E_2(x+1)+1),
    x ↦ E_3(E_2(x)+1),
    x ↦ E_3(x+1),
    x ↦ E_3(x),
    x ↦ x.

For a boundary of size m0, the complementary map is x↦280−F_m0(m0−x), with F_m0 its listed actual map. At the initial boundary the map is 7+x with D200 widths 1,1,1,1,11 at 3,4,8,10,14. The final five actual maximum connector pairs are (7,38),(38,5),(5,92),(92,3),(3,280). The full pointwise maps specify every installed boundary, while each individual birth record contains only the vertices born at that boundary. Their union emits the final original labels once. The 204-edge D201 continuation is a different target that shares the independent 89-edge input.

## 7. Prescribed named controls

| Control | Exact result |
| --- | --- |
| A | Family C at N=11. The actual section (2,12,1,1) uses path 26→22→18→12. Maximum cut 13, crossing [12,32], return P(32,20,12). |
| B | Family C at N=11. The actual section (4,21,4,1,1,2,1) uses 44→40→41→37→33→35→31→25→27→21→15→18→12. Maximum cut 16, crossing [12,53], return P(53,38,12). |
| C | Independent (3),(),(),(0,0), N=9. The actual section (7,35,3,1,1,1,2,1) uses 57→52→53→48→43→45→40→35→37→32→27→30→22→14→18→10. Maximum cut 15, crossing [10,69], return P(69,55,10). |
| D | Independent (8),(),(),(0,0), N=14. The fixed shell balances moment at two but supplies no possible residual terminal at the actual J0 host. |
| E | The separate original through 15→30→43→86→89→280, with final section (3,177,1,1,1,1). Both physical inventories and all five connector and transport records are retained. |

Exact graph identities were frozen before new prescribed labels. Partial snapshots are separate immutable copies of the assigned names, with all pending terminal names excluded and complementary labels verified. The controls preserve every indexed parent and actual edge. Verification involved fixed arithmetic, independent reconstruction and separate reviews, with zero numerical search, solver, checker, campaign or historical replay. Prior accepted scopes and closed lanes and the unclassified D198 fixed minimum-input w=0 branch remain intact.
