# D176 — Complete odd first-center H1 geometry menu

Task **LCL-ORDINARY-SPINE-EXCEPTIONAL-ODD-FIRST-CENTER-H1-MENU-001**.

**PROVED WITHIN THE DECLARED ARRANGEMENT / PENDING DIRECTOR REVIEW.** The five geometries in §2 are a complete reduced-exterior menu for any compatible H1 return in the broad D175 domain. Each geometry has the claimed raw spectrum under its physical role and quota requirements. For an inventory with exactly one quota four, H1 is infeasible at $r=3$ and feasible at every odd $r\ge5$ for every admissible positive even second split and physical order. D175 supplies the matched H0 exclusion on the entire domain.

## 1. Input, forced reservations and parity

Use the [D157 placement](ORDINARY_SPINE_ALTERNATING_EXCEPTIONAL_SPECTRUM.md#1-interface-and-exact-inventory-rule) from $S_{-1}$ to $S_{-1}$. All labels, sizes and quotas are exact integers, excluding booleans. Intervals are inclusive and reversed intervals are empty. The independently supplied graceful original prefix has $n=2c+2$ edges, its actual witnessing spine ends at extreme $v$, and its oriented labels satisfy $G(v)=0$. Write $d=c+2$, with oriented cut $c$, label equality on its upper side, input crossing weights $[d-1,n]$ and noncrossing weights $[1,d-2]$. Append the actual spine vertices $u,w$, $r\ge3$ actual first centers for odd $r$ with quotas in $\{2,4\}$ and at least one four, and no direct leaf at $u$. Write $F$ for the first terminal total. The second quotas are positive even integers of sum $R=r+3$. The sole actual direct leaf at $w$ belongs to the exterior. Preserve every original physical index and incidence. The fresh size is $2K=F+2r+8$, with $K=F/2+r+4$, $n\ge2K$ and $m=n+2K$.

Let $e_1,e_2$ count selected exterior terminals by section. Terminal balance requires both positive in H1. The connected crossing reduced exterior contains all positive centers, with $A=r+1+e_2$ fresh lower and $B=4+e_1$ fresh upper vertices. Put $s=2K-A-B$ and $k=K-A$ and require $s\ge K$ and $A\le K\le A+s$. Its pins are $v=A,u=A+1,w=0$. The weight-one edge forces $u=A+1$ because $vu$ is the sole new incidence at $v$. The D175 graph counts give $N_{\rm low}=2r+4=2(A+x)$, where $x$ counts lower gap sources at upper hosts. Thus $e_2=1,A=r+2,x=0$. In particular $k=F/2+2\ge r+3$. The other fresh graph class has size $4+F$. As in [D175 §§1–2](ORDINARY_SPINE_EXCEPTIONAL_ODD_FIRST_CENTER_DIRECT_PLACEMENT.md#1-exact-interface-and-graph-counts), in the gap each source coordinate $i$ is lower iff $i<k$. Subtracting the actual expanded endpoint gives the image $\pi(i)=i+A-1-j$ at lower host $j$ and $\pi(i)=s+b+1-i$ at upper host $A+b$. The corresponding difference is $d-1+\pi(i)$. Opposite source and host sides require $\pi(i)\ge K$, and the images must permute $[0,s-1]$.

Since $B\ge5$ and $s\ge K\ge A+B$, images $0,\ldots,4$ and sources $0,\ldots,3$ exist, and $k\ge B$. Upper gap hosts have $b\ge2$ because $u$ has no direct leaves, so their images are at least four. Lower shifts are nonnegative. By induction, images $0,\ldots,3$ require the identical four sources at the neutral slot $A-1$. This is an actual first center, its full quota is four, and no terminal is selected there. Its gap capacity is exhausted. For image four, a positive lower shift requires a used source and shift zero is exhausted. The upper formula forces $b=2,i=s-1$. The upper index two is therefore an actual second center with gap capacity. The source is physically upper since $s-k=K-B\ge A$, and image four is noncrossing, as required at an upper host. These arguments use the H1 capacity at $w$ of zero, and leave its original direct edge in the exterior.

The numerical reference exterior attaches lower slots $1,\ldots,A-1$ to $u$ and all upper slots of index at least two to $w$, with edges $vu,uw$. Its weights are $[1,A+B]$. Let $t$ be the lower reduced label of the unique selected second terminal and $b$ the upper index of its actual parent. The replacement of the reference lower attachment removes its distinct weight $A+1-t$ and adds the strictly greater weight $A+b-t$. A direct exterior leaf at $w$ keeps its reference weight. Thus a selected first terminal must restore the missing difference. With upper index $b'$ and lower parent $j$, it satisfies $j=b'+t-1\ge t+2$, since upper index two is a second center. Compare exact weight sums with the reference. Each selected first terminal reduces its reference weight by its lower parent label. The selected second terminal increases its weight by $b-1$. Consequently
$$
t+e_1+1\ \le\ \sum j\ =\ b-1\ \le\ B-1=e_1+3 .
$$
Here every other selected first parent has label at least one and repetitions in the sum are counted by terminal incidence. It follows that $t=1$ or $2$.

Independently take the permutation moment $\sum_i(\pi(i)-i)$ modulo two. For the lower contributions every first full quota is even and the gap direct-leaf capacity is zero. Removing the selected first terminals from their full quotas leaves modulo two the sum of their shifts, which equals $\sum j$ because $A=r+2$ is odd. At the upper hosts, the even full quotas give zero and removal of exactly one selected second terminal leaves $s+b+1$ modulo two. The term $-2i$ in each reflection contributes zero. By terminal balance the total modulo two is $(b-1)+(s+b+1)\equiv s$. Thus $s$ must be even. Since $2K$ is even and $A$ is odd, $B$ must be odd, and so must $e_1=B-4$.

## 2. Complete geometry reduction and raw spectra

**Case $t=1$.** Every selected first parent is at least two, and the restoring parent is at least three. Hence $2e_1+1\le\sum j\le e_1+3$, or $e_1\le2$. Odd parity gives $e_1=1$ and $B=5$. Now $j=b'$ and terminal balance gives $b=j+1$. The only possible restoring placements have $j=3$ or 4. The second center at index two is denoted by $Q$ and the selected second terminal's actual parent by $P$ throughout this proof. The direct leaf occupies the remaining upper slot.

**Case $t=2$.** The two extremes of the terminal-balance bound coincide, so every bound is attained. The restoring parent is $j=4$ with terminal at upper index three and $P$ at upper index $B$. Every other selected first terminal is at the actual parent of reduced label one. Its full quota is at most four, so $e_1\le5$ and parity leaves $1,3,5$. Call the additional selected first-terminal indices $S\subset[4,B-1]$. For each index $a\in S$, the replacement of the reference weight $A+a$ sends it to $A+a-1$. Apart from these changes, upper index three supplies the missing lower weight $A-1$, while the new edge at lower slot two adds $A+B-2$. For each $i\in[3,B-1]$ the exact multiplicity of $A+i$ therefore gives
$$
1=\mathbf{1}_{i\ge4}(1-\mathbf{1}_{i\in S})
  +\mathbf{1}_{i+1\in S}+\mathbf{1}_{i=B-2}.
$$
No other original edge can give any of these weights. If $B=5$, the second terminal supplies $A+3$, the equation excludes 4 from $S$, and $S$ is empty. For $B\ge7$, at $i=3$ the equation forces $4\in S$. Inductively for $4\le i<B-2$ it forces $i+1\in S$, and at $B-2$ the second terminal fills the vacancy and forces $B-1\notin S$. At $B-1$ its unchanged direct edge gives the correct weight. Thus exactly $S=[4,B-2]=[4,e_1+2]$, and the direct-leaf index is $B-1$.

In the table, terminal slots in the first column of assignments are upper indices measured from $A$, and the number after the arrow is their actual lower parent label. The lower slots of the first centers are $[1,A-1]\setminus\{t\}$ in every row. The selected second terminal is at lower slot $t$ and attached to $P$, and $Q$ is always at upper index two.

| Geometry | $t$ | $B$ | First terminal indices and parent labels | $P$ upper index | Direct-leaf upper index |
| --- | ---: | ---: | --- | ---: | ---: |
| I-a | 1 | 5 | $3\to3$ | 4 | 5 |
| I-b | 1 | 5 | $4\to4$ | 5 | 3 |
| II-a | 2 | 5 | $3\to4$ | 5 | 4 |
| II-b | 2 | 7 | $3\to4,\ [4,5]\to1$ | 7 | 6 |
| II-c | 2 | 9 | $3\to4,\ [4,7]\to1$ | 9 | 8 |

Assign these reduced roles to distinct actual centers, at physical indices of the required capacities. The neutral slot $A-1$ must have full quota four and no selected terminals. A first parent supplying one selected terminal needs at least one available actual terminal, and slot one in II-b or II-c must supply two or four distinct terminals, respectively. Thus II-c needs a second quota-four first center. At $r=3$, label four is the neutral slot, so I-b and all II patterns fail the neutral requirement. I-a has a distinct parent at label three. The selected second terminal uses one actual terminal of $P$, leaving at least one because its full quota is even and positive. $Q$ has its full even quota. Any eligible physical role order is permitted. At a given parent the selected original indices can be taken in increasing order by upper slot, or chosen as any distinct actual indices when assessing a candidate. The direct leaf is the one actual direct incidence at $w$, never a terminal of a branch center.

For completeness, each allowed raw placement gives all reduced labels $[0,A+B]$ once. It is a connected original subtree containing the three spine vertices and all centers. All its actual edges cross the reduced cut. In I-a or I-b, $vu$ and the first center attachments give $[1,A-1]$, and the selected first terminal restores $A$. In the remaining section, relative to the high range $A+[1,5]$, $uw$ gives index one and $wQ$ index two, while $wP$ and the selected second terminal give $b,b-1$ and the direct leaf gives the unused index. In each II geometry, the edges at $u$ to $v$ and its first centers give $[1,A]\setminus\{A-1\}$. The one terminal at parent 4 restores $A-1$. The extra first terminals at parent 1 give $A+[3,B-3]$. The second section uses $A+\{1,2,B-2,B-1,B\}$ on its five original edges. Thus all five rows have weight bijection $[1,A+B]$. The indexed quota requirements also ensure width admission. For $B=5$, $k\ge r+3\ge6$. In II-b, $r\ge5$ gives $k\ge8>7$. In II-c, the second first quota four gives $F\ge2r+4$ and $k\ge r+4\ge9=B$, allowing $s=K$ at equality. In each case $B\le k$ is equivalent to $s\ge K$, and gives the old membership bounds. These are raw exterior suppliers with the necessary physical qualifications. A compatible gap is a separate requirement.

## 3. Folded alphabets and the full negative at the one-four $r=3$ boundary

Write $J=s+3$, $L_j=j$, $H_j=J-j$. In any menu geometry, using $k=K-A$, the source rows are $L_{[0,k-1]}$ and $H_{[4,k+A+3-B]}$. The image rows are $L_{[0,K-1]}$ and $H_{[4,k+3-B]}$. The H rows encode the numerical upper source interval and crossing image interval, respectively. At a lower parent with shift $\delta=A-1-j_0$, the folded maps are $L_j\to L_{j+\delta}$ and $H_j\to H_{j-\delta}$. At the upper parent $Q$ the row exchange preserves the index. At $P$ the shifts for the row exchange are $-\rho,+\rho$ in L,H order, where $\rho=b-2$. These follow by direct substitution into §1. A lower-host L assignment and an upper-host H assignment are precisely the noncrossing types. The other two types are crossing. The two alphabets and row formulas enforce those predicates for each legal arrow.

Since $x=0$, all L sources must use lower parents. Every H image is then filled by a lower parent from an H source. The residual matching after lower reservations is entirely H-to-L with shifts 0 and $+\rho$, in the exact sense of the [D168 residue rule](ORDINARY_SPINE_EXCEPTIONAL_TWO_UPPER_HOST_RESIDUE_COMPRESSION.md#4-exact-residue-path-criterion). It uses all and only the $R-1$ upper-host gap leaves, at their individual residual quotas.

At $r=3$ with exactly one four, $F=8$ and I-a alone survives §2. The parameters are $A=B=5,K=11,s=12,k=6,J=15,\rho=2$. Sources are $L_{[0,5]},H_{[4,9]}$ and destinations $L_{[0,10]},H_4$. After the four neutral assignments, the lower shifts remaining are one copy of 1 at first label 3 and two copies of 2 at first label 2. The sole crossing image $H_4$ must come from $H_5$ at shift 1 or $H_6$ at shift 2. In the first case $L_4,L_5$ use shift 2 and fill $L_6,L_7$. The available upper formulas could hit $L_5$ only from $H_5$ at $Q$ or $H_3$ at $P$, respectively consumed and absent. In the second case the remaining shifts 1 and 2 must fill $L_5,L_7$: exchanging those two choices would give two copies of $L_6$. Then $H_5$ is an unassigned H source and both its legal upper images $L_5,L_7$ are already occupied. There is only one crossing image, so $H_5$ cannot be assigned at another lower host. These contradictions do not depend on whether the full quota two or four belongs to $P$. Thus both numerical role choices, and therefore the full H1 class on every physical order at this one-four boundary, are excluded within the declared arrangement.

## 4. One-four positives for every odd $r\ge5$

The first inventory is $r-1$ twos and one four. Give the four the neutral role and assign the other first roles in increasing reduced label order to the actual quota-two centers in physical index order. Assign the smaller second full quota to $P$ and the larger to $Q$. With this designation call them $p,q$ and set $p_g=p-1,q_g=q$. Both physical second orders are covered by the assignment. The parameters for the two constructions used here are
$$
F=2r+2,\quad K=2r+5,\quad A=r+2,\quad B=5,\quad k=r+3,\quad s=3r+3,\quad J=3r+6.
$$
Thus sources are $L_{[0,r+2]},H_{[4,2r+3]}$ and destinations $L_{[0,2r+4]},H_{[4,r+1]}$. Use the first actual indexed terminal of the stated selected first parent and of $P$. The sole direct leaf is exterior. The four neutral assignments are $L_0,\ldots,L_3$ with their identical L images.

### 4.1 II-a with $p=2$

This is the accepted [D175 supplier](ORDINARY_SPINE_EXCEPTIONAL_ODD_FIRST_CENTER_DIRECT_PLACEMENT.md#4-explicit-gap-bijection-at-every-admitted-multiplicity). For $j\in[4,r-2]$ use shift $j-3$ on both the pair $L_j\to L_{2j-3}$ and $H_{2j-3}\to H_j$. The four remaining L sources, at indices $r-1,r,r+1,r+2$, use the shifts $r,r-4,r,r-4$ and give indices $2r-1,2r-4,2r+1,2r-2$. To fill H images of indices $r-1,r,r+1$, use H sources $2r-4,2r-2,2r-1$ at shifts $r-3,r-2,r-2$ respectively. All shift quotas are used, including the single residual copy of $r-3$ at parent 4. The paired columns lie at most $2r-7$, below these special columns. Let $Y$ be the reserved H source indices and $X'$ the nonneutral L image indices. Here $X'=Y\sqcup\{2r+1\}$. Use $H_{2r+1}\to L_{2r+4}$ at $P$ and all other surviving H sources at $Q$ by identity of index. The upper capacities are one and $r+1$ as required. Both exact row partitions, including the empty pair interval at $r=5$, follow from these sets. The control of all 18 gap arrows at $r=5$ and exact original record remain D175's.

### 4.2 I-a for every needed $p\ge4$

I-a uses the first labels $[2,A-1]$. The active positive first shifts are $[1,r-1]$, each with two leaves except shift $r-2$ at parent 3, which has one gap leaf after the selection. The upper separation is two. The following construction works at every even $p=4+2a$ with $a\ge0$ and $3a\le r-5$. This suffices: for every admissible smaller quota $4\le p\le(r+3)/2$, one has
$$
3a=\frac{3(p-4)}2\le\frac{3(r-5)}4\le r-5 .
$$

On the common first-host source and destination indices $[4,r-2]$, use the first $3a$ positions as $a$ consecutively indexed blocks of three. For one block let $j,j+1,j+2$ be its indices, let $\delta=j-3$ and let $z=2j-3$. Assign the three L sources at $j,j+1,j+2$ to shifts $\delta,\delta,\delta+1$, respectively. Their L images are $z,z+1,z+3$. Fill the H images at $j,j+1,j+2$ using shifts $\delta+1,\delta+2,\delta+2$ respectively from the H sources $z+1,z+3,z+4$. This supplies two physical leaves at each shift $\delta,\delta+1,\delta+2$ and accounts for six lower-host assignments. In the H-to-L residue path of parity $z$, the destination hole $z$ and source hole $z+4$ are repaired by the two $P$ arrows
$$
H_z\longmapsto L_{z+2},\qquad H_{z+2}\longmapsto L_{z+4}.
$$
The common holes at $z+1,z+3$ are on the other residue. Thus both sources and images used by these two shifts exist and are distinct. Any remaining columns in this footprint can use the identity on the surviving H-to-L cells. Neighboring block footprints begin six columns apart, so no arrow meets another block.

For each remaining position $j\in[4+3a,r-2]$ use the pair $L_j\to L_{2j-3}$ and $H_{2j-3}\to H_j$, both at shift $j-3$. This creates a common hole with no shifted arrow. Every shift in $[1,r-5]$ now has exactly two leaves. The paired positions start above any preceding block footprint and are mutually distinct. If nonempty, all footprints and ordinary pair columns are within $[5,2r-7]$. All their L sources and H images are exactly $[4,r-2]$ in the corresponding rows.

Reserve the following seven remaining first-host assignments.

| Source | Lower shift | Destination |
| --- | ---: | --- |
| $L_{r-1}$ | $r-1$ | $L_{2r-2}$ |
| $L_r$ | $r-4$ | $L_{2r-4}$ |
| $L_{r+1}$ | $r-4$ | $L_{2r-3}$ |
| $L_{r+2}$ | $r-2$ | $L_{2r}$ |
| $H_{2r-4}$ | $r-3$ | $H_{r-1}$ |
| $H_{2r-1}$ | $r-1$ | $H_r$ |
| $H_{2r-2}$ | $r-3$ | $H_{r+1}$ |

The listed sources are valid at every $r\ge5$, and the H reservations and L images here start above $2r-7$. They give two uses each of $r-4,r-3,r-1$ and one of $r-2$. In particular the shift-$r-2$ first center has its full quota after counting the selected exterior terminal. The H image row is exhausted, as is the L source row. In the special columns the common H-source/L-image holes are $2r-4,2r-2$. In the odd residue the unmatched L hole $2r-3$ and H hole $2r-1$ admit one $P$ arrow. In the even residue the L hole $2r$ and the absent H boundary cell $2r+4$ require two $P$ arrows. Explicitly use
$$
H_{2r-3}\longmapsto L_{2r-1},\qquad
H_{2r}\longmapsto L_{2r+2},\qquad
H_{2r+2}\longmapsto L_{2r+4}.
$$
These arrows stay clear of both common holes, including $2r-2$ between the odd endpoints. The last image exists precisely in the enlarged L image row. The occupied H reservation $2r-1$ is the end of the odd path and is never used as an upper source. The middle even column $2r+2$ has both cells available. All other special columns match by identity wherever their cells survive. At $r=5$ there are no middle positions and the seven listed reservations and three arrows still apply.

More formally, on the encompassing H-to-L interval $[4,2r+4]$ place the absent boundary cell $2r+4$ in the source-hole set. After all common holes, the remaining discrepancies are exactly the two ends of each displayed path. The interiors have existing source and destination cells in the relevant residue. The paths are pairwise disjoint and avoid the common holes. Along a path the shifted source images fill the next successive available cells, including the last missing-source column. After removing all paths, surviving source and destination columns coincide. Give every such source to $Q$. This proves the bijection directly and also gives the positive instance of D168's residue criterion. In particular it does not rely on deleting common holes from an active path.

The total $P$ count is $3+2a=p-1$. All $r-2$ H images come from first hosts, so the H sources at upper hosts number $2r-(r-2)=r+2$, leaving $r+2-(p-1)=r+3-p=q$ at $Q$. All four neutral leaves and all remaining physical lower quotas have been accounted for. All L sources use lower hosts and are noncrossing. The $r-2$ reserved H sources at lower hosts cross, and the residual upper-host arrows are noncrossing. Thus the crossing count is $r-2=s-K$ and every physical sign and image threshold is correct.

Together §§3–4 give the exact H1 decision with selectable numerical role order on every original of the exactly-one-four inventory. At $r=3$ both even splits in physical order fail. For each odd $r\ge5$ every even positive quota pair of total $r+3$ is supplied. D175 also excludes H0 throughout this domain. The complete geometry menu applies more broadly, including inventories with several fours. Those broader allocation questions and feasibility in each prescribed numerical role order are separate.

## 5. Named reconstruction, exact inventories and admitted composition

The roles in §§4.1–4.2 name actual centers. Assign the remaining leaves at each host in increasing original terminal index order to that host's increasing numerical source coordinates. The two selected exterior terminal indices are excluded from these lists. Exact quota counts give a bijection at each host. The original direct leaf uses only its exterior assignment, and every old incidence and the extended witnessing spine are retained.

Orient all labels as in §1. Use the old shift $A$ below $c$ and $A+s$ at or above $c$, with output cut $C=c+K$. Old side membership is preserved since $A\le K\le A+s$. Gap coordinate $i$ receives $A+c+i$. Add $n+s$ to each upper reduced exterior label, giving all exterior differences the increment $n+s$ on actual crossing edges. The old vertex at $v$ agrees with reduced $v=A$. The precise palettes, with disjoint bands, are

~~~text
old labels    [A,A+c−1] ⊔ [A+c+s,n+s+A]
fresh labels  [0,A−1] ⊔ [A+c,A+c+s−1] ⊔ [n+s+A+1,m]
old weights   [1,d−2] ⊔ [d−1+s,n+s]
fresh weights [d−1,d+s−2] ⊔ [n+s+1,m].
~~~

The gap and reduced exterior bijections fill their exact intervals. Old noncrossing weights are unchanged and old crossing weights increase by $s$. The physical gap crossing predicate assigns weights $[d+K-1,d+s-2]$ to crossings and $[d-1,d+K-2]$ to noncrossings. Hence the full labels are $[0,m]$, the full differences are $[1,m]$, the crossing spectrum is $[d+K-1,m]$, and the noncrossing spectrum is $[1,d+K-2]$. Since $w=0$ and $m=2C+2$, the exact oriented return is $S_{-1}$.

For both constructions take the actual reserved H source indices $Y$ and the nonneutral first-host L images $X'$ as supplied above. These are exact sets from the formulas, including every active-block reservation in I-a. If $J-S$ denotes the pointwise reflection $\{J-j:j\in S\}$, the first-section gap sources and images are
$$
I=[0,r+2]\sqcup(J-Y),\qquad
J_1=[0,3]\sqcup X'\sqcup[K,s-1].
$$
The first set is the disjoint union over the physical first hosts. On each host its actual numerical images follow by the translation in §1. The exact complements in $[0,s-1]$ are
$$
I'=J-([4,2r+3]\setminus Y),\qquad J_2=[4,2r+4]\setminus X'.
$$
All $I'$ coordinates are upper and all $J_2$ images are noncrossing. For I-a let $t=1$, and for II-a let $t=2$. Let $b_P,b_D$ be their table indices for $P$ and the direct leaf, respectively. Both have the first selected terminal at upper index three. The first and second fresh exterior label sets in the oriented alphabet are
$$
E_1=([1,A-1]\setminus\{t\})\sqcup\{n+s+A+1,n+s+A+3\},\qquad
E_2=\{0,t,n+s+A+2,n+s+A+b_P,n+s+A+b_D\}.
$$
The first and remaining exterior edge sets give differences $n+s+[1,A]$ and $n+s+[A+1,A+5]$. If $L_{\rm old},D_{\rm old}$ denote the old palettes above, the first-section resources are exactly

~~~text
used labels         L_old ⊔ E₁ ⊔ (A+c+I)
remaining labels    E₂ ⊔ (A+c+I′)
used differences    D_old ⊔ (n+s+[1,A]) ⊔ (d−1+J₁)
remaining weights   (n+s+[A+1,A+5]) ⊔ (d−1+J₂).
~~~

Used lower labels are the old lower band, the first lower exterior slots and $A+c+[0,r+2]$. Used upper labels are the old upper band, the first upper exterior slots and $A+c+(J-Y)$. The only remaining lower labels are $0,t$. Used crossing differences consist of the old crossing band, first exterior band and $d-1+[K,s-1]$. Used noncrossing differences are the old noncrossing band and $d-1+([0,3]\sqcup X')$. Remaining crossing differences are exactly the remaining exterior band, and remaining noncrossing differences are $d-1+J_2$. The literal unfinished connector is $uw$ with oriented endpoints $(n+s+A+1,0)$ and crossing weight $n+s+A+1$.

For a maximum-frontier input use actual labels $n-G$ and complement the output about $m$. The actual input and output cuts are $n+1-c,m+1-C$. Reflection of the oriented shift yields actual shifts $B,B+s$ below and at or above the actual cut respectively, by $2K=A+B+s$. Minimum polarity uses shifts $A,A+s$. The label inventories and their sides complement and exchange. Difference inventories and crossing statuses are invariant. In the maximum case the returned frontier is $w=m$ and the connector has endpoints $(4,m)$ because $B=5$.

Independently supplied admissible inputs of arbitrarily large admissible sizes follow under the exact retained D157/D134 initializer premises as in D175. For an individually admitted finite sequence, let $C_i$ be the actual cut at a completed boundary and let $T_i,S_i$ be the sums of all later actual lower shifts and gap widths. Each subsequent shift preserves the old cut membership. Thus its eventual label map on that boundary is $x\mapsto x+T_i+S_i\mathbf{1}_{x\ge C_i}$. Each actual crossing weight gains $S_i$ and each noncrossing weight stays fixed. The same map lifts the first-section used label and weight sets and both actual endpoints of its crossing unfinished connector. Exact final complements in the final alphabets are the remaining inventories. Induction gives the graceful bijections with all actual named incidences at each admitted boundary. The finite backward sum and the finite scans of physical indices and formula intervals terminate and permit immutable final-alphabet emission. Every preceding block must meet its own phase, size, spectrum and port premises.

## 6. Frozen controls and disposition

D175 is Director accepted within its exact domains. Its original positive family at $r=5$ projects to ten frozen D174 named separators. The sole quota four has five physical positions and the two second full quotas $2,6$ have two physical orders. The [custody receipt](../evidence/validation/LCL_ORDINARY_SPINE_EXCEPTIONAL_ODD_FIRST_CENTER_H1_MENU_001/CUSTODY.json) binds all ten actual graph digests, canonical record hashes, original shards, and the common independent prefix. D174 target-0991 is the sole historical entered case among them. The other nine were unentered. D174 retains the one completed pair, two numerical arms and 3,518 unentered originals. D175's H0 theorem continues to apply symbolically to the 93 all-even $R=8$ originals. None of these projections changes a historical run status. The new I-a construction additionally handles the even split $(4,4)$ at $r=5$ as an instance of the theorem.

D172 and D173 remain distinct four-first-center controls. In particular D173 grows second quotas on one fixed width-$(6,5)$ geometry, and its full feasible domain remains open. The D176 three-position blocks vary actual first reservations on I-a and implement its separation-two path changes. The complete menu and the exact one-four decision follow symbolically. No hybrid work was necessary.
