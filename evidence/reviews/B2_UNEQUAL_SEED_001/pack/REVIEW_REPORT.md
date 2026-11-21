# Independent review of OpenChamber's B2-UNEQUAL-SEED-001 checkpoint

**Date:** November 21, 2026, Pacific/Honolulu.  
**Reviewed export:** checkpoint `0f0a39c4d8d97d211782d1a1d81aeba5e0481319`, following `6d0f8d23f4f0d9f1d4440f4bfa7a7c5f25051685`.  
**Overall verdict:** accept the exact restricted seed negative and conditional transport; revise evidence preservation, a few descriptions, and the next research plan before closing the local handoff.  
**New finding:** the original interval/adjacent-port objective is impossible for the zero-padding unequal family `q=1,r=2` whenever `K>=6`, even with freely chosen interval position and side.

This is a completed analysis of the supplied export and preserved release sources. It does not modify Will's Windows repository, change its review markers, certify its live Git refs, or start a successor search.

## 1. Decision summary

| Item | Verdict | Meaning |
|---|---|---|
| Prescribed alpha seed with `s:2=4` | **ACCEPT** | The exact eight-vertex named seed has no labeling under the declared domains and pin. |
| Original-edge fidelity and scope | **ACCEPT** | Inputs and both records describe the same seven original edges, with the same physical vertices and explicit restrictions. |
| DFS and oracle evidence | **ACCEPT, with provenance limits** | Records are internally consistent and match the preserved source; the current review independently reproduces the restricted negative. |
| Conditional high-side shift and path consumer | **ACCEPT as conditional only** | The formulas are correct, but their required seed does not exist. No supplier is obtained. |
| Evidence custody and minor reporting | **REVISE** | Track actual evidence bytes, identify the historical scratch error, correct the degree-list typo, and distinguish hash schemes. |
| Pin sweep as a repair of the existing all-`K` construction | **REVISE** | Moving the seed pin does not preserve the adjacent-port interface; the unchanged completion proposal already fails at `K=1`. |
| New `K>=6` interface obstruction | **CONFIRMED in this review** | A full proof and two separate agent challenges establish a stronger scoped result. Local adoption remains for the repository review task. |

The useful outcome is not merely another failed solver run. We now know a precise reason why the selected boundary cannot support the intended unequal all-parameter construction. That guides the next change of assumptions.

## 2. What was actually inspected and verified

Both uploaded ZIPs are byte-identical, with SHA-256

`a2def9c494ff49d7dbe89ca10416b1da804e82052c9a79db773ae50c819e2b97`.

Each contains 21 files: the actual proof note, current research records, handoff and instructions, exact target/pin/domain/limit JSON, both raw run records, reviewer scratch, and Git exports. All supplied bytes are preserved under `supplied/`.

The review read the actual mathematical arguments, not only the Owner report. Three separate agents handled the seed proof, evidence audit, and next-step assessment. The primary reviewer separately wrote and executed a standard-library enumeration using the seven explicit original edges; it imports no LCL solver, constructor, or verifier.

### Current independent replay

The script `independent_seed_check.py` enumerated the full prescribed space:

\[
4!\times3!=144
\]

named assignments. The four low vertices receive all permutations of `0..3`; the three unpinned high vertices receive all permutations of `5,6,7`; `s:2` remains fixed at `4`. No complement or automorphism quotient is used.

**Observed result:** 144 of 144 completed, zero graceful witnesses, 36 assignments with `h(s:1)=3`, zero general sum-identity mismatches, and zero violations of the difference-one forcing claim. The run used CPython 3.12.14 on Linux and took approximately 0.001 seconds for enumeration. Its declared limits were one worker, 144 assignments, two seconds cooperatively, and a 2,000,000-byte result cap. It produced a 55 KB record containing every named assignment and its seven differences.

The script's result is a new acceptance-review artifact, not a rewrite of either historical OpenChamber run. Its exact runtime, environment, input hashes, script hash and all assignments are in `independent_seed_check.json`.

### Record and source checks

Both canonical record hashes and configuration hashes recompute correctly. Both records carry the same source inventory, and all **21 inventoried files** match the preserved v0.1.0 source byte-for-byte. The shared inventory digest is

`2dfe3231007a18f4a74e4c4b49fd4a112ebbb66ef439e711ff59ac11fde7bbfd`.

Independent expansion of the input profile reproduces the named vertices, roles, spine and all seven edges in both records. The graph digest is

`9198e106ce33d9b83b8044e385b1599cfe26cd1fe471f4eec841a461868756b2`.

The code inspection confirms that DFS prunes repeated labels or repeated differences and uses MRV for ordering only. The oracle enumerates the seven unpinned labels before applying domains. Thus its **5,040 = 7! raw permutations** and **144 admissible assignments** are consistent. DFS's **65 nodes** count attempted partial assignments, so they are not another count of complete candidate labelings.

The reported 110 tests with six skips, doctor and demo results are OpenChamber's preflight report. Their stdout and demo record were not included here, so this review does not claim to have witnessed or repeated them. No code semantics changed in the supplied checkpoint; repeating the full release suite or the four completed pilot pairs was unnecessary to resolve the current mathematical question.

## 3. The restricted seed proof is correct

The low class is

`A={s:1,b:0:0,l:1:0:0,l:1:0:1}`,

and the high class is

`B={s:0,b:1:0,l:0:0:0,s:2}`.

All seven original edges cross between them. With low labels `0..3`, high labels `4..7`, and `s:2=4`, difference one can occur only between labels three and four. The sole neighbor of the physical vertex `s:2` in the seed is `s:1`. Therefore `h(s:1)=3`.

Set

\[
a=h(s:0),\quad b=h(b:1:0),\quad c=h(l:0:0:0),\quad x=h(b:0:0),
\]

and let `u,v` be the two leaf labels attached to `b:1:0`. Then `a,b,c` permute `{5,6,7}`, and `x,u,v` permute `{0,1,2}`. In the supplied original-edge order, the differences are

\[
a-3,\ a-x,\ c-x,\ b-3,\ b-u,\ b-v,\ 1.
\]

Their required sum is `1+...+7=28`. Using `a+b+c=18` and `x+u+v=3` gives

\[
a+2b-x=18.
\]

The complete cases are:

| `(a,b,c,x)` | Remaining `{u,v}` | Difference multiset |
|---|---|---|
| `(5,7,6,1)` | `{0,2}` | `{1,2,4,4,5,5,7}` |
| `(6,7,5,2)` | `{0,1}` | `{1,3,3,4,4,6,7}` |
| `(7,6,5,1)` | `{0,2}` | `{1,3,4,4,4,6,6}` |

Both named orders of `u,v` are included. Every case repeats difference four on actual original edges. Hence none can be graceful. This is a finite mathematical proof of the exact restricted impossibility, independently supported by complete computation. It is not a proof that the unrestricted tree is nongraceful.

## 4. The conditional transport is correct, but supplies no family

For a hypothetical seed meeting those restrictions, keeping low labels unchanged and adding `K` to all high labels would give:

| Quantity | Returned value |
|---|---|
| Used labels | `0..3` and `K+4..K+7` |
| Used prefix differences | `K+1..K+7` |
| Unused labels | `[4,K+3]` |
| Unused differences | `1..K` |
| Physical port | `s:2=K+4`, immediately above the interval |

Every prefix edge crosses the low/high split, so every prefix difference increases by exactly `K`. The alternating-endpoint path formula in `PROOF_OBLIGATIONS.md` then assigns the remaining `K` vertices with differences `K,K-1,...,1`, preserving the prefix and terminating after exactly `K` steps.

This is a correct quantified conditional statement. Since the required seed does not exist, it provides no actual supplier. OpenChamber appropriately retained it as conditional and did not implement or promote it.

## 5. Why the proposed pin sweep does not repair the current construction

For another seed port label `p` in `{5,6,7}`, the same high-side shift still leaves

\[
R=[4,K+3],\qquad D=\{1,\ldots,K\},
\]

but the physical port becomes `K+p`. The existing consumer requires `K+4`, exactly one above the interval. Being somewhere above the interval is insufficient to invoke that theorem.

The failure is visible at `K=1` without any search. The only unused label is `4`, and the single suffix edge would have difference

\[
|(p+1)-4|=p-3\in\{2,3,4\},
\]

when it must have difference one. Even a perfectly valid new seed therefore cannot establish the proposed unchanged all-positive-`K` construction.

For larger `K`, merely fitting the first edge within the difference budget requires `K>=p-3`. This is only a necessary condition, not a completion proof. A pin sweep can still be an explicit finite classification task, but its mathematical purpose and consumer obligations would need to be revised first.

The actual next-task document calls its transport suggestion preliminary, which was appropriate. This review now resolves that preliminary suggestion adversely. The issue is P05/P08/P09: the physical boundary, continuation, and quantified domain. It does not invalidate the existing p=4 negative.

## 6. A stronger deduction: the original interface is impossible for every K>=6

The full proof is in `B2_INTERFACE_OBSTRUCTION.md`. Its scope is the exact family `q=1,r=2,z0=z1=0`, the same eight-vertex prefix through `s:2`, unused consecutive labels `[ell,ell+K-1]`, unused differences `1..K`, and port immediately above or below the interval.

The argument does not assume alpha separation in advance:

1. The prefix must use differences `K+1..K+7`, including the maximum `m=K+7`. Hence both labels `0,m` already occur in the prefix, so `1<=ell<=7`.
2. The assigned labels are exactly two nonempty blocks, `0..ell-1` and `ell+K..K+7`. Each block has span at most six.
3. When `K>=6`, every required prefix difference is at least seven. Every prefix edge must therefore connect the two blocks.
4. The connected prefix's bipartition is `4/4`, forcing `ell=4`.
5. Subtracting `K` from the high block gives a graceful alpha labeling of the original seed.
6. An above-side port becomes `s:2=4`, the forbidden seed. A below-side port becomes `s:2=3` in the opposite orientation; complementing labels by `7-h` gives the same forbidden seed.

Thus neither side is possible. Two separate reasoning agents independently challenged the proof and confirmed it. It is a new deduction of this review, not a claim that OpenChamber already ran or established it.

**Practical consequence:** the precise original all-`K` adjacent-port objective is impossible for this unequal family. It should no longer be described merely as an unresolved independent-supply duty. The broader problem of constructing graceful labelings remains separate and is not refuted.

The threshold six is sufficient, not claimed sharp. No conclusion is drawn here about the interface for `K=1,...,5`. The earlier positive `K=1` pilot is consistent with the result. The padded and balanced suppliers remain valid on their separate domains.

## 7. Corrections to make in the local checkpoint

### A. Preserve the actual run records

The checkpoint tracks notes containing the paths and hashes of the two negative runs, while `runs/` is ignored. A path and hash identify bytes but cannot reconstruct them after cleanup or a fresh clone. The uploaded archive now preserves a copy for this review. For the local handoff rule, copy the unchanged records and exact inputs into a tracked evidence directory with an explicit manifest. Keep the historical run files intact.

The source fields in the records are inventories of hashes, not embedded source files. They match the preserved source available here. This review pack also includes the 21 matching source files under `source_snapshot/` for reproducibility.

### B. Preserve and identify the historical scratch diagnostic

The supplied `b2_review_scratch.py` still applies the specialized equation

`S=a+2*b-x+10`

to all 144 assignments. That equation requires `y=h(s:1)=3`. The general equation is

`S=a+2*b-x-2*y+16`.

The original note candidly discloses the resulting 108 apparent mismatches and reports a corrected slice check, but the supplied scratch file is the earlier diagnostic version. Its zero-witness enumeration is unaffected. Preserve it with that explanation, and cite the new independent script and output for a reproducible corrected identity check.

### C. Correct one degree-list typo

In `B2_UNEQUAL_SEED.md`, section 3, Step 3, the parenthesis puts `s:2` on the low side. It is a high-side degree-one vertex, contributing `+4`. The displayed sum already has the correct term, so this is a descriptive correction. A full degree list should include both low-side terminal leaves as well.

### D. State hashes and execution limits precisely

The reported `record_sha256` is the hash of canonical JSON excluding its own field, not a whole-file hash. The audit preserves both schemes. The 2 MB output cap comes from the record writer, not from the four-key limits JSON. `max_states=2000` is present in the shared configuration but is unused by these DFS/oracle runs; it is not their enforced memory cap.

### E. Repair the exported diff without altering original sources

The PowerShell-exported patch contains reversible CP437/UTF-8 character corruption. The directly uploaded Markdown files are intact. The forensic reviewer recovered `analysis/checkpoint.normalized.diff` and reconstructed every changed file from the archived preimages: all eight postimages match exactly, with 246 additions and 27 deletions. No source, checker, or configuration change appears in that patch. The raw export remains preserved.

### F. Reconcile the research direction and one next action

The supplied `STATE.md` leads with the pin sweep while conditioning it on review; the handoff names acceptance review as the immediate action. This does not show a sweep ran, but the immediate action should be stated consistently.

After local acceptance, retain the old pin-sweep proposal as superseded, add the new interface obstruction and its review, and revise the objective to a genuinely different interface. Do not silently delete a failed proposal or rewrite the historical p=4 restrictions.

## 8. Git and provenance boundaries

The supplied text exports identify the baseline `36ea1603602491bf3c1c5b81ed4c23aaa2210e70`, overlay `6d0f8d23f4f0d9f1d4440f4bfa7a7c5f25051685`, and reviewed checkpoint `0f0a39c4d8d97d211782d1a1d81aeba5e0481319`. The content diff and blob prefixes are consistent with the uploaded files.

The bundle does not contain Git objects or refs. Consequently this review does not independently certify the live branch, tag, parent links, clean status, or absence of a push on Will's machine. Local Codex should reconcile the actual checkout and record its acceptance in a subsequent review commit. If the overlay has not already been accepted, review it as part of the intervening changes rather than assuming its status from the session-start label.

The handoff's correction to avoid embedding a commit's own final hash is sensible. Use the externally known reviewed commit hash in the new review record and report the new commit's hash after committing.

## 9. One manageable next action

Give the included `CODEX_REVIEW_AND_RECORD_PROMPT.md` to Codex in the existing project folder. It scopes one local acceptance-and-record task: reconcile the checkout, accept the restricted negative and conditional identity, independently check and record the new obstruction, preserve evidence, correct descriptions, and replace the unsuitable queued direction. It does not authorize a pin sweep or a continuing campaign.

A possible *later* research question is a path-consumer theorem with a nonadjacent port, keeping the interval and difference inventories fixed. For example, offset two above the interval would correspond to the p=5 shift and necessarily requires `K>=2`; an all-positive-`K` construction would also need a separately justified `K=1` branch. No such consumer or matching seed is established here. A quantified consumer hypothesis should be specified before seed search resumes.

## 10. Reproduction and pack contents

From the extracted review-pack directory, run only the independent seed audit if a local replay is useful:

```powershell
python .\independent_seed_check.py --supplied .\supplied --out .\independent_seed_check_local.json
```

Use Python 3.12 or 3.13. The output name must be new; the script refuses to overwrite an existing result. It uses only the standard library and imports no project code. It is deliberately limited to the completed p=4 question, not the queued p=5/6/7 cases. Replaying it is optional; the observed output is already included.

The pack includes the unmodified 21 supplied files, their original ZIP, three independent review notes, the normalized diff, machine-readable evidence audit, independent enumeration script/output, this report, the new theorem note, a Codex follow-up prompt, a matching 21-file source snapshot, and a raw-byte checksum manifest. `README.md` explains the layout. The archive is a review deliverable, not an installer or a replacement repository.
