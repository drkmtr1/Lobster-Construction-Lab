# D162 — Exact odd-quota exceptional exterior classification

Task `LCL-ORDINARY-SPINE-EXCEPTIONAL-ODD-FIRST-QUOTA-CLASSIFICATION-001`. All labels, counts and parameters are exact integers with booleans excluded. Intervals are inclusive, reversed intervals are empty, and ⊔ denotes disjoint union.

## 1. Scope and conclusion

Supply an independently constructed ordinary graceful named prefix in the [D157](ORDINARY_SPINE_ALTERNATING_EXCEPTIONAL_SPECTRUM.md) S₋₁ state, with the actual witnessing spine ending at its extreme v. Orient G(v)=0. Write n=2c+2 and d=c+2. The crossing and noncrossing spectra at cut c are [d−1,n] and [1,d−2], with equality to the cut on the upper side.

Append two actual consecutive sections at u,w. The first has three positive centers with quotas 4,2r+1,2t+1 for independent integers r,t≥0. The second has positive centers of quotas 2 and 4 and its sole actual direct leaf. Retain every actual order, branch index, terminal name and parent incidence. The first adds 2r+2t+10 vertices and the second adds ten, so the new vertices and edges number 2K with K=r+t+10. Require n≥2K and put m=n+2K. Use the D157 membership-preserving placement, connected crossing exterior with all positive centers exterior, and a gap consisting of actual leaves at their original exterior hosts. The output returns exactly S₋₁. T means terminal-free exterior and E+ means an exterior with at least one actual original terminal.

**Classification.** Under these premises E+ is feasible for every r,t≥0. T is feasible if and only if max(r,t)≥2. Separation is therefore exact for r,t∈{0,1}. The separator domain in the two odd quotas is finite. Prefix size, original order and admitted composition can still vary. This classifies feasibility in the declared arrangement. In particular the chosen E+ neutral role is an explicit supplier choice. The proof makes no assumption that an arbitrary terminal-enabled exterior with a larger odd quota puts the quota-four center there.

The fresh actual graph bipartition from v lower has N_low=4+6=10 and N_high=4+(4+2r+1+2t+1)=2r+2t+10. Thus the fixed-phase parity condition does not obstruct these profiles. Existence requires the exact physical allocation proved below.

## 2. E+ exterior, coordinates and gap arrows

Set A=5,B=4,s=2K−9,k=K−5=r+t+5 and J=s+3=2k+4. These widths satisfy membership and s≥K because K≥10. Give the reduced labels and actual quotas as follows.

| Role | v | u | w | a | b | Z | Q | P |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Reduced label | 5 | 6 | 0 | 3 | 2 | 4 | 7 | 9 |
| Actual center quota | — | — | — | 2r+1 | 2t+1 | 4 | 4 | 2 |

Choose one actual indexed terminal at a for label 8 and one at P for label 1. The actual direct leaf at w remains in the gap. The exterior labels exhaust [0,9]. Edges vu,uZ,ua,ub and a-to-8 have weights 1,2,3,4,5. Edges uw,wQ,P-to-1 and wP have weights 6,7,8,9. Each edge crosses between reduced [0,5] and [6,9]. The parent connections prove the exterior is an original connected tree. No artificial vertex or incidence is introduced. Remaining quotas in order (a,b,Z,Q,P,w) are (2r,2t+1,4,4,1,1). In particular r=0 leaves no gap terminal at a while a and its exterior terminal remain present.

For a general declared placement let k=K−A and expand an upper reduced label by n+s. A gap leaf of coordinate i has label A+c+i. Subtracting endpoints, its actual weight is d−1+π(i). For a lower reduced parent label j this gives π(i)=i+A−1−j, and for an upper parent A+b₀ it gives π(i)=s+b₀+1−i. A source is lower precisely for i<k. An image must be in [0,s−1] and be at least K exactly when the leaf and its actual host lie on opposite physical sides at C=c+K. For this exterior the six maps are i+1,i+2,i,s+3−i,s+5−i,i+4 in the stated host order.

Write Lⱼ=j and Hⱼ=J−j. Sources L_[0,k−1] and H_[4,k+4] give [0,k−1] and [k,s−1] in opposite orders. Destinations L_[0,k+4] and H_[4,k−1] give [0,K−1] and [K,s−1]. Thus each pair partitions its own alphabet. Here and below a row interval denotes the cells with those indices.

| Host | L source image | H source image |
|---|---|---|
| a | L_(j+1) | H_(j−1) |
| b | L_(j+2) | H_(j−2) |
| Z | L_j | H_j |
| Q | H_j | L_j |
| P | H_(j−2) | L_(j+2) |
| w | L_(j+4) | H_(j−4) |

Use an arrow precisely when both cells exist. Lower-host arrows keep the row and upper-host arrows exchange rows, so destination H is equivalent to an actual crossing. w has only its one actual direct leaf.

## 3. Explicit E+ permutations, including zero quotas

Assign L_[0,3] to Z, L_[4,r+3] to a, and L_[r+4,k−1] to b. This partitions the lower sources, with lengths 4,r,t+1. Their L images are [0,3], [5,r+4] and [r+6,k+1], leaving exactly the L indices {4,r+5,k+2,k+3,k+4}. All lower images are noncrossing. The remaining H source assignments and their images are as follows.

### Case t=0

Here k=r+5. Use H_[5,r+4] at a, H indices {4,k,k+2,k+4} at Q, H_(k+1) at P and H_(k+3) at w. These cover H_[4,k+4] once, including the empty interval at a when r=0. Q gives L indices {4,k,k+2,k+4} and P gives L_(k+3), exactly the five missing L destinations. The a assignments give H_[4,r+3]=H_[4,k−2], and w gives H_(k−1). Therefore the whole H destination row is covered once. Upper-source counts are a=r,b=0,Q=4,P=1,w=1.

### Case t≥1

Use H_[5,r+4] at a. Use H_[r+6,k−1] and H_(k+1) at b. Use H indices {4,r+5,k+3,k+4} at Q, H_k at P and H_(k+2) at w. In source order the first entries run from 4 through r+5 with the a interval between the two Q endpoints. The b interval runs through k−1 and then P,b,w,Q,Q occupy k through k+4. In the boundary case t=1 the b interval is empty since k=r+6, and the six successive indices from r+5 through k+4 are still accounted for. The a interval can also be empty independently. Thus there are no coincidences and the upper source row is partitioned. Q gives L indices {4,r+5,k+3,k+4} and P gives L_(k+2), exactly the five missing L images. The H images are H_[4,r+3] from a, H_[r+4,k−3] and H_(k−1) from b, and H_(k−2) from w. They give precisely H_[4,k−1] with empty intervals allowed. Upper-source counts are a=r,b=(t−1)+1=t,Q=4,P=1,w=1.

In both cases the full gap quotas are (2r,2t+1,4,4,1,1). The exact crossing counts are x=0 from lower sources at upper hosts and y=r+t+1=s−K from upper sources at lower hosts. At t=0 the actual coordinate used at w is J−(k+3)=k+1, with image K. At t≥1 it is J−(k+2)=k+2, with image K+1. This is the displacement-four crossing of the actual direct leaf. The source and image proofs include r=t=0. They construct the allocation directly from the input quota roles.

## 4. Necessity for every terminal-free exterior

No selected exterior terminals means A=4, since the fresh lower exterior vertices are w and the three first centers. If the actual direct leaf remains in the gap, B=3. The reduced difference-one crossing and v's sole exterior incidence vu force u=A+1. At the first upper source i=k, which exists since s−k=K−B≥A, every lower host has image at most K−1 and would need a crossing. An upper host needs image K−B+b₀+1<K, which at B=3 admits only b₀=1, namely u. It has no direct gap leaf. This is the [D158 first-upper-source obstruction](ORDINARY_SPINE_EXCEPTIONAL_PHASE_PRESERVING_BRIDGE.md#2-first-physically-upper-source).

Thus a terminal-free solution has the actual direct leaf exterior, B=4 and all terminals in the gap. The actual three lower centers occupy labels 1,2,3 and have displacements 2,1,0 respectively. The two upper second centers have even quotas two and four. For any permutation of the entire gap alphabet,
```
Σ_i (π(i)−i) = 0.
```
At upper index b₀ each term is s+b₀+1−2i, so modulo two that parent's contributions vanish by its even quota. The even lower translations contribute zero modulo two as well. The quota at the unit translation must be even, hence four, the only even first quota. The remaining neutral host has an odd quota. Every upper image is at least four by b₀≥2. The lowest four images must use lower sources, and induction on them forces i to use the neutral host for i=0,1,2,3 because a positive shift would need an earlier consumed source. This is the [D160 forced reservation](ORDINARY_SPINE_EXCEPTIONAL_FIVE_HOST_EXTERIOR_SUPPLY.md#width-independent-first-center-obstruction-under-the-same-arrangement). Its quota is at least four, so being odd it is at least five. Therefore max(r,t)≥2. This argument covered both direct placements and all physical role orders. It concerns this exact return and placement class.

## 5. Terminal-free constructions for every remaining case

When an odd first quota is at least five, give numerical role Z to an actual such center of quota z≥5, resolving a tie or two eligible choices by physical index. Give a the other actual odd quota a₀≥1, and b the unique quota four. This preserves the actual order of the original.

Use reduced labels v=4,u=5,w=0,a=1,b=2,Z=3,Q=6,P=7, direct leaf 8, with Q the actual quota-four second center and P the quota-two center. All actual terminals are in the gap. The exterior edges vu,uZ,ub,ua give weights [1,4] and uw and the three actual w attachments give [5,8]. The reduced label range is [0,8], all edges cross, and the connected exterior is the actual two-section skeleton with its direct leaf. A=B=4,s=2K−8 and k=K−4 give s=2k. Now J=s+3=2k+3. L_[0,k−1] and H_[4,k+3] are the source partition and L_[0,k+3] and H_[4,k−1] the destination partition, by the same interval calculation with K=k+4. The legal arrows are:

| Host | L source image | H source image |
|---|---|---|
| a | L_(j+2) | H_(j−2) |
| b | L_(j+1) | H_(j−1) |
| Z | L_j | H_j |
| Q | H_j | L_j |
| P | H_(j−1) | L_(j+1) |

When specified in Case B exchange only the numerical labels at P and the actual direct leaf, giving P label 8 and the direct leaf 7. Both original vertices stay adjacent to w, so the reduced spectrum stays exact. Then P gives L_j→H_(j−2) and H_j→L_(j+2). In all variants the destination row certifies the cut predicate, by the same endpoint formulas as in Section 2.

Reserve L_[0,3] at Z and H_(k+2),H_(k+3) at Q. Their images are the corresponding L cells. The common columns [4,k−1] number k−4=(a₀+z+2)/2, since a₀+z=2r+2t+2. Use N_Z=(z−5)/2 neutral columns (Z,Z) followed by an opening (b,Q), with each pair ordered by its L and H source. The neutral columns fill both local images. The opening in column l gives L_l and L_(l+1), leaving H_l pending. Define a unit entry at j to mean that L_j is already supplied, H_(j−1) is pending, all lower-numbered L cells and H cells below j−1 are supplied, and no other local or future image is consumed. Account separately for the reserved last two L cells. The opening supplies a unit entry at l+1. A default (P,P) column at j gives L_(j+1) and H_(j−1), thus maintaining the entry at j+1.

### Packet U

Given a unit entry at j, choose (a,b) then (Z,b) in columns j,j+1. Their four images are L_(j+2),H_(j−1),L_(j+1),H_j, respectively. These fill the two available H obligations before j+1, supply the two new L images and leave H_(j+1) pending. Hence there is a unit entry at j+2. Its quota contribution is (a,b,Z)=(1,2,1). All of its H-source edges cross, and its L-source edges are noncrossing.

### Case A, a₀=1

After the opening use Packet U, then one default (P,P) column. There are exactly N_Z+4 common columns, as required. The resulting unit entry at k has L_k already supplied and H_(k−1) pending. Use H_k at b and H_(k+1) at Q for H_(k−1) and L_(k+1). Along with the reserved right cells this covers both rows completely. Including all reservations, a has one assignment, b has opening one, packet two and closing one, Z has 4+2N_Z+1=z, Q has two from the reservations and one each from the opening and closing, and P has two. The single lower P gives x=1. The upper neutral loops, two H edges of Packet U and H_k at b give y=N_Z+3=r+t+1.

### Case B, a₀=3

Use the swapped P/direct labels and after the opening put these four columns starting at j.

| Column | Hosts of (L,H) | Images of (L,H) |
|---|---|---|
| j | (b,P) | L_(j+1), L_(j+2) |
| j+1 | (a,a) | L_(j+3), H_(j−1) |
| j+2 | (P,Z) | H_j, H_(j+2) |
| j+3 | (b,a) | L_(j+4), H_(j+1) |

The incoming unit entry leaves L_j already supplied. The table fills the four L images from j+1 through j+4 and four H images from j−1 through j+2, leaving exactly a unit entry at j+4. In particular the H destination indexed j+2 is filled locally rather than by the next column. The table uses a=3,b=2,Z=1,P=2. This occupies exactly N_Z+5 common columns with the opening. Close at the unit entry at k using H_k at b and H_(k+1) at Q as in Case A. The resulting quotas are (3,4,z,4,2) at (a,b,Z,Q,P). Only the single lower P crosses from below, so x=1. The upper neutral loops and the table's H selections at a,a,Z, plus H_k at b, yield y=N_Z+4=r+t+1.

### Case C, a₀≥5 odd

Use the default exterior. After the opening use Packet U and one default (P,P) column. At the next unit entry j, use the [D160](ORDINARY_SPINE_EXCEPTIONAL_FIVE_HOST_EXTERIOR_SUPPLY.md#4-the-conversion-and-the-unified-allocation-word) conversion (a,b), then (a,Q). Their images are L_(j+2), H_(j−1), L_(j+3), L_(j+1). The conversion fills the pending H_(j−1) and all L images through j+3, leaving H_j and H_(j+1) for the double-displacement continuation. Use N_a=(a₀−5)/2 common (a,a) columns through k−1 and H_k,H_(k+1) at a. Their L images, if any, are L_[j+4,k+1]. All their H images, including completion, are H_[j,k−1]. Together with the reserved right images and the prior words these cover both rows, including N_a=0. The capacity is N_Z+6+N_a=(a₀+z+2)/2. The full quotas are a=1+2+2N_a+2=a₀, b=1+2+1=4, Z=4+2N_Z+1=z, Q=2+1+1=4, and P=2. The lower P is the sole source contributing x=1. The upper neutral loops, two H edges of Packet U, the first conversion's H at b, N_a paired a uses on H and the two final a uses give y=N_Z+N_a+5=r+t+1.

All packet starts follow the opening, so j−1≥4 whenever a pending H image is used. In A and B a last common column sends at most L_k, with remaining end images supplied by the two closing sources and the two reserved sources. In C the furthest common L image is L_(k+1), and the two right a sources finish the H range. Each individual displayed destination lies in the exact row alphabet. The formulas use nonnegative integer loop lengths, and each common interval fits by the stated counts. Minimum z=5, a₀=1,3,5 and empty loop sets are included. The sum x+y=r+t+2=s−K for all T cases. This proves sufficiency without an exhaustive finite-state assumption.

## 6. Exact named labels, weights and partial resources

In each explicit exterior retain v,u,w, every physical center and the direct leaf's original index. For E+ take the smallest original terminal index at a and at P for the two exterior terminals. At every actual parent assign that parent's remaining terminal indices in increasing order to its increasing supplied coordinate set. The choice of role is made before this step. A sole direct gap leaf receives the independently supplied w coordinate. The ordered profile and actual incidences are unchanged. This constructs every assigned label and both partial inventories from the input and formulas without solving a whole-target instance.

Place the old labels G using lower shift A and upper shift A+s. Let L_old and D_old be their full used label and weight sets. Since A≤K≤A+s holds, old membership is preserved. These sets and the new exact complements are
```
L_old    [A,A+c−1] ⊔ [A+c+s,A+n+s]
L_fresh  [0,A−1] ⊔ [A+c,A+c+s−1] ⊔ [n+s+A+1,m]
D_old    [1,d−2] ⊔ [d−1+s,n+s]
D_fresh  [d−1,d+s−2] ⊔ [n+s+1,m].
```
The upper expansion by n+s gives the exterior weights [n+s+1,m], all crossing the actual cut C. Each gap coordinate uses one unused label and its image one unused weight in the gap band. The disjoint sets prove the complete bijections. The actual gap crossing weights are [d+K−1,d+s−2] and its noncrossing weights are [d−1,d+K−2]. Together with the old and exterior bands, the exact crossing and noncrossing spectra are [d+K−1,m] and [1,d+K−2]. The continued original witnessing spine ends at w=0, and m=2(c+K)+2 gives S₋₁ at cut C.

Let S_a,S_b,S_Z be the three actual first-center gap source sets. Their disjoint union I is the first-section source set. In E+, first images J₁=(S_a+1)⊔(S_b+2)⊔S_Z. In T, J₁=(S_a+2)⊔(S_b+1)⊔S_Z. The two constructions prove these unions disjoint. Let I′ and J₂ be the respective complements in [0,s−1]. The used and remaining exterior labels after the first section, excluding the old v already in L_old, are

| Exterior | First labels E₁ | Remaining labels E₂ |
|---|---|---|
| E+ | {2,3,4,n+s+6,n+s+8} | {0,1,n+s+7,n+s+9} |
| T | {1,2,3,n+s+5} | {0,n+s+6,n+s+7,n+s+8} |

The first actual exterior differences are n+s+[1,5] in E+ and n+s+[1,4] in T, hence n+s+[1,A]. The remaining are n+s+[6,9] and n+s+[5,8], hence n+s+[A+1,A+B]. Swapping the two actual labels in Case B merely permutes the two exterior edge weights at w. The exact partial inventories are
```
used labels       L_old ⊔ E₁ ⊔ (A+c+I)
remaining labels  E₂ ⊔ (A+c+I′)
used weights      D_old ⊔ (n+s+[1,A]) ⊔ (d−1+J₁)
remaining weights (n+s+[A+1,A+B]) ⊔ (d−1+J₂).
```
Old labels and exterior labels have their declared cut sides. In each gap part the lower label coordinates are those below k. The used crossing weights are [d−1+s,n+s]⊔(n+s+[1,A])⊔(d−1+(J₁∩[K,s−1])). The used noncrossing weights are [1,d−2]⊔(d−1+(J₁∩[0,K−1])). Remaining crossing weights are (n+s+[A+1,A+B])⊔(d−1+(J₂∩[K,s−1])) and the remaining noncrossing weights are d−1+(J₂∩[0,K−1]). The actual partial frontier is u with label n+s+A+1, and the sole unfinished incidence into this next section is the original uw with w=0 and weight n+s+A+1. Its two supplied endpoints lie on opposite sides of the cut.

In maximum input polarity use G=n−g and complement the output about m. The actual cuts are n+1−c and m+1−C. An old actual label x below the input cut corresponds to oriented n−x≥c and yields m−(n−x+A+s)=x+B. An old actual upper label yields x+B+s. Thus minimum and maximum polarities have respective actual lower shifts A and B, adding s to either upper shift. In E+ the lower shifts are 5 and 4 respectively. Complement the partial label sets about m and preserve all weights and crossing flags. The actual maximum output has w=m and u=B−1, with the same unfinished edge and weight. No incidence or gap terminal is relabeled as a different physical role.

## 7. Admitted finite composition and retained controls

Start from any independent S₋₁ input. Compose any finite list of these supplied blocks and individually admitted D158–D160 bridges at S₋₁. Likewise include D157 legs wherever their exact input phase and original profiles permit, and individually supplied strict [D143](ORDINARY_SPINE_TWO_SECTION_CUT_STATE.md) blocks at S₀. A declared sequence can start in an independently supplied S₀ state under its own premises. The D157 outbound and inbound legs can connect the actual strict and exceptional stretches. For each step require exact physical frontier, phase, cut and size premises including n_before≥2K_i. Each old map preserves actual membership, and each output is an independently supplied full adapted input for the next step. Induction gives the exact labeling and inventories along that physical sequence.

At completed boundary i let C_i be the actual cut in its current polarity, Λ_i the sum of subsequent actual lower shifts and Σ_i the sum of subsequent gap widths. Each already placed label x finishes at Ψ_i(x)=x+Λ_i+Σ_i·1(x≥C_i), by membership invariance at each later boundary. Add Σ_i to its crossing edge weights and preserve its noncrossing edge weights. The same transforms apply to the independently supplied partial first-section resources in block i's output alphabet using that block's actual cut. The known unfinished uw crosses, so its final weight is n_before+s_i+A_i+1+Σ_i in the present families. Transform both actual endpoints and the partial label set by Ψ_i, and recover both final remaining inventories by taking exact complements. This fixes final labels before emission. There are finitely many declared blocks, finite quota-indexed assignments, and one finite sequence of suffix sums, so the process terminates. Only actual original sections and incidences are used.

For D161's independently supplied n=74 prefix and the selected quota values, the separate symbolic result reproduces the 24 separating *decisions* on their actual originals without replaying the campaign or claiming the same numerical labels. With other first quotas (1,1) or (3,3) there are three positions of the first quota four and two orders of the second quotas, giving six each. With other first quotas (1,3) there are six first orders and two second orders, giving twelve. The exact archived original and arm bindings are retained in new custody. The nine D161 separators with second quotas (4,4) and all other parity sectors are outside this classification. [D161 separating records](../evidence/runs/d161-exceptional-quota-four-001/SEPARATORS.md) · [Custody](../evidence/validation/LCL_ORDINARY_SPINE_EXCEPTIONAL_ODD_FIRST_QUOTA_CLASSIFICATION_001/CUSTODY.json)

Packet U preserves a unit boundary while spending an odd number of a and Z incidences. The four-column packet uses displacement-two reflection at the actual P role to spend a different odd a quota with the same unit boundary. The E+ construction uses the sole direct gap leaf as a displacement-four closing arrow. Together with the D160 conversion these exhibit compatible local operations in their stated resource settings. Their compatibility with other quota changes and exterior widths remains a separate question. [Strategic reassessment](../evidence/validation/LCL_ORDINARY_SPINE_EXCEPTIONAL_ODD_FIRST_QUOTA_CLASSIFICATION_001/STRATEGY.md)
