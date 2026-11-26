# D195 — Size-independent constructive lift and original one-section seeds

Task LCL-ORDINARY-SPINE-SIZE-INDEPENDENT-LIFT-AND-ORIGINAL-SEED-001. All structural parameters and labels are exact integers and every displayed interval is inclusive, with a reversed interval empty. The theorem below removes the prefix-size comparison from the constructive direction of [D157](ORDINARY_SPINE_ALTERNATING_EXCEPTIONAL_SPECTRUM.md). The incoming phase, supplied connected crossing exterior, exact gap allocation and original named incidences are premises. The exact initializer concerns a single original spine vertex with one positive child center and its original direct leaves. These results compose along declared consecutive sections of the actual spine.

## 1. Constructive lift

Let the original graceful named prefix have \(n=2c+2\) edges, \(c\ge1\), and a witnessing spine ending at its actual extreme frontier \(v\). Orient the labels \(G\) so that \(G(v)=0\), using the complement at \(n\) when needed. Cut \(c\) separates labels below \(c\) from those at least \(c\). Put \(d_0=c+2\). Assume the actual old crossing and noncrossing spectra are \([d_0+\varepsilon,n]\) and \([1,d_0+\varepsilon-1]\), respectively, where \(\varepsilon\in\{0,-1\}\). In particular \(1\le d_0+\varepsilon\le n\) follows from \(c\ge1\) and \(n=2c+2\).

Append the next two original indexed sections at \(u,w\), with \(2K\) fresh edges, \(K\ge1\). For the requested phase \(\varepsilon'\in\{0,-1\}\), set \(m=n+2K\), \(C=c+K\), \(\delta=\varepsilon'-\varepsilon\), \(T=K+\delta\), and \(k=K-A\). The exterior has widths \(A,B\ge1\), gap size \(s\ge0\), \(A+B+s=2K\), \(A\le K\le A+s\), and \(s\ge T\). It is the actual connected induced tree on \(v\) and the declared fresh exterior vertices, including \(u,w\) and every positive center. Its reduced labels exhaust \([0,A+B]\), with \(v=A,w=0\), and the actual reduced exterior differences exhaust \([1,A+B]\), with every edge crossing from \([0,A]\) to \([A+1,A+B]\). All remaining fresh vertices are actual leaves attached to their own exterior hosts. In particular \(u\) is upper because \(vu\) is a reduced crossing edge. The gap supplier assigns a distinct named leaf to each \(i\in[0,s-1]\) with its actual parent and the following difference index:
\[
 \pi(i)=\begin{cases}
 i+A-2-\varepsilon-j &\text{at lower reduced parent }j,\\
 s+b-\varepsilon-i &\text{at upper reduced parent }A+b .
 \end{cases}
\]
Require exact bijective images \([0,s-1]\). Require \(\pi(i)\ge T\) precisely for opposite physical sides, using source side lower iff \(i<k\) and the reduced exterior sides for hosts. There is no comparison between \(n\) and \(2K\).

Place the old labels by \(E(x)=A+x+s\,\mathbf 1_{x\ge c}\). The exact used palettes are
\[
 [A,A+c-1]\ \sqcup\ [A+c+s,A+n+s].
\]
The occupied ends nearest \(C\) obey \(A+c-1<C\le A+c+s\) precisely when \(A\le K\le A+s\). Therefore every old vertex retains its cut side. The complementary palettes in \([0,m]\) are
\[
 [0,A-1]\ \sqcup\ [A+c,A+c+s-1]\ \sqcup\ [n+s+A+1,m].
\]
Keep lower reduced exterior labels and add \(n+s\) to upper reduced exterior labels. The shared \(v\) agrees, since \(E(0)=A\). The exterior vertices are on the required sides since their extreme lower and upper endpoints lie respectively at or below \(A\) and at or above \(n+s+A+1\). Place source \(i\) at \(A+c+i\), lower iff \(i<k\). Its interval, when nonempty, starts above \(A\) and ends below \(n+s+A+1\) by \(n-c+2>0\). This holds even for \(s>n\). These are exact integer decompositions of the entire alphabet with the original vertex names.

For two old endpoints on the same side the old difference is unchanged. For opposite sides it increases by \(s\), since the upper endpoint receives the larger shift. The exact old difference palettes are
\[
 [1,d_0+\varepsilon-1]\ \sqcup\ [d_0+\varepsilon+s,n+s].
\]
Each exterior difference gains \(n+s\) since all its reduced edges cross. Gap endpoint order is fixed by the just-proved bounds. The lower-parent subtraction is \(A+c+i-j\); the upper-parent subtraction is \((n+s+A+b)-(A+c+i)=d_0+s+b-i\). Both are \(d_0+\varepsilon+\pi(i)\), since \(n-c=d_0\). The exact fresh palettes are therefore
\[
 [d_0+\varepsilon,d_0+\varepsilon+s-1]\ \sqcup\ [n+s+1,m].
\]
They complement the old palettes exactly. In the gap \(0\le T\le s\), and the noncrossing and crossing difference bands are \(d_0+\varepsilon+[0,T-1]\) and \(d_0+\varepsilon+[T,s-1]\). The exact noncrossing union with the old band is \([1,d_0+K+\varepsilon'-1]\). The exact crossing union with the shifted old band and expanded exterior is \([d_0+K+\varepsilon',m]\). When \(s=T\) the crossing gap is empty and the shifted old crossing band starts at the output crossing threshold. When \(T=0\), \(K=1,\delta=-1\); \(A,B\ge1\) imply \(A=B=1,s=0\). Conversely, \(s=0\) forces \(T=0\). All formulas still hold at that boundary.

Actual parent attachments and the two original spine edges yield a tree by extending the actual old spine. Every new vertex is at spine distance at most two, and the old spine witnesses that property for the old vertices. The placed \(w=0\), \(m=2C+2\) and the exact spectra give \(S_{\varepsilon'}\). The lift is finite, using one placement per actual name. For maximum orientation complement the entire construction at \(m\). The actual cut is \(m+1-C\), old actual cut \(n+1-c\), and the old label shifts are \(B\) below the old actual cut and \(B+s\) at or above it. Indeed an old minimum-oriented label \(x\) corresponds to \(n-x\), and \(m-E(x)=n-x+B+s-s\mathbf 1_{x\ge c}\). The final frontier is \(m\). Crossing membership and absolute differences are unchanged by complementation, so the proof supplies both physical polarities.

## 2. Physical balance and intermediate inventories

In the fresh tree color \(v,w\) low and \(u\) high, where colors refer to the exterior bipartition relative to \(v\). For each section let \(C_i,D_i,F_i\) count its actual positive centers, direct leaves and terminals. The fresh graph classes have sizes \(N_{\rm low}=1+C_1+D_1+F_2\) and \(N_{\rm high}=1+C_2+D_2+F_1\). Connectedness and exterior crossing identify the graph colors of the exterior with its numerical sides. Among gap edges let \(x\) count lower sources at upper parents and \(y\) upper sources at lower parents. The exact crossing images give \(x+y=s-T\). Upper parents have \(s-k-y+x\) gap children of low graph color, and lower parents have \(k-x+y\) children of high graph color. The fresh exterior contributes \(A\) low and \(B\) high vertices, excluding \(v\). Substitution of \(k=K-A\), \(T=K+\delta\) and \(A+B+s=2K\) gives
\[
 N_{\rm low}=2(A+x)+\delta,\qquad N_{\rm high}=2(B+y)+\delta .
\]
These are necessary for the declared arrangement at any prefix size. They do not force an exterior or an all-leaf gap in a wider placement model.

For the intermediate inventory, partition the actual fresh exterior label and edge-name sets into those installed in section one (including \(vu\), excluding the shared old \(v\) from new labels) and the remainder (including the unfinished original \(uw\)). Denote their reduced label sets by \(V_1,V_2\) and reduced difference sets by \(W_1,W_2\), using the supplied names and actual incidences to define the sets. Write \(P(x)=x+(n+s)\mathbf 1_{x>A}\), and let \(I_1\) be the actual source coordinates of the section-one gap leaves, \(I_2=[0,s-1]\setminus I_1\). For \(j=1,2\), the full fresh inventory of section \(j\), in the final block alphabet, is
\[
 V^{(j)}=P(V_j)\sqcup(A+c+I_j),\qquad
 W^{(j)}=(n+s+W_j)\sqcup(d_0+\varepsilon+\pi(I_j)).
\]
Adding the old inventories to the first pair gives the exact installed resources. The second pair gives the exact complementary resources. The lower part of each \(V^{(j)}\) is \(P(V_j\cap[0,A])\sqcup(A+c+(I_j\cap[0,k-1]))\) and the upper part is its complement there. The noncrossing part of each \(W^{(j)}\) is \(d_0+\varepsilon+(\pi(I_j)\cap[0,T-1])\); the rest crosses. Old sides and old crossing partitions were proved above. The intermediate vertex set is the actual prefix through \(u\), with its exact old and first-section edges. The one unfinished cut between installed and remaining graph vertices is the actual \(uw\), with endpoint labels \(P(\bar u),0\) for reduced \(\bar u\), or \(m-P(\bar u),m\) at maximum polarity. In particular if \(\bar u=A+1\) its maximum-oriented installed endpoint is \(B-1\). Upper and lower label parts swap under complementation; crossing and noncrossing edge parts do not. These sets use the actual exterior roles and gap arrows, including direct leaves or exterior-selected terminals in whichever section contains them.

## 3. Exact one-center original seed

The actual single-section tree consists of the original spine vertex \(v\), a sole positive center of quota \(q\ge1\), its \(q\) indexed terminal leaves, and \(z\) indexed direct leaves of \(v\). Any original child order is allowed. Let \(n=q+z+1=2c+2\), \(c\ge1\), and orient \(v\) to zero. Let \(L\) be the center label and \(U\) the set of terminal labels. The root edges take precisely the positive labels outside \(U\) as differences. Gracefulness forces the terminal differences to exhaust \(U\); \(t\mapsto |L-t|\) is a permutation of \(U\). Neither \(0\) nor \(L\) lies in \(U\). Any member \(t>L\) repeatedly decreases by \(L\) under forward iteration until entering \([1,L-1]\), unless it visits \(L\), which is impossible. After entering \([1,L-1]\) reflection stays there. Such an orbit cannot be a cycle through \(t>L\), contradicting the finite permutation. Thus \(U\subseteq[1,L-1]\) with reflection \(t\mapsto L-t\) preserving it.

For the requested phase put \(D=c+2+\varepsilon\), \(M=[c,D-1]\). Every \(t\in M\) is a terminal label: a root incidence with that label would cross at weight below \(D\). In particular \(L\notin M\). If \(L<c\) all terminals lie below \(c\), contradicting nonempty \(M\subseteq U\). Hence \(L\ge D\). If \(t\in M\) and its reflected partner is below \(c\), the partner's terminal edge crosses with weight \(t<D\). If the partner is at least \(D\), the edge at \(t\) is noncrossing with weight at least \(D\). Both contradict the exact spectra. Therefore reflection permutes \(M\), whose endpoint sum forces
\[
 L=c+D-1=2c+1+\varepsilon .
\]
The rest of \([1,L-1]\) consists of exactly the disjoint reflected pairs \(\{i,L-i\}\) with \(1\le i\le c-1\), whose high values are at least \(D\). Consequently \(U\) is \(M\) together with a chosen subset of these pairs, and \(q=2+\varepsilon+2t\) for some \(0\le t\le c-1\).

Conversely, choose any such subset (the first \(t\) low indices give deterministic choices). Assign the sorted \(U\) to actual terminal indices and the sorted unused positive labels other than \(L\) to actual direct leaves by their original child indices. Terminal differences exhaust \(U\) by reflection. Each low pair member \(i\) has a crossing edge of weight \(L-i\ge D\); the edge at its high partner is noncrossing of weight \(i\). Both endpoints of each terminal edge from \(M\) lie on the upper side and use the reflected weights in \(M\). Each root-edge difference is its outside-\(U\) label, crossing exactly for labels at least \(D\) since all of \(M\) is already reserved. This proves the exact crossing and noncrossing bands, label and difference bijections, and frontier \(v=0\) on the original graph. Complementation gives the maximum frontier \(n\) at actual cut \(n+1-c\).

At fixed \(n=2c+2\), the exact domain is even \(2\le q\le2c\) with positive odd \(z\) for \(S_0\), and odd \(1\le q\le2c-1\) with positive even \(z\) for \(S_{-1}\). The quota upper bounds are equivalent to \(z\ge1\) or \(z\ge2\), respectively, under the phase parities. At the largest quotas, every reflected pair is taken. With no direct leaves neither phase is possible in this topology. With zero positive centers and an extreme root, the root-zero star has exact crossing spectrum \([c,n]\), incompatible with both at \(c\ge1\); complementing preserves this obstruction. At \(n=4,c=1\) the only seed quota options are the strict \((2,0)\) and the exceptional \((1,0,0)\), up to the actual direct-leaf placement order. These are obstructions for the extreme-frontier initialization problem.

## 4. Audit of the size premise and positive transfer

[D157 §1](ORDINARY_SPINE_ALTERNATING_EXCEPTIONAL_SPECTRUM.md) states \(n\ge2K\) as part of the old admission and states \(d_0+\varepsilon\le n\) from size and spectrum. Section 1 above obtains that inequality from \(n=2c+2,c\ge1\) alone. The placement, endpoint order and threshold separate \(n,c\) from local widths; no step needs to upper-bound \(s\) or \(K\) by the old alphabet. D157 §§3–5 use only local formulas for the two leg allocations and check their physical thresholds. Its later composition and initialization impose size admission when choosing or repeating legs. A supplied incoming phase suffices here regardless of the construction of that phase.

[D143 §§1–2](ORDINARY_SPINE_TWO_SECTION_CUT_STATE.md) use \(K\le c+1\) from \(n\ge2K\) in a broader placement analysis. In particular the bounds relating \(B\) to \(c\) and weights incident to the expanded exterior, the inequality \(s-1\le 2K-1<d+K\), and the old proof that the same-side gap lengths lie below \(d\) are size-based. The necessity argument forcing polarity, a connected exterior and the exclusion of gap centers retains its full original hypotheses. Here exterior and leaf-gap completeness are constructive premises. [D134](ORDINARY_SPINE_PIECEWISE_CUT_SPECTRUM_TRANSITION.md) has a separate one-section step with premise \(n\ge h+Q\) and a separate independent initialization. Its theorem and its old path construction retain their written scopes. Neither is needed to produce the single original section in §3.

In each row below the listed positive allocation constructs an exact local supplier in exterior and gap coordinates. Its final palettes are the rule of §1 under the listed phases. Local integer and host admissibility conditions in the cited source are all retained. Nothing in those allocations compares a computed gap index or its host's reduced label with \(n\). Thus, for any actual incoming prefix with those phases, the corresponding positive corollary drops only \(n\ge 2K\).

| Supplier and actual local argument | Additional retained dependence or limit |
| --- | --- |
| [D143 §§3–5](ORDINARY_SPINE_TWO_SECTION_CUT_STATE.md), constructive direction and explicit supplied family | Strict phase, specified actual profiles and former local conditions. Its supplied gap direct leaves are allowed since their parents are exterior. Its necessity and broader classification retain the historical size hypothesis. |
| [D157 §§3–6](ORDINARY_SPINE_ALTERNATING_EXCEPTIONAL_SPECTRUM.md), both legs | Exact named profiles \((2r+1,2t),(2p,4,0)\), \(r\ge2,t\ge1,p\ge t\), respective exterior assignments and phase-specific gap thresholds. The old large-path initialization can still be used where originally applicable. |
| [D188 §§1–5](ORDINARY_SPINE_EXCEPTIONAL_DIRECT_LEAF_SLOT_CONSTRUCTION.md), slot substitution, parity packets, tail and growth | Effective slot geometry, actual sparse hosts, quotas, resident neutral bank, parity-tail and matching restrictions. |
| [D189 §§1–5](ORDINARY_SPINE_EXCEPTIONAL_WHOLE_SECTION_MONOTONE_ALLOCATION.md), ranked gaps and whole-section growth | Actual first host roles, geometry, split and matching, exact empty-bank or bank conditions. |
| [D190 §§1–6](ORDINARY_SPINE_EXCEPTIONAL_MOVABLE_TERMINAL_EXCHANGE.md), movable exchange, variable-origin ranks and growth | Exact selected-terminal names, role-dependent guard, supply and growth conditions, including its single-center cases. |
| [D191 §§3–5](ORDINARY_SPINE_LOW_CAPACITY_STRICT_PHASE_MATCHED.md), local strict boundary family and both matched strict positives | Their actual profiles, exteriors, arrows and strict phase. The separate guard, frozen 584-original corpus and numerical-lane disposition retain their accepted scopes. |
| [D192 §§1–4](ORDINARY_SPINE_STRICT_SIGNED_INDEPENDENT_GROWTH.md), signed defect and one-/two-anchor positive allocations | Strict layout, defect quota interval, named anchors and stated growth conditions. The historical ordered projection is immutable. |
| [D193 §§1–6](ORDINARY_SPINE_STRICT_RESIDUE_TWO_ANCHOR_ECONOMY.md), both positive residue chains and growth packets | Strict layout, exact baseline positive conditions, balanced or anchor-based growth. The fixed-exterior classifications and projection are retained as written. |
| [D194 §§1–7](ORDINARY_SPINE_BIDIRECTIONAL_PHASE_TOGGLE_SUPPLIER.md), outbound signed and reverse neutral allocations | Prescribed phase-dependent actual exteriors, quota, residue, growth and common-toggle constraints including the actual changed-phase threshold. |

The table transports only the verified positive constructions. Every historical size-dependent obstruction, exact classification in a larger placement universe, and frozen evidence disposition remains in its own accepted scope. An incoming state still has to be independently supplied. Matching and physical incidence cannot be inferred from counts or from the existence of a successful labeling of a larger tree.

## 5. Named controls and arithmetic boundaries

The exact named originals are recorded before their labels in [ORIGINAL_CONTROLS.json](../evidence/validation/LCL_ORDINARY_SPINE_SIZE_INDEPENDENT_LIFT_AND_ORIGINAL_SEED_001/ORIGINAL_CONTROLS.json). Their [placed arithmetic controls](../evidence/validation/LCL_ORDINARY_SPINE_SIZE_INDEPENDENT_LIFT_AND_ORIGINAL_SEED_001/NAMED_CONTROLS.json) contain actual incidences, both inventories and direct endpoint differences. An original section at index \(i\) has spine name \(\mathrm{s}:i\), child names \(\mathrm{b}:i:j\) and indexed terminal names \(\mathrm{l}:i:j:t\). An original quota zero denotes its actual direct child without a terminal. All edges are consecutive original spine edges, actual child-to-spine edges, or actual terminal-to-child edges. Reading the graph by these types gives a simple connected tree with the displayed witnessing spine and distances at most two. Intermediate fronts are restrictions of the actual original at the relevant sections.

For the four single-section controls the following are minimum-oriented. The terminal and direct-label lists are in the corresponding original index order.

| Control | Original profile | \(n,c\) | Center | Terminals | Direct leaves | Crossing | Noncrossing | Max cut |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| A strict | \((2,0)\) | \(4,1\) | 3 | 1,2 | 4 | [3,4] | [1,2] | 4 |
| B exceptional | \((1,0,0)\) | \(4,1\) | 2 | 1 | 3,4 | [2,4] | [1,1] | 4 |
| C strict | \((4,0,0,0)\) | \(8,3\) | 7 | 1,3,4,6 | 2,5,8 | [5,8] | [1,4] | 6 |
| C exceptional | \((3,0,0)\) | \(6,2\) | 4 | 1,2,3 | 5,6 | [3,6] | [1,2] | 5 |

The seed frontier is zero in the table and its complement is \(n\). The root differences are exactly the center and direct columns; the terminal differences are the listed terminal columns reflected in the center. The partition at the stated cut gives each band.

| Extension | Incoming seed | \(A,B,s,K,T\) | Output edges and max cut | Phase | Crossing | Noncrossing |
| --- | --- | --- | --- | --- | --- | --- |
| D D194 reverse \((6,2,0),(4,5,0,0)\) | B | \(5,6,15,13,14\) | 30,17 | strict | [16,30] | [1,15] |
| E D194 outbound same profiles | A | \(5,6,15,13,12\) | 30,17 | exceptional | [15,30] | [1,14] |
| F D190 B \((6),(4,0,0)\) | B | \(3,5,8,8,8\) | 20,12 | exceptional | [10,20] | [1,9] |
| F D193 B \((3,3,0),(5,3,0)\) | A | \(5,5,12,11,11\) | 26,15 | strict | [14,26] | [1,13] |
| G D157 \((5,2),(2,4,0)\) | B | \(3,4,13,10,11\) | 24,14 | strict | [13,24] | [1,12] |
| G D157 same profiles | A | \(3,4,13,10,9\) | 24,14 | exceptional | [12,24] | [1,11] |
| H \(() , ()\) | A | \(1,1,0,1,0\) | 6,5 | exceptional | [3,6] | [1,2] |

D and E use \(h=2,p=4,q=5\), reverse Q growth of width one and outbound positive first growth of width one, respectively. Each indexed target uses its own original seed. F exceptional uses five neutral L identities and three Q H-to-L identities at indices 5,6,7 with fold 12; its selected first terminal has reduced label 5 and both second direct leaves are exterior at 7,8. F strict uses D193 separation two with \(h=2,\gamma=4,d=5,e=4,J=15\), all three P sources on H at indices 4,6,8. G uses D157 parameters \(r=2,t=1,p=1\). In actual branch order first quota five, first quota two, second quota two, second quota four, the reverse source sets are \(\{0,1,2,3,6\},\{4,11\},\{5,12\},\{7,8,9,10\}\); outbound sets are \(\{0,1,2,3,9\},\{5,12\},\{7,8\},\{4,6,10,11\}\). The reduced first labels by quota are \(2,1\) on the reverse and \(1,2\) on the outbound; the second roles have labels 5,6 and the direct leaf 7. H has actual reduced path \(v,u,w\) with labels \(1,2,0\) and weights \(1,2\), and is the \(s=T=0\) case of §1. The reverse under this geometry would require \(T=2>s\), so the shifted old crossing threshold fails. The H control supplies one empty two-section block in this direction.

For I, start with B and append the actual D194 blocks \((h,p)=(2,4),(4,4),(8,26)\) using reverse, outbound and reverse allocations. The original section edge contributions in order are \(4,12,14,20,20,36,54\). Thus the seven-section spine ends at \(\mathrm{s}:6\) and the arithmetic is:

| End | Edges | Incoming edges for block | Fresh size | \(A,B,s,K,T\) | Phase | Max cut | Crossing | Noncrossing |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Seed | 4 | — | — | — | \(S_{-1}\) | 4 | [2,4] | [1,1] |
| Block 1 | 30 | 4 | 26 | \(5,6,15,13,14\) | \(S_0\) | 17 | [16,30] | [1,15] |
| Block 2 | 70 | 30 | 40 | \(9,10,21,20,19\) | \(S_{-1}\) | 37 | [35,70] | [1,34] |
| Block 3 | 160 | 70 | 90 | \(17,18,55,45,46\) | \(S_0\) | 82 | [81,160] | [1,80] |

Widths of the reverse Q growth are one and nine; the outbound uses the companion baseline with \(\rho=1\), \(q=7,p=4\), and one positive growth column from its common Q pair. This supplies every actual block under exactly its local role, quota, phase, and geometry conditions. Each fresh size exceeds its actual incoming prefix size.

## 6. Immutable transport and finite composition

Keep maximum orientation across the finite sequence. At each block all old physical cut memberships are preserved. After the admission at prefix boundary \(i\), let \(U_i\) be the sum of the actual later \(B\)'s and \(V_i\) the sum of the actual later \(s\)'s, and let \(c_i^{\max}\) be that boundary's actual cut. A label \(x\) assigned at that boundary has final value
\[
 x+U_i+V_i\mathbf 1_{x\ge c_i^{\max}} .
\]
Indeed every later step adds \(B\) or \(B+s\) according to that same physical side. An edge already present then keeps its weight if noncrossing and gains \(V_i\) if crossing. This follows by endpoint subtraction because the order is preserved, even across the cut. The analogous minimum-oriented transport uses later \(A\)'s and the minimum cut. At each intermediate stage use §2's installed and pending resources for the current block, transformed by this map, with the actual later inserted bands as the remaining resources. The equation gives both final numerical labels and exact edge differences without reassigning an earlier original name in the final alphabet.

For I the pairs \((U_i,V_i)\) are \((34,91),(28,76),(18,55),(0,0)\) from seed through final block. The five original seed vertices have final values 129 for the spine, 36 for the center, 37 for its terminal, and 35,34 for the indexed direct leaves. The local connector endpoint pairs \((5,30),(9,70),(17,160)\) transport to \((33,134),(27,143),(17,160)\), with actual weights \(101,116,143\). The final extreme frontier is 160. In the maximum final alphabet, the exact installed sets immediately after each first section are:

| First-section boundary | Installed labels | Installed differences |
| --- | --- | --- |
| I1 | [32,37] ⊔ [121,122] ⊔ [124,132] | [1,6] ⊔ {8,11} ⊔ [93,100] |
| I2 | {22} ⊔ [27,44] ⊔ {46,110} ⊔ [112,141] | [1,23] ⊔ {25,27} ⊔ [91,115] |
| I3 | [16,54] ⊔ [82,95] ⊔ [105,158] | [1,39] ⊔ [49,55] ⊔ [70,76] ⊔ [90,142] |

The remaining sets are their complements in [0,160] and [1,160]. Split the labels at 82 and the actual differences at 81 to get the physical cut partitions of both inventories. The named evidence gives both polarities and the exact endpoints. Each local exterior and gap allocation is obtained on the given named original, so no padding is used. A finite given list of supplied blocks, including an empty list, terminates by induction because each step places finitely many original names using exact arithmetic. Deterministic local extraction uses the cited indexed assignments and any required finite arithmetic matching of original roles within those scopes. Arbitrary decomposition, broader initialization and arbitrary empty runs remain separate obligations.
