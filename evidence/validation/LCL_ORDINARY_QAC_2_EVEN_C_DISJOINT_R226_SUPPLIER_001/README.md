# D119 verification evidence

**ACCEPT** the [symbolic supplier](../../../research/ORDINARY_QAC_2_EVEN_C_DISJOINT_R226_SUPPLIER.md) for exact ordered `[[q,a,c],[2]]`, independent odd integers q≥5 and a≥3, even integer c≥2 and pins `(s:0,s:1,b:1:0)=(0,q+a+c+7,1)`. The D118 core and both reservations are supplied directly. The two local projections, exact named quotas and global resource partitions give the original graceful labeling. At c=2 the formula specializes pointwise to D118. D112's physical premises pass.

The [frozen boundary](original.json) is `[[5,3,4],[2]]` with 20 vertices and 19 edges. Its odd and even progressions interleave at 7,8,9,10 and the odd progression crosses the Batch A midpoint 17/2. The [certificate and independent audit](result.json) give all labels, edges, differences, signs and resource checks. The unchanged checker rechecked D118 on its retained original exactly once, with pointwise agreement at all 18 names and identical reserved allocations.

| Control | Outcome |
| --- | --- |
| Wrong original digest | Rejected by the unchanged checker. |
| Swap 9 and 7 between L and C terminals | The label bijection, quotas and pins persist, but weights 6 and 7 disappear. Weight 4 repeats on `b:0:0--l:0:0:4` and `b:0:2--l:0:2:1`. Weight 5 repeats on `b:0:1--l:0:1:1` and `b:0:2--l:0:2:2`. |
| Move {5,10} to L in Batch B | Both local inventories remain exact. L/C quotas change from (2,4) to (4,2) and the local predicate rejects. |
| Replace Batch A's {6,11} by {5,12} | Both local predicates accept. The global predicate rejects repeated labels 5,12 and weights 3,10 and missing labels 6,11 and weights 4,9. |

**PASS** one [original preparation](preparation_receipt.json), one [parse-only preflight](preflight_receipt.json), and one [official invocation](command_receipt.json). Combined use was 0.390625 process-CPU seconds and approximately 1.422835 [supervised wall seconds](verification_supervision.json). All three standard-error records are empty. Counts were one worker, one new original and certificate, two positive reservations, one retained evaluation and recheck, and four controls. Additional profiles, assignments, solvers, searches, joins, replays, retries, restarts and successor experiments were zero.

[Contract](CONTRACT.md) · [Frozen configuration](config.json) · [Separate reviews](REVIEWS.md) · [SHA-256 manifest](MANIFEST.json)

## Reproduction under separate authorization

Use the pinned project-local Python and PowerShell 7 in a disposable checkout with vacant execution outputs. Preserve committed raw line endings, for example with clone-local `core.autocrlf=false`.

```powershell
$runner = 'evidence/validation/LCL_ORDINARY_QAC_2_EVEN_C_DISJOINT_R226_SUPPLIER_001/supervise.ps1'
$frozen = 'a8aea1302b0697cf3e1dedc58f4a74bc50c65cbef715171edbcf036daae4a02b'
& $runner -Phase prepare -FrozenConfig $frozen
# Continue only if preparation passes.
& $runner -Phase preflight -FrozenConfig $frozen
# Continue only if the parse-only preflight passes.
& $runner -Phase verify -FrozenConfig $frozen
```
