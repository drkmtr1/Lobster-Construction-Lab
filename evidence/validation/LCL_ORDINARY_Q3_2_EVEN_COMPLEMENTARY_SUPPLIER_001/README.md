# D114 verification evidence

**ACCEPT** the [symbolic ordinary supplier](../../../research/ORDINARY_Q3_2_EVEN_COMPLEMENTARY_SUPPLIER.md) for ordered `[[q,3],[2]]`, exact even q≥6. The necessary parity identity makes the second-center label odd. The reversed numerical host order lets the first center's remaining quota be filled by complete pairs. Both label and weight bijections are also proved directly.

The sole [original](original.json) is `[[6,3],[2]]`. Its canonical digest is `37b606962dc99112fe426c7e37c8e678bb076134e4f53fb56aff0d21dc1567d7`, with raw SHA-256 `dd9d6b87d8f68e95caac1bfc3541eaf5356277a0b71d0ff63e291940d4f2ec08`. The unchanged graph builder prepared it in a one-purpose invocation before labeling, recorded in [original preparation](original_freeze_receipt.json). The [certificate and independent audit](result.json) cover all 16 names and all 15 original incidences. The canonical ledger ID is `c3c3b3c1e7fb770104b48c9ce754c854ec58da718287243d66b84309432846b4`. The named spine, all three pins and actual D112 neighbor conditions were verified. The retained D111 certificate was rechecked once on its own original.

| Declared probe on the q=6 boundary | Outcome |
| --- | --- |
| Wrong graph digest | Ordinary checker rejects the mismatch. |
| Cross-center swap of 6 and 4 | Pins and vertex bijection survive. Weight 2 repeats on `s:0--b:0:0` and `b:0:0--l:0:0:1`. Weight 7 repeats on `b:0:0--l:0:0:4` and `b:0:1--l:0:1:0`. Weights 4 and 9 are missing, and the ordinary checker rejects. |
| Move pair {5,10} to the lower host | Both residual multisets remain exact, but lower/higher quotas change from (4,3) to (6,1). The allocation gate rejects without constructing a ledger. |
| Complement about 15 | Ordinary checker accepts, and the separate pin gate rejects (15,0,14) in entrance, exit and right-center order. |

The [parse-only preflight](preflight_receipt.json) checked 245 repository bindings, eight local input hashes plus config, four Python sources, the runtime and vacant output paths. No task imports or bytecode occurred. [Original preparation](original_freeze_receipt.json) took 0.078125 process-CPU seconds. The one [official invocation](command_receipt.json) used 0.171875 process-CPU seconds and 0.24534379999386147 internal wall seconds. The [supervisor](supervisor_receipt.json) recorded 0.5235727 seconds and exit zero with empty [standard error](official_stderr.txt). Combined preparation and official process CPU was 0.25 seconds. There was one new original and one certificate. No other numerical profile, solver, assignment enumeration, search, join, retry, restart, historical replay or successor experiment occurred.

[Contract](CONTRACT.md) · [Configuration](config.json) · [Separate reviews](REVIEWS.md) · [SHA-256 manifest](MANIFEST.json)

## Reproduction under separate authorization

Run from the project root in a disposable checkout with vacant official output paths and the pinned Python runtime. Use the already frozen original and preparation receipt.

```powershell
& .venv/Scripts/python.exe -B -E -X utf8 'evidence/validation/LCL_ORDINARY_Q3_2_EVEN_COMPLEMENTARY_SUPPLIER_001/preflight.py' '1b615ef40c463e78a1aaf32feec3840f4e9d8b5744e622e04da24986d513c196'
# Continue only if the preflight passes.
& 'evidence/validation/LCL_ORDINARY_Q3_2_EVEN_COMPLEMENTARY_SUPPLIER_001/supervise.ps1'
```
