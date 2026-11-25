# D141 — Boundary-block spectral obstruction in the canonical exterior placement

## Exact scope and four actual incidence classes

Use a named ordinary graceful [D134](ORDINARY_SPINE_PIECEWISE_CUT_SPECTRUM_TRANSITION.md) prefix with even edge count n, ordered witnessing spine, actual extreme frontier and an oriented label function with that frontier at zero. Its designated cut is c=n/2−p for an exact integer p≥1, and the actual crossing spectrum is [d,n] with d=n/2+1. The noncrossing spectrum is [1,d−1]. Let 1≤a<c and let M=[a,c−1] have length k=c−a≥1. Append the actual spine vertex w, h≥3 named physical centers at w and their positive named terminal quotas totaling Q. Let H=h+Q+1=2K, m=n+H, with n≥H. Require t and Q−t both positive. All parameters and labels are exact integers, and booleans are excluded. All intervals are integer intervals, empty when their upper endpoint is below their lower endpoint.

The old oriented map E translates the lower outer band [0,a−1] by h, the exceptional band M by h+t and the upper outer band [c,n] by h+Q. Reserve exterior widths A=h and B=1. Give w label m and the actual centers labels [0,h−1] in any numerical role order. Require all terminal labels in the two internal gaps. The returned state has exact D134 parameter p'≥1, extreme frontier, an exact designated half-spectrum, and preservation of actual old designated-cut membership. This proof concerns only this class.

For each actual old edge, retain its endpoints and its canonical original weight. Let W00 be the weights with endpoints in the same band, P the weights from lower outer to M, R the weights from M to upper outer, and W11 the weights from lower outer to upper outer. Every old edge is in exactly one class. The old injective weight inventory identifies each weight with its unique old incidence. P is noncrossing at c, and R and W11 are crossing, so
```
W00 ⊔ P = [1,d−1],    R ⊔ W11 = [d,n].
```
The old map is strictly increasing. Subtracting its values at the two actual endpoints gives the translated classes W00, P+t, R+Q−t, W11+Q, respectively. Their internal injectivity follows from that of the original weights. By [D139's](ORDINARY_SPINE_TWO_CUT_BOUNDARY_LEAF_BRIDGE.md#general-two-cut-resource-identities) criterion, injectivity of the old image holds exactly when these four sets are pairwise disjoint. The fresh difference inventory is
```
[1,m] minus (W00 ∪ (P+t) ∪ (R+Q−t) ∪ (W11+Q)).
```
This is a resource complement in the injective case. In a collision case the repeated old incidence already excludes graceful completion.

The translated old label bands are
```
[h,h+a−1], [h+a+t,h+c+t−1], [h+c+Q,h+n+Q].
```
Their exact complement in [0,m] consists of [0,h−1], the two gaps
```
[h+a,h+a+t−1], [h+c+t,h+c+Q−1],
```
and {m}. The gaps have positive lengths t and Q−t, separated by the nonempty moved block. Both lie in [h+1,m−1] because a≥1, c≤n and m=n+h+Q+1. All fresh terminal edges therefore have weight between a+1 and h+c+Q−1, obtained by subtracting a host in [0,h−1] from its actual gap label. The inherited frontier zero is below a and maps to h. Its actual connector vw has weight m−h=n+Q+1, and w's h attachments have the distinct weights [m−h+1,m]. These edges exhaust [n+Q+1,m] exactly, independently of the numerical role assignment.

## Maximum exceptional crossing weight

Assume a successful output and R nonempty. Set r=max R. Since R⊆[d,n], the required weight r+Q belongs to [d+Q,n+Q], a subinterval of [1,m]. Its own original incidence has moved to r+Q−t. The only potential alternative supplies are as follows.

- Every unchanged weight in W00 is at most d−1.
- Every weight in P+t is at most d−1+t<d+Q.
- Every weight in R+Q−t is at most r+Q−t<r+Q.
- A weight of W11+Q equal to r+Q would have original weight r, already belonging to a different, unique incidence in R.
- The connector and attachments begin at n+Q+1, strictly above r+Q even at r=n.

The weight r+Q must therefore occur on an actual fresh terminal. Its upper bound gives r+Q≤h+c+Q−1, or r≤h+c−1. Thus every actual exceptional crossing weight must satisfy
```
R ⊆ [d,h+c−1].
```
If R is empty the same containment holds. Equality at the terminal upper endpoint is permitted by this necessary bound. No sufficiency is inferred.

## Actual crossing count and general capacity

The oriented old frontier is zero and w is at m before output reorientation, so the returned zero-frontier orientation complements the new labels. For the exact D134 p' return the oriented cut is c'=m/2−p', so the designated pre-complement cut is C=m+1−c'=m/2+p'+1. The old image keeps its original cut membership. There is an actual old low vertex of placed label h below C, so all new centers are below C. The actual old high vertices number n−c+1. There are m−C+1 output labels at or above C. Hence the number of fresh vertices there is
```
(m−C+1)−(n−c+1) = K−p−p'−1.
```
These are w and the fresh terminals whose labels lie on the upper side. Each such terminal contributes one crossing to its named center below C. The actual connector crosses and so do the h attachments, with leaves and attachment edges distinct. The new crossing count is therefore h+K−p−p'−1. The old count is n−d+1=n/2 and is unchanged. The new spectrum begins at m/2+1 and hence has m/2 crossing edges. Subtracting the inherited count forces the fresh count to equal K. This proves
```
h=p+p'+1.
```
This argument uses the actual named connector, attachments and terminal incidences, irrespective of the internal block shifts. Combining with the maximum-weight condition gives h+c−1=d+p'−1, so
```
R ⊆ [d,d+p'−1],   |R| ≤ p'.
```
The weight bound constrains the old named incidences in R, not only their count.

## Minimum exceptional noncrossing weight

Suppose P is nonempty and set q=min P. In the original [1,d−1] noncrossing spectrum the unique incidence of weight q lies in P, so W00 cannot supply q. Every member of P+t is at least q+t>q. In a successful output the retained old crossings are still designated crossings and have weights at least m/2+1=d+K>q, ruling out both R+Q−t and W11+Q. The connector and attachments begin at n+Q+1>q. Consequently a fresh terminal must supply q, requiring q≥a+1. In particular any actual incidence in P of weight at most a excludes this placement and return.

If P is empty, all old noncrossing weights [1,d−1] remain in W00. The first gap is nonempty by t>0. When h+a<d, its smallest label h+a must belong to an actual terminal. Its weight is positive and at most h+a because its host label is nonnegative. It would repeat an unchanged noncrossing weight. This second obstruction uses the fixed exterior placement with only gap terminals.

## Singleton rigidity at p=p'=1

The crossing compatibility gives h=3. Take k=1, so a=c−1 and the single exceptional vertex carries c−1. Every incidence in P would then have weight at most c−1=a, contradicting the minimum condition. Hence P is empty. No edge can lie within the singleton. The input is a nontrivial tree, so this vertex has at least one incident edge and all its incidences belong to R. The crossing bound gives R⊆{d}, and the graceful weights are distinct. Therefore that actual vertex has degree one and its unique actual incidence has weight d. The neighbor is in the upper outer band and has label (c−1)+d=n−1. This proves the degree-one and exact incidence necessity behind D139's exceptional vertex. When the vertex is an off-spine terminal, the neighbor is its named host. The argument itself does not classify whether this degree-one vertex belongs to the chosen spine.

## Leaf strips on the repeatable D140 and preparatory outputs

For any [D140](ORDINARY_SPINE_TWO_CUT_EXACT_QUOTA_CLASSIFICATION.md) admitted triple (2t0+z,2b,z) the old extension total is Q0=2(t0+b+z)≥8. Write K0=(Q0+4)/2, so Q0−K0=(Q0−4)/2≥2. Let c_in denote its input cut and m0 its output size. In the placement before reorientation its cut is C0=3+c_in+K0. The deleted terminal source coordinate t0−1 is strictly below K0 by the required hole condition. Thus all actual placement labels in
```
[C0,3+c_in+Q0−1]
```
belong to its actual fresh crossing terminals, since their centers are low. There is no old high vertex in this interval because the old high band starts at 3+c_in+Q0. Orientation with new frontier zero maps this interval onto
```
[m0−(3+c_in+Q0−1), m0−C0].
```
The top label is c−1 in the new state, where c=m0+1−C0. Hence this gives its exact highest Q0−K0 low labels. Each belongs to a fresh named degree-one terminal, with its unique actual crossing incidence and distinct weight guaranteed by D140's allocation. This is a physical consequence of its label data and holds for each admitted indexed allocation.

The independently supplied D139 preparatory section instead uses the canonical D137 placement and Q0=8, K0=6. Its contiguous placement terminal coordinates 6 and 7 give exactly [C0,3+c_in+Q0−1] above the same cut. The reversal gives the same two highest low labels, with two distinct actual crossing terminal incidences. This conclusion uses the actual prescribed preparation, with no numerical construction.

Consider any next exceptional block [a,c−1] of length k≥2 for a p'=1 return on either of these p=1 families. It includes the two highest low labels. Each of their actual edges belongs to R because its host is an upper old vertex at the designated cut. They are distinct edges and weights, contradicting |R|≤1. With k=1 these conclusions do not exclude the retained positive singleton constructions.

More generally, assume the top L low labels of an incoming state are actual degree-one crossing terminals with distinct incidences and L>p'. Any exceptional block containing a non-leaf must include all L of these labels, since it ends at c−1 and must extend below this entire strip. Their actual crossing incidences then give |R|≥L, impossible. This conditional argument does not supply such a strip on any other state.

## Independently supplied non-leaf adverse family

Use the first returned p=1 state of [D134's independent initializer](ORDINARY_SPINE_PIECEWISE_CUT_SPECTRUM_TRANSITION.md#independent-symbolic-initialization-for-every-fixed-odd-h), before D139's preparatory section. Its initial maximum-frontier seed is independently supplied, and may be a retained D105 or D130 seed of size n0. Let gamma be D134's initializer parameter c0. Choose gamma arbitrarily large in its required parity class, with gamma≥n0+1 and all inherited conditions. The preliminary alternating path has size parameter N=3gamma,
```
T=(3gamma+1−n0)/2 ≥ gamma+1,
K_path=N−n0=2T−1.
```
Its labels from the new endpoint are j at positions 2j and N−j at positions 2j+1, ending at the translated original frontier at position 2T−1. The translated seed labels are [T,n0+T]. The chosen bound gives n0+T≤2gamma as well as T≥gamma+1. All path and first-section edges are actual incidences of the declared original. No unrelated target is padded.

The first branched section uses h=3, Q0=gamma+2 and split k0=Q0. Its preliminary cut is gamma and its preliminary crossing threshold is gamma+2 by D134. The size, pre-complement cut and new threshold are
```
n=N+Q0+4=4gamma+6,
C0=3+gamma+Q0=2gamma+5,
d=(gamma+2)+Q0=2gamma+4.
```
The new zero-frontier coordinates complement about n. Thus c=n+1−C0=2gamma+2. Each preliminary old high label x≥gamma has placement label 3+x+Q0 and new oriented label n−(3+x+Q0)=N+1−x.

The actual path coordinate 2gamma is internal because gamma≥1 and T≥gamma+1. Its label before the first section is gamma. Its two adjacent path positions are 2gamma−1 and 2gamma+1, with labels N−gamma+1 and N−gamma, respectively. When the latter is the translated seed frontier it remains the actual adjacent spine vertex. All three preliminary labels lie on the high side. After orientation the middle vertex has label 2gamma+1=c−1, and its two physical neighbors have labels gamma and gamma+1, respectively. Their actual edge weights are gamma+1 and gamma. In particular the boundary vertex is genuinely non-leaf.

Now consider every edge with both endpoints below c in the returned orientation. The newly attached centers and all its first-section terminals have pre-complement labels below C0 because k0=Q0. Hence they are high after orientation. The new frontier has oriented label zero and all its edges cross, since they go to those centers and the old frontier, which was low before the placement. Thus an edge with both endpoints below c can only come from a preliminary old edge with both labels at least gamma.

For a preliminary seed edge, both labels lie in [T,n0+T]⊆[gamma+1,2gamma]. For a preliminary path edge whose labels are both at least gamma, its small alternating entry is at most T−1≤2gamma. Its large alternating entry is N−j for some j≥gamma−1: at j≤gamma−2 both adjacent small entries that exist are j and j+1, strictly below gamma. Therefore both preliminary labels of this kind of edge are at most 2gamma+1. The new oriented formula N+1−x places each endpoint label at least gamma. This covers all actual low-low incidences, including a path edge incident to the translated original frontier.

For a subsequent canonical three-center placement with any 1≤a<c and positive two gaps there are two exhaustive cases.

- If a>gamma, the witnessed actual edge from gamma to 2gamma+1 belongs to P, since its lower end is below a and its upper end c−1 is in M. Its weight gamma+1 is at most a by integrality. The minimum P condition fails.
- If a≤gamma, any P edge would be an actual low-low edge with one endpoint below a. The proven low-low bound excludes it, so P is empty. The first gap is nonempty and its smallest label 3+a≤3+gamma<2gamma+4=d. The empty-P obstruction applies.

Hence no permitted exceptional block length or positive shift on this independently supplied infinite family gives a successful canonical three-center extension with the designated D134 return. At h=3 and p=1 the compatibility equation also forces p'=1. Prefixed symbolic sizes may be arbitrarily large among the admitted gamma values. No numerical initialization, new allocation, or label search is used. This is an obstruction for the declared resource architecture on an independently supplied family, within ordinary graceful labeling.

## Retained positive scope and polarity

For the exact D139 and D140 singleton exceptional leaf, its only original incident edge has weight d and crosses from M to the upper outer band. Thus P is empty and R={d}, saturating the p'=1 capacity without violating it. The first gap has smallest label 3+a=c+2=d at a=c−1, so the strict below-d obstruction does not apply. The accepted D139 ordinary and stronger returns and the D140 repeatable allocations remain valid in their exact scopes.

For actual zero-frontier input the proof uses E directly and the actual output frontier becomes maximum. For actual maximum-frontier input use the old oriented labels n−g and complement the displayed output about m. On the actual incoming label alphabet the cuts in increasing order are n+1−c and n+1−a, and the three actual shifts are 1, 1+Q−t and 1+Q. The two positive gap increments exchange order, and the exterior widths are conjugate to the oriented widths h and 1. The designated cut corresponds to the first actual cut in this polarity. Both old and new side conventions exchange on complement, so the old incidence membership and weights carry over with the appropriate actual output cut and frontier now zero. The obstructions and retained positive comparison therefore cover both actual polarities under the declared oriented placement.

The general conclusions are necessary spectral conditions, the three-center singleton degree-one condition, the conditional leaf-strip exclusion, and the full canonical exclusion on the stated D134 non-leaf inputs. Other exterior placements, additional cuts, nonextreme frontiers and different prescribed crossing spectra are outside this result. D131–D140 retain their exact scopes.
