# Next bounded research task: pin sweep of the unequal prefix seed

**ID:** B2-UNEQUAL-PIN-SWEEP-001. **Current status:** queued, not executed. `STATE.md` owns the live status. This task is the specific alternative port rule required by the exhausted-negative decision rule of its disposed predecessor. It does not repeat the completed four-pair control and does not widen any budget.

## Disposed predecessor: B2-UNEQUAL-SEED-001

The eight-vertex prefix `[[1],[2],[]]` with A-side `0..3` / B-side `4..7` bijective domains and pin `h(s:2)=4` **has no graceful labeling**. The proposed analytic obstruction was confirmed (independent recomputation plus a separate reviewer challenge with no unresolved objections); the declared bounded DFS (65 nodes) and the direct permutation oracle (5,040/5,040 permutations, 144 domain-admissible) both exhausted the declared scope with 0 solutions on the same original graph digest `9198e106ce33d9b83b8044e385b1599cfe26cd1fe471f4eec841a461868756b2`. This falsifies exactly that alpha/physical-port template; it is not a nongracefulness certificate for the unrestricted eight-vertex tree, for any other restriction set, or for the unequal B2 family at any K. The all-K high-side-shift transport is retained as a conditional identity only (its antecedent is false). Full record: `research/B2_UNEQUAL_SEED.md`; failure entry F-UNEQUAL-SEED; decision D015; handoff `OC-20261120-b2-unequal-seed` (PENDING_CODEX_REVIEW).

## Exact question (queued)

On the **same named eight-vertex prefix** (profile `[[1],[2],[]]`, the seven actual edges listed in `research/B2_UNEQUAL_SEED.md` section 1, same graph digest), with the **same alpha domains** (A-side `s:1, b:0:0, l:1:0:0, l:1:0:1` bijectively `0..3`; B-side `s:0, b:1:0, l:0:0:0, s:2` bijectively `4..7`), does a graceful labeling exist for the remaining physical port pins

- `h(s:2) = 5`
- `h(s:2) = 6`
- `h(s:2) = 7`

No further root pin, no complement quotient, no branch-symmetry assumption, no automorphism quotient. One specific alternative port rule per pin.

*Unverified preliminary observation, not evidence:* for each `p ∈ {5,6,7}` the port edge `s:1--s:2` has difference at least `p−3 ≥ 2` (since `h(s:1) ≤ 3`), so it cannot carry difference 1; difference 1 must instead be carried by an edge joining the B vertex labeled 4 to the A vertex labeled 3. This observation does not decide existence; the declared runs do.

## Declared bounded protocol (per pin)

At most three DFS runs, one per pin, from the project root:

```powershell
.\.venv\Scripts\python.exe -m lcl solve examples\unequal_seed.json --engine dfs --pins examples\unequal_seed_pins_p5.json --domains examples\unequal_seed_domains.json --limits configs\unequal_seed_limits.json
```

and likewise with `_p6`/`_p7`. The pin files are **new** inputs created at execution time, each exactly `{"s:2": p}`; the existing `examples/unequal_seed_pins.json` (`s:2=4`) is not modified. Domains (`examples/unequal_seed_domains.json`) and limits (`configs/unequal_seed_limits.json`: one worker, one eight-vertex target, 10,000 attempted assignments, 2.0 s cooperative, 2 MB record cap) are unchanged. No automatic enlargement.

For **each** exhaustive negative, the declared direct-permutation oracle cross-check (same pin, same domains and limits, `--engine oracle`) must complete before the obstruction is adopted: at most three additional oracle runs. If an unexpected witness appears, independently check its original seven edges and all declared restrictions against a separately supplied original target; quarantine any contradiction and resolve the discrepancy before accepting a conclusion.

## Decisions after the sweep

**Witness at some pin p:** record the seed as finite data on the original graph; have a separate role check the all-K high-side-shift transport for that pin (preliminary, unverified: the port label becomes `p+K`, which for `p ≥ 5` is still above the same unused label interval `[4,K+3]`, with unused differences `1..K`; the consumer is the original K-edge path); only then consider implementing a dedicated unequal supplier with exact domain and boundary tests. Compare the ordinary family/interface with retained R241/R246 and primary literature before any novelty statement.

**All three pins exhausted negative:** record failure of this whole alpha/port pin template on the same target. It does not show the unequal lobster or the seed tree is nongraceful. Do not expand a search range automatically; the next specific alternative (for example a different prefix-relabeling rule) becomes a new scope decision.

**Incomplete:** preserve the budget and result. Inspect why the case did not complete and decide whether an implementation issue or a different exact encoding is the next useful step. Do not reinterpret the stop as an obstruction.

Stop this task after its scoped disposition and handoff. Success means an independently supplied unequal family or a verified, useful template obstruction — not simply another solver run. Update `STATE.md`, the relevant finding/failure and proof duty, and give Will one next action.
