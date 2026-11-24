# D118 verification evidence

**ACCEPT** the [symbolic ordinary graceful supplier](../../../research/ORDINARY_QA2_2_DISJOINT_R226_SUPPLIER.md) for exact ordered `[[q,a,2],[2]]` at independent exact odd integers q≥5 and a≥3 and physical pins `(s:0,s:1,b:1:0)=(0,q+a+9,1)`. The ten-vertex core and both palettes are supplied directly. The local integral allocations, exact global partitions and disjoint named slots implement the [adopted R226 reserved-palette criterion](../../../references/upstream/mdl/N226_R226_two_host_completion.md#n226-closeout). Section 10 of the archived manuscript gives the corollary. The direct original-edge proof independently establishes both bijections.

The [single prepared original](original.json) is ordered `[[5,3,2],[2]]`, with 18 vertices and 17 edges, frozen before assigning labels. Its graph digest is `251199e28613d0928ae9341bdef911ec9fa8032daefa66d02c04a0bd7da60e20` and its certificate ledger is `761cdee2fb118b0374ba871698304ca45dd6fef36b9b70dcef403e7076dea996`. The unchanged checker and [independent audit](result.json) verified every incidence and both full inventories. The retained D111 certificate was rechecked once on its own original. D112 compatibility passed as a physical premise check. No right-growth application was executed.

| Declared probe | Verified outcome |
| --- | --- |
| Wrong expected digest | The unchanged ordinary checker rejects the original digest mismatch. |
| Swap labels 7 and 5 at the two specified L/C terminals | Both leaves are in Batch B. The label bijection and physical pins persist, while weights 5 and 6 disappear. Weight 3 repeats on `b:0:1--l:0:1:1` and `b:0:2--l:0:2:1`. Weight 4 repeats on `b:0:0--l:0:0:4` and `b:0:2--l:0:2:0`. The checker rejects. |
| Move reflected pair {5,8} from C to L | Both reserved palettes remain exact. The local L/C quotas change from (2,2) to (4,0) and the local predicate rejects. |
| Replace Batch A's pair {6,9} by {5,10} | Both local predicates accept with unchanged named quotas. Globally, labels 5 and 10 and weights 3 and 8 each occur twice, while labels 6 and 9 and weights 4 and 7 are missing. The global predicate rejects. |

**PASS** one [original preparation](preparation_receipt.json), one [parse-only preflight](preflight_receipt.json), and one [official verification](command_receipt.json), with empty standard error at all stages. Preflight checked 316 repository pins, the task sources, unique intended definitions, runtime and vacant outputs without importing task modules. Total process CPU was 0.515625 seconds including preflight, and total supervised wall was 1.9295974 seconds. The [final supervision receipt](verification_supervision.json) debits both earlier phases. There was one worker, one new original, one certificate, one retained recheck and four declared probes, with zero additional profiles, assignment enumeration, search, solvers, joins, replays, retries, restarts or successor experiments.

[Contract](CONTRACT.md) · [Frozen configuration](config.json) · [Separate reviews](REVIEWS.md) · [SHA-256 manifest](MANIFEST.json)

## Reproduction under separate authorization

Use the pinned project-local Python and PowerShell 7 in a disposable checkout with vacant execution outputs. The frozen config checks raw bytes. Preserve the committed line endings, for example with clone-local `core.autocrlf=false`.

```powershell
$runner = 'evidence/validation/LCL_ORDINARY_QA2_2_DISJOINT_R226_SUPPLIER_001/supervise.ps1'
$frozen = '267e8af27f05b33b4e086505458bfa2b6813c4d958961937592aa80ab8f315cf'
& $runner -Phase prepare -FrozenConfig $frozen
# Continue only if preparation passes.
& $runner -Phase preflight -FrozenConfig $frozen
# Continue only if the parse-only preflight passes.
& $runner -Phase verify -FrozenConfig $frozen
```
