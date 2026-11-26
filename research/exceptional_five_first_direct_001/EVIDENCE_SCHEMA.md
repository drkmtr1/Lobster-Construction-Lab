# D174 future evidence schema

The frozen runtime emits UTF-8 compact sorted JSON. Ordinary records use new files and atomic rename. An interrupted temporary record is retained separately from durable complete evidence.

| Record | Contents |
|---|---|
| CLAIM.json and WORKER.json | Manifest and authorization binds, claimed supervisor PID, cooperative deadline, single worker PID and start marker |
| target-NNNN-H0.json and target-NNNN-H1.json | Frozen original and prefix digest, exact physical profile and canonical record hash, arm, raw-exterior basis, claim and audit, charged work. For a skipped H1 retain NOT_REQUIRED_FOR_SEPARATOR with its verified H0 YES basis. |
| target-NNNN-PAIR.json | Frozen name/original/prefix, exact arm claims and separator flag. A separator binds both raw arm files by exact SHA and retains the H0 decision and audit, H1 exterior structure, eight host quotas and named roles, direct-placement comparison, resources, cut sides, connector and exact return. |
| SUMMARY.json | Status, failure reason or verified separator, counts of fully reconciled pairs, disqualification counts, pending case and logical frames, work by meter phase, CPU, charged bytes and worker memory peaks |
| SUPERVISION.json | Confirmed worker status, exit and summary receipt, combined observed wall, CPU and byte accounting, preparation charge and terminal disposition |

An audited positive retains the original named graph and digest, connected reduced labels and weights, the actual terminal incidences and direct-leaf slot, expanded exterior, each actual gap coordinate/host/image, all eight capacities, full labeled original, unchanged checker certificate, exact crossing/noncrossing and cut-side partitions, both intermediate inventories and literal unfinished connector. It also records the exact returned physical frontier and polarity transport. A separator compares direct-leaf placement and the associated zero/one direct capacity, widths at fixed selected counts, and actual named roles of the successful H1. A completing H0 geometry does not exist on an audited negative and no hypothetical H0 labeling is saved as a witness.

NO means independent exhaustive rejection in that arm with matched representative counts and strata. A cap, uncertain process exit, incomplete audit or consistency failure yields INCOMPLETE and no unproven absence. An untouched target or skipped H1 does not count as an arm NO. No campaign may start without a separate Owner authorization at the reviewed manifest hash.
