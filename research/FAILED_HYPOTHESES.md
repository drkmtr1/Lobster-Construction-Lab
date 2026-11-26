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

### F-R241-TWO-CENTER-STRICT-PORT

**REJECT** universal fixed physical offsets (1,1) for positive quotas on `[[a,b],[c]]`. On original `[[1,1],[1]]` the cut of size four and pins s:0=1, s:1=5 force a repeated original difference. This same graph has graceful alternate-port states. The verified (1,0) state also cannot directly precede an entrance of offset 1 under the prescribed R241 placement. [Proof](R241_TWO_CENTER_PORT_FALSIFIER.md) · D079

### F-R241-EQUAL-ONE-PAIR-ZERO-TO-ONE

**REJECT** offsets (0,1) on the original `[[1],[1]]`, at cut P=3 with s:0=0 and s:1=4. The required weight five forces b:0:0=5, and the only two remaining first terminal values duplicate an original weight. The same original supplies (0,0). The replacement `[[a],[a+1]]` has different original quotas and supplies (0,1). [Proof](R241_ZERO_TO_ONE_BRIDGE.md) · D080

### F-R241-UNEQUAL-FIRST-PAIR-ONE-ZERO

**REJECT** the original `[[1,2],[1]]` supplier at physical offsets (1,0). With P=5, the edge-weight sum forces one of three center-label triples, each missing weight 8 or duplicating weight 4. The same original is graceful at offsets (2,0). The tied-quota replacement `[[1,b],[b]]` is a different domain and supplies (1,0). [Proof](R241_UNEQUAL_TWO_CENTER_RETURN.md) · D081

### F-R241-222-STRICT-RETURN

**REJECT** `A(11,6;1,0)` on the original `[[2,2],[2]]` at physical s:0=1 and s:1=6. The signed-degree identity and extremal edge leave two actual branches: duplicate weight 5 or absent weight 3. This rejects the specified R241 starting state only. [Proof](R241_222_STRICT_RETURN.md) · D082

### F-R241-223-STRICT-RETURN

**REJECT** `A(12,6;1,0)` on exact original `[[2,2],[3]]` at physical s:0=1 and s:1=6. Signed-degree and maximum-weight constraints force right center 4 with a right terminal labeled 9. That actual edge duplicates the physical spine's weight 5. The obstruction applies to this state and its proposed use as B for the D080 bridge. [Proof](R241_223_STRICT_RETURN.md) · D083

### F-R241-222-EXCLUDED-OFFSETS

**REJECT** the 28 individual physical alpha offset states marked E in the [D084 menu](R241_222_OFFSET_MENU.md#the-complete-menu) for the exact named `[[2,2],[2]]` original at cut six. The signed degree sum excludes odd exit offsets. The remaining excluded states fail a mandatory incidence or residual-weight condition for every numerical center possibility. D082's (1,0) exclusion retains its historical evidence without replay. The same original has witnessed states (2,0) and (3,4). D084

### F-R241-232-OFFSET-20

**REJECT** A(12,7;2,0) on exact named `[[2,3],[2]]` at prescribed s:0=2 and s:1=7. The two unequal first-center roles have distinct signed-degree coefficients. All 12 ordered choices fail parity, the low inventory, a mandatory repeated weight or missing weight 3. The same original supplies A(12,7;3,4). [Proof](R241_232_TWO_PORT.md) · D085

### F-R241-3B2-PORT44

**REJECT** the simultaneous prescribed (4,4) physical state A(b+10,b+5;4,4) on exact named `[[3,b],[2]]` for every integer b≥2. With actual s:0=4 and s:1 equal to m, the three largest weights occupy the right attachment and the two right terminal edges. Every representation of m−3 lacks its actual required incidence. This closes the prescribed module at these ports. [Proof](R241_3B2_PORT44_SYMBOLIC.md) · D088

### F-R241-42-PORT53

**REJECT** A(10,6;5,3) on exact named `[[4],[2]]`, with entrance s:0 low at label 5 and exit s:1 at label 9. The realized incidences of weights 9, 8 and 7 prohibit every weight-six incidence. The separate signed-degree argument requires 2A=13 after forcing the right center to zero. This is an exclusion of the simultaneous prescribed physical state. D078 supplies this original at (1,1). [Proof](R241_42_PORT53_RETURN.md) · D091

### F-R241-43-PORT53

**REJECT** A(11,6;5,3) on exact named `[[4],[3]]` at the physical s:0=5, s:1=9 pins with s:0 low. The signed-degree equation forces (A,z)=(8,2). An actual right-terminal edge repeats the spine's difference four, and the required labels 0 and 10 lie at nonadjacent terminals. This excludes the selected state at cut six. D078 independently supplies the exact original at (1,1). [Proof](R241_43_PORT53_RETURN.md) · D092

### F-R241-43-2-LOWER-BLOCK

**REJECT** the claim that at least one of nine permitted thresholds supplies the original `[[4,3],[2]]` via one lower-block leaf insertion at `b:0:1` from the D098 `[[4,2],[2]]` ledger or its within-class reflection. Ledger I repeats 10−c and omits 9−c at c=4 through 8. Ledger II repeats 5 and omits 4 at c=5 through 7, then repeats 4 and omits 1 at c=8. This closes exactly the nine placements from the two fixed sources and does not adjudicate either prescribed numerical port pair across other labelings. [Proof](R241_43_2_LOWER_BLOCK.md) · D099

### F-R241-43-2-FIXED-EXIT3

**REJECT** A(14,9;x,3) on exact ordered `[[4,3],[2]]` for every integer entrance x in [0,8]. The signed-degree equation and forced extreme incidences give eight scalar cases, each excluded by an original-edge or terminal-capacity contradiction. The proof is independent of the stopped audit. The official executable audit is **INCOMPLETE** because its assertion incorrectly required the recorded repeated weight to be the sole repeat. Preserve the frozen sources and receipt. [Proof](R241_43_2_FIXED_EXIT3.md) · D100

The [separate D100 audit recovery](../evidence/validation/LCL_R241_43_2_FIXED_EXIT3_AUDIT_RECOVERY_001/README.md) **PASSED** after checking the named repeated weight among all repeats. It corroborates the same fixed-exit exclusion. The original D100 official audit remains **INCOMPLETE**.

### F-R241-42-2-MAXIMUM-HOST

**REJECT** the cut-8 alpha source on exact ordered `[[4,2],[2]]` with physical b:0:1=12, for all spine labels allowed by the orientation with s:0 low. All eleven necessary scalar cases fail their actual incidence differences. This closes the prescribed maximum-host preimage for the conditional translate-and-add-zero path. Other source states and target labelings retain their own scopes. [Proof](R241_42_2_MAXIMUM_HOST.md) · D101

### F-R241-43-2-RIGHT-ZERO-HOST

**REJECT** the cut-9 alpha state on frozen ordered `[[4,3],[2]]` with physical right center `b:1:0=0` for all spine labels allowed by the orientation with `s:0` low. The spine must supply weight M=max(A,B), which contradicts the signed degree sum in both strict orders. The exclusion applies only to this original and host constraint in the prescribed orientation. [Proof](R241_43_2_RIGHT_ZERO_HOST.md) · D102

### F-R241-43-2-ZERO-ENTRANCE

**REJECT** the cut-9 alpha state on frozen ordered `[[4,3],[2]]` with `s:0=0` for all exit labels allowed by the orientation. The seven possible scalar cases fail through absent left-terminal weights or repeated weight 9 on two named attachments. The exclusion applies only to the specified cut, orientation, entrance and original. [Proof](R241_43_2_ZERO_ENTRANCE.md) · D103

### F-R241-43-2-LEFT-TERMINAL-ZERO

**REJECT** cut-nine supply with zero at any left terminal on exact frozen ordered `[[4,3],[2]]` and both ports free. All 19 remaining cases miss a difference. Combined with D102 and D103 and the complement argument, this excludes both alpha orientations on this original. Ordinary gracefulness remains a separate open obligation. [Proof](R241_43_2_LEFT_TERMINAL_ZERO.md) · D104

### F-ORDINARY-53-2-SIGNED-SEED

**REJECT** the prescribed signed seed on ordered `[[5,3],[2]]` with `s:0=0`, `s:1=14`, `b:1:0=1` and the sole negative signed difference −1 on `l:0:0:3 → b:0:0`. All three center rows force repeats of absolute edge differences. The conclusion applies to these joint constraints on this exact original. [Proof](ORDINARY_53_2_SIGNED_SEED.md) · D108

### F-ORDINARY-53-2-FREE-REVERSAL

**REJECT** the location-free magnitude-one interface on frozen ordered `[[5,3],[2]]` at `s:0=0`, `s:1=14` and `b:1:0=1`, oriented from the class of `s:0`. All four scalar rows force repeated absolute differences. The exclusion applies to the sole −1 on an actual left terminal at these pins. Ordinary gracefulness under other constraints remains undecided. [Proof](ORDINARY_53_2_FREE_REVERSAL.md) · D109

### F-ORDINARY-53-2-MAGNITUDE-TWO

**REJECT** a sole −2 at any actual left terminal on frozen ordered `[[5,3],[2]]` with `s:0=0`, `s:1=14` and `b:1:0=1`, oriented from the class of `s:0`. A right-terminal 13 forces a center and terminal to share a label. A reversed first-left terminal 13 forces repeats 9 and 11. A reversed second-left terminal 13 contradicts the signed degree bound `107<111`. Other signed patterns and ordinary gracefulness remain undecided by this proof. [Proof](ORDINARY_53_2_MAGNITUDE_TWO.md) · D110

D111 supplies an ordinary graceful certificate at the same three pins with three negative signed incidences. It lies outside each of the three excluded D108–D110 signed interfaces. [Proof](ORDINARY_53_2_DIRECT_SEED.md) · D111

D112 uses that certificate as the base of ordinary right-terminal growth at the same seed pins. The conditional growth rule has no signed-edge restriction. D104's alpha exclusion and the D108–D110 single-reversal exclusions retain their exact domains. [Proof](ORDINARY_EXTREME_SPINE_GROWTH.md) · D112

D113 extends direct ordinary seed supply to odd first-left quotas. The q=5 specialization still has three negative signed edges and lies outside the historical single-reversal hypotheses. The midpoint-flip control exhausts both residual inventories and fails the original quotas. Thus exact label and difference inventories alone do not imply feasibility of this specific host allocation. [Proof](ORDINARY_Q3_2_ODD_COMPLEMENTARY_SUPPLIER.md) · D113

D114 proves that carrying over D113's second-left label 2 to the pinned even-quota seeds violates the necessary degree-parity identity. The exclusion is for that numerical assignment. D114's reversed host order supplies the same pinned even domain, and the pair-flip control independently shows why exact resources require a separate actual quota check. [Proof](ORDINARY_Q3_2_EVEN_COMPLEMENTARY_SUPPLIER.md) · D114

D115's retained allocation-only pair flip preserves complete residual label and weight multisets and keeps the midpoint at the lower host, yet changes lower/higher quotas from (1,5) to (3,3). It fails the exact named physical quotas. This scope concerns the modified allocation on the retained original. [Evidence](../evidence/validation/LCL_ORDINARY_QA_2_ODD_ODD_COMPLEMENTARY_SUPPLIER_001/result.json) · D115

D116 separates two scoped failures. The retained cross-center swap preserves actual quotas and pins but repeats weights 3 and 7. The pair-only flip preserves both inventories but fails quotas at (6,1). Symbolically, the even–even midpoint-only move also preserves both inventories and fails quotas at (ell−1,h−1), with no extra numerical original tested. [Proof](ORDINARY_QA_2_PARITY_COMPLEMENTARY_SUPPLIER.md) · [Evidence](../evidence/validation/LCL_ORDINARY_QA_2_PARITY_COMPLEMENTARY_SUPPLIER_001/result.json) · D116

D117's within-center swap on D111 disproves that retained ordinary validity and growth compatibility identify the deterministic indexed formula. The D114 cross-center swap preserves the label bijection, quotas and pins yet repeats 3 and 7 and omits 4 and 8. Complementation preserves the spectrum while failing the prescribed pins and growth labels. These are scoped control failures on the retained originals. [Audit](../evidence/validation/LCL_ORDINARY_QAR_ALL_PARITY_SUPPLIER_001/result.json) · D117

D118 disproves that local integral feasibility of two batches implies their global compatibility. The palette overlap probe passes both local allocations at their prescribed quotas, repeats global labels 5 and 10 and weights 3 and 8, and omits labels 6 and 9 and weights 4 and 7. Separately, a Batch B pair move preserves its two palettes and violates its named quotas. The cross-center swap within Batch B preserves the pins and label alphabet while duplicating two original weights. [Audit](../evidence/validation/LCL_ORDINARY_QA2_2_DISJOINT_R226_SUPPLIER_001/result.json) · D118

D119's interleaving boundary invalidates the extra assumption that the odd progression must lie entirely below the Batch A midpoint. The construction works across that midpoint. The allocation-only probes separately show exact resources with wrong local quotas, and exact local allocations with overlapping global resources. [Audit](../evidence/validation/LCL_ORDINARY_QAC_2_EVEN_C_DISJOINT_R226_SUPPLIER_001/result.json) · D119

D120's centered reservation separates arithmetic midpoint existence from local availability. Its midpoint-only move preserves both Batch B inventories but fails its named quotas. Its overlap probe preserves both local quota slices and fails the global inventory partitions. The genuine cross-batch swap also shows that retaining original vertex labels as a multiset and keeping physical pins and quotas do not suffice for the difference bijection. [Audit](../evidence/validation/LCL_ORDINARY_QAC_2_ODD_C_DISJOINT_R226_SUPPLIER_001/result.json) · D120

D121's retained binding probes separate index bijectivity from physical quota and slot compatibility. The within-host swap passes ordinary gracefulness and both physical checks while failing deterministic pointwise agreement. The necessary degree-parity identity also excludes the three prescribed pins when all three left quotas are even. This last filter concerns the pinned problem. [Audit](../evidence/validation/LCL_ORDINARY_QAC_2_TWO_ODD_ONE_EVEN_ROLE_TRANSPORT_001/result.json) · [Proof](ORDINARY_QAC_2_TWO_ODD_ONE_EVEN_ROLE_TRANSPORT.md) · D121

D122 refutes universal completion of the fixed D118 labeled core in the ordered two-even sector. At a=3 and c≥q−2 the residual permutation's parity-class capacity rules out every completion. The scope is the specified core, numerical roles and pins. The controls separately reject midpoint moves at fixed quotas and local allocations with overlapping global inventories. [Proof](ORDINARY_QAC_2_TWO_EVEN_FIXED_CORE_CLASSIFICATION.md) · [Audit](../evidence/validation/LCL_ORDINARY_QAC_2_TWO_EVEN_FIXED_CORE_CLASSIFICATION_001/result.json) · D122

D123's reflection-pair move preserves both local inventories while violating the X/M quotas. Its overlap fixture preserves both local integral allocations and violates the global resource partitions. The modified core supplies the symmetric even family where D122's prescribed core cannot complete, establishing that the D122 obstruction depends on the fixed labeled core. [Audit](../evidence/validation/LCL_ORDINARY_U3U_2_MODIFIED_SHARED_MIDDLE_CORE_001/result.json) · [Proof](ORDINARY_U3U_2_MODIFIED_SHARED_MIDDLE_CORE.md) · D123

D124's allocation-only chain control rejects the inference that an individually eligible host/label row may be selected independently. The move preserves all labels, repeats weight 15 and misses 17, and violates both named batch quotas. Its separate palette control retains both local allocations while duplicating a global label and difference. [Audit](../evidence/validation/LCL_ORDINARY_Q3C_2_UNEQUAL_MODIFIED_SHARED_MIDDLE_CORE_001/result.json) · D124

D125 extends the all-even excess-degree obstruction to every r≥2 at the three prescribed physical pins. It also excludes using the final edge count m in the fixed right-index-0 formula at r≥3, since that repeats m−1 at the last new right terminal. The retained adverse triple (6,3,4) is outside established coverage, with D122’s obstruction confined to its original fixed labeled core. [Proof](ORDINARY_QACR_CONSOLIDATED_SEED_D112_GROWTH.md) · [Audit](../evidence/validation/LCL_ORDINARY_QACR_CONSOLIDATED_SEED_D112_GROWTH_001/result.json) · D125

D126 rejects the assumption that the upper complementary interval must meet both parities for this exact modified-core completion. The singleton {13} gives one nonempty forced component. The eligible alternative M row for label 3 repeats weight 11 and loses 13 when used in isolation. The locally feasible overlap probe also duplicates global label 5 and weight 3. D122's old fixed-core obstruction remains in force. [Proof](ORDINARY_634_2_MODIFIED_SHARED_MIDDLE_CORE.md) · [Audit](../evidence/validation/LCL_ORDINARY_634_2_MODIFIED_SHARED_MIDDLE_CORE_001/result.json) · D126

D127's retained controls reject three distinct transport errors. A repeated physical index fails before quota binding, a bijective map can still omit and request incompatible named slots, and a reversible index map can still point in the wrong direction. The inverse of (1,2,0) round-trips with its own inverse but gives the wrong forward image at every index. [Audit](../evidence/validation/LCL_ORDINARY_QAC_2_TWO_EVEN_OUTER_ODD_ROLE_TRANSPORT_001/result.json) · D127

D128 shows that putting every intact A reflection pair at X is unnecessary for the modified core. At the new boundary, reversing its whole M pair preserves both local inventories and fails the exact quotas. The overlap probe separately passes both local allocations but repeats global label 13 and weight 11. The retained graphs and historical scopes remain intact. [Proof](ORDINARY_4A4_2_MODIFIED_SHARED_MIDDLE_CORE.md) · [Audit](../evidence/validation/LCL_ORDINARY_4A4_2_MODIFIED_SHARED_MIDDLE_CORE_001/result.json) · D128

D129's two allocation controls separate local weights from exact quotas and local feasibility from global compatibility. Flipping {8,14} preserves both A inventories and changes the X/M quotas from (5,3) to (3,5). Replacing label 8 and weight 6 with label 7 and weight 5 reconstructs a feasible A with pair {7,15}, and both batches individually pass. Their combined inventories repeat label 7 and weight 5 and miss label 8 and weight 6. D122's different fixed-core obstruction retains its original scope. [Audit](../evidence/validation/LCL_ORDINARY_QAC_2_UNIFIED_MODIFIED_SHARED_MIDDLE_CORE_001/result.json) · D129

D130 excludes every completion of the specified D123 labeled core on exact `[[2,a,c],[2]]` with odd a≥c+1 and even c≥4. The necessary X label t+a−1 exceeds the largest residual label. The obstruction covers all residual reservations and is scoped to the fixed labels and roles. D122's obstruction for its different labeled core retains its own scope. D130's pair move also preserves the local spectra while failing the named quotas, and its overlap mutation retains local feasibility while repeating label 12 and difference 10 globally. [Proof](ORDINARY_2AC_2_MODIFIED_CORE_CLASSIFICATION.md) · [Audit](../evidence/validation/LCL_ORDINARY_2AC_2_MODIFIED_CORE_CLASSIFICATION_001/result.json) · D130

D131's fixed reflection and zero-centered suffix require the connector frontier label n+2+δ. At δ>r that value exceeds the new maximum, so the prescribed transition cannot proceed. The obstruction is to this placement. The physical frontier control separately rejects s:0 despite a scalar deficit that agrees at that vertex, and the numerical control rejects an incorrect deficit at the correct frontier. [Proof](ORDINARY_SPINE_DEFICIT_TRANSITION.md) · [Audit](../evidence/validation/LCL_ORDINARY_SPINE_DEFICIT_TRANSITION_001/result.json) · D131

D132 rejects an appended two-center section from a supplied deficit-zero state at n≥q+a+2 under every single affine isometry of that supplied old labeling. The two unused label intervals force the canonical placement up to complement, and neither 0 nor n equals a positive quota. The restriction is to the supplied labels and affine embedding class. D132 also separates local reflection-first admission from existence of a mode plan for a whole mixed list. A symbolic translation-only control establishes that the mode must be carried in the plan. [Proof](ORDINARY_SPINE_TWO_CENTER_AFFINE_TRANSITION.md) · [Audit](../evidence/validation/LCL_ORDINARY_SPINE_TWO_CENTER_AFFINE_TRANSITION_001/result.json) · D132

D133 excludes every single-affine offset and slope for one appended section with h≥3 independently specified positive quotas at n≥h+Q, including equality. The required terminal coordinates can be covered only by the two extreme center labels, contrary to intermediate positive quotas. The same failure holds for any old relabeling with the same two inventory properties. This is a scoped embedding obstruction. D131 and D132 keep their positive transition scopes. [Proof](ORDINARY_SPINE_ARBITRARY_CENTER_AFFINE_OBSTRUCTION.md) · [Audit](../evidence/validation/LCL_ORDINARY_SPINE_ARBITRARY_CENTER_AFFINE_OBSTRUCTION_001/result.json) · D133

D134 isolates two distinct scoped failures. A shifted crossing weight can collide with an old noncrossing weight even when translated labels remain injective. A terminal transposition across the return split can preserve the full terminal spectrum while violating the needed crossing subinventory. At the declared maximum cut on D130, the crossing spectrum fixes oriented c=1 and d=19, which would require h=35 on a 20-edge prefix. The D133 obstruction retains its scope. [Proof](ORDINARY_SPINE_PIECEWISE_CUT_SPECTRUM_TRANSITION.md) · [Audit](../evidence/validation/LCL_ORDINARY_SPINE_PIECEWISE_CUT_SPECTRUM_TRANSITION_001/result.json) · D134

D135 excludes a nonzero quota moment for D134's fixed center labels and exact terminal spectrum. Even with the global spectrum and quotas satisfied, a cycle that crosses the return split changes the crossing subinventory and defeats the required return state. Failure of the chosen width packing leaves alternative layouts and other embeddings open. [Proof](ORDINARY_SPINE_GENERAL_DISPLACEMENT_CYCLE_ALLOCATION.md) · [Audit](../evidence/validation/LCL_ORDINARY_SPINE_GENERAL_DISPLACEMENT_CYCLE_ALLOCATION_001/result.json) · D135

D136 disproves two unsafe inferences within the packet placement. Virtual mass assigned to a pair of types need not support one complete packet, so rounding z=ab−1 upward overdraws the reserved mass. A valid rotation permutation straddling the return split preserves global resources and quotas while failing the required crossing band. In the strict improvement family, rearranging D135's selected separate spans cannot repair total width overflow. Other allocations remain open on a D136 rejection. [Proof](ORDINARY_SPINE_INTERLEAVED_ROTATION_PACKET_ALLOCATION.md) · [Audit](../evidence/validation/LCL_ORDINARY_SPINE_INTERLEAVED_ROTATION_PACKET_ALLOCATION_001/result.json) · D136

D137 excludes same-polarity return within the stated two-translation class because the original connector would have weight A≤n/2. Positive A duplicates an old noncrossing weight, and A=0 gives zero and repeats the frontier label. Forcing h=2p'+1 produces excess crossing incidences at p'>p and a deficit at p'<p even with arbitrary fresh placement in the class. The scope retains both cut states, extreme frontiers, the size regime and preserved cut membership. [Proof](ORDINARY_SPINE_MIXED_MULTIPLICITY_CUT_STATE_BRIDGE.md) · [Audit](../evidence/validation/LCL_ORDINARY_SPINE_MIXED_MULTIPLICITY_CUT_STATE_BRIDGE_001/result.json) · D137

D138 exhausts alternate exterior and gap placements within the exact D137 class. A terminal at m−1 repeats the connector or a distinct attachment when the upper exterior has more than one label. The exact two-interval coordinate count is strictly below any positive gap-center demand, even at e=0. On the dominant-increment family every numerical role assignment fails the necessary moment, while the distinct symbolic positive role exchange shows why a fixed-index moment test cannot give this obstruction. [Proof](ORDINARY_SPINE_CANONICAL_PLACEMENT_RIGIDITY.md) · [Audit](../evidence/validation/LCL_ORDINARY_SPINE_CANONICAL_PLACEMENT_RIGIDITY_001/result.json) · D138

D139 identifies the limit of its stronger state at b=1. The unique new boundary label lies at a terminal of center zero and its weight is d'+1. The ordinary D134 state survives. A D134 spectrum by itself does not certify the requested leaf incidence, and the claimed exceptional shift requires degree one for the named old boundary vertex. D138 still excludes its own two-translation class on D139's three distinct quotas. [Proof](ORDINARY_SPINE_TWO_CUT_BOUNDARY_LEAF_BRIDGE.md) · [Audit](../evidence/validation/LCL_ORDINARY_SPINE_TWO_CUT_BOUNDARY_LEAF_BRIDGE_001/result.json) · D139

D140 excludes a center-1 boundary return if Q−t=K because J omits the required fixed image. This is unavoidable for z=b=1 in the exact placement, while D139 still gives its ordinary final step. Outside the exact quota criterion no unit-step allocation in the declared placement can supply the stronger return. Alternative placements and other ordinary labelings remain open. [Proof](ORDINARY_SPINE_TWO_CUT_EXACT_QUOTA_CLASSIFICATION.md) · [Audit](../evidence/validation/LCL_ORDINARY_SPINE_TWO_CUT_EXACT_QUOTA_CLASSIFICATION_001/result.json) · D140

D141 excludes larger canonical exceptional blocks for p'=1 on every D140 repeatable output and on the named D139 preparation. The top two low labels already force two actual crossings in R. On the independently supplied D134 p=1 non-leaf family, a>gamma gives an actual too-small P edge, while a≤gamma leaves P empty and forces a first-gap collision below d. This excludes canonical three-center positive-gap completion for every permitted additional cut on those inputs. Other two-cut placements and other ordinary labeling architectures remain open. [Proof](ORDINARY_SPINE_BOUNDARY_BLOCK_SPECTRAL_OBSTRUCTION.md) · [Audit](../evidence/validation/LCL_ORDINARY_SPINE_BOUNDARY_BLOCK_SPECTRAL_OBSTRUCTION_001/result.json) · D141

D142 rules out equal frontier polarity on the independently supplied D141 non-leaf family throughout the declared embedding class. Under B≤a it excludes B>1 by exterior connectivity and repeated weights, and recovers D141 at h=A=3, B=1. In the smaller-cut regime, the required weight r+s also rules out placements with no gap endpoint in its exact window when r>A+c−1. These exclusions leave other variable-exterior placements unresolved. [Proof](ORDINARY_SPINE_VARIABLE_EXTERIOR_BRIDGE.md) · [Audit](../evidence/validation/LCL_ORDINARY_SPINE_VARIABLE_EXTERIOR_BRIDGE_001/result.json) · D142

## D143 scoped two-section exclusions

In the supplied D134 p=1, n≥H=2K two-section class with an extreme return and preserved old cut membership, opposite polarity is impossible. Exact high-weight coverage forces the actual first connector vu to reach the upper exterior and forces the exterior induced forest to be connected. Its actual edge uw crosses the exterior intervals, placing w in the lower exterior. Positive-quota gap centers are impossible, since their terminals would be in the gap on the same cut side and have weights below d. The width A=1 is also excluded because the smallest gap label has no eligible actual host weight. The Director accepted these symbolic exclusions within the declared class. Other embedding classes and ordinary gracefulness remain open. [Proof](ORDINARY_SPINE_TWO_SECTION_CUT_STATE.md) · D143

## D144 physical gap allocation obstructions

In the declared D143 embedding, a gap with B=1 cannot assign its first upper source k. At A=2 the first two gap coordinates must both go to the physical host carrying zero. On the independently supplied D143 five-vertex exterior a symbolic quota family has only one such leaf while satisfying the aggregate equations and the global parity test. Thus those tests do not ensure physical feasibility. A rejection by D144's sufficient packet recipe alone leaves other allocations open. [Proof](ORDINARY_SPINE_TWO_SECTION_GAP_ALLOCATION.md) · D144

## D145 fixed-exterior quota packet rejection

Failure of both D144 boundary recipes can occur for a feasible physical quota vector on the same fixed exterior. The symbolic family (3,0,1+2r,2,1) at k=r+4 violates the required packet width under rule 2 and demands a negative M_2 under rule 1. Its explicit boundary reflection pair gives a valid matching together with the remaining named assignments. The scoped D144 forced-endpoint adverse family still fails all exact allocations. The sufficient packet theorem remains accepted. [Proof](ORDINARY_SPINE_TWO_SECTION_EXACT_GAP_CRITERION.md) · D145

## D147 independent exterior supply obstructions

Within D143, a first section with no direct leaves and a second section with one positive center and no direct leaves cannot supply the first upper gap source. Its only upper host with gap leaves has maximal upper index B. With one first center and no first direct leaves and one second center plus at most three second direct leaves, the terminal-free arm also fails. It needs either a forbidden first-upper assignment or three gap direct leaves at w when at most two are available. The named profiles (3) and (2g+4,0,0,0) refute terminal-free sufficiency in this embedding because their terminal-enabled assignments are proved. Other graceful embeddings remain outside this conclusion. [Proof](ORDINARY_SPINE_EXTERIOR_SUPPLY_REASSESSMENT.md) · D147

## D148 matched exterior terminal-free obstruction

Within D143, a terminal-free exterior cannot complete the original profiles with one first center and no first direct leaves and two second centers with at most two second direct leaves. Actual host identities and the first three forced gap sources exceed the direct quota of w. This excludes Arm T throughout the specified subfamily. The symbolic obstruction does not decide Arm E. The finite Arm E outcomes are recorded below and the scope stays within D143. [Proof](../research/matched_exterior_001/CONTRACT.md)

## D148 official matched exterior execution exclusions

All 68 priority two-center originals with one first center and no direct leaves at u and at most two direct leaves at w failed Arm E by independent exhaustion within the frozen corpus and D143 interface. Their T exclusion follows from the separate Director-accepted symbolic obstruction. This finite outcome excludes a contrast on that tested subfamily only. Five matched contrasts occur elsewhere in the same two-center corpus. The unfinished and unentered arms have no inferred outcome. [Official evidence](../evidence/runs/d148-matched-exterior-001/README.md)

## D149 terminal-free parity obstruction

For a D143 original with one odd-quota positive center and no first-section direct leaves, and only even quotas at the second-section positive centers, no terminal-free exterior works. Its actual reduced sides force A=2, with the first center at low label 1. Its odd terminal count gives an odd contribution under translation −1. Every upper center contributes an even term in the D144 summed displacement identity, and spine-host direct leaves add zero. The contradiction holds regardless of how many second-section direct leaves are exterior. For (3) and (2p,2q,0,0,0,0), the explicit terminal-enabled supplier proves D143 feasibility on the same named target. [Proof](ORDINARY_SPINE_TWO_CENTER_EVEN_QUOTA_SUPPLIER.md#2-terminal-free-obstruction)

## D150 exact terminal-free exclusion on the (1,1) half-quota pair

For the ordered original (4), (2,2,0,0,0) and the admissible D143 input and embedding, all three direct leaves of w must go in the gap in a terminal-free placement. At the forced A=2, B=3 exterior, i=3 and the first three upper gap sources must use the actual center at upper index b=2. Both center quotas equal two, so the placement is impossible. The terminal-enabled proof supplies the same named original. The independently derived terminal-free construction supplies every larger half-quota pair in the stated family. Ordinary gracefulness outside D143 remains outside this result. [Proof](ORDINARY_SPINE_TWO_TO_ONE_TERMINAL_SUPPLIER.md#4-terminal-free-d143-classification)

## D151 one-direct-leaf D143 exterior obstruction

With exactly one positive center and no direct leaves at u, any completion in the declared D143 interface needs two distinct direct-gap leaves at w. Reduced difference two pins a=A−1, and differences 3 through A force the low-index upper vertices to be actual terminals of a. For gap sources 0 and A−1 the two translates at w and a imply that a cannot serve either source in a valid allocation. Hence at most one direct leaf at w excludes both terminal-free and terminal-enabled placements, irrespective of second-center count and terminal quotas. This excludes the scheduled one-direct-leaf stratum and leaves the two-direct-leaf boundary and alternative embeddings open. [Proof](ORDINARY_SPINE_ONE_DIRECT_LEAF_EXTERIOR_OBSTRUCTION.md)

## D152 scoped terminal-enabled exclusions

Within the D152 profiles, size regime and D143 contract, r=1 is impossible with any second quotas. For r≥2 and max(p,q)≤2, only the parameter triple (4,2,2) admits a terminal-enabled completion. Width A=3 and Δ=2 is ruled out by the parity of the total Q quota and the difference of its two source-side counts. At A=5 only the balanced small-quota setting can reach the gap constraints. The checked A=5, Δ=2 boundary gives the single exception. D149's terminal-free exclusion and other embedding scopes are unchanged. [Proof](ORDINARY_SPINE_TWO_DIRECT_LEAF_BOUNDARY.md)

## D153 two-first-center odd-class obstruction

For ordered (2r+1,2t), (2p,2q,0) with independently prescribed exact r,t,p,q≥1, both original fresh graph classes have odd cardinality. The total extension size is even, and the exact D143 interface still requires each class to be even. Thus every terminal-enabled or terminal-free D143 completion is excluded in the stated size and prefix regime. D151 also gives a distinct symbolic control where both parities and the aggregate crossing counts pass, while the actual gap assignment fails. The claim stays within D143 and preserves all previous obstruction and supplier scopes. [Proof](ORDINARY_SPINE_TWO_SECTION_TOPOLOGICAL_PARITY.md)

## D154 finite universal feasibility and matched separation

**INDEPENDENTLY AUDITED / PENDING DIRECTOR REVIEW.** The frozen universal E hypothesis is falsified by targets 0001–0004, with (r,t,p)=(1,1,1) and q=1 through 4. Both traversals completed each negative under the frozen D143 assumptions on the retained prefix. The finite existential E-only hypothesis is also falsified by the full matched table of 252 YES/YES and four NO/NO outcomes. These exact finite exclusions leave other parameter values, independently supplied prefixes outside the experiment, other embeddings and ordinary gracefulness open. [Official evidence](../evidence/runs/d154-parity-two-first-center-001/README.md)

## D155 exact exceptional two-first-center obstruction

**PROVED / PENDING DIRECTOR REVIEW.** For (2,2), (2,2q+1,0), every permitted D143 exterior and gap assignment fails for exact q≥1 on the supplied D134 p=1 interface with n≥2(q+7). The two terminal-free widths force a three-source collision. The reduced classifications for exteriors with terminals fail separate gap range, collision or displacement requirements. The four accepted D154 negatives retain their finite computational basis. Other embeddings and ordinary gracefulness remain open. [D155 proof](ORDINARY_SPINE_TWO_FIRST_CENTER_PARAMETERIZED_CLASSIFICATION.md)

## D156 (1,1) first-profile obstruction in D143

**PROVED / PENDING DIRECTOR REVIEW.** With ordered profiles (1,1), (2p,2q+1,0) and exact p,q≥1, the supplied D134 p=1 state and n≥2(p+q+5), no D143 exterior and gap allocation completes either arm. D153 and D147 force terminal-free A=B=3. The mandatory lower sources fix the lower images and displacement parity fixes the upper roles. Every use of the even upper center increases the image sum over the required reflection, contradicting its positive quota. Ordinary gracefulness under other placements remains outside the claim. [D156 proof](ORDINARY_SPINE_ODD_FIRST_CENTER_PARAMETERIZED_CLASSIFICATION.md#4-complete-obstruction-at-rt0)

## D157 fixed-phase restriction under a connected crossing exterior

**PROVED / PENDING DIRECTOR REVIEW.** Fix ε∈{0,−1}. With the declared membership-preserving placement, connected crossing exterior containing all positive centers, and leaf-only gap, an S_ε to S_ε transition forces x+y=s−K and both fresh graph classes even. A fixed one-extra-weight state therefore still excludes the odd classes on the selected family within these premises. The alternating construction changes the crossing count at each step and leaves other relaxed placements outside this restriction. [Proof](ORDINARY_SPINE_ALTERNATING_EXCEPTIONAL_SPECTRUM.md)

## D158 scoped first-upper-source obstruction

**PROVED / PENDING DIRECTOR REVIEW.** In the declared connected crossing exterior and leaf gap for S₋₁→S₋₁, the first upper coordinate k cannot use a lower host and requires an eligible upper index b≤B−2. At B=3 this permits only the actual u pinned at b=1. Thus the D155 A=B=3 exterior fails to return S₋₁ on the stated profiles, where u has no direct gap leaf. The wider supplied A=3,B=4 construction has its own positive domain. Other relaxed placements remain outside the obstruction. [D158 proof](ORDINARY_SPINE_EXCEPTIONAL_PHASE_PRESERVING_BRIDGE.md#2-first-physically-upper-source)

## D159 fixed exceptional exterior with unit first half-quotas

**SCOPED OBSTRUCTION / PENDING DIRECTOR REVIEW.** On the retained D158 A=3,B=4 exterior for (2r,2t), (2p,2q+1,0), the first four lower gap sources require the host b. If r=t=1, the physical quota at b is two, which excludes all allocations on that exterior. Both polarities are covered by conjugation. Other exceptional-phase placements remain outside this obstruction. The open right completion supplies T=2,q=1. [D159 proof](ORDINARY_SPINE_EXCEPTIONAL_BOUNDARY_STATE_ALLOCATION.md) · [Evidence](../evidence/validation/LCL_ORDINARY_SPINE_EXCEPTIONAL_BOUNDARY_STATE_ALLOCATION_001/README.md)

## D160 terminal-free exterior beyond the four-leaf first host

**SCOPED OBSTRUCTION / PENDING DIRECTOR REVIEW.** On the declared fixed S₋₁ connected crossing exterior with all three first centers, two second centers, no first direct leaf and one second direct leaf, all first quotas at most three exclude every terminal-free exterior. Putting the direct leaf in the gap leaves B=3 without a physically eligible host for the first upper gap source. Putting it exterior gives A=B=4 and forces sources 0 through 3 at the first center with reduced label three, irrespective of role order. The separate width-independent low-destination induction forces four gap leaves at an actual first center for every terminal-enabled exterior in this arrangement as well. This excludes both classes on the parity-compatible (2,2,2),(2,2,0) control. The fixed paired-terminal exterior forces five Z leaves. Other placement classes remain outside the obstruction. [D160 proof](ORDINARY_SPINE_EXCEPTIONAL_FIVE_HOST_EXTERIOR_SUPPLY.md) · [Evidence](../evidence/validation/LCL_ORDINARY_SPINE_EXCEPTIONAL_FIVE_HOST_EXTERIOR_SUPPLY_001/README.md)

## D161 scoped gap-compatibility exclusions

The fixed S₋₁ placement on the unique-quota-four topology cannot complete at T₂=2, and cannot complete with exterior terminals at T₂=4. These follow from physical crossing counts and reduced terminal balance even though both raw exterior classes exist. The fixed D160 paired-terminal exterior needs at least five gap terminals at its neutral host and is incompatible throughout the frozen corpus. The sufficient D160 terminal-free words also fall outside this corpus. General terminal-free feasibility remains an exact decision question where the frozen symbolic gates leave it open. These are placement-specific qualifications, not numerical study outcomes or unrestricted nongracefulness. [D161 contract](exceptional_quota_four_001/CONTRACT.md) · [Evidence](../evidence/validation/LCL_ORDINARY_SPINE_EXCEPTIONAL_FIVE_HOST_QUOTA_FOUR_MATCHED_001_PREP/README.md)

## D161 restricted terminal-free failures despite terminal-enabled supply

For the 33 frozen E+ YES / T NO originals, terminal-free feasibility fails in the declared connected crossing exterior and leaf-only gap with exact S₋₁ return. The numerical T negatives are backed by the separate exhaustive audit and each had qualified exterior representatives. Their verified E+ companions certify feasibility with actual exterior terminals under the same placement and supplied prefix. There were 18 originals negative in both arms. Every original has raw exterior shapes in both arms under the raw scope. These are finite compatibility dispositions with no unrestricted nongracefulness conclusion. [D161 closeout](../evidence/runs/d161-exceptional-quota-four-001/README.md) · [Raw and derived identities](../evidence/runs/d161-exceptional-quota-four-001/MANIFEST.json)

## D162 exact terminal-free obstruction in the small-odd selected family

**PROVED / PENDING DIRECTOR REVIEW.** With first quotas 4,2r+1,2t+1 and second quotas 2,4 plus the real direct leaf under the D157 fixed S₋₁ placement, terminal-free placement of that leaf in the gap is excluded at B=3. With it exterior, permutation-moment parity places quota four at the unit translation and forces an odd neutral quota of at least five. Thus when both odd quotas are at most three all terminal-free exteriors fail. The E+ supplier settles feasibility with exterior terminals. Excluding terminal-free arrangements even when an odd quota is at least five would be false, by the three constructive T cases. These are exact placement-specific statements. [D162 proof](ORDINARY_SPINE_EXCEPTIONAL_ODD_FIRST_QUOTA_CLASSIFICATION.md) · [Evidence](../evidence/validation/LCL_ORDINARY_SPINE_EXCEPTIONAL_ODD_FIRST_QUOTA_CLASSIFICATION_001/README.md)

## D163 fixed exterior quota obstruction and transported four/four negatives

**PROVED / PENDING DIRECTOR REVIEW.** On the fixed A=5,B=4 E+ exterior when r=t=0 and p≥2, forced early and late Q uses exhaust its capacity. The required p−1 lower-source crossings would all need P with only p−2 eligible lower positions. This excludes that fixed exterior. The three D161 both-arm negatives at p=2,r=t=0 are accepted finite exhaustion and transfer across the admitted named copies, prefixes and polarities by exact normalization. This is evidence plus symbolic transport for p=2. It does not establish an all-exterior E+ obstruction for p≥3 or unrestricted nongracefulness. The all-terminal-free parity necessity continues to exclude max(r,t)<2 at every p. [D163 proof](ORDINARY_SPINE_EXCEPTIONAL_EVEN_SECOND_QUOTA_EXTENSION.md) · [Evidence](../evidence/validation/LCL_ORDINARY_SPINE_EXCEPTIONAL_EVEN_SECOND_QUOTA_EXTENSION_001/README.md)

## D164 — Raw exterior supply and compatible gap supply

The raw width-(6,4) paired-terminal example exists at K≥10 but its upper-index-two vertex is an actual terminal. It cannot take the forced fifth image in the frozen first-quota-at-most-four domain. This failure is specific to that exterior. Raw T at B=3 is likewise incompatible by the first physically upper source restriction in the declared arrangement. All-first-quotas-at-most-three profiles and T₂=3 are excluded from compatible completion. T₂=5 excludes compatible E+ through the width bound and terminal balance. Raw E+ absence is separately classified at K<10. Neither symbolic qualification nor rejection of a supplied exterior decides the unresolved matched hypothesis. [Proof](exceptional_four_first_001/CONTRACT.md)

## D164 — Official cap and bounded E+ exhaustion

The 1,000,000 per-candidate retained-state ceiling prevented the first official pass from completing the frozen diagnostic. At T of target-0429 (1,3,4,4),(5,6,0) the worker emitted `LIMIT: retained per-candidate state ceiling`. No disposition exists for either arm of that original. Zero separations in the completed prefix does not settle the finite separation hypothesis.

Eight completed E+ arms exhaust incompatible gaps across 66 qualified representatives apiece. Both independent traversals agree by physical stratum. Those frozen original-specific negatives have T positives and concern the declared exceptional arrangement. No negative was newly counted from raw-present exteriors merely rejected by the necessary gap gate. [Reconciled categories](../evidence/runs/d164-exceptional-four-first-001/RECONCILIATION.json)

## D165 — Fixed-exterior obstructions and their scopes

The fixed width-(6,4) exterior cannot use the quota-two first center at reduced label 3. The permutation moment has odd parity. With p=1 and k=6, identity at Q forces paired equal lower-host shifts because the two L reservations have opposite parity. The available multiset (1,3,3,5) cannot split into such pairs. For k≥7 the same-parity pair of L reservations yields an explicit completion. Endpoint bounds exclude q<3 for even p and q<4 for odd p on this exterior.

Failure of that fixed exterior alone supplies no full E+ negative. Across all declared exteriors the R<7 obstruction instead follows by positive terminal balance and the fresh graph counts. At {1,6} the full-class negative uses accepted finite exhaustion via exact prefix and named-role transport. The D164 interruption supplies no further negative. [Proof](ORDINARY_SPINE_EXCEPTIONAL_FOUR_FIRST_CENTER_PARITY_CHAIN.md)

## D166 — Endpoint capacity and parity-path barriers

On the stated fixed width-(6,4) exterior, mandatory H₄ and H_(k+5) sources require Q. At q=2 they exhaust Q and the next upper boundary source consumes the unique direct leaf at w. H_(k+3) then has no destination. This excludes q<3 for every compatible first-role selection on the fixed exterior. It yields no such ordered obstruction for alternative E+ exteriors.

Moments and sorted endpoints alone do not guarantee residual compatibility. A common source/destination hole forces both adjacent shift indicators to zero and bars a repair from crossing it. The four constructive patterns prove exact residual feasibility with all common holes retained as absent cells. [Proof](ORDINARY_SPINE_EXCEPTIONAL_FOUR_FIRST_CENTER_EIGHT_DEFECT.md)

## D167 — Residual path barriers and scoped capacity constraints

Aggregate moments, parity counts and favorable endpoint ordering after common-hole cancellation do not suffice. In the abstract even path [4,14], source holes {4,8} and destination holes {8,10} prescribe a shift at missing source 8. The exact zero boundary at that common hole obstructs the repair. This is an abstract path control.

A universal q≥3 bound is not used for residual-neutral cases. The proved right-end obstruction gives q≥2 for every admitted inventory, and q=2 forces α_Z≥6 by two more neutral assignments at the left end. This retains the exhausted-neutral D166 obstruction. Failure of the type criterion excludes only this geometry on the stated original and arrangement. [Proof](ORDINARY_SPINE_EXCEPTIONAL_RESERVATION_SEMILINEAR.md)

## D168 — Unequal row intervals and exact capacity barriers

Equal source and destination baseline intervals cannot be assumed in either folded direction. In the general geometry both directional prefix-count identities need `−ℓ` because the upper rows begin at `ℓ` and the lower rows begin at zero. Dropping this term gives an incorrect flow count even when the two counts still agree. Index moments alone omit per-residue endpoints and capacity barriers. The saved abstract common-hole obstruction transports by changing the step size to `ρ`, with no new original infeasibility claim. Auxiliary bases must retain legal zero upper counts and apply the original topology and full positivity at the requested pair. The available periods are determined by each marked type, and the saved separation-one T reservation at target-0428 has none. [Proof](ORDINARY_SPINE_EXCEPTIONAL_TWO_UPPER_HOST_RESIDUE_COMPRESSION.md)

## D169 — A fixed role obstruction cannot exclude the role menu

D163's fixed-exterior obstruction for r=t=0,p≥2 exhausts Q when it has four gap leaves. At p≥3 the successful D169 role exchange gives Q 2p leaves and assigns three P gap leaves using fixed residue repairs. The complete named original is unchanged. At p=2 the particular new construction would require the absent H_6 crossing image. The full E+ exclusion there continues to use the accepted D161 exhaustion and D163 transport. [Proof and control scopes](ORDINARY_SPINE_EXCEPTIONAL_SECOND_ROLE_EXCHANGE.md)

## D170 — No template miss among completed D164 E+ positives

The proposed matched template-miss condition is excluded on the selected 108 completed E+ positive originals. Each actual saved compatible labeling uses the specified width-(6,4) role menu. Retained-record reconciliation resolves the selected finite question before any new numerical run. The original D164 separation hypothesis remains UNDECIDED under its historical execution cap. Cases outside the selected positive records and alternate exterior geometries are outside this coverage conclusion. [D170 proof](ORDINARY_SPINE_EXCEPTIONAL_ROLE_MENU_COVERAGE.md)

## D171 — Ordered Q bottleneck and limits of P-growth transport

A fixed ordered assignment with q≤2 cannot supply either additional first inventory on the width-(6,4) menu. The right end requires two Q leaves. At exactly two, the minimum P image forces six neutral leaves, exceeding the available first maximum four. The full E+ exclusion for odd R<7 uses the terminal-balance count. A one-column P-growth step can exchange the parity pairing, so it does not assert persistence of all old residual arrows. D167's protected two-column interval insertion yields the (4,0) rate when its long-gap premise holds. No historical D164 arm disposition is changed. [D171 proof](ORDINARY_SPINE_EXCEPTIONAL_P_GROWTH.md)

## D172 — Symbolic menu exclusion for all-even first inventories

For the specified width-(6,4) exchange menu the gap translation moment forces the sum of the full quotas at numerical roles b and c₁ to be odd. The upper reflections contribute an even total modulo two since exactly R−1 gap leaves use upper parents. This excludes the complete M menu on the 180 frozen all-even originals for every physical role assignment. The obstruction concerns M. The alternative E+ feasibility and the finite separation hypothesis remain undecided. [Menu moment](exceptional_alternate_exterior_001/CONTRACT.md#3-menu-moment)

## D172 official execution — Scoped role-menu coverage counterexample

The complete M role menu fails to cover every A-admitting original in the selected finite domain. Target-0780 has independently verified A YES and full symbolic M NO on the identical original and prefix. Its wider exterior and direct-leaf placement preserve the exact D157 return. D170's complete coverage on its 108 different retained positives still holds. Target-0777 is A NO within the declared complementary arm and frozen admission. [Official evidence](../evidence/runs/d172-exceptional-alternate-exterior-001/README.md)

## D173 — Pure-P internal growth is structurally excluded

For the stated width-(6,5) geometry and lower inventory, three active residues would force the two lower endpoint sets to have one index of each residue. The two different far-row endpoints agree modulo three, forcing the upper reservation endpoint distributions to match as well. This would make total displacement divisible by three, contrary to 13. Thus no reservation type carries a (6,0) generator, and fixed q cannot support unbounded p through this geometry. The (0,6) and (4,2) realizations and the exact domain beyond the ray remain open. The saved target-0777 full A negative retains its separate independent-exhaustion basis. [Symbolic proof](ORDINARY_SPINE_EXCEPTIONAL_ALTERNATE_EXTERIOR_RESIDUE_GROWTH.md)

## D174 — Candidate parity rejection has no arm-level implication

The new five-first-center moment forces the weighted sum of full quotas at first labels and second upper indices to equal A+B modulo two. On the 186 all-even originals this excludes the one-exchange H0 width total eleven. The corresponding H1 total twelve passes the parity gate. The two raw suppliers exist independently of this gate, and all alternative selections and widths remain subject to exact qualification and gap feasibility. The restriction does not exclude a complete arm or decide the finite separation hypothesis. [Qualification](exceptional_five_first_direct_001/CONTRACT.md#3-general-candidate-parity-moment)

## D174 official execution — Scoped direct-leaf-in-gap coverage counterexample

The terminal-enabled direct-leaf-in-gap class fails to cover all originals admitting a terminal-enabled direct-leaf-exterior return in the frozen population. On D174 target-0991, both traversals found zero qualified H0 exteriors across the admitted domain, even though a raw H0 exterior exists. Independently reconstructed H1 YES on the identical original and prefix witnesses the failure of coverage. The H0 negative uses the exhaustive audit of qualified exteriors across the allowed selections, beyond the parity gate's candidate-level scope. The remaining 3,518 originals were unentered. [Execution evidence](../evidence/runs/d174-exceptional-five-first-direct-001/README.md)

## D175 — Complete H0 exclusion in the selected odd-center domain

With odd r≥3 and second total r+3, the graph count and terminal balance force A=r+2 and one selected second terminal. Image four reserves upper index two for a second center. In H0 the restoration of the displaced reduced difference forces the selected lower terminal to label one and the sole selected first terminal to a parent at label three. Thus B=4 and the residual first contribution is odd while direct and upper host terms are even. H0 is raw-exterior positive even at r=3. This scoped exclusion applies symbolically to the 93 D174 all-even R=8 originals. Their saved historical dispositions remain distinct, with 92 unentered within that subset. [D175 proof](ORDINARY_SPINE_EXCEPTIONAL_ODD_FIRST_CENTER_DIRECT_PLACEMENT.md)

## D176 — One-four boundary exclusion and limits of the H1 menu

At r=3 and exactly one four, the forced neutral at reduced slot four excludes I-b and all II geometries. I-a requires its sole H image at index four from H₅ at shift one or H₆ at shift two. The first choice leaves L₅ without an upper source. The second leaves H₅ with both its upper images occupied. This excludes both upper numerical role choices and the full H1 class on that one-four boundary within the declared D157 arrangement. Raw I-a exterior supply survives. A raw menu entry elsewhere does not decide the separate gap-allocation question. [D176 proof](ORDINARY_SPINE_EXCEPTIONAL_ODD_FIRST_CENTER_H1_MENU.md)

## D177 — Direct prepend at special deficit two

The untranslated special tails have a common H-source and L-image hole at offset −4. Simply shifting the old core right by one and prepending a paired use of deficit two puts both the translated common hole and the new pair at column −3. This invalidates that direct prepend rule for I-a and II-a. Revised explicit tail cores supply the same promotion via different reservations and preserve the required P and Q capacities. The collision pertains to this insertion rule. [D177 proof](ORDINARY_SPINE_EXCEPTIONAL_ODD_FIRST_CENTER_QUOTA_EXPANSION.md#3-special-tail-patterns-for-every-remaining-quota-multiplicity)

## D178 — Preassigned II-a separated-tail limitation

Arbitrary even magnitudes do not give universal support at fixed deficit roles in the separated II-a tail. Its one P shift is forced at the last L image, so no first-host L reservation can reach the last position of its own row. Every cutoff in that row must be passed by a positive deficit. Counting these cutoffs and the total deficit moment gives u₀≤4+u₂+2u₃+3u₄ for the full tail quotas 2+2u_d. In particular u₀≥5 with all other u_d zero fails in this preassigned architecture. The exact ordered support has a finite weighted column language. The selectable construction supplies the requested original domain. [D178 proof](ORDINARY_SPINE_EXCEPTIONAL_ARBITRARY_EVEN_FIRST_QUOTA_LIFT.md#5-fixed-order-tail-scope-and-an-exact-state-criterion)

## D179 — Below-threshold terminal-enabled H1 exclusion and growth limits

The actual fresh lower graph class has size 1+r+R=2(A+x), and terminal balance forces at least one selected second terminal, hence A≥r+2. Thus R<r+3 excludes compatible terminal-enabled H1 within the declared same-phase placement. The argument does not use neutral exhaustion. The particular reversed I-a baseline rule at r=7 needs three regular shifts while only two are available. At r=5 with exactly one four and the other first quotas two, the D178 I-a baseline starts with a shift-four anchor, so the stated one-anchor strip cannot cover the larger second targets there. These last two limits concern the displayed constructions. [D179 proof](ORDINARY_SPINE_EXCEPTIONAL_INDEPENDENT_SECOND_QUOTA_GROWTH.md)

## D180 — Folded parity restriction for II-a and I-b

In the two specified width-five II-a and I-b geometries the folded image-minus-source index sum equals r+2, which is odd. The single first selection removes a terminal at shift r−3, which is even. Separation three therefore forces p−1 odd at the selected second parent P, so its actual full quota is even. This excludes odd p in those exact geometries and their expanded gap sizes. I-a has odd first selection shift and even separation, and the explicit two-shift tail supplies odd quotas there. These are geometry-scoped conclusions. [D180 proof](ORDINARY_SPINE_EXCEPTIONAL_ODD_SECOND_QUOTA_SUPPLIER.md#2-exact-width-five-rows-and-folded-parity-moment)

## D181 — H1 graph threshold and I-a mixed parity qualification

In the declared terminal-enabled H1 arrangement a compatible exterior forces R≥r+3 by independent graph counts and terminal balance, also with the stated mixed first quotas. The fixed I-a geometry further requires the sum of the full first quotas weighted by their actual numerical lower shifts to be even. A role assignment failing that moment cannot complete I-a. Mixed packets pair odd capacities at same-parity shifts and supply the exact row bijection. The moment alone is only a necessary qualification and the graph threshold concerns the declared terminal-enabled class. [D181 proof](ORDINARY_SPINE_EXCEPTIONAL_MIXED_FIRST_QUOTA_PARITY.md#1-exact-topology-and-necessary-threshold)

## D182 — Terminal-enabled graph threshold and scoped II-a moment

For the declared H1 arrangement, R<r+3 remains infeasible even when odd first quotas may be one. This follows from the graph-color counts and terminal balance, independently of h. On the selected II-a assignments with even full displacement moment, odd full quota at P fails the index parity moment. I-a does not have this parity restriction on its selected roles. An unsuccessful role assignment does not exclude another assignment or another exterior. [D182 proof](ORDINARY_SPINE_EXCEPTIONAL_PARITY_NEUTRAL_PACKETS.md)

## D183 — Necessary threshold and same-phase graph parity for multiple second centers

For the declared terminal-enabled H1 arrangement, R<r+3 excludes completion for the multiple-second-center topology by terminal balance and the fresh lower graph-class count. Both fresh graph-class sizes must be even. In the supplied exterior the folded moment is A(ν−1) and gives the stated necessary condition on numerical roles. The Q reservoir inequality describes the positive construction and gives no general H1 obstruction. [D183 proof](ORDINARY_SPINE_EXCEPTIONAL_UNBOUNDED_MULTI_UPPER_HOST.md)

## D184 — Partial-bank residue obstruction

After restoring a bank of width 1≤T<ρ, the two free intervals of length λ have equal index-residue counts modulo ρ only when ρ divides λ. Q identities and the single separation-ρ host preserve residue classes, so these intervals cannot be matched by those two hosts at any other positive λ. The obstruction concerns this specific free-set matching. At T=ρ arbitrary λ is supplied by pure growth. [D184 proof](ORDINARY_SPINE_EXCEPTIONAL_NEUTRAL_ANCHOR_BANK_GROWTH.md)

## D185 — Matching, local capacity and per-role parity restrictions

The redistribution tile requires disjoint adjacent pairs of eligible ordinary roles and at least 2k leaves at each of the two actual hosts, with 2k an available separation. Odd tile multiplicity at an individual separation gives the wrong baseline parity for the specified target when followed by even-only bank growth. An even total M alone cannot ensure each shifted parity. These restrictions apply to this supplier. The Q=7 control lies outside D184's sufficient domain and is supplied by D185. [D185 proof](ORDINARY_SPINE_EXCEPTIONAL_BASELINE_QUOTA_REDISTRIBUTION.md)

## D186 — Local matching and parity limits of the defined supplier

At fixed imbalances a local matching using the retained upper hosts requires every H-to-L gap difference to be an available separation in {0,2,…,ν}. A difference of one or a negative difference is unavailable. Subsequent even bank growth preserves the manufactured baseline parity at each actual second host. The earlier D185 fixed parities suffice in its construction, while all-even second quotas and four odd second quotas are supplied in D186. These comparisons concern this arrangement and the fixed local model. [D186 proof](ORDINARY_SPINE_EXCEPTIONAL_CUMULATIVE_IMBALANCE_ALLOCATION.md)

## D187 — Necessary graph parities in the stated same-phase arrangement

The fresh graph-class sizes 1+r+R and ν+2+F must both be even under the declared crossing-exterior and leaf-only-gap placement. Therefore R≡r+1 and F≡ν modulo two are necessary. These conditions apply to the named same-phase arrangement. The former odd-r and even-ν restrictions can be removed in the proved supplier by the unified tail. General H1 feasibility retains its own scope. [D187 proof](ORDINARY_SPINE_EXCEPTIONAL_PARITY_UNIFIED_MULTI_HOST.md)

## D188 — Host availability and same-phase restrictions with exterior direct leaves

A direct-leaf slot supplies no residual terminal arrows. A missing upper host is unavailable in the local gap matching even if the corresponding reduced exterior slot exists. If the eligible quota list is entirely zero, its local gap sets coincide and their index moment precludes any positive-separation match. The same-phase graph classes force R≡r*+1 and F≡ω modulo two, with R≥r*+3 for terminal-enabled placements having all first direct leaves exterior. These conditions apply to the stated models. [D188 proof](ORDINARY_SPINE_EXCEPTIONAL_DIRECT_LEAF_SLOT_CONSTRUCTION.md)

## D189 — Capacity and matching failures in the whole-section model

The prescribed neutral allocation and whole-section split require a nonnegative remaining H length. For (6,1,0),(5,1,0,0), the parity and s=K geometry hold, but F=7<α_N+ω=9 and H* is −1. At fixed splits in the width-four and width-two controls, ordered gap matching requires the unavailable separation one, while explicit nonidentity permutations give legal completions. At t=0 the proved growth adds only even quota at Q, keeping shifted quotas fixed. These are model-specific conclusions. [D189 proof](ORDINARY_SPINE_EXCEPTIONAL_WHOLE_SECTION_MONOTONE_ALLOCATION.md)

## D190 — Forced neutral guard and single-second-center limit

For any gap allocation on the fixed movable exterior, the first γ numeric images force identities at the actual neutral role. If s≤γ, making the entire gap neutral leaves no place for the second residual terminals. The specified adverse control has 17 fresh edges and violates the same-phase graph parity. The additional parity-clean (3,2,0),(5,1) control fits the full size and parity but still lacks four residual neutral terminals. In the ν=1 monotone model equal gap sets require B=γ and a balanced split; z₂<2 precludes this geometry for matching. These conclusions have their fixed-exterior and monotone scopes, respectively. [D190 proof](ORDINARY_SPINE_EXCEPTIONAL_MOVABLE_TERMINAL_EXCHANGE.md)

## D191 — Broad exceptional guard and strict boundary obstruction

For the declared S₋₁ same-phase arrangement with all actual direct leaves and positive centers exterior, the first four numeric images force four residual neutral terminals regardless of selected-terminal counts. A shorter gap cannot accommodate the positive second residual demand. This excludes the 144 low main originals in that phase context. The two actual strict boundary originals with second inventory (5,1) fail the reduced edge-moment cases and exact residual capacity conditions. The original D190 17-edge parity failure remains separate. These restrictions have their proved placement scopes. [D191 proof](ORDINARY_SPINE_LOW_CAPACITY_STRICT_PHASE_MATCHED.md)

## D192 — Baseline endpoints and anchor supply in the prescribed construction

In the prescribed even-quota movable-defect lists, the low interval gives q≥2h+2 and the companion interval gives q≥2h. There are exactly p/2−1 complete Q exchange pairs in their common interval. Thus p=2 supplies none and p=4 supplies one. The proved two-sign growth uses two disjoint Q pairs. These bounds describe the stated allocation and express no infeasibility for other signed allocations or exteriors. [D192 proof](ORDINARY_SPINE_STRICT_SIGNED_INDEPENDENT_GROWTH.md)

## D193 — Fixed-exterior baseline and parity restrictions

At separation one the folded moment requires even actual Q and P quotas for every successful allocation on that particular exterior. At separation two the forced baseline chains require p≥q+2 and the exact P parity of the arm. Both equal odd h=2 low controls (3,3) and (5,5) fail those exact baseline conditions in either role order. The common Q pairs are exactly the stated initial interval; the proved unequal-growth operation uses one pair. These conclusions leave other strict exteriors and other allocations beyond the stated scopes open. [D193 proof](ORDINARY_SPINE_STRICT_RESIDUE_TWO_ANCHOR_ECONOMY.md)

## D194 — Fixed outbound obstructions and phase-threshold corrections

In the specified signed S₀→S₋₁ exterior, even upper separation is impossible for any compatible first quota by the folded moment. At the separate equal-child-count baseline with F=2h+1 and one selected terminal per side, the forced initial transpositions exhaust the first gap quota. The two remaining matching directions then each have identical source and image sets, forcing Q only and excluding any positive residual P on that exterior. D157's threshold corrects the proposed crossing starts in E reverse, E outbound and H final to 51, 60 and 77, with the original cuts and sizes retained. These are phase- and placement-specific statements. [D194 proof](ORDINARY_SPINE_BIDIRECTIONAL_PHASE_TOGGLE_SUPPLIER.md)

## D195 — Exact excluded seed and empty-block cases

At the prescribed extreme frontier with the D157 cut, an original star with zero positive centers has crossing differences [c,n], excluding both phases for c≥1. A sole positive center with zero direct leaves cannot initialize either phase, by the forced reflection and the exact terminal quota maximum. For the declared two-empty-section geometry A=B=1 and s=0, the exceptional-to-strict direction requires T=2 and violates the old-crossing threshold. These obstructions concern the stated states and geometries. The prefix-size premise remains in D143's broader forcing results, including the gap-center exclusion. [D195 proof](ORDINARY_SPINE_SIZE_INDEPENDENT_LIFT_AND_ORIGINAL_SEED.md)

## D196 — Scoped packet, phase and odd-run obstructions

A zero global signed moment alone leaves a band-packing condition. For the strict-to-strict profile (3,0,3), every balanced indexed role assignment places the quota-three hosts at opposed unit shifts and the direct leaf at the neutral slot. Its two bands have odd lengths 5 and 1 and no neutral terminal. Hence it fails the exact declared return. The matched positive (2,2,2) fills both bands. For positive terminal total the all-lower-host placement requires 1≤D−c≤a. An odd terminal-free run from a D196 one-center seed gives D−c≤−1, excluding a positive-terminal next step in that placement. The equal-size frozen odd control has P(15,10,8) and only positive shifts. Alternative placements and general gracefulness remain open. [D196 proof](ORDINARY_SPINE_GENERALIZED_ONE_SECTION_CUT_SPECTRUM.md)

## D197 — Exact odd-run continuation obstructions

The fixed old odd-prefix labeling cannot extend to strict P(30,14,16) under the declared increasing two-translation placement, for any proper split, nonnegative widths, either extreme frontier or allowed actual fresh placements. The preserved-membership case fails by exterior forest and crossing counts. The relaxed case fails by old-band compatibility, reserved endpoints and final crossing-weight moments. This also settles D196's original fixed-cut membership-preserving comparison. The eight-edge control changes membership successfully on its different exact original. Other prefix labelings, embedding classes and unrestricted gracefulness remain open. [D197 proof](ORDINARY_SPINE_ODD_RUN_CUT_REPARTITION.md)

## D198 — Scope of single-gap exclusion and output nesting

The accepted D197 negative is exact for its two-translation class. D198's three-gap witness on the same frozen input establishes that this exclusion cannot extend to arbitrary increasing embeddings. A valid monotone continuation need not preserve all-cut nesting: the completed 11-edge control has incomparable actual cut intervals of weights one and two. All-cut output nesting requires the merged chain on both old and fresh incidences. The original fixed-minimum-order w=0 branch remains unclassified by the w=30 witness. [D198 proof](ORDINARY_SPINE_NESTED_CUT_RANK_INTERLEAVING.md)

## D199 — Scoped unsafe support and fixed-template moment failure

At any unsafe cut a unit insertion repeats a pair of adjacent original weights. Coordinated unsafe insertions can preserve order, and collision-free vectors can change order. The Family C controls give both distinctions. At n=8 with receiving quotas (1,1,0,1), all three old cuts are admitted but the exact fixed-template residual moment is 1 instead of the required 4. This original remains eligible for other placements. The three-gap output has unsafe minimum cuts 3 and 4 and even size, so the identical D199 template cannot immediately reapply. [D199 proof](ORDINARY_SPINE_PARTIAL_SAFE_CUT_THREE_GAP_CHAIN.md)
