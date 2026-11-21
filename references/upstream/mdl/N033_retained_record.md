# MDL N33: retained record

> ARCHIVED SOURCE EVIDENCE. Historical proposals, reviews, restrictions, and instructions below are quotations from the pinned source. They do not govern the new project. This excerpt is not a new review, formal verification, or a novelty claim. Later adoption/correction passages included here control the retained historical disposition.

Original: [research/candidates/volume-005.md](https://github.com/drkmtr1/Math-Discovery-Lab/blob/858a8c1fcfda87ba40bb1adee498a6131504a803/research/candidates/volume-005.md)  
Commit: `858a8c1fcfda87ba40bb1adee498a6131504a803`  
Verified source Git blob: `43084076ad525f4279a939dbf0cb95ac7536fa67`  
Curated scope: Complete selected historical session: statement, construction/argument, review and bounded disposition; original limits retained.

## Source lines 3717–3908

[Pinned source range](https://github.com/drkmtr1/Math-Discovery-Lab/blob/858a8c1fcfda87ba40bb1adee498a6131504a803/research/candidates/volume-005.md#L3717-L3908)

## MDL-NEXT-033 — rooted K certificate and explicit alpha-labelings, October 14, 2026

**Seed PASS; universal formula PASS at written-verification level.** The
Product Owner supplied the certificate and formula as an external ChatGPT
candidate in attachment `7921f977-e6aa-483d-a218-b060ad2d4e8d`. They were
reconstructed independently rather than accepted on provenance or agreement.
The proof below establishes an alpha-labeling of the exact T_h for every
integer h>=8, with threshold h+2 and f(v(2h))=0. N32's missing seed is supplied;
this is a universal restricted-family construction, not merely finite evidence.
Novelty and current literature coverage remain unverified. Formal verification
and qualified independent human review were not performed.

<!-- MDL migration anchor; historical heading ID -->
<a id="literal-graph-certificate-and-complete-finite-check"></a>
### Literal graph, certificate and complete finite check

K=G_6 has vertices v1,...,v12 and ui,ai,bi at i=4,11, with edges
vj-v(j+1) for j=1,...,11 and vi-ui, ui-ai, ui-bi at each site. The two
attachments are Ys, not three direct caterpillar pendants. Adding them to
the 12-vertex path preserves connectedness and acyclicity: order 18, size 17.

The supplied certificate, preserved without correction, is

    f(v1,...,v12)=(12,3,10,6,11,5,13,2,14,4,17,0),
    f(u4,a4,b4)=(9,7,8), f(u11,a11,b11)=(1,16,15).

Complete inverse inventory, in label order, is

    label:   0    1   2  3   4  5  6  7  8  9   10 11 12 13 14 15  16  17
    vertex: v12 u11 v8 v2 v10 v6 v4 a4 b4 u4  v3 v5 v1 v7 v9 b11 a11 v11

Every vertex and every integer 0..17 occurs once. The full edge inventory is:

| Edge | Endpoint labels | Absolute difference |
|---|---|---:|
| v1-v2 | 12,3 | 9 |
| v2-v3 | 3,10 | 7 |
| v3-v4 | 10,6 | 4 |
| v4-v5 | 6,11 | 5 |
| v5-v6 | 11,5 | 6 |
| v6-v7 | 5,13 | 8 |
| v7-v8 | 13,2 | 11 |
| v8-v9 | 2,14 | 12 |
| v9-v10 | 14,4 | 10 |
| v10-v11 | 4,17 | 13 |
| v11-v12 | 17,0 | 17 |
| v4-u4 | 6,9 | 3 |
| u4-a4 | 9,7 | 2 |
| u4-b4 | 9,8 | 1 |
| v11-u11 | 17,1 | 16 |
| u11-a11 | 1,16 | 15 |
| u11-b11 | 1,15 | 14 |

These are exactly 1..17, without repetition; f(v12)=0. In particular the
N32 stopping alternative is resolved by this supplied input: label 1 is on
u11, not v10. No search was used in N33 to select or replace the supplied seed.

The alpha classes are

    Low = {v2,v4,v6,v8,v10,v12,a4,b4,u11}, labels 0..8;
    High = {v1,v3,v5,v7,v9,v11,u4,a11,b11}, labels 9..17.

Consecutive spine vertices alternate between these classes. At site 4 the
edges are Low-High and High-Low twice; at site 11 they are High-Low and
Low-High twice. Thus EVERY edge crosses threshold 8. Equal class sizes alone
were not used as evidence for alpha-labelability.

<!-- MDL migration anchor; historical heading ID -->
<a id="explicit-universal-formula-and-proof"></a>
### Explicit universal formula and proof

**Statement.** For every integer h>=8 put q=h-6. Extend only K's terminal
spine to v(2h), keeping the Ys at positions 4 and 11. Define

    F_h(z)=f(z)+q                       for every old vertex z of K;
    F_h(v(12+2j-1))=17+q+j             for j=1,...,q;
    F_h(v(12+2j))=q-j                  for j=1,...,q.

Then F_h is an alpha-labeling of T_h, with threshold q+8=h+2 and endpoint
F_h(v(2h))=0.

**Graph and counts.** The added vertices are exactly v13,...,v(12+2q),
and 12+2q=2h. Only consecutive terminal spine edges are added. The graph is
therefore the specified T_h, with 18+2q=2h+6 vertices and 17+2q=2h+5 edges.

**Vertex bijection.** Old labels fill [q,q+17] once (18 labels). New even
spine vertices fill [0,q-1] once (q labels). New odd spine vertices fill
[q+18,2q+17] once (q labels). These three adjacent, disjoint intervals fill
[0,2q+17]=[0,2h+5]. Thus the label range and injectivity are exact.

**Edge differences.** Translation leaves all 17 old differences unchanged.
For pair j, the preceding even vertex v(12+2j-2) has label q-j+1; for j=1
this is the old vertex v12, whose label is q. The new odd vertex has label
17+q+j and the new even vertex has label q-j. Both subtractions are positive:

    (17+q+j)-(q-j+1)=16+2j,
    (17+q+j)-(q-j)=17+2j.

For j=1,...,q these disjoint consecutive pairs fill [18,17+2q]. Together
with the old [1,17] they give [1,2h+5] exactly once, on all 17+2q edges.

**Endpoint.** At j=q, v(12+2q)=v(2h) receives q-q=0.

**Alpha property.** Old low and high labels become [q,q+8] and [q+9,q+17].
New even labels lie in [0,q-1], and new odd labels in [q+18,2q+17]. Hence
the full bipartition is

    Low_h = {v(2k):1<=k<=h} union {a4,b4,u11}, labels [0,q+8];
    High_h = {v(2k-1):1<=k<=h} union {u4,a11,b11}, labels [q+9,2q+17].

Every old edge still crosses the threshold q+8; each added edge joins an
even low vertex to an odd high vertex. This directly verifies alpha, with
threshold q+8=h+2. Each class has h+3 vertices, consistently with the ranges.

**Boundary h=8.** Here q=2, order 22, size 21, and threshold 10:

    F_8(v1,...,v16)=(14,5,12,8,13,7,15,4,16,6,19,2,20,1,21,0),
    F_8(u4,a4,b4)=(11,9,10), F_8(u11,a11,b11)=(3,18,17).

Old labels are 2..19; new labels are 20,1,21,0. The four added differences
are |2-20|=18, |20-1|=19, |1-21|=20, |21-0|=21. Old differences remain
1..17. Low/high ranges are 0..10 and 11..21, and v16=0. This is a different
T8 labeling from N30's preserved C8/T8 certificate, not a replacement for it.

**Compatibility with N32.** Increasing q by one increases every existing
label by one, including both types of previously added vertex. The next
pair receives 2q+19 and 0. Since the previous edge count is m=17+2q, these
are m+2 and 0: exactly N32's forward step. Equivalently, a pair created at
step j with labels 17+2j,0 receives q-j subsequent translations, giving
the stated formula. N32's inverse still applies for h>=7 and stops at G_6;
no larger-seed search or modified inverse is needed. The same formulas cover
auxiliary G_6 (q=0, no new pairs) and G_7 (q=1); the target domain remains h>=8.

<!-- MDL migration anchor; historical heading ID -->
<a id="independent-review-interpretation-and-stopping"></a>
### Independent review, interpretation and stopping

The Agent Activation Gate classified this as supplied-certificate and formula
verification. One fresh Researcher (`next033_researcher`) and one genuinely
separate Reviewer (`next033_reviewer`) were invoked. Explorer was omitted
because no hypothesis generation or new mechanism was authorized. The Reviewer
received the literal graph, labels and formula before the expected arithmetic
or Researcher proof, and returned the full independently reconstructed
inventory, differences, partition, general argument and h=8 boundary.
The Director independently checked and reconciled the same calculations.
The Reviewer then audited the complete Researcher proof, four-file record diff
and owner's authorization: **seed PASS; universal formula PASS; alpha PASS**,
with no unresolved mathematical objection. The Director applied two editorial
clarifications: the absence of search refers only to N33 (the external
derivation history is unknown), and unchanged source means executable source,
not documentation. No supplied label, formula or proof needed correction;
zero of the permitted one consolidated mathematical corrections were consumed.

This supplies the exact seed left open by N32 and establishes the restricted
universal alpha-labeling statement above at reviewed written-proof level.
It does not use C_h balance, N31's parked interface, matching/endpoint
relocation, or an inferred zero at a peripheral vertex. N30's historical
certificates and all scoped failures remain unchanged. No conclusion about
balanced C_h existence or the full lobster conjecture follows. C2 remains
impact-first, C3,C2,C1 historical; U_t stays inactive, N22 BLOCKED, TOOLS-015
NO-GO, and all execution interlocks and unrelated holds remain intact.

Novelty/current literature coverage are unverified: the external certificate
is not a primary publication and the mission permits no new literature read.
Formal verification and qualified independent human review were not performed.
The finite check plus the valid quantified extension establishes more than
finite evidence; AI agreement alone is not the reason for the universal claim.

**Next owner decision — AUTHORIZATION REQUIRED:** consider one bounded
literature-coverage assessment of this exact T_h alpha-labeling result before
any novelty or publication claim. Proposed scope: reuse the existing ledger;
at most three targeted discovery queries and two new primary-document
inspections, one separate Reviewer, no construction/generalization/experiments.
Required capabilities: local records and adequate primary-text retrieval;
optional Consensus, no required Sources plugin. Deliver exact theorem/hypothesis
comparisons and residual uncertainty; stop at direct coverage, a defensible
limited assessment, missing essential text or the retrieval ceiling. Its
significance is establishing what this restricted result adds; feasibility is
a narrow source comparison, without guaranteed novelty clearance. No such
phase is authorized or started by N33.

Local PowerShell/filesystem/Git and native delegation were used. GitHub CLI
metadata and the existing guard serve administrative private backup only.
GitHub, Consensus and Wolfram tools were exposed but unnecessary/uninvoked;
their authentication was not probed through plugins. No required capability
was missing. External retrieval, mathematical execution, formalization and
new experiments: zero. Executable source, configuration and interlock changes:
zero.

**WORKFLOW EFFECTIVENESS: NO DEFECT OBSERVED** — exact independent inventories
and the quantified proof close the seed obligation while keeping novelty,
formal/human review and subsequent authorization separate.

---

