# D213 structural limit for simultaneous all-center safe-gap growth

**PROVED WITHIN EXACT SCOPE.** A simultaneous D212 certificate at all branch centers of the exact original `[[p],[q_1,...,q_ell],[b],[t]]`, with positive integer quotas, requires ℓ≤10. This bound applies to the specified architecture for any graceful base labeling. The three D212 bases remain INCOMPLETE and mathematically undecided. No assertion of sharpness is made.

## 1. Component bound for a compatible selection

Let T be a finite graceful tree with labels [0,n]. A proper cut c lies in [1,n] and has lower side f<c and upper side f≥c. A selected cut is safe if its actual crossing weights are [D(c),n]. For each selected cut there is a distinct actual host with label a. Use the exact D212 host constants and equalities of selected spans with the smaller-threshold sets. Write c* for the selected cut of minimum threshold in a nonempty selection. Let h₋,h₊ count selected hosts below and at or above c*. Define C₋,C₊ by taking on each side the induced graph on the vertices of degree at least two **in T** and counting its connected components, including isolated vertices. An empty induced graph has zero components. The bounds are

```text
h₊ ≤ C₋ + 1,
h₋ ≤ C₊ + 1.
```

**Nested actual edges and host sides.** Write X(c) for the set of actual crossing edges at c. Gracefulness gives each edge weight a unique identity. The crossing-weight upper intervals give X(c)⊆X(c*) for every selected c. Safe cuts have distinct thresholds. If two proper cuts shared a threshold, their crossing edge sets would coincide. The nonempty proper band between them has an external edge by connectedness, and that edge crosses exactly one of the two cuts.

For each nonminimum cut c, the D212 span of its host contains c*. If the host is upper relative to c, its span is c<c'≤a. Thus c<c*≤a. If the host is lower relative to c, its span is a<c'<c, so a<c*<c. At c* itself, the host belongs to just one of these two groups according to its label relative to c*. Accordingly all hosts counted in h₊ are upper relative to their own cuts, and their cuts lie at or below c*. All hosts counted in h₋ are lower relative to their own cuts, and their cuts lie at or above c*. The host at c* contributes once, even when its label equals c*.

**The exact edge partition for a band.** Take any two upper-host cuts c'<c, so c≤c*. They need not be consecutive integers or consecutive among the selected cuts. D(c')>D(c): if D(c')<D(c), the upper host at c would have to include c'<c in its rightward D212 span. This is impossible, and thresholds are distinct. Therefore X(c')⊆X(c).

Partition all vertices into three blocks by label, f<c', c'≤f<c, and f≥c. Call the middle block U. Edges joining the first and third blocks cross both cuts. Edges from U to the first block cross c' only and are absent by nesting. Edges from U to the third block cross c only. They are precisely the difference X(c)∖X(c'), so the total number of external edges of U is exactly D(c')−D(c). Internal edges of U cross neither cut and are unconstrained by this count. Every edge leaving U also crosses c*, since it belongs to X(c)⊆X(c*). Its U endpoint is below c*. Consequently the other endpoint is at or above c*. This shows that U has **no external edge inside the lower side of c***. It covers c=c* and does not depend on the edges internal to U.

**A separate component for each band.** If every vertex in U has degree one in T, no edge can join two of them. An edge between two degree-one vertices would make that pair a connected component of the entire tree, contradicting that U is proper in a connected T. For a band between two proper cuts, both outer blocks are nonempty. Thus the external edge count in the all-leaf case is the number c−c' of vertices in U. The upper-host constants would then coincide, since

```text
a(c') = c' + D(c') − 1
      = c' + D(c) + (c−c') − 1
      = c + D(c) − 1 = a(c).
```

This contradicts the distinct actual hosts and injective labels. So U contains a nonleaf of T. It has no exit inside the lower side, even through vertices outside the induced nonleaf graph, and therefore contains an entire nonempty component of that graph. Different consecutive bands are disjoint and no component can meet two of them. If h₊≥2 there are h₊−1 such bands, proving h₊−1≤C₋. For h₊=0 or 1 the asserted bound is immediate and uses no band.

**Other orientation and small trees.** Complement f by n−f and write ĉ=n+1−c, ĉ'=n+1−c', â=n−a for the complemented own cut, other cut, and host. Crossing edges and thresholds stay the same. The lower constant a=c−D becomes â=ĉ+D−1, and the lower span a<c'<c becomes ĉ<ĉ'≤â. Complementation is an involution, so upper conditions also become lower conditions. The original lower hosts become upper hosts and the original upper induced nonleaf graph becomes the lower one. Applying the proved inequality gives h₋≤C₊+1, including empty and singleton groups. For n=0 there is no proper cut or nonempty selection. For n=1 there is only one proper cut, both induced nonleaf graphs are empty, and at most one distinct host is selected. No separating-band argument is needed in either boundary case. An empty selection has no c* and the theorem is stated for nonempty selections only. [D212 exact span conditions](SIMULTANEOUS_SAFE_GAP_QUOTA_GROWTH.md#2-exact-local-starts-and-independent-width-coefficients)

## 2. Count the nonleaf components in the four-section original

Use the named spine s:0, s:1, s:2, s:3 in that order. Its three noncentral sections have one actual center each, and s:1 has exactly ℓ central centers. Every center has its own positive quota of actual pendant terminals. The nonleaf graph of the original is exactly the spine with its actual centers attached. Each spine endpoint has degree two, both internal spine vertices are nonleaves, each center has degree at least two because its quota is positive, and every terminal has degree one. No vertex or edge is suppressed or renamed.

Complement if necessary so s:1 is lower relative to c*. Write x,y for the upper and lower central center counts, t₊ for the upper count among the three noncentral centers, A for the noncentral upper centers at lower spine parents, B for the noncentral lower centers at upper spine parents, and u for the number of upper spine vertices. Let r₋ and r₊ count the contiguous lower and upper runs of the actual spine, with zero runs on an empty side.

Each same-side spine run gives one component. A center with a same-side parent attaches to that component and leaves its count unchanged. A center with an opposite-side parent is isolated in its side's induced nonleaf graph. It cannot connect two runs, because its only other neighbors in the original are terminals. Every upper central center is isolated and every lower central center is attached to s:1. Thus

```text
C₋ = r₋ + B,
C₊ = r₊ + x + A.
```

With all centers selected, h₊=x+t₊ and h₋=y+3−t₊. The component inequalities give

```text
x+t₊     ≤ r₋ + B + 1,
y+3−t₊  ≤ r₊ + x + A + 1.
```

The second inequality gives x+y ≤ r₊+2x+A+t₊−2. Substitution of the first yields

```text
ℓ ≤ 2r₋ + r₊ + 2B + A − t₊ ≤ 2r₋ + r₊ + 2u.
```

Here A≤t₊ by inclusion. Every upper spine vertex is noncentral and has exactly one center, so each B center uses a distinct one of the u upper spine parents, giving B≤u. All eight side words with s:1 lower give the following symbolic counts.

| Sides of s:0,s:1,s:2,s:3 | r₋ | r₊ | u | 2r₋+r₊+2u |
|---|---:|---:|---:|---:|
| LLLL | 1 | 0 | 0 | 2 |
| LLLU | 1 | 1 | 1 | 5 |
| LLUL | 2 | 1 | 1 | 7 |
| LLUU | 1 | 1 | 2 | 7 |
| ULLL | 1 | 1 | 1 | 5 |
| ULLU | 1 | 2 | 2 | 8 |
| ULUL | 2 | 2 | 2 | 10 |
| ULUU | 1 | 2 | 3 | 10 |

These cases exhaust three independent side choices. The maximum of the displayed necessary bounds is 10. The table does not assert that any side word or equality at 10 is attainable by a graceful labeling with the required certificate.

## 3. Prescribed hand controls

For the named path P0–P1–P2–P3–P4, the original labels are (0,4,1,3,2). The actual consecutive edge weights are (4,3,2,1), whose cut intervals are [1,4], [2,4], [2,3], [3,3]. The safe spectra at cuts 1,2,3,4 are respectively [4,4], [2,4], [1,4], [3,4].

**Positive.** Use P1 (label 4) at cut 1 with threshold 4, and P3 (label 3) at cut 2 with threshold 2. Both upper-host constants hold. The span for cut 1 contains the selected cut 2, and the span for cut 2 contains no other selected cut. Thus c*=2. On the lower side only P2 (label 1) is a nonleaf, giving C₋=1. On the upper side P1 and P3 are separate nonleaf components, giving C₊=2. Both hosts are upper, so h₊=2=C₋+1 and h₋=0≤C₊+1. The separating band between cuts 1 and 2 consists of the nonleaf P2, whose two external edges have weights 3 and 2, the difference of thresholds 4−2.

For widths u₁ at cut 1 and u₂ at cut 2, the actual old labels are (0,4+u₁+u₂,1+u₁,3+u₁+u₂,2+u₁+u₂). Their four edge weights in order are (4+u₁+u₂,3+u₂,2+u₂,1). The two new label gaps [1,u₁] and [2+u₁,1+u₁+u₂] at the actual P1 and P3 hosts give the weight intervals [4+u₂,3+u₁+u₂] and [2,1+u₂]. These complement the old four weights exactly, with an empty interval if the corresponding width is zero. The singleton P2 witnesses the two actual positive centers, with their original terminal names retained.

**Adverse.** At cut 2 with D=2 use P0 (label 0), and at cut 3 with D=1 use P4 (label 2). Both lower constants hold and a single chosen cut has no coefficients to match. For cut 2 the earlier threshold cut 3 is outside the lower span, so the joint condition fails. At unit widths the old labels are (0,6,1,5,3) and the old weights are (6,5,4,2). New label 2 at P0 gives weight 2 again. New label 4 at P4 gives weight 1. Weight 3 is missing. This control tests an incompatible selection and supplies no premise for the component bound. [Retained D212 controls](SIMULTANEOUS_SAFE_GAP_QUOTA_GROWTH.md#4-prescribed-path-controls)

## 4. Scope and strategic consequence

The component theorem counts exactly the selected hosts, so it applies to subset certification too. The deduction ℓ≤10 uses h₊ and h₋ for **all** centers, and does not forbid certifying a suitable subset in an original with ℓ>10. For ℓ>10 the exact original cannot supply one simultaneous D212 certificate supporting independent growth of every center. This removes the intended unbounded all-center route, regardless of base-label search or the size of the positive quotas. Neither the component lemma nor the numeric bound settles ordinary gracefulness, subset renewal, sequential constructions with independently renewed states, or allocations and reconstructions outside the matched-gap placement. B2, B3 and B4 have ℓ=2,3,4. All remain INCOMPLETE and mathematically undecided under their registered scope. No case classification was attempted.

[D210](ORDINARY_SPINE_SIMULTANEOUS_ORDINARY_SUPPLIER.md) and [D211](ORDINARY_SPINE_COORDINATED_FOUR_HOST_SUPPLIER.md) label a partial tree on the whole original and supply coordinated residual differences directly. Their proved layouts have two central centers and stated parity or quota domains. Their ordinary constructions remain valid. [R226](../references/upstream/mdl/N226_R226_two_host_completion.md) treats actual two-host choices in a supplied residual instance. [R232](../references/upstream/mdl/N232_R232_joint_allocation.md) coordinates allocations across supplied disjoint two-host palettes, with its singleton-forest and pair-capacity conditions. These mechanisms leave scope for simultaneous cross-host allocation outside the matched-gap architecture. Both start with a supplied partial labeling and residual resources; a supplier for arbitrary center multiplicity would still need to construct those inputs. D212 still offers a direct independent-quota lift at compatible bounded subsets of hosts. A construction that renews a usable state when inserting a center can forgo growth certificates at earlier centers. The current proof supplies no such state. The separate D212 host-side boundary-closure candidate stays held.

**One mathematical obligation for Director consideration.** Prove a renewable central-center insertion theorem on the exact named family `[[1],[q_1,...,q_ell],[1],[1]]`: start from an independently supplied nonempty ordinary labeling state on this family, allow insertion at the actual spine vertex s:1 of its next indexed center with any positive quota and that center's actual terminal names, preserve all earlier actual incidences, and return a state with the same insertion guarantee. The state need not certify every old center simultaneously. This obligation is proposed only.
