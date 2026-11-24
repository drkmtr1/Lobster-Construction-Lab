# D105 independent read-only reviews

## Mathematical review — ACCEPT

Reviewer `d105_math_review` independently inspected the direct proof, frozen original and D104 scope, then the exact producer and independent audit before invocation. Afterward the reviewer inspected the saved result and execution receipt. The 14 named labels are a bijection onto [0,13], with physical spine labels (0,13). The original's signed difference sequence is (13,10,8,7,2,−1,9,5,4,3,12,6,11) and the absolute sequence is a permutation of [1,13]. Both unused inventories are empty.

Traversing from the physical entrance yields the same two classes as in the result. Their label extrema rule out both separation orders. The only negative edge is the original incidence from l:0:0:3 to b:0:0, with value −1. The odd-distance weighted sum is 131 and the even-distance weighted sum is 42, giving 89=91−2. The witness is consistent with D104's alpha exclusion on the same frozen original. The swap changes 8 and 5 to 6 and 7, already present on two unchanged incidences. The saved control agrees. No edits or replay occurred during review.

## Implementation review — PASS

Reviewer `d105_impl_review` inspected the frozen run, independent auditor, parse-only preflight, configuration, contract, unchanged original-target checker and retained D099, D098 and D104 records. Before invocation the reviewer checked the fixed indexed construction, complete original topology and multiplicity checks, physical spine guard, separate ledger and inventories, signed-degree assertions, genuine controls, pinned files and bounded execution. The verified runtime and all 107 retained file pins and four source and contract pins matched.

The actual result and both receipts passed. The one official worker produced one original-bound certificate, rechecked D098 once and rejected all three D105 adverse inputs on their intended verification paths. The false expected digest and false physical labels (0,12) were rejected. The terminal swap preserved the label inventory and repeated 6 and 7 twice each while omitting 5 and 8. The audit independently verified the whole ordered incidence ledger, both empty inventories, and the D104 exclusion through the same raw original bytes and digest. There were zero new graphs, prohibited operations or task bytecode files.

The official invocation consumed 0.125 process-CPU seconds and 0.13624050002545118 in-process wall seconds, under the 0.4279599-second supervised outer interval with a 60-second deadline. All raw source and output links matched. Result SHA-256 is `62a71cf47642426a79a48890d63680a1fbee393fe5fce42d4f4040eb87518207`. Preflight receipt SHA-256 is `1654d2c0f8750edc3f74327fb4bb581aa784a17d23dd8df14b23e50a397d83f7`. Command receipt SHA-256 is `06b8395705bee66e01f821421a6aee2e9b6ae2a8c678dd70263d02e2e76652ba`. The review used no edits or replay.
