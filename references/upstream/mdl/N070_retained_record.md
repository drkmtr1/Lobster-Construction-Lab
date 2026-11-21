# MDL N70: retained record

> ARCHIVED SOURCE EVIDENCE. Historical proposals, reviews, restrictions, and instructions below are quotations from the pinned source. They do not govern the new project. This excerpt is not a new review, formal verification, or a novelty claim. Later adoption/correction passages included here control the retained historical disposition.

Original: [research/candidates/volume-004.md](https://github.com/drkmtr1/Math-Discovery-Lab/blob/858a8c1fcfda87ba40bb1adee498a6131504a803/research/candidates/volume-004.md)  
Commit: `858a8c1fcfda87ba40bb1adee498a6131504a803`  
Verified source Git blob: `aef2c40b4ba13b18c70cc3a8e664e3f348260126`  
Curated scope: Complete selected historical session: statement, construction/argument, review and bounded disposition; original limits retained.

## Source lines 476–728

[Pinned source range](https://github.com/drkmtr1/Math-Discovery-Lab/blob/858a8c1fcfda87ba40bb1adee498a6131504a803/research/candidates/volume-004.md#L476-L728)

## MDL-NEXT-070 — two-permutation alpha labelings and sharp arm imbalance, October 16, 2026

<!-- MDL migration anchor; historical heading ID -->
<a id="outcome-authority-and-claim-scope"></a>
### Outcome, authority and claim scope

**H70-A: VERIFIED WRITTEN THEOREM. H70-B: VERIFIED WRITTEN THEOREM.**
The external ChatGPT candidates were independently reconstructed symbolically;
the separate Reviewer's final disposition is recorded in the review paragraph
below. The construction works for every integer a>=1,p>=3 and every pair
sigma,tau in S_p. It supplies alpha threshold2p, diameter exactly six, and
inclusive lobster membership. All outputs with a>=2 are proper lobsters;
at a=1 the exact caterpillar criterion is given below. The attainable terminal
totals are exactly pa+Delta and pa-Delta, -(p-1)<=Delta<=p-1, within THIS model.
No arbitrary-profile theorem, original-mathematics claim, formal verification,
qualified human review or general alpha-hold reopening follows.

The owner accepted N69 at its existing written-proof/separate-AI-review level
and authorized this bounded extension. Original N68/N69 proofs, N65's exact
model obstruction, N67's earlier-project coverage, source corrections and all
holds remain intact. The changed obligation is the patch's equal-arm count:
two permutations preserve its actual differences while allowing unequal arm
orders. No unknown compatible input or finite extrapolation is used.

<!-- MDL migration anchor; historical heading ID -->
<a id="n701--full-labeling-and-vertex-inventory"></a>
### N70.1 — full labeling and vertex inventory

Put q=2p and m=q(a+1)+2. The core is r0-z-r1, with p children at each root.
Label z=0, r0=m, r1=a+q; the first root's children are1,...,p, and the second's
are p+1,...,q. A parent number below denotes that child's label.

Attach terminals as follows:

1. Every label in [q+1,a+q-1] has parent q.
2. Terminal a+2p+j has parent j+sigma(j), 1<=j<=p.
3. Terminal a+3p+i has parent p+i-tau(i), 1<=i<=p.
4. For h=0,...,a-2 put S_h=a+2q+1+(q-1)h. Terminal S_h+j-1 has parent
   c_j=2j mod(q-1), represented in1,...,q-1, for j=1,...,q-1.

Empty integer intervals/stages contribute nothing. The patch parents satisfy
2<=j+sigma(j)<=2p and 1<=p+i-tau(i)<=2p-1. Multiplication by2 permutes residues
modulo the odd q-1, so each tile uses every parent1,...,q-1 once. Each terminal
is a distinct new vertex with exactly one specified attachment.

The core labels are {0,...,q,a+q,m}. Since m-(a+q)=(q-1)a+2>0, they are
distinct. The terminal intervals are

    [q+1,a+q-1], [a+q+1,a+2q], [a+2q+1,m-1].

Their sizes are a-1,q,(a-1)(q-1), summing to aq. Adjacent tiles abut, and the
last tile ends at a+2q+(q-1)(a-1)=m-1. At a=1 the first/third intervals are
empty. Thus every vertex label0,...,m appears once; the graph has m+1 vertices
and q+2+aq=m edges. All roots and terminals have labels>q, whereas z and all
children have labels<=q.

<!-- MDL migration anchor; historical heading ID -->
<a id="n702--exact-seven-band-difference-proof-and-alpha-property"></a>
### N70.2 — exact seven-band difference proof and alpha property

The r0-child edges and zr0 give [m-p,m]. The r1-child edges give [a,a+p-1],
and zr1 gives a+2p. The initial run gives [1,a-1]. Each terminal label exceeds
EVERY possible child label, so pendant differences are terminal minus parent,
not unverified signed offsets. In the patch they are exactly

    (a+2p+j)-(j+sigma(j)) = a+2p-sigma(j),
    (a+3p+i)-(p+i-tau(i)) = a+2p+tau(i).

These give [a+p,a+2p-1] and [a+2p+1,a+3p], respectively, with no repetitions.
The signs -sigma(j),+tau(i) refer only to offsets from a+2p.

For a tile, c_j=2j when j<=p-1 and c_j=2j-(2p-1) when p<=j<=2p-1.
The offsets j-1-c_j are [-p,-2] and [-1,p-2], each once. Hence a tile gives
[S_h-p,S_h+p-2], of length q-1. Consecutive tile starts differ by q-1, so their
union is [a+3p+1,m-p-1]. The full spectrum is the disjoint consecutive union

    [1,a-1], [a,a+p-1], [a+p,a+2p-1], {a+2p},
    [a+2p+1,a+3p], [a+3p+1,m-p-1], [m-p,m].

It is exactly [1,m]. At a=1 the tile band is [3p+2,3p+1], correctly empty;
at a=2 there is exactly one tile. This proves gracefulness for all admitted
parameters without a parity condition. Every edge crosses [0,q] | [q+1,m],
so the labeling is alpha with threshold q=2p.

<!-- MDL migration anchor; historical heading ID -->
<a id="n703--child-counts-diameter-and-caterpillar-boundary"></a>
### N70.3 — child counts, diameter and caterpillar boundary

Write

    n_u = #{j:j+sigma(j)=u} + #{i:p+i-tau(i)=u}.

Each child u has a-1+n_u terminals: tiles supply a-1 to each child below q,
and the initial run supplies a-1 at q. Zero-terminal children are retained
vertices. Let C=sum_(u=1..p)n_u. The i=1 second-half parent lies in [1,p],
whereas the j=p first-half parent lies in [p+1,2p]. Thus

    1<=C<=2p-1.                                           (N70.1)

Both arms contain terminals even at a=1. The core plus pendant attachments
is connected and acyclic. Every vertex is within distance three of z, and
opposite-arm terminals are distance six apart; diameter is exactly six and
z is the unique center. Extend r0-z-r1 through a child and terminal in each
arm to a longest path. Every vertex is within distance two of this path,
so this also witnesses lobster membership under the longest-spine definition.

After deleting all leaves, the remaining graph is the central path together
with the occupied children (those having at least one terminal). The roots
survive because each has degree p+1. For a>=2 all p children in each arm are
occupied; the pruned graph has root degrees p+1>=4 and is not a path. Thus
every such output is a proper lobster. At a=1 it is a caterpillar IF AND ONLY
IF each arm has exactly one occupied child; otherwise it is a proper lobster.
For example sigma(j)=p+1-j,tau(i)=i occupies only children p+1 and p, with p
terminals each. This is a caterpillar for every p>=3, refuting an unqualified
universal-properness interpretation, not H70-A's inclusive lobster claim.

<!-- MDL migration anchor; historical heading ID -->
<a id="n704--literal-n69-embedding"></a>
### N70.4 — literal N69 embedding

The N69 modular patch before swaps has sigma(j)=j and tau(i)=p+1-i: parents
are2j in the first half and2i-1 in the second. The inverse position of an
original parent u is I(u)=u/2 for even u and (u+2p+1)/2 for odd u. Endpoints
s,t of an arithmetic triple satisfy s+t=2r and hence have the same parity.
Their inverse positions lie in the same signed half. Swapping their signed
offsets therefore transposes two sigma values or two tau values. Vertex-
disjoint triples give disjoint such swaps, including triples in either arm
and arbitrary admitted spacing. This proves inclusion of N69's literal
core/patch/tile assignments, not merely an isomorphism of profiles. N68's
graph family is inherited through N69; its different literal patch is preserved.
No claim about arbitrary overlapping triples or arbitrary profiles follows.

<!-- MDL migration anchor; historical heading ID -->
<a id="n705--sharp-imbalance-and-explicit-witnesses"></a>
### N70.5 — sharp imbalance and explicit witnesses

The first-arm patch count can also be written

    C = #{j:j+sigma(j)<=p} + #{i:tau(i)>=i}.

The arm terminal totals are L0=p(a-1)+C, L1=p(a-1)+2p-C. With Delta=C-p,
(N70.1) proves L0=pa+Delta,L1=pa-Delta and -(p-1)<=Delta<=p-1.

For 0<=k<=p-1 take tau=id and

    sigma(j)=k+1-j        (j<=k),
             p+k+1-j    (j>k).

This reverses the two disjoint value blocks [1,k] and [k+1,p], so is a
permutation, including the empty first block at k=0. First-half parents
are k+1 for k terminals and p+k+1 for p-k terminals. The former lie left,
the latter right; all p second-half parents equal p. Thus C=p+k, Delta=k.

For 1<=s<=p-1 take sigma(j)=p+1-j and the cyclic permutation

    tau(i)=i+s       (i<=p-s),
           i+s-p    (i>p-s).

Every first-half parent is p+1. Second-half parents are p-s for p-s terminals
and 2p-s for s terminals. These lie left and right respectively, yielding
C=p-s, Delta=-s. Every integer in the exact asserted range is attained.

At Delta=p-1, the only occupied patch parents are p (2p-1 terminals) and
2p (one terminal). The selected maximal-imbalance profiles are therefore

    {a+2p-2,(a-1)^(p-1)} / {a,(a-1)^(p-1)}.               (N70.2)

They have totals pa+p-1,pa-p+1 and are proper for a>=2, caterpillars for a=1.
The negative extreme exchanges the profiles. In fact these profiles are forced
at the extremes: C=2p-1 forces tau(i)>=i everywhere, hence tau=id by equal
permutation sums. It forces sigma(j)<=p-j for j<p; summing gives sigma(p)=p
and equality throughout. C=1 forces sigma(j)>=p+1-j, hence reversal; for
i>1 it forces tau(i)<=i-1, whose sum forces tau(1)=p and equality throughout.
This is extremal rigidity within the two-permutation model only.

At the smallest a=1,p=3, q=6,m=14, the positive-extreme witness is
sigma=(2,1,3),tau=id. Its first-half parents are3,3,6 and second-half
parents3,3,3. Profiles are {5,0,0}/{1,0,0}, on15 vertices with differences
1,...,14, a diameter-six caterpillar. This is a symbolic specialization,
not a finite search. The proof above also handles a=2, p=3 and p=4 without
exception or extrapolation; no parameter range below the admitted domain is claimed.

<!-- MDL migration anchor; historical heading ID -->
<a id="n706--intrinsic-enlargement-published-coverage-and-limits"></a>
### N70.6 — intrinsic enlargement, published coverage and limits

Deleting the unique center gives components of orders 1+p+pa+Delta and
1+p+pa-Delta. Nonzero Delta makes these unequal, whereas EVERY N69 output
has equal center-component orders. No sibling ordering, arm exchange or
alternate N69 parameters can remove this invariant. Thus N70 genuinely
enlarges N69's unlabeled graph family. Delta=0 does not prove N69 membership;
the two signs describe arm orientation, not necessarily different unlabeled
trees. No count of distinct graphs follows from the number of permutations.
N65's every-representation N61 exclusion is retained at its exact G_a scope;
it is not extended to general N70 outputs.

The [N70 source assessment](../sources.md#mdl-next-070--two-permutation-evidence-and-qualified-coverage-october-16-2026)
separates affirmative boundary/subfamily coverage from unresolved full-family
coverage. All caterpillar outputs have classical alpha-existence coverage as
stated in the inspected LCR report; the cited original proof was not inspected.
Mirrored N70 outputs with a>=3,p>=4 satisfy the existing N61 root-zero/Delta+1
mapping at its recorded theorem-statement level, with van Bussel's original
proof still uninspected. That mapping does not establish this alpha formula
or cover unequal center-component orders by identical copies. Superdock's
named centered odd-child interfaces, LCR's degree/matching interfaces and
MP2010's actual operation hypotheses are distinguished from broader unassessed
constructions. PM2008 m=1, MP2010 broader remarks and JS2013 retain their exact
input/decomposition gaps. **NOVELTY UNRESOLVED**: no full published-family mapping,
historical formula priority or global noncoverage was established.

The reusable gain is an explicit two-permutation patch with a complete global
spectrum and sharp linear imbalance. Structural restrictions remain: center
degree2, equal root degrees p+1, a uniform a-1 baseline and patch-constrained
profiles. Impact is a genuine extension beyond equal-arm N69, not all-lobster
progress by implication. Feasibility is established by complete supplied inputs.

<!-- MDL migration anchor; historical heading ID -->
<a id="n707--adversarial-review-resources-and-owner-recommendation"></a>
### N70.7 — adversarial review, resources and owner recommendation

One fresh Explorer challenged the model and source dependencies; one Researcher
reconstructed the entire proof; one genuinely separate Reviewer received exact
claims before completed arguments, then checked the full proof. The Reviewer
issued separate **SCOPED PASS for H70-A and H70-B**, with no unresolved critical
mathematical objection. This is AI review, not formal or qualified human review.
The Reviewer challenged a=1 properness, forced positive terminal totals, signed versus actual
differences, same-parity N69 embeddings, intrinsic isomorphism scope and known
caterpillar coverage. These qualifications are explicit above. No candidate
formula required repair; no mathematical correction/recheck was consumed.

Resource and capability details are in the linked source entry. No mathematical
execution, enumeration, installation, infrastructure change or successor occurred.
The source map materially aided selection by exposing N67's duplicate-coverage
lesson, N65's model scope, N69's corrected root condition and the N61 mirrored
mapping. No quantified token/productivity saving is claimed.

For next-direction comparison, fully characterizing prescribed profiles could
be tractable but retains this patch's structural limitations. Unequal root
degrees remove a different restriction and have greater prospective generality,
with unproved spectral feasibility. **One recommended owner action — AUTHORIZATION
REQUIRED:** authorize a separate coverage-first symbolic feasibility mission for
the exact uniform-arm family {a^r}/{a^(r+1)}, a>=1,r>=3, around r0-z-r1. Ordinary
gracefulness suffices. Compare broad inspected theorems first; if necessary allow
one Explorer with at most two mechanisms, one selected Researcher and a separate
Reviewer, one correction, at most two queries/one new work, zero mathematical
execution. Stop on prior coverage, a complete construction/usable reduction,
scoped failure or a precise unsupported input. No such research has begun;
this proposal neither reopens universal alpha work nor authorizes a successor.

**WORKFLOW EFFECTIVENESS: NO DEFECT OBSERVED** — separate reconstruction and
adversarial checks preserved the a=1 boundary and source corrections while
establishing the complete spectrum and intrinsic enlargement. Mathematical
yield is the explicit theorem and sharp totals, separately from process completion.

---

