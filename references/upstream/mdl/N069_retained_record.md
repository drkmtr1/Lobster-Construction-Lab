# MDL N69: retained record

> ARCHIVED SOURCE EVIDENCE. Historical proposals, reviews, restrictions, and instructions below are quotations from the pinned source. They do not govern the new project. This excerpt is not a new review, formal verification, or a novelty claim. Later adoption/correction passages included here control the retained historical disposition.

Original: [research/candidates/volume-004.md](https://github.com/drkmtr1/Math-Discovery-Lab/blob/858a8c1fcfda87ba40bb1adee498a6131504a803/research/candidates/volume-004.md)  
Commit: `858a8c1fcfda87ba40bb1adee498a6131504a803`  
Verified source Git blob: `aef2c40b4ba13b18c70cc3a8e664e3f348260126`  
Curated scope: Complete selected historical session: statement, construction/argument, review and bounded disposition; original limits retained.

## Source lines 732–999

[Pinned source range](https://github.com/drkmtr1/Math-Discovery-Lab/blob/858a8c1fcfda87ba40bb1adee498a6131504a803/research/candidates/volume-004.md#L732-L999)

## MDL-NEXT-069 — modular patch and tile alpha labelings, October 16, 2026

<!-- MDL migration anchor; historical heading ID -->
<a id="outcome-authority-and-provenance"></a>
### Outcome, authority and provenance

**H69-A: VERIFIED WRITTEN THEOREM. H69-B: VERIFIED WRITTEN THEOREM.**
Both external ChatGPT hypotheses have complete symbolic reconstructions and
separate-context AI SCOPED PASS. For all integers a>=1,p>=3, the tree with
profiles `{a^p}/{a+2,a-1,a-1,a^(p-3)}` has an alpha labeling with threshold
2p. More generally the same conclusion holds for

    {a^p}/{(a+2)^k,(a-1)^(2k),a^(p-3k)},
    1<=k<=floor(p/3).                              (N69.1)

Counts zero mean existing child vertices without terminals, not deleted
children. These one-arm families are proper diameter-six lobsters, including
a=1. A direct bilateral corollary and its caterpillar exception are below.
Neither formal verification, qualified human review nor originality is claimed.

The owner's attachment, repeating the authorized N69 prompt after an interrupted
acknowledgment, supplied the exact modular formulas. No N69 tool/research work
preceded that interruption. One Explorer challenged the formulas, one Researcher
reconstructed them, and one separate Reviewer scrutinized statements before
receiving the complete argument. H69-B was released only after the Researcher's
H69-A reconstruction PASS. One consolidated source correction/recheck was used;
the mathematical construction needed no repair. No extra mechanism was developed.

Map-led admission retrieved N68's exact patch/tile proof, N65.7's p=4 intrinsic
exclusion, N60.5/.6 and N61.4's fixed-label criteria, N64.9/.11's SOME-companion
limitation and N67's packed-family overlap. This selects the actual full-spectrum
audit rather than inferring generality from another transfer sequence. The new
construction changes the N61 labels; only p=4,a>=3 inherits N65.7's intrinsic
exclusion. General alpha-development, C+ and all other holds remain active.

<!-- MDL migration anchor; historical heading ID -->
<a id="1-exact-core-terminal-labels-and-modular-patch"></a>
### 1. Exact core, terminal labels and modular patch

Put q=2p and m=q(a+1)+2. The core is r0-z-r1, with p children per root.
Assign z=0,r0=m,r1=a+q, and child labels1,...,p at r0 and p+1,...,q at r1.
Parent numbers below refer to these child labels. The q+3 core labels are
distinct: a+q>q and m-(a+q)=(q-1)a+2>0.

Attach labels q+1,...,a+q-1 to child q. For j=1,...,q create a terminal of
label a+q+j. Its initial parent b_j and signed difference offset d_j are

    b_j = 2j                  (1<=j<=p),
          2j-(2p+1)          (p+1<=j<=2p);
    d_j = j-b_j = -j         (1<=j<=p),
                    2p+1-j  (p+1<=j<=2p).          (N69.2)

This is exactly multiplication by2 modulo2p+1 on nonzero representatives.
The parents list all even then all odd labels in [1,q], once each. The
offset multiset is [-p,-1] union [1,p], once each. The inverse position is

    I(u)=u/2                 if u is even,
         (u+2p+1)/2          if u is odd.            (N69.3)

For the primary claim, set s=p+1,t=p+3. They lie in the second arm since
p>=3, have the same parity, and I(t)-I(s)=1. Exchange the two offsets at
x=I(s),y=I(t) (using y avoids confusing an index with center z). With
b'_j=j-d'_j, the two changed parents are

    b'_x=x-(y-t)=t-1=p+2,
    b'_y=y-(x-s)=s+1=p+2.

The original occurrence of p+2 is untouched. Thus patch parent multiplicities
are zero at p+1,p+3, three at p+2, and one elsewhere. Every parent is valid.
The signed offsets are NOT absolute differences: the ACTUAL patch differences
are a+q+d'_j>0. Their unchanged multiset is

    [a+p,a+2p-1] union [a+2p+1,a+3p].              (N69.4)

This translation resolves the prompt's potentially ambiguous signed-spectrum
wording without changing its construction.

<!-- MDL migration anchor; historical heading ID -->
<a id="2-tile-identity-and-complete-vertex-inventory"></a>
### 2. Tile identity and complete vertex inventory

For each h=0,...,a-2 put S_h=a+2q+1+(q-1)h. Attach terminal S_h+j-1 to
parent c_j for j=1,...,q-1, where

    c_j = 2j                 (1<=j<=p-1),
          2j-(2p-1)          (p<=j<=2p-1).          (N69.5)

This equals the submitted modulo(q-1) rule including its zero representative:
c_(2p-1)=2p-1. The parents are a permutation of [1,q-1]. The offsets
j-1-c_j are -j-1 in the first range and 2p-2-j in the second. These supply
disjoint intervals [-p,-2] and [-1,p-2], respectively. Each tile therefore
has exactly the differences [S_h-p,S_h+p-2], one each. Its length is q-1;
successive starts differ by q-1, giving adjacent disjoint difference intervals.

The terminal label sets are

    [q+1,a+q-1], [a+q+1,a+2q],
    [a+2q+1,m-1] (tiled when a>=2).

The last tile ends at a+2q+(q-1)(a-1)=m-1. Sizes are a-1,q,(a-1)(q-1),
total aq. With the core they use [0,m] exactly once, and there are
aq+q+2=m edges. At a=1 the first and third sets are empty, and the patch
itself ends at m-1. No tile with a negative h-range is created.

Every child1,...,q-1 gets a-1 terminals from the tiles; child q instead
gets a-1 from the initial run. Thus the contribution OUTSIDE the patch is
uniformly a-1 at every child, even when q=p+3 at p=3. Adding patch counts
proves the asserted profiles and pa terminals/order1+p+pa in each arm.

<!-- MDL migration anchor; historical heading ID -->
<a id="3-complete-spectrum-alpha-property-and-boundaries"></a>
### 3. Complete spectrum, alpha property and boundaries

Core edges z-r0 and r0-child1,...,p give [m-p,m]. Edges r1-child(p+1),...,q
give [a,a+p-1], and z-r1 gives a+2p. All roots and terminals have labels
greater than q, so every stated difference is a positive subtraction.
The initial run gives [1,a-1]. The tile union for a>=2 is
[a+3p+1,m-p-1]. Combining this with (N69.4) gives

    [1,a-1], [a,a+p-1], [a+p,a+2p-1], {a+2p},
    [a+2p+1,a+3p], [a+3p+1,m-p-1], [m-p,m].       (N69.6)

These bands join consecutively without repetition and cover [1,m]. The only
possibly empty bands are the first and the tile band, both empty exactly at
a=1. Vertex bijection plus this edge inventory proves gracefulness. Every edge
crosses [0,q]/[q+1,m], proving alpha threshold q=2p.

- **a=1:** m=4p+2; profiles `{1^p}/{3,0,0,1^(p-3)}`. Nonempty bands are
  [1,p],[p+1,2p],{2p+1},[2p+2,3p+1],[3p+2,4p+2]. The absent tile interval
  is [3p+2,3p+1]. Zero-terminal children are retained as leaves at their roots.
- **a=2:** exactly one tile, S_0=4p+3, ending at6p+1=m-1. Its differences
  are [3p+3,5p+1], followed by high band[5p+2,6p+2]. Profiles are
  `{2^p}/{4,1,1,2^(p-3)}`.
- **p=3:** final patch parent sequence(2,5,5,1,3,5), tile(2,4,1,3,5).
  Second-arm counts are(a-1,a+2,a-1), including the deficit at child q.
  In particular a=1,p=3 gives15 vertices and differences1,...,14.
- **p=4:** patch(2,4,6,8,1,3,6,6), tile(2,4,6,1,3,5,7). These differ from
  N68's recorded patch/tile lists. The graph family, core labels, alpha
  threshold8 and difference bands specialize to N68, not its literal formula.

These are symbolic substitutions, not executed trials or finite extrapolation.
There is no parity restriction. The stated target requires a>=1 for nonnegative
deficits and p>=3 for three distinct children; a=0 also collides r1 with child q,
and p<3 puts p+3 outside [1,2p]. No larger family domain is asserted.

<!-- MDL migration anchor; historical heading ID -->
<a id="4-disjoint-arithmetic-triples-and-direct-bilateral-corollary"></a>
### 4. Disjoint arithmetic triples and direct bilateral corollary

For H69-B begin with the ORIGINAL patch b, before any primary swap. Choose
pairwise vertex-disjoint triples (s,r,t) in either arm, with s<r<t and
s+t=2r. Write delta=r-s=t-r. Endpoints have the same parity, so (N69.3)
gives I(t)-I(s)=delta. Swapping their original offsets sends their two
terminals to parents

    I(s)-(I(t)-t)=t-delta=r,
    I(t)-(I(s)-s)=s+delta=r.                       (N69.7)

There is no further restriction on midpoint or spacing parity. Bijectivity of
I and disjoint triple vertices give disjoint swapped positions and preserve
each midpoint's original occurrence. Thus each triple changes patch counts by
(-1,+2,-1), leaves all others fixed, and preserves the entire offset multiset.
All actual differences remain (N69.4), so the complete proof (N69.6) still applies.
The uniform baseline a-1 makes final counts a-1,a+2,a-1, all nonnegative.
Every terminal has one assigned parent. Each triple conserves its arm's count.

Take triples (p+3i-2,p+3i-1,p+3i), 1<=i<=k. They exist disjointly exactly
when 3k<=p, proving (N69.1) in its full stated domain. At p=3k no ordinary-a
child remains in that arm; at a=1 it still has k positive three-terminal
children. The triple positions are not independent unlabeled graph choices:
for fixed a,p,k their rooted count multisets specify the same tree.

The same argument directly permits independent numbers k0,k1 in
[0,floor(p/3)] of such triples in the two arms, giving

    {(a+2)^k0,(a-1)^(2k0),a^(p-3k0)} /
    {(a+2)^k1,(a-1)^(2k1),a^(p-3k1)}.             (N69.8)

This is a corollary of the same disjoint swaps, not an additional mechanism.
Rooted arms are isomorphic iff k0=k1, since the three count values are distinct;
for fixed a,p the unlabeled output depends only on the unordered pair{k0,k1}.
No overlapping-triple, arbitrary-profile or legal sequential-transfer theorem
is established. The result concerns simultaneous final incidence assignment.

<!-- MDL migration anchor; historical heading ID -->
<a id="5-graph-identity-topology-and-exact-proper-lobster-qualification"></a>
### 5. Graph identity, topology and exact proper-lobster qualification

The connected acyclic core gains one pendant edge per new terminal, so the
result is a tree. Each arm retains pa>0 terminals, even at a=1. All vertices
are within distance3 of z and opposite-arm terminals have distance6; z is the
unique center. The core path r0-z-r1 is a distance-two witness of lobsterhood.
The intrinsic center and rooted stars determine the unordered arm profiles,
including count-zero child vertices, so the construction covers every tree
with the stated profiles, not only one drawing.

The primary and one-arm k families are proper lobsters: after removing all
leaves, the uniform arm's root still has p+1>=4 neighbors, so the remaining
graph is not a path. For (N69.8), a>=2 leaves every child positive. At a=1,
arm i has p-2ki positive children, and its leaf-pruned root degree is
1+p-2ki. The pruned graph is a path exactly when both p-2ki=1. Under
p>=3,3ki<=p this occurs only at p=3,k0=k1=1. That one bilateral case is a
diameter-six caterpillar, hence an inclusive lobster. Every other bilateral
case is proper. This boundary qualification does not weaken either submitted
one-arm theorem and must accompany the optional corollary.

Different a,p may coincide in total order, but p is recovered from each root's
degree p+1 and a from the terminal total pa; no order-only isomorphism argument
is used. No exponential output count is claimed. N65.7's all-representation
N61 obstruction remains confined to p=4,a>=3; no larger-p exclusion is inferred.

<!-- MDL migration anchor; historical heading ID -->
<a id="6-sources-adverse-review-evidence-and-mathematical-yield"></a>
### 6. Sources, adverse review evidence and mathematical yield

The proof is self-contained. Multiplication by2 modulo an odd number is an
elementary permutation; preserving a difference multiset by swapping positions
is elementary bookkeeping, not an asserted new general operation. The contribution
is the actual compatible labeling, patch and tiles giving every edge once across
variable p,a and independently chosen disjoint triples. Known component-transfer
lemmas do not automatically provide this distinct-source-to-midpoint application.

The N69 source entry gives exact retained passages. Superdock Theorem4 and
Corollary5, as printed in arXiv:1402.6570v2,p5, both require odd child counts
at the central root and therefore do not directly apply (our center has two).
LCR2017 Theorem3 requires maximum degree3, contradicted by roots of degree
p+1>=4; its matching results require a perfect matching, contradicted by odd
order2p(a+1)+3. These are named-interface exclusions, not whole-paper or
all-representation literature exclusions. MP2010 general constructions/remarks,
PM2008 m=1 inputs/partition and broader source mappings remain unresolved.
No full published-family coverage, global noncoverage or originality clearance
was established. Exact modular formula/application priority is unresolved.

**Adverse evidence and one correction:** Director and Reviewer preliminarily
inserted a root exception into Superdock Corollary5 and suggested a=1,odd-p
coverage. Researcher challenged this against the actual page and N53 ledger.
Reinspection of the same primary version, including extracted text, confirms
NO such exception. Both preliminary claims were withdrawn; the final mapping
retains center-degree nonapplication and N53's separate proof-sentence qualification.
No source theorem was repaired and no N69 algebra changed. This consumed the
single consolidated correction/recheck (1/1). It is not a counterexample to
Superdock or evidence against the submitted labeling.

Final separate Reviewer dispositions: **SCOPED PASS for A; SCOPED PASS for B**,
with the bilateral caterpillar exception, distinct N68 formulas, signed-offset
qualification and corrected source comparison explicitly checked. No unresolved
critical objection. Review is independent AI evidence, not formal or human review.

Impact: this replaces N68's fixed eight-child patch with a variable-width
construction and establishes the two proposed full parameter families. It is
more structural freedom, but not arbitrary diameter-six lobster gracefulness.
Feasibility is demonstrated by closed formulas without unknown input labels.
The map prevented unsupported extension of N65 or confusing N67-style prior
project coverage with published priority. One Explorer/Researcher/Reviewer,
one correction, 1/2 discovery queries, 0/1 new works, zero mathematical execution.

**WORKFLOW EFFECTIVENESS: IMPROVEMENT OPPORTUNITY** — a preliminary source
reading inserted an absent exception, affecting only a proposed coverage claim.
Researcher challenge and direct primary-text reconciliation removed it before
promotion; final review confirmed the correction. The mathematical yield is
the two complete general constructions, not role completion or agreement.
No systemic cause, formal assurance or measured productivity gain is inferred.

**ONE recommended Product Owner action:** accept N69's two written theorems
with their exact scope and unresolved historical coverage, and defer further
disjoint-triple formula refinements pending a proposal that removes a different
substantive dependency. This is a recommendation, not an enacted new hold.
No successor, new source campaign or additional proof development has begun.

---

