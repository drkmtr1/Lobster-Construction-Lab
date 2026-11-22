# B4-THIRD-ZERO-HOST-SEED-001 evidence

The [restricted proof and outcome](../../../research/B4_THIRD_ZERO_HOST_SEED.md)
record the all-t>=3 fixed-low obstruction and the finite
zero-host/adjacent search. The [extension proof](../../../research/ALPHA_ZERO_HOST_LEAF_EXTENSION.md)
is conditional on a supplied zero host and physical witness.

## Preserved records

- [Configuration](config.json) gives the exact named 1122 target,
  full alpha domains and pins b:2:0=0 and s:4=7. One worker,
  at most 15 vertices, 100,000 nodes, five cooperative seconds
  and 2,000,000 bytes per result. Counting was not requested.
- [Preflight](preflight.json) freezes the configuration, original
  graph, runtime and dependency/source snapshot before DFS. The
  [retained-control recheck](control.json) verifies labels and
  differences on the same original and records b:2:0=2 as the
  only pin mismatch. The historical DFS was not repeated.
- [Start marker](query_start.json), [raw result](raw_result.json)
  and [bound query record](query_record.json) preserve the only
  DFS execution. It returned EXHAUSTED_NO_SOLUTION, 17,514 nodes,
  0.15197850001277402 seconds, exhausted=true and exact count 0.
  No limit was reached. There is no witness or positive certificate.
- [Independent audit](audit_result.json) recomputes exact graph
  multiplicities, control arithmetic and the full restriction set,
  and checks saved receipt and source identities. The audit ran
  zero queries and does not independently re-enumerate the search.
- [Command receipts](commands.json), [review records](REVIEWS.md)
  and [raw-byte manifest](MANIFEST.json) preserve the execution
  and closeout evidence.

## Accounting and scope

One retained control was rechecked and audited. One new restricted
query was recorded and audited. Zero new verified seeds, zero
direct completed targets and zero additional queries resulted
from the audits or reviews. The four direct cases declared for a
verified witness were inapplicable. There were no other searches,
suite runs, constructor or CLI changes. The exhausted negative
addresses only the declared 1122 alpha/zero-host/adjacent query.
