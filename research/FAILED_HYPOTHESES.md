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

### F-B4-1122-FIXED-LOW-ADJACENT-GROWTH

For integer t>=3 the exact prefix `[[1],[1],[t],[2],[]]` with
the retained seven named low pins and physical s:4=7 cannot
supply all alpha differences. High labels remain free apart
from the exit. The spectrum forces s:0=M and the fixed
non-third-terminal differences omit M-2. A third terminal at
center label 2 would require the already used M to supply it.
[Restricted proof](B4_THIRD_ZERO_HOST_SEED.md#restricted-obstruction-with-all-seven-named-lows-fixed)

### F-B4-1122-ZERO-HOST-ADJACENT-SEED

On the exact normalized 1122 prefix the one first-witness
DFS query with full [0,6]/[7,14] alpha domains and only
b:2:0=0,s:4=7 exhausted after 17,514 nodes with count zero.
This is a computational negative for the stated physical
host and exit. The retained adjacent seed has b:2:0=2.
[Original-bound query record](../evidence/validation/B4_THIRD_ZERO_HOST_SEED_001/query_record.json)

### F-B4-1122-ZERO-HOST-NONADJACENT-K1-INTERFACE

The high-shifted zero-host seed with normalized s:4=8 leaves
R={7} and D={1} at K=1. The actual port is 9, so the sole
s:4--s:5 edge has difference 2. This rules out that singleton
interface. At K=2 the completed path labels (10,8,7) straddle
the class of the middle vertex and prevent alpha threshold
separation for that labeling. The [later direct singleton](B4_THIRD_ZERO_HOST_K1_DIRECT.md)
supplies K=1 using a different resource contract.
[Precise scope](B4_THIRD_ZERO_HOST_NONADJACENT.md#original-path-completion-and-scope)

### F-B4-Q1T2-K1-RETAINED-CORE-SINGLE-CUT

On the retained q=1 core with first center label 3, appending
a leaf at label c while raising every old label at or above c
by one would require the exact cut-crossing difference set
[c-3,12]. Each possible integer c in [4,13] fails that set on
the retained ledger. This rejects the fixed-label single-cut
template for the first addition. The relabeled core supplies
the rooted family through a different crossing spectrum.
[Analytic restriction and new ledger](B4_Q1T2_K1_ROOTED_CORE.md#exact-core-and-the-retained-comparison)

### F-B4-1R22-FIXED-1122-LOWER-BLOCK

The complete lower incidence multiset at second center b:1:0
fails on both saved 1122 diagnostic ledgers and the distinct
third zero-host ledger for every cut c=1,...,7. Only the
adjacent diagnostic at c=2 has the correct cardinality, but
its weight 9 replaces the required 10. This rejects the
specified fixed-ledger insertion templates even with the first
port allowed to move. A separately supplied max-host and zero
terminal ledger supports the positive 1R22 construction.
[Exact comparison](B4_UNPADDED_1R22_SUPPLIER.md#why-the-retained-lower-block-instances-cannot-be-imported)

### F-B4-1R22-K1-DELETED-SECOND-PREFIX-SHIFT

Deleting the second center and its original terminal from the
retained r=1 normalized 1R22 ledger and subtracting one from
each surviving label gives the specific 13-vertex alpha
prefix of the deleted-second core, with p=6, s:1=0 and s:4=7.
One high shift leaves R={6}, D={1} and s:4=8. Its only
pending edge would have weight 2. This is a failure of that
specific retained-prefix transport, rather than a root-pin
obstruction. The direct full core has its own exact ledger.
[Core proof and comparison](B4_1R22_K1_ROOTED_CORE.md#exact-core-and-construction)

### F-B4-12T2-RETAINED-1222-UPPER-BLOCK

For the specified retained 16-vertex 1222 ledger at
b:2:0=3, preserving s:4=9 under upper-block insertion
requires c=10,...,15. At c=14 the actual and required
incident counts coincide, but the full spectrum is
{8,12,13,14,15} instead of [11,15]. Other cuts fail the
count. The rejection is specific to that fixed ledger,
physical host and port-preserving transition.
[Exact comparison](B4_12T2_ZERO_HOST_SUPPLIER.md#restricted-comparison-with-the-retained-r2-ledger)

### F-B4-12T2-K1-UPPER-INCIDENCE-AS-CROSSING

On the retained 13-vertex core `[[1],[1],[],[2],[],[]]`,
all twelve old edges meet the upper side at cut 2. Only six
cross it. The six same-side upper edges keep their weights
under the shift, for example the old first terminal edge
with labels 3 and 2 and difference 1. Substituting all upper
incidences for the cut-crossing set gives [1,12] instead of
the required [7,12]. The ordinary crossing-cut insertion
uses the six actual crossings and succeeds.
[Exact calculation](B4_12T2_K1_ROOTED_CORE.md#retained-original-and-a-single-ordinary-insertion)

### F-B4-1R32-SHIFT-AT-SEED-CUT

After minimum-high insertion at the second center in
the exact (1,r,3,2) prefix, using the original cut 8 for
the final high shift moves H and the new leaves together.
Their differences [1,r-2] stay assigned, including 1 for
all r>=3, and the missing labels start at 8. This rejects
that fixed transformation as a supplier for the required
inventories. The proved shift uses the updated cut r+6.
[Exact shift calculation](B4_1R32_MINIMUM_HIGH_SUPPLIER.md#updated-high-shift-and-original-suffix)

### F-B4-1R32-K1-UPPER-INCIDENCE-AS-CROSSING

On the retained 14-vertex core `[[1],[2],[],[2],[],[]]` at
cut 3, all thirteen edges meet an upper-side vertex. The
seven crossings have differences [7,13]. The six same-side
upper edges have differences [1,6], all preserved by a
shift of that side. Using the full upper-side incidence
spectrum [1,13] fails the ordinary cut hypothesis. This
rejects the substitution on this ledger. Using the actual
crossing set gives the accepted growth.
[Exact calculation](B4_1R32_K1_ROOTED_CORE.md#retained-ordinary-core-and-complete-cut-premise)

### F-B4-1RT2-FLAT-THIRD-TERMINAL-LABELS

Continuing the original-third-terminal formula r+11+j at
fresh terminal index j=3 gives r+14, already the label at
physical s:2. The accepted supplier separates the original
third-terminal names from fresh names, whose labels start
at r+15. The collision rejects only the flat formula.
[Exact formula](B4_1RT2_TWO_HOST_COMPATIBILITY.md#named-normalized-formula)

### F-B4-1RT2-K1-INTERVAL-TRANSPORT

The normalized 1RT2 supplier retains its nonadjacent K>=2
contract. At K=1 the same shift leaves R={r+6}, D={1} and
physical s:4=r+8. Its single pending edge would have weight
two. This confirms the previously proved interface restriction
on this exact family. The new ordinary core lift uses
R={r+4}, D={6} at physical s:4=r+10 and completes the target.
[Prior interface](B4_1RT2_TWO_HOST_COMPATIBILITY.md#original-nonadjacent-suffix)
· [Direct singleton](B4_1RT2_K1_DIRECT_SINGLETON.md#direct-formula-and-exact-singleton)

### F-B4-1342-PORT-PRESERVING-UPPER-BLOCK

On the retained normalized `[[1],[3],[4],[2],[]]` alpha
labeling, require H=b:0:0=1 and unchanged physical s:4=10.
Shift all old labels at least c by h and give the prescribed
fresh first terminals c through c+h-1 at H. For c=11..18,
the signed excess difference sum per unit h is
4,2,1,1,1,1,1,-1. Hence this exact template fails for every
positive batch, including attempts that bypass the lemma's
complete incidence premise. The failure leaves other
labelings and insertion interfaces open.
[Complete ledgers and proof](B4_1342_FIXED_LEDGER_UPPER_BLOCK_OBSTRUCTION.md)

### F-B4-1342-ALL-LEDGER-PINNED-UPPER-BLOCK

The operation now fails for all normalized graceful alpha
labelings of the exact named 1342 original with [0,8] low,
[9,18] high and b:0:0=1, b:2:0=0, s:4=10. For each
c=11..18 the selected count differs from 20-c by the
degree and descending-difference proof, so no positive
batch of the exact upper-block shift and insertion can
succeed. The pinned alpha class is nonempty. This is a
transition obstruction with the stated pins and retains
the preceding fixed-ledger failure as separate evidence.
[Quantified proof](B4_1342_ALL_LEDGER_PINNED_OBSTRUCTION.md)

### F-B4-1342-RELAXED-FIRST-HOST-FIXED-EXIT

For the exact named 1342 graph with low labels [0,8], high
labels [9,18], physical b:2:0=0 and s:4=10, relaxing the
first host to any a in [2,8] did not supply the general-host
upper-block predicate [c-a,18] at any c in [11,18].
Thirty-three pairs fail proved necessary tests, and all
23 admitted pairs are exhausted by reviewed exact DFS.
The conclusion covers this exact domain and predicate.
[Scope and evidence](B4_1342_RELAXED_HOST_SEED_RESULT.md)

### F-B4-1342-U9-RELAXED-HOST-UPPER-BLOCK

On exact named 1342 with physical b:2:0=0 and s:4=9, alpha
classes [0,8] and [9,18], host a=2..8 and c=10..18, no
candidate supplies the complete spectrum [c-a,18]. The six
structurally admissible selected sets fail by actual incidence
and label constraints. The prescribed operation requires
this spectrum for every positive h, so it is rejected across
that domain. The two-pin alpha existence question without
the insertion predicate is outside the obstruction.
[Structural proof](B4_1342_U9_STRUCTURAL_OBSTRUCTION.md)

### F-B4-1342-TWO-EXITS-UPPER-BLOCK-CLOSEOUT

The new label-one proof rejects the complete selected
spectrum on named 1342 at b:2:0=0 and physical s:4=9 for
c=10..18 and every prescribed positive batch. Together with
the retained results, the exact upper-block interface is
rejected throughout host labels a=1..8 at exits 9 and 10,
subject to c strictly above the actual exit and c<=18, and
the alpha bands [0,8] and [9,18]. Prior results retain their
individual proof or reviewed computational evidence.
[Closeout and scope](B4_1342_U9_A1_ANALYTIC_CLOSEOUT.md)

### F-B4-JOINT-MAX-ROOTED-CORE-RETAINED-CUT-TRANSFERS

The retained q=2,r=1 ledger at physical b:1:0=8 and the
retained q=1,r=2 ledger at physical b:0:0=4 have no complete
crossing tail required for adding the missing named terminal
by the exact one-cut shift. All proper cuts 1..13 and both
endpoint arithmetic comparisons fail on each ledger. The
single separate joint maximum-rooted search is INCOMPLETE,
with no feasibility verdict.
[Proof and bounded outcome](B4_JOINT_MAX_ROOTED_CORE_PILOT.md)

### F-B4-JOINT-22-DIRECT-LEDGER-A

The displayed Case A choices on named `[[2],[2],[],[2],[],[]]`
with s:1=0 and physical s:2=14 give two copies of difference 2
and omit 6. The latter is already impossible in its remaining
terminal assignment because labels 4 and 10 are occupied by the
first and second centers. This rejects the stated arrangement.
The direct Case B ledger supplies the exact rooted core.
[Candidate construction and ledger](B4_JOINT_22_DIRECT_LEDGER.md)

### F-B4-JOINT-22-SECOND-HOST-FIXED-LEDGERS

At physical b:1:0=9, the accepted Case B q=r=2 ledger and
its q=3,r=2 output from first cut 11 both lack the full
ordinary crossing tail at every threshold. The ranges
are 0..15 and 0..16, including endpoint comparisons.
This rejects the exact prescribed second-host shift and
insertion for any positive batch on either fixed ledger.
Other graceful labelings and transitions remain open.
[Full spectra and proof](B4_JOINT_22_CUT_COMPAT.md)

### F-B4-JOINT-23-CASE-A-AND-SECOND-HOST

The displayed s:1=0 partial allocation on C(2,3) cannot
place pending weight 7 after assigning labels 4 and 11
to the nonadjacent left centers. Other Case A choices
remain open. The supplied Case B ledger is graceful.

At physical b:1:0=10 in that Case B ledger, every proper
cut and both endpoint comparisons fail the necessary
crossing tail. Thus the specified positive batch fails
on this fixed ledger. The result gives no obstruction
to a relabeled core or other second-host transition.
[Scoped falsifiers](B4_JOINT_23_MAX_ROOTED_CORE.md)

### F-B4-JOINT-22-CUT-13-TOP-PAIR-ZERO-RIGHT

The specific second-host plan with s:0=13, s:2=14,
c=13 and s:3=0 cannot supply the required tail on
C(2,2). Its four crossings force b:1:0=2. Choosing
s:1=1 then needs b:0:0=2, choosing s:1=2 repeats
the host label, and s:1>=3 yields a weight at most
10. Other upper selections and right-zero ledgers
remain open. An alternative with s:1=0 succeeds.
[Scoped proof](B4_JOINT_SECOND_CENTER_CUT_READY_22.md)

### F-B4-K2-D062-SINGLE-GAP-TRANSPORT

On the exact named target `[[2],[2],[2],[2],[],[],[]]`,
the D062 K=1 labeling F with q=r=t=2 gives no graceful
extension under the tested single-gap model. Embed each
old label as x + I[x>=c] for c=0..18. Assign only the 17
names through the original s:4 boundary, then place c
and the embedded old s:5 label on physical s:5 and s:6
in either order. Eleven cuts repeat a prefix difference.
At each of the eight valid prefixes the two available
orders fail to use the exact missing difference multiset.
The 38-case grid was exhausted. Other named labelings and
other suffix interfaces are outside this negative.
[Proof and full scope](B4_K2_D062_TWO_EDGE_TRANSPORT.md)

### F-B4-K2-D062-TWO-GAP-ORDER-PRESERVING

On the exact original `[[2],[2],[2],[2],[],[],[]]`, retain the
17 D062 K=1 labels in their relative order after withholding old
s:5. Map them to the increasing complement of any two holes
from [0,18], then place those holes on the original s:5 and s:6
in either order. All 342 distinct cases fail. There are 161
prefixes with repeated assigned differences and ten valid
prefixes with unusable suffix inventories. This exhausts the
specified order-preserving transport and preserves the separate
single-gap failure. Other prefix rank orders remain open.
[Proof and exact scope](B4_K2_D062_TWO_GAP_ORDER_PRESERVING.md)

### F-B4-K2-D062-S4-ADJACENT-RANK-EXCHANGES

On the exact retained original `[[2],[2],[2],[2],[],[],[]]`,
the two tested D062 prefix rank exchanges (9,10) and (10,11)
give no graceful completion under any of the 171 two-gap pairs
and two physical suffix orders per rank. The first exchange has
one valid prefix, but its two suffix weights cannot supply D={1,7}.
The second exchange necessarily repeats an assigned difference
by the exact named rank-gap argument. The 684-map negative
leaves other rank changes and independent suppliers open.
[Proof and exact scope](B4_K2_D062_S4_ADJACENT_RANK.md)

### F-B4-D068-FIRST-HOST-UPPER-BLOCK

**REJECT** prescribed first-host upper-block insertion on the
exact D066 normalized `[[2],[2],[2],[2],[]]` ledger at
b:0:0=6 with physical s:4=9 held fixed. All seven admissible
cuts c=10,…,16 fail the full incidence predicate. For any
positive batch h the edge-difference sum falls short by h
times the corresponding strictly positive selected-count deficit.
The zero batch is the identity. Other ledgers and insertion
rules remain outside this failure.
[Proof and exact scope](B4_D068_FIRST_HOST_UPPER_BLOCK.md)

### F-B4-D070-SECOND-HOST-LOWER-BLOCK

**REJECT** the prescribed lower-block insertion at physical
b:1:0 on the D070 supplied normalized `[[q],[2],[t],[2],[]]` maps.
For exact q,t>=2 and c=6,7,8, the count surplus is q−2 plus
3,5,5 respectively. Each positive batch has a positive
difference-sum surplus equal to its size times that surplus.
No other suppliers or second-host rules are excluded.
[Proof and exact scope](B4_D070_SECOND_HOST_LOWER_BLOCK.md)

### F-B4-D071-PINNED-DUAL-BLOCK

**REJECT** simultaneous upper-block supply at b:0:0 and lower-block
supply at b:1:0 on a single normalized alpha-graceful labeling of
named 2222 with b:0:0=5, b:2:0=0 and s:4=9. All port-admissible
cuts u=10..16 and d=6..8 are covered by the symbolic degree,
containment and named-incidence contradictions. This concerns
these two complete predicates under these pins.
[Proof and exact scope](B4_D071_PINNED_DUAL_BLOCK_OBSTRUCTION.md)

### F-B4-D072-UNPIN-FIRST-HOST-DUAL-BLOCK

**REJECT** simultaneous complete upper and lower incidence
premises on the exact named normalized 2222 original with
s:4=9, b:2:0=0 and any first-host label a=1..7. The structural
proof covers u=10..16 and a<d<=8. Other exits and other growth
rules remain distinct proof obligations.
[Proof and exact scope](B4_D072_UNPIN_FIRST_HOST_DUAL_BLOCK.md)

### F-B4-D073-U8-DUAL-BLOCK

**REJECT** the same-ledger complete upper and lower block premises
on the exact named normalized 2222 original at physical s:4=8,
b:2:0=0 and any a=1..7. The proof covers 9≤u≤16 and a<d≤8
by count equality and actual original incidence contradictions.
Other exits, labelings outside this orientation, and growth methods
with different premises remain distinct.
[Proof and exact scope](B4_D073_U8_DUAL_BLOCK_STRUCTURAL.md)

### F-B4-D074-U10-DUAL-BLOCK

**REJECT** same-ledger upper and lower complete block supply
on normalized named 2222 with physical s:4=10, b:2:0=0 and free
first-host a=1..7. The structural proof covers all retained cuts.

**REJECT** K=2 completion of the specified high-shift interface
at offset three above max(R). Its first pending original edge
cannot realize either unused difference, independently of seed
existence. Other labelings and interfaces have separate scope.
[Proof and exact scope](B4_D074_U10_DUAL_BLOCK_FEASIBILITY.md)

### F-B4-D075-DIRECT-2322-K1-INTERFACE

**REJECT** completing K=1 by the direct 2322 seed's high-shift interface.
It leaves R={9} and D={1} at physical s:4=11, so the only pending
edge would have weight 2. The separate K=1 construction is unaffected.
[Proof](B4_D075_DIRECT_2322_ALPHA_S4_10.md) · D076

### F-R241-PAIRED-SPINE-L1

**REJECT** the exact high-shift suffix interface for one trailing empty section. At L=1 it leaves only vertex label P and difference 1 at physical exit s:(n−1)=P+2. The sole original pending edge would use difference 2. This result concerns that interface. [Proof](R241_PAIRED_BRANCHED_SPINE.md#exact-suffix-resources-and-termination) · D078
