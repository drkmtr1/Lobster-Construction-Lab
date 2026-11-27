# D223 — Affine cycles and independent cross-interior odd supply

**PARTIAL POSITIVE WITH UNBOUNDED MULTIPLICITY.** The two arbitrary named interior quotas are independently supplied at every registered split with h=5,6,7,8 and at every registered split with ℓ≥4. The D222 single-quota route covers either parameter equal to one at all sizes. Both exact proposed diagnostic interfaces have symbolic positives. No dormant diagnostic was needed. [Named controls](../evidence/validation/D223_AFFINE_CYCLE_CROSS_INTERIOR_ODD_SUPPLY/HAND_CONTROLS.md).

## 1. Exact resources and affine cycles

In the original T, the literal spine is s:0--s:1--s:2--s:3. The branch b:i:u at each original index u attaches to s:i, and each indexed terminal l:i:u:e attaches to its own branch. In S change only the two exterior center attachments inward to s:1 and s:2. All actual names, terminal parents and three spine edges persist. Use the D217 fixed-label reconstruction criterion. In the constructions here the two altered weights exchange. [D217](MARKED_DIAMETER_FIVE_EXTERIOR_RECONSTRUCTION.md#2-exact-criterion-on-a-supplied-source).

Write ℓ+j=2h−3, F for the terminal count and m=2h+2+F. Fix folded roots 0,m and slots [1,h+2] ∪ [m−h+1,m−1]. Assign the h−1 complementary pairs {k,m−k}, k=1,...,h−1, wholly to one root each. The left requires (ℓ+2)/2 pairs and the right (j−1)/2 pairs together with the unpaired low slots h,h+1,h+2. The two spine-end reserves a,b are among these slots and carry no terminal. The skeleton weights are [1,h−1] ∪ [m−h−2,m] on S. The available labels [h+3,m−h] and weights [h,m−h−3] each have length F. These facts are the D222 s=1 band arithmetic. In exact coordinates i=z−(h+3), w=difference−h, the rules are
```text
low k:       w=i+3−k
high m−k:    w=F−1−k−i .
```
All terminal labels lie strictly between the low and high bands, so these are actual endpoint differences. If the original quotas are mapped to allowable slots on their respective physical sides, a terminal allocation is precisely a permutation i→w of [0,F−1] with each arc labeled by its actual host and with the specified number of arcs at each host. A permutation decomposes into vertex-disjoint directed cycles, including fixed rows. Conversely, a system of disjoint cycles covering all coordinates and meeting the actual host quotas gives both complete palettes by assigning the cycle sources at each host to its distinct indexed terminals. No cycle requires a graph edge between numerical resources. Only each recorded host-terminal edge is installed in the original. [D222](PARITY_COMPATIBLE_ALL_ODD_SUPPLY.md#2-complementary-bands-with-general-imbalance).

If A_j(i)=ε_j i+t_j, with ε_j∈{−1,1}, define ε=ε_s⋯ε_1 for s maps in traversal order and T_*=Σ_j t_j∏_{l>j}ε_l. The composite is εi+T_* by induction. Closure is exactly (1−ε)i=T_*: for ε=1 it requires T_*=0 and places no additional constraint on i, and for ε=−1 it fixes i=T_*/2, which must be integral. Closure alone supplies neither a simple admissible cycle nor disjointness, full resource coverage or quotas. These checks are separate below.

## 2. Shared insertion and its exact limitations

A compatible old pair of cuts (I,W) has thresholds 0≤I,W≤F. For every low row, i≥I iff w≥W. For every high row, i≥I iff w<W. Increasing F by G and shifting each old coordinate above its respective threshold by G preserves both affine formulas. The low row shifts on both coordinates or neither. The high row shifts on exactly one coordinate. Conversely these threshold conditions are necessary for a positive insertion with this old-row transport and fixed offsets.

The fresh intervals start at I,W and both have length G. At a low host k the fresh map in interval coordinates u=i−I, v=w−W is v=u if and only if W−I=3−k. At a high host m−k it is v=G−1−u if and only if I+W=F−k. These are also the exact full-interval conditions at the two types of host for G>0, by comparing the endpoints. If both hold, the reflection u↦G−1−u splits the fresh inventory into two-element orbits for even G. Choosing α whole orbits for the low and β for the high gives independently arbitrary increments 2α and 2β, with G=2(α+β). A whole orbit uses the same coordinates as labels and weights at either host. For G=0 the new intervals are empty. The D222 singleton rule for odd G remains local to the same insertion mechanism.

Let H_+ count high rows and H_<I the high rows with input below I. The outputs below W are from the I−H_<I low-prefix rows and from the H_+−H_<I high-suffix rows. Hence W−I=H_+−2H_<I. In particular the numerical low recipient k satisfies k≡3−H_+ modulo 2 and the high offset k satisfies k≡F−H_+. For an all-unit (or all-odd quota) imbalance-three seed with one high reserve, H_+≡h−2 and F is odd, so both recipients have offset parity h+1. Without the quota-count assumptions, use the general congruences. These congruences neither assert any required cut exists nor select legal physical hosts.

For multiple dedicated gaps indexed by j, take distinct input cuts I_j, distinct output cuts W_j, and independently varying positive widths G_j, matched by the same j. Assume ordinal transport of old ranks, fixed affine offsets and a full fresh input interval assigned to its matched output interval by one host map. The new starts are I_j+Σ_{l:I_l<I_j}G_l and W_j+Σ_{l:W_l<W_j}G_l. Their difference must stay constant for a low identity map. Independence forces the predecessor coefficients for each other l to be equal. For a high reflection map their sum must be F−k+Σ_{l≠j}G_l, so those same two coefficients must sum to one. These statements follow by varying one positive width at a time. Thus each identity gap requires the same order against every other gap, and each reflected gap requires opposite order against every other gap. In particular a low identity and a high reflection at distinct dedicated gaps are incompatible under these premises, as their single comparison would need both orders. Two maps sharing one gap can evade that comparison, as the single-gap suppliers show. This does not classify several dependent widths, movable assignments, variable offsets or other graceful supply. The distinct-cut and exact span hypotheses of D212, and the D213 graph component bound, retain their own scopes. [D212](SIMULTANEOUS_SAFE_GAP_QUOTA_GROWTH.md) · [D213](ALL_CENTER_SAFE_GAP_STRUCTURAL_LIMIT.md).

## 3. The h=5 cycle suppliers

Both use a=m−1, b=7, c=3, d=4. Left pairs 1 and 3 are fixed and pair 4 is right. In (2,5), pair 2 is right and the two remaining unpaired low slots 5,6 are right interior hosts. The left interior roles are 1,m−3. The right roles are 2,5,6,m−4,m−2. The exact exterior exchange is 3 with m−4: m−1−3=m−4 and 7−4=3. For (4,3) move both unit hosts in pair 2 to the left. This exchanges that pair's two attachment differences while preserving all terminal assignments.

### A. One variable left quota and both flank growth parameters

Let F=9+2v. Use the four-cycle F−3→F−1→F−4→0→F−3 on hosts 1,6,m−3,m−2 respectively, by the shifts +2,−3 and the two high formulas. Use F−2 at host 3 by identity. These five distinct coordinates leave [1,F−5], of endpoint sum F−4. High m−3 reflects in this sum. Remove v full outer pairs for that host, leaving [l,l+3] with l=v+1. On it take the cycle
```text
l → l+2 → l+3 → l+1 → l
    m−4      2       5      4
```
where the four hosts are read on successive arcs. High m−4 indeed reflects l to F−5−l=l+2, and the other shifts are +1,−2,−1. All arcs cover the exact alphabet once in both coordinates. The sole enlarged seed quota is 1+2v at high m−3.

Use I=l+2,W=l+1. In the four-cycle of middle coordinates the low inputs l+2,l+3 map at or above W and the low input l+1 maps below W. The high input l maps at or above W. In the outer cycle and identity row the low inputs and outputs are all above their respective cuts, and the high rows cross in opposite directions. Removed reflection pairs have one index ≤v and one ≥v+5, so their high rows have the required opposite thresholds as well. W−I=−1 and I+W=F−4 supply independent even growth at low 4 and high m−4. Then enlarge low 3 independently by 2r. Increase F by 2r, move every existing index and weight up by r, and give the two fresh identity intervals [0,r−1] and [F+r,F+2r−1] to host 3, using pre-operation F. Both maps and full palettes persist, also for r=0.

The family is `[[1+2r],[1,1+2v],[1,1,1,1+2β,1],[1+2α]]` for independent nonnegative r,v,β,α. The companion has four left roles including the two unit moved hosts, and right roles 5,6,m−4 with only the last variable. In each case the chosen actual left and right branches can occupy the variable roles.

### B. Both selected left quotas enlarged with a unit right flank

Use nonnegative u,v,β, F=11+2(u+v+β), and the cycles 0→1→F−4→0 at hosts 2,m−2,m−3 and F−5→F−3→F−1→F−2→F−5 at hosts 1,1,4,6. The affine rules give every arrow and the seven visited coordinates are distinct since F≥11. The remainder [2,F−6] has length 4+2(u+v+β), endpoint sum S_*=F−4, and even length.

A packet starting at the smallest a of a symmetric interval uses a→a+2→S_*−a−2→S_*−a→a at hosts 1,m−3,1,m−3. Two packets with starts a,a+1 use the first four and last four positions, disjointly. The same host rules give both cycles. For ε=u mod 2, take (u−ε)/2 such double packets. If ε=1, let a be the smallest remaining coordinate before the last single packet. Use that packet and also the pair {a+1,S_*−a−1} at high m−3. Together they use three coordinates at each end, all distinct. Every packet keeps the remaining interval centered at S_*. For v≥u+ε, the (u−ε)/2 double packets can all run with at least four coordinates left after each step. For the odd final packet plus pair the current length is at least ten: after all double packets it equals 4+2(v−u+β)+4ε, with v−u≥1 when ε=1. This proves the required margins, including u=0 and all minimal quotas. The high m−3 has now used 2u+2ε extra rows. Give it v−u−ε additional symmetric outer pairs, a nonnegative number, leaving precisely 4+2β coordinates. Each step is finite and its symmetric trimming leaves the prescribed remainder.

Call the remainder [l,U]. When β=0, use the two-cycle l↔l+2 at low 1 and 5, the fixed row l+1 at high m−4, and U at identity host 3. The high row is fixed since 2(l+1)=S_*−1. For β≥1, use U−2↔U at lows 1 and 5, and low 3 at l+1. These three coordinates are distinct because U−l=3+2β≥5. On [l,U−1] the reflection sum is S_*−1, and the two excluded coordinates U−2,l+1 reflect into each other. The remaining 1+2β coordinates therefore give a complete set of high m−4 rows with no conflict.

Counting the fixed cycles, packets and final rows gives quota 3+2u at low 1, 1+2v at high m−3, 1+2β at high m−4, and one at every other host. Enlarge low 3 by any 2r as in A. Given two enlarged odd left quotas, put the smaller at low 1. Then 3+2u≤1+2v implies v≥u+1, sufficient for the packet rule. Thus both selected left branches may independently have any odd quotas ≥3, along with one arbitrary odd right interior quota and an arbitrary odd left flank, with right flank one. The construction also covers its stated parameter boundaries when v=0 and u=0. Pair 2 remains unit, giving the (4,3) companion with both other left quotas one.

### C. Exact D222 target

The named 27-edge candidate `[[3],[3,3],[1,1,1,1,1],[1]]` is precisely the u=0,v=1,β=0,r=1 instance of B with the prescribed name order. The independent hand record subtracts every actual endpoint in S and T and verifies their complete alphabets and spectra, including the 3↔23 restoration. This positively resolves the exact D222 proposed interface. [Full named check](../evidence/validation/D223_AFFINE_CYCLE_CROSS_INTERIOR_ODD_SUPPLY/HAND_CONTROLS.md#2-exact-d222-discriminator-positive).

## 4. Supplied h=6 and h=7 seeds

At h=6 the proposed marks are (0,25,23,6,2,4). Pair 2 contains the left reserve 23 and the left exterior 2. Pair 1 contains two left interior hosts including recipient m−1. Pair 4 is right, with its low exterior host 4. The right reserve 6 is unpaired, and low 7 is an actual right interior. Since m−2−2=m−4 and 6−4=2, the pair exchanges. The normalized named seed in the hand record has every i,w in [0,10] once. Its low-prefix rows for I=7,W=3 have (i,w)=(2,2),(4,0),(6,1), and all other low rows are above both cuts. All high rows have i<7 and w≥3. W−I=−4=3−7 and I+W=10=11−1 supply both recipients. For splits (2,7),(4,5),(6,3), retain compulsory pairs 1,2 left and 4 right. Assign the free pairs 3,5 in the quantities (ℓ−2)/2 left and the rest right. The chosen physical recipients never change sides.

At h=7 the marks are (0,29,28,9,4,5). Pairs 1,4 go left and 5 right. The high m−4 is left interior in pair 4, and low 8 is unpaired right interior. The exchange follows from m−1−4=m−5 and 9−5=4. At I=7,W=2 the low-prefix pairs are (1,0),(6,1), every other low is above both cuts, and the five high rows have i<7,w≥2. The recipient equations are W−I=−5=3−8 and I+W=9=13−4. For (2,9),(4,7),(6,5),(8,3), place the free pairs 2,3,6 in the quantities (ℓ−2)/2 left and the rest right. This preserves the physical roles. The hand record gives full labels and weights for each base and an unequal growth example at each size. Any chosen actual interior branch in its own side can occupy the receiving slot.

## 5. Exact h=8 interface and its bounds

For h=8,F=15,m=33 the high band is [26,32], of seven slots, and the low band is [1,10]. The shorter [27,32] omits the complementary slot of 7 and is not the registered geometry. Use the proposed marks (0,33,31,8,3,5), pairs 2,3 left and pair 5 right. The left interior recipient is m−3 from the pair of the left exterior 3, and low 9 is unpaired right interior. In the registered (2,11) split these are the only compulsory left pairs. The exchange is 3↔28 from 31−3=28 and 8−5=3.

Here is a direct allocation. Use upper input declines j_*=14−i for low suffix rows and upper weight declines q_*=14−w.

- In low host order (1,2,3,5,6,7) use j_*=(2,5,1,4,0,3). Their q_* are (0,4,1,6,3,7), respectively.
- The remaining low hosts (4,9,10) use (i,w)=(2,1),(8,2),(7,0).
- At high offsets (1,3,4,5,6,7) use i=(1,5,6,0,3,4), giving q_*=(2,8,10,5,9,11).

The upper-input set is [9,14]. The three low-prefix inputs and six high inputs partition [0,8]. Their outputs comprise [0,2] at the three low-prefix hosts and the disjoint upper decline sets giving [3,14] for all other rows. Thus all 15 labels and weights occur once. I=9,W=3 are compatible, with W−I=−6=3−9 and I+W=12=15−3. Section 2 proves the all-even-width transport and independent increases of the two actual odd quotas. Both named 33-edge graphs and endpoint spectra are in the hand record. The row at low 9 with i=8,w=2 also gives an adverse control for proposed cut (8,4), which would otherwise have the recipient equations for low 7 and high m−3. At that cut the low row has i≥8 but w<4. For all other h=8 splits (4,9),(6,7),(8,5),(10,3), place the free pairs 1,4,6,7 in the required side quantities, retaining the compulsory pairs. This preserves both recipients and all weights.

The broader conditional registration allowed all valid distinct a,c on the left and b,d on the right, either D217 restoration mode, and either orientation of the two types of receiving host across the two interiors. Before testing legality, the bound is binom(7,2)·4·3·13·12=39,312. For each such choice there are at most 2·11 left/right branch choices, so at most 864,864 marked role choices when charged by disjoint branches, with each role type then determined by its numerical slot. The numerical key (a,b,I,W) determines the host set by removing a,b and fixes every row predicate, because all quotas are unit, the two affine types depend only on actual numerical slots, and compatibility depends only on the cuts. Each lawful lift records the actual named a,b,c,d, side placement, restoration mode and receiving hosts. The lift must independently satisfy the two recipient formulas with hosts in the opposite physical interiors. Keeping at least one such lift for a key is sufficient for existence: any good numerical assignment on the key lifts to it by assigning its single terminal per slot. No invalid marked assignment becomes an admissible lift. One could keep all lifts without changing the shared numerical predicate. Omitting side, c,d and role orientation from the numerical key is justified only with this separation.

There are at most 17·16 ordered distinct reserve pairs and at most 10·7 possible ordered choices of low label k and high offset k′. The equations W−I=3−k and I+W=F−k′ give at most one (I,W) per such role choice, so the key cap 19,040 holds. Each key has at most 15·15 raw host/index rows before checking weight range and cuts. This gives 4,284,000 raw row attempts. For an exact cover of host, index and weight classes one row consumes a unit host, so at most 15 selected rows and 16 live frames including the root. The remaining proposed CPU, elapsed, node and evidence limits would cap work including audit and temporary evidence, and would not guarantee exhaustion. An interruption would remain incomplete. The symbolic positive decides this exact registration, so there is no frozen runner, scientific source, test run or execution claim.

## 6. Repeatable unbounded construction for every ℓ≥4

This construction supplies unit seeds at all h≥5, then enlarges exactly the two desired actual branches. It uses numerical role transport before assigning names to the final target and never requires a previously solved original with enlarged quotas.

Use reserves a=m−(h−2), b=h, and exterior centers c=1, d=h−1, with roots 0,m. The folded weights 1,m−h+1 exchange because a−c=m−h+1 and h−(h−1)=1. Put pairs 1,h−2,h−3 left and pair h−1 right. These indices are distinct for h≥5. The three mandatory left pairs fit exactly when ℓ≥4, and the one mandatory right pair fits even at j=3. The remaining pairs are allocated to meet the required side counts. The unpaired b=h is the right spine end. The high offset h−3 is a left interior host, and low h+1 is unpaired right interior. They are never exterior hosts or reserves. The other roles are all unit, so select the actual two named branches first and put them at those slots, then use increasing pair and branch order for the others.

For F=2h−1 we maintain a complete normalized unit assignment with compatible cuts (I,W)=(h,2). The low 2 row is (i,w)=(0,1), and the low 1 row has upper input decline j_*=2 and weight decline q_*=0, with declines taken from F−1. At h=5,6,7 the following table gives the base seeds. In every base, low h+2 uses (i,w)=(h−1,0) and low 2 has its fixed row. The high column gives (offset k,input i). The upper low column gives (host k,input decline j_*). Convert all weights by actual affine maps, using q_*=i+k at high rows and q_*=j_*+k−3 at upper low rows.

| h | High rows (k,i) | Upper low rows (k,j_*) |
|---:|---|---|
| 5 | (1,1),(2,3),(4,2) | (1,2),(3,1),(4,3),(6,0) |
| 6 | (1,1),(2,2),(3,4),(5,3) | (1,2),(3,3),(4,0),(5,4),(7,1) |
| 7 | (1,1),(2,5),(3,2),(4,4),(6,3) | (1,2),(3,3),(4,0),(5,4),(6,1),(8,5) |

Each high input list uses [1,h−2] once and each upper input decline set is [0,h−2]. Together with the two fixed low rows these are all inputs. The upper weight declines of high and upper low rows are respectively {2,5,6} and {0,1,3,4} for h=5, {2,4,7,8} and {0,1,3,5,6} for h=6, and {2,5,7,8,9} and {0,1,3,4,6,10} for h=7. Each pair partitions [0,2h−4] and therefore gives [2,F−1]. The two lower weights complete the alphabet. Every high row is below I and at or above W, every upper low is above both, and the other two lows are below both. The recipient formulas hold for low h+1 and high offset h−3, since W−I=3−(h+1) and I+W=F−(h−3).

### Induction from h to h+3

Use F′=F+6, and increase every old low host and every old high offset by three, including the numerical reserve slots. The old low reserve b=h becomes h+3 and the old high reserve offset h−2 becomes h+1, exactly the new reserves. First omit the old row at low 2. Carry every other old row to its shifted host with i′=i+3,w′=w. The low map holds because i and k increase equally. The high map holds because F grows by six and i and k each grow by three. The carried input set is [4,F+2], since the omitted row was i=0, and its weight set is [0,F−1] minus 1. Return (0,1) to the new actual low 2.

The remaining low hosts for the new rows are 1,3,5. The first two are newly available and 5 is the shifted old low 2 whose old row was omitted. The new high offsets are 1,2,3. Use these rows, with upper declines taken from F′−1=F+5.

| New role | Input choice | Upper weight decline |
|---|---|---:|
| Low 1 | upper input decline 2 | 0 |
| Low 3 | upper input decline 1 | 1 |
| Low 5 | upper input decline 0 | 2 |
| High offset 1 | index 2 | 3 |
| High offset 2 | index 3 | 5 |
| High offset 3 | index 1 | 4 |

The explicit shifts give all six differences and distinct indices. The three high indices cover 1,2,3 and the upper indices cover [F+3,F+5]. The six weight declines fill exactly the new weights [F,F+5]. Together with the fixed returned row and carried old rows both new palettes are full. All shifted old rows preserve their input inequality when I increases by three and W remains 2. The new high rows are below the new I, with outputs ≥2. The new upper lows are above both cuts, and (0,1) remains a lower low. The low 1 and low 2 invariants have returned exactly. The high recipient moves from offset h−3 to h and the low from h+1 to h+4, both the corresponding new roles. Reassigning reserves and exterior names according to the stated marks keeps the two actual reconstruction edges. The induction never requires the nonreceiving rows to retain the same physical names across auxiliary sizes.

Starting from the base h in {5,6,7} congruent to the input h modulo three and performing finitely many steps gives the needed unit assignment. After assigning the actual physical roles, apply the shared gap with independently arbitrary even increases at the two recipients, leaving every other branch unit. Large terminal labels and offsets in the skeleton are interpreted at the final m. The two actual exterior differences exchange after every enlargement by the same arithmetic. All original indexed vertices appear once and no auxiliary slots survive on the finished graph.

## 7. Scope and disposition

For unit flanks and at most the specified two enlarged quotas, the proved coverage is all registered splits at h=5,6,7,8 and all ℓ≥4 for every h≥5. The accepted D222 direct matching construction additionally supplies either selected quota equal to one at every multiplicity. The unresolved complement in this registration is therefore ℓ=2, h≥9 (j=2h−5), with both selected interior quotas ≥3. The repeatable construction in Section 6 needs three prescribed left pairs and cannot be assigned on that side count as stated. The h=8 positive proves that more general marking can fit two left pairs, but the proof does not produce a repeatable assignment of those roles for ℓ=2.

All constructions include physical spine reversal by mapping section i to 3−i and retaining the original branch and terminal indices within the transported section. For a single target record all final assignments on the actual named original, and pair names by that explicit isomorphism for its reversal. The larger h=5 A and B families retain their exact additional quota domains. The prior accepted all-even and all-odd obstructions, D212 incomplete certificate questions, held closure and insertion, and deferred D207 remain in their separate scopes. The exact D222 proposed discriminator and the exact h=8 interface here are both positively resolved by hand. No new discriminator was substituted. No scientific execution, diagnostic preparation, solver, protected checker or dependency installation occurred.
