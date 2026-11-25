# D142 — Variable exteriors on the D141 non-leaf family

## Scope and disposition

Use the independently supplied [D141 non-leaf family](ORDINARY_SPINE_BOUNDARY_BLOCK_SPECTRAL_OBSTRUCTION.md#independently-supplied-non-leaf-adverse-family), with its actual D134 initializer path, seed and first section. A supplied seed of size n0 carries the required maximum frontier. Choose gamma arbitrarily large in the inherited parity class with gamma≥n0+1 and all initializer hypotheses. In its resulting zero-frontier orientation the input has
```
n=4gamma+6,    c=2gamma+2,    d=2gamma+4.
```
The old crossing spectrum at c is [d,n], the noncrossing spectrum is [1,d−1], and both states have exact D134 parameter p=1. Preserve the actual named prefix, witnessing spine and old designated-cut membership.

Append one actual spine vertex w with h≥3 fresh physical centers and positive prescribed terminal quotas totaling Q. Put H=h+Q+1=2K and m=n+H, with n≥H. On the old oriented alphabet choose 1≤a<c, lower exterior A≥0, upper exterior B≥0 and gaps t and s−t, where A+B+s=H and 0<t<s. Translate [0,a−1], [a,c−1] and [c,n] by A, A+t and A+s. All integers are exact and exclude booleans. Fresh roles can use any unused labels subject to actual incidences. Require w to carry an extreme and the output to have the exact D134 p=1 state. Reversed intervals below are empty.

The results are exact old-image admission tests in each cut regime once the returned polarity is forced, necessary fresh-incidence constraints, exterior rigidity in its specified regime and a further missing-weight exclusion. They hold for the declared range of h without a multiplicity bound other than the size admission. Full feasibility in the remaining variable-exterior class and reusable bridge supply remain unresolved.

## Resource identities

Classify each actual old edge by its crossed cuts a and c. W00 is the same-band weight set, P the lower-to-exceptional set, R the exceptional-to-upper set, and W11 the lower-to-upper set. Original injectivity identifies each weight with its incidence. The noncrossing sets satisfy W00⊔P=[1,d−1], and the crossing sets satisfy R⊔W11=[d,n]. By subtracting the two images of the actual endpoints, or using [D139's four-class calculus](ORDINARY_SPINE_TWO_CUT_BOUNDARY_LEAF_BRIDGE.md#general-two-cut-resource-identities), the transformed sets are
```
W00,  P+t,  R+s−t,  W11+s.
```
Each is internally injective. The exact collision test is that all six intersections between different transformed sets are empty. More explicitly, for two different original classes X,Y with respective increments u,v, avoid every pair x∈X, y∈Y with x−y=v−u. The test refers to the actual weight sets. The fresh difference inventory is their exact complement in [1,m] once injectivity holds.

The three occupied label bands are [A,A+a−1], [A+a+t,A+c+t−1] and [A+c+s,A+n+s]. They are disjoint and ordered in [0,m]. Their exact complement is
```
[0,A−1] ⊔ [A+a,A+a+t−1] ⊔ [A+c+t,A+c+s−1] ⊔ [m−B+1,m].
```
The internal gaps have positive lengths t and s−t and are separated by the moved block of length c−a≥1. The initial vertex at oriented label zero maps to A since a≥1. The actual old designated crossing of weight d remains crossing and must obtain weight at least m/2+1=d+K. Its increase is at most s. Therefore s≥K, and A+B=H−s≤K≤n/2=d−1, irrespective of the output polarity.

## Actual old incidence sets of the D141 family

For the preliminary path write N=3gamma, T=(3gamma+1−n0)/2≥gamma+1, and Q0=gamma+2 for the first D134 section. Path labels from the endpoint are j at position 2j and N−j at position 2j+1, with the last odd position 2T−1 occupied by the translated old frontier. The translated seed labels lie within [gamma+1,2gamma]. At preliminary cut gamma, all crossings are precisely the path edges with starting index u=0,...,2gamma−2. The end at even position 2gamma−2 uses the last preliminary small label gamma−1. The rest of the path and the seed have no crossings at that preliminary cut, by the alternating formula and seed bounds. Each preliminary crossing weight is N−u. The first-section split is Q0, so all its terminals are on its pre-complement low side with their centers.

After the first D134 section and its orientation complement, the old high endpoint of a crossing, at N−j, has label N+1−(N−j)=j+1. It is the low endpoint for the designated cut c. Its incident crossing edges along the preliminary path are the adjacent ones with starting indices 2j and 2j+1, restricted to the full crossing index range 0,...,2gamma−2. Every such weight has become N+Q0−u=n−4−u. The four other actual crossings are the connector and the three attachments of the actual current frontier of label zero. Their weights are [n−3,n], and their low endpoint is zero. The first-section terminal edges are noncrossing, on the high side after orientation.

When 1≤a≤gamma, the preliminary path crossing with low label j+1 belongs to R exactly when j≥a−1. This selects precisely the actual edges with starting indices from 2a−2 through 2gamma−2. In particular a=1 includes the entire old path crossing set, while a=gamma leaves exactly the last such edge. None of the four actual frontier incidences is selected because a≥1. Hence
```
R=[d,r],   r=n−2a−2.
```
D141's low-low analysis gives both endpoints of every such noncrossing edge at least gamma. For clarity, after first-section orientation an actual low-low edge must come from a preliminary high-high edge. The preliminary seed is in [gamma+1,2gamma]. A preliminary high-high path edge has small entry at most T−1≤2gamma and large entry N−j with j≥gamma−1, since j≤gamma−2 has both adjacent small entries below the cut. Both preliminary labels are therefore at most 2gamma+1, and complement after the D134 high shift places them at least at gamma. The current frontier is incident to crossings only, and the first section's centers and terminals are entirely high. Thus no P edge exists when a≤gamma.

When gamma<a<c, all old crossing low endpoints lie in [0,gamma], by the preceding actual incidence analysis. Therefore R is empty. D141's witnessed internal path vertex at 2gamma+1=c−1 has its actual neighbor at gamma, with weight gamma+1. This is a P incidence for every cut in this regime. Every P edge has low-low labels within [gamma,2gamma+1], hence weight at most gamma+1. Thus P is nonempty, max P=gamma+1, and [gamma+2,d−1] lies in W00 and remains unchanged. This argument includes a=c−1, the singleton exceptional block.

## Forced polarity and cut bounds

First consider w=0 in the displayed placement. If A=0 the old frontier already occupies zero and its connector would have weight zero. Otherwise the connector has weight A with 1≤A≤K≤d−1. For a≤gamma, P is empty so W00=[1,d−1], and this weight would be repeated. For a>gamma, avoiding W00 requires A∈P. Since max P=gamma+1, its shifted value gamma+1+t is larger than gamma+1. Old-weight injectivity and the unchanged interval [gamma+2,d−1] require gamma+1+t≥d, or t≥gamma+3. For any q∈P, q+t≥1+gamma+3>gamma+1, so the same collision avoidance requires q+t≥d. This gives A+t≥d.

With w=0 the p=1 output cut in placement coordinates is C=m/2−1=c+K. The placed old label c−1 is A+c−1+t and must remain strictly below C. Exact integrality gives A+t≤K≤d−1, contradicting A+t≥d. Thus the placement necessarily has w=m and B≥1.

The next zero-frontier orientation complements the placement about m. Its designated pre-complement cut is
```
C=m+1−(m/2−1)=c+K+3.
```
Membership of the old vertices is preserved exactly when the largest old low image A+c−1+t is below C and the smallest old high image A+c+s is at or above C. Both old groups are nonempty. This is exactly A+t≤K+3≤A+s. The fresh upper-side vertex count is
```
U=(m−C+1)−(n−c+1)=K−3.
```
The upper exterior lies entirely on that side, so 1≤B≤K−3. These are conditions on any full successful return.

For an actual maximum-frontier input, first orient its labels by x↦n−x, then complement the displayed new placement about m to obtain the actual output. The old actual cuts in increasing order are n+1−c and n+1−a. The actual shifts on their three bands are B, B+s−t and B+s, since m−n−(A+s)=B and m−n−(A+t)=B+s−t. Thus both gap increments remain positive in reversed order and the exterior widths exchange. Old and new cut sides both exchange under conjugation, and weights retain the same values. The actual polarity flips in both input polarities.

## Exact old-image tests and side-specific residual spectra

For w=m and the displayed C, call the old image admissible when its labels and weights are injective, its designated vertex memberships persist, and old crossing weights are at least d+K while old noncrossing weights are below d+K. This is exactly the old-incidence compatibility from D139. The conditions here characterize the old image alone under the declared parameter and placement assumptions.

If a≤gamma, W00=[1,d−1], R=[d,r] and W11=[r+1,n]. The old occupied weight intervals are
```
[1,d−1] ⊔ [d+s−t,r+s−t] ⊔ [r+s+1,n+s].
```
They are disjoint because s−t>0 and t>0. The smallest crossing is d+s−t. Thus old-image admission holds exactly with A+t≤K+3≤A+s and s−t≥K, the latter already implying s≥K. The full residual spectrum is
```
[d,d+s−t−1] ⊔ [r+s−t+1,r+s] ⊔ [n+s+1,m].
```
The fresh noncrossing demands are [d,d+K−1]. The fresh crossing demands are [d+K,d+s−t−1], [r+s−t+1,r+s] and [n+s+1,m]. The first crossing interval is empty when s−t=K, and the second has length t. The four frontier weights included in W11 ensure its interval is present even at a=1.

If a>gamma, R is empty, W11=[d,n], and W00=[1,d−1] minus P. With t>0, a shifted weight in P need not ordinarily be above d. For this family, injectivity of max P+t against [gamma+2,d−1] first forces t≥gamma+3, and then every shifted P weight must be at least d by that same unchanged interval, as proved in the polarity argument. Its noncrossing incidence requires weight at most d+K−1. The old shifted crossing threshold requires s≥K. Conversely P+t⊆[d,d+K−1] and s≥K separate it from W00 below d and from old crossings [d+s,n+s] starting at or above d+K. Each class is itself injective. With the exact membership bounds these conditions are necessary and sufficient for the old image. The full residual spectrum is
```
P ⊔ ([d,d+s−1] minus (P+t)) ⊔ [n+s+1,m].
```
The fresh noncrossing demands are P and [d,d+K−1] minus (P+t). The fresh crossing demands are [d+K,d+s−1] and [n+s+1,m]. The first crossing interval is empty at s=K. All set differences use the exact P weights. A further immediate necessary bound in this cut regime is A≤K−gamma, from t≥gamma+3 and the cut inequality. These tests specify occupied and residual resources before any fresh assignment.

## Exterior connectivity when B≤a

Assume B≤a and a full successful return. All old weights are at most n+s. The unused upper band [n+s+1,m] has A+B entries. The connector to w=m from label A consumes m−A=n+s+B within that band.

An internal fresh incidence touching the gaps cannot supply a weight above n+s in this regime. The largest upper exterior to gap difference is at most m−(A+a)=n+s+B−a≤n+s. The largest lower exterior to gap difference is at most A+c+s−1≤n+s−2, using A≤K≤n/2 and c=n/2−1. The largest gap-to-gap difference is at most c+s−a−1, also below n+s. Empty endpoint classes make their bounds vacuous. Both same-exterior differences are at most A−1 or B−1, with each below n+s. Thus the A+B−1 remaining high residual differences must be supplied by exterior-to-exterior edges among the A+B fresh exterior vertices.

The internal fresh section is a tree, so its exterior induced subgraph is a forest. A forest on A+B vertices has at most A+B−1 edges, and equality holds exactly when connected. It follows that all induced exterior edges supply these high weights and the exterior tree is connected. This includes the singleton A=0,B=1. If A=0 and B>1 the only exterior pairs are in one interval and have no high weight, contrary to the required tree.

Any upper-exterior center would have its actual attachment to w inside the upper exterior, with weight at most B−1. The exterior tree thus has no such center. If a fresh exterior vertex is a terminal, its actual host must also be exterior because its unique edge is needed to connect it to w in that tree. A lower-exterior terminal would have a lower-exterior host and too small a weight. Consequently every lower-exterior vertex is a center and every upper-exterior vertex other than w is a terminal of a lower-exterior center.

Suppose B>1. The terminal at m−1 then has a lower center j∈[0,A−1]. When j=A−1 its weight m−1−j=m−A repeats the physical connector. Otherwise j≤A−2 and m−1−j is the actual attachment to the distinct lower-exterior center labeled j+1, since all those positions are centers. This repeats a weight on distinct incidences. Hence B=1 and A≤h. The conditions also allow A=0, where there are no exterior centers and the forest is the singleton w. The gap estimate for the upper exterior depends on B≤a and this rigidity is limited to that regime.

For h=3, A=3 and B=1, s=Q and all centers are lower exterior. All terminals must lie in the gaps, recovering the exact [D141 canonical obstruction](ORDINARY_SPINE_BOUNDARY_BLOCK_SPECTRAL_OBSTRUCTION.md). The necessary rigidity leaves B=1 with A<h, or with A=h and h>3, subject to all other conditions. It leaves B>a to separate treatment without inferring the exterior tree there.

## Actual crossing balance and one further missing-weight exclusion

Let h_U be the number of fresh centers on or above C. Classify each actual terminal incidence by its host and terminal side, writing T_LU, T_UL and T_UU for the respective counts. The old frontier of label A is below C because (A+t≤K+3) and (c≥1). Its connector crosses to w. The high fresh vertices are w, the h_U upper centers, and the upper terminals. Crossing fresh edges are the connector, attachments to the h−h_U lower centers and the terminal incidences of opposite sides. The old crossing count is n/2 by the specified input spectrum and stays fixed. The new crossing count is m/2, so the number of fresh crossing edges is K. Therefore
```
U = 1+h_U+T_LU+T_UU,
K = 1+h−h_U+T_LU+T_UL.
```
Using U=K−3 and subtracting gives h−3=2h_U+T_UU−T_UL. The counts follow actual named attachments and terminals, so the identity holds with arbitrary independently prescribed positive quotas and any admissible h. It supplies a necessary balance of physical roles.

There is a further quantified exclusion for a≤gamma. Put r=n−2a−2 and assume r>A+c−1. The required weight r+s is missing from the old image by its exact residual spectrum. It is also below the connector m−A=n+s+B since r≤n−4 and B≥1. An internal edge supplying it has to touch the upper exterior. Indeed, the gap-to-gap upper bound c+s−a−1 is smaller than r+s by n−c−a−1=d−a−1>0. Lower exterior to gap reaches at most A+c+s−1, smaller by the assumed strict inequality. Same-exterior pairs have weights at most A−1 or B−1, both below d. Thus the edge cannot have both endpoints in the upper exterior either.

Write its upper exterior endpoint as m−j, where 0≤j≤B−1. The smaller endpoint must be
```
m−j−(r+s)=A+B+2a+2−j.
```
It is strictly above the lower exterior and must be in one of the gaps. Consequently the interval [A+2a+3,A+B+2a+2] must intersect the union of the two fresh gaps. If it misses both, this entire parameter regime is excluded without any assignment. When B≤a the exterior result forces B=1, and the incidence providing r+s must be the actual w-to-gap-center attachment at label A+2a+3. Membership in the first gap requires t≥a+4. Membership in the second gap requires t≤2a−2gamma+1; at a≤gamma and t≥1 this requires a=gamma,t=1. These give a further explicit excluded subregion if neither alternative holds. They provide necessary endpoint conditions, and no full fresh assignment follows from them.

## Limits and retained results

D139 and D140 use the named singleton leaf with P empty and R={d}. This differs from the D141 non-leaf input and supports their existing positive domains. D141 retains its complete exclusion for canonical three-center placement on the specified non-leaf family. For the present variable exteriors the exact old-image filters, polarity and necessary fresh-role constraints are proved, with exterior rigidity and the missing-weight exclusions only in the stated regimes. There is no quantified full exclusion of the remaining class and no established fresh-label supplier or reusable bridge on the non-leaf family. In particular, an exact ordinary p=1 return would give a cut state without certifying the specific D141 initializer incidences as the next input.

All uses of independent supply are symbolic consequences of the retained D134/D141 construction with the actual declared initializer edges. The proof has no numerical allocation or placement search. The remaining difficulty concerns coupled fresh edge spectra and physical roles within a rigid one-section return. Changing the crossing-spectrum state could expose different kinds of unused weight sets, but would need independent state supply and an exact return contract of its own. A multi-section transition can instead keep an exact external boundary while allowing a different internal crossing state. Under the strategic stopping condition, the next question should change the composition architecture. D131–D141 retain their exact scopes.
