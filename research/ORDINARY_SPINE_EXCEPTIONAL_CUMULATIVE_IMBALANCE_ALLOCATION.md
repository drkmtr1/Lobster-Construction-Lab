# D186 — Cumulative-imbalance allocation on the wider exceptional exterior

Task **LCL-ORDINARY-SPINE-EXCEPTIONAL-CUMULATIVE-IMBALANCE-ALLOCATION-001**.

**PROVED WITHIN EXACT WRITTEN SCOPE / PENDING DIRECTOR REVIEW.** Retain D183's wider exterior, D182's parity-neutral packets, D183's widened tail and D184's neutral bank, under the named topology and size hypotheses in §1. On the eligible ordinary interval the two monotone role lists give exact gap columns $c_j+u_j$ and $c_j-u_j$. A permutation with the allowed separations characterizes the local completions and their exact upper quota vectors in this model. With $M$ positive-separation matches the manufactured baseline uses $r-2-M$ at Q. It can be grown to dominating, baseline-parity target quotas under the sufficient Q bound in §4. This retains the complete D185 domain and includes all-even second quotas and the odd-separation control. In the all-even first domain, a full neutral bank and the corresponding quota at $P_2$ permit a constant sufficient Q floor of five. The local criterion and the growth hypotheses have the scopes stated below.

## 1. Named topology, exterior and exact fold

All parameters and labels are exact integers, excluding booleans. Intervals are inclusive and an inverted interval is empty. Let $\nu=2+2\ell\ge4$, $g\ge0$, $e=g\bmod 2$ and odd $r\ge2g+6+e$. There are $r$ actual first centers, with exactly $2g$ positive odd quotas and otherwise positive even quotas, and $\nu$ actual second centers with positive target quotas. Use distinct even first hosts of quota at least six for neutral and at least $\nu$ for deficit two. There is no first direct leaf. The sole second direct leaf is exterior. Numerical roles may be selected among actual original indexed centers, preserving all incidences. The input is the independently supplied named [D157 $S_{-1}$ prefix](ORDINARY_SPINE_ALTERNATING_EXCEPTIONAL_SPECTRUM.md#1-interface-and-exact-inventory-rule). It has $n=2c+2$ edges, actual extreme frontier $v$, a witnessing spine and oriented labeling $G(v)=0$. The cut $c$ puts equality on the upper side. With $d=c+2$ its crossing and noncrossing weights are $[d-1,n]$ and $[1,d-2]$ respectively. Let $u,w$ be the actual new spine vertices, $F$ the first terminal total and $R$ the target second terminal total. Directly counting two spine vertices, $r+\nu$ actual centers, one direct leaf and all $F+R$ terminals gives $2K=F+r+\nu+R+3$. The final admitted size satisfies $n\ge2K$, and $m=n+2K$.

For the [D183 wider exterior](ORDINARY_SPINE_EXCEPTIONAL_UNBOUNDED_MULTI_UPPER_HOST.md#2-wider-named-exterior-folded-alphabets-and-moment), take $A=r+2$, $B=\nu+3$, reduced labels $v=A,u=A+1,w=0$, first centers at $[2,A-1]$, Q at $A+2$, $P_\rho$ at $A+2+\rho$ for $2\le\rho\le\nu$ and the actual direct leaf at $A+B$. The first indexed terminal at first parent 3 receives $A+3$, and the first indexed terminal at $P_2$ receives 1. This fills $[0,A+B]$ and gives a connected crossing exterior through the actual spine and parent edges. Its first differences are 1 on $vu$, $[2,A-1]$ on the first-center edges, and $A$ on the selected first terminal. The remaining differences are $A+1$ at $uw$, $A+2$ at $wQ$, $A+3$ at the selected $P_2$ terminal, $[A+4,A+\nu+2]$ at the shifted centers and $A+B$ at the direct edge. Every actual center is exterior even when it has zero assigned leaves at an auxiliary stage. This argument needs one actual terminal at $P_2$ and one at first parent 3. It places no individual second parity requirement on the reduced exterior.

Put $R_0=r+3$, with total $R_0+2z$ at cumulative width $z$. The construction below confirms that every final admitted $R$ is of this form. Write $h=F/2-r-1$, $t=(\alpha_{\rm neutral}-4)/2\ge1$, and use the neutral, regular and tail quota contributions $t,h_R,h_T$ of D183. The regular promotion $h_R=(\sum_{\rm regular}\alpha_i-2(r-5))/2$ is integral with $h_R\ge-g$. The tail promotion $h_T=\sum_{\rm tail}(\alpha_i-2)/2$ is at least $\ell$ by the qualifying deficit-two host. Thus $h=t+h_R+h_T\ge t+\ell-g$. The exact geometry has
$$
K=2r+5+h+\ell+z,\quad s=2K-A-B=3r+3+2h+2z,\quad k=K-A,\quad J=s+3 .
$$
The inequality $K-(A+B)=r-2+h-\ell+z>0$ follows from the stated lower bounds, giving $s\ge K$ and $A\le K\le A+s$. The full target size admits every width used in the allocation.

At numeric gap coordinate $i$ the actual oriented label is $A+c+i$, lower at $C=c+K$ iff $i<k$. Subtraction from a lower reduced parent $j_0$ gives actual weight $d-1+\pi(i)$ with $\pi(i)=i+\delta$, $\delta=A-1-j_0$. Subtraction of the leaf label from its expanded upper parent of label $n+s+A+b$ gives $\pi(i)=s+b+1-i$. The upper and lower host bands give the indicated absolute signs. Fold $L_j=j$ and $H_j=J-j$. The exact rows are
$$
\begin{array}{c|cc}
 &L&H\\
\text{sources}&[0,r+2+h+\ell+z]&[4,2r+3+h-\ell+z]\\
\text{images}&[0,2r+4+h+\ell+z]&[4,r+1+h-\ell+z].
\end{array}
$$
The H-source and H-image rows unfold to $[k,s-1]$ and $[K,s-1]$. The L rows give their respective numerical complements. A first host keeps rows, shifting by $+\delta,-\delta$ on L and H. An upper host $P_\rho$ swaps rows with shifts $-\rho,+\rho$ on L and H, while Q swaps at identical indices. An H image is exactly the case where source and actual parent are on opposite sides, and the physical crossing predicate is $\pi(i)\ge K$. Every increment of $z$ by $\lambda$ increases the upper endpoints of all four rows by $\lambda$, with $J$ increasing by $2\lambda$. These formulas use the total $R$ only.

## 2. Monotone first allocation and exact unused cells

At $z=0$ retain the first four L identities and the $t$ extra neutral pairs of [D184 §1](ORDINARY_SPINE_EXCEPTIONAL_NEUTRAL_ANCHOR_BANK_GROWTH.md#1-baseline-and-exact-fold), with the L bank at $[4,3+t]$ and distinct H arrows. Retain the reserved shift-one host and [D182 parity-neutral packets](ORDINARY_SPINE_EXCEPTIONAL_PARITY_NEUTRAL_PACKETS.md#3-two-independently-expandable-parity-neutral-packets) in their D183 order, starting the packet roles at shift two and using $2g+e$ roles there. There are at least $6+e$ even hosts for the neutral, four tail roles, shift one and the possible even packet middle. The eligible interval of remaining ordinary roles is $\mathcal D=[2+2g+e,r-5]$, of size $N=r-6-2g-e\ge0$. The positive regular shared positions run in order from $4+t$ through $r-2+h_*$, where $h_*=t+h_R$. All intermediate regular footprints lie at or below $2r-7+h_*$, below the retained tail's first intermediate column $2r-5+h_*\ge4$. The [D183 widened tail](ORDINARY_SPINE_EXCEPTIONAL_UNBOUNDED_MULTI_UPPER_HOST.md#4-wider-tail-and-baseline-quotas) keeps its local position and intermediate windows, the transferred $\ell$ deficit-two uses and four H-to-L arrows at $P_{\nu-1}$. The tail hypotheses depend on the unchanged quotas and endpoints, including the actual first deficit-two quota of at least $\nu$.

If $N=0$, there are no eligible positions and no local matches to change. If $N=1$, both boundary imbalances are zero, so the one even host uses equal L and H group lengths $k_1=\alpha_1/2$. The $k_1$ ordinary pairs cover identical contiguous intermediate columns in the two rows, leaving no gaps there. In both cases the baseline is the unchanged D183 one.

Now let $N\ge2$ and index these eligible actual hosts by $j=1,\ldots,N$ in increasing numerical shifts $\delta_j=\delta_1+j-1$. The full first quota at $j$ is $\alpha_j=2k_j$, $k_j\ge1$. Let $S=\sum_j k_j$ and $S_j=\sum_{i=1}^j k_i$, with $S_0=0$. The retained ordinary allocation gives the consecutive shared positions $[x,x+S-1]$ after the preceding neutral and regular groups. Hold this interval fixed in each of the L-source and H-image rows. For any integers $u_0,\ldots,u_N$ with $u_0=u_N=0$ and $|u_j-u_{j-1}|\le k_j$, use lengths
$$
\ell_j=k_j+u_j-u_{j-1},\qquad h_j=k_j-u_j+u_{j-1}
$$
at actual host $j$. They are nonnegative integers, sum there to $2k_j$, and telescope to total $S$ separately in each row. Use consecutive positions of the given row in increasing host order. At each L-source position $i$ use $L_i\to L_{i+\delta_j}$ and at each H-image position $i$ use $H_{i+\delta_j}\to H_i$. The two whole position alphabets are exhausted.

For either intermediate row put $a=x+\delta_1$ and use a sign $\varepsilon$ equal to $+1$ for L images or $-1$ for H sources. Its cumulative length at host $j$ is $P_j^\varepsilon=S_j+\varepsilon u_j$. The intermediate columns reserved by its $j$-th group are exactly
$$
[a+P_{j-1}^\varepsilon+j-1,\ a+P_j^\varepsilon+j-2] .
$$
This formula remains an empty interval when the group length is zero. For $j<N$ the separator after that group is the single column
$$
a+P_j^\varepsilon+j-1=c_j+\varepsilon u_j,\qquad c_j=a+S_j+j-1 .
$$
In particular, in each row the groups and their interposed singleton separators form one contiguous ordered partition of $[a,a+S+N-2]$: the first group starts at $a$, each singleton follows its group's right endpoint, the next group starts one after that singleton, and the final right endpoint is $a+S+N-2$. Reading an empty group simply places consecutive separators without consuming an intermediate column. This includes leading, trailing and repeated empty groups. Distinct gaps also follow directly since consecutive singleton coordinates differ by $1$ plus the next nonnegative group length. Thus these ordered partitions characterize the exact complements. The enclosing interval equals the original ordinary footprint in both intermediate rows, including its original boundary singleton gaps. The original increasing-position and increasing-shift bounds place every column of this interval in both intermediate rows and strictly beyond preceding footprints. It is below the separated tail start. No neutral arrow, earlier packet or tail use is displaced.

## 3. Local matching criterion, baseline and D185 specialization

Every local H-source gap $c_j-u_j$ must go to one local L-image gap by the retained upper maps. For fixed imbalances the two gap sets have distinct columns in their own alphabets. Matching all sources therefore selects a permutation $\sigma$ of $[1,N-1]$. Its difference is exactly
$$
\rho_j=(c_{\sigma(j)}+u_{\sigma(j)})-(c_j-u_j)
      =c_{\sigma(j)}-c_j+u_j+u_{\sigma(j)} .
$$
It is legal precisely when every difference belongs to $\{0,2,3,\ldots,\nu\}$. Zero uses the actual Q host and nonzero $\rho_j$ uses the actual $P_{\rho_j}$ host. The row maps then give all the indicated actual arrows, covering the exact two free sets and each source and image once. Conversely every completion of these local unused cells by the retained upper hosts, with the outside arrows fixed, specifies such a permutation and uses a host exactly as determined by the difference. In particular separation one is unavailable. This is an exact criterion for this local model. It permits no crossing of an assignment into or out of the fixed footprint.

Before the replacement, there was a Q identity at every zero-imbalance gap $c_j$ and no shifted assignment in the eligible interval. The new matching uses Q at the zero differences and each shifted role at its respective multiplicity $m_\rho$. Let $M=\sum_{\rho=2}^\nu m_\rho$. The unchanged remainder contains the four tail shifts at $P_{\nu-1}$ and the selected exterior terminal at $P_2$. Thus the exact baseline, including that terminal, is
$$
q_0=r-2-M,\quad q_2=1+m_2,\quad q_{\nu-1}=4+m_{\nu-1},\quad
q_\rho=m_\rho\quad(\rho\in[3,\nu]\setminus\{\nu-1\}).
$$
Use $M=0$ and zero multiplicities when $N=0$ or 1. In all cases $M\le\max(0,N-1)$, so $q_0\ge5+2g+e$ for $N\ge1$, and $q_0=r-2>0$ for $N=0$. The counts sum to $R_0=r+3$. These are auxiliary counts for a named target whose actual upper quotas will dominate them, with all actual centers present and no fabricated second leaf.

The complete baseline partitions both source and image alphabets into the unchanged neutral, packet and tail assignments with their residual Q identities, and the exact monotone groups and upper matching on the eligible footprint. The folded position sets are unchanged, and every L source and H image goes to the required lower first roles. Thus $x=0$ and $y=r-2+h-\ell$: the latter is exactly the full H-image row size for lower-host crossing uses. All remaining H sources go to upper hosts at the exact differences of their H-to-L arrows. The total upper gap use is $(2r+h-\ell)-(r-2+h-\ell)=r+2$. This gives the counts independently of any moment or parity shortcut.

The signed folded first-moment change relative to all ordinary pairs is
$$
\sum_{j=1}^N\delta_j(\ell_j-h_j)
=2\sum_{j=1}^N\delta_j(u_j-u_{j-1})
=-2\sum_{j=1}^{N-1}u_j ,
$$
where $\delta_{j+1}-\delta_j=1$. The added upper moment in that footprint is $\sum_j\rho_j=2\sum_j u_j$, since the column centers permute and the old identities contributed zero. The pair of changes cancels. The unchanged full folded moment is $A(B-4)$ by the two intervals of length $A$ added to L images starting at $k$ and removed from H images starting at $k+4-B$. In particular $\sum_\rho\rho m_\rho$ is even, despite the possible occurrence of odd individual separations. This is a consequence of the exact matching.

For a finite arithmetic characterization at fixed named first roles, enumerate signed integer sequences with the endpoint and step bounds. This is finite, since $|u_j|\le\min(S_j,S-S_j)$ by summing the step bounds from each endpoint. For a proposed histogram, the exact permutation test on its unused indices can be expressed as a recurrence. Process the H-source gaps in increasing $j$. At each step try each unused destination index whose difference is allowed and whose requested remaining histogram count is positive. Recur after removing that destination and decreasing that count. Accept the empty continuation exactly when all destinations and counts are exhausted. Induction gives the exact fixed-imbalance matching and extracts its permutation. The original candidate histogram is realized precisely when at least one of these finite imbalances passes. The fixed outside counts then give the displayed baseline vector. The arithmetic enumeration describes this model and was not run as an experiment.

For identity matching, $\rho_j=2u_j$. In the [D185 disjoint adjacent tile](ORDINARY_SPINE_EXCEPTIONAL_BASELINE_QUOTA_REDISTRIBUTION.md#2-eligible-ordinary-roles-and-one-local-redistribution-tile), set $u_j=k_{\rm tile}$ at each selected adjacent boundary and zero elsewhere. The selected boundaries do not neighbor one another, so the steps at a pair are $+k_{\rm tile},-k_{\rm tile}$ at its two hosts. They meet both half-quota bounds. The L length at host $j$ increases by $k_{\rm tile}$ and that of $j+1$ decreases by the same amount. The H lengths change oppositely. Compared to the original shared boundary, the L list extends the earlier host into the first $k_{\rm tile}$ positions of the later one. The H list extends the later host back over the last $k_{\rm tile}$ positions of the earlier one. Hence in the selected block every L position uses the earlier host and every H position the later host, with the before and after ordinary positions unchanged. The identity matching thereby makes exactly the D185 upper arrow on the shifted gap, and Q identities on all unselected boundaries. The selected original leaf names can be placed in precisely the D185 order at their own parents. This recovers every D185 disjoint selection, including the empty case and its parity-compatible growth domain.

## 4. Baseline-parity growth and finite selection on the actual target

Select any baseline as in §3 and actual second quotas $p_0,p_2,\ldots,p_\nu$ with each positive, $p_\rho\ge q_\rho$ and $p_\rho\equiv q_\rho\pmod2$. In particular the actual $P_2$ has its selected terminal and $P_{\nu-1}$ admits the four unchanged tail uses. Some other auxiliary counts can be zero before growth. The total $F$ is even by the first quota list. The manufactured baseline total $R_0=r+3$ is even and all subsequent increments are even, so the target $R$ is even. Odd $r$ and even $\nu$ now give integral $K$ in §1. All stage and final geometric checks in §1 depend on these totals and the actual host labels.

The [D184 bank invariant](ORDINARY_SPINE_EXCEPTIONAL_NEUTRAL_ANCHOR_BANK_GROWTH.md#2-removing-and-restoring-an-entire-bank) holds. There are exact four-row bijections, the four fixed initial L identities and unchanged named bank of width $t\ge1$, with every other folded endpoint at least four. All actual shifted hosts and Q are present. The local eligible footprint leaves this bank untouched. Thus whole-bank removal and restoration, with the exact pure and partial row partitions, apply for every positive width used below. These maps use actual folded separations and add leaves in pairs. Their local proofs do not assume any previous odd or even count at a specific second host.

Let $b'_\rho=(p_\rho-q_\rho)/2$ for $2\le\rho\le\nu$, a nonnegative integer. When $\rho\le t$, use the pure step of width $b'_\rho$ with bank width $\rho$. Otherwise divide $b'_\rho=tB_\rho+v_\rho$, $0\le v_\rho<t$. Use the partial step with bank width $t$ and batch $B_\rho$ and, if $v_\rho>0$, bank width $v_\rho$ and batch one. Zero steps are omitted. These supply the exact requested shifted increments at the [D184 costs](ORDINARY_SPINE_EXCEPTIONAL_NEUTRAL_ANCHOR_BANK_GROWTH.md#4-exact-target-schedule-and-q-requirements)
$$
C'_\rho=
\begin{cases}
0 & \rho\le t,\\
2\big(\rho\lceil b'_\rho/t\rceil-b'_\rho\big)& \rho>t .
\end{cases}
$$
Order all shifted steps by nonincreasing bank width, then by separation and step type for ties. Each step keeps its selected prefix of the bank, so the required bank remains available for its successor. These operations preserve all first quotas, all actual parent names and all exterior selections. Their upper increments are exact even counts regardless of the initial parities.

Under $p_0\ge q_0+\sum_\rho C'_\rho$ and $p_0\equiv q_0\pmod2$, apply the final Q-only strip of width $a=(p_0-q_0-\sum_\rho C'_\rho)/2\ge0$, integral by the even costs. It translates all noninitial folded endpoints and fills the common four-row strips by the two Q directions. This gives
$$
\lambda_{\rm final}=a+\sum_{\rho=2}^\nu(b'_\rho+C'_\rho/2),\qquad
R=r+3+2\lambda_{\rm final}.
$$
All stage quotas are at most their targets. When $t\ge\nu$ the costs vanish and the Q condition is simply domination and parity relative to $q_0$. The shifted growth is then independently parameterized by the allowed even increments over the selected baseline. Because first arrows keep their original rows throughout, $x=\lambda_{\rm final}$ and $y=r-2+h-\ell$. These equalities give $x+y=s-K$ and match the actual full row allocation.

A deterministic supplier uses the finite indexed choices of neutral and deficit-two pair, other tail roles obeying the retained minimum at deficit one, reserved role, packet roles and eligible ordered first roles. List the imbalance sequences and allowed gap permutations above, with the empty cases carried along explicitly. List all distinct indexed assignments of the actual second centers to Q and the shifted roles. Use fixed lexicographic orders on these finite lists, preserving equal-valued names. Apply the domination and parity tests, the sufficient Q-cost inequality and full size test. Use the first passing candidate, then the exact bank schedule above. This is a finite procedure within the defined sufficient model. It includes all D185-covered choices. Declining an input by these tests leaves other allocations and broader H1 feasibility undecided.

## 5. Constant floor and symbolic controls

If $N\ge1$, take any $0\le M\le N-1$ and set $u_j=1$ on the first $M$ internal boundaries and zero on the others, with both endpoint imbalances zero. The only nonzero steps are a possible $+1$ at the start and $-1$ immediately after the last chosen boundary, so every step respects $k_j\ge1$. Identity matching then changes exactly $M$ of the local Q identities to $P_2$ arrows with separation two. It supplies
$$
q_0=r-2-M,\quad q_2=1+M,\quad q_{\nu-1}=4,\quad q_\rho=0\text{ otherwise at shifted roles}.
$$
It retains $R_0=r+3$. For all-even first quotas, $N=r-6\ge1$, and $M=N-1=r-7$ gives $q_0=5,q_2=r-6$. When $t\ge\nu$, this is a sufficient constant Q floor of five, with Q and $P_2$ odd, $p_2\ge r-6$, even $p_{\nu-1}\ge4$, and positive even other shifted quotas. In the whole range, odd $M$ makes all baseline counts even, allowing every dominating all-even role assignment with the stated growth bound. Such an $M$ exists when $N\ge2$. In the mixed first domain $N=r-6-2g-e$ the same construction for $N\ge1$ reaches $q_0=5+2g+e$, $q_2=N$ at $M=N-1$, using the parities given by this baseline. When $N=0$ the unchanged baseline is the only one in the model. The target retains the independent input and full-size requirement throughout.

### A. Stronger reduction on the 74-edge prefix

For $(12,4,2,2,2,2,2,2,2,2,2)$ followed by $(5,5,4,2,0)$, the terminal totals are $F=12+4+9\cdot2=34$ and $R=16$. Here $g=e=0,r=11,\nu=4,\ell=1$, the original neutral quota 12 gives $t=4$, and the distinct quota four meets deficit two. There are $N=5$ eligible roles and $2K=34+11+4+16+3=68\le74$. Use $u_1=u_2=u_3=u_4=1$ and identity matching. The local L group lengths are $(2,1,1,1,0)$ and H lengths $(0,1,1,1,2)$, with their endpoints and gap partition as in §2. The resulting baseline is $(5,5,4,0)$ at $(Q,P_2,P_3,P_4)$, of total 14. One pure width-one step at $P_4$ with bank four fills the free L index 8 and H index 4 in both directions, giving the two new leaves at $P_4$ with Q unchanged. Under D185 the path of five eligible roles has at most two disjoint tiles, so the sufficient Q floor there is at least seven, above both actual odd quotas five. This distinguishes the sufficient domains.

### B. All-even second quotas on the same inventory

For the second profile $(6,4,4,2,0)$ use the same parameters and first inventory. Here $u=(0,1,1,1,0,0)$, including endpoint zeros. Identity matching gives $M=3$ and the exact baseline $(6,4,4,0)$. The same pure $P_4$ step gives the all-even target. All geometry and spectra apply at the same size. D185's written positive domain requires odd Q and $P_2$, while this target has neither. Its accepted symbolic control $(7,3,4,2,0)$ at the same size remains covered by its two disjoint $P_2$ tiles and the pure $P_4$ step, or equivalently the special imbalance choice of §3.

### C. Odd-separation matching on the independently supplied extension

First supply the named 142-edge prefix via accepted [D185's symbolic control](ORDINARY_SPINE_EXCEPTIONAL_BASELINE_QUOTA_REDISTRIBUTION.md#5-controls-and-infinite-family-baseline-reduction), using its exact first profile above and second profile $(7,3,4,2,0)$. Its two disjoint tiles give $(7,3,4,0)$ followed by the one pure $P_4$ step. This uses the actual frozen 74-edge prefix and satisfies $74\ge68$. For its maximum actual polarity orientation, the input cut is 39, giving oriented $c=74+1-39=36$. The oriented completed cut is $36+34=70$, the maximum-polarity completed cut is $142+1-70=73$, the maximum frontier is 142, and the crossing and noncrossing spectra are $[71,142]$ and $[1,70]$. This supplies the original named first extension independently of the next block.

Now append the original profiles $(20,8,4,2,6,2,2,2,2)$ and $(5,1,1,2,2,2,5,2,0)$, including the actual direct leaf indicated by zero. This gives $g=e=0,r=9,\nu=8,\ell=3$ and neutral quota 20 with $t=8$. The separate deficit-two quota eight meets its bound. Here $F=20+8+4+2+6+4\cdot2=48$, $R=20$ and $2K=48+9+8+20+3=88\le142$. Assign actual quotas $(4,2,6)$ to the eligible shifts $(2,3,4)$, using one other even quota two at reserved shift one and the remaining three eligible tail quotas two alongside the quota eight. With $k=(2,1,3)$ and $u=(0,2,3,0)$ the L lengths are $(4,2,0)$ and H lengths $(0,0,6)$. The exact enclosing footprint is $[a,a+7]$ with $S=6,N=3$. Relative to $a$, the L groups reserve $[0,3]\sqcup[5,6]$ and the H group $[2,7]$, so the free L images are $\{4,7\}$ and H sources $\{0,1\}$. The row maps allow $H_a\to L_{a+7}$ at $P_7$ and $H_{a+1}\to L_{a+4}$ at $P_3$. Both are noncrossing upper uses in the exact folded rows and match the two free sets. Their sum of separations is $7+3=2(2+3)$, compensating the first moment.

With the four retained tail uses at $P_7$, the exact baseline $(Q,P_2,\ldots,P_8)$ is $(5,1,1,0,0,0,5,0)$, of total 12. Use pure width-one steps in descending separation order at $P_8,P_6,P_5,P_4$, adding two leaves at each. Nothing grows at Q. This reaches the actual target, with four odd quotas, and $\lambda_{\rm final}=4$. The independently supplied first extension at oriented cut 70 is admitted for the second, giving oriented cut 114 and actual maximum-polarity cut $230+1-114=117$. Its new crossing and noncrossing spectra are $[115,230]$ and $[1,114]$. The immutable maps of §6 apply successively to the named prefix, the first extension and final target. These controls use direct symbolic arithmetic with retained data. No newly checker-verified certificate is claimed.

## 6. Named resources, exact spectra and admitted composition

At the two exterior-selected parents reserve the specified original terminal name. At baseline assign each first gap group to its own actual parent's original names in row and position order. Other first arrows come from the retained neutral, parity-packet and tail rules. The upper groups use only the necessary initial target names at their actual roles, after reserving the exterior terminal at $P_2$. For each bank step give newly inserted arrows available target terminal indices at their prescribed parent in a fixed order. The domination and final counts of §4 allow all these assignments. Moved and translated arrows preserve names, as do all original branches, the literal direct leaf and the witnessing spine.

In the modified ordinary footprint, let $\mathcal L_j$ and $\mathcal H_j$ denote the actual baseline L-source and H-image position intervals of first host $j$, determined by the cumulative group lists. With $J_0=3r+6+2h$, the baseline numeric gap source set there is
$$
S_j^{\rm b}=\mathcal L_j\sqcup\{J_0-i-\delta_j:i\in\mathcal H_j\}.
$$
Its exact image set is $S_j^{\rm b}+\delta_j$ by the actual endpoint formulas. At the untouched first parents use the baseline sources obtained by unfolding their actual retained arrows. Thus all first-role baseline sets are explicitly derived from the chosen new allocation, including any empty individual groups. Their respective unions of sources and images are disjoint by §§2–3.

Write $T_j,\lambda_j$ for the bank width and width increment of each shifted operation. The extra baseline neutral L identity at original position $i\in[4,3+t]$ has final numeric source and image
$$
\phi(i)=i+\lambda_{\rm final}-\sum_{j:\,i<4+T_j}\lambda_j .
$$
When eligible for a restored prefix in step $j$, it was eligible in every earlier step by nonincreasing widths and is still the same named arrow at $i$. Otherwise its current position is at least $i\ge4+T_j$ and it remains outside the current and subsequent selected prefixes. Complete removal of each translated selection makes this tracking valid even with overlap. The final Q-only shift appears only in $\lambda_{\rm final}$. The four initial identities stay fixed, and every other noninitial endpoint gains the full folded shift. For H endpoints the exact numerical change is also $+\lambda_{\rm final}$ because $(J_0+2\lambda_{\rm final})-(j+\lambda_{\rm final})=J_0-j+\lambda_{\rm final}$.

Thus for either baseline alphabet let $\Phi(i)=i$ on $[0,3]$, $\Phi(i)=\phi(i)$ on $[4,3+t]$, and $\Phi(i)=i+\lambda_{\rm final}$ elsewhere. In each alphabet the exceptional cells refer only to their corresponding neutral L identities, which already occupy those numeric cells uniquely. The final first gap sets are
$$
I=\bigsqcup_j\Phi(S_j^{\rm b}),\qquad J_1=\bigsqcup_j\Phi(S_j^{\rm b}+\delta_j),
$$
now summing over all first roles. Both unions are disjoint by the exact final row bijections. Every first image still differs numerically by its own host shift, since either both endpoints translate equally or the arrow is a neutral identity. With $I'=[0,s-1]\setminus I$ and $J_2=[0,s-1]\setminus J_1$, the remaining gap resources are exact by the actual achieved assignments.

In minimum polarity the old labels shift by $A$ below $c$ and by $A+s$ at or above $c$. The old side endpoints satisfy $A+c-1<C\le A+c+s$, hence old crossing weights gain $s$ and noncrossing weights stay fixed. Use $A+c+i$ for gap source $i$, and add $n+s$ to upper reduced exterior labels. The common frontier $v$ agrees at $A$. Every exterior edge crosses because its lower end is at most $A<C$ and its upper end at least $n+s+A+1>C$. It gains difference $n+s$. The exact vertex and edge palettes are
$$
\begin{array}{ll}
L_{\rm old}=[A,A+c-1]\sqcup[A+c+s,n+s+A],&
L_{\rm fresh}=[0,A-1]\sqcup[A+c,A+c+s-1]\sqcup[n+s+A+1,m],\\
D_{\rm old}=[1,d-2]\sqcup[d-1+s,n+s],&
D_{\rm fresh}=[d-1,d+s-2]\sqcup[n+s+1,m].
\end{array}
$$
They exhaust $[0,m]$ and $[1,m]$ using $m=n+s+A+B$, with the shared $v$ counted once. The exact row bijections and reduced exterior spectra fill the fresh palettes on actual labels and differences, and old differences fill their own bands. The physical gap crossing and noncrossing bands are $[d+K-1,d+s-2]$ and $[d-1,d+K-2]$. Their unions with old and exterior bands yield the exact crossing and noncrossing weights $[d+K-1,m]$ and $[1,d+K-2]$. This returns $S_{-1}$ with $w=0$, $m=2C+2$ and the original extended witnessing spine.

At the boundary after the first section, the first and remaining fresh exterior sets are
$$
E_1=[2,A-1]\sqcup\{n+s+A+1,n+s+A+3\},\qquad
E_2=\{0,1,n+s+A+2\}\sqcup[n+s+A+4,m],
$$
with difference bands $D^e_1=n+s+[1,A]$ and $D^e_2=n+s+[A+1,A+B]$. The two full intermediate inventories are
$$
\begin{array}{ll}
\text{used labels}&L_{\rm old}\sqcup E_1\sqcup(A+c+I),\\
\text{remaining labels}&E_2\sqcup(A+c+I'),\\
\text{used differences}&D_{\rm old}\sqcup D^e_1\sqcup(d-1+J_1),\\
\text{remaining differences}&D^e_2\sqcup(d-1+J_2).
\end{array}
$$
Partition old labels into their two bands and exterior labels by their reduced sides. The gap label partitions use intersections of $I,I'$ with $[0,k-1]$ and $[k,s-1]$ before adding $A+c$. The gap difference partitions use intersections of $J_1,J_2$ with $[0,K-1]$ and $[K,s-1]$ before adding $d-1$. Used crossing differences also include $[d-1+s,n+s]$ and $D^e_1$, remaining crossing ones include $D^e_2$, and used noncrossing ones include $[1,d-2]$. This keeps the literal unfinished original edge $uw$ with labels $(n+s+A+1,0)$ and difference $n+s+A+1$ in $D^e_2$.

In maximum polarity use input $n-G$ and complement output about $m$. The actual cuts are $n+1-c$ and $m+1-C$. Since $2K=A+B+s$, the actual old lower and upper shifts become $B$ and $B+s$. Both label inventories complement and exchange their sides, with all weights and crossings preserved. The actual frontier is $m$ at $w$ and the literal connector endpoints are $(m-(n+s+A+1),m)=(B-1,m)$.

For a finite sequence of individually admitted blocks, each keeps its own actual input graph, state, cut and spectrum and satisfies its size and topology requirements. Subsequent placements preserve the evolving sides of earlier labels. For a completed cut $C_i$ let $U_i,V_i$ sum later actual lower shifts and gap widths. The exact final map on that completed alphabet is $x\mapsto x+U_i+V_i\mathbf1_{x\ge C_i}$. Crossing weights gain $V_i$, noncrossing weights are unchanged. This lifts both exact intermediate inventories and the literal connector endpoints and weight. The later fresh values are disjoint at every insertion and belong to the remaining sets of earlier boundaries in the final alphabet. Induction proves all admitted returns. The finite indexed role lists, bounded imbalance sequences, finite gap permutations and growth and backward sums yield a terminating construction that emits each final original label immutably. The independent initializer and decomposition questions retain their own scopes.

## 7. Scope and continuity

The monotone local model gives exact quota support within its fixed footprint, and the broader parity-compatible growth gives a sufficient class for the named H1 arrangement. General H1 feasibility remains open. The concrete cumulative-imbalance mechanism resolves this investigation symbolically. The custody and reviews record zero scientific search, solver, checker, campaign and replay. There is no new scientific execution.

D185 is Director accepted in its exact written scope at checkpoint 89235bc021d35e84651a6b6d1b0b6b8ca32eb198. Its disjoint-tile theorem, D184's scoped neutral-bank conclusions and all earlier accepted proofs remain intact. The D174 history of one completed pair, two numerical arms and 3,518 unentered originals stays separate from D177's accepted symbolic projection of 93 with 92 historically unentered.
