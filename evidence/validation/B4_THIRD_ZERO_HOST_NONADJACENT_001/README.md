# B4-THIRD-ZERO-HOST-NONADJACENT-001 evidence

The [fixed seed ledger and proof](../../../research/B4_THIRD_ZERO_HOST_NONADJACENT.md)
establish ordinary gracefulness for the exact original
`[[1],[1],[t],[2]]+[[]]*(K+1)`, integers t>=2 and K>=2.
The normalized seed is alpha.

## Exact seed run

The [configuration](config.json) declares one worker, 15 vertices,
100,000 assignment nodes, five cooperative seconds and 2,000,000
bytes per result. The generic max_states setting is unused by DFS.
The full alpha domains and only pins b:2:0=0,s:4=8 bind the exact
named [original](original_graph.json). The frozen
[preflight](preflight.json) includes a synthetic in-memory schema
probe with zero solver calls. The [retained control](control.json)
passed original and alpha checks and failed only b:2:0, with actual
label 1. Its historical DFS and the prior s:4=7 query
were not repeated.

A [one-shot start marker](query_start.json), [raw result](raw_result.json)
and [original-bound record](query_record.json) preserve the only
search. It returned SAT at 2,368 nodes in 0.020261199999367818 s.
The run stopped at the first verified witness, with exhausted=false,
count=null and count_lower_bound=1. The [independent seed audit](audit_result.json)
reconstructed the exact named graph, original-edge differences,
both domain classes and pins, and bound the control and witness
to the saved identities. It added zero seeds or queries.

## Four direct targets

The exact four declared cases in (t,K) order were:
(2,2), (3,3), (4,4), and (3,5). They passed at one worker,
21 vertices and 2,000,000 bytes per result. The largest case
record is 7,958 bytes. No search supplied their labels beyond the
one already verified fixed seed. The [summary](direct_checks/summary.json)
and [identity](direct_checks/identity.json) bind their exact originals,
normalized extensions, shifted prefixes, both inventories and
actual physical s:4, named path traces and original-target
certificates.

The [independent direct audit](direct_audit_result.json) rebuilt
the named incidences and recalculated all four of those same
certificates, including the weight-2 bridge s:7--s:8 in the K=5
case. It added zero targets and zero queries. The K=2 path labels
(10,8,7) fail alpha threshold separation. The K=1 interface would
leave a singleton edge of difference 2 where D={1}.

[Commands](commands.json), [reviews](REVIEWS.md) and
[raw-byte manifest](MANIFEST.json) retain the execution and closeout.
The public routes, original checker, and both consumers were
unchanged.
