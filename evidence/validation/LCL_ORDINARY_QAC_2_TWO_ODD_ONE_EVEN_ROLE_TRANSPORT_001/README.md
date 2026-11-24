# D121 verification evidence

**ACCEPT** the [symbolic D119 transport](../../../research/ORDINARY_QAC_2_TWO_ODD_ONE_EVEN_ROLE_TRANSPORT.md) for exact ordered `[[q,a,c],[2]]` with exactly one even left quota at least two and two odd quotas at least three, one at least five. Select C at the even index, H at the first qualifying odd index and L at the remaining index. D119's numerical allocations and the incidence bijection supply both full inventories and preserve the physical pins and D112 premises.

The sole retained instance is D119's `[[5,3,4],[2]]`. The selected map and inverse are identity. All 20 named labels, both batches including their named slots and ordered allocations, and all 19 weights agree. The [audit](result.json) uses the retained [original](../LCL_ORDINARY_QAC_2_EVEN_C_DISJOINT_R226_SUPPLIER_001/original.json) and [certificate](../LCL_ORDINARY_QAC_2_EVEN_C_DISJOINT_R226_SUPPLIER_001/result.json). The nonidentity cases are established symbolically.

| Control | Verified outcome |
| --- | --- |
| Wrong digest | The unchanged checker rejects the identity mismatch. |
| Map (0,0,2) | Physical index zero repeats and index one is omitted. Binding rejects before quota, slot or label work. |
| Map (2,1,0) with role quotas (5,3,4) | Bijection passes. Quota and slot checks reject. It demands nonexistent `l:0:2:4` for H and omits actual `l:0:0:4` at C. No labeling is attempted under this map. |
| Swap labels 3 and 4 within H | Ordinary gracefulness, pins and D112 premises pass. The weights exchange 12 and 11 on the original edges to `l:0:0:1` and `l:0:0:2`. Pointwise agreement fails at precisely those two names. |

**PASS** one [parse-only preflight](preflight_receipt.json) and one [official verification](command_receipt.json). Total use was 0.53125 process-CPU seconds and approximately 1.405852 [supervised wall seconds](verification_supervision.json). There was one retained formula evaluation and checker recheck, two reserved batches, and four probes. No original preparation, new profile, graph identity, certificate, solver, assignment enumeration, search, join, right growth, replay, retry or successor execution occurred.

[Contract](CONTRACT.md) · [Frozen configuration](config.json) · [Separate reviews](REVIEWS.md) · [SHA-256 manifest](MANIFEST.json)

## Reproduction under separate authorization

Use the pinned project-local Python and PowerShell 7 in a disposable checkout with vacant outputs. Preserve committed raw line endings, for example with clone-local `core.autocrlf=false`.

```powershell
$runner = 'evidence/validation/LCL_ORDINARY_QAC_2_TWO_ODD_ONE_EVEN_ROLE_TRANSPORT_001/supervise.ps1'
$frozen = '70cea74f934892beb7d90b006383373e41ceab15547cbed4209cadd727a83e5e'
& $runner -Phase preflight -FrozenConfig $frozen
# Continue only after passing the parse-only preflight.
& $runner -Phase verify -FrozenConfig $frozen
```
