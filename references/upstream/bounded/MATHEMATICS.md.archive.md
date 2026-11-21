# Mathematical specification and proof obligations

> ARCHIVED SOURCE EVIDENCE. Historical proposals, reviews, restrictions, and instructions below are quotations from the pinned source. They do not govern the new project. This excerpt is not a new review, formal verification, or a novelty claim. Later adoption/correction passages included here control the retained historical disposition.

Original: [MATHEMATICS.md](https://github.com/drkmtr1/MDL_Bounded_Search/blob/e48b94eec4091b4fe189e325cab2eda464409943/MATHEMATICS.md)  
Commit: `e48b94eec4091b4fe189e325cab2eda464409943`  
Verified source Git blob: `a4a85b158de7820ee113af42b82cd1a49fd08a9c`  
Curated scope: Complete file at the pinned commit. Historical review/provenance limits remain part of the source record.

## Source lines 1–247

[Pinned source range](https://github.com/drkmtr1/MDL_Bounded_Search/blob/e48b94eec4091b4fe189e325cab2eda464409943/MATHEMATICS.md#L1-L247)

# Mathematical specification and proof obligations

This companion separates exact identities and elementary proofs from finite
computational evidence. It makes no novelty claim. The supplied roadmap is
preserved as project context; statements in that earlier document about past
repository work or previous test runs are not newly verified by this package.

## 1. Trees, profiles, and counts

A graceful labeling of a tree with `m` edges is a bijection
\(f:V(T)\to\{0,\ldots,m\}\) whose edge differences are exactly
\(\{1,\ldots,m\}\). Vertices are distinguishable: the count \(N(T)\)
does not divide by automorphisms, reflection, or label complementation.

A lobster profile describes a supporting spine \(s_0,\ldots,s_k\).
At \(s_i\), branch \(j\) has one center and \(q_{ij}\geq0\) leaf
children. A zero means a direct leaf. Thus

\[
m=k+\sum_{i,j}(1+q_{ij}).
\]

For example, `[[1,1,1]]` is a subdivided three-arm claw with six edges.
`[[],[],[],[]]` is a four-vertex path. The singleton `[[]]` has zero edges
and one labeling. Every lobster admits such a profile, but one tree may admit
several profiles. Sorting branches preserves the represented tree; trailing
empty spine sections must be retained. The final value of `m` is fixed before
any partial assignment.

## 2. Exact recurrence

Work in the commutative ring

\[
\mathcal R_m=\mathbb Z[x_0,\ldots,x_m,y_1,\ldots,y_m]/(x_a^2,y_d^2).
\]

The indices in the ideal range over all permitted labels and positive
differences. Repeating either resource kills the corresponding monomial.
Define

\[
C_b=\sum_{c\ne b}x_cy_{|b-c|},\qquad
B_q(a)=\sum_{b\ne a}x_by_{|a-b|}C_b^q,
\]

\[
L_i(a)=x_a\prod_jB_{q_{ij}}(a),\qquad F_0(a)=L_0(a),
\]

\[
F_i(b)=L_i(b)\sum_{a\ne b}y_{|a-b|}F_{i-1}(a).
\]

Every summation label belongs to \(\{0,\ldots,m\}\). Then

\[
\sum_aF_k(a)=N(T)\Omega_m,\qquad
\Omega_m=\prod_{a=0}^mx_a\prod_{d=1}^my_d.
\]

**Proof.** Expanding chooses one label for each original vertex and records
each original edge difference. Repetitions vanish. A surviving complete term
uses `m+1` distinct labels from a set of size `m+1` and `m` distinct positive
differences from a set of size `m`; therefore it is graceful and its monomial
is \(\Omega_m\). Conversely, each graceful assignment contributes once.
Powers and products count assignments to the actual specified vertices;
their multiplicities are required, not an overcount. All coefficients produced
are nonnegative. This proves exactness, not positivity for every lobster.

## 3. Why the implemented frontier evaluation is equivalent

The program expands one vertex at a time in section order: current spine
vertex, each branch center and its leaves, then the next spine vertex.
It retains the used-label mask `U`, used-difference mask `D`, and labels of
assigned vertices that still have an unassigned neighbor. During a branch,
this includes its center and the current spine vertex. At a section boundary,
only the active spine label is needed. A label is forgotten only after all
incident edges have been processed.

Two histories with identical retained labels, `U`, and `D` have exactly the
same legal future extensions. Their counts can therefore be added. This is
an alternative evaluation order of the same products and sums above. No
labeling is excluded by requiring a particular zero vertex, difference-`m`
edge, or alpha-labeling condition. One representative history is stored per
merged state so a full witness can be reconstructed.

Independent permutation enumeration checks complete assignments directly.
The separate DFS checks the same requirements without state merging. Agreement
on finite instances is useful implementation evidence; it is not the proof of
the universal conjecture.

## 4. Exact one-parent leaf supply

Let `a` be an already used parent label, `R` the unused vertex labels, and `Q`
the unused positive differences. Set

\[
J(a;R,Q)=\{d\in Q:a-d\in R\text{ or }a+d\in R\},
\qquad
\kappa_d=\mathbf1_{a-d\in R}+\mathbf1_{a+d\in R}.
\]

For `q` specified new leaves, the number of legal assignments is

\[
\Lambda_q(a;R,Q)=q![z^q]\prod_{d\in Q}(1+\kappa_dz).
\]

**Proof.** Choose `q` distinct available differences; each chosen difference
has \(\kappa_d\) possible leaf labels. Candidate label sets for different
differences are disjoint, because a fixed label determines one absolute
difference from `a`. Finally assign those `q` labels to the specified leaves
in `q!` ways. Consequently a legal attachment exists exactly when
\(|J(a;R,Q)|\geq q\). For `q=0`, the empty assignment counts once.

This statement concerns one parent with fixed resources. Separate successful
checks at multiple parents do not imply joint feasibility.

## 5. A reservation-aware branch and next-spine criterion

Attach a center `b` with `q` specified leaves to parent `a`, and also attach
one next spine vertex `c` to `a`. Define

\[
H_q(a;R,Q)=
\sum_{\substack{b,c\in R,\ b\ne c\\
d_b=|a-b|\in Q,\ d_c=|a-c|\in Q\\d_b\ne d_c}}
\Lambda_q\bigl(b;R\setminus\{b,c\},Q\setminus\{d_b,d_c\}\bigr).
\]

**Proposition.** This is the exact number of simultaneous assignments to
that branch and that next spine vertex. Such an extension exists if and only
if \(H_q(a;R,Q)>0\).

**Proof.** Every valid assignment has a unique ordered pair `(b,c)` satisfying
the summation conditions. After reserving those two labels and their two
distinct parent-edge differences, its remaining choices are exactly the
leaf assignments counted by \(\Lambda_q\). Conversely, each counted leaf
assignment combines with its reserved pair without a resource collision.
These cases are disjoint and exhaustive.

The reservation prevents the leaves from consuming the selected next vertex
or its edge difference. It guarantees **one** next edge. It does not show
that the residual resources at `c` permit arbitrary later spine sections.
Evaluating this exact finite criterion is not yet a structural invariant with
proved universal initial supply and closure.

## 6. Caterpillar interval baseline

For a supplied profile containing only `q=0` branches, maintain

\[
R=[\ell,r]\cap\mathbb Z,\quad Q=\{1,\ldots,N\},\quad
N=r-\ell+1,\quad a=\ell-1\text{ or }a=r+1.
\]

Start the first spine vertex at zero, with `R=Q={1,...,m}`. Give a direct leaf
the endpoint farthest from `a`. Its difference is `N`; deleting this endpoint
preserves the invariant at the same parent. Give the next spine vertex the
same far endpoint; now the new active label lies immediately outside the
opposite end of the shortened interval. Thus each operation consumes one
vertex label and the largest remaining difference. Processing every section
terminates after exactly `m` operations with a graceful labeling.

This is a transparent proof of the stated construction, recovering the known
caterpillar foundation rather than asserting a new result. See also
[Krop, arXiv:1402.3994](https://arxiv.org/abs/1402.3994) for related established
lobster results and context. A `q>0` supplied profile is not accepted by this
particular routine, even if its underlying tree admits a different caterpillar
spine.

## 7. Depth-two return gap

Take \(a=\ell-1\), \(R=\{\ell,\ldots,r\}\),
\(Q=\{1,\ldots,N\}\), and \(N=r-\ell+1\).
Choose center `b=r` and `q` leaf labels
\(\ell,\ldots,\ell+q-1\), where \(0\le q\le N-1\).
These consume differences \(N,N-1,\ldots,N-q\). On returning to `a`,

\[
R'=\{\ell+q,\ldots,r-1\},\qquad
Q'=\{1,\ldots,N-q-1\}.
\]

Differences from `a` to `R'` run from `q+1` through `N-1`. Intersecting with
`Q'` gives

\[
|J(a;R',Q')|=\max(0,N-2q-1).
\]

Reflection gives the same result from the opposite boundary. For `N=5,q=2`,
center `5` and leaves `1,2` leave labels `3,4` and differences `1,2`; parent
zero cannot continue. This refutes that particular greedy continuation rule,
not gracefulness of the underlying tree.

## 8. Fixed-path obstruction and simultaneous compatibility

Pin the middle edge of a four-vertex path to labels `0,3`. Remaining labels
and differences are both `{1,2}`. Either endpoint individually accepts a
leaf. Assigning distinct labels to both leaves nevertheless produces repeated
differences: either `(1,1)` or `(2,2)`. There is no simultaneous completion
of that pinned partial labeling. The unrestricted path is graceful, for
example in path order `0,3,1,2`.

Thus cardinality tests and separate supply tests are insufficient. The program
records the pins and remaining resources of every local obstruction so it
cannot be mistaken for a nongraceful tree.

## 9. What remains to reach the universal goal

A sufficient constructive theorem needs explicitly characterized state
families \(\mathcal C_i\) with:

1. **Initial supply:** for every allowed profile and its final budget, a
   reachable initial state belongs to \(\mathcal C_0\).
2. **Closure:** every reachable state covered by the theorem has a legal
   successor in \(\mathcal C_{i+1}\) for the required next section.
3. **Coverage and completion:** the argument allows arbitrary branch counts,
   leaf counts, and spine length, processes the exact original tree, and ends
   with every label and difference used once.

The families may depend on declared information about the known suffix, but
defining them merely as “states that have a graceful completion” does not
establish these obligations. A bounded leaf-resource audit or profile sweep
does not supply an unbounded composition theorem.

## 10. Interpretation of computational outcomes

An independently checked witness proves that **its finite tree** is graceful.
A fully exhausted exact count proves the computed finite count, conditional
on correctness of the implementation and execution. Finite universal-looking
patterns remain bounded evidence, regardless of the number of successful cases.

Time, node, state, memory, job, or campaign limits mean the search is incomplete;
they never establish zero solutions. A positive partial count is only a lower
bound. A zero count under fixed labels, a restricted construction, or a local
interface cannot refute ordinary gracefulness.

An exhaustive unrestricted zero would be a serious candidate counterexample.
It requires preserved exact topology, independently repeated unrestricted
search or independently checkable negative certification, and explicit review
of the completeness argument. A second implementation agreeing is valuable
cross-validation; it is not automatically a proof-assistant certificate. The
program does not declare the universal problem solved from a finite positive
sweep or a timed-out computation.

---

