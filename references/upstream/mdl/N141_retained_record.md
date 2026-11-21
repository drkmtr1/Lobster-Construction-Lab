# MDL N141: retained record

> ARCHIVED SOURCE EVIDENCE. Historical proposals, reviews, restrictions, and instructions below are quotations from the pinned source. They do not govern the new project. This excerpt is not a new review, formal verification, or a novelty claim. Later adoption/correction passages included here control the retained historical disposition.

Original: [research/candidates/volume-001.md](https://github.com/drkmtr1/Math-Discovery-Lab/blob/858a8c1fcfda87ba40bb1adee498a6131504a803/research/candidates/volume-001.md)  
Commit: `858a8c1fcfda87ba40bb1adee498a6131504a803`  
Verified source Git blob: `11dde2c5a38ba2721d24e62a96497346706439ae`  
Curated scope: Complete selected historical session: statement, construction/argument, review and bounded disposition; original limits retained.

## Source lines 531–837

[Pinned source range](https://github.com/drkmtr1/Math-Discovery-Lab/blob/858a8c1fcfda87ba40bb1adee498a6131504a803/research/candidates/volume-001.md#L531-L837)

## MDL-NEXT-141 — full positive-quota domain of the fixed N135 model, October 23, 2026

<!-- MDL migration anchor; historical heading ID -->
<a id="n1411--prospective-admission-and-retained-evidence-baseline"></a>
### N141.1 — prospective admission and retained-evidence baseline

**Director PROCEED; Mission 2/2 of the current Owner-initiated cycle.**
This is the final mission capacity in the cycle. At admission, exploration had
not yet started.

**Target.** Complete the exact assignment classification for the entire
degree-parity domain of N135.3: every ordered path of \(\ell\ge2\) positive
height-two factors, first root degree odd \(r_1\ge3\), later root degrees
even \(r_i\ge2\), and arbitrary positive terminal quotas in every factor.
Permit branch identities to move only within their own prescribed canonical
factor group. Seek a uniform constructive profile criterion that decides
whether some such assignment satisfies N135 closure and all nonfinal
position-capacity inequalities, reconstructs actual assignments when it
accepts, and excludes every allowed assignment in that fixed model when it
rejects. Retain N135's final-position convention: \(e_R=0\) by definition
even when the actual final quota is even, and the final quota is positive and
unrestricted by a nonfinal capacity inequality. A rejection is not a claim
that the tree is nongraceful or that another transfer history fails.
Merely restating existence over all placements or enumerating permutations is
not a successful criterion; the result must give a uniform profile-level
construction/rejection procedure with a proved finite-state or recurrence
bound polynomial in the explicitly listed factor and branch counts.

**Primary-source/theorem baseline.** N135.3 proves the exact fixed-order
criterion for an already assigned quota word: divisibility by
\(1+X+X^2+X^3\) gives the unique binary starts, and each \(j<R\) separately
requires \(t_j\ge1+c_j\), where \(c_j\) is the integer sum of the four
covering starts. N140.2 supplies a constructive assignment criterion when
the first degree is odd at least five and all first-factor quotas are odd,
while allowing arbitrary positive later quotas. The remaining obligation is
to handle arbitrary first-factor quotas and the N135-minimal first degree
three, including the boundary between the controlled prefix and the final
suffix. The final position must not be assigned a fictitious parity
constraint. Exact retained source limits are in [N141's source record](../sources.md#mdl-next-141--retained-evidence-admission-october-23-2026); no new original publication is needed for this symbolic model-completion question.

**Value, alternatives, and limits.** A complete criterion would identify the
full reach of this particular reusable N135 construction interface and give
actual inputs throughout its degree-parity domain. That is a stronger
endpoint than another quota subclass. The result remains a classification
within one fixed model; it does not establish that every profile is accepted,
that rejected trees are nongraceful, historical novelty, or universal lobster
gracefulness. A renewed historical-coverage audit would not resolve the
remaining first-suffix assignment question. A different construction model
would introduce a separate mechanism and is outside this final cycle mission.

**Methods, roles, resources, and stops.** Preserve an independent Explorer
first pass before selecting any mechanism. Then develop at most one route
after screening at most two. Use one Explorer, one Researcher, and a separate
Reviewer for the consequential proof. The Reviewer must examine the actual
first-group word and inventory, polynomial boundary and zero starts,
quota-specific capacities at every nonfinal position, the unrestricted final
position convention, degree-three and two-factor cases, actual ID
reconstruction, and all-assignment rejection semantics. Mission limits:
three role contexts, two routes screened, one developed, two consolidated
rechecks; zero discovery queries, new publications/acquisitions, new original
page inspections, and mathematical executable runs. Reuse N135/N140 project
proof records and their retained source qualifications. Stop at a complete
reviewed criterion or rigorous fixed-model obstruction, a critical unresolved
objection, no defensible route after two screens, or exhausted allowances.
This is mission 2/2; do not start another mission in this cycle.

Desktop Sources: local repository/retained proofs REQUIRED; external
connectors and mathematical executables NOT NEEDED for this symbolic target.

<!-- MDL migration anchor; historical heading ID -->
<a id="n1412--complete-criterion-proof-separate-review-and-director-disposition"></a>
### N141.2 — complete criterion proof, separate review, and Director disposition

**H141-A: complete written proof; separate-context AI mathematical SCOPED
PASS; accepted by the Director at that evidence level.** The criterion is
necessary and sufficient for an assignment in the fixed N135 canonical-order
binary unit-retention-loop model. It supplies actual branch identities and
starts on acceptance. Rejection excludes only assignments in this model; it
does not imply that the tree is nongraceful or exclude other histories. This
is not formal verification or qualified human review.

Let \(\ell\ge2\). Here \(r_i\) counts factor \(i\)'s children before its
root is joined to the root path: \(r_1\ge3\) is odd and each \(r_i\ge2\),
\(i\ge2\), is even. Each actual child branch has a positive integer terminal
quota and identity. Put \(R=\sum_i r_i\), let \(S\) be the sum of all
terminal quotas, and set \(M=R+S\). Define the canonical later-factor word by
\[
W_\ell=\ell^{r_\ell},\quad
W_i=i\,W_{i+1}\,i^{r_i-1}\ (i=\ell-1,\ldots,2).
\]
The full factor-position word is \(W_2\,1^{r_1}\). For \(\ell=2\), this is
\(2^{r_2}1^{r_1}\). Actual branch identities may be permuted only within
their own factor group.

**Local feasibility.** At each nonfinal position \(j<R\), N135 requires
\[
c_j=z_j+z_{j-1}+z_{j-2}+z_{j-3},\qquad
c_j\equiv {\bf1}(t_j\text{ even})\pmod2,\qquad t_j\ge c_j+1,
\]
where each start \(z_j\in\{0,1\}\) and \(0\le c_j\le4\). Thus the exact
quota classes and allowed integer coverages are
\[
\begin{array}{c|ccccc}
\text{quota}&1&2&3&\text{even }\ge4&\text{odd }\ge5\\
\hline
\text{coverage}&\{0\}&\{1\}&\{0,2\}&\{1,3\}&\{0,2,4\}.
\end{array}
\]
These sets encode parity and strict capacity together. Quotas in one class
are interchangeable for these local tests; original values and IDs are
retained for reconstruction.

**Automaton and factor inventories.** Let \(n_i\) be factor \(i\)'s vector
of five quota-class counts, \(\Omega=\{0,1\}^3\), and \(o=000\). For each
type \(X\), let Boolean \(T_X\) have transition
\[
T_X((a,b,c),(b,c,d))=1
\quad\Longleftrightarrow\quad d\in\{0,1\},\quad a+b+c+d\in C_X,
\]
with all other entries zero. Define Boolean matrices
\[
B(0)=I,\qquad B(n)=\bigvee_{X:n_X>0}T_XB(n-\mathbf e_X),
\]
\[
F_\ell=B(n_\ell),\qquad
F_i=\bigvee_{X:(n_i)_X>0}T_XF_{i+1}B(n_i-\mathbf e_X)
\quad(i=\ell-1,\ldots,2),
\]
and reserve one first-factor occurrence for the actual final position by
\[
G(n_1)=\bigvee_{X:(n_1)_X>0}B(n_1-\mathbf e_X).
\]
The criterion is
\[
\boxed{[F_2G(n_1)](o,o)=1.}
\]
There is no transition for the reserved branch.

Induction on \(|n|\) proves \(B(n)(s,t)=1\) exactly when a word with
inventory \(n\) gives a walk from state \(s\) to state \(t\): its first
type \(X\) is followed by inventory \(n-\mathbf e_X\), and Boolean matrix
products match the intermediate state. The identity matrix covers the empty
word. For \(F_i\), the first singleton of \(W_i=iW_{i+1}i^{r_i-1}\)
removes one occurrence from factor \(i\)'s own inventory; the nested word
uses the inner factors, and the remaining tail uses \(n_i-\mathbf e_X\).
Induction gives exactly all attainable endpoint pairs for each prescribed
factor subword, including degree-two tails and \(\ell=2\). Both endpoints
remain unrestricted. The same inventory argument proves that \(G(n_1)\)
represents all and only words reserving one first-factor type for the final
branch. Its actual quota is positive but is subject to neither a parity test
nor a nonfinal capacity inequality.

**Full nonfinal-word boundary.** For an assigned full quota word, define
\(e_j={\bf1}(t_j\text{ even})\) only for \(j<R\), and set \(e_R=0\) by
N135 convention, irrespective of the actual final quota. Put
\[
E(X)=\sum_{j=1}^{R-1}e_jX^{j-1},\qquad Q(X)=1+X+X^2+X^3
\quad\text{over }\mathbb F_2.
\]
N135 closure is \(Q\mid E\), with unique quotient \(Z=\sum z_jX^{j-1}\).
If \(E=0\), then \(Z=0\); otherwise \(\deg E\le R-2\), so
\(\deg Z\le R-5\) and every start has index at most \(R-4\).
With state \((z_{j-3},z_{j-2},z_{j-1})\) immediately before position \(j\),
the initial state before position \(1\) and the final state after position
\(R-1\) are both \(o\). Intermediate states need not be \(o\). Coefficient
comparison gives the local parity equations, and
N135 capacity gives every permitted automaton transition.

Conversely, a walk from \(o\) to \(o\) over exactly positions
\(1,\ldots,R-1\) has \(z_{R-3}=z_{R-2}=z_{R-1}=0\), hence starts only
through \(R-4\). Its transition parity equations give the coefficients of
\(E=QZ\); \(QZ\) has degree at most \(R-2\), so there are no omitted later
coefficients. Its transitions also impose \(t_j\ge c_j+1\) at every
nonfinal position. This proves both directions, including \(E=0\) and the
minimum \(R=5\). It imposes no condition on the actual final quota, and no
loop reaches the final child.

If the boxed entry is true, Boolean multiplication supplies a common state
between \(F_2\) and \(G\), yielding a compatible zero-to-zero walk through the
entire nonfinal canonical word. Backtracking stores the first type and
intermediate state for each true \(B\) entry, singleton and endpoint
witnesses for each \(F_i\), the reserved type for \(G\), and the shared
state. Choose an actual first-factor ID of the reserved type for the final
position. Assign remaining IDs in input order to occurrences within each
factor and type. This uses every original ID exactly once, keeps its original
quota, and never crosses factor groups. The exact class tests preserve each
actual capacity. Conversely, every successful permitted placement has one
actual first-factor final branch; its other type occurrences witness \(G\),
and its later factors witness \(F_2\). The boundary lemma supplies the
accepting walk. Therefore rejection excludes every permitted placement in
this model.

**Graceful realization.** The preceding tests supply N135.3's exact degree,
closure, capacity and final-child hypotheses. Invoke its retained aggregate
seed and chronological transfer proof; this is not a new audit of every
earlier transfer or publication. With \(q=(R-1)/2\), the seed has root 0,
child labels \([1,q]\cup[M-q,M]\), canonical
\(w_{2s+1}=M-s,w_{2s}=s\), and terminal interval
\([q+1,M-q-1]\) initially at child \(M\). These partition labels
\([0,M]\), and root plus terminal differences partition \([1,M]\). Each
start specifies the retained four-child loop with unit retention at its four
departures; the ordinary departure at \(j<R\) retains \(t_j-c_j\), a
positive odd integer. The last child is untouched and retains its full
positive quota. The inherited chronological ledger supplies legal overlapping
transfers and nonempty moving intervals. Its sign convention is
\(\delta=H-(a+b)\) for incoming interval \([a,b]\) and target reflection
sum \(H\); retaining \(d\) labels uses \(L=(d+\delta)/2\) below and
\(U=(d-\delta)/2\) above, so the moved interval has endpoint sum
\(a+b+\delta=H\).

For the root path, let \(k=\lfloor(\ell-1)/2\rfloor\), shift the aggregate
by \(k\), and use the retained root labels
\(\rho_{2j+1}=k-j\), \(\rho_{2j+2}=M+k+1+j\) where defined. N135's
parity-neutral whole-branch ledger, inherited from N121.4, preserves factor
incidences and attachment differences; it does not assume N121's separate
all-odd input-existence theorem. Spine edge \(i\) has difference \(M+i\).
The result has labels \([0,M+\ell-1]\), differences \([1,M+\ell-1]\),
order \(M+\ell\), diameter \(\ell+3\), and the prescribed proper-lobster
topology. No alpha-labeling follows.

**Polynomial bound.** Include all factors in
\(D_i=\prod_X((n_i)_X+1)\), \(D=\sum_iD_i\). One shared \(B\)-table per
factor has \(D_i\) fixed-size eight-state matrices, at most five type choices
per entry; \(F_i\) and \(G\) use a bounded number of fixed-size operations.
Thus decision uses \(O(D+R)\) Boolean/table operations and no inventory
product across factors, permutation enumeration, or per-ID table rebuilding.
Since \(r_i\ge2\), \(D_i\le(r_i+1)^5\le(3r_i/2)^5\), hence
\(D=O(R^5)\), polynomial in the explicit branch list. For binary input
length \(L_{in}\), the stated random-access bookkeeping bound is
\(O(L_{in}+(D+R)\log(R+1))\); backtracking visits \(O(R)\) nodes. With
\(b=\lceil\log_2(M+\ell+1)\rceil\), the compact branch/start/interval/root
witness uses \(O(L_{in}+Rb)\) bits. Printing every terminal label may cost
\(O((M+\ell)b)\), exponential in binary quota length. No practical speed
claim is measured.

**Recovery of N140.** On N140’s domain, all first-factor quotas are odd and
\(r_1\ge5\). Put \(K=R-r_1\). Then \(E\) is supported on positions
\(1,\ldots,K\). If \(E\ne0\), divisibility gives \(\deg Z\le K-4\), hence
starts end by \(K-3\); if \(E=0\), all starts vanish. Therefore the state
after the later prefix is \(000\), and every first-suffix coverage is zero.
When \(K<4\), divisibility forces \(E=0\). Thus H141-A acceptance implies
N140’s \(F_2(o,o)=1\). Conversely, an accepted N140 prefix extends through
the odd first-factor suffix using zero transitions and reserving any final
branch. The acceptance sets agree exactly on N140’s domain.

**Development cases.** These are written development checks, not executable
evidence. For \(\ell=2,r_2=2,r_1=3\) and all quotas 2, the nonfinal parity
word is 1111, \(E=Q\), \(z_1=1\), and the state sequence is
\(000\to001\to010\to100\to000\); every coverage is \(c_j=1<2\). The later
prefix ends at 010, so the complete nonfinal word, not the later prefix,
must close. Reserving an even final quota is necessary: later quotas (1,1),
first quotas (2,1,1), and final quota 2 give all-odd nonfinal positions and
zero starts. With later (2,2), first (1,1,1), the nonfinal parity word
1100 has \(E=1+X\), which is not divisible by \(Q\), so every placement
in this model rejects. All-odd quotas, including 1, accept with zero starts.
The Reviewer additionally checked single-even-branch placement, empty and
repeated type inventories, degree-two factors, and a closure-passing profile
that fails a quota-1 capacity inequality.

**Finite certificate.** Researcher checked the Director-supplied manual
certificate for \(\ell=2,r_1=3,r_2=2\), all quotas 2. Root 0 has children
14, 2, 13 with terminal pairs (4,6), (5,9), (7,8). Root 16 has children
15, 1 with pairs (3,11), (12,10); join roots 0 and 16. Roots, children and
terminals are respectively \(\{0,16\}\), \(\{1,2,13,14,15\}\), and
\(\{3,\ldots,12\}\), partitioning \([0,16]\). Root-child differences
are \(\{1,2,13,14,15\}\), terminal differences are \(\{3,\ldots,12\}\),
and the root edge contributes 16. Thus all differences 1 through 16 occur
once. The separate Reviewer independently checked this as a finite
certificate; it did not reconstruct the historical transfer derivation.

**Separate review and disposition.** The Reviewer returned mathematical
**SCOPED PASS**, with no required correction or critical objection. Review
covered the full-word closure boundary, final reservation, exact local
capacities, inventory induction, all-placement rejection, actual construction
interface, complexity and recovery of N140. Adversarial cases included
\(R=5\), an even final quota, a sole even quota in each factor, and closure
without capacity. The reviewer requested only transcription clarity; this
record states \(c_j=1<2\) at every nonfinal position in the all-2 example.
The Director accepts H141-A at complete-written-proof/separate-context
AI-review level. The transfer/source dependency chain is inherited, not
re-audited. Historical full-family input coverage, formula priority, novelty,
practical benefit, formal verification, qualified human review, and universal
lobster gracefulness remain unresolved.

**Final record recheck.** The second and final consolidated recheck reviewed
the integrated records. It preserved the mathematical SCOPED PASS but required
canonical-word and endpoint transcription corrections, restoration of the
reviewed N140 recovery argument, and current-summary/accounting updates. These
exact replacements require mechanical verification; no additional
mathematical recheck is authorized.

**Resources and workflow.** N141 used all three role contexts, screened one
of two routes, developed one route, and used two of two consolidated
rechecks. In the N140 cycle: six of six role contexts, two of four route
screens, two of two developed routes, and three of four consolidated
rechecks were used: one for N140 and two for N141. N141 has zero rechecks
remaining. New original-page inspections, queries, publications, acquisitions,
mathematical executions, formal builds, and edits by delegates: zero.
N134 count-one remains INCONCLUSIVE, N130 remains PARKED, and N81 remains
PARKED/BLOCKED BEFORE EXECUTION/UNTESTED with zero runs. All other holds and
source qualifications persist.

**WORKFLOW EFFECTIVENESS: IMPROVEMENT OPPORTUNITY** — mathematical review
found no defect in H141-A, while integrated documentation introduced a
duplicated suffix and omitted the N140 recovery argument. The Reviewer
specified exact repairs; the prior bounded-read truncation remains recorded,
and focused reads recovered the required evidence.

---

