# D185 — Baseline quota redistribution on the wider exceptional exterior

Task **LCL-ORDINARY-SPINE-EXCEPTIONAL-BASELINE-QUOTA-REDISTRIBUTION-001**.

**PROVED WITHIN EXACT WRITTEN SCOPE / PENDING DIRECTOR REVIEW.** Retain the D183 wider exterior, the independently supplied, full-size admitted named D157 $S_{-1}$ input, and the D184 actual first and second quota hypotheses. Select any matching of adjacent eligible ordinary first roles. A tile on a matched pair of even hosts $\delta,\delta+1$ with $2k_{\rm tile}\le\min(\alpha_\delta,\alpha_{\delta+1},\nu)$ transfers one baseline unit from Q to $P_{2k_{\rm tile}}$. If the number $m_\rho$ of tiles at each separation $\rho$ is even, the modified baseline preserves all retained target parities. With $M=\sum m_\rho$, its Q count is $r-2-M$ and its shifted counts are the accepted D183 counts plus the respective $m_\rho$. The D184 bank operations supply the exact dominating target quotas under the sufficient Q bound in §4. With bank width $t\ge\nu$, only the reduced odd baseline floor $r-2-M$ is needed at Q. This is a sufficient domain on the specified construction.

## 1. Original topology, fixed exterior and fold

All quantities and labels are exact integers, excluding booleans. Intervals are inclusive and an inverted interval is empty. Let $\nu=2+2\ell\ge4$, $g\ge0$, $e=g\bmod2$ and odd $r\ge2g+6+e$. The actual first section has $r$ centers, exactly $2g$ with positive odd quotas and the rest with positive even quotas. Choose distinct even first hosts of quota at least six for neutral and at least $\nu$ for deficit two. There is no first direct leaf. The second section has the $\nu$ actual centers and the sole actual second direct leaf, which is exterior. Use selectable numerical roles without changing the actual indices or incidences. The actual second target quotas $p_0,p_2$ are positive odd, $p_{\nu-1}$ is even at least four, and other shifted quotas are positive even. The first terminal total $F$ and second terminal total $R$ are even. With the two actual new spine vertices $u,w$, the fresh count is $2K=F+r+\nu+R+3$. Full size requires $n\ge2K$ and $m=n+2K$.

Take the independently supplied [D157 prefix](ORDINARY_SPINE_ALTERNATING_EXCEPTIONAL_SPECTRUM.md#1-interface-and-exact-inventory-rule) with $n=2c+2$ edges, actual extreme frontier $v$ oriented by $G(v)=0$ and its witnessing spine. At cut $c$, with equality upper and $d=c+2$, the crossing and noncrossing spectra are $[d-1,n]$ and $[1,d-2]$ respectively. Keep D183's independently supplied exterior at $A=r+2$, $B=\nu+3$. In reduced labels use $v=A,u=A+1,w=0$, all first centers at $[2,A-1]$, Q at $A+2$, $P_\rho$ at $A+2+\rho$ for $2\le\rho\le\nu$, and the direct leaf at $A+B$. The first indexed terminal at first parent 3 gets $A+3$, and the first indexed terminal at $P_2$ gets 1. These are the exact reduced labels $[0,A+B]$. The connected crossing exterior uses actual edges at those parents and on the spine. Its first differences are 1 for $vu$, $[2,A-1]$ for first-center edges, and $A$ for the selected first terminal. Its remaining differences are $A+1$ at $uw$, $A+2$ at $wQ$, $A+3$ at the selected terminal of $P_2$, $[A+4,A+\nu+2]$ at the shifted centers, and $A+B$ at the direct leaf. Thus the reduced spectra and relative placement of the two exterior inventories are exact. Every actual center remains present even if its auxiliary baseline count is zero.

Use $R_0=r+3$ and let $z$ denote cumulative growth, with total $R_0+2z$. Write $h=F/2-r-1$, $t=(\alpha_{\rm neutral}-4)/2\ge1$. Substituting gives $K=2r+5+h+\ell+z$, $s=2K-A-B=3r+3+2h+2z$, $k=K-A$ and $J=s+3$. The neutral contribution is $h_N=t$, the signed regular contribution $h_R=(\sum_{\rm regular}\alpha-2(r-5))/2$ is at least $-g$, and the four-tail contribution $h_T=\sum_{\rm tail}(\alpha-2)/2$ is at least $\ell$. The exact host partition gives $h=h_N+h_R+h_T$. Thus $K-(A+B)=r-2+h-\ell+z>0$ by $r\ge2g+6+e$. This supplies $s\ge K$ and $A\le K\le A+s$. At final placement the size premise is for the full actual $2K$, and every auxiliary allocation has at most that width.

A gap leaf at numeric coordinate $i$ has oriented label $A+c+i$ and is lower at $C=c+K$ iff $i<k$. From actual endpoint subtraction its difference is $d-1+\pi(i)$, with $\pi(i)=i+\delta$ at a lower host of reduced label $j_0$ where $\delta=A-1-j_0$, and $\pi(i)=s+b+1-i$ at the expanded upper host of label $n+s+A+b$. The lower host label is smaller than the gap label and the upper host larger, giving the stated signs. Put $L_j=j$ and $H_j=J-j$. The exact folded rows are
$$
\begin{array}{c|cc}
 &L&H\\
\text{sources}&[0,r+2+h+\ell+z]&[4,2r+3+h-\ell+z]\\
\text{images}&[0,2r+4+h+\ell+z]&[4,r+1+h-\ell+z].
\end{array}
$$
The H rows unfold to $[k,s-1]$ for sources and $[K,s-1]$ for images. The L rows give their respective complements in $[0,s-1]$. A lower host keeps rows, with $+\delta,-\delta$ on L and H. An upper host $P_\rho$ swaps rows with $-\rho,+\rho$ on L and H, while Q swaps at identical indices. Therefore an H image is exactly the case of a source and its actual parent on opposite physical sides. The crossing predicate is $\pi(i)\ge K$. The folded moment is $A(B-4)$: the L images add $A$ indices beginning at $k$ relative to the L sources, while the H images remove $A$ indices beginning at $k+4-B$ relative to the H sources. This also follows from the [D183 exact moment](ORDINARY_SPINE_EXCEPTIONAL_UNBOUNDED_MULTI_UPPER_HOST.md#2-wider-named-exterior-folded-alphabets-and-moment).

## 2. Eligible ordinary roles and one local redistribution tile

Use the accepted [D183 regular ordering](ORDINARY_SPINE_EXCEPTIONAL_UNBOUNDED_MULTI_UPPER_HOST.md#3-signed-regular-strip-and-the-reusable-anchor) at $z=0$. The numerical first shifts are $[0,r-1]$, the positive regular shifts $[1,r-5]$, and the remaining four positive shifts the tail. There are at least $6+e$ even hosts for neutral, four tail roles, shift one and the possible even middle of the three-host parity packet. Reserve shift one. The next $2g+e$ positive regular roles are exactly the parity-packet roles starting at shift two. The D182 packet footprints and ordinary grouping by increasing shift thus leave exactly
$$
\mathcal D=[2+2g+e,r-5]
$$
as the eligible ordinary even roles. These roles are all positive and have even quotas at least two. If $r-6-2g-e=0$, the interval is empty and the empty selection below suffices. The actual even hosts may be assigned to these numerical roles in any chosen order, since the D183 ordinary-pair argument uses the sum of their pair lengths and increasing numerical shifts. All tail and parity-packet hypotheses are retained.

An ordinary pair of shift $\delta$ at shared position $i$ uses $L_i\to L_{i+\delta}$ and $H_{i+\delta}\to H_i$ at the same actual parent. It reserves the common intermediate column $i+\delta$ in the L-image and H-source alphabets. For adjacent eligible shifts $\delta,\delta+1$, select $k_{\rm tile}=\kappa$ pairs at each host with
$$
1\le\kappa,\qquad 2\kappa\le\min(\nu,\alpha_\delta,\alpha_{\delta+1}).
$$
Take the last $\kappa$ pairs at shift $\delta$ and the first $\kappa$ pairs at shift $\delta+1$. All unselected pairs at the first host precede them and those at the second follow. Their contiguous shared positions are $U=[x,x+2\kappa-1]$. Set $a_*=x+\delta$. In the ordinary allocation both intermediate reservation sets on the block are
$$
[a_*,a_*+\kappa-1]\sqcup[a_*+\kappa+1,a_*+2\kappa].
$$
The only common free column of the enclosing interval is $a_*+\kappa$, which uses H-to-L Q identity. All cells in that interval are in the two actual intermediate rows, by the verified D183 regular footprint bound.

Instead, use the $2\kappa$ selected actual terminals at shift $\delta$ for $L_i\to L_{i+\delta}$ for every $i\in U$. Use the other $2\kappa$ selected actual terminals at shift $\delta+1$ for $H_{i+\delta+1}\to H_i$ on the same $U$. All selected terminals retain their actual parents. The shared L-source and H-image sets are unchanged and covered once each. The new L images are $[a_*,a_*+2\kappa-1]$, and the new H sources are $[a_*+1,a_*+2\kappa]$. Exactly the H source $a_*$ and L image $a_*+2\kappa$ remain. Since $2\le2\kappa\le\nu$, the actual shifted host $P_{2\kappa}$ is available. Its H-to-L map
$$
H_{a_*}\longrightarrow L_{a_*+2\kappa}
$$
completes both intermediate rows in the same footprint. The tile contains only the indicated legal arrows at the actual parents. Its L lower uses are noncrossing and its H lower uses crossing. The last upper use is noncrossing, like the prior Q identity. The transfer changes the prescribed second counts by $\Delta p_0=-1$, $\Delta p_{2\kappa}=1$ and $\Delta R=0$. It changes neither first quotas nor exterior incidences. In the ordinary block the signed first moment was zero since each pair contributed $+\delta$ and $-\delta$ at its own host. The tile's signed first moment is $2\kappa\delta-2\kappa(\delta+1)=-2\kappa$, offset by $+2\kappa$ from the new upper arrow. This agrees with the exact global moment at the same width.

The nearest unselected ordinary reservation before the block is at most $a_*-1$. The nearest following reservation is at least $a_*+2\kappa+1$. Both follow from strict ordering of positions and their shifts. In general each tile is contained in the interval from first position plus least shift to last position plus greatest shift. Distinct selected pairs in a matching have disjoint shift ranges, and strict increase in positions and shifts makes their footprints disjoint even when their role pairs are consecutive. Other regular footprints, the neutral bank and the widened tail are unchanged and separated. Thus one can form the chosen final baseline directly by using these tile rules at the selected blocks and ordinary rules elsewhere. The ordinary Q arrow used in the comparison is a slot in a conceptual allocation. No actual Q terminal is needed to remove it.

## 3. The simultaneous redistributed baseline

At $z=0$ retain the four fixed neutral L arrows and each extra neutral pair, with separate L and H terminals at positions $[4,3+t]$. The D182 regular parity packets remain unchanged, with their equal intermediate reservations and Q completions. The shared positions still run in increasing order from $4+t$ through $r-2+h_*$ for $h_*=t+h_R$. All regular intermediate footprints remain at or below $2r-7+h_*$ and at least four. The unchanged tail starts in the intermediate rows at $2r-5+h_*$, which is at least four, with its two position windows and intermediate windows intact. In particular its actual deficit-two parent has quota at least $\nu$. Thus the [D183 separated tail](ORDINARY_SPINE_EXCEPTIONAL_UNBOUNDED_MULTI_UPPER_HOST.md#4-wider-tail-and-baseline-quotas) has enough pairs to transfer the last $\ell$ H-image uses to L and leaves the four H-to-L shifts at $P_{\nu-1}$ in their exact endpoints. All other common free tail columns use Q identities.

The baseline consists of the fixed L cells $[0,3]$, the neutral pairs, parity packets and ordinary pairs with the selected disjoint tile substitutions, the unchanged tail, and the Q identities on remaining common intermediate columns. This partitions both source and both image alphabets. Indeed each substitution partitions exactly the same L-source positions, H-image positions and intermediate footprint as the previous ordinary block together with its Q identity. By §2 no untouched intermediate footprint overlaps such a substitution. All first arrows keep their respective lower host shifts and are counted once per actual terminal. The gap crossing counts therefore remain $x=0$ and $y=r-2+h-\ell$: all L sources use first hosts and all H images, numbering $r-2+h-\ell$, come from H sources at first hosts. There are $2r+h-\ell$ H sources, so exactly $r+2$ uses remain at upper hosts. This gives the same total as D183 by actual row decomposition.

Write $m_\rho$ for the number of chosen tiles of separation $\rho$, with $m_\rho=0$ for odd $\rho$, and $M=\sum_{\rho=2}^{\nu} m_\rho$. At the retained role parities every $m_\rho$ must be even for this construction with subsequent even growth, so $M$ is even. The baseline counts, including the one selected exterior terminal at $P_2$, are
$$
q_0^{(0)}=r-2-M,\quad q_2^{(0)}=1+m_2,\quad q_{\nu-1}^{(0)}=4,\quad
q_\rho^{(0)}=m_\rho\qquad(\rho\in[3,\nu]\setminus\{\nu-1\}).
$$
The last expression is zero at any other odd separation. These counts sum to $R_0=r+3$. Positivity at Q follows since $M\le\lfloor|\mathcal D|/2\rfloor\le(r-6)/2$, so $r-2-M\ge(r+2)/2>0$. With odd $r$ and even $M$ this count is odd. The changes in signed moments cancel separately at every tile, including simultaneously selected consecutive pairs, and the unchanged upper tail still has its original contribution. In particular the unchanged folded alphabet moment is supported by the explicit assignments, independently of parity and quota checks. When the selection is empty the same row partition and counts recover the accepted baseline of D184.

Use the unmodified exterior when assigning roles. For first-terminal identities, at each selected host designate the $2\kappa$ names that would have been used by its selected ordinary pairs, then distribute precisely those names on its new row list in increasing position order. Only first names need be designated in advance. The redistributed upper counts then specify which actual target terminal indices to assign at Q and every shifted host. This uses the target's own incidences and enough indices at every parent by the following domination tests. Nothing is removed from the original topology.

## 4. Growth, Q bound and arithmetic selection

Require the target numerical role assignment to dominate the redistributed baseline at each shifted role. Since $m_\rho$ is even, the desired growth counts
$$
b'_\rho=(p_\rho-q_\rho^{(0)})/2
$$
are nonnegative integers. D184 applies directly: the four row bijections hold as just proved, the four initial L identities are fixed, all other endpoints are at least four, the actual neutral bank has its original $t$ named L identities, and all physical shifted hosts and Q remain available. Each operation grows all right endpoints by its width increment. With $t=(\alpha_{\rm neutral}-4)/2\ge1$ use the [D184 pure and partial growth](ORDINARY_SPINE_EXCEPTIONAL_NEUTRAL_ANCHOR_BANK_GROWTH.md#3-pure-and-partial-growth) from this independent baseline. For $\rho\le t$ it increases the quota by $2b'_\rho$ at zero Q cost. For $\rho>t$, writing $b'_\rho=tq+v$ with $0\le v<t$, use a partial operation of width $t$ and batch $q$ if $q>0$ and one of width $v$ and batch one if $v>0$. These supply exactly $2b'_\rho$ with Q cost
$$
C'_\rho=
\begin{cases}
0 & \rho\le t,\\
2\big(\rho\lceil b'_\rho/t\rceil-b'_\rho\big) & \rho>t .
\end{cases}
$$
The empty increment costs zero. The operations are ordered by nonincreasing selected bank width, then increasing separation and listed operation order for ties. The [whole-bank restoration](ORDINARY_SPINE_EXCEPTIONAL_NEUTRAL_ANCHOR_BANK_GROWTH.md#2-removing-and-restoring-an-entire-bank) of each step preserves at least its own width, so every successor is permitted. It translates or restores only named arrows at their own parents. It continues to hold when the first owners of some baseline L and H positions have changed through a tile, since all hypotheses concern the actual updated row partition and bank.

Under
$$
p_0\ \ge\ r-2-M+\sum_\rho C'_\rho ,
$$
the final Q-only width $a=(p_0-(r-2-M)-\sum_\rho C'_\rho)/2$ is a nonnegative integer since $p_0,r-2-M$ are odd and all costs even. Apply the Q-only strip of width $a$ after all shifted operations. It preserves the four initial identities and fills both free rows in each direction at Q while increasing only its count by $2a$. This reaches all actual target quotas, never exceeding them at an earlier step. The final folded width change and total are
$$
\lambda_{\rm final}=a+\sum_\rho (b'_\rho+C'_\rho/2),\qquad R=r+3+2\lambda_{\rm final}.
$$
A width increase of $\lambda$ adds $\lambda$ L sources at upper hosts as all first arrows keep their row counts. The number of H sources at first hosts remains the same, giving $x=\lambda_{\rm final}$ and $y=r-2+h-\ell$, in agreement with $s-K$. When $t\ge\nu$ all shifted operations are pure, and the sufficient Q condition is just $p_0\ge r-2-M$ with odd parity. Every shifted quota can then grow independently by any even increment above its redistributed baseline.

For fixed numerical roles, a compatible tile selection can never raise the total sufficient Q bound above the no-tile choice. Let $b_\rho=(p_\rho-p_\rho^{(0)})/2$ refer to the original baseline. If $\rho\le t$ the contribution to the bound changes by $-m_\rho$. If $\rho>t$, the change after combining the Q baseline reduction $-m_\rho$ and the cost difference is
$$
2\rho\big(\lceil(b_\rho-m_\rho/2)/t\rceil-\lceil b_\rho/t\rceil\big)\le0 .
$$
This allows equality for some partial-bank increments and quantifies exactly the strict reduction when the whole bank is available. It compares sufficient bounds at a dominating target on the same roles.

For a deterministic terminating selection, work entirely on the finite indexed quota data. List the ordered pairs of eligible distinct even first hosts for neutral and deficit two. List assignments of the remaining first hosts to the retained category roles, using the D183 tail minimum and required odd and even packet roles. Within each choice order by the original indices, and keep the numerical role ordering for the allocation. List the finite matchings on the adjacency path of $\mathcal D$, and for each list all its integral tile sizes in the specified capacity intervals. Include the empty matching. Reject any matching with odd $m_\rho$. List assignments of the actual second centers satisfying the exact role parities and minima. At each candidate check domination of the redistributed baseline, the Q bound and full size. Take the lexicographically first passing indexed choice, or report that this supplier's arithmetic domain has not been met. Equal-valued centers remain distinct in each list. All ranges are finite, and every candidate described by this construction appears in them. The empty selection includes every D184-covered input under the same premises, including its original role assignment and corresponding bank size. This is an arithmetic specification of the supplier, with no search over actual labelings carried out in this investigation.

## 5. Controls and infinite-family baseline reduction

For the first profile $(12,4,2,2,2,2,2,2,2,2,2)$ and second profile $(7,3,4,2,0)$, the last entry denotes the actual direct leaf. The parameters are $g=0$, $r=11$, $\nu=4$, $\ell=1$, $F=12+4+9\cdot2=34$, $R=16$, and $2K=34+11+4+16+3=68$. The retained independent prefix has $n=74\ge68$. The neutral quota 12 gives $t=4$ and the separate quota four supports deficit two. Under D184 the odd Q floor is $r-2=9$. Only 7 and 3 are odd second quotas, so neither can meet that sufficient floor. This is a failure of the sufficient-test domain for every numerical order.

Under D185 put the actual quotas $7,3,4,2$ at Q, $P_2,P_3,P_4$. The regular shifts are $[1,6]$. Reserve shift one and choose the disjoint pairs $(2,3),(4,5)$ with $\kappa=1$. Both hosts of each pair have quota two. Here $h_N=4,h_R=0,h_T=1$, so the positive regular positions start at 8. The chosen blocks have positions $[9,10]$ and $[11,12]$, and footprints $[11,13]$ and $[15,17]$. Each uses one $P_2$ arrow, so $m_2=M=2$ and the redistributed baseline is $(7,3,4,0)$ with total $R_0=14$. A pure $P_4$ operation at bank width four and width increment one completes the target. In each L alphabet the translated bank $[5,8]$ is fully removed before restoration at $[4,7]$. The remaining L and H indices are 8 and 4, respectively. The two arrows $L_8\to H_4$ and $H_4\to L_8$ contribute the two required $P_4$ uses, with Q unchanged at seven. The matched positive control with the same first inventory and $(9,1,4,2,0)$ instead uses zero tiles. It meets the original Q floor nine and grows $P_4$ with the same pure step. Both checks are symbolic arithmetic with the retained independent prefix.

Selections such as $(2,3),(3,4)$ share a role and are excluded by the matching requirement. Using $\kappa=2$ with these quota-two hosts would require four actual terminals at each, so that local choice is unavailable even at $\nu=4$. Selecting just one $\kappa=1$ tile makes $m_2$ odd and flips the baseline parities at Q and $P_2$, which cannot be changed by even bank growth. Requiring only total $M$ even would still allow a parity mismatch at an individual shifted role. These restrictions govern this supplier. Other allocations retain their separate feasibility questions.

In the all-even first domain $g=e=0$, the eligible path $[2,r-5]$ has $r-6$ vertices. Its maximum matching size is $L=\lfloor(r-6)/2\rfloor$: each pair consumes two roles and the consecutive disjoint pairs $(2,3),(4,5),\ldots$ attain that bound. Every even $M$ between 0 and $L$ can be chosen by taking the first $M$ pairs at $\kappa=1$. All such even hosts support this tile. The baseline shifted quota at $P_2$ is then $1+M$. If $t\ge\nu$, any odd $p_2\ge1+M$, even $p_{\nu-1}\ge4$, other positive even shifted quotas, and odd $p_0\ge r-2-M$ are supplied. Retain odd $r\ge6$ in this domain, even $\nu\ge4$, the actual qualifying neutral host of quota at least $4+2\nu$ and distinct deficit-two host of quota at least $\nu$, the original topology and exterior, and the independent full-size admission $n\ge2K$. This is an infinite-family reduction of the sufficient Q floor. The same pair-count argument works in the mixed domain with $|\mathcal D|=r-6-2g-e$ in place of $r-6$. No checker-verified original certificate is claimed for either control.

## 6. Exact named first resources, unfolding and return

Let $S_\delta^{\rm b}$ be the numeric source set at actual first role $\delta$ in the **redistributed** baseline, with $J_0=3r+6+2h$. It is obtained by using the signed regular, neutral, and tail assignments of §3 with the following exact replacements. In a tile of §2 remove the selected ordinary sources at $\delta$ from shared positions $i\in[x,x+\kappa-1]$, namely $i$ and $J_0-i-\delta$. Remove the selected ordinary sources at $\delta+1$ from positions $i\in[x+\kappa,x+2\kappa-1]$, namely $i$ and $J_0-i-(\delta+1)$. Insert the full set $U=[x,x+2\kappa-1]$ at $\delta$ and $\{J_0-i-(\delta+1):i\in U\}$ at $\delta+1$. These sources carry exactly the first-terminal names specified in §3. The image set at every first role is $S_\delta^{\rm b}+\delta$ by actual endpoint subtraction, including in H. In particular the intermediate L images and H uses of a tile are precisely those in §2. Unselected arrows retain their original coordinates and incidences at baseline. The sets of sources at distinct hosts are disjoint, and so are the respective image sets, by the four row partitions. This derives the first inventories using the new assignments.

Write $T_j,\lambda_j$ for the selected bank width and width increment of each nonidentity shifted operation. Its prefix is selected in the actual neutral L bank at the positions in D184. For a named baseline extra neutral L identity at $i\in[4,3+t]$, its exact final index is
$$
\phi(i)= i+\lambda_{\rm final}-\sum_{j:\,i<4+T_j}\lambda_j .
$$
In fact when $i<4+T_j$, that inequality held at every earlier step by the width order, so this named arrow was restored to $i$ at every prior step and is the arrow restored in the current step. Otherwise its current index is at least $i\ge4+T_j$, and it stays outside this and all later selected prefixes. Removing the entire translated selection prevents overlaps from changing names. The last Q-only increment is included in $\lambda_{\rm final}$ and restores no bank. The four initial neutral identities are fixed at $[0,3]$. Every other noninitial baseline arrow, including the neutral H arrows, gains the full folded shift $\lambda_{\rm final}$. In H the unfolded numeric change is also $+\lambda_{\rm final}$ because
$$
(J_0+2\lambda_{\rm final})-(j+\lambda_{\rm final})=(J_0-j)+\lambda_{\rm final}.
$$
A fully translated L endpoint likewise gains $\lambda_{\rm final}$.

For either baseline alphabet define $\Phi(i)=i$ on $[0,3]$, $\Phi(i)=\phi(i)$ on $[4,3+t]$, and $\Phi(i)=i+\lambda_{\rm final}$ elsewhere. In each alphabet the cells of the first two cases are already used by the corresponding neutral L identities, so these cases refer to their actual named arrows. No other baseline endpoints share those cells. The final exact first gap sets and their complements are
$$
I=\bigsqcup_\delta\Phi(S_\delta^{\rm b}),\qquad
J_1=\bigsqcup_\delta\Phi(S_\delta^{\rm b}+\delta),\qquad
I'=[0,s-1]\setminus I,\qquad J_2=[0,s-1]\setminus J_1.
$$
Each union is disjoint by the exact baseline and growth bijections. The arrows stay at their original actual parents and the only selectively restored arrows are neutral identities. Thus the final numeric image still differs from its first-host source by that host's $\delta$. Every other gap position belongs to the second section, and those names are assigned at their actual upper hosts by the final baseline and subsequent stage quotas. First names and newly inserted second names can be ordered by their actual terminal indices. This provides a deterministic construction with no temporary Q vertex.

Use minimum polarity first. Translate old labels by $A$ below $c$ and $A+s$ at or above $c$, preserving old cut sides by $A+c-1<C\le A+c+s$. The old crossing weights gain $s$ and the old noncrossing weights are fixed. Give each gap source $i$ label $A+c+i$ and expand the upper reduced exterior band by $n+s$, with the lower reduced labels unchanged. The shared $v$ stays at $A$. Exterior incidences cross since their lower and upper labels lie at most at $A<C$ and at least at $n+s+A+1>C$, respectively. Their differences gain exactly $n+s$. Consequently the exact palettes are
$$
\begin{array}{ll}
L_{\rm old}=[A,A+c-1]\sqcup[A+c+s,n+s+A],&
L_{\rm fresh}=[0,A-1]\sqcup[A+c,A+c+s-1]\sqcup[n+s+A+1,m],\\
D_{\rm old}=[1,d-2]\sqcup[d-1+s,n+s],&
D_{\rm fresh}=[d-1,d+s-2]\sqcup[n+s+1,m].
\end{array}
$$
These exhaust $[0,m]$ and $[1,m]$ by $2K=A+B+s$. The shared frontier is counted once in the old palette. The exact exterior spectra and the complete final folded and unfolded bijections fill all indicated bands on actual vertices and actual edge differences. The gap crossing and noncrossing bands are $[d+K-1,d+s-2]$ and $[d-1,d+K-2]$. Together the full crossing and noncrossing spectra are $[d+K-1,m]$ and $[1,d+K-2]$. The endpoint $w=0$, the original witnessing spine through $u,w$ and $m=2C+2$ give the exact $S_{-1}$ return.

At the intermediate boundary after the first section the fresh exterior labels are
$$
E_1=[2,A-1]\sqcup\{n+s+A+1,n+s+A+3\},\qquad
E_2=\{0,1,n+s+A+2\}\sqcup[n+s+A+4,m],
$$
for the first and remaining sections. The exterior weight bands are $D^e_1=n+s+[1,A]$ and $D^e_2=n+s+[A+1,A+B]$. Hence the exact intermediate inventories are
$$
\begin{array}{ll}
\text{used labels}&L_{\rm old}\sqcup E_1\sqcup(A+c+I),\\
\text{remaining labels}&E_2\sqcup(A+c+I'),\\
\text{used differences}&D_{\rm old}\sqcup D^e_1\sqcup(d-1+J_1),\\
\text{remaining differences}&D^e_2\sqcup(d-1+J_2).
\end{array}
$$
Their cut partitions use the two old label bands and the exterior reduced sides. The gap label parts use intersections of $I,I'$ with $[0,k-1]$ and $[k,s-1]$ before shifting by $A+c$. The gap noncrossing and crossing parts use intersections of $J_1,J_2$ with $[0,K-1]$ and $[K,s-1]$ before shifting by $d-1$. The used crossing part also includes $[d-1+s,n+s]$ and $D^e_1$, the remaining crossing part includes $D^e_2$, and the used noncrossing part includes $[1,d-2]$. These exact sets retain the literal unfinished connector $uw$ with endpoint labels $(n+s+A+1,0)$ and crossing difference $n+s+A+1$ in $D^e_2$.

For maximum polarity the input is $n-G$ and the output is complemented about $m$, with cuts $n+1-c$ and $m+1-C$. The actual lower and upper shifts are $B,B+s$ instead of $A,A+s$ by $2K=A+B+s$. Both inventories of labels complement, swapping their cut sides. Actual differences and crossing statuses are fixed under complementation. The final frontier is $m$ at $w$ and the literal connector labels are $(m-(n+s+A+1),m)=(B-1,m)$.

For finite composition on individually admitted blocks, keep each actual incoming named graph, cut, frontier, phase and spectra. At each witnessed extension use its own size and topology premises. The maps preserve the cut sides of the old alphabet as its cut evolves. If $C_i$ is a completed cut and $U_i,V_i$ sum subsequent actual lower shifts and gap widths, then an actual label $x$ there reaches $x+U_i+V_i\mathbf1_{x\ge C_i}$ in the final alphabet. Crossing differences gain $V_i$, noncrossing ones stay fixed, and both exact intermediate inventories and literal connectors lift accordingly. Later fresh labels and weights are disjoint at every insertion and belong to the remaining inventories of earlier boundaries in the final alphabet. Induction gives the exact admitted returns. Finite arithmetic role and tile selection, finite allocation and growth lists, and finite backward sums produce each final original label for immutable emission. The independent initialization and decomposition hypotheses retain their previous scopes.

## 7. Accepted scope and method

The first-host tile gives baseline redistribution with unchanged topology and exterior. The nonincreasing-bank growth then establishes the stated sufficient domain on that independently supplied allocation. This resolves the authorized objective with symbolic reasoning and retained arithmetic controls. General multi-host feasibility remains open. D183's necessary topology threshold and D184's partial-bank divisibility obstruction retain their stated scopes.

D184 is Director accepted within its exact written scope at checkpoint b71bd603cacab15d40a4738a3e665fca216f4b6b. Its full- and partial-bank results and Q-bound scopes remain intact. D183 and earlier accepted findings and unresolved cases are preserved. D174 historically completed one pair and two numerical arms with 3,518 unentered originals, separate from D177's accepted 93-original symbolic projection with 92 historically unentered. The custody and review records report the exact frozen identities and zero search, solver, campaign and replay counters.
