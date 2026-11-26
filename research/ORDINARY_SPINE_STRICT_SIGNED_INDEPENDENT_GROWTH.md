# D192 — Strict-phase independent signed growth

Task **LCL-ORDINARY-SPINE-STRICT-SIGNED-INDEPENDENT-GROWTH-001**.

**PROVED WITHIN EXACT WRITTEN SCOPE / PENDING DIRECTOR REVIEW.** The two signed first hosts and two actual upper hosts give the stated exact movable-defect baseline domains. One complete Q exchange pair gives independent even growth at either one first host. Two disjoint Q pairs give independently prescribed even growth at both first hosts, with the original Q and P quotas preserved. Every construction uses the actual original topology and a fully admitted independent strict-phase prefix. D191 and D188–D190 remain separately accepted suppliers.

All labels and parameters are integers, excluding booleans. Intervals are inclusive and inverted endpoints denote the empty set. Quotas are attached to indexed original centers. We write $d_0=c+2$ for the old strict spectrum boundary, reserving $d$ for the movable defect.

## 1. Actual exterior and strict gap rows

Let $h\ge2$, $a=2h-1$, $\omega=2h-2$, and fix $A=B=2h+1$, $\gamma=2h$. There are two actual centers and $2h-3$ direct leaves at each appended spine vertex, so the first child count is $a$ and the second is $\omega+1=a$. Use an independently supplied [D157 $S_0$ input](ORDINARY_SPINE_ALTERNATING_EXCEPTIONAL_SPECTRUM.md#1-interface-and-exact-inventory-rule) with $n=2c+2$, actual witnessing spine ending at an extreme $v$, crossing differences $[d_0,n]$ and noncrossing differences $[1,d_0-1]$ in its minimum orientation. The minimum-oriented old cut is $c$ with equality on the upper side. The full actual target must satisfy $n\ge2K$, with $m=n+2K$. Append the actual spine vertices $u,w$.

Use reduced $v=A,u=A+1,w=0$. At $u$ put the actual positive-shift and negative-shift centers at $j_+=A-3=2h-2$ and $j_-=A-1=2h$. They are distinct elements of $[2,A-1]$ even at $h=2$. Give the $2h-3$ original first direct leaves the other slots of that interval, in original index order. One actual first terminal from the positive-shift center takes $A+j_+$. The actual Q and P children of $w$ take $A+b_0,A+b_0+1$ where $b_0=j_++1=2h-1$. These indices are in $[2,B]\setminus\{j_+\}$. The $2h-3$ original second direct leaves take all its remaining slots. One actual Q terminal takes 1. The low labels are exactly $[0,A]$, the upper labels exactly $[A+1,A+B]$. The exterior is connected, since each listed incidence is an original parent incidence and both spine edges are present. Every edge crosses these reduced sides.

In the first section $vu$ uses 1, the original first children use differences $[2,A-1]$ by subtraction from $A+1$, and the selected first terminal uses $A$. At the second section $uw$ uses $A+1$. The actual second child edges use $A+b$, $b\in[2,B]\setminus\{j_+\}$. The omitted difference $A+j_+$ occurs on the selected Q terminal because $A+b_0-1=A+j_+$. This is the exact reduced edge bijection onto $[1,A+B]$ on the actual named exterior.

Write $F$ for the first terminal total and $R=p+q$ for the second. Here $p$ means the full actual Q quota and $q$ the full actual P quota. Two spine edges, $4h-2$ child edges and $F+R$ terminal edges give $2K=4h+F+R$. At baseline $F_0=2h+2$, hence
$$
2K_0=6h+2+R,\quad s_0=2K_0-A-B=2h+R,\quad
k_0=K_0-A=h+R/2,\quad J_0=s_0+b_0.
$$
The fresh lower graph color (relative to lower $v$) contains $w$, all first children and all second terminals, and the fresh upper color contains $u$, all second children and all first terminals. The counts are $1+a+R=2h+R$ and $\omega+2+F=2h+F$. With the stated parities both are even. For the same phase, if $x$ counts lower gap sources at upper hosts and $y$ upper gap sources at lower hosts, the exact identities are $2(A+x)=2h+R$, $2(B+y)=2h+F$, and $x+y=s-K$. These follow by counting the gap leaves by side of parent and the crossing images $[K,s-1]$ as in D157 §2. At baseline $x=k_0-\gamma-1=R/2-h-1$, $y=0$ and $s_0-K_0=x$. The admitted companion baseline has $R\ge\gamma+2$ and the low baseline has $R\ge\gamma+4$ as proved below. Thus $s_0\ge K_0$, $k_0>0$, and $A\le K_0\le A+s_0$, including the companion equality $s_0=K_0$.

At any width of the construction set $s=2K-A-B$, $k=K-A$, $J=s+b_0$. The actual cut is $C=c+K$. A gap source $i$ denotes label $A+c+i$, which is lower exactly when $i<k$. The actual weight at image $\pi$ is $d_0+\pi$. A lower reduced parent $j$ gives $\pi=i+A-2-j$ by subtracting its unchanged lower label. An upper parent $A+b$ is expanded to $n+s+A+b$, giving $\pi=s+b-i$ because $n-c=d_0$. The two exterior bands flank the gap, so these subtraction signs are exact. The first shifts are $+1$ at $j_+$ and $-1$ at $j_-$. The cut crossing test is $\pi\ge K$ exactly for an upper source at a lower parent or a lower source at an upper parent.

Fold by $L_i=i,\ H_i=J-i$. Numeric H sources and images are $[k,s-1]$ and $[K,s-1]$, with exact numeric L complements $[0,k-1]$ and $[0,K-1]$. Since $J-(s-1)=b_0+1=\gamma$, the baseline folded rows (writing $k=k_0$ here) are
$$
L_{\rm src}=[0,k-1],\qquad H_{\rm src}=[\gamma,k+\gamma-1],\qquad
L_{\rm im}=[0,k+\gamma],\qquad H_{\rm im}=[\gamma,k-2].
$$
They follow from $J_0=2k+\gamma-1$ and $K_0=k+\gamma+1$. The same endpoint relations hold after growth. In particular the H-image row is empty when $k=\gamma+1$. A first numerical shift $\delta$ stays in the row, with folded shifts $\delta$ on L and $-\delta$ on H. Q exchanges rows at equal indices. P exchanges L to H by $-1$ and H to L by $+1$. All legal arrows in these rows obey exactly the physical crossing predicates. Neither first host is neutral in the strict coordinates.

## 2. Two exact movable-defect baselines

At baseline put the adjacent pairs $(0,1),(2,3),\ldots,(\gamma-2,\gamma-1)$ in L. At each even source use the positive-shift center for its next image and at the following odd source use the negative-shift center for the preceding image. These are $h$ actual terminals at each center. The sole additional first gap arrow is the defect. In the low arm the positive host has quota $h+1$ with one selected exterior terminal and the negative host has quota $h+1$ with no exterior selection. Its defect is at the negative host. In the companion the positive host has quota $h+2$ with one exterior selection and the negative host has quota $h$, so its defect is at the positive host. Both arm counts are exact.

### Low arm

For $\gamma+1\le d\le k-1$ use $L_d\to L_{d-1}$ at the negative host. After reserving the initial transpositions and the defect, make the following upper assignments, using the actual Q and P row exchanges.

| Host | L sources | H sources |
|---|---|---|
| Q | $[\gamma,d-1]$ | $[\gamma,d-2]$ |
| P | $[d+1,k-1]$ | $[d-1,k+\gamma-1]$ |

The L sources are the exact complement of the transpositions and defect. The H sources partition at $d-1$. Q and P fill the respective H images $[\gamma,d-1]$ and $[d,k-2]$, hence all H images. Their L images are $[\gamma,d-2]$ and $[d,k+\gamma]$, precisely the L complement of the first images. This verifies both alphabets including $d=\gamma+1$ and $d=k-1$. Counting the two Q intervals and its selected exterior terminal gives $p=2(d-\gamma)$. Both P intervals give $q=2k+\gamma-2d=R+2\gamma-2d$. Thus the prescribed interval corresponds bijectively to the even splits $p\ge2$, $q\ge\gamma+2=2h+2$, $p+q=R$, via $d=\gamma+p/2$. This is exact within this movable-defect construction. At $h=2,q=6$ it gives $d=k-1$ and exactly D191's low arm.

### Companion arm

For $\gamma\le d\le k-1$ use $L_d\to L_{d+1}$ at the positive host. The remaining lists are

| Host | L sources | H sources |
|---|---|---|
| Q | $[\gamma,d-1]$ | $[\gamma,d]$ |
| P | $[d+1,k-1]$ | $[d+1,k+\gamma-1]$ |

These partition the free L sources and all H sources. The H images are again $[\gamma,d-1]$ and $[d,k-2]$. The L images are $[\gamma,d]$ and $[d+2,k+\gamma]$, the complement of the first L images. This includes $d=k-1$ and the empty H-image row when $q=\gamma,p=2$. The total at Q is $p=2(d-\gamma+1)$ including its selected terminal. P has $q=2k+\gamma-2-2d=R+2\gamma-2-2d$. Thus the exact prescribed-model domain is even $p\ge2,q\ge\gamma=2h,p+q=R$, with $d=\gamma-1+p/2$. At $h=2,q=6$ this gives $d=k-2$ and recovers D191's companion. At $h=2,q=4$ it gives the new endpoint $d=k-1$.

In either arm every first arrow is L to L. Upper arrows with L sources are exactly $k-\gamma-1$ and are the crossing ones, so $x=k-\gamma-1$, $y=0$, agreeing with the independent graph count. The full geometric folded index moment is the sum of image indices minus the sum of source indices. The L difference adds $A$ indices starting at $k$ and the H difference removes $A$ starting at $J-K+1$. Thus the moment is $A(k-J+K-1)=A(B-\gamma)=A$. Independently, the initial transpositions contribute zero, the low defect contributes $-1$ and the companion defect $+1$. The P contribution is the H count minus the L count, respectively $\gamma+2$ and $\gamma$ by the tables. Q contributes zero. The totals are both $\gamma+1=A$. These identities also hold at empty endpoints. They do not characterize other allocations or exteriors.

## 3. One or two named Q anchors and independent first-quota growth

The initial $\gamma$ L arrows are the actual signed transpositions just supplied. Their sources and images are exactly $[0,\gamma-1]$, and every other folded endpoint has index at least $\gamma$ (the low defect image is at least $\gamma$). A complete Q exchange at a column means both $L_i\to H_i$ and $H_i\to L_i$ at that same actual center, with two distinct actual residual terminal names. In either arm their common Q interval has length $p/2-1$, starting at $\gamma$: this is $[\gamma,d-2]$ in the low arm and $[\gamma,d-1]$ in the companion. Thus $p\ge4$ supplies both directions at $\gamma$, and $p\ge6$ supplies them at $\gamma,\gamma+1$. At $p=4$ exactly one complete Q pair is present in this baseline. These are actual Q terminals separate from its selected exterior terminal.

Let the selected first hosts gain $2\lambda_+,2\lambda_-$ terminals, with $\lambda_\pm\ge0$ and $\lambda=\lambda_++\lambda_-$. The one-pair operation uses only one sign, with the other increase zero. The two-pair operation uses both signs, with a sign allowed zero increase. From the actual original count with $F=F_0+2\lambda$ and unchanged $R$ we obtain $K=K_0+\lambda$, $s=s_0+2\lambda$, $k=k_0+\lambda$, $J=J_0+2\lambda$. Thus each folded row extends its right endpoint by $\lambda$ with the same left endpoint. Since $s-K=(s_0-K_0)+\lambda$, $A\le K\le A+s$ still holds and the cut membership is preserved by the full admitted geometry.

For $b=1$ or 2 anchor pairs, keep the $\gamma$ signed transpositions fixed. Translate every other folded endpoint by $\lambda$ in its own row, at its actual parent. This preserves row maps and leaves exactly the common strip $[\gamma,\gamma+\lambda-1]$ free in each row. Remove the entire translated set of the $b$ selected Q pairs, keeping their actual names and row directions. In each row this opens the adjacent set $[\gamma+\lambda,\gamma+\lambda+b-1]$. The exact available interval is therefore $[\gamma,\gamma+\lambda+b-1]$ in all four rows. No other translated endpoint lies inside it. The calculation is also valid at $\lambda=0$, when only the removed pairs form the strip.

When $b=2$, split that interval into consecutive blocks of lengths $\lambda_++1$ and $\lambda_-+1$, in positive-sign then negative-sign order. Retain the first original anchored pair for the first block and the second pair for the second. In a single-anchor growth use the whole interval $[\gamma,\gamma+\lambda]$ as the block for the chosen sign. The two possible instructions on a block $[a_*,b_*]$ are as follows.

- For the positive sign use $L_i\to L_{i+1}$ and $H_{i+1}\to H_i$ at the actual positive first center for $a_*\le i<b_*$. The used L sources are $[a_*,b_*-1]$ and L images $[a_*+1,b_*]$. The H sources are $[a_*+1,b_*]$ and H images $[a_*,b_*-1]$. The remaining actual Q arrows are $H_{a_*}\to L_{a_*}$ and $L_{b_*}\to H_{b_*}$. These fill the one missing source and image in each row, using the original pair's corresponding H and L names. This adds exactly $2(b_*-a_*)$ at the positive host.
- For the negative sign use $L_{i+1}\to L_i$ and $H_i\to H_{i+1}$ at the actual negative first center for $a_*\le i<b_*$. The L sources are $[a_*+1,b_*]$ and images $[a_*,b_*-1]$, with the H sources $[a_*,b_*-1]$ and images $[a_*+1,b_*]$. Close with $L_{a_*}\to H_{a_*}$ and $H_{b_*}\to L_{b_*}$, using the original L and H names. The four alphabets again partition exactly. This adds exactly $2(b_*-a_*)$ at the negative host.

In length one, a block is just its Q exchange with both original named terminals. The blocks are disjoint across every source and image row and fill the precise freed intervals. All entries are genuine allowed maps in the strict folds. Neither operation changes Q or P quotas: the removed Q names are restored in the same row directions and all P endpoints undergo the common translation only. The added first arrows have opposite signed folded displacements in the two rows, so the folded moment remains $A$. The Q L-to-H count is restored and P retains its count, giving $x=k_0-\gamma-1$. Each extra pair of first arrows contributes one H image, so $y=\lambda$. This independently confirms the grown graph classes and $x+y=s-K$. The result uses one anchor for growth in one sign and two for the two independently specified signs.

Thus, for $p\ge6$, the supplied first profiles in numerical sign order are $(h+1+2\lambda_+,h+1+2\lambda_-)$ for the low arm and $(h+2+2\lambda_+,h+2\lambda_-)$ for the companion, each with $2h-3$ actual direct leaves. The actual second quotas are even $p\ge6$ and $q\ge2h+2$ or $q\ge2h$ respectively with $2h-3$ actual second direct leaves. This holds for every admissible $h,\lambda_\pm$ and size $2K=6h+2+p+q+2\lambda$, with selectable numerical roles on the actual original. The broader no-growth $p\ge2$ domains and the one-sign $p\ge4$ domains retain their respective conditions.

The stored 94-edge prefix supplies all fitting sizes. For unbounded admitted sizes, D157 §7 supplies independently initialized strict inputs of arbitrarily large admitted sizes under the stated D134 seed and named-spine premises. The family is conditional on independent full-size admission at each application.

## 4. Indexed realization and exact numerical first resources

Select numerical roles by the actual available quotas, breaking ties by original branch index and allowing either physical order. If the sign roles are specified, require their exact quotas. Set the exterior to §1 before assigning any gap terminals. Select the first indexed terminal of each of the positive first center and Q for its indicated exterior incidence. At each first center reserve the required baseline residual names in increasing original terminal order, assign them to the baseline source list in increasing numeric order, and keep the additional unused names for that center's packet. At each second host use its actual remaining terminal indices, with baseline arrows assigned in increasing unfolded source order. This defines which named Q terminals form the anchor pairs before growth. Translate all retained arrows and reassign the original Q anchor names according to their directions as in §3. Within each new first-host packet assign unused names in increasing unfolded source order. Exact arrow counts and the unchanged actual parents prove a bijection at every physical host. Direct leaves stay in their own indexed exterior slots. The auxiliary baseline describes calculations and reservations on the actual final target. No earlier physical target with different quotas is required.

Use the final $J=J_0+2\lambda$. Every translated H endpoint of old index $i$ unfolds to
$$
J-(i+\lambda)=J_0-i+\lambda ,
$$
so it gains the same numeric increment as a translated L endpoint. Fixed initial L arrows keep their actual indices. Restored Q anchors have their explicit packet endpoints, unfolded using the final $J$; they are not simply translated. The resulting first-host sets can therefore be written exactly as follows.

Put $E=\{0,2,\ldots,\gamma-2\}$ and $O=\{1,3,\ldots,\gamma-1\}$. Let $S_+$ and $S_-$ start with $E$ and $O$, respectively. Add $\{d+\lambda\}$ to the defect's actual sign set. For an active positive-sign block $[a_+,b_+]$ add
$$
[a_+,b_+-1]\ \sqcup\ [J-b_+,J-a_+-1]
$$
to $S_+$. For an active negative-sign block $[a_-,b_-]$ add
$$
[a_-+1,b_-]\ \sqcup\ [J-b_-+1,J-a_-]
$$
to $S_-$. These numeric intervals are the unfolded L and H packet source sets respectively. For an absent or one-cell block both its contributions are empty. Every union is disjoint by the four-row partitions and their distinct numeric L and H ranges. The exact first source set and first image set are
$$
I=S_+\sqcup S_-,\qquad J_1=(S_++1)\sqcup(S_--1).
$$
The shifts hold in numeric coordinates on both rows. Their exact complements in $[0,s-1]$ are $I'$ and $J_2$. This derives actual resource sets from the baseline and new arrows without any spectrum inference from quota counts.

The construction is deterministic with specified parameters and actual original indices. If only the two physical inventories are given, try the finite role assignments by indexed branch order and test the two stated arm quota equations and their even growth conditions. Ties retain the actual center identity. For a passing assignment compute $d$ by the relevant formula, reserve the original names, generate the finite interval lists, and lift as below. This termination argument uses finite explicit arithmetic and no search through labelings.

## 5. Placed labels, differences and both intermediate resource inventories

In the minimum orientation place old labels by adding $A$ below $c$ and $A+s$ at or above $c$. Because $A\le K\le A+s$ the placements preserve sides at $C=c+K$. Old crossing differences gain $s$ and old noncrossing differences remain fixed. Place the original gap terminal for source $i$ at $A+c+i$. Keep reduced lower exterior values and add $n+s$ to the reduced upper values. The shared $v=A$ agrees with the placed old label and appears once. Each exterior edge crosses the actual cut by its endpoints, which are at most $A$ on the lower side and at least $n+s+A+1$ on the upper side. Its difference gains $n+s$. The old and fresh full palettes are
$$
\begin{array}{ll}
L_{\rm old}=[A,A+c-1]\sqcup[A+c+s,n+s+A],&
L_{\rm fresh}=[0,A-1]\sqcup[A+c,A+c+s-1]\sqcup[n+s+A+1,m],\\
D_{\rm old}=[1,d_0-1]\sqcup[d_0+s,n+s],&
D_{\rm fresh}=[d_0,d_0+s-1]\sqcup[n+s+1,m].
\end{array}
$$
These are disjoint partitions of $[0,m]$ and $[1,m]$ by $m=n+s+A+B$. The reduced, unfolded gap and old bijections fill all named vertices and actual differences exactly once. The gap images below $K$ and at least $K$ are the noncrossing and crossing bands, respectively. Together with the old and exterior edges they give noncrossing $[1,d_0+K-1]$, crossing $[d_0+K,m]$, a frontier $w=0$, and $m=2C+2$. This is precisely $S_0$. Every added edge joins the actual named incidence, and the extended witnessing spine has distance at most two to each fresh vertex.

At the first-section boundary the exact fresh exterior label sets are
$$
E_1=[2,A-1]\sqcup\{n+s+A+1,n+s+A+j_+\},\qquad
E_2=\{0,1\}\sqcup\{n+s+A+b:2\le b\le B,\ b\ne j_+\}.
$$
The interval in $E_1$ comprises the actual first children at $u$, including original direct leaves. The two upper values belong to $u$ and to the selected positive-host terminal. The lower values in $E_2$ belong to $w$ and the selected Q terminal, and its upper values are the actual children at $w$, including the other direct leaves. From the explicit incidence differences in §1 the first and remaining exterior bands are $D^e_1=n+s+[1,A]$ and $D^e_2=n+s+[A+1,A+B]$. The literal unfinished connector is $uw$ with actual endpoints $(n+s+A+1,0)$ and that actual difference in $D^e_2$. The two exact inventories are
$$
\begin{array}{ll}
\mathrm{used\ labels}&L_{\rm old}\sqcup E_1\sqcup(A+c+I),\\
\mathrm{remaining\ labels}&E_2\sqcup(A+c+I'),\\
\mathrm{used\ differences}&D_{\rm old}\sqcup D^e_1\sqcup(d_0+J_1),\\
\mathrm{remaining\ differences}&D^e_2\sqcup(d_0+J_2).
\end{array}
$$
The old labels split into their indicated lower and upper bands, and exterior labels retain the indicated reduced sides. Split $I,I'$ at $k$ before adding $A+c$, to give the gap label sides. Split $J_1,J_2$ at $K$ before adding $d_0$, giving noncrossing and crossing differences, respectively. The two exterior bands and the old high difference band cross. The old low band is noncrossing. These partitions include a possibly empty crossing gap at baseline.

For the actual maximum polarity start by complementing the input at $n$ and complement the output at $m$. The corresponding cuts are $n+1-c$ and $m+1-C$. Because $2K=A+B+s$, the actual old lower and upper shifts for maximum polarity are $B$ and $B+s$. The first and remaining label inventories complement with exchanged sides, preserving all difference inventories and cut crossings. The literal connector becomes $(B-1,m)$, with $w=m$. The graph and all names are unchanged.

## 6. Symbolic controls on the accepted strict input

Use the independent 94-edge maximum-polarity input from [D191](ORDINARY_SPINE_LOW_CAPACITY_STRICT_PHASE_MATCHED.md), with actual cut 49, frontier $s{:}29=94$ and crossing differences $[48,94]$. Its minimum-oriented $c$ is 46 and $d_0$ is 48. For each control give the first listed actual positive center the positive-shift role, the second listed the negative-shift role, and the first and second positive children of $w$ the Q and P roles. The actual direct leaves retain their indexed parents. These are symbolic calculations on the original profiles.

| Control | Actual first and second profiles | $h,\gamma$ | $R,k_0,d$ | $2K$ | $m$, maximum cut |
|---|---|---|---|---|---|
| A low | $(3,3,0),(2,6,0)$ | $2,4$ | $8,6,5$ | 22 | $116,60$ |
| A companion | $(4,2,0),(2,6,0)$ | $2,4$ | $8,6,4$ | 22 | $116,60$ |
| B | $(3,3,0),(4,8,0)$ | $2,4$ | $12,8,6$ | 26 | $120,62$ |
| C | $(4,2,0),(2,4,0)$ | $2,4$ | $6,5,4$ | 20 | $114,59$ |
| D positive | $(5,3,0),(4,6,0)$ | $2,4$ | $10,7,6$ | 26 | $120,62$ |
| D negative | $(3,5,0),(4,6,0)$ | $2,4$ | $10,7,6$ | 26 | $120,62$ |
| E | $(5,7,0),(6,6,0)$ | $2,4$ | $12,8,7$ | 32 | $126,65$ |
| F | $(8,6,0,0,0),(6,8,0,0,0)$ | $3,6$ | $14,10,9$ | 40 | $134,69$ |

In every row the full 94-edge input admits the fresh size. The exact actual return bands are $[48+K,m]$ and $[1,47+K]$, and the maximum connector is $(B-1,m)$. The individual row data are:

- **A.** The tables in §2 with $h=2,q=6$ give the D191 allocations with $d=k_0-1$ for low and $d=k_0-2$ for companion. The original reduced incidences, both gap lists and actual return agree. Both cross in $[59,116]$ at the actual cut.
- **B.** The low defect $6\to5$ is inside the admitted range $[5,7]$ rather than at its last endpoint. Q uses L $[4,5]$ and H $\{4\}$ plus its selected terminal. P uses L $\{7\}$ and H $[5,11]$. The H images are $[4,6]$ exactly. This gives the actual second quotas $(4,8)$ on the new ray.
- **C.** The companion has $s_0=K_0=10$, so H images are $[4,3]$ and both upper L lists are empty. The defect is $4\to5$. Q uses $H_4\to L_4$ plus its selected terminal. P uses H $[5,8]$ to L $[6,9]$. Together with the five first L sources and their images this gives exact alphabets. This original stratum II profile has a different topology from D191's two strict $R=6$ boundary originals.
- **D.** At the low baseline $(3,3,0),(4,6,0)$, Q has L $[4,5]$ and H $\{4\}$, so index 4 is its only complete exchange pair. With $\lambda=1$ the free block is $[4,5]$. Positive growth uses $L_4\to L_5,H_5\to H_4$ at the positive host, leaving the original Q names at $H_4\to L_4,L_5\to H_5$. Negative growth instead uses $L_5\to L_4,H_4\to H_5$ at the negative host, with the Q names at $L_4\to H_4,H_5\to L_5$. The translated defect is $7\to6$ in either case. The exact target first quotas are $(5,3)$ and $(3,5)$ respectively and second quotas stay $(4,6)$.
- **E.** At the low arithmetic baseline Q has L $[4,6]$, H $[4,5]$ and $J_0=19$. At actual Q the exterior terminal index is 0; increasing numeric source order assigns the L names at 4, 5, 6 the terminal indices 1, 2, 3 and the H names at 5, 4 the indices 4, 5. The two growth blocks are $[4,5]$ and $[6,8]$, with $(\lambda_+,\lambda_-)=(1,2)$ and final $J=25$. Restore Q's original index 1 at $L_5\to H_5$, index 5 at $H_4\to L_4$, index 2 at $L_6\to H_6$ and index 4 at $H_8\to L_8$. Its nonanchor index 3 moves to the translated L exchange at 9. Thus the original four anchor names are preserved, as are the other Q names and every P use. The packets add two and four terminals at the actual first parents.
- **F.** The baseline with $(4,4,0,0,0),(6,8,0,0,0)$ has $A=B=7$, $2K_0=34$, $s_0=20,J_0=25$. Q's complete exchanges are at indices 6 and 7. With $\lambda_+=2,\lambda_-=1$ the blocks are $[6,8]$ and $[9,10]$ and $J=31$. Their actual first counts add four and two, the second quotas stay six and eight, and the fresh size is 40. This verifies the widened exterior and the two packets together.

## 7. Exact frozen-corpus projection

At $h=2$ intersect only the baseline sufficient domains with D191's existing stratum II strict records. The ordered second positions may be assigned Q and P in either numerical order. Require both actual quotas even and at least two; require the actual quota at P at least six for low or at least four for companion. Equivalently the larger quota reaches that arm's threshold. Write the actual ordered pair as $(2i,2j)$ with $i,j\ge1$. For $R/2=t\in[3,8]$ there are $t-1$ even ordered pairs before the P restriction. For low remove the pairs with both $i,j\le2$ (two at $t=3$, one at $t=4$, none later). For companion all $t\ge3$ pairs already have some quota at least four. The resulting counts at $R=6,8,10,12,14,16$ are respectively
$$
\begin{array}{c|rrrrrr|r}
\mathrm{low}&0&2&4&5&6&7&24\\
\mathrm{companion}&2&3&4&5&6&7&27\\
\mathrm{both\ arms}&0&2&4&5&6&7&24 .
\end{array}
$$
Both physical orders are retained even when reversing them gives another admitted original. For each selected record the evidence binds the existing graph and record hashes, actual second branch indices for Q and P, and the exact role split and defect. It also binds the distinct exceptional-context original for each low projection member to the accepted D191 guard. This is direct read-only graph and quota arithmetic. Neither the rest of the strict corpus nor other placements acquire dispositions from this projection.

## 8. Admitted composition and scope

The construction takes the actual independently supplied $S_0$ boundary. Its output can feed D191, another admitted D192 block, or D157's compatible $S_0$-to-$S_{-1}$ leg. At an actual $S_{-1}$ boundary use the accepted D157 return leg where admitted before reusing a strict supplier. Each block respects the exact current spectrum, polarity, extreme frontier and named spine, and must meet its own full actual size inequality. For example, from the retained 74-edge maximum input the D157 return gives 94, control A adds 22, the D191 strict quota-one boundary at $R=8$ adds 20, and the admitted $(r,t,p)=(2,1,1)$ D157 outbound and return legs add 20 each. This gives $74\to94\to116\to136\to156\to176$ with maximum cuts $39\to49\to60\to70\to80\to90$, the phase sequence $S_{-1},S_0,S_0,S_0,S_{-1},S_0$, and final crossing differences $[89,176]$. Each stage uses new actual indexed spine sections.

For a finite admitted sequence fix the physical polarity. Each old placement preserves the two sides at its evolving cut, including across D157 phase changes. If $U_i,V_i$ sum the actual later lower shifts and gap sizes from an earlier completed cut $C_i$, the final label of an earlier local value $x$ is $x+U_i+V_i\mathbf1_{x\ge C_i}$. This follows by induction on the successive side-preserving old maps. Every earlier crossing difference gains $V_i$ and every earlier noncrossing difference is fixed. Both boundary inventories and the literal connector transport accordingly, including later fresh resources in the exact complements, disjoint by each successive palette. The finite local arithmetic and later sums give immutable final-alphabet realization on the original names and terminate.

The baseline quota statements are exact within the given defect lists. The growth statements are sufficient within their anchor and admission hypotheses. Other quota parities, fewer anchors for joint growth, other strict-phase allocations and unrestricted gracefulness remain open. D191's accepted existential resolution, broader exceptional guard, frozen originals and prospective algorithms remain intact. Its numerical lane is **SYMBOLICALLY_RESOLVED / NO_EXECUTION_NEEDED**. This task used no numerical search nodes, solver allocation states, original-checker calls, scientific campaign executions or historical replays.
