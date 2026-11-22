# B4-UNPADDED-Q1T2-001 evidence

The [general-host rule](../../../research/ALPHA_UPPER_BLOCK_GENERAL_HOST.md)
proves conditional insertion and pointwise compatibility with
zero-host growth. The [family proof](../../../research/B4_UNPADDED_Q1T2.md)
gives ordinary gracefulness on the exact original
`[[q],[1],[t],[2]]+[[]]*(K+1)` for integer q>=1,t>=2,K>=2.

## Six new completed targets

The [fixed configuration](config.json) declares (q,t,K) as
(2,2,2), (2,3,3), (3,2,4), (3,3,5), (4,5,2), and (5,4,5).
They have 18,20,21,23,23,26 vertices, respectively. One worker,
26 vertices and 2,000,000 bytes per result were the limits.
All originals in `validation/originals/` were recorded before
labeling. The [summary](validation/summary.json) links six saved
certificates and the [source and runtime identity](validation/identity.json).
Each certificate preserves the original named graph, normalized
cut, ports and hosts, witness and full incident predicates,
shifted inventories, original suffix steps and full original
edge ledger. The unchanged checker verified each exact target.

## Controls and same-target checks

The [retained seed recheck](validation/retained_seed.json)
verifies the original 1122 certificate and the ten selected
incidences of weights 5..14. The four other edges have weights
1..4. This rechecks an existing seed. The
[retained completed control](validation/retained_control.json)
rechecks the saved q=1,t=3,K=5 original certificate and
pointwise agreement with the new formula. Neither control
adds a new completed target or search.

The [same-target comparison](validation/same_target_growth.json)
on (3,3,5) checks both named growth orders and the first
batch split 1+1. All eight recorded normalized states have
the full appropriate incidence predicate. All comparison
endpoints agree pointwise with the displayed formula.
The [domain probes](validation/domain_rejections.json) record
12 rejected values across the three parameters, covering
Booleans, floats, strings and out-of-domain integers. These
probes and comparisons add zero targets.

## Independent audit and custody

The [independent arithmetic audit](audit_result.json) reconstructed
the named roles, incidence multiplicities, digests and
differences, checked all six saved certificates and recalculated
both unused inventories and the original path. It checked
the same control, seed, intermediate states and rejection receipts.
It produced zero additional targets and zero queries.

No solvers, enumeration or historical replay were used.
Both historical K1 receipts remained byte-identical and
INCOMPLETE, reason max_nodes, at 100,000 nodes, with
exhausted=false, count=null, count_lower_bound=0 and witness=null.
[Raw receipt](../B4_THIRD_ZERO_HOST_K1_001/raw_result.json) ·
[Original-bound receipt](../B4_THIRD_ZERO_HOST_K1_001/query_record.json)

[Command receipts](commands.json), [separate AI reviews](REVIEWS.md)
and the [manifest](MANIFEST.json) preserve the bounded run and
raw bytes. The new proof bytes and prior attributes are preserved.
The production code, checker, consumers and public routes were
unchanged.

## Reproduction

The validator checks parent HEAD `3da61c39d3444c6286b34033d6ae9fd58b20c547` and
creates fresh `validation/` and `source/` outputs. To reproduce,
use a separate checkout at that parent, copy the two proof files
and the config and scripts to their recorded paths, and use the
commands in commands.json with fresh outputs. The audit publishes
its result by exclusive creation. For a read-only custody review
of this published run, use its saved results and manifest. Keep
its output directories and byte-sensitive snapshots intact.
