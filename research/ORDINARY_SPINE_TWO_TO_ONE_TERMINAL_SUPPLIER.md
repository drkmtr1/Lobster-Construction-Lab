# D150 — Two-to-one exterior terminals and exact terminal-free scope

Task `LCL-ORDINARY-SPINE-TWO-TO-ONE-TERMINAL-SUPPLIER-001`. All parameters and labels are exact integers, excluding booleans. Intervals are inclusive and reversed intervals are empty. The symbol ⊔ denotes disjoint union. The half-quotas are separate from the D134 state parameter, which is 1.

## 1. Original, input and result

Supply an independently constructed named ordinary graceful [D134](ORDINARY_SPINE_PIECEWISE_CUT_SPECTRUM_TRANSITION.md) p=1 prefix with n edges and actual extreme spine frontier v. In the orientation G(v)=0 its recorded cut c satisfies n=2c+2, threshold d=c+2, and actual crossing spectrum [d,n]. A label at the cut belongs to the upper side. Prescribe the actual next spine vertices u,w and ordered sections (4) at u and (2p,2q,0,0,0) at w. They add 6 and 2(p+q)+6 vertices respectively. The first section has one center a with four indexed terminals. The second has two indexed centers and three actual direct leaves of w. The added edge count equals the added vertex count. Put M=p+q, H=2K=2M+12, K=M+6 and m=n+2K. Require n≥2K and independent p,q≥1.

For choosing numerical center roles only, name the actual center with greater half-quota P and the other Q, resolving a tie in favor of P at the earlier index. In the formulas below write p≥q for their **role-ordered** half-quotas. The input physical order remains arbitrary. This merely assigns formulas to the selected named centers. The two attachments to w and every indexed terminal-to-parent incidence stay at their physical endpoints.

**Result.** A terminal-enabled [D143](ORDINARY_SPINE_TWO_SECTION_CUT_STATE.md) completion exists for every admitted ordered pair. Within the same original and input domain, a terminal-free D143 completion exists exactly when max(p,q)≥2. Thus only the half-quota pair (1,1) is E-only in this family. The result includes both actual polarities and an exact D134 return. The obstruction concerns the D143 terminal-free class.

## 2. Two-to-one exterior

For the terminal-enabled construction set A=3, B=5, s=2K−A−B=2M+4 and k=K−A=M+3. Then s−K=M−2≥0. Give the named reduced exterior the following labels and actual edge weights.

| Actual edge | Reduced endpoint labels | Reduced weight |
|---|---|---:|
| vu | 3,4 | 1 |
| ua | 4,2 | 2 |
| a to its penultimate indexed terminal | 2,5 | 3 |
| uw | 4,0 | 4 |
| a to its last indexed terminal | 2,7 | 5 |
| wP | 0,6 | 6 |
| Q to its last indexed terminal | 8,1 | 7 |
| wQ | 0,8 | 8 |

The endpoints use every reduced label in [0,8] exactly once per vertex, and the displayed weights use [1,8] once. Every edge crosses the reduced cut after 3. All entries are actual original incidences. Two terminals of a and one of Q are selected into the exterior. For comparison the [D147](ORDINARY_SPINE_EXTERIOR_SUPPLY_REASSESSMENT.md) terminal-free arithmetic reference has the weights 3,5,7 at the incidences to lower slot 1 and upper slots 5,7 respectively, from u=4 or w=0 as appropriate. In the actual exterior those slots contribute respectively 7,3,5 via their actual parents. This cycles those three differences, leaving 1,2,4,6,8 fixed. The comparison does not change the actual graph. The D147 weighted terminal balance also reads 2+2=5−1.

The actual gap quotas at w,a,P,Q are (3,2,2p,2q−1). Other exterior vertices have zero gap quota. At i=0,2 assign w, and at i=1,3 assign a. Their translations +1 and −1 give the two transpositions (0,1) and (2,3). Both hosts and all four sources are low, and the images are noncrossing because k≥5 and K≥8.

## 3. Terminal-enabled parity chains

For the remaining sources and images set x=i−4 and y=π(i)−4. Their common alphabet is [0,N], N=2M−1. By D143 the three remaining physical host maps in these coordinates are

    w: y=x+1,    P: y=N−x,    Q: y=N+2−x.

The actual low source interval is [0,M−2] and the upper source interval is [M−1,N]. A crossing image is y≥M+2. This crossing interval can be empty. Put z=p−q=M−2q, so 0≤z≤M−2.

Define R(x)=N−x. In the low interval assign x=z to w with image z+1. Give Q the progression z+2,z+4,…,M−2 and use P on the other low sources. The progression has q−1 entries since M−2−z=2q−2. Relative to the reference images R([0,M−2])=[M+1,N], Q replaces R(x) by R(x−2). It fills in series the omitted image R(z) and each intermediate displaced image, leaving out exactly R(M−2)=M+1. Equivalently, the inputs to R that come from P and Q together are [0,M−2] minus {M−2}, each once. This remains true when q=1, since then z=M−2 and the progression is empty. Their images are [M+2,N], all crossing from low to the two high hosts. The w image is z+1≤M−1, noncrossing at a low host.

On the upper interval use t=R(x), a bijection onto [0,M]. Give Q the progression z+1,z+3,…,M−1 and use P otherwise. Its length is q because M−1−(z+1)=2q−2. On those t values Q sends t to t+2. It replaces that progression by z+3,z+5,…,M+1, while P fixes the other t values. The upper sources thus produce all of [0,M+1] except z+1, each once. Every image is noncrossing because both upper hosts are high and M+1 is below the crossing threshold. The endpoints are in [0,N] because M≥2. Joining the w image z+1 and the upper images with the low high-host images supplies the entire alphabet [0,N] bijectively, with all actual crossing predicates satisfied.

After restoring the initial four coordinates, w has 3 leaves and a has 2. Q has (q−1)+q=2q−1 leaves. P has (M−2−(q−1))+(M+1−q)=2p leaves. At q=1 the sole upper Q use is t=M−1 and the low Q progression is empty. At p=q one has z=0, so w takes the first shifted source. If q≥2, the first lower Q source is x=2 and fills the vacated reference image R(0). The upper progression starts at t=1. At p=q=1 the entire low interval is the single w source, the crossing interval is empty, and the same upper image partition fills the remaining noncrossing images. These cases use the same rules without an overlap or a missing source.

Give each gap coordinate i the full label A+c+i at the indicated host. In each remaining named host list assign its labels in increasing source-coordinate order to its available terminal or direct-leaf indices in their given order. The exterior selected the last two terminals at a and the last at Q, leaving the remaining physical slots exactly available. The counts therefore label each original leaf at its actual parent exactly once. Assigning that rule to the physical host with the selected half-quota preserves order even when the larger quota is at the second center.

## 4. Terminal-free D143 classification

### Forced exterior and necessary host quota

In a terminal-free completion the D143 exterior contains all centers and both spine vertices. Its edges cross the reduced cut. Consequently the low fresh vertices are w and a, as u has no direct leaves and all exterior second-section attachments are upper. Hence A=2. If e of the three direct leaves at w are exterior, B=3+e. By D147 the reduced first spine label is u=A+1=3, since the unique crossing edge of reduced difference one must use v's sole exterior incidence vu. At A=2 the two low hosts w and a have translations 0 and −1, and u has no gap leaves. No eligible upper host admits i∈[0,2], since its index b≥2 requires i≥b+1 for its image to fit. These first three coordinates are low because s≥K and k=K−2, with K=M+6≥8. Source zero must therefore use w. At sources one and two the a option repeats the preceding image used by w. All three direct leaves of w are thus in the gap. This forces e=0 and B=3.

Write the terminal-free parameters as k=K−2=M+4, s=2k−1. The exact reduced exterior has v=2,u=3,w=0,a=1 and second centers at labels 4,5, with respective indices b=2,3. The actual edges vu,ua,uw and the two center attachments use [1,5] once and cross. The choice of which named center has which of 4 and 5 is free up to its physical quotas.

At upper sources i=k,k+1,k+2 the a images i−1 are all below K=k+2 even though a is low, and w has already used its quota. At b=3 the image at k is k+2, invalid for its upper-to-upper parent incidence. Thus i=k uses b=2 with image k+1. At i=k+1 the b=3 image would repeat k+1, forcing b=2 with image k. At i=k+2 the b=3 image would repeat k, again forcing b=2 with image k−1. All these sources exist since k≥6. This independently proves the proposed triple forcing. In addition i=3 must use b=2 because a repeats image 2 and b=3 would overflow. Thus that actual center must have at least four terminals. For the stated even quotas the triple alone already excludes both centers having quota two. This proves necessity of max(p,q)≥2 within this family and excludes the target-0188 original symbolically. D149's odd-first parity obstruction has a different premise.

### Symbolic terminal-free completions at every larger pair

Here assume p≥q≥1 and p≥2 and give P the b=2 role and Q the b=3 role. This preserves the original physical order by the named role convention in §1. Give the first three sources 0,1,2 to w as fixed points. Let J=2k+1; the high-host image maps for P and Q are J−i and J+1−i respectively. Set

    α₁=4,       α₂=q+5,
    β₁=q+3,     β₂=q+4.

The α values are distinct elements of [3,k−1]. The β values are distinct elements of [3,k−2], since k−2=p+q+2≥q+4. Give a the low sources α₁,α₂ and the upper sources J−β₁,J−β₂. The low sources give noncrossing images 3,q+4. The upper sources are at least k+3 and give crossing images J−(β₁+1),J−(β₂+1). They fit in the alphabet and are distinct.

For low sources i∈[3,k−1] other than α₁,α₂, use Q on [5,q+4] and P otherwise. This Q interval is contained in the low sources and avoids the two a sources. To see the image partition write h=J−π(i) for a crossing image. P gives h=i and Q gives h=i−1. The Q interval therefore sends [5,q+4] to [4,q+3], exactly shifting the missing position from 4 to q+4. The P identities retain every other low position except q+5. The two high a sources fill both remaining h positions q+4,q+5. Hence h ranges over [3,k−1] exactly once and the crossing images are precisely [K,s−1].

For upper sources use t=J−i∈[3,k+1]. The two a sources have t=β₁,β₂. Use Q at t∈[3,q+2] and P on the other non-a sources. Q shifts this interval to [4,q+3] and P fixes all other available t. Together these images fill [3,k+1] except 3,q+4, which are supplied by the low a sources. The resulting [3,k+1] is noncrossing, since its upper limit is K−1, all reflected sources in this step are upper at a high host, and the two a sources here were low. With w's fixed images [0,2], the entire noncrossing coordinate interval is filled.

The rules assign all sources once. Each Q interval has length q, for quota 2q, and a and w have quotas four and three. The remaining sources supply 2p at P because s=2M+7 in this terminal-free placement. The intervals stay valid at p=2 or q=1. All leaves, including the three direct leaves of w, receive their gap labels in increasing source-coordinate order within their actual named host lists, as in §3. No terminal occupies the exterior. The checked reduced spectrum and proved permutation with its actual crossings meet both tests of D143 §3, so this gives a terminal-free completion and exact same-polarity return for every larger ordered pair. This proves the stated **exact** terminal-free scope without numerical feasibility evaluation.

## 5. Full and intermediate inventories, polarities

Use the D143 embedding on old labels, with the particular A,B,s of the chosen construction. At the cut c the old maps are shifts A and A+s. Put C=c+K as the new oriented cut. The exact used old sets are

    L_old = [A,A+c−1] ⊔ [A+c+s,A+n+s]
    D_old = [1,d−1] ⊔ [d+s,n+s].

The first weight band is unchanged and the second follows by adding s to every actual old crossing. Expand the exterior high reduced labels and edge weights by n+s, keeping the low labels. The fresh exterior label set is E=[0,A−1]⊔[A+n+s+1,m], and its weight set, including vu, is [n+s+1,m]. All of those edges cross. The proved gap permutation puts the gap labels in A+c+[0,s−1] and, by subtraction from the actual host, gives precisely [d,d+s−1]. These are the exact unused intervals after the old and exterior assignments. Thus all named labels and actual edge differences are bijections on [0,m] and [1,m]. Old membership is preserved since the gap cut k=K−A has 0≤k≤s. The exact crossing spectrum is the disjoint union of [d+K,d+s−1], [d+s,n+s] and [n+s+1,m]. The exact noncrossing spectrum is [1,d+K−1]. The oriented frontier w has label zero, m=2C+2 and the new threshold is d+K=C+2. This returns the exact D134 p=1 interface.

The first section's reservations are computed before emitting the second section. Use E₁ for its expanded exterior vertices' labels, D₁ for its exterior edge differences including vu, and I₁,J₁ for its gap sources and images.

| Construction | E₁ | D₁ | I₁ | J₁ |
|---|---|---|---|---|
| Terminal-enabled | {2,n+s+4,n+s+5,n+s+7} | n+s+{1,2,3,5} | {1,3} | {0,2} |
| Terminal-free, when admitted | {1,n+s+3} | n+s+{1,2} | {α₁,α₂,J−β₁,J−β₂} | {3,q+4,J−(β₁+1),J−(β₂+1)} |

In the terminal-free row all four gap labels belong to a. In the terminal-enabled row only the two indicated gap leaves at a belong to the first section. In both rows all the other coordinates belong to the second section. The exact used and remaining inventories in the declared output alphabet are

    used labels        L_old ⊔ E₁ ⊔ (A+c+I₁)
    remaining labels   (E minus E₁) ⊔ (A+c+([0,s−1] minus I₁))
    used weights       D_old ⊔ D₁ ⊔ (d+J₁)
    remaining weights  ([n+s+1,m] minus D₁) ⊔ (d+([0,s−1] minus J₁)).

The used crossing weights are [d+s,n+s] ⊔ D₁ ⊔ (d+(J₁∩[K,s−1])). The last term is empty for the terminal-enabled row and consists of the two high a weights for the terminal-free row. The other used weights are noncrossing. The only unfinished original edge at the first-section boundary is uw. In the respective rows the oriented physical frontier u carries n+s+4 or n+s+3 and its connector to w=0 will have that weight. These data and both remaining sets follow directly from the declarations and explicit formulas before the second section is emitted.

For actual minimum input use the oriented labels. For actual maximum input first orient the given labels by n−g and return the complement m−F of the displayed labels. Then the actual cuts are n+1−c and m+1−C. The complements exchange sides at each cut and preserve actual old membership from input to output. The respective old shifts below and above the actual cut are A,A+s for minimum polarity and B,B+s for maximum polarity. All weights and actual crossing incidences are preserved by complementation. The actual first-section frontier becomes 4 in the terminal-enabled row or 2 in the terminal-free row under maximum polarity. Its inventories follow by complementing vertex labels about m and retaining weights. Its intermediate alphabet is the declared full alphabet and no normalized intermediate state is assumed.

## 6. Independence, composition and termination

The exterior and the gap formulas use only the fixed physical topology and declared quotas, so do not depend on a whole-target witness. D134's independent p=1 initializer can supply arbitrary large admitted sizes from a supplied maximum-frontier seed, its named path and actual branched section. Keep these in the original target. Complement if the opposite input polarity is prescribed. For any finite declared list of the proved blocks require n≥2K at each entry, and require max(p,q)≥2 for any block opting for the terminal-free rule. An independently supplied initial n at least the largest 2K in a finite list suffices. At each step the output increases n by 2K and c,d by K in its orientation, with unchanged actual polarity. Induction proves admitted closure for either rule or a mixed list.

For immutable labels write C_j for the actual cut at boundary j, L_j for the sum of actual lower shifts in later blocks, and S_j for the sum of their later gaps. The final image of a boundary label x is x+L_j+S_j·1_{x≥C_j}. Because actual cut membership persists under every extension, the composition never changes which of those later shifts a particular vertex receives. Every boundary weight gains S_j exactly when its incidence crosses. The same formulas apply to first-section labels and to its exact crossing and noncrossing sets in §5 using the cut of the current completed block. The images of the used sets remain injective, and the final unused sets are their exact complements in the two final alphabets. In particular the unfinished connector retains its actual endpoints and its final difference follows from their actual sides. Each named vertex can be emitted once at its final label. All coordinate rules are closed interval and parity tests with a constant number of indexed integer operations per source and simple per-host counters. Precompute the suffix shifts in one backwards pass. The full emission is linear in the supplied original vertices and the finite added list in indexed arithmetic operations. The construction terminates and makes no numerical search, transfer evaluation or bit-complexity claim.

## 7. Retained control and limits

The saved [target-0188](../evidence/runs/d148-matched-exterior-001/witnesses/target-0188.json) has the actual frontier and two spine vertices s:25,s:26,s:27; its first center is b:26:0, second centers b:27:0 and b:27:1, and direct leaves b:27:2 through b:27:4. Its graph digest identifies the named original, and its witness file hash binds the saved record. Both remain distinct from any certificate ledger identity. D148's saved T negative is independently exhausted and its saved E positive passed the original-target check. Those audit records are retained as provenance. The symbolic obstruction above proves the same scoped T exclusion independently.

In the terminal-enabled rule, equal quotas select P=b:27:0 and Q=b:27:1. The saved reduced labels at the exterior parents, two last terminals of a, and last terminal of Q are exactly those in §2. The archived first four gap rows use the two stated transpositions. In the remaining saved rows the sole low shifted source uses w, and on the upper rows the Q row is t=M−1 with the P rows giving the other t values. These are pointwise matches with the p=q=1 formulas. The archive also assigns the remaining leaf indices in increasing source order at each named host. Its use of the same frozen old prefix, A,B,s, and maximum-polarity complement gives the same labeling pointwise. This comparison reads the saved rows and checks the symbolic special-case formulas without creating a new numerical original or replaying its labeling. Full parameter coverage derives from the interval proofs and the physical role convention, not from this archived equality.

This result classifies terminal-free feasibility for the exact stated profiles and input domain within D143. It does not classify other first-center quotas, direct-leaf counts, embeddings, or ordinary gracefulness outside D143. D149 retains its exact distinct scope. D148 remains capped with 12 two-center pairs undecided, and its accepted finite records are unchanged. General independent exterior supply and the behavior of the forced exterior at variable first-center quota remain open.
