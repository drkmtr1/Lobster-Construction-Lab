# D114 — Even first-left quota by numerical host-role reversal

For every exact even integer q≥6, the ordered original `[[q,3],[2]]` admits a directly supplied ordinary graceful labeling at `s:0=0`, `s:1=q+9` and `b:1:0=1`. Here `m=q+9` is the actual edge count. No alpha or signed restriction is assumed.

## Original topology and necessary parity

The original spine `s:0--s:1` witnesses the tree. The three centers `b:0:0`, `b:0:1`, `b:1:0` attach to `s:0`, `s:0`, `s:1` respectively. Their terminals `l:i:j:k` attach only to their own centers, with index ranges `0..q−1`, `0..2` and `0..1` respectively. Each listed center or terminal adds one vertex and one edge to the tree already named. There are q+10 vertices and q+9 distinct edges including the spine and attachments, each of multiplicity one. Each center is one edge and each terminal two edges from the spine.

For any ordinary graceful f with m edges, the sum of the actual absolute edge differences equals the sum of the vertex labels because both are `m(m+1)/2`. Modulo two, `|f(u)−f(v)| ≡ f(u)+f(v)` on each edge. Summing over actual incidences and subtracting the vertex sum yields

```text
sum_v (degree(v)−1) f(v) ≡ 0 (mod 2).
```

The respective degrees of `s:0,s:1,b:0:0,b:0:1,b:1:0` are `3,2,q+1,4,3`. The terminals have degree one. Write A and B for the physical first and second left-center labels. At the required pins the left side becomes `qA+3B+(q+9)+2=qA+3B+q+11`. For even q this is congruent to `B+1`, so B must be odd. In particular the D113 value B=2 cannot meet these pins when q is even. The conclusion concerns that host label on this pinned original.

## Independently supplied core

Assign `A=2` and `B=q+7`, reversing the numerical host order from [D113](ORDINARY_Q3_2_ODD_COMPLEMENTARY_SUPPLIER.md) while preserving physical names and quotas. The following nine named core vertices and labels are prescribed before allocating any remaining resources.

| Named vertex or group | Label or indexed labels |
| --- | --- |
| `s:0,s:1` | `0,q+9` |
| `b:0:0,b:0:1,b:1:0` | `2,q+7,1` |
| `l:0:0:0,l:0:0:(q−1)` | `3,q+8` |
| `l:1:0:0,l:1:0:1` | `q+5,q+6` |

The last first-left index is q−1, distinct from zero. Both spine vertices and all centers belong to the core. Each of its four specified terminals is adjacent to its own center only. The spine connects the two sides, and each center and core terminal has a single edge to the previously named part. Thus this core is a tree with exactly eight edges. Its injective labels are `[0,3] ⊔ [q+5,q+9]`. Its spine, first-left attachment, second-left attachment and right attachment give q+9, 2, q+7 and q+8. The two first-left core terminals give 1 and q+6, and the two right terminals give q+4 and q+5. These weights are exactly `{1,2} ⊔ [q+4,q+9]` each once. This core is supplied directly from q.

The complements of these two occupied inventories are `R=[4,q+4]` and `D=[3,q+3]`, both of size q+1. The vacant original terminals are `l:0:0:k` for `1≤k≤q−2` at the lower host and all three `l:0:1:k` at the higher host. No other incidence is vacant. Thus the residual quotas are q−2 and three in R226's lower/higher order.

## R226 components and exact integral quotas

The lower host is the actual first center of label `L=2`. The higher host is the actual second center of label `H=q+7`. All x in R lie strictly between L and H, so

```text
d_L(x)=x−2,   d_H(x)=q+7−x,   rho(x)=q+9−x.
```

The two differences sum to q+5 and are exchanged by rho wherever both labels are considered. The map `d_H` bijects R onto D. Label 4 has lower difference 2, already used, and higher difference q+3, which is free. Its reflected partner q+5 is occupied. It gives the forced half-edge at q+3 with zero lower contribution.

Reflection preserves `[5,q+4]` and both options for all these labels lie in `[3,q+2]`. Because q+9 is odd there is no integer midpoint. This interval has q labels, partitioned into exactly q/2 pairs. For each pair `{x,rho(x)}`, the two eligible difference vertices are the distinct images `d_H(x),d_H(rho(x))`. Both labels connect these vertices with reversed host tags. Injectivity of `d_H` makes each pair's two difference vertices disjoint from those of all other pairs and from the forced vertex. Surjectivity supplies every unused difference. Every unused label has an eligible row. Each pair has two ordinary edges and two vertices, and the forced component has one half-edge and one vertex, so all satisfy `e_K+t_K=n_K`.

The core is independently labeled in the complete range, with distinct positive actual weights, distinct named hosts and exactly the named terminal extensions required by [R226.1 revision 2](../references/upstream/mdl/N226_R226_two_host_completion.md#n226-closeout). In its lower-host projection, `A0=0`, `c=q/2`, `eta=0`, hence

```text
p(P_Z) = {2j : j is an integer, 0≤j≤q/2}.
```

Assign the complete pair `{5,q+4}` and the forced singleton 4 to the higher host. Assign the other `j=q/2−1` pairs to the lower host. Each whole pair uses its two difference vertices once. This gives exactly q−2 labels to the lower host and three to the higher. In fact the lower palette is `[6,q+3]` and the higher palette is `{4,5,q+4}`. D113 uses the midpoint to meet a residual lower quota of one. D114 assigns the lower numerical label to the physical first center, where the two reserved core terminals leave an even residual quota, and supplies the higher host with one pair and the forced singleton.

## Complete indexed construction

Place `[6,q+3]` in order at first-left indices 1 through q−2, between the core values at indices 0 and q−1. In full index order the first-left labels are `(3,6,7,...,q+3,q+8)`, second-left labels `(4,5,q+4)`, and right labels `(q+5,q+6)`. The other five labels are those of the spine and centers. These disjoint residual allocations exhaust R and, together with the core labels, exhaust `[0,q+9]` once each.

| Actual incidence group | Absolute differences |
| --- | --- |
| First-left attachment | 2 |
| First-left terminals | `{1,q+6} ⊔ [4,q+1]` |
| Second-left attachment | q+7 |
| Second-left terminals | `{3,q+2,q+3}` |
| Right terminals | `{q+4,q+5}` |
| Right attachment | q+8 |
| Spine | q+9 |

Subtract 2 from each first-left terminal label, subtract each second-left terminal label from q+7, and subtract 1 from each right terminal label to obtain these weights. Sorting the displayed groups gives `{1,2,3} ⊔ [4,q+1] ⊔ [q+2,q+9]` with multiplicity one throughout. The actual edge spectrum and both empty final inventories follow independently of R226. The supplier requires exact integer type, even parity and q≥6, rejecting booleans and all unsupported inputs. Write the named core and the two residual indexed ranges with one pass through the terminal indices. This emits q+10 labels and q+9 actual incidences in O(q) indexed operations and terminates without search.

Orient edges from the traversal class containing `s:0`. The even class contains `s:0`, the right center and the left terminals. The odd class contains `s:1`, both left centers and the right terminals. Only the q first-left terminal edges are negative, with respective signed differences `−1`, the terms `−4,−5,...,−(q+1)`, and `−(q+6)` in index order. Each is the value 2 minus the terminal label. The second-left terminals are all below their center, the right terminals above theirs, and the spine and attachments are positive. These signs describe the witness.

## D112 premise compatibility

The actual witnessing spine ends at `s:1` of degree two with exact neighbors `s:0` on the spine and `b:1:0` off it. Their labels in predecessor, exit and off-spine host order are `(0,m,1)`. Therefore D112's hypotheses hold for every seed here. The prospective combined coverage `[[q,3],[r]]` for exact integers q≥4 and r≥2 draws on D107 for q=4, the D113 odd seeds and D114 even seeds for q≥5, and D112 as the conditional right-growth consumer. This task proves the even seeds and their premises. Wider left quotas and general ordinary composition remain separate.
