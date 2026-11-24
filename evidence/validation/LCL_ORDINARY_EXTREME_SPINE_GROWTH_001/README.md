# D112 verification evidence

**ACCEPT** the conditional sign-independent extreme-spine growth theorem and the independently supplied ordinary graceful family `[[5,3],[r]]` for every exact integer r≥2. The [symbolic proof](../../../research/ORDINARY_EXTREME_SPINE_GROWTH.md) establishes the two complete inventories, named spine and closure. The archived computations are corroborating controls.

The unchanged checker accepted D105, D106 and D111 once each on their own originals. The [independent audit](result.json) directly compares D105 and D106. It confirms that the only new terminal is `l:1:0:2` at `b:1:0`, that the two old weights at `s:1` change 13→14 and 12→13, and that the new terminal of label 13 supplies weight 12. The unchanged weights are exactly `[1,11]`. The auditor also checked the D111 base pointwise, including its original labels, named spine, full exit neighborhood and the three descriptive second-left negative incidences.

| Probe on retained D111 data | Ordinary verification | Growth premises |
| --- | --- | --- |
| Wrong expected graph digest | Rejects the mismatch | Ordinary digest check isolated |
| Swap 4 and 5 at the same left center | Accepts, exchanging only weights 8 and 7 | Accept |
| Complement all labels | Accepts, preserving every absolute weight | Rejects pins (14,0,13) in order u,v,c |
| Use the alternate path `(s:0,s:1,b:1:0)` | Retains the original verdict on identical graph and labels | The path still witnesses distance at most two. The proposed exit is interior and the host is on the path, so the premises fail. |

The [parse-only preflight](preflight_receipt.json) checked 211 repository pins, five task source hashes, unique intended Python functions, the runtime and vacant output paths. It imported no task modules and created no bytecode. The single [official invocation](command_receipt.json) used 0.234375 process-CPU seconds and 0.23861559998476878 in-process wall seconds. The [supervisor](supervisor_receipt.json) recorded 0.5297396 wall seconds and exit 0 with empty [standard error](official_stderr.txt). The counts include three retained rechecks and four declared probes. New profiles, graph identities, certificates, solver calls, assignment visits, search, joins, retries, restarts, historical replays and successor experiments were all zero.

[Contract](CONTRACT.md) · [Configuration](config.json) · [Separate reviews](REVIEWS.md) · [SHA-256 manifest](MANIFEST.json)

## Reproduction under separate authorization

Use project-local Python and PowerShell 7 from the project root in a disposable checkout where all official outputs are vacant.

```powershell
& .venv/Scripts/python.exe -B -E -X utf8 'evidence/validation/LCL_ORDINARY_EXTREME_SPINE_GROWTH_001/preflight.py' 'b97e17293c305e03885bc6e953e9ccdc23a3ad6b123719cebfd74ec75f6986cf'
# Continue only if the preflight passes.
& 'evidence/validation/LCL_ORDINARY_EXTREME_SPINE_GROWTH_001/supervise.ps1'
```
