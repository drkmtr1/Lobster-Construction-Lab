# D178 — Arbitrary even first quotas on width-five exceptional exteriors

Task **LCL-ORDINARY-SPINE-EXCEPTIONAL-ARBITRARY-EVEN-FIRST-QUOTA-LIFT-001**.

**PROVED WITHIN EXACT WRITTEN SCOPE / PENDING DIRECTOR REVIEW.** On the stated D157 input, every odd $r\ge5$ and every ordered first inventory of $r$ positive even quotas with at least one quota at least four have an independent named $S_{-1}$ supplier for each positive even second split of $r+3$. Both numerical second roles are selectable. The actual second direct leaf stays exterior. The construction uses II-a at smaller second quota two and I-a otherwise, with selectable numerical tail roles. Section 5 gives a scoped obstruction for some fixed II-a tail orders and an exact finite-state criterion for the separated-tail model.

## 1. Original, exterior and exact alphabets

All quantities are exact integers, excluding booleans. Intervals are inclusive, with a reversed interval empty. Retain the [D157 $S_{-1}$ placement](ORDINARY_SPINE_ALTERNATING_EXCEPTIONAL_SPECTRUM.md#1-interface-and-exact-inventory-rule). The independently supplied named graceful prefix has $n=2c+2$ edges, actual extreme frontier $v$, cut $c$ in orientation $G(v)=0$, $d=c+2$, crossing differences $[d-1,n]$ and noncrossing differences $[1,d-2]$. The old graph and witnessing spine remain intact. Append original spine vertices $u,w$. The first section has $r\ge5$ odd positive centers with even quotas $\alpha_i\ge2$, including a quota at least four, and no direct leaf. The second section has two actual positive even quotas of sum $R=r+3$, and the sole actual direct leaf at $w$. Write $F=\sum_i\alpha_i$. The fresh size counts two spine vertices, $r+2$ centers, that direct leaf and $F+R$ terminals. It is $2K=F+2r+8$. Require $n\ge2K$ and put $m=n+2K$.

Give the smaller second full quota $p$ to $P$ and the larger $q$ to $Q$, using original index order in a tie. Use $A=r+2,B=5$, $v=A,u=A+1,w=0$ and $Q=A+2$. These are the same actual incidences and raw exteriors as [D176 I-a and II-a](ORDINARY_SPINE_EXCEPTIONAL_ODD_FIRST_CENTER_H1_MENU.md#2-complete-geometry-reduction-and-raw-spectra). The original first centers take lower slots $[1,A-1]\setminus\{t_0\}$. One actual center of quota at least four takes the neutral slot $A-1$. The other roles are assigned below. Use the first actual indexed terminal at each parent selected for an exterior terminal.

| Exterior | $p$ | $t_0$, label of selected terminal at $P$ | First terminal and parent | $P$ | Actual direct leaf at $w$ | Upper separation $\rho$ |
| --- | ---: | ---: | --- | ---: | ---: | ---: |
| II-a | 2 | 2 | $A+3$ at 4 | $A+5$ | $A+4$ | 3 |
| I-a | $\ge4$ | 1 | $A+3$ at 3 | $A+4$ | $A+5$ | 2 |

Each exterior fills $[0,A+5]$, and its edges connect the named crossing subtree through the three spine vertices and actual centers. In I-a the first spine and center edges use $[1,A-1]$ and the selected first terminal adds $A$. In II-a the first spine and center edges use $[1,A]\setminus\{A-1\}$ and the selected first terminal adds $A-1$. The second section uses $A+1$ at $uw$, $A+2$ at $wQ$, $A+3$ at the selected $P$ terminal, and $A+4,A+5$ on the remaining two attachments at $w$. The exterior differences are exactly $[1,A+5]$, and all are crossing. These raw suppliers need only the stated role and quota premises.

Put $h=F/2-r-1\ge0$. Subtracting the exterior widths gives
$$
K=2r+5+h,\quad s=2K-A-B=3r+3+2h,\quad k=K-A=r+3+h,\quad J=s+3.
$$
The inequalities $K-A-B=r-2+h\ge3$, $s\ge K$ and $A\le K\le A+s$ give the required width and side admission. At gap coordinate $i\in[0,s-1]$ the actual oriented label is $A+c+i$, physically lower iff $i<k$. From the actual expanded endpoint subtraction, its difference is $d-1+\pi(i)$ with
$$
\pi(i)=i+\delta,\quad \delta=A-1-j_0 \quad\text{at lower host }j_0,\qquad
\pi(i)=s+b+1-i \quad\text{at upper host }A+b .
$$
The fold $L_j=j$, $H_j=J-j$ gives exact row alphabets
$$
\begin{array}{c|cc}
&L&H\\
\text{sources}&[0,r+2+h]&[4,2r+3+h]\\
\text{images}&[0,2r+4+h]&[4,r+1+h].
\end{array}
$$
Unfolding the H sources gives $[k,s-1]$, and unfolding the H images gives $[K,s-1]$. Each alphabet partitions $[0,s-1]$ into its own two numerical intervals. A lower host shifts an L index by $+\delta$ and an H index by $-\delta$. Upper hosts exchange rows. The index is unchanged at $Q$ and changes by $-\rho,+\rho$ in L-source and H-source order at $P$. Thus for each legal arrow the H image is exactly the crossing case, since it occurs iff source and parent occupy opposite physical sides.

Root the new graph colors at lower $v$. The lower fresh class is $w$, the $r$ first centers and the $R$ second terminals, of size $1+r+R=2r+4$. The upper fresh class consists of all first terminals, $u$, the two second centers and the actual direct leaf, of size $F+4$. In a compatible placement let $x$ count lower sources at upper hosts, and $y$ upper sources at lower hosts. Exactly $s-K$ images are crossing. There are $s-k-y+x=A+2x$ gap leaves at upper hosts by $x+y=s-K$. The fresh lower class therefore has $A+(A+2x)=2(A+x)$, because the connected crossing exterior has those graph colors and residual leaf colors are opposite their host. Here $A=r+2$, agreeing with the one selected exterior second terminal and the $r+1$ lower spine/center vertices, so $x=0$. In the supplied allocation all L sources use lower hosts and all H images come from H sources at lower hosts. The four smallest images force the four initial neutral matches by the same minimum-image induction as D175, since positive nonneutral shifts cannot fill the next smallest image from an unused source and every upper-host image is at least four. The neutral quota can exceed four, so this argument makes no exhaustion claim.

## 2. Arbitrary neutral and regular expansion

Denote the neutral quota by $4+2h_N$. Give $L_0,\ldots,L_3$ to the neutral host with their identical images. Prepend $h_N$ ordinary pairs of shift zero, matching $L_j\to L_j$ and $H_j\to H_j$ at positions $j=4,\ldots,3+h_N$. They give the extra $2h_N$ leaves at that actual host. All these H indices exist in both H windows by $h_N\le h$, and the paired columns are above the initial L matches. The common holes at these columns are removed from the upper matching.

The regular positive displacements in either exterior are $[1,r-5]$. Let $h_R$ be the sum of $(\alpha-2)/2$ over the actual hosts assigned to these displacements. The four remaining positive displacement roles are the tail roles. Let $h_T$ be the sum of $(\alpha-2)/2$ over their full quotas including the one selected terminal. Then
$$
h=h_N+h_R+h_T .
$$
At an ordinary regular host of quota $2+2a_\delta$ give successive positions to $a_\delta+1$ matched pairs
$$
L_j\to L_{j+\delta},\qquad H_{j+\delta}\to H_j .
$$
There is one common reservation column $j+\delta$ per pair. Arbitrary repetition adds distinct successive columns and the correct two new leaf incidences per pair.

If $p=2$ the entire regular strip uses ordinary pairs. Otherwise write $p=4+2a$ and form $a$ consecutive triples of distinct shifts using the first $3a$ regular shifts. Since $p\le(r+3)/2$, we have $3a\le3(r-5)/4\le r-5$. All required triples exist. On a triple $\delta,\delta+1,\delta+2$ with full quotas $(2+2a_1,2+2b_1,2+2c_1)$, set $\ell=3+b_1$. In its central block beginning at position $j$, take the first two L shifts to be $\delta$ and all remaining $\ell-2$ to be $\delta+1$. Take the first $\ell-2$ H-image shifts to be $\delta+1$ and the last two to be $\delta+2$. With $z=j+\delta$, the two sets of reserved intermediate columns are exactly
$$
X'=z+(\{0,1\}\cup[3,\ell]),\qquad
Y=z+([1,\ell-2]\cup\{\ell,\ell+1\}),
$$
where $X'$ denotes L images and $Y$ reserved H sources. Indeed each L column is its consecutive position plus its displayed shift, and each reserved H source is its image position plus its shift. In the encompassing interval $[z,z+\ell+1]$ the surviving H sources are exactly $z,z+\ell-1$ and the surviving L images exactly $z+2,z+\ell+1$. Thus the two $P$ arrows $H_z\to L_{z+2}$ and $H_{z+\ell-1}\to L_{z+\ell+1}$ give the exact residual bijection, including $\ell=3$. Used H sources and L images are distinct in their own alphabets. The central quotas are $(2,2+2b_1,2)$.

Prepend $a_1$ ordinary pairs at shift $\delta$ and append $c_1$ ordinary pairs at shift $\delta+2$ at the immediately neighboring positions. Their common-hole columns end at $z-1$ and start at $z+\ell+2$, respectively. They lie strictly outside the central footprint and leave its two shifted assignments intact. The totals at the three actual hosts are the intended full quotas. This verifies independent arbitrary growth in the three capacities, including empty prepended and appended sequences.

Process the neutral and successive regular groups by increasing shift group and assign their consecutive positions in order. Every group's intermediate columns and $P$ paths are contained between its first position plus its smallest shift and its last position plus its largest shift. Successive groups increase in positions and in allowed shifts, so these enclosing intervals are disjoint. Every ordinary pair has equal H-source and L-image holes and contributes no $P$ arrow. The positive regular positions are $[4+h_N,r-2+h_N+h_R]$. The neutral and positive regular intermediate columns all lie in $[4,2r-7+h_N+h_R]$, also when the regular strip is empty. The upper bound follows from last position plus $r-5$ for positive regular groups and from $3+h_N$ for neutral pairs. This proves all window and nonintersection claims. The strip uses no shifted upper assignment in II-a and exactly $2a$ in I-a.

## 3. Separated special-tail coordinates and the bounded-tail lift

Write $h_*=h_N+h_R$, $t=h_T$, $D_*=2r+h_*$ and $N=t+2$. The remaining L-source and H-image positions are $r+h_*+x$ with $x\in[-1,N]$ and $x\in[-1,N-1]$, respectively. A tail shift $\delta$ has deficit $d_0=r-\delta$. An L image from position $x$, or an H source for H image position $x$, is at column $D_*+x-d_0$. In the rest of this section and §4 tail columns are stated as offsets from $D_*$. The H-source window is $[-5,N+1]$ and the L-image window $[-5,N+2]$. They are a designated terminal subinterval of the larger alphabets, disjoint from all earlier footprints, whose maxima are at most $D_*-7$. We have $D_*-5\ge5$ so their minima lie above the first neutral L images and inside the nonlocal windows. The cell $N+2$ is a genuine L image and an absent H source. The exterior deficits for the two geometries are
$$
\text{II-a: }\{0,2,3,4\},\ \rho=3,\ \text{selected first terminal at deficit }3;
\qquad
\text{I-a: }\{1,2,3,4\},\ \rho=2,\ \text{selected first terminal at deficit }2.
$$
These come from the exact reduced first labels. The required counts at those four actual hosts are their full even quotas, less the single exterior terminal at the specified host.

Let $X',Y$ be the distinct L-image and H-source reservations from the tail positions. The surviving H sources are $S=[-5,N+1]\setminus Y$ and L images are $D=[-5,N+2]\setminus X'$. The exact tail criterion is a set $U\subseteq S$ of shifted sources with $U+\rho\subseteq D$, $|U|=1$ for II-a or 3 for I-a, and
$$
S\setminus U=D\setminus(U+\rho).
$$
Assign the displayed shifts at $P$ and all residual coinciding indices at $Q$. These are legal H-to-L arrows, and the equality is both necessary and sufficient for that separated residual bijection.

If one neutral and four other actual hosts of quotas in $\{2,4\}$ can be chosen, the four tail hosts may first be arranged exactly as in [D177's six cores and prepend schedules](ORDINARY_SPINE_EXCEPTIONAL_ODD_FIRST_CENTER_QUOTA_EXPANSION.md#3-special-tail-patterns-for-every-remaining-quota-multiplicity), using $t$ equal to their count of fours. Their exact local windows and assignments are the same as above. The unchanged offsets translate by $h_*$ compared with the unexpanded regular/neutral boundary, while the folded high endpoints advance by $h_*+t=h$. Unfolding uses the actual $J=3r+6+2h$, so its numeric H sources and images are exactly those in §1. Thus this is already a complete bounded-tail supplier with arbitrary even regular and neutral magnitudes. The six core lists and ten published schedules were also checked by direct arithmetic on those retained lists. Next we remove the bounded-tail premise.

## 4. Arbitrary selectable tail quotas

Write the four full tail quotas as $2+2u_d$. Then $t=\sum_d u_d$. After the chosen neutral and any four other actual centers are designated, the four tail quota values may be put in the numerical deficit roles as follows. There is no restriction on their original physical order. All rules assign deficits in the L positions and H-image positions, and every resulting intermediate column is computed as $x-d$ from its actual position.

Two elementary ways to fill consecutive positions will be used. An ordinary pair at a shared position $x$ with one deficit $d$ in each row reserves a common column $x-d$. For a sequence of these pairs with nonincreasing deficits, the used columns are strictly increasing. For constant $b$, a consecutive group in one row can also reserve exactly its position set translated by $-b$. In II-a use $b=1$: for $d=2$ or 3, a group of $d$ positions with deficits $(0,\ldots,0,d)$ has columns equal to that translate. Indeed the first $d-1$ positions give unchanged columns and the final position gives the column one below the first. In I-a use $b=2$: deficits $(1,3)$ or $(1,1,4)$ give exactly the position set translated by $-2$. For either group the first one or two positions give their columns minus one and the last gives the column two below the first. A single position at deficit 2 also gives the translate by $-2$. Thus the groups can be concatenated with disjoint translated interval images. Below L and H groups may differ but start at the same common position, preserving the asserted interval images.

### 4.1 II-a

Assign a smallest quota to deficit 0. Then $u_2\ge u_0$. The other deficits can be assigned by their physical index among remaining choices.

If $u_0=u_2=0$, use the retained unpromoted D175/D177 core. Its L-deficit list is $(0,4,0,4)$ and H-image list $(3,2,2)$ at positions beginning at $-1$. The resulting $X'=\{-4,-2,-1,1\}$, $Y=\{-4,-2,-1\}$ and $U=\{1\}$ satisfy the exact criterion at $t=0$. Prepend all extra pairs of deficits 4 and 3 in that order. For $e$ such pairs, the largest of their columns is at most $e-5$, while the translated core has minimum column $e-4$. The shifted last image is precisely the absent H-source cell of the enlarged window, and the one shifted assignment is preserved. This supplies all $u_3,u_4$ in this case.

If $u_0=0$ and $u_2\ge1$, take the retained D177 core with one promotion at deficit 2:
$$
L:(2,4,2,0,2),\qquad H:(2,4,0,3).
$$
At positions beginning $-1$, the first two positions in both lists reserve columns $-3,-4$. All other positions start at 1 and reserve columns at least $-1$. Their L images differ from the H reservations by the single column 2, with one $P$ shift $2\to5$. Insert $v_2=u_2-1$ ordinary pairs of deficit 2 at positions $[1,v_2]$ and translate the old positions at least 1 and their columns by $v_2$. The inserted holes are $[-1,v_2-2]$, while the shifted right part begins at intermediate column at least $v_2-1$. Disjointness with $-3,-4$ and with the shifted right part is exact. The single $P$ shift is now $2+v_2\to5+v_2$, ending at the absent H-source cell. The full quota at deficit 2 increases by exactly $2v_2$. Then prepend any extra pairs of deficits 4 and 3 as in the preceding case. The minimum core column remains $-4$ before that prepend. This verifies its windows and all arbitrary capacities.

If $u_0\ge1$, reserve a right portion beginning at a shared position $j_0$ to consume all $2+2u_0$ zero-deficit leaves. In its L list use $u_0+1$ groups $(0,2)$, and in its H list one group $(0,0,3)$ plus $u_0-1$ groups $(0,2)$. The lengths are $2u_0+2$ and $2u_0+1$. The combined deficit counts are $2u_0+2$ at 0, $2u_0$ at 2 and one at 3. The selected exterior terminal at deficit 3 makes the remainder at 3 even. All remaining physical capacities are nonnegative even counts at 2, 3 and 4 since $u_2\ge u_0$. Use them as ordinary pairs in the shared prefix of positions, in order of decreasing deficit. The total positions then have the required lengths $4+t,3+t$ since they use all $7+2t$ residual leaves and differ by one. In particular the final offsets are $N,N-1$.

Every prefix pair reserves a column at most $j_0-3$. The right portion in the two rows reserves the intervals $[j_0-1,N-1]$ and $[j_0-1,N-2]$ respectively by the translated groups. These are disjoint from the preceding holes. All reservations are in the stated windows because every deficit is at most four and every position is at least $-1$. Therefore $X'=Y\sqcup\{N-1\}$. The exact residual match uses the one $P$ shift $N-1\to N+2$ and uses $Q$ by identity elsewhere. This verifies the tail for every multiset of four positive even quotas in II-a.

### 4.2 I-a

Assign a smallest quota to deficit 1. If this quota is two and any remaining quota exceeds two, assign one such larger quota to deficit 3. Otherwise assign the unspecified roles using original index order. If all four quotas are two, use the unpromoted D176/D177 core with lists
$$
L:(1,4,4,2),\qquad H:(3,1,3).
$$
It gives $X'=\{-4,-3,-2,0\}$, $Y=\{-4,-2,-1\}$, and $U=\{-3,0,2\}$, satisfying the criterion at $t=0$.

For every other case consume all $2+2u_1$ deficit-1 leaves in a right portion of effective deficit 2. Use identical collections of groups in the two rows, followed by one additional L position of deficit 2. The fixed selected terminal at deficit 2 is exterior, so the other residual leaves at that host come in pairs. There is also a two-position part earlier, with L deficits $(4,4)$ and H deficits $(3,3)$, consuming two leaves from each of those hosts. After taking those leaves, the available counts at 3 and 4 are $2u_3,2u_4$.

If $u_3\ge u_1+1$, take $u_1+1$ groups $(1,3)$ in each right row. They consume exactly $2+2u_1$ leaves at deficit 1 and the same count at 3. If $u_3=u_1\ge1$, take $u_1-1$ groups $(1,3)$ and one group $(1,1,4)$ in each right row. They consume the same quota at 1 and consume $2(u_1-1)$ at 3 and two at 4. Since the smallest quota was assigned to 1, $u_4\ge u_1\ge1$. These are the only cases needed: if $u_1=0$ and some quota exceeds two, the role choice made $u_3\ge1$. After the shared right groups, the extra L position at deficit 2 and the selected exterior terminal, all remaining counts are nonnegative even counts at 2, 3 and 4.

Use all remaining deficit-4 leaves in ordinary pairs first. Immediately after these pairs put the two-position part just described at positions $x,x+1$. Its L columns are $x-4,x-3$ and its H columns $x-3,x-2$. They give one shifted upper arrow from $x-4$ to $x-2$, and the common hole $x-3$ is between opposite residues. Earlier pairs have maximum column $x-5$ or less. Use all remaining ordinary pairs of deficit 3 and then deficit 2 after this part. Their least possible column is $x-1$, above its footprint, and their columns are strictly increasing. Then place the right groups from the next shared position $j_0$, followed on L only by its extra position at deficit 2. The lengths of the two position rows differ by one and their sum is $7+2t$, so their ends are $N,N-1$ as claimed.

The right reservation intervals are $[j_0-2,N-2]$ on L and $[j_0-2,N-3]$ on H. Any intervening ordinary prefix pairs have largest column at most $j_0-3$. If there are none after the two-position part, then $j_0=x+2$ and its maximum column $x-2$ is below $j_0-2$. Hence the isolated interior shift meets no other reserved cell or shift path. The remaining two $P$ arrows are $N-2\to N$ and $N\to N+2$. The target $N+2$ is the absent H-source cell, the intermediate column $N$ is in both row windows and unreserved, and $N-2$ is an L reservation but an available H source. The two paths and common holes account for every mismatch. All other residual indices use $Q$ by identity. Thus all quotas and windows are exact for every multiset also in I-a.

## 5. Fixed-order tail scope and an exact state criterion

Selectable roles in §4 permit any four physical tail quota values. For preassigned deficits the separated support need not be universal. In II-a with one shifted arrow, the final target $N+2$ forces $U=\{N-1\}$. No lower reservation can reach $N+2$ and that cell is absent from the H sources, so $X'=Y\sqcup\{N-1\}$. Because $d_0\ge0$ and the final H-image position is $N-1$, every L reservation is at most $N-1$.

For each cutoff $j\in[-1,N]$, some L assignment at position $x\ge j$ must reserve $x-d_0<j$. Otherwise the assignments from $[j,N]$ would occupy the entire interval $[j,N]$ by injectivity, including the impossible column $N$. A displacement of deficit $d_0$ can cover at most $d_0$ cutoffs. Therefore $t+4\le\sum_L d_0$. The residual index moment is
$$
\rho|U|=2+\sum_L d_0-\sum_H d_0 ,
$$
by subtracting the sums of the surviving H sources from those of surviving L images. The unmatched final row endpoint contributes $N+2$, while the extra L position contributes $-N$ in the difference of the reservation sums. In II-a $\rho|U|=3$ and the combined deficit sum is $15+2(2u_2+3u_3+4u_4)$. Hence $\sum_L d_0=8+2u_2+3u_3+4u_4$, yielding the necessary bound
$$
u_0\le4+u_2+2u_3+3u_4.
$$
For instance $u_0\ge5$ with all other $u_d=0$ is excluded in this preassigned separated II-a tail. The obstruction concerns this ordered architecture. The selectable construction assigns the smaller quota to deficit 0.

For completeness the following finite column language recognizes the **exact** support for either preassigned separated tail. Scan offsets decreasing from $N+2$ to $-5$. A finite phase records the column types: the first two columns have neither position, the third has only an L position, the next $t+3$ columns have both positions (at least three), and the last four have neither position. The first column is the sole absent base H source. All columns are base L images. These flags reproduce $[-1,N]$ and $[-1,N-1]$ exactly as position windows.

1. At each position, choose one of the fixed deficits of the given geometry and mark its reservation in the corresponding L-image or H-source mask. Each mask contains distances $0,1,2,3,4$ from the current column. A new reservation at distance $d_0$ is rejected if already set in that mask. A zero distance is inserted before testing current availability. Since the scan is decreasing, no future assignment can reserve the current column. Marks at a nonexistent baseline cell are rejected when processed. Consume current marks and advance the masks one column, rejecting any pending marks beyond the end.
2. Compute $S_j,D_j$ as the binary surviving source and image flags at column $j$. Store the pending bits $B_j$ for shifted sources from the previous $\rho$ columns of the scan, initialized to zero at the right boundary. The [D168 H-to-L recurrence](ORDINARY_SPINE_EXCEPTIONAL_TWO_UPPER_HOST_RESIDUE_COMPRESSION.md#4-exact-residue-path-criterion) is $D_j=S_j-B_j+B_{j-\rho}$. Check $0\le B_j\le S_j$ and enqueue $B_{j-\rho}=D_j-S_j+B_j$ only if binary. Count each used $B_j=1$ with an upper bound of 1 or 3 as specified. At the end require the exact count and all pending bits zero.
3. Assign to each transition the four occurrence counts of its position assignments. Accept only when these sum to the requested four full quotas with the one exterior terminal subtracted. For a fixed request they determine the number $t+3$ of columns of the variable phase, because the total number of counted positions is $7+2t$. The phase also enforces both boundary markers and the minimum three.

The two masks are sufficient because all lower deficits are at most four and no earlier mark can extend farther than the next four columns. The residual queue is sufficient because only the $+\rho$ shift and identity meet an image. The phase, masks, queue and bounded shifted count are finite, independent of $t$ and of the occurrence totals. Every actual separated allocation chooses a path with its own marks and residue bits, which satisfy all the tests. Conversely an accepted path gives distinct actual reservations in both valid windows, the physical deficit occurrences and one legal incoming arrow at each residual image by the recurrence. Recording its transitions extracts the actual deficits and shifted sources. For a fixed quota vector the finite path of prescribed length can be found by exact reachability with remaining occurrence counts recorded, and backtracking one predecessor path gives the construction.

The language also gives a semilinear description of ordered support on the positive even full quotas. To impose that domain in the language itself, keep the parity and the count truncated at two for each host, initialized with the exterior terminal contribution. Update these finite registers at each counted occurrence and accept only when each is even and its truncated count is two. Eliminate states to express accepting paths by finite union, concatenation and star on transition symbols. Under additive occurrence weights those operations become union, addition of sets and finite-repetition closure. A finite union of sets $b_i+\mathbb N P_i$ with finite period sets $P_i$, where $\mathbb N P_i$ denotes all nonnegative integer sums of their vectors, is closed under all three operations. For the star, fix the subset of component types actually used. Take one copy of each used base, then add any nonnegative sum of their bases and periods, assigning each period to a copy of its own type. The empty subset gives zero. This proves the closure and therefore the finite semilinear description, shifted by the single exterior terminal. This criterion is for the separated ordered tail. No numerical support computation, enumeration, or new trial is needed for §4.

## 6. Whole assignment, exact inventories, and composition

Choose one actual neutral of quota at least four, choose four other actual centers for the tail (all may be unbounded), and assign the remaining $r-5$ to successive regular shifts in physical index order. In any numerical role tie use physical indices. Assign the designated terminal exterior indices exactly as in §1. The four initial neutral L positions, the neutral extra pairs, the regular strip and the tail exhaust the L source row. The latter three fill the entire H image row. The ordinary, active-block and tail footprints are pairwise disjoint, and their verified exact upper matching covers every residual H source and L destination. Any coinciding unaffected indices between the footprints go to $Q$ by identity. The upper shifted count is 1 in II-a and $2a+3=p-1$ in I-a. The H source row has $2r+h$ cells and its H-image reservations consume $r-2+h$, leaving $r+2$ actual upper-host terminals. Of these $p-1$ go to $P$ and $r+2-(p-1)=q$ to $Q$. The selected $P$ terminal restores full quota $p$. The lower assignments and selected first exterior terminal give each actual full first quota. All L assignments are noncrossing. The $r-2+h=s-K$ H assignments at lower hosts cross and all residual H assignments at upper hosts are noncrossing.

At each named physical host assign its increasing actual remaining terminal indices to that host's increasing numerical source coordinates. The original direct leaf keeps its one exterior assignment and the selected terminals keep their original incidences. These rules are finite scans, exact arithmetic and the explicit lists. They terminate on the given original without a search.

With output cut $C=c+K$, shift old oriented labels by $A$ below $c$ and by $A+s$ otherwise. This preserves their old side memberships. Give each gap leaf its oriented label $A+c+i$, and add $n+s$ to each upper reduced exterior label. The shared $v$ is labeled $A$ and the exterior edges cross, with old endpoint $v$ and fresh lower endpoints below $C$, and expanded upper exterior endpoints above $C$. The exact palettes are

~~~text
old labels    [A,A+c−1] ⊔ [A+c+s,n+s+A]
fresh labels  [0,A−1] ⊔ [A+c,A+c+s−1] ⊔ [n+s+A+1,m]
old weights   [1,d−2] ⊔ [d−1+s,n+s]
fresh weights [d−1,d+s−2] ⊔ [n+s+1,m].
~~~

The gap and exterior bijections fill the fresh bands exactly. Old crossing weights gain $s$ and old noncrossing weights stay fixed. The gap crossing weights are exactly $[d+K-1,d+s-2]$ and the gap noncrossing weights exactly $[d-1,d+K-2]$. Thus all named vertex labels form $[0,m]$ bijectively and all actual differences form $[1,m]$ bijectively. The full crossing spectrum is $[d+K-1,m]$ with noncrossing spectrum $[1,d+K-2]$. Since $w=0$ and $m=2C+2$ the exact oriented return is $S_{-1}$ on the original extended witnessing spine.

Now let $Y$ be the complete H-source reservation set at first hosts and $X'$ the noninitial L-image reservation set at those hosts, in the full folded indices, including the neutral extra pairs. For a set $S$ write $J-S=\{J-j:j\in S\}$. The first-section gap source and image sets and their complements are
$$
\begin{aligned}
I&=[0,k-1]\sqcup(J-Y), & I'&=J-([4,2r+3+h]\setminus Y),\\
J_1&=[0,3]\sqcup X'\sqcup[K,s-1], & J_2&=[4,2r+4+h]\setminus X'.
\end{aligned}
$$
The exact sets on each first host are defined by the allocations, and its numerical images are its source set plus its own $\delta$. Their disjoint unions give $I,J_1$. The complementary gap coordinates $I'$ are all upper and $J_2$ contributes only noncrossing differences. For the chosen exterior let $b_P,b_D$ be the upper indices of $P$ and the actual direct leaf. The first and remaining fresh exterior label sets are
$$
E_1=([1,A-1]\setminus\{t_0\})\sqcup\{n+s+A+1,n+s+A+3\},\qquad
E_2=\{0,t_0,n+s+A+2,n+s+A+b_P,n+s+A+b_D\}.
$$
Their exact difference sets are $n+s+[1,A]$ and $n+s+[A+1,A+5]$. With $L_{\rm old},D_{\rm old}$ the exact old palettes above, the intermediate resources are

~~~text
used labels         L_old ⊔ E₁ ⊔ (A+c+I)
remaining labels    E₂ ⊔ (A+c+I′)
used differences    D_old ⊔ (n+s+[1,A]) ⊔ (d−1+J₁)
remaining weights   (n+s+[A+1,A+5]) ⊔ (d−1+J₂).
~~~

Used lower labels comprise the old lower band, the lower part of $E_1$ and $A+c+[0,k-1]$. Used upper labels comprise the old upper band, the two upper first exterior labels and $A+c+(J-Y)$. The remaining lower labels are $0,t_0$ and all other remaining labels are upper. Used crossing differences are the old crossing band, the first exterior band and $d-1+[K,s-1]$. Used noncrossing differences are the old noncrossing band and $d-1+([0,3]\sqcup X')$. Remaining crossing differences are exactly the remaining exterior band, and remaining noncrossing differences are $d-1+J_2$. The literal unfinished connector $uw$ has endpoints $(n+s+A+1,0)$ with crossing weight $n+s+A+1$ in the remaining exterior band.

For maximum polarity use input $n-G$ and complement the output about $m$. The actual input and output cuts are $n+1-c$ and $m+1-C$. By $2K=A+B+s$, the actual lower and upper shifts become $B,B+s$, versus $A,A+s$ in minimum polarity. The label inventories complement and their sides exchange. Exact weights and crossing statuses are invariant. The maximum frontier is $w=m$ and the actual connector has endpoint labels $(4,m)$.

For each individually admitted finite sequence retain the old cut, all actual ports and edges, exact phases, spectra and size premises. In the actual polarity let $C_i$ be its completed cut at block $i$, and $T_i,S_i$ the sums of the respective later actual lower shifts and gap widths. Each later placement preserves the old memberships, so the final map on that boundary is $x\mapsto x+T_i+S_i\mathbf 1_{x\ge C_i}$. The final crossing weights from that boundary gain $S_i$ and noncrossing weights stay fixed. The same maps lift the first-section used inventories and both actual endpoints of its crossing unfinished connector. The final reserves are exact complements in the final alphabets. Induction gives the original named graceful bijections along the sequence. Finite backward sums and finite scans of the actual named incidences emit each label immutably in its final alphabet. Any arbitrarily large inputs used remain subject to the retained [D157/D134 independent initializer conditions](ORDINARY_SPINE_ALTERNATING_EXCEPTIONAL_SPECTRUM.md#7-independent-supply-cycle-closure-and-immutable-labels).

## 7. Accepted controls and boundary of the claim

D177 is Director accepted at c211d05c61d86f8f5aa870b93ff8665fd51858b8, including the theorem-derived 93-original D174 all-even $R=8$ projection on the frozen lattice. Ninety-two of those were historically unentered. D174's one completed pair, two numerical arms, normal separator stop and 3,518 historical unentered originals are unchanged. The admission receipt records the frozen identity and direct arithmetic checks on its prefix and the written D177 tail controls. [Custody](../evidence/validation/LCL_ORDINARY_SPINE_EXCEPTIONAL_ARBITRARY_EVEN_FIRST_QUOTA_LIFT_001/CUSTODY.json)

D178 supplies the entire requested ordinary positive domain via these two admitted named exteriors. The H0 obstruction and complete menu remain in the exact D175 and D176 domains. No H0 or all-exterior classification is inferred for first quotas greater than four. The fixed-order bound concerns only the separated II-a tail and leaves the other arrangements open. The new positive theorem closes the proposed objective symbolically, so no hybrid preparation or scientific run is needed.
