# D116 — One complementary supplier when at least one left quota is even

For independently chosen exact integers q≥5 and a≥3 with at least one even quota, the ordered original `[[q,a],[2]]` admits a direct ordinary graceful labeling at `s:0=0`, `s:1=m=q+a+6` and `b:1:0=1`. The construction uses the following numerical host selection, independently of any inequality between q and a.

| Parities of q,a | Lower host of label 2 and full quota ell | Higher host of label m−2 and full quota h |
| --- | --- | --- |
| even, odd | `b:0:0`, q | `b:0:1`, a |
| odd, even | `b:0:1`, a | `b:0:0`, q |
| even, even | `b:0:0`, q | `b:0:1`, a |

The first center is preferred when q is even. This chooses labels and the allocation roles only. Each physical center keeps its own full quota and its original name and indexed neighbors.

## Original and necessary degree parity

The actual spine is `s:0--s:1`. The two left centers attach to `s:0`, and `b:1:0` attaches to `s:1`. At each center its terminal names run through consecutive indices starting at zero, with q, a and two terminals respectively. Each terminal has only its named center as neighbor. These edges give two spine vertices, three centers and q+a+2 terminals, thus m+1 distinct vertices. The spine, three attachments and q+a+2 terminal edges are the m distinct original incidences, each of multiplicity one. The named graph is a tree because each center or terminal is attached by one edge to the previously named tree. The same spine witnesses the tree, with centers and terminals at distances one and two respectively.

By the [D114 parity argument](ORDINARY_Q3_2_EVEN_COMPLEMENTARY_SUPPLIER.md), each absolute difference satisfies `|f(x)−f(y)| ≡ f(x)+f(y) (mod 2)`. The complete vertex-label and weight sums both equal `m(m+1)/2`. Summing over actual edges and subtracting the label sum gives `Σ(deg−1)f≡0 (mod 2)`. The nonterminal degrees in order `s:0,s:1,b:0:0,b:0:1,b:1:0` are `3,2,q+1,a+1,3`. All terminals have degree one. With A,B the physical first and second left-center labels, the required pins give `qA+aB+m+2≡0 (mod 2)`.

If q is even and a odd, the only odd contributions are `aB` and m. If q is odd and a even, they are `qA` and m. If both quotas are even, each summand is even. Thus the selected roles satisfy the necessary identity in all three cases. Sufficiency follows from the inventories below.

## Independently supplied core and complementary palettes

The two spine vertices, all three centers, the lower host's terminal indices zero and ell−1, and the two right terminals form the nine-vertex core. Here ell is even and at least four, so its reserved indices are distinct. The spine, center attachments and four specified terminal edges give eight edges and a connected acyclic actual subtree. Its labels are fixed directly from the parameters.

| Named role | Labels in the stated order |
| --- | --- |
| `s:0,s:1` | `0,m` |
| Selected lower host, selected higher host, `b:1:0` | `2,m−2,1` |
| Selected lower-host terminals at indices 0 and ell−1 | `3,m−1` |
| `l:1:0:0,l:1:0:1` | `m−4,m−3` |

Since m≥14, the core labels give `[0,3] ⊔ [m−4,m]` injectively. The spine and three attachments give m, 2, m−2 and m−1, where the left attachments are listed in numerical host order. The reserved lower terminals have weights 1 and m−3, and the right terminals give m−5 and m−4. These are `{1,2} ⊔ [m−5,m]` with positive multiplicity-one weights. The residual labels and differences are `R=[4,m−5]` and `D=[3,m−6]`, both of size m−8. The actual vacancies are the lower-host indices 1 through ell−2 and all higher-host indices 0 through h−1. They account for `ell−2+h=m−8` original terminal edges. No solved target is an input to the core.

## Uniform R226 extraction

For x in R, `2<x<m−2`, so `d_L(x)=x−2` and `d_H(x)=m−2−x`. The decreasing map `d_H` bijects R onto D. Reflection `rho(x)=m−x` exchanges the options on reflected labels. At x=4 the lower option 2 is occupied and the higher option m−6 is available, giving a forced half-edge at m−6. The reflected mate m−4 is occupied.

On `[5,m−5]` both options lie in `[3,m−7]`, and reflection swaps its endpoints. Set `u=floor((m−1)/2)`. The labels strictly below half of m are precisely `5..u` in this interval. Each pairs with a distinct label strictly above half of m, represented by `{x,m−x}`. Thus there are `c=u−4` pairs and there is a singleton midpoint t=m/2 precisely when m is even. Its two host options equal t−2. In each pair, the two labels join the same two distinct difference vertices with opposite host tags. The bijection `d_H` shows that the difference vertices of distinct reflection orbits are disjoint and that these orbits, together with the forced half-edge, cover D. All unused labels have an eligible option. Each pair has two edges on two vertices, each midpoint is one loop on one vertex, and the forced component is one half-edge on one vertex. All satisfy `e_K+t_K=n_K`.

The [adopted R226.1 revision-2 theorem](../references/upstream/mdl/N226_R226_two_host_completion.md#n226-closeout) applies to the independently supplied tree core, its injective labels and distinct weights in the full alphabets, the distinct physical hosts in lower/higher order, and the exact named terminal extensions. Its full complementary palettes have the verified eligible rows and balanced components. No forced labels go to the lower host, so `A0=0`. With eta equal to one when m is even and zero otherwise, the quota-free integral lower projection is

```text
p(P_Z) = {2k+epsilon : k,epsilon are integers, 0≤k≤c, 0≤epsilon≤eta}.
```

Choose `j=(ell−2)/2`, `k=j` and `epsilon=0`. This gives the required lower quota ell−2. To see that the choice fits the projection, use `m=ell+h+6`. When m is odd, `u=(m−1)/2`, so `c−j=(h−1)/2`. When m is even, `u=m/2−1`, so `c−j=(h−2)/2`. In either case h≥3 and ell≥4 imply `0≤j≤c`.

## Indexed construction and direct weight proof

Give the j pairs whose representatives are `u−j+1,...,u` to the lower host. The resulting palette is

```text
S_L = [u−j+1,u] ⊔ [m−u,m−u+j−1].
```

Since j≤u−4, the lower interval starts at least at 5 and its image ends at most at m−5. Its image under rho is exactly the second interval. They are disjoint because `u<m−u`. Together they have `2j=ell−2` labels and are reflection invariant. If m is even, the midpoint strictly separates these intervals and goes to the higher host. If m is odd there is no integer midpoint. Set `S_H=R \ S_L`, which contains `(m−8)−(ell−2)=h` labels. In particular S_H contains forced label 4.

Assign the lower list in increasing order to indices 1 through ell−2, preserving its reserved endpoint values. Assign the higher list in increasing order to indices 0 through h−1. Keep the spine, centers and right labels fixed. This uses each original label once because the core and two allocated lists partition `[0,m]`. Independently of the R226 projection, `d_L=d_H∘rho` and `rho(S_L)=S_L` imply equality of the lower and higher images of `S_L` with multiplicity. Hence the actual residual differences are

```text
d_L(S_L) ⊔ d_H(S_H) = d_H(S_L) ⊔ d_H(S_H) = D.
```

The bijection of `d_H` gives disjointness and multiplicity one. Together with the core this exhausts `[1,m]`. Both unused inventories are empty, and every labeled incidence is on the original witnessing tree.

Require exact integer type for both inputs, the two lower bounds and at least one even quota. Reject booleans, nonintegers and odd–odd inputs. After the host selection, emit the fixed core and scan R once to assign the two sorted lists. The named terminal indices and their original edges are then written from their finite ranges. This produces m+1 labels and m edges in O(q+a) indexed output operations, without search.

Orient from the traversal class containing `s:0`. This class consists of `s:0`, `b:1:0` and the left terminals. The other class contains the exit, both left centers and the right terminals. Exactly the terminal incidences toward the selected lower host are negative, since each of those terminal labels exceeds 2. The indexed signed differences there are −1, followed by the decreasing list `2−x` for x in the increasing S_L list, followed by `3−m`. The other incidences have positive signed differences by the supplied labels. These are output properties.

## Symbolic adverse allocation, specialization and growth premises

In the even–even case the midpoint is assigned to the higher host. Moving only that label to the lower host preserves the label multiset, and both options have the same weight t−2, so the weight multiset is unchanged. The lower/higher counts become `(ell−1,h−1)` instead of `(ell−2,h)`. The changed integral allocation fails the prescribed quotas. This is a symbolic control and is evaluated without constructing an even–even numerical original.

For any even q≥6 with a=3, the lower host is physical `b:0:0`, `m=q+9`, `u=q/2+4` and `j=q/2−1`. Here `m−u=u+1`, so the adjacent intervals combine to `[6,q+3]`. Its complement is `{4,5,q+4}`. The whole core, host roles, palettes and original indexed lists agree with D114. The sole executable formula boundary is the [retained D114 certificate at (6,3)](../evidence/validation/LCL_ORDINARY_Q3_2_EVEN_COMPLEMENTARY_SUPPLIER_001/result.json). D111 is a separate recheck on its own odd–odd original.

At every seed the actual spine ends at `s:1`. Its exact neighbors are predecessor `s:0` labeled zero and off-spine `b:1:0` labeled one, and the exit carries m. These are all the [D112 conditional growth premises](ORDINARY_EXTREME_SPINE_GROWTH.md). This theorem and [D115](ORDINARY_QA_2_ODD_ODD_COMPLEMENTARY_SUPPLIER.md) together cover all four parity cases at the stated seed bounds. The corresponding `[[q,a],[r]]` application for exact integers q≥5, a≥3 and r≥2 is prospective. General spine composition and greater center multiplicity are separate questions.
