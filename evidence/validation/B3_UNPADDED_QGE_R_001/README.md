# B3-UNPADDED-QGE-R-001 validation and custody

The quantified result is the symbolic original-edge proof in `research/B3_UNPADDED_QGE_R.md`, separately challenged by an AI mathematical reviewer; the actual implementation was separately reviewed by another AI reviewer. These are not human peer review or formal verification. Finite tests corroborate, rather than prove, the family.

`config.json` and `regression.py` declare exactly the 12 requested ordered `(q,r,t,K)` tuples, zero padding, one worker, at most 39 vertices, and a 2,000,000-byte cap per result. No solver, search, pin sweep or solution counting is invoked. `regression_result.json` reports **COMPLETE/PASS on 12 cases**, preserving each independently declared original graph and digest, parameters, prefix, partial verifier report, full labeling and original-target certificate. It is 86,803 bytes. The environment is CPython 3.13.17, Windows 11, optimization level 0; exact run identity, limits and raw source/config/harness hashes are in the result.

`independent_audit.py` reconstructs the original named vertices and incidences, checks the exact named prefix formula and `s:3` remaining path, recomputes the unused inventories and full label/difference bijections arithmetically, and rechecks the saved certificates. `independent_audit_result.json` reports **PASS on the same 12 certificates**, not 12 additional targets; it is 6,207 bytes. The audit shares the project verifier with the regression and is not formal verification. Both scripts create their result exclusively; do not overwrite evidence.

`source/` preserves the 23 exact raw project source, dependency and focused-test files hashed by the regression. The audit compares the live and snapshot bytes with those hashes. Matching bytes at audit time is custody evidence, not a cryptographic attestation throughout execution. `.gitattributes` preserves evidence bytes across Git line-ending settings. The retained L008 was compared read-only against the pinned Bounded Search Git blob `f942e3b8b7628353ef7cf9d8cf53759c2eed0478` at commit `e48b94eec4091b4fe189e325cab2eda464409943`; the retained R241 source blob is `faca17cfa4c484127413762adc0c36b771a18f71` at MDL commit `858a8c1fcfda87ba40bb1adee498a6131504a803`. The source excerpts' distinct SHA-256 identities are recorded in `references/upstream/MANIFEST.json`.

The following commands ran with project-local `.venv/Scripts/python.exe` and `PYTHONUTF8=1`; the independent unittest module invocations ran concurrently, with no solver workers:

* `python -m unittest discover -s tests -p test_b3_unpadded_qge_r.py -v`: **4 methods passed**, including all 12 declared tuples and adverse admission/target/certificate checks.
* `python -m unittest discover -s tests -p test_unpadded_all_qr.py -v`: **5 methods passed**.
* `python -m unittest discover -s tests -p test_unpadded_k1.py -v`: **4 methods passed**.
* `python -m unittest discover -s tests -p test_nonadjacent_consumer.py -v`: **5 methods passed**.
* `python -m unittest discover -s tests -p test_ingest.py -v`: **11 methods passed**.
* `python evidence/validation/B3_UNPADDED_QGE_R_001/regression.py` and then `python evidence/validation/B3_UNPADDED_QGE_R_001/independent_audit.py`: **12/12 PASS**, followed by **12/12 PASS on the same records**.
* `python -m lcl construct evidence/validation/B3_UNPADDED_QGE_R_001/cli_input.json --out evidence/validation/B3_UNPADDED_QGE_R_001/cli_run`: `CONSTRUCTED`, original-target certificate valid, for `(3,2,1,4)`, one of the 12 cases.
* `python -m lcl demo --out evidence/validation/B3_UNPADDED_QGE_R_001/demo_gate`: `CONSTRUCTED`, original-target certificate valid for the retained H010 demo; this is not a B3 case.

The relevant test sources were inspected before execution for solver, enumeration and counting calls. Full unittest discovery was not run because other modules launch solver searches, excluded by this task. CLI and demo records preserve their source inventories, inputs, target identities and certificates. The all-staged-files whitespace check reports 12 inherited end-of-file blank-line notices in four unchanged source files reproduced in three byte-preserved snapshot trees; the staged check excluding those snapshots passes, and all 80 staged evidence files match their working-tree bytes. No remote push was authorized or performed.
