# D167 — General exceptional reservation types and semilinear quota supply

Task LCL-ORDINARY-SPINE-EXCEPTIONAL-RESERVATION-SEMILINEAR-001. All parameters are exact integers and all intervals are inclusive. Retain the declared D157 connected crossing exterior with a leaf-only gap and an independently supplied named \(S_{-1}\) prefix. Its actual extreme frontier \(v\) has oriented label \(G(v)=0\), \(n=2c+2\), \(d=c+2\), and oriented cut \(c\). A label equal to a cut is on its upper side.

## 1. Exact theorem and physical geometry

Fix four positive actual first-center quotas, even total \(F\), and no first direct leaves. The numerical roles assign them to \(b,a,c_1,Z\), with respective full quotas \(\alpha_b,\alpha_a,\alpha_c,\alpha_Z\). Keep the actual physical branch indices and each parent's named terminal list. The two positive second-center quotas are \(p,q\), with odd total \(R=p+q\), and the actual second spine vertex \(w\) has one direct leaf. The quota \(p\) belongs to \(P\) at reduced label 10, \(q\) to \(Q\) at 8.

For each fixed actual first inventory, **the feasible ordered second pairs for this specified terminal-exchange exterior are exactly a finite union of the following sets**:
\[
(p_0,q_0)+\sum_{a\in W}z_a(2a,4-2a),\qquad
W\subseteq\{0,1,2\},\quad z_a\in\mathbb Z_{\ge0}.
\]
Each base and its \(W\) are given by the finite symbolic reservation-type definition in Section 6, with \(k_0\le14F-8\). The finite union can be empty. For preassigned first roles use only their types. For selectable first roles take the union over actual role assignments. A prescribed second pair with the reverse physical role choice is handled by assigning the actual second centers to \(P,Q\) accordingly. No centers are merged, even when quotas coincide. The theorem requires \(n\ge 2K\) for the actual requested pair and produces a named labeling and exact \(S_{-1}\) return. Its scope is the single stated exterior geometry.

The first fresh section contains \(F+5\) vertices (one spine vertex and four centers in addition to the terminals); the second contains \(R+4\). Each fresh vertex contributes one actual parent edge. Hence
\[
2K=F+R+9,\quad m=n+2K,\quad N_{\rm low}=5+R,\quad N_{\rm high}=4+F.
\]
For the last two identities orient graph color from \(v\) on the lower side. The fresh lower color contains \(w\), the four first centers and the \(R\) second terminals. The upper color contains \(u\), the two second centers, the direct leaf and the \(F\) first terminals.

Take \(A=6,B=4\). Use reduced labels \(v=6,u=7,w=0,b=2,a=3,c_1=4,Z=5,Q=8,P=10\). Select one actual indexed terminal at \(a\) for 9 and one at \(P\) for 1. The actual direct leaf stays at \(w\) in the gap. The actual exterior edges \(vu,uZ,uc_1,ua,ub\) and the selected edge at \(a\) have weights \(1,2,3,4,5,6\). The edges \(uw,wQ\), the selected edge at \(P\), and \(wP\) have weights \(7,8,9,10\). All cross the reduced cut between 6 and 7. These edges form the connected exterior of the named original and use each reduced vertex label in \([0,10]\) once. This also applies when \(P\) or \(a\) has no gap terminal left.

## 2. Rows, capacity and necessary moments

Put
\[
k=K-6=(F+R-3)/2,\qquad s=2K-10=2k+2,\qquad J=s+3=2k+5.
\]
In orientation the old shifts are \(6,6+s\); upper exterior labels gain \(n+s\). The cut is \(C=c+K\). The gap vertex of coordinate \(i\) has label \(6+c+i\) and the weight of its actual parent edge is \(d-1+\pi(i)\). Subtracting the endpoints gives \(\pi(i)=i+5-j\) at lower reduced host \(j\) and \(\pi(i)=s+\beta+1-i\) at upper reduced host \(6+\beta\), since \(n-c=d\).

Write \(L_j=j,H_j=J-j\). The source rows \(L_{[0,k-1]},H_{[4,k+5]}\) partition \([0,s-1]\) into physically lower coordinates \([0,k-1]\) and upper \([k,s-1]\). The destination rows \(L_{[0,k+5]},H_{[4,k-1]}\) partition the same alphabet into noncrossing images \([0,K-1]\) and crossing images \([K,s-1]\). The two source sides are determined by \(6+c+i<C\) and the two destination sets by weight \(d-1+\pi(i)\) crossing the required spectrum threshold \(d+K-1\). An actual parent edge crosses exactly on opposite physical sides. The following arrows are legal when their indices lie in the appropriate destination row.

| Actual host | \(L_j\) source | \(H_j\) source |
|---|---|---|
| \(b\) | \(L_{j+3}\) | \(H_{j-3}\) |
| \(a\) | \(L_{j+2}\) | \(H_{j-2}\) |
| \(c_1\) | \(L_{j+1}\) | \(H_{j-1}\) |
| \(Z\) | \(L_j\) | \(H_j\) |
| \(w\) | \(L_{j+5}\) | \(H_{j-5}\) |
| \(Q\) | \(H_j\) | \(L_j\) |
| \(P\) | \(H_{j-2}\) | \(L_{j+2}\) |

In particular an \(H\) source at a lower host goes to a crossing \(H\) destination, and an \(L\) source at an upper host goes to a crossing \(H\) destination. The other two incidence types go to noncrossing \(L\).

Let \(x,y\) count lower sources at upper parents and upper sources at lower parents. In a compatible return there are \(s-K=x+y\) crossing gap weights. The lower-host count is \(k-x+y=B+2y\) and the upper-host count is \(A+2x\). The connected crossing exterior assigns physical sides by graph color from \(v\). Each gap leaf belongs to the graph color opposite its parent's, giving \(N_{\rm low}=2(A+x)\), \(N_{\rm high}=2(B+y)\). Thus
\[
x=(R-7)/2,\qquad y=(F-4)/2.
\]
In particular \(R\ge7\). Upper-host images are at least 4 and all lower shifts are nonnegative. Induction on destinations \(0,1,2,3\) forces their equal \(L\) sources at \(Z\), the only neutral host. A positive shift to any of these images would consume an earlier already used source. Thus \(\alpha_Z\ge4\), and since the other quotas are positive and \(F\) even, \(F\ge8\). If no actual center has adequate neutral capacity the type union is empty. Hereafter let \(h=(F-4)/2\). After these four forced cells the actual lower-host leaf capacities and shifts are
\[
 (b:\alpha_b,3),\quad (a:\alpha_a-1,2),\quad
 (c_1:\alpha_c,1),\quad (Z:\alpha_Z-4,0),\quad(w:1,5).
\]
They sum to \(F-4=2h\). Precisely \(h=y\) go in \(H\), so the other \(h\) go in \(L\). In particular the neutral remainder can be positive and can be assigned in either row subject to the exact conditions below.

A separate upper boundary bound is always available. \(H_{k+5}\) needs \(Q\) to reach \(L_{k+5}\). Its \(P\) image lies outside the row and no lower host shifts enough. If no further \(Q\) use were available, \(H_{k+4}\) would need the sole \(w\) leaf, and \(H_{k+3}\) could use neither that exhausted host nor its already occupied \(P\) image \(L_{k+5}\). Thus \(q\ge2\) independently of the residual neutral capacity. More precisely at least one of \(H_{k+4},H_{k+3}\) must use \(Q\). If \(q=2\), these right-end reservations exhaust \(Q\). The least \(P\) image is 6. Images 4 and 5 must then each use its equal source at \(Z\), by the same left induction, and \(q=2\) requires \(\alpha_Z\ge6\). This recovers the D166 \(q\ge3\) obstruction when the first four cells exhaust \(Z\). No blanket \(q\ge3\) conclusion for unexhausted \(Z\) is used.

Let \(X,Y\) be the \(h\) remaining lower-host source indices in \(L,H\) and \(X',Y'\) their translated images in \(L,H\) respectively. All four lists are sets, with each endpoint still attributed to its actual leaf and host. A zero shift makes that leaf's two marked endpoints coincide. The residual \(L\to H\) matching is on \([4,k-1]\), deleting source \(X\) and destination \(Y'\), with shift \(0\) or \(-2\). The residual \(H\to L\) matching is on \([4,k+5]\), deleting source \(Y\) and destination \(X'\), with shift \(0\) or \(+2\). The omitted initial neutral cells are outside those common intervals. Comparing source and destination index sums gives
\[
2N_{PL}=\sum Y'-\sum X,\quad 2N_{PH}=\sum Y-\sum X',\quad
p-1=\sum Y-\sum X-D/2,
\]
where the total nonneutral and neutral displacements after the forced cells have sum \(D=3\alpha_b+2(\alpha_a-1)+\alpha_c+5\). The last equality uses \(\sum X'-\sum X+\sum Y-\sum Y'=D\).

The two residual matchings preserve index parity. Thus the even and odd counts of \(X\) equal those of \(Y'\), and those of \(Y\) equal those of \(X'\). The two displayed differences must be nonnegative even integers, with halves summing to \(p-1\). Their combined parity forces \(D\) even, equivalently \(\alpha_b+\alpha_c\) odd. If \(o_H\) counts odd lower-host shifts in \(H\), then \(\sum Y-\sum X\equiv o_H\bmod 2\) and \(p-1\equiv o_H-D/2\bmod 2\). This uses \(\sum Y-\sum Y'\equiv o_H\bmod 2\); it allows both even and zero host shifts. These counts and moments are necessary. The local path conditions decide whether the required shifts actually fit.

## 3. Exact residual path condition and adverse control

In one parity of the \(L\to H\) common interval scan indices increasing by two. At index \(j\) let \(S_j,D_j\) indicate an existing source and destination, and \(B_j\) that the source uses the nonidentity shift at \(P\). The only incoming choices for destination \(j\) are identity at \(j\) and a negative shift from \(j+2\). Thus
\[
D_j=S_j-B_j+B_{j+2},\qquad B_{\rm first}=B_{\rm past\ last}=0.
\]
The first boundary forbids a move before the path and the last forbids a nonexistent source. In particular
\[
 B_j=\sum_{i\ \mathrm{earlier\ on\ the\ path}}(D_i-S_i)
 =\sum_{i\ \mathrm{earlier}}(\mathbf1_{\mathrm{source\ hole\ at}\ i}-\mathbf1_{\mathrm{destination\ hole\ at}\ i}).
\]
Reverse the scan for \(H\to L\), replacing the next index by \(j-2\), to get the identical rule. Empty paths impose no moves. The forced bits must be integral and satisfy \(0\le B_j\le S_j\) with both zero boundaries. These conditions are sufficient as well as necessary: assign \(P\) at the indicated sources and \(Q\) at the other surviving sources, then each destination receives exactly one arrow when \(D_j=1\) and none otherwise. Each \(P\) arrow has its valid index and physical crossing type because it terminates inside the required row. Thus the residual assignment for fixed reservations is unique. Its count of \(P\) uses must equal the actual residual quota at \(P\).

A common hole has \(S_j=D_j=0\) and forces both adjacent bits to zero. The abstract even path \([4,14]\) with source holes \(\{4,8\}\) and destination holes \(\{8,10\}\) has equal hole counts and, after cancelling the common hole for endpoint comparison, a forward ordered pair \(4,10\). The moment predicts three shifts. At 4 the recurrence initiates \(B_6=1\), and at surviving 6 it gives \(B_8=1\), impossible because 8 lacks a source. This is a symbolic adverse path, with no claim that it is an original lobster counterexample. In particular parity, aggregate sums and sorted endpoint dominance across common holes do not imply compatibility.

## 4. Marked gaps and reversible contraction

Mark a source and image endpoint for every one of the \(2h\) remaining actual lower-host assignments, counting \(4h\) occurrences. Also mark anchors \(4\) and \(k-1,k,k+1,k+2,k+3,k+4,k+5\). Coincidences are recorded as weak-order ties. Endpoints must be distinct within each of the four endpoint classes, with legal row bounds and exact paired host displacement. The first marked column is 4 and the last is \(k+5\), since all remaining sources and images are in those bounds. The seven tail anchors are consecutive. Therefore a gap between consecutive distinct marked columns with length at least six is contained in \([4,k-1]\). All its interior columns are unmarked and belong to both common intervals.

Every lower-host reservation has absolute index displacement at most five. A pair with endpoints on opposite sides of a cut strictly inside a long gap would therefore be at least six apart, which is impossible. Changing a long gap shifts both endpoints of any given reservation equally when they lie on its right and leaves both fixed on its left. This preserves the exact displacement, including coincident neutral endpoints. Short gaps are retained exactly. Normalize a long gap of even length to 6 and one of odd length to 7 by removing pairs of columns. Any later expansion adds \(2z\) columns to a long gap. All event order, coincidences, parity and row bounds are preserved: event order relative to the anchors is preserved, the tail anchors move together, and both ends of every adjusted gap remain consecutive marked columns. Marks at 4 retain column 4. In particular no reservation is removed.

On each parity path in each row direction the interior of such a gap consists only of columns with \(S=D=1\). The recurrence gives a constant bit on each consecutive same-parity run there. An explicit splice can be made after \(u+2\) in a long gap \((u,v)\): indices \(u+1,u+2,u+3,u+4\) are all interior, giving two consecutive cells of each parity. Insert two unmarked columns there and translate every later column by two. The parity-path order is obtained by inserting one neutral entry \(S=D=1\) into each path in each direction. In either scan order the inserted entry repeats the bit of that run, so all inequalities, common-hole zeros and boundary bits are preserved. The converse deletes neutral entries from these runs. For a deletion down to 6 or 7 there are still interior entries of each parity at the splice, so the path word has precisely the same event order and the same bit before and after the shortened neutral run. Equivalently removing an \(S=D=1\) entry identifies its equal incident bits and can neither relax an event condition nor change one. This proves that legal expansion and compression are mutually compatible with the exact recurrence, regardless of the bits at the neighboring marks. There are two new columns and both source and destination positions survive in both row intervals, hence four added sources and four added destinations. Each new source takes \(P\) iff the constant bit on its path is one.

## 5. Directional flow and exact quota generators

Take the cut between \(u+2\) and \(u+3\) within a long gap. Restrict the \(L\to H\) count to the common interval beginning at 4, and likewise for \(H\to L\). Each direction has one potential shifted arrow crossing this cut on each parity. Those potential arrows have interior endpoints and their actual uses are the constant bits of the preceding section. For \(L\to H\) all crossing shifts point left, so their count is left destinations minus left sources,
\[
 a=|X_{\rm left}|-|Y'_{\rm left}|.
\]
For \(H\to L\) all crossing shifts point right, so their count is left sources minus left destinations, \( |X'_{\rm left}|-|Y_{\rm left}|\). The two uncut baseline intervals have the same number of positions to the left of this cut. No lower-host reservation spans it, so \(|X_{\rm left}|=|X'_{\rm left}|\) and \(|Y_{\rm left}|=|Y'_{\rm left}|\). The two directional counts therefore equal \(a\in\{0,1,2\}\). Their individual parity bits need not agree.

An expansion by two adds \(2a\) shifted sources at \(P\) and \(4-2a\) identity sources at \(Q\). The fixed selected exterior terminal at \(P\) consumes its same one unit throughout. Thus the full second quotas increase by
\[
(2a,4-2a)\in\{(0,4),(2,2),(4,0)\}.
\]
The final anchor shows \(k\) grows by two, and \(R=2k-F+3\) grows by four as required. All first capacities and the sole direct leaf remain exactly as specified. The interval operation constructs capacity for actual extra second-center terminal indices for a different requested pair. It is an operation on the symbolic reservation coordinates.

The weak order and the before/after partition of marks at any other gap are unchanged by this expansion. Its left counts, hence \(a\), are unchanged. Each expansion adds its length change to every later mark, so operations on distinct gaps commute, including after repetitions. Compression removes the opposite capacity increments. The exact residual matching after all changes is unique once the reservations are fixed.

## 6. Finite symbolic type definition and proof of completeness

For a fixed actual first inventory consider its finitely many numerical role assignments with \(\alpha_Z\ge4\). Designate named selected exterior terminals and the four forced neutral leaves. For existence one may choose the first terminal at the actual \(a\) and \(P\), and the first four indices at the actual \(Z\) in their fixed source order. Permuting indices of sibling leaves at the same physical parent transports any solution to these designated roles without changing any edge constraint, so this convention preserves existence. At \(P\) the designated first terminal exists for every positive intended quota. Keep each other lower-host leaf, including the direct leaf, by its actual name. The following defines a finite catalog mathematically.

1. Assign \(h\) of those \(2h\) lower-host leaves to each source side. Mark their source and destination endpoints with the host shifts from Section 2.
2. Choose a weak order of all endpoints and the eight anchor occurrences. Allow zero-shift endpoint coincidences and other feasible ties. Enforce distinctness inside each of \(X,Y,X',Y'\) and valid source and image row membership.
3. Starting at anchor 4, assign length from \(\{1,2,3,4,5,6,7\}\) to each positive gap of the weak order. Lengths 6 and 7 are expandable. The tail anchors must have exact unit spacing. Read \(k_0\) from those anchors and enforce exact displacement, all row bounds and the exact parity-path recurrence with its zero boundaries. Discard invalid types.
4. Read \(N_P\) from the four valid residual paths, and assign \(a\) by Section 5 to every expandable gap. Store the base pair \(p_0=1+N_P,\ q_0=R_0-p_0\), where \(R_0=2k_0-F+3\).

The choices have no dependence on a requested \(p,q\). There are at most \(4h+8=2F\) marked occurrences, so at most \(2F-1\) gaps of length at most seven. The last anchor \(k_0+5\) and first 4 give \(k_0+1\le7(2F-1)\), hence \(k_0\le14F-8\). Row legality gives \(h=|X|\le k_0-4\), from which \(R_0\ge7\) and \(R_0\) is odd. In particular \(k_0\ge6\). With \(K_0=k_0+6,\ s_0=2k_0+2\), the placement bounds \(6\le K_0\le6+s_0\) and \(s_0\ge K_0\) hold. The residual source count is \(s_0-4-2h=s_0-F=R_0-1\), so \(q_0\) counts the identity assignments. The top \(H_{k_0+5}\) source necessarily survives because no lower host can shift by six. Its actual only legal residual arrow is \(Q\) to \(L_{k_0+5}\), proving \(q_0>0\) from a physical incidence. The right-end argument also gives \(q_0\ge2\). Clearly \(p_0\ge1\) from its exterior leaf. Every accepted base has exact arithmetic return premises. It is an auxiliary description, requiring no generated original or allocator evaluation.

For completeness, a compatible labeling on the requested named original induces reservations and legal residual paths. Compress every long gap to its parity-preserving base. This yields one of the listed weak orders and gap assignments, still with valid marks and paths. The contraction preserves all named lower-host incidences, and records the removed \(P,Q\) capacities exactly. Conversely an accepted type with any choices of expansion lengths defines legal reservations and exact residual paths by the reversible splice. The formulas supply its required second quotas before any labeling of an expanded target is used. If the actual input prefix satisfies the size premise at the requested pair, that expanded description is admissible for the reconstruction below. The smaller auxiliary \(K_0\) cannot exceed the actual \(K\).

## 7. Semilinear membership and extraction

For a valid base let \(W\) contain the distinct \(a\)-values of its expandable gaps. Repeated \(a\)-values can be aggregated because all such expansions have the same generator and are unbounded in either cardinality. Fix one representative gap per \(a\) and put the entire \(z_a\) there when constructing a witness. Independence and commutation ensure that these representative expansions attain exactly the same quota pairs as distributing each total.

For a candidate pair define exact arithmetic variables \(T=(p+q-p_0-q_0)/4,\ U=(p-p_0)/2\). Both must be nonnegative integers. The two equations are \(\sum z_a=T,\ \sum a z_a=U\). The full rules, including extraction, are:

| \(W\) | Condition | Choice of \(z_a\) |
|---|---|---|
| \(\varnothing\) | \(T=U=0\) | Empty assignment |
| \(\{a\}\) | \(U=aT\) | \(z_a=T\) |
| \(\{0,2\}\) | \(U\) even, \(0\le U\le2T\) | \(z_2=U/2,\ z_0=T-z_2\) |
| \(\{0,1\}\) | \(0\le U\le T\) | \(z_1=U,\ z_0=T-U\) |
| \(\{1,2\}\) | \(T\le U\le2T\) | \(z_2=U-T,\ z_1=2T-U\) |
| \(\{0,1,2\}\) | \(0\le U\le2T\) | \(z_2=\lfloor U/2\rfloor,\ z_1=U-2z_2,\ z_0=T-z_1-z_2\) |

The bounds are necessary from the two equations and the parity requirement when the only nonzero index is 2. The listed solutions have nonnegative integer entries and the exact totals. For the last row \(z_0\ge0\) since \(z_1+z_2=\lceil U/2\rceil\le T\). This works also at \(T=0\) and every endpoint. The required \(q\) follows by subtracting \(p\) from \(p+q\).

Compression of arbitrary compatible pairs proves necessity of the union in Section 1. For sufficiency select a qualifying type by any fixed order and solve the table. Expand the representative gaps, then reconstruct using the unique four residual paths. This is a finite symbolic enumeration definition and a terminating independent construction for each input. It does not assert a small catalog or polynomial complexity in \(F\), and does not count named labelings. No numerical enumeration of even the bases or runtime allocator evaluation is part of the result.

## 8. Symbolic controls and all three generators

The accepted D165 and D166 constructions are legal named reservations with, respectively, four and eight marked lower-host leaves after the four forced neutral cells. Their exact residual matchings therefore compress by Section 4. Expanding the same gaps by precisely their deleted amounts restores all marked indices and hosts. Uniqueness restores the residual coordinate-to-host assignments and the exact original quotas. Terminal names within each parent may be retained by using the original naming order on the reconstructed coordinate assignments. This preserves actual incidences in the requested named original and proves the general theorem represents both controls without a new allocation evaluation. D165's ordered fixed-exterior classification is symbolic. Its distinct full-E+ \(\{1,6\}\) corner retains the accepted finite exhaustion with symbolic transport. D166's ordered and full-E+ classifications retain their wholly symbolic proofs. The present theorem is for their common geometry, so it draws no new all-exterior inference from either control.

**Generator \((0,4)\).** In D166 Case A, \(p=1\) and the largest exceptional endpoint is 10. For \(k\ge17\), the gap from 10 to \(k-1\) is long and contains no marks. Every residual assignment uses \(Q\), so all four bits are zero and expanding adds four \(Q\) leaves.

**Generator \((2,2)\).** In D165's even-\(p\) construction take \(\Delta_1=5,\ \Delta_2=2r+3,\ k=2r+6,\ r\ge5\), giving \(p=4+2r,\ q=2r+3\). Use \(L_4,L_5\) at \(c_1\) (quota two), \(H_9\) at \(w\), and \(H_{2r+8}\) at \(b\) (quota one), with the quota-one \(a\)'s terminal exterior and four \(Z\) leaves forced. Thus \(X=\{4,5\}, X'=\{5,6\}, Y=\{9,2r+8\}, Y'=\{4,2r+5\}\). The offsets meet the D165 odd bounds, since \(2r+3=k-3\) and \(5\le k-1\). The gap from 9 to \(2r+5=k-1\) has length \(2r-4\ge6\); no other endpoint or anchor lies inside it. The short pair \(4,9\) has no \(L\to H\) shift and has its \(H\to L\) moving range entirely at or below 9. The other pair uses the odd \(L\to H\) path from source hole 5 to destination hole \(2r+5\), and the even \(H\to L\) path between destination hole 6 and source hole \(2r+8\). Both paths carry an active bit across the long gap. They are the only active paths there, so \(a=1\). Expansion shifts the moving upper source, upper image and tail anchors by two, keeps the fixed roles and grows both second quotas by two.

**Generator \((4,0)\).** For even \(k\ge14\) take the same first roles with \(\Delta_1=k-1,\Delta_2=k-3\), so \(p=2k-8,\ q=3\). Now \(X=\{4,5\}, X'=\{5,6\}, Y=\{k+3,k+2\}, Y'=\{k-2,k-1\}\). The gap from 6 to \(k-2\) has length \(k-8\ge6\) and no intervening mark. Both \(L\to H\) repairs run across it from holes 4 and 5 to holes \(k-2\) and \(k-1\) on the respective parities. Both \(H\to L\) repairs run from destination holes 5 and 6 to source holes \(k+3\) and \(k+2\), on odd and even paths respectively. Therefore \(a=2\). Expanding moves the upper endpoints and tail by two, leaves the two lower sources and images fixed, increases \(p\) by four and preserves \(q=3\).

## 9. Exact named lifting, intermediate resources and composition

On the requested original retain its actual spine, role assignment and named parents. Assign the selected exterior terminals their specified reduced labels and expand every upper exterior label by \(n+s\). Assign each lower-host reservation to its actual indexed leaf. At \(P,Q\) assign their surviving source coordinates to the remaining actual terminal indices in increasing order. The resulting actual source and image alphabets both exhaust \([0,s-1]\) once. Use the cut-preserving oriented old shifts as in Section 2. The placement inequalities follow from \(k\ge h+4\ge6\), \(6\le K\le6+s\) and \(s\ge K\). The old palettes and exact fresh complements are
~~~
L_old   = [6,c+5] ⊔ [c+s+6,n+s+6]
L_fresh = [0,5] ⊔ [c+6,c+s+5] ⊔ [n+s+7,m]
D_old   = [1,d−2] ⊔ [d−1+s,n+s]
D_fresh = [d−1,d+s−2] ⊔ [n+s+1,m].
~~~
Old crossing weights gain \(s\) while old noncrossing weights stay fixed. The gap fills its middle label band and lower weight band, and the actual exterior fills the outside label bands and the upper weight band via the common shift \(n+s\) on each crossing exterior edge. The full bijections are therefore \([0,m]\) on vertices and \([1,m]\) on differences. The exact crossing spectrum at \(C=c+K\) is \([d+K-1,m]\), by adjoining the gap crossing weights \([d+K-1,d+s-2]\) to the old and exterior crossing bands. The noncrossing spectrum is \([1,d+K-2]\). Since \(m=2C+2\) and oriented \(w=0\), this is exactly the desired \(S_{-1}\) return.

For the first-section boundary let \(S_b,S_a,S_{c_1},S_Z\) be the retained gap source sets at the first-center parents, including the forced and any residual \(Z\) cells. Put
\[
I=S_b\sqcup S_a\sqcup S_{c_1}\sqcup S_Z,\qquad
J_1=(S_b+3)\sqcup(S_a+2)\sqcup(S_{c_1}+1)\sqcup S_Z.
\]
Both unions are disjoint by the exact source and image partitions. Take \(I'\) and \(J_2\) to be the complements in \([0,s-1]\). The fresh exterior first and remaining label sets, excluding old \(v\), are \(E_1=\{2,3,4,5,n+s+7,n+s+9\}\) and \(E_2=\{0,1,n+s+8,n+s+10\}\). The actual reduced first and remaining edges use \([1,6]\) and \([7,10]\); all gain \(n+s\). Thus the intermediate resources are
~~~
used labels        L_old ⊔ E₁ ⊔ (6+c+I)
remaining labels   E₂ ⊔ (6+c+I′)
used weights       D_old ⊔ (n+s+[1,6]) ⊔ (d−1+J₁)
remaining weights  (n+s+[7,10]) ⊔ (d−1+J₂).
~~~
Label sides are their intersections with \([0,C-1]\) and \([C,m]\), with the lower gap coordinates the intersections with \([0,k-1]\). Keep the old crossing and noncrossing bands as written. Both exterior weight bands cross. In the gap weight parts use \(J_i\cap[K,s-1]\) for crossing and \(J_i\cap[0,K-1]\) for noncrossing. The actual unfinished connector is the literal edge \(uw\) in the remaining exterior weight band, with oriented endpoints \(n+s+7,0\) and crossing weight \(n+s+7\).

For actual minimum polarity retain these placements. For actual maximum polarity if the input actual label is \(g\), orient by \(G=n-g\) and complement the output about \(m\). The actual cuts are \(n+1-c\) and \(m+1-C\). Below the actual old cut \(G\ge c\), so its output label is \(m-(n-g+6+s)=g+4\); on the actual upper side it is \(g+4+s\). Thus minimum and maximum lower shifts are six and four, with \(s\) added on the upper band. Cut membership is invariant. In maximum polarity \(u=3,w=m\) and the unfinished connector is still crossing at the same weight. Complement the two intermediate label sets, reverse their side classifications, and retain the weight sets and crossing flags.

In a finite composition of admitted named initializers and transitions, including D157, D165 and D166 where applicable, each block requires its own exact incoming phase, size, port and palettes. By the own-block reconstruction the output meets its exact declared return and uses no later labeling. At any complete boundary \(i\), subsequent cut memberships are invariant. Let \(\Lambda_i,\Sigma_i\) sum the subsequent actual lower shifts and gap widths. By induction the final label of an existing vertex with label \(g\) is \(g+\Lambda_i+\Sigma_i\mathbf1[g\ge C_i]\) in actual polarity, where \(C_i\) is the actual cut at that boundary. Each existing crossing weight gains \(\Sigma_i\); other weights are fixed. Apply this embedding to the block's used first-section resources and assigned unfinished endpoints, then take exact final complements. The connector's weight gains \(\Sigma_i\) because it crosses. This provides immutable final labels and exact inventories along every admitted finite sequence. Finite type selection, integer extraction, the finite expanded intervals and the finite block list all terminate.

## 10. Comparison and strategic boundary

D145 and D146 give exact coefficient tests with constructive predecessor extraction and rational generating series for their D143 folded-gap settings. D146 handles general fixed widths there. D167 gives an explicit arithmetic description of existential quota support for a different, specialized exceptional geometry, with finitely bounded bases for each fixed actual first inventory and only three allowed generator vectors. It constructs the reservations by type selection and expansion, and reconstructs the rest by unique residual paths. It neither evaluates those strict-phase series nor gives allocation counts. The genuinely additional information here is the specific semilinear period set and the explicit inventory-dependent base bound across all odd \(R\), with a direct extraction rule for expansions.

The common intervals and two shifts differing by two are essential to the proved balance and splice. With a different single nonzero reflection offset after folding, residue paths and longer insertion periods are plausible if exact boundary anchors and no-spanning cuts can be proved. Additional upper hosts can introduce several incoming shifts and lose uniqueness, so the present proof does not give an extension there. The broader obstruction is independent physical exterior supply and, beyond this geometry, the validity of new residual descriptions. This theorem settles the selected question symbolically and needs no hybrid execution. It supplies neither all width-\((6,4)\) exteriors nor general E+ or T classifications, arbitrary topology decomposition, ordinary nongracefulness, or any new conclusion on D164's historical arms.

The single proposed unstarted next question is reservation compression with exactly two eligible upper hosts at arbitrary fixed reduced-label separation, within a separately authorized exceptional arrangement. The separation-two theorem here is its control. [D145](ORDINARY_SPINE_TWO_SECTION_EXACT_GAP_CRITERION.md) · [D146](ORDINARY_SPINE_TWO_SECTION_GENERAL_GAP_CRITERION.md) · [D165](ORDINARY_SPINE_EXCEPTIONAL_FOUR_FIRST_CENTER_PARITY_CHAIN.md) · [D166](ORDINARY_SPINE_EXCEPTIONAL_FOUR_FIRST_CENTER_EIGHT_DEFECT.md)
