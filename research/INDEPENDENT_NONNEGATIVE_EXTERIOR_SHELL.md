# D215 independent exterior-shell supply for arbitrary nonnegative quotas

**PROVED WITHIN EXACT SCOPE.** Let p,b,t and every qᵢ be nonnegative integers, with the finite list (q₀,…,q_{ℓ−1}) allowed to be empty. The exact named original `[[p],[q_0,...,q_(ell-1)],[b],[t]]` is ordinary graceful whenever its isolated central cluster admits an independently supplied ordinary graceful labeling with `s:1` at zero. This gives unconditional coverage when the number d of positive central quotas is at most one, or when d≥2 and the total central degree ℓ≥3. For d=2 and ℓ=2 this proof requires the rooted supply as a hypothesis. [Named hand controls](../evidence/validation/D215_NONNEGATIVE_EXTERIOR_SHELL/HAND_CONTROLS.md)

## 1. Exact named original and independent exterior labeling

The spine is `s:0,s:1,s:2,s:3` with consecutive incidences. Each quota in section i at position j contributes the vertex `b:i:j` joined to `s:i` and the q indexed edges to `l:i:j:e` for 0≤e<q. A listed zero keeps the edge to `b:i:j`, which is then a direct leaf. An empty section adds no such edge. All labels and intervals below are integral, and [a,b] is empty when a>b.

Use H of profile `[[p],[],[b],[t]]` with k=p+b+t+6 edges. The three spine edges, three branch attachments and p+b+t terminal edges account for k. The following table assigns the four spine vertices and three branch vertices, including every zero-quota branch vertex. The terminal intervals assign successive labels to increasing indices starting at zero at their own parents.

| Actual names | Label or interval under g |
|---|---|
| `s:0,s:1,s:2,s:3` | (t+4, t+3, p+t+6, 1) |
| `b:0:0,b:2:0,b:3:0` | (t+2, 0, p+t+5) |
| Terminals of `b:0:0` | [t+5,p+t+4] |
| Terminals of `b:2:0` | [p+t+7,k] |
| Terminals of `b:3:0` | [2,t+1] |

Below cut t+4, the labels are the consecutive disjoint pieces {0}, {1}, [2,t+1], {t+2}, {t+3}. At and above the cut they are {t+4}, [t+5,p+t+4], {p+t+5}, {p+t+6}, [p+t+7,k]. The interval lengths are t, p and b respectively. Thus the complete alphabet is [0,k], with exactly one label for every named vertex. The actual `s:1` has A=t+3, the maximum lower label.

The spine sides are upper, lower, upper, lower. The three exterior branch vertices in section order 0,2,3 are lower, lower, upper, opposite their respective spine parents. Left and opposite interior terminal labels are upper, and right terminal labels are lower. This verifies alpha separation on every actual incidence.

| Actual edges in order | Endpoint subtraction | Weights |
|---|---|---|
| Spine | (t+4)−(t+3), (p+t+6)−(t+3), (p+t+6)−1 | (1,p+3,p+t+5) |
| Branch attachments 0,2,3 | (t+4)−(t+2), (p+t+6)−0, (p+t+5)−1 | (2,p+t+6,p+t+4) |
| Left terminals | Their interval minus t+2 | [3,p+2] |
| Opposite interior terminals | Their interval minus 0 | [p+t+7,k] |
| Right terminals | p+t+5 minus [2,t+1], in reverse numerical order | [p+4,p+t+3] as a set |

The disjoint consecutive union in numerical order is {1,2}, [3,p+2], {p+3}, [p+4,p+t+3], {p+t+4,p+t+5,p+t+6}, [p+t+7,k]. The terminal weights are injective within each group because each group stays on one side of its host. A zero p deletes exactly the left terminal interval and its weight band. The next weight after 2 is then p+3=3. A zero t deletes exactly the right terminal interval and its weight band. The next weight after p+3 is then p+t+4=p+4. A zero b deletes exactly the opposite terminal interval and its weight band, leaving p+t+6=k. These deletions operate independently, covering each combination of zero quotas with all three original branch attachments retained. With p=b=t=0 the six edges have weights 1,…,6. H is supplied independently for all declared p,b,t.

## 2. Exact D212 realization when p,b,t are positive

On `[[1],[],[1],[1]]`, the present shell formula gives spine (5,4,8,1), branch labels (3,0,7), and terminal labels (6,9,2). It has alpha cut 5 and `s:1=4`. Its actual endpoint pairs in increasing weight order are as follows.

| Weight | Endpoints | Weight | Endpoints | Weight | Endpoints |
|---:|---|---:|---|---:|---|
| 1 | (4,5) | 4 | (4,8) | 7 | (1,8) |
| 2 | (3,5) | 5 | (2,7) | 8 | (0,8) |
| 3 | (3,6) | 6 | (1,7) | 9 | (0,9) |

An edge of labels x<y crosses c exactly when x<c≤y. At 6, the crossing differences are [3,9]. At 2, the crossing differences are [6,9]. At 9 the unique crossing difference is 9. Thus the three cuts are safe. For the [D212](SIMULTANEOUS_SAFE_GAP_QUOTA_GROWTH.md#2-exact-local-starts-and-independent-width-coefficients) triples the constants and spans among the other two selected cuts are exact.

| Host (a,c,D) | Constant test | Span and selected cuts in it | Selected cuts with smaller D |
|---|---|---|---|
| Left (3,6,3) | Lower, 6−3=3 | 3<c'<6, none | ∅ |
| Right (7,2,6) | Upper, 2+6−1=7 | 2<c'≤7, {6} | {6} |
| Opposite interior (0,9,9) | Lower, 9−9=0 | 0<c'<9, {2,6} | {6,2} |

This checks both pairwise conditions for each pair. The smaller-threshold cut is in the larger-threshold span and the larger-threshold cut is absent from the smaller-threshold span.

Take u=p−1, v=t−1, w=b−1 at cuts 6, 2, 9 respectively, so all widths are nonnegative. The D212 old-label map is E(x)=x+v·I(x≥2)+u·I(x≥6)+w·I(x≥9). In particular E(4)=4+v=A and E(5)=5+v=A+1. The old alpha sides are preserved. The new left and opposite terminals are in upper gaps and the new right terminals are in a lower gap, each opposite its host. Consequently the enlarged shell retains both its alpha cut and shared boundary root, now at A+1 and A.

The new terminal gaps at cuts 6, 9, 2 are [6+v,5+v+u], [9+v+u,8+v+u+w] and [2,1+v]. Adding the corresponding old terminal images E(6), E(9) and E(2) gives precisely the three full terminal palettes in Section 1. Under D212 transport each old index-zero terminal occupies the greatest label in its enlarged group. The direct formula in Section 1 uses increasing order across all indices. Both are valid assignments to the same exact indexed incidence set, and each keeps its own stated index convention.

This is a bounded three-host certificate on the shell. The D213 bound concerns all-center simultaneous certification on its declared full positive-quota family. D215 needs no growth certificate for the combined original. The proof of Section 1 supplies cases at zero directly and uses no negative D212 width. This application does not settle the separate held D212 boundary-closure candidate.

## 3. Independent root-zero central supply

Let C retain only the actual root `s:1` and the central branch list with its original names and edges. Its n=ℓ+Σqᵢ edges consist of ℓ attachments and Σqᵢ terminal edges. Let d count positive quotas and z count zero quotas, so ℓ=d+z.

- **Empty list.** The singleton has label 0, alphabet [0,0] and empty weight set.
- **d=0, nonempty list.** The cluster is a star at the root. Label it zero and its z original direct leaves 1,…,z in index order. Each root edge realizes its leaf label.
- **d=1.** At the one actual positive branch of quota q give its center q+1 and its terminals [1,q] in index order. Give the root 0 and the original zero-quota leaves [q+2,q+z+1] in their index order. The center-to-terminal differences are [1,q], the positive center attachment is q+1, and the direct leaf edges give [q+2,q+z+1]. The label and difference alphabets are exact also at z=0. The root is deliberately specified, and no tree-center assumption enters this construction.
- **d≥2 and ℓ≥3.** All vertices are within distance two of the root. Terminals of two different positive branches are at distance four. The root has eccentricity two, whereas a nonroot vertex has distance at least three to a terminal in a positive branch other than its own. A direct leaf has such a terminal at distance three. Thus the root is the unique center of this diameter-four tree, and its degree is ℓ, including all z direct leaves. Frank Van Bussel's thesis Theorem 4.5 applies to exactly this diameter and degree. Definition 4.1 places label zero at the actual center. The printed branch convention on page 109 calls a center-adjacent leaf a trivial branch, and the treatment on page 123 explicitly includes these branches, including how they enter the even-degree proof. The reported scope is degree at least three, with no exclusion of direct leaves. This uses the D214 source assessment and a focused check of its retained renders of printed pages 109, 112 and 123. The D214 Director's recorded acceptance did not include a fresh image retrieval. Pull back the existence theorem along an incidence-preserving isomorphism to the actual named cluster, whose unique center must map to the unique center. Each separate branch name and each terminal then has an exact label on its actual parent incidence. [D214 source assessment](../evidence/validation/D214_ROOTED_CLUSTER_EXTERIOR_SHELL/PRIMARY_SOURCES.md) · [Van Bussel, Theorem 4.5](https://www.nlc-bnc.ca/obj/s4/f2/dsk1/tape3/PQDD_0011/MQ53395.pdf#page=123) · [Trivial branch case](https://www.nlc-bnc.ca/obj/s4/f2/dsk1/tape3/PQDD_0011/MQ53395.pdf#page=134)
- **d=2 and z=0.** Use the conditional construction only when a root-zero graceful labeling of the exact C is independently supplied. Theorem 4.5 gives no such general supply at degree two. D215 does not classify that rooted case. The prescribed B2 control supplies its `[1,1]` cluster directly.

In every admitted case f has f(`s:1`)=0, label alphabet [0,n] and actual differences [1,n]. An alpha labeling of C is unnecessary.

## 4. Canonical amalgamation on the exact named original

The vertex intersection of C and H is exactly the actual `s:1` and their edge sets are disjoint. The complete original has N=n+k edges. For z∈C put F(z)=A+f(z), including the root. For z∈H other than the root, put F(z)=g(z) when g(z)<A and F(z)=n+g(z) when g(z)>A. The unique g-value A is at the root, which also receives A under the C rule. Hence the labels have the disjoint consecutive partition [0,A−1], [A,A+n], [A+n+1,n+k]. This is a bijection on the named original.

Every cluster difference is unchanged by its common translation and the cluster contributes exactly [1,n]. Every actual exterior edge has g-values l≤A<h, so its F-values are l and n+h. This applies to both spine edges incident to the root. Its weight is n+(h−l), and the exterior contributes exactly [n+1,n+k]. At physical cut A+n+1 the exterior edges cross and the cluster edges do not. For n=0 the central band is the singleton [A,A], its difference band is empty and every exterior value is unchanged.

The union is a tree since the two trees share one vertex and no edge. All four spine vertices and three spine edges are the original ones. Each nonspine branch vertex is adjacent to its specified spine parent, and terminals are adjacent to their own indexed branch vertex. The original spine witnesses the lobster property, including direct leaves. The construction transports the finite supplied f and lists finite integer intervals at the original names. The alphabet and incidence proofs require no search and no labeling from a solved whole original.

**Unconditional domain.** The theorem holds for every independently chosen nonnegative p,b,t and nonnegative central quota list when d≤1, or when d≥2 and ℓ≥3. It also holds for the specified two-unit cluster by its independent hand certificate.

**Conditional domain.** For every declared profile, including d=2,z=0, independent root-zero ordinary supply on C suffices. This is a sufficient interface for this composition. A failure of that rooted supply would leave other ordinary graceful constructions available.

## 5. Retained scope and research boundary

[D214](ROOTED_CLUSTER_EXTERIOR_SHELL_COMPOSITION.md) supplied this type of cluster with all positive quotas and ℓ≥3, using a different shell with b=1 and p,t positive. D215 includes that entire proved domain and removes the shell's unit quota and all three exterior positivity restrictions. It allows direct leaves in the center cluster and covers a singleton, root-zero stars and one-positive-branch clusters independently. The shared-root map is the same canonical amalgamation as D214 and Van Bussel's thesis Theorem 1.14, under the within-alpha-class numbering normalization established there. [Van Bussel, Theorem 1.14](https://www.nlc-bnc.ca/obj/s4/f2/dsk1/tape3/PQDD_0011/MQ53395.pdf#page=29)

[D206](ORDINARY_SPINE_BOUNDARY_ROOT_JOINT_BLOCK.md) uses the same arithmetic for endpoint-spine concatenation, and [D208](ORDINARY_SPINE_REVERSE_BLOCK_COMPOSITION.md) supplies reverse pendant-entry blocks with endpoint transport on actual connectors. The current shared root is interior to H and the two original neighboring spine edges are both part of H. The complete spine and graph here follow from Section 4 directly. Neither endpoint theorem needs a broader reading.

[D209](ORDINARY_SPINE_TWO_SIDED_ORDINARY_SUPPLIER.md) has a different two-spine-vertex core with separate port premises. [D210](ORDINARY_SPINE_SIMULTANEOUS_ORDINARY_SUPPLIER.md) and [D211](ORDINARY_SPINE_COORDINATED_FOUR_HOST_SUPPLIER.md) use simultaneous whole-original allocations in their stated two-central-center domains, without a root-zero cluster hypothesis. Their original profiles fit the syntax of D215 but have d=2,z=0. D215 covers the intersection for which the isolated central cluster at `s:1` is independently supplied at zero. Their independent unconditional subdomains and interface negatives retain their own scopes.

D212's B2, B3 and B4 originals now all have ordinary existence, B2 by control 6 and B3/B4 already by D214. All three registered simultaneous matched-gap questions remain INCOMPLETE and undecided. The D212 theorem and held boundary-closure candidate remain separate. [D213](ALL_CENTER_SAFE_GAP_STRUCTURAL_LIMIT.md)'s general component inequalities and its all-center bound ℓ≤10 on the positive-quota family retain their exact scope. The D207 monotone-return obligation stays unresolved and deferred. No historical novelty is claimed for the supplier theorem, shell or amalgamation.

Each exterior section in D215 still has exactly one listed branch vertex. In particular `[0]` is allowed and `[]` at an exterior section is outside the theorem. Larger exterior center multiplicities, multiple independently ordinary interior clusters and universal spine composition require additional arguments. A further specialization of this one-root shell would still consume only one ordinary input. A composition theorem for two independent ordinary clusters would address the first case in which both label and weight allocations must accommodate two rooted ordinary alphabets and their shared shell connector. That makes it the higher-leverage remaining question for the composition architecture.

**One held mathematical obligation for Director consideration.** On the exact named profile `[[p],[q_0,...],[r_0,...],[t]]` with p,t≥0 and each interior list having at least two positive entries and at least three entries in total, seek a composition theorem combining the two independently supplied root-zero ordinary clusters at the adjacent actual vertices `s:1` and `s:2`. It must furnish a single label bijection and complete difference partition while retaining the literal `s:1--s:2` edge and all original incidences. This would isolate the new resource compatibility obligation with both rooted suppliers already available. No investigation of this obligation was opened.

[Exact named hand controls](../evidence/validation/D215_NONNEGATIVE_EXTERIOR_SHELL/HAND_CONTROLS.md)
