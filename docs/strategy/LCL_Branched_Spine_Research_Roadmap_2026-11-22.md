# Lobster Construction Lab — Branched-Spine Transition Research Roadmap

**Research-director proposal, 2026-11-22 Pacific/Honolulu.** No repository change or Codex execution is asserted by this file. Candidate mathematics below has been derived and independently spot-checked in this ChatGPT session but **has not received LCL's required separate mathematical and implementation reviews**. Historical novelty is not claimed.

**Verified LCL checkpoint:** `39d4387c32f7b01e0b8b09d72e6bf1ee85ae3001`, D076. **Protected upstream pins:** MDL `858a8c1fcfda87ba40bb1adee498a6131504a803`; MDL Bounded Search `e48b94eec4091b4fe189e325cab2eda464409943`. Verify live HEAD again at Codex intake. D076 establishes a direct alpha seed `A(18,9;4,1)` on `[[2],[3],[2],[2],[]]` and ordinary gracefulness of `[[2],[3],[2],[2]]+[[]]*(K+1)` for every integer K>=2. Its zero and minimum-high host predicates are **not** supplied. The current unexecuted `STATE.md` next action seeks a new 2322 seed with `s:4=10` and `b:2:0=0`. Do not silently overwrite this action: a deliberate strategy update must first change STATE.md and the matching handoff, preserving the deferred candidate.

## Decision

**PIVOT from enumerating numerical pins on a fixed four-section seed to independently supplied modules that can process successive genuinely branched spine sections.** The immediate mathematical target is a concrete candidate derived from the accepted MDL R241 relational alpha-ports theorem. If accepted, it supersedes much of the previous B2/B3/B4 one-center-per-section gap and moves the bottleneck to multiple centers, empty sections, and non-alpha applicability. If rejected, retain its falsifier and test one alternate port/module model; do not automatically expand solver budgets.

## I. Precise candidate theorem: an arbitrary-length one-center spine

For any integer `n >= 1`, any **positive** integers `a_0,...,a_(n-1)`, and any integer `L >= 2`, let the **original named** tree be

```
T(n,a,L) = [[a_0],[a_1],...,[a_(n-1)]] + [[]]*L
```

with physical spine `s:0,...,s:(n+L-1)`; at each `s:i` for `0<=i<n` exactly one center `b:i:0` is joined to that spine vertex and exactly `a_i` named terminals `l:i:0:j` are joined to the center; no centers or leaves belong to later empty spine sections. Its order is `N+L`, where `N = sum_i(a_i+2)` is the order of the first n-section prefix. Its actual edges are precisely the consecutive spine edges plus the described attachments and terminal incidences.

**Candidate T1.** The n-section prefix without any appended empty vertices admits an independently generated normalized alpha-graceful labeling with a physical high exit at `s:(n-1)` having value `P+1`, where `P` is its low bipartition size. The complete original `T(n,a,L)` is ordinarily graceful for every L>=2 by shifting that alpha prefix's highs by L and applying the already accepted nonadjacent numerical path recurrence to the original suffix. In the existing B4 notation, setting L=K+1 proves the entire one-center-per-section family with all positive branch sizes and K>=1, for any n. All claims require independent LCL acceptance review before being promoted from candidate to theorem.

**Additional candidate T1a, also subject to review:** the paired module below allows `a,b >= 0` (a zero quota denotes a physical direct leaf `b:i:0`), so an even number n of sections works for arbitrary nonnegative a_i. The odd n construction below requires its first a_0>=1; do not extend this claim to odd n starting with zero or to sections with no center `[]` without further proof.

### A. Independently supplied two-section module M(a,b)

For exact integers `a,b >= 0`, take the named original with two consecutive spine vertices `s:i,s:(i+1)`, one center at each and a and b named terminal leaves at the respective centers. Put `p=a+2` and `N_M=a+b+4`.

| Original physical vertex | Normalized label |
| --- | --- |
| incoming `s:i` | 1 |
| outgoing `s:(i+1)` | p+1 |
| center `b:i:0` | p |
| first terminals `l:i:0:j`, 0<=j<a | j+2 |
| center `b:(i+1):0` | 0 |
| second terminals `l:(i+1):0:j`, 0<=j<b | p+2+j |

The lows are the incoming spine vertex, second center and first terminals: exactly `[0,p-1]`. The highs are the outgoing spine vertex, first center and second terminals: exactly `[p,N_M-1]`. Every actual edge crosses the cut. The complete difference list is:

- `b:i:0--l:i:0:j`: `a-j`, exhausting `[1,a]`;
- `s:i--b:i:0`: `a+1`;
- `s:i--s:(i+1)`: `a+2`;
- `s:(i+1)--b:(i+1):0`: `a+3`;
- `b:(i+1):0--l:(i+1):0:j`: `a+4+j`, exhausting `[a+4,a+b+3]`.

These bands partition `[1,N_M-1]`, including empty bands for a=0 or b=0. The actual physical port pair is `L=s:i` (label 1) and `U=s:(i+1)` (label `p+1`), and the path `L--U` witnesses all vertices within distance two. Thus M(a,b) **supplies** the normalized relational alpha state `A(N_M,p;1,1)` without any solver or whole-tree extraction.

### B. Independently supplied single-section starter S(a)

For odd n, use `a=a_0>=1` on original named section 0: `s:0--b:0:0` and `b:0:0--l:0:0:j`. Set `b:0:0=0`, `s:0=2`, first terminal `l:0:0:0=1`, and remaining terminals `l:0:0:j=j+2` for 1<=j<a. The high alphabet is `[1,a+1]`, low alphabet `{0}`, and differences `[1,a+1]` occur on the original star edges. Choose actual entrance `L=b:0:0` and exit `U=s:0`, with witness edge `L--U`. This independently supplies `A(a+2,1;0,1)`.

For even n start with M(a_0,a_1). For odd n start with S(a_0). In either case the active physical exit is on the final included spine vertex, with **high offset y=1**.

### C. Repeat using retained R241 — original spine connector

Suppose aggregate B has normalized alpha state `A(N_B,P_B;x_B,1)` ending at physical `U_B=s:(i-1)`. Independently supply next module A=`M(a_i,a_(i+1))` on the two **new original** spine vertices `s:i,s:(i+1)`; its first port is the actual low `L_A=s:i` with offset x_A=1. Their prescribed connector is exactly the originally required spine edge `s:(i-1)--s:i`, no other edge, vertex identification or invented topology.

The accepted R241 theorem uses, for next module A and existing aggregate B:

```
F(v) = f_A(v)+P_B             (v in A)
F(v) = f_B(v)                 (v in B low)
F(v) = f_B(v)+N_A             (v in B high)
```

Here `N_A=a_i+a_(i+1)+4`. The label blocks are consecutive and disjoint; A's internal original-edge differences stay `[1,N_A-1]`, the actual connector edge has difference `N_A` because the old high port becomes `P_B+1+N_A` while the new low port is `P_B+1`, and B's actual old-edge differences become `[N_A+1,N_A+N_B-1]`. This partitions `[1,N_A+N_B-1]` exactly, without sharing any label. The returned physical ports are the old L_B and new U_A at global low-size `P_B+p_A`, with offsets `(x_B,1)`. The concatenated witness uses original actual edges, and every center and terminal is respectively one or two edges away from that spine/witness.

Induct over the finitely many two-section modules. Even n returns `A(N,P;1,1)` with `P=sum_(j even,0<=j<n)(a_j+2)`; odd n with a_0>=1 returns `A(N,P;0,1)` with `P=1+sum_(j odd,1<=j<n)(a_j+2)`. The exit always has label `P+1`; the constructed named graph is exactly the first n consecutive branched sections of the target. This proof is not an assertion that independently feasible arbitrary components can be joined: the actual R241 offset equality is checked at **every** join.

### D. Finish an arbitrary positive-length empty tail of L>=2 edges

Let the completed alpha prefix from C have N vertices and P lows, with physical exit `s:(n-1)=P+1`. The full original adds only `s:n,...,s:(n+L-1)` along the consecutive L-edge suffix. Keep low labels unchanged and raise each high label by L. The actual assigned prefix then uses

```
labels       = [0,P-1] union [P+L,N+L-1]
differences  = [L+1,N+L-1]
R            = [P,P+L-1]
D            = [1,L]
physical port s:(n-1) = P+L+1.
```

Thus the retained nonadjacent `C_L` recurrence, translated by P, fits the **actual original path** `s:(n-1)--s:n--...--s:(n+L-1)`. The induction bases, reflected bridge, label coverage and termination come from the accepted consumer. This gives a full bijection `0..N+L-1` and actual difference partition `1..N+L-1` for every finite n, a and L in the stated domain. It asserts ordinary gracefulness only after adding the path; no alpha claim for the completed L>=2 tree is required. For L=1 the same shifted interface fails (edge difference 2 against required 1), which is **only an interface restriction**. For L=0 the normalized alpha prefix is already graceful.

### E. Small full original example and independent test receipt

For `a=(2,3,2,2)` and L=2, the full named profile is `[[2],[3],[2],[2],[],[]]`, with 19 vertices and 18 edges. One resulting full labeling is:

```
s:0..s:5                =  1,15,5,11,9,8
b:0:0, l:0:0:0..1       = 14,2,3
b:1:0, l:1:0:0..2       =  0,16,17,18
b:2:0, l:2:0:0..1       = 10,6,7
b:3:0, l:3:0:0..1       =  4,12,13
```

The original edge weights are exactly `[1,18]` once each; all labels `[0,18]` occur once. This is a finite certificate, not the quantified proof. This ChatGPT session independently regenerated all named edges from the input profile and checked 534 positive-quota configurations and 540 configurations including direct-leaf zero quotas, across suffix lengths 0,2,4,7/8 and up to nine branched sections. The checks corroborate, but do not certify, the proof. Codex must not count these as its own frozen project evidence; it should reconstruct and audit its own declared cases.

### F. Literature and precedence duties

The module is presented as an **application of the accepted R241 construction and its explicit physical compatibility**. Compare it with the retained R212-B module, R246's supplied entrance menu, N121/N135 arbitrary-length domains and current literature before any novelty/priority assertion. This is not yet an LCL-adopted theorem, formal proof or claim of original historical discovery. It is not a universal lobster theorem because the target has exactly one center at each initial section, no arbitrary empty sections within the chain, and no arbitrary multiple-center arrangements. R226/R232 do not independently supply the missing palette inputs for those classes.

## II. Strategic development program (conditional, one task at a time)

| Gate | Target structural freedom | Mathematical proof duty | Falsifier / stopping criterion |
| --- | --- | --- | --- |
| G0 — ACCEPT candidate | Unbounded number of successively branched original spine sections with one center each and arbitrary positive terminal quotas | Independent M/S suppliers; correct R241 connector, global labels/differences, physical witness, all-n induction; complete suffix inventory/consumer | Any wrong original edge or inventory or inapplicable R241 offset => REVISE/REJECT; no successor |
| G1 — vary local section topology | One section carrying two centers with independently prescribed terminal quotas, at fixed neighboring actual spine positions | Produce a physically keyed two-port module menu, or prove a scoped obstruction; no replacing an edge with an added connector | An extracted prefix is not supply; failed cut is not ordinary nongracefulness |
| G2 — allow direct leaves and empty interior sections | Zero terminal quotas (direct leaves), multiple direct leaves, and genuine `[]` gaps | Exact named graph and state transition for one new structural primitive at a time; prove gap and connector closure | M(a,b) with a=0 means `[0]`, **not** an empty section `[]` |
| G3 — allow arbitrary centers per section | Prescribed list `[a_i0,a_i1,...]` of arbitrary nonnegative quotas | Independent local supplier family, multi-host palette allocation or sound existence-preserving reduction; joint R/D and physical port completeness | R226/R232 consumers only when palettes independently supplied; branch-order and multiplicities preserved |
| G4 — beyond alpha-only | Lobsters that cannot be alpha graceful; arbitrary non-alpha states | A source-supplied ordinary-graceful transformation/reduction with graph identity and termination, or a broader exact frontier theorem | A graceful supertree or a failed alpha cut does not prove gracefulness/nongracefulness of the original |
| G5 — ultimate goal | All finite lobsters or a rigorous counterexample | Exhaustive case partition into proved suppliers/reductions and a terminating construction, or a complete impossibility argument for a named original | Finite tests, timeout, or merely exact N240 counting do not discharge universal positivity |

Gates are dependency/decision checkpoints, **not** an automatically scheduled sequence. Reassess after a consequential theorem or approximately three tasks in one direction. Preserve meaningful negative proofs and inconclusive outcomes.

## III. Other research directions to keep available

1. **R241/R246 module menus.** Generalize from the fixed `(x,y)=(1,1)` module to a **finite, independently supplied menu of exact physical port signatures** keyed to actual section topology, including sections with multiple centers, and prove transition closure under the original connector. Do not assume finite menu universality; source N135/N141 has model-specific finite-state bounds only.
2. **R226/R232 palette allocation.** For a candidate partially labeled named core, use the accepted exact two-/multi-host consumers to discharge terminal leaf batches if full unused label and difference partitions are constructively supplied. Avoid silently treating exact allocation feasibility as independent core supply.
3. **Source-to-target transformations.** R248 component palette reflection, R244 conditional reconstruction and reviewed N121/N135 transfer patterns can change entire labeling sections; do not insist on append-only labels. The transformation must preserve the exact requested original graph and measure decrease or show finite construction. R243's added connectors are not original graph edges without separately proved reconstruction.
4. **Counterexample-guided synthesis.** Generate one rule, challenge only the smallest discriminating named originals, repair/refute that rule. Unchanged checker and independent auditor are mandatory; a larger DFS/SMT engine alone does not prove the theorem.
5. **Proof-assistant milestone.** Once G0 is accepted in LCL, consider a separately authorized small formalization of R241 label/difference interval partition and its concrete M/S suppliers. Do not install Lean or use paid services in the first G0 task.

## IV. Handoff strategy and one next action

The live D076 STATE currently selects a new zero-host 2322 seed. **Do not silently execute a different task under that scope.** This roadmap recommends a replacement because G0 could eliminate a much larger structural restriction. When the owner adopts the attached one-task packet `LCL_Codex_R241_Arbitrary_Branched_Spine_2026-11-22.md`, that packet constitutes one bounded scope authorization. Codex must FIRST verify Git identities and change `STATE.md` and the matching handoff to record the new one selected action and the prior 2322 zero-host search as **DEFERRED/UNSTARTED**, without changing its meaning. Then execute only G0, complete separate reviews and Git synchronization, verify both SHAs and STOP. The next mathematical task after G0 must be selected in a new owner review; no automatic G1.

If G0 is accepted, reconsider whether a major proven change in the bottleneck warrants a full Project-instruction rewrite under the v7 freshness policy. For now **Project instructions: KEEP**, because the candidate is not yet independently accepted. Keep the immutable upstream pins. Do not mistake this roadmap for an edit to the user's Project settings or repository.
