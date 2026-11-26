# D194 — Bidirectional strict–exceptional phase toggle

Task **LCL-ORDINARY-SPINE-BIDIRECTIONAL-PHASE-TOGGLE-SUPPLIER-001**.

**PROVED WITHIN EXACT WRITTEN SCOPE / PENDING DIRECTOR REVIEW.** The phase-aware signed supplier and the reverse neutral supplier give the stated common families on identical original profiles. They choose their actual numerical exterior from the incoming phase. The widths agree on the common profiles, while the original first roles and some second slots differ. The crossing spectrum endpoints proposed in controls E and H require the corrections in §9. D157, D190, D192 and D193 remain separately accepted suppliers.

All labels and structural parameters are exact integers, excluding booleans. Intervals are inclusive; reversed intervals are empty. Use $d_0=c+2$ for the input strict threshold reference, and $d,e$ for defect source and image. Write $p,q$ for the full numerical Q and P quotas, distinct from their actual branch order.

## 1. Phase-aware inventory, placement and crossing tests

Use an independently supplied [D157 input](ORDINARY_SPINE_ALTERNATING_EXCEPTIONAL_SPECTRUM.md) on $n=2c+2$ edges. Its actual witnessing spine ends at extreme $v$, oriented to zero in the minimum form; equality at $c$ is upper. An incoming phase $\varepsilon\in\{0,-1\}$ has actual crossing differences $[d_0+\varepsilon,n]$ and noncrossing differences $[1,d_0+\varepsilon-1]$. Extend by the actual spine vertices $u,w$, with $2K$ fresh edges and $n\ge2K$, $m=n+2K$. Set the output cut $C=c+K$, target phase $\varepsilon'$, $\delta=\varepsilon'-\varepsilon$, and normalized image threshold $T=K+\delta$.

For a supplied connected crossing exterior of widths $A,B$, let $s=2K-A-B$ count the true terminal gap leaves. The placements require $A\le K\le A+s$ and $s\ge T$. The first inequalities put $A+c-1<C$ and $A+c+s\ge C$, preserving the input sides. The second places the smallest shifted old crossing weight $d_0+\varepsilon+s$ at or above the new threshold. At numeric source $i$ the new label is $A+c+i$, physically lower iff $i<k=K-A$. Edge subtraction at actual reduced lower parent $j$ or upper parent $A+b$ gives weight $d_0+\varepsilon+\pi(i)$ with
$$
\pi(i)=i+A-2-\varepsilon-j \quad\text{or}\quad
\pi(i)=s+b-\varepsilon-i,
$$
respectively. Upper reduced labels acquire $n+s$, which together with $n-c=d_0$ gives the second formula. D157's physical criterion is that $\pi(i)\ge T$ exactly when source and parent straddle the cut. Thus numeric H source and H image intervals are $[k,s-1]$ and $[T,s-1]$, with L complements in $[0,s-1]$.

Root graph colors at lower $v$. For actual first and second child counts $a,a_2$ and terminal totals $F,R$, the fresh graph-class counts are $1+a+R$ and $1+a_2+F$. They are $A+s-k-y+x$ and $B+k-x+y$, respectively, where $x$ counts lower gap sources at upper parents and $y$ upper gap sources at lower parents. The exact image crossover count is $s-T=x+y$. Substitution gives
$$
N_{\rm low}=2(A+x)+\delta,\qquad N_{\rm high}=2(B+y)+\delta .
$$
These equalities retain the chosen changed phase even when the crossing gap is empty. All supplied placements are checked below before the full palettes are assembled.

For any fold $J=s+b_0-\varepsilon$, set $\gamma_*=b_0-\varepsilon+1$, the first H column. The rows are $[0,k-1]$ and $[\gamma_*,J-k]$ for sources and $[0,T-1]$ and $[\gamma_*,J-T]$ for images. L uses its numeric index; H uses $J$ minus that index. A lower numeric translation by $\eta$ has folded shifts $\eta,-\eta$ in the respective rows, and a second upper index $b=b_0+\rho$ exchanges L to H by $-\rho$ and H to L by $+\rho$. This follows by applying the fold to the actual maps. Every listed legal arrow crosses exactly when its destination is H. The geometric signed moment, summed image indices minus summed source indices, adds $T-k=A+\delta$ L indices beginning at $k$ and removes that many H indices beginning at $J-T+1$. It is therefore
$$
M=(A+\delta)(k-J+T-1)=(A+\delta)(B+\delta-\gamma_*).
$$
This interval identity is independent of the allocations.

## 2. Signed strict-input exterior and row geometry

Take $\varepsilon=0$ and $\delta\in\{0,-1\}$ with $\varepsilon'=\delta$. For $h\ge2$ write $\gamma=2h$, $a=\gamma-1$, $a_2=\gamma-1-\delta$, $A=\gamma+1$, $B=\gamma+1-\delta$. Both sections have two actual positive centers and, respectively, $\gamma-3$ and $\gamma-3-\delta$ actual direct leaves. Give $v,u,w$ reduced labels $A,A+1,0$. The positive and negative first centers occupy $j_+=A-3=\gamma-2$ and $j_-=A-1=\gamma$. The remaining original first children occupy the remaining slots of $[2,A-1]$. One actual first terminal at the positive center takes reduced $A+j_+$. The actual Q at $w$ occupies $b_0=\gamma-1$ and P occupies upper index $b_0+\rho$ with $1\le\rho\le2-\delta$. Put one actual Q terminal at 1. The second child slots are $[2,B]\setminus\{j_+\}$ in upper-index coordinates; fill those remaining after Q and P with the original second direct leaves. This is exactly $B-2=a_2$ slots. All specified values of $\rho$ give actual allowable slots, including P at $B$ for the largest separation.

The reduced low labels are $[0,A]$ and the upper labels $[A+1,A+B]$, each used once. Incidences connect via the actual spine, child and two selected terminal edges, all crossing. The first edge $vu$ uses difference 1, the first children use $[2,A-1]$, and the selected first terminal uses $A$. The connector $uw$ uses $A+1$, the second children use $A+([2,B]\setminus\{j_+\})$, and the selected Q terminal takes the missing $A+b_0-1=A+j_+$. This is the exact reduced edge bijection and all original leaf parents are unchanged. The lower shifts in §1 are $+1,-1$, $\gamma_*=\gamma$, and upper P has separation $\rho$.

At baseline the numerical sign quotas are $(h+1,h+1)$ in low and $(h+2,h)$ in companion. The first total is $F_0=\gamma+2$. There are $4h-\delta$ child and spine edges, giving
$$
2K_0=6h+2-\delta+R,\quad
k_0=h+(R-\delta)/2,\quad s_0=\gamma+R=2k_0+\delta,\quad J_0=s_0+\gamma-1 .
$$
The fresh graph counts are $\gamma+R$ and $\gamma-\delta+F$ at general first total $F$. The parity identities force $R\equiv\delta\pmod2$ and $F$ even. At baseline they give $x=k_0-\gamma-1$, $y=0$. For $k=k_0$ the four exact folded rows are
$$
L_{\rm src}=[0,k-1],\quad H_{\rm src}=[\gamma,k+\gamma+\delta-1],\quad
L_{\rm im}=[0,k+\gamma+\delta],\quad H_{\rm im}=[\gamma,k-2].
$$
Indeed $T_0=k+\gamma+1+\delta$ and $J_0-T_0=k-2$. Their H rows unfold to the intervals in §1, with the stated L complements and the same actual crossing tests. Success requires $x\ge0$, i.e. $k\ge\gamma+1$. This implies $K_0\ge B,A$ and $s_0\ge T_0$, and at $k=\gamma+1$ the H-image row is empty. In the outbound case this equality gives $s_0=K_0-1$. All positive domains below prove $k\ge\gamma+1$ and require independent full size admission.

## 3. Exact baseline classification on the signed layouts

At baseline $y=0$, so all $\gamma+1$ first gap terminals use L sources. An upper arrow has both numeric source and image at least $b+1\ge\gamma$, since its numeric map is $s+b-i$ on $[0,s-1]$. Thus the first $\gamma$ sources and images must use the lower shifts. For each successive even $i\in[0,\gamma-2]$, source $i$ must go to $i+1$ because its other candidate image $i-1$ is absent or occupied. Image $i$ must come from $i+1$ because the earlier candidate source $i-1$ is absent or used. This forces all adjacent transpositions. They use $h$ actual gap leaves per first host. The remaining one belongs to the negative host in low and the positive host in companion, after excluding the actual selected positive terminal. Write $\sigma=-1$ in low and $+1$ in companion. The sole defect $L_d\to L_e$ has $e=d+\sigma$, with $\gamma+(1-\sigma)/2\le d\le k-1$ by the exhausted initial interval. This is exactly the two stated defect bounds.

Upper L-to-H matching has sources $[\gamma,k-1]\setminus\{d\}$ and images $[\gamma,k-2]$. Upper H-to-L has sources $[\gamma,k+\gamma+\delta-1]$ and images $[\gamma,k+\gamma+\delta]\setminus\{e\}$. For either direction, counts on residues modulo $\rho$ require that the respective deleted slots have the same residue. This gives
$$
d\equiv k-1,\qquad e\equiv k+\gamma+\delta\pmod\rho,
\qquad \rho\mid(\gamma+\delta+1-\sigma).
$$
Conversely, with those residues, image $d$ requires source $d+\rho$ in the first matching if $d<k-1$. Then each subsequent image along that residue requires the next source until $k-1$. If $d=k-1$ that chain is empty. The forced P sources are exactly $d+\rho,d+2\rho,\ldots,k-1$, and their images under $-\rho$ make the residual source and image sets identical in every residue. For the second matching source $e$ must use image $e+\rho$, then the succeeding source on the same residue must use the next image, through the last P source $k+\gamma+\delta-\rho$. Their images under $+\rho$ reach the upper endpoint $k+\gamma+\delta$ and leave identical residual sets. All remaining moves are Q, since equality of the respective index sums and the one-signed allowed shifts force zero shifts. This proves uniqueness of the upper position matchings, their exact source/image partitions, and legal completion by actual parent. The second chain is nonempty here since $\gamma+\delta+1-\sigma>0$; the first may be empty. If the H-image row is empty, all L sources are consumed by first arrows, the first chain is empty and no Q L arrow remains. The proof includes that case.

Put $d=k-1-\rho t$, $t\ge0$. The P counts in the two rows are $t,(k+\gamma+\delta-e)/\rho$. With
$$
q_{\min}=(\gamma+\delta+1-\sigma)/\rho ,
$$
the full P quota is $q=q_{\min}+2t$. The bound on $d$ becomes $R\ge\gamma+\delta+3-\sigma+2\rho t=\rho q+2$, or $p\ge(\rho-1)q+2$. The exact baseline support for each fixed choice of $\delta,\rho,\sigma$ with $\rho\mid\gamma+\delta+1-\sigma$ is therefore
$$
q\ge q_{\min},\quad q\equiv q_{\min}\pmod2,\quad
p\ge(\rho-1)q+2,\quad p+q\equiv\delta\pmod2.
$$
Conversely these conditions give the integer $t=(q-q_{\min})/2$ and the indicated $d,e$ inside their intervals. The two chains and transpositions fill the four rows, use exactly $q$ P terminals, and leave $p-1$ Q uses plus the selected Q terminal. The minimum $d$ in the residue class is the first allowed integer at or above the appropriate bound, and $d=k-1$ is the maximum. The lower bound on $d$ also gives $k\ge\gamma+1$, verifying both geometry inequalities. There are $k-\gamma-1$ upper L sources and zero lower H sources, giving the stated $x,y$.

At $\delta=0$, $\rho=1,2$ both divide $\gamma+1-\sigma$. Their minima and conditions give exactly D193's low and companion baselines and its signed same-phase supplies. For $\delta=-1$ the numerator is $\gamma-\sigma$, an odd integer. Separation 1 is always admitted. Separation 3 is admitted precisely when $h\equiv1\pmod3$ in low or $h\equiv2\pmod3$ in companion. Separation 2 has no baseline on either fixed outbound layout. The independent moment in §1 is $M=A+\delta$, because $B+\delta-\gamma=1$. The baseline arrows contribute $\sigma+\rho q_{\min}=\gamma+\delta+1=A+\delta$, with zero from Q and from the transpositions. Beyond baseline, every actual first gap arrow has odd folded displacement, and there are $F-1$ of them; P has $q$ arrows with parity $\rho$, and Q contributes zero. Therefore
$$
A+\delta\equiv F-1+\rho q\pmod2 .
$$
The outbound left side is even and $F$ is even by the graph classes, so every even $\rho$ fails on this fixed outbound exterior at any successfully allocated first total. At odd outbound separation it also requires odd $q$ and even $p$, in agreement with the baseline domains. In the strict same phase, at $\rho=1$ it retains D193's even P and Q obstruction. Other reduced exteriors need their own analysis.

## 4. Q pair counts and phase-aware signed growth

A complete Q pair at $i$ consists of the two row exchanges at equal index $i$, with distinct actual Q terminal names. Below both holes $d,e$ each available arrow is Q. At the earlier of the two holes a first reservation or a P arrow prevents a pair. The contiguous initial Q pair interval is therefore $[\gamma,d-2]$ for low and $[\gamma,d-1]$ for companion, with exact length
$$
d-\gamma-(1-\sigma)/2
=\big(p-(\rho-1)q-2\big)/2 .
$$
For $\rho=1$ all later eligible cells meet a P chain or the defect and there are no further complete pairs. For $\rho=2$, beyond the two adjacent holes Q occurs in the L row only on the residue opposite $d$, and in H only on the residue opposite $e$. They are different, so here too there are no further pairs. For $\rho=3$, the remaining common residue above the holes is the unique one different from $d$ and $e$. Its indices up through $k-1=d+3t$ are $d+1,d+4,\ldots,d+3t-2$ in low and $d+2,d+5,\ldots,d+3t-1$ in companion. The larger hole itself has either an unavailable L source or a P H arrow. Thus these additional progressions contain exactly $t$ complete pairs outside the initial contiguous interval. The construction below uses the initial pair at $\gamma$ when present.

Add requested even first-terminal increments $2\lambda_+,2\lambda_-$, with $\lambda=\lambda_++\lambda_-$. The actual increase in the first total is $2\lambda$ at fixed second quotas, hence $K=K_0+\lambda$, $s=s_0+2\lambda$, $k=k_0+\lambda$, $J=J_0+2\lambda$, $T=T_0+\lambda$. Each folded right endpoint increases by $\lambda$ with left endpoint fixed, and $A\le K\le A+s$ and $s\ge T$ persist. Write $b=\min(\lambda_+,\lambda_-)$ and $\eta=|\lambda_+-\lambda_-|$, so $\lambda=2b+\eta$.

Keep all named initial transpositions on $[0,\gamma-1]$ fixed, and translate every other folded endpoint by $\lambda$ at its own actual parent. All such endpoints have index at least $\gamma$, so the four free rows are exactly $[\gamma,\gamma+\lambda-1]$. If the old H-image row was empty, the new row is exactly that strip. The upper and lower folded maps preserve displacements under the translation. When $\eta=0$, the $b$ adjacent column pairs partition the strip. For each pair $[i,i+1]$ use $L_i\to L_{i+1}$ and $H_{i+1}\to H_i$ at the positive host, and $L_{i+1}\to L_i$ and $H_i\to H_{i+1}$ at the negative host. These are the two full row transpositions of the pair. They supply two terminals per actual signed parent and preserve all Q and P names and quotas, including the identity case $b=0$.

When $\eta>0$, require the initial pair at $\gamma$, supplied by $p\ge(\rho-1)q+4$. After the same translation remove the two translated arrows of this Q pair. This vacates column $\gamma+\lambda$ in all four rows, so the exact free interval is $[\gamma,\gamma+\lambda]$. Put $b$ balanced pairs in the first $2b$ columns and use the last block $[l,r]=[\gamma+2b,\gamma+\lambda]$ for the larger sign. For positive use $L_i\to L_{i+1},H_{i+1}\to H_i$ for $l\le i<r$. The unused source cells are $L_r,H_l$ and the unused image cells are $L_l,H_r$; restore Q's original names as $L_r\to H_r,H_l\to L_l$. For negative use $L_{i+1}\to L_i,H_i\to H_{i+1}$. The unused sources are $L_l,H_r$ and images $L_r,H_l$; restore $L_l\to H_l,H_r\to L_r$. The explicit source and image intervals of these arrows partition the exact final block, each at the correct actual parent. Each restored Q name retains its original row direction. Thus the balanced part supplies $2b$ uses per sign, and the last block supplies $2\eta$ further uses of the larger sign. This is the D193 one-anchor argument with the actual phase-dependent row endpoints checked.

All P names, all nonanchor Q names and the retained first names stay at their actual parents. The existing outer selections keep their incidences. The total signed folded moment stays $A+\delta$, since each new same-sign pair contributes opposing folded shifts and the restored Q displacements are zero. The old number of L-to-H upper arrows stays fixed (any removed Q exchange is restored with both directions), while the $\lambda$ added first pairs give $\lambda$ H images. Thus $x=k_0-\gamma-1$, $y=\lambda$, and $x+y=s-T$ by the actual geometry. This proves equal even growth at any supplied baseline and independent even increases when the stated initial Q pair exists. It retains D193's full same-phase supplies and gives outbound supplies on the corresponding phase-specific baselines.

## 5. Reverse exceptional-to-strict supplier

Use $\varepsilon=-1,\ \varepsilon'=0,\ \delta=1$ on the actual profiles $(h+4,h)$ and $(p,h+3)$ with $h\ge2$, $p\ge h$ and $p\equiv h\pmod2$, adding the original $2h-3$ and $2h-2$ direct leaves, respectively. Set $A=2h+1,B=2h+2$. The original first quota-$(h+4)$ center occupies $A-1$, and the quota-$h$ center occupies 2. Put its selected first indexed terminal at $A+2$. Q occupies upper index 3, with its first indexed terminal at 1. P occupies upper index $2h+1$. The original first and second direct leaves fill the remaining proper child slots in $[2,A-1]$ and $[2,B]\setminus\{2\}$, respectively. The spine takes reduced $(A,A+1,0)$. This is a movable-exchange layout of the type used in [D190](ORDINARY_SPINE_EXCEPTIONAL_MOVABLE_TERMINAL_EXCHANGE.md), now with the actual changed-phase threshold.

Both low and high reduced alphabets are filled once. All actual edges cross in the exterior and connect through the original spine and original parent incidences. The first spine edge and first children give $[1,A-1]$, and the selected first terminal gives $A$. The connector gives $A+1$. Second children give $A+([2,B]\setminus\{2\})$, while the selected Q terminal supplies $A+3-1=A+2$. Thus the exact reduced difference alphabet is $[1,A+B]$. The lower shifts in §1 are zero at the quota-$(h+4)$ center and $\rho_R=2h-2$ at the other first center. With $J=s+4$, $\gamma_R=5$, the actual Q and P exchanges have folded separations zero and $\rho_R$, respectively.

The auxiliary Q count $p_0=h$ gives $R_0=2h+3$ and $F=2h+4$. The original child and spine edges number $4h+1$. Hence
$$
2K_0=8h+8,\quad K_0=4h+4,\quad s_0=4h+5,\quad
k_0=2h+3,\quad J_0=4h+9,\quad T_0=K_0+1=s_0.
$$
The folded rows are L sources $[0,2h+2]$, H sources $[5,2h+6]$, L images $[0,4h+4]$, H images $[5,4]$ (empty). The width inequalities $A\le K_0\le A+s_0$ and $s_0\ge T_0$ hold. The neutral center receives all L identities on $[0,h+3]$. The first shifted center uses L sources $[h+4,2h+2]$ with images $[3h+2,4h]$ and retains its selected exterior terminal. The H sources partition into P on $[5,h+3]$ and $[2h+3,2h+6]$ and Q on $[h+4,2h+2]$. P has L images $[2h+3,3h+1]$ and $[4h+1,4h+4]$; Q has equal-index L images $[h+4,2h+2]$. In increasing order the five image intervals are the neutral, Q, first P, shifted first, and last P intervals, consecutive with no overlap. Thus every L image and both source rows are filled exactly. Q has $h-1$ gap uses plus its selected terminal and P has $(h-1)+4=h+3$. Every baseline gap arrow is noncrossing by the empty H-image row and the physical maps.

Set $z=(p-h)/2$. Keep the first five named neutral identities on $[0,4]$ fixed, and translate all other folded endpoints by $z$. At the full actual size $2K=7h+8+p$ we have $K=K_0+z$, $s=s_0+2z$, $k=k_0+z$, $J=J_0+2z$, and $T=T_0+z$. Each folded right endpoint grows by $z$. The exact common free strip is $[5,5+z-1]$ in both source and both image rows. In particular the previously empty H image becomes that strip. Fill both directions at equal index in that strip at the actual Q center. This uses exactly $2z$ further Q terminals and no other new quota, with legal crossings at the new cut. The result has $x=z,y=0$, $x+y=s-T$, in agreement with the actual graph counts $2(A+z)+1,2B+1$ for the two fresh colors. The geometric signed moment is $(A+1)(B+1-5)=(2h+2)\rho_R$. The first shifted arrows contribute $(h-1)\rho_R$, P contributes $(h+3)\rho_R$, and all neutral and Q arrows contribute zero, including the growth strip. The actual shifted old and exterior resources meet the new strict spectrum by §1. All assignments refer to the actual admitted target and its own residual names; the auxiliary quota calculation adds no intermediate graph.

## 6. The common original toggle families

Consider the original first and second profiles
$$
(h+4,h,\underbrace{0,\ldots,0}_{2h-3}),\qquad
(p,h+3,\underbrace{0,\ldots,0}_{2h-2})
$$
in any physical order with selectable numerical roles. The outbound uses the companion baseline $(h+2,h)$ at $\delta=-1$ and the positive-only growth $(\lambda_+,\lambda_-)=(1,0)$. Hence the first quota-$(h+4)$ center is the positive signed host with the selected first terminal; the reverse uses that same physical center as neutral and selects a terminal from the quota-$h$ center. Both keep Q at the actual quota-$p$ center and P at the actual quota-$(h+3)$ center. These are two independent exteriors on the same indexed child and terminal topology.

- With outbound separation 1, $q_{\min}=2h-1$ and $q-q_{\min}=4-h$. This is nonnegative and even exactly at $h=2,4$ within $h\ge2$. Even $p\ge4$ satisfies the initial-pair threshold, gives the odd total $R$, and meets the reverse requirement $p\ge h,\ p\equiv h\pmod2$.
- With outbound separation 3, take even $h\equiv2\pmod3$, i.e. $h=6j+2$ with $j\ge0$. Then $q_{\min}=(2h-1)/3=4j+1$, $q=h+3=6j+5$ and $t=(q-q_{\min})/2=j+2$. Even $p\ge2(h+3)+4$ gives the required odd total and an initial Q pair, and also satisfies $p\ge h$ and the reverse parity. The upper index $b_0+3=B$ is an actual P slot, with the remaining real children placed as in §2.

Both suppliers compute the identical full fresh size $2K=7h+8+p$ from the actual graph. The construction reads the incoming phase, chooses the proper numerical exterior, and checks that actual prefix's full admission for the target. The widths agree, but the selected terminal's physical parent and some labels differ. The family is unbounded in $p$, and at separation three also in $h$. Such sizes require correspondingly large independently supplied inputs. D157 §7 gives independent strict seeds within its hypotheses and compatible phase-changing legs at sufficiently large sizes, supplying independent inputs of both phases on their own particular original prefixes. The common-block theorem requires admission for whichever actual prefix is supplied; it neither duplicates nor pads the actual target.

## 7. Indexed terminal realization and exact numerical gap resources

For the signed supplier, enumerate the finite possible numerical roles and admitted separations at the actual indexed centers, breaking ties by original child indices. Check the stated arm, quota and growth conditions and the full size; extract $d,e$ by §3. For the reverse, check the original quota equations and compute $z$ directly. For the common block use §6 according to the incoming phase. Order the original direct leaves by their indices in their assigned complement slots. Choose the first indexed actual terminal at each selected parent as specified by the exterior. In each gap host allocate the baseline residual names in increasing original index order to that host's baseline sources in increasing unfolded numeric order. This reserves the actual Q names before translations or anchor removal. Then translate the retained assignments, reassign the explicitly named Q pair if used, and give new packet or free-strip arrows their remaining original terminal names in unfolded source order at their own parent. All quota balances were proved in the row partitions. The calculation uses finite arithmetic and the actual full target's terminal lists.

For a signed grown block, set $J=J_0+2\lambda$. A translated H endpoint of original folded index $i$ gains $\lambda$ numerically by $J-(i+\lambda)=J_0-i+\lambda$, as does a translated L endpoint. The initial fixed L arrows keep their endpoints. The restored Q arrows use their actual prescribed packet endpoints under the final unfolding. Define numeric first source sets $S_+,S_-$ beginning with the even and odd indices of $[0,\gamma-1]$, respectively. Add $\{d+\lambda\}$ to the defect's sign source set. For the balanced pairs, put $U=\{\gamma+2j:0\le j<b\}$. Add $U\sqcup(J-(U+1))$ to $S_+$ and $(U+1)\sqcup(J-U)$ to $S_-$. These reflect the L and H sources of their actual arrows, with set arithmetic elementwise. If present, the excess positive block $[l,r]$ adds $[l,r-1]\sqcup[J-r,J-l-1]$ to $S_+$; the excess negative block adds $[l+1,r]\sqcup[J-r+1,J-l]$ to $S_-$. The exact signed first source and image sets are
$$
I=S_+\sqcup S_-,\qquad J_1=(S_++1)\sqcup(S_--1).
$$
Disjointness follows from the row partitions and the exact unfolded alphabets. These images use the actual lower numeric translations on both rows.

For the reverse, all first arrows use L; the five initial neutral identities stay fixed. The actual neutral source and image set is $I_N=[0,4]\sqcup[5+z,h+3+z]$. The shifted first source set is $I_R=[h+4+z,2h+2+z]$ and its image set is $I_R+\rho_R$. Thus
$$
I=I_N\sqcup I_R,\qquad J_1=I_N\sqcup(I_R+\rho_R).
$$
Every old reverse H index translated by $z$ also gains $z$ numerically, since $J=J_0+2z$. The new reverse Q uses both directions in the explicit free strip and no neutral name leaves its first parent. In either supplier define remaining $I',J_2$ as the exact respective complements of $I,J_1$ in $[0,s-1]$. These formulas derive resources from actual placed arrows, including reserves at the literal first-section boundary.

## 8. Full palettes, intermediate inventories, both polarities

The minimum-oriented old label map adds $A$ below $c$ and $A+s$ at or above $c$. The verified inequalities keep the old labels on their respective sides at $C=c+K$. The lower exterior remains in place, and $n+s$ is added to the upper exterior and to each exterior difference. The placed shared $v=A$ agrees with the old value. Exterior incidences cross because their lower labels are at most $A<C$ and their upper labels are at least $n+s+A+1>C$. Gap leaves take the exact numeric placements of §1. The two pairs of exact old and fresh palettes are
$$
\begin{array}{ll}
L_{\rm old}=[A,A+c-1]\sqcup[A+c+s,n+s+A],&
L_{\rm fresh}=[0,A-1]\sqcup[A+c,A+c+s-1]\sqcup[n+s+A+1,m],\\
D_{\rm old}=[1,d_0+\varepsilon-1]\sqcup[d_0+\varepsilon+s,n+s],&
D_{\rm fresh}=[d_0+\varepsilon,d_0+\varepsilon+s-1]\sqcup[n+s+1,m].
\end{array}
$$
They are disjoint partitions of $[0,m]$ and $[1,m]$, and the actual positions, differences and spectra constructed above exhaust them once. The input crossings gain $s$ and input noncrossings are unchanged. Gap differences split at $T$ before adding $d_0+\varepsilon$, and $\varepsilon+\delta=\varepsilon'$. Hence the combined actual crossing and noncrossing bands are $[d_0+K+\varepsilon',m]$ and $[1,d_0+K+\varepsilon'-1]$. All actual graph incidences and the distance-two witnessing spine remain valid. Since $w=0$ and $m=2C+2$, this is exactly $S_{\varepsilon'}$.

Let $j_e=j_+$ for the signed exterior and $j_e=2$ for the reverse. At the first-section boundary the exact placed first and remaining exterior label sets are
$$
E_1=[2,A-1]\sqcup\{n+s+A+1,n+s+A+j_e\},\qquad
E_2=\{0,1\}\sqcup\{n+s+A+b:2\le b\le B,\ b\ne j_e\}.
$$
The first set comprises the actual first children at $u$, $u$ itself and the selected terminal at its actual first parent. The remaining set comprises $w$, the selected Q terminal and all actual second children in their slots. The two suppliers use their respective $j_e$ even when their widths agree. The actual reduced difference computations in §§2 and 5 give $D^e_1=n+s+[1,A]$ and $D^e_2=n+s+[A+1,A+B]$. Thus
$$
\begin{array}{ll}
\mathrm{used\ labels}&L_{\rm old}\sqcup E_1\sqcup(A+c+I),\\
\mathrm{remaining\ labels}&E_2\sqcup(A+c+I'),\\
\mathrm{used\ differences}&D_{\rm old}\sqcup D^e_1\sqcup(d_0+\varepsilon+J_1),\\
\mathrm{remaining\ differences}&D^e_2\sqcup(d_0+\varepsilon+J_2).
\end{array}
$$
The old label bands keep their indicated sides, and exterior values retain their reduced sides. Split $I,I'$ at $k$ and $J_1,J_2$ at $T$ before applying the offsets, for the two exact label-side and difference-crossing partitions. The old difference bands in order are noncrossing and crossing, and all exterior differences cross. The actual unfinished connector is $uw$, with endpoints $(n+s+A+1,0)$ and weight $n+s+A+1$ in the remaining exterior band.

For maximum polarity complement the input at $n$ to orient it and complement the output at $m$. The actual cuts are $n+1-c$ and $m+1-C$. The maximum-oriented shifts below and at or above its input cut are $B$ and $B+s$, by $A+B+s=2K$. The complementary labels exchange sides in both inventories, while both difference inventories and crossing flags are unchanged. The actual connector endpoints become $(B-1,m)$ with the same crossing weight and actual frontier $w=m$.

## 9. Symbolic original-target controls and corrected spectra

Use the retained named maximum-polarity inputs on 74 edges in $S_{-1}$ at cut 39 and on 94 edges in $S_0$ at cut 49. Their oriented $d_0$ references are 38 and 48, respectively. In controls below the listed center orders are the physical profile order, with the sign or neutral roles chosen as specified by each supplier. Each zero is an actual indexed direct leaf. In all cases the new maximum cut is the old maximum cut plus $K$, and the minimum crossing weight is $d_0+K+\varepsilon'$.

**A — strict retention.** At $\delta=0$ the signed row geometry, defect ranges and chains are exactly D193's. At $h=2$ with $(p,q)=(2,6)$ and $\rho=1$ they give $k=6,d=5$ in low and $d=4$ in companion. With $\rho=2$ and $(5,3)$ in low they give $k=6,d=5,e=4$ and P on H indices $4,6,8$. The same-phase balanced and one-anchor operations have the exact D193 domains, since both initial bank counts recover its values and all row and crossing tests coincide.

**B — outbound separation one.** For $(3,3,0),(2,5,0,0)$ take $h=2,\rho=1,\sigma=-1$. Then $q_{\min}=5$, $t=0$, $k=6,d=5,e=4$, $2K=22$, $s=11$ and $T=10$. Q uses $L_4\to H_4$ plus its selected terminal, and P uses H indices $4,\ldots,8$ to L indices $5,\ldots,9$. For $(4,2,0),(2,3,0,0)$ take $\sigma=+1$, $q_{\min}=3$, $k=5,d=4,e=5$, and $2K=20$. Here $s=T=9=K-1$, the H images are empty, Q uses $H_4\to L_4$ plus its selected terminal, and P uses H indices $5,6,7$ to L indices $6,7,8$. The first arrows fill the other L images in each case. Their output sizes, maximum cuts and actual crossing bands are $(116,60,[58,116])$ and $(114,59,[57,114])$.

**C — outbound separation three with P quota one.** For $(4,2,0),(4,1,0,0)$ take $h=2,\sigma=+1,\rho=3$, $q_{\min}=1,p=4,t=0,k=5,d=4,e=5$, and $2K=20$. The first arrows use all L sources $[0,4]$ and L images $[0,3]\sqcup\{5\}$. The H sources are $[4,7]$, the P arrow is $H_5\to L_8$, and Q uses H indices $4,6,7$ by identity plus its selected terminal. These fill the exact remaining L alphabet $\{4,6,7,8\}$. The H image is empty because $s=T=9$. The output is $S_{-1}$ on 114 edges, actual maximum cut 59 and crossing differences $[57,114]$.

**D — outbound separation-three low arm.** For $(5,5,0,0,0,0,0),(8,3,0,0,0,0,0,0)$, $h=4,\gamma=8,q_{\min}=3,R=11,k=10,d=9,e=8$ and $2K=38$. P uses H $8,11,14$ to L $11,14,17$. The other H indices $9,10,12,13,15,16$ go to Q identities, and $L_8\to H_8$ and the selected Q terminal complete its quota eight. The first arrows give L images $[0,7]\sqcup\{8\}$. The output is 132 edges at maximum cut 68, crossing $[66,132]$.

**E — common toggle at $h=2$.** The exact original profiles are $(6,2,0),(4,5,0,0)$. For outbound separation one, $(q_{\min},t,k_0,d,e)=(3,1,7,5,6)$. The baseline Q pair at 4 consists of terminal indices 1 (L direction) and 3 (H direction) after the selected index 0, since its other H source is at column 5 and $J_0=16$. Positive growth of width one uses $[4,5]$, restoring those original Q names at $L_5\to H_5$ and $H_4\to L_4$. The quota-six first center is positive and has its own first terminal exterior. For the reverse it is neutral and the other center provides the first exterior terminal. The reverse at $z=1$ has neutral source/image set $[0,4]\sqcup\{6\}$, first shifted source 7 with image 9, and adds Q on both directions at index 5. These are two independent allocations on the actual same profile with $2K=26$, $A=5,B=6,s=15$. On the retained 74-edge exceptional input, the reverse gives 100 edges at maximum cut 52 with crossings **$[51,100]$** and noncrossings **$[1,50]$**. On the retained 94-edge strict input, the outbound gives 120 edges at maximum cut 62 with crossings **$[60,120]$** and noncrossings **$[1,59]$**. The phase formula adds 13 to the input strict reference and then applies the outgoing phase. The proposed endpoints $50$ and $59$ respectively used one too low a crossing weight. The two full original contexts have different prefixes.

**F — common toggle at $h=4$.** The actual first quotas are $(8,4)$ with five direct leaves; the second are $(4,7)$ with six. The outbound has $q_{\min}=7,t=0,k_0=10,d=9,e=10$ and its pair at 8 supplies positive growth on $[8,9]$. The reverse uses $p=h$ and $z=0$. Both have $2K=40$ and retain the actual named parents and counts. On the 94-edge input the outbound returns 134 edges at cut 69 with crossings $[67,134]$. On the 74-edge input the reverse returns 114 edges at cut 59 with crossings $[58,114]$.

**G — wider separation-three toggle.** The actual first quotas are $(12,8)$ with 13 direct leaves and the second $(26,11)$ with 14. Here $h=8,\gamma=16,\rho=3,q_{\min}=5,t=3,R=37,k_0=27,d=17,e=18$. P's L indices are $20,23,26$ and H indices $18,21,24,27,30,33,36,39$. There is exactly one initial Q pair at 16 and three additional residue pairs at 19, 22 and 25. Positive growth uses the initial pair on $[16,17]$. The full size is $2K=90$, admitted by the 94-edge strict input, giving 184 edges at cut 94 with crossings $[92,184]$. For the reverse use the 120-edge exceptional output of the actual E extension of the 94-edge input, already constructed independently above. It admits the larger original G sections and gives $z=9$. The first neutral and shifted allocations and Q strip of §5 give 210 edges at maximum cut 107, crossing $[106,210]$ and noncrossing $[1,105]$. The additional E block is part of that exact original prefix.

**H — three-copy cycle and final labels.** On the 74-edge exceptional input append three distinct named copies of E. The actual sizes are $74\to100\to126\to152$, the phases $S_{-1}\to S_0\to S_{-1}\to S_0$, and the actual maximum cuts $39\to52\to65\to78$. Each input admits the whole next size 26. At the successive outputs the crossing bands are $[51,100]$, $[63,126]$ and **$[77,152]$**. In particular the final strict noncrossing band is **$[1,76]$**. The proposed crossing start 76 is one too low because the final oriented cut is 75, so its strict reference is 77.

For immutable final labels in H, every actual copy has maximum lower shift 6 and gap increment 15. On the initial graph the final image of a local label $x$ is $x+18+45\mathbf1_{x\ge39}$. For a label at completed copy $i$ (with $i=1,2,3$ and actual cut $C_i$), its image is $x+6(3-i)+15(3-i)\mathbf1_{x\ge C_i}$. This gives an exact value for every named original vertex once its local copy is supplied. The three literal connectors with local endpoint pairs $(5,100),(5,126),(5,152)$ end at $(17,142),(11,147),(5,152)$, respectively. The crossing differences gain the remaining gap sums; noncrossings stay fixed. The entire actual original topology and both evolving inventory partitions are retained.

**Adverse equal-child-count baseline.** Take equal child counts $a=a_2=\gamma-1$ with the same signed roles, one selected terminal in each section, and $F=\gamma+1$. Then $A=B=\gamma+1$ and $\delta=-1$ implies odd $R$. From the actual fresh count $s=2k$, $T=k+\gamma$, and the graph classes give $y=0$ and $x=k-\gamma\ge0$ for a success. In the fold $J=s+\gamma-1$, the initial transpositions are forced by the same low source and image argument, and use all $F-1=\gamma$ first leaves. The upper L sources and H images then both use $[\gamma,k-1]$ and upper H sources and L images both use $[\gamma,k+\gamma-1]$. In either direction the total index change is zero and the only shifted upper moves have a single sign. They cannot be used. All upper arrows therefore belong to Q, ruling out positive P residual quota on that fixed exterior with those counts. This does not decide other phase-changing layouts.

## 10. Composition, termination and remaining scope

Every return supplies the independently usable actual D157 boundary for its phase, including both literal frontier and inventories. Within either fixed physical polarity, an admitted next block preserves old cut sides. At an earlier completed boundary $i$ with actual cut $C_i$, let $U_i,V_i$ be the sums of actual subsequent lower shifts and gap sizes. The final label of local value $x$ is $x+U_i+V_i\mathbf1_{x\ge C_i}$, since each next placement preserves the evolving cut sides. Every earlier crossing difference gains $V_i$ and every noncrossing difference is unchanged. Both intermediate inventories and unfinished connector endpoints transport by these formulas. Their exact remaining resources in the eventual alphabet also include the disjoint subsequent fresh palettes. Finite indexed role tests, explicit arithmetic interval scans, and backward sums give a terminating immutable realization. Every step checks admission on its actual incoming graph.

The theorem addresses phase compatibility on the stated named two-section profiles. Its unbounded parameter families retain independent initialization, actual size admission and compatible cuts as hypotheses. Small and empty sections, further actual topologies, initial states outside the retained independent-seed premises and arbitrary decomposition into compatible blocks remain open. D191's numerical lane remains **SYMBOLICALLY_RESOLVED / NO_EXECUTION_NEEDED**. The current investigation used no numerical search, allocation states, original checker, scientific campaigns or historical replays.
