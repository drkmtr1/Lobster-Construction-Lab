# D179 — Independent second-quota growth on width-five exceptional exteriors

Task **LCL-ORDINARY-SPINE-EXCEPTIONAL-INDEPENDENT-SECOND-QUOTA-GROWTH-001**.

**PROVED WITHIN EXACT WRITTEN SCOPE / PENDING DIRECTOR REVIEW.** For every odd $r\ge9$, every physical first order of $r$ positive even quotas with at least one quota at least four, and every pair of positive even second quotas, terminal-enabled H1 feasibility in the declared D157 $S_{-1}$-to-$S_{-1}$ arrangement is equivalent to $R\ge r+3$, where $R$ is the second quota total. The input prefix is independently supplied and admissible for the full requested size. The first section has no direct leaf. The single actual second direct leaf is exterior. Numerical role selection preserves all original physical incidences and admits both physical orders. The negative threshold follows from original graph-class counts and terminal balance. The positive proof uses II-a or I-a and grows the numerical second capacities by explicit strip assignments.

## 1. Exact original counts and threshold necessity

Use the [D157 exceptional placement](ORDINARY_SPINE_ALTERNATING_EXCEPTIONAL_SPECTRUM.md#1-interface-and-exact-inventory-rule). All structural quantities and labels are exact integers, excluding booleans. Intervals are inclusive, with a reversed interval empty. The independently supplied named graceful prefix has $n=2c+2$ edges, its actual witnessing spine ends at an extreme frontier $v$, and orient to $G(v)=0$. The oriented cut is $c$, with equality on its upper side, and $d=c+2$. The input crossing differences are $[d-1,n]$ and the remaining differences are $[1,d-2]$. Append the actual first and second spine vertices $u,w$. Write $F$ for the sum of the $r$ first quotas and $R=p+q$ for the second terminal total. Counting the two new spine vertices, $r+2$ centers, the actual direct leaf at $w$, and $F+R$ terminals gives
$$
2K=F+r+R+5,\qquad m=n+2K,\qquad n\ge2K.
$$

In the fresh graph color class rooted at $v$ as lower, the lower fresh vertices are $w$, the $r$ first centers and the $R$ second terminals. The other class contains $u$, the two second centers, the direct leaf and the $F$ first terminals. Thus $N_{\rm low}=1+r+R$ and $N_{\rm high}=4+F$. In any compatible H1 exterior of the declared arrangement, all actual centers and the direct leaf are exterior, and the induced connected crossing reduced exterior places the actual graph colors on its two occupied sides. If $e_1,e_2$ count selected exterior terminals in the first and second section, the width counts are $A=r+1+e_2$, $B=4+e_1$. Here $v=A,w=0$, with $v$ an old lower label in oriented placement. The unique reduced weight-one edge crossing $[0,A]$ to $[A+1,A+B]$ uses $A,A+1$. Its actual edge must be $vu$ because that is the sole new incidence at $v$. Thus $u=A+1$.

Use the numerical reference with $vu,uw$, attaching each lower slot $j\in[1,A-1]$ to $u$ and each upper slot $A+b$ for $b\ge2$ to $w$. Its differences fill $[1,A+B]$. For an actual selected first terminal at upper slot $A+b$, its parent $j$ is a first center of positive lower reduced label and the reference difference is reduced by $j$. For an actual selected second terminal at a lower slot, its parent is an actual second center at $A+b$ with $b\ge2$, and its difference exceeds the reference by $b-1$. All other edges, including the direct leaf, keep their reference differences. Equality of the sums of the two spectra gives $\sum_{\text{first selected}}j=\sum_{\text{second selected}}(b-1)$. Each summand is positive. A terminal-enabled exterior has at least one selected terminal, so $e_1,e_2\ge1$. This proof uses the actual parent incidences and requires no bound on residual neutral capacity.

Put $s=2K-A-B$, $k=K-A$. An admitted completion preserves old side memberships with $A\le K\le A+s$. Since the least old crossing difference $d-1$ grows by $s$ and the output crossing interval starts at $d+K-1$, the same-phase placement requires $s\ge K$. Exterior differences fill $[n+s+1,m]$ and cross. Old crossings fill $[d-1+s,n+s]$. Thus exactly $s-K$ gap differences cross and a gap index of difference $\pi(i)$ in the normalized alphabet crosses iff $\pi(i)\ge K$. The $k$ lower and $s-k$ upper physical gap sources are determined by the cut. Let $x$ count lower sources at upper hosts and $y$ count upper sources at lower hosts. Then $x+y=s-K$. All residual leaves have color opposite their actual host, independent of their spatial labels, so the number of fresh lower-color gap leaves is the count at upper hosts. This is
$$
s-k-y+x=A+2x,\qquad N_{\rm low}=A+(A+2x)=2(A+x).
$$
Consequently $1+r+R\ge2(r+2)$ since $e_2\ge1$, proving $R\ge r+3$ as a necessary condition for every compatible terminal-enabled H1 exterior in the stated arrangement. This excludes below-threshold H1 targets and makes no decision about terminal-free returns or ordinary gracefulness without the placement constraints.

## 2. Fixed width-five exteriors and admitted baseline rows

For positive supply retain the [D178 constructions](ORDINARY_SPINE_EXCEPTIONAL_ARBITRARY_EVEN_FIRST_QUOTA_LIFT.md) of II-a and I-a as described below. Set $R_0=r+3$ and write $h=F/2-r-1\ge0$. Keep the actual first quotas fixed throughout. With $A=r+2,B=5$, choose $v=A,u=A+1,w=0$, and $Q=A+2$. Choose the actual neutral center of an even quota at least four. Each other numerical role is supplied at the corresponding actual quota and physical center by D178. The lower original first centers take slots $[1,A-1]\setminus\{t_0\}$. The relevant upper indices and terminal roles are:

| Geometry | Reduced slot $t_0$ of terminal at $P$ | First selected terminal | $P$ | Actual direct leaf at $w$ | Separation $\rho$ |
| --- | ---: | --- | ---: | ---: | ---: |
| II-a | 2 | $A+3$ at parent 4 | $A+5$ | $A+4$ | 3 |
| I-a | 1 | $A+3$ at parent 3 | $A+4$ | $A+5$ | 2 |

Choose the first actual numbered terminal at each selected parent. These actual edges give a connected crossing exterior. In I-a the first attachments at $u$ together with $vu$ give $[1,A-1]$, with $A$ from the first selected terminal. In II-a they give $[1,A]\setminus\{A-1\}$ and that terminal adds $A-1$. The other edges give $A+1$ at $uw$, $A+2$ at $wQ$, $A+3$ at the selected $P$ terminal and $A+4,A+5$ at the two remaining true attachments at $w$. The raw difference and vertex-label spectra are $[1,A+5]$ and $[0,A+5]$. The direct incidence belongs to the original exterior and never consumes a gap slot. The two upper residual quota counts at the baseline are $p_0-1,q_0$. Neither geometry requires a quota equality or inequality to supply its reduced exterior, apart from the existence of the selected terminals.

At total $R_0$, $K_0=2r+5+h$, $s_0=3r+3+2h$, and $k_0=K_0-A=r+3+h$. For a requested increase $2\lambda$ in $R$, with $\lambda\ge0$, these become
$$
K=K_0+\lambda,\qquad s=s_0+2\lambda,\qquad k=k_0+\lambda,\qquad J=s+3 .
$$
In particular $s-K=r-2+h+\lambda\ge0$, and $A\le K\le A+s$. The admitted input size $n\ge2K$ also suffices for each baseline and each intermediate parameter value in the construction.

Subtract actual expanded endpoints using $A+c+i$ for source coordinate $i$ and $d-1+\pi(i)$ for its actual difference. Then $\pi(i)=i+\delta$ for a lower host at reduced label $j_0$, with $\delta=A-1-j_0$. At upper reduced label $A+b_0$, $\pi(i)=s+b_0+1-i$. This sign uses the lower host smaller than every gap label and the expanded upper host larger than every gap label. The folded notation $L_j=j,H_j=J-j$ gives row alphabets
$$
\begin{array}{c|cc}
&L&H\\
\text{sources}&[0,r+2+h+\lambda]&[4,2r+3+h+\lambda]\\
\text{images}&[0,2r+4+h+\lambda]&[4,r+1+h+\lambda].
\end{array}
$$
The H rows unfold to $[k,s-1]$ for sources and $[K,s-1]$ for images, giving two full numerical alphabets $[0,s-1]$. A lower host gives $+\delta$ on L indices and $-\delta$ on H indices. An upper host exchanges rows with unchanged index at $Q$ and with shifts $-\rho,+\rho$ on L and H sources at $P$. Every legal arrow therefore has the exact physical predicate: opposite source and host sides correspond to H images and to weights $\pi(i)\ge K$.

The D178 baseline supplies $L_j\to L_j$ for $0\le j\le3$ at the neutral host. Other L sources and L images are at least four by bijectivity, and the H rows both start at four. Its baseline gap arrows are given independently by the actual quota parameters. The input need not be a previously solved target, and D178's original preassigned-tail obstruction and exact support statement remain separate.

## 3. Q-only growth

For any $\lambda\ge0$, use the row expansions of §2. Fix the four initial neutral arrows. Translate every other folded source and image by $\lambda$ in its respective row and keep its original parent. Row indices $[4,U]$ become $[4+\lambda,U+\lambda]$ for each old upper endpoint $U$. Every old legal displacement is preserved, and precisely $[4,3+\lambda]$ remains in each of the four source and image rows. Give both directions in this common strip to $Q$:
$$
L_j\to H_j,\qquad H_j\to L_j\quad (4\le j\le 3+\lambda).
$$
They are disjoint and give the exact four complementary row sets. The first direction crosses and the second one does not. Thus only the quota at $Q$ grows, by exactly $2\lambda$. The $Q$ growth proof works for II-a and I-a and at any compatible input allocation retaining the four initial neutral arrows. This includes the relevant D178 baselines at $r=5,7$.

In the new fold $J$ increases by $2\lambda$. A translated L index $j+\lambda$ unfolds to the old L numerical coordinate plus $\lambda$, and a translated H index $j+\lambda$ unfolds to $(J_{\rm old}+2\lambda)-(j+\lambda)=(J_{\rm old}-j)+\lambda$. The four initial neutral coordinates are fixed. This numerical calculation accounts for the relocated cut and gap-weight threshold. Exterior high labels and the old high band are instead placed with the full new gap width $s$. The operation concerns folded allocation arrows at fixed actual hosts, with additional actual terminals assigned at $Q$.

## 4. Balanced growth in I-a

The D178 I-a baseline has the first-host arrow $L_4\to L_{4+\delta}$ with $\delta\in\{0,1\}$ for $r\ge7$. Indeed if there are extra neutral pairs, the first one is at 4 with shift zero. Otherwise the regular strip is nonempty, beginning at shift one. At an ordinary host its first pair begins at 4. When the first group is active, any prepended first-host pair uses its least shift one. If there is no prepended pair, the first L position of the central block uses that same least shift one, independent of its middle multiplicity and appended pairs. These exhaust the modes. The anchor belongs to an actual first gap terminal, distinct from the selected exterior terminal.

Use a first expansion of size $\lambda_b=2b$, $b\ge1$. Temporarily use the translation of §3 with insertion strip $S=[4,3+2b]$. Replace the translated anchored arrow at its own first host:
$$
L_{4+2b}\to L_{4+2b+\delta}\quad\longmapsto\quad L_4\to L_{4+\delta}.
$$
Both new cells lie in $S$ since $b\ge1$ and $\delta\le1$. The displacement and physical lower-host assignment are unchanged. All other translated old arrows remain in their own cells, and the same old anchored source and image are freed. This move takes exactly its new L source and L image out of the tentative $Q$ strip and leaves both H rows' free sets equal to $S$.

**L-source direction.** The free L sources are $(S\setminus\{4\})\sqcup\{4+2b\}$ and the free H images are $S$. Give $P$ the $b$ arrows
$$
L_{4+2j}\to H_{4+2j-2},\qquad j=1,\ldots,b.
$$
The first source is at 6 and the last is the freed old source at $4+2b$. The images run from 4 to $2+2b$ in steps of two, all in $S$. Exactly the odd columns of $S$ remain in both rows. Match them by identity at $Q$. The $b$ shifted and $b$ identity arrows exhaust the sets and all are crossing.

**H-source direction.** The free H sources are $S$ and the free L images are $(S\setminus\{4+\delta\})\sqcup\{4+2b+\delta\}$. Give $P$ the $b$ arrows
$$
H_{4+\delta+2j}\to L_{6+\delta+2j},\qquad j=0,\ldots,b-1.
$$
The last source is $2+2b+\delta\le3+2b$, so every source is in $S$. The images are the next same-residue columns in $S$ and the freed old image at $4+2b+\delta$. All shifted sources and images are distinct in their alphabets. The $b$ columns of the opposite residue in $S$ require the $b$ $Q$ identities. All these arrows are noncrossing. No arrow hits a translated reservation because the only used cells outside the common strip are the two explicitly freed L cells. The two directions have disjoint rows in their source alphabets and in their image alphabets. Together they give complete bijections and add $2b$ residual assignments at each of $P,Q$, preserving every first quota and selected exterior incidence.

The moved anchor is still legal by direct unfolding with $J_b=J_0+4b$. Every other translated arrow unfolds as in §3 and every new arrow satisfies the exact row cut predicate. In particular neither the old first-host crossings nor their count change because the single move uses L source and L image. The $b=0$ operation is the original allocation without a move. After either operation all noninitial folded indices stay at least four, so a subsequent Q-only strip of size $a\ge0$ uses §3 exactly. This gives the claimed net change
$$
(p_0,q_0)\longmapsto(p_0+2b,\ q_0+2b+2a).
$$
Here the total parameter in §2 is $\lambda=2b+a$.

## 5. Baseline choice and the principal domain

Take the requested roles with $p\le q$ and break a tie by original index. At $R\ge R_0$, if $p=2$, choose the independent D178 II-a baseline $(2,r+1)$ and use Q-only growth. The target size and the genuine terminal indices at both centers admit this baseline. For $p\ge4$ choose I-a. Let $P_0$ be the largest even integer at most $(r+3)/2$. If $p\le P_0$, put $p_0=p,q_0=R_0-p$. The baseline has $p_0\le q_0$ and the target has $q\ge q_0$. Q-only growth suffices.

If $p>P_0$, try $p_0=P_0,q_0=R_0-P_0$. When $R_0\equiv0\pmod4$ this baseline is equal, so both coordinates fit and $p-p_0\le q-q_0$ follows from $p\le q$. When $R_0\equiv2\pmod4$, the baseline difference is $q_0-p_0=2$. If $p<q$, then $q-p\ge2$ by evenness. Since $p>P_0$ one has $p\ge P_0+2$, and the requested capacities fit and satisfy the needed growth inequality. In these cases the baseline is an admitted direct D178 I-a allocation.

The remaining case has $p=q>P_0$ and $r\equiv3\pmod4$. Choose the reversed allocation with
$$
p_0=(r+5)/2,\qquad q_0=(r+1)/2 .
$$
Here $p_0=P_0+2$, $q_0=P_0$, so both are positive even, they fit at the actual requested parents, and $q-q_0=(p-p_0)+2$. To justify this reversed numerical choice, inspect the constructive D178 proof. The exterior I-a needs just the selected terminal at $P$ and one at the first parent, with the same reduced labels as §2. The neutral and ordinary first assignments and the selectable tail constructions depend on the first quotas and the exterior, never on an inequality between the full upper quotas. In [D178 §2](ORDINARY_SPINE_EXCEPTIONAL_ARBITRARY_EVEN_FIRST_QUOTA_LIFT.md#2-arbitrary-neutral-and-regular-expansion), $p_0\le q_0$ was used to ensure that there are $3a_0$ regular shifts for $a_0=(p_0-4)/2$ active triples. With this reversed choice their actual requirement is
$$
3a_0=3(r-3)/4\le r-5\quad\Longleftrightarrow\quad r\ge11 .
$$
The tail still gives three $P$ residual assignments, with the same exact reservation positions. The active triples contribute $2a_0$, so $P$ gets $2a_0+3=p_0-1$, and the other upper assignments total $r+2-(p_0-1)=q_0$. This verifies the reversed construction directly. The principal odd $r\ge9$ restriction ensures $r\ge11$ in this residue class. It uses new verification of the construction at reversed roles and does not change the accepted D178 theorem's stated scope.

For every admitted baseline with $p_0\le p$, $q_0\le q$ and $p-p_0\le q-q_0$, take
$$
b=(p-p_0)/2,\qquad a=((q-q_0)-(p-p_0))/2 .
$$
Both are nonnegative integers and the growth of §4 reaches the exact target. This proves sufficiency on the full principal domain. Together with §1 it gives precisely $R\ge r+3$ as claimed.

The same formulas give restricted secondary positives. At $r=7$, they cover the admissible unequal targets, and the threshold excludes lower totals. For the larger equal targets this baseline rule would use the reversed quotas $(p_0,q_0)=(6,4)$ and three regular shifts, while only two are available. That particular baseline rule does not settle them. At $r=5$, Q-only growth covers all targets with smaller quota two or four at or above threshold. For larger targets use equal baseline $(4,4)$ if its anchor has shift 0 or 1. This holds if one may select a neutral quota at least six. It also holds if there are at least two first quotas at least four: choose one as neutral, leaving a nontrivial I-a tail at $r=5$. In the non-all-two tail of [D178 §4.2](ORDINARY_SPINE_EXCEPTIONAL_ARBITRARY_EVEN_FIRST_QUOTA_LIFT.md#42-i-a), the first L position is either an ordinary deficit-four pair or begins the part with L deficits $(4,4)$, so its shift at $r=5$ is $5-4=1$ when the neutral has no extra pair. With exactly one four and all other quotas two, the unpromoted D178 I-a tail starts at deficit one, giving shift four and failing the required anchor window for the larger targets. That is a limit of these explicit formulas. Those secondary open cases require separate arguments.

## 6. Named allocation and exact inventories in the final target

Use the target's named host vertices and chosen actual exterior terminal indices throughout. The mathematical baseline prescribes arrows at the same hosts with baseline quotas. Identify these arrows with the required number of actual residual terminal indices at each parent (for instance the first such indices in the baseline arrow order). Keep their actual names when translating or moving an arrow. Assign the new arrows at $P,Q$ to their remaining actual terminal indices, in finite order. The available index counts are exactly those proved in §§3–5. Every first and exterior incidence is unchanged and the direct leaf is the actual original edge at $w$. The baseline is computed from the independent data and formulas inside the full target admission. The proof does not extract it from a previously solved target.

First compute on the baseline the numerical source set $I_0$ of all gap leaves at actual first hosts and their numerical image set $M_0$ in the corresponding difference-coordinate alphabet. In particular these are filled by the D178 assignments at the individual first parents, with each image given by adding its own $\delta$. Both contain the four fixed neutral coordinates $E_0=[0,3]$. Write $T_\lambda(D)=E_0\sqcup((D\setminus E_0)+\lambda)$ for a baseline set containing $E_0$, where $+\lambda$ shifts the set pointwise and $\lambda=2b+a$ in the balanced-plus-Q construction. For Q-only growth the final exact sets are
$$
I=T_\lambda(I_0),\qquad J_1=T_\lambda(M_0).
$$
For $b\ge1$ the L anchor is moved in the first step and follows the subsequent Q-only translation of size $a$. Thus
$$
\begin{aligned}
I&=(T_\lambda(I_0)\setminus\{4+\lambda\})\sqcup\{4+a\},\\
J_1&=(T_\lambda(M_0)\setminus\{4+\delta+\lambda\})\sqcup\{4+\delta+a\}.
\end{aligned}
$$
These formulas follow by exact unfolding: every unmodified noninitial old H coordinate becomes $J_0+2\lambda-(j+\lambda)=J_0-j+\lambda$, while the L anchor displacement and parent are unchanged. They describe the first-host sets in the larger alphabets without assigning all L sources to first hosts. The final complements are $I'=[0,s-1]\setminus I$, $J_2=[0,s-1]\setminus J_1$. Each new allocation has $x=\lambda$ lower sources at upper hosts (one per new free L source) and $y=s_0-K_0=r-2+h$ upper sources at lower hosts, with only L first-host cells moved. This agrees with
$$
1+r+R=2r+4+2\lambda=2(A+\lambda),\qquad x+y=s-K .
$$
The folded row bijections give the exact numerical bijection and crossing threshold at their final coordinates. In particular the upper-host L assignments contribute crossing weights to the remaining inventory.

In orientation the output cut is $C=c+K$. Keep the old membership-preserving shifts $A$ below $c$ and $A+s$ at or above it. Give source $i$ label $A+c+i$ and add $n+s$ to each upper reduced exterior label. The old shared vertex $v$ has label $A$ and already agrees with its reduced exterior value. The expanded lower ends of exterior edges are at most $A<C$ and the upper ends at least $n+s+A+1>C$. Every exterior difference increases by $n+s$ and is crossing. Old crossing differences increase by $s$ and old noncrossing differences are unchanged. The exact palettes are
~~~text
old labels    [A,A+c−1] ⊔ [A+c+s,n+s+A]
fresh labels  [0,A−1] ⊔ [A+c,A+c+s−1] ⊔ [n+s+A+1,m]
old weights   [1,d−2] ⊔ [d−1+s,n+s]
fresh weights [d−1,d+s−2] ⊔ [n+s+1,m].
~~~
The unions are disjoint by width and size admission. The numerical gap bijection and the reduced exterior spectra fill the indicated fresh intervals. The gap crossings use exactly $[d+K-1,d+s-2]$, and its noncrossing differences exactly $[d-1,d+K-2]$. Together the vertex-label and actual edge-difference palettes are $[0,m]$ and $[1,m]$, each bijectively. The full crossing spectrum is $[d+K-1,m]$, with noncrossing spectrum $[1,d+K-2]$. Since $w=0$ and $m=2C+2$, this is exactly the oriented $S_{-1}$ return along the original extended spine.

For the first-section boundary let $b_P,b_D$ be the actual chosen exterior indices of $P$ and the direct leaf. The first and remaining fresh exterior label sets are
$$
E_1=([1,A-1]\setminus\{t_0\})\sqcup\{n+s+A+1,n+s+A+3\},\qquad
E_2=\{0,t_0,n+s+A+2,n+s+A+b_P,n+s+A+b_D\}.
$$
Their exact differences are $n+s+[1,A]$ and $n+s+[A+1,A+5]$. With the exact old sets $L_{\rm old},D_{\rm old}$, the complete boundary resources are
~~~text
used labels         L_old ⊔ E₁ ⊔ (A+c+I)
remaining labels    E₂ ⊔ (A+c+I′)
used differences    D_old ⊔ (n+s+[1,A]) ⊔ (d−1+J₁)
remaining weights   (n+s+[A+1,A+5]) ⊔ (d−1+J₂).
~~~
For cut partitions, the old used labels are separated by the two old bands, exterior labels by their reduced sides, and gap labels by intersecting $I$ or $I'$ with the two intervals $[0,k-1],[k,s-1]$ before adding $A+c$. For crossing differences the old crossing band and both exterior bands cross. In either gap inventory the crossing portion is obtained by intersecting $J_1$ or $J_2$ with $[K,s-1]$ before adding $d-1$. The remaining portions, with indices $[0,K-1]$, are noncrossing and the used noncrossing portion includes the old band $[1,d-2]$. The literal unfinished original connector $uw$ has oriented endpoint labels $(n+s+A+1,0)$ and crossing weight $n+s+A+1$ in the remaining exterior band.

For actual maximum polarity use input $n-G$ and complement output about $m$. The cuts are then $n+1-c$ and $m+1-C$. By $2K=A+B+s$ the actual lower and upper shifts become $B,B+s$, versus $A,A+s$ in minimum polarity. Both exact label inventories complement and their sides exchange, and the exact weights and crossing statuses are invariant. The maximum output frontier is $w=m$ and the actual connector labels are $(4,m)$.

For each admitted finite sequence, keep the actual evolving cut, input state and all connector incidences with their own size and spectrum premises. For completed cut $C_i$ let $T_i,S_i$ denote the sums of later actual lower shifts and of later gap widths. All later placements preserve the old sides, so the exact final label map on this alphabet is $x\mapsto x+T_i+S_i\mathbf 1_{x\ge C_i}$. A crossing difference gains $S_i$ and a noncrossing difference stays unchanged. The same maps lift the first-section inventories and both endpoints of the literal unfinished crossing connector. Remaining resources are exact complements in the final alphabets. Induction gives all original graceful bijections at the admitted returns. Finite parameter arithmetic, finite backward sums and direct scans of the named incidences terminate and emit each final label immutably. This uses the independently supplied prefix, with arbitrarily large admitted sizes available only under the retained [D157/D134 initializer premises](ORDINARY_SPINE_ALTERNATING_EXCEPTIONAL_SPECTRUM.md#7-independent-supply-cycle-closure-and-immutable-labels).

## 7. Accepted controls and scope

D178 is Director accepted within its exact written scope at 0ca6ab2d60fbf179ea52345e05baed47e39aa9a9, including arbitrary first capacities and its separately scoped ordered-tail results. The accepted D177 symbolic projection continues to cover all 93 frozen D174 all-even $R=8$ originals, including 92 historically unentered. D174 historically completed one matched pair and two numerical arms, stopped normally at the first verified separator, and left 3,518 unentered originals. Its literal independent 74-edge prefix and actual cut were checked by direct arithmetic on frozen labels. [Custody](../evidence/validation/LCL_ORDINARY_SPINE_EXCEPTIONAL_INDEPENDENT_SECOND_QUOTA_GROWTH_001/CUSTODY.json)

D179 is a complete terminal-enabled H1 threshold on its principal domain with selectable numerical roles in the declared placement. The two constructed exteriors are sufficient for that domain. The D175 H0 obstruction and D176 complete-menu classification retain their exact old quota scopes. The stated secondary gaps, preassigned numerical role decisions and other classes are separate. The symbolic growth rules and exact baseline selection close the requested principal objective without a hybrid plan or scientific run.
