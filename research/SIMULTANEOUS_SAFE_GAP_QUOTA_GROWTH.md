# D212 simultaneous matched safe-gap growth

The proposed conditions are necessary and sufficient for the declared matched-gap placement to work for every vector of independent nonnegative widths. The positive path supplies two independently expandable actual centers. The adverse path shows that individually feasible gaps may fail jointly. The B2, B3 and B4 supplier questions are left undecided by the symbolic results and are specified for one bounded dormant diagnostic. No numerical discovery ran.

## 1. Conventions and exact unused inventories

Let a named tree have n edges and a graceful labeling f onto the integer interval [0,n]. Cut c means the partition into labels below c and labels at least c, with 1≤c≤n. It is safe if the differences of its actual crossing edges are [D,n]. Each difference denotes a unique edge. The weight-n edge crosses every proper cut. Distinct safe cuts have distinct thresholds: for c<c' with equal threshold, the two sets of crossing edges would coincide. An edge with exactly one endpoint in the nonempty middle label band [c,c'−1] crosses exactly one of these cuts. Such an edge exists by connectedness, since the middle band is a proper nonempty vertex set. This recovers the uniqueness used in the [D199 proof](ORDINARY_SPINE_PARTIAL_SAFE_CUT_THREE_GAP_CHAIN.md#1-partial-safe-cut-ranks-and-maximal-robust-support).

Select distinct actual hosts vᵢ and distinct proper safe cuts cᵢ with respective thresholds Dᵢ. Write aᵢ=f(vᵢ) and take independent nonnegative integer widths gᵢ. The prescribed actual extension adds just gᵢ pendant vertices at vᵢ, retaining every old vertex, edge and terminal name. With M=n+Σᵢgᵢ define

```text
E(x) = x + Σ_{j: cⱼ≤x} gⱼ,
Lᵢ = cᵢ + Σ_{j: cⱼ<cᵢ} gⱼ,
Bᵢ = Dᵢ + Σ_{j: Dⱼ<Dᵢ} gⱼ.
```

The strictly increasing map E installs every old label exactly once in [0,M], with endpoints 0 and M. Adjacent labels at cᵢ−1,cᵢ have images Lᵢ−1,Lᵢ+gᵢ, so the disjoint label gaps [Lᵢ,Lᵢ+gᵢ−1] are the exact complement of the old labels. For an original edge of difference d and old endpoint labels x<y, endpoint subtraction gives

```text
E(y)−E(x) = d+Σ_{j: x<cⱼ≤y}gⱼ = d+Σ_{j: Dⱼ≤d}gⱼ = W_d.
```

Set W₀=0. The successive jumps in this strictly increasing sequence have size one plus the width at the represented rank and size one elsewhere. Thus [Bᵢ,Bᵢ+gᵢ−1] is the exact gap at threshold Dᵢ, since W_{Dᵢ−1}=Bᵢ−1 and W_{Dᵢ}=Bᵢ+gᵢ. The intervals are disjoint and exhaust the unused differences in [1,M], since W_n=M. This covers Dᵢ=1 and empty widths.

## 2. Exact local starts and independent width coefficients

By **matched-gap placement** we mean that the gᵢ new named leaves at vᵢ use exactly their label gap and must realize exactly the difference gap associated with Dᵢ. There is no reuse of a gap at a different host or exchange of differences between gap indices in this requirement. For each active index (gᵢ>0) the actual differences at its host form an interval of size gᵢ, in either order:

| Host position in old labels | Minimum actual difference after embedding |
|---|---|
| Lower aᵢ<cᵢ | Lᵢ−E(aᵢ)=cᵢ−aᵢ+Σ_{j: aᵢ<cⱼ<cᵢ}gⱼ |
| Upper aᵢ≥cᵢ | E(aᵢ)−(Lᵢ+gᵢ−1)=aᵢ−cᵢ+1+Σ_{j: cᵢ<cⱼ≤aᵢ}gⱼ |

Every label in the gap is strictly above the lower host or strictly below the upper host by monotonicity. Matching is equivalent to equality between the first actual difference and Bᵢ. For a **fixed** width vector this gives exactly one start equality at each active index and none at inactive indices. Coefficient equality is only forced by requiring all independent width vectors.

Indeed set gᵢ=1 and all other widths zero to force the constant. Keep gᵢ=1 and vary each other gⱼ separately from zero to one to force its coefficient. This yields exactly

```text
lower: aᵢ=cᵢ−Dᵢ,      {j : Dⱼ<Dᵢ} = {j : aᵢ<cⱼ<cᵢ};
upper: aᵢ=cᵢ+Dᵢ−1,   {j : Dⱼ<Dᵢ} = {j : cᵢ<cⱼ≤aᵢ}.
```

Conversely the constants and coefficients imply equality for every width vector. Assign gap labels in increasing order to the new leaves in their actual index order, preserving all original names. Each new edge has the actual difference just calculated, so its batch fills its entire difference gap with multiplicity one. Together with the old edges, the vertex and difference inventories exhaust [0,M] and [1,M]. Adding only pendant vertices preserves the tree. If the old tree is a lobster with a supplied witnessing spine and each expanding host is distance at most one from it, the same spine witnesses the new lobster. Finite emission consists of the old labels and one pass over the finite original-indexed new intervals. An empty selection or all-zero widths gives the original, including the possibility n=0 when no proper cut is available. This is an exact theorem for the declared matched placement and safe support. Its converse makes no claim about differently paired gaps, coordinated widths, nonmonotone embeddings, or ordinary gracefulness.

If hosts are still assigned their designated label gaps but the difference-gap pairing is left implicit, any successful vector pairs each active host batch with an entire difference gap of the same width. Each batch realizes one consecutive interval. It cannot straddle an old difference, so must be contained in one gap. Every active difference gap needs a batch, and the number of batches equals the number of active gaps. Thus the pairing is bijective and each gap is filled by its single batch. For one fixed vector, an equal-width permutation may therefore be relevant. For robustness over all independent vectors the same coefficient conditions remain necessary, even with implicit pairing. Activate i alone at width one for the constant, then activate i at one and j at two for a single coefficient. The distinct widths force the intended pairing in each test. This corollary still requires the prescribed host-to-label-gap placement.

## 3. Threshold order and compatibility

For a proposed host-cut-threshold triple (a,c,D) define its span among other cuts as a<c'<c in lower orientation and c<c'≤a in upper orientation. The exact joint condition says that the cuts inside this span are precisely the selected cuts with smaller threshold. In increasing threshold order, each cut after the first lies strictly outside the interval spanned by all earlier cuts. If the new cut is to their right, its host is below their minimum cut. If the new cut is to their left, its host is at least their maximum cut. This follows because the span lies entirely on one side of the new cut and must contain every earlier cut. In particular the last threshold cannot belong to an interior cut of a selected list of size at least three. Exterior insertion alone leaves both the host bounds and the exclusion of later cuts from earlier spans to check.

Exterior insertion already follows from safety alone. For any new threshold, the unique edge of the largest earlier threshold crosses every earlier cut. Its interval contains their entire hull. The new cut cannot cross that edge, whose weight is less than the new threshold. The host bounds and the required exclusion of later cuts from earlier host spans are the additional matched-growth constraints.

With distinct cut and threshold values, a pair of triples is compatible exactly when the smaller-threshold cut lies in the larger-threshold span and the larger-threshold cut lies outside the smaller-threshold span. This is an equivalent pairwise test of the set equalities and not just the exterior-order necessary condition. It also explains why the fresh edges of a gap cross the boundaries of precisely the other selected gaps with smaller threshold: the host and the new leaf are on opposite sides of such a boundary exactly under the span condition.

## 4. Prescribed path controls

Use the named consecutive path P0–P1–P2–P3–P4 with labels (0,4,1,3,2). Consecutive actual differences are (4,3,2,1), with cut intervals [1,4], [2,4], [2,3], [3,3] respectively. Thus the cuts 1,2,3,4 have spectra [4,4], [2,4], [1,4], [3,4], as prescribed.

**Positive.** Use P1 of label 4 at cut 1 and threshold 4, and P3 of label 3 at cut 2 and threshold 2. Both are upper hosts. For the former 1+4−1=4 and the span contains exactly the earlier cut 2. For the latter 2+2−1=3 and its span contains none of the other selected cuts. With widths u at cut 1 and v at cut 2, the old path is labeled

```text
(0, 4+u+v, 1+u, 3+u+v, 2+u+v).
```

The new labels at P1 are [1,u], realizing [4+v,3+v+u]. The new labels at P3 are [2+u,1+u+v], realizing [2,1+v]. The old spectrum is {1,2+v,3+v,4+v+u}. These bands are the exact complementary inventories for all u,v≥0, including zeros. The singleton witnessing spine P2 has two actual centers P1 and P3, with P0 and P4 their respective original terminals. The enlarged actual quotas are 1+u and 1+v, with their original parents unchanged.

**Adverse.** Use P0 of label 0 at cut 2 (threshold 2) and P4 of label 2 at cut 3 (threshold 1). Each lower host satisfies the constant and can be grown alone. For cut 2 the earlier-threshold cut 3 does not lie in its span. For cut 3 the selected cut 2 is at its host label, so it is not inside its span, as required. When both widths are one, the old path is (0,6,1,5,3), with actual old differences (6,5,4,2). The fresh labels 2 at P0 and 4 at P4 give weights 2 and 1. Weight 2 repeats and 3 is absent. This refutes independent joint use of these two specified ports and gaps; it does not imply nongracefulness.

## 5. Retained mechanisms and decision on the three bases

[D199](ORDINARY_SPINE_PARTIAL_SAFE_CUT_THREE_GAP_CHAIN.md) proves robust old-weight rank transport and numerical gap complements on safe support. D212 adds the matched fresh-incidence coefficient criterion. [D196](ORDINARY_SPINE_GENERALIZED_ONE_SECTION_CUT_SPECTRUM.md#1-the-generalized-state-and-one-section-outer-placement) also extracts unused bands at a supplied cut, then assigns several actual terminal quotas through a permutation in a single gap of an outer placement. D212 fixes separate gaps at existing hosts, forces each image to its own band, and uses no extreme frontier or returned one-section state. [D210](ORDINARY_SPINE_SIMULTANEOUS_ORDINARY_SUPPLIER.md) supplies an entire partial original and reflected transfers within its base allocation. [D211](ORDINARY_SPINE_COORDINATED_FOUR_HOST_SUPPLIER.md) coordinates a split reflected pair across four hosts on a supplied partial original. D212 instead transports a fully labeled smaller original and separates arbitrary independent growth from supply of that base. Its strict matched-gap constraints give a cheaper growth operation when fulfilled. The whole-original methods can potentially work when that interface fails. No historical novelty is asserted.

[R226](../references/upstream/mdl/N226_R226_two_host_completion.md#n226-closeout) classifies a supplied two-host completion with named eligible difference choices and optional reflection pairs and midpoint. [R232](../references/upstream/mdl/N232_R232_joint_allocation.md#n232-closeout) joins supplied locally balanced two-host palettes via singleton-forest and pair-capacity conditions. In this theorem the same-host absolute difference map is monotone on its consecutive gap. There is no two-host choice after the gap pairing is fixed. The multi-host compatibility is in the coefficients of the gap transport itself. It cannot be inferred from separate feasibility at each host, as the adverse path shows.

The three B bases have k required hosts and n=2k+3. The numerical constraints alone allow k formal triples with cᵢ=k+2−i, Dᵢ=2i−1 and aᵢ=k+i, for i=1,…,k. These values are in range, and for each upper host its span contains exactly the earlier cuts. This is a relaxation with no base vertex labels or crossing spectra assigned. It isolates the missing proof duty of realizing safe spectra simultaneously on actual edges.

This investigation provides no symbolic witness or exclusion for B2, B3 or B4. The held diagnostic addresses only those three fixed bases. A positive would supply all independent quotas at the fixed host count by this theorem. Three positives would still leave a parameterized base supplier for arbitrary multiplicity, or a different coverage theorem, open. An exhaustive negative would exclude the simultaneous matched-gap architecture for that named base only. [Frozen originals](../evidence/validation/D212_MULTI_CENTER_QUOTA_GROWTH/ORIGINALS.md) · [Dormant diagnostic and proposed limits](../evidence/validation/D212_MULTI_CENTER_QUOTA_GROWTH/PREPARATION.md)

## 6. Separate mathematical review

An independent reviewer inspected the written proof, frozen originals, discovery encoding and separate growth audit. The review reproduced both prescribed path controls by hand and passed the endpoint constants, independent coefficients, exact scope at fixed widths, implicit pairing corollary, complement and whole-arm symmetries, and completeness of the paired spans. The reviewer identified the stronger exterior-order deduction from safety alone and checked the formal coordinate relaxation. No obstruction or witness for an actual B base was established. No numerical or executable verification ran.
