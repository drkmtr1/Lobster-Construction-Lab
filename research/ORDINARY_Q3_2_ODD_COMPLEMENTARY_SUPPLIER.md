# D113 — Odd first-left quota by complementary allocation

For every exact odd integer q≥5, the ordered original `[[q,3],[2]]` admits a direct ordinary graceful labeling at the physical pins `s:0=0`, `s:1=q+9` and `b:1:0=1`. The construction assumes no alpha cut or signed-edge condition.

## Named original and independently supplied core

The actual spine is `s:0--s:1`. Centers `b:0:0`, `b:0:1` and `b:1:0` attach to `s:0`, `s:0` and `s:1` respectively. Each terminal `l:i:j:k` attaches to its own center `b:i:j` alone. The three index ranges are `0..q−1`, `0..2` and `0..1` in that order. The spine edge, three center attachments and q+5 terminal edges give `m=q+9`. Every vertex name is distinct, and each center or terminal attaches by one edge to the part already named. This is a connected tree on q+10 vertices, with every center and terminal at distance one and two respectively from the given spine.

Put `A=q+7`, `B=2` and `t=(q+9)/2`, where A and B denote the labels of `b:0:0` and `b:0:1` respectively. The core is the actual subtree containing both spine vertices, all three centers, second-left terminals at indices 0 and 2, and both right terminals. Its nine vertices and eight actual edges are prescribed by these names before allocation. In particular it is connected and acyclic, as deleting the other terminal leaves preserves the unique paths among core vertices. Supply the following labels directly.

| Named vertex or group | Label or indexed labels |
| --- | --- |
| `s:0,s:1` | `0,q+9` |
| `b:0:0,b:0:1,b:1:0` | `q+7,2,1` |
| `l:0:1:0,l:0:1:2` | `3,q+8` |
| `l:1:0:0,l:1:0:1` | `q+5,q+6` |

The occupied labels are the disjoint bands `[0,3] ⊔ [q+5,q+9]`, without repeated entries. On the spine, the first and second left attachments and the right attachment, the weights are q+9, q+7, 2 and q+8 respectively. The two supplied second-left terminal edges give 1 and q+6. The right terminals give q+4 and q+5. Thus the occupied weights are exactly `{1,2} ⊔ [q+4,q+9]`, without repeats. The core inputs require no prior complete labeling.

The vacant original positions are every first-left terminal and `l:0:1:1`. They have residual quotas q at the first center and one at the second. Taking the two complements in the full alphabets gives independently supplied residual labels `R=[4,q+4]` and differences `D=[3,q+3]`, each of size q+1.

## R226 components and integral quota

All x in R satisfy `B<x<A`. Thus the two possible absolute differences are `d_A(x)=q+7−x` and `d_B(x)=x−2`, with sum q+5. The map `x↦d_A(x)` is a bijection from R to D, including the endpoints `4↦q+3` and `q+4↦3`. Reflection `rho(x)=q+9−x` exchanges those options because `d_A(rho(x))=x−2` and `d_B(rho(x))=q+7−x` wherever both labels are considered. Here B is R226's lower host and A its higher host.

- At x=4, the B option 2 is already occupied and the A option q+3 is available. The reflected label q+5 is already occupied. This gives one forced high-host half-edge at difference q+3.
- Reflection preserves `[5,q+4]`, swapping its endpoints. Both options for every label in this smaller interval belong to `[3,q+2]`. Since q is odd, `t=(q+9)/2` is integral and `5<t<q+4` for q≥5. It is the only fixed point. Both options there give t−2, so the midpoint contributes one loop with two host choices at that difference.
- The remaining pairs have representatives `x=5,...,t−1` and distinct partners `rho(x)>t`. There are `t−5=(q−1)/2` such pairs. Each has two labels with reversed host tags at the same two distinct difference vertices. In fact these difference vertices are `d_A(x)` and `d_A(rho(x))`. The bijectivity of `d_A` shows that the vertex sets from distinct pairs, the midpoint and the forced label are disjoint and cover all of D. Therefore they are exactly the multigraph components.

The two parallel edges in each pair give two labels on two vertices. The midpoint gives one loop on one vertex, and the forced singleton gives one half-edge on one vertex. Every label has an eligible option and each component satisfies `e_K+t_K=n_K` in the [adopted R226.1 revision-2 theorem](../references/upstream/mdl/N226_R226_two_host_completion.md#n226-closeout). The named core meets that theorem's input conditions with eight edges and the required q+1 fresh terminal incidences at two distinct actual hosts. There are no forced assignments to the lower host, so `A0=0`, `c=(q−1)/2`, `eta=1`. Its quota-free integral projection onto the lower-host count is

```text
p(P_Z) = {2j+epsilon : j is an integer, 0≤j≤c, epsilon∈{0,1}}.
```

A whole pair contributes either zero or two to the lower host. The required quota one is attained at `j=0, epsilon=1`. Allocate every pair and the forced label to the higher host, and the midpoint to the lower host. The higher count is `2c+1=q`. These counts specify an integer allocation to the actual host slots.

## Indexed labeling and direct verification

The first-left terminal labels are the increasing list of `[4,q+4] \ {t}` assigned to the indexed terminals `l:0:0:0` through `l:0:0:q−1`. The full second-left group in index order is `(3,t,q+8)`, the right group is `(q+5,q+6)`, and the spine and center labels are as in the core. The disjoint core and residual labels fill `[0,q+9]` once. The absolute weight from assigning any residual label to A would be `d_A(x)`; the one allocated to B has `d_B(t)=d_A(t)`. Thus the actual terminal weights fill D bijectively by the same map, independently of the R226 quota projection. The occupied and newly supplied weights exhaust `[1,q+9]` once. Both inventories are empty and the original labeled incidences retain their named roles.

The supplier first requires `type(q) is int`, `q≥5`, and odd parity, rejecting booleans, nonintegers and other values outside the domain. Generate the prescribed indexed original, write its fixed core labels and visit `[4,q+4]` once, skipping t for the increasing first-left list. Fill the one second-left vacancy with t. The ranges terminate and write q+10 labels and q+9 incidences in O(q) indexed output operations, with no assignment enumeration or solver.

Orient from the traversal class containing `s:0`. The even class consists of `s:0`, the right center and all left terminals. The odd class consists of `s:1`, both left centers and the right terminals. The three second-left terminal edges, directed toward center 2, have signed differences `−1`, `−(q+5)/2` and `−(q+6)` in index order. All other signed differences are positive by the specified labels. These signs are consequences of this supplier.

## Boundary and compatibility

At q=5 the indexed formula gives first-left `(4,5,6,8,9)`, second-left `(3,7,13)`, right `(10,11)`, spine `(0,14)` and center labels `(12,2,1)`. Every original name and value agrees with [D111](ORDINARY_53_2_DIRECT_SEED.md) and the [retained ledger](../evidence/validation/LCL_ORDINARY_53_2_DIRECT_SEED_001/result.json). Its two reflected pairs are `{5,9}` and `{6,8}`, with forced label 4 and midpoint 7. Only this retained original and certificate are used for executable corroboration. The symbolic argument proves the full domain.

For each supplied seed, `s:1` is the terminal endpoint of the actual witnessing spine. Its exact neighbor set is `{s:0,b:1:0}`, its own label is m, its predecessor carries zero, and its off-spine neighbor carries one. Hence all [D112](ORDINARY_EXTREME_SPINE_GROWTH.md) premises hold. This identifies the prospective two-parameter application `[[q,3],[r]]` for odd q≥5 and r≥2. The present task establishes the compatible seeds. A separate application, wider left quotas and ordinary composition are outside its scope.
