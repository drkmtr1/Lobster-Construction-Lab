# Independent review of records, resumable pilots, CLI, and optional adapters

## Review outcome

The record and pilot mechanisms preserve immutable case attempts, distinguish incomplete computation from negative evidence, and bind positive witnesses to the caller's original target and declared restrictions. The final focused checks passed: **15 record/pilot tests and 12 optional-adapter/CLI tests**. All optional-adapter tests ran with their packages installed; none were skipped in that validation.

This review inspected `records.py`, `experiments.py`, `engines.py`, and their CLI entry points. It identified defects, returned them to the implementation owners, and added independent regressions. The reviewer did not edit those implementation files. The separate ingestion helper and its dedicated tests were implemented and reviewed by the core owner; this review checked the CLI route that rejects an enormous declared profile before invoking its graph builder.

## What a record certifies

The caller retains the original graph and supplies it to `checked_record`. A graph embedded in an engine response cannot replace that target. A positive witness is checked independently for the exact original topology and graceful-labeling conditions. The record additionally checks the witness against caller-retained pins and domains, supplied separately from any restrictions claimed by the engine.

These are separate obligations. A labeling can be graceful on the requested tree while failing the requested restricted experiment. Such a result is quarantined even though its unrestricted graceful certificate is valid. CLI solver calls pass their input pins and domains to this check; allocation calls pass the independently fixed core labels. B2 pilots derive and retain their actual interval and physical-port restrictions from the declared case.

The record also rejects basic evidence contradictions: a positive status without a witness, a negative status with a witness, an incomplete result claiming an exact count or exhaustion, malformed counts, and a count lower bound greater than an exact count. These consistency checks do not independently certify a reported exhaustive count or prove an UNSAT result. A valid witness certifies existence for its exact target and restrictions; larger counts and negative results remain outputs of their stated finite computation.

An incomplete run may contain an independently valid witness. Its record remains `INCOMPLETE`, and its positive count is only a lower bound. Every record explicitly sets `universal_claim=false`.

## Evidence preservation and resumption

A single invocation saves its original target, result, certificate, expected restrictions, configuration, environment description, and runtime source inventory. The inventory covers the package's Python source files, requirement files, and `pyproject.toml` when present. The recorded file hashes are checked when copying that source snapshot. Documentation and unrelated repository files are not included in this executable-source inventory.

Case attempts have distinct numbered filenames. A later retry writes a new attempt; it does not replace the earlier record. The JSON writer rejects an existing evidence path by default. Checkpoints are replaceable summaries reconstructed from the attempt files, while the attempts remain the evidence. Output-size checks occur before replacement, so an oversized write cannot replace an earlier record with a truncated one.

A pilot manifest binds the exact configuration, runtime source inventory, and environment. Resume verifies its stored fields and recomputed signature against the current invocation, checks the declared case IDs, and rehashes the preserved source files. A source, configuration, dependency/environment, manifest, or snapshot mismatch stops resumption.

Before relying on a saved latest attempt, resume checks its record checksum, original graph, case identity, configuration and source binding, expected restrictions, certificate, and classification. Positive certificates and extracted exploratory prefixes are recomputed against the retained original. A changed checksum is rejected; merely recomputing a checksum does not make an invalid witness acceptable.

These hashes are local integrity and reproducibility checks, not digital signatures or proofs of execution. A person with permission to rewrite every source and metadata file can rewrite the audit trail. The project must retain the original files and follow its separate source-review process when making mathematical claims.

The exclusive `RUNNING.lock` prevents another cooperating invocation from writing the same run concurrently. Normal exceptions release the lock. An existing lock is not silently removed. This is a local filesystem protocol, not a distributed lock service or a guarantee about every network filesystem.

Resume operates at **case boundaries**. It does not restore an internal DFS stack or SMT search state. By default, an existing incomplete attempt is left untouched. `--retry-incomplete` creates a fresh attempt under the same declared configuration. Increasing limits or changing code requires a new run with its own manifest. A quarantined attempt stops subsequent cases and also blocks resume pending review; it is not treated as a completed successful case that may be skipped.

## Invocation and input bounds

The pilot validates its finite declared case list before running it. The initial configuration format permits at most 5,000 explicitly declared cases, at most 100 attempted cases per invocation, at most 3,600 configured invocation seconds, and at most 2,000,000 bytes per case record. The pilot independently rejects a target exceeding 100 vertices before constructing its profile or graph. These are design limits, not mathematical bounds on the lobster family.

An invocation stops before starting another case once its case or wall-time allowance is exhausted. Each case receives the smaller of its engine time allowance and the remaining invocation allowance. Partial limit mappings are normalized through the validated defaults before this calculation. Wall-time checks are cooperative; graph admission, setup, serialization, and individual non-preempted operations can add overhead. There is no operating-system process containment.

CLI graph admission now uses the bounded ingestion layer before expansion. Solve inputs have a 100-vertex admission ceiling, while construction, verification, and allocation allow up to the helper's 10,000-vertex ceiling. Input JSON is limited to 2,000,000 bytes. Constructor parameters are also sized before formula dispatch, so a tiny input containing a huge branch count cannot bypass a graph-size check through parameter expansion. Public mathematical formula APIs retain their stated domains; a CLI size rejection is not a theorem that the target has no construction.

Malformed verification payloads return a structured CLI error. Verification always takes a separately supplied original graph/profile; labels for a different graph embedded in a certificate cannot substitute for it.

## Optional adapters

The Z3 adapter encodes integer vertex labels with their explicit domains, all-different vertex labels, and distinct original edge differences in `1..m`. For a tree with `m+1` vertices, these conditions specify graceful labeling exactly. It has no hidden root-zero, alpha, or symmetry requirement. A satisfiable model is independently checkable; the adapter reports one witness rather than claiming an exhaustive positive count.

Z3 resource exhaustion or another `unknown` outcome maps to `INCOMPLETE`. A genuine solver `unsat` maps to a negative result only for its declared scope, and the output explicitly states that no independently checked proof object is supplied. `max_nodes` is used as Z3's resource-unit limit, not as a DFS-node count. The solver's 512 MiB internal memory setting is not a process-memory guarantee.

NetworkX performs a second topology/degree check and optional isomorphism diagnostics. It preserves the actual named vertices and does not authorize merging physical-port identities. SymPy checks two stated polynomial identities; its output explicitly excludes the additional inequalities, disjointness, domain coverage, and novelty obligations. Missing optional packages produce `UNAVAILABLE` instead of weakening the mathematical checks silently.

## Defects corrected and regressed

| Initial defect | Final regression |
|---|---|
| Valid unrestricted witnesses could be accepted for a different requested restricted scope | Caller-retained pins/domains are independently checked; violation is quarantined. |
| Contradictory result statuses and exact counts were stored without review | Contradictions are quarantined. |
| Resume skipped a quarantined case and continued later cases | Quarantine stops a new invocation and blocks resume. |
| Partial limit mappings passed validation but failed during case execution | Defaults are normalized before accessing time limits. |
| Pilot schema accepted floating-point `1.0` | Schema requires the true integer `1`. |
| Saved attempts were trusted by classification alone | Checksums, bindings, positive certificates, and candidates are checked on resume. |
| Manifest fields and preserved source content could diverge from their claimed identity | Manifest identity is recomputed and snapshot bytes are rehashed. |
| CLI profile expansion preceded resource admission | A bounded ingestion route preflights profiles and parameters. |
| Malformed certificate wrappers caused an uncaught attribute error | CLI validates wrapper shapes and emits a structured error. |

## Validation performed

The focused commands were:

```text
python3 -m unittest discover -s tests -p 'test_records.py' -q
python -m unittest discover -s tests -p 'test_engines.py' -q
```

The second command used the isolated project build environment with these installed packages:

| Package | Observed version |
|---|---|
| NetworkX | 3.7 |
| SymPy | 1.14.0 |
| mpmath | 1.3.0 |
| z3-solver | 5.4.1.0 |

Execution used Python 3.12.14 on Linux. The 15 record/pilot tests completed in approximately 0.06 seconds, and the 12 adapter/CLI tests in approximately 0.65 seconds. The supported release targets are Python 3.12 and 3.13; these observations are not a Python 3.13 or Windows execution result.

The tests exercise bounded real DFS cases, immutable retries, source/config/environment mismatches, record tampering with and without a recomputed checksum, manifest and source-snapshot alteration, lock exclusion, case and invocation-time caps, size limits, quarantine, and explicit restriction checking. Storage tests use an isolated synthetic source directory and fixed environment metadata so concurrent project edits cannot invalidate their intended resume fixtures. Mathematical witness checks still use the actual local implementations.

Optional tests use real installed backends on singleton, four- and six-vertex paths, the six-vertex spider with legs 2,2,1, a restricted impossible core, and a pinned non-alpha graceful labeling. The enormous-profile CLI regression patches the builder to fail immediately if reached: no enormous graph is allocated during the test. No upstream MDL executable code or discovery campaign was run by this review.
