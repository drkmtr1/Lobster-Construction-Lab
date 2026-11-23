# Proof obligations for B2-P1 and its continuation

This file defines the mathematical duties behind [RESEARCH_PLAN.md](../docs/RESEARCH_PLAN.md). It preserves the independently recalculated baseline corollary and path-consumer argument, and specifies the obligations for a future broader supplier. It does not replace the project's authoritative theorem or finding status records. Source IDs refer to [SOURCES.md](../docs/SOURCES.md).

## 1. Quantified supplier target

Specify a nonempty infinite set

\[
\mathcal D\subseteq\{(q,r,z_0,z_1,K):q,r,K\ge1,\ z_0,z_1\ge0\}.
\]

An independent supplier `F` accepts one tuple in `D`, constructs the exact B2-P1 graph in the final alphabet `0..m`, and returns labels on the prefix together with an interval position and side. Its totality claim is

\[
\forall p\in\mathcal D,\quad F(p)\text{ terminates and meets obligations P01--P08.}
\]

The algorithm and its domain must be explicit. A condition saying “there exists a successful prefix,” “the coefficient is positive,” or “a full solver succeeds” is not the independent input-supply conclusion. A conditional R226 consumer may be part of the construction only if the supplier proves that its required core, palettes and quotas are actually obtainable for every allowed tuple. [U04]

## 2. Obligations attached to every claimed supplier

| ID | Obligation | What would falsify or fail to establish it |
|---|---|---|
| P01 — target | Construct the exact named profile `[[q]+[0]*z0,[r]+[0]*z1]+[[]]*(K+1)`, with `m=q+r+z0+z1+K+4` | Added/removed connector edges, lost direct leaves, collapsed empty spine sections, or changed named incidences |
| P02 — assigned set | Assign exactly all vertices except `s:3,...,s:K+2`; include physical `s:2` | An unlabeled prefix leaf or a different return vertex hidden by isomorphism |
| P03 — labels | Prefix labels are distinct integers in the final alphabet `0..m` | Collision, out-of-range label, Boolean-as-integer input, or proof using a smaller intermediate alphabet without a valid embedding |
| P04 — differences | On every actual assigned edge, differences are distinct and their set is `[K+1,m]` | An omitted edge, duplicate difference, or leftover difference inventory other than `[1,K]` |
| P05 — residual labels | Unused labels are exactly `[ell,ell+K-1]`, with active label `ell+K` or `ell-1` in `0..m` | Merely matching cardinalities, a hole in the interval, or an active label inside it |
| P06 — physical boundary | The unfinished graph is the actual K-edge path starting at `s:2`; all assigned/unassigned crossing edges use that port | A resource-valid state whose remaining incidence is branched or attached at another assigned vertex |
| P07 — independence | Supply labels, choices, and any allocation inputs from parameters without first solving the complete target | Deleting a suffix from a full solver witness, assuming a compatible core exists, or using a finite table without a proved transport argument covering the claimed domain |
| P08 — continuation | The stated consumer labels every suffix vertex, uses exactly `[1,K]`, preserves the prefix, and terminates | A consumer that changes an undeclared prefix label, adds edges, or requires another unproved input |
| P09 — quantified domain | The proof covers every parameter tuple claimed, including equality bounds and parity cases | A formula checked only for a finite sample or a parameter restriction missing from the theorem statement |
| P10 — comparison | Compare with applicable retained formulas and known sufficient regimes; distinguish new state supply from ordinary-family novelty | Promoting a direct retained composition as a new mathematical advance or asserting literature priority without research |

P04 and P05 are set equalities, not a requirement to use the same unused label and difference values. The shifted label interval is intentional. P06 is additional to the numerical `interval_boundary` predicate; that function checks inventories and crossing-port incidence, not a theorem about every remaining topology.

## 3. Explicit shifted-interval path consumer

This elementary calculation supplies P08 for the exact B2-P1 suffix. It uses the existing endpoint-interval idea in U03, translated or reflected in the label alphabet.

Write `a=ell`. Let `w0=s:2`, `wj=s:(j+2)` for `1<=j<=K`. The only unfinished edges are `w(j-1)--wj`. Suppose unused labels are `[a,a+K-1]` and unused differences are `[1,K]`.

### Active endpoint above the interval

If `f(w0)=a+K`, assign

\[
f(w_j)=
\begin{cases}
a+(j-1)/2,&j\text{ odd},\\
a+K-j/2,&j\text{ even}.
\end{cases}
\]

The values alternate the lowest and highest remaining labels: `a, a+K-1, a+1, a+K-2, ...`. Odd and even positions occupy disjoint consecutive subintervals whose union is `[a,a+K-1]`. For every `j=1,...,K`, direct substitution gives

\[
|f(w_{j-1})-f(w_j)|=K-j+1.
\]

Thus every remaining label and every remaining difference is used once. The prefix is unchanged.

### Active endpoint below the interval

If `f(w0)=a-1`, reflect the preceding values through the map `x -> 2a+K-1-x`. Equivalently,

\[
f(w_j)=
\begin{cases}
a+K-1-(j-1)/2,&j\text{ odd},\\
a-1+j/2,&j\text{ even}.
\end{cases}
\]

The labels alternate `a+K-1, a, a+K-2, a+1, ...`; differences remain `K,K-1,...,1`. Reflection preserves pairwise differences and the interval. This proof handles `K=1` and both parities without an additional endpoint assumption.

This is a path-consumer argument. Replacing the path by an arbitrary branched suffix is a different theorem, even if both resource sets have the same sizes.

## 4. Written retained-composition baseline

**Evidence level:** a derived project corollary, independently recalculated by the methods and implementation roles during assembly. It is implemented as `two_section_padded`, with implementation checks described separately in [CONSTRUCTION_IMPLEMENTATION.md](../docs/CONSTRUCTION_IMPLEMENTATION.md) and the verification record. It is not an additional upstream retained lemma, formal verification, or a historical novelty claim. It makes the retained-overlap comparison precise.

### 4.1 One-positive-branch prefix block

Use local parameters: `M>=1` unfinished edges, one branch with `q>=1` terminal leaves, and `z>=M+1` direct leaves. Let

\[
N=M+q+z+2,\quad t=M+2,\quad b=2M+q+3,\quad A=[M+2,M+q+1].
\]

Label the local root zero, the branch center `b`, the named terminal leaves bijectively by `A`, and the outgoing next-spine vertex `M+1`. Use every remaining value in `[M+2,N]` once on the named direct leaves.

The branch interval has `q` labels. The center lies strictly above it, since

\[
b-(M+q+1)=M+2>0.
\]

It lies within the final local alphabet because

\[
N-b=z-M-1\ge0.
\]

The high interval contains `N-M-1=q+z+1` values; after removing `q` terminal labels and one center, exactly `z` remain for the direct leaves. No missing or extra direct leaf is created.

Reflection by `b` permutes `A`:

\[
b-A=A.
\]

The root-to-center difference is `b`; the branch's terminal differences are precisely `A`; each direct-root edge uses its direct-leaf label as difference; the outgoing edge has difference `M+1`. All labels and differences in `[M+1,N]` are consumed exactly once, leaving labels and differences `[1,M]` and active label `M+1`.

This is the one-branch specialization of the retained L010 formula. H010 uses the same formula on its more restricted one-branch domain. The calculation does not require `q<=M+2`; that generic H010 condition is unnecessary for this single-branch specialization. [U03]

Crucially, the calculation concerns only this prefix and its outgoing vertex. It does not assume the internal topology of the unfinished `M`-edge tree. Completion of that tree requires a separate consumer. This is why the calculation can be used to investigate composition while the existing complete-constructor API still requires its stated caterpillar suffix.

### 4.2 Apply the first block

For B2-P1 put `K1=r+z1+K+2` and assume

\[
z_0\ge K_1+1,\qquad z_1\ge K+1.
\]

The full edge count satisfies `m=K1+q+z0+2`. Apply the preceding prefix block with `M=K1` to `s:0`, its branch, its direct leaves, and outgoing vertex `s:1`. The used high values/differences are `[K1+1,m]`; the root uses zero. Its only remaining port is `s:1`, with label `K1+1`. The remaining unused labels and differences are exactly `[1,K1]`.

### 4.3 Apply and embed the second block

Consider the unfinished tree rooted at `s:1` in a local alphabet `0..K1`. Its local edge count is `K1=K+r+z1+2`. Apply the one-branch prefix calculation with `M=K`, branch size `r`, and direct-leaf count `z1`. Write its local labels as `g`, with `g(s:1)=0` and `g(s:2)=K+1`.

Map each local assigned label to the actual label

\[
f=K_1+1-g.
\]

The local root maps to the already assigned `s:1=K1+1`. Every other local label is in `1..K1`, so its image is also in `1..K1` and cannot collide with the first block. The map is injective and preserves every absolute difference on actual second-block edges. The second block consumes differences `[K+1,K1]`, disjoint from the first block's `[K1+1,m]`.

Unused local labels `[1,K]` map exactly to `[K1-K+1,K1]`; unused differences remain `[1,K]`. The actual return label is

\[
f(s:2)=K_1+1-(K+1)=K_1-K,
\]

one below the returned interval. Section 3 finishes the exact suffix path. These label/difference partitions, rather than an appeal to separately graceful pieces, establish the intended compatibility calculation.

### 4.4 Review boundary and regression duties

The independent recalculations check the quantified parameter domain, alphabet sizes, the single shared root, the exact edge partition, and both inventory transformations. Any implementation revision must preserve every named vertex and use the actual `s:2` port. These are narrow regression/review duties, not a reason to launch a larger search campaign. The package's dedicated prefix helper keeps this derivation separate from the complete L010/H010 APIs' narrower suffix contract.

This baseline establishes no claim for zero direct leaves, because `z1>=K+1>=2`. A violation of its sufficient bounds is not a counterexample to its construction on its domain, and is not a nongraceful tree. Repeating another block requires another quantified budget/interface calculation; arbitrary iteration is not adopted here.

## 5. Balanced supplier: discharged duties and remaining unequal seed

The [balanced-family proof](B2_BALANCED_SUPPLIER.md) establishes P01–P09 for the infinite domain `q=r=t>=1,z0=z1=0,K>=1`. It directly assigns the exact prefix; its label partition leaves `[t+2,K+t+1]`; its actual differences partition `[K+1,m]`; its active port is `s:2=K+t+2`; and Section 3's path consumer finishes in K steps. Independence follows from the explicit formulas, without solving the K-dependent whole target. Separate methods and implementation roles recalculated this argument.

The implementation and independent certificate checks are reported separately. P10 remains a scope/overlap duty for any novelty claim: the padded retained construction is compared, current subcubic coverage is recorded, and no historical priority is asserted. The proof does not discharge P01–P09 for unequal branches or a further branched suffix. `FINDINGS.md` owns accepted findings and `STATE.md` owns current work.

B2-UNEQUAL-SEED-001 is now disposed as an **exhausted restricted negative** (full record: [B2_UNEQUAL_SEED.md](B2_UNEQUAL_SEED.md)). The eight-vertex prefix with A-side `0..3` / B-side `4..7` bijective domains and pin `h(s:2)=4` has no graceful labeling: the analytic obstruction (difference 1 forces `h(s:1)=3`; `a+2b−x=18` admits only `(a,b,x)∈{(5,7,1),(6,7,2),(7,6,1)}`; every resulting assignment duplicates difference 4 on at least two actual edges) was confirmed by independent recomputation and a separate reviewer challenge, and both the declared bounded DFS and the direct permutation oracle exhausted the declared scope with 0 solutions on the same original graph digest. The falsified claim is exactly that alpha/physical-port template — not the unrestricted eight-vertex tree, not any other restriction set, and not the unequal B2 family at any K.

The proposed all-K high-side-shift transport is **retained as a conditional identity only**: it is correct that a valid seed, if one existed, would supply every `K>=1` of the declared family (unused labels `[4,K+3]`, unused differences `1..K`, port `s:2=K+4` one above, consumer terminating in K steps), but its antecedent is false, so it discharges no P07 obligation and is not implemented as a supplier. P07 remained open under that false-premise template; the separate port-5 construction below now satisfies the independent-supply requirement for the revised nonadjacent interface on `q=1,r=2,K>=2`. A successful fixed seed plus a proved parameterized transformation can satisfy P07; a different searched full-tree prefix for every K cannot establish the same quantified conclusion. The previously queued next task — the specific alternative port rule `h(s:2)∈{5,6,7}` on the same named target (see [NEXT_TASK.md](NEXT_TASK.md)) — is now **recorded superseded, not executed**: for `p∈{5,6,7}` the same high-side shift still returns unused labels `[4,K+3]` and unused differences `1..K`, but places the physical port at `K+p`, not the adjacent port `K+4` (one above the interval) that the Section 3 consumer requires, and at `K=1` the single suffix edge would have difference `p−3∈{2,3,4}` instead of 1. The full supersession reasons are in `NEXT_TASK.md` and decision D016.

The external independent acceptance review of the B2-UNEQUAL-SEED-001 checkpoint (November 21, 2026; pack custody at `evidence/reviews/B2_UNEQUAL_SEED_001/`) established a stronger scoped result, adopted as [B2_INTERFACE_OBSTRUCTION.md](B2_INTERFACE_OBSTRUCTION.md) (independently accepted at reviewed revision `2cfb2df`; D018): for `q=1,r=2,z0=z1=0` and every `K>=6`, no injective prefix labeling leaves unused labels `[ell,ell+K-1]`, unused differences `1..K`, and port `ell-1` or `ell+K` for any `ell` or side, with no alpha assumption and no root pin. The old adjacent-port interface is therefore impossible for this family at `K>=6` (threshold sufficient; sharpness not established; `K=1` has the preserved `ell=1`, above-side witness; `K=2..5` are not adjudicated here). A different interface now has a separately reviewed conditional path consumer: for integer `K>=2`, unused labels `[ell,ell+K-1]`, unused differences `1..K`, and the physical port `ell+K+1`, the recurrence in [B2_NONADJACENT_CONSUMER.md](B2_NONADJACENT_CONSUMER.md) completes the exact original K-edge path. K=1 is impossible for this interface. This is not a revision of P05's adjacent-port contract: it is a different consumer. The port-5 fixed seed now independently supplies a compatible original-graph prefix for exactly `q=1,r=2,z0=z1=0,K>=2`, via the explicit formulas and proof in [B2_NONADJACENT_SEED_P5.md](B2_NONADJACENT_SEED_P5.md). This discharges the revised nonadjacent analogue of P05 and P07/P08 for that domain, not literal adjacent-port P05. A separate previously checked K=1 witness gives ordinary gracefulness for that one case, not the nonadjacent interface. This does not change the discharged balanced duties, the retained conditional transport, or the padded construction.


The revised nonadjacent resource interface now has an explicit independent supplier for **all integers `q,r>=1,K>=2` with `z0=z1=0`**, not only `(q,r)=(1,2)`: see [B2_UNPADDED_ALL_QR.md](B2_UNPADDED_ALL_QR.md), finding B2-UNPADDED-ALL-QR-001 and D021. Its actual prefix uses `[0,r+1] ∪ [K+r+2,m]` and differences `[K+1,m]`, leaving `[r+2,K+r+1]`, differences `1..K`, and port `K+r+3`. This discharges P01–P04 and P06–P09 for that domain with the **revised nonadjacent analogue of P05**, not the literal adjacent-port P05. P10 remains a scoped source-comparison duty, not a novelty claim. K=1, nonzero padding, further branched suffixes and arbitrary repeated sections are outside this theorem.

For K=1 and all integer `q,r>=1`, the separately reviewed [B2-UNPADDED-K1-001](B2_UNPADDED_K1.md) explicitly supplies the original prefix with the different contract `R={q+4}`, `D={q+3}`, port `s:2=1`; the actual edge to `s:3=q+4` consumes that difference. It establishes ordinary gracefulness on its exact target and, together with the K>=2 theorem above, for every positive integer `q,r,K` at zero padding. This K=1 contract does not meet literal P04, P05 or P08, which prescribe `D={1}` and an adjacent endpoint; those restrictions retain their meanings. The balanced K=1 supplier already meets the earlier contract for `q=r`, whereas other prescribed-boundary instances require their own proof or disproof. Nonzero padding, additional branched sections, and repeatable transitions remain separate obligations. Decision D022.

The [fixed-ell=2 obstruction](B2_INTERVAL_OBSTRUCTION.md) for the unit family at K>=3 is a proved reason not to extrapolate successful small ell=2 states. It does not constrain the balanced supplier's different interval.

## 6. Falsifiers and finite evidence

The pilot contains four explicit target/interface pairs, all with `z0=z1=0`, `K=1` and no pin on `s:0`: `(q,r,ell)=(1,1,1),(1,1,2),(1,2,1),(2,1,1)`, each on the above side. There are three named profiles, not four. Every pair asks its own finite existence question; the experiment does not assume that all four answers are positive. Independent development review identified the first pair as a restricted failure and the second as a positive control on the same graph. Their exact receipts and certificate belong in the authoritative findings/verification records.

An exhaustive failure at `ell=1` refutes a claim requiring that particular state on that graph. A witness at `ell=2` demonstrates that changing the interval can matter, and proves ordinary gracefulness of that finite graph after verification. Neither result proves a general independent supplier.

For a proposed formula `F` on domain `D`, a concrete tuple in `D` producing a P01–P08 violation is a formula counterexample. A tuple outside `D` is a coverage limitation. A finite solver timeout is neither. If the theorem says that one of several interfaces works, failure of only one interface does not falsify it.

An exhausted exact search can establish a finite negative only for the correctly encoded domain and restrictions. Record the full model and independently challenge the result where practical. The independent permutation oracle is a bounded implementation cross-check; it does not certify untested sizes. A solver's unsatisfiability report is not a proof-assistant certificate in this project.

## 7. Obligations for repetition beyond the first target

The [B4 unit supplier](B4_UNPADDED_UNIT.md) independently gives the exact above-side adjacent contract at original `s:4` on `[[1],[1],[1],[1]]+[[]]*(K+1)` for integer K>=1. It leaves labels `[6,K+5]`, differences `1..K`, and port `K+6`. The retained adjacent consumer completes the original path, including K=1, with completed alpha low-class size `6+(K+1)//2`. This result concerns one fixed branch pattern and a variable path length. Other four-section branch sizes and arbitrary repetition still need independent proofs.

The [B3 singleton and all-K selection proof](B3_UNPADDED_K1.md#deterministic-selection-for-every-positive-path-length) proves that the exact original unpadded `[[q],[r],[t]]+[[]]*(K+1)` is graceful for all positive integers q,r,t,K. At K=1 the independent prefix supplies `R={q+2}`, `D={t+3}`, and `s:3=q+t+5` for the one original edge to `s:4`. At K>=2 the accepted four cases below carry their own adjacent or nonadjacent contracts. The singleton conclusion leaves the earlier P04/P05/P08 meanings intact. Padding, multiple positive branches per section, further sections, and arbitrary repetition remain separate proof duties.

The [exceptional B3 supplier and selection proof](B3_UNPADDED_Q1_R2.md#coverage-and-deterministic-constructor-selection) close the `q=1,r=2,t>=3,K>=2` gap. For positive integers q,r,t and K>=2, choose the q>=r supplier, the q<r and t<=q+1 supplier, the q<r and t>=q+2 and r>=3 supplier, or the exceptional supplier, in that order. The last case follows since q<r<3 forces q=1,r=2. This proves ordinary gracefulness of the exact original unpadded three-section profile on the stated domain. All four branches supply `R=[a,a+K-1]` and `D=1..K` with `a=q+t+3`. The adjacent branch supplies `s:3=a+K`, and the other branches supply `s:3=a+K+1`. The direct singleton above covers ordinary gracefulness for K=1. Padding, multiple positive branches per section, further sections, and arbitrary repetition remain separate proof duties.

The [large-t B3 supplier](B3_UNPADDED_QLT_R_LARGE_T.md) proves the original zero-padding profile for integers `1<=q<r`, `r>=3`, `t>=q+2`, and `K>=2`. Its parity-based alpha seed supplies the shifted interval `[a,a+K-1]`, differences `1..K`, and the nonadjacent port `s:3=a+K+1`, with `a=q+t+3`. The first three suppliers left exactly `q=1,r=2,t>=3` outside their K>=2 domains, which the exceptional supplier now covers.

The [adjacent B3 supplier](B3_UNPADDED_QLT_R_ADJACENT.md) covers the original unpadded named three-section target for integers `1<=q<r`, `1<=t<=q+1`, and `K>=1`. It supplies `R=[a,a+K-1]`, `D=1..K`, and physical `s:3=a+K` with `a=q+t+3`. The original K-edge path uses those resources, including the singleton case. This discharges that contract on its domain. This adjacent contract applies only on its stated domain.

The separately accepted [B3-UNPADDED-QGE-R-001](B3_UNPADDED_QGE_R.md) constructs one three-section original target for every integer `q>=r>=1`, `t>=1`, `K>=2` with zero padding. Its prefix supplies `R=[q+t+3,q+t+K+2]`, `D=1..K` and actual port `s:3=q+t+K+4`; the accepted recurrence completes the original K-edge path. This is a fixed three-section family with a nonadjacent port, not literal B2 adjacent P05, an arbitrary transition, or a proof for `q<r`. K=1 needs a different interface; padding, extra branches, fourth sections and arbitrary repetition remain separate duties. See D023 and `FINDINGS.md` for disposition.

To promote a two-section supplier into a repeated construction, specify a state class `S`, a transition for the next actual section, and a domain of admitted input sequences. Prove that each admitted input reaches `S`, each transition receives independently available resources and preserves its invariant, and a finite measure decreases until a terminal consumer applies.

The state must carry the physical port, actual label or normalization map, both resource inventories, remaining topology, and any quota constraints needed later. A compact normalized representation is acceptable only after its equivalence to those facts is proved. A transfer-state transition valid for one parity or capacity regime does not automatically cover another. [U06]

The project can instead find a useful global reconstruction theorem. That alternative must recover the exact requested target and quantify source reachability; it need not preserve the earlier prefix labels. The repeated-prefix route is a research choice, not an additional condition imposed on the lobster problem itself.

### Four-section 111t boundary

The [B4 111t proof](B4_UNPADDED_111T.md) and separate AI reviews discharge
ordinary gracefulness for the exact `[[1],[1],[1],[t]]+[[]]*(K+1)`
profile for integers `t>=2,K>=1`. For K=1 the actual terminal
`s:5=4` consumes `R={4}`, `D={t+3}` at `s:4=t+7`, and the full
low-class size is t+6. For K>=2 the nonadjacent path at `s:4=t+K+6`
consumes `R=[t+5,t+K+4]`, `D=[1,K]`. The earlier unit constructor gives
the adjacent alpha branch for t=1. Thus the exact family is graceful for
all positive t,K through these three contracts. Varying any of the
first three branch sizes, padding, multiple branches in a section, further
sections, and arbitrary repetition still require independent proofs.

### Four-section 1121 boundary

The [B4 1121 proof](B4_UNPADDED_1121.md) supplies an above-side adjacent
interval for every integer K>=1 on exactly
`[[1],[1],[2],[1]]+[[]]*(K+1)`. The prescribed second third-branch leaf
attaches to physical `b:2:0`. Both inventories and the exact original
suffix from `s:4` yield the full alpha low-class size `6+(K+1)//2`.
This discharges the exact 1121 profile. Other unproved branch
placements and sizes, padding, multiple branches per section, further
sections and arbitrary repetition still require independent proofs.

### Four-section 1211 boundary

The [B4 1211 proof](B4_UNPADDED_1211.md) discharges the exact unpadded
`[[1],[2],[1],[1]]+[[]]*(K+1)` profile for every integer K>=1. Both
middle leaves remain at `b:1:0`. The original path from `s:4` uses
the two adjacent resources and completes an alpha labeling with
low-class size `7+(K+1)//2`. Other unproved placements and sizes,
padding, multiple branches per section, additional sections and
arbitrary repetition still require independent proofs.

### Four-section 2111 boundary

The [B4 2111 proof](B4_UNPADDED_2111.md) discharges the exact
`[[2],[1],[1],[1]]+[[]]*(K+1)` profile for integer K>=1. The second
first-branch leaf stays at `b:0:0`; the checked original suffix
starts at `s:4` and consumes both adjacent resources. The result
is alpha with low-class size `6+(K+1)//2`. The discarded
[exact port template](FAILED_HYPOTHESES.md#f-b4-2111-port-template)
has its own restricted obstruction. Other unproved branch sizes,
padding, multiple branches per section, additional sections and
arbitrary repetition require separate proofs.

### Zero-port extension and symbolic (q,1,1,1) coverage

The [zero-port lemma](ALPHA_ZERO_PORT_LEAF_EXTENSION.md) discharges
conditional finite repeated leaf addition at the same supplied
physical label-zero host. It preserves both ports and offsets.
With exit offset zero and the exact unfinished K-edge path,
the high-side shift and adjacent consumer give full alpha
low-class size p0+ceil(K/2). The retained unit seed establishes
the exact unpadded `[[q],[1],[1],[1]]+[[]]*(K+1)` family for all
integers q,K>=1. [3111](B4_UNPADDED_3111.md) is the only new
executable scope. Supplying label zero at another prescribed host,
other branch placements or sections, and arbitrary input topology
remain open. The same-host closure keeps its explicit hypotheses.

### Minimum-high extension and symbolic (q,r,1,1) coverage

The [minimum-high proof](ALPHA_MINIMUM_HIGH_LEAF_EXTENSION.md)
establishes conditional same-host finite closure with the supplied
minimum-high label and distance-one witness hypothesis. It discharges
the exact unpadded `[[q],[r],[1],[1]]+[[]]*(K+1)` family for positive
integers q,r,K. The original path from `s:4=K+r+5` consumes
`R=[r+5,K+r+4]` and `D=[1,K]`, giving completed alpha size
r+5+ceil(K/2). Extension of the topology witness along that path
is valid. Exporting a further relational state, supplying arbitrary
hosts, other unproved branch placements or sections, padding,
and arbitrary topology remain separate obligations. The only new
executable route is [1311](B4_UNPADDED_1311.md).

### Upper-block insertion and symbolic (q,r,t,1) coverage

The [upper-block proof](ALPHA_UPPER_BLOCK_LEAF_INSERTION.md) preserves
the extra incident-edge multiset at the updated threshold c+h.
The retained base supplies it at c=7 and keeps the minimum-high
second host, the zero first center, and exit offset one. The
fixed order of extensions and composition supplies the exact
`[[q],[r],[t],[1]]+[[]]*(K+1)` family for positive integers q,r,t,K.
The original path starts at s:4=K+r+5 with R=[r+5,K+r+4] and
D=[1,K], and gives full alpha size r+5+ceil(K/2). Only
[QR21](B4_UNPADDED_QR21.md) has new executable coverage.
Fourth-branch growth, other sections, padding, multiple branches
per section and arbitrary-host or topology supply remain separate.

### Fourth-size-two supply

The [direct Q112 proof](B4_FOURTH_2_SUPPLY.md) discharges the exact
`[[q],[1],[1],[2]]+[[]]*(K+1)` family for positive integers q,K
with original adjacent s:4=K+7, R=[7,K+6], D=[1,K], and full
alpha low size 7+ceil(K/2). Meeting the prescribed R241 join
with the earlier offset-one left supplier and this right
component is obstructed. The two separate 15-vertex diagnostic
prefixes have verified first witnesses at each of the declared
above-side exits. They give finite candidates. An independent
parameterized supplier for arbitrary (q,r,t,2) remains open.

### QR12 supply and retained lower-block predicate

The [lower-block insertion proof](ALPHA_LOWER_BLOCK_LEAF_INSERTION.md)
preserves the complete incident spectrum below the fixed threshold c
with the updated host label. The [QR12 proof](B4_UNPADDED_QR12.md)
discharges ordered (q,r,1,2) for positive integers q,r,K through
the directly checked 1212 seed and lower-then-upper growth at r>=2,
with exact Q112 reuse at r=1. The original adjacent s:4=K+r+6
has R=[r+6,K+r+5], D=[1,K], and gives completed alpha low size
r+6+ceil(K/2). Both post-growth predicates are proved in the
specified order. Third-branch growth with fourth size two, broader
hosts or topology, mixed-operation repetition and any further
exported relational state require their own proofs.

### Third-branch growth with a supplied zero host

The [conditional insertion](ALPHA_ZERO_HOST_LEAF_EXTENSION.md)
preserves a supplied normalized alpha state and both named ports
when the zero host lies within one edge of the supplied witness.
The exact fixed-low adjacent extension fails for t>=3 and the
relabeled zero-host adjacent 1122 seed query exhausted with
zero solutions. [Proof and restricted outcome](B4_THIRD_ZERO_HOST_SEED.md)

The later nonadjacent and direct suppliers below discharge the
ordinary (1,1,t,2) family with their own interfaces. The
fixed-low result and exact zero-host adjacent restriction retain
their original scopes.

### Nonadjacent zero-host supply for third-branch growth

The [fixed nonadjacent seed and composition](B4_THIRD_ZERO_HOST_NONADJACENT.md)
discharge ordinary gracefulness on the exact (1,1,t,2) family
for integers t>=2,K>=2. Zero-host growth preserves the supplied
normalized alpha state with exit offset one, and the high shift
returns physical s:4=K+8, R=[7,K+6], D=[1,K].
The actual K-edge path then consumes both inventories.
This K=1 interface fails. The separate direct singleton
below supplies all positive t at K=1.

### Direct K=1 zero-host supplier

The [ordinary extension and resource reduction](B4_THIRD_ZERO_HOST_K1.md)
would carry a complete 16-vertex zero-host seed to every t>=2
at K=1 on the exact (1,1,t,2) family. The complete derived
control for t=2 has host label 2. The separate first-witness
query with sole b:2:0=0 reached its declared node cap and
left the seed and actual singleton resources undetermined.
The later direct construction below supplies this case independently
of that incomplete query.

### Direct K=1 supply and combined (1,1,t,2) coverage

The [direct proof](B4_THIRD_ZERO_HOST_K1_DIRECT.md) discharges
the named K=1 supplier for all positive t, with R={5}, D={6}
and physical s:4=11. The exhaustive parameter split with
the retained t=1 adjacent and t,K>=2 nonadjacent branches
discharges ordinary gracefulness for the exact (1,1,t,2)
family at all positive t,K. Each branch retains its own
interface. Separate obligations include larger first or
second branches with growing third branch, padding, multiple
branches per section and extra sections. The unselected
spine-maximum and C=14 placements were left open.

### First-branch insertion and (q,1,t,2) coverage

The [general-host proof](ALPHA_UPPER_BLOCK_GENERAL_HOST.md)
requires the full incident multiset and supplies its updated
predicate. The named compatibility proof keeps both physical
hosts and both offsets. The [Q1T2 proof](B4_UNPADDED_Q1T2.md)
discharges ordinary gracefulness on the exact (q,1,t,2) family
for integers q>=1,t>=2,K>=2. Its nonadjacent physical s:4 path
uses R=[7,K+6] and D=[1,K] after the high shift.
The retained t=1 and q=1 singleton results remain in force.
The rooted-core construction below discharges the remaining K=1
domain.

### Rooted-core K=1 supply and complete (q,1,t,2) coverage

The [rooted-core proof](B4_Q1T2_K1_ROOTED_CORE.md) discharges
gracefulness with physical s:2=q+11 on the exact deleted-third
core for integer q>=2. Translating that core and restoring
the original third center at zero gives a singleton at s:4=6
with R={5} and D={1} on every original t>=2 at K=1. The
previously proposed fixed retained-label single-cut extension
fails only on its own restrictions.

For positive integers q,t,K, the new singleton, the retained
q=1 singleton, Q112 at t=1, and Q1T2 at t,K>=2 exhaust the
exact original (q,1,t,2) family. This is ordinary gracefulness
with separate interfaces. The restricted second-branch
growth at q=1,t=2 is discharged below for K>=2. Broader
original profiles remain separate.

### 1R22 normalized supply and nonadjacent completion

The [1R22 proof](B4_UNPADDED_1R22_SUPPLIER.md) discharges
second-branch supply on the exact normalized `[[1],[r],[2],[2],[]]`
for integer r>=2. At threshold 1 the supplied original zero
terminal has one incident edge at the maximum host. The
growing first-port label is r+4; the high exit offset stays
one. Both the complete incidence predicate and the same
original witness persist. This supplies normalized alpha
labelings independently of finite diagnostics.

After a high shift by K, R=[r+6,r+K+5] and D=[1,K] are
consumed at physical s:4=r+K+7 on the original nonadjacent
K-edge path, for integer K>=2. The direct K=1 singleton below
completes the exact 1R22 scope. Broader original profiles
remain separate.

### Rooted-core 1R22 singleton and exact all-positive coverage

The [1R22 K=1 rooted-core proof](B4_1R22_K1_ROOTED_CORE.md)
gives the exact 14-vertex deleted-second core with physical
s:1=0 and realizes the conditional translate-and-restore
lift for integer r>=2. The resulting direct prefix leaves
R={r+3}, D={5} at physical s:4=r+8, and the original
s:4--s:5 consumes both. Finite same-name growth preserves
the maximum second center and the original zero terminal.

The selector exhausts positive integers r,K using the retained
r=1 constructions, the preceding r,K>=2 supplier, and this
K=1 supplier on the exact ordered (1,r,2,2) profile. The restricted additional
third-branch growth at r=2 is supplied below for K>=2.
Broader profiles require separate supply.

### 12T2 independent zero-host supply and nonadjacent completion

The [12T2 proof](B4_12T2_ZERO_HOST_SUPPLIER.md) discharges
the explicit A(17,8;1,1) seed on the exact normalized 1232
prefix with zero at the original third center. The old
witness, physical ports and complete alpha spectrum meet
the retained zero-host lemma's hypotheses. Its application
discharges normalized alpha supply A(t+14,8;1,1) for exact
integer t>=3, with finite pointwise named closure.

High shift and the nonadjacent numerical path give ordinary
gracefulness for exact t>=3,K>=2, with R=[8,K+7], D=[1,K],
and physical s:4=K+9 on the original ordered full profile.
The exact (1,2,t,2) family is covered for all positive t at
K>=2 after adjoining the retained t=1 and t=2 routes. The
rooted-core singleton below supplies the remaining K=1 domain.
Broader original profiles require separate supply.

### 12T2 rooted core and exact all-positive coverage

The [ordinary insertion lemma](ORDINARY_CUT_LEAF_INSERTION.md)
requires the full cut-crossing multiset and returns an updated
cut and host label. The [12T2 K=1 proof](B4_12T2_K1_ROOTED_CORE.md)
checks its one-leaf instantiation and supplies the exact
14-vertex deleted-third core with physical s:2=13. Thus
the conditional lift produces ordinary gracefulness at
t>=3,K=1 and leaves R={6}, D={6} at physical s:4=12.
The original s:4--s:5 completes both resources and the
named third-leaf growth preserves all prior labels.

The four disjoint cases of the selector cover all positive
integers t,K on the exact (1,2,t,2) family. The prior t=1,
t=2 and nonadjacent t>=3,K>=2 routes retain their individual
interfaces. The fixed third size three
and K>=2 case is supplied below. Broader profiles remain
separate.

### 1R32 minimum-high supply and original nonadjacent completion

The [1R32 proof](B4_1R32_MINIMUM_HIGH_SUPPLIER.md) discharges
normalized alpha supply on the exact `[[1],[r],[3],[2],[]]`
for integer r>=3. The retained 1232 seed supplies a minimum-high
second center, so the ordered extension gives A(r+15,r+6;1,1)
with the same witness and the third center still zero.

Shifting at the updated cut r+6 leaves R=[r+6,r+K+5] and
D=[1,K] at physical s:4=r+K+7. The original nonadjacent
path gives ordinary gracefulness for r>=3,K>=2. With the
retained r=1 and r=2 branches the exact (1,r,3,2) family
is covered for every positive r at K>=2. The singleton
below discharges the remaining fixed-third K=1 obligation.

### 1R32 rooted core and exact all-positive coverage

The [1R32 rooted core proof](B4_1R32_K1_ROOTED_CORE.md) checks
the retained core at cut 3 and uses its full crossing spectrum
[7,13] to supply the graceful core with physical s:2=r+11 for
each exact r>=3. It discharges the direct K=1 singleton at
physical s:4=r+10 with R={r+4}, D={6} for fixed third size three.
The returned core and completed cuts support finite named growth,
and the original third-branch lift commutes pointwise with it.

The selector combines the new singleton with the retained r=1
and r=2 singleton cases and the earlier K>=2 cases to cover
positive r,K on the exact ordered (1,r,3,2) profile. The next
result addresses the normalized r>=3,t>=4 case and its K>=2 completion.

### 1RT2 two-host compatibility and nonadjacent completion

The [conditional compatibility lemma](ALPHA_MINIMUM_HIGH_ZERO_HOST_COMPATIBILITY.md)
preserves the supplied physical minimum-high and zero hosts,
both actual ports and offsets, the witness, and the ordered
leaf-name lists under every finite interleaving.

The [1RT2 construction](B4_1RT2_TWO_HOST_COMPATIBILITY.md)
discharges both host premises on the explicit 1232 seed, gives
A(r+t+12,r+6;1,1) on the exact normalized profile for r>=3,t>=4,
and proves ordinary original-path completion for K>=2. The
disjoint selector extends that K>=2 coverage to all positive r,t.

K=1 remains outside the accepted nonadjacent interface. The
direct singleton below meets that case by an ordinary core lift.

### 1RT2 direct singleton and all-positive selection

The [direct 1RT2 proof](B4_1RT2_K1_DIRECT_SINGLETON.md)
uses the independently supplied core with maximal physical
s:2 to settle the exact remaining K=1 corner r>=3,t>=4.
The direct prefix uses R={r+4}, D={6} at physical s:4=r+10.
The original edge s:4--s:5 consumes both resources.
The complete ordinary crossing-cut predicate supports finite
second-host additions pointwise compatible with third zero-host
additions.

The disjoint selector combines this case with retained K=1
and K>=2 suppliers to prove ordinary gracefulness on the exact
ordered (1,r,t,2) family for all positive r,t,K. First-branch
growth beyond size one is a separate supply obligation.

### 1342 fixed-ledger obstruction and remaining first-host supply

The [fixed-ledger result](B4_1342_FIXED_LEDGER_UPPER_BLOCK_OBSTRUCTION.md)
rejects first-branch general-host upper-block insertion on
the retained 1342 state with the prescribed anchors.
All permitted thresholds fail the necessary difference-sum
test for any positive batch. The retained 1122 positive
control confirms the conditional lemma on its own state.

The fixed-ledger result led to the three-pin supply question
on the same original. The next proof discharges that question.

### 1342 all-ledger obstruction at three fixed pins

The [all-ledger proof](B4_1342_ALL_LEDGER_PINNED_OBSTRUCTION.md)
discharges the exact three-pin supply question negatively
for the prescribed port-preserving operation. At every
permitted threshold the selected edge count misses the
necessary count, and every positive batch has a nonzero
sum defect. A relabeling with all three numerical pins
therefore cannot supply the transition.

The next experiment relaxed only the first-host numerical
label. Its reviewed outcome is recorded below.

### Relaxed first host on the original 1342 graph

The [restricted exhaustion](B4_1342_RELAXED_HOST_SEED_RESULT.md)
discharges seed existence negatively with b:2:0=0, s:4=10,
a in [2,8], c in [11,18], the forced alpha orientation and
full selected spectrum [c-a,18]. The necessary prefilter
accounts for all 56 pairs. The positive transport therefore
has no supplied fixed seed. The all-positive (1,r,t,2) result
remains accepted.

The subsequent adjacent-exit question kept the named graph,
zero host, relaxed host domain and alpha orientation. Its
disposition is below.

### Adjacent exit on the original 1342 graph

The [structural proof](B4_1342_U9_STRUCTURAL_OBSTRUCTION.md)
discharges the relaxed-host incidence supply negatively at
physical s:4=9, b:2:0=0, a=2..8 and c=10..18. The same
argument rejects every positive batch because the operation
needs the exact selected spectrum. The subsequent
[label-one closeout](B4_1342_U9_A1_ANALYTIC_CLOSEOUT.md)
discharges the remaining U=9, a=1 case negatively. The
same proof records the complete two-exit disposition and
preserves the evidence basis of each row.

### Joint maximum-rooted ordinary core supply

The proposed named core `[[q],[r],[],[2],[],[]]` for q,r>=2
requires an independent graceful labeling with the maximum
at original physical s:2. The [joint pilot](B4_JOINT_MAX_ROOTED_CORE_PILOT.md)
rejects transfer from both retained fixed ledgers and records
the sole q=r=2 query as INCOMPLETE. The
[direct-ledger proof](B4_JOINT_22_DIRECT_LEDGER.md) supplies
the fixed q=r=2 core with maximum 14 at physical s:2 and zero
at s:3. Its lift supplies the K=1 target for every positive
integer t. The [cut proof](B4_JOINT_22_CUT_COMPAT.md)
supplies repeatable first growth, extending this to all q>=2
at r=2 and K=1. It rejects the exact second-host operation
on the seed and first one-leaf output. The
[C(2,3) supplier](B4_JOINT_23_MAX_ROOTED_CORE.md)
now gives the exact maximum-rooted ledger and fixed q=2,r=3
all-t K=1 lift. First growth is repeatable at its c=12 cut.
Its second-host cut fails. The
[alternative C(2,2) ledger](B4_JOINT_SECOND_CENTER_CUT_READY_22.md)
now supplies all second growth at q=2 and its exact K=1
lift for all r>=2,t>=1. Composition of the distinct
retained r=3 first-growth ledger gives all q>=2,t>=1 at
r=3,K=1. The [nested-cut proof](B4_JOINT_NESTED_CUT_TWO_HOST.md)
now discharges shared growth and joint maximum-rooted supply for
all exact q,r>=2, with named labels preserved under finite batch
interleavings. Its lift covers all positive t at K=1. The retained
q=1 and r=1 routes complete the all-positive q,r,t coverage at K=1.
Continuation for q,r,t>=2,K>=2 remains open. The
[single-gap test](B4_K2_D062_TWO_EDGE_TRANSPORT.md)
exhausts only the exact D062 transport with both suffix orders
at q=r=t=K=2. It supplies no valid two-edge consumer state.
The [two-gap test](B4_K2_D062_TWO_GAP_ORDER_PRESERVING.md)
also exhausts all hole pairs and both suffix orders for the fixed
D062 prefix ranking on the same exact target. It reaches two
additional valid prefixes and neither supplies a two-edge
completion.
The [adjacent-exit test](B4_K2_D062_S4_ADJACENT_RANK.md)
rejects the two exact adjacent exchanges of the D062 port's
rank at the same target. The second exchange also has a
structural repeated-difference obstruction. A structurally
independent supplier or continuation is still needed for
the interior. These finite rank restrictions do not settle
ordinary gracefulness of the smallest interior original.
The [analytic alpha supplier](B4_K2_ALPHA_PREFIX_S4_9.md)
now supplies the exact smallest interior original at q=r=t=K=2.
Its independently verified two-edge interface has R={8,9},
D={1,2}, and physical s:4=11 after the high shift. The finite
result discharges that target.
The [fixed-profile continuation proof](B4_2222_NONADJACENT_ALL_K.md)
now discharges all exact K>=2 at q=r=t=2. It shifts only
D066's high labels and composes the numerical nonadjacent
consumer on the actual path from s:4, with both exact
inventories proved. The D062 K=1 supplier stays separate.
The [third-center extension](B4_22T2_ZERO_HOST_ALL_TK.md)
discharges the fixed q=r=2 case for all exact t,K>=2 while
retaining the D066 physical port, witness and D067 consumer.
D037 and D062 cover its remaining positive boundary cases.
The joint supply for arbitrary q,r,t>=2 and K>=2 remains open.
The [first-host obstruction](B4_D068_FIRST_HOST_UPPER_BLOCK.md)
discharges the proposed upper-block premise negatively on the
exact D066 ledger at fixed r=t=2 and s:4=9. Its sum proof rejects
all positive batches on that ledger for the seven admissible cuts.
The [alternative first-host supply](B4_D069_ALT_ALPHA_FIRST_HOST.md)
now discharges the same-original seed question with s:4=9,
b:2:0=0, a=5 and c=10. Its proved two-host composition supplies
q,t,K>=2 at fixed r=2, with the fourth branch fixed at size two.
The [second-host obstruction](B4_D070_SECOND_HOST_LOWER_BLOCK.md)
rejects the lower-block premise and every positive batch at
the original b:1:0 on every D070 map for q,t>=2. Supply for
variable interior r remains open. The
[pinned dual-block obstruction](B4_D071_PINNED_DUAL_BLOCK_OBSTRUCTION.md)
rejects the simultaneous complete premises on the same named
2222 original whenever b:0:0=5, b:2:0=0 and s:4=9 under the
normalized alpha orientation. The
[unpinned first-host obstruction](B4_D072_UNPIN_FIRST_HOST_DUAL_BLOCK.md)
rules out the same joint premise for all allowed a=1..7
with physical s:4=9 and b:2:0=0. The
[exit-eight obstruction](B4_D073_U8_DUAL_BLOCK_STRUCTURAL.md)
rules out the same premises at s:4=8, keeping the zero-host pin
and the first-host label free. The
[exit-ten result](B4_D074_U10_DUAL_BLOCK_FEASIBILITY.md)
rules out simultaneous supply at s:4=10 under the same zero-host
pin and free first-host label. Its hypothetical high-shift gate at
K=2 fails independently. The [direct 2322 supplier](B4_D075_DIRECT_2322_ALPHA_S4_10.md)
discharges normalized supply at low size 9 and physical s:4=10.
It also discharges the original nonadjacent continuation at fixed
ordered 2322 for all exact K≥2. Its ledger places 7 at b:2:0 and
17 at b:1:0, so third-host zero extension and minimum-high second-host
extension cannot be invoked on that ledger. The former independent
zero-host 2322 seed question is **DEFERRED / UNSTARTED** under D077.

### R241 paired branched-spine supply

The owner selected [LCL-R241-PAIRED-BRANCHED-SPINE-001](../tasks/LCL_Codex_R241_Arbitrary_Branched_Spine_2026-11-22.md). Prove the independent single-section and paired suppliers, verify the R241 connector on the actual spine and the returned offset at every join, induct over any finite number of modules, and account for the label and difference complements on the original suffix. The direct-leaf variants require one actual center per section. Zero quota denotes `[0]`, distinct from `[]`. This is a candidate pending execution and separate reviews.
