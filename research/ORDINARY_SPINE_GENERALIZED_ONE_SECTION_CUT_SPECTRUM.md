# D196 — Generalized one-section cut-spectrum transition

Task LCL-ORDINARY-SPINE-GENERALIZED-ONE-SECTION-CUT-SPECTRUM-001. All structural parameters and labels are exact integers. Integer intervals include their endpoints and are empty when reversed. The positive results are suppliers for the stated actual placements and original profiles. The exact local obstructions concern those same placements.

## 1. The generalized state and one-section outer placement

Supply a named graceful lobster prefix with \(n\ge1\) edges, original witnessing spine ending at its actual extreme frontier \(v\), and actual inventories. In minimum-oriented labels \(G(v)=0\) and cut \(1\le c\le n\), require actual crossing differences \([D,n]\) and noncrossing differences \([1,D-1]\), with \(1\le D\le n\). Use \(P(n,c,D)\) for this interface together with the supplied graph, labeling, physical polarity, cut and ordered spine. A label below the cut is lower. A maximum-frontier actual labeling is \(n-G\) with cut \(n+1-c\). The D157 states are the instances \(n=2c+2,D=c+2+\varepsilon\) with \(c\ge1\) and \(\varepsilon\in\{0,-1\}\). Set \(\Delta=D-c\).

Append the actual next original spine vertex \(w\) with \(a\ge0\) indexed children and \(F\ge0\) terminal leaves attached to their actual positive centers. Write \(m=n+a+F+1\). Assign the actual children bijectively to labels \(j\in[0,a-1]\), independently of child order. All indexed terminals go in the gap, and original direct leaves are among these exterior children. Construct temporarily with
\[
 E(G)=a+G+F{\bf1}_{G\ge c},\qquad w=m,\qquad
 \text{terminal at source }i\mapsto a+c+i,\quad i\in[0,F-1].
\]
The old vertices use exactly \([a,a+c-1]\sqcup[a+c+F,a+n+F]\), and the fresh vertices use \([0,a-1]\sqcup[a+c,a+c+F-1]\sqcup\{m\}\). These adjacent bands partition \([0,m]\) and include the old \(v\) at \(a\). This is an exact partition also for \(F=0\), and \(a=0\) has \(F=0\) by the actual topology.

Every gap terminal lies strictly above every child label since \(c\ge1\). The actual terminal difference at parent \(j\) is
\[
 a+c+i-j=D+\pi(i),\qquad
 \pi(i)=i+a-\Delta-j=i+\eta_j.
\]
Old noncrossing edges keep their differences; old crossing edges gain \(F\) by subtraction of the two shifts. The actual connector \(vw\) has difference \(m-a=n+F+1\); each actual child edge has difference \(m-j\) and together they exhaust \([n+F+2,m]\). Since \(D\le n\), the exact used old bands \([1,D-1]\sqcup[D+F,n+F]\) and the exterior bands \([n+F+1,m]\) leave precisely \([D,D+F-1]\) for actual terminal edges. Thus the prescribed labeling is graceful exactly when the terminal images permute \([0,F-1]\), with each leaf at its actual parent. The proof uses no comparison between prefix and section sizes.

## 2. Exact return, physical polarity and local criterion

Take \(0\le k\le F\), with temporary cut \(C=a+c+k\). The old endpoints adjacent to the cut satisfy
\(a+c-1<C\le a+c+F\); all old vertices remain on their respective oriented sides. Every child label is below \(C\), as is \(v=a\). The new frontier \(w=m\) is upper since \(C\le a+n+F=m-1\). In particular \(1\le C\le m-1\). The connector and all child edges cross. A terminal at source \(i\) crosses precisely for \(i\ge k\). If the images of \([0,k-1]\) and \([k,F-1]\) exhaust the same respective intervals, the actual noncrossing and crossing differences are
\[
 [1,D-1]\sqcup[D,D+k-1]=[1,D+k-1],
\qquad
 [D+k,D+F-1]\sqcup[D+F,n+F]\sqcup[n+F+1,m]=[D+k,m].
\]
The first crossing band in the latter union is empty at \(k=F\), and the terminal noncrossing band is empty at \(k=0\). For \(F=0\) both vanish. Conversely, with this physical cut, the upper terminal sources number \(F-k\). For a graceful labeling with a contiguous crossing spectrum, all old and exterior crossing edges are exactly \([D+F,m]\). Hence its \(F-k\) additional crossing differences must be precisely \([D+k,D+F-1]\). The remaining terminal differences must be \([D,D+k-1]\). This gives the necessary band preservation for any successful allocation in this placement at that cut, independently of the construction of the permutation.

For actual minimum input, keep the temporary output and cut \(C\); the old actual lower and upper translations are \(a,a+F\), and the actual output has maximum frontier. For actual maximum input, complement the temporary output at \(m\) and use cut \(m+1-C\). An old actual label \(x=n-G\) below \(n+1-c\) has \(G\ge c\) and is mapped to \(x+1\); if at or above \(n+1-c\) it is mapped to \(x+1+F\). The two reversals preserve actual old membership, and the actual output has minimum frontier. In both cases the next normalized minimum-frontier state is
\[
 P(n',c',D')=P(n+a+F+1,\ n+F+2-c-k,\ D+k).
\]
Here \(2\le c'=m+1-C\le m\) by the bounds on \(C\), and \(1\le D'\le n+F<m\). The actual new spine vertex and every original child and leaf are supplied at their original incidence. Adding the connector and these pendant attachments extends the tree, and the extended actual spine still witnesses distance at most two. The exact local criterion is a permutation using each actual host shift with its specified quota and preserving the two exact bands. For a prescribed output interface, \(k\) also has to give the required normalized cut and threshold. This criterion concerns the declared outer placement.

## 3. Exact unit-sided packet criterion

For a fixed indexed role assignment denote by \(q_u\) the number of actual terminal arrows of displacement \(u\). Each slot \(j\) has its own displacement \(\eta_j=a-\Delta-j\); the shifts are distinct. A zero-quota direct-leaf slot contributes no arrows. Every permutation of a band has zero displacement sum because the sum of its source coordinates equals the sum of its image coordinates.

Suppose every used positive shift is \(+1\). Write \(z=q_0\), taking missing shifts to have count zero. The exact global moment equation is
\[
 q_{+1}=\sum_{r\ge1}r q_{-r}.
\]
A first band can use \(u_r\) of the actual \(-r\) arrows and \(w\) neutrals only if
\[
 0\le u_r\le q_{-r},\quad 0\le w\le z,\qquad
 \sum_{r\ge1}(r+1)u_r+w=k .
\]
Indeed the band moment forces exactly \(\sum_r r u_r\) positive arrows and the band size gives the stated length. Thus necessity uses only the exact counts and the per-band moment, even for a non-packet permutation.

Conversely, for each designated \(-r\) token place one disjoint consecutive interval \([b,b+r]\) within its band. Use \(b\to b+1\to\cdots\to b+r\to b\), consuming one actual \(-r\) terminal and \(r\) actual \(+1\) terminals. Use \(w\) singleton neutral identities in the first band. Assign the complement of the packet counts and neutral count to the second band. By the global moment the second band has exactly its available unit arrows; its lengths sum to \(F-k\). Each packet permutes exactly its own interval, and the consecutive partition exhausts its band. For every actual host, assign the sources it receives in increasing source order to its original terminal indices in increasing order. Each real quota is met and every original positive center or direct leaf has its declared role. In the negative-unit case change signs: \(q_{-1}=\sum_r r q_{+r}\), \(0\le u_r\le q_{+r}\), with the same length equation and bounds on \(w\). Each packet is the reversed cycle on the same consecutive interval, with one \(+r\) arrow and \(r\) arrows of \(-1\).

The empty first or second band selects no tokens there. An all-neutral allocation uses \(w=k\) with \(z=F\); it is the identity. Without a neutral role take \(z=0\). Used nonzero shifts strictly of one sign violate the global moment, including when the opposite unit condition is vacuous. A terminal-free section has all counts zero, \(k=0\), and the empty permutation, even if it has no child. A deterministic integer extractor can traverse the bounded vectors \(u_r\) in lexicographic order, take \(w=k-\sum_r(r+1)u_r\), and stop at the first legal vector; with a legal vector it emits consecutive packets in increasing \(r\) and then the neutral singletons. This is a finite symbolic procedure on counts. No allocation search was run for the controls.

[D134](ORDINARY_SPINE_PIECEWISE_CUT_SPECTRUM_TRANSITION.md) supplies opposed transpositions of equal displacement magnitudes with neutral interiors on its original domain. [D135](ORDINARY_SPINE_GENERAL_DISPLACEMENT_CYCLE_ALLOCATION.md) extracts cycles from a balanced walk and obtains a sufficient packing test; [D136](ORDINARY_SPINE_INTERLEAVED_ROTATION_PACKET_ALLOCATION.md) improves packing via two-magnitude rotations and residual cycles. Their local permutations can be consumed by §§1–2 when their actual shift, quota and two-band premises match. D136’s rotation for magnitudes \(1,r\) is the packet with no unused interior here. Their historical scopes and sufficient packing conditions are retained. For other menus the exact obligation remains a genuine quota-constrained, band-preserving permutation. Global or per-band vanishing moment alone is not claimed sufficient for those menus.

## 4. The four exact one-section D157 domains

Take incoming \(S_\varepsilon\) and require outgoing \(S_{\varepsilon'}\). Thus \(n=2c+2\), \(D=c+2+\varepsilon\), the output size \(m\) must be even, and \(\delta=\varepsilon'-\varepsilon\). Require \(c'=(m-2)/2\), \(D'=c'+2+\varepsilon'\). Since the new temporary frontier is \(m\), its temporary cut is \(C=m+1-c'=(m+4)/2\). This cut must preserve the old physical membership as in §2, so \(k=C-a-c\in[0,F]\). Exactly the terminal sources at and above \(k\) cross, regardless of actual host. Their exact number of prescribed high images forces \(k=D'-D\). The two equations read
\[
 k=\frac{F+7-a}{2},\qquad k=\frac{a+F+1}{2}+\delta.
\]
They give \(a=3-\delta\) and \(k=(F+4+\delta)/2\). Even \(m\) is equivalent to \(F\equiv\delta\pmod2\) at this \(a\); \(k\le F\) is equivalent to \(F\ge4+\delta\), which also guarantees \(k>0\). The shifts are \(a-(2+\varepsilon)-j=1-\varepsilon'-j\). At equality \(F=4+\delta\) the upper band is empty and the whole balanced profile goes into the first band; larger admissible \(F\) gives two nonempty bands.

| Incoming and outgoing phase | Children and exact quota criterion with selectable indexed roles |
| --- | --- |
| Strict to strict | \(a=3\), shifts \(+1,0,-1\), even \(F\ge4\). Require \(q_{+1}=q_{-1}\). There must be \(0\le u\le q_{-1}\), \(0\le w\le q_0\) with \(2u+w=k\). |
| Strict to exceptional | \(a=4\), shifts \(+2,+1,0,-1\), odd \(F\ge3\). Require \(q_{-1}=2q_{+2}+q_{+1}\). There must be \(0\le u_2\le q_{+2}\), \(0\le u_1\le q_{+1}\), \(0\le w\le q_0\) with \(3u_2+2u_1+w=k\). |
| Exceptional to strict | \(a=2\), shifts \(+1,0\), odd \(F\ge5\). All terminals are at the neutral host; the other indexed child is a direct leaf. |
| Exceptional to exceptional | \(a=3\), shifts \(+2,+1,0\), even \(F\ge4\). All terminals are at the neutral host; the other two indexed children are direct leaves. |

The neutral-only cases follow by the moment and have the identity in both bands. For the two signed cases §3 proves both directions, even when some slots are direct leaves. The roles can be tried in a deterministic finite order over original child indices without rearranging the physical incidences. These domains characterize returns in this placement with its actual cut membership.

## 5. Exact original one-center seeds for \(D>c\)

Use one original spine vertex \(v\) and a sole positive center of quota \(q\ge1\), with \(z\ge0\) original direct leaves at \(v\) and \(n=q+z+1\). Let \(1\le c<D\le n\), take \(v=0\), and write \(L\) for the center label and \(U\) for the actual terminal labels. The root edges consume all positive labels outside \(U\) as differences. Gracefulness requires that \(t\mapsto |L-t|\) permute \(U\). Neither \(0\) nor \(L\) belongs to \(U\). An orbit starting above \(L\) would strictly decrease by \(L\) until it hits \(L\) (forbidden) or enters \([1,L-1]\). From this latter interval reflection never leaves it, so there can be no such orbit in a finite permutation. Hence \(U\subseteq[1,L-1]\) is reflection invariant.

Every label of \(M=[c,D-1]\) must be a terminal, since a root incidence at such a label crosses below \(D\). Because \(M\) is nonempty, \(L<c\) contradicts \(M\subseteq U\subseteq[1,L-1]\), and \(L\in M\) contradicts the root incidence. Thus \(L\ge D\). If \(t\in M\) has reflected partner \(p=L-t<c\), the edge at \(p\) crosses with difference \(t<D\). If \(p\ge D\), the edge at \(t\) is noncrossing with difference \(p\ge D\). Both contradict the spectra. Reflection permutes \(M\), which forces \(L=c+D-1\le n\). Outside \(M\) in \([1,L-1]\) the exact disjoint reflection pairs are \(\{i,L-i\}\) for \(1\le i\le c-1\). Therefore \(q=D-c+2t\) with \(0\le t\le c-1\), and \(U\) is \(M\) and exactly \(t\) of the pairs.

Conversely, choose any such pairs and use increasing terminal indices for the sorted \(U\); send the remaining positive labels except \(L\) to the actual direct leaves in index order. Reflection gives terminal differences exactly \(U\). The edge at a low pair member crosses with the high partner as difference at least \(D\), and the edge at its high partner is noncrossing with the low member as difference. Edges at members of \(M\) are noncrossing and exhaust its differences. Root edges outside \(U\) cross exactly for labels at least \(D\), since all of \(M\) is reserved. The full spectra and alphabets follow from these exact partitions. This proves the stated characterization for \(D>c\), with maximum orientation supplied by complement at \(n\) and cut \(n+1-c\). At \(n=2c+2,D=c+2+\varepsilon\), it is the exact [D195 seed theorem](ORDINARY_SPINE_SIZE_INDEPENDENT_LIFT_AND_ORIGINAL_SEED.md). For zero positive centers, the root-extreme star has crossing spectrum \([c,n]\) in normalized coordinates at every valid cut, since every edge is incident to the root. A classification for one-center \(D\le c\) is outside this argument.

## 6. Arbitrary terminal-free runs and a scoped guard

If \(F=0\), all \(a\) actual children are direct leaves, \(k=0\) and the gap condition is empty. The return is \(P(n+a+1,n+2-c,D)\), with flipped actual polarity. For pairs of successive sections, of contributions \(a_1+1,a_2+1\), the second cut is \((n+a_1+1)+2-(n+2-c)=c+a_1+1\). Consequently a run of \(2r\) sections, with odd-position contribution sum \(U\) and even-position contribution sum \(V\), returns \(P(n+U+V,c+U,D)\) in the original actual polarity. For one more section of contribution \(L_{\rm last}=a_{2r+1}+1\), writing \(U,V\) for the complete pairs, the result is
\[
 P(n+U+V+L_{\rm last},\ n+V+2-c,\ D)
\]
in the opposite actual polarity. These are finite successive applications to the actual run. Both assignments preserve all original direct-leaf parents and spine edges. Thus an arbitrary finite terminal-free suffix always extends an incoming \(P\) gracefully, even with odd final edge count and with \(D-c\) negative along the run.

If \(F>0\), \(a\ge1\) and all available shifts are in \([1-\Delta,a-\Delta]\). For \(\Delta<1\) every shift is strictly positive; for \(\Delta>a\) all are strictly negative. The global moment therefore gives the necessary guard \(1\le\Delta\le a\). For a one-center seed of §5 after an odd run, \(\Delta_{\rm out}=c+D-n-V-2=L-n-V-1\le-1\). This excludes a further positive-terminal step in this placement regardless of its quotas. The argument concerns the all-lower-host placement from that supplied seed. Alternatives involving other placements, other seed types, other phase structures, or a two-section transition remain open.

## 7. Infinite even-run bridge

Take \(b\ge3\) and an arbitrary given even-length original terminal-free run with sums \(U,V\). Start on the actual single-child profile \((b+U-1)\) with no direct leaves. Section 5 with \(c=1,n=D=b+U\), \(L=n\), and all terminal labels \([1,n-1]\) supplies \(P(b+U,1,b+U)\). After the run the state is \(P(b+2U+V,1+U,b+U)\). Thus its current \(\Delta=b-1\).

At the next actual section take \(a=b\). The shift is \(1-j\), so the actual hosts \(j=0,1,b-1\) receive respectively \(b-2,\ b+V,\ 1\) terminals. The other \(b-3\) actual children are direct leaves. Set \(F=2b+V-1\), \(k=b+V+1\), and hence \(F-k=b-2\). Assign the packet of length \(b-1\) first, with \(b-2\) unit steps and a closing \(-(b-2)\) step. In the first band finish with \(V+2\) neutral identities; the second band has \(b-2\) neutral identities. Their total equals the neutral quota \(b+V\). Exhaustion of both bands follows from the disjoint packet and consecutive identity parts. Inserting the input and these counts into §2 gives
\[
 m=4b+2U+2V,\qquad c'=2b+U+V-1,\qquad D'=2b+U+V+1.
\]
This is an exact strict return on the actual original and gives a supplier for arbitrarily long even interior runs, including the empty run. The initial and returning sections are the stated profiles.

## 8. Exact control profiles and transport

[Original controls](../evidence/validation/LCL_ORDINARY_SPINE_GENERALIZED_ONE_SECTION_CUT_SPECTRUM_001/ORIGINAL_CONTROLS.json) bind the actual indexed graphs separately before arithmetic placement. Each section \(i\) has original spine vertex \(\mathrm{s}:i\), child \(\mathrm{b}:i:j\), and actual terminal \(\mathrm{l}:i:j:t\) at its original parent. The graph is its actual spine and these indexed attachments. Direct arithmetic on the [placed controls](../evidence/validation/LCL_ORDINARY_SPINE_GENERALIZED_ONE_SECTION_CUT_SPECTRUM_001/NAMED_CONTROLS.json) checks every actual incidence, cut spectrum and resource inventory. For A–F the original controls use the stated child order as numerical slot order for one-section additions, subject to the actual roles from the D194 two-section supplier in F. The D195 strict and exceptional seeds use its original four-edge constructions.

- **A.** Profiles \((2,0,2)\), \((1,0,0,2)\), \((0,5)\), and \((0,0,4)\) are the four rows of §4 in order. Their \((a,F,k)\) are \((3,4,4),(4,3,3),(2,5,5),(3,4,4)\). Use two consecutive transpositions, the negative-unit three-cycle \(0\to2\to1\to0\), or the identities, respectively. Each returns size 12, normalized cut 5, and threshold 7 for strict or 6 for exceptional. The entire terminal band is below the temporary cut in each case.
- **B.** On the strict seed the profile \((2,2,2)\) gives \(F=6,k=5,m=14,c'=6,D'=8\). Use transpositions on \([0,1]\), \([2,3]\) and identities at 4 and 5. For the strict-to-strict candidate \((3,0,3)\), the global moment forces the two quota-three hosts at opposite unit shifts and the zero slot at shift zero. Both bands of lengths 5 and 1 are odd, impossible with no singleton by §3, for every numerical role assignment. A strict-to-exceptional return would require four children. The same balanced role assignment gives generalized returns \(P(14,11-k,3+k)\) at the four even splits \(k=0,2,4,6\), which separate the exact D157 obstruction from general graceful extension in this placement.
- **C.** Seed \((3)\) is \(P(4,1,4)\) from §5 with \(L=4\). Use \(b=4,U=V=0\) and actual \((2,4,0,1)\), with \(F=7,k=5\), beginning with \([0,2]\) for the packet. The return is \(P(16,7,9)\). The seed lies outside the D195 phase domains.
- **D.** Seed \((7)\) gives \(P(8,1,8)\). Use \((0,0),(),(),(0)\), with contributions \(3,1,1,2\), \(U=4,V=3\). The successive states are \(P(11,9,8),P(12,4,8),P(13,10,8),P(15,5,8)\). The actual next profile \((2,7,0,1)\) has \(F=10,k=8\), the packet on \([0,2]\) and all other sources neutral. It gives \(P(30,14,16)\). The odd sizes and negative \(\Delta\) at intermediate states impose no guard on a terminal-free next step.
- **E.** Two actual empty sections from the strict four-edge seed give \(P(5,5,3)\) and \(P(6,2,3)\). The latter is \(S_{-1}\), with \([3,6]\) crossing, \([1,2]\) noncrossing, as in the separate D195 empty-pair return.
- **F.** From the actual maximum-frontier strict seed, use the specified one-section steps and [D194 outbound toggle](ORDINARY_SPINE_BIDIRECTIONAL_PHASE_TOGGLE_SUPPLIER.md) on \((6,2,0),(4,5,0,0)\) via the D195 size-independent lift. The two-section step has \(A=5,B=6,s=15,K=13,T=12\), with the original named companions and signed-anchor allocation. The state and physical cut sequence is as follows.

| Boundary in F | Normalized \(P(n,c,D)\) | Actual frontier polarity | Actual cut | Lower shift, inserted gap from prior boundary |
| --- | --- | --- | --- | --- |
| Seed | \(P(4,1,3)\) | Maximum | 4 | — |
| First one-section | \(P(12,5,6)\) | Minimum | 5 | \(1,3\) |
| Second one-section | \(P(20,9,11)\) | Maximum | 12 | \(2,5\) |
| D194 two-section | \(P(46,22,23)\) | Maximum | 25 | \(6,15\) |
| Fourth step | \(P(54,26,28)\) | Minimum | 26 | \(1,5\) |
| Empty final section | \(P(55,30,28)\) | Maximum | 26 | \(0,0\) |

The final exact differences are crossing \([28,55]\) and noncrossing \([1,27]\); the odd final alphabet is generalized. The stages have downstream \((\text{lower shift sum},\text{gap sum})\) equal to \((10,28),(9,25),(7,20),(1,5),(0,0),(0,0)\) in order. The final labels of the endpoints of the successive original spine connectors are \((42,9),(9,47),(47,6),(6,52),(52,0),(0,55)\) in original spine order. The D194 block’s unfinished literal connector has local labels \((5,46)\) and final labels \((6,52)\). With the opposite initial polarity, the actual cuts are \(1,8,9,22,29,30\), the step lower shifts are \(4,1,5,2,1\), and the inserted gaps are still \(3,5,15,5,0\). The complementary downstream pairs are \((13,28),(9,25),(8,20),(3,5),(1,0),(0,0)\). Each final connector endpoint label is complemented at 55.

## 9. Immutable resource inventories and composition

Let boundary \(i\) in any finite admitted sequence have actual edge count \(n_i\), cut \(C_i\), and first crossing weight \(D_i\). Both §§1–2 and D195 preserve the actual old cut membership, even when a one-section step flips the actual frontier. Let \(A_i\) be the sum of all subsequent actual lower translations and \(S_i\) the sum of all subsequent inserted gaps, zero at the last boundary. Subsequent one-section lower translations are \(a\) for minimum input and 1 for maximum input; a subsequent D195 two-section lower translation is its exterior width \(A\) or \(B\), for minimum or maximum input, respectively. The old upper translation differs from the lower by the corresponding gap \(F\) or \(s\). Therefore at the birth boundary a label \(x\) can be written once with final value \(x+A_i+S_i{\bf1}_{x\ge C_i}\). This is the actual composite, since at each subsequent step the same vertex remains on its actual side. An old edge keeps its difference if noncrossing and gains \(S_i\) if crossing, by subtraction of those shifts on its endpoints. This equality applies to the original connector endpoints at each birth boundary, including the unfinished connector of a D195 block.

The exact installed final label bands at a complete boundary are \([A_i,A_i+C_i-1]\) and \([A_i+C_i+S_i,A_i+n_i+S_i]\), actual lower and upper respectively. The remaining labels are exactly \([0,A_i-1]\), \([A_i+C_i,A_i+C_i+S_i-1]\), and \([A_i+n_i+S_i+1,n_{\rm final}]\), divided at the actual final cut. Installed final difference bands are \([1,D_i-1]\) and \([D_i+S_i,n_i+S_i]\), actual noncrossing and crossing. The remaining differences are exactly \([D_i,D_i+S_i-1]\) and \([n_i+S_i+1,n_{\rm final}]\), divided at the final crossing threshold. For a single section its fresh resources are its exterior and two terminal bands in §§1–2, on the appropriate actual sides. Applying its suffix map to these label bands and adding later gap sums only to its crossing weights gives its exact fresh final bands. For a two-section intermediate boundary use D195's actual named first and remaining resources before applying its suffix map; include the actual later inserted resources in the final complement. For the assigned graph through any original section boundary, the only incidence from its names to the unassigned suffix is the original next spine edge if there is such a section. Its assigned and pending endpoint labels are the ones supplied by the final map, and its difference is counted only when the original edge is placed. The exact actual old-side partitions and both inventories are retained for the controls at their local and final cuts.

Every step places only original named vertices, independently supplies all its required differences, and returns its exact recorded state. Forward planning and backward suffix sums terminate for a finite list, followed by finite emission of original vertices. Conditional suppliers require the exact gap permutations on their own profiles. General initialization, arbitrary compatible positive sections and arbitrary original-spine decomposition remain open.

## 10. Matched odd-run boundary and a discovery question

The frozen odd comparison is \((7),(0,0),(),(0,0),(2,7,0,1)\). Its terminal-free contributions are \(3,1,3\), giving \(P(15,10,8)\) immediately before the receiving section. Its actual child shifts in the declared outer placement are \(6,5,4,3\), so no numerical role assignment can meet the moment. The positive even comparison D has the same initial section, the same receiving section, and the same sizes 15 before reception and 30 after it. Its different original run gives \(P(15,5,8)\) and the proved strict return. These are distinct named original targets; the odd target’s last section is unplaced.

A falsifiable question for separate Owner authorization is whether the frozen odd comparison can reach strict \(P(30,14,16)\) from its recorded normalized prefix with an alternative one-section placement that preserves actual old cut membership and translates each of its two old label bands by a constant. Any exact witness on that named target would answer positively; complete exhaustion or symbolic exclusion in that specified placement class would answer negatively. The equal-size even comparison is the positive control for any such investigation. D196 neither prepares an execution package nor runs this question.
