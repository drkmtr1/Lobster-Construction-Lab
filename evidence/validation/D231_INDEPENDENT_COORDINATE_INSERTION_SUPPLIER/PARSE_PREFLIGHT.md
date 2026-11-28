# D231 — Parse-only preflight

**PASS.** The existing project-local CPU-only CPython 3.13.17 (MSC v.1944, 64-bit AMD64) parsed the three new scientific files as text using the standard-library AST parser from an isolated `-I -S -B -` invocation. It checked lexical definition uniqueness, exact source-directory membership, duplicate JSON object fields, all manifest bytes, reserved destinations and absence of task bytecode. It loaded no project module and generated no target or scientific fixture.

| Checked file | Result |
|---|---|
| `audit.py` | Parsed, 9 lexical definitions |
| `driver.py` | Parsed, 19 lexical definitions |
| `model.py` | Parsed, 3 lexical definitions |
| `registration.json` | Parsed, SHA-256 `298114c1d88e2da7ef7fc35fc72e97e7aabfddac059912d1f5af726ccb0a06f0` |
| `source_manifest.json` | Parsed, all 26 path bindings verified, SHA-256 `ca2f6a00371c834e8c4c41c2a5aaf89270bd9dff042c6e0aefd10e8a6492ad41` |

Both `runs/d231-unequal-pair-return-kernel-001` and `evidence/runs/d231-unequal-pair-return-kernel-001` were vacant. Source files were bounded to 1 MiB per manifest read. Observed parser CPU was 0.0625 s and outer wall 0.321098 s. The existing interpreter launcher's SHA-256 was `4e67d9e9a3673aa7b6219f1280d5bd98ea8688c72d0cb7582d664`.

These are preparation checks of syntax, structure and exact bytes. They do not test solver performance, produce a classified key or grant execution authority. The future scientific entry point and the protected checker were never invoked.
