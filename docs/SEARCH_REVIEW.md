# Independent review of exact engines and boundary states

## Scope and result

This review covers `search.py`, `dp.py`, `states.py`, and `budget.py`, with graph-admission comparisons against the independent verifier. The reviewer did not edit those implementation files. Findings were returned to their owners; the regression tests below pass after their corrections. This is a source review and finite implementation check, not a formal proof of the Python programs or the lobster conjecture.

The inspected DFS and frontier DP preserve all named graceful assignments in their declared scope. Their default scope has no root pin, alpha-labeling requirement, complement reduction, or automorphism quotient. Explicit pins and domains change the scope and remain recorded in their results. Both engines validate the actual original graph before enumeration. A nonlobster, invalid spine, unsupported supplied schema version, or malformed explicit role metadata is rejected.

## Why the DFS checks are sufficient

Each recursive step assigns one currently unassigned physical vertex a previously unused label in `0..m`. For every edge from that vertex to an already assigned neighbor, it checks the difference against both the earlier difference mask and other differences introduced in the same step. Every original edge is introduced exactly once, when its later endpoint is assigned.

At completion, the admitted tree has `n=m+1` vertices. Its distinct vertex labels in `0..m` therefore exhaust that alphabet. Its `m` distinct positive differences in `1..m` exhaust that alphabet too. These are exactly the finite graceful-labeling conditions. The minimum-remaining-values heuristic chooses which vertex to visit next, with deterministic tie breaking; it does not discard any currently legal label. Any valid full assignment determines one unique recursive route through these choices.

The public first-witness mode may return `SAT` with `exhausted=false` and `count=null`: it has established existence without establishing a total count. Counting mode reports an exact integer only after exhaustive completion. A witness found before an interruption remains available, but an interrupted counting run remains `INCOMPLETE`.

## Why the DP state contains enough information

Fix the input vertex order and one completed layer. Let `A` be its assigned vertices, and let the live frontier `F` be the vertices of `A` incident to any future vertex. The implementation retains:

1. The exact set `U` of used labels, represented by a bit mask.
2. The exact set `D` of used differences, represented by a separate bit mask.
3. The label on every named live frontier vertex, in the layer's fixed frontier order.

The layer itself determines which physical vertices are assigned, so it need not be repeated in every dictionary key. A forgotten vertex has no future incident edge. Consequently, every future edge that touches an assigned vertex touches the retained frontier. `U` determines which labels remain available, `D` determines which differences remain available, and the frontier labels determine the future differences touching the assigned part. Future vertex domains are fixed external inputs.

Two histories with the same full state therefore accept exactly the same future assignments. The DP can add their multiplicities without losing named counts. Retaining one representative history for reconstruction is sufficient because that representative has the same resources and frontier; multiplicity is stored separately and is never replaced by one. New differences are checked against one another as well as against the prior mask. At the final layer, all vertices and edges have been processed, giving the same complete-spectrum argument as the DFS.

This is an argument for the mathematical state description and its inspected transitions. It does not claim that a constant-size state exists. The inventories retain global information and can cause exponential state growth.

### Each state component matters

On the six-vertex path, assign the first three vertices the following triples. Direct enumeration of the remaining three labels gives these continuation counts:

| Component omitted | First prefix | Its completions | Second prefix | Its completions | Components that agree |
|---|---|---:|---|---:|---|
| Used differences | `(0,2,5)` | 0 | `(2,0,5)` | 1 | Used labels `{0,2,5}` and active label `5` |
| Used labels | `(1,0,2)` | 0 | `(1,3,2)` | 1 | Used differences `{1,2}` and active label `2` |
| Live frontier label | `(0,4,1)` | 0 | `(1,4,0)` | 1 | Used labels `{0,1,4}` and differences `{3,4}` |

Every displayed partial assignment is valid. Each proposed omission would merge two histories with different continuation counts. These finite pairs are checked against the independent oracle, DFS, and DP. They justify retaining these resources in the reference engine; they do not rule out a different, carefully proved compression for a narrower family.

## Physical boundary semantics

`interval_boundary` checks a valid partial assignment with unused labels forming an integer interval of size `K`, unused differences exactly `1..K`, and an active label just outside that interval. Every assigned-to-unassigned edge must use the declared active **physical vertex**. Matching the numerical endpoint at a different vertex is insufficient.

For a valid partial assignment on a tree, these inventories also imply that the assigned subgraph is connected: with `a` assigned vertices and `K=n-a` remaining vertices, the number of used differences is `m-K=a-1`. This is the number of assigned-to-assigned edges, and an induced forest on `a` vertices with `a-1` edges is connected. This observation does not establish a supplier or a continuation theorem for every possible unassigned topology.

The B2 pilot adds a specific graph domain. It requires a canonical profile, one positive branch followed by any direct leaves at each of the first two spine sections, and empty sections from `s:2` onward. Its actual suffix is therefore a pure path with exactly the declared `K` vertices beyond `s:2`. A rewired graph, an explicit graph without the required profile, or a branched suffix is rejected. Root pins are optional and explicit; interval and root values must lie within the actual alphabet.

`extract_b2_candidate` verifies the **complete** labeling before removing suffix entries. It labels the result `solver_derived_exploratory_prefix`, records `independent_supplier=false`, and checks the boundary afterward. This finite discovery operation is not a noncircular supplier construction.

A useful finite control is the profile `[[1],[1],[],[]]`. For `K=1`, interval `[1,1]` with active label `2` has zero completions. Interval `[2,2]` with active label `3` has a verified completion:

| Vertex | Label |
|---|---:|
| `s:0` | 1 |
| `b:0:0` | 4 |
| `l:0:0:0` | 6 |
| `s:1` | 7 |
| `b:1:0` | 0 |
| `l:1:0:0` | 5 |
| `s:2` | 3 |
| `s:3` | 2 |

Deleting `s:3` leaves unused label `2` and unused difference `1`, at the physical port `s:2`. Complementing all labels by `7-x` gives the reflected below-interval case. This is finite evidence that a rigid normalized interval can miss a valid translated interface, not a theorem that translation always succeeds.

## Limits and result classification

`Limits` validates both direct construction and mapping construction. Node, vertex, and state limits are positive true integers; time limits are positive finite numbers. The starter exact engines reject a configured vertex cap above 100. Their defaults are 200,000 nodes, five seconds, 16 vertices, and 20,000 DP states per layer.

DFS counts accepted assignment extensions as nodes. DP counts attempted label transitions, including those rejected because a label was already used. These counters describe different units and should not be treated as equal work when comparing engines. `max_states` bounds distinct keys in a DP layer. Old and new dictionaries coexist while advancing a layer, and representative histories also consume memory: this is not a process-memory bound. `peak_states` records the largest layer dictionary, including an interrupted partial layer.

Time checks are cooperative. Graph admission and restriction normalization occur before the engine budget starts, and individual transition work is not forcibly preempted. No operating-system resource isolation is provided. A cap or keyboard interruption produces `INCOMPLETE`, never an exhaustive negative result. Partial final-layer DP totals are lower bounds backed by complete labelings.

Malformed graphs return `INVALID_INPUT`. Malformed restrictions and limits raise `ValueError` at the library boundary for the CLI to report. Contradictory well-formed restrictions, such as an empty domain or mutually incompatible pins and domains, can have an exact restricted count of zero. The independent direct oracle classifies repeated pinned labels as malformed input; DFS/DP can instead exhaust that contradictory scope to zero. Neither convention treats the underlying unrestricted tree as nongraceful.

## Findings corrected during review

| Finding | Correction independently regressed |
|---|---|
| Direct `Limits` objects bypassed mapping validation | Validation moved into `Limits.__post_init__`. |
| DP peak size omitted an interrupted partial layer | Peak updates occur when each new key is allocated. |
| B2 restrictions checked suffix names but not actual shape | Independent graph validation and exact canonical profile conditions added. |
| Candidate extraction discarded a bad suffix before verification | Complete original-graph certificate is checked first. |
| Explicit root pins lacked an alphabet-range check | True integer and range checks added. |
| Model and verifier differed on schema versions and explicit role objects | Model graph admission aligned with the independent checks. |
| Restriction coercion accepted unintended non-mapping inputs | Pins and domains now require mappings and give clear `ValueError`s. |

## Finite validation performed

On Linux with Python 3.12.14, the following commands passed in approximately 0.2 seconds combined:

```text
python3 -m unittest discover -s tests -p 'test_search_dp.py' -q
python3 -m unittest discover -s tests -p 'test_states.py' -q
```

There are 13 engine test methods and nine state test methods. The engine tests compare all 125 named trees on five vertices against the direct permutation oracle, plus singleton, two-vertex path, four-vertex path, six-vertex path, the six-vertex spider with legs 2,2,1, varied vertex orders, explicit restrictions, and a pinned non-alpha graceful labeling. They cover every cap, deterministic cooperative clock expiry, retained witnesses during interruption, exact named multiplicities, and actual graph admission. The state tests cover translated/reflected intervals, the wrong physical port, multiple ports, incomplete difference inventories, empty boundaries, exact B2 shape, parameter limits, and invalid full witnesses.

Supported release targets are Python 3.12 and 3.13. This review's executions used 3.12.14 on Linux; they do not establish a Python 3.13 or Windows execution result.
