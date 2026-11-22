# B4-JOINT-22-CUT-COMPAT-001

## Named seed and the complete cut condition

Use the verified Case B ledger from the
[direct construction](B4_JOINT_22_DIRECT_LEDGER.md) on the
[retained 15-vertex original](../evidence/validation/B4_JOINT_22_DIRECT_LEDGER_001/validation/core_original.json).
Its three branches attach at sections 0, 1 and 3. The
physical spine has labels 13,1,14,0,7,5 in order. The
first center is 2 with terminals 12,11, the second is 9
with terminals 4,8, and the fourth is 6 with terminals
3,10. The spine witnesses every vertex within distance
two. Both growth hosts lie one edge from the spine.
The prior Case A ledger is a negative control with
duplicate weight 2 and missing weight 6.

For a graceful ledger with maximum m, let E_c be the set
of old edges with exactly one endpoint label below c and
one at or above c. Shift every old label at least c by h
and give fresh terminal i at the prescribed host label
c+i-1, for 1<=i<=h. Original edges in E_c gain h in
weight. Every other edge keeps its difference, including
an edge with both endpoints above the cut.

Let b be the old host label. If b<c, a fresh leaf has
weight c+i-1-b and the new weights start at d0=c-b.
This is the low-side arithmetic of the
[q-only core](B4_Q1T2_K1_ROOTED_CORE.md). If b>=c the host
also shifts and the fresh weight is b+h-(c+i-1), giving
the same contiguous new band [d0,d0+h-1] with d0=b-c+1.
The latter is the [ordinary high-side cut rule](ORDINARY_CUT_LEAF_INSERTION.md)
used by the [r-only core](B4_1R32_K1_ROOTED_CORE.md).
Consequently either side requires the complete crossing
tail [d0,m]. The fixed, fresh, and shifted label bands
are [0,c-1], [c,c+h-1], and [c+h,m+h]. The complete
crossing tail gives disjoint new weight bands [1,d0-1],
[d0,d0+h-1], and [d0+h,m+h], with empty intervals
understood as empty.

For necessity at every h>=1, assume the resulting weight
multiset is [1,m+h]. If any crossing weight lies below
d0, the least such old weight is missing: it cannot be
unchanged or fresh, and its shifted copy would need a
smaller crossing weight. For w from d0 to min(m,d0+h-1)
a fresh edge already provides w, forcing the old w to
cross or else repeat. For subsequent w up to m the
already crossing w-h supplies the shifted w and forces
the same conclusion. An empty induction range, including
d0=m+1, has no further condition. Thus the cut predicate
is necessary as well as sufficient for a positive batch
of this exact operation. At c=0 and c=m+1 the crossing
set is empty, so those arithmetic comparisons require,
respectively, b=m and b=0. They are not proper cuts and
c=m+1 would in any case place the new maximum on a leaf.

## Complete spectra on the original and one-leaf output

Each original edge of weight d crosses exactly when
min(label endpoints)<c<=max(label endpoints). The
following ledger therefore derives the whole spectrum
at every integral c. The complete named per-threshold
ledgers, including each host's required tail, are in the
[cut arithmetic](../evidence/validation/B4_JOINT_22_CUT_COMPAT_001/audit_result.json).

| Original edge | Weight | Crosses at c |
|---|---:|---|
| b:1:0--l:1:0:1 | 1 | 9 |
| s:4--s:5 | 2 | 6..7 |
| b:3:0--l:3:0:0 | 3 | 4..6 |
| b:3:0--l:3:0:1 | 4 | 7..10 |
| b:1:0--l:1:0:0 | 5 | 5..9 |
| s:3--b:3:0 | 6 | 1..6 |
| s:3--s:4 | 7 | 1..7 |
| s:1--b:1:0 | 8 | 2..9 |
| b:0:0--l:0:0:1 | 9 | 3..11 |
| b:0:0--l:0:0:0 | 10 | 3..12 |
| s:0--b:0:0 | 11 | 3..13 |
| s:0--s:1 | 12 | 2..13 |
| s:1--s:2 | 13 | 2..14 |
| s:2--s:3 | 14 | 1..14 |

At the first center b=2 the complete tail matches exactly
c=11,12,13. These have spectra [9,14], [10,14], and
[11,14]. The other proper cuts have explicit falsifiers.
At c=1,2,3,4,5 a required weight 2,1,1,2,4 respectively
is missing. At c=6,7,8,9,10 the crossing spectrum includes
an unwanted 2,2,4,1,4 respectively. At c=14 weight 12
is missing. Both endpoints have empty spectra and require
nonempty tails.

At c=11 the shifted vertices are s:0, s:2, l:0:0:0 and
l:0:0:1. Their six crossing edges have weights 9..14 and
all other original weights 1..8 are unchanged. The
candidate one-leaf output keeps the weight 1..8 intervals
in the table. It adds weight 9 on b:0:0--l:0:0:2,
crossing at 3..11. The intervals for old weights 9..14
keep their lower limits, increase their upper limits by
one, and now represent weights 10..15. This derives all
c=0..16 spectra for that exact output.

The second center b=9 is unchanged in both ledgers.
For c<=9 its required tail starts at 10-c, and for c>=10
it starts at c-9. Neither ledger has a matching cut:

| c | Falsifier common to both ledgers |
|---|---|
| 0 | Required tail is nonempty, and no old edge crosses. |
| 1,2 | Required weight 9 is missing. |
| 3 | Unwanted weight 6 crosses. |
| 4,5 | Unwanted weight 3 crosses. |
| 6 | Unwanted weight 2 crosses. |
| 7 | Required weight 3 is missing. |
| 8,9 | Required weight 2 is missing. |
| 10 | Required weight 1 is missing. |
| 11 through the respective last cut | Required first weight c-9 lies in [2,7], and none of these weights crosses. |

This rejects second-center insertion for every positive
batch from the exact Case B ledger and its exact c=11
one-leaf output. These two failed interfaces supply
no two-host compatibility theorem. They leave other
graceful ledgers, other growth operations and further
parameters outside the negative.

## First-center construction at c=11

For every exact integer h>=0 put q=h+2. Keep all
original labels below 11. Shift the four original
vertices at or above 11 by h. Attach only the original
new names l:0:0:j for 2<=j<q to b:0:0, with label j+9.
This produces the exact core `C(q,2)=[[q],[2],[],[2],[],[]]`
with q+13 vertices and maximum m=q+12 at physical s:2.

| Named vertices | Complete core formula f_q |
|---|---|
| s:0,s:1,s:2,s:3,s:4,s:5 | q+11,1,q+12,0,7,5 |
| b:0:0,l:0:0:0,l:0:0:1 | 2,q+10,q+9 |
| l:0:0:j for 2<=j<q | j+9 |
| b:1:0,l:1:0:0,l:1:0:1 | 9,4,8 |
| b:3:0,l:3:0:0,l:3:0:1 | 6,3,10 |

The label bands are fixed [0,10], fresh [11,q+8], shifted
[q+9,q+12]. The actual weight bands are fixed [1,8],
fresh [9,q+6] because the host stays at 2, and shifted
[q+7,q+12]. Each is filled once. At h=0 both fresh bands
are empty, and the ledger is Case B. No old incidence
moves, and each fresh leaf has one edge to the original
first center. The named spine still witnesses every
vertex within distance two.

For continued batches advance the cut to c'=11+h=q+9.
Exactly the four original selected vertices remain at
or above it, with the original six crossings now
[q+7,q+12]. Neither the old low side nor any fresh leaf
moves in the next batch. The next fresh labels start at
c', and another batch k increases the four original labels
by k. Thus every grouping of successive prescribed names
gives the same labels as one concatenated batch in that
name order. Finite growth is pointwise on the named
graph and never changes either physical port s:4 or s:5.
This supplies the stated core independently of t and any
completed lift.

## Zero-host lift and original singleton

For every exact integer q>=2 and t>=1 translate the
core formula by one, restore b:2:0=0 at original s:2,
and give l:2:0:j the label q+14+j for 0<=j<t. Restore
exactly s:2--b:2:0 and the t named terminal incidences at
its center. The resulting original `[[q],[2],[t],[2],[],[]]`
has q+t+14 vertices and maximum M=q+t+13. The full label
partition is {0}, [1,q+13], [q+14,M]. Translation keeps
all old differences [1,q+12], the edge at physical
s:2=q+13 gives {q+13}, and the fresh terminal weights
equal their labels [q+14,M]. These partitions are
complete for every parameter pair, including t=1.

Withhold only s:5. Original s:4 retains value 8 after
translation and s:5 has only that neighbor. The missing
label is f_q(s:5)+1=6 and the missing difference is
|f_q(s:4)-f_q(s:5)|=2. Thus R={6}, D={2} at physical
s:4=8. Assign s:5=6 to complete the original edge.
The two branch families keep all named incidences and
the spine witness, with no extra section or connecting
edge. K=1 and r=2 are fixed. Neither arbitrary second
growth nor K>=2 continuation follows.

[Bounded evidence](../evidence/validation/B4_JOINT_22_CUT_COMPAT_001/README.md) covers four new
graphs and rechecks the two existing ledgers on the same
original. No search or labeling enumeration was used.
