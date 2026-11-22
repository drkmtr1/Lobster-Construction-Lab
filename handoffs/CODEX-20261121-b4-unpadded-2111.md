# B4-UNPADDED-2111-001 continuity handoff

Completed November 21, 2026, Pacific/Honolulu, on `main` of
`drkmtr1/Lobster-Construction-Lab`. The accepted parent is
`e29ceaf787543ab5ef430c75f071fe5c2223381b`. The initial working tree was clean, and
the freshly fetched and independently read GitHub main matched that
parent. Resolve the new checkpoint from the Git commit introducing
this handoff. The closeout report supplies the verified local and
remote SHAs.

## Accepted finding and remaining scope

The exact ordered unpadded `[[2],[1],[1],[1]]+[[]]*(K+1)` profile has
an alpha labeling for every integer K>=1, excluding booleans.
The retained unit seed extended at the original label-zero center
gives the 14-vertex arithmetic seed with low-class size 6. Its
shifted prefix has original root m-1 and second leaf m. The
retained adjacent path from physical `s:4=K+6` uses `R=[6,K+5]`
and `D=[1,K]`. The complete low-class size is `6+(K+1)//2` and
the cutoff is one less. At K=1 the original final edge has labels
7 and 6 and difference 1. Separate AI reviews returned ACCEPT.
See `research/B4_UNPADDED_2111.md` and D032. The CLI graph ceiling
gives K<=9986 and the inherited record byte cap applies separately.
Other unproved profiles, padding, multiple branches per section,
additional sections and arbitrary repetition remain open.

## Evidence and continuity

`evidence/validation/B4_UNPADDED_2111_001/` preserves the original graphs, certificates and audit,
source and dependency snapshots, runtime, configuration, exact
commands, review and raw-byte manifest. All 12 declared original
targets and their same-certificate audit passed with one worker,
a 78-vertex cap and a 2 MB cap per result. One fixed 14-vertex
seed passed separately. All 65 targeted tests, actual K=1 CLI
construction and retained demo passed. The proof uses extension
after R241 composition. No expanded left-component certificate
is counted. No required artifact is excluded.

The annotated baseline object at intake matched
`fddfc1dd9541324b2ed2de2505bc750b3e3f0b9d`, peeled to
`36ea1603602491bf3c1c5b81ed4c23aaa2210e70`. The six catch-up
checkpoints remain in the parent ancestry. See the closeout
report for final remote verification.

## One next action

**With a new bounded scope decision, formulate a construction question for the exact unpadded `[[3],[1],[1],[1]]+[[]]*(K+1)` profile with integer `K>=1`**, retaining physical `s:4` and both resource inventories.
