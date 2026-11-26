# D193 — Strict-phase residue-two allocation and anchor economy

Task **LCL-ORDINARY-SPINE-STRICT-RESIDUE-TWO-ANCHOR-ECONOMY-001**.

**PROVED WITHIN EXACT WRITTEN SCOPE / PENDING DIRECTOR REVIEW.** On the two specified strict exteriors, the baseline transpositions are forced and the remaining upper matching is exact in each residue. The separation-one parity obstruction holds for all successfully allocated first quotas on that fixed exterior. Balanced even first-quota growth uses no Q anchor, and one Q exchange pair suffices for arbitrary independent even first-quota growth under the stated baseline conditions. D192 and all earlier suppliers retain their own accepted scopes.

Intervals are inclusive and reversed endpoints mean empty sets. All quotas, counts and labels are exact integers, excluding booleans. Use $d_0=c+2$ for the strict input difference threshold, and $d,e$ for the defect's source and image. Numerical Q and P quotas are $p,q$ respectively, independent of actual branch order.

## 1. Two indexed strict exteriors

Take $h\ge2$, $a=2h-1$, $\omega=2h-2$, $A=B=2h+1$, and $\gamma=2h$. Both original sections have exactly two positive centers and $2h-3$ original direct leaves. Extend an independently supplied [D157 strict input](ORDINARY_SPINE_ALTERNATING_EXCEPTIONAL_SPECTRUM.md#1-interface-and-exact-inventory-rule) on $n=2c+2$ edges. In minimum orientation its actual extreme frontier $v$ is zero, its cut is $c$ (equality upper), and the actual crossing and noncrossing differences are $[d_0,n]$ and $[1,d_0-1]$. For the full actual target require $n\ge2K$ and put $m=n+2K$.

Use reduced $v=A,u=A+1,w=0$ at the actual spine vertices. At $u$ the positive and negative first centers occupy $j_+=A-3=2h-2$ and $j_-=A-1=2h$, respectively. Put the original first direct leaves in the remaining slots in $[2,A-1]$, retaining their actual indices. Select the first indexed terminal at the positive center for $A+j_+$. At $w$ give Q and P their upper indices $b_0=j_++1=2h-1$ and $b_0+\rho$ for $\rho\in\{1,2\}$. Fill the remaining actual second child slots in $[2,B]\setminus\{j_+\}$ with the original second direct leaves. Select the first indexed Q terminal for reduced label 1. The upper slot at index $B$ belongs to P when $\rho=2$. Only the original selected terminals occupy their new terminal slots. The exterior is connected by those actual incidences and the two spine edges, and all its edges cross between the lower labels $[0,A]$ and upper labels $[A+1,A+B]$. Those two ranges exhaust the reduced alphabet once.

By actual endpoint subtraction the first spine edge $vu$ has weight 1, all first child edges fill $[2,A-1]$, and the selected first terminal has weight $A$. The connector $uw$ has weight $A+1$. The actual second child edges fill $A+([2,B]\setminus\{j_+\})$, and the selected Q terminal uses the missing weight $A+b_0-1=A+j_+$. This proves the reduced difference bijection for both exterior layouts. All original children and both selected terminals remain at their actual physical parents.

The count of fresh edges is $2K=4h+F+R$, where $F$ is the first terminal total and $R=p+q$. Two spine edges and $4h-2$ child edges give the $4h$ term. The fresh graph colors relative to lower $v$ consist of $w$, first children and second terminals on one side, and $u$, second children and first terminals on the other. Their counts are $2h+R$ and $2h+F$. Since all children are exterior and all nonexterior vertices are actual terminals, D157's direct side count gives
$$
2h+R=2(A+x),\qquad 2h+F=2(B+y),\qquad x+y=s-K ,
$$
where $s=2K-A-B$, $x$ counts lower sources at upper parents and $y$ upper sources at lower parents. Indeed the fresh lower and upper exterior counts are $A,B$; at $k=K-A$ the gap adds $s-k-y+x$ lower-colored vertices and $k-x+y$ upper-colored vertices. The gap has $s-K$ crossing differences under strict return. Thus successfully allocated $F,R$ are both even. At either baseline $F_0=2h+2$, so $y=0$, $x=R/2-h-1$, and
$$
2K_0=6h+2+R,\quad s_0=2h+R,\quad k_0=h+R/2,\quad J_0=s_0+b_0.
$$
Success requires $R\ge2h+2$ by $x\ge0$. Every supplied baseline below satisfies that bound, hence $s_0\ge K_0$ and $A\le K_0\le A+s_0$. The full original size is separately required.

At cut $C=c+K$ place the numeric gap source $i$ at $A+c+i$, lower exactly for $i<k$. An image $\pi$ denotes actual weight $d_0+\pi$. An actual lower parent $j$ gives $\pi=i+A-2-j$, and an upper parent with expanded label $n+s+A+b$ gives $\pi=s+b-i$. These signs follow by subtraction from the lower and upper bands flanking the gap, using $n-c=d_0$. Lower shifts are $+1$ and $-1$, respectively. The crossing criterion is $\pi\ge K$ exactly when the actual source and parent have opposite sides. Define $J=s+b_0$ and fold using $L_i=i,H_i=J-i$. The numeric H ranges are $[k,s-1]$ for sources and $[K,s-1]$ for images; the numeric L ranges are their exact complements in $[0,s-1]$. The folded rows are
$$
L_{\rm src}=[0,k-1],\quad H_{\rm src}=[\gamma,k+\gamma-1],\quad
L_{\rm im}=[0,k+\gamma],\quad H_{\rm im}=[\gamma,k-2].
$$
In fact $J-(s-1)=b_0+1=\gamma$, $s=2k$, $K=k+\gamma+1$. The formulas apply at baseline and after even first growth, including the empty H-image case $k=\gamma+1$. A lower shift $\delta$ maps within L by $+\delta$ and within H by $-\delta$. Q exchanges rows at equal indices. P exchanges L to H by $-\rho$ and H to L by $+\rho$. Membership in those rows is precisely the image bound and actual crossing test.

## 2. Forced transpositions and unique upper chains

Fix a successful baseline allocation on either exterior, with numerical first quotas $(h+1,h+1)$ (low) or $(h+2,h)$ (companion). Since $y=0$, every first gap terminal uses an L source. There are $F_0-1=\gamma+1$ such terminals. For an upper-parent arrow to have numeric image $\pi=s+b-i\le s-1$, necessarily $i\ge b+1\ge\gamma$. Also $\pi\ge b+1\ge\gamma$ because $i\le s-1$. Thus every source and image in $[0,\gamma-1]$ must use the first shifts. The interval is present in L by $k\ge\gamma+1$.

Induct on the even indices $j=0,2,\ldots,\gamma-2$. At the start of step $j$ every earlier source and image is already exhausted in pairs. Source $j$ can only go to $j+1$: its other possible image $j-1$ is occupied or outside the alphabet. Image $j$ can only come from source $j+1$: $j-1$ is already used or absent, and upper hosts cannot supply it. This forces both arrows on each adjacent transposition, preserving the actual positive and negative parents. After the initial $\gamma$ arrows exactly one first gap terminal remains. The actual first quota accounting (one terminal selected at the positive host) makes it a negative defect in low, a positive defect in companion. Its source must be in $[\gamma,k-1]$ and its image outside the exhausted initial interval. The exact bounds are therefore
$$
\begin{array}{ll}
\text{low:}&\gamma+1\le d\le k-1,\quad e=d-1,\\
\text{companion:}&\gamma\le d\le k-1,\quad e=d+1 .
\end{array}
$$
Every listed $e$ fits in the L-image alphabet. This argument uses both source and image exhaustion, independent of the original D192 defect lists.

The upper L to H matching has source set $[\gamma,k-1]\setminus\{d\}$ and image set $[\gamma,k-2]$, with displacements zero at Q or $-\rho$ at P. The upper H to L matching has source set $[\gamma,k+\gamma-1]$ and image set $[\gamma,k+\gamma]\setminus\{e\}$, with displacements zero or $+\rho$. Counts on each residue modulo $\rho$ give necessary conditions $d\equiv k-1$ and $e\equiv k+\gamma$. For $\rho=1$ these are automatic. For $\rho=2$, since $\gamma$ is even and $e=d\pm1$, the two conditions are equivalent.

These conditions suffice and determine each upper matching uniquely at the fixed defect. For L to H, on the affected residue the source omits $d$ and the image omits the top cell $k-1$. If $d=k-1$ the sets coincide. Otherwise image $d$ must receive source $d+\rho$, then image $d+\rho$ must receive $d+2\rho$, and so on through source $k-1$. In either case the P sources are exactly $d+\rho,d+2\rho,\ldots,k-1$. Their shifted images supply exactly the needed differing cells and all intermediate cells along that chain. After removing the chain, source and image sets coincide. On the other residue, if present, they coincide from the start. All remaining arrows must be Q, since equal sums of indices and the nonpositive allowed displacements forbid a remaining strictly negative move. For H to L, on the affected residue source $e$ cannot have its image at $e$, so it must use $e+\rho$ and recursively force each succeeding source up one step, through the last source $k+\gamma-\rho$. The P sources are $e,e+\rho,\ldots,k+\gamma-\rho$. Their images fill exactly the shifted cells, and the complementary source and image sets coincide on both residues. The nonnegative displacements force the rest to be Q. This proves the partitions and uniqueness for both matching directions, including the empty L chain and empty H-image row at $d=k-1=\gamma$. On the actual graph only interchangeable sibling terminal names can still be assigned to these fixed position arrows.

## 3. Exact baseline support and the general parity obstruction

For $\rho=1$ the unique lists in §2 are exactly the [D192 lists](ORDINARY_SPINE_STRICT_SIGNED_INDEPENDENT_GROWTH.md#2-two-exact-movable-defect-baselines). The low arm has Q from L $[\gamma,d-1]$, Q from H $[\gamma,d-2]$, P from L $[d+1,k-1]$, and P from H $[d-1,k+\gamma-1]$. The companion changes the last two H lists to Q $[\gamma,d]$, P $[d+1,k+\gamma-1]$. Including the exterior terminal at Q, low gives $p=2(d-\gamma),q=2k+\gamma-2d$ and companion gives $p=2(d-\gamma+1),q=2k+\gamma-2-2d$. The exact bounds on $d$ give even $p\ge2$ and even $q\ge2h+2$ for low or $q\ge2h$ for companion. The inverses are $d=\gamma+p/2$ and $d=\gamma-1+p/2$. The forced transpositions and unique upper chains make these the complete baseline domains on this fixed exterior and selected-role topology.

Independently of the baseline, the folded moment is the total image indices minus total source indices. L adds $A$ indices starting at $k$, and H loses $A$ indices starting at $J-K+1$. Thus
$$
M=A(k-J+K-1)=A(B-\gamma)=A .
$$
This holds across every fully compatible size on the two fixed exteriors. Each actual first gap arrow has odd folded displacement, whether its sign is positive or negative and in either row. There are $F-1$ of them. Q contributes zero. At $\rho=1$ every P arrow has odd displacement and no P terminal was selected exterior. Hence $A\equiv F-1+q\pmod2$. Since $A$ is odd and the two graph classes force even $F,R$, every successful allocation has even $q$ and even $p$. This parity obstruction holds beyond the baseline counts on the fixed separation-one exterior. At $\rho=2$ the P displacements are even, so the equation is simply $A\equiv F-1$ and imposes no additional parity on $q$. The statements concern these exact exteriors.

For $\rho=2$ write $d=k-1-2t$ with $t\ge0$. The unique chains of §2 give respectively $(k-1-d)/2=t$ P uses from L and $(k+\gamma-e)/2$ P uses from H. Thus $q=h+1+2t$ in low and $q=h+2t$ in companion. The lower bound on $d$ is $k\ge\gamma+2+2t$ in low or $k\ge\gamma+1+2t$ in companion. In both cases this is $R/2\ge q+1$, or $p\ge q+2$. Therefore the exact baseline domains on the fixed separation-two exterior are:

- Low has $q\ge h+1$, $q\equiv h+1\pmod2$, $p\ge q+2$ and even $p+q$.
- Companion has $q\ge h$, $q\equiv h\pmod2$, $p\ge q+2$ and even $p+q$.

For either domain set $t=(q-q_{\min})/2$ and $d=k-1-2t$. The conditions enforce every stated bound, and produce exactly $q$ P arrows. The remaining upper gap arrows plus the selected Q terminal give $p$ since their full total is $R$. This proves both directions, including the minimum $d$, the last admissible $d$ and the empty H-image boundary. No choice of exterior or selected terminal roles beyond the two fixed layouts is classified.

The transpositions contribute zero folded moment, the low defect contributes $-1$ and the companion defect $+1$. For $\rho=1$ the H minus L P counts are $\gamma+2,\gamma$, respectively; for $\rho=2$ they are $h+1,h$. In each case multiplying the P count difference by $\rho$ and adding the defect gives $A$. The exact crossing counts by the row partitions are $x=k-\gamma-1=R/2-h-1$ and $y=0$ at baseline, since the only crossing arrows are the $k-\gamma-1$ L sources assigned to the upper hosts. These checks agree independently with the geometry.

## 4. Exact common Q anchors

A complete Q pair at index $i$ consists of both $L_i\to H_i$ and $H_i\to L_i$ at that actual upper parent. For $\rho=1$ the lists above give the full common interval starting at $\gamma$, of length $p/2-1$. It is $[\gamma,d-2]$ in low and $[\gamma,d-1]$ in companion.

For $\rho=2$ the Q L sources are $[\gamma,d-1]$ and the opposite-$d$ residue indices above $d$ within the L sources. The Q H sources are $[\gamma,e-1]$ and the opposite-$e$ residue indices above $e$ within the H sources. Because $e=d\pm1$, the two latter residue classes are disjoint. In low the intermediate index $d-1=e$ is a P H source; in companion index $d$ is the defect and index $d+1=e$ is a P H source. So the whole common Q interval is $[\gamma,d-2]$ in low or $[\gamma,d-1]$ in companion, with no additional complete Q pair outside it. Its length is $d-\gamma-1$ in low or $d-\gamma$ in companion. Substituting $d=k-1-2t$ and the corresponding $q$ gives $(p-q-2)/2$ in both arms. Thus zero pairs occur at $p=q+2$ and one or two initial pairs are supplied at $p\ge q+4$ and $p\ge q+6$, respectively. These anchor counts describe the exact baseline, while their use below supplies sufficient growth.

## 5. Balanced growth and one-anchor independent growth

Let the desired first-quota increases be $2\lambda_+$ and $2\lambda_-$ with $\lambda_\pm\ge0$, and put $b=\min(\lambda_+,\lambda_-)$, $\eta=|\lambda_+-\lambda_-|$, and $\lambda=2b+\eta$. Equivalently the first total is $F=F_0+2\lambda$. The unchanged original second total and exterior give $K=K_0+\lambda$, $s=s_0+2\lambda$, $k=k_0+\lambda$, $J=J_0+2\lambda$. Thus every folded right endpoint extends by $\lambda$ and every folded left endpoint remains fixed. The old label side inequalities persist and $s-K=(s_0-K_0)+\lambda$ with full target admission.

Keep the first $\gamma$ signed transpositions fixed, including all their actual names. Every other folded endpoint is at least $\gamma$. Translate each of those endpoints by $\lambda$ within its row at the same physical parent. Every map remains valid by the displacements and row alphabets in §1. Exactly $[\gamma,\gamma+\lambda-1]$ is vacant in every row. When the old H-image row was empty its right endpoint was $\gamma-1$, so its new row consists of that strip.

### Balanced packets with no Q pair

If $\eta=0$, split the vacant strip into $b$ adjacent pairs of columns $[i,i+1]$ starting at indices $\gamma,\gamma+2,\ldots,\gamma+2b-2$. At the actual positive first host use $L_i\to L_{i+1}$ and $H_{i+1}\to H_i$. At the actual negative first host use $L_{i+1}\to L_i$ and $H_i\to H_{i+1}$. Both rows biject by their adjacent transpositions on each pair. Thus each pair adds exactly two actual terminals at each sign, and each existing upper terminal is translated at its own parent. The proof applies with $b=0$ (identity) and at an initially empty H-image row.

### Balanced packets followed by the one-sign block

If $\eta>0$ use one original complete Q exchange pair at $\gamma$. After the translation, remove both translated arrows of that pair, retaining their two actual names and row directions. It vacates the single additional column $\gamma+\lambda$ in all four rows. No other translated endpoint is in the resulting free interval $[\gamma,\gamma+\lambda]$. Use the first $2b$ columns in balanced packets as just proved. The last $\eta+1$ columns form a block $[l,r]=[\gamma+2b,\gamma+\lambda]$. Use the following exact [D192 single-pair block](ORDINARY_SPINE_STRICT_SIGNED_INDEPENDENT_GROWTH.md#3-one-or-two-named-q-anchors-and-independent-first-quota-growth) for the sign with larger prescribed increase.

- If positive is larger, use $L_i\to L_{i+1}$ and $H_{i+1}\to H_i$ for $l\le i<r$ at the original positive host. L sources $[l,r-1]$ and images $[l+1,r]$ leave cell $r$ and cell $l$ free, respectively. H sources $[l+1,r]$ and images $[l,r-1]$ leave cell $l$ and cell $r$ free. Restore the original named Q arrows as $H_l\to L_l$ and $L_r\to H_r$.
- If negative is larger, use $L_{i+1}\to L_i$ and $H_i\to H_{i+1}$ for $l\le i<r$ at the original negative host. L sources $[l+1,r]$ and images $[l,r-1]$ leave cell $l$ and cell $r$ free, respectively. H sources $[l,r-1]$ and images $[l+1,r]$ leave cell $r$ and cell $l$ free. Restore the original named Q arrows as $L_l\to H_l$ and $H_r\to L_r$.

Each restored name retains its original Q parent and source row direction, and both remaining endpoints belong to the actual block. The balanced and final blocks are disjoint and exhaust the four exact vacant sets. They add $2b$ first terminals at each sign and $2\eta$ further at the larger sign, giving the desired $2\lambda_+,2\lambda_-$. The entire second quota vector is unchanged, including supplied odd quotas. Every P name and every unselected Q name simply translates. The selected exterior terminals retain their exterior roles.

The new first arrows have total signed folded moment zero: each same-sign pair uses opposite folded displacement. Translation and the restored Q pair leave all original displacements unchanged. Thus the total remains $A$. The crossing count $x$ is unchanged, since the removed Q pair, when present, is restored with the same directions and P only translates. Each of the added $\lambda$ pairs of first arrows uses one H image, so $y=\lambda$ and $x=R/2-h-1$. These agree with the fresh graph colors and $x+y=s-K$.

This proves balanced even growth on every supplied baseline, and arbitrary independent even growth at $\rho=1$ for $p\ge4$ or at $\rho=2$ for $p\ge q+4$. The final actual first quotas are $(h+1+2\lambda_+,h+1+2\lambda_-)$ in low and $(h+2+2\lambda_+,h+2\lambda_-)$ in companion. At either separation the fresh size is $6h+2+p+q+2(\lambda_++\lambda_-)$. The theorem retains the actual topology, roles, both selected incidences, and full independent-prefix admission. D192's previously proved one- and two-pair constructions remain valid within their original scopes. The new theorem requires at most one pair under the stated hypotheses. Unequal growth outside those hypotheses remains open.

## 6. Exact named realization and first resources

Choose actual indexed roles from the specified quotas, retaining the two first centers and both second centers even when their quotas agree. With only physical inventories given, try the finite sign/Q/P assignments, the two $\rho$ choices and the two arm formulas. Check the baseline conditions, whether the first increases are even and nonnegative, the required anchor if unequal, and full admission. Use original branch index order to break ties. Then extract $d$ from §3 and place the actual children and selected terminals as in §1. All subsequent lists are finite explicit arithmetic.

At each actual first parent reserve its original baseline residual terminal names in increasing numeric index order, excluding the actual selected exterior terminal at the positive parent. Assign the reserved names in increasing unfolded baseline source order. Assign original Q and P names in increasing unfolded source order at baseline, excluding only the indexed exterior Q terminal. This defines the two physical Q anchor names before any transport. Translate all noninitial retained arrows and reassign the anchor names at the endpoints in §5 when used. Assign the unused actual first terminal indices at each parent in increasing unfolded source order in its new packets. Exact counts give a full bijection of original terminals at every host. The baseline calculation operates on the actual final target, including its retained exterior names and available residual terminal names.

Let $J=J_0+2\lambda$ be final. For a fully translated H endpoint at baseline folded index $i$, the new numeric coordinate is $J-(i+\lambda)=J_0-i+\lambda$. Translated L endpoints also gain $\lambda$ numerically. Fixed initial L arrows keep their old numerical endpoints. The restored Q anchors use the final unfolding on their prescribed endpoints.

For exact first numeric sources $S_+,S_-$ start with $\{0,2,\ldots,\gamma-2\}$ and $\{1,3,\ldots,\gamma-1\}$, respectively. Add the translated defect $d+\lambda$ to its actual sign. For the balanced packets put $T=\{\gamma+2j:0\le j<b\}$. Add $T\sqcup(J-(T+1))$ to $S_+$ and $(T+1)\sqcup(J-T)$ to $S_-$. Here translation and subtraction of sets are elementwise. These are precisely the L and H packet sources under the final unfolding. For an active excess block $[l,r]$ of positive sign add $[l,r-1]\sqcup[J-r,J-l-1]$ to $S_+$. If its sign is negative add $[l+1,r]\sqcup[J-r+1,J-l]$ to $S_-$. The unions are disjoint by the four-row partitions and their disjoint numeric complements. In numeric strict coordinates the first image map adds 1 or subtracts 1 at the two respective hosts, so the exact resource sets are
$$
I=S_+\sqcup S_-,\qquad J_1=(S_++1)\sqcup(S_--1).
$$
Their exact remaining sets $I',J_2$ are their respective complements in $[0,s-1]$. These sets are taken directly from the actual arrows and unfolding.

## 7. Both full palettes, intermediate inventories, and polarities

In minimum orientation shift the old labels by $A$ below $c$ and $A+s$ at or above $c$. They retain their sides at $C=c+K$ by $A\le K\le A+s$. The old actual crossing differences gain $s$ and other old differences are fixed. Give gap source $i$ its placed label $A+c+i$. Keep the lower reduced labels and add $n+s$ to the upper reduced values. The exterior agrees at $v=A$ with the old placement and each actual exterior incidence crosses the cut, since its lower value is at most $A<C$ and its upper value at least $n+s+A+1>C$. The old and fresh palettes are
$$
\begin{array}{ll}
L_{\rm old}=[A,A+c-1]\sqcup[A+c+s,n+s+A],&
L_{\rm fresh}=[0,A-1]\sqcup[A+c,A+c+s-1]\sqcup[n+s+A+1,m],\\
D_{\rm old}=[1,d_0-1]\sqcup[d_0+s,n+s],&
D_{\rm fresh}=[d_0,d_0+s-1]\sqcup[n+s+1,m].
\end{array}
$$
Because $m=n+s+A+B$, these give disjoint partitions of $[0,m]$ and $[1,m]$. The reduced, unfolded gap and old bijections fill these intervals once at the actual named vertices and physical edges. The gap noncrossing and crossing sets are $d_0+[0,K-1]$ and $d_0+[K,s-1]$. With the old and exterior difference bands the actual output crossing spectrum is $[d_0+K,m]$ and its noncrossing counterpart is $[1,d_0+K-1]$. The continued original witnessing spine has actual extreme frontier $w=0$, distance at most two to every added vertex, and $m=2C+2$. This gives the exact $S_0$ return.

At the first-section boundary the exact newly used and remaining exterior label sets are
$$
E_1=[2,A-1]\sqcup\{n+s+A+1,n+s+A+j_+\},\qquad
E_2=\{0,1\}\sqcup\{n+s+A+b:2\le b\le B,\ b\ne j_+\}.
$$
The first set comprises the original first children, $u$ and the selected first terminal. The second comprises $w$, the selected Q terminal, and all actual second children, with P in the last upper slot at $\rho=2$. By the explicit edges of §1, their exterior difference bands are $D^e_1=n+s+[1,A]$ and $D^e_2=n+s+[A+1,A+B]$. The shared $v$ is counted once in the old resource set. The two complete intermediate inventories are
$$
\begin{array}{ll}
\mathrm{used\ labels}&L_{\rm old}\sqcup E_1\sqcup(A+c+I),\\
\mathrm{remaining\ labels}&E_2\sqcup(A+c+I'),\\
\mathrm{used\ differences}&D_{\rm old}\sqcup D^e_1\sqcup(d_0+J_1),\\
\mathrm{remaining\ differences}&D^e_2\sqcup(d_0+J_2).
\end{array}
$$
Split the two gap label inventories at $k$ and the gap difference inventories at $K$ before adding their offsets. Old labels split into their indicated low and high bands; exterior values retain the reduced sides. Both exterior difference bands cross, and the old difference bands are noncrossing and crossing in their order above. The literal unfinished edge $uw$ has endpoints $(n+s+A+1,0)$ and its absolute difference belongs to the remaining exterior band.

For actual maximum polarity orient the input by complementation at $n$ and complement the output at $m$. Its actual cuts are $n+1-c$ and $m+1-C$. Because $2K=A+B+s$, the actual old shifts below and at or above the input maximum cut are $B$ and $B+s$. The two label inventories complement and exchange sides, preserving all actual crossing and difference inventory partitions. The literal connector becomes $(B-1,m)$ with the same difference and actual frontier $w=m$.

## 8. Symbolic original-target controls

Use the independently supplied D191 maximum-polarity $S_0$ prefix on 94 edges, actual cut 49, actual frontier $s{:}29=94$, crossing differences $[48,94]$ and noncrossing differences $[1,47]$. Orient it with $c=46,d_0=48$. In each positive control assign sign roles and Q/P roles according to the listed positive branch order. Every zero is an original direct leaf. The numeric checks below use the explicit lists and original parent roles.

| Control | Actual first and second profiles | Arm and $\rho$ | $h,R,k_0,d,e$ | $2K$ | $m$, maximum cut |
|---|---|---|---|---|---|
| A low | $(3,3,0),(2,6,0)$ | low, 1 | $2,8,6,5,4$ | 22 | $116,60$ |
| A companion | $(4,2,0),(2,6,0)$ | companion, 1 | $2,8,6,4,5$ | 22 | $116,60$ |
| B | $(3,3,0),(5,3,0)$ | low, 2 | $2,8,6,5,4$ | 22 | $116,60$ |
| C | $(5,3,0,0,0),(5,3,0,0,0)$ | companion, 2 | $3,8,7,6,7$ | 28 | $122,63$ |
| D | $(4,4,0,0,0),(6,4,0,0,0)$ | low, 2 | $3,10,8,7,6$ | 30 | $124,64$ |
| E even | $(5,5,0),(2,6,0)$ | low, 1 | $2,8,6,5,4$ | 26 | $120,62$ |
| E odd | $(5,5,0),(5,3,0)$ | low, 2 | $2,8,6,5,4$ | 26 | $120,62$ |
| F | $(5,7,0),(4,6,0)$ | low, 1 | $2,10,7,6,5$ | 30 | $124,64$ |
| G | $(5,7,0),(7,3,0)$ | low, 2 | $2,10,7,6,5$ | 30 | $124,64$ |

Each full fresh size is admitted. The exact maximum-oriented return has crossing and noncrossing differences $[48+K,m]$ and $[1,47+K]$, and maximum connector $(B-1,m)$ by §7. In particular:

- **A.** The forced transpositions, defect and unique $\rho=1$ chains give the exact original D192/D191 lists for both arms at $h=2$. The complete previous one- and two-anchor domains remain accepted and the baseline characterization is now exact on that exterior.
- **B.** With $\gamma=4$, P has no L uses and uses H indices $4,6,8$ with images $6,8,10$ in L. Q uses $L_4\to H_4$ and H indices $5,7,9$ to their equal L images. Its exterior-selected terminal gives total five. The initial L images $0,\ldots,3$ and defect image 4 complete the actual alphabets. The strict return is at 116 edges, cut 60, crossing $[59,116]$, noncrossing $[1,58]$, and connector $(4,116)$. The general $\rho=1$ moment forbids this odd second split on that alternative fixed exterior.
- **C.** With $\gamma=6$ and $k=7$, $s=K=14$. The H-image interval $[6,5]$ is empty; all L sources go to first hosts and the defect is $6\to7$. P uses H $7,9,11$ to L $9,11,13$, while Q uses H $6,8,10,12$ to the same L indices and its selected terminal. The first L images $[0,5]\sqcup\{7\}$ plus those two sets give L $[0,13]$. This attains the companion minimum P quota at $h=3$.
- **D.** P uses H $6,8,10,12$ to L $8,10,12,14$, with no L uses. Q uses L index 6 to H index 6 and H $7,9,11,13$ by identity, and has its selected terminal. The defect $7\to6$ plus the initial transpositions complete L. This is below the D192 low minimum $q=8$ on the numerical P role at $h=3$.
- **E.** Both low baselines have no complete Q anchor. In the even case this follows from $p/2-1=0$; for the odd case it follows from $(p-q-2)/2=0$. Width $\lambda=2$ gives the single balanced packet on $[4,5]$ and translates all upper arrows at their own original names. It adds two first terminals per signed host, keeping $(2,6)$ and $(5,3)$ respectively, with 26 fresh edges in each case.
- **F.** In the low $\rho=1$ baseline Q uses L indices 4 and 5 and H index 4. Its only complete pair is at 4. At $J_0=17$, the Q gap terminal indices in increasing unfolded source order are 1 at L index 4, 2 at L index 5 and 3 at H index 4; its selected index is 0. For $\lambda_+=1,\lambda_-=2$, the free interval $[4,7]$ is filled by the balanced packet on $[4,5]$ and excess negative block on $[6,7]$. Restore Q name 1 at $L_6\to H_6$ and name 3 at $H_7\to L_7$. Name 2 translates to $L_8\to H_8$. The two packets add two positive and four negative terminals, preserving all six P uses and four Q terminals, with 30 fresh edges.
- **G.** On the $\rho=2$ low baseline with $(p,q)=(7,3)$, P uses H $5,7,9$ and Q uses L $4,5$ and H $4,6,8,10$. Only 4 is a complete pair. With $J_0=17$, increasing numeric source order gives Q anchor indices 1 for L and 6 for H after its selected terminal at index 0. The same growth blocks as F restore indices 1 and 6 at $L_6\to H_6$ and $H_7\to L_7$, respectively. All other Q and P names translate. The final odd quotas stay $(7,3)$ and the full size contribution is 30.

For the $h=2$ low equal odd splits $(3,3)$ and $(5,5)$ neither orientation satisfies $p\ge q+2$ on the separation-two exterior. The exact baseline characterization excludes both. The general moment also excludes those odd splits on the fixed separation-one exterior. These are fixed-exterior conclusions. They leave other strict exteriors and other allocations outside the prescribed baseline topology open.

## 9. Exact read-only D191 projection

Intersect the proved baseline domains at $h=2$ with the D191 stratum II strict originals. Both numerical assignments of the two actual second centers are allowed, independently of their original order. At total $R$ the separation-one baselines give the accepted D192 low counts $0,2,4,5,6,7$ and companion counts $2,3,4,5,6,7$ for $R=6,8,10,12,14,16$. These follow by writing the physical quotas $(2i,2j)$ with $i,j\ge1$, and requiring the larger quota at least six or at least four, respectively.

For separation two the low numerical P quota is odd and at least three, and Q is odd and at least P plus two. Allowing both actual orders therefore adds exactly the ordered unequal odd splits with both quotas at least three. At even total $R$ the first odd quota ranges over $3,5,\ldots,R-3$, a list of $R/2-2$ values. Remove the equal split when $R/2$ is odd, since it otherwise violates the strict two-unit separation between the quotas. The counts are $0,2,2,4,4,6$, totaling 18 disjoint additions to the low arm. For the separation-two companion the numerical P quota is even and at least two and numerical Q is even and at least four. The same original has a separation-one companion realization by assigning a quota of at least four to P, so every such original already lies in the D192 companion projection.

The union is consequently **42 low originals, 27 companions and 24 matched pairs**. The newly supplied odd low originals have companions unclassified by these domains. The record evidence retains all 69 strict graph and record identities, their actual indexed numerical roles including each eligible exterior choice, and the distinct 42 exceptional-context low originals bound to the accepted D191 guard. It verifies exact agreement with D192's frozen projection on the separation-one records and preserves all 584 originals and their prefix identities. These are symbolic baseline supplies and the limited earlier guard dispositions.

## 10. Composition, remaining obligations and scope

Each constructed return is an exact independently usable $S_0$ state on its actual named graph, with either physical polarity and full admission for the next block. It can feed an admitted D191 or D192 block, or an admitted D157 $S_0$-to-$S_{-1}$ leg; a D157 return leg can reestablish $S_0$ before another strict supplier. For example, from the retained 74-edge maximum $S_{-1}$ input use the accepted D157 return to 94, D193 control B to 116, the low arm of D192 control A to 138, the D191 $R=8$ quota-one block to 158, and D157's two compatible phase-changing legs with $(r,t,p)=(2,1,1)$ to 178 and 198. Full admission holds at every step. The maximum cuts are $39,49,60,71,81,91,101$ and the phase sequence is $S_{-1},S_0,S_0,S_0,S_0,S_{-1},S_0$. The final crossing spectrum is $[100,198]$, obtained from the correct final strict threshold.

In any finite such sequence in fixed physical polarity, every old-label map preserves membership at its evolving cut. Let $U_i,V_i$ be the sums of all subsequent actual lower shifts and gaps after the earlier completed cut $C_i$. The immutable final label of local value $x$ is $x+U_i+V_i\mathbf1_{x\ge C_i}$ by induction over those maps. Each earlier crossing edge gains $V_i$ and each earlier noncrossing difference remains fixed. Both local inventories and the literal connector transport by those formulas; their remaining complements also include the disjoint later fresh palettes. The calculation is finite, uses the original indexed names, and preserves exact alphabet realization through phase changes.

The exact baseline theorem and the anchor economy concern the two specified strict exteriors. Unequal growth without the supplied pair, other strict topologies and fixed exterior choices, independent initialization beyond the retained seed hypotheses, and arbitrary decomposition into compatible phase blocks remain open. The results separate the interval and parity constraints on a block from the incidence and phase constraints on composing such blocks. The accepted D191 existential question remains **SYMBOLICALLY_RESOLVED / NO_EXECUTION_NEEDED**. Numerical search, allocation states, original-checker calls, campaigns and replays were zero.
