# Mathematical method selection

**Decision date:** 2026-11-21 UTC / 2026-11-20 Pacific/Honolulu.  
**Purpose:** choose methods that can improve independent compatible-state supply and repeated branched-section continuation. This is a research plan, not a new theorem or an assessment of historical novelty. Source identifiers below resolve in [SOURCES.md](SOURCES.md).

## 1. The actual gap

The retained projects already contain formulas for infinite families, exact completion consumers, and repeated constructions. The new lab should spend its first research budget on an input those consumers cannot yet independently obtain, or a continuation step they cannot yet justify. Another exact reformulation of gracefulness would be useful infrastructure only if it enables such a result. [U01–U07]

A supplier must construct its partial labeling from the declared tree parameters, without first obtaining a complete successful labeling of that target and deleting its suffix. A finite solver can discover promising states, and a verified full witness proves that particular tree graceful. Neither is an independent supplier theorem.

**Build outcome:** the direct approach produced the reviewed balanced zero-padding supplier in `research/B2_BALANCED_SUPPLIER.md`. Its all-parameter label/edge partition gives the independent input guarantee. The next bounded task asks for one unequal alpha/physical-port seed and a conditional high-side shift proof; see `research/NEXT_TASK.md`. This concrete outcome strengthens the case for structural formulas and exact verification before adding another solver framework.

For a tree with final edge count `m`, keep both inventories: unused labels from `0..m` and unused differences from `1..m`. Keep the actual boundary vertices, their labels, and the exact remaining incidences. Equal inventory sizes, equal inventory sets, separate feasibility, and support for each individual difference are each weaker than joint completion. The retained P4 example and C007–C009 records explain why. [U02, U04, U08]

## 2. First scientific task: B2-P1

Use the named profile

```text
[[q] + [0]*z0, [r] + [0]*z1] + [[] for _ in range(K+1)]
q,r,K >= 1; z0,z1 >= 0
m = q + r + z0 + z1 + K + 4
```

There is one positive branch at each of `s:0` and `s:1`, with `q` and `r` terminal leaves; `z0` and `z1` are actual direct leaves. The prefix ends at physical vertex `s:2`. The unfinished suffix is the specified `K`-edge path starting there. The complete profile, including trailing empty sections, is part of the target.

**Research objective:** independently label that prefix and return an interface at `s:2` which a proven path or caterpillar consumer can finish. Seek a stated infinite parameter domain, preferably reaching smaller or zero direct-leaf budgets, or an interface broader than the retained interval construction. Record its actual improvement over applicable retained constructions.

The familiar candidate interface is active label `K+1` with unused labels and differences both `[1,K]`. It is a useful hypothesis, not a mandatory definition of success or a promise that every parameter choice admits it. A translated or reflected endpoint interval, or another explicitly proved finishable interface, is admissible. Failure of this interface does not show that the target is nongraceful.

### A retained-composition comparison must come first

H010 leaves active label `K1+1` and unused labels/differences `[1,K1]`. Reflecting local labels by `f_actual = K1+1 - g` embeds a local root-zero prefix at that physical port and preserves absolute differences. The one-branch L010 formula gives the same prefix without H010's additional generic branch-size bound. During assembly, the methods and implementation roles independently recalculated the two-block composition under `K1=r+z1+K+2`, `z1>=K+1`, and `z0>=K1+1`. The returned interval is `[K1-K+1,K1]`, with active label `K1-K` just below it. This is implemented as `two_section_padded`; its proof is preserved in [PROOF_OBLIGATIONS.md](../research/PROOF_OBLIGATIONS.md). It is a derived corollary of retained ingredients, with no novelty claim. [U03]

Therefore, “two branched sections with enough extra leaves” is not automatically new coverage. Before promoting a B2-P1 candidate, compare its parameter conditions with this composition baseline, L010/H010, and applicable MDL constructions. Do not infer universal iteration from the two-block result. Ordinary gracefulness of a family, a new useful returned interface for it, and a historically new theorem are three separate claims.

### Evidence the first investigation should produce

1. A precise prefix specification, all imposed label restrictions, and the actual returned state.
2. A small bounded table separating unrestricted witnesses, prescribed-interface feasibility, and constructor applicability.
3. An explicit formula or finite structural rule proposed from those observations, with all parameter domains stated.
4. Counterexample attempts aimed at the rule's sign, parity, endpoint, and resource-collision boundaries.
5. Either a proof of a noncircular supplier on a useful infinite subfamily, or a precise refutation of the proposed interface with a justified next alternative.

Finite solver states remain exploratory until step 5. The value of a negative result is the assumption it resolves, not the number of additional trees searched.

## 3. Selected portfolio

| Method | Decision | Specific job | Coverage or evidence limit |
|---|---|---|---|
| Direct constructors | Implement and preserve as baselines | Caterpillar, L007, L010/H010, padded composition and the project-derived balanced zero-padding supplier | Each formula has its own sufficient domain; domain rejection is not nongracefulness |
| Constructive allocation / matching / flow | Implement R226; use R232 and reduction ideas selectively | Finish leaves from independently supplied core labels and both resource palettes; identify supply obligations | A generic flow model does not remove parity, compatibility, physical-incidence, or palette-supply duties |
| Bounded DFS | Implement now | Obtain small exact witnesses and discriminating counterexamples with transparent restrictions | A limit or failed prescribed state is not an unrestricted negative result |
| Exact frontier DP | Implement now with bounded memory/states | Cross-check counts and expose state collisions while retaining every globally relevant resource | Tree structure alone does not make graceful-labeling resource state constant size |
| Z3 finite integer constraints | Optional real adapter | Challenge prescribed states and search alternatives independently of DFS | `unknown` is incomplete; `unsat` applies to the exact encoded restrictions and trusted solver, not a checked theorem certificate |
| CP-SAT | Research-backed alternative, deferred | A different finite-integer engine if a concrete workload exposes a Z3/DFS weakness | A second solver is not automatically a better research result; no speed claim without a benchmark |
| Algorithm X / dancing links | Defer implementation | Potentially combine precomputed complete local assignments by exact resource cover | Shared vertices and connector edges require a sound, complete reduction first |
| Transfer automata and finite rule certificates | Inspect the recent subcubic certificate before designing another bounded-degree construction | Understand its independently supplied cells, transition closure and coverage theorem; assess possible extensions | Its degree-three scope and theorem's output must not be silently broadened to arbitrary lobsters or prescribed B2 return states |
| Nilpotent resource algebra | Retain as an exact specification and diagnostic | Express simultaneous label and difference exclusion; explain DP and failed local positivity | Exact coefficient extraction does not establish positivity or efficient evaluation |
| Counterexample-guided template synthesis | Use as a disciplined workflow | Propose small parameter formulas, then target violations and refine domains | Bounded falsification is not full CEGIS verification over unbounded integer parameters |
| Symbolic algebra and formal proof | SymPy optional now; proof assistant later | Check exact identities and sign cases, then formalize a stable consequential theorem | A CAS result or AI review is not a complete kernel-checked argument |

## 4. Why these choices address the gap

### 4.1 Constructive allocation and structural reduction

R226 is the strongest immediate extraction baseline. For fixed core labels and two physical hosts, it builds the actual difference multigraph, preserves isolated difference demands, forces tree assignments, and handles reflected pairs and a possible midpoint. After availability and balance checks, its attainable first-host totals are `A0 + 2j + epsilon`, with bounded `j` and a zero-or-one midpoint option. It supplies a completion when the requested quota qualifies. It supplies neither a successful core nor a useful palette partition. [U04]

R232 removes another conditional input by coordinating reserved batches without requiring a successful quota split in advance, under its own structural and capacity hypotheses. Use it when a candidate supplier naturally produces those batches. Do not replace its integral conditions with a claim that fractional feasibility or a single flow value proves completion. [U05]

Reduction remains a serious alternative to a prefix architecture: construct a simpler graceful source, transform it, and recover exactly the requested target. R248 demonstrates source-based reflection without an alpha premise, but target reachability still has to be supplied. A connector that inserts extra edges proves a result for the expanded tree unless a reconstruction theorem removes them. The corrected failure of count monotonicity leaves positivity preservation as a separate unproved possibility. [U07, U09]

### 4.2 Exact finite search and frontier DP

For each actual vertex `v`, the direct constraint model uses an integer `x[v]` in `0..m`; all `x[v]` are distinct. For each actual edge `uv`, let `d[uv] = abs(x[u]-x[v])`. Requiring all `m` differences distinct and in `1..m` makes their set exactly `1..m`. This is an exact finite encoding by elementary cardinality. It is also the project specification. [U02]

Pins, interval domains, alpha conditions, fixed root zero, and requested return states are additional restrictions and must be reported. Complementation preserves gracefulness, but it does not put zero at an arbitrary chosen root. The unrestricted default therefore adds no such condition.

A sound frontier key contains the processing position, the used-label mask, the used-difference mask, and labels of every processed vertex incident to an unfinished edge. Store any additional state needed by imposed restrictions. Merge states only when these data make their future extension sets identical; preserve integer multiplicities when counting named labelings. The two masks alone have up to `2^(2m+1)` combinations before frontier labels are considered. This is a state-space observation, not a tight reachable-state bound. A short physical frontier does not erase those global resources.

The direct permutation oracle and independent certificate checker have deliberately different code paths. Agreement on a bounded instance checks implementation; it is not an infinite-family proof. Do not quotient named counts by automorphisms unless a separate counting argument accounts for the orbit sizes.

### 4.3 SAT/SMT and CP-SAT

Z3 provides integer arithmetic, logical constraints, incremental solving, models, assumptions, and solver-result diagnostics. Its Python API supports the required finite constraint model without introducing floating-point arithmetic. A SAT encoding using Boolean assignment variables is possible, but it adds encoding and certificate infrastructure without a demonstrated first-task benefit. [E02, E03]

Use model output only after the independent checker accepts the actual graph and labels. Preserve unknown reasons and all bounds. If the model is unsatisfiable, preserve the exact constraints and solver version; an unsat core is an explanation relative to asserted assumptions, not automatically an independently checked impossibility proof.

CP-SAT has integer variables and explicit feasible, infeasible, invalid, and unknown statuses. Its official documentation explicitly distinguishes a stopped unknown run from infeasibility. It is a credible future alternative if its propagation or enumeration performs better on measured LCL cases. It is deferred because the initial mathematical question does not need two optional compiled solver stacks. [E04]

### 4.4 Exact cover

Knuth's Algorithm X enumerates exact covers, and dancing links makes changes reversible during the search. A natural LCL use would make one row a complete admissible assignment of a local piece, with columns recording the piece choice and consumed label/difference resources. [E01]

That reduction is incomplete if adjoining pieces can give different labels to their shared physical vertex. Separator assignments must be fixed consistently or represented by a proved compatible formulation; their labels must be counted once, and connector edges must contribute their actual differences. Naively making a row for each edge-label triple does not enforce one consistent label per shared vertex. Establish and test the reduction before investing in a fast cover engine. Row generation may itself be the hard part.

### 4.5 Transfer states and square-zero algebra

Retained small-state constructions, including N135/N141 and port-based module assembly, are valuable because their transition rules carry actual mathematical meaning. Extend them by proving that a new input domain reaches the required states and stays within the transition hypotheses. Do not interpret a finite-state model as a complete quotient of arbitrary graceful labelings. [U06]

N240's commuting square-zero variables record labels and differences: `x[t]^2 = y[d]^2 = 0`. Any monomial reusing either resource vanishes. The full coefficient counts graceful assignments on named vertices, with powers retaining named-leaf multiplicities. Its spine recurrence still carries global resource subsets. Local nonzero factors can multiply to zero; the four-vertex diagnostic already witnesses that obstruction. [U07, U08]

This gives a useful common language for DP, certificates, and possible future positivity lemmas. It is not itself a supplier, positivity proof, polynomial-time algorithm, or reason to install a large symbolic tensor package.

### 4.6 Template synthesis, symbolic work and formalization

Solar-Lezama's synthesis work combines a candidate synthesizer with a validation procedure that supplies counterexamples. Adopt that separation: the proposer chooses a small explicit formula or construction grammar; a challenger searches the stated domain for violations. [E05]

For B2-P1, good templates include affine label intervals, parity-dependent ordering, reflected blocks, and a finite menu of return interfaces. Preserve every falsifier and the exact version it rejects. If the challenger tests only finitely many sizes, the result is bounded evidence. To close an unbounded claim, prove the interval bounds, injectivity, coverage of all actual edges, disjoint difference blocks, and the consumer's preconditions for every allowed parameter.

SymPy can check exact symbolic identities and simplify parameter expressions. Declare integer and sign assumptions explicitly; its assumptions interface can return unknown. Avoid interpreting numerical sampling, floating-point equality, or a generic simplification call as a complete argument about intervals and absolute values. [E06, E07]

When a consequential supplier statement stabilizes, a Lean formalization can check that exact statement and its proof through a logical kernel. First isolate the finite graph model, palette bijections, and arithmetic lemmas. A `sorry`, an added axiom asserting the goal, or a proof of a narrower statement is not completion. Formalization is deferred until there is a theorem worth formalizing. [E08]

## 5. When agents should modify algorithms

Algorithm changes are appropriate when a retained counterexample, measured bottleneck, or new invariant justifies them. Require the agent to state the mathematical effect: ordering-only change, completeness-preserving pruning, additional declared restriction, state quotient, or new construction. The independent reviewer should challenge the relevant effect, and the oracle should check bounded equivalence where applicable.

Do not improve apparent performance by silently fixing a root label, sorting distinguishable branches, dropping the difference mask, relaxing target topology, or changing named counts into isomorphism-class counts. Do not add a method solely because it sounds advanced. A method earns promotion through a specific missing duty it resolves and evidence proportionate to its claim.

The initial standard-library core and optional adapters keep that process inspectable. The preferred first gain is a small, clearly delimited supplier theorem with a reusable returned state; a broad engine with no new supply or continuation result is infrastructure progress only.

## 6. Recent primary-source checkpoint: subcubic lobsters

Akram Younso's November 3, 2026 Zenodo v2 archive claims gracefulness for every finite lobster of maximum degree at most three, using a 6,104-rule certificate and Lean. We retrieved its archive and inspected the graph-level statement, coverage argument, certificate checks and README. Three checks use `native_decide`. We did not rebuild Lean or independently audit the entire proof. [E10]

This is a concrete primary source to investigate before creating another finite transition scheme. Its coverage source separates discovery from certification: a bounded exploration proposes states, while a subsequent all-outgoing-transition closure/acceptance check supports induction over arbitrary words. The useful design lesson is to prove that the finite state set suffices, not to infer universal coverage from many successful sample trees. [E10]

All three profiles in the starter four-pair pilot are subcubic: the branch centers have degree `q+1` and `r+1`, each at most three; `s:1` has degree three and the other spine vertices have smaller degree. Thus the archive's stated ordinary-gracefulness scope includes those targets. It does not assert our required interval and physical return port. The finite pilot remains useful for that interface distinction, but is not an attempt to establish new ordinary-family coverage.

For a broader supplier proposal, compare first with this source's actual cell and joining interfaces. A candidate with `q>=3` or `r>=3` already leaves its stated maximum-degree-three scope, though that alone does not establish novelty. Do not import its rule table as a universal oracle. A deliberate future reproduction must use the pinned source/toolchain, inspect the theorem and computational trust boundary, and record whether the build actually succeeds. No Lean installation or proof execution is claimed in this package's method research.
