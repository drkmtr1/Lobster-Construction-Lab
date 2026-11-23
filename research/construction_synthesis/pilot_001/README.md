# Construction Synthesis joint-core pilot

**SYNTH-CATALOG-JOINT-CORE-PILOT-001** indexes existing accepted results on the exact
ordered fourth-size-two family. The pilot records named ledgers and their
interfaces. It carries no new theorem, solver, rule engine, or catalog migration.

## Six named states

| Index key | Source | Named original | Zero | Physical maximum at s:2 | Verified supplied cuts |
|---|---|---|---|---:|---|
| `case-b-22` | D058 | C(2,2) | s:3 | 14 | First, 11, 12, 13 (D059) |
| `case-b-grown-32` | D059 | C(3,2) | s:3 | 15 | First, returned cut 12 |
| `direct-23` | D060 | C(2,3) | s:3 | 15 | First, 6, 12, 13, 14 |
| `alternative-22` | D061 | C(2,2) | s:1 | 14 | First, 7 (D062), second, 13 (D061) |
| `alternative-grown-23` | D061 | C(2,3) | s:1 | 15 | Second, returned cut 14 |
| `nested-34` | D062 | C(3,4) | s:1 | 17 | First, 8, second, 16 |

C(q,r) is the exact named original `[[q],[r],[],[2],[],[]]`. The two C(2,2)
records share a graph digest and differ as assignments. The two C(2,3) records
also share a graph digest and differ as assignments. Each full map retains the
original terminal indices, physical branch hosts, maximum-root name, and spine.
Proof, original, certificate, verification receipt and review identities are
source-linked through the decisions and the SHA-256 byte bindings in the index.

## Eight rule entries

| Rule | Required input | Output and applicability |
|---|---|---|
| `first-case-b` | D058 Case B, first host 2, cut 11, full crossing tail [9,14] | D059 C(q,2), q≥2, with returned cut q+9. |
| `first-direct-23` | D060 direct C(2,3), first host 2, cut 12, full tail [10,15] | C(q,3), q≥2, with returned cut q+10. Its independent seed differs from D061's r-grown example. |
| `second-alternative` | D061 alternative C(2,2), second host 2, cut 13, full tail [11,14] | C(2,r), r≥2, with returned cut r+11. |
| `nested-cuts` | Same D061 alternative C(2,2), both physical hosts 1 and 2 and full tails [6,14] and [11,14] at 7 and 13 | D062 C(q,r) for q,r≥2 with both predicates preserved under arbitrary finite named interleavings. |
| `zero-host-lift` | Named graceful core with m at physical s:2 and no section-2 branch, supplied by one of the indexed proofs | K=1 target for every t≥1 on that supplied domain. |
| `physical-singleton` | Only s:5 withheld after the lift, with sole pending original edge s:4--s:5 | Finish on that edge using the ledger's actual unused label and difference. |
| `retained-q-one` | Exact q=1 parameters supplied by D051's retained selector | Ordinary gracefulness for every positive r,t,K with that selector's resource contracts. |
| `retained-r-one` | Exact r=1 parameters supplied by D043's retained selector | Ordinary gracefulness for every positive q,t,K with that selector's resource contracts. |

A crossing has exactly one endpoint below the cut. Count its original
incidence once. For a host label b below c, the required tail begins at
c−b. For a host at or above c, it starts at b−c+1. The indexed positive
growth rules use the low-host case. Each batch fills the gap at the old
cut and preserves all existing incidences. Proper returned cuts support
further batches with fresh names in their prescribed order. Completed
cores use both full alphabets and carry no pending suffix inventories.

For D062, with h=q−2 and k=r−2, original labels ≥7 gain h and those ≥13 also
gain k. New first terminal j is j+5 and new second terminal j is h+11+j,
starting at j=2 at each host. The five complete edge bands are
[1,5], [6,5+h], [6+h,10+h], [11+h,10+h+k], and [11+h+k,14+h+k].
The returned cuts are 7+h and 13+h+k, with respective tails [6+h,m]
and [11+h+k,m], where m=q+r+10 at physical s:2. First growth shifts
any previously added second terminals. Second growth shifts only the
original two highest vertices. This accounts for pointwise batch
agreement, including empty batches.

The lift translates the core by one, restores original b:2:0 at zero,
and labels its fresh terminal j by m+2+j. The last edge retains the
core difference. The D062 singleton has R={q+9}, D={1}, and s:4=q+8,
with s:5=q+9. D058/D059 supply R={6}, D={2} at s:4=8. The D060
seed and first-growth family supply R=D={4} at s:4=8. The D061
second-growth family supplies R={11}, D={1} at s:4=10.

## Exact coverage and failures

Each atlas row specifies a disjoint integer box. The q=1 and r=1
routes and the D062 interior-q/r route exhaust K=1, including t=1.
For K≥2 the q=1, r=1, or t=1 boundary has a retained supplier.
D037 supplies the t=1 boundary by its adjacent alpha construction.
The region q,r,t≥2 and K≥2 is unproved in this catalog.

D059's two second-host failures attach to the Case B ledger and its
exact c=11 one-leaf output. D060's second-host failure attaches to
its direct C(2,3) ledger. D061's right-zero failure attaches to its
particular top-pair cut-13 plan with s:0=13 and s:2=14. These
dispositions concern those operations or that plan only. The two
historical INCOMPLETE receipts checked in this task retain their status.
The earlier candidates and evidence remain in their original archives.

## Schema and reproducibility

- [index.json](index.json) is schema version 1. Each `ledgers` item binds a
  full name-to-label map and spine to an archived graph and certificate.
  A `ledger_id` is lower-case SHA-256 of UTF-8 JSON
  `{"graph_digest":...,"labels":[[name,label],...]}` with keys sorted,
  pairs sorted lexically by original name, separators comma and colon,
  no extra whitespace and no ASCII escaping. This is distinct from the
  original digest, which identifies named topology.
- `rules` are source-backed records, with literal formulas or selectors.
  Input references identify the specific ledger hash or preceding rule.
  Complete cut spectra use inclusive endpoints and symbolic expressions as
  strings. `resources: null` means no pending-resource interface is exported
  at that stage. A symbolic inverted interval denotes an empty band.
- `failures` record rejected scopes. A null ledger ID identifies a partial
  plan without a completed ledger. `atlas.rows` use axis bounds `[min,max]`
  with null max for an unbounded upper side. A null source and empty route
  mark the unproved box. D037 is a direct proof reference without an extra
  rule record.
- Provenance SHA-256 binds Git blob bytes at the recorded starting commit.
  Manifest entries for the six archived originals/certificates and D058–D062
  proof/review/audit sources are checked. This avoids checkout line-ending
  ambiguities. [audit.py](audit.py) imports no production code. It checks all
  original-edge multiplicities, recalculates differences and crossing sets,
  and checks the retained lift and atlas partition. The audit verifies
  archival arithmetic and bindings. Quantified claims rest on their proofs.

From the repository root, in a disposable checkout with this pilot's exact
input bytes and the starting commit available in Git, leave
`audit_result.json` absent and run this command once with the project-local
Python 3.12/3.13 environment:

```powershell
& .venv/Scripts/python.exe -B -X utf8 research/construction_synthesis/pilot_001/audit.py
```

The audit refuses to replace a receipt. Preserve the published receipt.
Runtime timings can differ between reproductions. See [the receipt](audit_result.json),
[reviews](REVIEWS.md), and [raw-byte manifest](MANIFEST.json).

Primary proofs and their reviews are pinned in the index: [D058](../../B4_JOINT_22_DIRECT_LEDGER.md),
[D059](../../B4_JOINT_22_CUT_COMPAT.md), [D060](../../B4_JOINT_23_MAX_ROOTED_CORE.md),
[D061](../../B4_JOINT_SECOND_CENTER_CUT_READY_22.md), [D062](../../B4_JOINT_NESTED_CUT_TWO_HOST.md),
[D051](../../B4_1RT2_K1_DIRECT_SINGLETON.md#selection-for-all-positive-rtk),
[D043](../../B4_Q1T2_K1_ROOTED_CORE.md#family-coverage-and-validation-scope), and
[D037](../../B4_UNPADDED_QR12.md#original-completion-for-all-qrk1).
