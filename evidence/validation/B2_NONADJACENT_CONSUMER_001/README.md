# B2 nonadjacent consumer validation

The proof and its exact conditional scope are in `research/B2_NONADJACENT_CONSUMER.md`; finite tests here do not establish an independently supplied unequal prefix or replace induction.

- `config.json` and `regression.py`: 31 fixed cases, `K=2..32`, `ell=1`, one worker, at most 35 vertices. Each original target is the named pure path `s:0--...--s:(K+2)` with supplied prefix `s:0=K+1,s:1=0,s:2=K+2`. The script independently evaluates the direct recurrence and actual original edges, preserves the caller's graph and prefix, and checks the full certificate. It is not a seed search.
- `regression_result.json`: **COMPLETE/PASS**, 31/31 cases, Python 3.13.17, 0.243 seconds as measured in that run. It records every exact original target, graph digest, prefix, full labeling, actual edge differences, independent certificate, configuration and source identities.
- `demo/`: separately executed standard `python -m lcl demo` output, original target, independent certificate, configuration, environment and full immutable source snapshot. Its source files and `test_nonadjacent_consumer.snapshot.py` match all 23 source/test raw hashes in the regression result. The latter is a copy of the exact test file run.
- `reviewer_receipts.md`: exact separate reviewer scratch scripts and reported outputs, including an exploratory K=2..4 prefix fixture search with unrecorded actual attempts and unrecorded interpreter/source identity. It is finite first-witness data, not an exhausted classification, an independent all-K supplier, or a p=5 seed claim. The superseded pin sweep was not executed.
- Full unit suite: `python -m unittest discover -s tests -v`, project Python 3.13.17, 115 tests run, six optional-dependency skips, no failures; final run 0.952 s reported by unittest. The focused file includes the independently reviewed actual-path and adverse tests.

Run data and snapshots are byte-preserved by the local `.gitattributes`. A changed code, configuration or environment requires a new run identity and output; do not overwrite these files. Regression output is created with exclusive mode and a 2 MB cap.
