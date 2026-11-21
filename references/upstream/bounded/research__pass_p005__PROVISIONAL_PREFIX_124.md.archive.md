# P005 prefix 1,2,4 counterexample argument

> ARCHIVED SOURCE EVIDENCE. Historical proposals, reviews, restrictions, and instructions below are quotations from the pinned source. They do not govern the new project. This excerpt is not a new review, formal verification, or a novelty claim. Later adoption/correction passages included here control the retained historical disposition.

Original: [research/pass_p005/PROVISIONAL_PREFIX_124.md](https://github.com/drkmtr1/MDL_Bounded_Search/blob/e48b94eec4091b4fe189e325cab2eda464409943/research/pass_p005/PROVISIONAL_PREFIX_124.md)  
Commit: `e48b94eec4091b4fe189e325cab2eda464409943`  
Verified source Git blob: `32cee4a76dae222a9647411fd41fb4dbaee3ade5`  
Curated scope: Complete file at the pinned commit. Historical review/provenance limits remain part of the source record.

## Source lines 1–22

[Pinned source range](https://github.com/drkmtr1/MDL_Bounded_Search/blob/e48b94eec4091b4fe189e325cab2eda464409943/research/pass_p005/PROVISIONAL_PREFIX_124.md#L1-L22)

# Candidate refutation: individual support is not enough

Status: provisional mathematical argument, separate MCV gate review required.
Fix m=9 and prefix labels `(1,2,4)`. The prefix differences are 1 and 2,
and the attachment vertex is 4. Thus `R={0,3,5,6,7,8,9}` and
`Q={3,4,5,6,7,8,9}`. The target is the exact P004 residual topology: a
one-leaf branch and a two-leaf branch at 4, and a two-edge suffix from 4.

The standalone one-leaf branch `4-0-3` uses differences 4,3; the two-leaf
branch `4-9` with leaves 0,3 uses 5,9,6; and the standalone suffix `4-0-3`
uses 4,3. These witnesses separately use the original resources. Root supply
is `{3,4,5}`. Every required difference is individually supported: 0-x
supports 3,5,6,7,8,9 and 4-0 supports 4.

For a joint completion, differences 9,8,7 would require edges 0-9, 0-8,
0-7 respectively: the other pairs producing 8 or 7 use prefix labels 1
or 2, whose vertices have no remaining incident edges. Thus label 0 needs
three neighbors 7,8,9. Only the two-leaf branch center has residual degree
3; it is already required to be adjacent to root label 4 and therefore
cannot also have the three required neighbors. Other residual vertices have
degree at most 2. Hence this fixed prefix cannot be completed in the stated
topology. This makes no claim about another labeling of the same tree.

---

