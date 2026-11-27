# D210 simultaneous ordinary supplier for unit flanks

The exact original `[[1],[q,a],[b],[1]]` is ordinary graceful for independently chosen exact integers q≥5, even a≥4, b≥2, with at least one of b and q even. In particular this supplies every all-even D117 central triple with unit flanks. The construction labels a partial tree spanning the full original and allocates the remaining original terminals. It requires neither a graceful central component nor alpha separation, a prescribed return, or old label order.

## 1. Original and independently labeled partial tree

Let the actual spine be L,x,y,R, with names `s:0,s:1,s:2,s:3`. In spine order, the original centers `b:0:0,b:1:0,b:1:1,b:2:0,b:3:0` have quotas 1,q,a,b,1. Every terminal `l:i:d:e` is adjacent to exactly its original center `b:i:d`. The spine, five center edges and q+a+b+2 terminal edges give m=q+a+b+10 edges. The partial tree includes the entire spine, every center and both original flank terminals. These are eleven vertices and ten actual edges. The remaining q+a+b vertices are exactly the indexed terminals at the three central centers.

Use H=m−4 for the quota-b center and use the following assignments. For a=4 put k=8. For a≥6 put j=(a−6)/2, k=10+j and K=m−8−j.

| Original vertices in order | Labels |
|---|---|
| L,x,y,R | 0,m,4,m−2 |
| Left flank center, q-center, a-center, b-center, right flank center | m−1,3,2,H,5 |
| Left and right flank terminals | k,m−5 |

All labels are in [0,m] and distinct. Indeed m≥21, and 6≤k≤m−6. In the a≥6 branch m−6−k=q+b+j≥7, so the same bound holds even when j=0. The used labels are 0,2,3,4,5,k,m−5,m−4,m−2,m−1,m. Hence the unused label palette is exactly

```text
R = {1,m−3} ⊔ ([6,m−6] minus {k}).
```

The actual absolute differences in original edge order within each group are

| Original edges | Actual differences |
|---|---|
| Lx, xy, yR | m, m−4, m−6 |
| Five spine-to-center edges | m−1, m−3, m−2, m−8, m−7 |
| Left and right flank terminal edges | m−1−k, m−10 |

The weights other than the left flank terminal form [m−10,m] except {m−9,m−5}, once each. For a=4 the left flank terminal uses m−9. For a≥6 its weight is m−11−j, which lies in [1,m−11] since m=q+b+16+2j. Thus the ten weights are distinct in both branches and the unused weight palette is

```text
a=4:   D = [1,m−11] ⊔ {m−5}
a≥6:   D = ([1,m−11] minus {m−1−k}) ⊔ {m−5,m−9}.
```

Both unused palettes have size m−10=q+a+b. Here and below intervals contain integers and a reversed interval is empty.

## 2. Base allocation at the three actual centers

The host subscript denotes the actual center's assigned label. The base allocation uses quotas a, q+b−2, 2 at hosts 2, 3, H, respectively. The middle list is a palette for redistribution, not an assignment to q+b−2 original named terminals at the q-center.

### Case a=4

Here k=8. The following columns give the proposed label groups and their actual absolute differences.

| Host | Labels | Weight image |
|---|---|---|
| 2 | {1,6,7,m−3} | {1,4,5,m−5} |
| 3 | [9,m−8] | [6,m−11] |
| H | {m−7,m−6} | {3,2} |

The label bands {1,m−3}, [6,7], [9,m−8] and [m−7,m−6] are disjoint and exhaust R. The images are injective on each row and partition D. At label 1 the host-2 difference is the absolute value |1−2|=1; the other host-2 differences are increasing positive shifts. The quotas are 4, m−16=q+b−2, 2.

### Case a≥6 even

In this branch K−k=q+b−2≥5, k≥10, and K≤m−8. The four consecutive middle bands [7,k−1], {k}, [k+1,K−1], [K,m−9] partition [7,m−9]. This includes j=0 when K=m−8 and the final band is empty. Together with the separate labels 1,6,m−8,m−7,m−6,m−3 this gives exactly the following partition of R, omitting k.

| Host | Labels | Weight image |
|---|---|---|
| 2 | {1,m−3,m−7} ⊔ [K,m−9] ⊔ [7,k−1] | {1,m−5,m−9} ⊔ [K−2,m−11] ⊔ [5,k−3] |
| 3 | {6} ⊔ [k+1,K−1] | {3} ⊔ [k−2,K−4] |
| H | {m−6,m−8} | {2,4} |

The two smaller images [5,k−3] and [k−2,K−4] join to [5,K−4], while the upper interval starts at K−2 and ends at m−11. The sole missing internal weight is K−3=m−1−k; if j=0 this is the missing top weight m−11 and the upper interval is empty. The other weights give [1,4] and the two extras m−5,m−9. All weights occur once and the union is D. Host 2 uses 3+j+(k−7)=6+2j=a labels, host 3 uses K−k=q+b−2 and host H uses two.

## 3. Exact invariant transfer menu and final original

Write S₂,S₃,S_H for the three base groups in their respective branch. All z in S₃ are greater than 3 and strictly below H. Define ρ(z)=m−1−z. When both a label and its mate lie in S₃,

```text
|ρ(z)−H| = H−ρ(z) = z−3.
```

In the a=4 branch the invariant intersection S₃∩ρ(S₃) is I=[9,m−10], since the reflected band is [7,m−10]. In the a≥6 branch it is I=[k+1,K−4]. There 6 has mate m−7 outside S₃, and the upper band reflects to [k−2,K−4]. Its intersection with the original upper band gives the stated I. Thus every stated I is invariant and lies in S₃.

For a transfer S⊆S₃ with the base labels otherwise fixed, the differences released at host 3 are {z−3 : z∈S}. The differences added at host H are {H−w : w∈S}={ρ(w)−3 : w∈S}. Both maps are injective. Since the base consumes each difference once, equality of the two sets is necessary and sufficient for the new complete inventory, and it is equivalent to S=ρ(S). In particular the size-(b−2) transfer must be a union of reflection orbits in I. This necessity applies only to a transfer of base labels from host 3 to H with everything else fixed.

The size of I is q+b−4 for a=4 and q+b−6 for a≥6. The excess over b−2 is q−2≥3 and q−4≥1, respectively. When m is even the involution has only pairs. When m is odd it has the integer midpoint (m−1)/2 in I and all remaining orbits are pairs. To see the midpoint assertion, I is a nonempty integer interval with endpoint sum m−1 and contains its average whenever that average is integral. For an even request b−2 choose (b−2)/2 pairs. The capacity bound suffices even after dropping a midpoint, since the even request does not exceed the largest even cardinality at most |I|. For an odd request b−2 take the midpoint and (b−3)/2 pairs. The odd request then fits because |I| is odd and the previously proved size bound holds. An odd request fails if there is no midpoint. As a and 10 are even, m is odd exactly when q+b is odd. Therefore for odd b the midpoint is available exactly when q is even. This proves the exact parity restriction for this menu, and every requested transfer in the theorem's domain is available.

For a deterministic choice, take the midpoint exactly when b is odd. Take the required number of pairs in increasing order of their smaller labels. Give the a-, q- and b-centers the final label groups

```text
A₂ = S₂
A₃ = S₃ minus S
A_H = S_H ⊔ S.
```

They partition R and have sizes a,q,b. Each list in increasing order goes to the increasing original terminal indices of its own physical center. The named graph is unchanged. Each new label is used once, its actual weight is the one proved above, and the new weight images exhaust D with multiplicity one. Adding the fixed partial tree gives all vertex labels [0,m] and all edge differences [1,m]. The procedure enumerates finite intervals and their paired representatives, fixes the required finite number of orbits, then emits each actual index in order. No search through alternate allocations is needed.

## 4. Source comparison and exact scope

[D105](ORDINARY_43_2_EXTREME_SPINE.md) independently labels the isolated 13-edge (4,3),(2) core with its actual opposite-extreme spine labels. [D117](ORDINARY_QAR_ALL_PARITY_SUPPLIER.md) supplies the isolated q,a,b core with opposite-extreme ports, first by allocating a two-host residual seed with reflection and then growing the actual right quota. D210 shares the idea of independently supplying actual partial labels and using reflected differences. It fixes both outer vertices, both flank centers and both flank leaves from the start. Its provisional three-host allocation reserves two right-central leaves and transfers a subset from the fixed base. It never requires a separately graceful central tree. In particular the actual central edge xy has weight m−4, above the central edge count n=m−6. That edge already precludes a translated or reflected graceful n-edge core as the source of this labeling. The all-even sequential-D131 and pure-translation exclusions remain valid on their respective models. [D209 proof and exclusions](ORDINARY_SPINE_TWO_SIDED_ORDINARY_SUPPLIER.md#4-exact-limitations-of-the-unit-flank-interface)

The displayed certificate has no alpha separation. L at 0 and x at m force the class of L below the class of x in any putative alpha cut. The a-center at label 2 lies in the class of L, and its terminal at label 1 lies in the class of x. This reversed order across their original edge rules out the cut.

[R226](../references/upstream/mdl/N226_R226_two_host_completion.md#n226-closeout) classifies integral completion on a supplied two-host residual instance using actual eligible differences, including parallel pairs and a possible midpoint. After the D210 base, freeze S₂ and all other fixed vertices and use the reserved palette (S₃, {z−3 : z∈S₃}) at the two actual hosts 3 and H. Its forced labels are precisely S₃ outside I at host 3. On I the eligible weights have the reflected pair or midpoint structure. D210 constructs these palettes from the original parameters and proves their capacity directly. R232 handles simultaneous allocation among supplied locally balanced two-host palettes with a forest restriction on singleton resources and pair capacity conditions across hosts. D210 supplies its whole-original partial tree and base palette itself and uses one active two-host transfer. No inter-batch singleton orientation or pair matching is required here. [R232](../references/upstream/mdl/N232_R232_joint_allocation.md#n232-closeout)

In the D117 unit-flank slice, D209 covers the cases for which b+2 divides q+1 or a+1. Its other positive subdomains have unequal flanks or require a larger equal quota. D210 therefore adds exactly the unit-flank inputs in its stated domain where neither divisibility holds, including all-even central triples. In the unit-flank slice the union of these two proofs leaves the nondivisibility cases with a odd, or with a even and both q and b odd. These are complements of the proved coverage. The latter parity excludes the exact D210 transfer menu, while a odd is outside its base formulas. The unresolved larger equal-flank complement of D209 is unaffected. No assertion of universal ordinary supply or historical novelty follows.

The Director's symbolic candidate preceded computational preparation and resolves the specific all-even benchmark by an independent formula, so the proposed hybrid benchmark remains deferred without execution. The prescribed originals were fixed independently of their certificates. [Frozen original identities](../evidence/validation/D210_SIMULTANEOUS_ORDINARY_SUPPLIER/ORIGINALS.md) · [Fixed hand arithmetic](../evidence/validation/D210_SIMULTANEOUS_ORDINARY_SUPPLIER/FIXED_ARITHMETIC.md)

## 5. Independent mathematical review

A separate read-only reviewer inspected this actual proof and both control records. The review independently derived the ten partial weights, both base partitions including the missing top weight when j=0, the exact reflection intersection, and the capacity and parity conditions for the fixed transfer. It confirmed the original indexed parents and quotas, the central-edge and alpha comparisons, and the relative coverage and complement of D209 and D210. The reviewer hand-checked all 98 endpoint differences and 102 vertex assignments in A–D, and all ten partial differences and eleven partial vertex assignments in E, where a one-label transfer requires 2z=21. The proof and prescribed hand controls passed. There was no executable or formal verification.
