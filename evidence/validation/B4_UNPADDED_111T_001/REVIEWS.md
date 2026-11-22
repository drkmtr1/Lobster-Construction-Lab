# Separate AI review dispositions

Both reviewers were read-only. The integrator was the sole working-tree
writer. These are project AI reviews of the actual proof, implementation
and recorded evidence.

## Mathematical review — ACCEPT

Reviewer `b4111t_math` rederived both label and original-edge partitions
and checked the exact named target and suffix. Both left-component
spectra and actual port witnesses satisfy the retained binary R241
rule. The L008 right component and its K=1 extension at the actual
maximum-labeled endpoint yield compatibility 0=0 and 1=1, respectively.
Only the original edge `s:2--s:3` is restored. Actual returned ports are
`b:0:0` and `s:4`, with offsets (2,1) for the unshifted K>=2 seed
and (0,1) for the K=1 full labeling. The reviewer checked the
reflect-and-prepend proof, its bridge from reflected 0, its termination,
and the distinct singleton resources and alpha threshold. The K=2
suffix illustrates why the K>=2 branch has an ordinary-gracefulness
claim. The t=1 adjacent alpha branch retains its scope. No mathematical
correction was required. The reviewer inspected
`research/B4_UNPADDED_111T.md` and the retained pinned arguments and ran
no constructions or searches.

## Implementation review — ACCEPT

Reviewer `b4111t_impl` inspected the actual diff, unchanged verifier and
parser, targeted tests, and regression and audit scripts. It checked
strict integer and exact-profile admission, both dispatch paths,
original-target independence, copied prefix labels, and the actual
`s:4` frontier and original suffix edges. It checked the normalized
path starts at the supplied port, the continuation starts assigning
at `s:5`, and the singleton branch checks its difference and alpha
cut. The 10,000/10,001-vertex parameter preflight is distinct from
the inherited 2 MB record cap.

A read-only inspection of saved JSON verified 23 source hashes,
configuration and script links, all 12 original graph digests and
bijections, both resource inventories, original suffixes, four K=1
alpha cuts, and two separately recorded component certificates. The
initial audit failed on vertex list order. The retry preserves
multiplicity, named edges and exact assignments, binds to the same
unchanged regression and both script identities, and adds zero
targets. Both CLI records match cases in the declared set, the demo
certificate passed, and all three source/config/record hash sets
matched. The retained command outputs show 53 targeted method passes
in 11 modules. No code revision was required. The reviewer ran no
constructors, tests or saved audit scripts.
