# D168 — Residue-class compression with two eligible upper hosts

Task `LCL-ORDINARY-SPINE-EXCEPTIONAL-TWO-UPPER-HOST-RESIDUE-COMPRESSION-001`. All numerical data are exact integers, excluding booleans. Intervals are inclusive and reversed intervals are empty. A union denoted by `⊔` is disjoint.

## 1. Physical input and theorem

Use the declared [D157](ORDINARY_SPINE_ALTERNATING_EXCEPTIONAL_SPECTRUM.md) two-section, connected crossing-exterior, leaf-only-gap arrangement for an `S₋₁ → S₋₁` transition. The independently supplied named prefix is ordinary graceful with `n=2c+2` edges, actual extreme frontier `v`, oriented to `G(v)=0`, cut `c` (equality belongs to the upper side), and `d=c+2`. Its crossing weights are `[d−1,n]` and noncrossing weights `[1,d−2]`. Its actual witnessing spine and all old incidences are retained.

Independently supply a fixed connected reduced exterior of widths `A,B` with labels `[0,A+B]`. The lower side is `[0,A]`, with `v=A` and the new frontier `w=0`. The upper side is `[A+1,A+B]`. Every exterior edge crosses and the actual reduced edge differences are `[1,A+B]`. The exterior contains the actual appended spine vertices `u,w`, the edges `vu,uw`, every declared positive branch center and the fixed selected exterior leaves. Preserve their actual names, sections, original branch indices, selected terminal indices and parent incidences. Every remaining fresh vertex is an actual gap leaf at its own exterior parent. The old frontier has only its declared joining incidence among the new edges. In particular the two upper candidates are fresh, eligible physical parents `Q,P` with labels `A+β,A+β+ρ`, where `1≤β<β+ρ≤B`. All other upper parents have zero gap capacity. Keep the named lower gap leaves fixed, with total `M`.

For the requested family prescribe nonnegative residual upper gap quotas `(p_g,q_g)` in the order `(P,Q)`. For a positive center with `e_P` or `e_Q` fixed exterior terminals its full quota is the residual quota plus that fixed count and must be positive. A permitted spine host keeps its actual direct-leaf slot incidences. It may have zero residual capacity if allowed by the requested profile. Its direct leaves remain direct leaves. Any fixed bounds on a spine-host quota or other physical restrictions of the declared topology are imposed on the requested pair. Include exactly the prescribed indexed gap leaves at each parent. The independent data determine the graph by this leaf attachment to the supplied exterior joined at `v`. They suffice to name every edge before a complete labeling is obtained. The declared spine continues to witness distance at most two. The requested graph must satisfy the exact original size and placement conditions below.

**Theorem.** For these fixed data, there is a finite symbolic catalog of types independent of `(p_g,q_g)`. For each valid type there is a base `(p_g0,q_g0)∈ℕ²` and a set `W⊆[0,ρ]`. The feasible pairs are exactly the requested pairs meeting the original topology and size constraints in the union of

```text
(p_g0,q_g0) + Σ_(a in W) z_a(2a,2ρ−2a),  z_a ≥ 0 integral.
```

The base bound is `k₀+A≤(N_marks−1)(G+ρ−1)` with the quantities in §5. A type can have no expandable gap and the catalog can be empty. The theorem gives exact feasibility and a named reconstruction in the supplied embedding. It supplies no exterior for an arbitrary original. The symbolic catalog and extraction are proved here without numerical evaluation.

## 2. Size, coordinates, arrows and physical crossings

There are `s=M+p_g+q_g` actual gap leaves and `A+B` fresh exterior vertices. The extension adds `2K=A+B+s` vertices and edges, where `K` is integral, `n≥2K`, and `m=n+2K`. The exceptional return at `C=c+K` requires `s≥K` for the shifted old crossing band and `A≤K≤A+s` for the old sides. Hence with `k=K−A`,

```text
s=2k+A−B,  p_g+q_g=2k+A−B−M,  s−K=k−B.
```

Here `k≥B` is equivalent to the inherited width/placement inequalities at this integral size. It gives `K≥A` and `A+s−K=A+k−B≥0`. The independently supplied prefix must meet its size premise at the requested pair.

The old lower labels advance by `A`, old upper labels by `A+s`, and an upper reduced exterior label advances by `n+s`. Gap coordinate `i∈[0,s−1]` has label `A+c+i`. Its edge weight is `d−1+π(i)`. For a lower parent at reduced `j₀` the leaf is above the parent in numerical value and subtraction gives `π(i)=i+A−1−j₀`. For an upper parent at `A+b` the leaf is below the parent, and subtraction using `n−c=d` gives `π(i)=s+b+1−i`. An actual source is lower exactly at `i<k`. The weight threshold is `d+K−1`, so the required crossing image is precisely `π(i)≥K`. The input admissions imply these cuts lie in the required coordinate ranges, allowing an empty crossing gap at `k=B`.

Set `J=s+β+1=2k+A−e`, `ℓ=β+2`, `e=B−β−1≥0`. A lower-row coordinate is `L_j=j` and an upper-row coordinate is `H_j=J−j`. Source and image alphabets are folded separately:

| Cell alphabet | Numeric coordinates | Column indices |
| --- | --- | --- |
| Lower source | `[0,k−1]` | `I_LS=[0,k−1]` |
| Upper source | `[k,s−1]` | `I_HS=[ℓ,k+A−e]` |
| Noncrossing image | `[0,K−1]` | `I_LD=[0,k+A−1]` |
| Crossing image | `[K,s−1]` | `I_HD=[ℓ,k−e]` |

For the upper rows subtract the endpoints from `J`. The near upper index is `J−(s−1)=ℓ`. The far upper source and image indices differ by `A`. The crossing image interval is empty exactly when `k=B`, since its right bound is then `ℓ−1`. This folding maps each of the full source and full image alphabets bijectively to its own row cells.

For a lower parent let `δ=A−1−j₀` be its signed displacement. A lower source is noncrossing at that parent and uses `L_j→L_(j+δ)`. An upper source crosses and uses `H_j→H_(j−δ)`. For each upper parent the lower source crosses and the upper source is noncrossing. At `Q` the image is `J−i`, giving `L_j→H_j` and `H_j→L_j`. At `P` it is `J+ρ−i`, giving `L_j→H_(j−ρ)` and `H_j→L_(j+ρ)`. An arrow is legal precisely when its source and indicated destination lie in their own windows in the table. This accounts for both absolute differences and physical crossing, including all absent row cells.

## 3. Reservations, graph counts and moments

Use actual lower-host leaf identities to choose reservations. Let `X,X′` be their lower-row source and corresponding translated destination index sets, and `Y,Y′` the upper-row sets. Each named leaf keeps its host and displacement. Require distinct indices within each class and legal arrows. Coincidences between different classes are allowed where these conditions hold, including the two marks of a zero-displacement leaf.

Put `x` for the number of lower sources at upper parents and `y` for the number of upper sources at lower parents. Lower sources total `k` and upper sources total `s−k`. Exactly `s−K` images cross, so `x+y=s−K`. Lower parents take `M=k−x+y=B+2y`, upper parents take `p_g+q_g=s−k−y+x=A+2x`. In the actual bipartition of the fresh graph rooted at `v`, the reduced exterior contributes `A` fresh lower vertices and `B` upper vertices. Each gap leaf has graph color opposite its exterior parent even if it occupies its parent's physical label side. Therefore `N_low=A+p_g+q_g=2(A+x)` and `N_high=B+M=2(B+y)`. Require integral `x=(p_g+q_g−A)/2`, `y=(M−B)/2`, with `0≤x≤k` and `0≤y≤s−k`. A valid reservation has `|X|=k−x` and `|Y|=y`, and the remaining matches must pass exact per-residue feasibility.

Write `ΣI` for the sum of the index interval `I`. In the first residual direction a P edge subtracts `ρ` from its source index. In the second it adds `ρ`. Comparing the residual index sums gives

```text
ρ N_PL = ΣI_LS−ΣI_HD−ΣX+ΣY′
ρ N_PH = ΣI_LD−ΣI_HS−ΣX′+ΣY
ρ p_g = ΣI_LS−ΣI_HD+ΣI_LD−ΣI_HS−ΣX−ΣX′+ΣY+ΣY′ .
```

The unequal baseline intervals occur in each identity. All signed displacements and every fixed leaf, including neutral leaves, enter the actual reservation conditions. These sums only count shifts in a valid matching. They do not test an unavailable source at a specific index or balance separately along each residue.

## 4. Exact residue path criterion

For each residue modulo `ρ` in `[0,k+A]`, scan increasing for `L→H`. At a column `j` of this residue put `S_j=1` for a surviving `I_LS∖X` source and `D_j=1` for a surviving `I_HD∖Y′` destination, with zero otherwise. The only possible incoming arrows to an existing destination are identity from `j` and shift from `j+ρ`. The nonidentity source bit `B_j` therefore satisfies

```text
D_j = S_j−B_j+B_(j+ρ).
```

The first bit is zero because a shift would leave the scan interval. The bit after the last residue cell is zero because no such source can enter. Require integer bits and `0≤B_j≤S_j`. Given them, send each existing source by its indicated shift or by identity. The equality gives exactly one arrow into each existing destination and zero into unavailable destinations. It follows that every arrow lands legally, including at the ends. The recurrence `B_next=B_current+D_current−S_current` starting at zero determines every bit uniquely. For `H→L` scan decreasing with `S=I_HS∖Y` and `D=I_LD∖X′`; the successor is now `j−ρ`, so the identical scan formula applies. All assertions apply to some or all absent cells, disjoint endpoint regions, an empty residue, and the all-zero P pattern. Terminal zeros also express each residue's exact source/destination balance.

At a common missing source and destination, the incoming and outgoing bits in scan order are both zero. D167's abstract adverse path has source holes at 4 and 8, destination holes at 8 and 10, and step size two on `[4,14]`. A source hole at 4 makes the next bit one, and the common hole at 8 then demands zero. Replacing the seven ordered cells by `a+jρ`, `0≤j≤6`, keeps the same obstruction for every `ρ≥1`. This is a path-level check, separate from any physical original. A common hole cannot be cancelled as if its capacity remained available.

## 5. Marked columns, anchor coverage and base admission

Mark each reservation's source and destination, with its class, identity, displacement and coincidences. Let `D_max` be the maximum absolute displacement among the fixed lower leaves, zero for an empty inventory. Let `D_tail=max(1,e)` and `G=max(D_max+1,2ρ+1)`. Include every left anchor `[0,ℓ]` and right anchor `[k−D_tail,k+A]`, recording ties. All cell columns belong to `[0,k+A]`. In particular `ℓ≤B+1≤k+1≤k+A` since `v,w` are distinct and `A≥1`. The right group starts at a nonnegative column because `k≥B` and `D_tail≤B`. The left anchors record both starts. The right anchors contain `k−1,k+A−e,k+A−1,k−e` even when an interval is empty. The fixed-width differences from the last anchor determine every right cutoff.

Each group is consecutive. If they touch or overlap there is no gap with length greater than one induced by those marks, and extra marks cannot enlarge a gap. Otherwise any gap of length at least `G` lies with its endpoints in `[ℓ,k−D_tail]`. Every interior column has all four baseline cells because `k−D_tail≤min(k−1,k−e)` and the upper rows begin at `ℓ`. No actual lower reservation can have endpoints on opposite sides of such a gap, including its marked endpoints, because that would span at least `G>D_max`.

For every distinct marked-column gap of length `g<G`, keep its length. For `g≥G`, use the base length `G+((g−G) mod ρ)` and allow multiples of `ρ` to be added. Fix the first anchor at 0. All marks to the right of any changed gap move by a multiple of `ρ`, including the entire right anchor group. Distinct marked columns remain distinct and ordered. Ties and residues remain exact. A lower reservation either stays fixed or translates both its endpoints by the same amount, so the signed displacement is preserved. Lower and upper comparisons with their respective anchored row cutoffs are preserved as well. If there is no changed gap, the original `k` stays fixed, including overlapping groups and the smallest `k=B`. When compression changes any gap, a retained long gap still has length at least `G` between `ℓ` and the shifted `k₀−D_tail`. Therefore `k₀≥ℓ+D_tail+G≥B` since `B=ℓ+e−1`. There is no additional base admission required to keep the width inequalities. The original prefix, if used for a smaller size, already meets its size bound there. The compressed certificate data remain auxiliary until the nonnegative base quotas satisfy the actual topology.

## 6. Reversible expansion and equal directional flow

Let consecutive marked columns enclose a long gap `(l,r)`. There are at least `2ρ` consecutive unmarked interior columns. On each residue, in both directions, these are entries with `S=D=1`, so the local bits are constant across the run. Splice after `l+ρ`, using the first `ρ` interior columns on one side and the next `ρ` on the other. Inserting `ρ` unmarked columns gives one extra neutral entry per residue in each scan. Existing events preserve order, residues, indicators, displacements, capacity bounds and boundary conditions. The inserted entry has the common bit so replaces a constant run by a longer constant run. Conversely, two successive legal lengths separated by `ρ` have the same event sequence, with one neutral entry per path removed from that run. A neutral entry passes its bit unchanged. Deletion to the shorter length leaves the interval long and retains all reservation events and all zero barriers. Induction gives reversibility down to the representative base length. This is an operation on allocation parameters whose additional leaves have actual upper hosts.

For a cut after column `t` inside the gap take `t=l+ρ`. Each residue has one last cell on the left and one first cell on the right, both interior. The arrows that cross the cut are precisely the active shift bits among these residue boundaries. No reservation spans the cut, so the counts of `X` and `X′` to the left agree, as do those of `Y` and `Y′`. Interpret the subscript `left` relative to this cut. In `L→H` all crossing arrows enter the left; left destinations minus left sources thus gives

```text
a_L = (t−ℓ+1−|Y′_left|)−(t+1−|X_left|)
    = |X_left|−|Y′_left|−ℓ.
```

In `H→L` the shift arrows exit the left. Left sources minus left destinations gives

```text
a_H = (t−ℓ+1−|Y_left|)−(t+1−|X′_left|)
    = |X′_left|−|Y_left|−ℓ.
```

Hence `a_L=a_H=a` and `0≤a≤ρ`. Equality concerns the totals, with no assertion that individual corresponding bits agree. Each insertion adds `2ρ` surviving sources and `2ρ` destinations across the two directions. It adds one P assignment per active bit, hence `2a` P leaves and `2ρ−2a` Q leaves. The right anchors give `k→k+ρ`, agreeing with the total increment from §2. Fixed selected exterior counts make the increments identical for the full terminal quotas when applicable.

Different long gaps have disjoint open interiors containing only neutral entries. The changed columns translate all subsequent events by whole multiples of `ρ` and leave their boundary bits and event word intact. In the two scan orders the inserted portions each pass the incident bit unchanged. Thus operations on distinct gaps commute and preserve each other's generator indices.

## 7. Finite catalog, exact support and arithmetic extraction

Start with the finite named lower inventory and fixed exterior. Choose a source row for every actual lower leaf. Choose a weak order of the labeled endpoint marks and of the boundary-anchor occurrences, with ties allowed. Retain the orders with first anchor 0, last anchor `k₀+A` and the prescribed consecutive relations in each group. For consecutive distinct marks choose a base length from `[1,G+ρ−1]`, treating lengths at least `G` as expandable. The last column determines `k₀`. Impose `k₀≥B`, exact anchor placement, legal reservations with their original displacements and within-class distinctness, and both exact residue-path tests. Take the resulting P and Q counts as the base quotas and check the aggregate laws with the auxiliary inventory. These data determine complete path indicator sequences. The procedure is a finite definition even with repeated displacements, coincident endpoints and zero residual counts.

The two anchor groups contribute `ℓ+1` and `D_tail+A+1` occurrences. Thus

```text
N_marks = 2M + ℓ + A + D_tail + 2,
k₀ + A ≤ (N_marks−1)(G+ρ−1).
```

The second inequality sums the consecutive base lengths. Ties only reduce the number of distinct gaps. It gives an explicit finite bound independent of the requested pair. Every successful allocation compresses to an enumerated type by §§5–6. Its actual reservations and exact bits survive and the removed lengths account for precisely the displayed generators. Conversely, expand a compatible type by those multiples of `ρ` and recover the unique residual assignment by §4. The new geometry has the requested quotas and continues to satisfy the width and parity laws. Test positivity for centers and every other named topology constraint, and size of the independent input prefix, at the requested pair. An auxiliary base with zero full quota need not represent a physical positive-center original. Dropping it would risk losing valid expansions. Enforcing these constraints at the requested pair is exact since compression provides an auxiliary type for every successful physical original and every retained expanded assignment lifts on an admissible actual original.

For a type, retain one representative expandable gap for each available index `a`. Because distinct expansions commute and have no further length limit in the symbolic type, the sum of the exponents at gaps with the same generator can all be placed at that representative. Define

```text
T = ((p_g+q_g)−(p_g0+q_g0))/(2ρ),     U = (p_g−p_g0)/2 .
```

Both must be nonnegative integers. Then require `Σ z_a=T` and `Σ a z_a=U`. For `W=∅` require `T=U=0`. For `W={a}` take `z_a=T` iff `U=aT`. For at least two indices put `a_min=min W`, `a_max=max W`, and `d_W=a_max−a_min`. Replacing `d_W` copies of an interior index `a` by `a−a_min` copies of `a_max` and `a_max−a` copies of `a_min` preserves both sums. Reducing all interior multiplicities in this way gives a solution with each interior `0≤z_a<d_W` whenever any solution exists. For each of the at most `d_W^(|W|−2)` bounded choices compute

```text
z_max = (U−a_min T−Σ_interior(a−a_min)z_a)/d_W,
z_min = T−Σ_interior z_a−z_max.
```

Accept iff both remaining values are nonnegative integers for some choice. The test handles a negative numerator, failure of exact division and exhausted slot total by rejection for that choice. When `T=0` only the all-zero tuple works, and when `d_W=1` there are no interior indices. The search bound on choices depends on the generator set and `ρ` only, with arithmetic on the requested integers. This proves termination and extraction. The full catalog has no asserted small or polynomial size. No count of all allocations follows from this support description.

## 8. Retained controls

**D167 at separation two.** Take `A=6,B=4,β=2,ρ=2`, so `ℓ=4,e=1`, `s=2k+2`, and `J=2k+5`. The source rows are `[0,k−1],[4,k+5]`, and the image rows `[0,k+5],[4,k−1]`. Include the four forced D167 neutral assignments at columns 0 through 3 in both `X,X′`, or remove them together with the four baseline cells in the lower source and image rows. The latter restriction replaces `|X_left|,|X′_left|` by their reduced counts and cancels the `−4` offset. Both residual matches now have common baseline intervals in their own directions, as in D167. Its lower maximum displacement is five and the generic long gap threshold is six. D167's sharper bound `k₀≤14F−8` from its own explicit marking after the forced cells is retained. Its boundary obstructions `q≥2` and `α_Z≥6` when `q=2` retain their geometry.

The saved symbolic D167 controls give all three permitted generators on their respective reservations. The D166 Case A gap from 10 to `k−1` has no active path and gives `(0,4)`. The D165 even-p construction with `Δ₁=5, Δ₂=2r+3, k=2r+6, r≥5` has one active path in each direction between 9 and `2r+5` and gives `(2,2)`. For even `k≥14` with `Δ₁=k−1,Δ₂=k−3` both paths in each direction cross the gap from 6 to `k−2`, giving `(4,0)`. The forced cells and extra left and tail anchors are outside the open interiors of those gaps. The generic arithmetic recovers the D167 cases. Empty and singleton sets give their exact cases. Two indices `a<b` give `aT≤U≤bT` with `U−aT≡0 mod (b−a)`. With `W={0,1,2}` take `z_1=U mod 2` and `z_2=(U−z_1)/2`; for `0≤U≤2T` the remaining `z_0` is nonnegative. Fixed exterior counts cancel when converting from gap to full quotas. [D167 proof and symbolic controls](ORDINARY_SPINE_EXCEPTIONAL_RESERVATION_SEMILINEAR.md)

**D164 target-0428 T at separation one.** The frozen terminal-free record at SHA-256 `8d8ac74c31b8903788db7e46f9385d5f7529ed2539870e0fb15717e318a53b28` binds original digest `6f4cc649a76e055160ade2e856544762df550e4f49235df0c17e181421760256`. Here `A=5,B=4,s=21,K=15,k=10,J=24,ℓ=4,e=1,ρ=1`. The exterior's named ports `s:27,s:28,s:29` carry reduced labels 5,6,0. The four actual first centers carry 1,3,4,2 in branch order and have displacements 3,1,0,2. The actual second centers `b:29:0,b:29:1` carry 7,8 and take 5,4 gap leaves, respectively. The original direct leaf `b:29:2` is exterior at 9. The actual reduced differences are `[1,9]` and every edge crosses.

The archived source rows are `[0,9],[4,14]` and image rows `[0,14],[4,9]`. The saved reservations yield:

```text
X  = {0,1,2,3,4,5,6,8}       X′ = {0,1,2,3,6,7,8,9}
Y  = {6,7,8,11}              Y′ = {4,5,7,9}
```

Surviving lower sources 7 and 9 map to H images 6 and 8 by P. Surviving upper sources `{4,5,9,10,12,13,14}` map into `{4,5,10,11,12,13,14}` by P at 9 and 10 and Q at the other five. These are the saved bits, with both terminal bits zero and the recurrence holding, so they reconcile the actual counts `(p_g,q_g)=(4,5)`. The graph counts give `x=2,y=4`. The marked columns here fill `[0,15]` because `X∪X′` fills `[0,9]` and the tail anchors fill `[9,15]`. This archived reservation type has no expandable gap. The available generator set on any separation-one geometry is contained in `{(0,2),(2,0)}`. Neither generator is inferred from this record. This check uses archived data only and leaves D164's historical disposition and the T question at target-0429 intact. [Frozen reconciliation and binding](../evidence/runs/d164-exceptional-four-first-001/RECONCILIATION.json)

## 9. Complete lifting, physical boundary and composition

At the requested size the old oriented labels and the exact fresh complement are

```text
L_old   = [A,A+c−1] ⊔ [A+c+s,A+n+s]
L_fresh = [0,A−1] ⊔ [A+c,A+c+s−1] ⊔ [n+s+A+1,m].
```

The exterior's shared root at `A` is already counted among the old labels. The shifted exterior fills the two end intervals of the complement. Gap source assignments use each gap coordinate once. Assign lower leaves by their recorded names. At each upper parent take its declared remaining actual leaf indices in order and pair them with its assigned coordinates in increasing order. This retains every original name, physical parent, edge and distinguishing branch index. All labels fill `[0,m]` bijectively. Old weights preserve their actual crossing classification and add `s` exactly on crossing edges. All exterior edges cross and gain `n+s`. Thus the weight partitions are

```text
D_old   = [1,d−2] ⊔ [d−1+s,n+s]
D_fresh = [d−1,d+s−2] ⊔ [n+s+1,m].
```

The exterior consumes the last band, and each exact gap image appears once and gives its corresponding weight in the first band. The old crossing band starts at least at `d+K−1`. The gap images below and at or above `K` split the remaining lower band at that threshold. Exterior weights all exceed it. The return is ordinary graceful with `w=0`, cut `C=c+K`, crossing weights `[d+K−1,m]`, and noncrossing weights `[1,d+K−2]`. Also `m=2C+2`, the exact `S₋₁` shape.

For the actual first-section boundary let `V_1` be the first-section fresh exterior vertices, and let `E_1` be the first-section exterior edges including the joining edge `vu`, excluding the unmade `uw`. Put `V_2` and `E_2` for their complements in the fresh exterior vertices and exterior edges, respectively. These sets come from the supplied named sections and their parent incidences. Denote the physical exterior labels of `V_j` by `F_j` and exterior weights of `E_j` by `W_j`, obtained by the stated upper-label shift and actual subtraction. Split the gap sources into `I_1,I_2` by the sections of their actual parents, including an eligible spine host at its correct section. Set `J_j=π(I_j)` from the reconstructed assignment. The partition of original vertices, with distinct sources and bijective images, makes each of `I_1⊔I_2` and `J_1⊔J_2` equal to `[0,s−1]`. The exact partial inventories are

```text
used labels        L_old ⊔ F_1 ⊔ (A+c+I_1)
remaining labels   F_2 ⊔ (A+c+I_2)
used weights       D_old ⊔ W_1 ⊔ (d−1+J_1)
remaining weights  W_2 ⊔ (d−1+J_2).
```

Split gap labels at source threshold `k` and exterior/old labels by their actual cut sides. Split both gap-weight sets by their images at `K`; the exterior sets `W_j` are entirely crossing and the old two bands give the old split. This is exact even when no gap image crosses. The literal unfinished connector is `uw∈E_2`. Since `u` is on the upper exterior side and `w=0`, its oriented assigned endpoints are `n+s+g_red(u),0` and its future difference is `n+s+g_red(u)`. Its crossing weight is reserved in the actual remaining inventory.

For an actual maximum-frontier input complement the output by `m−f`, returning the same named frontier at maximum. The actual output cut is `m−C+1` because cut equality is on the upper side. The actual old input had cut `n−c+1`. Subtracting the oriented translation from the total order increment `A+B+s` gives actual old shifts `B` below the actual input cut and `B+s` above or at it. In minimum polarity the shifts are `A,A+s`. Complement all partial label sets and connector endpoints consistently. Magnitudes and crossing status are preserved. This also verifies the exact two actual side memberships needed at later blocks.

For a finite admitted sequence each transition checks the incoming phase, size, actual port and inventories at its own boundary. All subsequent old embeddings preserve actual cut membership. Summing the subsequent actual lower shifts `Λ` and subsequent gaps `Σ` gives final label `g+Λ+Σ·1[g≥cut]` for an already assigned vertex at a complete boundary. Existing crossing weights gain `Σ` and other weights are fixed. The same transformation of the partial first-section used resources and the two reserved endpoints is valid through the complete current cut and all later ones. Taking exact complements in the final alphabets supplies remaining inventories, including the transformed crossing connector reserve. Thus one can emit immutable final-alphabet labels for each actual vertex, with no artificial section. The finite catalog, bounded arithmetic choices, finite expanded paths, terminal name assignment and finite list of blocks all terminate. No general admission of arbitrary sequences or decomposition of arbitrary topologies follows.

## 10. Strategic reassessment

D145 and D146 provide exact coefficient consumers on supplied D143 embeddings, with witness extraction and D146's rational series at fixed widths. D167 went further on its specified exceptional exterior by giving exact semilinear support with three generators. D168 gives the analogous exact support for every fixed separation of two eligible upper hosts on the supplied exceptional exterior, even with unequal row intervals. The constructive elements are the deterministic residual bits, reversible compression and explicit inventory-dependent bound. The results address different interfaces and neither coefficient positivity nor source supply follows from the other.

Further conditional allocation work, such as adding a third upper reflection, would require a new representation. Multiple incoming shifts need not determine a unique bit from the next cell count. That effort would still depend on an independently supplied physical exterior. Independent exterior supply now has higher leverage because the two-host allocation question is settled once the required geometry and lower inventory are supplied. The literature review's pinned two-host shell lift is a credible independent D157 initializer question. It must prove the correct actual extreme port, both palettes and exceptional crossing return when surplus leaves are restored. Ordinary shell gracefulness and the specified-endpoint correction for Krop do not supply those properties. Existing D157 initializers already give usable inputs in the present setting. Another initializer would leave the independently supplied fresh exterior as a separate requirement.

**One unstarted next action.** Under separate Owner authorization after Director review, seek independent terminal-enabled exterior supply, or a scoped no-supply proof, for D163's open corner `r=t=0,p≥3` on the prescribed original `(4,1,1),(2p,4,0)` family and its exact D157 exceptional transition. Preserve the fixed-geometry obstruction and the distinct `p=2` transported finite control. The falsifiable question is whether each such admissible original admits any compatible independently supplied terminal-enabled exterior in that arrangement. The current conditional result can assess a supplied geometry when it has exactly two eligible upper hosts. No hybrid campaign is needed for D168, and no successor has been prepared or run. The shell lift stays an unstarted strategic candidate. No historical novelty or change to unresolved primary-source checks is asserted. [D163 scope](ORDINARY_SPINE_EXCEPTIONAL_EVEN_SECOND_QUOTA_EXTENSION.md) · [Literature register](../docs/LOBSTER_LITERATURE_REGISTER.md) · [Research alignment](../docs/LOBSTER_RESEARCH_ALIGNMENT.md)
