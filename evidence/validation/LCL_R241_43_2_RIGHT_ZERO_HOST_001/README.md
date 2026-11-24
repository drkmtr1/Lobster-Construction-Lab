# D102 verification evidence

The [proof](../../../research/R241_43_2_RIGHT_ZERO_HOST.md) excludes cut-9 alpha supply on the frozen ordered original `[[4,3],[2]]` with physical right center `b:1:0=0` and both ports free. The [D099 original](../LCL_R241_43_2_LOWER_BLOCK_001/original.json) is reused byte for byte. Its canonical graph digest is `2060a4e5a7d8f8ebc1906499facea2730250938d4550bb4c6ca34582a1f5b6e6`.

The [result](result.json) records exact named incidences for four disjoint edge groups, alpha classes, degrees, both bound rows, the retained D098 positive check and three actual adverse rejections. No D102 labeling certificate was produced. The positive control has its own original graph digest and separate labeling ledger ID. The independent audit rebuilt the target incidence multiset from its literal profile and confirmed which groups can supply weight M. Its evidence corroborates the symbolic impossibility proof.

The [parse-only preflight](preflight_receipt.json) passed with 65 repository-relative input pins and no task-module imports. The [official invocation](command_receipt.json) passed with one worker, 0.171875 process-CPU seconds and 0.1843304000212811 in-process wall seconds. The launcher enforced the 60-second outer deadline. It checked two order cases, one retained positive certificate and three adverse probes. There were zero new graph identities or certificates, separate exit tests, solver calls, complete assignments, search nodes or states, joins, retries, restarts and historical replays.

See the [frozen contract](CONTRACT.md), [configuration](config.json), [reviews](REVIEWS.md) and [SHA-256 manifest](MANIFEST.json). The archive binds both historical execution versions for D083, D093 and D100. Those dispositions and the earlier mathematical scopes remain preserved.

## Replay command for separately authorized reproduction

Run with the pinned project-local executable from the project root, using vacant outputs in a separate disposable checkout. The official archived invocation used these arguments with the outer wall limit.

```text
.venv/Scripts/python.exe -B -X utf8 evidence/validation/LCL_R241_43_2_RIGHT_ZERO_HOST_001/preflight.py 7e17c0cd2a5122a223d77eb55b7df8df93d9b8698f6843abef0364bdce7da9e3
.venv/Scripts/python.exe -B -X utf8 evidence/validation/LCL_R241_43_2_RIGHT_ZERO_HOST_001/run.py
```
