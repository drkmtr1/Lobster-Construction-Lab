# D229 — Parse-only preflight

**PASS.** From the LCL root, the existing project-local CPython 3.13.17 was invoked with `-I -S -B -` on an inline standard-library parsing script. It read source as text, called `ast.parse`, and checked definition names for uniqueness within their lexical declaration scopes. It also checked the declared file set and parsed the two JSON inputs. No Python module from the D229 package or LCL was imported. No bytecode was written.

| Parsed input | Result |
|---|---|
| `audit.py` | Syntax and unique definitions pass |
| `coverage.py` | Syntax and unique definitions pass |
| `driver.py` | Syntax and unique definitions pass |
| `model.py` | Syntax and unique definitions pass |
| `retained.py` | Syntax and unique definitions pass |
| `search.py` | Syntax and unique definitions pass |
| `control_originals.json` | Parse passes |
| `registration.json` | Parse passes |

The reserved `runs/d229-homogeneous-pair-finite-kernel-001` and `evidence/runs/d229-homogeneous-pair-finite-kernel-001` paths were vacant. No `__pycache__` or `*.pyc` existed under the prepared source directory. The preflight did not call a candidate row generator, test fixture, solver, protected checker, control-construction function or diagnostic driver. These static checks establish structure and custody. They do not certify execution or performance. Exact byte bindings are in the package source manifest and Director handoff.
