# D188 — Direct-leaf slots in the wider exceptional exterior

Task **LCL-ORDINARY-SPINE-EXCEPTIONAL-DIRECT-LEAF-SLOT-CONSTRUCTION-001**.

**PROVED WITHIN EXACT WRITTEN SCOPE / PENDING DIRECTOR REVIEW.** In the named topology and independently admitted D157 arrangement of §1, the construction permits arbitrary nonnegative counts of actual direct leaves on both new sections, subject to the stated effective width, first quota and full target conditions. All direct leaves are in the exterior at their own spine parents. The construction uses zero arithmetic quota at their first-section slots and a sparse menu of actual second terminal hosts. Its sufficient target domain is given by the exact local support, baseline parities and bank costs in §§3–5. It retains the complete D187 domain and includes the stated three-second-center topology. General H1 feasibility retains its separate scope.

## 1. Original vertices, graph counts and exterior

All quantities and labels are exact integers, excluding booleans. Intervals are inclusive and inverted intervals are empty. Let $r,\nu$ count the actual positive first and second centers, $z_1,z_2\ge0$ the actual direct leaves, and $F,R$ the full terminal totals excluding direct leaves. Put $r_*=r+z_1$ and $\omega=\nu+z_2-1$. Require $\nu\ge3$, $\omega=2+2\ell+\eta\ge4$ with $\ell\ge1$, $\eta\in\{0,1\}$, and $r\ge2g+6+e$ with $g\ge0,e=g\bmod2$. There are exactly $2g+\eta$ positive odd first quotas among the $r$ actual positive first centers and the other quotas are positive even. Take distinct actual first centers for the neutral and deficit-two roles, an even quota at least six and a quota at least $\omega$ of parity $\eta$, respectively. The other three tail roles, the reserved shift-one role and any even packet middle use actual positive even centers. The actual second quotas are positive and must meet the baseline and growth tests below.

Use the independently supplied named [D157 $S_{-1}$ input](ORDINARY_SPINE_ALTERNATING_EXCEPTIONAL_SPECTRUM.md#1-interface-and-exact-inventory-rule), with $n=2c+2$ edges, witnessing spine ending at actual extreme frontier $v$, and oriented label $G(v)=0$. Equality is on the upper side of cut $c$. Put $d=c+2$, so the input crossing and noncrossing bands are $[d-1,n]$ and $[1,d-2]$. Append the original spine vertices $u,w$. The two spine edges, all actual child edges and all terminal edges give the exact fresh count
$$
2K=F+r+z_1+\nu+z_2+R+2=F+r_*+\omega+R+3.
$$
Full admission requires $n\ge2K$ and $m=n+2K$.

In the declared same-phase arrangement root the new original graph colors at lower $v$. The first centers and direct leaves are lower, as are $w$ and the second terminals. The upper vertices are $u$, the second centers and direct leaves and the first terminals. Hence
$$
N_{\rm low}=1+r_*+R,\qquad N_{\rm high}=\omega+2+F .
$$
A connected crossing exterior identifies its graph colors with its reduced sides. For widths $A,B$, $s=2K-A-B$ and $k=K-A$, let $x$ count lower gap sources at upper hosts and $y$ upper gap sources at lower hosts. Those are exactly the crossing gap edges. The least old crossing weight becomes $d-1+s$, so the same-phase requirement gives $s\ge K$. The crossing gap images are $[K,s-1]$ and $x+y=s-K$. Counting graph colors by the actual parent colors at the gap gives
$$
N_{\rm low}=A+s-k-y+x=2(A+x),\qquad N_{\rm high}=B+k-x+y=2(B+y).
$$
Both are even, giving $R\equiv r_*+1$ and $F\equiv\omega\pmod2$.

In any terminal-enabled compatible exterior of the declared kind the reduced weight one joins $A,A+1$. It is the actual edge $vu$, since $v=A$ has just that fresh incidence. Compare the reduced edge spectrum with the reference using $vu,uw$, attaching slots $[1,A-1]$ to $u$ and upper slots $A+b$ for $b\ge2$ to $w$. Their weights are $[1,A+B]$. Replacing reference parents by the actual selected-terminal parents decreases the sum by each first selected terminal's positive lower parent label and increases it by each second selected terminal's positive value $b-1$. Exterior direct leaves keep their actual reference parent edges. Equal sums force both selections to be nonempty when either is nonempty. If all first direct leaves are exterior, the fresh lower exterior size is then $A=r_*+1+e_2$ where $e_2\ge1$ is the number of selected second terminals. The lower count gives $R\ge r_*+3$. These restrictions concern the stated exterior and gap arrangement.

For the supplier take $A=r_*+2$, $B=\omega+3$ and reduced labels $v=A,u=A+1,w=0$. Give all $r$ actual first centers and $z_1$ direct leaves the slots $[2,A-1]$, at their common actual parent $u$. The assignment below makes reduced label 3 the actual deficit-two center. Its first indexed terminal goes at $A+3$. Give Q label $A+2$. The remaining upper slots for actual children at $w$ are $A+2+\rho$ for $\rho\in[2,\omega+1]$. Choose any indexed menu $\Gamma\subseteq[2,\omega+1]$ of size $\nu-1$ containing $\{2,\omega-1\}$. Such a choice is possible since these two required indices are distinct, $\nu-1\ge2$, and $\nu-1\le\omega$. Assign the remaining actual positive second centers to $P_\rho$ for $\rho\in\Gamma$, and the actual second direct leaves to the complementary slots. That complement has $\omega-(\nu-1)=z_2$ members. Give the first terminal of the actual $P_2$ reduced label 1. The vertices have exactly labels $[0,A+B]$, with the final upper slot occupied by whichever actual child its menu specifies.

All reduced edges cross, and the spine and actual parent incidences make the exterior connected. Its exact weights are 1 at $vu$, $[2,A-1]$ at the first child edges, $A$ at the selected first terminal, $A+1$ at $uw$, $A+2$ at $wQ$, $A+3$ at the selected $P_2$ terminal, and $[A+4,A+B]$ at the remaining second child edges. This exhausts $[1,A+B]$ independently of how many of those children are direct leaves. Only genuine positive centers and the actual spine vertices support the edges just specified. The residual terminal allocation will use only actual positive centers.

## 2. Effective fold and regular role availability

Write $t=(\alpha_{\rm neutral}-4)/2\ge1$, $h_N=t$, $h_R=(\sum_{\rm regular}\alpha-2(r_*-5))/2$, $h_T=(\sum_{\rm tail}\alpha-8-\eta)/2$, and $h=t+h_R+h_T$. The $r_*-5$ regular slots will contain all $z_1$ direct leaves of arithmetic quota zero and all $2g$ regular odd quotas. Positive even quotas are at least two and positive odd quotas at least one, so
$$
\sum_{\rm regular}\alpha\ \ge2(r_*-5-z_1)-2g,\qquad h_R\ge-g-z_1 .
$$
The regular sum is even. At tail deficits $d_0=1,\ldots,4$ use $\alpha_{d_0}=2+2v_{d_0}+\eta\mathbf1_{d_0=2}$. Their hypotheses give nonnegative integer $v_{d_0}$ and $v_2\ge\ell$, hence $h_T=\sum v_{d_0}\ge\ell$. The neutral, regular and tail sum is $F=2r_*+2+2h+\eta$. Put $R_0=r_*+3$ and use $R=R_0+2z$ at cumulative width increase $z$. This total and $F$ meet the graph parities. From the actual count,
$$
K=2r_*+5+h+\ell+\eta+z,\qquad s=2K-A-B=3r_*+3+2h+\eta+2z,\qquad k=K-A,\quad J=s+3 .
$$
In particular
$$
K-(A+B)=r_*-2+h-\ell+z\ge r-2+t-g+z>0,
$$
using $r\ge2g+6+e$. Thus $s\ge K$ and $A\le K\le A+s$. Final size admission covers every auxiliary width.

A gap source of numeric coordinate $i$ has label $A+c+i$ and is lower at $C=c+K$ iff $i<k$. Difference subtraction from a lower reduced parent of label $j_0$ gives $d-1+\pi(i)$ with $\pi(i)=i+\delta$ and $\delta=A-1-j_0$. At upper host $n+s+A+b$ it gives $\pi(i)=s+b+1-i$. The lower and upper bands flank the gap, which fixes both absolute signs. Folding by $L_j=j,H_j=J-j$ gives the exact alphabets
$$
\begin{array}{c|cc}
 & L & H\\
\text{sources}&[0,r_*+2+h+\ell+\eta+z]&[4,2r_*+3+h-\ell+z]\\
\text{images}&[0,2r_*+4+h+\ell+\eta+z]&[4,r_*+1+h-\ell+z].
\end{array}
$$
The two H rows unfold to $[k,s-1]$ and $[K,s-1]$. Their respective L rows are the numerical complements in $[0,s-1]$. Actual lower hosts keep rows and shift $+\delta,-\delta$ on L and H. Actual upper hosts $P_\rho$ exchange rows with shifts $-\rho,+\rho$, and Q exchanges at equal index. These maps apply only at actual centers and with endpoints inside their actual rows. An H image corresponds exactly to the source and its actual parent on opposite physical sides, with predicate $\pi(i)\ge K$. Increasing $z$ by $\lambda$ adds $\lambda$ to each upper row endpoint and $2\lambda$ to $J$.

Assign the first roles in increasing lower shifts $\delta$ from $0$ to $r_*-1$, at label $A-1-\delta$. The neutral role has shift zero and the four tail deficits use shifts $r_*-d_0$. Among the three even tail hosts choose a smallest at deficit one, so $v_3\ge v_1$. The actual even hosts required for neutral, the other three tail roles, shift one and the possible even packet middle number $5+e$, plus $1-\eta$ for deficit two. The bound $r-2g-\eta\ge6+e-\eta$ supplies them. When $\eta=1$ the odd deficit-two center is reserved before packing the other $2g$ odd quotas. The positive regular shift one is reserved and the next $2g+e$ roles are the [D182 parity packets](ORDINARY_SPINE_EXCEPTIONAL_PARITY_NEUTRAL_PACKETS.md#3-two-independently-expandable-parity-neutral-packets). Thus the eligible ordinary interval $\mathcal D=[2+2g+e,r_*-5]$ has $N=r_*-6-2g-e\ge z_1$ slots. It accommodates all $z_1$ direct leaves and exactly $r-6-2g-e$ remaining even centers. When $N=0$ there are no such vertices and the reserved host and packets fill the positive regular roles.

Use the four initial neutral L identities at $[0,3]$. The $t$ extra neutral pairs at $[4,3+t]$ give the unchanged L bank and their separate H identities. A pair at shift $\delta$ and position $i$ uses $L_i\to L_{i+\delta}$ and $H_{i+\delta}\to H_i$ at the actual first parent. At shift one use all its pairs. For each parity packet use its actual consecutive shift block and the D182 local lists and expansions. The three-host and four-host central lists reserve identical sets in both intermediate rows, with root quota counts $(1,2,1)$ and $(1,1,1,1)$. Their ordinary expansions still reserve the same columns in both rows, and common free columns use Q. Those local proofs use only consecutive positions, actual quota counts and the lower shifts. Each retained paired or packet group uses equal L-source and H-image position counts. The eligible interval also has equal counts in aggregate, including after the reassignment in §3. Across the positive regular strip the total count in each row is $r_*-5+h_R$. Thus the regular positions run from $4+t$ through $r_*-2+h_*$ for $h_*=t+h_R$, allowing empty arithmetic groups at zeros. The intermediate footprints have the uniform bound $2r_*-7+h_*$ from adding largest regular shift $r_*-5$ to the regular endpoint. Neutral pairs also satisfy that bound since $h_R\ge-g-z_1$ gives $2r_*-10+h_R\ge2r+z_1-10-g\ge0$. The tail starts at $2r_*-5+h_*\ge2r+z_1+t-g-5\ge4$, strictly above the regular bound. The exact eligible footprint and its absent-host cases are addressed next.

## 3. Monotone groups with zero-quota slots and sparse matching

Write the eligible slot quotas as $2k_j$, $1\le j\le N$, with $k_j\ge0$. A positive $k_j$ belongs to its actual even center and a zero belongs to its actual direct leaf. At consecutive shifts $\delta_j=\delta_1+j-1$, put $S_j=\sum_{i\le j} k_i$, $S_0=0$ and $S=S_N$. When $N=0$ there are no eligible positions or local matchings to change. Otherwise let $x_0$ be the first shared position after the reserved role and parity packets, and give the eligible slots the shared position interval $[x_0,x_0+S-1]$, which is empty when $S=0$. Use the [D186 cumulative model](ORDINARY_SPINE_EXCEPTIONAL_CUMULATIVE_IMBALANCE_ALLOCATION.md#2-monotone-first-allocation-and-exact-unused-cells) with $u_0=u_N=0$ and $|u_j-u_{j-1}|\le k_j$. The L and H group lengths are $k_j+u_j-u_{j-1}$ and $k_j-u_j+u_{j-1}$. Each is nonnegative and the two total counts are $S$. At $k_j=0$ the step bound forces $u_j=u_{j-1}$ and both lengths zero. Therefore there is no residual arrow or terminal at the actual direct leaf. Its original edge at $u$ is already exterior.

For sign $\varepsilon=+1$ in the L-image row and $-1$ in the H-source row, let $P_j^\varepsilon=S_j+\varepsilon u_j$ and $a_*=x_0+\delta_1$. The group at slot $j$ reserves the exact interval
$$
[a_*+P_{j-1}^\varepsilon+j-1,\ a_*+P_j^\varepsilon+j-2].
$$
This follows by adding its shift $\delta_j$ to its consecutive position interval. For $j<N$ its intervening singleton column is
$$
c_j+\varepsilon u_j,\qquad c_j=a_*+S_j+j-1 .
$$
The reservation intervals and these intervening singletons are an ordered contiguous partition of $[a_*,a_*+S+N-2]$. The first group starts at $a_*$, a following singleton is immediately after the last reservation of that group, and the next group starts one after the singleton. An empty group consumes no column and still gives the same ordered partition. The last right endpoint follows from $P_N^\varepsilon=S$. This verifies the exact complements, injectivity and separation even for leading, trailing and consecutive empty groups, whether the emptiness occurs at a positive center or a zero slot.

When $N=1$ the imbalances are both zero. A positive quota contributes a full common group of $S$ consecutive cells with no local gap. A zero gives $S=0$ and an empty footprint $[a_*,a_*-1]$. When $N\ge2$ and $S=0$ every $k_j=0$ and all $u_j=0$, so the footprint has exactly the $N-1$ common singleton columns and no lower assignments. Any complete local matching on identical gap sets has total index difference zero. The available H-to-L differences are nonnegative, with positive ones only at actual shifted hosts. Thus all differences must vanish, so the exact local completion is the Q identity even for consecutive zeros.

For any $N\ge1$ the preceding intermediate groups end at most at $(x_0-1)+(\delta_1-1)=a_*-2$. The stated footprint's right endpoint is $(x_0+S-1)+(\delta_1+N-1)=2r_*-7+h_*$, since $x_0+S-1$ is the regular endpoint and $\delta_1+N-1=r_*-5$. This upper bound also applies when its end is calculated from empty groups. Its left endpoint lies within the two intermediate rows, and the right bound is below the separated tail. Thus the zero-slot singleton columns are genuine H-source and L-image cells, with neither rows nor preceding groups disturbed. The remaining common columns between these footprints use Q.

For fixed imbalances, the exact local matching pairs distinct H-source gaps $c_j-u_j$ with distinct L-image gaps $c_{\sigma(j)}+u_{\sigma(j)}$ for a permutation $\sigma$. Its required separations are
$$
\rho_j=c_{\sigma(j)}-c_j+u_j+u_{\sigma(j)}\ \in\ \{0\}\cup\Gamma .
$$
These conditions are sufficient by the actual H-to-L maps and necessary since any local completion with those upper hosts determines just such a bijection and those differences. Zero uses Q and a positive $\rho_j$ uses the actual indexed $P_{\rho_j}$. An absent upper host, including at a slot occupied by a direct leaf, has no available arrow. The multiplicity $m_\rho$ is exactly the number of positive matches at that host. With the original ordinary common Q completion as comparison, the signed first-moment change is $2\sum_j\delta_j(u_j-u_{j-1})=-2\sum_{j<N}u_j$. The matched gap contribution is $\sum_j\rho_j=2\sum_{j<N}u_j$, so exact compensation holds even across zero slots. The cases $N=0,1$ have no positive local matches.

For the stated direct-leaf-assisted case $N\ge2$, take true first positive even centers at the first and last slots, and $u_j=1$ at every internal boundary. Only the first and last steps are nonzero and those two $k_j$ are at least one. All intermediate zero slots obey equality of adjacent imbalances. With identity permutation every separation equals two. Thus $M=N-1$, and the baseline of §4 gives $q_0=5+2g+e$ and $q_2=N$. This sufficient baseline Q floor is independent of $z_1$, while the baseline total and required $P_2$ quota account for the additional slots. With a full bank the baseline Q floor and its parity suffice at Q for these dominating targets, together with all other stated conditions.

## 4. Tail on the actual sparse host menu and complete baseline

Use the parity-unified local tail of [D187 §3](ORDINARY_SPINE_EXCEPTIONAL_PARITY_UNIFIED_MULTI_HOST.md#3-unified-tail) at the effective parameters. Put $H_T=\sum v_d=h_T$, $N_T=H_T+2$ and $D_*=2r_*+h_*$. The actual tail positions are $r_*+h_*+x$ with local L-source offsets $[-1,N_T+\ell+\eta]$ and H-image offsets $[-1,N_T-1-\ell]$. Their right endpoints match the baseline folded rows and their starts follow the regular positions exactly. A deficit $d_0$ reserves column $D_*+x-d_0$. The tail windows relative to $D_*$ are H sources $[-5,N_T+1-\ell]$ and L images $[-5,N_T+2+\ell+\eta]$. Their right endpoints match the full intermediate rows. Their common start $D_*-5$ is the separated bound proved in §2.

Among the three even tail hosts assign a smallest quota to deficit one, so $v_3\ge v_1$. Use the arithmetic even parts of their actual quotas and the full even part of deficit two. Starting at local position $-1$, use $1+v_4$ ordinary pairs at deficit four, then $v_3-v_1$ at deficit three, then $v_1+1$ ordered groups $(1,3)$ in each row, then $v_2$ ordinary pairs at deficit two. Follow with one L-only arrow at deficit two. The groups $(1,3)$ reserve their two-position block shifted by minus two, and the later pairs also reserve their positions minus two. Earlier pair columns are strictly below these footprints. Each shared alphabet uses $3+H_T$ positions through $N_T-1$ and the L-only use is at $N_T$. The two rows' group totals supply the exact even-part quotas at each host after restoring the one exterior terminal at deficit two.

Transfer the last $\ell$ H-image uses at $[N_T-\ell,N_T-1]$ to L positions $[N_T+1,N_T+\ell]$ at the same actual deficit-two host. This is legal since $v_2\ge\ell$. For $\eta=1$ put one further actual terminal at L position $N_T+\ell+1$ there, supplying its exact odd quota. The retained H reservation set $Y$ lies at most at $N_T-\ell-3$. The L list retains the occupied columns $[N_T-\ell-2,N_T-3]$ from the transferred positions and its L-only $N_T-2$, adds $[N_T-1,N_T+\ell-2]$ for the transferred L uses, and adds $N_T+\ell-1$ iff $\eta=1$. Therefore the exact L reservation set is $Y\sqcup[N_T-\ell-2,N_T+\ell-2+\eta]$. Its columns and those of $Y$ are distinct in each row and lie inside the actual windows. The local position lists exactly fill the stated source and image positions.

Below $N_T-\ell-2$ the intermediate residual columns coincide and use Q. The four terminal H-source cells $[N_T-\ell-2,N_T-\ell+1]$ go in order to the four terminal L-image cells $[N_T+\ell-1+\eta,N_T+\ell+2+\eta]$. Their difference is $\omega-1$, and this actual $P_{\omega-1}$ is required in $\Gamma$. These exact partitions require no available center at any other tail separation.

The signed folded moment required by the four alphabets is $A(B-4)$, since the L images add $A$ indices starting at $k$ and H images remove $A$ indices starting at $J-K+1=k+4-B$. The shared neutral and regular ordinary and packet groups have zero net contribution because their L-source and H-image positions agree and their intermediate reservations agree. The cumulative change cancels exactly in §3. The first tail contribution is $(r_*-2)(1+2\ell+\eta)$, from the final L-only arrow, the changes in signs of $\ell$ transfers and the extra L use for odd $\omega$. The four upper tail arrows contribute $4(\omega-1)$. Thus the total is $(r_*+2)(\omega-1)=A(B-4)$. This is a separate check from the explicit four-row partitions.

The initial four L identities, neutral pairs, regular footprints, exact eligible completion and tail together give all four bijections at baseline. Every L source uses a first host and every H image comes from a first host. The H-source and H-image rows have $2r_*+h-\ell$ and $r_*-2+h-\ell$ cells, leaving $r_*+2$ upper gap uses. In the unredistributed case exactly four of these use $P_{\omega-1}$ and the rest Q. With the one exterior terminal at $P_2$, this gives $q_0=r_*-2$, $q_2=1$, $q_{\omega-1}=4$ and zero elsewhere among actual shifted hosts. For a chosen local histogram the exact counts are
$$
q_0=r_*-2-M,\qquad q_2=1+m_2,\qquad q_{\omega-1}=4+m_{\omega-1},\qquad
q_\rho=m_\rho\quad(\rho\in\Gamma\setminus\{2,\omega-1\}).
$$
They sum to $R_0=r_*+3$. Since $M\le\max(0,N-1)$, $q_0\ge5+2g+e$ for $N\ge1$, and $q_0=r_*-2>0$ for $N=0$. These are auxiliary counts only at actual centers, and the eventual target quotas dominate them. The row counts also give $x=0$ and $y=r_*-2+h-\ell$ at baseline.

## 5. Bank growth and finite indexed supplier

The [D184 bank invariant](ORDINARY_SPINE_EXCEPTIONAL_NEUTRAL_ANCHOR_BANK_GROWTH.md#2-removing-and-restoring-an-entire-bank) is present: exact four-row bijections, fixed four initial L identities, all other folded endpoints at least four, and the unchanged named L bank of width $t$. Every required growing host is actually in $\Gamma$. Equal width increments advance all four row ends by the same amount. The D184 proof uses just the row maps, the named bank and these endpoints. For a chosen bank width $T$ and increment $\lambda>0$, translating and then completely removing the chosen bank before restoring it gives free L intervals $[4+T,3+T+\lambda]$ and H intervals $[4,3+\lambda]$. At $T=\rho$ a pure step uses the whole free sets in both directions at the actual $P_\rho$ and requires no Q increment. At $T<\rho$ and $\lambda=\rho b$ it uses the $T$ affected residues at $P_\rho$, with the remaining equal intervals by residue matched at Q, for $2Tb$ shifted leaves and $2(\rho-T)b$ Q leaves. Both proofs include the possible actual separation $\omega+1$, using its own $\rho$ in the window formulas and no shifted arrow at a missing role.

Take actual positive target quotas $p_\rho\ge q_\rho$ and $p_\rho\equiv q_\rho\pmod2$ at each role. For the shifted roles set $b_\rho=(p_\rho-q_\rho)/2$. For $\rho\le t$ a pure step of width $b_\rho$ gives cost zero. For $\rho>t$ divide $b_\rho$ by $t$. Use the quotient as the batch at bank width $t$ and, for a nonzero remainder, one batch at the remainder width. Thus the Q cost is $C_\rho=2(\rho\lceil b_\rho/t\rceil-b_\rho)$ in that case. Omit zero operations and order all shifted steps by nonincreasing bank width, then separation and step type. Each keeps its selected bank prefix for the next step. Under the sufficient bound $p_0\ge q_0+\sum_{\rho\in\Gamma}C_\rho$ and matching parity, finish with the Q-only step of integer width $a=(p_0-q_0-\sum C_\rho)/2\ge0$. It translates all noninitial folded endpoints and fills both directions of the remaining common strip by Q. This gives
$$
\lambda_{\rm final}=a+\sum_{\rho\in\Gamma}(b_\rho+C_\rho/2),\qquad R=r_*+3+2\lambda_{\rm final}.
$$
Every stage has room in the actual target counts. The exact crossing counts are $x=\lambda_{\rm final}$ and $y=r_*-2+h-\ell$ since first-host row counts stay fixed. The paired growth increments have opposite signed changes in the two upper directions, and the restored identities have zero shift. Thus the signed moment stays exact. The sufficient full-bank test for all actual shifted hosts is $t\ge\max\Gamma$. An actual center at the last slot may require $t\ge\omega+1$ for pure growth there. Parity and quotas govern only the actual roles.

A finite indexed supplier can list eligible ordered neutral and deficit-two pairs, the other tail choices satisfying the minimum at deficit one, actual regular and packet assignments, the original direct leaves in eligible ordinary slots, and the sparse upper menus satisfying their inclusion and cardinality tests. The second centers, Q and remaining direct leaves are indexed assignments to their actual slots. In each choice list the bounded imbalance sequences with $|u_j|\le\min(S_j,S-S_j)$, and the finite gap permutations or empty cases. Apply the exact matching, positive target domination and parity, Q-cost and full-size tests. Choose the first passing indexed tuple in fixed lexicographic order and extract its bank schedule. Equal-valued vertices retain distinct actual names. This arithmetic specification terminates and was not run as a search. Taking $z_1=0,z_2=1$ and $\Gamma=[2,\nu]$ recovers $r_*=r,\omega=\nu$ and the full D187 exterior, local choices, quotas and growth. The lone second direct leaf then occupies the last slot. This retains every accepted D187 input under the same admissions.

## 6. Symbolic original-target controls

Use the retained independent 74-edge $S_{-1}$ input with actual maximum frontier 74 at $s:27$ and actual cut 39. Its minimum orientation uses $c=36$. Each zero in these ordered profiles denotes the actual direct leaf at that section. The first listed first center is neutral and the second is deficit two. Assign the listed positive second centers to Q and the increasing listed members of $\Gamma$ for each control. Assign direct leaves in original index order within the designated slots.

| Case | Actual first section | Actual second section | $(r,\nu,z_1,z_2)$ | $(r_*,\omega)$ | $(F,R,2K)$ | $t$ | $\Gamma$ |
| --- | --- | --- | --- | --- | --- | ---: | --- |
| A | $(12,4,2,2,2,2,2)$ | $(5,1,4,2,0)$ | $(7,4,0,1)$ | $(7,4)$ | $(26,12,52)$ | 4 | $\{2,3,4\}$ |
| B | $(14,4,2,2,2,2)$ | $(4,1,4,2,2)$ | $(6,5,0,0)$ | $(6,4)$ | $(26,13,52)$ | 5 | $\{2,3,4,5\}$ |
| C | $(14,6,2,2,2,2)$ | $(4,1,6,0,0,0,0)$ | $(6,3,0,4)$ | $(6,6)$ | $(28,11,54)$ | 5 | $\{2,5\}$ |
| D | $(12,4,2,2,2,2,0,0)$ | $(6,1,4,2,0)$ | $(6,4,2,1)$ | $(8,4)$ | $(24,13,52)$ | 4 | $\{2,3,4\}$ |
| E | $(16,5,2,2,2,2,2,2,0,0)$ | $(5,4,4,2,0,0)$ | $(8,4,2,2)$ | $(10,5)$ | $(33,15,66)$ | 6 | $\{2,4,6\}$ |

The displayed totals sum only terminals, and the fresh counts add the actual child and spine edges by §1. All are admitted by 74. In every control $g=e=0$. In C, $\ell=2,\eta=0$, and in E, $\ell=1,\eta=1$. Elsewhere $\ell=1,\eta=0$. Each tail uses three other even quotas two and the listed qualifying deficit-two quota. Thus $v_2=\ell$, $v_1=v_3=v_4=0$ and $N_T=\ell+2$. The H reservations retained in the tail are $\{-5,-2,-1\}$. The L list adds $[0,2\ell+\eta]$. The suffixes are $[0,3]$ in H and $[2\ell+1+\eta,2\ell+4+\eta]$ in L, with the two other free common columns $-4,-3$ assigned at Q. This checks the tail explicitly at the controls.

- **A.** There is one ordinary eligible even host and no local gap. Use $(5,1,4,0)$ as the baseline. Pure width one at $P_4$ with bank four fills L index 8 and H index 4 in both directions. Q stays five and the final slot is the original second direct leaf. This is the accepted [D187 control A](ORDINARY_SPINE_EXCEPTIONAL_PARITY_UNIFIED_MULTI_HOST.md#5-matched-symbolic-controls).
- **B.** There are no ordinary eligible slots. The actual baseline at $Q,P_2,P_3,P_4,P_5$ is $(4,1,4,0,0)$. Apply the pure width-one steps at $P_5$ then $P_4$, with bank widths five and four. The free L indices are 9 and 8, respectively, and the free H index at each step is 4. The final exterior slot stands at actual $P_5$ with reduced label $A+7$. No direct leaf is required at either section.
- **C.** There are no eligible ordinary slots. The actual baseline $(4,1,4)$ at $Q,P_2,P_5$ is followed by pure width one at $P_5$. Actual direct leaves occupy the four slots of index 3, 4, 6 and 7, which are unavailable for terminal uses at these shifts. The widest actual shift is five despite $\omega=6$. This is a three-positive-second-center topology. The completed target has exactly six at $P_5$ and Q stays four.
- **D.** Both eligible slots at shifts 2 and 3 contain actual direct leaves. Here $h_R=-2$, $h_*=2$, regular endpoint 8, and the empty shared interval begins at $x_0=9$. Thus $a_*=11$ and the entire eligible footprint is the single common gap 11, filled by $H_{11}\to L_{11}$ at Q. The baseline $(6,1,4,0)$ is followed by pure width one at $P_4$. If only one of those first zeros is present, the corresponding $r_*=7$ and $N=1,S=0$ give an empty eligible footprint. For example with second section $(5,1,4,2,0)$ the fresh count is $24+7+4+12+3=50\le74$, the baseline is $(5,1,4,0)$ and the same $P_4$ growth applies.
- **E.** Here $h_R=-2$, $h_*=4$ and the eligible positions are $[11,12]$. Put actual even quotas two at the endpoints of shifts $[2,5]$ and the two actual first direct leaves at shifts 3 and 4, in original index order. They all retain their original parent $u$. With $k=(1,0,0,1)$ and $u=(0,1,1,1,0)$ the L group lengths are $(2,0,0,0)$ and the H group lengths $(0,0,0,2)$. Relative to $a_*=13$ the footprint is $[0,4]$. The H-source gaps are $\{0,1,2\}$ and the L-image gaps $\{2,3,4\}$. Identity matching gives three $P_2$ arrows. The second direct leaves occupy the slots at separations 3 and 5, retaining their actual parent $w$, and none is used for a terminal arrow. The odd deficit-two quota is five and the extra L assignment is at that actual first center. With the four widened-tail arrows at $P_4$, the baseline $(5,4,4,0)$ at $Q,P_2,P_4,P_6$ has total 13. The actual $P_6$ occupies the final upper slot. Pure width one with bank six matches L index 10 to H index 4 in both directions there and adds the two target uses at $P_6$ with Q unchanged. Here $\max\Gamma=6=\omega+1$.

The completed maximum-polarity $(m,\text{cut})$ for A through E are $(126,65),(126,65),(128,66),(126,65),(140,72)$. The lower crossing weights are $63,63,64,63,70$, respectively, and the upper endpoints are $m$ in each case. These follow from the verified spectra in §7. The full composition can also apply A and then E. The first supplies a named 126-edge return, sufficient for E's 66 new edges. It gives 192 edges at maximum cut $65+33=98$ with crossing band $[96,192]$. Both direct-leaf counts change between the blocks. All controls establish symbolic coverage on the retained input data.

## 7. Exact original resources and immutable return

All original centers and direct leaves retain their actual indexed names and spine parents in the exterior of §1, with the two selected terminals at their own actual centers. At baseline assign each first lower arrow to its actual original terminal in fixed row and position order. In particular a zero first slot has no such name to assign. At the upper roles name baseline gap uses from the actual available terminal indices, leaving out the terminal already selected at $P_2$. Name inserted upper arrows at their actual hosts during the finite bank schedule. No step exceeds any target's own available count. All translations and restorations keep actual names and parents. This realizes all original terminals, every direct leaf and the witnessing spine.

Use the exact baseline $J_0=3r_*+6+2h+\eta$. For an actual first center of shift $\delta_j$, let $S_j^{\rm b}$ be its numeric baseline source set. Derive it from its L-source positions and its H-image positions, converting the latter's index $i$ to $J_0-i-\delta_j$. For an eligible center these two position intervals are the cumulative group lists of §3. For tail hosts they are the exact lists of §4 at positions $r_*+h_*+x$, including the extra odd deficit-two L use where applicable. The neutral and other regular hosts use their exact paired or packet lists. A direct-leaf slot has empty terminal sets. Each actual first center's baseline image set is $S_j^{\rm b}+\delta_j$ by §2. Pairwise disjointness in each alphabet follows from the full baseline partitions.

For each shifted step let $T_j,\lambda_j$ denote its bank width and width increment. The extra baseline neutral L identity at $i\in[4,3+t]$ has final coordinate in both alphabets
$$
\phi(i)=i+\lambda_{\rm final}-\sum_{j:\,i<4+T_j}\lambda_j .
$$
Indeed any such name eligible at step $j$ was restored at every earlier step by the width order and is still at the original $i$. Once ineligible its current index is at least $i\ge4+T_j$ and it stays outside every later selected prefix. Complete removal and restoration of the chosen set preserve that exact name tracking. The last Q step restores none. The initial four remain fixed and all other noninitial endpoints gain the full folded shift, including the neutral H arrows. The final H unfolding at $J=J_0+2\lambda_{\rm final}$ gives $J-(i+\lambda_{\rm final})=J_0-i+\lambda_{\rm final}$ for a fully translated H endpoint. This uses the actual parity-dependent baseline $J_0$.

On baseline numeric coordinates define $\Phi(i)=i$ for $i\in[0,3]$, $\Phi(i)=\phi(i)$ for $i\in[4,3+t]$, and $\Phi(i)=i+\lambda_{\rm final}$ otherwise. In each alphabet the two initial intervals are already occupied by their respective neutral L identities. The exact first and remaining gap resources are
$$
I=\bigsqcup_j\Phi(S_j^{\rm b}),\quad J_1=\bigsqcup_j\Phi(S_j^{\rm b}+\delta_j),\qquad
I'=[0,s-1]\setminus I,\quad J_2=[0,s-1]\setminus J_1 ,
$$
summing over actual first centers. The unions are disjoint by the exact final bijections. Every first arrow still has its original numeric translation because its endpoints either translate equally or are a neutral identity.

For minimum polarity shift old labels by $A$ below $c$ and by $A+s$ at or above $c$, preserving sides at $C=c+K$ by $A+c-1<C\le A+c+s$. The old crossing differences gain $s$ and the old noncrossing differences are fixed. Place each gap source $i$ at $A+c+i$ and add $n+s$ to each upper reduced exterior label. The common $v$ agrees at $A$ and every exterior difference gains $n+s$. All exterior edges cross since their lower endpoints are at most $A<C$ and upper endpoints at least $n+s+A+1>C$. The exact old and fresh palettes are
$$
\begin{array}{ll}
L_{\rm old}=[A,A+c-1]\sqcup[A+c+s,n+s+A],&
L_{\rm fresh}=[0,A-1]\sqcup[A+c,A+c+s-1]\sqcup[n+s+A+1,m],\\
D_{\rm old}=[1,d-2]\sqcup[d-1+s,n+s],&
D_{\rm fresh}=[d-1,d+s-2]\sqcup[n+s+1,m].
\end{array}
$$
These partition $[0,m]$ and $[1,m]$ by $m=n+s+A+B$. The exact reduced spectra and folded and unfolded bijections fill their indicated fresh intervals on actual values and count the shared $v$ only once. Physical gap crossings use $[d+K-1,d+s-2]$ and noncrossings $[d-1,d+K-2]$. Together with old and exterior edges this gives exact crossing and noncrossing spectra $[d+K-1,m]$ and $[1,d+K-2]$. Since $w=0$, $m=2C+2$ and the original witnessing spine extends through $u,w$, this is the exact $S_{-1}$ return.

At the boundary after the first section the fresh exterior labels of the first and remaining sections are
$$
E_1=[2,A-1]\sqcup\{n+s+A+1,n+s+A+3\},\qquad
E_2=\{0,1,n+s+A+2\}\sqcup[n+s+A+4,m].
$$
The interval $[2,A-1]$ in $E_1$ consists of actual first centers and actual first direct leaves, all with their edge to $u$. The two individual upper values are $u$ and the selected terminal of first center 3. In $E_2$ the two lower values are $w$ and the selected $P_2$ terminal, and $n+s+A+2$ is Q. Its remaining upper interval is precisely the actual shifted centers and the original second direct leaves. The difference bands are $D^e_1=n+s+[1,A]$ and $D^e_2=n+s+[A+1,A+B]$ by those very incidences. Thus the two exact inventories are
$$
\begin{array}{ll}
\text{used labels}&L_{\rm old}\sqcup E_1\sqcup(A+c+I),\\
\text{remaining labels}&E_2\sqcup(A+c+I'),\\
\text{used differences}&D_{\rm old}\sqcup D^e_1\sqcup(d-1+J_1),\\
\text{remaining differences}&D^e_2\sqcup(d-1+J_2).
\end{array}
$$
Partition labels from the old bands and exterior reduced sides. Gap labels use intersections of $I,I'$ with $[0,k-1]$ and $[k,s-1]$ before adding $A+c$. Gap differences use intersections of $J_1,J_2$ with $[0,K-1]$ and $[K,s-1]$ before adding $d-1$. Used crossing differences also include $[d-1+s,n+s]$ and $D^e_1$, the remaining crossing ones include $D^e_2$, and the used noncrossing ones include $[1,d-2]$. The inventories preserve the literal unfinished original connector $uw$ with endpoints $(n+s+A+1,0)$ and actual difference $n+s+A+1$ in $D^e_2$.

For maximum polarity use the input $n-G$ and complement the output at $m$. The actual cuts are $n+1-c$ and $m+1-C$. By $2K=A+B+s$ the old lower and upper shifts there are $B$ and $B+s$. Both label inventories complement and exchange sides, and all actual crossing and difference inventories are preserved. The actual frontier is $m$ at $w$ and the literal connector endpoints become $(m-(n+s+A+1),m)=(B-1,m)$.

In any finite sequence of individually admitted blocks, each uses its actual incoming named graph, cut, frontier and spectrum, and its own $z_1,z_2$ and target size. Each output reaches the same phase with an extreme frontier. Subsequent placements preserve the evolving cut sides of all earlier values. From any completed cut $C_i$, if $U_i,V_i$ sum the actual later lower shifts and gap sizes, then $x\mapsto x+U_i+V_i\mathbf1_{x\ge C_i}$ gives the exact final label. Each earlier crossing weight gains $V_i$ and noncrossing weights stay fixed. This lifts both inventories and both literal connector endpoints. The remaining values at an earlier boundary in the final alphabet also include the later fresh values, disjoint by the exact palettes at each insertion. The argument is an induction on the admitted actual sequence and works when both direct-leaf counts change. The finite indexed choices, bounded imbalances, permutations and growth schedule, followed by finite backward sums, give terminating immutable final-alphabet realization on the original named graph.

## 8. Scope and acceptance

The slot substitution, equality at zero-quota first slots and sparse upper matching supply the stated topology generalization symbolically, with no scientific search, solver allocation, original checker, campaign or historical replay. The necessary graph conditions have the declared same-phase scope and the constructed quota class is sufficient. General H1 feasibility, independent initialization and arbitrary decomposition remain separate.

D187 is Director accepted within its exact written scope at checkpoint 9761e85502d9013b70997c5bc900d358e189aff4, including its five symbolic controls and 74→126→180 symbolic composition. Its domain and the accepted D186 and earlier domains are retained. D174's historical one completed pair and two numerical arms with 3,518 unentered originals remain separate from D177's accepted symbolic projection of 93, of which 92 were historically unentered. The custody receipt and the two independent reviews record the verified identities and symbolic control status.
