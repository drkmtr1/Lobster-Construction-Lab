# LCL — D081 one-task mathematical authorization: unequal two-center port return

**Proposed task ID:** `LCL-R241-UNEQUAL-TWO-CENTER-RETURN-001`  
**Status:** PROPOSED / UNSTARTED. This packet authorizes no task until the owner supplies it to Codex as the bounded scope decision.  
**Expected LCL starting HEAD:** `0841a681219a4445741265998ddbeb1ffc57e38d`; verify live local HEAD, actual remote `main`, clean worktree, and any newer handoff. **STOP on material divergence** rather than overwriting state.  
**Protected upstream pins (read-only):** MDL `858a8c1fcfda87ba40bb1adee498a6131504a803`; Bounded Search `e48b94eec4091b4fe189e325cab2eda464409943`.  
**Source theorems:** `research/R241_PAIRED_BRANCHED_SPINE.md` (D078), `research/R241_TWO_CENTER_PORT_FALSIFIER.md` (D079), `research/R241_ZERO_TO_ONE_BRIDGE.md` (D080), `references/upstream/mdl/N241_relational_ports.md`, `research/B2_NONADJACENT_CONSUMER.md`, and the committed strategic roadmap.

## A. One bounded scope decision and hypothesis classification

The **live selected action** is to investigate the exact original `[[1,2],[1]]` at physical offsets `(1,0)`, with the actual low entrance `s:0` and high exit `s:1`, as a potential replacement for D080's fixed first pair. **Adjudicate that exact question first.** The extension in this single task is to challenge a concrete analytical replacement supplier `F(b)=[[1,b],[b]]` and its mathematically immediate composition with the D080 accepted bridge `H(a)=[[a],[a+1]]`. Do not call these new candidates accepted before separate reviews. Record this one-task scope adjustment in `STATE.md` and the matching intake/handoff before execution, preserving the former question verbatim.

Define a normalized alpha state `A(N,P;x,y)` with a vertex-label bijection to `[0,N-1]`, original-edge-difference bijection to `[1,N-1]`, low labels `[0,P-1]`, high labels `[P,N-1]`, physical low entrance `s:0=x` and high exit `s:1=P+y`, plus a witnessing original path and distance-at-most-two property. Preserve each named center and indexed terminal. `[[1,0],[0]]` retains two physical direct-leaf centers; `[0]` is not `[]`.

## B. Analytic falsifier for the live question

For the exact original `G=[[1,2],[1]]` there are nine vertices and eight edges, with low size `P=5` under the orientation `s:0` low, `s:1` high. Pin `(x,y)=(1,0)`, i.e. `s:0=1`, `s:1=5`. Let `A=f(b:0:0)`, `B=f(b:0:1)`, `z=f(b:1:0)`. Since all edges cross the alpha cut, the weighted-degree sum is

`sum_edges |f(u)-f(v)| = 19+A+2B-z = 1+...+8 = 36`, hence `A+2B-z=17`.

The high labels `A,B` are two distinct members of `{6,7,8}` and `z in {0,2,3,4}`. The only count-admissible triples `(A,B,z)` are `(6,7,3)`, `(7,6,2)`, and `(8,6,3)`.

* In the first two cases, the only vertex labeled 8 is the section-one terminal, whose neighbor is `z=3` or `z=2`, so its edge difference is 5 or 6, not 8. The unique difference 8 (requiring adjacent labels 0 and 8) is missing.
* In the third case, difference 8 forces the section-zero first terminal (`l:0:0:0`) to be zero, adjacent to `A=8`. The two indexed terminals at `B=6` must use the remaining low labels 2 and 4, creating difference 4 on the edge from `B=6` to the terminal labeled 2. The actual spine edge `s:0--s:1` already has difference 4. Contradiction.

Challenge the signed sum, the three cases and the actual edges independently. This would reject **only** fixed `(1,0)` supply on `G`, not ordinary gracefulness or other physical ports. At zero batch there is no leaf operation to discuss.

### Exact positive controls

1. **Same graph, alternate offsets `(2,0)`.** On `[[1,2],[1]]`, use:
   `s:0=2,s:1=5; b:0:0=7,l:0:0:0=3; b:0:1=8,l:0:1:0=0,l:0:1:1=1; b:1:0=4,l:1:0:0=6`. Its original edge differences are exactly `[1,8]` once each and its low labels `[0,4]`.
2. **Neighbor with strict `(1,0)`.** On `[[1,2],[2]]`, use:
   `s:0=1,s:1=5; b:0:0=9,l:0:0:0=0; b:0:1=8,l:0:1:0=2,l:0:1:1=3; b:1:0=4,l:1:0:0=6,l:1:0:1=7`. Its original edge differences are exactly `[1,9]` once each and its low labels `[0,4]`.

The author's exploratory nonquotiented counts, **not yet accepted evidence**, are: `[[1,2],[1]]` at `(1,0)`: `0/144`; same original at `(2,0)`: `2/144`; `[[1,2],[2]]` at `(1,0)`: `4/576`. Record actual independent counts and factorial-rank coverage; stop if discrepant. The 144+144 cases on the same named graph overlap in graph identity but have distinct pinned label domains.

## C. Candidate independent supplier for all nonnegative b

For exact integer `b>=0`, define **F(b)** on the original `[[1,b],[b]]`, with the first section having centers `b:0:0` (quota one) and `b:0:1` (quota b), and second section having center `b:1:0` (quota b). Let

`N_B=2b+6`, `P_B=b+3`, `m_B=2b+5`.

Assign **all and only** the named vertices:

```
s:0 = 1                        s:1 = b+3
b:0:0 = 2b+5                   l:0:0:0 = 0
b:0:1 = 2b+4                   l:0:1:j = 2+j, 0<=j<b
b:1:0 = b+2                    l:1:0:j = b+4+j, 0<=j<b
```

**Proof challenge:** the low vertices are `s:0,b:1:0,l:0:0:0,l:0:1:j`, using precisely `[0,b+2]`; the remaining high vertices use `[b+3,2b+5]`. Show that the original-edge differences form these complete, disjoint groups:

```
s:1--b:1:0                       {1}
b:1:0--l:1:0:j                   [2,b+1]
s:0--s:1                         {b+2}
b:0:1--l:0:1:j                   [b+3,2b+2]
s:0--b:0:1                       {2b+3}
s:0--b:0:0                       {2b+4}
b:0:0--l:0:0:0                   {2b+5}
```

At b=0 the two indexed ranges are **empty**, and both corresponding centers remain actual original direct leaves. The physical witness is `s:0--s:1`, with all other vertices within distance two. Therefore the **proposed**, not yet accepted, result is `F(b):A(2b+6,b+3;1,0)` for all b>=0. Its b=1 case must be reconciled with D079's retained ledger; its b=2 case supplies the exact neighboring positive control. No full-solution extraction is permitted.

## D. Immediate R241 consequences to prove or reject in this task

D080's **accepted** independent bridge supplies `H(a)=[[a],[a+1]]:A(2a+5,a+2;0,1)` for exact `a>=1`. Place F(b) at original sections 0,1 and H(a) at 2,3; join via the sole original spine edge `s:1--s:2` using adopted R241 with **old aggregate B=F(b), new block A=H(a)**. The actual compatibility equation is `y_B=x_A=0`.

This would give the **candidate** four-section macro

```
R(b,a)=[[1,b],[b],[a],[a+1]]
  A(2a+2b+11,a+b+5;1,1), b>=0, a>=1.
```

Prove the four label bands, the new-block differences `[1,2a+4]`, the connector difference `{2a+5}`, the shifted old-block differences `[2a+6,2a+2b+10]`, the exact original physical ports and witness, and the same-graph identity. A normalized return `(1,1)` would permit **finite repetition of R(b_i,a_i)** with independently chosen parameters. The R241 physical join must always be the actual next spine edge; no connector insertion or named-vertex identification is permitted.

For any finite nonempty macro list, verify exact normalization, low size `P=sum_i(a_i+b_i+5)` and order `N=sum_i(2a_i+2b_i+11)`, physical exit `P+1`. For `L=0` the prefix would already be alpha graceful. For `L>=2` trailing **empty** spine sections, prove used/unused inventories after high shift `R=[P,P+L-1]`, `D=[1,L]`, original exit `P+L+1` and the retained physical path consumer. At `L=1` reject only the shifted-suffix **interface**, whose first required edge would have weight 2 instead of 1. Do not claim arbitrary multi-center profiles, internal empties or a non-alpha theorem.

Optionally compare **interleaving** R(b,a) with the already accepted D078 M(c,d) only if this follows directly from the same R241 offset equality with no extra search or cases. Such an observation is conditional until documented and reviewed. Do not broaden beyond this proof.

## E. Closed validation plan and resource ceilings

- Starting parent and source hashes fixed at intake; no source rewriting or solver installation. Use one CPU worker under project-local Python 3.12/3.13 and **zero solver calls**. One authorized official run, no retries, background processes or new research task.
- At most **900** complete named assignment visits: exactly three products of sizes 144,144,576 for the specified pinned scopes. Do not quotient, exchange named centers, or suppress terminal multiplicity. Archive full visit ranks, a genuine original-edge duplicate for each rejected row, and complete checker certificates for accepted maps. Keep graph digest distinct from ledger ID.
- At most **eight new original graph identities**, counting two-center controls and symbolic construction checks; archived D079 F(1) must be reused by source identity if used. Illustrative checks: F(0),F(1),F(2),F(4), R(2,1), R(3,2), and a two-macro original with L=5. Exact project limits govern and output filenames must be free.
- At most **three adverse checks**: an incorrect expected original digest, an incorrect R241 incoming port, and an incorrect residual difference inventory. All must actually reach the original-bound verifier or physical-state gate and be rejected. Preserve their raw inputs/outputs.
- Maximum **30 combined process-CPU seconds**, **2,000,000 bytes per record**, **8,000,000 total generated evidence bytes**. Stop immediately on any limit. No automatic retries, larger budgets, or successor.
- Separate **read-only mathematical and implementation reviews**: mathematical reviewer challenges signed-degree obstruction, all parameter bands, R241 direction/closure and reflected continuation; implementation reviewer challenges named graph construction, enumeration completeness, source/manifest hashes, integer/domain checks, no hidden quotient, adverse controls and protected changes. AI review is not formal certification.

Record one of ACCEPT / REVISE / REJECT / INCOMPLETE for each claimed scope. A proven fixed-port obstruction must not be labeled a nongraceful lobster. Successful finite witnesses alone are insufficient for all-b/a or all-L claims. Update `research/FINDINGS.md`, `research/FAILED_HYPOTHESES.md`, `research/PROOF_OBLIGATIONS.md`, `research/DECISIONS.md`, live `STATE.md`, the matching `handoffs/` record and immutable evidence. Preserve earlier D078–D080 proofs, the deferred D076 action, baseline tag, both protected upstreams, checker/production files, and historical INCOMPLETE. Verify current local HEAD, clean worktree, actual GitHub remote HEAD, SHA/hash match and publication contents. **STOP after this single task; do not execute the next roadmap gate.**
