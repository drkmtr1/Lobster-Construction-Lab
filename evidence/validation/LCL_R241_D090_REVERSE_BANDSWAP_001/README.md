# D093 symbolic reversal and incomplete executable verification

`LCL-R241-D090-REVERSE-BANDSWAP-001` · November 23, 2026, Pacific/Honolulu · parent `8d726a8abe7e0d600d1427c7164a4284599e71b3`.

[Symbolic proof](../../../research/R241_D090_REVERSE_BANDSWAP.md) · [External failure receipt](external_failure_receipt.json) · [Tool output](tool_output.txt) · [Separate reviews](REVIEWS.md) · [SHA-256 manifest](MANIFEST.json)

**Mathematics review — ACCEPT.** The proved transformation supplies A(a+b+20,11;5,3) on exact `[[3],[3,b],[2],[2,a]]` for all integers a,b≥2. Reversal is a bijection on the named graph and the band exchange maps each difference d to N−d. The proof's boundary paragraph specifies the intended regression. No boundary certificate was produced in this attempt.

**Executable verification — INCOMPLETE.** The sole official Python invocation stopped on import of the frozen `audit.py`, line 233, where a duplicated function block begins immediately after the closing brace of a return value. This syntax error occurred before the script could build a target, call the checker, run the auditor or write its receipt. PowerShell then failed to read the absent internal receipt. The external receipt records the tool exit and exact task inputs. Process-CPU usage was not captured. Tool wall time was about 1.89 seconds. Exactly one invocation was launched. Zero target originals or certificates, checker rechecks, adverse probes, solver calls, assignment visits, new joins or replays occurred. No retry or restart was made. The three expected in-script output files are absent.

The frozen sources and retained D090–D092 bindings are preserved byte for byte. The preflight matched the configuration, source and runtime hashes, but it missed the malformed duplicate. Static arithmetic shows the prescribed swap would replace differences 3 and 15 with two additional instances of difference 9. This arithmetic is retained as a prediction, with the executable check still pending.

## Recorded invocation

The producer and auditor are the exact failed sources. From the recorded parent with the task inputs in their original paths and the configured project-local executable, the official command was:

```powershell
.venv/Scripts/python.exe -B -X utf8 evidence/validation/LCL_R241_D090_REVERSE_BANDSWAP_001/run.py
```

The archived hashes identify the failed attempt. Its only supported execution outcome is INCOMPLETE. A correction and fresh verification require separate authorization and a new evidence identity.
