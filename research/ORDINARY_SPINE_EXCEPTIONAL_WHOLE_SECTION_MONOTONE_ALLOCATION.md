# D189 — Whole-section monotone allocation in the exceptional exterior

Task **LCL-ORDINARY-SPINE-EXCEPTIONAL-WHOLE-SECTION-MONOTONE-ALLOCATION-001**.

**PROVED WITHIN EXACT WRITTEN SCOPE / PENDING DIRECTOR REVIEW.** The construction supplies the original named target on an independently supplied, fully admitted D157 input when the indexed roles, whole-section split, actual-host gap matching and growth conditions below hold. The split and matching criterion is exact for this monotone baseline model. D188 remains a separate accepted supplier. General H1 feasibility remains open.

## 1. Named topology, graph classes and exterior

All sizes, quotas, coordinates and labels are integers, excluding booleans. Intervals are inclusive with inverted endpoints denoting the empty set. Let $r,\nu$ count actual positive centers on the two new sections and $z_1,z_2$ their actual direct leaves. Let $a=r+z_1$, $\omega=\nu+z_2-1$, and $F,R$ be the respective terminal totals. Require $r\ge2,a\ge3,\nu\ge2,\omega\ge1$. Choose distinct actual first centers for neutral quota $\alpha_N=4+2t$, $t\ge0$, and a selected first parent of any positive quota. Require $F\equiv\omega\pmod2$ and $F\ge\alpha_N+\omega$. These two hosts keep their own actual terminal incidences. Other actual positive first quotas are arbitrary positive integers. All direct leaves are exterior at their own spine parents.

Use the independent named [D157 $S_{-1}$ input](ORDINARY_SPINE_ALTERNATING_EXCEPTIONAL_SPECTRUM.md#1-interface-and-exact-inventory-rule) on $n=2c+2$ edges. In the minimum orientation the actual frontier $v$ has label zero, the upper side starts at $c$, and $d=c+2$ gives crossing differences $[d-1,n]$ and noncrossing differences $[1,d-2]$. The actual target extends the witnessing spine by $u,w$. Two spine edges, $a+(\omega+1)$ child edges, and $F+R$ terminal edges give $2K=F+a+\omega+R+3$ and $m=n+2K$. Full admission requires $n\ge2K$.

Root the fresh graph colors at the lower color of $v$. The lower color contains $w$, the first children and the second terminals. The upper color contains $u$, the second children and the first terminals. Thus $N_{\rm low}=1+a+R$ and $N_{\rm high}=\omega+2+F$. In the declared same-phase arrangement a connected crossing exterior identifies its sides with these colors. At widths $A,B$, the gap size is $s=2K-A-B$ and its sources split into $k=K-A$ lower and $s-k$ upper labels. Old crossing differences increase by $s$, so $s\ge K$ is required by the least returned crossing difference $d-1+K$. If $x$ lower sources go to upper hosts and $y$ upper sources to lower hosts, exactly those edges cross, filling the $s-K$ crossing gap differences. Counting the two colors at actual parents gives
$$
N_{\rm low}=A+s-k-y+x=2(A+x),\qquad
N_{\rm high}=B+k-x+y=2(B+y).
$$
In particular $R\equiv a+1$, $F\equiv\omega$ modulo two.

For the threshold in a terminal-enabled compatible exterior, $v=A$ has only $vu$ as a fresh incidence, so reduced difference one forces $u=A+1$. Compare summed reduced differences with the reference in which $vu,uw$ are present, every slot in $[1,A-1]$ attaches to $u$, and each slot $A+b$, $2\le b\le B$, attaches to $w=0$. The reference realizes every difference in $[1,A+B]$. A selected first terminal attaching to its actual lower parent of label $j>0$ decreases the sum by $j$. A selected second terminal attaching to its actual upper parent of index $b\ge2$ increases the sum by $b-1$. All direct leaves in the exterior keep their reference edges. Equality of the two sums requires both selections to be nonempty if either is nonempty. With all first children exterior, the fresh lower exterior count is $A=a+1+e_2$, where $e_2\ge1$ counts selected second terminals. Therefore $1+a+R=2(A+x)\ge2(a+2)$, or $R\ge a+3$. This argument concerns the declared terminal-enabled same-phase arrangement.

Supply the exterior with $A=a+2,\ B=\omega+3,\ v=A,\ u=A+1,\ w=0$. Assign all actual first children bijectively to $[2,A-1]$. Put the neutral center at $A-1$ and the selected first parent at 3. These are distinct since $a\ge3$. Its first indexed terminal has reduced label $A+3$. Put an actual second center Q at $A+2$. Choose $\Gamma\subseteq[2,\omega+1]$ of size $\nu-1$ containing 2. Such a menu exists because $1\le\nu-1\le\omega$. Give the remaining actual second centers the slots $A+2+\rho$ for $\rho\in\Gamma$, and give actual second direct leaves the complementary slots, exactly $\omega-(\nu-1)=z_2$ of them. Assign the first indexed terminal at $P_2$ reduced label 1. This supplies the bijection $[0,A+B]$. At $\omega=1$ the menu is $\{2\}$ with no second direct leaves. At $\omega=2$ the child slots beyond Q have separations 2 and 3, with 3 occupied by a center or a direct leaf according to the actual inventory.

The spine and every actual child and selected terminal edge connect the exterior. With reduced lower labels $[0,A]$ and upper labels $[A+1,A+B]$, all its edges cross. The edge $vu$ has weight 1. Actual first child edges have weights $[2,A-1]$ by subtracting their labels from $A+1$; the first selected terminal has difference $A+3-3=A$. The connector $uw$, edge $wQ$, and selected $P_2$ terminal have weights $A+1,A+2,(A+4)-1=A+3$. All remaining actual second child edges have differences $[A+4,A+B]$. In particular the final upper slot can be an actual center. Every edge and vertex in this construction belongs to the original topology.

## 2. Exact gap geometry and physical maps

Set $R_0=a+3$, $R=R_0+2z$ for cumulative width $z\ge0$. The original edge count gives
$$
K=a+3+(F+\omega)/2+z,\quad s=F+a+1+2z,\quad
k=1+(F+\omega)/2+z,\quad J=s+3 .
$$
Here $s-K=(F-\omega-4)/2+z\ge t+z$, $k>0$, and $A\le K\le A+s$. These inequalities include equality $s=K$. The full actual size admission covers all auxiliary widths.

At output cut $C=c+K$ the gap label at numeric source $i\in[0,s-1]$ is $A+c+i$. It is lower iff $i<k$. Image index $\pi$ denotes the actual difference $d-1+\pi$. At an actual first center with reduced label $j_0$ and shift $\delta=A-1-j_0$, subtraction gives $\pi=i+\delta$; its parent is lower, so the edge crosses iff $i\ge k$. At an actual second center with upper index $b$ and label $n+s+A+b$, subtraction gives $\pi=s+b+1-i$; its parent is upper, so the edge crosses iff $i<k$. These absolute signs follow from the lower and upper exterior bands flanking the gap and $n=2c+2$. A legal arrow must consequently have image $\pi\ge K$ exactly when its edge crosses. Use $L_j=j,H_j=J-j$ with the four folded rows
$$
\begin{array}{c|cc}
 &L&H\\
\mathrm{source}&[0,(F+\omega)/2+z]&[4,a+3+(F-\omega)/2+z]\\
\mathrm{image}&[0,a+2+(F+\omega)/2+z]&[4,1+(F-\omega)/2+z].
\end{array}
$$
The H source and image rows unfold to $[k,s-1]$ and $[K,s-1]$, respectively, and the L rows to their respective complements in $[0,s-1]$. The H-image row can be empty at baseline. The lower host maps stay in each row with index shifts $+\delta,-\delta$ on L and H. Upper host $P_\rho$ has $b=2+\rho$; its maps exchange rows with shifts $-\rho,+\rho$ on L and H. Q has $b=2$ and exchanges at equal index. These rules, with both endpoints in their indicated rows, enforce the actual crossing predicates, including the weak width case. There are no maps at direct-leaf slots. Increasing $z$ by $\lambda$ extends each folded right endpoint by $\lambda$ and increases $J$ by $2\lambda$.

## 3. Whole-section split and exact partitions

At baseline reserve the first four neutral L identities at $[0,3]$, and one L identity and one H identity at each index in $[4,3+t]$. The H identities exist because the right endpoint of the H-image row is $3+(F-\omega-4)/2\ge3+t$, and the H-source row contains these indices too. The neutral uses $4+2t$ actual terminals. Put $x_0=4+t$, $N=a-1$; the nonneutral slots are the increasing shifts $1,\ldots,N$. Let $\beta_j$ be their actual residual quota, $\alpha_j-1$ at shift $a-2$ and $\alpha_j$ elsewhere, with $\alpha_j=0$ only at actual direct leaves. A selected quota-one center has zero residual quota because its only terminal is already exterior. Both kinds of zero slot get no gap terminal.

The remaining L-source and H-image position intervals are $[x_0,x_0+L^*-1]$ and $[x_0,x_0+H^*-1]$, where
$$
L^*=(F+\omega)/2-3-t,\quad H^*=(F-\omega-4)/2-t .
$$
The hypotheses give integers $H^*\ge0,\ L^*-H^*=\Delta=\omega-1\ge0$, and $L^*+H^*=F-\alpha_N-1=\sum\beta_j$. Choose lengths $\ell_j,h_j\ge0$ with sum $\beta_j$ at each slot and respective totals $L^*,H^*$. Such lengths exist arithmetically, for example by distributing $H^*$ under the successive capacities and taking the complementary L lengths. A legal subsequent matching is a separate requirement. For $X=L,H$ let $P_j^X$ be the corresponding cumulative length, $P_0^X=0$. Assign the positions
$[x_0+P_{j-1}^X,x_0+P_j^X-1]$ at the actual shift $j$, as $L_i\to L_{i+j}$ on L and $H_{i+j}\to H_i$ on H. The consecutive lists exhaust both position alphabets and give $\beta_j$ uses at each actual parent. Every zero group is empty.

The L-image or H-source reservation interval of group $j$ is
$$
[x_0+P_{j-1}^X+j,\ x_0+P_j^X+j-1].
$$
Let $g_j^X=x_0+P_j^X+j$ for $0\le j\le N$. In increasing order from $x_0=g_0^X$, there is one separator $g_{j-1}^X$ immediately before each group $j$; that group is exactly the interval strictly between $g_{j-1}^X$ and $g_j^X$. In fact the difference of successive separators is one plus the corresponding length. This proves the same disjoint partition for leading, trailing and consecutive empty groups. After group $N$, the remaining suffix is $[g_N^X,g_N^X+2]$. The suffix endpoints are $x_0+L^*+N+2=a+2+(F+\omega)/2$ and $x_0+H^*+N+2=a+3+(F-\omega)/2$, the actual intermediate endpoints. Below $x_0$ the neutral consumes the L-image interval $[0,x_0-1]$ and H-source interval $[4,x_0-1]$. Thus the exact unused intermediate sets are
$$
G_X=\{g_j^X:0\le j<N\}\ \sqcup\ [g_N^X,g_N^X+2],
\qquad |G_X|=N+3=A .
$$
This is a partition by consecutive endpoints. It applies with an empty H split, even when there are also no neutral H identities. If $L^*=0$ then $H^*=0$. If all nonneutral residual quotas vanish, $F=\alpha_N+1$ forces $\omega=1$; both sets are identical and all upper assignments are Q identities.

## 4. Exact support of the monotone baseline

All remaining baseline arrows run from the H-source set $G_H$ to the L-image set $G_L$. They are exactly a bijection $h\mapsto l$ whose differences $\rho=l-h$ belong to $\{0\}\cup\Gamma$. Separation zero uses actual Q; each positive separation uses its indexed actual $P_\rho$. Every such matching fills the exact remaining cells and every legal completion within this model yields one. A separation occupied by a direct leaf is unavailable. Both minima are $x_0$, so the image $x_0$ can only receive the source $x_0$; it gives at least one Q use. Let $q_0$ count identities and $q_\rho$ count the positive separations, with one added to $q_2$ for its exterior terminal. Then $q_0\ge1$, and $q_0+\sum_{\rho\in\Gamma}q_\rho=A+1=a+3$. Auxiliary zero counts at actual shifted hosts are permitted. Actual target quotas are positive.

For a given claimed baseline histogram at fixed indexed roles, enumerate the finite length choices $0\le\ell_j\le\beta_j$ of the correct total with $h_j=\beta_j-\ell_j$. For each, subtract the one exterior $P_2$ use from the histogram. Starting with the least H source, a recurrence tries each unused L image with allowed separation of positive remaining count, removes that cell and decrements the count. The empty source list succeeds exactly when the image list and counts are exhausted. Necessity and sufficiency follow by restricting a complete matching to its first arrow and the remaining sources. This is an arithmetic characterization within the prescribed monotone model.

For the signed index moment let $D_j=P_j^L-P_j^H$, $D_N=\Delta$. The actual first-host contribution by the row shifts is
$$
\sum_{j=1}^N j(\ell_j-h_j)=N\Delta-\sum_{j=1}^{N-1}D_j .
$$
This is summation by parts, with zero contribution from neutral. Upper assignments contribute $\sum_{l\in G_L}l-\sum_{h\in G_H}h=3\Delta+\sum_{j=1}^{N-1}D_j$, since each corresponding separator difference is $D_j$ and the three suffix differences are $\Delta$. This holds for every legal matching. The global folded change independently equals the sum of the $A$ new L indices starting at $k$ minus the sum of the $A$ lost H indices starting at $J-K+1$. Its value is $A(k-J+K-1)=A(B-4)=(a+2)\Delta$, exactly the sum of the two contributions. All L sources at baseline go to first hosts, so $x=0$. All H images belong to first hosts; their number is $y=(F-\omega-4)/2$, counting the $t$ neutral H identities and the $H^*$ other assignments.

## 5. Bank growth and finite supplier

The first four L identities are fixed, all other endpoints have folded index at least four, and every baseline row is exhausted exactly. With $t\ge1$, the extra named neutral L identities give the consecutive bank $[4,3+t]$. These are the hypotheses of the [D184 bank operations](ORDINARY_SPINE_EXCEPTIONAL_NEUTRAL_ANCHOR_BANK_GROWTH.md#2-removing-and-restoring-an-entire-bank). At a selected width $T$, translate all noninitial endpoints by the width increase, remove the entire translated bank of width $T$, and restore its named L identities. For increase $\lambda$, each L free interval is $[4+T,3+T+\lambda]$; each H free interval is $[4,3+\lambda]$. This follows by subtracting the restored interval from the union of the open strip and the removed bank, also when the banks overlap. The unchanged endpoints stay in their rows. For $T=\rho$ both free interval pairs are matched by $P_\rho$ with shifts $-\rho,+\rho$, supplying $2\lambda$ terminals at that actual host. For $T<\rho$ and $\lambda=\rho b$, the $T$ residue paths from the original bank indices $i$ use $i+\rho j$ in L and $i+\rho(j-1)$ in H, $1\le j\le b$, in the two respective arrow directions. These distinct residue classes fill the displaced endpoints and leave identical residual columns for Q. They add $2Tb$ at $P_\rho$ and $2(\rho-T)b$ at Q. For either operation the $T$ named L identities stay at their original indices. All maps use only an actual indexed upper host and Q, including at possible separation $\omega+1$.

Require positive target quotas $p_\rho\ge q_\rho$ with $p_\rho\equiv q_\rho\pmod2$ at shifted roles and put $b_\rho=(p_\rho-q_\rho)/2$. For $\rho\le t$, use pure growth of width $b_\rho$. For $\rho>t$, divide $b_\rho=tq+v$ with $0\le v<t$, use the width-$t$ bank for $q$ batches and the width-$v$ bank for one batch if $v>0$. Empty batches are omitted. The exact costs of this schedule are
$$
C_\rho=\begin{cases}
0&\rho\le t,\\
2(\rho\lceil b_\rho/t\rceil-b_\rho)&\rho>t .
\end{cases}
$$
Sort the nonidentity operations by nonincreasing bank width, breaking ties by separation and original batch order. Every operation leaves a bank at least as large as the next one requires. Require $p_0\ge q_0+\sum C_\rho$ and $p_0\equiv q_0\pmod2$. Then $\lambda_Q=(p_0-q_0-\sum C_\rho)/2$ is a nonnegative integer. A full bank $t\ge\max\Gamma$ removes the growth surcharge for this baseline.

At $t=0$, require every shifted target quota equal its baseline quota. Take $p_0\ge q_0$ with matching parity and $\lambda_Q=(p_0-q_0)/2$. In either bank case Q-only growth fixes the initial four, translates the other folded endpoints by $\lambda_Q$, and fills the common strip $[4,3+\lambda_Q]$ in both row-exchange directions at actual Q. When the old H-image row is empty its right endpoint is 3, so its new row is exactly the new strip. Thus the proof uses the four fixed identities and row complements alone and applies at the empty-bank boundary.

The final increase is $\lambda_{\rm final}=\lambda_Q+\sum(b_\rho+C_\rho/2)$ for $t\ge1$ and $\lambda_Q$ for $t=0$. The exact second total is $R=a+3+2\lambda_{\rm final}$; all first counts stay fixed. Each width increase adds that many L-to-H upper arrows, and the H-to-H first arrows are unchanged in number. Thus $x=\lambda_{\rm final}$, $y=(F-\omega-4)/2$, and $x+y=s-K$. Every newly inserted pair of opposite row-exchange directions cancels in the signed folded moment, while preserved arrows keep their signed displacements. Full folded partitions follow from the matched free strips at every operation.

Choose roles by indexed finite enumeration of actual centers and exterior slots, preserving physical port and terminal order. Order compatible menus, splits and the recurrence choices in §4 lexicographically; take the first candidate meeting the target and admission conditions. Generate the bank list and identify each named assignment as in §7. These are finite arithmetic definitions, with no labeling search or campaign executed for this proof. Supply with the separate accepted D188 arm remains available on its exact domain. Its specialized baseline need not lie in the whole-section monotone model.

## 6. Infinite families and original controls

### Effective width one

Take $\omega=1,\nu=2,z_2=0$, an even neutral quota at least four, an actual positive odd selected quota and even quotas on the other nonneutral slots, allowing zero at direct leaves. Then $F\equiv1\pmod2$, $F\ge\alpha_N+1$ and the residuals are all even. The balanced splits $\ell_j=h_j=\beta_j/2$ give identical gap sets. Identity completion yields $q_0=a+2,\ q_2=1$. With $t\ge2$ every positive dominating target with matching parities and full size admission follows by pure $P_2$ and Q growth. With $t=1$ the schedule of §5 requires $2b_2$ additional Q uses before Q-only growth. With $t=0$ the covered case keeps $p_2=1$ and permits Q-only even increases.

### Small nonneutral quotas with $q_0=1$

Take $\omega\ge3$, $d_0=\lfloor(\omega-1)/2\rfloor$, $\varepsilon=(\omega-1)\bmod2$, and $a=r\ge d_0+3$. Use the qualifying neutral host, quota $1+\varepsilon$ at the selected shift $j_*=a-2$, and quota two at every other nonneutral shift. Then $F-\alpha_N=2a-3+\varepsilon\ge\omega$ and $F\equiv\omega\pmod2$. At the first $d_0$ shifts put both assignments in L. At $j_*>d_0$ put all $\varepsilon$ residual uses in L. Each other shift contributes one to each row. This gives $H^*=a-2-d_0,\ L^*=a-2+d_0+\varepsilon$.

Match gaps in increasing order. The initial pair has separation zero. The noninitial separators have respective differences $D_j$ for $1\le j<N$; the last three each have difference $\Delta$. Explicitly the positive histogram has one use at each of $2,4,\ldots,2(d_0-1)$, $a-2-d_0$ uses at $2d_0$, and four uses at $\Delta=2d_0+\varepsilon$. The latter comprise the last separator and the suffix. Add overlapping counts when $\varepsilon=0$, and add the exterior terminal at $P_2$. All noninitial differences are positive, so $q_0=1$. Require every used positive separation in the actual $\Gamma$. With $t\ge\max\Gamma$, all positive dominating targets of matching parities follow under full admission. This uses only small nonneutral quotas and does not decide other target histograms.

### Direct symbolic controls

In the following table the given ordered profiles record original child indices; each zero is an actual direct leaf. Quota tuples for Q and shifted roles are in numerical separation order. The retained independent prefix has 74 edges, actual maximum cut 39 and frontier $s{:}27=74$, with actual crossing differences $[37,74]$ and noncrossing differences $[1,36]$.

| Control | Actual first and second profiles | $a,\omega$ | $F,R,2K$ | $t$ | $\Gamma$ |
|---|---|---|---|---|---|
| A | $(12,4,2,2,2,2,2),(5,1,4,2,0)$ | $7,4$ | $26,12,52$ | 4 | $2,3,4$ |
| B | $(4,2,2),(2,1,2,1,0)$ | $3,4$ | $8,6,24$ | 0 | $2,3,4$ |
| B with Q growth | $(4,2,2),(4,1,2,1,0)$ | $3,4$ | $8,8,26$ | 0 | $2,3,4$ |
| C | $(8,1,0),(5,3)$ | $3,1$ | $9,8,24$ | 2 | $2$ |
| D | $(6,2,0),(3,3,0)$ | $3,2$ | $8,6,22$ | 1 | $2$ |
| E | $(12,2,2,2),(1,2,4,2,0)$ | $4,4$ | $18,9,38$ | 4 | $2,3,4$ |
| F | $(6,1,1,1),(2,5,0,0)$ | $4,3$ | $9,7,26$ | 1 | $2$ |

Each has $2K\le74$. In all use the first indexed center for neutral and the second indexed center for the selected parent, assigning remaining actual slots in increasing index order. For the new arm assign second numerical roles in the given positive port order and direct leaves in the remaining upper slots in increasing index order. Control A retains its [D188 arm](ORDINARY_SPINE_EXCEPTIONAL_DIRECT_LEAF_SLOT_CONSTRUCTION.md#6-symbolic-original-target-controls) and corresponding named role assignment instead. The table is direct arithmetic, with the exact placements as follows.

- **A.** The accepted D188 baseline is $(5,1,4,0)$; its pure width-one operation at $P_4$ supplies the target. This is the separate fallback control.
- **B.** At baseline $K=s=12,\ k=7,\ J=15$. The H-image alphabet $[4,3]$ is empty. Splits $(1,2),(0,0)$ give $L^*=3,H^*=0$ and relative gaps $G_H-x_0=\{0,1,2,3,4\}$, $G_L-x_0=\{0,2,5,6,7\}$. Pair $0\to0,1\to5,2\to2,3\to6,4\to7$, giving separations $0,4,0,3,3$ and full baseline $(2,1,2,1)$. Ordered matching would require separation one at its second pair. The matched Q-growth input adds only the two actual Q terminals, so $\lambda_Q=1$, $K=13,s=14$, and the H-image row is exactly the newly filled strip $[4,4]$. This is the $t=0$ operation.
- **C.** The actual selected quota-one center and actual first direct leaf both have residual zero for their distinct physical reasons. There are no nonneutral arrows. Both gap sets are $x_0+[0,4]$, giving $(5,1)$. The pure $P_2$ step at width one uses L index 6 and H index 4 in both directions and supplies $(5,3)$. There is no second direct leaf; the last upper slot is the actual $P_2$.
- **D.** Splits $(1,0),(0,0)$ give relative $G_H=\{0,1,2,3,4\}$ and $G_L=\{0,2,3,4,5\}$. Pair $0\to0,1\to3,2\to2,3\to5,4\to4$. The two shifted uses and selected terminal give $P_2=3$; Q uses three. Ordered matching would require the unavailable separation one. The last upper slot belongs to the actual second direct leaf.
- **E.** Splits $(2,1,1),(0,0,1)$ give cumulative separator differences $0,2,3$ and suffix differences $3,3,3$. This is the small-quota corollary with $\omega=4,d_0=1,\varepsilon=1$. The baseline is $(1,2,4,0)$. Pure $P_4$ width one supplies the last two target terminals, with Q unchanged. The actual selected quota is two, below D188's width-four quota requirement.
- **F.** Splits $(1,0,1),(0,0,0)$ use the middle shift for the selected quota-one center. The relative gap sets are $G_H=\{0,1,2,3,4,5\}$ and $G_L=\{0,2,3,5,6,7\}$. Pair $0\to0,1\to3,2\to2,3\to5,4\to6,5\to7$. Four matches use $P_2$ and two use Q, giving $(2,5)$ with the selected $P_2$ terminal. The two unavailable separations 3 and 4 are occupied by original direct leaves. All three nonneutral positive first quotas are one; the proof uses the actual residuals without parity packets.

For an adverse capacity case take $(6,1,0),(5,1,0,0)$. Here $a=3,\omega=3,F=7,R=6$; the baseline fresh size is 22, and $s=K=11$. The parity holds, but $7<6+3$ and $H^*=-1$. The empty H-image row cannot realize the required neutral H identity. This is the precise failure of the prescribed baseline with that neutral choice. General target feasibility remains open in this case. All controls are symbolic original-topology coverage or scoped arithmetic failures.

## 7. Named realization, exact resources and return

At baseline give each first arrow the name of one distinct residual terminal of its actual parent in fixed row and increasing position order. At each second host take the requisite initial available terminal indices for baseline uses, excluding the selected exterior terminal at $P_2$. Name additional arrows from the still unused target terminal indices of their actual host at each growth step. Every step is within the final physical count and the final arrows use exactly all available indices. This makes the baseline and each growth stage a construction from the named target parameters, with unchanged parent identities. Direct leaves get their own exterior labels and edges in §1.

Write $J_0=F+a+4$. For actual positive nonneutral first host $j$, its baseline numeric gap source set $S_j^{\rm b}$ is the union of its L-source positions and $\{J_0-i-j : i \text{ is its H-image position}\}$, with both position intervals given in §3. Its baseline image set is $S_j^{\rm b}+j$. For neutral, the source and image sets coincide and are $[0,3+t]\sqcup\{J_0-i:4\le i\le3+t\}$. Direct-leaf slots have no terminal sets. The selected terminal stays exterior even at a quota-one parent. All named first-gap sets are disjoint in their respective baseline alphabets by the explicit partitions.

Let shifted growth step $j$ restore width $T_j$ and increase width by $\lambda_j$, and write $\lambda=\lambda_{\rm final}$. For a named extra neutral L identity at baseline index $i\in[4,3+t]$ the final index in both rows is
$$
\phi(i)=i+\lambda-\sum_{j:\ i<4+T_j}\lambda_j.
$$
Each such name still eligible at step $j$ was restored earlier under the nonincreasing width order, so is at its original index. Once ineligible, it stays outside each later bank and gets every remaining translation. The final Q-only step restores none. The initial four identities remain fixed. Every other noninitial endpoint gains the full folded shift, including the neutral H identities. Its H unfolding is $J_0+2\lambda-(i+\lambda)=J_0-i+\lambda$ for a baseline H index $i$. At $t=0$ the extra neutral interval and restoration sum are absent. Thus define the transport on baseline numeric endpoints by
$$
\Phi(i)=
\begin{cases}
i&0\le i\le3,\\
\phi(i)&4\le i\le3+t,\\
i+\lambda&\text{otherwise}.
\end{cases}
$$
The first two cases are occupied solely by the initial neutral L identities and the extra neutral L bank in each numeric alphabet. Every other first arrow retains its actual numeric lower translation. Writing $\delta_j$ for the shift of actual first center $j$, including neutral, the first and remaining source and image resources are
$$
I=\bigsqcup_j\Phi(S_j^{\rm b}),\quad
J_1=\bigsqcup_j\Phi(S_j^{\rm b}+\delta_j),\qquad
I'=[0,s-1]\setminus I,\quad J_2=[0,s-1]\setminus J_1 .
$$
The unions are disjoint by the growth partitions and numeric unfolding. These sets follow from the new monotone first lists and their named transport.

For minimum polarity place old labels by adding $A$ below $c$ and $A+s$ at or above $c$. The inequalities $A+c-1<C\le A+c+s$ preserve their sides. Old differences crossing $c$ gain $s$; old noncrossing differences stay fixed. Place gap source $i$ at $A+c+i$, and shift each upper reduced exterior label by $n+s$, leaving the reduced lower labels fixed. The shared $v=A$ coincides with its old placed label and is counted once. All exterior edges cross the actual cut since their lower endpoints are at most $A<C$ and upper endpoints at least $n+s+A+1>C$. The exact palettes are
$$
\begin{array}{ll}
L_{\rm old}=[A,A+c-1]\sqcup[A+c+s,n+s+A],&
L_{\rm fresh}=[0,A-1]\sqcup[A+c,A+c+s-1]\sqcup[n+s+A+1,m],\\
D_{\rm old}=[1,d-2]\sqcup[d-1+s,n+s],&
D_{\rm fresh}=[d-1,d+s-2]\sqcup[n+s+1,m].
\end{array}
$$
They partition $[0,m]$ and $[1,m]$ since $m=n+s+A+B$. The actual exterior differences, gap permutations and old spectra exhaust their indicated intervals once. Physical gap crossings fill $[d+K-1,d+s-2]$ and gap noncrossings $[d-1,d+K-2]$; the former is empty if $s=K$. Combining the three actual spectra yields crossing differences $[d+K-1,m]$ and noncrossings $[1,d+K-2]$. The attached vertices preserve the original tree and the witnessing spine through $u,w$, with distance at most two from it. As $m=2C+2$ and $w=0$, this is precisely the minimum-oriented $S_{-1}$ return.

At the first-section boundary the exact fresh exterior label sets are
$$
E_1=[2,A-1]\sqcup\{n+s+A+1,n+s+A+3\},\qquad
E_2=\{0,1,n+s+A+2\}\sqcup[n+s+A+4,m].
$$
The interval of $E_1$ consists of the actual first children at $u$; its two upper labels belong to $u$ and the first selected terminal. The two lower labels in $E_2$ belong to $w$ and the selected terminal at actual $P_2$. Its other labels are Q and the actual shifted centers and second direct leaves in their assigned slots. By their actual edges the exterior difference bands are $D^e_1=n+s+[1,A]$ and $D^e_2=n+s+[A+1,A+B]$. The literal unfinished connector $uw$ has endpoints $(n+s+A+1,0)$, and its difference $n+s+A+1$ belongs to $D^e_2$. Consequently
$$
\begin{array}{ll}
\text{used labels}& L_{\rm old}\sqcup E_1\sqcup(A+c+I),\\
\text{remaining labels}& E_2\sqcup(A+c+I'),\\
\text{used differences}& D_{\rm old}\sqcup D^e_1\sqcup(d-1+J_1),\\
\text{remaining differences}& D^e_2\sqcup(d-1+J_2).
\end{array}
$$
Lower and upper old labels are their two bands in order. Exterior sides are the reduced sides carried to their placed values. Split $I,I'$ at $k$ before adding $A+c$. Split $J_1,J_2$ at $K$ before adding $d-1$; their upper pieces are crossing differences. Used crossing differences additionally include $[d-1+s,n+s]$ and $D^e_1$, remaining crossing differences include $D^e_2$, and used noncrossings include the old $[1,d-2]$.

For maximum polarity use the input $n-G$ and complement the output at $m$. The actual cuts are $n+1-c$ and $m+1-C$, the old lower and upper shifts are $B$ and $B+s$ by $2K=A+B+s$, and $w=m$. Both label inventories complement and exchange sides, and both difference inventories with their crossing partitions are preserved by endpoint subtraction. The connector becomes $(B-1,m)$. On the retained 74-edge maximum input the output cut is $39+K$ and crossing differences are $[37+K,m]$. In table order these cuts are $65,51,52,51,50,58,52$ at $m=126,98,100,98,96,112,100$, respectively.

In any finite sequence of individually admitted blocks, each takes its actual incoming named graph, cut, extreme frontier and prescribed spectrum. Orient all in the chosen common polarity. Each old map preserves sides as its cut evolves and each block returns the same phase, so this uses no restriction on the earlier arm beyond its actual returned interface. For a local completed cut $C_i$, let $U_i,V_i$ be the sums of later lower shifts and gap sizes. Each local completed label $x$ has final label $x+U_i+V_i\mathbf1_{x\ge C_i}$; each earlier crossing weight gains $V_i$ and each noncrossing difference is fixed. This follows inductively by side preservation. It transports the literal connector endpoints and both cut-partitioned inventories; the remaining resources also include later fresh values, disjoint by the palettes at their insertions. For example A's D188 arm gives $74\to126$, then B's admitted 24-edge block gives $126\to150$, with maximum cuts $39\to65\to77$ and final crossing differences $[75,150]$. Each local step uses its own actual named incidence data and exact size. Computing the finite local allocations and backward sums allows emitting immutable final-alphabet labels on each original named vertex. Finite role and split sets, finite gap matching, finite growth quotas and a finite list of admitted blocks give termination. No universal initialization or decomposition follows.

## 8. Scope

The principal result replaces the first allocation by one whole ordered split and exact local gap matching. It removes the packet and four-host-tail premises on its supplied domain, including the prescribed first parity patterns, deficit-two quota bound and old minimum center counts. D188 remains a separate accepted construction arm, with no embedding into this split asserted. Neither the capacity failure, unavailable host in a prescribed matching, nor a negative within this finite arithmetic model decides unrestricted H1 or ordinary gracefulness. One-positive-second-center cases and arbitrary decomposition remain open. The proof uses direct symbolic arithmetic on named profiles. There were no numerical search nodes, solver states, original-checker calls, scientific campaigns or historical replays.
