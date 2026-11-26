# D203 — Consecutive all-positive safe-gap return

Task LCL-ORDINARY-SPINE-CONSECUTIVE-POSITIVE-SAFE-GAP-RETURN-001-PREP.

**SYMBOLICALLY_RESOLVED / NO_EXECUTION_NEEDED.** The exact independently supplied 32-edge D202 Control A does not admit the actual next section (1,1,1,1) through any registered safe-supported increasing embedding with an extreme new frontier and normalized state P(41,c,c+2). Both frontier branches are excluded. The same-size matched actual (4,0,0,0) section admits P(41,20,22) and its prescribed further (1,1,1) section. The scope is the frozen incoming labeling, named original, supported embedding class and requested return relation.

## 1. Fixed input, safe cuts and known restricted obstructions

The admitted independently supplied input original has profiles (0,0),(),(),(),(0,0,0,0,0),(2,12,1,1), 32 edges, frontier s:5 at zero and P(32,20,12). Its graph digest is fd4289cb555097994341bf023415e231841e01e95c1098c7890643252241f061. Retain exactly the committed minimum labels of [D202 Control A](ORDINARY_SPINE_ZERO_DIRECT_LEAF_MULTI_HOST_DETOUR_PATH.md). Before placement, freeze the two original 41-edge targets and their separate 48-edge suffix targets, with the actual indexed (1,1,1) section. The main 48-edge original is frozen for the conditional interface check; no 41-edge main labeling is used for it.

For each old edge with actual endpoints x,y and weight d=|x−y|, its proper crossing cuts are min(x,y)<r≤max(x,y). Direct subtraction at all cuts 1,...,32 gives exactly the safe pairs

    (6,26), (10,22), (14,18), (20,12), (21,11),
    (22,10), (23,8), (25,6), (26,4).

The frozen cut table lists each actual crossing set and its complement, with an explicit gap above the minimum crossing weight for each unsafe cut. In particular all safe thresholds are at least four, occur strictly decreasing in cut order, and the largest supported cut is 26.

In the [D196](ORDINARY_SPINE_GENERALIZED_ONE_SECTION_CUT_SPECTRUM.md) all-lower four-child placement the indexed labels j=0,1,2,3 have one terminal each. The displacement moment is Σ_(j=0)^3 (4−Δ−j)=10−4Δ, impossible to vanish for integral Δ. The exact [D202](ORDINARY_SPINE_ZERO_DIRECT_LEAF_MULTI_HOST_DETOUR_PATH.md) family on the target forces d=0, p=q=s=1 and K0=9. For the standard roles, h+J0=10 differs from K0−7=2, even apart from cut availability. For a geometrically valid relocated role h≥4 with K0≥h+4, only h=4 or 5 is possible. Its required moment 2h+3 differs from K0−h−4=5−h; moreover the required lowest cut h−1 is absent from this input's safe table. These are failures in the respective declared placements.

## 2. Exact embedding and cut brackets

Let S be the listed safe cut set. The registered geometry is a vector of nonnegative integer widths (A,B,(g_r)_(r∈S)) of sum nine. Set unsupported widths to zero whenever a cut outside S is referenced. Let G=Σg_r. By [D199](ORDINARY_SPINE_PARTIAL_SAFE_CUT_THREE_GAP_CHAIN.md), the old coordinate and ordered weight maps are

    E(x)=A+x+Σ_(r≤x) g_r,
    W_d=d+Σ_(D_r≤d) g_r.

Both orders are strictly increasing. The used label and difference palettes are {E(x):0≤x≤32} and {W_d:1≤d≤32}; their respective exact complements in [0,41] and [1,41] are the fresh palettes. Equivalently, a label gap is [E(r−1)+1,E(r)−1] and its paired weight gap is [W_(D_r−1)+1,W_(D_r)−1], with W_0=0. The extra label ends are [0,A−1] and [42−B,41], while the extra high weights are [W_32+1,41]=[42−A−B,41]. Definitions use empty intervals when widths vanish. All widths remain registered, including zero support. In particular W_1=1, W_2=2 and W_3=3.

Write C for the proper physical cut, D for its crossing threshold and h for the number of old labels below C. Exact compatibility means each old edge crosses at C if and only if its new weight is at least D. If 1≤h≤32, the induced old cut is h. By order preservation on weights, the old crossing ranks must then be a nonempty suffix, hence h must be safe. Conversely if h is safe, the exact windows are

    A+h+J_h ≤ C ≤ A+h+J_h+g_h,
    D_h+R_h ≤ D ≤ D_h+R_h+g_h,

where J_h=Σ_(r<h)g_r and R_h=Σ_(D_r<D_h)g_r. The first is the exact integer bracket E(h−1)<C≤E(h), and the second is W_(D_h−1)<D≤W_(D_h). The defined physical state demands D=C+2 for w=0, or D=44−C for w=41. These equations apply to the same C,D as the two exact old-resource brackets.

For proper h the remaining crossing weight count is 42−D−(33−D_h)=9−D+D_h. Let S_w be the number of fresh vertices on w's side, including w, b the number of its four children on that side, and t=S_w−1−b the number of fresh terminals there. Let L count terminals of those b children on the opposite side, and I indicate the actual connector crossing. Crossings contribute I, 4−b from the child edges, L from those b children's terminal edges and t−(b−L) from the other children. The result is I+3+S_w−3b+2L, with 0≤L≤b and 0≤t−b+L≤4−b. These are necessary aggregate constraints. All terminal edges still require their actual endpoint differences.

The following equivalent bookkeeping will be useful. Classify arms by whether the child and its only terminal lie on the side opposite w. Let X count arms with both opposite, Y those with only child opposite, and Z those with only terminal opposite. Let k=2X+Y+Z be the number of fresh vertices opposite w. The arms contribute exactly X+2Y+Z=k+Y−X crossings, or I+k+Y−X including the connector.

If w=0, the vacancy of 0 forces A≥1. Weight 41 can only be between labels 0 and 41. The only possible old neighbor of w has label E(0)=A≤9, so 41 must be fresh and belong to an actual child, forcing B≥1. If w=41, its vacancy forces B≥1. With A=0 its connector realizes 41. With A>0 that connector cannot realize 41 and zero must be an actual child. These conclusions use only original endpoints and the full alphabet.

## 3. Both improper old cuts fail

For h=0 or 33, all old edges are noncrossing, so D>W_32≥32. If w=0, C=D−2≥31. Thus at most 11 vertices are upper and h=0 is impossible with 33 old vertices. If w=41, C=44−D≤11. Thus h=33 is impossible. In the remaining improper cases all old vertices are on w's physical side. In particular I=0. The opposite side is a consecutive extreme label interval of length k, all fresh, and D=44−k for either frontier. The desired crossing count is therefore k−2. Comparing with the arm count gives X−Y=2 and X+Y+Z≤4. The only possibilities are X=2,Y=0 with k=4,5,6, or X=3,Y=1,Z=0 with k=7.

Every one of the X wholly opposite arms requires a terminal difference within that k-cell interval, and the X pairs have disjoint endpoints. Old weights use 1,2,3, so those fresh differences must all belong to [4,k−1] and be distinct. For k=4 or 5 there are fewer than two. At k=6 two pairs would have to realize 4 and 5. The weight-5 pair uses both endpoints of the six-cell interval, whereas every weight-4 pair uses at least one of these endpoints. At k=7 three pairs must use 4,5,6 and the same argument excludes disjoint pairs of weights 5 and 6. This proves failure of the remaining improper cut cases.

## 4. Proper cut with w=0

Put C=A+h+J_h+ell and D=D_h+R_h+omega, with 0≤ell,omega≤g_h. The bracket equality D=C+2 gives

    D_h−h−2=A+J_h−R_h+ell−omega.

The safe thresholds strictly decrease, so J_h+R_h+g_h=G. The right side is in [A−G,A+G]⊆[−6,8] since A,B≥1. The values on the left in the displayed safe order are 18,10,2,−10,−12,−14,−17,−21,−24. Thus h=14 with D_h=18.

The old frontier is below every proper induced old cut, so I=0. Here k=9−(C−14)=23−C and the remaining count 9−D+18=25−C is k+2. It follows that Y−X=2. The arm count gives X=0,Y=2 and k=2,3,4, or X=1,Y=3,Z=0 and k=5. Consequently B≤k≤5, as all B upper exterior labels occupy the side opposite w. This last inclusion also follows directly from C≤E(32) when h is proper.

The A+B strictly high unused differences [42−A−B,41] cannot be old edges. They cannot be the connector, which has weight A. Every other fresh edge of one of these weights must meet a vertex in the upper exterior [42−B,41]. To see this, all fresh labels other than the upper exterior lie in the lower exterior or a supported gap. Each gap ends at E(r)−1≤r+8−B≤34−B. If A≤7 this is strictly less than 42−A−B. If A=8 then B=1 and G=0, so there are no gap labels and the same required incidence follows from the lower exterior labels alone. In either case the lower endpoint of such a high edge is at most A+B−1. Since the first supported cut is 6 and B≤5, every label in [A,A+B−1] is already old. A fresh terminal edge in the high band therefore has its lower endpoint among the A−1 labels [1,A−1]. Its other endpoint is in the upper exterior. The terminal edges have pairwise disjoint endpoints, hence at most A−1 of them can supply high weights. At most B child edges can supply high weights because each such child is in the upper exterior. This supplies at most A+B−1 of the A+B distinct required weights, a contradiction. There is no remaining w=0 branch in the registered D203 question.

## 5. Proper cut with w=41

The old frontier is lower, so I=1. Now k=C−h and the desired fresh crossing count is C+D_h−35=k−κ, where κ=35−h−D_h. Comparing with 1+k+Y−X gives X−Y=κ+1. The listed h+D_h values are 32,32,32,32,32,32,31,31,30. Thus κ≥3, and with only four arms the only possibility is κ=3, X=4,Y=Z=0. All eight fresh child and terminal labels lie strictly below C=h+8. Hence h∈{6,10,14,20,21,22} and D_h=32−h. The connector and all four child attachments cross; all four terminal edges are noncrossing.

The only fresh label at or above the cut is the frontier 41. Thus B=1, every supported gap above h has width zero, and E(h)=C. As A+G=8, the whole h-gap is below C. In the weight bracket R_h=0, and D=44−C=36−h=D_h+4, so g_h≥4. The four fresh noncrossing weights are exactly [D_h,D_h+3], precisely the first four weights of the h-gap. Any earlier label gap has a larger threshold and contributes exclusively crossing weights. All exterior high weights are crossing, and are [41−A,41]. The connector consumes 41−A and the other exterior high weights force every label in [0,A−1] to be a child. This includes the empty set at A=0.

For h=6 or 10, an interval of low labels [0,C−1] cannot realize even the least required noncrossing terminal weight: C−1 is 13 or 17, respectively, and D_h is 26 or 22. At h=14 the required weights 20 and 21 cannot be realized by disjoint terminal pairs among [0,21], by the endpoint argument of §3. It remains to exclude h=20,21,22.

For any earlier supported cut r<h with g_r>0, one has D_r=32−r. The label gap at r is I_r=[A+r+J_r,A+r+J_r+g_r−1]. The weight gap [D_r+R_r,D_r+R_r+g_r−1] must be used by child attachments and therefore reflects at 41 into child labels. Since all support above h vanishes and thresholds decrease, R_r=8−A−J_r−g_r. Substituting shows that those forced child labels form exactly I_r+2. If g_r≥2, the penultimate shifted coordinate is E(r), already old. Hence g_r=1. Then its only shifted coordinate is E(r)+1, which would equal E(r+1) if g_(r+1)=0. So g_(r+1)>0, with r+1≤h. The earlier gaps are thus a consecutive chain of singleton gaps directly before h. Let J be their number. The safe table implies J≤0,1,2 at h=20,21,22 respectively, since 19 is unsafe.

All nonexterior fresh coordinates below C lie between the first gap label A+h−J and C−1=h+7. Their span is 7−A+J≤7,8,9 in the three cases, strictly below the least required terminal differences D_h=12,11,10 respectively. A child in that span cannot reach any terminal label, as every lower exterior position is already forced to be a child. Hence every child must be exterior and A=4. Now g_h≥4 and A+J+g_h=8 force J=0 and g_h=4. The child labels are 0,1,2,3 and terminal labels h+4,...,h+7, regardless of pairing. The sum of the four terminal differences is 4(h+4), but the required sum is 4D_h+6. These are incongruent modulo four, a contradiction. This finishes the w=41 exclusion without any candidate generation.

## 6. Matched positive and conditional continuation

For the actual matched (4,0,0,0) section use the safe pair (14,18), A=4, B=1 and g_14=4. The old map is E(x)=4+x+4·1_(x≥14). New w=41 and its four actual indexed children have labels 0,1,2,3. The first child's four terminal labels in actual index order are 18,19,20,21, giving their actual differences [18,21]. Old differences are [1,17] and [22,36]. The new connector (4,41) weighs 37 and the child edges give [38,41]. Thus labels and weights exhaust their complete alphabets. At C=22, exactly the old crossing weights [22,36], connector 37 and child attachments [38,41] cross. This is maximum orientation with normalized state P(41,20,22). The all-unit proof does not apply across unequal arm quotas.

For any admitted main or matched P(41,c,c+2), take the D196 actual next section (1,1,1) with a=3,F=3,k=0 and Δ=2. The shifts at child labels 0,1,2 in the incoming minimum coordinate convention are +1,0,−1. The two nonzero shifts exchange two gap positions and the neutral uses an identity. The exact D196 formula yields P(48,46−c,c+2). This is an independently constructive interface check, conditional for the frozen main 48-edge original. For the matched actual maximum input, the old actual map is x↦1+x+3·1_(x≥22). The new actual minimum frontier is zero. The child labels in index order are 48,47,46 and their actual terminal labels 25,23,24, yielding weights 23,24,22. The new connector (45,0) weighs 45 and the child weights are [46,48]. The old difference palette is [1,21] union [25,44], with the latter crossing. At actual minimum cut 26, old cut membership transfers to its old side and all seven fresh edges cross. This gives crossing [22,48], noncrossing [1,21] and P(48,26,22). Complementation at the output size verifies both polarities.

The pointwise installed maps into the final minimum orientation on the 32-, 41- and 48-edge cuts are respectively the two actual monotone maps composed, the 41-to-48 map, and identity. Each original edge is checked by subtraction of its named endpoints at each boundary, including the connectors and the exact side changes. The birth records cover only newly assigned original labels; the pointwise records cover whole boundaries. The frozen records keep both label and difference inventories and their physical split and complement, including independent partial snapshots when fresh terminals are pending.

## 7. Analytical bounds and numerical disposition

For completeness, an analytical comparison counts geometries and canonical placements without generating any. A vacant chosen extreme requires one exterior width positive. Subtract one from that coordinate in the eleven-coordinate stars-and-bars model, giving 2·binom(18,10)=87,516 raw geometries with frontier choice. Endpoint forcing restricts w=0 to binom(17,10)=19,448 cases. The w=41 cases with A,B≥1 give the same count. With w=41, A=0,B≥1 the ten remaining coordinates give binom(17,9)=24,310. Thus the endpoint-filtered geometry count is 63,206 prior to other conditions.

The four identical receiving arms of the main original are actual paths (w,b_i,l_i). Simultaneously permuting their center-terminal pairs fixes w and the entire old graph and preserves incidence, weight and cut predicates. This is an existence-only symmetry permitting their center labels to be increasing in original index order. It gives no count of exact named labelings and no analogous quotient across unequal quotas in the matched case. For eight vacancies after placing w, a required opposite-extreme child leaves at most binom(7,3)=35 selected center sets. Otherwise binom(8,4)=70. The resulting upper bound is 2·19,448·35+24,310·70=3,063,060 selected center sets. Each has at most 4!=24 terminal bijections, hence 73,513,440 canonical complete attempts.

On a raw recursive pair traversal with increasing centers, a depth-k state chooses k of eight coordinates as centers and orders k distinct terminals from the remaining 8−k, bounded by binom(8,k)P(8−k,k). The five depths give 1,56,840,3360,1680, of sum 5937. Multiplying by 87,516 gives 519,582,492 raw recursion entries as an analytical upper bound. These bounds precede actual weight compatibility and are independent of runtime. An abstract exact cut-mask approach computes all old-compatible cuts once per geometry. For a chosen pair of endpoints x,y and its actual weight d, intersect the current mask with the cuts where min(x,y)<C≤max(x,y) is equivalent to d≥D(C). Intersections over every new edge preserve precisely the common admissible cuts, without separate allocation traversals. No candidate enumeration, algorithms, benchmarks, official execution proposal or allocation caps are needed for this closed existential question.

D203 preparation used only the proved symbolic exclusions, fixed-input arithmetic and matched controls. Both registered extreme branches are resolved within the safe-supported class. Unsupported-gap or nonmonotone old embeddings, a different supplied labeling, different output states and general consecutive positive-terminal continuation are outside the conclusion. D198's separate fixed minimum-input w=0 branch remains unclassified. All prior accepted scopes, closed numerical lanes and incomplete dispositions are retained.
