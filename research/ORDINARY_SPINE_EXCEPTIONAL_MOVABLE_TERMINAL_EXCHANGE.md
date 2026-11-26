# D190 — Movable terminal exchange and a variable folded origin

Task **LCL-ORDINARY-SPINE-EXCEPTIONAL-MOVABLE-TERMINAL-EXCHANGE-001**.

**PROVED WITHIN EXACT WRITTEN SCOPE / PENDING DIRECTOR REVIEW.** A movable pair of exterior terminal incidences supplies an exact monotone baseline test with a variable folded origin and a residual neutral group. It embeds D189 and provides the stated single-positive-center families. Inside a fixed movable exterior, the neutral residual capacity obstruction holds for every allocation of its gap. The matching and growth criteria below have their own construction scopes. D188 also remains a separate accepted supplier.

## 1. Actual graph, necessary counts and movable exterior

All structural parameters, quotas and coordinates are integers, excluding booleans. Intervals are inclusive and inverted intervals are empty. Let $r,\nu\ge1$ count actual positive first and second centers, and $z_1,z_2\ge0$ count original direct leaves. Let $F,R$ count actual terminals at the respective centers. Set $a=r+z_1$, $\omega=\nu+z_2-1$, $A=a+2$, $B=\omega+3$. Keep all actual direct leaves exterior, at their own spine parent. The [D157 interface](ORDINARY_SPINE_ALTERNATING_EXCEPTIONAL_SPECTRUM.md#1-interface-and-exact-inventory-rule) takes an independently supplied named $S_{-1}$ input on $n=2c+2$ edges, minimum-oriented frontier $v=0$, cut $c$ (equality on the upper side), and $d=c+2$. Its actual crossing and noncrossing intervals are $[d-1,n]$ and $[1,d-2]$. Append the actual vertices $u,w$ in the witnessing spine. The original two spine edges, $a+\omega+1$ child edges and $F+R$ terminal edges give $2K=F+a+\omega+R+3$. Full size admission is $n\ge2K$ with output $m=n+2K$.

The fresh lower graph color relative to lower $v$ contains $w$, all first children and all second terminals. The fresh upper color contains $u$, all second children and all first terminals. Their counts are $1+a+R$ and $\omega+2+F$. In the declared connected crossing exterior and leaf-only gap, write $s=2K-A-B$, $k=K-A$. At the same-phase cut $c+K$ the least shifted old crossing difference is $d-1+s$, so $s\ge K$. Write $x$ for the lower gap sources at upper parents and $y$ for the upper gap sources at lower parents. The gap must supply exactly $x+y=s-K$ crossing differences. Since the exterior sides coincide with the graph colors, the lower and upper fresh graph counts also equal $A+s-k-y+x=2(A+x)$ and $B+k-x+y=2(B+y)$, respectively. Thus $F\equiv\omega$, $R\equiv a+1$ modulo two. For the stated exterior $A=a+2$ gives $R\ge a+3$ and $R=a+3+2x$.

The threshold also holds in the broader declared terminal-enabled same-phase arrangement when all first children are exterior. For that statement allow the exterior widths to vary. The reduced crossing difference one forces $vu$ to join $v=A$ to $u=A+1$, since $v$ has only that fresh incidence. Compare summed differences with the reference that attaches every low slot $[1,A-1]$ to $u$ and each upper slot $A+b$ for $2\le b\le B$ to $w=0$, retaining both spine edges. It has precisely differences $[1,A+B]$. Each selected first terminal changes the sum by minus its positive lower parent label. Each selected second terminal at upper parent $A+b$ changes it by $b-1>0$. Actual direct leaves retain their reference edges. Equal sums force both types of selection whenever either is present. With $e_2\ge1$ selected second terminals the fresh lower exterior count is $a+1+e_2$, and the lower graph count gives $R\ge a+3$. These graph restrictions apply within the declared arrangement.

For the new exterior fix $v=A,u=A+1,w=0$. Give the $a$ actual first children the slots $[2,A-1]$. Choose a selected actual first center at label $j_e$ with $2\le j_e\le a+1$ and $j_e+1\le B$. Give its first indexed terminal $A+j_e$. The available second child indices are $[2,B]\setminus\{j_e\}$, exactly $B-2=\nu+z_2$ slots. Fix an actual positive center at $b_s=j_e+1$ and place its first indexed terminal at 1. Assign all actual second children bijectively to these slots, with label $A+b$ at index $b$. Lower labels are exactly $[0,A]$ and upper labels are $[A+1,A+B]$. Each spine, child and selected terminal edge crosses these sides and the actual incidences connect the exterior. Their respective differences are 1 at $vu$, $[2,A-1]$ at the first child edges, $A$ at the first selected terminal, $A+1$ at $uw$, $A+b$ for each actual second child and $A+b_s-1=A+j_e$ at the second selected terminal. The last difference restores exactly the omitted child difference. This is the full bijection of exterior labels and differences.

The selected first parent can be the neutral center at $A-1$, and the selected second center can be the first actual upper host. For $a=1$ the unique first slot is 2 and it supplies the selected terminal; the available second indices are $[3,B]$. For $\nu=1$ all but $b_s$ of the second child slots are direct leaves. In particular $\omega=0$ is possible for the exterior at $B=3,j_e=2,b_s=3$ when $\nu=1,z_2=0$. No admissible exterior placement introduces an artificial child or residual terminal host.

## 2. Folded geometry and the forced neutral guard

Let $B_{\rm actual}$ be the upper indices of the actual second centers, of size $\nu$ and containing $b_s$. Put $b_0=\min B_{\rm actual}$, $\gamma=b_0+2$, $\Gamma=\{b-b_0:b\in B_{\rm actual}\}$ and $\rho_s=b_s-b_0$. Thus Q has separation zero and $P_\rho$ denotes the actual host at positive separation $\rho\in\Gamma$. An original direct leaf in an upper slot supplies no separation. An actual host at separation one is allowed.

For a baseline total $R_0=a+3$ and $R=R_0+2z$ with $z\ge0$, the edge count gives
$$
K=a+3+(F+\omega)/2+z,\quad s=F+a+1+2z,\quad k=K-A,\quad J=s+b_0+1 .
$$
Under the supply hypotheses of §3, $s-K=(F-\omega-4)/2+z\ge t+z$, $k=1+(F+\omega)/2+z>0$, and $A\le K\le A+s$. The final size admission covers every auxiliary width. At cut $C=c+K$, source $i$ has actual label $A+c+i$ and is lower iff $i<k$. Image $\pi$ has actual difference $d-1+\pi$. Actual subtraction at a first center of reduced label $j$ gives $\pi=i+\delta$ with $\delta=A-1-j\ge0$. Its parent is lower, so it crosses iff $i\ge k$. At a second center of actual label $n+s+A+b$ subtraction gives $\pi=s+b+1-i$, crossing iff $i<k$. The signs follow from the actual exterior bands flanking the gap and $n-c=d$. A correct image is crossing exactly when $\pi\ge K$.

Define $L_i=i,H_i=J-i$. The actual four folded rows are
$$
\begin{array}{c|cc}
 &L&H\\
\mathrm{source}&[0,k-1]&[\gamma,J-k]\\
\mathrm{image}&[0,K-1]&[\gamma,J-K].
\end{array}
$$
The H rows unfold to $[k,s-1]$ and $[K,s-1]$ and the L rows are their numeric complements in $[0,s-1]$. This includes the empty H-image row at $s=K$, with folded right endpoint $\gamma-1$. At a first center the maps within L and within H shift by $+\delta,-\delta$ respectively. At an actual second center with $b=b_0+\rho$ they exchange L to H with shift $-\rho$ and H to L with shift $+\rho$. These maps enforce the physical crossing test when both endpoints belong to their respective rows. A width increase by $\lambda$ adds $\lambda$ to all four right endpoints and $2\lambda$ to $J$.

Independently of any split, at every second host $\pi=s+b+1-i\ge b+2\ge\gamma$ on the whole numeric gap domain. First hosts have only the nonnegative translations $\pi=i+\delta$. Image 0 therefore requires source 0 with shift zero. Inductively each image $j<\min(s,\gamma)$ can come only from a first-host source $i\le j$; all $i<j$ are already used by the preceding forced identities. Hence the arrow is $j\mapsto j$ at the actual center of reduced label $A-1$. If that slot is a direct leaf the needed arrows are unavailable. If $s\le\gamma$, every image is forced to that neutral role, leaving no image for the $R-1\ge a+2>0$ actual residual second terminals. Thus a successful allocation on this fixed exterior has $s>\gamma$ and requires a neutral center with residual quota at least $\gamma$, excluding its selected exterior terminal if it is the selected first parent. This obstruction applies to all gap allocations on the specified exterior, including allocations outside the monotone model.

The exact global folded index moment is the sum of destination indices minus the sum of source indices. L gains $A$ successive indices beginning at $k$; H loses $A$ successive indices beginning at $J-K+1$, also at $s=K$. This gives $A(k-J+K-1)=A(B-\gamma)$. It is a geometric row identity prior to any split or matching.

## 3. Neutral reservations and full ordered split

For the monotone supplier require $B\ge\gamma$, and put $\Delta=B-\gamma$. Choose an actual positive neutral first center at $A-1$. Let $e_N$ be 1 if this is the selected first parent and 0 otherwise. Take $t\ge0$ such that
$$
\alpha_N-e_N\ge\gamma+2t,\qquad F\equiv\omega\pmod2,\qquad F\ge\omega+4+2t .
$$
Use the fixed neutral L identities on $[0,\gamma-1]$ and the $t$ additional neutral L/H pairs on $[\gamma,\gamma+t-1]$. At baseline the H-image row contains exactly $(F-\omega-4)/2\ge t$ positions and the H-source row is larger by $A$. The remaining lengths below show $k_0\ge\gamma+t$, so the L reservations are also admitted. Write $x_0=\gamma+t$, $N=a-1$, $k_0=1+(F+\omega)/2$. Index first slots by shift $j=0,\ldots,N$. The neutral residual is $\beta_0=\alpha_N-e_N-\gamma-2t$. At other actual positive centers subtract one precisely at the selected parent, and give every direct-leaf slot arithmetic residual zero. A selected quota-one center uses its only actual terminal in the exterior. An exhausted neutral has no further uses after the indicated reservations.

The leftover L-source and H-image position intervals start at $x_0$ and have lengths
$$
L^*=k_0-\gamma-t,\qquad H^*=(F-\omega-4)/2-t.
$$
Their difference is $\omega+3-\gamma=\Delta$ and their sum is $F-1-\gamma-2t=\sum_{j=0}^N\beta_j$. Both are nonnegative integers, since $H^*\ge0$ and $\Delta\ge0$. This establishes the L reservation bound even at an empty residual L row. Choose nonnegative $\ell_j,h_j$ summing to $\beta_j$ at each slot and to $L^*,H^*$ by row. An arithmetic choice exists by distributing $H^*$ up to the successive capacities and taking complements. Matching imposes its own further test.

Write $P_j^X$ for cumulative lengths through $j$ in row $X=L,H$, starting with $P_{-1}^X=0$. Increase the shift in both rows, using positions $[x_0+P_{j-1}^X,x_0+P_j^X-1]$ at shift $j$. Use $L_i\to L_{i+j}$ in L and $H_{i+j}\to H_i$ in H. This exhausts the exact L-source and H-image positions and assigns $\beta_j$ actual residual terminals to their respective parents. At any zero residual the group is empty, for each of the physical reasons above. When $N=0$, the residual neutral at shift zero is the sole group.

In the intermediate row (L images or H sources), group $j$ reserves
$$
[x_0+P_{j-1}^X+j,\ x_0+P_j^X+j-1].
$$
Group zero starts at $x_0$ and ends just before $g_0^X=x_0+P_0^X$. In general the column $g_j^X=x_0+P_j^X+j$ is immediately after group $j$, and group $j+1$ starts at $g_j^X+1$. The successive differences $g_{j+1}^X-g_j^X=1+(P_{j+1}^X-P_j^X)$ are positive even for empty groups. This gives a disjoint ordered interval-and-separator partition without gaps other than the listed separators. The final remainder is $[g_N^X,g_N^X+2]$: its right endpoint is $x_0+L^*+N+2=K_0-1$ on L and $x_0+H^*+N+2=J_0-k_0$ on H. The intermediate columns below $x_0$ were already filled by the reserved L identities on $[0,x_0-1]$ and H identities on $[\gamma,x_0-1]$. Hence
$$
G_X=\{x_0+P_j^X+j:0\le j<N\}\ \sqcup\ [x_0+P_N^X+N,x_0+P_N^X+N+2],
\qquad |G_X|=N+3=a+2 .
$$
The proof also gives the exact endpoints for empty leading, internal or final groups and entirely empty residual rows. The residual neutral group may consume $x_0$. At $N=0$, the three-cell suffix alone remains in each intermediate row.

## 4. Exact monotone baseline support

The positions left after §3 are precisely H sources $G_H$ and L images $G_L$. Completion exists within the model exactly when a bijection $h\mapsto l$ has $l-h\in\Gamma$ on every edge. This is the actual upper-host map derived in §2, so such a bijection gives all gap cells and conversely any legal completion at that split yields one. Its separation histogram plus the exterior-selected terminal at $\rho_s$ determines each $q_\rho$. In particular $q_0$ may include the selected terminal, or it may be zero when neither an identity nor that terminal uses Q. Equal minimum columns force an identity there because all separations are nonnegative, but the minima can differ. The total is $|G_H|+1=a+3$. Zero auxiliary counts describe the number of assigned actual terminals at a given stage, with all actual centers already exterior and every final actual quota positive.

A finite exact support test at fixed placements and $t$ enumerates the lengths $0\le\ell_j\le\beta_j$ of the prescribed total, taking $h_j=\beta_j-\ell_j$. For each claimed baseline histogram, remove the exterior count at $\rho_s$, rejecting negative counts. Process the H sources in order, trying each unused image with available separation and positive remaining multiplicity. Remove that image and decrement its multiplicity. At the empty source set require every image and count exhausted. Restricting any legal matching to its first pair and the remaining subproblem proves completeness. This arithmetic definition is exact within the ordered allocation, and was used symbolically.

Writing $D_j=P_j^L-P_j^H$ gives $D_{-1}=0$ and $D_N=\Delta$. The actual first-host moment by its row shifts is
$$
\sum_{j=0}^N j(\ell_j-h_j)=N\Delta-\sum_{j=0}^{N-1}D_j .
$$
The reserved arrows have zero contribution. The upper gap moment is $\sum G_L-\sum G_H$, where the sums are over individual columns in each set. The corresponding separators contribute $\sum_{j=0}^{N-1}D_j$ and the three suffix columns contribute $3\Delta$, independently of the chosen pairing. Their sum is $(N+3)\Delta=A(B-\gamma)$, agreeing with the separately derived geometric moment. For $N=0$ both separator sums are empty. Every baseline L source uses a first host, so $x=0$; every H image uses a first host, so $y=t+H^*=(F-\omega-4)/2$. These are actual counts of crossings at the cut.

## 5. Growth at the variable origin and finite indexed extraction

At baseline the four rows are bijected, the initial L identities on $[0,\gamma-1]$ are fixed, and every other endpoint has folded index at least $\gamma$. For $t>0$ the named neutral L pairs supply the consecutive bank $[\gamma,\gamma+t-1]$. A growth step of width $\lambda$ translates every noninitial endpoint by $\lambda$ at its original parent, keeping the initial arrows fixed. This preserves the signed displacements and leaves exactly $[\gamma,\gamma+\lambda-1]$ free in each row. When the old H-image row is empty, its right endpoint is $\gamma-1$ and the new row consists entirely of that strip.

For a step selecting $T$ initial bank arrows, remove their entire translated interval $[\gamma+\lambda,\gamma+T+\lambda-1]$ from both L rows. It is adjacent to the free strip. Restore the same named L identities to $[\gamma,\gamma+T-1]$. Both L free rows are now $[\gamma+T,\gamma+T+\lambda-1]$ and both H free rows are still $[\gamma,\gamma+\lambda-1]$. The entire translated bank was removed first, so even overlap for $\lambda<T$ meets no retained cell. Every unselected translated L endpoint was already above the removed interval. This is the [D184 free-set argument](ORDINARY_SPINE_EXCEPTIONAL_NEUTRAL_ANCHOR_BANK_GROWTH.md#2-removing-and-restoring-an-entire-bank) reestablished at the new origin.

For an actual positive separation $\rho$, at $T=\rho$ the new arrows
$$
L_{\gamma+\rho+j}\to H_{\gamma+j},\qquad H_{\gamma+j}\to L_{\gamma+\rho+j}
\quad(0\le j<\lambda)
$$
fill both directions exactly at $P_\rho$. This adds $2\lambda$ of its actual terminals and none at Q. In particular $\rho=1$ uses a single neutral L anchor, and arbitrary $\lambda$ works. For $1\le T<\rho$ and $\lambda=\rho b$ use the pairs
$$
L_{i+\rho j}\to H_{i+\rho(j-1)},\qquad H_{i+\rho(j-1)}\to L_{i+\rho j}
\quad(\gamma\le i<\gamma+T,\ 1\le j\le b)
$$
at $P_\rho$. The H list for each $i$ lies in the H strip and gives its entire residue class there; the L list gives the whole corresponding class in the L strip. Different $i$ use different residues. Translating the H strip by $T$ drops its first $T$ cells and adds the same residues at the far end because $\lambda$ is divisible by $\rho$. Thus after removing the indicated classes, the two remaining column sets coincide. Use Q in both directions at their common columns. This adds $2Tb$ at $P_\rho$ and $2(\rho-T)b$ at Q. Each of these operations keeps the same named prefix bank of width $T$, all first counts, the actual parents and the initial identities. Width zero acts as identity.

Given positive actual target quotas $p_\rho$ dominating their $q_\rho$ with matching parities, put $b_\rho=(p_\rho-q_\rho)/2$ at $\rho>0$. For $t\ge1$, use pure growth of width $b_\rho$ at $T=\rho$ if $\rho\le t$. Otherwise divide $b_\rho=tq+v$, $0\le v<t$, and use $q$ batches at $T=t$ and one at $T=v$ if $v>0$. Omit zero operations and order the rest by nonincreasing bank width, with separation and batch order breaking ties. Each step retains the bank needed by the next. The exact assigned Q cost is
$$
C_\rho=0\ (\rho\le t),\qquad
C_\rho=2(\rho\lceil b_\rho/t\rceil-b_\rho)\ (\rho>t).
$$
All costs are nonnegative even integers. Require $p_0\ge q_0+\sum_{\rho>0}C_\rho$ and let $\lambda_Q=(p_0-q_0-\sum C_\rho)/2$. With matching parity this is a nonnegative integer. When $t=0$, require $p_\rho=q_\rho$ at all positive separations and take $\lambda_Q=(p_0-q_0)/2$, with no shifted operations or division by $t$. Final Q-only growth uses the translation of noninitial endpoints described above, with the common strip filled in both directions by Q at matching indices. This supplies exactly $2\lambda_Q$ further actual Q terminals even at an empty bank and an initially empty H-image row. If $q_0=0$, positivity and even parity of the actual $p_0$ force at least two actual Q terminals, provided by the shifted-step Q costs and/or the Q-only strip.

The total width change is $\lambda_{\rm final}=\lambda_Q+\sum_{\rho>0}(b_\rho+C_\rho/2)$ for a positive bank, and $\lambda_Q$ for an empty bank. Each step exactly partitions its free rows. Its added opposite row-exchange arrows cancel in the signed moment, and every retained arrow keeps its signed displacement. Its L-to-H upper arrows increase $x$ by its width and it preserves the number of H-to-H first arrows. Hence $R=a+3+2\lambda_{\rm final}$, $x=\lambda_{\rm final}$, and $y=(F-\omega-4)/2$. The actual graph parities, all final quotas, and $x+y=s-K$ follow. A full bank $t\ge\max\Gamma$ incurs zero surcharge at each actual shifted host. This is a sufficient growth schedule for supplied baseline vectors.

For a deterministic supplier, use the actual indexed graph to order choices of first child placements, $j_e$, second child placements and $b_s$. Discard slot assignments failing the stated role and incidence conditions. The allowed selected first roles are exactly the actual positive first centers with $2\le j_e\le a+1$ and $j_e+1\le B$. Read $\Gamma$ from the resulting actual centers. For each such choice, try the finite admissible $t$ in increasing order and the finite row splits and actual-host matchings from §4 in lexicographic order. Test the resulting histogram against the final quota growth and full size admission, then extract the first passing allocation and apply the indicated schedule. Original indices break all ties, including equal quotas and leaf slots. Each finite choice is bounded by the input and the growth list is finite. The negative result of the arithmetic test concerns its defined model. No numerical enumeration of these choices was run for this investigation.

## 6. Embedding and single-center domains

### Exact D189 embedding

For the [D189 supplier](ORDINARY_SPINE_EXCEPTIONAL_WHOLE_SECTION_MONOTONE_ALLOCATION.md) take $j_e=3$, $b_0=2$, $\gamma=4$, $\rho_s=2$, distinct neutral and selected first parents, $\alpha_N=4+2t$, and $\beta_0=0$. D189's upper menu becomes $\Gamma$ after adjoining zero. The original selected terminal labels and all child slots agree. The new group zero is empty and its separator is exactly $x_0$; both rows have that minimum gap and therefore a Q identity. The capacity $F\ge\alpha_N+\omega$ becomes precisely $F\ge\omega+4+2t$. Row endpoints, split lengths, selected terminal histogram, target parities, growth strips and full admission then coincide, including the $t=0,s=K$ case. D188 remains a separate earlier arm.

### One positive second center

When $\nu=1$, Q is the selected second parent at $b_0=b_s=j_e+1$ and $\Gamma=\{0\}$. A legal gap matching requires identical gap sets, because all its differences are zero. In each sorted set its last three cells are the suffix. Equality at their largest cells forces $D_N=\Delta=0$. Equality of the preceding $N$ ordered separators gives $D_j=0$ for each $j<N$, so every $\ell_j=h_j$. For $N=0$ the suffix alone proves the same equality of the sole group's lengths. Thus existence of the required balanced split means every $\beta_j$ is even, subject to the stated capacity conditions; any split used in the construction must itself be balanced. Conversely, if all residual quotas are even and $\Delta=0$, the balanced split gives the exact row totals and identical gaps. The relation $B=\gamma=b_0+2$ forces $j_e=B-3=\omega$, so $2\le\omega\le a+1$. Every upper gap arrow is a Q identity, and Q also receives the selected terminal, yielding $q_0=a+3$. Under the fixed role, capacity, parity and independent admission conditions, this proves the exact characterization for the monotone baseline and Q-only growth model. It gives every actual sole quota $R\ge a+3$ of parity $a+3$ with full admission. For $\nu=1$ one has $\omega=z_2$; when $\omega=0$ or 1, a movable exterior may exist, but $\gamma=j_e+3\ge5>B$ and this baseline model cannot balance its suffixes.

### One positive first center

Let $a\ge1$ with exactly one positive first center and $a-1$ actual first direct leaves. Take that center as neutral and selected at $j_e=a+1$, with $b_0=b_s=a+2$, $\gamma=a+4$, and $\omega\ge a+1$. For $t\ge0$ use $F=\omega+4+2t$ and $\Delta=\omega-a-1$. Then $F-1-\gamma-2t=\Delta$ is all at shift zero. The capacity conditions hold with $H^*=0$ and $L^*=\Delta$. Put all those residual neutral uses in L. Every cumulative L length is $\Delta$ and every cumulative H length is zero, so $G_L=G_H+\Delta$.

If $\Delta=0$, take $\nu=1$ and $z_2=\omega=a+1$. The sole actual second center has the selected exterior terminal and all $a+2$ Q identities. Q-only growth gives the original family
$$
(a+5+2t,\underbrace{0,\ldots,0}_{a-1}),\qquad
(a+3+2z,\underbrace{0,\ldots,0}_{a+1})
$$
for integers $t,z\ge0$ and any physical order. Its exact size is $2K=4a+12+2t+2z$ and the independently supplied prefix must admit that full size.

If $\Delta>0$, put the two actual second centers at $b_0$ and $B-2=\omega+1$. The latter exceeds $b_0$ by $\Delta$ and is distinct from the removed slot $j_e$. Give the remaining $z_2=\omega-1$ actual direct leaves the other child slots. The ordered matching assigns every upper gap arrow at actual $P_\Delta$. The baseline has $q_0=1$ (selected terminal) and $q_\Delta=a+2$. With $t\ge1$ use §5 to grow positive dominating quotas of matching parities and the required Q cost, zero at $t\ge\Delta$. With $t=0$ keep $p_\Delta=a+2$ and grow Q by any even increase. These are original named targets for all physical orders and the full admitted size. Neither family requires an even neutral quota or two distinct first parents.

## 7. Direct symbolic controls and the guard boundary

Use the independent 74-edge input with actual maximum cut 39, frontier $s{:}27=74$, crossing differences $[37,74]$ and noncrossing differences $[1,36]$. The ordered profiles specify actual child indices, and zeros are original direct leaves. Use the first indexed first center as neutral. A, C, F and G select the second indexed first center, while B, D and E select neutral. Assign unused first slots and unused second leaf slots in increasing original index order. The second positive-center order below is the increasing upper-index order in each case.

| Case | Original first and second profiles | $a,\omega$ | $A,B$ | $j_e,b_0,b_s,\gamma$ | $F,R,2K$ | $t,\Delta$ |
|---|---|---|---|---|---|---|
| A | $(4,2,2),(2,1,2,1,0)$ | $3,4$ | $5,7$ | $3,2,4,4$ | $8,6,24$ | $0,3$ |
| B | $(6),(4,0,0)$ | $1,2$ | $3,5$ | $2,3,3,5$ | $6,4,16$ | $0,0$ |
| C | $(5,1),(5,0,0)$ | $2,2$ | $4,5$ | $2,3,3,5$ | $6,5,18$ | $0,0$ |
| D | $(7),(1,3,0,0)$ | $1,3$ | $3,6$ | $2,3,3,5$ | $7,4,18$ | $0,1$ |
| E | $(9,0),(4,3)$ | $2,1$ | $4,4$ | $3,2,4,4$ | $9,7,22$ | $2,0$ |
| F | $(5,1,0,0),(2,6,1)$ | $4,2$ | $6,5$ | $4,2,5,4$ | $6,9,24$ | $0,1$ |
| G | $(6,1,0),(2,6,0,0)$ | $3,3$ | $5,6$ | $3,2,4,4$ | $7,8,24$ | $0,2$ |

All the fresh sizes are admitted. Here are the actual baseline allocations, with gaps in folded columns.

- **A.** Upper positive indices are $2,4,5,6$. At $s=K=12$ take L lengths $(0,1,2)$, H lengths $(0,0,0)$, and $x_0=4$. Relative gaps are $G_H-x_0=\{0,1,2,3,4\}$ and $G_L-x_0=\{0,2,5,6,7\}$. The exact D189 matching $0\mapsto0,1\mapsto5,2\mapsto2,3\mapsto6,4\mapsto7$ gives baseline $(2,1,2,1)$ at $Q,P_2,P_3,P_4$. The H-image alphabet is empty.
- **B.** The sole second positive index is 3. After one exterior terminal and five fixed L identities at neutral, every remaining first group is empty. At $K=s=8$ the suffixes are $G_H=G_L=[5,7]$, and Q gets three identities and its exterior terminal, giving four. The original two second leaves are at upper indices 4 and 5.
- **C.** The quota-five center uses the five neutral L identities, and the quota-one selected first center uses its own terminal in the exterior. Both residual first groups are empty. At $K=s=9$ the two intermediate gap sets are $[5,8]$. Their four identities and the selected terminal give actual Q quota five at index 3. The two second leaves remain at indices 4 and 5.
- **D.** Upper indices 3 and 4 give Q and $P_1$. At $K=s=9$ the first center supplies its selected terminal, five fixed L identities and one residual L identity at 5. The gap sets are $[5,7]$ on H and $[6,8]$ on L. Translation by one gives all three uses at $P_1$, and Q uses its exterior terminal. The remaining upper indices 5 and 6 are the two actual leaves.
- **E.** The neutral is selected. Its residual eight uses supply four initial identities and two L/H pairs. The other first slot is a direct leaf at 2. The baseline has $K_0=10,s_0=12,x_0=6$ and both gap sets equal to $[6,9]$. Actual Q at 2 gets four identities and actual $P_2$ at 4 gets its exterior terminal. Pure width-one growth with bank width two supplies $(4,3)$ on the same actual graph. Both second children are centers.
- **F.** Upper indices $2,3,5$ are actual Q, $P_1$, $P_3$. The quota-five neutral at 5 uses the four initial identities and one residual L identity at 4. The selected quota-one center at 4 is exhausted in the exterior. Both direct leaves stay attached to $u$ at labels 2 and 3. At baseline $K_0=s_0=11$, $G_H=[4,9]$, $G_L=[5,10]$. Six uses at $P_1$ and the selected terminal at $P_3$ give $(0,6,1)$. Q already exists in the exterior, and a Q-only width-one step supplies its two actual terminals. Neither actual first center meets D189's even-neutral premise.
- **G.** Upper indices 2 and 4 give Q and $P_2$; actual direct leaves are at indices 5 and 6. Keep the two neutral residual uses in L at $t=0$, while the selected quota-one center is exhausted by its exterior terminal. At $K_0=s_0=11$ the gap sets are $[4,8]$ on H and $[6,10]$ on L. All five matches use $P_2$, which also supplies the selected terminal. From $(0,6)$ take a Q-only width-one step for $(2,6)$. D189's prescribed bank with neutral quota six required $F\ge9$ at this width; the actual $F=7$ passes the new allocation. This is a difference between the sufficient supplier domains.

The required adverse profiles $(3,1,0),(5,1)$ have $a=3,\omega=1,F=4,R=6$ and 17 fresh edges. Their edge count fits within 74, but gives no integer $K$. The lower graph count is even and $F\not\equiv\omega\pmod2$, so this original also fails the same-phase count condition. Every neutral residual candidate has capacity at most three and every movable-origin guard is at least four. Thus the guard obstruction independently applies to its fixed-exterior gap model. It gives no unrestricted gracefulness obstruction.

A parity-clean comparison isolates the guard. With $(3,2,0),(5,1)$ the same $a,\omega,R$ and $F=5$ give $2K=18$ and satisfy both graph parities and full size admission. Every neutral candidate still has at most three residual terminals. In contrast, $(4,1,0),(5,1)$ with the same counts uses the embedded $j_e=3,b_0=2$ placement, $t=0$, four fixed neutral identities, all zero residual groups and both gap sets $[4,8]$. Five Q identities plus the selected $P_2$ terminal complete that control. This matched pair isolates the obstruction on the low-capacity input. All controls here are symbolic arithmetic on original named topology.

One separately authorizable hybrid question concerns a changed phase. Append the already supplied [D157 return block](ORDINARY_SPINE_ALTERNATING_EXCEPTIONAL_SPECTRUM.md) $(5,2),(2,4,0)$ to the same independent input. Its parameters are $(r,t,p)=(2,1,1)$ and its 20 fresh edges give a common 94-edge named $S_0$ input. On that input, can the parity-clean low-capacity member $(3,2,0),(5,1)$ realize an exact terminal-enabled $S_0$-to-$S_0$ return with all direct leaves exterior, compared with $(4,1,0),(5,1)$ under the identical finite exterior and gap rules? The two 18-edge targets fit that common input. The $S_0$ first-host shift formula admits a negative shift at reduced label $A-1$, so the present induction does not settle that question. Require exact named incidences and spectra, and keep the proved $S_{-1}$ results for the matched originals on the 74-edge input as separate phase controls. This question is outside the completed investigation.

## 8. Named realization and both exact boundary inventories

At baseline assign each first arrow a distinct available actual terminal index at its original parent in fixed row and position order. At each upper host use the initial available indices for its baseline arrows, excluding its first indexed terminal if it is the selected parent. Growth arrows use further available indices of their actual parents. No stage exceeds any final physical count. The fixed and restored arrows retain the same names throughout. In particular absence of a Q arrow at baseline leaves its physical center and incidence to $w$ intact.

The baseline folded origin has $J_0=F+a+b_0+2$. At each actual lower shift $j$ form its numeric source set $S_j^{\rm b}$ from the L-source positions in §3 and the values $J_0-i-j$ at its H-image positions $i$. Its image set is $S_j^{\rm b}+j$. At the neutral, add its reserved initial and paired L identities on $[0,\gamma+t-1]$ and the separate reserved H identities at numeric values $J_0-i$ for $\gamma\le i<\gamma+t$. Its residual group is already included in $S_0^{\rm b}$. At a direct leaf there are no such sets to supply, and selected exterior terminals are excluded from the residual counts. The baseline first sets are disjoint in each alphabet by the four-row and unfolded partitions.

Write $\lambda=\lambda_{\rm final}$ and index each shifted step by its bank width $T_j$ and width increase $\lambda_j$. Each original extra neutral L identity at baseline index $i\in[\gamma,\gamma+t-1]$ ends in both rows at
$$
\phi(i)=i+\lambda-\sum_{j:\ i<\gamma+T_j}\lambda_j .
$$
A name still eligible at step $j$ was restored at each earlier step by the nonincreasing width order, hence is at its original index. Once excluded it moves up and cannot enter a later bank of weakly smaller width. The final Q-only translation restores none. The initial fixed identities remain unchanged. All other noninitial baseline endpoints, including neutral H endpoints and residual neutral L endpoints, gain the full folded translation $\lambda$. Each H endpoint of baseline index $i$ unfolds at $J_0+2\lambda$ to $J_0+2\lambda-(i+\lambda)=J_0-i+\lambda$. There is no bank case in this transport when $t=0$.

Define a map on baseline numeric resources by $\Phi(i)=i$ on $[0,\gamma-1]$, $\Phi(i)=\phi(i)$ on $[\gamma,\gamma+t-1]$, and $\Phi(i)=i+\lambda$ elsewhere. The first two intervals are exclusively occupied by those reserved neutral L identities in their respective baseline alphabets. Therefore this map takes each actual baseline first-host numeric source and image to its exact final coordinate. Its restored arrows are identities and the other first arrows translate both endpoints equally. The final sets are
$$
I=\bigsqcup_j \Phi(S_j^{\rm b}),\quad
J_1=\bigsqcup_j \Phi(S_j^{\rm b}+j),\qquad
I'=[0,s-1]\setminus I,\quad J_2=[0,s-1]\setminus J_1 .
$$
Here $j$ ranges over actual first centers. They are disjoint in their respective alphabets by the final bijections. These definitions use the actual new residual lists and named bank history.

For the minimum polarity shift old labels by $A$ below $c$ and by $A+s$ at or above $c$. The cut $C=c+K$ preserves sides because $A+c-1<C\le A+c+s$. Old crossing differences gain $s$, with other old differences fixed. Place a gap label $i$ at $A+c+i$. Retain the reduced low exterior labels and add $n+s$ to the reduced upper exterior labels. The shared frontier agrees at $v=A$ with the placed old value. All exterior edges cross since their low labels are at most $A<C$ and their upper labels at least $n+s+A+1>C$. The palettes are
$$
\begin{array}{ll}
L_{\rm old}=[A,A+c-1]\sqcup[A+c+s,n+s+A],&
L_{\rm fresh}=[0,A-1]\sqcup[A+c,A+c+s-1]\sqcup[n+s+A+1,m],\\
D_{\rm old}=[1,d-2]\sqcup[d-1+s,n+s],&
D_{\rm fresh}=[d-1,d+s-2]\sqcup[n+s+1,m].
\end{array}
$$
Since $m=n+s+A+B$, these partition $[0,m]$ and $[1,m]$. The exact exterior and gap bijections and actual old spectra exhaust each specified band once. The gap noncrossing differences are $[d-1,d+K-2]$ and the crossing ones are $[d+K-1,d+s-2]$, empty at $s=K$. Joining old, gap and exterior differences gives actual crossing $[d+K-1,m]$ and actual noncrossing $[1,d+K-2]$. The original graph extends at its original named incidences and its witnessing spine extends through $u,w$, with all fresh vertices within distance two. The frontier $w=0$ and $m=2C+2$ give exact $S_{-1}$ return.

At the first-section boundary define
$$
E_1=[2,A-1]\sqcup\{n+s+A+1,n+s+A+j_e\},\qquad
E_2=\{0,1\}\sqcup\{n+s+A+b:2\le b\le B,\ b\ne j_e\}.
$$
The child interval in $E_1$ includes its actual centers and direct leaves, and the two upper labels belong to $u$ and its section's selected terminal. The two lower labels of $E_2$ belong to $w$ and the selected second terminal. Its upper labels are precisely the actual children at $w$. The actual incidences of §1 give fresh exterior difference sets $D^e_1=n+s+[1,A]$ and $D^e_2=n+s+[A+1,A+B]$. In particular the literal unfinished incidence is $uw$ with endpoints $(n+s+A+1,0)$ and actual difference $n+s+A+1$ left in $D^e_2$. The exact inventories are
$$
\begin{array}{ll}
\mathrm{used\ labels}&L_{\rm old}\sqcup E_1\sqcup(A+c+I),\\
\mathrm{remaining\ labels}&E_2\sqcup(A+c+I'),\\
\mathrm{used\ differences}&D_{\rm old}\sqcup D^e_1\sqcup(d-1+J_1),\\
\mathrm{remaining\ differences}&D^e_2\sqcup(d-1+J_2).
\end{array}
$$
Old label bands retain their sides, and exterior labels use the placed reduced sides. Partition $I,I'$ at $k$ before adding $A+c$, and $J_1,J_2$ at $K$ before adding $d-1$, giving each inventory's lower and upper labels and noncrossing and crossing gap differences. The used exterior and old high bands are crossing, and the used old low differences are noncrossing. All remaining exterior differences cross.

For maximum polarity use input $n-G$ and complement the output at $m$. Its cuts are $n+1-c$ and $m+1-C$, the old lower and upper shifts are $B$ and $B+s$ because $2K=A+B+s$, and $w=m$. Both label inventories complement with swapped sides; the two difference inventories and their crossing partitions are preserved. The literal connector endpoints become $(B-1,m)$. For controls A through G the maximum cuts are respectively $51,47,48,48,50,51,51$, the final sizes $98,90,92,92,96,98,98$, and the crossing bands are $[37+K,m]$, with noncrossing band $[1,36+K]$ in each case.

## 9. Admitted composition and scope

Every output is an actual named $S_{-1}$ input with the corresponding polarity, regardless of which of D188, D189 or D190 supplies the next admitted block. For a finite such sequence use a common polarity. Each old map preserves its cut sides as the cut evolves. From actual completed cut $C_i$, let $U_i,V_i$ be the sums of later lower shifts and gap sizes. Then a completed label $x$ has final label $x+U_i+V_i\mathbf1_{x\ge C_i}$, by induction on those maps. Each earlier crossing difference gains $V_i$, while earlier noncrossing differences stay fixed. This transports both inventories and the literal connector; the remaining inventories also include subsequent fresh bands disjoint at their respective insertions. So arithmetic planning of local allocations and later shifts gives immutable final-alphabet realization of every original named vertex, with finite termination. For example the retained D188 extension of 52 edges, the admitted D189 control A here of 24 edges, and the D190 control B of 16 edges give $74\to126\to150\to166$, maximum cuts $39\to65\to77\to85$ and final crossing band $[83,166]$. Each uses its own independent incoming state on the continued actual graph and meets its full admission.

The movable proof gives the specified single-positive-center families and the exact baseline criterion at the chosen exterior and neutral capacities. The guard is stronger in scope than failure of the monotone criterion and concerns every allocation on that fixed exterior. General H1 feasibility, other exteriors, unrestricted gracefulness, independent initialization and arbitrary decomposition remain open. The investigation used symbolic proof and direct arithmetic only. No numerical search nodes, solver states, original-checker invocations, campaigns or historical replays were used.
