# Independent Codex acceptance review: B2 integration

**Date:** November 21, 2026, Pacific/Honolulu. **Reviewed revision:** `2cfb2df708345572e5340a2b889fc1d64674fc87`. **Last previously accepted baseline:** tag `lcl-v0.1.0-baseline`, commit `36ea1603602491bf3c1c5b81ed4c23aaa2210e70`. The reviewed revision includes `6d0f8d2`, `0f0a39c`, `5fb2fa1`, `2cc3cc0` and the closeout `2cfb2df`. This review accepts the identified revision's scoped work; the later commit containing this review records the decision and cannot name its own SHA.

**Independence and limits:** Two fresh, separate Codex reviewer sessions independently inspected the original mathematics and actual named target; a third separately inspected the checkers, evidence and change history. They did not author the OpenChamber checkpoints or the preceding Codex closeout and did not inherit the prior closeout chat; each did receive project instructions and its assigned review task. They are AI reviewers, not human peer reviewers or independent proof assistants; separate sessions do not establish independent model families. The integrating Codex cross-checked their reasoning and wrote this decision. No claim of formal verification, historical novelty, or universal lobster gracefulness follows.

## Dispositions

| Item | Decision and exact scope |
|---|---|
| Restricted seed `B2-UNEQUAL-SEED-001` | **ACCEPT.** The exact named eight-vertex graph `[[1],[2],[]]`, low A=`{s:1,b:0:0,l:1:0:0,l:1:0:1}` bijectively `0..3`, high B=`{s:0,b:1:0,l:0:0:0,s:2}` bijectively `4..7`, and actual port pin `h(s:2)=4` have no graceful labeling. No root pin, symmetry/automorphism or complement quotient. This says nothing about the unrestricted graph or ordinary nongracefulness. |
| All-K high-side shift | **ACCEPT as a conditional identity only.** For a hypothetical seed meeting precisely the above premises and every integer `K>=1`, the stated transport and existing path consumer work on the original B2 target. The premise is false, so this gives no supplier and discharges no unequal-family P07. |
| Interval/adjacent-port obstruction | **ACCEPT.** For `q=1,r=2,z0=z1=0,K>=6`, no injective labeling of the actual eight-vertex prefix returns exactly `[ell,ell+K-1]`, differences `1..K`, and physical port `ell-1` or `ell+K`, for any ell or side; no initial alpha assumption or root pin. This is an interface obstruction, not a nongracefulness theorem. Six is sufficient; sharpness is not established. |
| Finite K=1 witness | **ACCEPT** the existing `q=1,r=2,K=1,ell=1`, above-side witness as a verified finite solver-derived example, not an independent supplier. `K=2..5` are not adjudicated in this review. |
| Superseded p=5/6/7 pin sweep | **ACCEPT** supersession as a repair of the unchanged all-positive-K adjacent-port construction; it remains unexecuted. A different finite classification task is not decided by this disposition. |
| Earlier metadata and descriptions | **REVISE, completed in `2cfb2df`.** Old manifest path prefixes, archive identities, overbroad smaller-K summaries and the historical checker replay description were corrected; previous records and failures remain preserved. The original 33 successful entries are 31 predicates and two informational raw-config observations; config contents are separately tested. |
| Historical and portable custody checkers | **ACCEPT for their documented custody scopes**, not as solvers, negative certificates, provenance authentication or theorem proofs. The old checker requires external inputs and overwrites its old output if rerun; it remains untouched. The new checker inspects tracked payloads, canonical identities and source bytes, and creates a new output exclusively. Its attributes predicate checks declarations; actual Git attributes were separately checked. Its mutable manifest is not an external signature. Independent adverse tests reported with the external review are retained in the closeout packet. |
| Core algorithms, verifier, pruning, symmetry and configurations | **ACCEPT as unchanged from the already accepted baseline:** Git comparison shows no changes under `lcl/`, `tests/`, `configs/`, `examples/`, or `scripts/`, nor to package/dependency files. No new solver, target, pruning, symmetry or original-target verifier was introduced. Acceptance of the separate custody script has only the limited scope above. |
| Handoff overlay, `/runs/` ignore correction, scoped Git attributes and continuity changes | **ACCEPT as operational provisions**, not mathematical results or proof of live service behavior. Root runs remain ignored; curated nested evidence remains tracked; exact evidence byte rules and later continuity changes are retained. A commit or push is not mathematical acceptance. |
| Claims beyond scope | **REJECT** any inference that the restricted negative is an unrestricted nongraceful graph, that the false-premise transport is an independent supplier, or that the nonadjacent-port candidate has a proof or matching seed. These are rejected inferences, not allegations that the current records assert them. |

## Seed proof and targeted independent enumeration

The seven actual edges are `s:0--s:1`, `s:0--b:0:0`, `b:0:0--l:0:0:0`, `s:1--b:1:0`, `b:1:0--l:1:0:0`, `b:1:0--l:1:0:1`, and `s:1--s:2`. Each crosses the declared cut. With the port pinned to 4, a difference 1 must use `s:1--s:2`, forcing `h(s:1)=3`. Writing `a=h(s:0)`, `b=h(b:1:0)`, `x=h(b:0:0)`, the sum of the seven differences is `a+2b-x+10`; gracefulness requires 28. The only admissible `(a,b,x)` with `a+2b-x=18` are `(5,7,1)`, `(6,7,2)`, `(7,6,1)`. Each of the two named leaf orders for every triple duplicates difference 4. This is an analytic proof on the actual target and restrictions.

One separate reviewer independently ran the following in-memory Python 3.13.17 standard-library check once, with no project imports, files, symmetry quotient, solver, successor task or pin sweep. It exhausts `4! * 3! = 144` named assignments. Aliases: `s0=s:0`, `s1=s:1`, `s2=s:2`, `b0=b:0:0`, `b1=b:1:0`, `c=l:0:0:0`, `u=l:1:0:0`, `v=l:1:0:1`.

```python
from itertools import permutations
from collections import Counter
A=('s1','b0','u','v')
B=('s0','b1','c')
E=(('s0','s1'),('s0','b0'),('b0','c'),('s1','b1'),('b1','u'),('b1','v'),('s1','s2'))
counts=Counter(); triples=Counter(); bad_identity=0
for low in permutations(range(4)):
  for high in permutations((5,6,7)):
    h=dict(zip(A,low)); h.update(zip(B,high)); h['s2']=4
    dif=[abs(h[x]-h[y]) for x,y in E]; counts['assignments']+=1
    counts['has_one']+=1 in dif
    counts['y3']+=h['s1']==3
    counts['graceful']+=set(dif)==set(range(1,8))
    a,b,x,y=h['s0'],h['b1'],h['b0'],h['s1']
    bad_identity+=sum(dif)!=a+2*b-x-2*y+16
    if y==3 and sum(dif)==28:
      triples[(a,b,x)]+=1
      assert dif.count(4)>=2
print('counts:',dict(counts),'general_identity_errors:',bad_identity,'sum_28_y3_triples:',dict(triples))
for K in range(1,51):
  vals=[K+4]+[4+(j-1)//2 if j%2 else 4+K-j//2 for j in range(1,K+1)]
  assert set(vals[1:])==set(range(4,K+4))
  assert [abs(vals[i]-vals[i-1]) for i in range(1,K+1)]==list(range(K,0,-1))
print('path formula checked K=1..50')
```

Observed output: 144 assignments, 36 with difference 1, 36 with `s:1=3`, zero graceful assignments, zero general-identity errors, and two named assignments for each of the three triples. The finite K=1..50 path-formula check is supplemental; the all-K conclusion rests on the algebraic path-consumer proof, not a finite sample. Historical DFS and permutation-oracle records are preserved under `evidence/reviews/B2_UNEQUAL_SEED_001/raw/`; their respective exhaustion counts are 65 DFS nodes and 5,040 direct permutations, with 144 domain-admissible and zero graceful.

## Conditional shift and interface proof

If the nonexistent seed `h` existed, leaving A unchanged and adding K to B would use labels `0..3` and `K+4..K+7`, change every original prefix difference by exactly K, and leave labels `[4,K+3]`, differences `1..K`, and physical port `K+4`. The original K-edge path is the only remaining topology; the separately proved alternating endpoint consumer uses each remaining label and difference exactly once. The false antecedent is essential.

For the obstruction, a hypothetical prefix uses difference `K+7`; thus labels `0,K+7` are assigned and `1<=ell<=7`. The assigned labels form blocks `[0,ell-1]` and `[ell+K,K+7]`, each spanning at most six. Since every prefix difference is at least `K+1>=7`, every actual edge crosses blocks. Connectivity fixes the bipartition up to exchange; both classes have four vertices, hence `ell=4`. Subtract K from high labels: all seven actual differences become `1..7`. On the above side the physical `s:2` is high and compresses to 4, producing the forbidden seed directly. On the below side it is low and remains 3; complementing by `7-g` preserves differences and yields the forbidden seed with port 4. This complement is a proof map, not a counting quotient.

For the saved K=1 witness, the retained original graph has `s:0=4,s:1=8,s:2=2,s:3=1,b:0:0=6,l:0:0:0=3,b:1:0=0,l:1:0:0=5,l:1:0:1=7`. Its prefix differences on the listed edges are `4,2,3,8,5,7,6`; the original suffix edge adds 1. Labels are exactly `0..8`, unused prefix label/difference are both `{1}`, and the port is 2. Source record: `evidence/validation/release_final/pilot/cases/31da62597181ea39545cd89689e591113261ea7c9c7af56e60383894da947a57.attempt-0001.json`.

## Evidence and outstanding duty

The independent external report at `evidence/reviews/B2_INTEGRATION_CLOSEOUT_20261121/ACCEPTANCE_REPORT.md` reviewed export `5fb2fa1`, not the live Windows checkout. The subsequent local closeout's 72/72 result is `evidence/reviews/B2_UNEQUAL_SEED_001/custody_check_codex_20261121T211900Z.json`. These are source-identity and custody checks, not theorem proofs. Exact archival and historical hash qualifications are in `handoffs/CODEX-20261121-b2-integration-closeout.md` and D017. The earlier proof bodies and historical handoffs remain available without rewriting their original statuses.

The unequal independent supplier remains open. A nonadjacent-port consumer for an explicit K-domain and an independently supplied compatible prefix are separate unproved duties. No successor research or superseded pin sweep was initiated in this review.
