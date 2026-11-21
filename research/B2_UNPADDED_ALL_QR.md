# B2-UNPADDED-ALL-QR-001: two-section unpadded supplier

**Disposition:** ACCEPT as an explicit independently supplied prefix and original-path construction on the exact domain below, after separate mathematical and implementation review. This is expanded project parameter coverage, not a claim of historical novelty, human peer review, formal verification, or universal lobster gracefulness. Starting checkpoint: `a7d3c9162d00ff6a487da9ad592be2337f42114f`.

## Exact theorem and target

Let `q,r,K` be integers with `q>=1`, `r>=1`, `K>=2`; booleans are not structural integers. Set `z0=z1=0` and use the original named profile

```text
[[q],[r]] + [[] for _ in range(K+1)]
```

with `m=q+r+K+4` edges and spine `s:0,...,s:(K+2)`. The prefix is the actual set of vertices excluding exactly `s:3,...,s:(K+2)`. There is one positive branch at each of `s:0` and `s:1`; their named leaves and attachment points are unchanged. Define

```text
s:0 = K+r+4           s:1 = 1             s:2 = K+r+3
b:0:0 = 0             l:0:0:j = K+r+5+j   (0 <= j < q)
b:1:0 = K+r+2         l:1:0:j = 2+j       (0 <= j < r)
```

This explicitly supplies the prefix from parameters, with no successful full-target solution, seed search or allocator as an input. The value `s:1=1` is a formula choice, not a purported restriction on other labelings.

## Labels and original-edge differences

The labels `b:0:0`, `s:1`, and the named `r` leaves at `b:1:0` are exactly `[0,r+1]`. The labels `b:1:0`, `s:2`, `s:0`, and the named `q` leaves at `b:0:0` are exactly `[K+r+2,m]`, since the last leaf is `K+r+q+4=m`. Both blocks are internally injective and disjoint. Thus all prefix values lie in `0..m`, and the unused vertex-label set is exactly

```text
R = [r+2,K+r+1],     |R| = K.
```

The differences on the **actual original prefix edges** partition the high difference interval as follows:

| Original edge family | Differences |
|---|---|
| `b:1:0--l:1:0:j`, `0<=j<r` | `[K+1,K+r]` in reverse leaf order |
| `s:1--b:1:0` | `K+r+1` |
| `s:1--s:2` | `K+r+2` |
| `s:0--s:1` | `K+r+3` |
| `s:0--b:0:0` | `K+r+4` |
| `b:0:0--l:0:0:j`, `0<=j<q` | `[K+r+5,m]` |

The intervals are disjoint and cover exactly `[K+1,m]`, including when `q=1` or `r=1`. Consequently the unused differences are exactly `[1,K]`. No isomorphism, symmetry quotient, omitted edge, reordered physical branch, or enlarged target is involved.

## Physical boundary and completion

Set `ell=r+2`. Then `R=[ell,ell+K-1]` and the actual assigned port is

```text
f(s:2) = K+r+3 = ell+K+1.
```

The only prefix-to-unassigned edge is the actual `s:2--s:3`; the unassigned topology is the original K-edge path `s:2--s:3--...--s:(K+2)`. The independently accepted nonadjacent consumer in [B2_NONADJACENT_CONSUMER.md](B2_NONADJACENT_CONSUMER.md) applies for each integer K>=2. It labels exactly that path, uses every label in R and every difference `1..K`, and leaves the prefix unchanged. Hence the completed original target is graceful on the stated infinite domain.

This proves the revised **nonadjacent** analogue of the resource/physical obligations P01–P04 and P06–P09, with its own replacement for P05. It does not alter literal P05 or `interval_boundary`, both of which require an adjacent port. The prefix's low/high partition is an alpha separation of its assigned edges; no alpha condition is asserted for the completed full graph.

For K=1, this very interface leaves one label `ell` and places the port at `ell+2`, so its remaining edge would have difference 2 rather than the unused difference 1. The proposed theorem therefore does not cover K=1. This is not a nongracefulness assertion; other constructions and previously retained witnesses may apply.

## Comparison and source limits

- For `(q,r)=(1,2)`, the formula is exactly the vertex-by-vertex port-5 construction in [B2_NONADJACENT_SEED_P5.md](B2_NONADJACENT_SEED_P5.md), not just an isomorphic graph.
- For `q=r=t`, the same zero-padding family and label interval occur in [B2_BALANCED_SUPPLIER.md](B2_BALANCED_SUPPLIER.md), but that supplier uses a different prefix labeling and adjacent port `K+t+2`, and also works at K=1. This construction uses nonadjacent port `K+t+3` and requires K>=2.
- The retained L010 composition in [PROOF_OBLIGATIONS.md](PROOF_OBLIGATIONS.md) §4 requires `z1>=K+1` and `z0>=r+z1+K+3`; it does not apply at zero padding. Its source is the pinned [Bounded Search L010 record](../references/upstream/bounded/research__LEMMAS.md.archive.md) at commit `e48b94eec4091b4fe189e325cab2eda464409943`, not an additional upstream lemma.
- The retained R241/R246 port and reconstruction methods require their own supplied modules and physical compatibility; see [FINDINGS.md](FINDINGS.md) §1 and the pinned [R241](../references/upstream/mdl/N241_relational_ports.md) and [R246](../references/upstream/mdl/N246_reconstruction_and_count_correction.md) records at MDL commit `858a8c1fcfda87ba40bb1adee498a6131504a803`. Their existence does not by itself prove this exact supplied interface, and this comparison is not an exhaustive reachability or novelty audit.
- The [E10 source record](../docs/SOURCES.md) claims ordinary gracefulness for subcubic lobsters, overlapping these profiles when `q,r<=2`; it does not prescribe this port. Its Lean archive was inspected but not rebuilt or fully audited. Leaving that degree bound does not establish historical novelty.

Separate fresh reviewer sessions challenged the symbolic proof and, after implementation, the actual code and original-target checks. They are AI reviews, not human peer review or formal proof-assistant verification. Targeted finite evidence is recorded separately; it corroborates but does not replace the quantified partition above.
