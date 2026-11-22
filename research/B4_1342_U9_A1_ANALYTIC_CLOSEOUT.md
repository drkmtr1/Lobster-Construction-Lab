# B4-1342-U9-A1-ANALYTIC-CLOSEOUT-001

## Named original and scope

Use the [retained named original](../evidence/validation/B4_1342_UPPER_BLOCK_OBSTRUCTION_001/validation/originals/1342.json)
with ordered profile `[[1],[3],[4],[2],[]]`. Its five spine
vertices have the four consecutive spine edges. Four original
centers attach at the corresponding sections 0 through 3,
with respectively 1, 3, 4 and 2 terminals. Its order is 19
and its size is 18.

Let g be any graceful alpha labeling with low labels [0,8]
and high labels [9,18], with physical H=L=b:0:0 labeled 1,
Z=b:2:0 labeled 0, and U=s:4 labeled 9. The witness is the
named path b:0:0--s:0--s:1--s:2--s:3--s:4. Every vertex
is within two edges of it, H lies on it, and Z is one
edge away. For each integer c in [10,18], let S_c be the
vertices with label at least c and E_c their complete
original incident edge set. This is the strict port-preserving
threshold range in the [general-host rule](ALPHA_UPPER_BLOCK_GENERAL_HOST.md#exact-state-and-incident-edge-hypothesis).

**Claim A.** No such g and c supply the selected difference
multiset [c-1,18], once each.

**Claim B.** For every such g and c and every positive integer h,
the prescribed upper-block operation fails to give a graceful
labeling.

## Claim A: physical degrees and descending differences

Since s:4 is high, alternating the spine and then the actual
branch and terminal edges gives exactly the following highs.
The other nine vertices are low.

| High vertex | All original neighbors | Degree |
|---|---|---:|
| s:0 | s:1, b:0:0 | 2 |
| s:2 | s:1, s:3, b:2:0 | 3 |
| s:4 | s:3 | 1 |
| b:1:0 | s:1 and l:1:0:j for 0<=j<3 | 4 |
| b:3:0 | s:3 and l:3:0:j for 0<=j<2 | 3 |
| l:0:0:0 | b:0:0 | 1 |
| each l:2:0:j for 0<=j<4 | b:2:0 | 1 |

Each original edge has exactly one high end. The incident
sets of the selected highs are therefore disjoint, and their
degree sum is |E_c|. The bijection selects k=19-c vertices
and always excludes s:4. The other nine physical highs have
sorted degrees 1,1,1,1,1,2,3,3,4 and sum 17. The required
multiset [c-1,18] has 20-c=k+1 entries.

| c | k | Required count | Consequence of the original degrees |
|---:|---:|---:|---|
| 10 | 9 | 10 | All eligible highs selected, exactly 17 edges. |
| 11 | 8 | 9 | Minimum degree sum 13. |
| 12 | 7 | 8 | Minimum degree sum 10. |
| 13 | 6 | 7 | Equality requires s:0 and five degree-one highs. |
| 14 | 5 | 6 | Equality requires s:0 and four degree-one highs. |
| 15 | 4 | 5 | Equality requires s:0 and three degree-one highs. |
| 16 | 3 | 4 | Equality requires s:0 and two degree-one highs. |
| 17 | 2 | 3 | Equality requires s:0 and one degree-one high. |
| 18 | 1 | 2 | Equality requires s:0 alone. |

In every row with c>=13, equality would leave one unit
above the baseline of one edge per selected vertex. Only
s:0 has degree two. Equality would thus select s:0 and
exclude degree-three s:2. The original neighbors of Z
are s:2 and the four third terminals. Difference 18
must join label 18 to zero. Since label 18 is selected
and s:2 is excluded, its vertex is a third terminal
whose only edge goes to Z.

Assume all vertices of labels j+1 through 18 are such
terminals, for c<=j<=17. The original difference j must
have a high endpoint with label at least j. Larger high
labels supply only their own differences at the zero host.
Thus the high label is exactly j and its low endpoint
is again zero. As s:2 is excluded, this forces another
third terminal. Induction forces every selected vertex
to be a degree-one third terminal, contradicting s:0.
The base alone applies at c=18. The argument also yields
a contradiction if too many distinct terminals are required.

This independently reproduces the degree and descent
inferences of the [older U=10 proof](B4_1342_ALL_LEDGER_PINNED_OBSTRUCTION.md)
for c>=11. That proof uses U=10 in its count obstruction
only to orient the alpha bipartition and exclude physical
s:4 from selection. U=9 serves both purposes. The c=10
row here is additional. No other numerical value of the
older retained ledger is used. In particular, the new
argument contradicts count equality itself at all nine
thresholds, which proves Claim A.

## Claim B: necessary spectrum for a positive batch

Raise each old label at least c by h, keep lower old labels,
and attach the fresh named terminals l:0:0:j (1<=j<=h)
only to H with labels c+j-1. The fixed, fresh and shifted
label bands are [0,c-1], [c,c+h-1] and [c+h,18+h].
They partition the enlarged label alphabet [0,18+h].
The original incidences and physical exit stay fixed.

Every edge of E_c has exactly one shifted high end.
Write S for its set of old weights, which have no
multiplicities above one by original gracefulness.
For d0=c-1, the new difference multiset consists of
the unchanged [1,18] minus S, the shifted S+h, and the
fresh band [d0,d0+h-1] at H=1. To exhaust [1,18+h]
once each, the unchanged old difference inventory must
be [1,d0-1] and the selected inventory must be [d0,18].
Here is the [accepted necessity argument](B4_1342_U9_STRUCTURAL_OBSTRUCTION.md#necessity-for-every-positive-batch)
checked on these three bands.

If any selected weight is below d0, the least such weight
is missing from the result. It has no unchanged or fresh
copy, and a shifted copy would require a smaller selected
weight. For w from d0 through min(18,d0+h-1) a fresh
copy already exists, so w must be selected to avoid an
unchanged duplicate. For each later old w from d0+h
through 18, induct upward. The earlier selected w-h
creates a shifted copy, again forcing selection of w.
If the fresh interval extends past 18, the first step
already forces the entire old tail and the later step
is empty. This proves necessity for every positive h.
Claim A excludes that selected inventory, proving B.
The identity h=0 is outside Claim B.

## Exact disposition of the two interfaces

On this exact named original and fixed alpha orientation
with Z=0 and H=a in [1,8], the prescribed interface is
rejected for every positive batch in each row. Each
predicate below is [c-a,18].

| Physical exit | Host and permitted thresholds | Evidence |
|---|---|---|
| s:4=9 | a=1, c=10..18 | Analytic Claims A and B above. |
| s:4=9 | a=2..8, c=10..18 | [Accepted structural proof and batch necessity](B4_1342_U9_STRUCTURAL_OBSTRUCTION.md). |
| s:4=10 | a=1, c=11..18 | [Accepted pinned analytic proof](B4_1342_ALL_LEDGER_PINNED_OBSTRUCTION.md). |
| s:4=10 | a=2..8, c=11..18 | [Reviewed exhaustion of the predicate](B4_1342_RELAXED_HOST_SEED_RESULT.md) and analytic batch necessity. |

The last row can use the same necessity argument with
d0=c-a. All shifted old endpoints are high, H and U are
below c, and 1<=d0<=18, so the three bands and each
induction step still apply. The U=9 disposition is
entirely analytic. The U=10 relaxed-host predicate
disposition retains its reviewed computational basis.
These conclusions have no bearing on other exit labels,
hosts, cuts, ordinary graceful relabelings or existence
on any enlarged original tree. The accepted [all-positive
(1,r,t,2) construction](B4_1RT2_K1_DIRECT_SINGLETON.md)
remains separate. The [bounded audit](../evidence/validation/B4_1342_U9_A1_CLOSEOUT_001/README.md)
uses the 1342 original and 1122 positive control, with
no labeling enumeration.

## PIVOT after closeout

Retire these two exact exit interfaces unless new mathematics
supplies a reason to reopen them. A future bounded task can
compare the [q-only core](B4_Q1T2_K1_ROOTED_CORE.md) and
[r-only core](B4_1R32_K1_ROOTED_CORE.md) on the joint named
core `[[q],[r],[],[2],[],[]]` with q,r>=2, starting at
q=r=2. The desired ordinary graceful labeling has the
maximum m at the original physical s:2.

Conditionally on that root property, translating the core
by one preserves differences [1,m] and occupies labels
[1,m+1]. Restoring the original b:2:0 at zero uses
difference m+1 on s:2--b:2:0. Attaching the prescribed
third terminals with labels m+2 through m+t+1 uses those
same differences at zero. Together both complete
inventories partition the enlarged alphabets, preserving
the named incidences and the core's K=1 spine. This is the
[accepted translate-and-zero-root lift](B4_1RT2_K1_DIRECT_SINGLETON.md)
conditional on independent maximum-rooted supply. Joint
core existence and any K>=2 continuation remain open.
