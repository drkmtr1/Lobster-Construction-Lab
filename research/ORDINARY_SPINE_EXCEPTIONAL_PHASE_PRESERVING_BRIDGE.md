# D158 — Exceptional-phase-preserving ordinary bridge

Task `LCL-ORDINARY-SPINE-EXCEPTIONAL-PHASE-PRESERVING-BRIDGE-001`. All structural parameters and labels are exact integers, excluding booleans. Intervals include both endpoints and reversed intervals are empty. The symbol ⊔ denotes disjoint union.

## 1. Statement and exact fixed-phase inventories

Supply an independently constructed ordinary graceful named prefix carrying the [D157](ORDINARY_SPINE_ALTERNATING_EXCEPTIONAL_SPECTRUM.md) state S₋₁, with its actual witnessing spine ending at an extreme v. Orient the labels to G(v)=0. Write n=2c+2, d=c+2. At the actual oriented cut c, crossing weights are precisely [d−1,n] and noncrossing weights [1,d−2]. A label equal to the cut is upper.

Append the actual ordered profiles (2r,2t), (2p,2q+1,0) at u,w with r,t,p,q≥1. Their fresh vertex counts including spine vertices are 2r+2t+3 and 2p+2q+5, hence K=r+t+p+q+4 and m=n+2K. Each fresh vertex contributes exactly one actual parent edge. Require n≥2K.

**Sufficient domain.** The original admits an independent S₋₁ to S₋₁ bridge if max(r,t)≥3, or if max(r,t)≥2 and q≥2. The proof uses a fixed reduced exterior and two packet closures, and leaves feasibility outside the sufficient domain open. The bridge composes with admitted D157 phase changes and admitted strict D143 blocks of the kind specified in Section 6.

For the declared old placement choose A,B,s≥0 with A+B+s=2K. Shift old labels below c by A and the others by A+s. Preserve actual side membership at output cut C=c+K. Because the old sides are nonempty and their nearest occupied labels after shifting are A+c−1 and A+c+s, membership is exactly A≤K≤A+s, equivalently A≤K and B≤K. The old and fresh labels have the disjoint bands
```
L_old        [A,A+c−1] ⊔ [A+c+s,A+n+s]
fresh labels [0,A−1] ⊔ [A+c,A+c+s−1] ⊔ [n+s+A+1,m].
```
A noncrossing old edge keeps its weight. A crossing old edge acquires s by subtracting its actual low endpoint from its actual high endpoint after placement. Thus the old and required fresh differences are
```
D_old         [1,d−2] ⊔ [d−1+s,n+s]
fresh weights [d−1,d+s−2] ⊔ [n+s+1,m].
```
The return requires crossing spectrum [d+K−1,m]. Thus the shifted first old crossing requires s≥K, while the unchanged noncrossing differences lie below that threshold. For a supplied crossing reduced exterior on the actual selected fresh vertices and v, require low labels [0,A], upper labels [A+1,A+B], v=A, w=0, and its actual spectrum [1,A+B]. Add n+s to upper exterior labels. The exterior differences are then [n+s+1,m] and all cross. The remaining gap must have s actual leaves of exterior hosts and use exactly the low fresh difference band. These conditions are the sufficient arrangement of D157, with no necessity assertion for arbitrary relaxed placements.

A gap source i∈[0,s−1] gives label A+c+i, and is physically lower exactly for i<k=K−A. The actual gap weight is d−1+π(i), where
```
lower host with reduced label j:         π(i)=i+A−1−j
upper host of reduced label A+b:          π(i)=s+b+1−i.
```
The first formula subtracts the host label from the larger gap label. The second subtracts the gap label from n+s+A+b and uses n−c=d. Actual gap differences fill [d−1,d+s−2] exactly when π maps the assigned sources bijectively onto [0,s−1]. To realize the cut spectrum, π(i)≥K must hold exactly for opposite physical sides of the source and its actual host. This is the fixed-phase threshold, with the input and output both using the same one-weight correction.

## 2. First physically upper source

At the first physically upper gap source i=k, provided k<s, a lower host would require a crossing. Its image is K−1−j≤K−1, so it cannot serve that source. An upper host would require a noncrossing, and its image is K−B+b+1 by A+B+s=2K. Thus b≤B−2 is necessary. With the given placement inequalities and s≥K this condition is also exactly the numerical range and noncrossing test at this source for an upper host of index b≥1: the image is nonnegative and at most K−1≤s−1. The host still needs an actual eligible leaf and sufficient quota.

The source exists in the chosen constructions. More generally, w=0 is a fresh lower exterior vertex, so A≥1. In this arrangement s≥K gives s−k=K−B≥A≥1 and membership gives k≥0. For the D155 exterior A=B=3, only b=1 can serve k. Reduced weight one can occur only between A and A+1, and the only incidence at v is its connector vu, so that host is the actual u. It has no direct gap leaf in the ordered D155 profiles. The remaining leaves of that first section are terminals with their own center parents. Consequently this D155 exterior cannot preserve S₋₁. This obstruction concerns the declared width and host situation, with other widths and arrangements outside its scope.

## 3. Fixed wider exterior and legal row alphabets

Take A=3,B=4,s=2K−7,k=K−3. In the full profile family K≥8, so s≥K and both membership inequalities hold. Give numerical role b to the actual first center of larger half-quota T=max(r,t), using the earlier original index at a tie. Put R=min(r,t) at the other center a. This assigns numerical labels to the original named centers and retains their physical order and terminal indices.

Give v,u,w,a,b,Q,P reduced labels 3,4,0,1,2,5,6, respectively. Q is the actual odd-quota second center, P the actual even-quota second center. The sole actual direct leaf of w occupies reduced label 7. All terminals stay in the gap. The actual edges vu,ub,ua,uw,wQ,wP and the edge from w to its direct leaf give reduced differences 1 through 7 in that order. They cross the reduced cut between 3 and 4. The exterior is connected on the original incidences. The only gap hosts, and their full quotas, are a=2R, b=2T, Q=2q+1, P=2p. These sum to s. At the first upper source k the sole eligible index in this original exterior is 2, occupied by Q.

Put J=s+3=2k+2 and use Lⱼ=j, Hⱼ=J−j. Source L uses [0,k−1], and source H uses columns [4,k+2], giving the physically upper coordinates [k,s−1] in reverse. Destination L uses [0,k+2]=[0,K−1]. Destination H uses columns [4,k−1], giving the crossing image coordinates [K,s−1] in reverse. These are separate two-row representations of the complete source and image alphabets. The formulas above give

| Actual host | Lⱼ image | Hⱼ image |
|---|---|---|
| a | Lⱼ₊₁ | Hⱼ₋₁ |
| b | Lⱼ | Hⱼ |
| Q | Hⱼ | Lⱼ |
| P | Hⱼ₋₁ | Lⱼ₊₁ |

The arrows' H destinations occur exactly for lower sources at upper hosts or upper sources at lower hosts. The L destinations are noncrossing. This interpretation requires the destination cell to exist, which is checked by the partitions below.

Reserve L₀,L₁,L₂,L₃ at b and Hₖ,Hₖ₊₁,Hₖ₊₂ at Q. They supply L₀ through L₃ and Lₖ through Lₖ₊₂ respectively, and all their sources and images exist. The remaining source and image cells occupy both rows of [4,k−1], numbering k−4=R+T+p+q−3 common columns.

The [D155](ORDINARY_SPINE_TWO_FIRST_CENTER_PARAMETERIZED_CLASSIFICATION.md) strict supplier applies to these same profiles on S₀, since the sufficient domain below has T≥2 and its size premise is the same. That is an independent strict-phase control on the identical ordered quota domain. It uses a different placement of the actual direct leaf and has its own label assignments.

## 4. Two endpoint closures of the mixed-column packet

Place the packet on columns from ℓ=4 to z=4+R+p, of length R+p+1. There are R+p−1 interior columns and T+q−4 columns left after the packet. In each admitted closure T+q−4≥0, so every packet cell exists. At any interior column j with both sources at a, the arrows give L_(j+1) and H_(j−1), respectively. At P the arrows give those same two images in the opposite order. Thus each interior column supplies one image in each of its two neighboring columns, independently of the ordering of interior types. The endpoint assignments next provide the missing images and stop arrows at the packet's boundaries.

### Closure A

Assume T≥2 and q≥2. At ℓ use L at a and H at Q, producing L_(ℓ+1) and L_ℓ. At z use L at Q and H at a, producing H_z and H_(z−1). The first column receives L locally and H from the next column, and the last receives H locally and L from its predecessor. Every interior column receives L from its predecessor and H from its successor, including the inward arrows at the two endpoints. All images stay inside the packet and each image cell has exactly one preimage.

Use the first R−1 interior columns at a and the remaining p at P, using both source cells in each column at that one host. The packet uses 2R at a, 2p at P and two at Q. Of the T+q−4 remaining common columns use the first T−2 at b twice each, fixing both cells, and the last q−2 at Q twice each, swapping both. These counts sum to T+q−4. Total use at b is 4+2(T−2)=2T and at Q is 3+2+2(q−2)=2q+1. Uses at a and P are already complete. The crossings from lower sources to upper hosts are the p interior P uses, the last L at Q, and the q−2 Q column swaps, giving x=p+q−1. From upper sources to lower hosts they are the R−1 interior a uses, the last H at a, and the T−2 b pairs, giving y=R+T−2. When R=p=1,T=q=2 this consists of one interior P column and an empty pair remainder.

### Closure B

Assume T≥3 and q≥1. At ℓ use L at b and H at P, producing L_ℓ and L_(ℓ+1). At z use L at P and H at b, producing H_(z−1) and H_z. As in Closure A the first and last columns receive one image locally and the other from their interior neighbor. Each interior column receives exactly L from its predecessor and H from its successor. Every endpoint arrow either remains at the endpoint or points inward, so the image cells are exactly the packet.

Use the first R interior columns at a and the remaining p−1 at P, each using both sources. The packet uses a=2R, P=2(p−1)+2=2p and b=2. Of the T+q−4 leftover columns use the first T−3 as neutral pairs at b and the last q−1 as swaps at Q. This is exact capacity. Total b use is 4+2+2(T−3)=2T and total Q use is 3+2(q−1)=2q+1. The x crossings come from the p−1 interior P columns, the final L at P and the q−1 Q pairs, so x=p+q−1. The y crossings come from the R interior a columns, the last H at b and the T−3 b pairs, so y=R+T−2. When R=p=q=1,T=3 there is one interior a column and neither remainder is used.

Both closures have valid source, host and destination bounds throughout. Their crossing counts also agree with the D153 and D157 fixed-phase equations: the fresh graph colors have sizes 2(p+q+2) and 2(r+t+2) from the actual parent pattern, and these equal 2(A+x) and 2(B+y). One may choose Closure A when q≥2 and T≥2, and otherwise Closure B on the remaining admitted domain. Their union is exactly the stated sufficient condition on T=max(r,t) and q. The proof specifies which assignments to use without searching terminal placements.

## 5. Named reconstruction, both partial inventories and both polarities

For each actual parent, assign its increasing source coordinates to the increasing original terminal indices, assigning the full leaf labels A+c+i. Give the physical direct leaf at w the required expanded label n+s+7. Keep the prescribed original spine and branch roles. With the already declared old embedding and exterior expansion, every named vertex receives a unique label, by the three fresh bands and the old bands in Section 1. The original edges have their respective old differences, exterior band [n+s+1,m], or gap band [d−1,d+s−2]. These are disjoint and complete. On the actual gap edges the crossing interval is [d+K−1,d+s−2] and the noncrossing interval is [d−1,d+K−2]. Joining the old and exterior contributions yields crossing [d+K−1,m] and noncrossing [1,d+K−2]. The physical frontier w=0 and c_new=c+K give a new named S₋₁ state, with m=2(c+K)+2. The original graph is a lobster because each new named vertex is attached to its original parent along or within distance two of the continued witnessing spine.

To specify the first-section state, let S_a,S_b be the actual integer source coordinates prescribed at a and b by the reservations, packet and remainder. These are known before the second section is emitted. Put I=S_a⊔S_b and J₁=(S_a+1)⊔S_b by the actual translations of the first parents. The two image components are disjoint by the partition just proved. The first exterior labels are {1,2,n+s+4}, and the actual exterior edges vu,ub,ua use n+s+[1,3]. With the Section 1 consumed bands,
```
used labels       L_old ⊔ {1,2,n+s+4} ⊔ (A+c+I)
remaining labels  {0,n+s+5,n+s+6,n+s+7} ⊔ (A+c+([0,s−1] minus I))
used differences  D_old ⊔ (n+s+[1,3]) ⊔ (d−1+J₁)
remaining weights (n+s+[4,7]) ⊔ (d−1+([0,s−1] minus J₁)).
```
Used crossing weights are [d−1+s,n+s]⊔(n+s+[1,3])⊔(d−1+(J₁∩[K,s−1])). Used noncrossing weights are [1,d−2]⊔(d−1+(J₁∩[0,K−1])). For the remaining weights put J₂=[0,s−1] minus J₁. The remaining crossings are (n+s+[4,7])⊔(d−1+(J₂∩[K,s−1])), and the remaining noncrossings are d−1+(J₂∩[0,K−1]). All are taken at the block's output cut. The actual first frontier is u at n+s+4. The only edge from this assigned prefix to this block's second section is the original uw. Its placed difference is n+s+4, and the three second exterior attachments use n+s+[5,7]. The second-section gap images are exactly J₂. The independently supplied intermediate is in the declared target alphabet.

For maximum-frontier input with actual labels g, use G=n−g and complement the output labels about m. The actual input and output cuts are n+1−c and m+1−C. For an actual old label x below n+1−c its oriented G=n−x is at or above c, so the new actual label is m−(A+s+n−x)=x+B. For x at or above n+1−c its oriented label is below c, yielding x+B+s. Thus the actual lower shift is 3 in minimum polarity and 4 in maximum polarity, and the upper shift adds s in either case. Each actual old side is preserved, and complementation preserves absolute differences and whether any edge crosses. The actual final frontier is m in maximum polarity and zero in minimum polarity. In the maximum case invert both intermediate label sets about m, the actual u has label 3, and the unfinished uw retains weight n+s+4. All exact weight and crossing descriptions hold in either polarity.

## 6. Independently supplied mixed-phase composition

Use an actual independently supplied S₀ prefix, for example the D134 p=1 initializer under its exact named seed, path, branch and parity premises. The accepted D157 outbound leg independently produces S₋₁ on its actual two sections. Follow it with any declared finite list of D158 bridges, then a D157 return leg. Each bridge consumes the state supplied by its predecessor and returns S₋₁. The D157 return restores S₀. Zero bridges are permitted. At phase S₀ one can also insert admitted retained same-polarity D143 strict blocks, such as a separately supplied D155 placement within its proven domain. Here a retained strict block is a D143 S₀→S₀ construction whose exact original exterior and gap data and admission premises are supplied. All these placements follow the same membership-preserving old-map contract.

More generally, declare a finite list of these phase transitions with actual sections and initial S₀. In block i require its input phase to agree with the actual previous output, and let K_i be its fresh size parameter. Write n_i=n₀+2Σ_(j≤i)K_j and c_i=c₀+Σ_(j≤i)K_j. The exact size admission for these supplied blocks is n_(i−1)≥2K_i at every step, in addition to the individual theorem's parameter and supply premises. Tuples can vary independently subject to these tests. Induction gives the labeled original, exact phase and cut at each boundary. The same admitted profile can repeat in a phase that allows it because its required size stays fixed and n increases. If the initial size is selectable, the independent initializer has arbitrarily large admissible sizes and can meet each bound of a finite declared list. Every initializer and block occupies its declared original sections, with fresh names and unchanged incidences. This proves mixed closure within those interfaces.

At completed boundary i let C_i denote the actual cut, Λ_i the sum of subsequent actual lower shifts and Σ_i the sum of subsequent gaps. A strict block has its own A_i,B_i,s_i from its supplier. For every block the actual lower shift is its A_i on a minimum input and B_i on a maximum input. All the admitted maps preserve actual cut membership, so an existing label x receives exactly the final value
```
Ψ_i(x) = x + Λ_i + Σ_i·1(x≥C_i).
```
This is the composition of all future placements and commutes with passing from each supplied normalized boundary to the next. At a completed boundary the final used labels are [Λ_i,Λ_i+C_i−1]⊔[Λ_i+C_i+Σ_i,Λ_i+n_i+Σ_i]. If ε_i is the boundary phase and d_i=c_i+2, its final used weights are [1,d_i+ε_i−1]⊔[d_i+ε_i+Σ_i,n_i+Σ_i]. The complements in the final alphabets give the exact remaining palettes.

At a partial first-section boundary inside block i apply Ψ_i to its used label set, since these labels are already expressed in block i's target alphabet. Leave its used noncrossing weights unchanged and add Σ_i to its used crossing weights, using the supplied block-specific intermediate sets. Compute the exact remaining palettes by complementing these used sets in the final alphabets. Apply Ψ_i to both independently determined endpoints of the unfinished edge uw. In the bridge it is a crossing so its difference becomes n_before+s_i+4+Σ_i. This rule also tracks the transformed partial frontier and the named connector in each other admitted block from its own crossing status. The resulting final label of every vertex is fixed when emitted. A backward pass computes the sums for the finite sequence. Scans of each block's explicitly reserved cells and actual host indices then emit every declared vertex and edge once, giving linear indexed-integer operation count in the supplied and emitted sizes.

The result is sufficient on the stated profile and phase contracts. It leaves exact feasibility outside the two closures and general profile coverage open. The strict D143, D153 and D155 conclusions retain their hypotheses; the new width obstruction applies only to the specified exceptional-phase placement and its actual host restrictions.
