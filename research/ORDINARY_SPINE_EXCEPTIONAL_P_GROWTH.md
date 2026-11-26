# D171 — Unbounded P-growth and complete additional inventory classification

Task LCL-ORDINARY-SPINE-EXCEPTIONAL-P-GROWTH-001. Base checkpoint 09887e1569f5ee41ebda921dc753cd509428ff7a. D170 is Director accepted within its written scope. D171 is proved and pending Director review.

## 1. Exact scope and exterior

Use the [D157](ORDINARY_SPINE_ALTERNATING_EXCEPTIONAL_SPECTRUM.md) connected crossing-exterior, leaf-only gap arrangement and independently supplied named \(S_{-1}\) prefix. The actual extreme \(v\) is oriented to \(G(v)=0\), with \(n=2c+2,\ d=c+2\), cut \(c\), crossing weights \([d-1,n]\), and noncrossing weights \([1,d-2]\). A label equal to the cut is on the upper side. Parameters are exact integers and intervals are inclusive, with an empty interval when its upper endpoint is smaller.

Append the two actual sections at \(u,w\). Inventory A is \((1,1,4,4)\) and inventory B is \((1,2,3,4)\), in every original first branch order and with no first direct leaf. The second section has two positive centers of full quotas \(p,q\), odd sum \(R=p+q\), and its sole actual direct leaf at \(w\). Either original second-center order is permitted. Write \(F=10\) for the first terminal total. The fresh vertices comprise the two spine vertices, six centers, one direct leaf and \(F+R\) terminals, so \(2K=R+19,\ m=n+2K\), with individual admission \(n\ge2K\). The alternation along the actual spine puts \(w\), the four first centers and the \(R\) second terminals in the lower graph class. The other fresh class comprises \(u\), the two second centers, the sole direct leaf and the ten first terminals. Their sizes are \(5+R\) and 14.

Use the [D167](ORDINARY_SPINE_EXCEPTIONAL_RESERVATION_SEMILINEAR.md) and [D170](ORDINARY_SPINE_EXCEPTIONAL_ROLE_MENU_COVERAGE.md) exterior with lower and upper widths \(A=6,B=4\) and \(s=2K-10\ge K\). The reduced labels at \(v,u,w\) are \(6,7,0\). The first roles \((b,a,c_1,Z)\) have reduced labels \((2,3,4,5)\) and the second roles \((Q,P)\) have labels \((8,10)\), with full quotas \(q,p\) respectively. Use the first actual indexed terminal at \(a\) for reduced label 9 and the first at \(P\) for reduced label 1. The direct leaf remains in the gap. The residual quotas at \(P,Q\) are \(p-1,q\); at \(a\) remove exactly one from its full quota. The selected terminals exist by positivity. The actual original edges \(vu,uZ,uc_1,ua,ub\), and the first selected terminal edge have reduced weights \(1,\ldots,6\) in that order. The remaining exterior edges \(uw,wQ\), the second selected terminal edge, and \(wP\) have weights \(7,8,9,10\). Each crosses the reduced cut between 6 and 7. They form a connected tree on exactly the labels \([0,10]\) and retain their original endpoints. The numerical role assignments select unused actual centers of the specified quotas, breaking ties by original branch index.

## 2. Fold and common lower-to-upper allocation

Let \(C=c+K,\ k=K-6=(R+7)/2,\ s=2k+2,\ J=s+3=2k+5\). Lift a reduced label above 6 by adding \(n+s\). For gap source \(i\in[0,s-1]\) the actual oriented label is \(6+c+i\), lower at the return cut iff \(i<k\). Subtracting the expanded endpoint gives weight \(d-1+\pi(i)\). At a lower host of reduced label \(r\), \(\pi(i)=i+5-r\); at an upper host of reduced label \(r\), \(\pi(i)=s+r-5-i\). A crossing weight must have \(\pi(i)\ge K\) under the exact return. Physically the edge crosses iff the source is below the cut and the host is upper, or the source is upper and the host lower.

Use \(L_j=j,H_j=J-j\). The source rows \(L_{[0,k-1]},H_{[4,k+5]}\) are the two numerical bands \([0,k-1],[k,s-1]\). The destination rows \(L_{[0,k+5]},H_{[4,k-1]}\) are \([0,K-1],[K,s-1]\). Each pair partitions its own alphabet. The lower hosts \(b,a,c_1,Z,w\) with shifts \(3,2,1,0,5\) translate \(L_j\) to \(L_{j+\delta}\) and \(H_j\) to \(H_{j-\delta}\). Host \(Q\) exchanges rows at identical indices, while \(P\) sends \(L_j\) to \(H_{j-2}\) and \(H_j\) to \(L_{j+2}\). The maps follow from the computed image rules. Each arrow is legal only within its destination row. These bounds enforce exactly the physical crossing predicate.

Let \(x\) count lower gap sources at upper hosts and \(y\) upper sources at lower hosts. A fresh lower graph-class vertex is either a lower exterior vertex or a gap leaf at an upper host. The \(s-k\) upper sources include \(y\) leaves at lower hosts. Likewise the upper graph class counts the \(B\) upper exterior vertices and leaves at lower hosts. Counting gives
\[
5+R=6+x+(s-k-y),\qquad 14=4+y+(k-x).
\]
Exactly \(s-K\) gap weights cross, so \(x+y=s-K\). Substitution gives \(5+R=2(6+x),\,14=2(4+y)\), hence \(x=k-7=(R-7)/2,\ y=3\), and \(k\ge7\) is necessary. The first four numerical images force their equal sources \(L_0,\dots,L_3\) at \(Z\). Indeed upper-host images are at least four, and a positive lower shift to one of the four images would reuse an earlier forced source. The neutral role exhausts its quota four. Six lower-host gap assignments remain, including \(w\), exactly three in each source row by the counts.

For each minimum-Q construction below their lower indices are \(X=\{4,5,6\}\). Their upper image indices are \(Y'=\{4,k-2,k-1\}\). The indices in \(Y'\) are distinct even at \(k=7\). The remaining lower sources \([7,k-1]\) and upper images \([5,k-3]\) differ by exactly two and are empty together at \(k=7\). Use \(P\) for every remaining lower source, so \(N_{PL}=k-7\) and no lower source is assigned to \(Q\).

## 3. Four unbounded minimum-Q constructions

For even \(p\ge4\) use \(q=3,\ p=2k-10\). For odd \(p\ge3\) use \(q=4,\ p=2k-11\). Both require \(k\ge7\). The indicated upper and lower rows are source rows. In all cases \(H_{k+2}\) is attached at \(b\) and \(H_{k+3}\) is the actual direct leaf at \(w\).

| Case | Full \((b,a,c_1,Z)\) | Hosts of \(L_4,L_5,L_6\) | Additional H reservation | \(X'\), the lower image indices of \(X\) | \(Y\), the upper source indices |
|---|---|---|---|---|---|
| A-even | \((1,1,4,4)\) | \(c_1,c_1,c_1\) | \(H_5\) at \(c_1\) | \(\{5,6,7\}\) | \(\{5,k+2,k+3\}\) |
| A-odd | \((4,1,1,4)\) | \(c_1,b,b\) | \(H_7\) at \(b\) | \(\{5,8,9\}\) | \(\{7,k+2,k+3\}\) |
| B-even | \((1,3,2,4)\) | \(c_1,c_1,a\) | \(H_6\) at \(a\) | \(\{5,6,8\}\) | \(\{6,k+2,k+3\}\) |
| B-odd | \((1,3,2,4)\) | \(c_1,a,a\) | \(H_5\) at \(c_1\) | \(\{5,7,8\}\) | \(\{5,k+2,k+3\}\) |

The lower translations give precisely the displayed \(X'\). In the upper row the fixed source maps to \(H_4\), \(H_{k+2}\) to \(H_{k-1}\), and \(H_{k+3}\) to \(H_{k-2}\). These are \(Y'\) and are all in the crossing image row. The fixed source index \(f\) in each row of the table is at most 7, before \(k+2\ge9\), and all three sources lie in \([4,k+5]\). All \(X'\) indices lie in \([4,k+5]\) since \(k+5\ge12\), and are disjoint from the neutral images at 0 through 3. The row bounds and distinctness hold at \(k=7\), even when an index belongs to different endpoint classes. After removal of \(a\)'s selected terminal and the four neutral cells, the remaining counts \((b,a,c_1,w)\) are \((1,0,4,1),(4,0,1,1),(1,2,2,1),(1,2,2,1)\), respectively, exactly as used by the table. The direct leaf source is \(i=J-(k+3)=k+2\) and its image is \(J-(k-2)=k+7=K+1\), a crossing image at the actual \(w\) incidence.

### Exact upper-to-lower parity-path repairs

The common H→L index interval is \([4,k+5]\), with missing sources \(Y\) and missing destinations \(X'\). On each parity path, a missing destination \(z\) paired to a missing source \(x\ge z\) is repaired by assigning the existing sources \(z,z+2,\ldots,x-2\) to \(P\), moving them by \(+2\). This realizes the D167 recurrence: if \(S_j,D_j\) indicate source and destination presence and \(B_j\) indicates the forward P move, \(D_j=S_j-B_j+B_{j-2}\). On a nonempty repair the move bits begin at \(z\), continue through \(x-2\), and stop at \(x\). Interior destinations each receive their preceding source, \(z\) receives none and \(x\) receives the last source. If \(z=x\) the shared missing cell has both incident bits zero. Away from repair intervals and common holes, the identity \(Q\) arrow gives \(D_j=S_j=1\). Thus the recurrence holds at all endpoints with zero flow outside the row, provided the repairs avoid common holes and other missing cells. The corresponding reverse scan implements the L→H arrows already partitioned in Section 2.

The following table lists \((z,x)\) on the moving even and odd paths, and the fixed event, for both parities of \(k\).

| Case | Fixed event | \(k\) even, even and odd moving pairs | \(k\) odd, even and odd moving pairs |
|---|---|---|---|
| A-even | common 5 | \((6,k+2),(7,k+3)\) | \((6,k+3),(7,k+2)\) |
| A-odd | odd repair \((5,7)\) | \((8,k+2),(9,k+3)\) | \((8,k+3),(9,k+2)\) |
| B-even | common 6 | \((8,k+2),(5,k+3)\) | \((8,k+3),(5,k+2)\) |
| B-odd | common 5 | \((8,k+2),(7,k+3)\) | \((8,k+3),(7,k+2)\) |

The two moving source endpoints are consecutive, at least 9, so both moving pairs preserve parity and have \(x\ge z\), including equality for the moving odd pair of A-odd at \(k=7\). Other holes on each path are earlier: the A-even and B-odd common odd hole 5 precedes the moving odd path, and the B-even common even hole 6 precedes its moving even path. In A-odd the fixed odd repair ends at 7, before the later odd repair at 9. Moving paths of opposite parities have disjoint indices; the fixed repairs and barriers are disjoint from all moving intervals on their own parity. The recurrence therefore covers every surviving cell exactly once. All surviving H sources outside these repairs use \(Q\).

### Counts, moments and growth

The number of shifted sources on a pair is \((x-z)/2\). In A-even the H count is \((2k+5-6-7)/2=k-4\). In A-odd it is \((7-5)/2+(2k+5-8-9)/2=k-5\). In B-even it is \((2k+5-5-8)/2=k-4\), and in B-odd it is \((2k+5-7-8)/2=k-5\). The H row has \(k+2\) sources and three reservations are removed, leaving \(k-1\). Hence the remaining \(Q\) count is 3 in the even cases and 4 in the odd cases. Combining directions, \(N_P=2k-11=p-1\) for even \(p\) and \(N_P=2k-12=p-1\) for odd \(p\). The selected exterior terminal completes \(P\)'s quota.

For an independent index-sum check, the two residual bijections give \(2N_{PL}=\sum Y'-\sum X\) and \(2N_{PH}=\sum Y-\sum X'\). Adding gives \(N_P=\sum Y-\sum X-D/2\), where \(D\) sums the six nonneutral displacements. The four displacement sums are \(12,18,14,14\), respectively. Since \(\sum X=15\) and \(\sum Y=f+2k+5\), the identity gives the same two counts. This check follows the path proof and does not substitute for it. The crossings are exactly \(x=k-7\) lower sources at \(P\) and \(y=3\) H reservations at lower hosts. They sum to \(k-4=s-K\).

Increasing \(p\) by two at its corresponding minimum \(q\) advances \(k\) and the two moving H source and image indices by one. The formulas give a new complete assignment, with parity pairing allowed to exchange. Thus old residual arrows need not persist. Increasing \(p\) by four advances them by two and preserves the parity pairing. For \(k\ge17\), the gap from the largest fixed marked column (including the anchor at 4, at most 9) to the first moving column \(k-2\) has length at least six. Its open interior has no endpoint or tail anchor. In L→H the two moving paths go from holes 5 and 6 to the two destination holes \(k-2,k-1\), with the common hole 4 below them. Both are active in the long gap. In H→L both moving paths start at fixed destination holes and end at \(k+2,k+3\), and all fixed repairs end before the gap. Thus both parity paths in both directions are active there. D167's internal two-column insertion adds four P assignments and leaves \(q\) unchanged, recovering the \((4,0)\) generator on these reservations. The direct formulas cover \(7\le k<17\) as well and need no long gap initially.

## 4. Explicit small-quota boundaries

For \((p,q)=(1,6)\) or \((2,5)\), \(k=7\) and \(J=19\). Each case uses \(Z\) at \(L_0,\ldots,L_3\) and all three remaining L sources at lower hosts. The H sources are \(H_{[4,12]}\), the crossing images are \(H_4,H_5,H_6\), and the residual H→L interval is \([4,12]\) with the holes shown.

| Case | Full \((b,a,c_1,Z)\) | Hosts of \(L_4,L_5,L_6\) | H reservations | \(X'\) | \(Y\) | P repair |
|---|---|---|---|---|---|---|
| A, \(p=1\) | \((4,1,1,4)\) | \(b,b,b\) | \(H_9:w,H_8:b,H_7:c_1\) | \(\{7,8,9\}\) | \(\{7,8,9\}\) | none |
| A, \(p=2\) | \((1,1,4,4)\) | \(c_1,b,c_1\) | \(H_{10}:w,H_7:c_1,H_5:c_1\) | \(\{5,7,8\}\) | \(\{5,7,10\}\) | \(H_8\to L_{10}\) |
| B, \(p=1\) | \((1,3,2,4)\) | \(a,a,b\) | \(H_9:w,H_7:c_1,H_6:c_1\) | \(\{6,7,9\}\) | \(\{6,7,9\}\) | none |
| B, \(p=2\) | \((1,3,2,4)\) | \(b,c_1,a\) | \(H_9:w,H_8:a,H_6:c_1\) | \(\{6,7,8\}\) | \(\{6,8,9\}\) | \(H_7\to L_9\) |

The H image indices in the listed source order are \((4,5,6),(5,6,4),(4,6,5),(4,6,5)\), by the physical shifts. They consume the whole crossing row, including the direct leaf's crossing from \(w\). The displayed lower-host uses are respectively \((b,a,c_1,w)=(4,0,1,1),(1,0,4,1),(1,2,2,1),(1,2,2,1)\). These are the quotas after selecting one terminal at \(a\) and accounting for the four separate \(Z\) cells. The L image sets are distinct and disjoint from the four neutral images. When \(p=1\), equal hole sets allow identity at every surviving H source. When \(p=2\), the indicated single P arrow fills the unmatched destination and all other surviving sources use identity. The common holes are outside the moving repair. There are six residual H sources, so \(P\) uses \(p-1\) and \(Q\) uses \(7-p=q\). The crossing counts are \(x=0,y=3\). All source and destination cells are used once even when a host's residual quota is zero.

The rows match D170's saved target-0129, target-0132, target-0237 and target-0240, respectively. The saved-record check binds their original records, archived member identities and actual assignments without a checker replay. These explicit tables are historically extracted controls. Their use here rests on the incidence and partition proof above, independently of the correctness of the archived labeling runs. [Custody and control bindings](../evidence/validation/LCL_ORDINARY_SPINE_EXCEPTIONAL_P_GROWTH_001/CUSTODY.json)

## 5. Exact classification for both inventories

For the fixed template, \(R\ge7\) follows from the crossing count in Section 2. The accepted D167 right-end argument excludes \(q<3\) for these two inventories. The source \(H_{k+5}\) must go to \(Q\) for \(L_{k+5}\), since the P image is out of range and the largest lower shift, five, is insufficient to reach the H destination row. If neither \(H_{k+4}\) nor \(H_{k+3}\) uses Q, then the former must use \(w\), the only eligible lower host, and the latter has no unused \(w\) leaf or permissible P image. Thus at least two Q uses are required. If \(q=2\) these exhaust Q and its two images are at the right. The least available P image is 6 because its numerical reflection is \(s+5-i\). All lower shifts are nonnegative. The first six numerical destinations must then be supplied by their six equal sources at the only neutral host \(Z\), by the same increasing induction as for the first four. This would require \(\alpha_Z\ge6\), exceeding the maximum first quota four. The argument applies across all first-role selections on this template.

For sufficiency the least admissible opposite-parity \(q\) subject to \(q\ge3\) and \(R\ge7\) is 6 for \(p=1\), 5 for \(p=2\), 4 for odd \(p\ge3\), and 3 for even \(p\ge4\). Sections 3 and 4 give every such base. For \(q=q_0+2j\) with integer \(j\ge0\), apply the [D170 Q-tail rule](ORDINARY_SPINE_EXCEPTIONAL_ROLE_MENU_COVERAGE.md): each step raises \(k,K\) by one and \(s,J\) by two, keeps old folded arrows, and adds \(L_k\mapsto H_k\) and \(H_{k+6}\mapsto L_{k+6}\) at \(Q\) using the pre-step \(k\). These are precisely the new source and destination cells. The new images are respectively \(K'\) and \(K'-1\), and the sources have opposite physical sides. Existing upper-row numerical coordinates increase by two and existing lower-row coordinates stay fixed. Thus \(x\) increases by one per step and \(y=3\) is fixed. The requested expanded original needs its own admitted independent prefix, with \(n\ge2K\) at its final requested size. This proves **ordered template feasibility iff \(q\ge3\) and \(p+q\ge7\)**, with selectable first roles and no upper bound on either quota.

For any full E+ exterior in the declared D157 arrangement, the actual \(vu\) is the unique exterior incidence at \(v=A\); the reduced weight-one edge forces \(u=A+1\). The [D147](ORDINARY_SPINE_EXTERIOR_SUPPLY_REASSESSMENT.md) terminal-balance identity transports to this arrangement, since the reduced spectrum and crossing parent incidences are the same. Relative to the numerical reference exterior, every second terminal in a lower slot adds its parent's upper index minus one to the weight sum, and every first terminal in an upper slot subtracts its positive lower parent label. The two positive sums agree, so E+ requires a selected terminal from each section. The four first centers, \(w\), and every second exterior terminal are on the lower side. This forces \(A\ge6\). The D157 graph counts \(5+R=2(A+x)\), where \(x\ge0\), then require \(R\ge7\) for every E+ exterior. Conversely put the smaller second quota at P and the larger at Q. For odd \(R\ge7\) the larger quota is at least four, so the ordered theorem supplies E+. Thus **full E+ feasibility iff \(R\ge7\)** for either first inventory on the declared arrangement. This result uses the direct constructions for feasibility and symbolic necessity. It requires no new numerical search or finite exhaustion. D170's separately accepted fixed-base evidence and its original restricted scope remain as recorded. T remains unclassified here, and the E+ exclusions concern the declared placement class.

## 6. Exact named resources, return and closure

Assign each surviving coordinate to its own actual host's remaining leaf indices in order, with \(w\)'s direct leaf at its prescribed coordinate. The two selected exterior terminal indices and the numerical branch roles preserve every original named incidence. The oriented old and fresh labels and differences are
\[
\begin{aligned}
L_o&=[6,c+5]\sqcup[c+s+6,n+s+6],\\
L_f&=[0,5]\sqcup[c+6,c+s+5]\sqcup[n+s+7,m],\\
D_o&=[1,d-2]\sqcup[d-1+s,n+s],\\
D_f&=[d-1,d+s-2]\sqcup[n+s+1,m].
\end{aligned}
\]
The old embedding is \(G+6\) for \(G<c\) and \(G+6+s\) for \(G\ge c\). Membership persists at \(C\) since \(6\le K\le6+s\). This keeps old noncrossing weights and raises all old crossing weights by \(s\). The crossing exterior reductions expand by \(n+s\) in their differences. The interval of gap labels is bijective by source coverage and its weight interval by image coverage. These disjoint palettes fill \([0,m]\) and \([1,m]\). The gap crossing images \([K,s-1]\) give \([d+K-1,d+s-2]\); the old crossing band and the exterior extend it consecutively to \(m\). Noncrossing weights fill \([1,d+K-2]\). The new oriented frontier is the actual \(w=0\), and \(m=2C+2\), giving exactly \(S_{-1}\).

For the first-section boundary write \(S_b,S_a,S_{c_1},S_Z\) for the actual numeric source sets of the four first centers. Their disjoint union is \(I\), and \(J_1=(S_b+3)\sqcup(S_a+2)\sqcup(S_{c_1}+1)\sqcup S_Z\). Disjointness follows from the proven source and destination partitions. Here \(J_1\) is an image set and \(J\) the fold constant. Explicitly at each base
\[
I=[0,6]\sqcup(J-U_1),\qquad
J_1=[0,3]\sqcup X'\sqcup(J-V_1),
\]
where \(U_1,V_1\) are the folded H source and image indices belonging to the first centers. In the four large-p cases \(U_1=\{f,k+2\}, V_1=\{4,k-1\}\) with \(f\) the fixed upper reservation. In short-table order they are
\[
(\{8,7\},\{5,6\}),\quad(\{7,5\},\{6,4\}),\quad
(\{7,6\},\{6,5\}),\quad(\{8,6\},\{6,5\}).
\]
Each omits exactly the direct-leaf assignment. At a Q-tail enlargement by \(j\), keep these base folded indices and \(X'\) and substitute \(J+2j\) for \(J\) in the numeric H coordinates. The additional Q cells belong to the second section. Let \(I^c,J_1^c\) be their exact complements in the requested interval \([0,s-1]\).

The first and remaining exterior label sets are \(E_1=\{2,3,4,5,n+s+7,n+s+9\}\) and \(E_2=\{0,1,n+s+8,n+s+10\}\), with exterior weights \(n+s+[1,6]\) and \(n+s+[7,10]\).

| Resource | Used at first frontier | Remaining |
|---|---|---|
| Labels | \(L_o\sqcup E_1\sqcup(6+c+I)\) | \(E_2\sqcup(6+c+I^c)\) |
| Weights | \(D_o\sqcup(n+s+[1,6])\sqcup(d-1+J_1)\) | \((n+s+[7,10])\sqcup(d-1+J_1^c)\) |

Membership on the lower label side follows from the old cut, the reduced label side, and \(i<k\) in the current gap. On the weight side the crossing inventories consist of the old crossing band where present, all exterior weights in the column, and gap images in the respective sets intersected with \([K,s-1]\). The remaining weights in each column are noncrossing. The unfinished literal \(uw\) is the only edge joining the used and remaining vertices. Its oriented endpoints are \(n+s+7,0\) with crossing weight \(n+s+7\), and \(u\) is the physical first frontier.

In minimum polarity the displayed labels are actual. In maximum polarity conjugate the old labels by \(n-\cdot\) and the completed labels and both partial label sets by \(m-\cdot\). The actual cuts are then \(n+1-c\) and \(m+1-C\). Actual side reverses in both states, preserving each old vertex's actual cut membership through the placement. The old actual lower shift is \(2K-6-s=4\) and upper shift \(2K-6=4+s\), compared with \(6,6+s\) in minimum polarity. The maximum-polarity unfinished endpoints are \(3,m\), with the same crossing weight. Conjugation preserves both weight inventories and their crossing status.

For any finite admitted sequence, begin with its independently supplied phase and use each block only at its prescribed physical frontier, phase, inventories and size. Each later embedding preserves actual cut membership of all existing vertices. The immutable final label is the current label plus all later actual lower shifts and, for current upper members, all later gap widths. A same-side weight is fixed and a crossing weight gains all later gap widths. This applies to both assigned endpoints of each admitted unfinished connector, and to the used partial inventories by their respective memberships. The final remaining inventories are the complements in the final full alphabets, including all later blocks. Induction gives the same complete label and weight bijections as successive embedding. The formulas use finitely many indexed cells per requested block and finitely many Q-tail steps. A finite admitted list therefore terminates with exactly its declared named original incidences and no auxiliary sections.

## 7. Four witnessed inventories and the next question

All rows retain four positive first centers with no first direct leaf, two positive second centers of odd total, one actual direct leaf at \(w\), all physical orders, and an independent admitted D157 \(S_{-1}\) input.

| First inventory | Exact full E+ criterion in the declared arrangement | Evidence basis |
|---|---|---|
| \((1,1,2,4)\) | \(R\ge7\) and unordered second pair different from \(\{1,6\}\) | D165 symbolic supply and accepted D164 exhaustion with symbolic transport at \(\{1,6\}\) |
| \((1,1,4,4)\) | \(R\ge7\) | D171 direct constructions and symbolic necessity |
| \((1,2,3,4)\) | \(R\ge7\) | D171 direct constructions and symbolic necessity |
| \((1,3,4,4)\) | \(R\ge7\) | D166 symbolic supply and necessity |

The four theorems allow arbitrary independent magnitudes of the two quotas, subject to these exact conditions and positive odd total. They do not change the original 108-record population or any D164 disposition. In particular, target-0429 retains D166 symbolic E+ supply and unresolved T, with neither historical arm complete.

D167 internal growth explains two-column periods on protected intervals and D168 extends conditional residue allocation to arbitrary two-host separation. D169 demonstrates why physical numerical roles matter. D170 grows Q at a boundary while preserving old folded arrows. D171 supplies all P magnitudes at each minimum Q for the two inventories, even where no long protected interval yet exists, with re-pairing allowed. This removes the need for a hybrid run on the present task. A general role-menu theorem still needs a criterion that guarantees a useful supply geometry across first inventories. Other independent widths and center multiplicities could cover actual cases that fail this menu. The literature-informed pinned two-host shell lift addresses a separate valuable initializer objective. The current results already have an independent D157 input on their stated domain, so the more immediate leverage is to distinguish lack of a compatible role on this template from a genuine need for different exterior supply. The shell lift and its literature checks remain unstarted.

**One next action**

Under separate Owner authorization after Director review, prepare one matched hybrid diagnostic on frozen D164 originals with a first inventory outside the four classified inventories, a quota-four first center and odd second total R≥7. Test whether any original has an independently verified E+ completion outside the width-(6,4) role menu and an independently audited negative for that menu. This action is UNSTARTED.

The prospective matched arms use the same frozen named original and independent prefix: the full width-(6,4) template menu, and admitted E+ exteriors outside that menu. Preserve known D165 adverse and D166/D170 positive controls as controls, with no historic result overwritten. A separating witness needs the complete exterior, numerical roles, selected actual terminal identities, residue or quota barriers, exact resources and return, and an exact independently audited menu rejection. Exhaustion without a separator would address only the frozen domain. This task neither freezes a successor population nor prepares or executes its algorithms. Separate preparation and execution authority are required.
