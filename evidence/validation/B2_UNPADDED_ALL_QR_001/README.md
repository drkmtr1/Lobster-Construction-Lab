# B2-UNPADDED-ALL-QR-001 targeted validation

The theorem is the symbolic argument in `research/B2_UNPADDED_ALL_QR.md`, not a finite-test extrapolation. The original named target, `q,r>=1`, `K>=2`, and `z0=z1=0` are part of the scope.

- `config.json` and `regression.py` declare and check 12 fixed `(q,r,K)` tuples, one worker, at most 32 target vertices and 2,000,000 bytes per result. They include unequal ordered pairs, minimum values, balanced controls and the `(1,2)` seed specialization. They call no solver and examine no K=1 case.
- `regression_result.json` records **COMPLETE/PASS, 12 cases**, Python 3.13.17, Windows 11, and approximately 0.227 seconds measured in that run. It includes every retained original target, graph digest, prefix, both unused inventories, full labeling, certificate, limits and source/config/harness hashes. The script checks the explicitly named edge set separately from the constructor, then uses the project's independent certificate verifier on the retained target.
- `independent_audit.py` and `independent_audit_result.json` separately recheck the **same 12 saved certificates and original edges**, without invoking the constructor or any solver; they report **PASS**, exact inputs, environment and Python optimization level. The builder and certificate verifier are shared project components, so this is not independent implementation or formal certification.
- `source/` contains exact copies of the 23 source, dependency and test files whose raw hashes appear in the regression result. The recorded hashes were calculated after the regression checks; matching snapshot/live bytes is custody evidence, not a cryptographic attestation of all bytes throughout execution. The audit checks both copies against those hashes. All run files are protected against line-ending conversion by the local `.gitattributes`.
- The targeted command `python -m unittest discover -s tests -p test_unpadded_all_qr.py -v` passed all five test methods under project Python 3.13.17. It was run twice: once before and once after adding two adverse checks; the final run reported 0.009 seconds. The final test source is snapshotted. No full suite, unrelated experiment, or K=1 search was run.

The implementation author also reported a separate informal, first smoke check on `q=2,r=3,K=2` before the retained regression. The exact command and stdout were:

```text
python -c "from lcl.constructors import two_section_nonadjacent; from lcl.ingest import construction_input; from lcl.model import build_graph, graph_digest; from lcl.verify import verify_certificate; spec={'method':'two_section_nonadjacent','parameters':{'q':2,'r':3,'K':2},'profile':[[2],[3],[],[],[]]}; original,result=construction_input(spec); print(result['method'], result['trace'][0]['unused_labels'], result['trace'][0]['unused_differences'], verify_certificate(original,result['labels'],graph_digest(original))['valid'])"
two_section_nonadjacent [5, 6] [1, 2] True
```

That smoke check did not record its interpreter, environment, source hashes, timestamp or certificate object; it is not the retained reproducible regression and does not establish an exact run identity. The quantified proof and separately preserved validation do not depend on it. A changed algorithm, configuration or environment requires a new run identity and output; do not overwrite this evidence.
