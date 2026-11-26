# D184 — Neutral anchor-bank growth on the wider exceptional exterior

Task **LCL-ORDINARY-SPINE-EXCEPTIONAL-NEUTRAL-ANCHOR-BANK-GROWTH-001**.

**PROVED WITHIN EXACT WRITTEN SCOPE / PENDING DIRECTOR REVIEW.** Retain the named D183 wider exterior and its independent baseline, with even $\nu=2+2\ell\ge4$, odd $r\ge2g+6+e$, $g\ge0$, $e=g\bmod2$, and exactly $2g$ positive odd first quotas. The other first quotas are positive even. Use distinct actual even first hosts at the neutral and deficit-two roles, of quotas at least six and at least $\nu$, respectively. Let $t=(\alpha_{\rm neutral}-4)/2$. Retain selectable numerical roles, no first direct leaf, the actual second direct leaf exterior, and an independently supplied named D157 $S_{-1}$ input admitted for the full target with $n\ge2K$.

The D183 baseline counts are $p_0^{(0)}=r-2$, $p_2^{(0)}=1$, $p_{\nu-1}^{(0)}=4$ and zero at all other shifted roles. At the target Q and $P_2$ have odd quotas, $p_{\nu-1}$ is even and at least four, and every other shifted quota is positive even. For $b_\rho=(p_\rho-p_\rho^{(0)})/2$, the following is a sufficient Q condition for terminal-enabled H1 in the declared arrangement:
$$
p_0\ge r-2+\sum_{\rho=2}^{\nu} C_\rho,\qquad
C_\rho=
\begin{cases}
0&\rho\le t,\\
2\big(\rho\lceil b_\rho/t\rceil-b_\rho\big)&\rho>t.
\end{cases}
$$
In particular, for $\alpha_{\rm neutral}\ge4+2\nu$ all shifted quotas can grow independently and the only Q condition for this supplier is its odd quota floor $r-2$. The bounds concern this construction. General H1 feasibility and D183's necessary graph threshold retain their separate scopes.

## 1. Baseline and exact fold

All quantities and labels are exact integers, excluding booleans. Intervals are inclusive and an inverted interval is empty. The [D157 named input](ORDINARY_SPINE_ALTERNATING_EXCEPTIONAL_SPECTRUM.md#1-interface-and-exact-inventory-rule) has $n=2c+2$ edges, actual extreme frontier $v$ at the end of its witnessing spine, and orientation $G(v)=0$. Write $d=c+2$. Its crossing weights at cut $c$ are $[d-1,n]$ and its noncrossing weights are $[1,d-2]$. Equality belongs to the upper side. Denote the two new actual spine vertices by $u,w$, the first terminal total by $F$ and the second total by $R$. The fresh named count is $2K=F+r+\nu+R+3$, including the two spine vertices, all centers and terminals, and the direct leaf. Write $m=n+2K$.

The accepted [D183 exterior](ORDINARY_SPINE_EXCEPTIONAL_UNBOUNDED_MULTI_UPPER_HOST.md#2-wider-named-exterior-folded-alphabets-and-moment) has $A=r+2,B=\nu+3$, reduced labels $v=A,u=A+1,w=0$, all first centers in $[2,A-1]$, Q at $A+2$ and $P_\rho$ at $A+2+\rho$ for $2\le\rho\le\nu$. The first indexed terminal at first-center label 3 receives $A+3$, the selected first indexed terminal at $P_2$ receives 1, and the literal direct leaf at $w$ receives $A+B$. These are exactly the reduced labels $[0,A+B]$. All exterior edges join opposite reduced sides and are connected through their actual named parent and spine edges. The first exterior differences are $[1,A]$, with 1 at $vu$, $[2,A-1]$ at the first centers and $A$ at the selected first terminal. The remaining differences are $[A+1,A+B]$, with $A+1$ at $uw$, $A+2$ at $wQ$, $A+3$ at the selected second terminal, $[A+4,A+\nu+2]$ at the shifted centers and $A+B$ at the direct edge.

For clarity write $z$ for the cumulative width increment at an intermediate stage, so $R_0=r+3$ and its allocation counts sum to $R_0+2z$. With $h=F/2-r-1$, the geometry has
$$
K=2r+5+h+\ell+z,\quad s=2K-A-B=3r+3+2h+2z,\quad k=K-A,\quad J=s+3 .
$$
The distinct neutral and deficit-two hosts give $h\ge t+\ell-g$: the neutral contributes $h_N=t$, the regular total promotion is $h_R\ge-g$ by its $2g$ odd quotas, and the tail promotion is $h_T\ge\ell$ by the even quota at least $\nu$. Thus $K-(A+B)=r-2+h-\ell+z\ge r-2-g>0$. The required inequalities $s\ge K$, $A\le K\le A+s$ follow at every stage. The full target size $n\ge2K$ is used at final placement. A baseline with zero counts at some exterior hosts is only an auxiliary allocation on these rows.

The numeric coordinate $i$ of a gap leaf has actual oriented label $A+c+i$ and is below the cut $C=c+K$ exactly for $i<k$. Subtracting its lower parent's reduced label $j_0$ gives difference $d-1+\pi(i)$ with $\pi(i)=i+\delta$, $\delta=A-1-j_0$. Subtracting its own label from an expanded upper host $n+s+A+b$ gives $\pi(i)=s+b+1-i$. The differences use these positive signs because the lower and upper host bands flank the gap. Using $L_j=j$, $H_j=J-j$, the exact folded alphabets are
$$
\begin{array}{c|cc}
 & L & H\\
\text{sources}&[0,r+2+h+\ell+z]&[4,2r+3+h-\ell+z]\\
\text{images}&[0,2r+4+h+\ell+z]&[4,r+1+h-\ell+z].
\end{array}
$$
The H-source and H-image windows unfold to $[k,s-1]$ and $[K,s-1]$. The L rows give their respective complements in $[0,s-1]$. Thus the lower host maps keep rows with increments $+\delta,-\delta$, and $P_\rho$ swaps rows with $-\rho,+\rho$, with Q using index identity across rows. For each legal arrow the H image occurs exactly when its source and actual host have opposite physical sides. The exact crossing predicate is $\pi(i)\ge K$. An increase of $z$ by an integer $\lambda\ge0$ grows every upper row endpoint by $\lambda$ and $J$ by $2\lambda$, with fixed lower endpoints.

The hypotheses of the independently supplied [D183 regular and tail allocation](ORDINARY_SPINE_EXCEPTIONAL_UNBOUNDED_MULTI_UPPER_HOST.md#3-signed-regular-strip-and-the-reusable-anchor) are met. Use the distinct eligible pair for neutral and deficit-two roles selected in §4, and order other hosts by index subject to the D183 minimum tail choice at deficit one. There are $r-2g\ge6+e$ even hosts for neutral, four tail roles, a reserved shift-one host and the even middle of a three-host packet when needed. The lower shifts $[1,r-5]$ admit that reserved host and $2g+e$ packet roles. D182's parity-neutral packets and the ordinary pairs use the same intermediate reservations and require zero shifted assignments. The signed regular endpoint is $r-2+h_N+h_R$, and its last footprint is at most $2r-7+h_N+h_R$, below the tail start $2r-5+h_N+h_R$. At the tail the actual deficit-two quota gives at least $\ell$ trailing shared pairs of deficit two, so the [D183 widened tail](ORDINARY_SPINE_EXCEPTIONAL_UNBOUNDED_MULTI_UPPER_HOST.md#4-wider-tail-and-baseline-quotas) transfers those $\ell$ H positions to new L positions. On the separated windows its L reservations add $[N-\ell-2,N+\ell-2]$ to its H reservations at the D183 tail coordinate $N=h_T+2$. The residual suffixes $[N-\ell-2,N-\ell+1]$ and $[N+\ell-1,N+\ell+2]$ match by $2\ell+1=\nu-1$, exactly four H-to-L arrows at $P_{\nu-1}$. All residual common columns use Q. These accepted local partitions supply the full independent baseline at $z=0$, with all L sources and H images at first parents, $r+2$ H-to-L uses at upper parents, and the exact baseline counts displayed above. In particular $x=0$ and $y=r-2+h-\ell$ for the crossing classes of lower sources at upper hosts and upper sources at lower hosts.

The first four neutral L identities are fixed at $[0,3]$. At each shared position $j\in[4,3+t]$ an additional ordinary neutral pair independently uses $L_j\to L_j$ and $H_j\to H_j$. They are distinct named terminals at the same actual neutral parent. The extra L identities give the initial neutral bank of width $t$. The H identities are ordinary noninitial arrows and can translate.

## 2. Removing and restoring an entire bank

The invariant at a growth stage consists of exact bijections of the current four rows, the four fixed initial L identities at their actual neutral parent, all other endpoints at least four, and a neutral L bank $[4,3+T]$ of available width $T\ge1$. The exterior still contains the same physical hosts Q and $P_\rho$. A step may choose a prefix of a wider available bank.

Increase the current cumulative width by $\lambda\ge1$. Retain the four initial identities, and translate every other folded endpoint by $\lambda$ at its actual parent. The folded maps are invariant under this common translation, and the new windows admit the translated cells. In each row the exact free strip is $S=[4,3+\lambda]$. Remove the entire selected bank of $T$ translated named L arrows. Its cells are $[4+\lambda,3+T+\lambda]$ in each L row, immediately above $S$. Thus the free set in each L row at this point is the entire $[4,3+T+\lambda]$. Restore those same named arrows at $[4,3+T]$, each L identity at its original index. This leaves
$$
\text{free L sources and L images }[4+T,3+T+\lambda],\qquad
\text{free H sources and H images }[4,3+\lambda].
$$
The proof includes $\lambda<T$. The two bank intervals then overlap, but all their former translated occupants were removed before restoration. Every other translated L endpoint starts at or above $4+T+\lambda$, since both old L rows used their entire first bank at the selected arrows. No retained assignment meets a restored cell. The H rows have only undergone translation. The fixed four and the restored bank use the same names at the same parents, preserving all first capacities. The new rows can be completed as below, retaining at least the selected bank width $T$.

## 3. Pure and partial growth

### Pure growth at width $T=\rho$

Choose the first $\rho$ available bank arrows. For arbitrary $\lambda\ge1$ the preceding free-interval result gives the L interval $[4+\rho,3+\rho+\lambda]$ and the H interval $[4,3+\lambda]$ in each alphabet. At the actual host $P_\rho$ use
$$
L_{4+\rho+j}\to H_{4+j},\qquad H_{4+j}\to L_{4+\rho+j}\quad(0\le j<\lambda).
$$
Each formula is the actual row map. They biject their respective free source and image intervals, disjoint across physical rows. The first direction crosses and the second does not. They use exactly $2\lambda$ additional leaves at $P_\rho$ and none at Q. All other host counts and the restored bank of width $\rho$ remain. The case $\lambda=1$ uses exactly the L index $4+\rho$ and H index 4 in both alphabets for any actual separation $\rho$. The removal-before-restoration argument applies even though $\lambda<\rho$. A zero increment is the identity operation.

### Partial growth at width $1\le T<\rho$

For $b\ge1$ let $\lambda=\rho b$. Select the first $T$ available bank arrows. For $i\in[4,3+T]$, the H free interval meets residue $i$ modulo $\rho$ in exactly $i,i+\rho,\ldots,i+\rho(b-1)$. The L free interval meets that residue in exactly $i+\rho,\ldots,i+\rho b$. The first L index in the list is at least $4+T$ since $\rho>T$, and the last is at most $3+T+\lambda$. The H list starts in $S$ and ends at most at $3+T+\lambda-\rho\le3+\lambda$. They give the precise portions of each interval since the neighboring indices on that residue fall outside. Use at the same actual $P_\rho$:
$$
L_{i+\rho j}\to H_{i+\rho(j-1)},\qquad
H_{i+\rho(j-1)}\to L_{i+\rho j}\quad(1\le j\le b).
$$
Distinct $i$ have distinct residues because $T<\rho$. Each pair of directions is bijective on the indicated pieces, using disjoint physical source and image rows. Removing those pieces leaves equal columns on every unselected residue: such a residue has no indices in the portion $[4,3+T]$ dropped when moving $S$ to $S+T$, or in the portion $[4+\lambda,3+\lambda+T]$ added at the far end. Use Q identities across rows on the identical complements. There are $\lambda-Tb$ such columns in each direction. No moved or new arrow meets an unchanged translated endpoint, because all are assigned within exactly the free sets of §2. The restored bank remains fixed at its actual parent. Thus
$$
\Delta p_\rho=2Tb,\qquad \Delta p_0=2(\rho-T)b ,
$$
with the other host quotas fixed. A zero batch is the identity.

The divisibility of $\lambda$ by $\rho$ is also necessary **for these free intervals at partial width with only Q and $P_\rho$ allowed on the unfilled cells**. Each such arrow preserves the folded index residue modulo $\rho$. Write $\lambda=\rho b+d_0$ with $0\le d_0<\rho$. The H free interval has $b$ representatives of every residue, plus one more on the cyclic block of $d_0$ successive residues beginning at 4. The L free interval has the corresponding excess block beginning at $4+T$. For $0<d_0<\rho$, the characteristic function of a cyclic block has exactly one transition from outside to inside around the cycle. Its initial residue is therefore identifiable from the excess counts. Equality of the residue counts forces $T\equiv0\pmod\rho$, impossible here. If $d_0=0$, the construction just given supplies both directions. The case $T=\rho$ has matching residues at every $\lambda$ and already has the pure completion. This necessary condition concerns only the stated partial-bank interval problem.

## 4. Exact target schedule and Q requirements

Use the baseline counts in §1. By the retained role parities and minima, every $b_\rho=(p_\rho-p_\rho^{(0)})/2$ is a nonnegative integer. If $\rho\le t$, schedule a pure operation at width $\rho$ with increment $\lambda=b_\rho$ when $b_\rho>0$. The Q cost is zero. If $\rho>t$, write
$$
b_\rho=tq_\rho+v_\rho,\qquad 0\le v_\rho<t .
$$
For $q_\rho>0$ schedule a partial operation using width $t$ and batch $q_\rho$. Its shifted increment is $2tq_\rho$ and Q cost $2(\rho-t)q_\rho$. For $v_\rho>0$ schedule a partial operation of width $v_\rho$ and batch one, with shifted increment $2v_\rho$ and Q cost $2(\rho-v_\rho)$. Summing gives exactly $2b_\rho$ at the actual shifted host and cost
$$
C_\rho=2\big(\rho(q_\rho+\mathbf1_{v_\rho>0})-b_\rho\big)
      =2\big(\rho\lceil b_\rho/t\rceil-b_\rho\big)
$$
to Q. At $b_\rho=0$ no operation is needed and the cost is zero. All costs are nonnegative even integers.

Globally order the nonidentity operations by nonincreasing selected width $T$, then increasing separation and listed operation order for ties. Each starts within the available bank since the initial width is $t$ and a completed step retains its own selected width. In particular a remainder operation does not deprive a later full-width operation of its required bank. Each step keeps every other noninitial endpoint at least four. This proves the induction on the finite list. For a numerical role assignment obeying the stated Q bound, $p_0$ and $r-2$ are odd so
$$
a=\big(p_0-(r-2)-\sum_{\rho=2}^{\nu}C_\rho\big)/2
$$
is a nonnegative integer. After all shifted operations, apply the [D183 Q-only strip](ORDINARY_SPINE_EXCEPTIONAL_UNBOUNDED_MULTI_UPPER_HOST.md#5-exact-growth-at-a-shifted-upper-host) of width $a$. Indeed translating all noninitial folded endpoints by $a$ at their parents leaves the same free interval $[4,3+a]$ in all four rows. Both Q directions match it exactly, increasing only Q by $2a$. The initial four identities remain fixed. The operation may shift the remaining neutral bank and is last.

With $\lambda_j$ denoting the width increase of operation $j$ on the finite shifted list, the full width change is
$$
\lambda_{\rm final}=a+\sum_j\lambda_j
=a+\sum_{\rho=2}^{\nu}(b_\rho+C_\rho/2),
\qquad R=r+3+2\lambda_{\rm final}.
$$
The equality follows either from each strip's count, or directly from the increments at the target parents. The successively added L sources at upper hosts number $\lambda_j$ in each shifted step and $a$ in the Q step. The number of L-to-L first arrows is constant, and the H-to-H first arrows keep their rows and count. Thus $x=\lambda_{\rm final}$ and $y=r-2+h-\ell$. Their sum is the required $s-K$ at the final geometry. All stage quotas increase to the exact target counts, making enough actual leaves available at each step.

At fixed baseline and role assignment, D183's Q growth surcharge per shifted role is $2(\rho-1)b_\rho$. Our pure cost is zero, and in the partial regime $\lceil b_\rho/t\rceil\le b_\rho$ for $t\ge1$ and $b_\rho\ge0$. Thus the bound is never larger than D183's. When $t\ge\nu$, every operation is pure. Ordering the nonzero increases by descending separation retains the bank needed for every later step. Each shifted role can grow by any independent allowed even increment at zero Q surcharge. The baseline still puts $r-2$ leaves at Q and the only additional Q leaves are prescribed by the actual odd target $p_0\ge r-2$.

All role selections can be made by finite arithmetic on the actual quotas. Among feasible ordered pairs for the neutral and deficit-two first roles, choose one maximizing the neutral quota, breaking ties by branch indices. This also maximizes $t$, and each $C_\rho$ is nonincreasing in $t$ by the ceiling formula and the transition to zero. For the second roles, there must be exactly two odd actual quotas to allocate to Q and $P_2$. Try both odd orders and each eligible even center of quota at least four for $P_{\nu-1}$, in original index order. At each such fixed triple of distinguished roles, minimize the stated cost by finite assignment of the remaining indexed even quotas to the remaining distinct separations. For example, evaluate the exact finite recurrence on subsets of unused even centers: for the next separation take the minimum, over centers still available, of its exact $C_\rho$ plus the residual minimum for the remaining separations, with base-case cost zero when there are no roles left. Distinguish centers of equal quota by their indices and break ties lexicographically. Fixed-role costs enter additively. Induction on the number of remaining roles proves this selects an admissible assignment whenever one meets the displayed bound. This arithmetic definition is part of the terminating supplier. No case search over labelings is involved and no rearrangement claim for the piecewise cost is needed.

## 5. Direct scope-separating control

For the specified actual sections $(12,4,2,2,2,2,2)$ and $(5,1,4,2,0)$, there are $g=0,r=7,\nu=4,\ell=1$. The zero entry denotes the original direct leaf. The totals are $F=12+4+5\cdot2=26$ and $R=5+1+4+2=12$, so $2K=26+7+4+12+3=52$. The retained independent input has $n=74\ge52$. The actual neutral capacity 12 gives $t=4$ and the distinct first quota four meets the deficit-two hypothesis. Here $R_0=10$, $h=5$ and $K_0=25$. The only numerical role order meeting the D183 parity, shifted minima and baseline Q floor is $Q=5,P_2=1,P_3=4,P_4=2$: the alternate odd order makes Q equal to 1 below $r-2=5$, and the two even quotas are forced by the minimum at $P_3$.

In that numerical assignment $b_4=1$ and $b_2=b_3=0$. D183's sufficient bound requires $5+2(4-1)=11$ at Q. D184 instead uses the width-four bank at indices $[4,7]$ and a pure $P_4$ increment of width one. In both L alphabets remove the translated bank on $[5,8]$ before restoring it on $[4,7]$. The free L index in both alphabets is then 8, and the free H index is 4. The actual $P_4$ uses $L_8\to H_4$ and $H_4\to L_8$, leaving Q at 5. This proves symbolic coverage at the actual target size and distinguishes the two sufficient bounds. D183's feasibility outside its bound is undecided by that bound. This control is a direct consequence of the theorem and the retained independent prefix data. Its arithmetic records no newly checked original certificate or campaign.

## 6. Named unfolding and both intermediate inventories

Choose the two exterior terminal indices and the direct leaf as in §1. At baseline give the prescribed arrows their actual terminal names by row and index order at each parent. In particular each neutral L identity is assigned its own named terminal, distinct from every neutral H identity. At each upper role use only its baseline number of actual terminal indices, with the exterior terminal at $P_2$ already reserved. Give each new arrow an available index at its specified parent. The ordered increases and the exact final counts in §4 ensure there are enough indices at every stage. Removed and restored neutral arrows keep their actual names and parent. Translations never change any named incidence. This is a construction from the named physical input and its quotas, including all actual branches and edges.

For each extra baseline neutral L identity, let $i\in[4,3+t]$ be its original folded index. At shifted step $j$ with bank width $T_j$ and increment $\lambda_j$, it is restored iff $i<4+T_j$. Indeed, if that inequality holds, it held for every prior step by nonincreasing widths, and the arrow is still at $i$ immediately before translation in step $j$. If it fails, any earlier restored steps kept the arrow at $i$, and any earlier steps that did not restore it could only increase its index. Its current index is therefore at least $i\ge4+T_j$, outside the selected bank. The same remains true at all later weakly smaller widths. This induction applies to the actual named arrow, even when a translated bank overlaps its restored positions. Its exact final source and image index is
$$
\phi(i)=i+\lambda_{\rm final}
      -\sum_{j:\,i<4+T_j}\lambda_j .
$$
The Q-only increment is in $\lambda_{\rm final}$ and never contributes to the subtraction. If there are no shifted operations the sum is empty. The initial four identities stay fixed. Every other noninitial baseline arrow gains the full folded shift $\lambda_{\rm final}$, including the extra neutral H identities. For a noninitial H endpoint, the new fold gives
$$
(J_0+2\lambda_{\rm final})-(j+\lambda_{\rm final})
=(J_0-j)+\lambda_{\rm final},\qquad J_0=3r+6+2h .
$$
Thus a numerically unfolded baseline H coordinate gains $\lambda_{\rm final}$, as does a baseline L endpoint translated in every step.

Use baseline numeric coordinates for both source and image alphabets. Put $E_0=[0,3]$, $E_t=[4,3+t]$, and define a coordinate action for baseline endpoints by
$$
\Phi(v_0)=
\begin{cases}
v_0&v_0\in E_0,\\
\phi(v_0)&v_0\in E_t,\\
v_0+\lambda_{\rm final}&\text{otherwise}.
\end{cases}
$$
In each alphabet the ranges $E_0,E_t$ are precisely the coordinates used by the initial and extra neutral L arrows. The folded bijections and guard windows ensure no unfolded H endpoint can occupy them. For each actual first host let $S_i^0$ be its numeric source set obtained by unfolding its baseline assigned arrows at $J_0$. Its exact baseline image set is $S_i^0+\delta_i$. Hence the final first gap sets are
$$
I=\bigsqcup_i\Phi(S_i^0),\qquad J_1=\bigsqcup_i\Phi(S_i^0+\delta_i).
$$
Here $\Phi$ on a set is its pointwise image. The simultaneous row partitions in §§2–4 prove that the two displayed unions are disjoint and that every endpoint lies in the correct current alphabet. In particular, the operation restores only identities, so $\Phi(S_i^0+\delta_i)=\Phi(S_i^0)+\delta_i$ for every actual first host. The exact remaining gap sets are $I'=[0,s-1]\setminus I$ and $J_2=[0,s-1]\setminus J_1$ at the final $s$. These formulas keep individual arrow identities even when a proper subset of the baseline bank is restored.

For actual minimum polarity, translate old labels by $A$ below $c$ and $A+s$ at or above $c$. The old bands preserve sides at $C=c+K$ by $A+c-1<C\le A+c+s$, and old crossing differences gain $s$ while noncrossing ones are fixed. Put gap label $A+c+i$ at its assigned source. Add $n+s$ to each upper reduced exterior label and keep each lower one. The shared frontier $v$ agrees at label $A$. Exterior endpoints are on opposite sides of $C$ since the lower ones are at most $A<C$, and the upper ones are at least $n+s+A+1>C$. The exact palettes are
$$
\begin{array}{ll}
L_{\rm old}=[A,A+c-1]\sqcup[A+c+s,n+s+A],&
L_{\rm fresh}=[0,A-1]\sqcup[A+c,A+c+s-1]\sqcup[n+s+A+1,m],\\
D_{\rm old}=[1,d-2]\sqcup[d-1+s,n+s],&
D_{\rm fresh}=[d-1,d+s-2]\sqcup[n+s+1,m].
\end{array}
$$
The disjoint old and fresh palettes exhaust $[0,m]$ and $[1,m]$ using $m=n+s+A+B$. The independent exterior spectra fill the exterior bands, counting the shared $v$ only in the old set. The final source and image bijections fill the remaining two bands on actual vertex labels and actual absolute edge differences. The physical predicate gives gap crossing weights $[d+K-1,d+s-2]$ and noncrossing weights $[d-1,d+K-2]$. Adding the old and exterior bands yields crossing spectrum $[d+K-1,m]$ and noncrossing spectrum $[1,d+K-2]$. Thus the return is exactly $S_{-1}$ with $w=0$, $m=2C+2$, and the extended actual witnessing spine.

At the boundary after the first of the two new sections, the first and remaining fresh exterior labels are
$$
E_1=[2,A-1]\sqcup\{n+s+A+1,n+s+A+3\},\qquad
E_2=\{0,1,n+s+A+2\}\sqcup[n+s+A+4,m].
$$
Their exterior differences are $D^e_1=n+s+[1,A]$ and $D^e_2=n+s+[A+1,A+B]$. The full intermediate inventories are
$$
\begin{array}{ll}
\text{used labels}&L_{\rm old}\sqcup E_1\sqcup(A+c+I),\\
\text{remaining labels}&E_2\sqcup(A+c+I'),\\
\text{used differences}&D_{\rm old}\sqcup D^e_1\sqcup(d-1+J_1),\\
\text{remaining differences}&D^e_2\sqcup(d-1+J_2).
\end{array}
$$
The old label bands and the exterior reduced sides give their exact lower and upper sets. For each of $I,I'$ intersect with $[0,k-1]$ and $[k,s-1]$ before adding $A+c$ for its lower and upper contributions. For each of $J_1,J_2$ intersect with $[0,K-1]$ and $[K,s-1]$ before adding $d-1$ for its noncrossing and crossing contributions. The used crossing set also contains $[d-1+s,n+s]$ and $D^e_1$, the remaining crossing set contains $D^e_2$, and the used noncrossing set contains $[1,d-2]$. This gives both exact intermediate inventories with their partitions, preserving the actual unfinished edge $uw$ with endpoints $(n+s+A+1,0)$ and crossing difference $n+s+A+1$ in $D^e_2$.

For the maximum polarity input use $n-G$ and complement the output about $m$. The actual cuts are $n+1-c$ and $m+1-C$. Since $2K=A+B+s$, the maximum-polarity actual lower and upper shifts are $B$ and $B+s$, replacing $A$ and $A+s$. Both label inventories complement and exchange sides, and all actual weights and crossing statuses remain fixed. The frontier $w$ has label $m$ and the literal connector endpoints are $(m-(n+s+A+1),m)=(B-1,m)$.

For a finite sequence of individually admitted blocks, keep each incoming actual named graph, frontier, cut, phase and spectra, and apply its own size and topology requirements. Each subsequent placement preserves the old sides relative to the evolving cut. At completed cut $C_i$, let $T_i^*$ be the sum of subsequent actual lower shifts and $S_i^*$ the sum of subsequent gap widths. The final map on that reached alphabet is $x\mapsto x+T_i^*+S_i^*\mathbf1_{x\ge C_i}$. The final crossing weights gain $S_i^*$ and noncrossing weights remain fixed. These maps lift the intermediate inventories and the literal connector endpoints and weight. The remaining sets taken in the full final alphabet also contain all subsequent fresh labels and differences, which are disjoint at every stage by the palettes. This proves individually admitted composition by induction. Finite arithmetic role selection, finite row lists and strips, and finite backward sums give the exact final label on each original named vertex for immutable emission. Independent initialization and arbitrary decomposition remain outside this construction.

## 7. Scope and retained evidence

The multianchor mechanism establishes both the partial and zero-surcharge sufficient domains symbolically. The residue obstruction is confined to the two free intervals under the two stated host maps. The necessary H1 graph threshold and the accepted D183 sufficient reservoir theorem remain intact. General placements and arbitrary quota roles remain separate. No hybrid investigation is needed for the stated symbolic objective.

D183 is Director accepted at checkpoint e9b7663f2dde8719027639f5a430a9c4d0d2abed within its exact written scope, including its wider exterior, four-arrow tail, signed regular allocation and single-anchor growth. D182 and earlier proofs retain their accepted scopes. The D174 history of one completed pair and two numerical arms with 3,518 unentered originals stays separate from D177's accepted 93-original symbolic projection with 92 historically unentered. The custody receipt records all zero scientific search, solver, campaign and historical replay counters, the exact held identities and the retained prefix checks.
