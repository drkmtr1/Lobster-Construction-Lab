# Seed-independent two-section reduction and fixed direct-leaf block

Task LCL-HYBRID-JOINT-TWO-SECTION-PILOT-001. One symbolic challenge against the frozen hypothesis SHA-256 `0ff4085340417401a794d3fb8705de90ad284eb20329ece05ed8da011af36976`. All statements refer to the actual named graph, its supplied witnessing spine and the declared embedding. Intervals are inclusive integer intervals. Exact integers exclude booleans.

## 1. Candidate A holds in the declared affine placement

Let P be the supplied graceful prefix with n edges, labels g onto [0,n] and actual last spine vertex v with g(v)=n. The names of all old vertices and edges are fixed. Let the two declared fresh sections add A and B vertices, respectively, including their spine vertices u and w in that order. Write H=A+B and m=n+H. The fresh edges are the two connectors vu and uw and the actual center, direct-leaf and terminal incidences declared within the two sections. Each fresh vertex is added by a single actual parent edge, so there are H fresh edges. The old tree remains induced. The spine extended by u,w witnesses the lobster condition because all new off-spine vertices have distance one or two from it.

Let W be the tree consisting of v and every fresh vertex, with the H fresh edges. Its first-section tree W1 is the induced named tree on v and all A first-section vertices. The prefix-plus-first-section tree I1 is induced in the original full graph. P and W intersect only in v and share no edges. I1 contains precisely P and W1 with intersection v. These are descriptions of the named originals, not new builder records.

### Full labeling and both directions

Translate every old label by A. Its vertex labels occupy [A,n+A] exactly, and its actual absolute differences are [1,n]. Independently of any completion, the required fresh labels are [0,A−1] and [n+A+1,m], and the required fresh differences are [n+1,m]. Including v, the two allowed endpoint bands of W are

    L = [0,A−1]
    U = [n+A,m]

A same-band difference is at most A−1 or B. Both bounds are less than n+1 under n≥H+1. Thus every fresh edge crosses L to U in any full graceful completion. The lower label never exceeds the upper label.

On W retain low labels and subtract n from every upper label. The result is a bijection onto [0,H], has v=A, and puts U onto [A,H]. Each actual edge difference decreases by n, so W has exactly [1,H]. The actual final physical frontier is w. Its allowed full labels m,m−1,m−2 are all above n+A since B≥3. Its allowed reduced labels are exactly H,H−1,H−2. Equivalently the final deficit in {0,1,2} is unchanged. The labels in that menu lie above A, so v's label is never a competing slot.

Conversely, start from a graceful labeling of this same named W with v=A, crossing at cut A and the reduced final frontier domain. Add n to each reduced high label and leave each low label unchanged. At v this agrees with g(v)+A. Combine it with g+A on P; no other names are identified. The expanded fresh labels are exactly the two fresh intervals and the expanded actual W differences are [n+1,m]. Together with the old inventories these give bijections onto [0,m] and [1,m]. The actual connectors and terminal hosts stay fixed. These reductions are mutual inverses on the label assignments. In particular the joint feasible set is determined by the two ordered suffix sections and the reduced menu, independent of all other old labels and incidences given the hypotheses.

### Normalized arm and ranks

Let r be the zero-based ranks induced within W1 by its reduced labels. Removing the second section changes neither the order of remaining low labels nor their order relative to the upper labels. Let L1 be the number of first-section fresh vertices in the lower band. In the small tree W1 the old frontier is the least upper label, so r(v)=L1. In the full I1 the old translated labels occupy a single contiguous block between all low fresh labels and all other upper labels. In I1 the ranks are therefore

    first-section lower vertex x: r(x)
    old vertex x:                  L1+g(x)
    first-section upper x≠v:       n+r(x)

At v the old-vertex formula gives n+L1=n+r(v), so it also agrees with the upper rule. The old edge differences in the rank labeling are exactly [1,n]. Every edge in W1 crosses the bands and its I1 rank difference is n plus its W1 rank difference. Both rank label inventories are bijections by construction. The remaining A rank differences in I1 must be [n+1,n+A], which is equivalent to W1 rank differences [1,A]. This proves both normalized directions, including the actual physical first connector. No intermediate rank choice has been substituted for the rank map of a full witness.

## 2. Candidate B holds in the declared maximum-cut-gap placement

Assume additionally that the actual edges crossing the input cut at n have weights n−1 and n. Only v carries n, so these are precisely the old incidences at v. Noncrossing old incidences have differences [1,n−2]. With s=B−2≥1 the embedding translates the other old labels by A and translates v by A+s. The old labels are [A,n+A−1] and {m−2}. The corresponding actual old differences are the disjoint union

    [1,n−2] and {n−1+s,n+s}.

The required difference n−1 is absent. The fresh label reserve is [0,A−1] together with [n+A,m] minus {m−2}. The difference reserve is the exact complement of the displayed old spectrum in [1,m]. Including v=m−2, every endpoint of each fresh edge is in [0,A−1] or [n+A,m]. A same-band edge has difference at most max(A−1,B), strictly less than n−1 by the declared bound. A cross-band edge has difference at least (n+A)−(A−1)=n+1. Thus no fresh edge can supply n−1. Joint feasibility and hence normalized feasibility both fail for this fixed placement. The larger premise n≥A+B+1 implies the stated strict width bound, since A≥1. This argument covers B=3, including s=1 where n may itself be restored but n−1 cannot be.

For any successful embedding outside these premises the omitted weight need not have these endpoint constraints. The result concerns the frozen max-cut-gap architecture only.

## 3. Symbolic classification of the eight declared suffixes

The exact D105 source has n=13 and actual maximum cut weights 12,13. The already authorized retained input for the other seed has n=20 and maximum cut weights 19,20. These are input facts. For both seeds the listed suffixes have max H=12, so n≥H+1 holds and §2 excludes all eight max-cut-gap pairs. The affine equivalences in §1 then transfer the exact mathematical feasibility of both arms on each corresponding ordered suffix. This proves the predeclared seed-independence prediction about feasible sets. No holdout output was opened or inferred from observed search status. Timing, sample counts and termination behavior are outside this prediction.

For an ordered section let b_i be its number of branch entries, including quota-zero entries that are named direct leaves. Let q_i be its sum of terminal quotas. Then A=1+b_1+q_1 and B=1+b_2+q_2. In the reduced W the high vertex v forces u low and w high. Every first-section branch entry is high and every one of its terminals is low. Every second-section branch entry is low and every one of its terminals is high. The forced counts from these actual edges are

    low = 1+q_1+b_2
    high including v = 2+b_1+q_2.

The available low and high counts are A and B+1. Both are met exactly when b_1=b_2. An empty section still contributes its spine vertex. A quota-zero entry contributes one branch incidence and no terminal incidences.

| Ordered suffix | A | B | Forced low | Affine disposition |
|---|---:|---:|---:|---|
| [1], [1] | 3 | 3 | 3 | Both arms supplied by the D131 control |
| [2], [1] | 4 | 3 | 4 | Both excluded by the actual difference argument below |
| [1], [2,1] | 3 | 6 | 4 | Both excluded by the low count |
| [1,1], [1] | 5 | 3 | 4 | Both excluded by the low count |
| [1,1,1,1], [1] | 9 | 3 | 6 | Both excluded by the low count |
| [1], [1,1,1,1] | 3 | 9 | 6 | Both excluded by the low count |
| [0,1], [1,0] | 4 | 4 | 4 | Both supplied by §4 |
| [], [2,1] | 1 | 6 | 3 | Both excluded by the low count |

For [2],[1] the lower band is [0,3], the upper band [4,7] and v=4. Difference 1 across this cut can only occur on 3–4. Since vu is the only edge of W at v, u=3. Let y be the first center, a and b its terminal labels, z the second spine, r the second center and q its terminal. Then {y,z,q}={5,6,7} and {a,b,r}={0,1,2}. The sum of the seven actual reduced differences is

    1+(y−3)+(y−a)+(y−b)+(z−3)+(z−r)+(q−r)
    =3y+2z+q−8−r
    =2y+z−r+10.

Here a+b=3−r and y+z+q=18. Gracefulness requires the sum 28, hence 2y+z−r=18. For y=5 this requires z−r=8, above the upper bound 7. For y=6 it requires z−r=6, forcing z=7 and r=1. The first terminal carrying 2 then has difference 4, as does uw. For y=7 it requires z−r=4. Both possible values z=5,6 force r=z−4. The attachment at w to its own center then has difference 4, which repeats the actual u-to-first-center attachment y−3=4 in both subcases. The two terminal names remain distinct and the argument is independent of which carries a or b. This exhausts the forced role cases without trying label permutations or changing the frontier menu.

For the [1],[1] positive control, D131 on a maximum-frontier seed admits the two quota-one steps with deficits 0,1,0. Their two reflections compose to g+3 on the old prefix. In section order the fresh labels (spine, center, terminal) are (2,n+4,1) and (n+6,0,n+5). The six actual fresh weights in the same connector/attachment/terminal order are n+1,n+2,n+3 and n+4,n+6,n+5. The intermediate labels occupy [1,n+4], so rank compression is a translation and keeps the intermediate graceful. This gives both arms symbolically within the named original.

## 4. Exact direct-leaf witnesses and repeatability

Let the first new section have [0,1], the second [1,0]. Use u,D1,C1,L1,w,C2,L2,D2 in the Owner's table order, with D_i direct leaves, C_i centers, and L_i their sole terminals. If the next section index is k, the names are

    s:k, b:k:0, b:k:1, l:k:1:0,
    s:(k+1), b:(k+1):0, l:(k+1):0:0, b:(k+1):1.

The exact fresh incidences in the difference-table order are

    vu, uD1, uC1, C1L1, uw, wC2, C2L2, wD2.

Translate g by four. Then v=n+4. In each row the eight labels occupy exactly [0,3] and [n+5,n+8], so they complement the unchanged old label block [4,n+4]. The difference table subtracts the actual endpoints and records the offsets from n.

| Witness | Fresh labels in the declared order | Eight actual weights minus n |
|---|---|---|
| Rank-invalid A | 3, n+6, n+5, 1, n+8, 0, n+7, 2 | 1, 3, 2, 4, 5, 8, 7, 6 |
| Rank-invalid B | 3, n+7, n+5, 2, n+8, 0, n+6, 1 | 1, 4, 2, 3, 5, 8, 6, 7 |
| Rank-valid | 3, n+5, n+6, 2, n+8, 1, n+7, 0 | 1, 2, 3, 4, 5, 7, 6, 8 |

Thus all three give the complete new difference band [n+1,n+8] without disturbing [1,n]. The actual last spine vertex w=n+8 is the new maximum, so its returned deficit is exactly zero. These constructions work for every supplied graceful maximum-frontier prefix with exact n≥0, including the one-vertex case with a witnessing spine. This wider elementary formula domain follows directly from the displayed inventories and does not enlarge the domain claimed for the general reduction in §1.

For each first-section boundary the old edges and the first four listed edges occupy [1,n+4]. The unused differences are [n+5,n+8]. The exact full-alphabet intermediate label inventories are

| Witness | Used labels | Unused labels |
|---|---|---|
| Rank-invalid A | {1} union [3,n+6] | {0,2,n+7,n+8} |
| Rank-invalid B | [2,n+5] union {n+7} | {0,1,n+6,n+8} |
| Rank-valid | [2,n+6] | {0,1,n+7,n+8} |

The only unfinished incidence at this boundary is the actual spine connector uw. Each variant has two lower first-section labels in order L1,u. Both rank to 0,1, respectively. The contiguous old block ranks to g+2 and v to n+2. For A and B the first center and direct leaf rank to n+3 and n+4. Hence the rank weights of vu,uD1,uC1,C1L1 are n+1,n+3,n+2,n+3. The old rank spectrum stays [1,n], so n+3 repeats and n+4 is missing. In the rank-valid row the first direct leaf ranks to n+3 and the center to n+4, giving n+1,n+2,n+3,n+4 and the exact graceful intermediate rank spectrum. The two failed rank assignments are full graceful witnesses but give no obstruction to a separate successful normalized witness for the same pair.

The rank-valid prefix-plus-first-section labeling is independently executable as a symbolic supplier for this single first-section type. Translate g by two and give (u,D1,C1,L1) labels (1,n+3,n+4,0) immediately. Its first four actual weights are n+1 through n+4 as above, with labels covering [0,n+4]. This first-section rule does not require the second section. Translating this whole intermediate by two realizes the rank-valid row's immutable intermediate alphabet [2,n+6]; its actual frontier in the normalized intermediate is 1, with deficit n+3. It is a fixed intermediate supplier and a specifically compatible second step, with no arbitrary independently supplied intermediate state or open-ended single-section closure.

For repeated occurrences of this fixed two-section block, start from any such independently supplied prefix and use any declared one of the three rows at each block. Every block increases the size by eight and returns the same ordinary maximum-frontier state. Induction proves closure for every finite repetition, also for zero blocks. If an intermediate rank-graceful witness is needed at each repetition, use the rank-valid row throughout. Each block has a constant number of named fresh vertices and incidences, so the finite emission terminates.

For immutable final labels in k declared blocks, put n_i=n+8i and T_i=4(k−i) for boundary i. In local coordinates every old vertex is translated by four at the next block. Its final image after remaining translations is x↦x+T_i. The equality T_(i−1)=4+T_i proves agreement at every already assigned label. Set seed labels once using T_0 and emit each block once in its local construction translated by T_i. At boundary i the actual used labels are [T_i,T_i+n_i], used differences [1,n_i], and the actual frontier label is T_i+n_i. The remaining inventories in the final alphabet are [0,n_k] minus the used label interval and [n_i+1,n_k]. At block i the new labels are the translate by T_i of [0,3] and [n_(i−1)+5,n_i], the disjoint complement in the new used interval of the old translated interval. The new weights are [n_(i−1)+1,n_i]. Uniform translation preserves each actual connector and old edge difference. Both inventories finish empty, and the supplied prefix and declared blocks require only linear indexed output operations.

## 5. Historical comparison and exact remaining obligations

- D131 supplies one positive-center spine section using an affine reflection and an admitted deficit recurrence. Two D131 quota-one steps give the affine control here. The direct-leaf block has an additional named direct leaf in each section and an ordinary maximum return, with a two-step translation closure proved for that fixed topology. It does not follow from the single-center section formula alone. LCL primary proof `research/ORDINARY_SPINE_DEFICIT_TRANSITION.md`, sections Single transition, Returned state, and Fixed final alphabet.
- D133 uses the same underlying inventory observation that sufficiently large new weights force edges between exterior bands. It treats one section with at least three positive centers and uses the class geometry of that topology to force the extremal-host obstruction. Here W includes two adjacent spine sites and both original connectors; the reduced feasibility test is for a prescribed maximum-frontier affine offset. There is no conflict with D133's stated class. LCL primary proof `research/ORDINARY_SPINE_ARBITRARY_CENTER_AFFINE_OBSTRUCTION.md`, sections Reduction and Exact residual bands.
- D134 changes the old labels and crossing spectrum in its supplied cut state and proves an exact returned cut spectrum, alongside polarity and allocation hypotheses. This task proves neither a D134 input supply nor an exact half-spectrum return. D142's non-leaf family, candidate layouts, old-image tests and necessary role balance retain their scope; its fresh-placement question remains open. The deferred two-section D134 task would require an independent intermediate crossing state and a precise final half-spectrum, neither proved here. LCL primary proofs `research/ORDINARY_SPINE_PIECEWISE_CUT_SPECTRUM_TRANSITION.md` and `research/ORDINARY_SPINE_VARIABLE_EXTERIOR_BRIDGE.md`.
- MDL R227.1 revision 2, part 8, already gives a repeatable two-site consumer on an independently graceful tree at a designated port K+1, with K equal direct-leaf counts at both sites and nonnegative center quotas. At K=1 its physical pattern includes one direct leaf per site, but its prescribed port is 2 and returns 2. The present fixed [0,1],[1,0] pair consumes and returns the actual maximum, uses translation by four and has an exact rank comparison. This is a scoped derivation and does not settle graph-domain inclusion or historical priority. Pinned MDL commit `858a8c1fcfda87ba40bb1adee498a6131504a803`, `research/candidates/volume-010.md` lines 925–1026, revision 2 and separate review, with related retained N246 scope notes.
- MDL N241 uses independently supplied alpha modules and matched actual low/high offsets; its R212-B.1 supplier and the retained LCL D078 paired modules have distinct port, branch and optional empty-tail contracts. The N240 resource algebra retains the complete label/difference state for general named incidences and is an exact reformulation rather than an existence proof. The restricted affine reduction here removes P from the completion test because both of its occupied inventories are known. No historical novelty or noncoverage claim is needed. Pinned MDL commit `858a8c1fcfda87ba40bb1adee498a6131504a803`, retained `references/upstream/mdl/N241_relational_ports.md` source lines 4364–4405 and `references/upstream/mdl/N240_resource_algebra_counting.md`. LCL D078 proof `research/R241_PAIRED_BRANCHED_SPINE.md`, sections Exact claim and Independently supplied modules.

The gain is an exact seed-independent affine reduction and genuine reusable closure for one fixed named direct-leaf block. The rank-valid formula independently supplies the intermediate of that block. General two-section resource supply, arbitrary multiplicities and quotas, general direct-leaf and interior-empty combinations, and the exact external D134 return remain open. For the one screened interior-empty suffix the incompatible cut counts exclude only this affine placement, and the missing-weight lemma excludes its matching maximum-cut-gap placement. No global nongracefulness follows.

The frozen D105 campaign found no joint-only feasibility advantage. The proof now explains why the second retained seed cannot discriminate feasibility at these exact scopes. It adds a usable fixed block without discharging the larger structural obligation. Recommend closing the temporary pilot and returning to primarily symbolic work, subject to Director review and a later separate governance decision. The exact D134 obligation and the 2322 investigation remain separately deferred and unstarted. No detailed holdout outcomes were read or released. No searches, generated originals, solver calls, placement sweeps or successor experiments were performed.
