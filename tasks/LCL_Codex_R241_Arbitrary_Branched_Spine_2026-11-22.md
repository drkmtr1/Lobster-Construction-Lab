# Codex one-task authorization packet — R241 original-spine repeatable two-section modules

**Proposed task ID:** `LCL-R241-PAIRED-BRANCHED-SPINE-001`  
**Status:** NEW PROPOSAL, **UNEXECUTED**; once the owner gives this file to Codex as a new bounded scope decision, it authorizes **only this task**.  
**Starting LCL Git main:** `39d4387c32f7b01e0b8b09d72e6bf1ee85ae3001` (recheck live HEAD and actual remote main at intake).  
**Pinned upstream MDL:** `858a8c1fcfda87ba40bb1adee498a6131504a803` (READ-ONLY).  
**Pinned MDL Bounded Search:** `e48b94eec4091b4fe189e325cab2eda464409943` (READ-ONLY).  
**Scientific source:** `references/upstream/mdl/N241_relational_ports.md`, accepted actual R241 connector/join, plus `research/B2_NONADJACENT_CONSUMER.md` and D067 original-path transfer.  
**Companion full research plan:** `LCL_Branched_Spine_Research_Roadmap_2026-11-22.md` (attachment, do not pretend it is already a repo file).

## A. Authority and preflight

1. Read live `AGENTS.md`, `STATE.md`, `docs/REPOSITORY_CONTINUITY.md`, `research/FINDINGS.md` and `research/PROOF_OBLIGATIONS.md`, most recent handoff `handoffs/CODEX-20261122-b4-d075-direct-2322-alpha-s4-10.md`; source/premise R241 and accepted path consumer; D076 proof, audit, reviews and source/runtime hashes. Check `git status --short`, HEAD, upstream pins, baseline tag, and **actual** GitHub main (not just origin tracking).
2. **Strategy-change reconciliation comes FIRST.** The live D076 selected action is a distinct direct 2322 zero-host seed. Explicitly mark it **DEFERRED / NOT EXECUTED**, preserve its old literal text in the scientific handoff/decision record, and update `STATE.md` and a matching preliminary handoff to select this single new G0 task and why. Do not claim that the chat or the roadmap edited the repo. If the expected Git state or source identity differs materially, STOP for review rather than force sync.
3. No edits to either upstream, no installations, paid services, security changes or production checker modifications. Do not launch an automatic next task. No Git publication until complete evidence screening and review.

## B. One falsifiable mathematical claim

For any integer n>=1, positive integers a_0,...,a_(n-1), and L>=2, let the exact original named tree be

```
[[a_0],[a_1],...,[a_(n-1)]] + [[]]*L
```

with exactly one center b:i:0 at every initial physical spine vertex s:i, and named terminal leaves l:i:0:j only on that center. Prove, revise or reject that a normalized alpha labeling on the n-section original prefix is independently supplied with **outgoing physical s:(n-1) high offset y=1**, and that the accepted nonadjacent consumer gracefully completes all L empty suffix sections on the full original. The prefix must have labels `[0,N-1]`, differences `[1,N-1]`, low size P, outgoing `f(s:(n-1))=P+1`. After shifting highs by L, it must leave exactly

```
R=[P,P+L-1]; D=[1,L]; port s:(n-1)=P+L+1.
```

Also audit the candidate stronger **even-n** version with nonnegative a_i (where a_i=0 means an **actual direct leaf center**, never a missing center `[]`), and odd-n with a_0>=1 and other a_i>=0. Keep all domains disjoint in the claim ledger. Do not infer odd-n a_0=0 or multiple centers.

## C. Concrete supplier templates to challenge

**Two-section module M(a,b), a,b>=0:** on two consecutive original spine positions i,i+1 with one center each, p=a+2 and order N_M=a+b+4:

```
s:i=1;
s:(i+1)=p+1;
b:i:0=p;
l:i:0:j=j+2, 0<=j<a;
b:(i+1):0=0;
l:(i+1):0:j=p+2+j, 0<=j<b.
```

Prove exactly `A(N_M,p;1,1)` on the **original named graph**: all original labels and edge differences bijective, each edge crosses the cut, actual incoming `L=s:i` and outgoing `U=s:(i+1)`, witness path `L--U` and all terminal distances<=2. In particular verify the empty edge-weight bands for a=0 or b=0.

**Odd-length starter S(a), a>=1:** on the original single-section star set `b:0:0=0`, `s:0=2`, first terminal `l:0:0:0=1`, and other terminal `l:0:0:j=j+2` for 1<=j<a. Prove exactly `A(a+2,1;0,1)` with physical `L=b:0:0` and `U=s:0`; the actual witness is L--U.

**Accepted R241 composition:** existing aggregate B ends at physical `U_B=s:(i-1)` with y_B=1. Independently supplied next two-section module A has `x_A=1` at physical `L_A=s:i`. Join **only the actual original spine edge** `s:(i-1)--s:i`. Use the precise source formula, with N_A=|V(A)| and P_B the earlier low size:

```
F(A vertices) = f_A + P_B
F(B-low)      = f_B
F(B-high)     = f_B + N_A.
```

Prove label blocks disjoint and exhaustive, A original differences `[1,N_A-1]`, connector difference N_A and old B differences `[N_A+1,N_A+N_B-1]`; return physical `L_B,U_A` with normalized high exit offset 1. Induct over all n, including n=1,2, odd/even start, empty tail L=0 prefix, and n>=1 with L>=2. Explicitly derive `P=sum_(j even)(a_j+2)` for even n and `P=1+sum_(j odd)(a_j+2)` for odd n, where j ranges over initial section indices.

**Original nonadjacent path completion:** shift all prefix highs by L, not lows. Confirm used label and difference blocks, exact R,D, final physical port, the actual suffix edge set and the L-decreasing C_L recurrence including its reflected bridge. Build no non-original connector and make no whole-solution-prefix inference. State that L=1 fails this exact consumer; do not claim its tree is nongraceful.

## D. Fixed diagnostic grid, controls and independent audit

Perform at most the following **nine** complete named-target checks (one certificate each); seed/module checks may reuse the same target data without counting a new original. Treat each line as a separate original graph identity, even if an isomorphic graph exists elsewhere.

| ID | Initial branch terminal sizes a_i | L trailing empty sections | Purpose |
| --- | --- | ---: | --- |
| T1 | [1] | 2 | S(a), odd base, K=2 recurrence |
| T2 | [2,3] | 2 | Single M, unequal quotas |
| T3 | [1,3,2] | 2 | S plus M, odd join |
| T4 | [2,3,2,2] | 2 | Previously missing B4 K=1 original; see explicit ledger |
| T5 | [2,3,2,2] | 3 | Compare D076 graph; distinct labeling ledger on same original |
| T6 | [2,3,1,4,2] | 2 | Two joins after S, odd length |
| T7 | [2,4,1,3,5,2] | 3 | Three pairs, nonuniform; recursive C_3 |
| T8 | [7,1,2,4,3,1,5] | 5 | Multiple odd joins, recursive C_5 |
| T9 | [0,2,3,0,1,4,0,5] | 4 | Even-n zero-quota direct-leaf extension; `[0]` not `[]` |

**Positive exemplar for T4 (independent starting diagnostic, not Codex evidence until rechecked):**

```
spine s:0..s:5 = [1,15,5,11,9,8]
b:0:0,l:0:0:0..1 = [14,2,3]
b:1:0,l:1:0:0..2 = [0,16,17,18]
b:2:0,l:2:0:0..1 = [10,6,7]
b:3:0,l:3:0:0..1 = [4,12,13]
```

Independently regenerate named original incidences **directly from profiles**, not from the constructor's mutated graph. Verify full graph identity, vertex/edge counts, label bijection `[0,m]`, exact multiset of actual differences `[1,m]`, witness/distances, physical port at all intermediate R241 boundaries, and exact R/D before suffix completion. A graph digest alone is not a label ledger ID; bind sorted named labels separately. Check precise prefix ports before and after each join. Preserve D076's different co-original labeling without changing or replaying its proof.

**Adverse controls (exactly three, no new graph identities):**
1. Misassign the physical connector between wrong spine vertices and require original-graph identity rejection.
2. Supply a wrong incoming port value (x_A!=y_B) to the R241 premise and require scoped applicability rejection; do not claim the resulting tree nongraceful.
3. Corrupt D (e.g. remove difference 1 from the L=2 inventory) and require exact original-path resource predicate rejection.

**Independent audit** must use fresh standard-library arithmetic and separate topology generation; no producer/production verifier imports. Compare the unchanged original-bound production checker to the auditor for every complete certificate. Require **separate read-only mathematical and implementation reviews** of proof and actual code/evidence. If a reviewer finds an error, record correction before execution or preserve changed-version identity and reauthorize, never silently modify frozen inputs.

## E. Hard budget and STOP conditions

- **One declared task, one Python 3.12/3.13 CPU worker.** No solver/DFS/SMT/CP-SAT feasibility calls; **zero** enumerated assignment nodes; no GPU, paid API or new package installation.
- **Nine declared full named target checks at most (T5 reuses the retained D076 original; no duplicate new graph identity)**, three in-memory negative controls, plus only necessary module/seed arithmetic checks on the same records; no historical replay. No automatic retries or scope escalation.
- **30 seconds aggregate process CPU** for the official bounded verification, 2,000,000 bytes maximum per record, **10,000,000 bytes total** evidence cap. If exceeded or interrupted, status `INCOMPLETE`, preserve partial outputs and STOP.
- Preserve exact input/profile, original-edge order, named vertices, physical ports, alpha partitions, used and unused R/D, execution/source/runtime identities, reviewer objections and raw receipts. Version algorithm changes and failures. Do not modify the original-graph verifier or accepted proofs, corrections or incomplete records.
- **Success:** quantified theorem proved from independently supplied S/M and R241 + accepted consumer; all declared certificates and controls pass; both reviews ACCEPT. **Falsifier:** find any original graph/incidence, label, difference, witness, offset, or resource mismatch and REVISE/REJECT as justified; preserve counterexample. **INCOMPLETE:** evidence budget/interruption/failed guard not exhaustion. The finite grid cannot substitute for arbitrary-n induction.
- Update `research/FINDINGS.md`, `FAILED_HYPOTHESES.md`, `PROOF_OBLIGATIONS.md`, `DECISIONS.md` as applicable; update `STATE.md` to terminal disposition and **exactly one proposed unstarted successor** determined by the accepted/rejected scope. Create a matching detailed handoff. Screen complete publication contents, synchronize **LCL only**, check actual GitHub main and local HEAD and clean status, verify protected upstream pins and baseline tag, then **STOP**; do not execute the next task.

## F. Long-term interpretation (not new authorization)

If ACCEPT, the next valuable missing structure is **multiple branch centers on one spine vertex**, then arbitrary direct leaves/empty sections, and ultimately non-alpha original-tree transformations. Do not launch these successor tasks automatically. **Project instructions: KEEP for now**; after acceptance, independently evaluate whether the general arbitrary-length theorem changes the bottleneck sufficiently to justify a fully rewritten, <8,000-character Project charter under the v7 freshness rule. Only the owner can change Project settings.
