# LCL Codex bounded task packet — D080 zero-to-one R241 bridge

**Proposed task:** `LCL-R241-ZERO-TO-ONE-BRIDGE-001`  
**Status:** Proposed, **UNSTARTED**. This document is a new bounded-scope proposal; it is not an accepted mathematical theorem or permission to run successors. Giving it to Codex with explicit user authorization permits only the one task below.  
**Expected accepted parent:** `eb75d7a31cc240cec4d4cc90e432286e6de319e1` (verify live local HEAD, actual GitHub `main`, worktree, branch and handoff before any execution).  
**Protected upstream:** MDL `858a8c1fcfda87ba40bb1adee498a6131504a803`; MDL Bounded Search `e48b94eec4091b4fe189e325cab2eda464409943` — **READ ONLY**.  
**Retained materials:** `AGENTS.md`, live `STATE.md`, `docs/REPOSITORY_CONTINUITY.md`, committed branched-spine roadmap, `research/R241_PAIRED_BRANCHED_SPINE.md` (D078), `research/R241_TWO_CENTER_PORT_FALSIFIER.md` (D079), `references/upstream/mdl/N241_relational_ports.md`, `research/B2_NONADJACENT_CONSUMER.md`, D079 originals/certificates/audit/reviews, and latest D079 handoff.

## 1. Authority and scope reconciliation

Live D079 `STATE.md` selects a strict `(0,1)` state on the **exact original** `[[1],[1]]` as a possible bridge. This task **first adjudicates that exact selected question**. It then proposes one directly related positive replacement `[[a],[a+1]]` and the one resulting repeatable multi-center macro. This additional family/closure proof is a **new scope decision**, not an implication of the old STATE.md alone. Require explicit user authorization for this entire one-task packet. Preserve the literal former action in `research/DECISIONS.md` and the handoff; record the bounded expansion in `STATE.md` **before** executing mathematical evidence, so future agents know what was actually selected. The previously deferred D076 zero-host task remains deferred/unstarted.

No edits to upstream repositories, packages, production checker, security/settings, or paid services. No successor task, automatic enlarged search, repeated trial or background campaign. Do not change the target graph or identify named terminal indices.

## 2. Falsifier A — exact selected `[[1],[1]]` bridge

Use the original named six-vertex tree with spine `s:0--s:1`, center edges `s:0--b:0:0`, `s:1--b:1:0`, and terminal edges `b:0:0--l:0:0:0`, `b:1:0--l:1:0:0`. Its forced normalized alpha partition at this physical orientation is low `s:0,b:1:0,l:0:0:0` labeled `[0,2]` and high `s:1,b:0:0,l:1:0:0` labeled `[3,5]`, so `p=3`.

Selected ports `(x,y)=(0,1)` require `s:0=0`, `s:1=4`. **Challenge, do not assume**, this proposed impossibility proof:

- The original edge `s:0--s:1` weighs 4. Difference 5 requires the actual edge between labels 0 and 5. Because 0 is already at `s:0`, the high label 5 must lie at its neighbor `b:0:0`; the other high terminal is consequently 3.
- The low labels 1 and 2 go to `b:1:0` and `l:0:0:0`. If the first terminal is 1, its edge to `b:0:0=5` repeats difference 4. If the terminal is 2, that edge weighs 3 and the remaining center `b:1:0=1` makes `s:1--b:1:0` weigh 3 again.
- Therefore the strict `(0,1)` predicate fails **on this named graph and orientation only**. The four pinned assignments are `2!2!=4`; an exhaustive named check is a corroborative diagnostic, not the proof.

**Positive same-graph control:** `s:0=0,s:1=3,b:0:0=5,l:0:0:0=1,b:1:0=2,l:1:0:0=4` yields alpha graceful weights 3,5,4,1,2, i.e. `(0,0)`, demonstrating the target itself is graceful.

## 3. Candidate positive bridge family, to independently prove or refute

For every exact integer `a>=1`, take the **original** `H(a)=[[a],[a+1]]` with two spine vertices, one physical center at each, `a` first terminals and `a+1` second terminals. Its order is `N_A=2a+5` and normalized low-class size is `p_A=a+2`.

Candidate direct labeling:

```
f(s:0)       = 0
f(s:1)       = p_A+1 = a+3
f(b:0:0)     = N_A-1 = 2a+4
f(b:1:0)     = p_A-1 = a+1
f(l:0:0:j)   = j+1,       0<=j<a
f(l:1:0:0)   = p_A = a+2
f(l:1:0:j)   = p_A+j+1,   1<=j<=a
```

All names are distinct; for `a=1`, `l:1:0:1` exists. This candidate is an independently constructed `A(2a+5,a+2;0,1)` with physical low entrance `s:0`, high exit `s:1`, and witness the actual spine edge `s:0--s:1`. The label bands are exactly `[0,a+1]` and `[a+2,2a+4]`.

Demand separate edge-by-edge proof that the differences on the **actual edges** partition:

- `b:1:0--l:1:0:0`: `{1}`
- `s:1--b:1:0`: `{2}`
- `b:1:0--l:1:0:j`, 1<=j<=a: `[3,a+2]`
- `s:0--s:1`: `{a+3}`
- `b:0:0--l:0:0:j`, 0<=j<a: `[a+4,2a+3]`
- `s:0--b:0:0`: `{2a+4}`.

These bands purport to exhaust `[1,2a+4]` once each. If any formula or named incidence fails, preserve the falsifier and do not promote the family. Supply physical witness distances and finite termination for every `a`.

Exploratory exact counts, **not established evidence until independently reproduced**: fixed `(0,1)` alpha assignments on `[[1],[1]]`: `0/4`; on `[[1],[2]]`: `2/12`; on `[[2],[3]]`: `12/144` (all counts nonquotiented, all named). The actual formula itself needs no solver.

## 4. Candidate R241 joint macro and arbitrary-length repeatability

Retain the **already checked D079** exact original `B=[[1,1],[1]]`, with the specific verified alpha state `A(8,4;1,0)`, low entrance original `s:0=1`, high exit original `s:1=4`, and the unchanged named ledger from D079. It is not a `(1,1)` state.

Place a fresh disjoint `H(a)` on original consecutive sections 2 and 3, with names mapped exactly from its sections 0,1. Add **only** the original connector `s:1--s:2`. In the accepted R241 convention `B` is the old aggregate and `A=H(a)` is the new supplier. Its physical port requirement is `y_B=0=x_A`; **verify the orientation**. After the R241 relabeling, old B lows stay fixed, new A labels shift by `p_B=4`, and old B highs shift by `N_A=2a+5`. The original connector must weigh exactly `N_A`.

Candidate output is the normalized original `Q(a)=[[1,1],[1],[a],[a+1]]` with

```
A(N_Q,p_Q;x_Q,y_Q) = A(2a+13,a+6;1,1),
L_Q = physical s:0,
U_Q = physical s:3,
f(L_Q)=1,
f(U_Q)=p_Q+1.
```

Demand complete named vertex-label bijection, original edge identity, internal spectrum bands and actual connector singleton, alpha partition, and spine witness. This output's `x_Q=y_Q=1` is the claimed closure resource.

Then, **within this single task**, prove or reject that any finite list `Q(a_1),...,Q(a_k)` for `k>=1` and all exact positive `a_i` can be R241-composed consecutively, restoring **only the actual original spine edges** between modules. The output should remain an independently supplied normalized alpha state with a high physical exit of offset 1. Explicitly state finite induction, returned port names and both difference/label partitions; no extracted full-solution prefixes. For the exact original obtained by adding `L>=2` terminal empty spine sections, test the accepted nonadjacent high shift and original-path consumer with `R=[P,P+L-1]`, `D=[1,L]`, physical exit `P+L+1`. `L=0` is the normalized alpha case; `L=1` is *outside* this prescribed consumer. This would establish only the repeated restricted multi-center macro family, **not arbitrary multiple-center sections or universal lobster gracefulness**.

A valid positive instance is the named `Q(1)=[[1,1],[1],[1],[2]]` with `N=15,p=7, entrance s:0=1, exit s:3=8`. An exact `L=2` completion has original path label triple `s:3,s:4,s:5=(10,8,7)` with remaining differences 2,1. The `Q(1),Q(2)` repeated macro with `L=5` has 37 vertices; it exercises the recursive nonadjacent bridge, not just the base.

## 5. Frozen bounded evidence / controls

One standard-library Python 3.12 or 3.13 CPU worker. **No SMT, CP-SAT, additional packages, GPU, paid service or production algorithm changes.** One official validation sequence with independent auditor; zero retries/replays; at most 30 combined process-CPU seconds, <=2 MB per evidence record, <=8 MB total evidence, and at most 160 small exact named assignment visits (4+12+144, with preserved correct factorial-rank coverage if enumeration is used). All other cases use direct formulas. At most **six new original graph identities** beyond the retained D079 two-center original; no graph substitutions.

Fixed controls: `[[1],[1]]` strict `(0,1)` negative and alternate `(0,0)` positive; direct H(1) and H(2) original certificates; retained D079 B `(1,0)` positive recheck; Q(1) normalized, Q(1) with L=2, and Q(1)+Q(2) with L=5, each bound to its original named graph. If counting requires additional graph identities, reduce redundant finite checks within the fixed ceiling rather than expand it. Reject a deliberately wrong graph digest, a mismatched R241 physical offset, and a false suffix difference inventory before claiming correct handling of adversarial inputs. No quotient or symmetry assumption.

The independent auditor must reconstruct original incidences from profiles without importing the producer, check each named vertex and original edge exactly once, verify graph digest separately from ledger ID, match any assignment ranks and duplicate-edge falsifiers, compare all complete spectra and exact inventories, and confirm physical spine/witness/port compatibility. Enforce executable/input SHA-256, saved command receipts, limits, no optimized-assert ambiguity, and byte manifest custody. Preserve archived INCOMPLETE receipts, prior proofs and failures without modification.

Separate **read-only** AI mathematics and implementation reviewers must challenge the specific universal algebra, exact physical port orientation, joint composition, recurrence bridge, negative scope and audit soundness. AI review is not formal proof-assistant certification. If the general formula/closure fails, classify REVISE/REJECT and keep any valid smaller statements separately; a diagnostic is never a universal theorem.

## 6. Authoritative records, release and STOP

Recheck Git state and protected baselines. First reconcile explicit user-approved new scope with live `STATE.md`, preserving the exact old question and deferred D076 question. At closeout update `research/FINDINGS.md`, `FAILED_HYPOTHESES.md`, `PROOF_OBLIGATIONS.md`, `DECISIONS.md`, the live `STATE.md` **with exactly one next action**, and a matching handoff. If the theorem is accepted, the next unstarted frontier is compatibility of arbitrary multiple-center sections, not an automatic successor.

Classify **ACCEPT / REVISE / REJECT / INCOMPLETE** for each theorem level (exact bridge obstruction, direct H family, Q macro and repeated composition), plus a single overall disposition and **CONTINUE / ADVANCE / PIVOT / REVISE** strategic decision. Report full parameters and why the project gained original-graph structural coverage. Screen publication contents, commit/push **only LCL** without routine force, verify local HEAD, actual remote main, clean tree, hashes, and matching handoff. STOP after this one task. Do not execute any successor or enlarge bounds automatically.
