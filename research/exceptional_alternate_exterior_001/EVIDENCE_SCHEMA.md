# D172 future evidence schema

All JSON records are UTF-8 with the sorted compact serialization defined in runtime.py. Whole records are stored as immutable filenames under the one claimed run directory. A partial temporary filename does not certify a disposition.

| Record | Required contents |
|---|---|
| CLAIM.json | Manifest hash, approval hash, exclusive status, supervisor PID, absolute monotonic worker stop deadline |
| WORKER.json | PID and single-worker start status |
| target-NNNN-M.json | Original ID, graph and record digest, prefix digest, ordered parameters, arm, result, independent audit and charged work. A symbolic NO gives reference and basis. A numerical NO has two independently completed matching representative counts and strata. |
| target-NNNN-A.json | Same identity fields and independent audit for a tested A disposition. For NOT_REQUIRED_FOR_SEPARATOR retain the original, prefix and basis VERIFIED_M_YES. No A feasibility assertion follows from this value. |
| target-NNNN-PAIR.json | Original and prefix binding, two arm claims, separator flag. A separator links the two arm files by filename and exact SHA-256 and retains the M proof/audit, original parameters, A exterior structure, exact resources and connector. |
| SUMMARY.json | Worker status, reason, separator ID if proved, completed and disqualification counts, pending target/arm, phase/candidate/exact deterministic cursor and active frames on controlled abort, counters by phase, charged bytes, CPU and traced and retained-state peaks. |
| SUPERVISION.json | Observed final disposition and reason, worker exit and summary availability, process CPU accounting, preparation charge, observed wall accounting and bytes before receipt. |

An audited positive includes the full named original and digest, reduced and actual exterior labels, reduced crossing edges and differences, actual selected terminal identities and parent slots, direct-leaf exterior indicator, normalized gap coordinates/images, each actual parent and residual quota, cut crossing predicate and counts, actual vertex labels, unchanged original checker certificate, exact exceptional crossing and noncrossing spectra, physical endpoint and return phase, both first-section resource inventories partitioned by label side and weight crossing, literal unfinished connector with endpoints and weight, opposite-polarity transport data, and explicit outside-menu structural reasons for A. Direct proof of membership or exclusion uses both numerical geometry and actual incidence.

SEPARATOR_VERIFIED requires a validated M NO and A YES at the same prefix and original, completed pair binding and confirmed supervisor. EXHAUSTED_NO_SEPARATOR requires all 396 pair decisions, with each learned original disqualified by verified M YES or independently audited A NO. INCOMPLETE preserves previously durable records and gives neither aggregate absence nor a disposition for the interrupted arm. Control references are documentary records and reside outside the research population.
