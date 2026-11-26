# D177 — Expandable odd first-center quota allocations

Task **LCL-ORDINARY-SPINE-EXCEPTIONAL-ODD-FIRST-CENTER-QUOTA-EXPANSION-001**.

**PROVED WITHIN EXACT WRITTEN SCOPE / PENDING DIRECTOR REVIEW.** In the declared D157 exceptional-return arrangement, for every odd $r\ge5$, every $1\le g\le r$, and every positive even second split of $r+3$, the inventory of $r-g$ twos and $g$ fours admits an independently constructed H1 return in every physical order with selectable numerical second roles. The independent regular quota expansions cover $g\le r-4$. Fixed tail patterns cover the four larger multiplicities. [D175](ORDINARY_SPINE_EXCEPTIONAL_ODD_FIRST_CENTER_DIRECT_PLACEMENT.md) excludes H0 on this entire domain, so each supplied original separates H1 from H0.

## 1. Original and exact row alphabets

All quantities are exact integers and all intervals are inclusive. A reversed interval is empty. Use the [D157 $S_{-1}$ input](ORDINARY_SPINE_ALTERNATING_EXCEPTIONAL_SPECTRUM.md#1-interface-and-exact-inventory-rule) on an independently supplied original named prefix, whose witnessing spine ends at the actual extreme vertex $v$. Orient its labeling $G$ with $G(v)=0$, $n=2c+2$ edges, cut $c$, $d=c+2$, exact crossing differences $[d-1,n]$ and noncrossing differences $[1,d-2]$. Labels equal to the cut are upper. Append actual spine vertices $u,w$, the ordered positive first centers with their prescribed terminal indices and no first direct leaf, and the two actual second centers and the single actual direct leaf at $w$. The second terminal total is $R=r+3$. Thus $F=2r+2g$, and two spine vertices, $r+2$ centers, the direct leaf and $F+R$ terminals give
$$
2K=2r+8+F,\qquad K=2r+g+4,\qquad m=n+2K,\qquad n\ge2K.
$$

Use only I-a or II-a in the [accepted D176 menu](ORDINARY_SPINE_EXCEPTIONAL_ODD_FIRST_CENTER_H1_MENU.md#2-complete-geometry-reduction-and-raw-spectra). In each, $A=r+2,B=5$, $v=A,u=A+1,w=0$. The smaller of the two full positive even second quotas is put at the selected parent $P$ and written $p$, and the larger is put at $Q=A+2$ and written $q$. In a tie use original physical index order. This numerical role choice works for either physical order. Let $t_0$ be the reduced label of the exterior terminal at $P$. The first centers occupy $[1,A-1]\setminus\{t_0\}$. Choose an actual quota-four center for the neutral role at $A-1$. All other actual first roles will be chosen to match the full quotas specified below.

| Geometry | $t_0$ | First exterior terminal | $P$ reduced label | Direct-leaf reduced label | Upper separation $\rho$ |
| --- | ---: | --- | ---: | ---: | ---: |
| II-a, $p=2$ | 2 | $A+3$ at parent 4 | $A+5$ | $A+4$ | 3 |
| I-a, $p\ge4$ | 1 | $A+3$ at parent 3 | $A+4$ | $A+5$ | 2 |

Use the first actual indexed terminal at each selected parent. The direct leaf is the unique prescribed actual direct incidence at $w$ and never uses a gap slot. The two exteriors fill $[0,A+5]$ and are connected crossing subtrees on the original edges. In I-a the first spine and center edges use $[1,A-1]$ and the selected first terminal gives $A$. In II-a these edges use $[1,A]\setminus\{A-1\}$ and the selected first terminal gives $A-1$. The second edge set comprises $uw$ of weight $A+1$, $wQ$ of weight $A+2$, the two edges at $P$ and the direct edge. In I-a those last three weights are $A+4,A+3,A+5$ and in II-a they are $A+5,A+3,A+4$. This gives $[1,A+5]$ exactly by direct reduced subtraction. All selected indices and edges exist with either first quota two or four at the selected parent.

Write $h=g-1$. Subtracting the exterior widths from $2K$ gives
$$
K=2r+5+h,\quad s=3r+3+2h,\quad k=K-A=r+3+h,\quad J=s+3.
$$
We have $K-A-B=r-2+h\ge3$, so $s\ge K$ and $A\le K\le A+s$. Under the D157 insertion the gap vertex at coordinate $i\in[0,s-1]$ receives oriented label $A+c+i$. It is physically lower iff $i<k$. Its actual edge difference is $d-1+\pi(i)$, where subtracting the original expanded endpoint gives $\pi(i)=i+\delta$ at a lower parent of reduced label $j_0$, with $\delta=A-1-j_0$, and $\pi(i)=s+b+1-i$ at an upper parent of reduced label $A+b$. In the lower case the gap label exceeds the parent, and in the upper case the expanded parent exceeds the gap label. The folded rows use $L_j=j,H_j=J-j$:
$$
\begin{array}{c|cc}
& L & H\\
\text{sources} & [0,r+2+h] & [4,2r+3+h]\\
\text{images} & [0,2r+4+h] & [4,r+1+h].
\end{array}
$$
Indeed the H source endpoints unfold to $[k,s-1]$ and the H image endpoints to $[K,s-1]$. The two rows of each alphabet partition all of $[0,s-1]$, with different numerical breakpoints $k$ and $K$. A lower host translates an L index by $+\delta$ and an H index by $-\delta$. The upper host $Q$ exchanges rows by identity of index and $P$ exchanges rows with $-\rho$ on L and $+\rho$ on H. Thus image H corresponds exactly to opposite physical sides, for each legal arrow. In particular H-to-L upper arrows are noncrossing.

The actual fresh graph color lower count is $1+r+R=2r+4=2A$. The D175/D157 graph-class identity forces $x=0$ lower sources at upper parents. We will reserve all L sources at actual first hosts and fill every H image from a first-host H source. The four neutral assignments $L_0,\ldots,L_3$ at shift zero fix those four images and exhaust the chosen neutral host. All other assignments use positive first shifts or the two upper parents with residual capacities $p-1,q$.

## 2. Regular first shifts and independently expanded blocks

Both geometries have the regular shifts $[1,r-5]$. Their full quotas are all consumed by gap arrows since the selected first terminal belongs to a special-tail host. Designate any set of $h_0$ regular shifts for promotion to full quota four, with $0\le h_0\le r-5$. The other regular shifts have quota two. Use the first $r-5+h_0$ consecutive positions starting at 4 for L sources and H images. We will reserve these two equal position intervals at the regular first hosts. Thus the last position is $r-2+h_0$ if the interval is nonempty.

For $p=2$, use only ordinary matched pairs, one pair per quota-two regular shift and two pairs per promoted regular shift. For $p\ge4$, put $p=4+2a$, with $a\ge0$. Form $a$ consecutive blocks of three shifts from the first $3a$ regular shifts. The inequality
$$
3a=\frac{3(p-4)}2\le\frac{3(r-5)}4\le r-5
$$
follows from $p\le(r+3)/2$. The remaining regular shifts use ordinary matched pairs. Consume positions in increasing order by these disjoint groups of displacement values. At an ordinary pair with shift $\delta$ at position $j$, assign
$$
L_j\to L_{j+\delta},\qquad H_{j+\delta}\to H_j .
$$
The two intermediate columns coincide as a common H-source and L-image hole at $j+\delta$. They are removed from the upper residual matching. A second pair of the same shift consumes the next position and gives a different column one unit later.

For an active triple of shifts $\delta,\delta+1,\delta+2$, first describe its central block and let $j$ be that block's initial position and $z=j+\delta$. With the middle shift unpromoted, the three L shifts at consecutive positions are $(\delta,\delta,\delta+1)$ and the three shifts supplying the H images are $(\delta+1,\delta+2,\delta+2)$. Thus the L image offsets from $z$ are $\{0,1,3\}$ and the H reservation source offsets are $\{1,3,4\}$. The two $P$ arrows are $H_z\to L_{z+2}$ and $H_{z+2}\to L_{z+4}$. Common holes at $z+1,z+3$ lie off that active residue.

With the middle shift promoted, the central block uses four positions with L shifts $(\delta,\delta,\delta+1,\delta+1)$ and H-image shifts $(\delta+1,\delta+1,\delta+2,\delta+2)$. Its L image offsets are $\{0,1,3,4\}$ and its H reservation source offsets are $\{1,2,4,5\}$. Across the two rows this gives exact quotas $(2,4,2)$ on the three actual hosts. The surviving $P$ sources are $H_z,H_{z+3}$ and their images $L_{z+2},L_{z+5}$ are the two distinct available holes' counterparts in the H-to-L matching. The common holes $z+1,z+4$ lie off their respective paths. Explicitly, in the interval $[z,z+5]$ both surviving H sources and both surviving L destinations are exactly the ones just assigned. The unpromoted block likewise exhausts both residual sets in $[z,z+4]$. Both modes use exactly two $P$ assignments.

To promote the first host prepend an ordinary matched pair of shift $\delta$ at the position immediately before the central block. Its common hole is $z-1$, below every central column. To promote the last host append an ordinary matched pair of shift $\delta+2$ just after the central block. If the central length is $\ell=3$ or 4, the appended pair's hole is $z+\ell+2$, strictly above the last central column $z+\ell+1$. Each pair adds two actual leaves to its own host and consumes one additional position in each first-host row. Either pair can be present with either central mode, so all three promotions combine independently.

For each group all its H reservations, L images and shifted-arrow columns are between its first position plus its minimum shift and its last position plus its maximum shift. The positions of successive groups increase strictly and the shifts of successive groups are increasing and disjoint. Hence those footprints are disjoint. This includes adjacent active blocks, repeated pairs of any one ordinary shift and the transition to ordinary positions. When the regular region is nonempty its footprints lie in $[5,2r-7+h_0]$. In fact the first position is 4, the least positive shift is 1 and the last position and largest shift are at most $r-2+h_0,r-5$. All the footprint cells lie within both the H-source and L-image windows. Across groups the regular reservations occupy exactly $[4,r-2+h_0]$ in the L-source and H-image rows. They use exactly $2a$ residual $P$ assignments in I-a, and zero in II-a. In the empty case $r=5$, $h_0=0$, there are no regular shifts or groups and I-a has $a=0$.

## 3. Special-tail patterns for every remaining quota multiplicity

Let $t=h-h_0$ be the number of extra fours beyond the neutral and chosen regular hosts. Take $h_0=h$ when $h\le r-5$, and otherwise take $h_0=r-5$. Then $0\le t\le4$. Write $D=2r+h_0$. In the tail, each L source and H image position is written $r+h_0+x$ in terms of a local offset $x$. The tail L-source positions have $x\in[-1,2+t]$ and its H-image positions have $x\in[-1,1+t]$. For each special first shift $\delta$ let $d_0=r-\delta$, called its deficit here. At an L source of offset $x$, the L image has index $D+x-d_0$. At an H image of offset $x$, its reserved H source has the same index formula $D+x-d_0$. All upper residual path columns in this section are stated as offsets from $D$. The final H source has index $D+3+t$, and the final L image has index $D+4+t$. The latter denotes an absent H-source cell in the residual matching.

The special deficits are $\{0,2,3,4\}$ in II-a, and $\{1,2,3,4\}$ in I-a. Before promotion every special host has two actual leaves, with one selected terminal at deficit 3 in II-a and deficit 2 in I-a. All table entries describe actual arrows at those original parents. The number $\tau$ in the table is the number of promotions in a core tail. Rows are given by their consecutive positions $[-1,2+\tau]$ for L sources and $[-1,1+\tau]$ for H images. Subtract the displayed deficit from the position offset to obtain each L image or reserved H source. Let $X'$ be the core's L image offset set and $Y$ its reserved H source offset set.

| Geometry | $\tau$ | L deficits | H-image deficits | $X'$ | $Y$ | Core $P$ source offsets |
| --- | ---: | --- | --- | --- | --- | --- |
| II-a | 0 | $(0,4,0,4)$ | $(3,2,2)$ | $\{-4,-2,-1,1\}$ | $\{-4,-2,-1\}$ | $1$ |
| II-a | 1 | $(2,4,2,0,2)$ | $(2,4,0,3)$ | $\{-4,-3,-1,1,2\}$ | $\{-4,-3,-1,1\}$ | $2$ |
| II-a | 2 | $(0,2,4,2,0,2)$ | $(0,2,4,0,3)$ | $\{-3,-2,-1,0,2,3\}$ | $\{-3,-2,-1,0,2\}$ | $3$ |
| I-a | 0 | $(1,4,4,2)$ | $(3,1,3)$ | $\{-4,-3,-2,0\}$ | $\{-4,-2,-1\}$ | $-3,0,2$ |
| I-a | 1 | $(2,4,1,4,2)$ | $(3,2,1,3)$ | $\{-4,-3,-2,0,1\}$ | $\{-4,-2,-1,0\}$ | $-3,1,3$ |
| I-a | 2 | $(2,4,1,1,4,2)$ | $(1,3,1,3,2)$ | $\{-4,-3,-1,0,1,2\}$ | $\{-3,-2,-1,0,1\}$ | $-4,2,4$ |

Here every assignment from a displayed $P$ source adds $\rho$ to its offset. These constant tail patterns follow from the two row types and their far-end discrepancy. For example, the index moment of a core tail gives $\rho N_P=2+\sum_{\mathrm{L}}d_0-\sum_{\mathrm{H}}d_0$: the surplus L source position is $2+\tau$ and the absent H source at the last L target is $4+\tau$. A promotion can add equal deficits to each sum. The tables also solve the incidence constraints explicitly, as follows.

In the $\tau=0$ rows the lists are the unexpanded D175 II-a and D176 I-a tails. A direct prepend at deficit 2 fails in either geometry: the added pair at position $-1$ would give column $-3$, already occupied by the translated common hole from $-4$. The revised $\tau=1$ rows instead give two more leaves to the deficit-2 host. In II-a the two additional occurrences are obtained with an altered distribution of deficits between rows, as given by the lists. In each $\tau=2$ row the high-shift host of deficit 0 in II-a or deficit 1 in I-a gains two more leaves. This is verified by tallying the concatenated lists. With the one selected first terminal restored, every intended physical host has its full quota, including the promoted selected parent in I-a. Each row contains exactly $4+\tau$ distinct L images and $3+\tau$ distinct reserved H sources, since every entry in the displayed sets is distinct. The II-a row with $\tau=2$ can also be obtained by translating the $\tau=1$ core one column and adding one pair of deficit zero at position $-1$. Its common hole $-1$ avoids the translated holes and the single shifted path.

For II-a in all three rows, $X'=Y\sqcup\{1+\tau\}$. The $P$ arrow from the available H source $1+\tau$ goes to the final $4+\tau$. The latter is the absent H-source cell, so this one arrow fills the exact missing residual destination. In I-a for $\tau=0,1,2$ the following paths give the indicated arrows. The short paths are respectively $-3\to-1$, $-3\to-1$, $-4\to-2$. Each start is in $X'\setminus Y$ and the end is in $Y\setminus X'$. The other path is $\tau\to \tau+2\to \tau+4$. Its initial offset belongs to $X'\setminus Y$, the offset $\tau+2$ is absent from both hole sets and is within both actual row windows, and the last offset $\tau+4$ is the absent H-source cell. The short and far paths have disjoint used cells and avoid common holes even when a common hole lies between two positions of a different residue. Thus the short path uses one upper assignment and the far path uses two. Together with the common holes the endpoints account for all discrepancies of the displayed sets. This proves the exact source and destination partition for every row, with identity at $Q$ on unaffected surviving columns.

The full tail is obtained by selecting a core and prefix pairs as follows.

| $t$ | Prepend paired deficits, in order | Core $\tau$ | Additional promoted deficits |
| ---: | --- | ---: | --- |
| 0 | none | 0 | none |
| 1 | 4 | 0 | 4 |
| 2 | 4, 3 | 0 | 4, 3 |
| 3 | 4, 3 | 1 | 4, 3, 2 |
| 4 | 4, 3 | 2 | all four |

Let $w_0$ be the number of these prepend pairs, so $t=w_0+\tau$. Place the pair of deficit 4 at offset $-1$ in the position rows and, if present, the pair of deficit 3 at offset 0. Their common-hole offsets from $D$ are $-5,-3$, respectively. Translate every core position, intermediate column and residue path offset by $w_0$, keeping its own deficit and upper parent. A single prepend pair lies below the shifted core because the core minimum is at least $-4$ and thus becomes at least $-3$. With two pairs the shifted core minimum is at least $-2$, above both prefix holes. The same displacement formulas apply on translated positions and all differences along residue paths are preserved. The translated endpoint $4+\tau+w_0=4+t$ is the absent H-source cell of the full tail. Its predecessor is present and all other used H sources have offset at most $3+t$. Every L image has offset at most $4+t$. Together the positions occupy precisely $[-1,2+t]$ and $[-1,1+t]$ in their respective position rows.

The lowest tail intermediate index is at least $D-5$, strictly above the regular upper bound $D-7$, and at least 5 when $r\ge5$. Thus no special arrow overlaps a regular footprint or encounters an invalid lower boundary. The same argument proves the pure regular-expansion case $t=0$: moving the tail to $h_0=h$ translates all its indices by $h$ from the one-four control, and moves the absent H boundary by exactly $h$. The unfolded H numerical intervals change with $J=3r+6+2h$, so the verification is by the exact two alphabets of §1, including their translated endpoints, rather than assuming equal numerical shifts in the two rows.

## 4. Exact total capacities and constructive scope

Choose actual first-center labels by matching full quotas to the neutral, regular and special roles just specified. Within each quota class use increasing physical indices for increasing reduced labels. The number of prescribed quota-four roles is exactly $1+h_0+t=g$. The construction transports the numerical roles to the actual original incidences for every physical order. For $g\le r-4$, the regular promotions may be chosen independently at any corresponding regular shifts, including inside active blocks. For $g=r-3,r-2,r-1,r$, use all regular promotions and the displayed special selection for $t=1,2,3,4$. The special choices use selectable numerical first roles at the actual fixed physical centers.

The four neutral L sources, the consecutive regular strip and the tail exhaust the L-source row. The regular strip and tail also fill the entire H-image row. Let $Y$ now denote the complete set of H reservations at first hosts and $X'$ the complete set of nonneutral L images at those hosts, in the actual folded index alphabet. The two sets are within the proved windows and their positions derive from the ordinary pairs, block offsets and tail formulas. The residual matching is H-to-L on the common encompassing interval $[4,2r+4+h]$. The H-source holes are $Y\sqcup\{2r+4+h\}$ and the destination holes are $X'$. The preceding paths, pairwise disjoint and avoiding common holes, account for every discrepancy. Each uses all its intervening surviving source cells and fills all its intervening surviving destination cells. Everywhere else the surviving indices coincide and use $Q$ by identity. This is a constructive instance of [D168's exact residue criterion](ORDINARY_SPINE_EXCEPTIONAL_TWO_UPPER_HOST_RESIDUE_COMPRESSION.md#4-exact-residue-path-criterion), with the correct absent far-boundary cell.

In II-a there is one $P$ gap assignment from the tail. In I-a there are $2a+3=p-1$, from the $a$ regular active blocks and the tail. The H-source row contains $2r+h$ cells and the H-image row $r-2+h$. Every H image uses one H source at a first parent, leaving $r+2$ upper-host assignments. Thus $Q$ receives exactly $r+2-(p-1)=q$. Along with the selected terminal at $P$, all individual quotas are exact. Every L-source assignment is at a lower host and noncrossing. The only gap crossings are precisely the $r-2+h=s-K$ H assignments at first parents. All upper residual arrows are noncrossing. This proves the entire asserted H1 domain independently of any search or new exterior geometry. At $g=1$ the rules reduce to D175/D176's accepted suppliers. The result leaves the multiple-four $r=3$ boundary and exact classifications at preassigned numerical second roles as separate questions.

## 5. Named lift, both inventories and exact return

Assign each remaining original terminal at its own actual parent in increasing terminal index order to that parent's increasing numerical gap coordinates. The selected terminal is omitted at each of its two parents and the direct leaf keeps its unique exterior assignment. The exact quota counts make this a bijection at each parent. The original names, incidences and extended witnessing spine are retained. The method is a finite sequence of direct arithmetic and finite scans of the named input, block lists and interval; it supplies labels without solving a fresh instance.

In oriented labels take $C=c+K$, shift the old labels below $c$ by $A$ and those at or above $c$ by $A+s$, preserving their sides at $C$. Add $n+s$ to each upper reduced exterior label. The shared $v$ agrees with its old placed label $A$. Each such exterior edge crosses and gains $n+s$ because its lower endpoint is at most $A<C$ and its upper endpoint is at least $n+s+A+1>C$. Each gap coordinate $i$ receives $A+c+i$. The exact label and difference palettes are

~~~text
old labels    [A,A+c−1] ⊔ [A+c+s,n+s+A]
fresh labels  [0,A−1] ⊔ [A+c,A+c+s−1] ⊔ [n+s+A+1,m]
old weights   [1,d−2] ⊔ [d−1+s,n+s]
fresh weights [d−1,d+s−2] ⊔ [n+s+1,m].
~~~

All displayed unions are disjoint. Old crossing weights gain $s$ and old noncrossing weights are fixed. The exterior and gap allocations fill their entire label and difference intervals. The gap crossing weights are $[d+K-1,d+s-2]$ and the noncrossing weights $[d-1,d+K-2]$ by the physical predicate and exact image ranges. Hence the full vertex and actual edge-difference bijections onto $[0,m]$ and $[1,m]$ have exactly crossing spectrum $[d+K-1,m]$ and noncrossing spectrum $[1,d+K-2]$. Since $w=0$ and $m=2C+2$, this is the exact oriented $S_{-1}$ return.

For the first-section boundary use the proved reservation sets $Y,X'$ of §4, and let $J-S=\{J-j:j\in S\}$ for any column set $S$. The first-section gap source and image sets are
$$
I=[0,k-1]\sqcup(J-Y),\qquad J_1=[0,3]\sqcup X'\sqcup[K,s-1].
$$
At each actual first parent the image set is its numerical source set translated by its own $\delta$. Their disjoint unions give these exact $I,J_1$. The corresponding complements in the gap alphabet are
$$
I'=J-([4,2r+3+h]\setminus Y),\qquad J_2=[4,2r+4+h]\setminus X'.
$$
All $I'$ coordinates are physically upper and all $J_2$ images are noncrossing. For the respective known exterior table row let $b_P,b_D$ be the upper indices of $P$ and the actual direct leaf. The first and second fresh exterior label sets are
$$
E_1=([1,A-1]\setminus\{t_0\})\sqcup\{n+s+A+1,n+s+A+3\},\qquad
E_2=\{0,t_0,n+s+A+2,n+s+A+b_P,n+s+A+b_D\}.
$$
Their exact differences are $n+s+[1,A]$ and $n+s+[A+1,A+5]$. With $L_{\rm old},D_{\rm old}$ from the old palettes, both actual resources at this boundary are

~~~text
used labels         L_old ⊔ E₁ ⊔ (A+c+I)
remaining labels    E₂ ⊔ (A+c+I′)
used differences    D_old ⊔ (n+s+[1,A]) ⊔ (d−1+J₁)
remaining weights   (n+s+[A+1,A+5]) ⊔ (d−1+J₂).
~~~

In orientation, used lower labels are the old lower band, the lower first exterior slots and $A+c+[0,k-1]$. Used upper labels are the old upper band, the two upper first exterior slots and $A+c+(J-Y)$. The remaining lower labels are $0,t_0$, and the other remaining labels are upper. Used crossing weights consist of the old crossing band, the first exterior band and $d-1+[K,s-1]$. Used noncrossing weights are the old noncrossing band and $d-1+([0,3]\sqcup X')$. Remaining crossing weights are exactly the remaining exterior band, while remaining noncrossing weights are $d-1+J_2$. The unfinished edge is the literal original $uw$, with oriented endpoints $(n+s+A+1,0)$ and crossing weight $n+s+A+1$ in the remaining exterior band.

For an actual maximum-frontier input the actual old labels are $n-G$. Complement the output about $m$. The input and output cuts become $n+1-c,m+1-C$, respectively. The actual old shifts are $B,B+s$ below and at or above the actual cut, by $2K=A+B+s$. For minimum polarity they are $A,A+s$. Complementing transforms both actual label inventories and exchanges their sides, while all actual differences and crossing statuses remain fixed. The maximum output frontier is $w=m$ and the actual connector endpoints are $(4,m)$.

The independently supplied arbitrary-large admitted size premise follows under the retained [D157/D134 initializer conditions](ORDINARY_SPINE_ALTERNATING_EXCEPTIONAL_SPECTRUM.md#7-independent-supply-cycle-closure-and-immutable-labels). For any finite sequence of individually admitted blocks, with their own input phase, physical port, spectrum and size conditions, let $C_i$ be its actual cut after block $i$. Let $T_i,S_i$ be the respective sums of the later actual lower shifts and gap widths. Each placement preserves old side membership, so the exact eventual label map on this boundary is $x\mapsto x+T_i+S_i\mathbf{1}_{x\ge C_i}$. Each crossing difference gains $S_i$ and each noncrossing difference stays fixed. Apply these same maps to the exact first-section used inventories and both fixed endpoints of its literal unfinished crossing edge. The final complements are the remaining resources in the final alphabets. Induction gives the exact graceful bijections and preserved named incidences at every admitted boundary. The finite backward sums and finite original-index scans terminate, and the map emits each label once in its final alphabet.

## 6. Status of controls and historical results

D176 is Director accepted within its exact written scope at scientific checkpoint 5602efe6bdbcb215f7d659fbe74562a3decdf274. The retained D175 and D176 theorems project to 15 matched separators among the 93 frozen D174 all-even $R=8$ originals: the five possible physical positions of the sole first quota four and three physical second profiles $(2,6,0),(4,4,0),(6,2,0)$. The [custody receipt](../evidence/validation/LCL_ORDINARY_SPINE_EXCEPTIONAL_ODD_FIRST_CENTER_QUOTA_EXPANSION_001/CUSTODY.json) binds all 15 canonical original-record hashes and graph digests to the four exact frozen shards and the common independent prefix. The five accepted D176 additions are target-0993, target-1002, target-1074, target-1380 and target-2748. Only target-0991 was historically entered in that projection. The other fourteen, and 3,518 in the whole D174 execution population, remain historically unentered. D174 still has one completed matched pair, two numerical arms and a normal separator stop. Raw exterior supply and compatible allocation retain their separate meanings.

As a D177 corollary pending Director review, the simultaneous H0 exclusion and H1 supply now apply to every original in that 93-member D174 stratum. For $r=5$ there are $2^5-1=31$ ordered first inventories with at least one four and the three second profiles just listed. Their independent prefix has $n=74$, and $K=14+g\le19$, so all meet the size premise. This is a theorem-derived projection on the frozen domain. The 15 previously accepted identities retain their separate custody basis. The D174 historical record is unchanged.

The new construction closes the requested range $1\le g\le r$ for $r\ge5$ with selectable numerical second roles. No hybrid discovery or new scientific execution is required for this result. The exact D176 exterior menu and the separate scope of each retained adverse and positive control are preserved.
