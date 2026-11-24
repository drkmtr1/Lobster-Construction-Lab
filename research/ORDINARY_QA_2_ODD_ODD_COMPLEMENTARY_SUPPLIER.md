# D115 — Complementary allocation for independently varying odd left quotas

For every independently chosen pair of exact odd integers q≥5 and a≥3, the ordered original `[[q,a],[2]]` has a direct ordinary graceful labeling with physical `s:0=0`, `s:1=q+a+6` and `b:1:0=1`. Write `m=q+a+6`, `t=m/2`, `j=(a−3)/2`, `H=m−2` and `L=2`. The assumptions imply even m≥14 and nonnegative integer j.

## Original topology and independently supplied core

The actual spine is `s:0--s:1`. The centers `b:0:0`, `b:0:1` and `b:1:0` attach to `s:0`, `s:0` and `s:1`, respectively. Each terminal `l:i:j:k` is adjacent only to its named center `b:i:j`. The terminal index ranges are `0..q−1`, `0..a−1` and `0..1`. These distinct original names yield two spine vertices, three centers and q+a+2 terminals. Each added center or terminal has a single edge to the previously named part, so the graph is a tree. It has m+1 vertices and m actual edges, each of multiplicity one. Centers are one edge from the spine and terminals are two edges away.

The core consists of both spine vertices, the three centers, the first and last second-left terminals, and the two right terminals. Its eight actual edges are the spine, three attachments and four terminal edges. The first and last second-left terminals are distinct since a≥3. The specified attachment structure gives a connected acyclic nine-vertex subtree. Supply the labels below directly from the parameters.

| Actual vertex or group | Label or indexed labels |
| --- | --- |
| `s:0,s:1` | `0,m` |
| `b:0:0,b:0:1,b:1:0` | `m−2,2,1` |
| `l:0:1:0,l:0:1:(a−1)` | `3,m−1` |
| `l:1:0:0,l:1:0:1` | `m−4,m−3` |

The occupied labels are `[0,3] ⊔ [m−4,m]`, once each. The actual spine has weight m. The first-left, second-left and right attachments have weights m−2, 2 and m−1. The two second-left terminal edges have weights 1 and m−3, and the two right terminal edges have weights m−5 and m−4. This supplies `{1,2} ⊔ [m−5,m]`, once each. Taking complements in the complete alphabets leaves

```text
R = [4,m−5]
D = [3,m−6].
```

They both have m−8=q+a−2 elements. The vacancies are the entire first-left group, q positions at the higher host, and second-left indices 1 through a−2, giving a−2 positions at the lower host. The labels and occupied differences of the core are fixed before any of these slots are filled.

## Difference components and integral allocation

Each x in R is strictly between L and H. Its two absolute options are `d_H(x)=m−2−x` and `d_L(x)=x−2`. The map `d_H` bijects R onto D, taking 4 to m−6 and m−5 to 3. The reflection `rho(x)=m−x` exchanges the options, with `d_H(rho(x))=d_L(x)` and the reverse equality. Label 4 is forced to H because its lower weight 2 is used and its higher weight m−6 is available. Its reflected partner m−4 belongs to the core.

On `[5,m−5]` both options lie in `[3,m−7]`. The reflection preserves this interval and fixes exactly t, which is an available integer since m≥14 is even. The two options at t equal t−2. The other labels in the interval give pairs represented by `x=5,...,t−1`, with partners strictly above t. Their number is `c=t−5=(q+a−4)/2`. Each pair gives two parallel edges on the two different vertices `d_H(x),d_H(rho(x))`, with opposite host tags. The midpoint gives one loop with two host choices, and 4 gives a single forced higher-host half-edge. The images under the bijection `d_H` show that these difference-vertex groups are disjoint and cover all of D. Every label has at least one eligible option. In each pair there are two labels for two differences, and the forced and loop components each have one label for one difference. Thus each component satisfies `e_K+t_K=n_K` with the loop counted as one edge.

The [adopted R226 revision-2 theorem](../references/upstream/mdl/N226_R226_two_host_completion.md#n226-closeout) applies to this independently labeled tree core with injective labels in `[0,m]`, distinct positive actual differences, distinct named hosts in lower/higher order and exactly the prescribed pendant extensions. Its residual label equations and difference equations apply to the complete complements R and D. With the physical second-left center as the first, lower host, `A0=0`, `c=(q+a−4)/2` and `eta=1`. The quota-free integral projection is

```text
p(P_Z) = {2k+epsilon : k is an integer, 0≤k≤c, epsilon∈{0,1}}.
```

The required lower count a−2 equals `2j+1`. Since j≥0 and `c−j=(q−1)/2≥2`, the choice `k=j, epsilon=1` is in range. Take the midpoint and the j pairs closest to it at the lower host. Their labels form the interval `I=[t−j,t+j]`, with exact endpoints `(q+9)/2` and `(q+2a+3)/2`. Indeed `t−j=5+(c−j)` and `t+j=m−5−(c−j)`. These bounds prove containment in `[5,m−5]` without comparing q to a. The endpoints add to m, so reflection preserves I. There are `2j+1=a−2` labels in I, exactly t and j complete pairs. Its complement in R has `(q+a−2)−(a−2)=q` labels and consists of the remaining pairs and forced label 4. Put I at the lower host and the complement at the higher host. This meets both actual integral quotas.

## Indexed formula and direct inventories

Assign the increasing list of `R \ I` to all first-left terminals in index order. At the second-left center keep label 3 at index 0 and m−1 at index a−1, and assign I in increasing order to indices 1 through a−2. Keep the spine, centers and two right terminals as in the core. The two residual lists exhaust R without repetitions. With the core labels they give the complete label bijection onto `[0,m]`.

Independently of R226, each of those first-left incidences carries weight `d_H(x)` for its assigned label x, and each second-left vacant incidence carries `d_L(x)`. Since `d_L=d_H∘rho` on I and rho permutes I, the two image multisets `d_L(I)` and `d_H(I)` are equal with multiplicity. The direct residual weight partition is therefore

```text
d_H(R \ I) ⊔ d_L(I) = d_H(R \ I) ⊔ d_H(I) = D.
```

The disjointness and multiplicity one follow from the bijection of `d_H`. These weights together with the occupied weights exhaust `[1,m]`. The named vertices and edges are those of the original, its spine remains a witness, and the unused label and difference inventories are empty.

First require both parameters to have exact integer type, the stated lower bounds and odd parity, rejecting booleans and other inputs outside the domain. Emit the fixed core, walk R once to assign its complement of I in order, and fill the remaining second-left positions with I in order. Construct each named terminal edge to its own center from the corresponding finite index range. This writes q+a+7 labels and q+a+6 incidences in O(q+a) indexed output operations. The choices are explicit and no search is involved.

Orient from the traversal class containing `s:0`. The even class consists of the entrance, the right center and all left terminals. The odd class contains the exit, the two left centers and the two right terminals. Every left terminal directed into the higher center has a smaller label than that center. The right terminals are above the right center, and every spine or attachment incidence has positive signed difference. Exactly the a second-left terminal incidences directed into center 2 are negative. Their respective differences are `−1`, the descending sequence from `2−(t−j)` to `2−(t+j)`, and `3−m`. The signs describe the output.

## Retained boundary and growth premises

At a=3, `m=q+9` and `j=0`. The last second-left terminal has index 2 and I is the singleton `{t}`. The entire core, both residual allocations in index order, physical pins and the actual original graph agree with [D113](ORDINARY_Q3_2_ODD_COMPLEMENTARY_SUPPLIER.md) throughout its odd q domain. This specialization is symbolic. At (q,a)=(5,3) the first-left list is `(4,5,6,8,9)`, second-left `(3,7,13)`, right `(10,11)`, spine `(0,14)` and centers `(12,2,1)`. These agree at every name with the [frozen D111 ledger](../evidence/validation/LCL_ORDINARY_53_2_DIRECT_SEED_001/result.json), the sole executable boundary.

In every supplied seed, `s:1` ends the actual witnessing spine and has exact neighbor set `{s:0,b:1:0}`. The predecessor carries zero, the off-spine neighbor carries one, and the exit carries the maximum m. This verifies [D112](ORDINARY_EXTREME_SPINE_GROWTH.md)'s conditional growth premises. The corresponding three-parameter application would have ordered profile `[[q,a],[r]]` with these odd q and a domains and integer r≥2. The proved scope here is the seed and its compatibility. Other parity combinations, wider center multiplicities and ordinary composition remain separate.
