# D175 — Odd first-center direct-leaf placement

Task `LCL-ORDINARY-SPINE-EXCEPTIONAL-ODD-FIRST-CENTER-DIRECT-PLACEMENT-001`.

**PROVED WITHIN THE DECLARED ARRANGEMENT / PENDING DIRECTOR REVIEW.** H0 has raw exterior supply but no compatible completion throughout the domain below. H1 has an explicit supplier for every odd $r\ge5$ with first inventory $(2^{r-1},4)$ and second inventory $(2,r+1,0)$, where the exponent denotes repetition. All physical center orders are retained. The broader H1 inventory domain remains open.

## 1. Exact interface and graph counts

Use the [D157 exceptional interface](ORDINARY_SPINE_ALTERNATING_EXCEPTIONAL_SPECTRUM.md#1-interface-and-exact-inventory-rule), with input and output $S_{-1}$. All structural parameters and labels are exact integers, excluding booleans, and intervals include both endpoints. A reversed interval is empty. The independently supplied named graceful prefix has $n=2c+2$ edges and its actual witnessing spine ends at the extreme vertex $v$. Orient its labeling $G$ so that $G(v)=0$. The oriented input cut is $c$, with labels at the cut on its upper side. With $d=c+2$, the actual crossing weights are $[d-1,n]$ and the actual noncrossing weights are $[1,d-2]$.

Append the actual spine vertices $u,w$. There are odd $r\ge3$ actual positive first centers, with quotas in $\{2,4\}$, at least one quota four and no direct leaf at $u$. Write $F$ for their total. The second section contains two actual positive centers with positive even quotas $p,q$ and $R=p+q=r+3$, and its single actual direct leaf at $w$. The new vertices and edges total
$$
2K=2+r+2+1+F+R=F+2r+8,qquad K=F/2+r+4,qquad m=n+2K.
$$
Require $n\ge2K$. Both polarities and all physical branch orders retain their named incidences. All positive centers and both new spine vertices belong to the connected crossing reduced exterior. Gap vertices are actual leaves at their own exterior hosts. H0 and H1 are the two terminal-enabled classes in this arrangement, distinguished by whether the actual direct leaf is assigned to the gap or the exterior.

Taking $v$ lower in the exterior graph coloring, the fresh lower class comprises $w$, the $r$ first centers and the $R$ second terminals. The fresh upper class comprises $u$, the two second centers, the direct leaf and the $F$ first terminals. Thus $N_{\rm low}=1+r+R=2r+4$ and $N_{\rm high}=4+F$. Write $e_1,e_2$ for the exterior terminal counts by section, $h\in\{0,1\}$ for exterior direct-leaf placement, and $A,B$ for the fresh exterior label counts by lower and upper side. Counts of the actual vertices give
$$
A=r+1+e_2,qquad B=3+e_1+h,qquad s=2K-A-B.
$$
The oriented reduced labels satisfy $v=A,w=0$. The unique possible weight-one crossing edge joins labels $A,A+1$. Since $vu$ is the only exterior incidence at $v$, $u=A+1$.

In the numerical reference exterior use $vu,uw$, each slot $j\in[1,A-1]$ attached to $u$, and each slot $A+b$ with $b\ge2$ attached to $w$. Its differences are $[1,A+B]$. With the actual labels, replacing a reference upper attachment by a first terminal at lower parent $j$ reduces the weight by $j$. Replacing a reference lower attachment by a second terminal at upper parent $A+b$ increases the weight by $b-1$. The direct leaf in the exterior gives its reference weight. Equating the weight sums yields the [D147 balance](ORDINARY_SPINE_EXTERIOR_SUPPLY_REASSESSMENT.md#2-terminal-balance-and-paired-exchange)
$$
\sum_{\text{selected first terminals}} j
=\sum_{\text{selected second terminals}}(b-1).
$$
Each parent contribution is positive. Hence terminal-enabled means $e_1,e_2\ge1$.

For a compatible completion $s\ge K$, so $A+B\le K$ and $A\le K\le A+s$. Put $k=K-A$. A gap source $i\in[0,s-1]$ has oriented label $A+c+i$ and is physically lower iff $i<k$. Subtracting its actual exterior endpoint, its weight is $d-1+\pi(i)$ with
$$
\pi(i)=i+A-1-jquad(\text{lower host }j),qquad
\pi(i)=s+b+1-i\quad(\text{upper host }A+b).
$$
The lower host is smaller than the gap label and the expanded upper host is larger. The formulas use $n-c=d$. The gap images permute $[0,s-1]$, and $\pi(i)\ge K$ iff the source and its host are on opposite physical sides. Let $x$ count lower sources at upper parents, and $y$ count upper sources at lower parents. Then $x+y=s-K$. There are $k-x+y=B+2y$ gap leaves at lower parents and $s-k-y+x=A+2x$ at upper parents. Their graph colors are opposite those of the hosts. This proves the two counts
$$
N_{\rm low}=2(A+x),qquad N_{\rm high}=2(B+y).
$$
Consequently $A+x=r+2$. Since $A=r+1+e_2$ and $e_2\ge1$, necessarily $e_2=1, A=r+2, x=0$ in either compatible arm.

## 2. Complete H0 obstruction and independent raw supply

In H0, $B=3+e_1\ge4$. Since $s\ge K\ge A+B$ and $A\ge5$, the first five gap images exist. Upper gap hosts are second centers with $b\ge2$, since $u$ has no direct leaves. Their minimum possible image is $b+2\ge4$. Lower translations are nonnegative, so image zero forces source zero at the unique neutral reduced slot $A-1$. Inductively after using sources $0,\ldots,j-1$, image $j\le3$ can only come from source $j$ with shift zero. These sources are lower since $k\ge B\ge4$. The neutral slot must be an actual first center at $A-1$ of quota four with all its terminals in the gap. In particular it is neither the selected second terminal nor $w$. This exhausts the neutral center.

Now image four cannot come from a lower host. A positive shift would use a consumed source and the neutral capacity is exhausted. The upper formula forces $b=2, i=s-1$, so a second center occupies $A+2$ with residual capacity. At $B=4$ it needs at least two residual leaves. Indeed the first physically upper source $i=k$ cannot use a lower host because $k+A-1-j\le K-1$, which fails its crossing requirement. An upper host gives the noncrossing image $K-B+b+1$, requiring $b\le B-2=2$. The two sources $k$ and $s-1$ are distinct since $s-k=K-B\ge A\ge5$. The argument below uses the forced incidence at $A+2$ even before $B$ is determined.

Let $t\in[1,A-1]$ be the unique selected second terminal's reduced label. Its replaced reference edge removes weight $D_t=A+1-t\in[2,A]$. Every unaffected reference edge has a different weight. The new edge at $t$ has weight $D_t+b-1>D_t$ at its actual upper parent of index $b\ge2$. There is no exterior direct leaf. Thus restoring $D_t$ requires a selected first terminal. If its upper index is $b'$ and its actual lower parent has label $j$, the required equality gives $j=b'+t-1$. The forced second center at upper index two excludes that index for this terminal, so $b'\ge3$ and $j\ge t+2$.

Every other selected first terminal has parent label at least one, even when several terminals share a parent. Terminal balance and $b\le B$ give
$$
t+e_1+1\le\sum j=b-1\le B-1=e_1+2.
$$
Thus $t=1$. Every first-center label is now at least two, because label one is occupied by this selected terminal. The restoring parent is at least three. Counting again, $2e_1+1\le\sum j\le e_1+2$, so $e_1=1, B=4$. The assignments forced by these equalities are first parent $j=3$, selected first terminal at $A+3$, and selected second terminal at 1 attached to the second center at $A+4$. In particular the parity gate is applied after ruling out every other count and width.

For an actual gap permutation $\sum_i(\pi(i)-i)=0$. Compute its parity from the actual residual hosts. The first centers have even full quotas and their shifts are $A-1-j$. Removing the selected first terminal at $j=3$ makes the total first-center contribution odd because $A-4$ is odd. The gap direct leaf at $w=0$ contributes the even shift $A-1$. Since $s=2K-A-4$ is odd, the two upper reflection intercepts $s+3,s+5$ are even. Each of their assignments contributes that intercept minus $2i$, hence an even term, whatever its residual quota. The sum is odd, a contradiction. This excludes every H0 completion in this exact domain.

The forced-width reduced geometry is itself an independent raw H0 supplier. Give the first centers slots $[2,A-1]$, assigning a quota-four center to $A-1$. Choose a terminal at the actual center 3 for label $A+3$ and a second terminal at the actual center $A+4$ for label 1. The second centers are $A+2,A+4$ in either chosen role order. The actual direct leaf remains at its original host in the gap. With $v=A,u=A+1,w=0$, these actual exterior vertices fill $[0,A+4]$ bijectively. Its connected edges all cross. The edges at $u$ to $v$ and the first centers have differences $[1,A-1]$, and the first terminal gives $A$. On the other side the connector and the two center attachments give $A+1,A+2,A+4$ and the second terminal gives $A+3$. Thus the reduced differences fill $[1,A+4]$. Both positive second quotas are at least two. The center at upper index two has no selected terminal and retains that capacity, and the neutral center keeps all four leaves. The width is admitted since $F\ge2r+2$ and $K-(A+4)=F/2-2\ge r-1$. This includes $r=3$, where $A=5$, all slots and selected parents are distinct and $k\ge4$ for every compatible candidate. Raw supply and the H0 obstruction both apply there.

## 3. Independent H1 exterior on the narrower inventory

Take odd $r\ge5$, first inventory $(2^{r-1},4)$ and actual second quotas $(2,r+1,0)$, with either physical center order and the direct leaf at its declared index. Then $F=2r+2$ and $K=2r+5$. Set $A=r+2,B=5,s=3r+3,k=r+3$. We have $K-(A+B)=r-2\ge3$, so the size and membership inequalities hold. Assign $v=A,u=A+1,w=0$. Put the actual quota-four center at $A-1$ and the quota-two centers at the other first slots $\{1\}\sqcup[3,A-2]$ by original index. The upper parent $Q=A+2$ has full quota $r+1$, and $P=A+5$ has full quota two. Select the first actual terminal at first center 4 for label $A+3$ and the first actual terminal at $P$ for label 2. The actual direct leaf at $w$ gets $A+4$.

The labels are exactly $[0,A+5]$. Every chosen terminal and the direct leaf is attached to its original parent. The resulting connected tree crosses the reduced cut. The edges from $u$ to $v$ and to the first centers give reduced weights $1,[2,A-2],A$, with the first terminal restoring $A-1$. The connector $uw$, the edge $wQ$, the terminal edge at $P$, the actual direct-leaf edge and the edge $wP$ give $A+1,A+2,A+3,A+4,A+5$, respectively. These are disjoint and fill $[1,A+5]$. The exterior and its roles are supplied by parameters and actual indices.

## 4. Explicit gap bijection at every admitted multiplicity

Write $J=s+3=3r+6$, $L_j=j$, $H_j=J-j$. The actual source bands $[0,k-1]$, $[k,s-1]$ and actual image bands $[0,K-1]$, $[K,s-1]$ from §1 give the folded rows
$$
\begin{array}{c|cc}
 & L & H \\
\text{sources} & [0,r+2] & [4,2r+3] \\
\text{images} & [0,2r+4] & [4,r+1].
\end{array}
$$
A first host of displacement $\delta=A-1-j$ sends $L_i\to L_{i+\delta}$ and $H_i\to H_{i-\delta}$. The available first shifts are $0,[1,r-2],r$. The shift zero has quota four, shift $r-3$ has gap quota one after the selected terminal, and every other positive shift has quota two. The upper formula gives $Q$ the same-index row exchange and $P$ the row exchange with offsets $-3$ on L and $+3$ on H. The gap direct-leaf capacity is zero. These arrows use the two different alphabets above. In the L source row lower hosts are noncrossing and upper hosts crossing. In the H source row lower hosts cross and upper hosts do not. These are precisely the L/H destination statuses, since H images represent $\pi(i)\ge K$.

Use $L_0,L_1,L_2,L_3$ at shift zero with the identical images. For each $j\in[4,r-2]$ use one leaf at the first host of displacement $j-3$ in each row:
$$
L_j\longmapsto L_{2j-3},qquad H_{2j-3}\longmapsto H_j .
$$
There are $r-5$ such pairs, empty for $r=5$. In addition prescribe the following first-host reservations.

| Source | Host shift | Destination |
| --- | ---: | --- |
| $L_{r-1}$ | $r$ | $L_{2r-1}$ |
| $L_r$ | $r-4$ | $L_{2r-4}$ |
| $L_{r+1}$ | $r$ | $L_{2r+1}$ |
| $L_{r+2}$ | $r-4$ | $L_{2r-2}$ |
| $H_{2r-1}$ | $r-2$ | $H_{r+1}$ |
| $H_{2r-4}$ | $r-3$ | $H_{r-1}$ |
| $H_{2r-2}$ | $r-2$ | $H_r$ |

The paired shifts range exactly over $[1,r-5]$. The table gives both uses of $r-4,r-2,r$ and the single residual use of $r-3$. This accounts for every actual first quota, including the quota restored at shift $r-3$ by its selected terminal. All L sources are consumed, and the first-host H images fill $[4,r-2]\sqcup\{r-1,r,r+1\}=[4,r+1]$. Let
$$
U=\{2j-3:4\le j\le r-2\},qquad
Y=U\sqcup\{2r-4,2r-2,2r-1\}.
$$
The variable pair columns lie in $[5,2r-7]$ when nonempty. The three special columns of $Y$ are distinct and above that interval, and $2r+1$ lies strictly above $Y$. All four special columns lie in $[4,2r+3]$ also at $r=5$. Hence the H source reservations are exactly $Y$, and the nonneutral first-host L images are exactly $Y\sqcup\{2r+1\}$. Both image rows have disjoint prescribed cells.

Give $H_{2r+1}$ to $P$, with image $L_{2r+4}$. Give every other surviving H source to $Q$ with identical L index. The Q source indices are
$$
V=[4,2r+3]\setminus(Y\cup\{2r+1\}).
$$
They also give exactly the remaining L destination indices after taking $L_{2r+4}$ at $P$. Their number is $2r-|(Y\cup\{2r+1\})|=2r-(r-1)=r+1$. The single residual leaf at $P$ and its exterior terminal give full quota two. The direct leaf has already been used in the exterior. All source and image cells are now accounted for. There are $x=0$ lower-to-upper-host crossings and $y=|Y|=r-2=s-K$ upper-to-lower-host crossings.

In the [D168 residue-path formulation](ORDINARY_SPINE_EXCEPTIONAL_TWO_UPPER_HOST_RESIDUE_COMPRESSION.md#4-exact-residue-path-criterion) the L-to-H residual matching is empty. In the H-to-L direction, use the encompassing interval $[4,2r+4]$. The source holes are $Y\cup\{2r+4\}$, where $2r+4$ is the absent boundary cell, and the destination holes are $Y\cup\{2r+1\}$. The common holes lie strictly below $2r+1$. The holes at $2r+1,2r+4$ belong to one residue modulo three and the single shifted assignment repairs that path without crossing any common hole. This is the same exact treatment of an absent far-boundary cell used in [D173](ORDINARY_SPINE_EXCEPTIONAL_ALTERNATE_EXTERIOR_RESIDUE_GROWTH.md#3-exact-reservations-and-residue-ray). D173 grows the second quotas on a fixed exterior and D168 compression fixes the lower-host data. Here $r$ changes the width and actual first inventory, so supply follows from the parameterized reservations above.

## 5. Exact named lifting, resources and phase

Keep all original names and incidences. At each parent assign its increasing numerical gap sources to its remaining indexed leaves in original index order, after the two prescribed exterior selections. This is a bijection at each actual host by the quota counts. For the old vertices use the oriented shifts $A$ below $c$ and $A+s$ at or above $c$. Their old cut membership is preserved at $C=c+K$. Use oriented label $A+c+i$ at each gap source and add $n+s$ to the upper exterior labels. The shared exterior $v=A$ agrees with the old embedding. The exact D157 palettes are
```text
old labels   [A,A+c−1] ⊔ [A+c+s,n+s+A]
fresh labels [0,A−1] ⊔ [A+c,A+c+s−1] ⊔ [n+s+A+1,m]
old weights  [1,d−2] ⊔ [d−1+s,n+s]
fresh weights [d−1,d+s−2] ⊔ [n+s+1,m].
```
Old noncrossing differences are unchanged and old crossing differences gain $s$ and still cross. Each expanded exterior edge gains $n+s$ and crosses since its lower endpoint is at most $A<C$ and its upper endpoint is at least $n+s+A+1>C$. The gap bijection gives its entire label and difference intervals. The physical crossing test in §4 gives gap crossing weights $[d+K-1,d+s-2]$ and noncrossing weights $[d-1,d+K-2]$. Together the disjoint partitions give labels $[0,m]$ and actual differences $[1,m]$, with crossing weights $[d+K-1,m]$ and noncrossing weights $[1,d+K-2]$. The appended edges are exactly the original spine and pendant incidences. The witnessing spine extends through $u,w$. Because $m=2(c+K)+2$ and $w=0$, the output is the exact oriented $S_{-1}$.

At the first-section boundary the gap sources and images are
$$
I=[0,r+2]\sqcup(J-Y),qquad
J_1=[0,3]\sqcup Y\sqcup\{2r+1\}\sqcup[K,s-1].
$$
Here $J-Y=\{J-j:j\in Y\}$. The source sets split by the original individual first hosts and $J_1$ is their disjoint union after translating each actual numerical source by its own host shift. The remaining gap sources and images are their exact complements $I'=(J-V)\sqcup\{J-(2r+1)\}$ and $J_2=V\sqcup\{2r+4\}$. In the oriented alphabet the first exterior label set $E_1$ consists of $\{1\}\sqcup[3,A-1]\sqcup\{n+s+A+1,n+s+A+3\}$. The remaining exterior set is $E_2=\{0,2,n+s+A+2,n+s+A+4,n+s+A+5\}$. Their difference sets are $n+s+[1,A]$ and $n+s+[A+1,A+5]$, respectively. With $L_{old},D_{old}$ the old palettes above, this yields
```text
used labels        L_old ⊔ E₁ ⊔ (A+c+I)
remaining labels   E₂ ⊔ (A+c+I′)
used differences   D_old ⊔ (n+s+[1,A]) ⊔ (d−1+J₁)
remaining weights  (n+s+[A+1,A+5]) ⊔ (d−1+J₂).
```
The used lower labels are the old lower band, the low first exterior slots and $A+c+[0,r+2]$. The used upper labels are the old upper band, the two first high exterior slots and $A+c+(J-Y)$. The remaining lower labels are $\{0,2\}$, and all other remaining labels are upper. Used crossing differences are the old high weight band, the first exterior weights and $d-1+[K,s-1]$. Used noncrossing differences are the old low weight band and $d-1+([0,3]\sqcup Y\sqcup\{2r+1\})$. Remaining crossing differences are exactly the remaining exterior weights, and remaining noncrossing differences are $d-1+J_2$. The unfinished edge is literally $uw$ with oriented endpoints $(n+s+A+1,0)$, so its crossing weight $n+s+A+1$ belongs to the second exterior inventory.

Minimum polarity uses the oriented labels. For maximum polarity express the actual input label as $n-G$ and complement the output about $m$. The actual input and output cuts are $n+1-c$ and $m+1-C$. The actual old lower and upper shifts become $B=5$ and $B+s$; in minimum polarity they are $A=r+2$ and $A+s$. These identities follow by substituting the reflected input into its actual lower or upper branch of the old map and using $2K=A+B+s$. Both actual label inventories and their side partitions transform by complementation, with sides exchanged. All actual differences and crossing statuses are fixed. The maximum-polarity frontier is $w=m$ and the unfinished connector has actual endpoints $(4,m)$.

## 6. Controls, unbounded admission and composition

At $r=5$ the paired range is empty. The first L sources 4, 5, 6, 7 map to 9, 6, 11, 8 at their prescribed parents and the H source indices 9, 8, 6 go to H indices 6, 5, 4. The sole P gap assignment is $H_{11}\to L_{14}$. $Q$ uses H indices $4,5,7,10,12,13$. With $J=21$, these are exactly the 18 numerical source/host/image triples in the [retained D174 target-0991 H1 record](../evidence/runs/d174-exceptional-five-first-direct-001/raw/target-0991-H1.json), including the four neutral sources. The selected terminals, numerical roles and direct-leaf placement also agree. For $n=74$ with that maximum input, $c=36$, the resulting actual cut is 54 and the spectra are $[52,104]$ and $[1,51]$. The literal unfinished edge has actual endpoints $(4,104)$ and weight 100. The remaining actual labels are $\{0,1,3,44,45,47,50,51,52,53,102,104\}$. The remaining weights are $\{41,42,44,47,49,50,51\}\sqcup[100,104]$. Their complements agree with the saved used inventories. The historical H0 result retains its distinct exhaustive numerical basis.

The D174 all-even $R=8$ stratum has $2^5-1=31$ ordered first profiles with a four and the three ordered second profiles $(2,6,0),(4,4,0),(6,2,0)$. All 93 named originals satisfy §2 with $r=5$ and the retained prefix size, since $F\le20$ gives $K\le19<74/2$. That is a new symbolic implication for the frozen graphs. D174 retains one completed pair and two numerical arms. The other 92 of these 93 originals and all other unentered originals keep their historical unentered statuses. D172 and D173 are separately scoped four-first-center controls.

For each finite requested $r$, an independently supplied admitted $S_{-1}$ can meet $n\ge2K$ using the arbitrary-large admissible-size supply in [D157 §7](ORDINARY_SPINE_ALTERNATING_EXCEPTIONAL_SPECTRUM.md#7-independent-supply-cycle-closure-and-immutable-labels) under its retained D134 initializer, named path and branching premises. This gives an unbounded family of original transitions. No assertion of availability at every numerical prefix size is needed.

For any individually admitted finite list, retain each block's actual frontier, input phase, contract, cut membership, original incidence and size premises. Let $C_i$ be the actual cut at completed boundary $i$, $L_i$ the sum of all later actual lower shifts and $S_i$ the sum of all later gap widths. Since each later admitted placement preserves old side membership, the final image of a label from this boundary is $x+L_i+S_i\mathbf{1}_{x\ge C_i}$. Each crossing difference gains $S_i$ and each noncrossing difference is fixed. The same transformation applies to the used labels and weights at the partial boundary in the same alphabet and to both fixed endpoints of its crossing unfinished connector. Final reserves are the exact complements in the final alphabets. Induction on the admitted interfaces proves both graceful bijections after each block. The translated representation gives immutable final label emission. These transformations also allow D157 legs with their own phase and size hypotheses. A finite backward scan produces the later shift sums, and finite scans of the stated intervals and original names emit each label and incidence once. This proves termination for the given finite admitted list.

## 7. Scope

The proved separator family combines the complete symbolic H0 obstruction of §2 with the independently supplied H1 witness of §§3–5, for all stated physical orders, all odd $r\ge5$ and every independently supplied prefix satisfying the exact interface and size premises. No new search was needed. Other H1 first inventories, other second splits and the $r=3$ H1 boundary are open in this investigation. This is a statement about exceptional returns in the declared arrangement. D173's full feasible domain and the independent pinned shell initializer remain separate.
