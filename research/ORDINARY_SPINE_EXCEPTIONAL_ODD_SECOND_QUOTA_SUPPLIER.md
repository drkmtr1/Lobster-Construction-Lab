# D180 — Odd second-quota supplier on width-five exceptional exteriors

Task **LCL-ORDINARY-SPINE-EXCEPTIONAL-ODD-SECOND-QUOTA-SUPPLIER-001**.

**PROVED WITHIN EXACT WRITTEN SCOPE / PENDING DIRECTOR REVIEW.** For every odd $r\ge17$, arbitrary positive even first quotas with at least one quota at least four, and odd second quotas $p,q\ge3$, compatible terminal-enabled H1 in the declared D157 $S_{-1}$-to-$S_{-1}$ arrangement exists exactly when $R=p+q\ge r+3$. The named prefix is independently supplied and admissible for the full target. The first section has no direct leaf and the sole actual second direct leaf belongs to the exterior. All physical branch orders are admitted with selectable numerical roles. The positive construction uses I-a with an explicit two-shift tail, followed by the D179 growth strips.

## 1. Necessity for the declared class

Use the [D157 exceptional placement](ORDINARY_SPINE_ALTERNATING_EXCEPTIONAL_SPECTRUM.md#1-interface-and-exact-inventory-rule). All structural data and labels are exact integers, excluding booleans. Intervals include both endpoints and a reversed interval is empty. The independently supplied named graceful prefix has $n=2c+2$ edges, ends at the actual extreme witnessing-spine vertex $v$, and is oriented by $G(v)=0$. Its cut $c$ places equality on the upper side. With $d=c+2$, its exact crossing and noncrossing spectra are $[d-1,n]$ and $[1,d-2]$. Append the actual spine vertices $u,w$. With $F$ the first terminal total, the two new spine vertices, $r+2$ actual centers, direct leaf and $F+R$ terminals give
$$
2K=F+r+R+5,\qquad m=n+2K,\qquad n\ge2K.
$$
The sum is even for odd $r$ and even $F,R$, including the proposed odd-odd split.

For any compatible terminal-enabled H1 exterior, color by taking $v$ lower. The fresh lower graph class comprises $w$, the $r$ first centers and the $R$ second terminals. It has size $1+r+R$. The fresh upper class comprises $u$, the two second centers, the direct leaf and the $F$ first terminals. The connected crossing reduced exterior places each of its actual vertices on its graph color's side. If $e_1,e_2$ are the selected exterior terminal counts by section, its widths are $A=r+1+e_2$ and $B=4+e_1$. This counts the actual direct leaf in the upper class. The unique weight-one crossing edge between the reduced sides must join $A,A+1$. The lower label $A$ is $v$, whose sole new incidence is $vu$. Thus $u=A+1$.

To verify terminal balance, keep $vu,uw$ and consider the reference edges from lower slots $[1,A-1]$ to $u$ and from upper slots $A+b$, $b\ge2$, to $w$. Their reduced weights fill $[1,A+B]$. In the true exterior, selecting a first terminal at an upper slot decreases its edge weight relative to reference by its actual lower parent label $j\ge1$. Selecting a second terminal at a lower slot increases its edge weight by $b-1\ge1$, where $A+b$ is its actual parent. The second direct leaf stays at its actual parent $w$ and keeps the reference difference. Hence equality of the sums of the two reduced spectra requires $\sum_{\rm first\ selected}j=\sum_{\rm second\ selected}(b-1)$. A terminal-enabled exterior has at least one selected terminal, so both $e_1,e_2\ge1$. Neither the argument nor the counts depend on the parity of the individual second quotas.

Put $s=2K-A-B$ and $k=K-A$. Same-phase admission gives $A\le K\le A+s$ and $s\ge K$. The first condition preserves old sides and the second follows since the least old crossing $d-1$ gains $s$ and the output crossing spectrum starts at $d+K-1$. Exterior differences are $[n+s+1,m]$ and crossing, and the lifted old crossing band is $[d-1+s,n+s]$. The normalized gap image interval is $[0,s-1]$, corresponding to weights $d-1+\pi(i)$. Exactly the $s-K$ images with $\pi(i)\ge K$ cross. There are $k$ physically lower sources. Let $x$ count lower sources at upper hosts and $y$ upper sources at lower hosts. Then $x+y=s-K$. The $s-k-y+x$ gap leaves at upper hosts have lower graph color, opposite their actual parents, irrespective of their label side. Thus, just as in [accepted D179 §1](ORDINARY_SPINE_EXCEPTIONAL_INDEPENDENT_SECOND_QUOTA_GROWTH.md#1-exact-original-counts-and-threshold-necessity),
$$
N_{\rm low}=1+r+R=A+(s-k-y+x)=2(A+x)\ge2(r+2).
$$
This is the necessary threshold $R\ge r+3$. It uses no exhausted-neutral premise. It excludes only below-threshold terminal-enabled H1 in this declared arrangement.

## 2. Exact width-five rows and folded parity moment

From now on keep the widths $A=r+2,B=5$, $R_0=r+3$, $h=F/2-r-1\ge0$, and $R=R_0+2\lambda$, $\lambda\ge0$. There is one selected exterior terminal in each section. Then
$$
K=2r+5+h+\lambda,\quad s=3r+3+2h+2\lambda,\quad k=K-A=r+3+h+\lambda,\quad J=s+3.
$$
The margin is $K-(A+B)=r-2+h+\lambda\ge0$ throughout the positive domains. Thus $s\ge K$ and $A\le K\le A+s$. A gap coordinate $i$ receives oriented label $A+c+i$ and is physically lower iff $i<k$. The actual endpoint subtraction gives $\pi(i)=i+\delta$ at lower reduced label $j_0$, where $\delta=A-1-j_0$. At upper label $A+b_0$ it gives $\pi(i)=s+b_0+1-i$. These formulas use the actual expanded upper labels and the lower host smaller than each gap label. The exact folded notation is $L_j=j$ and $H_j=J-j$, with
$$
\begin{array}{c|cc}
 & L & H\\
\text{sources} & [0,r+2+h+\lambda] & [4,2r+3+h+\lambda]\\
\text{images} & [0,2r+4+h+\lambda] & [4,r+1+h+\lambda].
\end{array}
$$
The H rows unfold to $[k,s-1]$ for sources and $[K,s-1]$ for images. Thus each folded alphabet represents its own complete numerical $[0,s-1]$. A lower host translates indices by $+\delta$ from L and $-\delta$ from H, keeping the row. The upper-host roles in these geometries are $Q=A+2$ and $P=A+2+\rho$. Upper arrows exchange rows. The index is fixed at $Q$ and changes by $-\rho,+\rho$ on L and H sources at $P$. For every legal arrow the H image is exactly the physical crossing case and has $\pi(i)\ge K$.

Let $M_*=r+2+h+\lambda$. The L-image row adds $[M_*+1,M_*+A]$ to the L-source row. The H-image row removes $[M_*,M_*+A-1]$ from the H-source row. The difference of the sums of all destination and source indices is therefore $A=r+2$ by subtracting these two intervals of equal length. For an allocation, the index increment at a first host contributes $\delta$ or $-\delta$. There are $\alpha'$ uses at that host after the exterior selection. At $Q$ the increment is zero and at $P$ it is $\pm\rho$, through exactly $p-1$ residual uses, where $p$ is the actual full ordered quota at $P$. Modulo two these signs disappear. Consequently
$$
r+2\equiv\sum_{\text{first hosts}}\delta\alpha'+\rho(p-1)\pmod2 .
$$
Since all first full quotas are even and exactly one first terminal is exterior, the sum has the parity of its selected host shift. The direct leaf has no gap contribution. In the specific II-a and I-b geometries of [D176 §2](ORDINARY_SPINE_EXCEPTIONAL_ODD_FIRST_CENTER_H1_MENU.md#2-complete-geometry-reduction-and-raw-spectra), the selected first parent is at 4, of shift $r-3$, and $\rho=3$. The odd left side and even first term force $p-1$ odd, hence $p$ even. This obstruction holds throughout the expanded gap sizes of these two particular geometries. It uses their incidences and width and is no general exterior-menu claim. In I-a the selected first parent is at 3, of shift $r-2$, and $\rho=2$. The first term is odd, so the moment is satisfied without restricting the parity of $p$.

## 3. Actual I-a exterior and the odd baseline tail

Use $v=A,u=A+1,w=0$, and $Q=A+2,P=A+4$. At $P$ select its first actual terminal and give it reduced label 1. All actual first centers occupy $[2,A-1]$. At the actual first parent assigned label 3, select its first actual terminal at $A+3$. Take an actual quota-at-least-four center as the neutral at $A-1$. The literal direct leaf at $w$ receives $A+5$. These edges form the intended connected crossing exterior. The first edges at $u$ give $[1,A-1]$ including $vu$, and its selected first terminal gives $A$. The second edges have weights $A+1,A+2,A+3,A+4,A+5$ at $uw,wQ$, the selected $P$ terminal edge, $wP$, and the direct edge at $w$. Thus the exact reduced vertex and difference alphabets are $[0,A+5]$ and $[1,A+5]$. Every incidence is an edge of the named original.

Work at the independent total $R_0$ for the baseline. After selecting the neutral, choose four other actual first centers as the special tail. Assign the remaining $r-5$ to successive positive regular shifts in original index order. The tail roles have deficits $1,2,3,4$, meaning a lower host has shift $r-d_0$ when its deficit is $d_0$. Their actual full quotas are $2+2u_{d_0}$. Assign a smallest actual tail quota to deficit 1, breaking ties by original index, and assign the other three roles by original index. In particular $u_3\ge u_1$. The exterior terminal at first parent 3 is at deficit 2 and uses one of its actual indexed terminals.

Set $h_N=(\alpha_{\rm neutral}-4)/2$, $h_R=\sum_{\rm regular}(\alpha-2)/2$, $t=\sum_{d_0}u_{d_0}$ and $h_*=h_N+h_R$. Thus $h=h_*+t$. In the exact separated tail coordinates of [D178 §3](ORDINARY_SPINE_EXCEPTIONAL_ARBITRARY_EVEN_FIRST_QUOTA_LIFT.md#3-separated-special-tail-coordinates-and-the-bounded-tail-lift), $N=t+2$, the L-source and H-image positions are $r+h_*+j$ with local $j\in[-1,N]$ and $j\in[-1,N-1]$, respectively. Intermediate columns are offsets from $2r+h_*$. A position $j$ at deficit $d_0$ reserves column $j-d_0$ in the respective L-image or H-source alphabet. The local windows are $[-5,N+1]$ for H sources and $[-5,N+2]$ for L images. The last L cell $N+2$ is an absent H-source cell.

Use ordinary matched pairs, one use of the same deficit in each row at the same position, in decreasing deficit order 4,3,2:
$$
1+u_4\text{ pairs at 4},\qquad u_3-u_1\text{ pairs at 3},\qquad u_2\text{ pairs at 2}.
$$
All counts are nonnegative integers. At deficit 2 the one other L-only use and the actual exterior terminal account for the two unpaired quota units. After these pairs use $u_1+1$ successive groups $(1,3)$ in **each** row. For a group starting at $x$, the two columns are $x-1,x-2$, exactly its position interval translated by $-2$. It consumes one terminal of each deficit in each row. This gives all $2+2u_1$ leaves at deficit 1 and that many at deficit 3, with its remaining $2(u_3-u_1)$ leaves supplied by the earlier pairs. The deficit-4 pairs use all $2+2u_4$ actual leaves, and the deficit-2 pairs plus the extra L use and exterior selection use $2+2u_2$. Thus every physical tail quota and selected incidence is exact.

The shared positions number
$$
(1+u_4)+(u_3-u_1)+u_2+2(u_1+1)=3+t,
$$
so they fill $[-1,N-1]$ in both lists. In the ordinary part, advancing $j$ and using nonincreasing deficits makes its reserved columns strictly increasing. If the special groups begin at position $j_0$, the earlier pair columns are at most $j_0-3$ and the group columns are exactly $[j_0-2,N-3]$. Each group interval is disjoint from all others. The earliest possible reservation is at least $-1-4=-5$, and all shared reservations are at most $N-3$. Append the final L-only position $N$ at deficit 2, reserving column $N-2$. The two reservation sets therefore obey
$$
X'=Y\sqcup\{N-2\},
$$
where $Y$ is the H-source reservation set and $X'$ the L-image reservation set, each distinct in its own alphabet. The additional L reservation exists and lies above all shared reservations. The H sources $N-2,N$ exist and are unreserved, and the L images $N,N+2$ exist and are unreserved. Assign the two $P$ arrows
$$
H_{N-2}\to L_N,\qquad H_N\to L_{N+2}
$$
in local offset notation, with separation two. This covers precisely the displaced pair of positions in the residual matching. In fact the surviving H and L index sets differ by the missing destination $N-2$ and the missing source $N+2$, with one common available position $N$ moved along the path. Removing the two assigned sources and images leaves equal sets, paired at $Q$ by identity. All named H assignments at first hosts and at upper hosts have their respective crossing types.

For the all-two tail, $t=0,N=2$. The ordinary pair at deficit 4 from $-1$ gives $-5$, the group at $0,1$ gives $-1,-2$, and the final L position 2 gives 0. Thus $Y=\{-5,-2,-1\}$, $X'=Y\sqcup\{0\}$ and the shifts are $0\to2$ and $2\to4$ on the two local H-source and L-image rows. These are available in $[-5,3]$ and $[-5,4]$ and leave the exact identity complement, establishing the boundary arithmetic without a search.

## 4. Exact independent odd baseline and its anchor

Take odd $p_0,q_0\ge3$ of total $R_0$. Put $a_0=(p_0-3)/2$ and assume $3a_0\le r-5$. Retain the actual [D178 neutral and regular allocations](ORDINARY_SPINE_EXCEPTIONAL_ARBITRARY_EVEN_FIRST_QUOTA_LIFT.md#2-arbitrary-neutral-and-regular-expansion). Give $L_0,\ldots,L_3$ their identical initial neutral images. Use $h_N$ ordinary zero pairs at positions $[4,3+h_N]$. In the regular shifts use $a_0$ active triples on the first $3a_0$ successive shifts, with their actual independent quota promotions, and ordinary pairs thereafter. Each triple gives exactly two $P$ arrows and all ordinary pairs give common holes. D178 proves the exact windows and each individual quota for these rules. The only change in the use of that proof is the independently specified number of triples, which meets its exact shift-count requirement. Nothing here requires $p_0\le q_0$.

The regular and neutral pairs use consecutive L-source and H-image positions up to $r-2+h_*$, with no intermediate column above $2r-7+h_*$. The tail positions start at $r-1+h_*$ and their used columns start at least $2r-5+h_*$, strictly above all the previous footprints. Its shifts and residue path lie entirely within its upper windows, with the correct absent final H source. At $r\ge5$ that local minimum also lies at least at index 5. Along the two dimensions, all reserved L sources and H images are therefore exactly covered, and after the active paths and two tail shifts the remaining upper assignments have identical indices at $Q$. The H-source count is $2r+h$ and the H images used by first hosts number $r-2+h$, leaving $r+2$ uses at upper hosts. The total shifted uses are $2a_0+2=p_0-1$ and the $Q$ uses are $r+2-(p_0-1)=q_0$. Including the actual selected exterior terminal, the full second quotas are exact. The baseline has $x=0$ and $y=r-2+h$. Its first four neutral L arrows are unchanged.

If the neutral has extra pairs, the first at $L_4$ has shift zero. When it has none and $r\ge7$, the regular strip begins at shift one. A first ordinary pair, a prepended first-host pair or the first L position of a first active central block all use this least shift. Thus the D179 anchor $L_4\to L_{4+\delta}$ exists with $\delta=0$ or 1. For the directly relevant $r=5$ baseline one has $a_0=0$ and no regular shifts. If there is no neutral extra pair, the odd tail begins with an ordinary deficit-four pair because $1+u_4\ge1$. Its shift is $r-4=1$, again at $L_4$. These arguments use the actual same lower parent and an actual gap terminal.

## 5. Growth and parity-correct baseline selection

The [D179 Q-only and balanced I-a strips](ORDINARY_SPINE_EXCEPTIONAL_INDEPENDENT_SECOND_QUOTA_GROWTH.md#3-q-only-growth) require the precise folded rows, the four initial neutral L arrows with all other folded cells at least four, and for balanced growth an existing $\delta=0$ or 1 first arrow at $L_4$. Sections 2–4 give these premises. Here is the direct verification of their use with odd quotas.

For a growth of total $2\lambda$, the four endpoints in the displayed rows of §2 grow by $\lambda$. Translate all noninitial arrows by $\lambda$ on both folded indices, preserving the parent. The complementary rows are the common strip $[4,3+\lambda]$. Use both identity row exchanges there at $Q$ to add $2\lambda$ leaves to that host only. Its L arrows cross and its H arrows do not. This works for arbitrary full quotas on a given compatible starting allocation.

For balanced growth put $\lambda_b=2b$, $b\ge1$, and first perform the translation with tentative strip $S=[4,3+2b]$. Move the anchored first arrow from $L_{4+2b}\to L_{4+2b+\delta}$ to $L_4\to L_{4+\delta}$ at the same parent. Both new cells belong to $S$ since $\delta\le1$. The other old arrows stay in their translated cells. In the L-source direction the free sources are $(S\setminus\{4\})\sqcup\{4+2b\}$ and the H images are $S$. The $b$ shifted arrows
$$
L_{4+2j}\to H_{4+2j-2}\qquad(1\le j\le b)
$$
use the replaced even-index interval, with odd columns matched identically at $Q$. In the H-source direction the free sources are $S$ and the L images $(S\setminus\{4+\delta\})\sqcup\{4+2b+\delta\}$. Use the $b$ shifted arrows
$$
H_{4+\delta+2j}\to L_{6+\delta+2j}\qquad(0\le j<b).
$$
The last source is $2+2b+\delta\le3+2b$. Their images extend exactly through the freed old image and the other residue in $S$ matches identically. Both sets of shifted arrows are at $P$ and hit exactly their free cells. Both matches use disjoint source rows and disjoint image rows, and the only cells outside the strip used in these matches are the explicitly freed old source and image. Each upper host gains $2b$ terminal assignments, half crossing and half noncrossing among these new assignments. The actual first host and its quota stay fixed.

At $b=0$ use the original arrows. All noninitial indices after the first step remain at least four, with the initial neutral cells unchanged. A subsequent Q-only growth of $2a$ terminal leaves therefore gives
$$
(p_0,q_0)\longmapsto(p_0+2b,q_0+2b+2a),\qquad a,b\ge0.
$$
These are exact combinatorial row and host correspondences and never use the parity of the old quotas. In particular they preserve the odd quota parities of the new baseline. The net parameter of §2 is $\lambda=2b+a$.

For the requested full quotas choose the numerical roles with $p\le q$, breaking a tie by physical index. Let $M$ be the largest odd integer no greater than $(r+3)/2$. At $R\ge R_0$, if $p\le M$ use $(p_0,q_0)=(p,R_0-p)$, which fits since $q\ge R_0-p$. If $p>M$, take the ordinary baseline $(M,R_0-M)$ except in the reversed case below.

- If $R_0\equiv2\pmod4$, then $M=(r+3)/2$ is odd and this largest ordinary baseline is equal. At $p>M$ it fits at both parents and $q-q_0\ge p-p_0$ follows from $p\le q$. Its maximum ordinary triple requirement is $3(M-3)/2=3(r-3)/4\le r-5$ for $r\ge11$.
- If $R_0\equiv0\pmod4$, then $M=(r+1)/2$ is odd, the ordinary baseline difference is 2 and its maximum ordinary triple requirement is $3(M-3)/2=3(r-5)/4\le r-5$. If $p>M$ and $p<q$, then $p\ge M+2$ and $q-p\ge2$. Thus the ordinary baseline fits and $q-q_0\ge p-p_0$. If $p=q>M$, use the reversed $\bigl((r+5)/2,(r+1)/2\bigr)$. Here $p_0=M+2\le p$ and $q_0=M\le q$, and $q-q_0=p-p_0+2$. The exact active-triple requirement is $3(p_0-3)/2=3(r-1)/4\le r-5$ precisely for $r\ge17$.

All ordinary baselines with $p\le M$ meet the corresponding maximum bounds above. All used baseline quotas are odd and at least three. In the reversed case the actual numerical $P$ role gets the larger baseline quota and the independent construction of §4 applies by its verified triple count. In all cases set $b=(p-p_0)/2$ and $a=((q-q_0)-(p-p_0))/2$. They are nonnegative integers because the baseline and target are both odd at each host. The resulting row construction supplies precisely $(p,q)$. For the principal odd $r\ge17$, every residue case and every physical order are thus covered. Necessity from §1 gives the exact threshold.

The same formulas give the following smaller-domain observations without additional allocation work. For $r=11,15$ all admissible splits meet a nonreversed baseline selection. For $r=9,13$ the ordinary cases are supplied, leaving the larger equal targets $p=q>M$ open by these rules. For $r=7$, the baseline $(3,7)$ supplies targets with $q-p\ge4$ at or above threshold. The ordinary equal baseline $(5,5)$ would need three regular shifts and only two are present. At $r=5$ the baseline $(3,5)$ and its tail anchor supply all unequal pairs at or above threshold, leaving larger equal targets open by these rules. Below-threshold necessity applies in all these smaller stated domains. These observations are limited to the displayed constructions. Quota-one cases remain separate.

## 6. Named placement, exact full and partial inventories

At the full target size choose the actual roles and selected exterior indices as above. An independently calculated baseline is a prescription of arrows at those same named hosts. Assign its arrows to the requisite number of actual residual terminal indices at each host, using their order within each host. The counts $p_0\le p$, $q_0\le q$ give enough actual indices. Translate each baseline arrow at its same actual parent and move the anchored arrow at its original first parent. Supply growth arrows at $P,Q$ to their remaining actual indices. No new vertex is introduced outside the specified original. The oriented numerical baseline counts are admitted since the input size is enough for the full target, with $K=K_0+\lambda$. All selected terminals and the direct leaf keep their actual original incidences. The prescription terminates by finite parameter arithmetic and scans of the named original, and it is independent of any target solution.

Every noninitial, unmodified old folded coordinate increases by $\lambda$ in its row. Since the final $J$ has increased by $2\lambda$, an old H index $j$ now unfolds to $J_0+2\lambda-(j+\lambda)=J_0-j+\lambda$. An old translated L index gives its old numerical coordinate plus $\lambda$ as well. The four initial L cells stay fixed, and the balanced move sends the anchored L source and image to $4+a,4+\delta+a$ after the last Q-only strip. Thus the final H coordinates, source cut $k$, and image threshold $K$ are computed in the full enlarged numerical alphabets. Each folded row bijection verified above yields a complete numerical one. The new $x$ is the number of added lower sources assigned to upper hosts, $2b+a=\lambda$. The baseline $y=r-2+h$ first-host upper sources is unchanged. This gives $x+y=s-K$ and also the independent count $1+r+R=2(A+\lambda)$. Every gap arrow's crossing status is the one dictated by its final row and actual host. The new lower-source upper assignments contribute crossing weights to the remaining first-section inventory.

To give the exact first-host resources, compute the baseline numerical sets $I_0,M_0$ of actual gap coordinates and their images from the odd-tail and regular prescriptions, including $E_0=[0,3]$. The image at each actual first parent is its source plus its own $\delta$. Define $T_\lambda(D)=E_0\sqcup((D\setminus E_0)+\lambda)$ for such a numerical set. The exact final first-host sets, by the unfolding and the anchor move just verified, are
$$
\begin{array}{ll}
b=0:\quad I=T_\lambda(I_0), & J_1=T_\lambda(M_0),\\[1mm]
b>0:\quad I=(T_\lambda(I_0)\setminus\{4+\lambda\})\sqcup\{4+a\},&
J_1=(T_\lambda(M_0)\setminus\{4+\delta+\lambda\})\sqcup\{4+\delta+a\}.
\end{array}
$$
These are disjoint unions of the sets actually used at the first hosts, not the entire L row after growth. Their exact complements are $I',J_2$ in $[0,s-1]$.

For the final original set $C=c+K$ and shift old oriented labels by $A$ below $c$ and by $A+s$ at or above $c$. Side memberships are preserved. Give numerical gap coordinate $i$ label $A+c+i$, and add $n+s$ to each upper reduced exterior label. All exterior edges cross and gain $n+s$ because their lower labels are at most $A<C$ and their upper labels at least $n+s+A+1>C$. The old shared $v$ agrees with its reduced exterior label $A$. The full palettes are
~~~text
old labels    [A,A+c−1] ⊔ [A+c+s,n+s+A]
fresh labels  [0,A−1] ⊔ [A+c,A+c+s−1] ⊔ [n+s+A+1,m]
old weights   [1,d−2] ⊔ [d−1+s,n+s]
fresh weights [d−1,d+s−2] ⊔ [n+s+1,m].
~~~
The unions are disjoint. Old noncrossing differences remain fixed and old crossing differences gain $s$. The exact numerical gap bijection and the raw exterior spectra fill the fresh intervals. Gap crossing weights are $[d+K-1,d+s-2]$ and gap noncrossing weights are $[d-1,d+K-2]$. Thus actual vertex labels and actual edge differences are exactly $[0,m]$ and $[1,m]$ bijectively. The final crossing spectrum is $[d+K-1,m]$, its noncrossing counterpart is $[1,d+K-2]$, and $w=0$, $m=2C+2$. This is the exact oriented $S_{-1}$ return along the original extended witnessing spine.

In the first section the fresh exterior label set is $E_1=[2,A-1]\sqcup\{n+s+A+1,n+s+A+3\}$. The remaining fresh exterior label set is $E_2=\{0,1,n+s+A+2,n+s+A+4,n+s+A+5\}$. Their actual difference sets are $n+s+[1,A]$ and $n+s+[A+1,A+5]$. With $L_{\rm old},D_{\rm old}$ from the full palettes, both exact boundary inventories are
~~~text
used labels         L_old ⊔ E₁ ⊔ (A+c+I)
remaining labels    E₂ ⊔ (A+c+I′)
used differences    D_old ⊔ (n+s+[1,A]) ⊔ (d−1+J₁)
remaining weights   (n+s+[A+1,A+5]) ⊔ (d−1+J₂).
~~~
Old used labels are separated by their two old bands, and exterior labels by their reduced sides. For each of $I,I'$ the source cut partitions are their intersections with $[0,k-1]$ and $[k,s-1]$, translated by $A+c$. Both exterior weight bands cross. For each of $J_1,J_2$, intersect with $[K,s-1]$ for crossing weights and $[0,K-1]$ for noncrossing weights before adding $d-1$. The used weights additionally include the exact old crossing and noncrossing bands. In particular the remaining crossing set includes the new L-source upper-host contributions and the second exterior band. Its literal unfinished original connector $uw$ has oriented endpoint labels $(n+s+A+1,0)$ and crossing weight $n+s+A+1$.

For actual maximum polarity use input $n-G$ and complement the output about $m$. The actual input and output cuts become $n+1-c$ and $m+1-C$. The actual lower and upper shifts are $B,B+s$ in maximum polarity and $A,A+s$ in minimum polarity, by $2K=A+B+s$. This complements the label inventories and exchanges their sides. It preserves all differences and crossing statuses, gives actual maximum frontier $w=m$ and assigns the literal connector endpoints $(4,m)$.

For an individually admitted finite sequence keep every actual evolving cut, spectrum, physical port and size premise. With actual completed cut $C_i$ and sums $T_i,S_i$ of later actual lower shifts and gap widths, later side-preserving lifts give exact final labels $x+T_i+S_i\mathbf 1_{x\ge C_i}$. Actual crossing differences gain $S_i$ and noncrossing ones stay fixed. The same maps lift each used first-section resource inventory and both endpoints of its literal unfinished crossing connector. Final remaining resources are exact complements in the final alphabets. Induction gives the named graceful bijections at the admitted returns. Finite backward sums and scans of the actual original indices give immutable final-alphabet emission. The independently supplied prefix and arbitrary-large admitted sizes remain subject to the retained [D157/D134 initializer premises](ORDINARY_SPINE_ALTERNATING_EXCEPTIONAL_SPECTRUM.md#7-independent-supply-cycle-closure-and-immutable-labels).

## 7. Accepted controls and stopping scope

D179 is Director accepted within its exact written scope at 947f4db5c5beb8f545a4e71ce553e8af50f5140e. Its even-second theorem and smaller limitations are preserved. D178's arbitrary-even first supplier and ordered-tail results, D175's H0 obstruction and D176's complete menu remain in their earlier exact scopes. The new odd-quota result is an H1 theorem under its stated placement, not a completeness claim about other geometries. The scoped parity negative for I-b and II-a concerns their fixed exteriors.

D177's accepted symbolic D174 projection still covers all 93 frozen all-even $R=8$ originals, including 92 historically unentered. D174 historically completed one matched pair and two numerical arms, stopped normally at its first verified separator and left 3,518 unentered. Its independent 74-edge prefix was checked by direct arithmetic on the frozen named data. [Custody](../evidence/validation/LCL_ORDINARY_SPINE_EXCEPTIONAL_ODD_SECOND_QUOTA_SUPPLIER_001/CUSTODY.json)

The explicit tail and growth rules resolve the principal odd-quota question symbolically. The secondary limits, quota-one cases, preassigned numerical roles and other first parities remain separate. No hybrid study is needed for this result.
