# Existing pieces of a general lobster-labeling construction

**Review date:** November 20, 2026, Pacific/Honolulu  
**Question:** Have Math Discovery Lab and MDL Bounded Search already found pieces of a rule that could work for every finite lobster tree?

## Executive finding

**Yes. Both repositories contain more than successful numerical examples. They contain parameterized constructions for infinite families, exact local completion theorems, compatible-state suppliers, and operations that can be repeated within stated domains. Neither audited repository assembles these into a construction or existence proof covering every finite lobster.**

The earlier characterization of the projects as mainly testing specific numerical cases was incomplete. The most useful next scientific objective is to connect or broaden the existing constructions by proving a missing input-supply, compatibility, reconstruction, or continuation theorem. Recreating the same exact equation, enlarging a test table without a discriminating hypothesis, or adding another conditional operation without its required inputs would not by itself address that gap.

There are three distinct meanings of “a master equation”:

1. **An equation that describes or counts all valid answers:** already present in N240 and the Bounded Search mathematical specification.
2. **A formula or algorithm guaranteed to construct an answer for an entire specified family:** already present in several records, including N33, N121, N135, L007, L010/H010, and restricted module chains.
3. **A construction or existence proof covering every finite lobster:** unresolved in the audited commits.

A proof of existence would also meet the universal goal, even if it did not give a fast or simple formula.

## Scope and evidence

| Repository | Audited default-branch commit | Relevant current state |
|---|---|---|
| Math Discovery Lab | 858a8c1fcfda87ba40bb1adee498a6131504a803 | N248 is the latest completed scientific cycle. Exact-spine M0–M1 are documentation/baseline completion; mathematical M2 remains open. |
| MDL Bounded Search | e48b94eec4091b4fe189e325cab2eda464409943 | P004 is completed. P005 remains incomplete on an admission-safety hold; its genuinely branched-suffix study has not run. |

Sources: [MDL current state][mdl-state], [exact-spine plan][spine-plan], [Bounded current state][bs-state], [P004 completion report][p004].

This is a read-only audit of committed mathematical arguments, adopted dispositions, corrections, review records, and relevant computational reports. Three separate source-review tasks covered earlier MDL constructions, recent MDL mechanisms, and Bounded Search; the main review inspected the decisive primary passages and reconciled their implications.

No repository was modified, no new research campaign was launched, and no mathematical program, solver, certificate replay, or formal proof checker was run. This is not a fresh certification of every proof or every archived computation. Repository descriptions such as “SCOPED PASS” refer to the recorded written argument and separate AI review, not human peer review or proof-assistant verification.

The scope is the two GitHub snapshots. Newer findings that exist only in local LBT folders or previous attachments are not established by this review. Current world-literature status and originality were not independently re-audited.

## 1. What the input actually is

A graceful labeling assigns the integers 0 through m to the m+1 vertices of a tree so that the absolute differences on its m edges are exactly 1 through m, each once.

A lobster can be described by a path called its spine, the branches attached to each spine vertex, and the number of leaves on each branch. A branch with zero additional leaves is just a direct leaf. Thus the input is the **whole structure**, not only the total number of edges. Different trees of the same size can need different numbering choices.

The Bounded Search profile representation records this structure explicitly. For a spine with k edges and branch leaf counts q_ij, the total number of edges is

\[
m=k+\sum_{i,j}(1+q_{ij}).
\]

A single tree may admit more than one profile. Consequently profile counts should not be reported as counts of distinct tree isomorphism classes. [Source: mathematical specification, §1][bs-math]

## 2. The strongest existing assets

| Asset | What is established | Why it is useful | Restriction still present |
|---|---|---|---|
| MDL N33 | Explicit labeling F_h for every h≥8 in a fixed two-Y family | A literal formula valid for infinitely many inputs | It lengthens one fixed topology; it does not vary arbitrary branching |
| MDL N121 | Arbitrary-length joins of unequal height-two factors with independently supplied compatible labels | Both input construction and repeated composition are given | All terminal counts odd; specific first/later root-degree parities |
| MDL N135 | A binary recurrence and capacity conditions, plus an unconditional restricted mixed-factor family of arbitrary length | Makes transfer choices explicitly; admits repeated all-even interior factors | Degree, parity, quota-size, and fixed-model conditions remain |
| MDL N145 | Paired unequal-order two-port block construction | Tracks both entry and exit vertices and fills every connector difference | Valued-copy pairing and specific input profiles remain |
| MDL R226 | Exact constructive two-host leaf-completion criterion | Determines feasibility and extracts a completion without assuming one already exists | Successful core labeling and remaining resource inventories must be supplied |
| MDL R232 | Exact simultaneous allocation for reserved batches under its forest and capacity conditions | Removes the need to supply successful per-batch quota splits | Both palette partitions and passing global conditions remain inputs |
| MDL R241/R246 | Explicit module suppliers and reusable port-based composition | A genuine supplier-to-consumer chain for parameterized families | Actual port choices, adjacent compatibility and alpha restrictions |
| MDL R243 | Exact fixed-leaf connector relation and reusable assembly | Can connect certain mismatched module offsets | Inserts an expanded connector topology |
| MDL R248 | Reusable whole-component reflection from a graceful source | Can change branch placement without an alpha hypothesis | Requires an already graceful source and suitable movable groups |
| Bounded L007 | Formula for arbitrarily many equal-size positive branches, plus direct leaves | A complete infinite-family construction at the stated budget | Isolated cluster plus terminal next edge; no later suffix remains |
| Bounded L010/H010 | Branched first section followed by any prescribed caterpillar suffix | One construction leaves exactly the interface the next construction needs | Direct-leaf budget and, for H010, branch-size bounds; no arbitrary branched suffix |
| N240/Both repositories | Exact full-incidence counting recurrence | Common mathematical specification and finite reference computation | No proof that the count is positive for every lobster |

Primary evidence: [N33][n33], [N121][n121], [N135][n135], [N145][n145], [R226][r226], [R232][r232], [R241][r241], [R246][r246], [R243][r243], [R248][r248], [Bounded lemmas][bs-lemmas], [H010 proof][h010], [N240][n240].

### 2.1 N33 already answers the “any number” idea for one family

N33 begins with a completely specified 18-vertex seed K. It keeps the two Y-shaped attachments at spine positions 4 and 11 and extends the terminal spine.

For every integer h≥8, put q=h−6. Its formula is

\[
F_h(z)=f(z)+q \quad \text{for each old seed vertex }z,
\]

\[
F_h(v_{12+2j-1})=17+q+j,\qquad
F_h(v_{12+2j})=q-j,\quad j=1,\ldots,q.
\]

The old edge differences remain 1,…,17. Every new pair of spine edges contributes the next two unused differences. The vertex-label intervals are disjoint and exhaustive, so the argument applies to every allowed h, not just the displayed h=8 example.

This is exactly a “feed in a size parameter, obtain the numbering” formula. Its limitation is structural: changing h extends this particular tree pattern. It says nothing about arbitrary new branches or their distribution. [Proof and recorded review][n33]

### 2.2 N121 and N135 go beyond one growing example

N121 accepts an arbitrary finite sequence of prescribed height-two rooted pieces and joins their roots along a path. Their sizes need not be equal and need not grow in a particular order.

For the main family, every branch has a positive odd number of terminal leaves; the first root has odd branch degree at least 3 and later roots have even branch degree at least 2. The construction independently produces the compatible aggregate labeling and the required branch placement. It does not merely assume that separately graceful pieces will fit together.

This is repeatable composition by simultaneous relabeling: one may reconstruct the labeling of the enlarged tree. It is not a claim that every old number stays unchanged when a piece is appended. The source explicitly identifies the family as an application/reconstruction of established transfer and path-composition mathematics, not demonstrated new ordinary-family coverage. [N121 complete construction and coverage discussion][n121]

N135 extends the mechanism through a binary recurrence. Its unconditional family permits an arbitrary number and arrangement of qualifying all-odd or all-even later factors. The restrictions are substantial: first root degree odd and at least 5; later root degrees divisible by four; later odd quotas at least 5 or even quotas at least 4, with each such factor entirely odd or entirely even. The generic criterion can admit additional cases, but its failures only exclude the specified model. [N135][n135]

The practical conclusion is that MDL already possesses mechanisms that work at unbounded spine lengths. The remaining difficulty is not simply “make the tree longer”; it includes arbitrary branch counts, mixed small quotas, direct leaves, and compatible boundary states.

### 2.3 N145 is another composition route, with a different boundary

N145 gives actual compatible labelings for certain diameter-five inputs and joins blocks through two physical center ports. Different paired blocks may have different orders and profiles. Its declared physical order uses pairs of identically valued copies, with an optional independent middle block.

The proof tracks the missing connector differences and fills them exactly. It reaches a domain outside the stated N135/N141 center-degree pattern, but does not cover arbitrary unpaired block sequences. Its known source operations and unresolved historical priority are retained. [N145][n145]

This is useful evidence that more than one construction architecture exists in MDL. It is not evidence that their domains automatically combine into all lobsters.

### 2.4 N107 supplies inputs rather than assuming them

N107 is especially relevant to the supply problem. For integers a≥2 and r≥4, it constructs actual compatible rooted labelings for positive profiles of length r and total ar when every value other than a occurs an even number of times. Its path/permutation and integer-allocation construction produces the labels directly from the restricted profile. Two such inputs with the same a and r have compatible signatures and feed the retained two-arm joining construction.

This is a genuine solution of an input-supply obligation on its stated domain. It does not assume a full solution of the final lobster and extract components afterward. Paired multiplicities and common joining parameters remain restrictions. [N107 input theorem and actual labels][n107]

N141 also develops the N135 model into an eight-state assignment criterion that can reconstruct branch assignments when it accepts. It treats arbitrary positive quotas within its fixed degree-parity model, but does not guarantee acceptance of every profile or cover every lobster. Its small internal state must not be confused with a universally sufficient state for the unrestricted labeling problem. [N141 criterion][n141]

### 2.5 N68 shows how a failed model can lead to a successful new construction

N65 excludes the entire family with arm profiles {a,a,a,a} and {a+2,a,a−1,a−1}, a≥3, from its fixed N61 labeling model. N68 supplies fresh labels for every member of that same family, using an initial patch and repeated interval tiles.

Both statements can be true: the old model cannot label those trees, while another construction can. This is a useful precedent for changing the representation or state assumptions when a general argument fails, rather than interpreting the failure as nongracefulness. N69/N70 develop the patch-and-tile approach further, but arbitrary requested profiles remain outside the established conclusion. Historical novelty is not established. [N68 recorded proof and review][n68]

## 3. R226 and R232 solve meaningful allocation problems

### 3.1 R226: finish leaves at two attachment points

Suppose a tree core has already received distinct labels and distinct edge differences. There are two actual vertices where new leaves must attach, along with the unused label set and unused difference set.

R226 determines exactly when those leaves can be added while keeping the core fixed. Its proof uses the geometry of absolute differences to classify forced choices, reflected label pairs, and a possible midpoint. It then extracts a completion.

After the availability and component-balance tests, the possible first-host totals have the form

\[
A_0+2j+\epsilon,\qquad 0\le j\le c,\quad 0\le\epsilon\le\eta,
\]

where the variables describe forced assignments, free pairs and a possible singleton. The result has real mathematical content beyond “a completion exists if the constraints have a solution”: it resolves the structure of those solutions and how to construct them. [R226 manuscript][r226]; [adopted disposition][r226-final]

Its missing input is the successful core and resource supply. An arbitrary target lobster has not been shown to admit a core labeling whose remaining resources pass the criterion.

### 3.2 R232: coordinate several such jobs

R232 removes one real burden from R226’s batch assembly. Instead of requiring a successful host split for every batch in advance, it coordinates allocations to satisfy the total demand at each physical host.

It assumes disjoint partitions of both unused labels and unused differences, passing local two-host tests, and a forest condition on the graph of singleton resources. Its exact criterion then checks parity, capacity and subset inequalities for pair resources. The pair-resource graph itself may have cycles and parallel edges.

It reconstructs actual labels on the actual requested leaves. This is a reusable conditional completion theorem. It still does not manufacture suitable core labels and both resource partitions for arbitrary targets, or show that its completed result automatically supplies a fresh instance for another iteration. [R232 manuscript and review][r232]; [final disposition][r232-final]

**Plain-English significance:** the project can coordinate some complicated finishing jobs. The unresolved task is to arrange an arbitrary tree so that these proven finishing rules apply.

## 4. R241 and R246 supply blocks with usable connections

R241 records a numbered block together with two actual attachment vertices, their label offsets, and a path witnessing that the block is a lobster. Two blocks can be combined when the outgoing offset of one matches the incoming offset of the next.

The formula returns the same kind of data for the joined block. That is the important closure property: the output can serve as an input to another join.

R241 also includes independently constructible, unduplicated modules. Their displayed chain requires an adjacent relationship between branch quantities, so this is a real family construction with restrictions, not an arbitrary-target solution. [R241][r241]

R246 improves the supplied choices by using a designated physical direct leaf as the entrance and permitting two exit offsets. For module parameters d,h,q≥1, the entrance offset can be any integer from 1 to d and the exit offset can be h or q. A chain is compatible within this supplied menu exactly when

\[
\min(h_i,q_i)\le d_{i+1}.
\]

The inequality is necessary and sufficient for compatibility **within that menu**, not necessary for all possible labelings of the same tree. It changes the physical entrance relative to an earlier center-entrance construction; it does not remove a condition while keeping that earlier interface unchanged. [R246 argument][r246]; [final disposition][r246-final]

This is one of the clearest examples of an existing partial construction: topology determines a family of manufactured states, and an explicit numerical test permits repeated joining.

## 5. Bounded Search already connects one construction to another

### 5.1 L007 is a genuine formula

For q≥1 leaves per positive branch, r≥1 such branches, and z≥0 direct leaves, set s=q+1 and N=sr+z+1. At root label zero, L007 assigns

\[
f(b_i)=si,\qquad f(\ell_{ij})=s(r-i)+j.
\]

It assigns the terminal next-spine vertex sr+1 and the remaining direct leaves sr+2,…,N.

Multiples and nonmultiples of s partition the labels and edge differences. This proves the whole family, not just tested q and r values. However, it consumes the full budget for the cluster and one next edge; it leaves no further suffix. L008 is the one-branch special case, so these should not be counted as independent advances. [L007/L008][bs-lemmas]; [L007 review][l007-review]

### 5.2 L010 and H010 supply an actual suffix interface

These are especially relevant because the first stage deliberately leaves

\[
R=Q=\{1,\ldots,K\},\qquad a=K+1,
\]

where R is the unused vertex labels, Q the unused differences, and a the current spine label. The already proved caterpillar construction accepts exactly this state and finishes any prescribed K-edge caterpillar continuation.

A caterpillar here has only direct leaves relative to the chosen continuing spine. It does not have further off-spine centers with their own leaves in that supplied representation.

L010 allows arbitrary mixed positive branch sizes in the first section, subject to an explicit label-budget bound. H010 packs the leaf intervals more tightly, reducing the required number of direct leaves in some cases, but imposes a bound on total branch leaf count.

The source example uses a one-edge suffix and first-section branch sizes (1,2). L010’s displayed recipe needs eight direct leaves; H010 needs two. That is a concrete improvement in a parameterized construction, not merely another successful search.

Those direct leaves must already be part of the input tree. Adding them to make the inequality hold changes the mathematical target. L009 is H010’s all-one-branch-size special case. L010 and H010 remain complementary because L010 does not impose H010’s bound on the total leaf count. [L010][bs-lemmas]; [H010 frozen proof][h010]; [H010 proof review][h010-review]

**The important unfinished bridge:** a returned state that can process another genuinely branched section, repeatedly, under an independently justified starting supply.

## 6. The general equation is already present

N240 and the Bounded specification express the problem using a bookkeeping algebra with one resource for every vertex label and every edge difference.

Each term corresponds to a possible assignment. Reusing a label or difference makes the term vanish. The surviving complete terms are exactly the graceful labelings of the named vertices. The final expression is

\[
F_T=N(T)\,\Omega_m,
\qquad
\Omega_m=\prod_{a=0}^{m}x_a\prod_{d=1}^{m}y_d.
\]

The equation is valid for arbitrary finite lobster profiles. Its coefficients count the answers. The universal theorem would require

\[
N(T)>0\quad\text{for every finite lobster }T.
\]

Exact counting and guaranteed positivity are different statements. A compactly written recurrence can still carry a very large set of used-label and used-difference states. No efficient fixed-size state compression or universal positivity proof is established.

The exact-spine intake explicitly reconciles this representation with N240 and credits it as retained mathematics. It also reconciles the cited N(T) and G(T) conventions as counts of labelings on named vertices without symmetry division. It does not count the imported equation as another existence breakthrough. [N240][n240]; [mathematical specification, §§2–3][bs-math]; [exact-spine baseline][spine-plan]

**What this means for the original question:** a universal language for the answers exists. A rule guaranteed to produce an answer for every allowed structure remains missing.

## 7. The failures identify requirements for a broader rule

### 7.1 Separate success is not simultaneous success

Take a four-vertex path. Pin its middle two vertices to 0 and 3. The two outer leaves must receive 1 and 2.

| Left outer leaf | Right outer leaf | Two outer differences |
|---:|---:|---|
| 1 | 2 | 1 and 1 |
| 2 | 1 | 2 and 2 |

Either leaf can be attached successfully by itself. Together, the two assignments duplicate a difference. Yet the same unpinned path is graceful in path order 0,3,1,2, with differences 3,2,1.

This disproves the inference from separate feasibility to compatible completion. It also explains why a failed partial numbering is not a nongraceful tree. Both repositories retain this diagnostic. [Bounded specification, §8][bs-math]; [N240][n240]

### 7.2 Matching the remaining label set and difference set is not enough

C007 has a legal partial branch 0–2–1, leaving R=Q={3,4}. A further one-leaf branch would use labels 3 and 4, producing internal difference 1, which is already used.

So a general state needs more information than equal resource sets or cardinalities. [Counterexamples][bs-counterexamples]

### 7.3 Supported differences can still demand incompatible incidences

C008 shows that the largest required difference can demand an edge incident to a vertex with no remaining neighbor in the specified topology.

C009 strengthens the lesson: every remaining difference can have an available endpoint pair, yet several large differences collectively demand too many neighbors at one label. The actual graph’s remaining degrees make the joint assignment impossible.

A state supplier must respect physical attachment points and joint degree capacity, not just count available numbers. These are adopted fixed-prefix refutations, not nongraceful lobsters. The file titled PROVISIONAL_PREFIX_124 preserves its original submission status; the later counterexample index and separate review adopt C009 at the exact stated scope. [Counterexample index][bs-counterexamples]; [C009 argument][c009]; [C009 review][c009-review]

### 7.4 An alpha-only route has a genuine coverage limit

An alpha labeling imposes an additional low-versus-high separation across every edge. R241/R243/R246 preserve this stronger form.

The seven-vertex subdivided claw is an actual lobster that has a graceful labeling but no alpha labeling. A graceful example assigns hub 0, centers 2,4,6, and corresponding terminal leaves 5,3,1, giving differences 2,4,6,3,1,5. R243 provides a self-contained parity argument ruling out alpha labelings.

Therefore an alpha-preserving construction alone cannot cover all lobsters. It would need a further transformation that leaves the alpha class, or a more general interface. R244 supplies a conditional contraction and a finite non-alpha target example; R248 does not require alpha. Neither supplies arbitrary target reconstruction. [R243 diagnostic][r243]; [R244 adopted correction][r244-final]; [R248][r248]

### 7.5 Adding connectors changes the target

R243 can bridge certain incompatible offsets by inserting a double-star connector. It replaces the original inter-block connection with a five-edge path and additional structure. It correctly proves the expanded family graceful.

It does not prove the original target graceful unless the added structure can be removed or contracted with a valid reconstruction theorem. This is an essential distinction for any modular “master rule.” [R243][r243]

### 7.6 Counting all solutions is stronger than preserving one

N246’s corrected independent count gives 24 named graceful labelings for a six-vertex path and 16 for the corresponding spider with leg lengths 2,2,1. This refutes H229-C’s proposed nondecreasing count under the split.

Both counts are positive. The weaker implication “a graceful merged tree implies a graceful split tree” is not refuted by this example and remains an unproved possible route. The retained structural merger reduction is therefore not erased by the failed stronger count inequality.

Earlier spider counts were erroneous and were not adopted; the corrected value is 16. [Count correction and domain check][count-correction]; [N246 disposition][r246-final]

## 8. Why the existing pieces cannot yet be assembled mechanically

Their input and output requirements differ.

| Mechanism | Required input | Supplied output | Missing cross-mechanism bridge |
|---|---|---|---|
| R226/R232 | Independently labeled partial core; coordinated unused labels and differences | Complete labeling of a prescribed leaf extension, under exact tests | A general rule that manufactures passing cores and palettes |
| R241/R246 | Completely labeled alpha modules with actual ports | Larger labeled alpha module with returned ports | A decomposition of every target into supported modules with matching ports |
| L010/H010 | First-section topology satisfying its bounds | A precise interval state and complete caterpillar continuation | A repeatable transition for an arbitrary later branched section |
| R243 | Suitable alpha modules plus added connector graphs | Graceful expanded target | Reconstruction of the original target after connector removal |
| R248 | Complete graceful source with reflected hosts and invariant component palettes | Another complete graceful tree and reusable toggle groups | A noncircular source choice and proof of reachability of every prescribed target |
| N240 | Arbitrary lobster profile | Exact representation/count of all graceful assignments | A positivity theorem or independently supported existence implication |

These are genuine mathematical assets. Their existence does not establish that one theorem’s output satisfies another theorem’s hypotheses.

For a universal construction, it is enough to prove that every target has some justified successful choice of spine, order, state or source. Demanding that every possible choice work would impose a stronger and unnecessary claim. An algorithm may relabel earlier vertices if its proof permits that; append-only preservation of old labels is not inherently part of the problem.

## 9. What the finite searches contribute

P004 reports 80 new unrestricted profile witnesses. Across P001–P004, 160 profile identities in its specified 747-candidate four-section domain have witnesses, leaving 587 unvisited. These are profile identities, not a count of nonisomorphic trees.

Its separate compatibility study covers 680 legal ordered fixed-prefix states. Every component request is separately feasible; only 160 states admit simultaneous allocation. Of the 520 joint failures, 512 satisfy the additional root-supply threshold and refute the proposed implication. The elementary C008 proof explains one failure independently of search.

The mathematical value is the rejected implication and the resulting design requirement, not a percentage of the universal problem solved. [P004 report][p004]

P005 is not a completed new scientific pass. Its prepared genuinely branched-suffix study remains unexecuted; its single completed remediation search pilot is the zero-edge singleton. Operational fixes, gate checks and that trivial pilot must not be credited as a theorem about general lobsters. [Bounded state][bs-state]; [P005 checkpoint][p005]

Some summary wording about E009 review remains historical. Its later review accepts a specified set of local-interface certificates with explicit limits. The infinite H010 claim rests on the frozen proof and proof review, not on silently treating all computational provenance as resolved. [E009 review][e009-review]; [H010 review][h010-review]

## 10. Recommended scientific direction

### Main recommendation

Use the established recurrence as the common specification and aim the next bounded mathematical task at an **independently supplied, reusable state for a clearly stated parameterized family**, feeding an already proved consumer.

The existing exact-spine plan already identifies the right unresolved implication: independent joint input supply plus usable continuation. This audit supports that diagnosis. It does not establish that this route is uniquely best or guaranteed to solve the problem. [Exact-spine milestones][spine-plan]

A meaningful next result should answer all of these:

1. **Which original trees are covered?** State the topology and all parameter ranges. Do not change the target by adding convenient leaves or connectors without accounting for reconstruction.
2. **How are the starting labels obtained?** Give a formula, recurrence or independent construction from the input structure. Extracting a prefix from a full solver-produced graceful labeling does not prove an independent supplier.
3. **What resources remain?** Track unused vertex labels and unused differences jointly, together with the actual attachment vertices and relevant remaining incidence constraints.
4. **Which existing theorem accepts those resources?** Verify every hypothesis of the selected R226/R232, port-composition, or interval consumer.
5. **What is returned?** Show that the output permits another required step, a specified final suffix, or a well-founded reduction.
6. **What remains outside the proof?** Preserve restricted scope; do not infer arbitrary coverage from large parameters or many successful tests.

For Bounded Search, a scientifically informative direction is to move from a branched first section followed by a caterpillar to a supplier/transition for genuinely successive branched sections. Finite tests should try to falsify the exact proposed invariant and feed counterexamples back into the proof design.

For MDL, R226/R232 are useful consumers when the target question can independently supply both resource inventories. R241/R246 give explicit module-state menus and a concrete model of repeatable composition. R248 is useful for source-to-target transformation questions, but should not be used as though it supplies the source.

These are recommendations, not a launched successor mission or changes to either repository’s execution holds.

### Keep an alternative existence route available

A proof that suitable reductions preserve the existence of at least one graceful labeling could establish the universal theorem without supplying one simple numbering formula. The failed H229-C count inequality does not rule out the weaker positivity direction.

No numerical “percent solved” is justified. The record demonstrates real reusable mathematics and clearly identified missing implications; it does not measure distance to a universal theorem.

## Technical appendix A — exact recurrence and count conventions

Fix the final edge count m. In the commutative algebra with x_a²=y_d²=0, put

\[
W_b=\sum_{c\ne b}x_cy_{|b-c|},\qquad
B_q(a)=\sum_{b\ne a}x_by_{|a-b|}W_b^q,
\]

\[
L_i(a)=x_a\prod_jB_{q_{ij}}(a),\qquad
F_0(a)=L_0(a),
\]

\[
F_i(b)=L_i(b)\sum_{a\ne b}y_{|a-b|}F_{i-1}(a).
\]

Then

\[
\sum_aF_k(a)=N(T)\prod_{a=0}^{m}x_a\prod_{d=1}^{m}y_d.
\]

Each label index ranges over 0,…,m. A zero q represents a direct leaf. Powers account for assignments to distinct named terminal vertices; dividing by factorials would change the convention. The coefficient is a count of named graceful bijections, without automorphism or complementation quotient. Exactness follows because a surviving complete assignment consumes all m+1 vertex labels and m differences exactly once. The identity alone does not establish N(T)>0. [Specification][bs-math]; [retained crosswalk][spine-plan]

## Technical appendix B — selected explicit restricted interfaces

### N135 binary-loop interface

For its fixed ordered quotas t_i, set e_i=1 when t_i is even and 0 otherwise, excluding the designated final quota from this parity data. The recurrence

\[
z_j=e_j\oplus z_{j-1}\oplus z_{j-2}\oplus z_{j-3}
\]

determines binary loop decisions. It requires terminal closure and the integer capacities

\[
t_i\ge c_i+1,\qquad
c_i=z_i+z_{i-1}+z_{i-2}+z_{i-3}.
\]

These are exact conditions for the stated binary-loop transfer model and order, not for all graceful labelings. Its unconditional family satisfies these tests by the degree and quota restrictions described above. [N135][n135]

### L010 interface

For K≥1, r≥1, positive q_i and z≥0, set

\[
N=K+1+\sum_i(q_i+1)+z,\qquad
t_1=K+2,\quad b_i=2t_i+q_i-1,\quad t_{i+1}=b_i+1.
\]

If N≥b_r, use center b_i and leaf interval [t_i,t_i+q_i−1], fill the unused high labels with the tree’s z direct leaves, and use next-spine label K+1. Each branch consumes identical label/difference sets because reflection about b_i permutes its leaf interval. The remaining interval interface supports the prescribed K-edge caterpillar. [Hypothesis H009][bs-hypotheses]; [L010 proof][bs-lemmas]

### H010 interface

Let Q_leaf=Σq_i and impose

\[
Q_{\rm leaf}\le K+2,\qquad
z\ge\max(0,K+2+Q_{\rm leaf}-q_r-r).
\]

Use

\[
t_i=K+2+\sum_{j<i}q_j,\qquad b_i=2t_i+q_i-1.
\]

The leaf intervals now pack consecutively; the total-size condition separates them from every center. The z bound ensures the last center fits in the final alphabet. The same residual caterpillar interface follows. These bounds are sufficient, not asserted necessary or minimal. [H010 proof][h010]; [review][h010-review]

### R248 transformation

Given a fully graceful source with connected core C and off-core components S_j, choose an involution ρ(x)=c−x. A selected union must have an invariant label palette and actual reflected attachment hosts in C. Reflect selected component labels and move their attachments to the reflected hosts.

Every selected internal edge and attachment keeps its absolute difference; palette invariance preserves the vertex bijection. Available component groups can be toggled repeatedly, and distinct groups commute. With C equal to a witnessing spine, lobster membership is preserved. This is closure within the supplied source’s group structure, not arbitrary-target reachability. [R248][r248]

## Technical appendix C — interpretation safeguards

- A parameterized theorem can cover infinitely many trees while retaining a severe structural restriction.
- A construction’s failure can refute that construction without refuting the tree’s gracefulness.
- A successful labeling of each component does not prove compatible labelings exist for their join.
- A formula may encode the original existence question exactly without solving it.
- A finite witness proves its actual tree graceful; a timeout or restricted zero is not a nongraceful-tree proof.
- A proof-review pass and a computational-provenance pass are different claims.
- Known-source reconstruction is still useful project infrastructure and mathematical understanding, but does not establish historical novelty.
- “UGD0” in the retained records does not mean that a lemma has no value. It means no universal-gap reduction was established at that closeout.
- A universal construction may choose a favorable decomposition and relabel earlier vertices; requiring every choice or fixed prior labels is a separate stronger problem.
- A future theorem can bypass this proposed assembly route; no particular recurrence or invariant is mandatory.

## Primary source index

All links are fixed to the audited commits. Sections and later adopted dispositions should be read together when an earlier proof header preserves an “unreviewed” status.

[mdl-state]: https://github.com/drkmtr1/Math-Discovery-Lab/blob/858a8c1fcfda87ba40bb1adee498a6131504a803/PROJECT_STATE.md
[spine-plan]: https://github.com/drkmtr1/Math-Discovery-Lab/blob/858a8c1fcfda87ba40bb1adee498a6131504a803/research/records/exact-spine-program-v1/plan-and-intake.md
[n33]: https://github.com/drkmtr1/Math-Discovery-Lab/blob/858a8c1fcfda87ba40bb1adee498a6131504a803/research/candidates/volume-005.md#explicit-universal-formula-and-proof
[n121]: https://github.com/drkmtr1/Math-Discovery-Lab/blob/858a8c1fcfda87ba40bb1adee498a6131504a803/research/candidates/volume-002.md#n1213--universal-strong-input-complete-construction
[n135]: https://github.com/drkmtr1/Math-Discovery-Lab/blob/858a8c1fcfda87ba40bb1adee498a6131504a803/research/candidates/volume-001.md#n1353--exact-binary-loop-allocation-criterion
[n145]: https://github.com/drkmtr1/Math-Discovery-Lab/blob/858a8c1fcfda87ba40bb1adee498a6131504a803/research/candidates/volume-006.md#h145-a--exact-family-and-evidence-level
[r226]: https://github.com/drkmtr1/Math-Discovery-Lab/blob/858a8c1fcfda87ba40bb1adee498a6131504a803/research/candidates/volume-010.md#n226-researcher
[r226-final]: https://github.com/drkmtr1/Math-Discovery-Lab/blob/858a8c1fcfda87ba40bb1adee498a6131504a803/research/candidates/volume-010.md#n226-closeout
[r232]: https://github.com/drkmtr1/Math-Discovery-Lab/blob/858a8c1fcfda87ba40bb1adee498a6131504a803/research/candidates/volume-010.md#n232-manuscript
[r232-final]: https://github.com/drkmtr1/Math-Discovery-Lab/blob/858a8c1fcfda87ba40bb1adee498a6131504a803/research/candidates/volume-010.md#n232-closeout
[n240]: https://github.com/drkmtr1/Math-Discovery-Lab/blob/858a8c1fcfda87ba40bb1adee498a6131504a803/research/candidates/volume-010.md#n240-first-return
[r241]: https://github.com/drkmtr1/Math-Discovery-Lab/blob/858a8c1fcfda87ba40bb1adee498a6131504a803/research/candidates/volume-010.md#n241-first-return
[r243]: https://github.com/drkmtr1/Math-Discovery-Lab/blob/858a8c1fcfda87ba40bb1adee498a6131504a803/research/candidates/volume-010.md#n243-first-return
[r244-final]: https://github.com/drkmtr1/Math-Discovery-Lab/blob/858a8c1fcfda87ba40bb1adee498a6131504a803/research/candidates/volume-010.md#n244-closeout
[r246]: https://github.com/drkmtr1/Math-Discovery-Lab/blob/858a8c1fcfda87ba40bb1adee498a6131504a803/research/candidates/volume-010.md#n246-first-return
[r246-final]: https://github.com/drkmtr1/Math-Discovery-Lab/blob/858a8c1fcfda87ba40bb1adee498a6131504a803/research/candidates/volume-010.md#n246-closeout
[count-correction]: https://github.com/drkmtr1/Math-Discovery-Lab/blob/858a8c1fcfda87ba40bb1adee498a6131504a803/research/candidates/volume-010.md#n246-count-correction-review
[r248]: https://github.com/drkmtr1/Math-Discovery-Lab/blob/858a8c1fcfda87ba40bb1adee498a6131504a803/research/candidates/volume-010.md#n248-first-return
[bs-state]: https://github.com/drkmtr1/MDL_Bounded_Search/blob/e48b94eec4091b4fe189e325cab2eda464409943/research/STATE.md
[bs-math]: https://github.com/drkmtr1/MDL_Bounded_Search/blob/e48b94eec4091b4fe189e325cab2eda464409943/MATHEMATICS.md
[bs-lemmas]: https://github.com/drkmtr1/MDL_Bounded_Search/blob/e48b94eec4091b4fe189e325cab2eda464409943/research/LEMMAS.md
[bs-hypotheses]: https://github.com/drkmtr1/MDL_Bounded_Search/blob/e48b94eec4091b4fe189e325cab2eda464409943/research/HYPOTHESES.md
[bs-counterexamples]: https://github.com/drkmtr1/MDL_Bounded_Search/blob/e48b94eec4091b4fe189e325cab2eda464409943/research/COUNTEREXAMPLES.md
[l007-review]: https://github.com/drkmtr1/MDL_Bounded_Search/blob/e48b94eec4091b4fe189e325cab2eda464409943/research/verification/pilot_inputs/L007-review.json
[h010]: https://github.com/drkmtr1/MDL_Bounded_Search/blob/e48b94eec4091b4fe189e325cab2eda464409943/research/verification/pilot_inputs/H010-proof.txt
[h010-review]: https://github.com/drkmtr1/MDL_Bounded_Search/blob/e48b94eec4091b4fe189e325cab2eda464409943/research/verification/pilot_inputs/H010-review.json
[e009-review]: https://github.com/drkmtr1/MDL_Bounded_Search/blob/e48b94eec4091b4fe189e325cab2eda464409943/research/verification/pilot_inputs/E009-review.json
[c009]: https://github.com/drkmtr1/MDL_Bounded_Search/blob/e48b94eec4091b4fe189e325cab2eda464409943/research/pass_p005/PROVISIONAL_PREFIX_124.md
[c009-review]: https://github.com/drkmtr1/MDL_Bounded_Search/blob/e48b94eec4091b4fe189e325cab2eda464409943/research/verification/reviews/6b35b35b0883df657390e2e2eab3fa4807854d9aea3a52d9e4466a184fc7cd14.json
[p004]: https://github.com/drkmtr1/MDL_Bounded_Search/blob/e48b94eec4091b4fe189e325cab2eda464409943/research/pass_p004/COMPLETION_REPORT.md
[p005]: https://github.com/drkmtr1/MDL_Bounded_Search/blob/e48b94eec4091b4fe189e325cab2eda464409943/research/pass_p005/CHECKPOINT.md

[n107]: https://github.com/drkmtr1/Math-Discovery-Lab/blob/858a8c1fcfda87ba40bb1adee498a6131504a803/research/candidates/volume-002.md#n1074--uniform-allocation-and-full-paired-positive-input-theorem
[n141]: https://github.com/drkmtr1/Math-Discovery-Lab/blob/858a8c1fcfda87ba40bb1adee498a6131504a803/research/candidates/volume-001.md#n1412--complete-criterion-proof-separate-review-and-director-disposition
[n68]: https://github.com/drkmtr1/Math-Discovery-Lab/blob/858a8c1fcfda87ba40bb1adee498a6131504a803/research/candidates/volume-004.md#mdl-next-068--a-complete-labeling-of-the-g_a-model-obstruction-family-october-16-2026

