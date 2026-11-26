# D199 — Partial-safe-cut ranks and an exact three-gap chain supplier

Task LCL-ORDINARY-SPINE-PARTIAL-SAFE-CUT-THREE-GAP-CHAIN-001. The registered parameterized continuation holds with exactly the three prescribed safe-cut hypotheses. Its actual terminal assignments are supplied by a single decreasing chain of step four at the quota-\(p\) host, and identities at the quota-\(q\) host. The old prefix may fail full nesting.

## 1. Partial-safe-cut ranks and maximal robust support

Use an actual connected graceful \(n\)-edge prefix with labels \([0,n]\), \(n\ge1\). Each old difference \(d\) identifies a unique actual edge, and the cuts it crosses are the integer interval \(I_d=[x+1,y]\) for its endpoints \(x<y\). A proper cut \(r\in[1,n]\) is safe when its crossing spectrum is \([D_r,n]\). Every proper cut is crossed by weight \(n\).

Distinct safe cuts have distinct thresholds. If \(r<s\) had the same threshold, their sets of actual crossing edges would be identical because every difference names a unique edge. Every incidence from a vertex with label in \([r,s-1]\) to its complement crosses exactly one of \(r,s\). Such an incidence must exist by connectedness, since the middle label set and its complement are both nonempty. This gives the contradiction.

Any increasing integer embedding into \([0,M]\) has the form
\[
 E(x)=A+x+\sum_{r\le x}g_r,\qquad
 g_r=E(r)-E(r-1)-1\ge0,\quad A=E(0),\quad B=M-E(n),
\]
with proper cuts \(r\) in the sum and \(A,B\ge0\). For arbitrary gap widths, direct subtraction at the old edge gives
\[
 W_d=d+\sum_{r\in I_d}g_r.
\]
If widths are supported on a safe set \(S\), this simplifies to \(W_d=d+\sum_{r\in S,\ D_r\le d}g_r\). Set \(W_0=0\). Then \(W_d-W_{d-1}=1+g_r\) at a selected threshold \(d=D_r\), and is 1 at every unrepresented rank. Distinct thresholds give unique recovery of every width from these jumps. Conversely any sequence of integer jumps at least one, with all jumps one outside the selected thresholds, recovers the widths exactly. The same endpoint calculation proves that, for any legal offset \(A\), the total span is \(E(n)-E(0)=W_n\), with \(A+B=M-W_n\). This proves reversibility and strict old difference order for safe support.

The exact unused labels are the two exterior intervals \([0,A-1]\), \([M-B+1,M]\), and all interiors \([E(r-1)+1,E(r)-1]\). The exact unused old-difference complement is \([W_n+1,M]\) and the intervals \([W_{d-1}+1,W_d-1]\). At each safe cut \(r\) its label interval and the difference interval at \(d=D_r\) each have exactly \(g_r\) cells, including zero. The exterior label count \(A+B\) agrees with the high difference count. These are numerical partitions. The actual supplier in §3 verifies every fresh incidence.

A fixed allowed support guarantees distinct old weights for **all** independent nonnegative widths exactly when every supported cut is safe. Sufficiency follows from strict weight order above. For necessity an unsafe cut contains a crossing weight \(d\) for which \(d+1\) is noncrossing. Such an adjacent pair exists because the set contains \(n\) and fails to be an upper interval. A unit gap at that cut alone thus repeats \(d+1\). For arbitrary coordinated widths, strict original order holds exactly when
\[
 \sum_{r\in I_{d+1}\setminus I_d}g_r
 \ \ge\
 \sum_{r\in I_d\setminus I_{d+1}}g_r
 \quad (1\le d<n).
\]
Indeed the difference of adjacent new weights is one plus the left sum minus the right, and the two sums are integers. This is an exact strict-order characterization. Collision-free vectors may change the old order.

For a concrete distinction, the nonnested Family C in §4 has unsafe cut 2, crossing \(\{3\}\cup[5,n]\), and safe cut 5, crossing \([4,n]\). The unit gap at cut 2 repeats 4. Coordinated unit gaps at 2 and 5 give the strict sequence \((1,2,4,5,7,8,\ldots,n+2)\). A single gap of width \(n\) at cut 2 also gives distinct weights, since the shifted weights are above \(n\) and the unshifted ones at most \(n\). It reverses old ranks 3 and 4.

[D134](ORDINARY_SPINE_PIECEWISE_CUT_SPECTRUM_TRANSITION.md) characterizes a specified single width \(s\) by whether every shifted crossing weight \(d+s\le n\) was already in the crossing set. That criterion admits some widths at unsafe cuts. D199 instead characterizes support robust to every independent width and separately treats coordinated vectors. [D198](ORDINARY_SPINE_NESTED_CUT_RANK_INTERLEAVING.md) is the specialization where every cut is safe, with thresholds a permutation and unconstrained positive jumps. These comparisons make no historical priority claim.

## 2. Exact safe-cut transport through terminal-free sections

For any supplied graceful prefix with minimum frontier \(v=0\), add a new spine vertex with \(a\ge0\) actual direct children and no terminals. In normalized coordinates send the old label \(x\) to \(n+1-x\), put the new frontier at 0 and its direct children at \(n+a+1-j\) for their increasing original indices \(0\le j<a\). The old labels occupy \([1,n+1]\) and their absolute differences are unchanged. The new connector from the old frontier gives \(n+1\), and the direct incidences give every weight from \(n+2\) to \(n+a+1\). This is [D196](ORDINARY_SPINE_GENERALIZED_ONE_SECTION_CUT_SPECTRUM.md)'s normalized terminal-free map, with no safe cut required to verify gracefulness. For actual minimum input use the complementary output with maximum frontier and old shift \(a\). For actual maximum input use the displayed normalized output and the actual old shift 1. Taking the complementary physical representation reflects integer cut coordinates by \(r\mapsto m+1-r\) at size \(m\).

In normalized output every new edge runs from 0 to a label at least \(n+1\). Cut 1 has precisely weights \([n+1,n+a+1]\) crossing. An old cut \(r\in[1,n]\) corresponds to \(r'=n+2-r\), ranging over \([2,n+1]\), and its old crossing set is unchanged by reflection and translation. Every new weight crosses at \(r'\). Thus the new full crossing set is the old set union \([n+1,n+a+1]\). An old safe cut stays safe at its old threshold. An old hole above its least crossing weight remains a hole, so unsafe cuts stay unsafe. Finally every proper \(r'\ge n+2\) crosses exactly \([r',n+a+1]\), because no old label reaches it and only the new high direct children cross there. This is the complete safe-cut update. The last range is empty when \(a=0\). The assignments always use the actual original spine and children, and the update iterates over any finite supplied terminal-free sequence.

## 3. The exact three-gap supplier

Let \(n\ge8\) and append the actual indexed section \((p,q,0,1)\) with \(p,q\ge1,\ p+q=n-6\). The section has four children, \(p+q+1\) terminals and the original connector, totaling \(n\) fresh edges. Assume independently supplied minimum frontier \(v=0\), safe cuts 3 and 4 with thresholds 1 and 2 in either order, and safe cut \(n-1\) with threshold \(n-1\). Put
\[
 M=2n,\qquad E(x)=1+x+{\bf1}_{x\ge3}+{\bf1}_{x\ge4}+(n-4){\bf1}_{x\ge n-1}.
\]
The exterior widths are \(A=B=1\). The old label sequence occupies \([1,n+1]\setminus\{4,6\}\) and \(\{2n-2,2n-1\}\). The old differences, by §1, occupy \(\{2\}\cup[4,n]\cup\{2n-3,2n-2\}\). In particular \(W_1=2,\ W_d=d+2\) for \(2\le d\le n-2\), \(W_{n-1}=2n-3\), and \(W_n=2n-2\). Both orders of the two small thresholds give the same palettes because the two widths are one. At the original cut separating \(x<n-1\), the old crossing weights after placement are \(2n-3,2n-2\).

Place \(w=2n\), with actual children in original index order at \((4,0,6,2n-3)\). The last child is the quota-one center, whose terminal is at \(2n-4\). The connector from \(E(0)=1\) uses \(2n-1\). The child-edge weights in order are \(2n-4,2n,2n-6,3\), and the designated terminal edge uses 1. At physical cut \(C=n+2\), the connector and first three attachments cross. The upper quota-one center and its terminal stay upper with their two noncrossing incidences. Old vertices are split exactly at old cut \(n-1\), since \(E(n-2)=n+1<C<E(n-1)=2n-2\) for \(n\ge8\).

After the placements and old edges, the exact remaining terminal-label and terminal-difference sets are
\[
 R=[n+2,2n-5],\qquad Q=[n+1,2n-5]\setminus\{2n-6\}.
\]
All of \(R\) is upper. Its physical eligible parents are the two remaining lower hosts 4 and 0. At the first host each difference subtracts four from its terminal label, and at the other each difference equals its terminal label. Each parent edge is an actual original incidence. Since \(Q\) removes \(2n-6\) from \(R\) and adds \(n+1\), the exact displacement condition is
\[
 4p=\sum R-\sum Q=n-7 .
\]
Thus \(n=4p+7\), \(q=3p+1\) is necessary within this fixed template.

For these parameters set \(v_j=2n-6-4j\) for \(j=0,\ldots,p\). Then \(v_p=n+1\) and the \(p\) sources \(v_0,\ldots,v_{p-1}\) are distinct in \(R\), the last equal to \(n+5\). Put them at the actual quota-\(p\) host 4. Their exact differences are \(v_1,\ldots,v_p\). Use every remaining source at the actual quota-\(q\) host 0. Each source except \(v_0\) removed from the identity set returns as a chain weight, and the new bottom weight \(v_p=n+1\) substitutes for \(v_0=2n-6\). Thus the exact distinct differences are \(Q\), with actual quotas \(p,q\). Assign sorted labels to each parent's actual terminal indices in increasing order. The construction uses all actual names and neither reassigns a parent nor changes an incidence.

The old noncrossing weights are \(\{2\}\cup[4,n]\) and the fresh noncrossing weights \(\{1,3\}\). The fresh crossing weights are \([n+1,2n]\setminus\{2n-3,2n-2\}\), and the old ones supply exactly those two missing ranks. Every stated crossing predicate follows from physical sides and the old cut. The label inventories are old lower \([1,n+1]\setminus\{4,6\}\), old upper \(\{2n-2,2n-1\}\), fresh lower \(\{0,4,6\}\), and fresh upper \([n+2,2n-3]\cup\{2n\}\). Complementing all labels at \(2n\) gives cut \(n-1\), frontier 0, and identical differences and crossing flags. The normalized output is strict \(P(2n,n-1,n+1)\). The actual connector is \((1,2n)\) in the displayed maximum output and \((2n-1,0)\) in the complementary one. Complementing the input and output gives the corresponding placement and both inventories in the other physical orientation while preserving the actual names. The argument proves necessity and sufficiency within the declared parameters and fixed template.

## 4. Independently supplied input families

**A. Odd-run family.** Use original \((q_0),(0^a),(),(0^b)\), where \(q_0\ge1,\ a\ge0,\ b\ge2,\ q_0+a+b=4p+3\). Start with the one-center minimum seed from D198, with labels \(0,q_0+1,1,\ldots,q_0\), and apply §2 across the next three actual sections. The intermediate sizes are \(n_1=q_0+a+2,\ n_2=q_0+a+3,\ n=q_0+a+b+4\). The first map on initial labels is \(q_0+2-x\), and the composition of the next two normalized maps on these labels adds one. Thus the initial vertices end at \(q_0+3-x\): old root \(q_0+3\), center 2 and indexed terminals \(q_0+2-j\). The next spine vertex ends at 1, its direct children at \(q_0+a+3-j\), the third spine vertex at \(q_0+a+4\), and the final frontier at 0 with direct children \(n-j\).

The seed cuts \(q_0+1,q_0\) have thresholds 1,2 and transport to cuts 3,4. For \(q_0=1\), the second of these is the root-center crossing at cut 1 of weight 2, so the same conclusion holds. Since \(b\ge2\), cut \(n-1\ge n_2+2\) is newly safe in the last step at threshold \(n-1\). The designated input cut from seed cut 1 is \(q_0+3\) with threshold \(q_0+1\). This proves the entire odd-run family, including \(a=0\). The fixed \(a=b=2,q_0=4p-1\) family has exactly D198's original and labels at \(p=2\).

**B. Reversed-threshold seed.** Use the original one-center profile with three terminals and \(n-4\) direct leaves, root zero, center 4, terminals \(1,2,3\) and direct labels \([5,n]\). The weight-one edge crosses cut 4 only. The weight-two interval is \([3,4]\), and higher weights also cross both appropriate cuts by the D198 nested seed proof. Thus cuts 3,4 have thresholds 2,1 respectively. Cut \(n-1\) crosses exactly the last two direct weights. The two small unit gaps work in this order without replacing any name.

**C. Nonnested prefix.** Use original \((0,0),(),(),(),(0^{n-6})\) with the five actual spine labels \(2,4,1,7,0\). The first spine vertex's children are at 3,6, and the last one's children at 5 and \([8,n]\) in that index order. The displayed vertices partition \([0,n]\). The four spine weights are \(2,3,6,7\), the first two attachments use \(1,4\), and the last children supply 5 and \([8,n]\). These exactly exhaust all weights. Their cut intervals for weights 1 through 7 are \([3,3],[3,4],[2,4],[3,6],[1,5],[2,7],[1,7]\). The higher direct weights have intervals \([1,d]\). Therefore cuts 3,4 have thresholds 1,2, cut \(n-1\) has threshold \(n-1\), and the rank-three and rank-four intervals are incomparable. This is an independently supplied nonnested original that enters §3.

## 5. Complete output safe-cut classification for the template

Work first in maximum output coordinates. For a proper cut \(C'\le6\), the attachment of the direct leaf at 6 is noncrossing at weight \(2n-6\). The lowest \(R\) label \(n+2\) is an identity at host 0, since all chain sources are at least \(n+5\). Its weight \(n+2<2n-6\) crosses. For \(C'\ge2n-4\), the direct attachment crosses but the highest label of \(R\), \(2n-5\), is an identity whose own edge is noncrossing. Each of these extremal cut ranges is therefore unsafe.

For \(7\le C'\le n+2\) let \(h=|\{x:E(x)<C'\}|\). This is a proper old cut, in \([4,n-1]\). The fresh crossing set throughout this range remains exactly \([n+1,2n]\setminus\{2n-3,2n-2\}\) by the physical locations of the children and terminals. For safety both high old differences \(2n-3,2n-2\) must also cross. Weight \(W_1=2\) must stay noncrossing because fresh weight 3 is noncrossing. Then the old ranks with weights in \([4,n]\) must cross on precisely an upper rank interval, possibly empty. Conversely these conditions fill the complete output crossing interval. Thus the output cut is safe exactly when \(h\) is old safe with \(2\le D_h\le n-1\). Its threshold is \(D_h+2\) for \(D_h\le n-2\), and \(n+1\) for \(D_h=n-1\).

For \(n+2\le C'\le2n-5=v_0+1\), the old split stays at \(n-1\). Fixed crossing edges give the weights \(\{2n-6,2n-4,2n-3,2n-2,2n-1,2n\}\). The upper quota-one center and its terminal stay upper together and neither of their edges crosses. At \(C'=v_0+1\) the only crossing terminal is the top identity giving \(v_0+1\), so this cut is safe at \(v_0\). At \(v_j+1\le C'\le v_{j-1}\), \(1\le j\le p\), the crossing chain sources are exactly \(v_0,\ldots,v_{j-1}\) with differences \(v_1,\ldots,v_j\). All other crossing terminal labels at or above \(C'\) give identities. When \(C'=v_j+1\), the chain differences replace the missing chain sources in \([v_j+1,v_0+1]\) using the fixed weight \(v_0\), and add \(v_j\). Along with the other fixed edges this fills \([v_j,2n]\). Otherwise \(v_j\) crosses but \(v_j+1\) is absent because it is neither a fixed weight nor a chain weight and is below the identity cutoff. Thus the safe pairs in normalized minimum coordinates on this range are exactly
\[
 (6+4j,\ 2n-6-4j),\qquad 0\le j\le p.
\]
The two central ranges meet consistently at the strict cut. Together with the extremal exclusions this classifies every proper output cut in the exact template. In particular each output supplies new safe gap coordinates in addition to the strict cut. Section 1 applies to any selection of those output coordinates for old-part transport. Admitting fresh terminal incidences at a later arbitrary section remains a separate problem.

For the exact D198 labels, direct subtraction at every one of the 30 proper cuts in minimum orientation gives the following complete safe list:
\[
 (6,24),(10,20),(14,16),(15,14),(16,13),(17,12),\quad
 (r,28-r)\ \ (18\le r\le24).
\]
Every other cut has a hole above its least crossing weight. The exact crossing and noncrossing lists at every cut, with both physical orientation checks, are frozen in the prescribed controls. This also follows from the displayed two ranges and the actual D198 old threshold table. The new minimum cuts 3 and 4 lie in the unsafe extremal range. There is no immediate repeat of the identical D199 shape, and the new size is even. This says nothing about a general positive-terminal closure theorem.

## 6. Admitted repetition and immutable actual transport

The strict output of §3 admits D196's strict-to-strict step on the actual next profile \((2,0,2)\), with \(a=3,F=4,k=4\) and two adjacent transpositions on the lower packet band. Its higher packet band is empty. This follows from D196's actual weights and side test. It can repeat for any given finite number \(k\ge0\) of these sections, since each step returns strict and preserves all old physical memberships at its supplied and returned cuts. After the \(k\)-th repetition the normalized state is \(P(2n+8k,n-1+4k,n+1+4k)\).

Starting with D199's maximum output, each subsequent step has low shift 1 from maximum input or 3 from minimum input. Its high shift adds another 4. Let \(\ell_k=\lceil k/2\rceil+3\lfloor k/2\rfloor\). For any already placed maximum-output label \(y\) the final label is
\[
 y+\ell_k+4k{\bf1}_{y\ge n+2}.
\]
For each initial original label \(x\) this becomes \(E(x)+\ell_k+4k{\bf1}_{x\ge n-1}\), since \(E(n-2)<n+2\le E(n-1)\). It adds the later shifts at precisely the pulled-back old threshold. For the complementary polarity use the reflected cuts and complementary lower shifts \(3,1,3,1,\ldots\). At a later birth boundary the same calculation uses its actual cut and only the remaining shift and gap sums. Thus each name is written once according to its birth map as in D198, while both exact used and remaining resources follow from final endpoint subtraction and actual sides. The first D199 connector keeps its actual original endpoints, reaching labels \(1+\ell_k,2n+\ell_k+4k\). The later connectors use their own birth maps. This is a finite admitted mixed composition, not universal closure.

For the frozen mixed control, \(n=15,k=2\). The successive sizes are \(30,38,46\), with actual port and cut pairs \((30,17),(0,18),(46,25)\) and minimum crossing weights \(16,20,24\). The first connector finishes at \((5,42)\) by direct transport. Its initial old-label map becomes a base increment 5 with gap widths \(1,1,19\) at old cuts 3,4,14. Both polarity inventories at each step and at every final original boundary are supplied in the named record.

## 7. Exact fixed controls and retained scope

The [eight original records](../evidence/validation/LCL_ORDINARY_SPINE_PARTIAL_SAFE_CUT_THREE_GAP_CHAIN_001/ORIGINALS.json) freeze each actual target and its separate prefix graph before identification of new vertex labels. The [prefix records](../evidence/validation/LCL_ORDINARY_SPINE_PARTIAL_SAFE_CUT_THREE_GAP_CHAIN_001/PREFIXES.json) and [placed controls](../evidence/validation/LCL_ORDINARY_SPINE_PARTIAL_SAFE_CUT_THREE_GAP_CHAIN_001/SYMBOLIC_CONTROLS.json) bind all indexed children and terminals and use exact prescribed formulas and endpoint arithmetic.

| Control | Prefix size | Receiving quotas | Chain or scoped result |
| --- | ---: | --- | --- |
| Fixed odd run, \(p=1\) | 11 | \((1,4,0,1)\) | \(16,12\) |
| Fixed odd run, \(p=2\) | 15 | \((2,7,0,1)\) | \(24,20,16\), all exact D198 labels and weights |
| Fixed odd run, \(p=3\) | 19 | \((3,10,0,1)\) | \(32,28,24,20\) |
| \(q_0=1,\ a=0,\ b=6\) | 11 | \((1,4,0,1)\) | Exact independent odd boundary |
| Reversed thresholds | 11 | \((1,4,0,1)\) | Exact reversed seed |
| Nonnested prefix | 11 | \((1,4,0,1)\) | Exact Family C |
| Moment adverse | 8 | \((1,1,0,1)\) | Remaining label sum minus weight sum 1, required 4 |
| Mixed | 15 | \((2,7,0,1)\), then two \((2,0,2)\) sections | \(30\to38\to46\) |

The adverse original uses the B-type seed \((3,0,0,0,0)\) at \(n=8\), with the required three safe cuts. Its receiving placement fails precisely by the moment in §3. Other placements on that original remain open. D197's exact two-translation exclusion and D198's fixed minimum-input \(w=0\) unclassified branch retain their earlier scopes. D198, D197 and D191 numerical lanes remain closed. General fresh-parent allocation and arbitrary original-spine decomposition remain open.
