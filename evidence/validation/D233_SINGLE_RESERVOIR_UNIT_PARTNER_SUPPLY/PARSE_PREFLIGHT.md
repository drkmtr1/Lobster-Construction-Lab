# D233 — Static parse-only preflight

The test was performed with the project-local CPython 3.13.17 launcher, using `-I -B -S -` with a standard-library-only inline reader. It read source bytes, checked SHA-256, applied `ast.parse` to each bound Python file and checked unique function/class definitions within each statement body. It did not import any project or task module, run the registry or any scientific fixture, compile task bytecode, call a solver or invoke a protected checker.

- All 22 source-manifest file bindings matched the exact working bytes and resolved within LCL.
- All bound Python sources parsed and contained no duplicate function or class definitions in the inspected bodies.
- The exact registered domains and integer ceilings matched the independently derived 248-key, 42,512-placement and 54,415,360-attempt bounds.
- Both registered scientific paths were absent, including symlink checks. No admission receipt, task bytecode, scientific output or archive was created.
- `source_manifest.json` SHA-256 `072f209bf1110342201c8e8edd841b63e075068227fba1d67f80b3bf407e54ea`.
- `registration.json` SHA-256 `2840da288676cfe0e4e57527888c0206fd49dfde7ba64bac7fb59a3cefa19a15`.

This is evidence of byte binding and syntax, together with the static arithmetic and independent review. Execution readiness, runtime no-shadowing and cache checks, actual approvals and qualified foreground supervision remain fresh admission predicates for any separately authorized execution.
