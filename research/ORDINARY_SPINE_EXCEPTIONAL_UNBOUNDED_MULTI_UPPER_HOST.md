# D183 — Unbounded multi-host exterior and independent upper-host growth

Task **LCL-ORDINARY-SPINE-EXCEPTIONAL-UNBOUNDED-MULTI-UPPER-HOST-001**.

**PROVED WITHIN EXACT WRITTEN SCOPE / PENDING DIRECTOR REVIEW.** Take an even number $\nu=2+2\ell$ of actual second centers with $\ell\ge1$. Take $g\ge0$, $e=g\bmod 2$, and odd $r\ge2g+6+e$. Exactly $2g$ of the $r$ first quotas are positive odd integers and the rest are positive even integers. Reserve distinct actual even hosts of quota at least four and at least $\nu$. In the admitted named D157 $S_{-1}$ arrangement with no first direct leaf, the sole second direct leaf exterior, and independently supplied prefix with $n\ge2K$ for the full target, the exterior and allocation below supply H1 in every physical order with selectable numerical roles in the following domain. At the shifted roles let $p_2$ be odd and positive, $p_{\nu-1}$ even and at least four, and all other $p_\rho$ positive even. At the unshifted role Q let $p_0$ be odd. Set
$$
p_2^{(0)}=1,\qquad p_{\nu-1}^{(0)}=4,\qquad p_\rho^{(0)}=0\ \ (\rho\notin\{2,\nu-1\},\ 2\le\rho\le\nu).
$$
The sufficient Q condition is $p_0\ge r-2+\sum_{\rho=2}^{\nu}(\rho-1)(p_\rho-p_\rho^{(0)})$. The shifted capacities are independently parameterized subject to that Q supply. This is a positive construction and a reusable folded growth rule. General H1 feasibility within the arrangement requires the graph threshold $R\ge r+3$, where $R=\sum_\rho p_\rho$ including Q. The Q condition is specific to this supplier.

## 1. Original graph counts, terminal balance and necessary conditions

All structural parameters and labels are exact integers, excluding booleans. Intervals are inclusive and an inverted interval is empty. Use the named independent [D157 input](ORDINARY_SPINE_ALTERNATING_EXCEPTIONAL_SPECTRUM.md#1-interface-and-exact-inventory-rule) with $n=2c+2$ edges. Its actual extreme frontier $v$ ends the witnessing spine and is oriented by $G(v)=0$. The cut $c$ includes equality on its upper side. With $d=c+2$ its crossing differences are $[d-1,n]$ and noncrossing differences $[1,d-2]$. Append the original spine vertices $u,w$. The fresh count includes the two spine vertices, $r+\nu$ centers, the actual direct leaf and all $F+R$ terminals. Each new vertex contributes its actual parent edge. Thus
$$
2K=F+r+\nu+R+3,\qquad m=n+2K,\qquad n\ge2K.
$$
Here $F$ is the full first total. In the positive domain $F$ is even by the $2g$ odd first quotas, and $R$ is even because precisely Q and the separation-two role have odd quotas. Together with odd $r$ and even $\nu$ this gives integral $K$.

For any compatible same-phase terminal-enabled H1 placement on this topology, root the fresh graph colors at lower $v$. Lower fresh vertices are $w$, the first centers and the second terminals. Upper fresh vertices are $u$, the second centers, the direct leaf and the first terminals. The fresh counts are $N_{\rm low}=1+r+R$ and $N_{\rm high}=\nu+2+F$. The connected crossing exterior identifies its two physical label sides with the graph colors. With $e_1,e_2$ selected terminal leaves of the respective sections, its widths are $A=r+1+e_2$ and $B=\nu+2+e_1$. The exterior reduced labels include $v=A,w=0$. The unique reduced crossing weight one connects $A$ to $A+1$, and $vu$ is the sole fresh edge at $v$. Thus $u=A+1$.

Keep $vu,uw$ as reference incidences, attach every lower slot $[1,A-1]$ to $u$ and each upper slot $A+b$ for $2\le b\le B$ to $w$. The reference weights fill $[1,A+B]$. A selected first terminal at an upper slot replaces the reference weight with one smaller by $j\ge1$, the label of its actual first-center parent. A selected second terminal at a lower slot increases its reference weight by $b-1\ge1$, for actual parent $A+b$. Every other edge keeps its reference weight, including the direct edge from $w$. Equality of the reduced weight sums therefore implies $\sum_{\rm first}j=\sum_{\rm second}(b-1)$. A terminal-enabled exterior has at least one selected terminal, so both counts are positive.

For the D157 same-phase return $s=2K-A-B$, $k=K-A$, $A\le K\le A+s$ and $s\ge K$. The last inequality follows from the least old crossing weight $d-1$ gaining $s$ to reach the output crossing band starting at $d+K-1$. There are $k$ physically lower gap sources. Let $x$ count lower sources at upper hosts and $y$ upper sources at lower hosts. Those incidences are precisely the crossing gap edges. The gap weight at image $\pi$ is $d-1+\pi$ and the crossing images are $[K,s-1]$, so $x+y=s-K$. By the actual parent colors,
$$
N_{\rm low}=A+(s-k-y+x)=2(A+x),\qquad
N_{\rm high}=B+(k-x+y)=2(B+y).
$$
In particular $1+r+R\ge2(r+2)$ gives $R\ge r+3$. Both graph counts must be even for this same-phase placement. For odd $r$ and even $\nu$ this forces even $R,F$. The threshold and graph parity do not need the positive construction's reservoir or per-host quota parities.

## 2. Wider named exterior, folded alphabets and moment

Use $A=r+2,B=\nu+3$. In reduced labels take $v=A,u=A+1,w=0$. Give every actual first center a distinct label in $[2,A-1]$. At parent 3 select the first actual indexed terminal and give it $A+3$. Give Q label $A+2$ and the actual second center at separation $\rho$ label $A+2+\rho$ for $2\le\rho\le\nu$. Denote that center by $P_\rho$. At $P_2$ select its first actual indexed terminal and give it label 1. Put the actual direct leaf at $A+B$. The distinct vertices give exactly $[0,A+B]$. The crossing exterior is connected through the three spine vertices and the actual centers, with both selected leaves and the direct leaf at their actual parents. The edge $vu$ has weight one, and the first center edges give weights $[2,A-1]$. The selected first terminal gives $A$. The second section uses $A+1$ at $uw$, $A+2$ at $wQ$, $A+3$ on the selected $P_2$ terminal edge, $[A+4,A+\nu+2]$ at the shifted centers, and $A+B$ at the direct edge. These exhaust the exact reduced differences $[1,A+B]$. All actual centers are exterior.

Put $R_0=r+3$ and $R=R_0+2\lambda$. The two qualifying even hosts are distinct, so
$$
F\ge4+\nu+2(r-2g-2)+2g=2r+2+2\ell-2g,\qquad h=F/2-r-1\ge\ell-g .
$$
Substituting gives
$$
K=2r+5+h+\ell+\lambda,\quad s=3r+3+2h+2\lambda,\quad
k=K-A=r+3+h+\ell+\lambda,\quad J=s+3.
$$
The increase in $2K$ due to widening the second-center count at fixed $F,R,r$ equals the increase in $B$, so $s$ is independent of that width change. For $\lambda\ge0$, $K-(A+B)=r-2+h-\ell+\lambda\ge r-2-g>0$. In particular $s\ge K$ and $A\le K\le A+s$. The actual input size satisfies $n\ge2K$ for the final target. The oriented output cut is $C=c+K$. A gap leaf of coordinate $i$ has label $A+c+i$ and is physically lower exactly when $i<k$. The lower host of reduced label $j_0$ is smaller than any gap label, so the actual difference is $d-1+i+\delta$ with $\delta=A-1-j_0$. Subtracting the gap leaf label from the expanded upper host $n+s+A+b$ gives $d-1+s+b+1-i$. Hence the numerical image is $i+\delta$ at the lower host and $s+b+1-i$ at the upper host.

Use $L_j=j$, $H_j=J-j$. The source H row unfolds to $[k,s-1]$ and the image H row to $[K,s-1]$. Their lower folded endpoint is $J-(s-1)=4$. The L rows are their numerical complements. Thus the exact rows are
$$
\begin{array}{c|cc}
 & L & H\\
\text{sources}&[0,r+2+h+\ell+\lambda]&[4,2r+3+h-\ell+\lambda]\\
\text{images}&[0,2r+4+h+\ell+\lambda]&[4,r+1+h-\ell+\lambda].
\end{array}
$$
The lower maps keep rows with increments $+\delta,-\delta$ on L,H. Upper hosts with $b=2+\rho$ exchange rows with increments $-\rho,+\rho$ on L,H, and Q uses $\rho=0$. These follow by substitution in the actual image formulas. For any arrow in its specified source and image domains the H image is exactly the physical crossing case: either a lower L source uses an upper host or an upper H source uses a lower host. This gives the actual predicate $\pi(i)\ge K$. The four rows contain their indicated initial cells and the common starting column four for noninitial endpoints in the verified bounds.

In the folded index moment the L row adds the $A$ indices $[k,K-1]$ and the H row removes $[J-K+1,J-k]$, also of length $A$. The latter begins at $k+4-B$, from $J=s+3$ and $s=2K-A-B$. Subtraction of the interval sums gives $A(B-4)=A(\nu-1)$. At lower hosts the increments are $\pm\delta_i$, and at the shifted upper hosts $\pm\rho$. Modulo two the signs disappear, so any allocation on this exterior satisfies
$$
A(\nu-1)\equiv
\sum_i\delta_i\alpha_i-(r-2)
+\sum_{\rho=2}^{\nu}\rho\big(p_\rho-\mathbf1_{\rho=2}\big)\pmod2 .
$$
Here $\alpha_i$ is the full first quota and the selected first terminal has shift $r-2$ at label 3. The assigned first weighted sum is even: a three-host packet pairs odd quotas at shifts $\eta,\eta+2$, and a four-host packet has shifts summing to $4\eta+6$ at its four odd quotas. Other first quotas are even. At the baseline and final targets the residual shifted-host quotas are all even, so the upper contribution is even. The odd left side agrees with the odd selected first subtraction. Q and the exterior direct leaf have no folded moment contribution. This parity check supplements the exact construction.

## 3. Signed regular strip and the reusable anchor

Choose distinct qualifying actual first hosts for neutral label $A-1$ and the selected first parent at 3. Choose the lexicographically first eligible pair of original indices. Choose three more even hosts for the tail, one further even host for shift one, and an additional even host for the middle of the three-host packet if $e=1$. Such choices exist because $r-2g\ge6+e$. The numerical first shifts are $[0,r-1]$, with regular positive shifts $[1,r-5]$ and tail shifts $r-d_0$ at deficits $d_0\in\{1,2,3,4\}$. The actual first parent for shift $\delta$ is at reduced label $A-1-\delta$. Deficit two therefore belongs to the designated quota-at-least-$\nu$ host. All roles keep their original names and parent incidences.

Give the reserved shift-one host its ordinary pairs. Assign $\lfloor g/2\rfloor$ four-odd-host packets and when $e=1$ one three-host packet to consecutive shift groups starting at shift two, using odd hosts in original index order. The packets use $2g$ odd centers and $e$ even centers across $2g+e$ shifts. There is room since $r-5\ge1+2g+e$. Assign remaining regular roles to the remaining even hosts by original index. At $g=0$ the packet list is empty, and ordinary even pairs fill all positive regular shifts. Define
$$
h_N=(\alpha_{\rm neutral}-4)/2,\quad
h_R=\frac{\sum_{\rm regular}\alpha_i-2(r-5)}2,\quad
h_T=\sum_{\rm tail}(\alpha_i-2)/2,\quad h_*=h_N+h_R .
$$
The exact quota partition gives $h=h_*+h_T$. The regular sum contains all $2g$ odd quotas, so $h_R$ is integral, with $h_R\ge-g$. The other two terms are nonnegative. In particular $h_*\ge-g$ and $h_T\ge\ell$.

Work at $\lambda=0$. The first four neutral L arrows are $L_j\to L_j$ for $0\le j\le3$. A shared position $i$ uses one L source and one H image. An ordinary pair of shift $\delta$ there puts $L_i\to L_{i+\delta}$ and $H_{i+\delta}\to H_i$ at the same actual first parent. Its intermediate reservations in the L-image and H-source rows are identical. Use $h_N$ neutral pairs at positions $[4,3+h_N]$. Then process positive regular groups by increasing shifts at successive shared positions. Each ordinary even host uses half its quota in pairs. For the [D182 packets](ORDINARY_SPINE_EXCEPTIONAL_PARITY_NEUTRAL_PACKETS.md#3-two-independently-expandable-parity-neutral-packets), the central three-host lists $(2,0)$ and $(1,1)$ relative to the least shift reserve the same two columns in either intermediate row, and occupy capacities $(1,2,1)$. The four-host lists $(3,0)$ and $(1,2)$ have the same property and capacities $(1,1,1,1)$. Their expansions add only ordinary pairs at their designated shifts before or after the two shared central positions. The two identical reservation sets remain injective, and their complementary columns require only H-to-L Q identities. These proofs depend on neither the number of shifted hosts nor their separations. Each packet uses positive shared length equal to half the sum of its actual quotas. Its full footprint, including local complementary Q identities, is contained between first position plus least shift and last position plus greatest shift. The same bound holds at each ordinary pair or group of pairs.

The total regular shared length is $r-5+h_R$, and its positions are $[4+h_N,r-2+h_*]$. Signed $h_R$ changes this sum while leaving every constituent group length positive. Shared positions and the shift groups increase strictly across groups. Therefore their intermediate footprints are disjoint and confined to $[4,2r-7+h_*]$. The extra neutral columns precede those of the regular groups, and $3+h_N\le2r-7+h_*$ by $h_R\ge-g$ and the lower bound on $r$. The first L source after the four fixed arrows is $L_4$. If $h_N>0$ it belongs to a neutral pair and has image $L_4$. Otherwise it belongs to the reserved shift-one host and has image $L_5$. This gives the actual anchor $L_4\to L_{4+\delta}$ with $\delta\in\{0,1\}$ in every case. The next section checks the upper windows of the regular footprints and supplies the tail.

## 4. Wider tail and baseline quotas

Use $t=h_T$, $N=t+2$, $D_*=2r+h_*$. At deficit $d_0$ write the actual even quota as $2+2u_{d_0}$. The chosen host at deficit two gives $u_2\ge\ell$. Among the three other actual hosts put a smallest quota at deficit one, with ties by original index, and assign deficits three and four by index among the other two. Thus $u_3\ge u_1$. The selected first exterior terminal is at the actual deficit-two parent.

The regular endpoint of §3 leaves L-source positions and H-image positions $r+h_*+x$ with local offsets $[-1,N+\ell]$ and $[-1,N-1-\ell]$, respectively. Indeed their right endpoints are $r+2+h+\ell$ and $r+1+h-\ell$, and both start just after $r-2+h_*$. The earlier shared H positions are legal because $r-2+h_*\le r+1+h-\ell$ by $t\ge\ell$. The intermediate column for offset $x$ and shift $r-d_0$ is $D_*+x-d_0$, both for a reserved L image and for a reserved H source. We use the terminal portions of those rows, expressed locally relative to $D_*$:
$$
\text{H sources }[-5,N+1-\ell],\qquad
\text{L images }[-5,N+2+\ell].
$$
Their right endpoints are the actual baseline row endpoints $2r+3+h-\ell$ and $2r+4+h+\ell$. Their common left endpoint $D_*-5$ is at least $2r-g-5\ge4$ and strictly above the earlier maximum $D_*-7$. All earlier intermediate footprints therefore lie inside both rows and are disjoint from the local tail. All used columns at the tail start at least at $-5$, since no deficit is larger than four and no position lower than $-1$.

First use the [D180 local two-shift tail counts](ORDINARY_SPINE_EXCEPTIONAL_ODD_SECOND_QUOTA_SUPPLIER.md#3-actual-i-a-exterior-and-the-odd-baseline-tail) in a different shared order. At positions starting at $-1$ put $1+u_4$ ordinary pairs of deficit four, then $u_3-u_1$ pairs of deficit three, then $u_1+1$ two-position groups $(1,3)$ in each row, then $u_2$ ordinary pairs of deficit two. At the final L-only position use deficit two once more. Every ordinary pair at $x$ reserves a common column $x-d_0$. The first ordinary columns strictly increase. If the groups start at $j_0$, the preceding pair columns are at most $j_0-3$. Each group on positions $x,x+1$ has columns $x-1,x-2$, exactly its positions translated by $-2$. The groups and following deficit-two pairs jointly reserve their full position interval translated by $-2$ in each row, disjoint from the preceding pair columns. All pair counts are nonnegative. There are
$$
(1+u_4)+(u_3-u_1)+2(u_1+1)+u_2=3+t
$$
shared positions through $N-1$, and the final L-only position is $N$. The groups supply all $2+2u_1$ uses at deficit one and the same count at three, and the early pairs supply the rest of three and all of four. At two the pairs, last L-only use and selected exterior terminal consume $2+2u_2$. This proves the precise capacities and injective intermediate reservations of the reordered lists before widening.

Keep the L list through $N$. Transfer the last $\ell$ H-image uses, at positions $[N-\ell,N-1]$, to new L positions $[N+1,N+\ell]$ at their same deficit-two parent. All transferred positions belong to the trailing deficit-two pairs because $u_2\ge\ell$. This changes only the allocation of that parent's gap leaves. The new positions exactly fill both required local position windows. The remaining H reservations $Y$ are the common reservations from the retained shared positions. Their maximum is at most $N-\ell-3$: the terminal groups and deficit-two pairs have effective deficit two, and earlier ordinary pairs reserve columns at least three below their own positions. Truncating H removes the distinct columns $[N-\ell-2,N-3]$ from its old reservation set. Those columns remain on L, which also retains its last L-only image $N-2$ and adds $[N-1,N+\ell-2]$ from the transferred uses. Hence the L reservations are exactly
$$
X'=Y\sqcup[N-\ell-2,N+\ell-2].
$$
Their maximum is at most $N+2+\ell$, and the H reservations lie inside their required window with its smaller endpoint bound. The quota counts remain exact at all first hosts, and both intermediate reservation sets are injective. In particular the last retained shared position exists since $t\ge\ell$ makes $N-1-\ell\ge1$.

Below $N-\ell-2$ the remaining H sources and L images in the tail coincide and use Q identity. Above those common cells the two exact residual suffixes are
$$
[N-\ell-2,N-\ell+1]\quad\text{and}\quad[N+\ell-1,N+\ell+2].
$$
Both have four entries. The translation between them is $2\ell+1=\nu-1$, exactly the available H-to-L map at $P_{\nu-1}$. These arrows and the common identities exhaust the tail. The argument includes $\ell=1$ and $u_2=\ell$ without any empty-position exceptions. Regular and neutral intermediate reservations coincide, and the free common columns outside all earlier footprints and below the tail use Q identities as well. The initial L images $[0,3]$ are already reserved and are below the H-source window. Thus the regular, initial and tail partitions give exact baseline source and image bijections.

At baseline every L source uses a first host and every H image comes from a first host. The H-source row has $2r+h-\ell$ cells and the H-image row $r-2+h-\ell$, leaving exactly $r+2$ H-to-L upper uses. Exactly four of these are at $P_{\nu-1}$ and $r-2$ at Q. All other upper gap uses are zero. Thus, including the one selected terminal at $P_2$, the full assigned counts are $p_0^{(0)}=r-2$, $p_2^{(0)}=1$, $p_{\nu-1}^{(0)}=4$, and zero elsewhere, with sum $R_0$. These are intermediate counts in an allocation, with all actual target centers present in the exterior and the required target terminals accounted for by the growth. The baseline crossing counts are $x=0$ and $y=r-2+h-\ell$. They also give $x+y=s-K$ at $\lambda=0$.

## 5. Exact growth at a shifted upper host

Extend the [D179 folded strip](ORDINARY_SPINE_EXCEPTIONAL_INDEPENDENT_SECOND_QUOTA_GROWTH.md#4-balanced-growth-in-i-a) as follows. The premises are an exact four-row bijection at the current $\lambda$, the fixed initial four neutral arrows, the anchor $L_4\to L_{4+\delta}$ at its actual first parent with $\delta\in\{0,1\}$, and an actual host $P_\rho$ of separation $\rho\ge2$. For integer $b\ge1$ let $u_0=\rho b$. Increase $\lambda$ by $u_0$. Each upper row endpoint increases by $u_0$, with lower endpoints fixed, and $J$ increases by $2u_0$. Keep the four initial neutral arrows fixed and translate every other folded endpoint by $u_0$. The upper and lower folded maps preserve all existing displacements and retain the parent. They leave precisely $S=[4,3+u_0]$ open in each row. Move the translated anchor from $L_{4+u_0}\to L_{4+u_0+\delta}$ back to $L_4\to L_{4+\delta}$ at the same first parent. The new endpoints are in $S$ and the two freed old endpoints are the only free endpoints outside $S$.

In the L-source direction the free L sources are $(S\setminus\{4\})\sqcup\{4+u_0\}$ and the free H images are $S$. For $1\le j\le b$ use
$$
L_{4+\rho j}\longrightarrow H_{4+\rho(j-1)}
$$
at $P_\rho$. The last source is the freed old source and all other sources lie in $S$ away from 4. Every H image lies in $S$. These assignments occupy the former excess and missing endpoints and all intermediate columns of that residue class. They leave exactly the same $u_0-b$ column indices in both rows, namely $S$ minus $\{4+\rho j:0\le j<b\}$, for Q identities.

In the H-source direction the free H sources are $S$ and the free L images are $(S\setminus\{4+\delta\})\sqcup\{4+u_0+\delta\}$. For $0\le j<b$ use
$$
H_{4+\delta+\rho j}\longrightarrow L_{4+\delta+\rho(j+1)}
$$
at $P_\rho$. The last source $4+\delta+u_0-\rho$ is at most $3+u_0$ since $\delta\le1$ and $\rho\ge2$. The first source is at least 4. The last image is the freed old image and the previous images are in $S$ above the omitted $4+\delta$. Removing these shifted arrows leaves precisely $S$ minus $\{4+\delta+\rho j:0\le j<b\}$ in both alphabets, of size $u_0-b$. Use Q by identity. Each direction is bijective on its own free cells and the two directions have disjoint rows. No endpoint collides with an unchanged translated arrow. The first direction crosses and the second does not. The moved anchor keeps its row and actual first host. These are the exact increments
$$
\Delta p_\rho=2b,\qquad \Delta p_0=2(u_0-b)=2(\rho-1)b .
$$
All other counts and selected incidences are preserved. With $b=0$ use the identity operation. Each operation ends with the same four neutral arrows and the anchor at its original folded coordinates. In consequence the induction applies to arbitrarily many distinct actual shifted hosts in a finite target, with every noninitial endpoint still at least four at each stage.

After the shifted operations, Q-only growth for $a\ge0$ translates all noninitial folded endpoints by $a$. This increases each upper row endpoint by $a$. Fill the common free strip $[4,3+a]$ in both directions by Q identity across rows. This uses exactly $2a$ new leaves at Q. It moves the anchor by $a$, which is why it is applied after the shifted operations. All arrows use their correct physical hosts, row domains and crossing predicates from §2. No auxiliary original graph or labeled prefix is required for any stage.

## 6. Actual target quotas and numerical role selection

Suppose the actual quotas admit a role assignment in the stated positive domain. Set $b_\rho=(p_\rho-p_\rho^{(0)})/2$. Its integrality follows from the role parities, and the role minima give $b_\rho\ge0$. The reservoir condition and the oddness of both $p_0$ and $r-2$ give the nonnegative integer
$$
a=\frac{p_0-(r-2)-2\sum_{\rho=2}^{\nu}(\rho-1)b_\rho}{2}.
$$
Use the $b_\rho$ strips in increasing separation order and then the Q-only strip. The exact increments restore every actual target capacity at its own center. Summing the counts, a shifted-host step adds $2\rho b_\rho$ leaves to the second total, and the Q-only step adds $2a$. Thus
$$
\lambda=a+\sum_{\rho=2}^{\nu}\rho b_\rho,\qquad R=R_0+2\lambda.
$$
This agrees with the target row sizes. At each stage the first-host L and H counts remain unchanged, because only a single L-to-L first arrow is moved. For each new common column precisely one new L source goes to an upper host, by the free-set counts in §5. Hence at the end $x=\lambda$ and $y=r-2+h-\ell$. This agrees with $x+y=s-K$ and the graph equations in §1. Every physical branch order is admitted because the roles are assignments to centers by quota and index, with all original parent incidences kept.

For a deterministic choice from an unordered numerical assignment on the actual indexed centers, the quota inequalities can also be checked directly. There must be exactly two odd second quotas, for Q and $P_2$. Try their two possible role orders and each eligible even center of quota at least four for the $P_{\nu-1}$ role, in original index order. For each fixed set of these three roles, put the remaining even quotas in descending quota order at the remaining increasing separation indices, with index ties fixed. This minimizes the reservoir cost for the fixed three roles: exchanging an inverted pair with weights $\rho_1-1<\rho_2-1$ and capacities $p_1<p_2$ reduces the cost by $(\rho_2-\rho_1)(p_2-p_1)$. The subtracted baseline terms are fixed. Hence accepting the first such assignment meeting the bound finds a compatible role assignment whenever one exists for this supplier. This is a finite arithmetic quota selection, separate from labeling feasibility in other domains. The resulting sufficient class is nonempty at every even $\nu\ge4$: for each admitted first inventory choose the minimum positive shifted quotas from the displayed conditions and choose Q at the odd bound or above it. All statements retain the independently supplied input and full-size premises.

## 7. Named realization, inventories and immutable return

The allocation uses the actual target names throughout. Select the first indexed terminal at the first parent of label 3 and at $P_2$ for the exterior. Assign each baseline arrow to a named leaf at its actual parent in fixed row and index order, taking only the needed number of actual terminal indices at each second center. At first parents the baseline uses every nonexterior terminal. At second parents it never requires more indices than the actual target offers, including zero residual uses at $P_2$ when its full quota is one. All moved or translated arrows keep their leaf identities and actual parent incidences. At each growth step give the new arrows in a fixed order to available actual terminal indices at Q and the designated shifted host. The counts in §6 make the final assignments exact. The actual direct leaf stays at $w$ in the exterior. The construction computes its intermediate normalized allocation from the original quotas and named incidences.

For each actual first host $i$ let $S_i^0$ be its baseline numeric gap source set, obtained by unfolding the packet, ordinary or tail arrows at $J_0=3r+6+2h$. Its baseline image set equals $S_i^0+\delta_i$ by numerical subtraction. Put $I_0=\bigsqcup_i S_i^0$ and $M_0=\bigsqcup_i(S_i^0+\delta_i)$. The two unions are disjoint by the row bijections. Both contain $E_0=[0,3]$. Define $T_\lambda(D)=E_0\sqcup((D\setminus E_0)+\lambda)$ for a numeric baseline set containing $E_0$. Every noninitial arrow that is neither moved back as the anchor nor newly introduced gains folded index $\lambda$ in both alphabets, and its H coordinate unfolds at $J_0+2\lambda$. Thus an old coordinate $J_0-j$ becomes $(J_0+2\lambda)-(j+\lambda)=J_0-j+\lambda$. The numeric L coordinate also gains $\lambda$ at such an endpoint.

If every $b_\rho$ vanishes, the exact first-section coordinate sets after Q-only growth are $I=T_\lambda(I_0)$ and $J_1=T_\lambda(M_0)$. If any shifted growth occurs, every shifted step retains the anchor at folded $L_4\to L_{4+\delta}$ and the last Q-only strip translates it by $a$. Hence
$$
I=(T_\lambda(I_0)\setminus\{4+\lambda\})\sqcup\{4+a\},\qquad
J_1=(T_\lambda(M_0)\setminus\{4+\delta+\lambda\})\sqcup\{4+\delta+a\}.
$$
The anchor cells exist and are disjoint from all retained first cells by §5's exact partition. The final first image sets remain the union of each actual first-host numeric source set translated by its own shift. With $I'=[0,s-1]\setminus I$ and $J_2=[0,s-1]\setminus J_1$ these are the exact used and remaining gap resources at the first-section boundary, including all earlier H intervals unfolded at the true $J$. The crosses at that boundary and on the remaining edges are determined by the actual row predicates in §2.

For the oriented final return, translate old labels by $A$ below $c$ and $A+s$ at or above $c$. The old endpoint bounds $A+c-1<C\le A+c+s$ preserve the old cut sides. Thus old crossing differences gain $s$ and noncrossing differences stay fixed. Use the gap label $A+c+i$ for each numeric source $i$. Expand upper reduced exterior labels by $n+s$ and keep the lower reduced labels. The common frontier $v$ has label $A$ in both placements. All lower exterior endpoints are at most $A<C$ and upper exterior endpoints are at least $n+s+A+1>C$. All exterior differences gain $n+s$. The old and fresh palettes are exactly
$$
\begin{array}{ll}
L_{\rm old}=[A,A+c-1]\sqcup[A+c+s,n+s+A],&
L_{\rm fresh}=[0,A-1]\sqcup[A+c,A+c+s-1]\sqcup[n+s+A+1,m],\\
D_{\rm old}=[1,d-2]\sqcup[d-1+s,n+s],&
D_{\rm fresh}=[d-1,d+s-2]\sqcup[n+s+1,m].
\end{array}
$$
They give disjoint complete alphabets $[0,m]$ and $[1,m]$ using $m=n+s+A+B$. This also counts the shared $v$ just once. The gap resource bijections and exact exterior spectra place every indicated fresh label and every actual fresh edge difference once. By the physical crossing predicates the gap crossings give $[d+K-1,d+s-2]$ and the noncrossings $[d-1,d+K-2]$. Taking the unions with the old and exterior bands gives the exact final crossing spectrum $[d+K-1,m]$ and noncrossing spectrum $[1,d+K-2]$. The actual frontier is $w=0$ and $m=2C+2$. This returns $S_{-1}$ along the original extended witnessing spine.

At the boundary after the first new section, the reduced first fresh exterior vertices are the first centers $[2,A-1]$, $u$, and the selected first terminal at $A+3$ attached to the center at 3. The remaining exterior vertices are $w$, the selected second terminal, Q, all the shifted centers, and the direct leaf. Thus in the actual alphabet the two fresh exterior label sets are
$$
E_1=[2,A-1]\sqcup\{n+s+A+1,n+s+A+3\},\qquad
E_2=\{0,1,n+s+A+2\}\sqcup[n+s+A+4,m].
$$
The matching exterior weight sets are $D^e_1=n+s+[1,A]$ and $D^e_2=n+s+[A+1,A+B]$. By the named incidence groups just proved, the two inventories are
$$
\begin{array}{ll}
\text{used labels}&L_{\rm old}\sqcup E_1\sqcup(A+c+I),\\
\text{remaining labels}&E_2\sqcup(A+c+I'),\\
\text{used differences}&D_{\rm old}\sqcup D^e_1\sqcup(d-1+J_1),\\
\text{remaining differences}&D^e_2\sqcup(d-1+J_2).
\end{array}
$$
For each of $I,I'$ the lower gap part is its intersection with $[0,k-1]$, the upper part its intersection with $[k,s-1]$, before adding $A+c$. The old label sides are the two old bands and the exterior label sides are the original reduced sides. In each of $J_1,J_2$, the noncrossing and crossing parts are its intersections with $[0,K-1]$ and $[K,s-1]$ before adding $d-1$. The used crossing set also includes $[d-1+s,n+s]$ and $D^e_1$, the remaining crossing set includes $D^e_2$, and the used noncrossing set includes $[1,d-2]$. These are the exact side and crossing partitions. The literal unfinished connector is the original edge $uw$ with endpoints $(n+s+A+1,0)$ and difference $n+s+A+1$ in $D^e_2$.

For actual maximum polarity use input $n-G$ and complement the output about $m$. The cuts are $n+1-c$ and $m+1-C$. Since $2K=A+B+s$, the actual lower and upper shifts become $B$ and $B+s$ in place of $A$ and $A+s$. Both exact label inventories complement and switch cut sides. Absolute differences and crossing statuses are unchanged. The final actual frontier is $m$ at $w$. The connector endpoints become $(m-(n+s+A+1),m)=(B-1,m)$, with the same difference as in minimum polarity.

For any finite sequence of individually admitted blocks, each uses its actual incoming graph, stably named ports, exact phase and cut spectra, and its own size and topology premises. Every subsequent placement preserves the evolving cut sides of the old alphabet. At a completed cut $C_i$, with $T_i$ the sum of later actual lower shifts and $S_i$ the sum of later gap widths, the final label on its alphabet is $x\mapsto x+T_i+S_i\mathbf1_{x\ge C_i}$. The final crossing weights gain $S_i$ and noncrossing weights remain fixed. This transports both exact intermediate inventories and the literal connector's endpoints and weight. The remaining sets in the final alphabet also include all later fresh vertices and edges, which are disjoint from the lifted old alphabets at each insertion by the palettes. Induction gives the admitted returns. Finite role selection, the finite packet, tail and growth strips, direct scans of original incidences and finite backward sums give the final labels for immutable emission. The independent initializer and admission requirements retain their earlier scopes.

## 8. Scope and accepted controls

This exterior takes an unbounded number of actual upper hosts. Its four shifted baseline arrows at $P_{\nu-1}$ come from the widened tail, and its quota growth uses the same actual anchor for each shifted host. The construction resolves the stated sufficient domain symbolically with zero scientific search, solver allocations, new campaigns or historical replays. Outside the stated positive domain the necessary floor and graph parities still have their stated scope, while general exterior and quota feasibility remain separate. The Q inequality is a sufficient capacity for this construction. The proof gives neither universal initialization nor arbitrary decomposition.

D182 is Director accepted at checkpoint 76354f6a0de4437531e85d642be707b1845372ce within its exact written scope. It supplies the parity-neutral regular rules used here. The D180 tail arithmetic and D179 two-host growth are local controls for the widened constructions, and earlier theorem scopes remain unchanged. D174 historically completed one pair and two numerical arms with 3,518 unentered originals. The separately accepted D177 projection includes 93 original records, of which 92 were historically unentered. All prior evidence and open obligations are retained.
