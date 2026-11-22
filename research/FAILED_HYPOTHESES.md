# Failed hypotheses and adverse controls

These are failures of specified rules or claims. None is a nongraceful-lobster certificate. The preserved primary excerpts and preceding audit contain the original reasoning and corrected dispositions.

| ID | Failed inference / evidence | Consequence for this project |
|---|---|---|
| F-SEP | Separate leaf/component feasibility need not combine. On P4 with middle labels 0 and 3, the two end jobs can each be done alone but cannot jointly use labels/differences once each. | Keep joint inventories and actual incidences. The unrestricted path has four named graceful labelings. |
| F-EQUAL | Bounded C007: fixed prefix 0–2–1 leaves labels and differences {3,4}, yet the required new one-leaf branch cannot use them consistently. | Equality `R=D` alone is not a continuation theorem. |
| F-SUPPORT | C008 and C009: locally supported large differences can demand unavailable or incompatible physical incidences. C009's prefix (1,2,4) with m=9 forces 9,8,7 through zero beyond the available degree capacity. | Difference-by-difference support is weaker than simultaneous incidence feasibility. |
| F-ALPHA | The seven-vertex subdivided claw is ordinarily graceful but lacks an alpha-labeling under the retained obstruction. | Alpha-only search cannot establish unrestricted nongracefulness or cover every lobster. A direct ordinary witness is kept in checker tests. |
| F-COUNT | Corrected H229-C: named counts `G(P6)=24` and `G(spider(2,2,1))=16` refute the proposed count monotonicity. | A false count inequality does not refute a weaker existence-preservation claim. Both counts are independently reproduced. |
| F-TOPOLOGY | R243's connector can create a graceful expanded tree with additional edges. | Check the original target; successful expansion is not a labeling of the original graph. |
| F-SUPPLY | A complete solver solution can yield a valid prefix without supplying a noncircular construction from parameters. | Keep extraction labeled `solver_derived_exploratory_prefix`; require an independent supplier proof. |
| F-PROJECTION | On P6, omitting either resource mask or the live frontier label merges prefixes with different completion counts. | Preserve the full DP key; explicit pairs and oracle counts are in `SEARCH_REVIEW.md`. |
| F-FIXED-INTERVAL | For q=r=1 and zero padding, the above-side ell=2 interface succeeds at K=1,2 but is impossible for every K>=3. | The elementary prefix bipartition proof is in `B2_INTERVAL_OBSTRUCTION.md`; the balanced supplier uses ell=3 instead. |
| F-UNEQUAL-SEED | B2-UNEQUAL-SEED-001: the eight-vertex prefix `[[1],[2],[]]` with A-side `0..3` / B-side `4..7` bijective domains and pin `h(s:2)=4` has no graceful labeling. Analytic obstruction (difference 1 forces `h(s:1)=3`; `a+2b−x=18` admits only `(a,b,x)∈{(5,7,1),(6,7,2),(7,6,1)}`; every resulting assignment duplicates difference 4 on at least two actual edges) confirmed by independent recomputation and a separate reviewer challenge; bounded DFS (65 nodes) and direct-permutation oracle (5,040/5,040 permutations, 144 domain-admissible) both exhausted with 0 solutions. | The falsified claim is exactly this alpha/physical-port template — not the unrestricted eight-vertex tree, not the unequal B2 family at any K, not a nongracefulness certificate. The conditional all-K high-side shift is retained as a conditional identity only. Full record: `B2_UNEQUAL_SEED.md`. |
| F-INTERFACE-K6 | For `q=1,r=2,z0=z1=0` and every `K>=6`, the exact eight-vertex prefix through `s:2` cannot leave unused labels `[ell,ell+K-1]`, unused differences `1..K`, and physical port `ell-1` or `ell+K`, for any `ell` or side (no alpha assumption, no root pin). Maximum difference `K+7` forces labels `0` and `K+7` into the prefix; the two used-label blocks have span at most 6; all prefix edges must cross for `K>=6`; the connected 4/4 bipartition forces `ell=4`; high-block compression by `K` gives exactly the forbidden p=4 seed (above side directly, below side after complementation by `7-g`, a proof map not a counting quotient). | The falsified claim is the all-K interval/adjacent-port interface for this family at `K>=6` — not ordinary nongracefulness of the full tree, and does not settle smaller K (the preserved `K=1,ell=1`, above-side pilot is feasible; `K=2..5` are not adjudicated here; threshold 6 sufficient, sharpness not established). Consequence: the queued pin sweep is superseded as a repair of this interface. ACCEPTED at reviewed revision `2cfb2df` (D018). The later port-5 supplier uses a distinct nonadjacent interface and does not invalidate this obstruction (D020). Full proof: `B2_INTERFACE_OBSTRUCTION.md`. |

## Current B2 fixed-interval control

For profile `[[1],[1],[],[]]` (m=7), the prescription `s:2=2`, `s:3=1` is infeasible in the exact finite model; shifting to `s:2=3`, `s:3=2` has a checked full witness. The release pilot and independent control tests preserve this contrast. `evidence/validation/VALIDATION_REPORT.md` states what completed during this build.

Thus the rule "always return the above interval starting at 1" already fails on this case. The graph's ordinary gracefulness remains witnessed. This does not exclude other shifted intervals, the below side, a noninterval interface, or a construction that relabels earlier vertices. The case was selected as a diagnostic control, not advertised as a novel theorem.

## Historical disposition rule

The C009 source filename and early header say provisional; the later retained counterexample index adopts the obstruction. Likewise use the corrected N246 count review rather than reviving the earlier H229-C claim. The archive preserves both context and correction so a fresh agent can see why the disposition changed.

For new failures, retain the exact original graph, parameters, declared restrictions, source/config identity, witness or scope of exhaustion, and the claim actually falsified. A smaller counterexample must still falsify that same claim; deleting a vertex changes the target and requires recomputing labels/domains.

### F-B4-2111-PORT-TEMPLATE

A discarded nine-vertex left-component template required alpha low-class
size 4, with `b:0:0=3` and `s:2=4` on the original first-three-section
unit graph. Any alpha edge of difference 1 at that cut must join labels
3 and 4. The two named vertices are nonadjacent, so this exact template
is impossible. The obstruction follows from the required edge difference
and uses no search. The accepted label-zero extension supplies the
`2111` seed through a different port state. [Derivation](B4_UNPADDED_2111.md)

### F-ZERO-PORT-FRESH-LABEL

For a graceful seed on n vertices, keeping old labels fixed and
assigning fresh label n to one new leaf at a host of label c>0
duplicates the old difference n-c, which lies in 1..n-1. This
rules out that fixed-label step at that host. It is an arithmetic
obstruction to the operation. [Zero-port proof](ALPHA_ZERO_PORT_LEAF_EXTENSION.md#host-restriction-and-source-comparison)

### F-MINIMUM-HIGH-WRONG-HOST

For an alpha seed on n vertices with low size p, raising old highs
by one and giving a fresh leaf label p at an old high host p+c with
c>0 gives difference c+1. That difference occurs in the shifted
old spectrum 2..n. This rules out that placement. In the composed
(q,r,1,1) seed the second center is two above the minimum high,
so the insertion belongs in the left component before R241.
A host at distance two from a supplied witness also puts the
new leaf at distance three from that same path.
[Minimum-high proof](ALPHA_MINIMUM_HIGH_LEAF_EXTENSION.md#scope-and-source-comparison)

### F-UPPER-BLOCK-WRONG-THRESHOLD

The retained relabeled nine-vertex alpha left state has p=4,
actual high exit 5, and the third center at 1, one edge from its
witness. Threshold c=8 meets the numerical bounds but selects only
s:0, whose full incident spectrum is {6,8}. It lacks the required
{7,8}. A single insertion at c=8 shifts those two differences
to 7 and 9 and creates a new difference 7 at the label-one host.
The unaffected first terminal edge already supplies 7, and
difference 6 is missing. This is a failure of that placement.
The supplied c=7 selects the full required block.
[Proof](ALPHA_UPPER_BLOCK_LEAF_INSERTION.md#independent-base-on-the-original-left-graph)

### F-B4-FOURTH-2-R241-ENTRANCE-ONE

With s:3=1 in the low class of the five-vertex original
right component, fixing s:4=3 repeats difference 2 and
fixing s:4=4 repeats difference 3. The low and high physical
classes force these cases. The retained left exit offset one
requires this entrance under the unchanged R241 connector
rule. This rules out that join with that left exit and
right component. [Proof](B4_FOURTH_2_SUPPLY.md#restricted-right-component-compatibility)

### F-QR12-MINIMUM-HIGH-PLACEMENT

The supplied 1212 state has low-class size 8 and actual host
b:1:0=10. Raising every high by one and giving the fresh leaf
label 8 makes weight 3 at host label 11, repeated in the
shifted old spectrum [2,15]. This is failure of the proposed
minimum-high placement at this particular host. The lower-block
rule instead uses the supplied full spectrum [7,14] at c=4.
[Conditional lower-block proof](ALPHA_LOWER_BLOCK_LEAF_INSERTION.md#comparisons-and-limits)

### F-QR12-BASE-UPPER-THRESHOLD-12

The initial 1212 proof draft used upper threshold 12. This
includes l:2:0:0 along with s:0 and l:0:0:0, and the complete
incident spectrum is [9,12,13,14]. The proof and certificate
use threshold 13, whose incident multiset is [12,14].
[Preserved draft and correction](../evidence/validation/B4_UNPADDED_QR12_001/attempts/base-upper-threshold-draft/README.md)
