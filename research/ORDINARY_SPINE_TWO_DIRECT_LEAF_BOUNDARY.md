# D152 — Exact two-direct-leaf D143 boundary

Task `LCL-ORDINARY-SPINE-TWO-DIRECT-LEAF-BOUNDARY-001`. All counts and labels are exact integers, excluding booleans. Intervals include both endpoints and are empty when reversed. The parameters r,p,q are quotas or half-quotas and the D134 state parameter is fixed at one.

## 1. Domain and classification

Use [D143](ORDINARY_SPINE_TWO_SECTION_CUT_STATE.md) with an independently supplied named [D134](ORDINARY_SPINE_PIECEWISE_CUT_SPECTRUM_TRANSITION.md) p=1 prefix. Orient its actual extreme frontier v to zero, with n=2c+2 edges, cut c, threshold d=c+2, and exact crossing spectrum [d,n]. Append the actual ordered sections (2r+1) at u and (2p,2q,0,0) at w, for independent r,p,q≥1. There are 2r+3 vertices in the first section and 2(p+q)+5 in the second, so K=r+p+q+4 is half the number of new vertices and edges. Require n≥2K, put m=n+2K, and require the exact D143 embedding and D134 return. The cut considers vertices at the cut upper. [D149](ORDINARY_SPINE_TWO_CENTER_EVEN_QUOTA_SUPPLIER.md) excludes the terminal-free arm throughout.

**Exact result for the terminal-enabled arm.** It is feasible precisely if either r≥2 and max(p,q)≥3, or (r,p,q)=(4,2,2). This holds on the same named originals in either physical order of the second quotas and for either input polarity, subject to the stated prefix and size conditions. A proof of the reduced exterior classification is separate from the allocation proof.

## 2. Exact reduced exterior classification

In a completion the D143 widths obey A≥2, B≥1, s=2K−A−B≥K. The reduced exterior is labeled bijectively onto [0,A+B], every edge crosses after A, and its edge differences are [1,A+B]. The old v and new w have reduced labels A and 0, with u=A+1 by [D147](ORDINARY_SPINE_EXTERIOR_SUPPLY_REASSESSMENT.md). Use [D151](ORDINARY_SPINE_ONE_DIRECT_LEAF_EXTERIOR_OBSTRUCTION.md) to pin a=A−1, force actual terminals of a at upper indices b=2,…,A−1, and put both available direct leaves of w in the gap. Those leaves use sources 0 and A−1 respectively as far as source coordinates are concerned. The exterior vertices high of A are therefore u, the two second centers and terminals of a. The only other lower slots besides w,a,v are terminals of the two second centers, at j∈[1,A−2]. In particular B≥1+2+(A−2)=A+1.

Write B=A+Δ with Δ≥1. To attain reduced difference A+B the vertex at A+B must be a neighbor of w as in D147. Since w's exterior neighbors are u and the two centers, role Q is the center at A+B. Slot b=A cannot be a terminal of a because its difference to a would be A+1, already used by uw. As b=A is distinct from b=1 and B, it must be the other named center P. Thus its label is 2A. The weights of vu, ua, uw and all terminal edges at a are respectively 1, 2, A+1 and b+1 for b∈[2,B−1] minus {A}. Together these are exactly [1,B]. The remaining weights [B+1,A+B] have deficits [0,A−1] from A+B. The w attachments to Q and P contribute deficits 0 and Δ. A lower slot j contributes j+Δ if it belongs to P, and j if it belongs to Q. For the following count set D=A−1.

A valid deficit bijection needs Δ≤D. For each j∈[1,D−1], the value j is already supplied if j=Δ or if slot j−Δ previously used P. Otherwise its only possible supplier is slot j at Q. If it is already supplied, slot j must use P to avoid a duplicate. Induction from j=1 forces exactly the positive multiples of Δ among j to use P. Since deficit D has no slot D, it is supplied precisely if D=Δ or slot D−Δ is a positive multiple of Δ at P. Hence Δ divides D. Conversely, if D=LΔ, the multiples j=Δ,2Δ,…,(L−1)Δ at P give deficits 2Δ,…,LΔ, and the attachments supply 0,Δ. The nonmultiples at Q give every remaining deficit. Each is distinct and in range, proving sufficiency for the reduced spectrum. This proof includes Δ=D and A=2. At Δ=D, P has no exterior terminal and the attachment supplies D directly. At A=2 only Δ=1 is possible and the lower terminal interval is empty.

Thus for either assignment of the two actual centers to P,Q, the classification after requiring the two leaves of w in the gap is

    A≥2, Δ≥1 divides A−1, B=A+Δ, A+B≤K, s=2K−A−B
    exterior terminal counts at (a,P,Q) = (A+Δ−3, L−1, A−1−L).

These counts must fit the corresponding actual terminal quotas 2r+1,2p,2q, where p,q hereafter denote half-quotas at P,Q in role order. They are sufficient for a named reduced exterior at those widths: select that many actual terminal slots at each fixed host and assign its prescribed labels in order to those slots. For explicit constructions choose the highest terminal indices for these slots and assign their reduced labels in increasing order. The remaining terminals keep their actual names and parents. The only incidence across the old/new boundary is vu. All roles come from the original named graph. This classification neither changes physical branch order nor presumes that arbitrary gap quotas will fit.

## 3. Gap restrictions and the r=1 obstruction

The remaining quotas of (w,a,P,Q) are (2,2r+4−A−Δ,2p−L+1,2q−A+1+L). All other named vertices have zero gap quota. The lower translations at w and a are A−2 and −1. Upper host b uses i↦s+b−i. The gap sources and destinations both occupy [0,s−1], the source cut is k=K−A, and an image must be at least K exactly on an actual crossing. Summing images minus sources gives the [D144](ORDINARY_SPINE_TWO_SECTION_GAP_ALLOCATION.md) identity, where T is the sum of sources assigned to upper hosts,

    2(A−2) − (2r+4−A−Δ)
    + (s+A)(2p−L+1) + (s+B)(2q−A+1+L) = 2T.

Since s≡Δ modulo two, the left side is congruent to

    A+Δ+(A+Δ)(1−L)+A(1−A+L) ≡ ΔL ≡ A−1  (mod 2).

Here A(1−A) is even. Thus A is odd and A≥3. The sources 0 and A−1 use both leaves of w by D151. No upper host can take a source below A+1, since the smallest eligible upper index is A. Consequently sources 1,…,A−2 and A must all use a. All of these exist below k because k=B+g≥A+1 for g=s−K≥0. This requires at least A−1 leaves at a and gives 2A+Δ≤2r+5.

At r=1 the inequality forces A=3, Δ=1. The two w uses at 0,2 and the two necessary a uses at 1,3 exhaust both their quotas, and map these positions by transpositions (0,1),(2,3). On the shifted remaining interval x=i−4, whose maximum is N=s−5, the only maps are x↦N−x at P and x↦N−x+1 at Q. The first map alone has the same sum over the shifted sources as the required sum of images. Every use of Q adds one to that sum. Q has positive quota 2q, since it has zero exterior terminals at these widths. This contradicts bijectivity for every pair of positive half-quotas. It independently excludes both arms when r=1.

We also need a crossing count that applies to all widths. Let x_cross count lower sources using upper hosts and let y_cross count upper sources using lower hosts. Then x_cross+y_cross=g. The sum of the lower host quotas is k−x_cross+y_cross=B+2y_cross. Substituting the two lower quotas gives

    y_cross = r+3−B,    x_cross = p+q+1−A.

Both must be nonnegative. The two w sources are lower, and consequently a has precisely r+1 lower-source uses in any completion.

## 4. Infinite supplier at r≥2 and max(p,q)≥3

Assign the largest half-quota to P and write p≥q, with a tie resolved by giving P to the earlier physical center. Take A=3, Δ=1, B=4, so by §2 the reduced labels of v,u,w,a,P,Q are 3,4,0,2,6,7. Give one actual terminal of a reduced label 5 and one actual terminal of P reduced label 1, using the last index at each. This follows the proved exterior classification. The gap quotas at w,a,P,Q are 2,2r,2p−1,2q. Set M=r+p+q. Then s=2M+1≥K=M+4 since M≥6. The initial transpositions on [0,3] use w at 0,2 and a at 1,3, all noncrossing. Put x=i−4, let y=π(i)−4, and use N=2M−4 and R(x)=N−x. The remainder has source and destination alphabet [0,N], source split with low interval [0,M−4], and crossing image interval [M,N]. Its available maps are a:y=x−1, P:y=R(x), Q:y=R(x)+1.

Choose q_j≥0 for j=1,…,r−1 with sum q. This choice can be deterministic, for instance q_1=q and the rest zero. Use consecutive lower packets [α_j,α_j+q_j] starting at α_1=1, and put β_j=α_j+q_j−1. The last lower endpoint is q+r−1≤M−4 precisely when p≥3. The consecutive upper packets, written in t=R(x) on upper sources, are [α_j−1,β_j]. They are disjoint because the next starts at β_j+1. Their endpoints are in [0,M−1], the full reflected parameter interval of the upper sources. For each pair of packets use:

- On the low source α_j use a, giving noncrossing image α_j−1.
- On the other low packet sources [α_j+1,β_j+1] use Q. Their crossing images are R(x)+1=R(x−1), taking exactly R([α_j,β_j]).
- On upper source R(β_j) use a, giving R(β_j)−1=R(β_j+1), the remaining crossing image of the lower packet.
- On upper sources with t∈[α_j−1,β_j−1] use Q and image t+1. These fill [α_j,β_j], and the noncrossing image α_j−1 was supplied by the low a source.
- On every other shifted source use P. The unused lower sources map under R to the crossing images outside the lower packet images. The unused upper sources have identity y=t and give the noncrossing images outside the upper packet intervals.

Thus the crossing images of each packet pair are exactly R([α_j,β_j+1]), all at least M, and the noncrossing images are [α_j−1,β_j], below M. Distinctness of the packet intervals and the reflectors on their complements proves bijectivity and every actual crossing condition. At q_j=0 both Q intervals are empty and β_j=α_j−1. The two a assignments then supply the singleton images in the corresponding bands. There are r−1 new uses of a in each source side, plus the initial two, for 2r. The Q uses are q on each side, and the remaining 2p−1 shifted sources are at P. The construction includes q=1, r=2, p=3 and both physical center orders. When p=q and the quotas qualify either physical order works by the named role rule.

## 5. Exact classification at smaller second quotas

It remains to consider r≥2 with physical p,q∈{1,2}. The crossing identity x_cross=p+q+1−A together with odd A≥3 limits A to 3, or to 5 when both half-quotas equal two.

**Width A=3.** The divisor choices are Δ=1,2. The latter gives B=5 and L=1. It makes the two formulas at the upper hosts differ by two rather than one, but the initial four sources still undergo the same two transpositions. On the shifted interval, put N=s−5=2M−3−Δ, M=r+p+q. In either case P gives R(x)=N−x and Q gives R(x)+Δ. Low sources are [0,M−4], the crossing image interval is [M,N], and the upper-source parameter t=R(x) lies in [0,M−Δ]. The remaining a uses follow from §3: a had r+1 low uses and two have already gone into the initial transpositions. Write y_cross=r+3−B=r−Δ as before. Thus it has r−1 low and r−Δ upper uses after removal. Use lower a source set S and upper a parameter set T_a. At any upper a source the actual crossing image is R(t+1) and at a low a source the noncrossing image is x−1.

For a clean sum computation set m_0=M−4 and h=N−y for crossing images. Those h values run through [0,m_0+1−Δ], and the low source interval is [0,m_0]. Low P contributes h=x and low Q contributes h=x−Δ, while upper a supplies h=t+1. Noncrossing images have required interval [0,M−1]; upper P contributes t, upper Q t+Δ and low a contributes x−1. Let X_Q and Y_Q count low and upper Q uses. Taking the two sums gives
```
Δ X_Q = sum[0,m_0] − sum[0,m_0+1−Δ] − sum S + sum_{t in T_a}(t+1),
Δ Y_Q = sum[0,M−1] − sum[0,M−Δ] − sum S + |S| + sum T_a.
```
For Δ=1 the interval corrections are zero, |S|=|T_a|=r−1, and X_Q=Y_Q=q because Q's total is 2q. For Δ=2 the first correction is m_0, the second is M−1, and |S|=r−1, |T_a|=r−2. Thus 2(Y_Q−X_Q)=(M−1)−m_0+|S|−|T_a|=4, giving Y_Q−X_Q=2. But at Δ=2, L=1 and Q's total quota is 2q−1, odd. This is incompatible with the even difference. This excludes Δ=2 at A=3 for all r,p,q. At Δ=1, the remaining number of low P uses is (M−3)−(r−1)−q=p−2. The shifted low source zero exists for r≥2 and p,q≥1. It must use P: a underflows and Q has h=−1 outside the crossing interval. Hence p≥3 in numerical role order, impossible in this residual stratum.

**Width A=5.** Here p=q=2 and x_cross=0. All low sources except 0 and 4 go to a, and the two w sources give images 3 and 7. Thus the used lower-source images are [0,k−2] together with 7. If k≥9 then a repeats 7 and the allocation fails. When g>0 the upper sources k,…,K all exist. None can use a because its image is i−1<K. The w quota is exhausted, so these A+1=6 sources would need upper hosts. Their combined quota is A+2x_cross=5. This is impossible. Therefore g=0, B=k=5+Δ, K=s=10+Δ and r=2+Δ. The possibilities Δ=1,2,4 follow from §2. The last has k=9 and was excluded by collision.

At g=0 every upper source uses P or Q. Write t=s+A−i, which varies over [6,10] in reverse as i increases from k to s−1. Their image maps are t and t+Δ. The remaining image set is [k−1,K−1] minus {7}. At Δ=1 that set includes 5, below the smallest possible upper image 6. At Δ=2, the set is {6,8,9,10,11}. In the interval [6,10] give Q the positions t=7,9, shifting their images to 9,11, and give P the other three positions, which then give 6,8,10 unchanged. These are exactly the missing images and all are noncrossing. The exterior has Δ=2, L=2, so Q's residual quota is two and P's three, exactly supplied. The low-source uses are w at 0,4, and a at the other five low sources. Their images complete the same noncrossing range without a repeat. This is the single residual solution, at (r,p,q)=(4,2,2). It uses the exact same exterior formula of §2 with A=5, B=7. Its gap has s=K, so it needs no crossing gap weight. This direct boundary argument checks all allowed parameters without a solver or enumeration of labelings.

## 6. Named reconstruction, inventories and composition

In either positive rule, assign each remaining named terminal or direct leaf its gap label A+c+i in increasing i within its actual host list, preserving the given order of available names. Reserve the exterior indices by §2 and give the reduced labels as there. This yields an original vertex bijection on the gap and exterior using exactly the two physical quotas at the two second centers. The same parent incidences occur before and after assigning numerical roles, including the exceptional equal-quota case.

For an oriented old label G(v_old) use F(v_old)=G(v_old)+A+s·1_{G(v_old)≥c}. The exact old label and difference inventories are
```
L_old = [A,A+c−1] ⊔ [A+c+s,A+n+s]
D_old = [1,d−1] ⊔ [d+s,n+s].
```
Expand each upper reduced label by n+s and leave lower labels fixed. The fresh exterior labels are E=[0,A−1]⊔[A+n+s+1,m], and exterior incidences including vu have differences [n+s+1,m], all crossing. The gap labels are [A+c,A+c+s−1] and their actual weights are d+π(i) by subtraction at the named host. Thus they exactly supply [d,d+s−1]. These complementary resources give the full label and weight bijections. At C=c+K the old membership is preserved by 0≤k≤s. All old crossing weights gain s. The gap crossings supply [d+K,d+s−1], so the full crossing spectrum is [d+K,m] and the noncrossing spectrum is [1,d+K−1]. The output has w oriented at zero, m=2C+2 and threshold d+K=C+2, the exact D134 p=1 return.

For the first-section boundary put V_a=[2,B−1] minus {A}, the exterior upper indices of terminals at a. Let E₁ consist of A−1 and n+s+A+b for b∈{1}∪V_a. It accounts for a, u and those actual exterior terminals. Its exterior incidences including vu have weights D₁=n+s+([1,B] minus {A+1}). The gap source and image sets belonging to a are as follows.

| Rule | Source set I₁ | Image set J₁ |
|---|---|---|
| A=3 packets | {1,3} ⊔ (4+{α_j,R(β_j) over j}) | {0,2} ⊔ (4+{α_j−1,R(β_j+1) over j}) |
| A=5 residual | [1,k−1] minus {A−1} | [0,k−2] minus {A−2} |

The exact used labels are L_old⊔E₁⊔(A+c+I₁), and the remaining labels are (E minus E₁)⊔(A+c+([0,s−1] minus I₁)). The exact used weights are D_old⊔D₁⊔(d+J₁), with remaining weights ([n+s+1,m] minus D₁)⊔(d+([0,s−1] minus J₁)). The crossings already used are [d+s,n+s]⊔D₁⊔(d+(J₁∩[K,s−1])), and the other used weights are noncrossing. These inventories are established independently of emitting the second section. The actual first frontier u carries n+s+A+1. The sole unfinished incidence here is uw, of that weight when w is placed at zero.

For an actual minimum input emit the oriented labels as written. For an actual maximum input use G=n−g_old and emit m−F, with actual cuts n+1−c and m+1−C. The two side translations on actual low and high labels are B and B+s in this polarity, and A and A+s in minimum polarity. Hence actual memberships and weights are preserved with the stated crossing shifts. The actual first frontier in the maximum case is B−1 and the partially used label set is complemented about m. This does not impose an intermediate normalized state.

The D134 independent p=1 initializer supplies arbitrarily large states using the supplied seed and its actual declared initialization sections. For any admitted finite block list, size increases by 2K and the oriented cut and threshold by K each time, retaining the same polarity. The largest required 2K suffices as an initial size bound. Induction gives finite closure for either or mixed positive constructions. At any completed boundary j with actual cut C_j, let L_j sum the remaining actual lower shifts and S_j the remaining gap widths. Future membership preservation gives each boundary label z final value z+L_j+S_j·1_{z≥C_j}; each current edge gains S_j if crossing. At the first-section boundary use the cut and reservations for its current full block, and the later suffix sums. Injectivity supplies both final-alphabet complementary inventories and the actual connector weight. The suffix sums take a backwards pass. The fixed interval and reflection rules can be evaluated once per source with advancing packet endpoints and per-host named counters. This terminates and uses linear indexed integer operations in the supplied original size and the total appended named size. This operation statement separates integer operations from bit complexity.

## 7. Controls and preparation disposition

The retained n=54 D134 prefix has actual maximum frontier s:25, oriented cut c=26 and exact weights [28,54] crossing. The saved prefix was verified against its named incidences and exact graceful spectra. At r+p+q≤23 one has 2K≤54. For the proposed residual finite stratum, each ordered (p,q) in {1,2}² has r ranging from 2 through 23−p−q. The respective counts 20,19,19,18 sum to 76. The symbolic proof gives one terminal-enabled and 75 impossible ordered profiles, and D149 excludes the terminal-free arm on all 76. Neither profile order was quotiented.

The frozen original-bound D148 controls target-0032, -0035, -0044 and -0047 have r=1 and respectively ordered second-center half-quotas (1,1),(1,2),(2,1),(2,2). All eight historical arm bindings verified with the saved T and E negatives. These are retained controls and agree with the all-parameter r=1 exclusion. The smallest infinite-supplier positive is r=2 and numerical (p,q)=(3,1), with either physical order. It is a symbolic control. D149 and the Director-accepted [D150](ORDINARY_SPINE_TWO_TO_ONE_TERMINAL_SUPPLIER.md) retain their separate positive and separating comparators with different physical profiles.

**RESOLVED SYMBOLICALLY BEFORE NUMERICAL EXECUTION.** The entire stated existence question is decided, including the residual for every r. No hybrid corpus, algorithm, execution configuration, preflight or arm disposition was needed. This is a scoped result within the D143 embedding and D134 return, and leaves other shapes and ordinary embeddings open. D148's capped historical run and 12 undecided pairs remain unchanged.
