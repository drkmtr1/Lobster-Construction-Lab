# D104 verification evidence

The [proof](../../../research/R241_43_2_LEFT_TERMINAL_ZERO.md) excludes cut-9 alpha supply with zero at any left terminal and both ports free. It reuses the exact frozen ordered [D099 original](../LCL_R241_43_2_LOWER_BLOCK_001/original.json), graph digest `2060a4e5a7d8f8ebc1906499facea2730250938d4550bb4c6ca34582a1f5b6e6`.

The [result](result.json) records all 24 ordered high-role pairs, 84 entrance scalar checks and 19 expanded survivors. It gives the unordered right-terminal and forced maximum-center palettes, six fixed weights, all fixed multiplicities and repeats, the residual low labels and a missing weight with both candidate endpoints excluded. The audit independently reconstructs the indexed incidences, signed degree sum, entrance interval and residual palette checks.

The archived D102 and D103 results bind the same original bytes, graph digest and 9/5 orientation and exclude zero at the right center and entrance. D104 excludes the remaining seven zero locations in the size-nine class. Complementation preserves differences and exchanges the two possible alpha orientations. This proves absence of an alpha labeling on this original, with zero additional cut tests. Ordinary gracefulness remains undecided.

The [parse-only preflight](preflight_receipt.json) passed with 93 frozen repository input pins and zero imports of task modules. The single [official invocation](command_receipt.json) used one worker, 0.1875 process-CPU seconds, 0.2055007999879308 in-process wall seconds and 0.6445339 outer supervised wall seconds. The unchanged checker accepted the retained D098 certificate and the three genuine probes rejected the wrong digest, false left-terminal zero pin and spectrum-breaking swap. The swap repeats 5 and 7 twice and omits 4 and 8. There were zero new graph identities, certificates, solvers, complete assignments, search states or nodes, terminal-index sweeps, separate exit or cut tests, joins, retries, restarts and historical replays.

See the [contract](CONTRACT.md), [configuration](config.json), [reviews](REVIEWS.md) and [SHA-256 manifest](MANIFEST.json). Earlier dispositions and all original and versioned receipts remain preserved.

## Reproduction under separate authorization

Use the pinned project-local executable from the project root in a disposable checkout with vacant output paths. Supervise the official invocation with a 60-second outer deadline.

```text
.venv/Scripts/python.exe -B -X utf8 evidence/validation/LCL_R241_43_2_LEFT_TERMINAL_ZERO_001/preflight.py 8877df969c8fcbbc7a2a0f1704abd5838920805284f39f04023635615dac4e8b
.venv/Scripts/python.exe -B -X utf8 evidence/validation/LCL_R241_43_2_LEFT_TERMINAL_ZERO_001/run.py
```
