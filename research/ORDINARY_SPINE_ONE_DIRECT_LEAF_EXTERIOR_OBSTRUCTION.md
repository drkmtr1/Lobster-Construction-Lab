# D151 — One-direct-leaf obstruction in the D143 exterior class

Task `LCL-ORDINARY-SPINE-ONE-DIRECT-LEAF-EXTERIOR-STUDY-001`. All parameters and labels are exact integers, excluding booleans. An inclusive interval with reversed endpoints is empty.

## 1. Domain and result

Use the [D143](ORDINARY_SPINE_TWO_SECTION_CUT_STATE.md) two-section embedding on an independently supplied named [D134](ORDINARY_SPINE_PIECEWISE_CUT_SPECTRUM_TRANSITION.md) p=1 prefix with actual frontier v. Orient the input so that v has zero. The prefix has n=2c+2 edges, minimum crossing difference d=c+2 at the input cut, and exact old crossing weights [d,n]. Append two named sections at u,w with 2K actual fresh vertices and n≥2K. Require the D143 old membership-preserving two-translation placement and the exact D134 return. In a purported completion D143 puts all positive centers and both spine vertices in the exterior, with exterior widths A≥2, B≥1 and gap length s≥K, where A+B+s=2K. Its reduced exterior is graceful on [0,A+B], with each edge crossing the cut between A and A+1.

Suppose the first section has exactly one positive center a and no direct leaves, and the second has at most one actual direct leaf at w. No further condition is imposed on the positive terminal quotas, the number of second-section centers, the exterior widths, the chosen exterior terminals or which admissible input polarity is supplied.

**Theorem.** There is no D143 completion of this structure. More precisely, any completion under the same first-section premise forces a=A−1, forces actual terminals of a in every reduced upper slot b=2,…,A−1, and requires at least two actual direct leaves of w in the gap. The latter lower bound concerns leaves assigned to the gap, so placing the sole direct leaf in the exterior gives zero available leaves. It excludes the full terminal-enabled class in this topology, including its terminal-free subclass. The claim concerns the D143 embedding and interface.

## 2. The reduced exterior forces a and its upper terminals

The following label notation refers to vertices' reduced labels. In the reduced exterior v=A and w=0 by D143. The only crossing pair with reduced difference one is (A,A+1). The sole exterior incidence of the old v is the actual connector vu. Hence u=A+1, the [D147](ORDINARY_SPINE_EXTERIOR_SUPPLY_REASSESSMENT.md) pin.

A crossing edge of difference two has upper role b=1 with lower endpoint A−1, or b=2 with lower endpoint A if that upper slot exists. The latter would be an edge of v other than vu and is impossible. The former uses u. In the reduced exterior the actual neighbors of u are v,w,a. Its existing edges to v and w have weights 1 and A+1 respectively. Since A≥2, neither supplies 2. Thus the actual edge ua gives the weight two and the label of a is A−1. This includes A=2.

For each t=3,…,A, suppose all upper slots b=2,…,t−2 have already been shown to be actual terminals of a. The required weight t belongs to [1,A+B]. A crossing edge with upper label A+b at difference t would have lower label A+b−t. Consider every possible existing upper slot b.

- At b=1 the vertex is u and its complete list of reduced incidence weights is 1,2,A+1. None equals t.
- At 2≤b≤t−2 the vertex is, by induction, an actual terminal of a. Its sole edge has weight b+1≤t−1.
- At b=t−1 the required lower label is A−1, the label of a.
- At b=t the required lower label is A, the label of v. Its only reduced edge has weight one.
- At b>t the required lower label exceeds A.

In a successful exterior the difference t must occur, so b=t−1 exists. The actual edge between a and that slot must be present. Apart from ua the only possible incidences of a are its named terminal edges. The upper vertex in the slot is therefore an actual terminal of a, supplying difference t. This proves the induction. If a slot is missing because B<t−1, the same elimination leaves difference t absent and rules out that exterior. Distinct slots denote distinct named actual terminals, so insufficient terminal quota at a also prevents such an exterior. For A=2 the forced interval is empty. The single forced edge ua and the following gap argument still apply.

## 3. Forced gap host and collision

Every gap vertex is an actual direct leaf or terminal of an exterior parent by D143. Of the low exterior vertices, the old v cannot host a new leaf, and the only eligible parents are w and a. Indeed, u is upper and has no direct leaves, every center of the second section is upper by its actual attachment to w, and any other low fresh vertex is a terminal of a second-section center. Such a terminal has no child. Thus at lower hosts w=0 and a=A−1 the D143 image rules are respectively

    w: π(i)=i+A−2,
    a: π(i)=i−1.

An upper parent at role b can supply an in-range image only if s+b−i≤s−1, equivalently i≥b+1. The role b=1 at u has no direct quota and the upper roles 2,…,A−1 are terminals, so every eligible upper parent has b≥A and requires i≥A+1. If no eligible upper parent exists, upper assignments are simply unavailable. In particular both sources 0 and A−1 cannot use an upper parent. The gap length satisfies s≥K≥A+B≥A+1, so both source coordinates exist and are distinct.

At source 0 the a translation underflows. Thus it is required to use w and gives image A−2. If the actual crossing test were to reject this sole candidate, completion is already impossible. Otherwise source 0 consumes one actual direct-gap leaf of w. At source A−1 the a translation gives A−2 again, which repeats the image of source 0. It follows that any completion must use a second actual direct-gap leaf at w for source A−1. The argument already rules out all other actual incidences using the raw index range, physical eligibility and injectivity, whether or not those alternatives would also fail the crossing test. Using w for both distinct sources requires two distinct named direct leaves. If w has no gap direct leaf, source 0 alone is impossible. If w has only one, source A−1 cannot be assigned. This proves the theorem. The simultaneous input/output complementation of D143 retains the actual crossing statuses and all these incidences, so both actual polarities are covered.

## 4. Applicability and exact preparation disposition

The proposed ordered study profiles are (2r) at u and (2p,2q,0) at w for 2≤r≤6, p,q≥1, and r+p+q≤12. The first section has 2r+2 fresh vertices and the second has 2(p+q)+4. Thus 2K=2(r+p+q+3), so K ranges from 7 through 15. For each r the number of ordered positive pairs with p+q≤12−r is `binom(12−r,2)`, by summing the positive compositions of each total. The five counts are 45, 36, 28, 21 and 15, hence 145 ordered triples. This is an arithmetic count. The two branch positions keep their prescribed order.

The [retained D148 prefix](../evidence/validation/LCL_ORDINARY_SPINE_MATCHED_EXTERIOR_TWO_CENTER_001/input/prefix.json) has n=54, oriented c=26, d=28 and its actual maximum frontier s:25. Its named initializer and actual labels are frozen. Read-only inspection of its saved vertices, edges and label data confirms the palette [0,54], difference palette [1,54], exact crossings [28,54] and noncrossings [1,27] at c in the orientation. Its actual cut is 29. Since 2K≤30≤54, this single independently initialized D134 state meets the entire size range. The theorem applies to every advertised triple, independent of the use of this particular prefix. Both arms are therefore excluded symbolically throughout the proposed study. These are proofs of nonexistence in the declared interface, separate from numerical arm dispositions.

**Disposition — RESOLVED SYMBOLICALLY BEFORE NUMERICAL EXECUTION.** No new original, candidate naming, configuration for execution, search, transfer evaluation, solver call or arm disposition was generated. A numerical campaign would retest a question the theorem already decides. Under KEEP v11, method selection follows mathematical leverage, with separately authorized hybrid discovery at a genuine unresolved bottleneck. The earlier proposal targeted an open question and the symbolic obstruction has removed that bottleneck. This work provides no information on alternate ordinary embeddings beyond the D143 class.

## 5. Retained original-bound controls

The four requested originals remain in D148's frozen input shard and their eight official arm payloads remain in the raw archive. Their named identities, graph digests and ordered profiles were matched to those records. T is an accepted forced-three symbolic negative. E is an independently exhausted negative in the retained evidence. This proof is compatible with those four records and is independent of their negative outcomes.

| Original | First section | Second section | Historical T / E |
|---|---|---|---|
| target-0056 | (4) | (2,2,0) | NO / NO |
| target-0059 | (4) | (2,4,0) | NO / NO |
| target-0068 | (4) | (4,2,0) | NO / NO |
| target-0071 | (4) | (4,4,0) | NO / NO |

The accepted [D150](ORDINARY_SPINE_TWO_TO_ONE_TERMINAL_SUPPLIER.md) positive controls have three actual direct leaves at w. Its target-0188 boundary is terminal-enabled and terminal-free excluded. Its larger-quota family also has terminal-free constructions. These are different originals with a different physical direct-leaf budget, and meet the lower bound proved here. This boundary leaves the two-direct-leaf case outside the present exclusion. D148's 12 undecided pairs remain undecided in the historical campaign, and no D148 search was resumed or rerun.
