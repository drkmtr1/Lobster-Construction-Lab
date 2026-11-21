# P004 fixed-prefix counterexample

> ARCHIVED SOURCE EVIDENCE. Historical proposals, reviews, restrictions, and instructions below are quotations from the pinned source. They do not govern the new project. This excerpt is not a new review, formal verification, or a novelty claim. Later adoption/correction passages included here control the retained historical disposition.

Original: [research/pass_p004/C1_COUNTEREXAMPLE.md](https://github.com/drkmtr1/MDL_Bounded_Search/blob/e48b94eec4091b4fe189e325cab2eda464409943/research/pass_p004/C1_COUNTEREXAMPLE.md)  
Commit: `e48b94eec4091b4fe189e325cab2eda464409943`  
Verified source Git blob: `1556749d6f2f35aea755dc50d219592561a220d9`  
Curated scope: Complete file at the pinned commit. Historical review/provenance limits remain part of the source record.

## Source lines 1–25

[Pinned source range](https://github.com/drkmtr1/MDL_Bounded_Search/blob/e48b94eec4091b4fe189e325cab2eda464409943/research/pass_p004/C1_COUNTEREXAMPLE.md#L1-L25)

# P004-C1 counterexample: fixed-prefix local compatibility

Take m=9 and fix path labels `(a,b,c)=(0,1,3)`. The prefix differences are
1 and 2, so the unused labels are `R={2,4,5,6,7,8,9}` and the unused
differences are `Q={3,4,5,6,7,8,9}`. At c=3 the available root differences
are `{3,4,5,6}`, so S=4 >= 3.

Each requested component is feasible using the original resources independently:

- One-leaf branch: `c=3, u=6, v=2`, edge differences 3,4.
- Two-leaf branch: `c=3, x=9, y=2, z=4`, edge differences 6,7,5.
- Two-edge suffix: `c=3, d=6, e=2`, edge differences 3,4.

These three witnesses need not be mutually compatible. A simultaneous
completion must use difference 9. Its only possible endpoints among labels
0..9 are 0 and 9. Vertex a already has label 0, and in the specified complete
topology its only neighbor is b, whose fixed label is 1. Thus no edge can have
difference 9, so no simultaneous completion exists. This is an elementary
proof of failure for this fixed prefix; it is not a nongraceful-tree result.
The separate reviewer identified this argument; the two bounded implementations
also independently exhausted the corresponding role assignments.

Case ID `0caffda95c62846c1fa53746ef7af6bbe541e790bb919553c6300c2aa12f6176`;
see `COMPATIBILITY_PLAN.md` and the two P004-C1 SQLite checkpoints for inputs,
predicate results, witnesses, attempt hashes, and limits.

---

