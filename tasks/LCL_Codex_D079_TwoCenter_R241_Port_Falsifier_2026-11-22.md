# Codex bounded task — R241 two-center pair: fixed-port falsifier and menu controls

**Proposed task:** `LCL-R241-TWO-CENTER-PORT-001` (D079 candidate; do not preassign a scientific disposition).  
**Expected LCL parent:** `abd43466e1333e8c3f792a7e2109fa6cbaed418c`; verify live `main` locally and on GitHub before any file mutation.  
**Upstreams:** MDL `858a8c1fcfda87ba40bb1adee498a6131504a803`; Bounded Search `e48b94eec4091b4fe189e325cab2eda464409943`, both read-only.  
**Task status:** proposal for one new owner-approved bounded scope decision; not automatically authorized by the roadmap.

## A. Context, exact target and hypothesis

Read `AGENTS.md`, live `STATE.md`, `docs/REPOSITORY_CONTINUITY.md`, `research/R241_PAIRED_BRANCHED_SPINE.md`, accepted R241 source and its offset-sensitive join, the D078 evidence/reviews, `research/FINDINGS.md`, `research/PROOF_OBLIGATIONS.md`, `research/FAILED_HYPOTHESES.md`, `research/DECISIONS.md` and latest matching handoff. Record expected graph, source/raw hashes and both local/remote Git identities. Preserve the D078 theorem and the deferred D076 zero-host investigation.

Investigate **exactly** the live selected next supplier interface on the original named pair `[[a,b],[c]]` with a,b,c positive. Its spine vertices are `s:0,s:1`; `s:0` has two distinct center vertices `b:0:0,b:0:1` with a and b indexed terminals, and `s:1` has center `b:1:0` with c indexed terminals. No extra edges, identifications, auxiliary connectors or quotienting. The order is `N=a+b+c+5`. For the R241 orientation forced by the prescribed low entrance `L=s:0` and high exit `U=s:1`, the low class has size `P=a+b+2`, with low names `s:0,b:1:0` and both first-section terminal groups. High names are `s:1,b:0:0,b:0:1` and the second-section terminal group. The strict proposed universal supplier demands an independently constructed alpha state `A(N,P;1,1)`, namely `f(s:0)=1`, `f(s:1)=P+1`, for **every** positive triple a,b,c.

This task attempts to **falsify that strict universal port claim on the smallest exact input**, while preserving alternative physical offset states as possible successors. No claim of nongracefulness is permitted.

## B. Candidate analytic falsifier — independently challenge it

For `(a,b,c)=(1,1,1)` the original tree has eight named vertices and seven actual edges. Its low labels are 0,1,2,3 and highs 4,5,6,7, with prescribed `s:0=1,s:1=5`. The free low names `b:1:0,l:0:0:0,l:0:1:0` receive `{0,2,3}`; the free high names `b:0:0,b:0:1,l:1:0:0` receive `{4,6,7}`.

A proposed elementary contradiction uses the required difference 7:

- If high label 7 is at the second-center terminal `l:1:0:0`, its only possible low neighbor 0 is the actual center `b:1:0`. Then the first two centers have labels 4 and 6; `s:0--(high 6)` and `s:1--(low 0)` both weigh 5.
- Otherwise high label 7 must be at one of the first-section centers, and its own terminal must be low 0. The original attachment from `s:0=1` weighs 6 and its terminal edge weighs 7. If the other first-section center has label 4 (leaving second terminal high 6), the second terminal edge has weight 3 or 4, already taken by an attachment/spine edge. If the other first center has label 6 (leaving high second terminal 4), its terminal at low 2 repeats the spine's weight 4, while low 3 forces the second center low 2 and duplicates weight 3 on the first-center terminal and `s:1--b:1:0`.

Check all physical incidences and each branch of this reasoning without relying on the claimed conclusion. If correct, it proves the strict all-positive-quotas `(1,1)` offset module impossible, **not** the unpinned graph nongraceful. If wrong, preserve a complete counterexample labeling and correct the argument.

## C. Independent positive controls and exact enumeration

**Same original with a different physical exit offset:** For `[[1,1],[1]]`, check the following complete normalized labeling, with actual `s:0=1,s:1=4`: `b:0:0=7`, `l:0:0:0=0`, `b:0:1=6`, `l:0:1:0=2`, `b:1:0=3`, `l:1:0:0=5`. Its edges should give the exact differences `[1,7]`; its R241 offsets are `(x,y)=(1,0)`, not `(1,1)`.

**A neighboring positive strict-port pair:** For `[[1,1],[2]]`, check `s:0=1,s:1=5`, `b:0:0=8,l:0:0:0=0`, `b:0:1=7,l:0:1:0=2`, `b:1:0=3,l:1:0:0=4,l:1:0:1=6`. This independently supplies `A(9,4;1,1)` for this one named graph only. It is not proof for all quotas.

After the analytic argument, use one small CPU-only standard-library enumerator for corroboration, with every named vertex distinguishable. Exhaust **exactly** the 36 pinned alpha assignments for `[[1,1],[1]]`; independently count all 576 alpha-orientation assignments on that same graph to verify alternate-port supply; and exhaust the 144 strict-port alpha assignments for `[[1,1],[2]]`. No automorphism quotient, no hidden root normalization, no solver calls, no other profiles. Expected diagnostic counts to challenge are respectively 0/36, 4/576 unpinned total, and 4/144 strict positive; discrepancies require mathematical and implementation review and retention of the raw corrected record. Distinguish independently verified finite counts from the analytic universal-domain falsifier.

Use unchanged original-bound graceful verifier on each saved positive certificate, bound both originals to separate graph digests and their labelings to ledger IDs, and include an actual deliberately wrong-digest rejection. An offset mismatch is an R241-interface rejection, not necessarily a graceful-checker failure. Reconstruct named graph edges in the independent arithmetic auditor without importing the producer or production graph model. Preserve all original branch/terminal indices and multiplicities.

## D. Execution bounds and STOP conditions

One CPU worker; Python project-local 3.12/3.13; zero external dependencies installed; zero solver calls; at most 800 complete named labeling assignments across the three declared diagnostic enumerations (36+576+144=756); at most 30 **combined measured process-CPU seconds**, including setup; at most 2 MB per record and 6 MB total new evidence. Two positive controls, one checker adverse probe, one R241 offset-premise rejection. Run one official producer + independent auditor sequence, no automatic retries, larger budgets, extra original profiles, inferred quotient counts or broad scanning. Retain all inputs, command receipts, raw result/certificate/graph hashes, audit and complete/INCOMPLETE status, exact source/runtime identities. Any exceeded cap or failed preflight means STOP and record INCOMPLETE rather than rerun.

Separate read-only mathematical and implementation AI reviews must challenge the proof, enumeration completeness, port semantics, original checker's unchanged behavior and evidence custody. Classify `ACCEPT` only the proposition actually established; `REVISE` or `REJECT` unsupported claims and preserve falsifiers. A failure for the fixed `(x,y)=(1,1)` module **must not** be broadened to every physical port, every alpha labeling, arbitrary non-alpha labelings or nongracefulness of any lobster.

## E. Authoritative closeout and continuity

Update `research/FINDINGS.md`, `research/FAILED_HYPOTHESES.md`, `research/PROOF_OBLIGATIONS.md`, `research/DECISIONS.md`, `STATE.md` and one matching final handoff. Preserve the accepted D078 source, immutable roadmap, deferred D076 task, protected upstream refs, baseline tag, historical files and prior INCOMPLETE receipts. If the strict fixed-port claim fails, the logically next **proposed** obligation is a physically compatible offset-menu or alternative composition for multi-center sections; do not execute it. Record that a positive offset (1,0) at one small original does not by itself supply a composable arbitrary-length menu. No production checker changes, source-history rewrites, paid services or installations.

Synchronize only the authorized LCL repository. Verify local HEAD, clean working tree, actual GitHub `main`, source hashes and matching handoff, then **STOP**. Do not begin a successor.
