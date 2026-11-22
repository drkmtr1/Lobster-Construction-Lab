# B4-1342-U9-STRUCTURAL-OBSTRUCTION-001

## Exact physical scope

Let `T=[[1],[3],[4],[2],[]]` be the [retained named original](../evidence/validation/B4_1342_UPPER_BLOCK_OBSTRUCTION_001/validation/originals/1342.json).
It has five consecutive spine vertices `s:0` through `s:4`,
the four attachments `s:i--b:i:0` for i=0,1,2,3,
and ten terminal edges from `b:i:0` to `l:i:0:j` at the
prescribed indices. Its order is 19 and its size is 18.

Let g be any graceful alpha labeling with low [0,8] and high
[9,18], physical `Z=b:2:0=0`, exit `U=s:4=9` and low port
`H=L=b:0:0=a` for an integer 2<=a<=8. The threshold c is
any integer 10<=c<=18. This is exactly the threshold range
allowed by the [general-host rule](ALPHA_UPPER_BLOCK_GENERAL_HOST.md)
while keeping U=9. The named path
`b:0:0--s:0--s:1--s:2--s:3--s:4` is a witness: H lies on it,
Z and the other off-path centers are one edge away, and each
terminal is at distance at most two. No vertex is renamed.

**Claim A.** No such g and c supply the complete selected
incidence spectrum [c-a,18].

**Claim B.** On the same domain the prescribed first-host
upper-block operation fails to give a graceful labeling for
every positive integer batch h. Claim A alone proves only
failure of a premise. The necessity proof below establishes B.

## Forced orientation and labels

Alternate the two alpha classes along the actual spine from
high s:4, then along each original center and terminal edge.
The ten physical highs and all their original neighbors are:

| Physical high | Original neighbors | Degree |
|---|---|---:|
| s:0 | s:1, H | 2 |
| s:2 | s:1, s:3, Z | 3 |
| s:4 | s:3 | 1 |
| b:1:0 | s:1 and the three l:1:0:j | 4 |
| b:3:0 | s:3 and the two l:3:0:j | 3 |
| l:0:0:0 | H | 1 |
| each l:2:0:j, 0<=j<4 | Z | 1 |

The other nine vertices are low. Each original edge occurs
once in this ledger because it has precisely one high end.
The set S_c of vertices at or above c excludes U and has
k=19-c vertices. The selected incident sets at these highs
are disjoint, so the selected weight count is the sum of
their degrees. The required interval [c-a,18] has k+a entries.
Thus under Claim A's putative premise the sum of deg(v)-1 over
S_c must equal a.

Difference 1 has only the alpha pair (8,9). The unique
neighbor of U=9 is s:3, so s:3=8 and a cannot be 8.

Under the putative premise, s:2 must be selected. Otherwise
difference 18 forces label 18 at a third terminal, since its
low endpoint must be Z and the other neighbor of Z is
unselected s:2. Descend from j=17 down to c. A high endpoint
with label below j cannot supply j against a nonnegative low.
Any higher label has already been forced onto a third terminal
whose single edge to zero supplies its own larger difference.
Thus the high endpoint for j has label j and touches zero, so
it too is a third terminal. This induction includes c=18 by
its base alone. All selected highs would have degree one,
giving excess zero in contradiction to a>=2.

At c=10 all highs except s:4 are selected, with degree sum 17.
The required count 9+a forces a=8, already excluded.

For c>=11, difference 2 can only come from (7,9) or (8,10).
U=9 meets only s:3=8, ruling out (7,9). The high neighbors
of s:3 are U, selected s:2 with label at least 11, and b:3:0.
Therefore b:3:0=10 and is unselected.

## Complete physical-subset reduction

Put d0=c-a. Since g is graceful, the unselected edges must
supply exactly [1,d0-1] if the selected edges supply [d0,18].
Every unselected high neighbor of Z would have its own high
label as its edge difference, so that label would lie in
[11,d0-1] with 9 and 10 occupied by U and b:3:0 elsewhere.
But the selected s:2--s:3 has difference at most 18-8=10,
so d0<=10. The interval for an unselected zero neighbor
is empty. All four third terminals are selected with s:2.

These five mandatory highs have excess two. The only
optional highs are s:0, b:1:0 and l:0:0:0, with excesses
1,3,0 respectively. For c=11 choose all three, for c=12
choose exactly two, and for c=13 choose exactly one.
The lone l:0:0:0 option at c=13 gives a=2 and d0=11,
which violates d0<=10. For c=14 the mandatory five alone
give a=2 and d0=12, which also violates it. For c>=15,
k<=4 cannot fit the mandatory five. Hence the full 7-by-9
grid leaves only the following six pairs, each with exactly
one physical set beyond the mandatory five.

| c | a | Additional selected highs |
|---:|---:|---|
| 11 | 6 | s:0, b:1:0, l:0:0:0 |
| 12 | 3 | s:0, l:0:0:0 |
| 12 | 5 | b:1:0, l:0:0:0 |
| 12 | 6 | s:0, b:1:0 |
| 13 | 3 | s:0 |
| 13 | 5 | b:1:0 |

## Six contradictions on the original incidences

Throughout, s:4--s:3 and b:3:0--s:3 are unselected
edges of weights 1 and 2. Write F for b:3:0=10. Its two
remaining edges go to the two physical fourth terminals.
Their ordered names need no symmetry convention.

- **(11,6).** U and F are the only unselected highs and the
  unselected band is [1,4]. The two F terminal weights must be
  3,4, requiring labels 7,6. The host H already occupies 6.
- **(12,3).** The remaining unselected high is b:1:0=11 and
  the band is [1,8]. Weight 3 cannot come from 11 because s:3
  already has 8 and is outside its neighborhood. Weight 8
  cannot come from 11 because H already has 3 and is outside
  its neighborhood. Thus the two F terminals give weights 3
  and 8, using 7 and 2. The four b:1:0 edges must then use
  weights 4,5,6,7. Weight 4 requires the label 7 at one of its
  neighbors, distinct from the fourth terminal carrying 7.
- **(12,5).** The remaining unselected high is s:0=11 and
  the band is [1,6]. The edge s:0--H gives 6. Weight 5
  cannot come from an F terminal, which would need H's label 5.
  The only remaining edge for it is s:0--s:1, forcing s:1=6.
  F's terminal weights 3,4 force 7,6, duplicating s:1.
- **(12,6).** The remaining unselected high is
  l:0:0:0=11 with one edge to H giving 5, in band [1,5].
  The remaining weights 3,4 on F's terminal edges again
  require 7,6 while H already has 6.
- **(13,3).** The selected band is [10,18]. The selected
  edge s:2--s:3 forces s:2=18, giving weights 10 to s:3
  and 18 to Z. If v=g(s:0), the four third terminals use
  [13,17] except v. Their weights equal their labels, leaving
  exactly {11,12,v} on s:0--H, s:0--s:1 and s:2--s:1.
  The first weight is v-3. It cannot equal v, so v=14 or 15.
  At v=14 the remaining weights {12,14} differ by 2 but their
  high endpoints differ by 4. At v=15 the remaining weights
  {11,15} differ by 4 but their high endpoints differ by 3.
  In both cases the two edges share s:1, so those differences
  must agree. This uses the selected edges alone and applies
  for either assignment of 11 and 12 to the two unselected
  highs b:1:0 and l:0:0:0.
- **(13,5).** The unselected highs besides U and F are
  s:0 and l:0:0:0 with labels 11,12 in either order. Their
  two H edges contribute 6,7 in the band [1,7]. The
  remaining weights are 3,4,5 on F's two terminal edges and
  s:0--s:1. Weight 5 at F would require H's label 5, so
  s:0--s:1 supplies it. If s:0=11 this forces s:1=6, and
  if s:0=12 it forces s:1=7. F's terminal weights 3,4
  require 7,6 in either ordering, repeating s:1's label.

This proves Claim A universally over the restricted domain.

## Necessity for every positive batch

Use the prescribed batch h>=1. Keep all original labels below
c, raise the others by h, and attach fresh named first terminals
l:0:0:j, 1<=j<=h, only to H, with labels c+j-1.
The three consecutive label bands are [0,c-1], [c,c+h-1]
and [c+h,m+h] with m=18. All original incidences and the
port label 9 stay fixed. Each selected edge has just one
shifted high endpoint. With S the set of its old differences,
the new difference multiset consists of unchanged [1,m] minus
S, the weights S+h, and the new leaf interval [d0,d0+h-1].
Here 1<=d0<=m.

If the result is graceful, no old weight below d0 is selected.
Otherwise choose the smallest selected weight w<d0. It has no
unchanged occurrence and no new leaf occurrence, and a
shifted occurrence would require the smaller selected w-h.
Thus w would be missing.

For each w in [d0,min(m,d0+h-1)], a fresh leaf already supplies
w, so w cannot also remain unchanged. Hence w belongs to S.
Induct upward for w in [d0+h,m]. The smaller w-h is at least
d0 and has already been shown selected, so it supplies w
after shifting. Again w must be selected to avoid duplication.
If the inserted interval extends past m, its intersection
with the old alphabet already forces the whole tail and the
second induction is empty. Thus S=[d0,m] is necessary for
each h>=1. In this application gracefulness of the original
g gives each difference once, so the necessary set is exactly
the necessary multiset as well. Claim A now proves Claim B.
An empty batch acts as the identity and is outside the negative.

## Evidence and boundary

The [evidence bundle](../evidence/validation/B4_1342_U9_STRUCTURAL_OBSTRUCTION_001/README.md)
uses the retained 1342 certificate with U=10 solely to
check graph identity and the previous result. The [1122
positive control](../evidence/validation/B4_UNPADDED_Q1T2_001/validation/retained_seed.json)
with H=4, U=8 and c=9 still supplies its own [5,14] spectrum.
The two controls do not supply a labeling for the U=9 question.
The earlier [U=10 relaxed-host result](B4_1342_RELAXED_HOST_SEED_RESULT.md),
[pin-one obstruction](B4_1342_ALL_LEDGER_PINNED_OBSTRUCTION.md)
and [fixed-ledger obstruction](B4_1342_FIXED_LEDGER_UPPER_BLOCK_OBSTRUCTION.md)
have separate scopes and evidence. The new proof excludes the
stated insertion predicate, and Claim B the stated operation.
Gracefulness without that predicate, alpha labelings with the
two pins alone and other operations remain outside these claims.
