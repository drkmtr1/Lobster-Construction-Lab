# D181 — Mixed first-quota parity packets on width-five exceptional exteriors

Task **LCL-ORDINARY-SPINE-EXCEPTIONAL-MIXED-FIRST-QUOTA-PARITY-001**.

**PROVED WITHIN EXACT WRITTEN SCOPE / PENDING DIRECTOR REVIEW.** Take integers $g\ge1$ and odd $r\ge6g+17$. The $r$ actual first centers have exactly $2g$ odd quotas at least three and otherwise positive even quotas, including an even quota at least four. There is no first direct leaf. Take two actual second centers with full quotas $p,q\ge g+3$ of the same parity, and the sole actual second direct leaf in the exterior. With an independently supplied admissible named D157 $S_{-1}$ prefix of size $n\ge2K$ for the full target and selectable numerical roles in every actual physical order, terminal-enabled H1 in the declared D157 arrangement is feasible exactly when $R=p+q\ge r+3$.

## 1. Exact topology and necessary threshold

All structural quantities and labels are exact integers. Intervals are inclusive and an inverted interval is empty. In the [D157 arrangement](ORDINARY_SPINE_ALTERNATING_EXCEPTIONAL_SPECTRUM.md#1-interface-and-exact-inventory-rule), the independently supplied named prefix has $n=2c+2$ edges, a witnessing spine ending at the actual frontier $v$, and oriented graceful labeling $G(v)=0$. The lower side is below $c$. With $d=c+2$ its crossing weights are $[d-1,n]$ and its noncrossing weights $[1,d-2]$. Append the actual spine vertices $u,w$. There are $r+2$ new center edges, two new spine edges, one actual direct edge, and $F+R$ terminal edges, where $F=\sum_i\alpha_i$ is the first total. Exactly $2g$ odd summands make $F$ even and the prescribed same second parity makes $R$ even. Thus
$$
2K=F+r+R+5,\qquad m=n+2K,\qquad n\ge2K.
$$

In any compatible terminal-enabled H1 candidate, color the original extension with $v$ lower. Its fresh lower graph class consists of $w$, the $r$ first centers and $R$ second terminals. Its upper class consists of $u$, the two second centers, the direct leaf and $F$ first terminals. The connected crossing exterior gives these colors to its physical sides. If $e_1,e_2$ count selected exterior terminals, the reduced widths are $A=r+1+e_2$ and $B=4+e_1$. In the D157 reduced exterior $v=A,w=0$. The unique crossing weight one joins $A$ and $A+1$. Since $vu$ is the only new edge at $v$, $u=A+1$.

For terminal balance, keep $vu,uw$ and use reference edges from lower slots $[1,A-1]$ to $u$ and upper slots $A+b$ with $2\le b\le B$ to $w$. Their reduced weights partition $[1,A+B]$. At a selected first terminal, the true edge weight is less than the reference by its lower parent's label $j\ge1$. At a selected second terminal, the true edge weight exceeds the reference by $b-1\ge1$ for its parent $A+b$. The actual exterior direct edge at $w$ has the reference weight. Equality of the sums gives $\sum_{\rm first}j=\sum_{\rm second}(b-1)$. Terminal-enabled therefore implies $e_1,e_2\ge1$.

Write $s=2K-A-B$ and $k=K-A$. The admitted D157 placement has $A\le K\le A+s$ and $s\ge K$. In particular its least old crossing weight $d-1$ gains $s$ and must reach the output crossing band starting at $d+K-1$. The gap has $k$ physically lower sources and $s-K$ crossing image coordinates, since a gap image $\pi$ contributes weight $d-1+\pi$ and crosses exactly at $\pi\ge K$ in a compatible return. If $x$ counts lower sources at upper hosts and $y$ upper sources at lower hosts, then $x+y=s-K$. The gap leaves of lower graph color number $s-k-y+x$, including lower sources at upper hosts. Adding the exterior gives
$$
1+r+R=A+s-k-y+x=2(A+x)\ge2(r+2).
$$
The upper graph color comprises the $B$ exterior upper vertices and the $k-x+y$ gap leaves at lower hosts. Thus $4+F=B+k-x+y=2(B+y)$, using $x+y=s-K$ and $s=2K-A-B$.
Thus $R\ge r+3$. This argument also applies with the present mixed quotas to any compatible exterior in the declared terminal-enabled H1 arrangement. It uses only the counts and actual incidences. The resulting exclusion concerns this arrangement, leaving terminal-free and ordinary gracefulness questions outside it.

## 2. Independent I-a exterior, rows and moment

For the supplier use I-a with $A=r+2,B=5$, exterior $v=A,u=A+1,w=0$, first centers $[2,A-1]$, and $Q=A+2,P=A+4$. Select the first actual terminal at the first parent of label 3 and give it reduced label $A+3$. Select the first actual terminal at $P$ and give it 1. Give the actual direct leaf of $w$ reduced label $A+5$. The neutral host at $A-1$ has even quota at least four. The assignment of all actual centers to these distinct labels is specified below. Every named exterior edge crosses the reduced cut. In the first section $vu$ and the $u$-center edges give $[1,A-1]$, and the terminal edge at 3 gives $A$. The second weights in order are $A+1$ on $uw$, $A+2$ on $wQ$, $A+3$ from $P$ to its selected terminal, $A+4$ on $wP$, and $A+5$ on the direct edge. The connected named exterior has exactly labels $[0,A+5]$ and differences $[1,A+5]$.

Set $R_0=r+3$, $h=F/2-r-1\ge0$, $R=R_0+2\lambda$. Then
$$
K=2r+5+h+\lambda,\qquad s=3r+3+2h+2\lambda,\qquad k=r+3+h+\lambda,\qquad J=s+3.
$$
The inequality $K-(A+B)=r-2+h+\lambda\ge0$ gives $s\ge K$, and $A\le K\le A+s$. Use cut $C=c+K$. Gap coordinate $i$ gives label $A+c+i$ and is lower iff $i<k$. The upper expanded exterior label is $n+s+A+b$. Subtracting the gap label from it, or subtracting the lower host label $j_0$ from the gap label, gives weight $d-1+\pi(i)$ with
$$
\pi_{\rm lower}(i)=i+\delta,\quad \delta=A-1-j_0,\qquad
\pi_{\rm upper}(i)=s+b+1-i.
$$
In each case the host size relative to the gap gives the displayed sign of the absolute difference. The exact folded rows, with $L_j=j$ and $H_j=J-j$, are
$$
\begin{array}{c|cc}
 & L & H\\
\text{sources} & [0,r+2+h+\lambda] & [4,2r+3+h+\lambda]\\
\text{images} & [0,2r+4+h+\lambda] & [4,r+1+h+\lambda].
\end{array}
$$
Source H unfolds to $[k,s-1]$ and image H to $[K,s-1]$. Each alphabet unfolds bijectively to $[0,s-1]$. The lower maps keep rows with shifts $+\delta,-\delta$ in L,H. Q swaps rows with the same index; P swaps with shifts $-2,+2$ on L,H sources. For lower hosts the H source crosses; for upper hosts the L source crosses. Thus on every arrow within its stated row windows the H image is exactly the physical crossing case.

In the index sum, the L images add $[k,k+A-1]$ and the H images remove $[k-1,k+A-2]$ relative to the source rows. The difference is $A=r+2$. Modulo two an actual residual quota $\alpha'_i$ at first shift $\delta_i$ contributes $\delta_i\alpha'_i$. Q contributes zero; P contributes $2(p-1)$ modulo two and the direct leaf has no gap use. Consequently
$$
r+2\equiv\sum_i\delta_i\alpha'_i+2(p-1)
=\sum_i\delta_i\alpha_i-(r-2)+2(p-1)\pmod2 .
$$
Here the subtracted $r-2$ is the shift of the selected first parent at 3. Thus $\sum_i\delta_i\alpha_i\equiv0\pmod2$ on I-a. Two odd quotas at shifts $\eta,\eta+2$ supply even combined parity, a necessary moment which the actual construction below augments with exact row bijections.

## 3. An independently expandable mixed packet

At consecutive shifts $\eta,\eta+1,\eta+2$ take full capacities $(3+2a,2+2b,3+2c)$ for nonnegative integers $a,b,c$. Here $c$ is a local count. For the central minimal packet at consecutive shared positions $j,\ldots,j+3$, put $z=j+\eta$. Choose L-source relative shifts $(0,2,0,1)$ and H-image relative shifts $(0,1,2,2)$. A chosen relative shift $e$ sends $L_{j+i}$ to $L_{j+i+\eta+e}$ or uses $H_{j+i+\eta+e}$ for $H_{j+i}$. The actual L-image reservation columns are $z+(0,3,2,4)$ in position order, and the actual H-source reservations are $z+(0,2,4,5)$. Both lists are injective in their own alphabets. The host counts by increasing shift are $(2,1,1)$ in L and $(1,1,2)$ in H. In $[z,z+5]$ the free H source indices are $z+1,z+3$ and the free L image indices $z+1,z+5$. The only legal completion uses $H_{z+1}\to L_{z+1}$ at Q and $H_{z+3}\to L_{z+5}$ at P. The two first rows are filled at the four shared positions by their corresponding lower arrows. After unfolding their L arrows are noncrossing and their H arrows crossing. The residual H-to-L arrows are noncrossing.

An ordinary pair at shift $\delta$ uses $L_i\to L_{i+\delta}$ and $H_{i+\delta}\to H_i$, at shared position $i$, with common column $i+\delta$. Prepend $a$ such pairs at shift $\eta$ immediately before the central beginning $j$. Their columns are $[z-a,z-1]$. Expand the middle by keeping position $j$ and its two reservations at $z$, inserting $b$ ordinary pairs at shift $\eta+1$ at $[j+1,j+b]$, and translating the old noninitial positions and their reservation columns by $b$. The inserted columns are $[z+2,z+b+1]$. The resulting central reservations are
$$
\begin{aligned}
X'&=\{z\}\sqcup[z+2,z+b+1]\sqcup(z+b+\{2,3,4\}),\\
Y&=\{z\}\sqcup[z+2,z+b+1]\sqcup(z+b+\{2,4,5\}).
\end{aligned}
$$
The union bounds separate all three parts even at $b=0$. The central footprint is $[z,z+b+5]$. The remaining H sources are $z+1,z+b+3$ and remaining L images are $z+1,z+b+5$. Their exact completion is Q at $z+1$ and P from $z+b+3$ to $z+b+5$. In particular the would-be P target $z+3$ from $z+1$ is reserved, for $b=0$ in the original L list, for $b=1$ at $z+b+2$, and for $b\ge2$ in the inserted range. Append $c$ ordinary pairs at shift $\eta+2$ starting at shared position $j+b+4$. Their columns start at $z+b+6$. All ordinary pairs use common columns in the two intermediate alphabets and leave no residual hole within their own footprints.

The combined packet uses $4+a+b+c$ consecutive shared positions in each of the L-source and H-image rows, covers both intermediate alphabets within its enclosing interval, and produces the specified expanded capacities at the same actual parents. Each cap can be empty and the middle can be left unexpanded. It contributes exactly one P and one Q arrow, with exactly the same crossing rules throughout. Its first shared position uses the least shift in L, with or without its prepended pairs. The full footprint begins at its first shared position plus $\eta$ and ends at its last shared position plus $\eta+2$. These facts follow from the endpoints just computed, including simultaneous expansions in all three roles.

## 4. Construction of the independent baseline

Fix the actual first inventory. Choose the earliest qualifying even center for the neutral role. Choose four other even centers for the tail and $g$ further even centers for mixed triple middles, by original index. There are $r-2g$ even centers and the construction requires $g+5$ of them for these roles. The available regular shifts of I-a are $[1,r-5]$, and $r-5\ge3g$ gives both counts. Pair the $2g$ odd centers in original index order, placing each pair at the outer shifts of one successive triple in $[1,3g]$. Give each triple its designated even middle. Assign the remaining regular roles to the remaining even centers in original index order. The numerical parent for a shift $\delta$ is exactly $A-1-\delta$. The tail consists of the four deficits $d_0\in\{1,2,3,4\}$, with shift $r-d_0$ and parent $1+d_0$. The selected first terminal belongs to deficit two. The precise assignment of actual tail centers to deficits uses the tail rule below. This procedure chooses all physical roles without moving or reindexing any original center.

Write
$$
h_N=(\alpha_{\rm neutral}-4)/2,\quad
h_R=\big(\sum_{\rm regular}\alpha_i-2(r-5)\big)/2,\quad
h_T=\sum_{\rm tail}(\alpha_i-2)/2,\quad
h_*=h_N+h_R .
$$
The regular sum contains all $2g$ odd quotas and each quota is at least two, so $h_R$ is a nonnegative integer. The choices of neutral and tail give nonnegative integral $h_N,h_T$, and the partition of all first quotas gives $h=h_*+h_T$.

At $\lambda=0$ first assign $L_0,\ldots,L_3$ identically to the neutral center. Its $h_N$ extra ordinary pairs of shift zero occupy shared positions $[4,3+h_N]$ and use their common intermediate columns. Next use the $g$ constructed mixed packets in increasing shift order. Let $\beta\in\{g+3,g+4\}$ and take $p_0=\beta+2a_0$, $q_0=r+3-p_0$ for integer $a_0\ge0$, with $q_0>0$ and
$$
3a_0\le r-5-3g .
$$
On the first $3a_0$ available even regular shifts after the mixed packets, use $a_0$ successive [D178 even active triples](ORDINARY_SPINE_EXCEPTIONAL_ARBITRARY_EVEN_FIRST_QUOTA_LIFT.md#2-arbitrary-neutral-and-regular-expansion). Use ordinary pairs for each remaining regular host. In an even triple at shifts $\delta,\delta+1,\delta+2$ of quotas $(2+2u,2+2v,2+2w_0)$, the central block has length $\ell=3+v$ and origin $z=j+\delta$. The L shift list is two copies of $\delta$ then $\ell-2$ of $\delta+1$, and the H-image shift list $\ell-2$ copies of $\delta+1$ then two of $\delta+2$. This reserves L images $z+(\{0,1\}\cup[3,\ell])$ and H sources $z+([1,\ell-2]\cup\{\ell,\ell+1\})$, with exact residual P arrows $z\to z+2$ and $z+\ell-1\to z+\ell+1$. Prepend $u$ ordinary pairs at the least and append $w_0$ at the greatest shift. Their common columns are strictly below and above the central interval, respectively. The resulting quota and footprint depend only on the three actual even hosts. In particular the retained rule applies here independently of the other hosts' quotas.

Each positive regular group uses half its full total quota as its shared length. Their total length is $r-5+h_R$ and their consecutive shared positions are $[4+h_N,r-2+h_*]$. Each group's intermediate columns, including the shifted and identity residual arrows it supplies, lie between its first shared position plus its least shift and its last shared position plus its greatest shift. These intervals are disjoint by increasing positions and increasing shift groups. Every regular intermediate column lies in $[4,2r-7+h_*]$, along with the common columns of the extra neutral pairs. Initial L reservations lie in $[0,3]$ and use no H positions. All regular and neutral shared H positions exist within the H-image window. The corresponding H-source and L-image columns exist in both intermediate alphabets. All local upper arrows in the regular groups are H-to-L. Unoccupied common columns between them can use Q by identity.

Put $t=h_T$, $N=t+2$ and $D_*=2r+h_*$. The remaining L-source and H-image positions are $r+h_*+x$ for $x\in[-1,N]$ and $x\in[-1,N-1]$, respectively. A tail use of deficit $d_0$ at such a position has intermediate column $D_*+x-d_0$. The local H-source window $[-5,N+1]$ and L-image window $[-5,N+2]$ are stated relative to $D_*$. Their right endpoints are the actual baseline row endpoints $2r+3+h,2r+4+h$. Their common left endpoint $D_*-5$ lies at least at 4 and strictly above the earlier maximum $D_*-7$. This separation and the complete position partitions follow by substituting $h=h_*+t$ in the row table, including when an ordinary group is empty.

All four tail quotas are even. Write them as $2+2u_d$ in the chosen deficit roles. For either tail put a smallest quota at deficit 1, with ties by original index. In the two-shift tail assign the other roles by index, giving $u_3\ge u_1$. In the three-shift tail, if $u_1=0$ and some quota exceeds two, put one larger quota at 3, choosing the earliest such center. Fill the remaining roles by index. Assign the selected actual exterior leaf to its deficit-two parent. The retained local rules use only this tail's quotas and windows. Here are their reservations and residual checks.

- **Two shifts, $\beta=g+3$ ([D180 §3](ORDINARY_SPINE_EXCEPTIONAL_ODD_SECOND_QUOTA_SUPPLIER.md#3-actual-i-a-exterior-and-the-odd-baseline-tail)).** In both shared rows use ordinary deficit pairs in decreasing order, with counts $1+u_4,u_3-u_1,u_2$ at deficits $4,3,2$. Then use $u_1+1$ groups $(1,3)$ in each row, followed by one L-only deficit-two use at $N$. The paired part fills $[-1,N-1]$ in both rows. An ordinary pair at $x$ reserves the common column $x-d$; these columns strictly increase. Each group $(1,3)$ reserves its two positions translated by $-2$. Its first group starts at column two below its first position, strictly above the preceding ordinary maximum. The shared reservations lie in $[-5,N-3]$ and coincide in the two alphabets. The last L-only use adds $N-2$ to the L images. The P arrows $N-2\to N$ and $N\to N+2$ fill the exact mismatch from the added L reservation and the absent H source at $N+2$. Both sources and images are free in their own windows. The remaining indices coincide and use Q. The groups supply all $2+2u_1$ uses at 1 and the same count at 3, the pairs supply the rest of 3 and all of 4, and the pairs, last L use and selected leaf supply all of 2. At the all-two boundary the shared reservations are $\{-5,-2,-1\}$, the extra L reservation is 0, and the P arrows are $0\to2$ and $2\to4$.
- **Three shifts, $\beta=g+4$ ([D178 §4.2](ORDINARY_SPINE_EXCEPTIONAL_ARBITRARY_EVEN_FIRST_QUOTA_LIFT.md#42-i-a)).** If all tail quotas are two, use L deficits $(1,4,4,2)$ and H-image deficits $(3,1,3)$ beginning at $-1$. Their L reservations are $\{-4,-3,-2,0\}$ and H reservations $\{-4,-2,-1\}$. The three arrows $-3\to-1,0\to2,2\to4$ leave exactly the identity complement in $[-5,3]$ and $[-5,4]$. Otherwise consume two uses at deficit 4 in L and two at deficit 3 in H in a joint two-position block. For a right part with effective deficit two in both rows, take $u_1+1$ groups $(1,3)$ per row if $u_3\ge u_1+1$, or $u_1-1$ such groups and one $(1,1,4)$ per row if $u_3=u_1\ge1$. Each group reserves precisely its positions translated by $-2$. The right groups exhaust deficit 1 and cost $2(u_1+1)$ uses at 3 in the first case, or $2(u_1-1)$ at 3 and two at 4 in the second case. These costs are available after the joint block since $u_4\ge u_1$ and by the choice of 3. Reserve a final L-only use at deficit two and the selected exterior terminal at that same host. All remaining quotas are nonnegative even counts at $4,3,2$ and use ordinary pairs. Place the remaining deficit-4 pairs first, the joint block next, then the remaining deficit-3 and deficit-2 pairs in order, then the right groups and the final L-only use. For the joint block starting at $x$, the L reservations are $x-4,x-3$, the H reservations $x-3,x-2$, and the P arrow is $x-4\to x-2$. Preceding pairs end at most at $x-5$, following pairs start at least at $x-1$. The right groups begin at column two below their first position and are strictly above the preceding block or pairs. The lengths are exactly $4+t$ for L and $3+t$ for H, because all residual physical quota units are used and only the final L-only position is unpaired. As in the two-shift case, the final L reservation $N-2$ and the absent H source at $N+2$ give the two arrows $N-2\to N$ and $N\to N+2$, disjoint from the joint block. All reservations and shifted arrows lie in the stated windows and the remaining indices coincide and use Q. This accounts for all four physical quotas with exactly three P assignments.

The baseline uses every L source and every H image at lower hosts, and the four fixed L assignments, neutral pairs, regular footprints and tail supply every first quota with the selected exterior leaf restored. The residual upper assignments are all H-to-L. On the regular groups and the tail their P arrows and Q identity complements are exact. Outside those footprints the remaining H sources and L images coincide, except for the initial L reservations $[0,3]$ below the H window and the last L cell already handled in the tail. This proves both complete baseline bijections. The H sources total $2r+h$ and the H images at first hosts total $r-2+h$. So there are $r+2$ upper uses. P uses $g+2a_0+(\beta-g-1)=p_0-1$ residual terminals and its one actual selected terminal. Q uses $r+2-(p_0-1)=q_0$. Here $x=0$ and $y=r-2+h$. Both quota orders are valid whenever the stated strip bound and quotas are satisfied. The argument uses the local even blocks and tail only at their actual even hosts.

The first neutral L arrows stay fixed. The baseline has an anchor $L_4\to L_{4+\delta}$, with $\delta=0$ if there is an extra neutral pair and $\delta=1$ otherwise. In the latter case the first mixed triple starts at shift one, and its first L arrow uses that shift in both the prepended and unprepended cases.

## 5. Exact growth and the split choice

The [D179 Q-only and balanced strips](ORDINARY_SPINE_EXCEPTIONAL_INDEPENDENT_SECOND_QUOTA_GROWTH.md#3-q-only-growth) require the four fixed neutral arrows, the same I-a physical maps, the row table and the anchor just established. Their proofs use neither the parity of the local first capacities nor the parity of the upper quotas. Here is their direct use.

For Q-only growth by $2a$ translate all folded indices of every arrow outside the fixed neutral four by $a$, with $a\ge0$. Every such source and destination index is at least four. Each of the four row endpoints grows by $a$, and the unchanged initial L cells plus the translated old cells leave exactly $[4,3+a]$ in each row. At each of those columns place both Q arrows $L_j\to H_j$ and $H_j\to L_j$. All old folded shifts and physical roles are unchanged. There are $2a$ additional Q uses and no other changes in counts.

For balanced growth by $2b$ at each upper host, $b\ge1$, let $v_0=2b$. Use the same translation by $v_0$ outside the four initial neutral cells, hold the new common strip $D_0=[4,3+v_0]$ open, and move the translated anchor at its actual lower host back from $L_{4+v_0}\to L_{4+v_0+\delta}$ to $L_4\to L_{4+\delta}$. Both new anchor endpoints are in the open strip since $0\le\delta\le1$. The free L-source indices are now $(D_0\setminus\{4\})\sqcup\{4+v_0\}$ and the free H-image indices are $D_0$. The P assignments
$$
L_{4+2j}\to H_{4+2j-2}\quad(1\le j\le b)
$$
pair exactly the excess endpoint with the missing endpoint along one residue chain. Removing those source and image lists leaves equal sets for Q. The other direction has free H-source indices $D_0$ and free L-image indices $(D_0\setminus\{4+\delta\})\sqcup\{4+v_0+\delta\}$. Use
$$
H_{4+\delta+2j}\to L_{6+\delta+2j}\quad(0\le j\le b-1).
$$
Its last source $2+\delta+2b$ is at most $3+v_0$, and its last image is the freed endpoint at $4+\delta+v_0$. Removing these sources and images again leaves equal sets for Q. In each direction there are $b$ P uses and $b$ Q uses. The two directions operate in disjoint physical source and destination rows. Their open cells were derived by exact translation and anchor replacement, so they do not collide with any other old arrow. All original first-host counts are unchanged. With $b=0$ use the identity operation. The balanced result still fixes the four initial arrows and has every other folded endpoint at least four, so subsequent Q-only growth gives the exact combined increment $(2b,2b+2a)$.

Order the actual second roles by full target quotas $p\le q$, breaking ties by original branch index. For $p+q\ge R_0$, take $\beta=g+3+\varepsilon$ with $\varepsilon\in\{0,1\}$ chosen to match their parity. Both target quotas are at least $\beta$. Put $M$ equal to the largest integer of this parity at most $R_0/2$. At the principal bound $r\ge6g+17$, $M\ge R_0/2-1\ge\beta$. The ordinary near-balanced pair $(M,R_0-M)$ has difference $d_0=R_0-2M\in\{0,2\}$. The following choices keep the numerical roles of the actual target hosts.

- If $p\le M$, use $(p_0,q_0)=(p,R_0-p)$. Then $q_0\ge p_0\ge\beta$, $q\ge q_0$ by the total threshold, and the desired increment at P is zero.
- If $p>M$ and $q-p\ge d_0$, use $(M,R_0-M)$. The same parity gives $p\ge M+2$, so both target quotas are at least the larger baseline quota. Also $(q-q_0)-(p-p_0)=q-p-d_0\ge0$.
- The remaining case has $d_0=2$ and $p=q>M$, since target differences are even. Use the reversed $(M+2,M)$. Both target quotas are at least $M+2$ and the difference of required increments is two. The reversed baseline uses the same I-a construction with its P host's actual larger baseline quota.

All cases have $p_0,q_0\ge\beta$, the required parity, and $p_0\le(r+5)/2$. Hence
$$
3a_0=\frac{3(p_0-\beta)}2
\le \frac{3(r-2g-1)}4
\le r-5-3g
\qquad(r\ge6g+17).
$$
This is exactly the supply bound for the even regular triples after the mixed ones. Apply the strips with $b=(p-p_0)/2$ and $a=((q-q_0)-(p-p_0))/2$, nonnegative integers by the displayed choices. The resulting width change is $\lambda=2b+a=(R-R_0)/2$. Exactly $\lambda$ new L sources go to upper hosts, so $x=\lambda$. The count $y=r-2+h$ of H sources at lower hosts is unchanged. This verifies $x+y=s-K$ and $1+r+R=2(A+x)$ on the actual final assignment.

A sharper sufficient range follows from the same formulas. At parity $\varepsilon$, the bound using $(r+5)/2$ is $r\ge6g+17-6\varepsilon$. For cases using an ordinary baseline, $p_0\le(r+3)/2$ instead, and $r\ge6g+11-6\varepsilon$ suffices. At both bounds $r-5\ge3g$ and $M\ge(r+1)/2\ge\beta$ for $g\ge1$. More generally the explicit choice suffices if those two availability conditions hold and $3(p_0-\beta)/2\le r-5-3g$. These are sufficient variants, with no infeasibility conclusion for cases where this particular baseline choice runs out of regular shifts.

## 6. Original named realization, inventories and return

The allocation uses the actual ordered branch identities and original witnessing spine throughout. At the selected first parent and P, reserve the prescribed actual indexed terminal for the exterior. Assign the baseline arrows at each parent to the first available actual residual terminal indices, in a fixed row and index order. The baseline first capacities are those of the full target, and its second capacities fit the actual target after the single P selection. Keep these actual names when moving or translating an arrow. The two growth operations use exactly the remaining actual indexed terminal vertices at Q and P, in order. The direct edge is the actual exterior edge at $w$. All these assignments are obtained from the quotas, independently of any solved full target. The baseline is only a normalized allocation used in computing the target; it needs no separately extracted labeled prefix.

For each actual first host at shift $\delta_i$, let $S_i^0$ be the set of its numeric baseline gap sources, unfolded at $J_0=3r+6+2h$. The exact baseline first-section sets are the disjoint unions
$$
I_0=\bigsqcup_i S_i^0,\qquad M_0=\bigsqcup_i(S_i^0+\delta_i).
$$
They are obtained from the explicit lower arrows at their actual first hosts. Disjointness of sources and images was proved in the interval and position partitions. The second set follows from numerical endpoint subtraction and includes all actual first gap edges. Let $E_0=[0,3]$ and define $T_\lambda(D)=E_0\sqcup((D\setminus E_0)+\lambda)$ for sets containing $E_0$. All unchanged noninitial L coordinates increase by $\lambda$. An unchanged noninitial H index becomes $j+\lambda$ but unfolds at $J_0+2\lambda$, so its numeric coordinate is $J_0+2\lambda-(j+\lambda)=(J_0-j)+\lambda$. Thus for $b=0$ the exact final first sets are $I=T_\lambda(I_0)$, $J_1=T_\lambda(M_0)$. For $b>0$ the moved anchor followed by Q translation of size $a$ gives
$$
\begin{aligned}
I&=(T_\lambda(I_0)\setminus\{4+\lambda\})\sqcup\{4+a\},\\
J_1&=(T_\lambda(M_0)\setminus\{4+\delta+\lambda\})\sqcup\{4+\delta+a\}.
\end{aligned}
$$
The added cells are in the adjusted strip and distinct from the retained assignments, as checked in §5. In the full allocation these are precisely the unions of first source sets $S_i$ and first image sets $S_i+\delta_i$ at the actual first hosts. The remaining gap sets are $I'=[0,s-1]\setminus I$ and $J_2=[0,s-1]\setminus J_1$. In particular when $\lambda>0$ some lower sources belong to the second section.

For the oriented final return, translate old labels by $A$ below $c$ and by $A+s$ at or above $c$. The low old maximum $A+c-1<C$ and high old minimum $A+s+c\ge C$ by width admission, so every old side is preserved. Old noncrossing differences stay unchanged and old crossing differences gain $s$. Use labels $A+c+i$ on the gap leaves. Expand the upper reduced labels by adding $n+s$, retaining every lower reduced label. The shared frontier $v$ receives $A$ by both formulas and is counted in the old alphabet. Exterior lower ends are at most $A<C$ and upper ends at least $n+s+A+1>C$. The exact palettes are
$$
\begin{array}{ll}
L_{\rm old}=[A,A+c-1]\sqcup[A+c+s,n+s+A],&
L_{\rm fresh}=[0,A-1]\sqcup[A+c,A+c+s-1]\sqcup[n+s+A+1,m],\\
D_{\rm old}=[1,d-2]\sqcup[d-1+s,n+s],&
D_{\rm fresh}=[d-1,d+s-2]\sqcup[n+s+1,m].
\end{array}
$$
The old and fresh palettes are disjoint and cover $[0,m]$ and $[1,m]$, respectively, using $m=n+s+A+5$. The exterior spectra give every indicated exterior value and the unfolded row bijections give each gap label and each actual gap difference exactly once. Gap weights $d-1+[0,K-1]$ are noncrossing and $d-1+[K,s-1]$ cross, by the actual parent subtraction and source sides in §2. Thus the exact full crossing spectrum is $[d+K-1,m]$ and the noncrossing spectrum is $[1,d+K-2]$. The output has $w=0$ and $m=2C+2$, giving $S_{-1}$ with the original extended witnessing spine.

At the first-section boundary the fresh exterior label sets are
$$
E_1=[2,A-1]\sqcup\{n+s+A+1,n+s+A+3\},\qquad
E_2=\{0,1,n+s+A+2,n+s+A+4,n+s+A+5\}.
$$
The associated difference sets are $D_1^e=n+s+[1,A]$ and $D_2^e=n+s+[A+1,A+5]$. Put $I_\ell=I\cap[0,k-1]$, $I_u=I\cap[k,s-1]$, and partition $I'$ the same way. For $J_z$ equal to $J_1$ or $J_2$, put $J_z^{\rm nc}=J_z\cap[0,K-1]$ and $J_z^{\rm cr}=J_z\cap[K,s-1]$. Let $O_\ell,O_u$ denote the old low and high bands, and let $E_z^\ell,E_z^u$ denote the respective lower and upper reduced sides after expanding $E_z$. With these partitions the two exact inventories are
$$
\begin{array}{ll}
\text{used labels} & L_{\rm old}\sqcup E_1\sqcup(A+c+I),\\
\text{remaining labels} & E_2\sqcup(A+c+I'),\\
\text{used differences} & D_{\rm old}\sqcup D_1^e\sqcup(d-1+J_1),\\
\text{remaining differences} & D_2^e\sqcup(d-1+J_2).
\end{array}
$$
Explicitly, used label side $v_0\in\{\ell,u\}$ is $O_{v_0}\sqcup E_1^{v_0}\sqcup(A+c+I_{v_0})$, and the remaining side is $E_2^{v_0}\sqcup(A+c+I'_{v_0})$. Used crossing differences are $[d-1+s,n+s]\sqcup D_1^e\sqcup(d-1+J_1^{\rm cr})$, remaining crossing ones $D_2^e\sqcup(d-1+J_2^{\rm cr})$. Used noncrossing differences are $[1,d-2]\sqcup(d-1+J_1^{\rm nc})$, remaining ones $d-1+J_2^{\rm nc}$. All disjointness and complements follow from the actual first and second incidences and the full palettes. The literal unfinished original connector $uw$ has oriented endpoints $(n+s+A+1,0)$ and crossing weight $n+s+A+1$ in the remaining exterior band.

For actual maximum polarity the input is $n-G$ and the actual output is the complement about $m$. The actual input and output cuts are $n+1-c$ and $m+1-C$. Under complementation the lower and upper shifts become $B$ and $B+s$ by $2K=A+B+s$, versus $A$ and $A+s$ in minimum polarity. Both label inventories are complemented and exchange cut sides. All differences and crossing statuses are preserved. The actual frontier is $w=m$ and the unfinished connector endpoints are $(4,m)$.

For any admitted finite sequence, use each block's own independent allocation, actual input phase, named spine roles and size and spectrum premises on its incoming alphabet. Each placement preserves prior cut sides as they evolve. From any completed cut $C_i$ the exact final label map is $x\mapsto x+T_i+S_i\mathbf1_{x\ge C_i}$, where $T_i$ sums later actual lower shifts and $S_i$ sums later gap widths. Its crossing differences gain $S_i$ and its noncrossing differences keep their values. Apply these maps to both exact first-section inventories and to both endpoints of each literal unfinished connector. For the inventory relative to that stage, take the unused complements in its lifted alphabet; at the final alphabet the later named vertices and incidences are included in the unused complements as appropriate. The gap and exterior bands at each further insertion are disjoint from lifted old values. Induction verifies all admitted returns and preserves both current and subsequent connector incidences. The formulas select finitely many groups and then scan only the finite input incidences, and the final backward sums are finite. This yields immutable emission in the final alphabet and uses the independent initializer under its retained D157/D134 hypotheses. Its domain consists of individually admitted sequences.

## 7. Scope and controls

The explicit mixed packet, parity-sensitive tail choice and exact balanced strip prove the principal threshold without any solver verdict. D178's even active block and three-shift tail and D180's two-shift tail are used on their proved local capacities and windows. The D179 strips are checked at the actual mixed baseline anchor. D180 is Director accepted at checkpoint 2669adda6052a861fde9734ce35749eeecc40d08 in its exact written scope, including the scoped moment obstruction and smaller-case qualifications. Its frozen manifest and primary proof retain their accepted bytes. All earlier scopes, approvals and historical dispositions are retained.

This investigation leaves quota-one cases, general first parity or totals, preassigned numerical roles, other numbers of second centers, more general independent initialization, terminal-free feasibility and unrestricted gracefulness outside its conclusion. D175's H0 obstruction and D176's complete menu retain their original quota premises. The independent frozen D174 prefix is a custody control. The historical execution remains one completed matched pair and two numerical arms with 3,518 unentered originals, including 92 of the 93 in D177's separately accepted symbolic projection. No new numerical search, solver use, scientific campaign or historical checker replay contributed to D181.
