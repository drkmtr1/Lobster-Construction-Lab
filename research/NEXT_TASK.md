# Next bounded research task: an unequal prefix seed

**ID:** B2-UNEQUAL-SEED-001. **Current status:** queued, not executed by release validation. `STATE.md` owns the live status. This task advances beyond the proved balanced supplier; it does not repeat the completed four-pair control.

## Exact question

Take the eight-vertex, seven-edge prefix with profile `[[1],[2],[]]`. Its actual edges are the same prefix through `s:2` that would precede a K-edge path in the unequal B2 family `q=1,r=2,z0=z1=0`. This seed has no appended path: K=0 here is a fixed auxiliary target, not an input to the positive-K B2 constructor.

Its bipartition is:

- Low side A: `s:1`, `b:0:0`, `l:1:0:0`, `l:1:0:1`.
- High side B: `s:0`, `b:1:0`, `l:0:0:0`, `s:2`.

Does it have a graceful labeling using `0..3` exactly on A, `4..7` exactly on B, with the **actual leaf `s:2` labeled 4**? These alpha/port restrictions are deliberate and explicit. Files `examples/unequal_seed*.json` encode them. The existence of such a seed is not assumed.

## Why this finite seed could supply an infinite family

If such a fixed seed `g` exists, retain its low-side labels and add K to every high-side label. Every actual prefix edge crosses the two sides, so its positive difference increases by K. The prefix then uses differences `K+1..K+7` and labels `0..3` plus `K+4..K+7`. It leaves `R=[4,K+3]`, `D=[1,K]` and active label `f(s:2)=K+4`, exactly the endpoint interval for the appended path. The alternating endpoint consumer would complete every `K>=1`.

This is a conditional, elementary transport argument, not a claim that the seed exists. A single independently verified fixed seed plus this quantified argument would be an explicit parameterized supplier; solving each whole K-dependent target and extracting its prefix would remain a different, weaker procedure.

## One bounded run

After reading the balanced proof and reviewing the transport argument, use this PowerShell command from the project root:

```powershell
.\.venv\Scripts\python.exe -m lcl solve examples\unequal_seed.json --engine dfs --pins examples\unequal_seed_pins.json --domains examples\unequal_seed_domains.json --limits configs\unequal_seed_limits.json
```

It permits one worker, one eight-vertex target, 10,000 attempted assignments and two seconds, with no automatic enlargement. The ordinary run record cap is 2 MB. The tiny prescribed alphabets give at most `4!*3!=144` full assignments after the port is fixed; the implemented DFS may visit additional partial assignments. The case count is one exact named target and restriction set, not an isomorphism-class survey.

## Decisions after the run

**Verified seed:** check the original seven edges and all requested restrictions independently, record the seed as finite data, have a separate role check the all-K transport proof, then implement a dedicated unequal supplier with exact domain and boundary tests. Compare its ordinary family/interface with retained R241/R246 and primary literature before any novelty statement.

**Exhausted negative:** record failure of this particular alpha/port template. It does not show the unequal lobster or seed tree is nongraceful. Cross-check the finite restricted negative with the existing direct permutation oracle before adopting that obstruction; do not expand a search range automatically. Then formulate one specific alternative port/interface or prefix-relabeling rule.

**Incomplete:** preserve the budget and result. Inspect why this small case did not complete and decide whether an implementation issue or a different exact encoding is the next useful step. Do not reinterpret the stop as an obstruction.

Stop this task after its scoped disposition and handoff. Success means an independently supplied unequal family or a verified, useful template obstruction—not simply another solver run. Update `STATE.md`, the relevant finding/failure and proof duty, and give Will one next action.
