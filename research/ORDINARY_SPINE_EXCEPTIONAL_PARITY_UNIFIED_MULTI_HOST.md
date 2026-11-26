# D187 — Parity-unified multi-host construction on the wider exceptional exterior

Task **LCL-ORDINARY-SPINE-EXCEPTIONAL-PARITY-UNIFIED-MULTI-HOST-001**.

**PROVED WITHIN EXACT WRITTEN SCOPE / PENDING DIRECTOR REVIEW.** Let $\eta\in\{0,1\}$, $\nu=2+2\ell+\eta$ with $\ell\ge1$, and $r\ge2g+6+e$, where $g\ge0$ and $e=g\bmod 2$. There are exactly $2g+\eta$ positive odd first quotas, with the rest positive even. Choose distinct actual qualifying hosts, one even of quota at least six for neutral and one of quota at least $\nu$ and parity $\eta$ for deficit two. Retain the named topology and independently admitted D157 $S_{-1}$ input of §1. The unified exterior and tail in §§1–3, the D186 baseline selection, and the D184 bank schedule in §4 supply the positive actual targets that satisfy the stated domination, parity and Q-cost conditions. Both parities of each center count are admitted. At $\eta=0$ and odd $r$ the complete accepted D186 domain is recovered. General H1 feasibility has a separate scope.

## 1. Actual counts, exterior and fold

All structural parameters and labels are exact integers, excluding booleans. Intervals are inclusive and inverted intervals are empty. The independently supplied [D157 named input](ORDINARY_SPINE_ALTERNATING_EXCEPTIONAL_SPECTRUM.md#1-interface-and-exact-inventory-rule) has $n=2c+2$ edges, a witnessing spine ending at its actual extreme frontier $v$, and oriented label $G(v)=0$. At cut $c$ equality is on the upper side. With $d=c+2$, crossing and noncrossing spectra are $[d-1,n]$ and $[1,d-2]$. Append the two actual spine vertices $u,w$. There is no first direct leaf. At the second section exactly one actual direct leaf is exterior. All actual centers and positive terminal quotas belong to the original target. Write $F,R$ for the full first and second terminal totals. Counting spine, centers, terminals and direct leaf gives
$$
2K=F+r+\nu+R+3,\qquad m=n+2K,\qquad n\ge2K
$$
for the final target.

For the same-phase connected crossing exterior and leaf-only gap of the declared arrangement, root the fresh graph colors at lower $v$. Lower fresh vertices are $w$, the $r$ first centers and the $R$ second terminals. Upper fresh vertices are $u$, the $\nu$ second centers, the direct leaf and the $F$ first terminals. Thus $N_{\rm low}=1+r+R$, $N_{\rm high}=\nu+2+F$. In any compatible placement with exterior widths $A,B$, gap width $s=2K-A-B$ and $k=K-A$, the crossing exterior identifies its graph colors with its reduced sides. Let $x$ count lower gap sources at upper hosts, and $y$ upper gap sources at lower hosts. The exact gap weight interval starts at $d-1$, of which images $[K,s-1]$ cross, so $x+y=s-K$. The lower and upper gap color counts from their actual host colors give
$$
N_{\rm low}=A+s-k-y+x=2(A+x),\qquad
N_{\rm high}=B+k-x+y=2(B+y).
$$
Here $s\ge K$ is required by the smallest translated old crossing weight $d-1+s$. In particular $R\equiv r+1$ and $F\equiv\nu$ modulo two are necessary in this same-phase arrangement.

In a terminal-enabled compatible exterior the two terminal selection counts $e_1,e_2$ are both positive. Indeed the weight-one edge joins reduced $A,A+1$ and must be $vu$ since the old shared frontier $v=A$ has just this new incidence. Compare the reduced spectrum to the tree with $vu,uw$, all lower slots $[1,A-1]$ attached to $u$, and all upper slots $A+b$, $b\ge2$, attached to $w$. The spectra have equal sums since both are $[1,A+B]$. A first selected terminal decreases the reference sum by its actual positive lower parent's label. A second selected terminal increases it by its actual upper parent's index $b-1$, which is positive. Thus if one section selects any terminals, both must do so. In that case $A=r+1+e_2$ and the lower count gives $R\ge r+3$. These necessary conditions concern the declared arrangement.

For the actual supplier retain the [D183 reduced exterior](ORDINARY_SPINE_EXCEPTIONAL_UNBOUNDED_MULTI_UPPER_HOST.md#2-wider-named-exterior-folded-alphabets-and-moment) with the actual $\nu$ here. Set $A=r+2$, $B=\nu+3$, $v=A,u=A+1,w=0$. The actual first centers have reduced labels $[2,A-1]$. Choose the first indexed terminal at first parent 3 for reduced $A+3$. Put Q at $A+2$ and the actual shifted host $P_\rho$ at $A+2+\rho$ for $2\le\rho\le\nu$. Put its selected first terminal at label 1 for $\rho=2$ only. The actual direct leaf of $w$ receives $A+B=A+\nu+3$. These distinct labels exhaust $[0,A+B]$. The exterior is connected by the two spine edges, actual center-parent edges and the three leaf-parent edges. All cross opposite reduced sides. The exact weight bands by incidence are:

- $1$ at $vu$, $[2,A-1]$ at the first centers, and $A$ at the selected first terminal.
- $A+1$ at $uw$, $A+2$ at $wQ$, $A+3$ at the selected terminal of $P_2$, $[A+4,A+\nu+2]$ at the shifted centers, and $A+B$ at the actual direct leaf.

Thus both reduced spectra hold for both $r$ parities and both $\eta$. When $\eta=1$ the upper host list has the additional actual final center, and the direct leaf takes the new endpoint $A+B$. The actual first and second terminal selections require only one original terminal at each prescribed parent. Every actual center stays in the exterior, even if an auxiliary baseline puts no terminals at its gap positions.

Let $t=(\alpha_{\rm neutral}-4)/2$, $h_N=t$, $h_R=(\sum_{\rm regular}\alpha-2(r-5))/2$, $h_T=(\sum_{\rm tail}\alpha-8-\eta)/2$ and $h=h_N+h_R+h_T$. The $\eta$ odd tail contribution is confined to deficit two. The $2g$ odd regular quotas contribute an even sum of at least $2g$, and the other regular quotas are at least two. Thus $h_R$ is an integer at least $-g$. Write the four tail quotas as $\alpha_d=2+2v_d+\eta\mathbf1_{d=2}$, $1\le d\le4$, with nonnegative integers $v_d$ and $v_2\ge\ell$ by $\alpha_2\ge\nu$. This proves $h_T=\sum v_d\ge\ell$. Adding the neutral count, regular sum and tail sum gives $F=2r+2+2h+\eta$. In particular $F\equiv\nu\pmod2$. Use $R_0=r+3$ and $R=R_0+2z$ at cumulative width $z\ge0$, which gives $R\equiv r+1\pmod2$. Substituting into the original edge count yields
$$
K=2r+5+h+\ell+\eta+z,\qquad s=2K-A-B=3r+3+2h+\eta+2z,\qquad
k=K-A,\quad J=s+3.
$$
Since $h\ge t-g+\ell$ and $t\ge1$, $K-(A+B)=r-2+h-\ell+z>0$. Hence $s\ge K$ and $A\le K\le A+s$. Every stage width is at most its admitted actual target width.

A gap coordinate $i$ has oriented label $A+c+i$ and is lower at $C=c+K$ iff $i<k$. Subtracting its lower reduced parent label $j_0$ gives difference $d-1+\pi(i)$ with $\pi(i)=i+\delta$, $\delta=A-1-j_0$. At an upper parent of label $n+s+A+b$ the subtraction gives $\pi(i)=s+b+1-i$. The flanking host bands ensure the positive signs of these differences. Use $L_j=j$, $H_j=J-j$ and the exact rows
$$
\begin{array}{c|cc}
 &L&H\\
\text{sources}&[0,r+2+h+\ell+\eta+z]&[4,2r+3+h-\ell+z]\\
\text{images}&[0,2r+4+h+\ell+\eta+z]&[4,r+1+h-\ell+z].
\end{array}
$$
Indeed H sources unfold to $[k,s-1]$ and H images to $[K,s-1]$, with L rows giving their respective complements in $[0,s-1]$. First-host arrows keep their row with index changes $+\delta$ on L and $-\delta$ on H. An upper host $P_\rho$ swaps rows with $-\rho$ on L and $+\rho$ on H, and Q swaps at equal index. These rules follow from the actual subtractions, with the H image corresponding exactly to a physical crossing, namely $\pi(i)\ge K$. At fixed $h,z$ and other parameters, increasing $\eta$ by one adds one cell to each L row and keeps both folded H index intervals. The numerical H coordinates themselves increase by one at fixed folded index because $J$ increases by one. A width change by $\lambda$ increases each of the four upper endpoints by $\lambda$, and increases $J$ by $2\lambda$.

The required folded signed moment, sum of image indices minus sum of source indices, is $A(B-4)$. The L images add the interval of length $A$ starting at $k$, and H images remove the interval of length $A$ starting at $J-K+1=k+4-B$. The two interval sums differ by $A(B-4)$. This holds at all stage widths. The construction's signed contributions are checked below.

## 2. Regular roles, local packets and their bounds

Reserve an actual qualifying neutral host and a distinct deficit-two host. There are $r-2g-\eta\ge6+e-\eta$ even hosts. The neutral, other three tail hosts, reserved shift-one host and any even three-host-packet middle require $5+e$ even hosts. The deficit-two role needs one additional even host exactly when $\eta=0$, for $6+e-\eta$ in total. When $\eta=1$ its one odd host is reserved and the other $2g$ odd hosts enter the regular packets. Among the three even tail choices put a smallest quota at deficit one, breaking ties by index, and give the two remaining even tail roles by index. This makes $v_3\ge v_1$. The neutral label is $A-1$. Positive first shifts are $[1,r-1]$, with $[1,r-5]$ regular and deficits $d=1,\ldots,4$ at shifts $r-d$. Thus deficit two is the actual first center at reduced 3.

Keep the four fixed L identity arrows at $[0,3]$. The $t$ extra ordinary neutral pairs at $[4,3+t]$ each use two distinct actual neutral terminals, one L and one H, giving the L bank of width $t$. An ordinary pair of shift $\delta$ at shared position $i$ uses $L_i\to L_{i+\delta}$ and $H_{i+\delta}\to H_i$. Reserve shift one and use its ordinary pairs. Beginning at shift two, use $\lfloor g/2\rfloor$ four-odd-host packets and, for $e=1$, one three-host packet on consecutive shift groups. This uses exactly $2g+e$ roles. These [D182 packets](ORDINARY_SPINE_EXCEPTIONAL_PARITY_NEUTRAL_PACKETS.md#3-two-independently-expandable-parity-neutral-packets) depend only on their adjacent shifts and the actual local quotas. At shared positions $j,j+1$, with $a=j+\eta_0$ for least shift $\eta_0$, the three-host relative lists $(2,0)$ and $(1,1)$ have identical reservations $\{a+1,a+2\}$ and quota totals $(1,2,1)$. The four-host lists $(3,0)$ and $(1,2)$ have identical reservations $\{a+1,a+3\}$ and quotas $(1,1,1,1)$. Their expansions add ordinary pairs at the prescribed shifts with separated footprints, preserving those equal reservation sets in the two intermediate rows. Each group has equal L-source and H-image position counts and fits between its first position plus least shift and last position plus greatest shift. Its residual common intermediate columns use Q. No local rule uses the parity of $r$ or $\nu$.

The reserved role and packets fit because $r-5\ge1+2g+e$. The remaining eligible ordinary roles occupy $\mathcal D=[2+2g+e,r-5]$, of size $N_{\rm ord}=r-6-2g-e$. At equality this interval is empty and all positive regular positions come from the reserved host and packets. This includes $r=6$ with $g=0$ and the mixed $r=9,g=e=1$ boundary. Every unused regular role has an even quota and may use its ordinary pairs. Their cumulative joint allocation is included in §4. For unredistributed allocation the positive regular position count is $r-5+h_R$ in each row. The increasing shared positions occupy $[4+t,r-2+h_*]$, where $h_*=t+h_R$. Increasing disjoint shift groups and increasing position intervals keep their intermediate footprints disjoint. Every regular intermediate index lies at least at four and at most at $2r-7+h_*$, including the neutral pairs since $3+t\le2r-7+h_*$ by $h_R\ge-g$. The common upper bound and the following tail separation apply without changing when $r$ is even.

## 3. Unified tail

At $z=0$ put $H_T=\sum v_d=h_T$, $N_T=H_T+2$ and $D_*=2r+h_*$. Here $d$ in a tail quota subscript is a deficit. The remaining L-source and H-image positions are $r+h_*+x$ with local offsets
$$
[-1,N_T+\ell+\eta],\qquad [-1,N_T-1-\ell],
$$
respectively. They start after the regular endpoint $r-2+h_*$, and their right endpoints are the actual row endpoints $r+2+h+\ell+\eta$ and $r+1+h-\ell$. The regular H-image positions fit because $h_T\ge\ell$. At $x$ with deficit $d_0$ the reserved intermediate column relative to $D_*$ is $x-d_0$, from the shift $r-d_0$. The terminal portions of the H-source and L-image rows relative to $D_*$ are
$$
[-5,N_T+1-\ell],\qquad [-5,N_T+2+\ell+\eta],
$$
with the exact actual row endpoints $2r+3+h-\ell$ and $2r+4+h+\ell+\eta$. Their common start $D_*-5\ge2r+t-g-5\ge4$ lies above the preceding maximum $D_*-7$. In particular every indicated tail reservation is in the tail footprint, and all earlier regular intermediate columns fit both rows.

Use the [D183 local order](ORDINARY_SPINE_EXCEPTIONAL_UNBOUNDED_MULTI_UPPER_HOST.md#4-wider-tail-and-baseline-quotas) on the arithmetic even parts $2+2v_d$ of the actual quotas. At positions starting at $-1$ take $1+v_4$ ordinary pairs at deficit four, then $v_3-v_1$ ordinary pairs at deficit three, then $v_1+1$ groups $(1,3)$ in each row, then $v_2$ ordinary pairs at deficit two. One L-only use at deficit two follows. The initial identical lists have $3+H_T$ shared positions through $N_T-1$, and the L-only use is at $N_T$. The initial ordinary pairs give strictly increasing common columns $x-d_0$. Each $(1,3)$ group on consecutive positions $x,x+1$ gives the two columns $x-1,x-2$, exactly its position block minus two. The subsequent deficit-two pairs also give their positions minus two, so these groups and pairs have disjoint footprints and lie strictly above the initial ordinary columns. The groups exhaust the quota at deficit one and give the same number of uses at three, with the remainder of three and all of four supplied by the initial pairs. At deficit two the arithmetic counts include $2v_2$ shared uses, the L-only use and the actual selected exterior terminal.

Now transfer the last $\ell$ H-image uses at $[N_T-\ell,N_T-1]$ to additional L-source positions $[N_T+1,N_T+\ell]$ at their same parent. They all use deficit two by $v_2\ge\ell$. The shared H reservations that remain form a set $Y$ of distinct columns at most $N_T-\ell-3$, because the terminal part reserves its positions minus two and the earlier deficit-three and deficit-four columns are smaller. The L list retains its former reservations, including the columns $[N_T-\ell-2,N_T-3]$ from the transferred pairs and the L-only column $N_T-2$. The added L positions reserve $[N_T-1,N_T+\ell-2]$. When $\eta=1$ assign one further actual named terminal at deficit two to position $N_T+\ell+1$, giving column $N_T+\ell-1$. This uses the actual additional odd quota unit. Taken together the resulting L-image reservations are exactly
$$
Y\sqcup[N_T-\ell-2,N_T+\ell-2+\eta].
$$
The terminal interval is disjoint from $Y$. Both position windows are exhausted, all columns lie in their specified intermediate windows, and the actual leaf counts at each first parent are exact. These rules act as quota arithmetic on the actual target throughout.

Below $N_T-\ell-2$ the residual H-source and L-image columns are identical and use Q. The remaining suffixes in these rows are
$$
[N_T-\ell-2,N_T-\ell+1],\qquad
[N_T+\ell-1+\eta,N_T+\ell+2+\eta].
$$
Each contains four cells and their exact translation is $2\ell+1+\eta=\nu-1$. The corresponding H-to-L arrows use the actual $P_{\nu-1}$. All tail reservations and completions therefore give exact local bijections, with the common free columns between the regular groups and tail using Q. The four initial neutral L identities occupy $[0,3]$ below the first H-source index. No shifted terminal is required at the former even-tail separation by this odd-tail rule.

For the signed moment, neutral and regular groups contribute zero in total before cumulative imbalance: their lower L-source and H-image positions coincide in each group, as do their L-image and H-source reservation sets, and their Q uses have zero increment. The shared arithmetic tail initially has cancelling + and − shifts, and the final L-only use contributes $r-2$. Each transferred use changes the signed first contribution from $-(r-2)$ to $+(r-2)$. The extra L at $\eta=1$ adds another $r-2$. Thus the tail first moment is $(r-2)(1+2\ell+\eta)=(r-2)(\nu-1)$, with upper contribution $4(\nu-1)$ from its four shifts. The full moment is $(r+2)(\nu-1)=A(B-4)$ as required. The increment at fixed $r,\ell,h$ in passing from $\eta=0$ to 1 is exactly $(r-2)+4=A$, agreeing with the one-unit increase in $B$. This calculation is separate from the interval proof of the bijections.

## 4. Exact baselines, indexed selection and growth

At $z=0$ all L sources and H images belong to first hosts, so $x=0$ and $y=r-2+h-\ell$, the size of the H-image row. The H-source row has $2r+h-\ell$ cells, leaving $r+2$ upper arrows. Exactly four are at $P_{\nu-1}$ and the rest are Q identities. With the selected exterior terminal at $P_2$, the unredistributed counts are
$$
q_0=r-2,\qquad q_2=1,\qquad q_{\nu-1}=4,\qquad q_\rho=0\ \text{at other shifted roles}.
$$
The total is $R_0=r+3$. An even $r$ gives even Q here and odd $R_0$. Both fit the graph counts in §1.

Apply the [D186 monotone model](ORDINARY_SPINE_EXCEPTIONAL_CUMULATIVE_IMBALANCE_ALLOCATION.md#2-monotone-first-allocation-and-exact-unused-cells) within the unchanged eligible ordinary footprint $\mathcal D$. If its size $N=N_{\rm ord}$ is zero, there are no eligible shared positions. If $N=1$, both the L and H groups use the host's half quota in the same positions, giving no gaps. For $N\ge2$ order the shifts $\delta_j=\delta_1+j-1$, write their actual quotas as $2k_j$ and $S_j=\sum_{i\le j}k_i$, $S=S_N$. On shared positions $[x_0,x_0+S-1]$, choose integers $u_0=u_N=0$, $|u_j-u_{j-1}|\le k_j$. Use L-source and H-image group lengths $k_j+u_j-u_{j-1}$ and $k_j-u_j+u_{j-1}$. These are nonnegative and sum to the actual quota per host and to $S$ per position row. For sign $\varepsilon=+1$ in the L-image reservation row or $-1$ in the H-source reservation row, put $a_*=x_0+\delta_1$ and $P_j^\varepsilon=S_j+\varepsilon u_j$. Group $j$ reserves
$$
[a_*+P_{j-1}^\varepsilon+j-1,\ a_*+P_j^\varepsilon+j-2].
$$
Together with the singleton separators $c_j+\varepsilon u_j$ at $c_j=a_*+S_j+j-1$ for $j<N$, these are a contiguous ordered partition of $[a_*,a_*+S+N-2]$, also for any empty groups. This is exactly the original eligible footprint in both rows and does not meet the new tail. To match these distinct gap sets, choose a permutation $\sigma$ of $[1,N-1]$ for which each $c_{\sigma(j)}-c_j+u_j+u_{\sigma(j)}$ lies in $\{0,2,\ldots,\nu\}$. The actual upper maps make each such arrow legal, and all local matchings of these cells by the retained upper hosts are of this form. In particular the possible extra shifted host is just one additional allowed separation. The fixed outside allocation and the complete local partition preserve the four exact row bijections.

Write $m_\rho$ for the positive separation histogram and $M=\sum_{\rho=2}^\nu m_\rho$. The new baseline counts are
$$
q_0=r-2-M,\qquad q_2=1+m_2,\qquad q_{\nu-1}=4+m_{\nu-1},\qquad q_\rho=m_\rho\ \text{at other shifted roles}.
$$
They sum to $r+3$. Since $M\le\max(0,N-1)$, Q is positive, with $q_0\ge5+2g+e$ for $N\ge1$ and $q_0=r-2$ for $N=0$. These formulas do not single out parity for Q. The L-source and H-image counts at first hosts stay unchanged, so $x=0$ and $y=r-2+h-\ell$ remain the exact baseline counts, including when $\eta=1$. The first-moment change is $2\sum_j\delta_j(u_j-u_{j-1})=-2\sum_{j<N}u_j$. The matched gap indices contribute $+2\sum_{j<N}u_j$ by cancellation of the centers under permutation. Thus the signed total retains the value in §3. The empty choices recover the unredistributed counts.

Require every actual target upper quota to be positive and dominate its corresponding $q_\rho$ with the same parity. In particular there is an actual selected terminal at $P_2$, and $P_{\nu-1}$ supplies the widened tail. Set $b_\rho=(p_\rho-q_\rho)/2\ge0$ for shifted roles. The [D184 neutral-bank invariant](ORDINARY_SPINE_EXCEPTIONAL_NEUTRAL_ANCHOR_BANK_GROWTH.md#2-removing-and-restoring-an-entire-bank) holds: the four row bijections are exact, the initial L identities stay at $[0,3]$, the other endpoints are at least four, the actual neutral L bank on $[4,3+t]$ has its original names and all specified upper hosts are present. For any width increase the four row ends advance equally and $J$ advances twice as much by §1. Thus the D184 proofs of whole-bank restoration, overlap handling and pure and partial growth apply using the same folded host maps, independently of either center-count parity or initial role counts.

For $\rho\le t$ use the pure step at width $b_\rho$ with selected bank width $\rho$. For $\rho>t$ divide $b_\rho=tB_\rho+v_\rho'$ with $0\le v_\rho'<t$. Use the partial step of bank width $t$ and batch $B_\rho$, then include a partial step of bank width $v_\rho'$ and batch one if needed. Omit all zero operations. The exact increments at the shifted role and Q are $2b_\rho$ and
$$
C_\rho=
\begin{cases}
0& \rho\le t,\\
2(\rho\lceil b_\rho/t\rceil-b_\rho)&\rho>t.
\end{cases}
$$
Order the global list by nonincreasing chosen bank width, then by separation and step type. Each operation preserves its selected prefix, so every successor has its required width. For $p_0\ge q_0+\sum C_\rho$ and $p_0\equiv q_0\pmod2$, finish with a Q-only step of integral width $a=(p_0-q_0-\sum C_\rho)/2\ge0$. It translates all noninitial endpoints and fills both directions by Q on the common free interval. The counts become exactly the target quotas, and
$$
\lambda_{\rm final}=a+\sum_{\rho=2}^\nu(b_\rho+C_\rho/2),\qquad
R=r+3+2\lambda_{\rm final}.
$$
The second equality proves the required $R$ parity and, with $F$, the integral $K$ condition of §1. The bank moves and translations keep the first counts in their respective rows. Thus $x=\lambda_{\rm final}$, $y=r-2+h-\ell$ and $x+y=s-K$. The signed moments of the paired upper directions cancel, and restored neutral arrows keep zero index change. When $t\ge\nu$, all shifted growth is pure, so the Q condition is exactly domination and parity for this selected schedule.

A deterministic finite supplier lists eligible distinct actual first pairs for neutral and deficit two, indexed assignments of the remaining first hosts to their retained numerical roles and packets, and tail roles with a minimum quota at deficit one among the three even hosts. It lists the eligible imbalance vectors and permitted gap permutations, with the two empty-gap cases included. This is finite by $|u_j|\le\min(S_j,S-S_j)$ and finite permutation length. Finally list indexed assignments of all actual second roles. Choose the first passing candidate in fixed lexicographic order after applying the exact baseline domination, parity, Q-cost and full-size tests, then extract the stated bank schedule. All role and leaf selections retain distinct original names even when quota values coincide. This is an arithmetic specification, with no numerical search conducted. Taking $\eta=0$ and odd $r$ gives exactly the D186 geometry, role premises, tail and local choices, along with their bank and inventory rules. Thus every accepted D186 input is retained under the same admissions.

## 5. Matched symbolic controls

Use the retained independent 74-edge prefix with actual maximum cutoff 39. Its minimum orientation has $c=74+1-39=36$. The listed profiles below are actual ordered sections, with the last zero denoting the single original direct leaf. At each profile the first listed host is neutral and the second first host is deficit two. Assign actual second hosts to $Q,P_2,\ldots,P_\nu$ in their listed order.

| Control | First section | Second section | $(g,e,r,\nu,\eta)$ | $F$ | $R$ | $2K$ | $t$ | $N_{\rm ord}$ |
| --- | --- | --- | --- | ---: | ---: | ---: | ---: | ---: |
| A | $(12,4,2,2,2,2,2)$ | $(5,1,4,2,0)$ | $(0,0,7,4,0)$ | 26 | 12 | 52 | 4 | 1 |
| B | $(12,4,2,2,2,2)$ | $(4,1,4,2,0)$ | $(0,0,6,4,0)$ | 24 | 11 | 48 | 4 | 0 |
| C | $(14,5,2,2,2,2,2)$ | $(5,1,2,4,2,0)$ | $(0,0,7,5,1)$ | 29 | 14 | 58 | 5 | 1 |
| D | $(14,5,2,2,2,2)$ | $(4,1,2,4,2,0)$ | $(0,0,6,5,1)$ | 27 | 13 | 54 | 5 | 0 |
| Mixed boundary | $(14,5,1,1,2,2,2,2,2)$ | $(7,1,2,4,2,0)$ | $(1,1,9,5,1)$ | 31 | 16 | 64 | 5 | 0 |

The sums in the table are the actual first and second terminal totals, and each fresh size includes the two spine vertices, centers and the actual direct leaf. All sizes are admitted by 74. In each case $\ell=1$, $v_2=1$ and $v_1=v_3=v_4=0$, so $H_T=1$ and $N_T=3$. The retained H reservations in the local tail are $\{-5,-2,-1\}$, from the deficit-four pair and the $(1,3)$ group. The shifted H deficit-two use leaves the H list. The L reservations add $[0,2+\eta]$, containing the L images of the original deficit-two pair, final L-only use, transferred use and the extra use when $\eta=1$. The two residual suffixes are $[0,3]$ and $[3+\eta,6+\eta]$, with shifts 3 or 4 at the actual $P_{\nu-1}$. The remaining common free columns $-4,-3$ use Q. The actual direct leaf has reduced label $A+7$ in A and B, and $A+8$ in C, D and the mixed boundary.

- A has baseline $(5,1,4,0)$. It recovers the accepted [D184 scope-separating control](ORDINARY_SPINE_EXCEPTIONAL_NEUTRAL_ANCHOR_BANK_GROWTH.md#5-direct-scope-separating-control) by a pure width-one increase at $P_4$ with bank four. Its two new arrows join folded indices 8 in L and 4 in H, using the two prescribed directions. No Q increment is needed.
- B has baseline $(4,1,4,0)$ of total nine and uses the same pure $P_4$ step. At $r=6$ the sole positive regular shift is the reserved role one. There are exactly six even first hosts, and the entire eligible ordinary interval is empty. Both r and Q are even.
- C has baseline $(5,1,0,4,0)$ of total ten. Its actual quota-five first center supplies the odd deficit-two tail, including the extra L use. Use pure width-one steps at $P_5$ and then $P_3$, with bank widths five and three. The respective free L indices are 9 and 7 and both free H indices are 4 at their own stages. Only those shifted roles grow.
- D has baseline $(4,1,0,4,0)$ of total nine and uses the same two pure steps. There are five even first hosts for neutral, three even tail roles and shift one, and one odd host for deficit two. This is the minimum $r$ with odd $\nu$ and $g=0$, and its eligible ordinary interval is empty.
- The mixed boundary has baseline $(7,1,0,4,0)$ of total twelve and uses the same two pure steps. The distinguished odd tail host uses its actual quota five. The two odd regular quotas one enter the three-host packet at shifts 2 and 4 with an actual even quota two at shift 3. The positive regular positions start at 9, with the reserved ordinary pair at 9 and the packet at 10 and 11, using equal intermediate reservations at 13 and 14 and its ordinary common Q completion. Here $h_R=-1$ and $h_*=4$, so the last regular position is $r-2+h_*=11$ and the largest intermediate column in the packet footprint is 15, below the tail start $2r+h_*-5=17$. This verifies the exact signed regular and odd-tail interaction at the empty ordinary interval.

For A, B, C, D and the mixed boundary the completed maximum-polarity $(m,\text{cut})$ are respectively $(126,65),(122,63),(132,68),(128,66),(138,71)$. Their crossing intervals are respectively $[63,126],[61,122],[66,132],[64,128],[69,138]$ and the noncrossing bands begin at 1 and end one below those lower crossing endpoints. These follow from $m=74+2K$, actual cut $39+K$ and the exact spectra in §6. For a composition with both center-count parities changing, independently append A first, then append D on its named 126-edge return. D requires only 54 input edges, so that extension is admitted. Its actual maximum-polarity cut is $65+27=92$, its frontier label is 180, and its crossing and noncrossing bands are $[90,180]$ and $[1,89]$. The proof of composition below verifies immutable realization of this and all individually admitted sequences. All controls use symbolic arithmetic and the retained input data.

## 6. Named realization, both inventories and the exact return

Reserve the actual selected terminals at first parent 3 and $P_2$ as above. Name first arrows at their prescribed original hosts in row and position order. At the deficit-two host the arithmetic even-part allocation and any extra L arrow use distinct actual terminal names after the selected exterior terminal. At baseline name the upper gap arrows using the initial available actual indices at each host and at each growth step give inserted arrows the next available names at their designated parent. The stage counts in §4 ensure enough indices. All old or restored arrows keep their names and actual parents, and the direct leaf and original witnessing spine remain as supplied. The auxiliary allocation acts on rows of the actual target and introduces no additional physical center, terminal or incidence.

The baseline unfolding uses $J_0=3r+6+2h+\eta$. For a first parent of shift $\delta_j$, call its baseline numeric source set $S_j^{\rm b}$. It is obtained by using actual L-source positions and converting each H-source index $i$ to $J_0-i$. In particular a monotone host with L-source positions $\mathcal L_j$ and H-image positions $\mathcal H_j$ uses
$$
S_j^{\rm b}=\mathcal L_j\sqcup\{J_0-i-\delta_j:i\in\mathcal H_j\}.
$$
In the unified tail the analogous source sets use the exact lists in §3 at positions $r+h_*+x$, including the extra L position $r+h_*+N_T+\ell+1$ at the actual deficit-two parent when $\eta=1$. For any other first host the set is obtained from its exact retained lists. The baseline image set at each parent is $S_j^{\rm b}+\delta_j$ by §1. These first source sets are pairwise disjoint, and so are the image sets, by the complete baseline bijections. In particular the changed H numeric coordinates of the odd case and extra L cell enter the baseline resources.

Let $T_j,\lambda_j$ denote the bank width and width increase of shifted operation $j$. The original extra neutral identity at $i\in[4,3+t]$ has final source and image
$$
\phi(i)=i+\lambda_{\rm final}-\sum_{j:\ i<4+T_j}\lambda_j .
$$
Indeed the nonincreasing widths keep that very named arrow at $i$ until it first lies outside a selected prefix. It then shifts to the right and can never qualify at a later weakly smaller width. Every selected set is removed before restoring it, preserving names even when translated and restored intervals overlap. The final Q-only step contributes its width to $\lambda_{\rm final}$ and restores no bank. The first four identities stay fixed. Other noninitial endpoints gain the full folded shift, and in H they unfold to $(J_0+2\lambda_{\rm final})-(j+\lambda_{\rm final})=J_0-j+\lambda_{\rm final}$. This also gives the same numeric increase as a full L translation while using the actual $J_0$ for the target parity.

Define $\Phi(i)=i$ on $[0,3]$, $\Phi(i)=\phi(i)$ on $[4,3+t]$, and $\Phi(i)=i+\lambda_{\rm final}$ elsewhere in the baseline numeric alphabets. In both alphabets the two exceptional intervals already belong to their respective named neutral L arrows. The first-section gap coordinate sets and remaining complements are exactly
$$
I=\bigsqcup_j\Phi(S_j^{\rm b}),\qquad
J_1=\bigsqcup_j\Phi(S_j^{\rm b}+\delta_j),\qquad
I'=[0,s-1]\setminus I,\quad J_2=[0,s-1]\setminus J_1 .
$$
The unions are disjoint by the final bijections. Whole translated endpoints move equally, and selectively restored arrows are identities. Thus at each first host the final numeric image still differs from its source by that host's $\delta_j$. These are the exact named first and remaining resources.

For minimum polarity shift old labels by $A$ below $c$ and by $A+s$ at or above $c$. The endpoint inequalities $A+c-1<C\le A+c+s$ preserve old cut sides. Therefore the old crossing differences gain $s$ and the noncrossing differences are fixed. Use $A+c+i$ at each gap source $i$ and add $n+s$ to each upper reduced exterior label. The common frontier agrees at label $A$. All exterior edges cross since their lower endpoints have labels at most $A<C$ and the upper ones at least $n+s+A+1>C$. Their differences gain exactly $n+s$. The palettes are
$$
\begin{array}{ll}
L_{\rm old}=[A,A+c-1]\sqcup[A+c+s,n+s+A],&
L_{\rm fresh}=[0,A-1]\sqcup[A+c,A+c+s-1]\sqcup[n+s+A+1,m],\\
D_{\rm old}=[1,d-2]\sqcup[d-1+s,n+s],&
D_{\rm fresh}=[d-1,d+s-2]\sqcup[n+s+1,m].
\end{array}
$$
At final size these partition $[0,m]$ and $[1,m]$ since $m=n+s+A+B$. The shared $v$ is counted once. Exact source and image bijections and the actual exterior spectra fill each of the fresh values exactly once. Numeric absolute differences are given by the actual endpoint subtractions, with gap crossing and noncrossing bands $[d+K-1,d+s-2]$ and $[d-1,d+K-2]$. The full crossing and noncrossing spectra are $[d+K-1,m]$ and $[1,d+K-2]$. The actual frontier $w=0$, $m=2C+2$ and extended witnessing spine give exactly $S_{-1}$.

At the boundary after the first section let the first and remaining fresh exterior labels be
$$
E_1=[2,A-1]\sqcup\{n+s+A+1,n+s+A+3\},\qquad
E_2=\{0,1,n+s+A+2\}\sqcup[n+s+A+4,m],
$$
with differences $D^e_1=n+s+[1,A]$ and $D^e_2=n+s+[A+1,A+B]$. In $E_2$ the upper interval includes all actual shifted hosts and the direct leaf at its final endpoint, using the current $B$. The intermediate inventories are
$$
\begin{array}{ll}
\text{used labels}&L_{\rm old}\sqcup E_1\sqcup(A+c+I),\\
\text{remaining labels}&E_2\sqcup(A+c+I'),\\
\text{used differences}&D_{\rm old}\sqcup D^e_1\sqcup(d-1+J_1),\\
\text{remaining differences}&D^e_2\sqcup(d-1+J_2).
\end{array}
$$
The old and exterior label partitions use their respective old bands and reduced sides. The gap label partitions intersect $I,I'$ with $[0,k-1]$ or $[k,s-1]$ before shifting by $A+c$. The gap difference partitions intersect $J_1,J_2$ with $[0,K-1]$ or $[K,s-1]$ before shifting by $d-1$. Used crossing differences also include $[d-1+s,n+s]$ and $D^e_1$, remaining crossing differences include $D^e_2$, and used noncrossing differences include $[1,d-2]$. These inventories retain the literal unfinished edge $uw$ with endpoints $(n+s+A+1,0)$ and crossing difference $n+s+A+1$ in $D^e_2$.

In actual maximum polarity use input $n-G$ and complement output about $m$. Both actual cuts are $n+1-c$ and $m+1-C$, respectively. By $2K=A+B+s$, old lower and upper shifts become $B$ and $B+s$. Both label inventories complement and their sides switch, with all weights and crossings invariant. The actual frontier is $m$ at $w$, and the literal connector endpoints become $(m-(n+s+A+1),m)=(B-1,m)$.

In a finite sequence, each admitted actual block has its own original roles, $\eta,r$ and size, and uses its actual incoming named graph, frontier, cut and spectrum. Every block returns the same phase with an extreme frontier and preserves the evolving cut sides of old values. So a change of $\eta$ or first-center parity does not alter the next interface. At any completed cut $C_i$, let $U_i,V_i$ be the sums of the later actual lower shifts and gap widths. The exact final map on that completed alphabet is $x\mapsto x+U_i+V_i\mathbf1_{x\ge C_i}$. Crossing weights gain $V_i$ and noncrossing ones stay fixed. This lifts the recorded inventories and literal connector endpoints and weight as well. At each insertion the fresh palettes are disjoint from those transported values, so the remaining sets of earlier boundaries in the final alphabet also include all later original fresh values. Induction proves exact admitted composition. The finite role lists, bounded imbalance sequences, gap permutations and growth steps, followed by finite backward sums, terminate and give immutable final emission on the original named graph. Independent initialization and arbitrary decomposition retain their separate scopes.

## 7. Scope, method and acceptance

The extra-cell tail opens all four parity combinations of the center counts within the proved supplier. The necessary graph-class parity conditions and the sufficient quota tests retain their stated scopes. General H1 feasibility, arbitrary lobster coverage, and $\nu\le3$ are outside the new theorem. The explicit extra-cell mechanism resolves the bounded inquiry symbolically with no scientific search, solver allocation, original checker, campaign or historical replay.

D186 is Director accepted within its written scope at checkpoint e2b862cdc8540ff19ece52658b7731ebdbc427a5. Its local gap criterion, prior construction domain, and 74→142→230 symbolic composition retain their accepted status. All five D187 controls are symbolic coverage. D185, D184 and all earlier accepted scopes are retained. The D174 historical one pair and two numerical arms with 3,518 unentered originals stay separate from D177's accepted 93-original projection with 92 historically unentered. Exact custody, prior bindings and both independent reviews are recorded separately.
