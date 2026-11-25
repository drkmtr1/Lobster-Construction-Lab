# D159 — Exact exceptional-phase boundary-state allocation

Task `LCL-ORDINARY-SPINE-EXCEPTIONAL-BOUNDARY-STATE-ALLOCATION-001`. All labels, size parameters and quotas are exact integers, excluding booleans. All displayed intervals are inclusive, with reversed intervals empty. The symbol ⊔ denotes disjoint union.

## 1. Fixed named exterior and scope

Use an independently supplied [D157](ORDINARY_SPINE_ALTERNATING_EXCEPTIONAL_SPECTRUM.md) S₋₁ prefix in the exact [D158](ORDINARY_SPINE_EXCEPTIONAL_PHASE_PRESERVING_BRIDGE.md) placement and return. Retain the original named graph, spine, physical extreme frontier v and actual cut. Orient G(v)=0, with n=2c+2 and d=c+2. Actual crossing and noncrossing weights are [d−1,n] and [1,d−2]. For two new actual spine sections at u,w, require n≥2K, K≥8, A=3, B=4, s=2K−7, k=K−3 and m=n+2K. The outside tree retains reduced labels v=3,u=4,w=0,a=1,b=2,Q=5,P=6 and the actual direct leaf of w at 7. The second centers P,Q occur at the first and second positive branch indices at w. All terminal leaves stay in the gap. The two first centers retain their original physical roles when assigned the numerical labels a and b. There is no direct gap leaf. The actual edges vu,ub,ua,uw,wQ,wP and the edge from w to its direct leaf have reduced differences 1 through 7 and all cross.

In the prescribed family the actual ordered profiles are (2r,2t), (2p,2q+1,0) with exact r,t,p,q≥1 and K=r+t+p+q+4. Give the larger first half-quota T=max(r,t) the role b, with ties by original index, and put R=min(r,t) at a. **This fixed exterior admits an S₋₁-preserving allocation exactly when T≥2.**

The more general result uses actual positive gap quotas α,β,γ,η at a,b,Q,P, respectively, with α+β+γ+η=s, while retaining the size, roles and other exterior premises above. The second center order and direct leaf remain as declared. Q and P denote numerical roles, so γ can be even in the generalized problem. **The exact conditions are β≥4, γ≥2, α≡β≡η modulo two and γ of the opposite parity.** Both statements concern the fixed exterior and the designated return contract.

## 2. Exact arrows and forced boundary reservations

In the oriented placement old lower labels shift by 3 and upper labels by 3+s. The new cut is C=c+K, so a gap label 3+c+i is below C exactly when i<k. Subtract the actual endpoints of its edge. Lower hosts a,b have labels 1,2 and hence respective weight coordinates π(i)=i+1,i in weights d−1+π(i). Upper hosts Q,P have full labels n+s+5,n+s+6, giving π(i)=s+3−i,s+4−i. The leaf label is between the two exterior bands, so these subtractions give the absolute weight. D158 requires π to permute [0,s−1] and π(i)≥K exactly for opposite physical sides of source and host.

Put J=s+3=2k+2. For sources, Lⱼ=j with j∈[0,k−1] are physically lower and Hⱼ=J−j with j∈[4,k+2] are the upper coordinates [k,s−1] in reverse. For destinations, Lⱼ with j∈[0,k+2] represent [0,K−1], and Hⱼ with j∈[4,k−1] represent [K,s−1] in reverse. Each pair partitions the full coordinate alphabet separately. In this notation the complete arrow table is

| Actual host | Image of source Lⱼ | Image of source Hⱼ |
|---|---|---|
| a | Lⱼ₊₁ | Hⱼ₋₁ |
| b | Lⱼ | Hⱼ |
| Q | Hⱼ | Lⱼ |
| P | Hⱼ₋₁ | Lⱼ₊₁ |

An arrow is legal exactly when its source and destination cells exist. Indeed, these cells certify coordinate range, and the table sends an opposite-side pair to H precisely in the two cases of a physically upper source at a lower host, or a physically lower source at an upper host. In every other case its L image is noncrossing. There are no other physical gap hosts.

At the left, destination Lⱼ for j=0,…,3 has incoming possibilities only from Lⱼ at b and L_(j−1) at a if the latter exists. The potential H sources at j or j−1 do not exist in this range. Inductively start with L₀ at b. After each earlier L source has been forced at b, Lⱼ has just its own source available, so L₀ through L₃ all use b.

At the right, Hₖ₊₂ has no destination in row H, and P would require nonexistent Lₖ₊₃. Thus it uses Q, supplying Lₖ₊₂. Hₖ₊₁ has no H image and its P image repeats that used L cell, so it uses Q to give Lₖ₊₁. At Hₖ, b has no H image and P would repeat Lₖ₊₁. It can either use Q to give Lₖ, or use a to give Hₖ₋₁. In the latter case Lₖ must be filled by a rightward arrow from common column k−1, because every other possible source for it has been reserved. The first physically upper source is Hₖ₊₂, with coordinate k. Hₖ is the distinct coordinate k+2, and its optional assignment to a respects the first-upper-source restriction of D158.

These arguments include the minimum K=8, when k=5 and the common interval [4,k−1] contains one column. There is no overlap between the forced left L reservations, the common L and H sources, and the three terminal H columns on the right. No arrow from the common interval can enter a filled left destination: the only possible leftward arrow would have to reach the absent H₃. The forced rightmost two H sources supply only their two reserved L cells.

For the empty common row boundary of the inventory calculus, s≥K alone gives K≥7. If K=7 then k=4. The same reservations apply, Hₖ cannot use a because H₃ is absent, and the only completion uses b four times and Q three times. This is a symbolic boundary check. The retained family has K≥8 and the positive four-host criterion cannot be met at K=7.

## 3. Two states and exact local conservation

For each common column j∈[4,k−1], let R_j record an arrow to L_(j+1) and D_j record one to H_(j−1). These are Boolean in a legal permutation, since two arrows of the same type from that column would collide. The boundary values are R₃=0 and D₄=0 on the left, and Dₖ is one exactly when Hₖ uses a. Every other arrow from a common column stays in that column. Thus the number of local sources consumed locally is 2−R_j−D_j. The number of local destinations filled locally is 2−R_(j−1)−D_(j+1), because the only outside arrivals are at Lⱼ from the preceding column and at Hⱼ from the following one. Equating these gives
```
R_j+D_j=R_(j−1)+D_(j+1),
R_j−D_(j+1)=R_(j−1)−D_j.
```
The difference vanishes at the left and hence on every boundary. Write z_j=R_j=D_(j+1), starting at z₃=0. The state is the presence (1) or absence (0) of the two arrows across that boundary.

The complete transition table specifies actual hosts in the order of the L and H sources in the column. A local L destination is needed exactly when z_(j−1)=0 and a local H destination exactly when z_j=0. If z_(j−1)=1 the column must send H left, and if z_j=1 it must send L right. These four demands give

| State in → out | Hosts of (L,H) | Exactly the image cells sent from column j |
|---|---|---|
| 0→0 | (b,b) or (Q,Q) | Lⱼ and Hⱼ |
| 0→1 | (a,Q) or (b,P) | Lⱼ and L_(j+1) |
| 1→1 | (a,a) or (P,P) | L_(j+1) and H_(j−1) |
| 1→0 | (Q,a) or (P,b) | Hⱼ and H_(j−1) |

For completeness, 0→0 uses two local images and only b and Q supply them on either source. Both sources must use the same host, either b or Q. Mixing them repeats an image. For 0→1 the L source can give the rightward arrow via a with the H source using Q for local L, or it gives local L via b with the H source using P for the rightward arrow. For 1→1, either L gives the rightward arrow via a and H the leftward arrow via a, or L gives the leftward arrow via P and H the rightward arrow via P. In 1→0, L can give local H via Q with H using a for the leftward arrow, or L gives the leftward arrow via P with H using b for local H. The table exhausts the legal choices.

Conversely, choose a word of these transitions starting in state zero and complete its final state e=z_(k−1) with Hₖ at Q if e=0 and a if e=1. At each common column Lⱼ has exactly one arrival from its predecessor if its incoming state is one, and otherwise from its own local sources. Hⱼ has exactly one arrival from its successor if its outgoing state is one, and otherwise from its local sources. The rule at Hₖ is exactly the needed successor for Hₖ₋₁ when e=1. In that case Lₖ receives the last common column's outgoing rightward arrow, and when e=0 Lₖ is filled by Hₖ at Q. The forced left state prevents an arrow to H₃. All other outside images belong to the forced reservations. Thus every cell has exactly one preimage and every assigned arrow is legal, even for one common column. The two constructions invert each other on coordinate-to-host allocations with the fixed roles. The state bit accounts for the local boundary condition. The separate quotas keep the global resource counts.

## 4. Formal support and the D158 packets

Let N=k−4 be the number of common columns and let X_a,X_b,X_Q,X_P be distinct formal variables. Give each host assignment its variable as weight. Multiplication records all uses through their exponents. The table yields a transfer matrix M indexed by (0,1), with
```
M_00 = X_b² + X_Q²        M_01 = X_a X_Q + X_b X_P
M_10 = X_a X_Q + X_b X_P  M_11 = X_a² + X_P².
```
The prefix L reservations and the final two H reservations have weight X_b⁴ X_Q². The last Hₖ completion contributes X_Q or X_a. Hence the exact support polynomial is
```
F_N = X_b⁴ X_Q² · (1,0) · M^N · (X_Q,X_a)^T.
```
Expanding a product selects one table entry choice per column and the consistent right completion. By the bijection in Section 3 its monomial coefficient is positive precisely for feasible fixed-role quotas, and coefficients count coordinate-to-host allocations. They do not count all assignments of original terminal names or all ordinary graceful labelings. Constructively, a positive coefficient permits subtraction of the forced and ending quotas and then successive predecessor choices with positive residual coefficients, back to the initial state zero. Each extracted choice supplies actual source, host and image. For positive quotas Section 5 gives a direct extraction without evaluating this polynomial.

D158 Closure A opens with (a,Q), uses all-a and all-P loops in state one, and returns to zero with (Q,a). Closure B opens with (b,P), has the same two types of state-one loops, and closes with (P,b). Both are closed state excursions followed by their stated state-zero remainder and Hₖ at Q. Thus both exact earlier constructions are retained in the state language.

## 5. Exact admission for positive quotas

For a valid word let n_a,n_P be counts of state-one loops at a and P, n_b,n_Q the state-zero loop counts, and m_AQ,m_BP the switch counts using the host pairs {a,Q} and {b,P}, in either direction. Starting in zero and ending at e gives m_AQ+m_BP≡e modulo two. With zero switches and e=0 state one is never visited. Including the reservations and Hₖ,
```
α = e   + 2n_a + m_AQ
β = 4   + 2n_b + m_BP
γ = 3−e + 2n_Q + m_AQ
η =       2n_P + m_BP.
```
Thus β≥4, γ≥2, β≡η≡m_BP, and α≡e+m_AQ≡m_BP. Also γ≡1−e+m_AQ≡1+m_BP. This proves necessity.

For sufficiency assume those bounds and parities and positive quotas. End in e=1 using exactly one opening switch. The following orders are deterministic. A repeated loop count of zero gives an empty interval.

| Quota regime | State-zero loops at b and Q | Opening (L,H) | State-one loops at a and P |
|---|---|---|---|
| α,β,η even, γ odd | (β−4)/2 and (γ−3)/2 | (a,Q) | (α−2)/2 and η/2 |
| α,β,η odd, γ even | (β−5)/2 and (γ−2)/2 | (b,P) | (α−1)/2 and (η−1)/2 |

Use the two left loops in the displayed order, then the opening, then the two right loops in their displayed order. Complete Hₖ at a and use all the forced reservations. In the even regime positivity gives α,η≥2 and γ≥3. In the odd regime β≥5 and α,η≥1. Both sets of loop counts are nonnegative integers. Substituting the counts and e=1 into the four usage equations gives the prescribed quotas. Equivalently the outside reservations and completion use seven sources, and the one switch and each loop use two. Thus the used column count is (α+β+γ+η−7)/2=(s−7)/2=k−4=N, with no additional space constraint.

The even regime has lower-to-upper crossings x=(γ−3)/2+η/2 and upper-to-lower crossings y=(β−4)/2+(α−2)/2+1. In the odd regime these are x=(γ−2)/2+(η−1)/2 and y=(β−5)/2+(α−1)/2+1. The opening column contributes no crossing in either word, and Hₖ at a contributes one to y. Both give x=(γ+η−3)/2 and y=(α+β−4)/2, agreeing with the fixed-phase counts from actual hosts. The one-column limit N=1 permits the odd opening alone when the loop counts all vanish. The even regime requires at least two common columns by the lower bounds on its positive quotas. No numeric transfer evaluation is needed.

For the prescribed D158 family substitute α=2R, β=2T, γ=2q+1, η=2p. The exact criterion reduces to T≥2 with the other assumptions already satisfied. The explicit word has T−2 b loops, q−1 Q loops, one (a,Q) opening, R−1 a loops and p P loops. Its common capacity is
```
(T−2)+(q−1)+1+(R−1)+p=R+T+p+q−3=N.
```
Its uses are α=2R, β=2T, γ=2q+1, η=2p and its crossing counts are x=p+q−1 and y=R+T−2. This covers all T=2,q=1 with arbitrary admitted R,p. The smallest admitted family case R=p=q=1,T=2 uses just the opening and one P loop. All empty loop sets are allowed. If T=1, β=2 cannot meet the four forced assignments at b. This settles the fixed exterior with the prescribed role selection. Other exceptional-phase exteriors remain outside the obstruction.

## 6. Exact named reconstruction and admitted closure

For an admitted word, use each host's increasing actual source coordinates to label its original terminal indices in order at that parent, with full labels 3+c+i. The actual direct leaf receives n+s+7 and the spine and center roles retain the declared physical names. All these data are supplied by the explicit word and boundary rules before the second section is emitted. A given word requires no separately solved complete graph in order to supply the intermediate state.

In the oriented placement the occupied old and fresh label bands are respectively
```
L_old        [3,c+2] ⊔ [c+s+3,n+s+3]
fresh labels [0,2] ⊔ [c+3,c+s+2] ⊔ [n+s+4,m].
```
The old weights are D_old=[1,d−2]⊔[d−1+s,n+s]. The gap fills [d−1,d+s−2] by the exact image permutation. The connected crossing exterior contributes [n+s+1,m]. These bands exactly partition [0,m] for vertices and [1,m] for actual edge differences. The threshold K separates the gap's crossing [d+K−1,d+s−2] and noncrossing [d−1,d+K−2]. Old crossings gain s and exterior weights all cross, giving the exact full crossing [d+K−1,m] and noncrossing [1,d+K−2]. The old sides are maintained at C=c+K by 3≤K≤3+s. The actual w=0 and m=2(c+K)+2 give the S₋₁ return.

Write S_a and S_b for the prescribed source coordinate sets of the two first centers. The supplied first-section gap source and image sets are I=S_a⊔S_b and J₁=(S_a+1)⊔S_b. Their two image components are disjoint by the state-word partition. The first exterior labels are {1,2,n+s+4}, and edges vu,ub,ua supply n+s+[1,3]. With J₂=[0,s−1] minus J₁, the exact first-boundary inventories are
```
used labels       L_old ⊔ {1,2,n+s+4} ⊔ (c+3+I)
remaining labels  {0,n+s+5,n+s+6,n+s+7} ⊔ (c+3+([0,s−1] minus I))
used weights      D_old ⊔ (n+s+[1,3]) ⊔ (d−1+J₁)
remaining weights (n+s+[4,7]) ⊔ (d−1+J₂).
```
At C the used crossing set is [d−1+s,n+s]⊔(n+s+[1,3])⊔(d−1+(J₁∩[K,s−1])). Its used noncrossing complement in the used set is [1,d−2]⊔(d−1+(J₁∩[0,K−1])). The remaining exterior edges all cross, and the gap remainder uses the two intersected sets with J₂ instead. The actual partial frontier is u at n+s+4. Its sole unfinished edge into the second section is uw, with w at zero and weight n+s+4. The further second-section edges consume exactly the gap J₂ and n+s+[5,7] on the three remaining exterior attachments.

For a maximum input complement about n to obtain oriented labels and complement the output about m. Before and after, the actual cuts are n+1−c and m+1−C. An old actual lower label x was oriented to n−x≥c and is sent to m−(3+s+n−x)=x+4. An actual upper x is sent to x+4+s. The minimum input instead adds 3 or 3+s. Both preserve actual membership at the designated cuts. The output physical frontier is 0 or m, and in maximum polarity the actual u is at 3. Complement the partial label sets about m in that polarity. All weights and crossing statuses, including uw, are invariant.

For mixed composition take an independently supplied S₀ prefix, for example the D134 initializer under its exact named premises, and use the D157 outbound leg to supply S₋₁. At that phase use any finite list of individually admitted D159 bridges, followed, if declared, by the D157 return. D158 bridges are also admitted via their sufficient assignments. At phase S₀ allow supplied strict D143 blocks of the same membership-preserving placement type. For any such declared sequence, independently prescribed tuples may vary as long as the actual previous phase matches and n_before≥2K_i at each step. Each transition raises n by 2K_i, advances the oriented cut by K_i, and preserves the exact named boundary it returns. Induction therefore supplies every section, with no deleted or artificial incidences. The independent initializer can supply a large enough start when the starting size is selectable.

At completed boundary i let C_i be the actual cut, Λ_i the sum of subsequent actual lower shifts and Σ_i the sum of subsequent gaps. For a strict block use its own supplied shifts and widths. Membership preservation gives the final map Ψ_i(x)=x+Λ_i+Σ_i·1(x≥C_i), since the side indicator of each already placed vertex is invariant. The completed used label set is Ψ_i([0,n_i]); the used weight set in the final alphabet keeps the boundary's full noncrossing band and shifts its full crossing band by Σ_i. At the partial first boundary use Ψ_i on the displayed partial label set, adding Σ_i only to its used crossing differences, with the cut of block i. The remaining sets at either boundary are the exact complements in the final alphabets. The actual unfinished uw in a D159 block crosses that cut, so applying Ψ_i to its known endpoints adds Σ_i to its difference and gives the transformed physical frontier label. Every vertex is emitted once with its final label. The word is supplied by bounded symbolic formulas for loop lengths, each explicit assignment is processed in a finite scan, and the suffix shifts require one backward pass. This is linear in the supplied and emitted graph sizes in indexed-integer operations.

The exact calculation above concerns the supplied four-host exterior, not a classification of competing placements. The D158 sufficient theorem, D157 phase changes and retained strict interface theorems keep their written scopes. [Strategic reassessment](../evidence/validation/LCL_ORDINARY_SPINE_EXCEPTIONAL_BOUNDARY_STATE_ALLOCATION_001/STRATEGY.md)
