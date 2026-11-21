# Lobster Construction Lab — initial research context

**Snapshot:** version 0.1.0, November 20, 2026, Pacific/Honolulu. This is an upload snapshot; the Codex folder's `STATE.md` and research records become authoritative as work advances. ChatGPT uploads do not automatically synchronize with local files.

## Purpose in plain language

Will noticed that the old projects seemed to test specific numbered inputs and wanted a general rule. The desired input is actually the tree's structure, not simply its number of vertices. A universal construction could take any lobster structure and produce a valid labeling by an algorithm or a collection of proved repeatable rules. A short equation is not required.

A tree with m edges is graceful if its vertices receive 0..m bijectively and its actual edge differences are exactly 1..m, each once. A lobster is a finite tree with a path within distance two of every vertex. The ultimate goal is universal lobster gracefulness or a rigorously established nongraceful lobster; this package claims neither.

## Source foundations

MDL: `drkmtr1/Math-Discovery-Lab`, commit `858a8c1fcfda87ba40bb1adee498a6131504a803`. Bounded Search: `drkmtr1/MDL_Bounded_Search`, commit `e48b94eec4091b4fe189e325cab2eda464409943`. Authenticated live checks found their main heads unchanged from the preceding audit. Both private upstream repositories remain unchanged. No remote fork was created.

The package preserves the source-linked `MDL_General_Construction_Review_2026-11-20.md`, 31 curated source excerpts from 20 blob-verified complete files, exact pinned links and normalized excerpt hashes. This is a new curated derivative workspace with its own active instructions. Archived administrative text is source evidence, not a continuation order for the old campaign. No permissive upstream license was found or invented.

Useful retained pieces include N33's explicit infinite family; N68–70's fresh-label and patch/tile constructions; N107's independently supplied paired inputs; N121's parity-restricted unequal-factor composition; N135/N141's recurrence/capacity criterion; N145's paired two-port composition; R226/R232's conditional exact completion/allocation; R241/R246's physical-port modules; R243's expanded connectors; R244/R248's conditional reconstruction/source transformations; and L007/L010/H010's explicit family rules. N240 and the exact recurrence formulate counts but do not establish positivity for every lobster.

Preserve the failures: separate feasibility need not combine; equal residual label/difference sets do not imply completion; local difference support can conflict with incidences; alpha-only search misses ordinarily graceful trees; inserted connectors change the target; and the corrected P6/spider counts refute the earlier count-monotonicity claim rather than existence itself.

## Exact B2 family and target interface

Profiles encode a section for each spine vertex. An entry q at section i creates branch `b:i:j` with q terminal leaves attached, while q=0 is a direct leaf. Empty trailing sections are real spine vertices.

The first family is

```text
[[q]+[0]*z0, [r]+[0]*z1] + [[] for _ in range(K+1)]
q,r,K >= 1; z0,z1 >= 0; m=q+r+z0+z1+K+4.
```

The prefix ends at actual `s:2`; the unfinished target is a K-edge path. A usable interval boundary has unused labels `R=[ell,ell+K-1]`, unused differences `D=1..K`, and active label `ell-1` or `ell+K`. Every unfinished incidence must be at this actual port. A boundary check alone does not establish independent supply or verify a different suffix topology.

## Two established project baselines

**Padded composition:** Let `K1=r+z1+K+2`. Two retained one-branch L010 prefix blocks compose if `z1>=K+1` and `z0>=K1+1`. Reflect the second local block by `K1+1-g`. It returns unused labels `[K1-K+1,K1]`, differences `1..K`, and active label `K1-K`. This reviewed corollary uses substantial extra direct leaves and arbitrary positive q,r,K.

**Balanced, with no direct leaves:** For every `q=r=t>=1`, `z0=z1=0`, `K>=1`, set `m=2t+K+4`. Assign

```text
s:0=m; b:0:0=0; l:0:0:j=K+t+4+j, j=0,...,t-1
s:1=t+1; b:1:0=K+t+3; l:1:0:j=j+1, j=0,...,t-1
s:2=K+t+2.
```

These labels use exactly `0..t+1` and `K+t+2..m`. Their actual prefix differences form the disjoint blocks

```text
K+1; K+2; K+3..K+t+2; K+t+3; K+t+4..K+2t+3; m.
```

They therefore use `K+1..m` exactly and leave `R=[t+2,K+t+1]`, `D=1..K`, with the active label just above R. Complete the path by alternately taking the low and high endpoints of R; the differences decrease from K to 1. This is an explicit parameterized supplier, independently recalculated by two separate roles and implemented as `two_section_balanced(t,K)`. The unit wrapper fixes t=1.

This family proof is stronger than finite testing, but its domain is restricted. It does not prove historical novelty, all unequal branch cases, arbitrary future branched sections, or all lobsters. Its full local proof is `research/B2_BALANCED_SUPPLIER.md`.

## Finite controls and their meaning

Release validation checks named counts `G(P4)=4`, `G(P6)=24`, and `G(spider(2,2,1))=16` with separate methods. P4 with its middle labels pinned to 0 and 3 has zero restricted completions although the unrestricted path is graceful.

The four B2 controls all have z0=z1=0,K=1,no root-label pin, above-side boundary:

| q,r | Interval start ell | Result |
|---|---:|---|
| 1,1 | 1 | Exhausted restricted negative |
| 1,1 | 2 | Independently checked witness |
| 1,2 | 1 | Independently checked witness |
| 2,1 | 1 | Exhausted restricted negative |

These are four exact target/interface pairs on three named profiles, not four isomorphism classes or a universal survey. The first negative was cross-checked by direct permutation enumeration. Extracted solver prefixes remain explicitly marked `independent_supplier=false`.

For the unit family, the tempting fixed start ell=2 cannot work in the same above-state for all K: a separate elementary prefix obstruction covers K>=3. The balanced supplier's ell=3 when t=1 avoids that specific obstruction. See `B2_INTERVAL_OBSTRUCTION.md`; do not treat the successful K=1 ell=2 witness as an inductive rule.

## Selected next task — not yet executed

**B2-UNEQUAL-SEED-001:** On fixed prefix `[[1],[2],[]]` (8 vertices, 7 edges), seek an alpha labeling with low vertices `s:1,b:0:0,l:1:0:0,l:1:0:1` receiving 0..3 and high vertices `s:0,b:1:0,l:0:0:0,s:2` receiving 4..7, with actual `s:2=4`.

If a checked fixed seed exists, add K to every high label. Every prefix difference then increases by K, leaving labels `[4,K+3]`, differences `1..K` and active `K+4`, so the path consumer would work for every K>=1. A separate reviewer must check this transport proof. A fixed seed plus the quantified transformation is independent supply; extracting a different prefix from each solved whole tree is not.

The declared DFS check is one case, 8 vertices, 10,000 attempted assignments, two seconds, one worker, and a 2 MB result cap. Input/pin/domain/limit JSON files and the exact PowerShell command are in `research/NEXT_TASK.md`. A negative excludes only this alpha/port template; cross-check it with the tiny oracle before adoption. An incomplete result remains undecided. Stop after the task's scoped disposition, not an automatically growing campaign.

## Working tools and agent rules

The standard-library core includes exact profiles, retained constructors, R226, bounded DFS, full-resource frontier DP, independent checker, direct permutation oracle, original-target records and case-level resumable experiments. Optional adapters use NetworkX3.7, SymPy1.14.0/mpmath1.3.0 and z3-solver5.4.1.0. CP-SAT/DLX/formalization and generalized automata are deferred until a selected proof or performance need justifies them. No GPU, local LLM, paid API or training is needed initially.

Agents may improve algorithms. Preserve baselines and failed evidence; state changed assumptions/interfaces; version hypotheses/source/configurations; run meaningful comparisons; and use separate review for semantics, pruning, symmetry, completeness and checker changes. A solver must never weaken its checker or redefine the target. Use actual available agent capabilities; no assumed automatic memory, background execution or synchronization.

Original named topology and caller-retained restrictions govern checking. SAT witnesses are checked independently; bad positives are quarantined. Exact counts require exhaustion. Time/node/state interruptions are incomplete. Resume is at case boundaries, with immutable attempts and identity checks; it is not continuation of an unfinished search stack. Limits are cooperative design controls, not measured hardware guarantees or hard OS containment.

## Literature and validation limits

The primary November 3, 2026 Zenodo record [23932907](https://zenodo.org/records/23932907) claims a finite Lean certificate for all subcubic lobsters. The build inspected its graph-level statement, coverage/certificate structure and rule table, but did not run Lean or conduct a full proof audit. It uses three compiler-dependent native checks. All three small pilot profiles lie within its stated ordinary-gracefulness domain; our prescribed returned-state property is additional. It illustrates the distinction between finding finite states and proving closure for all permitted transitions.

The [gracesize paper](https://arxiv.org/abs/2511.11331v2) gives almost-graceful asymptotic coverage; the [supertree paper](https://arxiv.org/abs/2611.01340) supplies expanded graceful targets. Their abstracts were inspected; neither substitutes for the exact original-target obligations here. Recheck primary literature before claiming novelty or worldwide problem status.

The release executed on Linux with Python3.12.14 and the optional versions listed above. Windows11/64-bit Python3.12/3.13 setup materials are provided, but Windows and Python3.13 were not executed here. `evidence/validation/VALIDATION_REPORT.md` is the authoritative executed report. No universal result, new counterexample, remote fork or native ChatGPT Project was created.

## Handoff

Read the current local `STATE.md`, then the exact task and relevant proof. ChatGPT handles explanation, literature, proof development and review; Codex owns actual files, runs and evidence. Exchange accepted statements and exact result artifacts deliberately. At completion, update the authoritative finding/failure/proof records and leave one next action. Routine scoped work is authorized; upstream writes, publication/pushes, paid usage, security changes and indefinite work require separate authorization.
