# D200 — Generalized safe-gap shell and composition of two distinct multi-gap lifts

Task LCL-ORDINARY-SPINE-GENERALIZED-SAFE-GAP-SHELL-COMPOSITION-001. The registered symbolic claims hold. The generalized three-gap shell reduces the named fresh terminal problem to an exact two-host balance. D199's nonnested Family C supplies a parameterized composition through an actual terminal-free section and a distinct relocated-safe-cut shell.

## 1. Exact shell and residual palettes

Let the independently supplied graceful prefix have \(N\) edges, actual minimum frontier 0 and proper safe cuts \(r<t<N-1\) with distinct thresholds \(D_r,D_t\le N-2\). Cut \(N-1\) is safe at threshold \(N-1\). Let the receiving section have original quotas \((p,q,0,1)\) with \(p,q\ge1\), fresh size \(K=p+q+6\), and target size \(M=N+K\). The size counts its four child edges, connector and \(p+q+1\) terminal edges. Define \(u=\min(D_r,D_t)\), \(v^*=\max(D_r,D_t)+1\). As in the exact supported-rank theorem of [D199](ORDINARY_SPINE_PARTIAL_SAFE_CUT_THREE_GAP_CHAIN.md), use
\[
 E(x)=1+x+{\bf1}_{x\ge r}+{\bf1}_{x\ge t}+(K-4){\bf1}_{x\ge N-1}.
\]
The old labels are \(([1,N+1]\setminus\{r+1,t+2\})\cup\{M-2,M-1\}\). Indeed the two unit gaps miss \(r+1,t+2\), the last low old label is \(E(N-2)=N+1\), and the last gap is \([N+2,M-3]\). The supported rank jumps are one except for extra widths 1 at \(D_r,D_t\) and \(K-4\) at \(N-1\). Thus old differences are \(([1,N]\setminus\{u,v^*\})\cup\{M-3,M-2\}\). In particular the old ranks \(N-1,N\) carry the last two weights. These calculations preserve exact original endpoint differences.

Choose \(H,J\) with \(\{H,J\}=\{r+1,t+2\}\) and \(4\le H,J\le K-1\). The numerical role \(H\) belongs to the original first child of quota \(p\) and \(J\) to the original third child, which is the actual direct leaf. The second child of quota \(q\) has label 0. The fourth child of quota one has label \(c=M-\alpha\) and its actual terminal has label \(l=c+\sigma\beta\), where \(\{\alpha,\beta\}=\{u,v^*\}\), \(\sigma=\pm1\), and both labels are in \([N+2,M-3]\). Set the new spine vertex \(w=M\). These placements use only distinct unused labels: the exterior labels are 0 and \(M\), \(H,J\) use the two lower gaps, and \(c,l\) are in the big gap with \(\beta>0\).

At physical cut \(C=N+2\), old \(x<N-1\) are lower and all other old vertices are upper. Their crossing weights are precisely \(M-3,M-2\). The original connector \((E(0),w)=(1,M)\) crosses with weight \(M-1\). The original child edges give \(M-H,M,M-J,\alpha\) in their actual order. The first three cross since \(H,J\le t+2\le N\) and the second host is 0. The last child edge and its terminal edge of weight \(\beta\) are upper on both ends. The two small weights therefore supply the two omitted low ranks. The other child weights \(M-H,M-J\) are distinct in \([N+1,M-4]\) by the bounds on \(H,J\).

The exact remaining resources are
\[
 R=[N+2,M-3]\setminus\{c,l\},\qquad
 Q=[N+1,M-4]\setminus\{M-H,M-J\}.
\]
Both base intervals have length \(K-4\) and both deletions have size two, so \(|R|=|Q|=K-6=p+q\). Every source is upper and every remaining terminal's actual parent is lower at \(H\) or 0. Any assignment using exactly \(Q\) crosses for each of these edges with the required threshold \(N+1\). The exact moment of the two palettes is
\[
 \sum R-\sum Q=K-4+2\alpha-\sigma\beta-H-J.
\]
This follows by subtracting the two unpunctured intervals, whose sum difference is \((M-3)-(N+1)=K-4\), and then accounting for the two deletions in each.

## 2. Exact deterministic two-host consumer

In one-sided geometry with every \(x\in R\) strictly above \(H>0\), let \(b_x\) indicate allocation of source \(x\) to the actual host \(H\), with \(b_x=0\) for absent sources. Every source at host 0 gives difference \(x\). Every source at \(H\) gives \(x-H\). The two possible contributions to weight coordinate \(x\) are the identity source \(x\) and the shifted source \(x+H\), so the exact multiplicity-one balance is
\[
 {\bf1}_Q(x)={\bf1}_R(x)-b_x+b_{x+H},\qquad
 b_x={\bf1}_R(x)-{\bf1}_Q(x)+b_{x+H}.
\]
On each residue modulo \(H\), start with zero above the largest occupied coordinate of \(R\cup Q\), then scan downward. All candidates are uniquely forced. It is enough to compute through a full residue layer below the smallest occupied coordinate and check zero there: all lower indicators are zero and the bit would otherwise persist. The case of two empty palettes gives only the empty assignment. If just one is empty the complete balance and cardinality test rejects unequal palettes.

Feasibility is equivalent to the following exact finite test. All forced bits must be 0 or 1 and bounded above by \({\bf1}_R(x)\), the lower residual flow must be zero, \(\sum b_x=p\) and \(|R|-p=q\), and the actual resulting edges must have the stated crossing predicates. Necessity follows from counting actual incidences. For sufficiency assign \(x\) to \(H\) precisely when \(b_x=1\). Exact balance supplies one incidence at every required difference and none at any excluded value. Any geometry-specific edge predicate is then checked directly. In §1 it already follows from actual sides and the exact \(Q\) membership. Sort the selected labels separately for each parent and assign them in increasing original terminal index. This deterministic construction has no search over parent choices and does not quotient original children or count all named labelings.

Summing label minus difference across the assignments gives \(Hp=\sum R-\sum Q\). This is necessary. It only records the first moment of the forced bits. For example, a supplied eight-edge all-direct star has \(D_r=r\). Use \(r=3,t=4,H=4,J=6,\alpha=5,\beta=3,\sigma=-1\) and actual \((3,4,0,1)\). Here \(K=13,M=21,c=16,l=13\), so every shell side condition is valid. The residuals are
\[
 R=\{10,11,12,14,15,17,18\},\qquad Q=\{9,10,11,12,13,14,16\}.
\]
Their sum difference is \(97-85=12=Hp\). But weight 16 would require source 16 or 20, and neither is present. Equivalently \(b_{16}=-1\) since \(b_{20}=0\). This proves exact failure on that fixed shell even at equal moment.

The retained [R226 §§1–7](../references/upstream/mdl/N226_R226_two_host_completion.md) use exact label/weight incidence balance for any supplied two-host core. Restricting to labels above both actual hosts gives options \(\{x,x-H\}\) on residue paths and forced rows at one-option labels. The component forcing there gives the same unique assignment. In this one-sided restriction \(H>0\) rules out an equal-option loop and the maximum of an ordinary option pair identifies its unique label, so there is no parallel pair. The [D165 parity repairs](ORDINARY_SPINE_EXCEPTIONAL_FOUR_FIRST_CENTER_PARITY_CHAIN.md) are explicit step-two hole chains. The [D166 exact residual recurrence](ORDINARY_SPINE_EXCEPTIONAL_FOUR_FIRST_CENTER_EIGHT_DEFECT.md) has the same equation \(D_j=S_j-B_j+B_{j+2}\) in one direction, and scans the opposite direction in reverse. [D167](ORDINARY_SPINE_EXCEPTIONAL_RESERVATION_SEMILINEAR.md) uses those paths and reversible neutral-run compression. [D168 §4](ORDINARY_SPINE_EXCEPTIONAL_TWO_UPPER_HOST_RESIDUE_COMPRESSION.md) has the arbitrary residue step \(\rho\) and the same zero-boundary balance. With \(S={\bf1}_R,D={\bf1}_Q,\rho=H,B=b\), the equation here is exactly that directional recurrence on actual coordinates, solved from the upper boundary. The geometric shell independently provides its palettes. These comparisons settle source overlap without claiming novelty.

Whenever the consumer passes, the old and fresh label and difference inventories of §1 are exact. The noncrossing weights are \([1,N]\) and the crossing weights \([N+1,M]\). Complement at \(M\) to get actual minimum frontier zero at cut \(M+1-C=K-1\), with unchanged named differences and crossing flags. The normalized returned state is \(P(M,K-1,N+1)\). It is strict when \(K=N\). Both physical polarities retain actual child and terminal parents and literal connector \((1,M)\) or \((M-1,0)\).

## 3. Size independence and the two numerical roles

Use the D199 cuts 3 and 4 with thresholds 1 and 2 in either order, and cut \(N-1\) at \(N-1\). For \(H=4,J=6,\alpha=3,\beta=1,\sigma=-1\), the deleted upper labels are \(M-3,M-4\) and the corresponding weight holes are \(M-4,M-6\). Thus
\[
 R=[N+2,M-5],\qquad Q=[N+1,M-5]\setminus\{M-6\}.
\]
Their exact moment is \(K-7\), as \(Q\) replaces \(M-6\) by \(N+1\). For \(p\ge1\) the necessary condition is \(K=4p+7,\ q=3p+1\). Conversely the \(p\) sources \(M-6-4j\), \(0\le j<p\), lie in \(R\) and subtract four to the successive chain entries, ending at weight \(N+1\). Use all other labels identically at the actual host 0. This fills both residual alphabets with actual counts. The proof uses the independent supplied length \(N\) only through the shell's cut and range conditions. It returns \(P(N+K,K-1,N+1)\).

Swapping numerical roles gives \(H=6,J=4\) with the same \(R,Q\), still with actual first child at the positive shift host and actual direct leaf at \(J\). Now the exact conditions are \(K=6p+7,\ q=5p+1\). The chain \(M-6-6j\) ends at \(N+1\) and its last source is \(N+7\), in \(R\). Both directions follow by the same exact moment and construction. These are size-independent fixed templates. The accepted D199 statement retains its original scope and is recovered by \(K=N\) in the first case.

## 4. Relocated-safe-cut supplier

For \(z\ge1\) and \(N\ge z+6\), assume safe \(r=z+2,t=z+4\) with thresholds \(z,z+2\), and safe cut \(N-1\) with threshold \(N-1\). Use \(H=z+3,J=z+6,\alpha=H,\beta=z,\sigma=+1\). The range of the actual shell begins at \(K=J+1=z+7\). This is exactly the lower bound for the role \(J\le K-1\), and it also makes \(c=M-H\) and \(l=M-H+z=M-3\) both lie in \([N+2,M-3]\). The exact residuals are
\[
 R=[N+2,M-4]\setminus\{M-H\},\qquad
 Q=[N+1,M-4]\setminus\{M-H,M-J\}.
\]
At the boundary \(K=J+1\), the weight hole \(M-J=N+1\) makes \(Q=R\), so all shifts are zero by the moment and the required \(p\ge1\) fails. For any allowed \(K\) the moment is \(K-J-1\), so the necessary conditions for positive quota \(p\) are
\[
 K=z+7+(z+3)p,\qquad q=(z+2)p+z+1.
\]
Conversely these conditions give the chain \(v_j=M-J-Hj\) for \(0\le j\le p\), with \(v_p=N+1\). The source \(v_{p-1}=N+1+H\) is at least \(N+5\), and all sources are at most \(M-J<M-H\) and in \(R\). Their distinct weights \(v_1,\ldots,v_p\) replace the top deleted value \(M-J\) by the bottom new value \(N+1\), and all other terminals use identities at zero. This proves exact necessity and sufficiency. The shell gives all names, physical predicates, resources, connector and both polarities proved in §§1–2. The returned state is \(P(N+K,K-1,N+1)\), strict exactly when \(K=N\).

## 5. Composition of distinct multi-gap lifts

Take the independently supplied nonnested D199 Family C at \(n=4P+7\), \(P\ge2\): actual original \((0,0),(),(),(),(0^{n-6})\), spine labels \(2,4,1,7,0\), two children of the first vertex at 3 and 6, and last children at 5 and \([8,n]\) in increasing original indices. D199 proves its exact original label and difference spectra and safe cuts 3,4 and \(n-1\). For each \(k\in[8,n-2]\) all edges except the high direct leaves have endpoints at most 7, and those leaves at labels at least \(k\) contribute exactly \([k,n]\). Thus its threshold is \(k\).

Append the actual section \((P,3P+1,0,1)\) by D199. In maximum output coordinates, the old cut \(k\) is induced at physical cut \(k+3\), because \(E_1(k-1)=k+2\) and \(E_1(k)=k+3\), where \(E_1\) is the first rank map. The complete D199 safe-cut classification returns threshold \(k+2\) there. Complement for normalized cut \(2n-k-2\). The actual next terminal-free section with \(a\ge2\) direct children has \(N=2n+a+1\) and uses D199's exact terminal-free transport. Its safe cut matching this normalized old one is \(2n+2-(2n-k-2)=k+4\), with threshold \(k+2\). Its new direct leaves supply safe cut \(N-1\) at threshold \(N-1\) since \(N-1\ge2n+2\).

For any independent choice \(10\le z\le n-2\), take \(k=z-2,z\) to get the two required relocated cuts \(z+2,z+4\) with thresholds \(z,z+2\). Apply §4 with arbitrary \(p\ge1\), to the actual receiving section \((p,(z+2)p+z+1,0,1)\). All range conditions, including \(N\ge z+6\), follow from these parameters. The exact final size and state are
\[
 M=2n+a+1+z+7+(z+3)p,\qquad P(M,K-1,N+1).
\]
The standard actual polarity sequence starts at minimum, then maximum after D199, minimum after the terminal-free section, and maximum after the relocated shell. Both physical polarities are obtained by complementing every boundary's labels and corresponding cuts. If \(a=K-2n-1\ge2\), the result is strict. The direct leaves are part of that exact original. A resulting strict state admits the qualifying D196 \((2,0,2)\) transitions and finite repetition by the accepted D199/D196 mixed transport result.

For immutable transport, the actual terminal-free step from maximum input shifts every previously placed actual label by 1. Use \(E_2\) for the relocated rank map. An original initial label \(x\) therefore has final value \(E_2(E_1(x)+1)\). For \(4\le x\le n-2\), \(E_1(x)+1=x+4\), so the relocated thresholds \(z+2,z+4\) pull back to \(z-2,z\). The new large-gap threshold \(N-1=2n+a\) is above all already shifted first-output labels, whose maximum is \(2n+1\). Thus the actual map of the initial prefix is exactly
\[
 3+x+{\bf1}_{x\ge3}+{\bf1}_{x\ge4}
     +{\bf1}_{x\ge z-2}+{\bf1}_{x\ge z}+(n-4){\bf1}_{x\ge n-1}.
\]
The birth-coordinate maps for the first shell and terminal-free boundaries are \(y\mapsto E_2(y+1)\) and \(y\mapsto E_2(y)\), respectively. For each boundary of size \(m\) with final map \(F\), the complementary law is \(y\mapsto M-F(m-y)\). For every original edge subtract its two transported endpoints, using their respective birth maps, and classify the final sides at the final actual cut. This is exact immutable transport because each local old map agrees pointwise with its consecutive embedding. It gives both used and remaining inventories on every actual cut boundary and the original connector endpoints. The final connector pairs in actual maximum orientation at the three appended sections are \((3,2n+4),(2n+4,1),(1,M)\), since the first receiving frontier \(2n\) becomes \(E_2(2n+1)=2n+4\) and the terminal-free frontier 0 becomes \(E_2(0)=1\). Arbitrary finite admitted compositions use D198's pulled-back steps. The final difference of an edge whose crossing status changes follows from its individual endpoint maps.

## 6. Inherited safe coordinates and scope of repetition

For any valid §1 shell and physical cut \(C'\in[\max(H,J)+1,N+2]\) in maximum orientation, define the induced proper old cut \(h=|\{x:E(x)<C'\}|\). The fresh lower child labels \(0,H,J\) and the old frontier label 1 lie below \(C'\), and every other fresh endpoint is at or above \(N+2\). Thus every new edge retains its crossing status, and the fresh crossing weights stay exactly \([N+1,M]\setminus\{M-3,M-2\}\). To be safe the two old high weights must also cross. The two omitted low weights \(u,v^*\) stay noncrossing, so every old weight below \(v^*\) must stay noncrossing. The old weights above \(v^*\) below \(N+1\) must cross on an upper suffix, possibly empty. Thus safety in this range is equivalent to the actual old \(h\) being safe with
\[
 \max(D_r,D_t)\le D_h\le N-1.
\]
The returned threshold is \(D_h+2\) for \(D_h\le N-2\), and \(N+1\) for \(D_h=N-1\). This proves a definite inheritance criterion, with a boundary gap between the highest surviving small hole and the allowed old crossing tail.

In the relocated template there is also an exact second range. For \(C'\in[N+2,c]\) the old induced cut stays \(N-1\), the designated upper terminal and its upper parent are on the same side as \(w\), and the fixed crossing weights are
\[
 \{v_0,c,M-3,M-2,M-1,M\}.
\]
For \(v_j+1\le C'\le v_{j-1}\), \(1\le j\le p\), the \(j\) crossing chain sources contribute \(v_1,\ldots,v_j\), and other crossing terminal labels at or above the cut contribute identities. At \(C'=v_j+1\) these fill \([v_j,M]\) with the fixed edges: \(v_0\) and the common vacancy at \(c=M-H\) are filled by the fixed attachments. At a larger cut in that interval \(v_j\) crosses while \(v_j+1\) cannot occur, as it is neither a chain weight nor a fixed weight and lies below the identity cutoff. For \(C'\in[v_0+1,c]\) there are zero chain sources crossing. It is safe exactly at \(v_0+1\), by the same identity cutoff and the fixed weight \(v_0\). Thus the chain range gives exactly the safe pairs \((v_j+1,v_j)\), \(0\le j\le p\), in maximum coordinates.

Cuts \(C'\le J\) are unsafe: the direct attachment of weight \(v_0\) is noncrossing while the bottom identity terminal at \(N+2<v_0\) crosses from 0. Cuts \(C'>c\) are unsafe: the designated child edge crosses at weight \(H\), while old weight \(N>H\) stays noncrossing. That old edge did not cross at \(N+2\), and it cannot lie wholly among the two old upper labels at distance one. Together these facts and the first range classify the safe cuts of the relocated template. Complement by \(r\mapsto M+1-r\) for minimum coordinates.

After the composed second shell, for original \(k\in[z,n-2]\) the old safe coordinate \(h=k+4\) has threshold \(k+2\). Its exact output maximum cut \(h+3=k+7\) is safe at threshold \(k+4\). A subsequent terminal-free step would move these to \((k+8,k+4)\) in actual minimum coordinates. Those inherited coordinates give threshold four below cut, so they do not by themselves yield the two-below relation of §4. The chain points, after that step, are \((v_j+2,v_j)\), with spacing \(H\ge4\) among themselves. There is also inheritance from the preceding direct-leaf tail: an old \(h\in[2n+2,N-2]\) has threshold \(h\), so its maximum output cut \(h+3\) has threshold \(h+2\), and it transports after a further terminal-free step to \((h+4,h+2)\). If that original tail contains both \(h\) and \(h+2\), as can occur for \(a\ge5\), the pair does have the relocated two-below pattern. An actual further terminal-free section with at least two direct leaves could supply the new high safe cut, conditional also on the stated receiving-quota and shell conditions. This describes useful coordinates without treating independently chosen targets as padded ones. Arbitrary positive-terminal closure still needs suitable independent pairs and an exact compatible fresh-parent allocation on the actual next section.

The small relocated control gives a failure of unconditional pair renewal. Its exact maximum-output safe pairs are \((8,5),(9,7),(10,9),(14,13)\). These follow from the lower corridor and the two chain points, and agree with direct subtraction on the named control. Any one terminal-free step sends them to \((9,5),(10,7),(11,9),(15,13)\) in normalized minimum coordinates. Its new cut 1 has threshold 21 and its new high cuts have thresholds equal to their coordinates. Only cuts 11 and 15 have threshold two below the coordinate, and their separation is four. Thus that returned template supplies no relocated pair across a single terminal-free step, even with at least two actual direct children.

## 7. Fixed original records and dispositions

The [eight original records](../evidence/validation/LCL_ORDINARY_SPINE_GENERALIZED_SAFE_GAP_SHELL_COMPOSITION_001/ORIGINALS.json) bind every prescribed target and its actual supplied prefix graphs before new labels. The [supplied prefix records](../evidence/validation/LCL_ORDINARY_SPINE_GENERALIZED_SAFE_GAP_SHELL_COMPOSITION_001/PREFIXES.json) and [fixed evidence](../evidence/validation/LCL_ORDINARY_SPINE_GENERALIZED_SAFE_GAP_SHELL_COMPOSITION_001/SYMBOLIC_CONTROLS.json) verify the named endpoint spectra, cuts, exact resource partitions, both polarities and immutable endpoint transport. The retained D199 \(p=2\) original is its exact odd-run graph, distinct from the Family C starts for the two new compositions.

| Control | States or exact obstruction |
| --- | --- |
| General composition \(P=2,a=2,z=10,p=1\) | \(30\to33\to63\), chain \(47,34\), \(P(63,29,34)\) |
| Strict composition \(P=2,a=12,z=10,p=2\) | \(30\to43\to86\), chain \(70,57,44\), \(P(86,42,44)\) |
| Retained D199 \(p=2\) | Exact old and new original names, labels and spectra |
| Size-independent \(H=4\) on Family C | \(N=11,K=15\), \(P(26,14,12)\) |
| Swapped \(H=6\) on Family C | \(N=11,K=13\), \(P(24,12,12)\) |
| Small relocated | \(N=8,K=12\), chain \(13,9\), \(P(20,11,9)\) |
| Relocated moment adverse | \(N=8,K=11\), actual moment 3, required 4 |
| Equal moment recurrence adverse | \(N=8,K=13\), actual moment 12, required 12, unavailable weight 16 |

For the composed controls the relocated input cuts are \((12,10),(14,12)\) and \((32,32)\) or \((42,42)\). Actual maximum cuts are 35 and 45, crossing spectra \([34,63]\) and \([44,86]\), with noncrossing spectra \([1,33]\) and \([1,43]\). The final connector pairs are \((3,34),(34,1),(1,63)\) and \((3,34),(34,1),(1,86)\). The common initial map is the stated \(H(x)=3+x+{\bf1}_{x\ge3}+{\bf1}_{x\ge4}+{\bf1}_{x\ge8}+{\bf1}_{x\ge10}+11{\bf1}_{x\ge14}\) in actual maximum output coordinates.

The small relocated prefix is the actual \((2),(),(),(0,0)\) original. The D199 odd-run reflection formula with \(q_0=2,a=0,b=2\) gives center 2, original root 5, its terminals 4,3 in original order, middle spine labels 1,6, frontier 0, and final direct leaves 8,7. Direct subtraction gives cut 3 threshold 1, cut 5 threshold 3, and cut 7 threshold 7. This is a supplied \(z=1\) prefix. With its adverse \((1,4,0,1)\) section all fixed geometry is valid and the exact residuals are \(R=[10,14]\) and \(Q=\{9,10,11,13,14\}\). The failure is within the fixed relocated template. The equal-moment adverse is a distinct fixed star shell and fails the stronger residue criterion.

D199's accepted scope, D197's exact two-translation negative, D198's unclassified fixed-minimum-input \(w=0\) branch and the closed D198, D197 and D191 lanes remain intact. General fresh-parent supply, arbitrary positive-terminal closure and arbitrary original-spine decomposition remain open. No numerical labeling search, solver, original checker, campaign, or replay was used.
