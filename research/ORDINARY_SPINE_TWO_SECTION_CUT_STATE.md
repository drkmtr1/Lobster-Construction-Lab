# D143 — Two-section ordinary spine transition returning the D134 cut state

Task `LCL-ORDINARY-SPINE-TWO-SECTION-CUT-STATE-001`. All structural parameters and labels are exact integers, excluding booleans. Intervals are inclusive and reversed intervals are empty. Write ⊔ for disjoint union and a+S for the translate of a set S. The proof is symbolic throughout.

## Scope and theorem

Supply an independently constructed ordinary graceful named lobster prefix P with n edges, its actual ordered witnessing spine ending at v, and a D134 p=1 state. In coordinates G oriented to G(v)=0, the cut c≥1 satisfies n=2c+2 and the exact actual crossing spectrum is [d,n] for d=c+2. A label equal to a cut is on its upper side. The noncrossing spectrum is [1,d−1] because all old differences are used once. Retain the complete supplied state and the actual names, incidences and ordered roles.

Append two actual sections, with next spine vertices u,w and original connectors vu,uw. A section with ordered branch entries q_j≥0 contributes 1+Σ_j(1+q_j) vertices. Entry zero gives a direct leaf, while an empty vector still contributes the actual spine vertex. Write H_i for each count, H=H_1+H_2=2K and m=n+H. Require n≥H. All added edges come from the declared parent incidences and each new vertex contributes one. The resulting named graph is a tree because every new vertex attaches to its parent in the enlarged rooted tree. Extending the original spine witnesses the lobster condition. No old vertex, branch or edge is renamed or moved.

Consider precisely the membership-preserving embedding of the old side below c by shift A, and its side at or above c by shift A+s, with A,B,s≥0 and A+B+s=H. Require the actual final spine vertex w to carry an extreme and return the exact D134 p=1 state. In this class a successful extension keeps the input frontier polarity and has A≥2, B≥1 and s≥K. Its two spine vertices belong to a connected exterior tree. The gap vertices are actual direct leaves or terminals of exterior centers. Section 3 gives an if-and-only-if reduction to that smaller named tree and a physically compatible gap permutation.

The positive family in Section 4 admits both polarities, an odd intermediate edge count and arbitrary finite admitted lists of its blocks. It uses a five-vertex exterior extension and two independent quota parameters r,t≥0 subject to K≥5+2t+r. It is an explicit sufficient family within the class.

## 1. Combined inventories and both proposed output polarities

For each vertex x of P define E(x)=A+G(x)+s I(G(x)≥c). Its labels occupy

    [A,A+c−1] ⊔ [A+c+s,A+n+s].

The exact unused label intervals in [0,m] are the lower exterior [0,A−1], gap [A+c,A+c+s−1], and upper exterior [m−B+1,m]. The spread between endpoints of every old noncrossing edge is unchanged. On an old crossing edge the higher endpoint moves s farther than the lower endpoint. By the prescribed actual crossing spectrum, the exact old and fresh difference inventories are

    old   [1,d−1] ⊔ [d+s,n+s]
    fresh [d,d+s−1] ⊔ [n+s+1,m].

Both old bands are in range and disjoint. All counts follow from these interval complements before assigning fresh labels. In the placement coordinates, a return at w=0 has cut C=m/2−1=c+K. A return at w=m has cut C=m+1−(m/2−1)=c+K+3. The latter relation follows by complementing into the zero-frontier orientation. In either placement the exact crossing threshold is d+K and the required crossing spectrum is [d+K,m]. An edge below the threshold must be noncrossing and an edge at or above it must cross.

The old minimum crossing weight d+s is still a crossing by the required membership. Thus s≥K and A+B≤K≤c+1. Membership preservation is equivalent to A+c≤C≤A+c+s, using the occupied last lower and first upper positions. With C=A+c+k it follows that 0≤k≤s. Exactly n−c+1 old vertices are upper, so the fresh upper cardinality is m−C+1−(n−c+1)=H+c−C. This is K when w=0 and K−3 when w=m. The lower exterior is wholly below C and the upper exterior wholly at or above C by the old endpoint inequalities. In particular B is at most the fresh upper cardinality. The two fresh difference demands by crossing status are

    noncrossing [d,d+K−1]
    crossing    [d+K,d+s−1] ⊔ [n+s+1,m].

These are necessary for any successful return. The interval [d+K,d+s−1] is empty at s=K.

## 2. Exterior connectivity, forced polarity and leaves in the gap

First establish B≤c in every successful case. For w=m, B≥1 and B≤K−3≤c−2. For w=0, zero must be fresh, so A≥1 and B≤K−1≤c. Thus the following bounds cover both orientations whenever the relevant endpoint class exists. An internal fresh edge incident with a gap vertex has weight at most the indicated bound:

| Endpoint classes | Maximum possible weight |
|---|---:|
| both in gap | s−1 |
| gap and lower exterior | A+c+s−1≤n+s−2 |
| gap and upper exterior | m−(A+c)=n+s+B−c≤n+s |

A same-exterior edge has weight at most A−1 or B−1, both below n+s+1. Empty classes give no possible edge. Hence only opposite exteriors can supply a weight above n+s internally. The old frontier v is placed at A and is below C. Its connector vu can supply a weight above n+s exactly when u lies in the upper exterior. In that case its weight is at least n+s+1 because the smallest upper exterior label is A+n+s+1. With u in the gap the connector weight is at most c+s−1. With u in the lower exterior it is at most A.

There are E_0=A+B fresh exterior vertices and E_0 high residual weights. The proposed extreme requires E_0≥1. The induced graph on those exterior vertices is a forest, so it has at most E_0−1 edges. At most one further high weight can come from vu. Exact coverage therefore forces vu to be high and every exterior forest edge to use one distinct high weight, with exactly E_0−1 internal edges. Thus the exterior forest is connected. It contains u in the upper exterior and w in an exterior because w is the proposed extreme. The singleton possibility is excluded by these distinct vertices. The actual edge uw belongs to that induced tree and has a high weight, so its endpoints are in opposite exteriors. This forces w into the lower exterior and hence w=0. The conclusion is retention of frontier polarity, including after the coordinate conjugation in Section 3.

The only possible fresh gap vertices are degree-one direct leaves or terminals. Both spine vertices are exterior. Any terminal of a gap center must also lie in the gap, since an exterior terminal with its only edge to a gap center would be isolated in the connected exterior tree of at least two vertices. An edge between two gap labels cannot cross C, since its weight is at most s−1≤2K−1<d+K. After w=0 is forced, k=K−A and the two gap sides have lengths K−A and K−B. Each is below d because A,B≥1, K≤c+1 and d=c+2. Thus a gap-to-gap edge on one side cannot supply any fresh weight, all of which are at least d. A positive-quota gap center would have such a terminal edge and is impossible. In a successful allocation each gap leaf is therefore attached to its own exterior host, which can be either a spine vertex or a positive center.

If A=1, the smallest gap label is c+1. Its difference to the sole lower exterior label 0 is c+1<d. Its difference to any upper exterior label is at least n+s+1−c=d+s+1, above the gap difference band. By the high-weight endpoint bounds, this gap incidence cannot consume a high residual weight either. This excludes A=1. Together the proof gives A≥2, B≥1 and K≥3 for successful completion in the stated embedding. It gives no obstruction to ordinary gracefulness under different embeddings.

## 3. Exact exterior and gap reduction

Fix A≥2, B≥1, s≥K and A+B+s=2K. Select a subset of the actual named fresh direct leaves and terminals to occupy the gap, with cardinality s. The other fresh vertices include u,w and induce the proposed exterior tree. Retain v and its connector vu in a smaller named tree consisting of that exterior tree plus v. The proposed reduction has two simultaneous tests.

1. Label this smaller tree gracefully onto [0,A+B]. Fix v at A, w at 0 and u in [A+1,A+B]. Its low class [0,A] and high class [A+1,A+B] must meet every actual edge in opposite classes.
2. Assign the actual selected gap leaves bijectively to i∈[0,s−1], with label A+c+i in the full tree. Their actual hosts are all exterior. If a leaf is at a lower exterior host of reduced label j∈[0,A−1] its weight is d+π(i) with π(i)=A−2+i−j. If its host is upper with reduced label A+b, 1≤b≤B, its weight is d+π(i) with π(i)=s+b−i. Require π to permute [0,s−1]. Require π(i)≥K exactly when the gap leaf and its own host are on opposite sides. The gap side is lower for i<k=K−A and upper otherwise.

These tests are necessary by Section 2. Indeed, keeping lower exterior labels and v=A and subtracting n+s from the upper exterior labels translates their union to [0,A+B]. It subtracts n+s from each actual high incidence weight, yielding [1,A+B]. Subtraction of the actual labels at gap leaf and host gives the displayed formulas, including the signs because the gap lies strictly between the two exterior label intervals. Each gap incidence consumes one actual weight in [d,d+s−1]. Its actual crossing side gives test 2. The physical selection refers to names, including their attachment and terminal indices.

Conversely suppose both tests hold. Expand the upper exterior labels by adding n+s and keep all lower exterior labels. The resulting connector at v agrees with its placed old label A. Assign the gap labels according to test 2. The labels complement the old image, and the exterior weights consume [n+s+1,m]. The gap incidences consume [d,d+s−1]. Thus both full inventories are bijective. The old membership holds at C=c+K because k=K−A≥0 and s−k=K−B≥0. Every expanded exterior edge crosses, including vu. Gap crossings are exactly those with coordinate ≥K by test 2, and all old crossings gain s. Hence the entire crossing spectrum is [d+K,m], with complement [1,d+K−1]. The final named frontier w=0 directly returns the p=1 state at m with oriented cut c+K and threshold d+K. This is an equivalence for the declared placement class and permitted choice of the named gap subset. The smaller exterior labeling and the gap assignment must be supplied compatibly.

For actual minimum-frontier input use these oriented labels directly. For actual maximum-frontier input, read G=n−g and return labels m−F for the oriented placement labels F. Actual cuts are the complementary cuts n+1−c and m+1−C. The induced actual old map shifts labels below the actual cut by B, and those at or above it by B+s, as follows from m−n=A+B+s. This is an increasing two-translation map, exchanging sides on both input and output. It preserves actual membership and all absolute spectra. The actual final frontier is then m and has the same maximum polarity as its input. Sections 1–3 apply to this conjugate placement without an additional output assumption.

## 4. An independent constructive family with an odd intermediate size

Choose r,t≥0 and K≥5+2t+r, with n≥2K. Define k=K−2, A=2, B=3 and s=2K−5=2k−1. Then s≥K, A+B+s=2K, and C=c+K=d+k. For a nonnegative integer j write 0^j for the list of j zero entries. Use these exact physical ordered vectors:

    section at u: (t, 0^(1+2r+t))
    section at w: (t, 1, 0^(s−2−2r−3t)).

The exponent in the second vector is at least 3+t because 2t+r≤k−3. In the first section call the branch at index zero a. In the second call the branches at indices zero and one b_2,b_3. Branches a and b_2 retain those same physical indices and are direct leaves when t=0. All unnamed entries in these displays are the actual indexed direct leaves indicated by the zeros.

Independently label the smaller exterior tree on v,u,w,a,b_2,b_3 by 2,3,0,1,4,5 respectively. The actual edges vu,ua,uw,wb_2,wb_3 have differences 1,2,3,4,5 and all cross the cut after reduced label 2. Thus the full placement gives u=m−2, w=0, a=1, b_2=m−1, b_3=m. The high weights are n+s+1 through n+s+5 in the listed order. These physical exterior incidences are supplied without requiring an intermediate rank layout.

To supply the gap use the following disjoint reserved coordinate sets:

    X_3 = {2,4,...,2t}
    X_2 = [2t+2,2t+r+1]
    y(x) = 2k−x
    Y_j = {y(x): x∈X_j} for j=2,3.

The low sources X_3, X_3+1 and X_2 are pairwise disjoint inside [2,k−2]. When the sets are empty the claim is vacuous. The high partners lie in [k+2,2k−2], stay in the gap, and are all distinct as y is injective. Neither side uses the special coordinates k,k+1.

With A=2 the gap labels are d+i. The weight coordinates at actual hosts w,a,u,b_2,b_3 are respectively i, i−1, 2k−i, 2k+1−i, 2k+2−i by Section 3. Allocate the following leaves, with the actual host indicated:

- At k attach a direct leaf to u, and at k+1 attach the sole terminal of b_3. Both coordinates are fixed because these two host formulas give π(k)=k and π(k+1)=k+1.
- For every x∈X_2 attach both the leaves at x and y(x) directly to u. The coordinates transpose because its formula gives y(x) and x respectively.
- For every x∈X_3 attach x directly to u, y(x) to b_2, and x+1 to a. The coordinates form the three-cycle x→y(x)→x+1→x using the three actual host functions.
- Attach every remaining coordinate directly to w. These are fixed by the actual weight at w=0.

The cycles and fixed points are disjoint and cover [0,s−1]. Each special coordinate is at or above k with an upper host, so is noncrossing and its coordinate lies below K=k+2. In the transposition the low x has an upper host and weight coordinate y(x)≥K, while the high y(x) has an upper host and weight coordinate x<K. In the three-cycle the low x again crosses with weight coordinate y(x)≥K. The high y(x) is noncrossing at b_2 with coordinate x+1<K, and the low x+1 is noncrossing at a with coordinate x<K. For the remaining fixed points at w, i<k is noncrossing and all remaining i≥k have i≥k+2=K and cross. These are precisely the two fresh difference demands from test 2. The proof never requires an alpha labeling of P or of the full tree.

The first section has t terminals at a and 1+2r+t direct gap leaves. The second has t terminals at b_2, one at b_3, and s−2−2r−3t direct gap leaves. These counts equal the named vectors including t=0. Emit terminal and direct-leaf labels in increasing gap coordinate within each named host and ordered zero-entry list, preserving every physical index. The actual spine and positive/zero branch roles are thus exactly the announced originals. The counts give H_1=3+2r+2t and H_2=s+2−2r−2t=2K−3−2r−2t. Both are odd. They sum to 2K. When t>0 there are positive centers in both sections. The proof handles the minimal budget K=5+2t+r and the empty cycle sets, since the two special points exist at all k≥3.

## 5. Independently supplied first-section state

Reserve both phases from the given P and declared block parameters, before any leaf is assigned. Let L_P and D_P denote the displayed occupied old label and difference sets. Define the first-section coordinate sets

    I_1 = {k} ⊔ X_2 ⊔ Y_2 ⊔ X_3 ⊔ (X_3+1)
    J_1 = {k} ⊔ X_2 ⊔ Y_2 ⊔ X_3 ⊔ Y_3.

A first-section source x of a three-cycle supplies y(x), and its first-section source x+1 supplies x. Its second-section source y(x) will supply x+1. The two sets need not agree. The independently emitted first-section prefix has exact used and remaining labels

    used      L_P ⊔ {1,m−2} ⊔ (d+I_1)
    remaining {0,m−1,m} ⊔ (d+([0,s−1] minus I_1)),

and exact used and remaining weights

    used      D_P ⊔ [n+s+1,n+s+2] ⊔ (d+J_1)
    remaining [n+s+3,m] ⊔ (d+([0,s−1] minus J_1)).

At cut C=c+K in the declared final alphabet the actual used crossing spectrum is

    [d+s,n+s] ⊔ (d+(Y_2 ⊔ Y_3)) ⊔ [n+s+1,n+s+2].

The exact used noncrossing spectrum is [1,d−1] ⊔ (d+({k}⊔X_2⊔X_3)). The first new spine vertex u carries m−2. Its only unfinished incidence to the second section is the actual edge uw. Its weight will be m−2=n+s+3 since w uses 0, and the two second-section exterior attachments then occupy the remaining high weights. The second gap leaves are exactly the complementary sources and map to the complementary destinations because π is the independently specified full permutation. Their actual hosts realize those weights with the required crossing status. This proves compatibility from independently determined partial data rather than extracting it from a solved tree. For actual maximum orientation complement partial labels about m and the cut about m+1. Weights and crossing statuses are unchanged, and the partial frontier label is then 2.

The first-section count n+H_1 is odd, so it cannot satisfy the exact normalized D134 p=1 relation n'=2c'+2. The proof places an intermediate state in the declared target alphabet and uses neither an extreme intermediate nor a half-spectrum or rank hypothesis there.

## 6. Independent input supply, repeatability and immutable labels

D134's symbolic initializer at p=1 supplies available states of arbitrarily large even size. One exact option is the D141 non-leaf family before any additional attempted bridge. It uses the retained independently supplied maximum-frontier seed, the actual declared alternating path of the D134 initializer, and its actual first branched section. In the notation of that proof the parameter γ can be arbitrarily large in the required parity class and gives n=4γ+6, c=2γ+2 and d=2γ+4. Choose it large enough for any finite declared list, keeping all original initializer sections present. This is a conditional and independently realizable input class. Complementing the supplied state gives the other actual polarity. Nothing in this construction requires the D139/D140 distinguished boundary leaf, or a full D142 single-section placement.

For any finite list of admitted blocks, n_i=n_(i−1)+2K_i stays even and the returned oriented cut and threshold each increase by K_i. The placement returns the same extreme polarity with the exact D134 cut spectrum. It therefore preserves the full input contract for the next block whenever n_(i−1)≥2K_i and the block's own parameter bounds hold. Induction proves closure, including an empty list. Any one admitted block can repeat finitely as often as declared because the size only increases. Distinct actual successive block names and every physical incidence already supplied persist.

For immutable labels, at each completed block boundary i write C_i for the actual cut and d_i for the crossing threshold. Future old maps are increasing two-translation maps preserving the actual sides. The actual lower shifts are 2 for a minimum-frontier input and 3 for a maximum-frontier input, with upper shift plus s_j in either case. Write L_i for the sum of later actual lower shifts and S_i for the sum of their gaps s_j. The final image of a vertex present at boundary i with label x is

    Ψ_i(x)=x+L_i+S_i I(x≥C_i).

This follows vertex by vertex because the same side predicate survives every subsequent boundary. If E_i is the actual embedding into block i, then Ψ_(i−1)(x)=Ψ_i(E_i(x)) for every previously supplied vertex. Emit the original seed once using Ψ_0 and each new vertex once using the Ψ_i of its block. This works even when emitting the first section before the second, because its positions in the local target alphabet and sides were already determined.

At boundary i the actual final-alphabet used label set is [L_i,L_i+C_i−1] ⊔ [L_i+C_i+S_i,L_i+n_i+S_i]. The used differences are [1,d_i−1] ⊔ [d_i+S_i,n_i+S_i]. Both remaining inventories are the exact complements in the final alphabets. At a first-section boundary the same rule pushes forward the used label set in Section 5 and adds S_i to precisely its displayed crossing weights, leaving the noncrossing weights unchanged. At any block the new labels and new weights accounted for after the final-alphabet transform are disjoint from the consumed inventories because the label transform is injective and the crossing threshold separates unchanged noncrossing weights from shifted crossings. This also verifies the actual next spine connectors after all later embeddings. At the final boundary Ψ is identity and the inventories are empty. All ordered leaves can be emitted by one scan of the gap indices using the explicit cycle intervals and local host counters. Computing suffix shifts and writing the declared graph and labels takes linearly many indexed operations and terminates. This counts exact integer operations and makes no bit-complexity claim.

## 7. Symbolic controls, retained scope and open question

**Inherited positive control.** Use two successive D134 sections with actual quota vector (1,2,1), h=3 and Q=4. Their weighted pair cost is 2 and the split K_step=(h+Q+1)/2=4, within Q. The quotas are symmetric, positive and even in total, with Q=h+1. For the combined size premise take an independently supplied state with n≥2(h+Q+1), so each local n≥h+Q. Start in zero-frontier coordinates. In the first placement the actual lower and upper shifts are 3 and 7, and the output polarity is maximum. In the second placement the actual shifts are 1 and 5, by conjugating D134. Since membership persists their sums are 4 and 12. Thus the combined parameters are A=4, s=8, B=4 and K=8, with preserved input polarity through the two flips. This is exactly the permitted general exterior class. It invokes only the retained composition theorem. The odd first-section family above cannot be such a composition through a D134 state.

**Adverse control.** With A=1 and s≥K, the first gap label c+1 has neither an eligible lower nor an eligible upper host, by Section 2. This rules out the exact exterior width even when the total fresh palettes have the correct cardinalities. The complementary-polarity proposal w=m also fails the actual connected exterior tree test independently of allocation.

**Ordinary-return comparison.** The Director-accepted pilot direct-leaf block preserves old differences under a single affine translation. It provides an ordinary maximum return and one rank-valid intermediate for its fixed topology. In this exact membership-preserving D134 application its old shift has s=0, which fails s≥K for a positive block. This comparison neither supersedes the ordinary block nor uses it as a D134 control. D131's one-section ordinary deficit state and D133's consecutive old-label obstruction retain their own hypotheses. The retained affine suffix reduction suggested eliminating irrelevant old internal structure. Here the smaller named exterior tree accounts for just the high reserve and a separate gap assignment must supply both sides of the crossing threshold.

D134 and D137 give positive single-section mechanisms whose input and output states constrain that one section. D139 and D140 use a boundary leaf, and D141 and D142 study boundary-block or exterior constraints for one section. Neither the opposing-polarity single-section argument nor D142's one-section placement is being applied to a two-section intermediate. The proof uses the actual two-edge spine vu,uw in the exterior forest. D142's unresolved fresh placement remains open. This task establishes a conditional exact reduction for arbitrary declared profiles in the stated two-section embedding class and a parameterized reusable supplier within it. It does not establish arbitrary fresh profiles, independent existence of compatible reduced exteriors generally, or general two-section closure under different states or embedding classes. A general symbolic allocation rule for independently prescribed gap-host quotas and these crossing demands remains a distinct open obligation.
