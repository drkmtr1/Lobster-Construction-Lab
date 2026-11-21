# B3-UNPADDED-QGE-R-001: three unpadded sections

**Disposition: ACCEPT** on the exact domain below after separate AI mathematical and implementation reviews. The mathematical reviewer independently rederived both supplied components, original-edge partitions, high-side shift, boundary cases and continuation; a separate implementation reviewer inspected the actual code, fixed-port B2 interface, caller-retained target and tests. These reviews are not human peer review or formal verification. The construction is a project corollary of retained R241 and L008 together with the explicitly proved supplier B below; no historical novelty is claimed. The 12-case original-target regression and a separate audit of those same saved certificates are recorded in [the evidence package](../evidence/validation/B3_UNPADDED_QGE_R_001/README.md).

## The exact target and theorem

For integers `q>=r>=1`, `t>=1`, `K>=2` (booleans excluded), take the original profile

```python
[[q], [r], [t]] + [[] for _ in range(K + 1)]
```

There are `K+4` named spine vertices `s:0,...,s:(K+3)`, consecutive spine edges, branch centers `b:i:0` attached to `s:i` for `i=0,1,2`, and respectively `q,r,t` named terminal leaves attached to these centers. Hence the graph has `m=q+r+t+K+6` edges and `m+1` vertices. Its prefix consists of `s:0,...,s:3` and all three complete branches; its only unassigned vertices are `s:4,...,s:(K+3)`, with incident edges exactly the original `K`-edge path from `s:3`. No vertex is identified, inserted, renamed or moved.

Set `a=q+t+3` and `x=q-r`. Assign the prefix directly from the parameters:

```text
s:0=x           s:1=K+a+2       s:2=q+2       s:3=K+a+1
b:0:0=m         b:1:0=q+1       b:2:0=K+a
l:0:0:j=j       for 0<=j<x
l:0:0:j=j+1     for x<=j<q
l:1:0:j=K+a+3+j for 0<=j<r
l:2:0:j=q+3+j   for 0<=j<t
```

We prove that it leaves precisely `R=[a,a+K-1]`, unused differences `D=[1,K]`, and physical port `s:3=a+K+1`, then the original path can be completed while keeping every prefix label. The formulas use neither a solver nor a supplied full-target labeling.

## Prefix vertex inventory

Because `q>=r>=1`, `0<=x=q-r<=q-1`. The first branch's named leaves use `[0,x-1]` and `[x+1,q]`; together with `s:0=x` they use exactly `[0,q]` once. When `q=r`, `x=0` and the first interval is empty; the second still gives `[1,q]`. Adding `b:1:0=q+1`, `s:2=q+2`, and the third-branch leaves `[q+3,q+t+2]` yields exactly the disjoint low block `[0,a-1]`.

The high prefix block consists, in order, of `b:2:0=K+a`, `s:3=K+a+1`, `s:1=K+a+2`, the second-branch leaves `[K+a+3,K+a+r+2]`, and `b:0:0=m=K+a+r+3`. It is exactly `[K+a,m]`. The two blocks are disjoint, inside `[0,m]`, and cover every original prefix vertex once, including the named leaf ordering. Their gap is exactly the `K` unused labels `[a,a+K-1]`. The blocks have `a` and `r+4` entries, for `q+r+t+7=m-K+1` distinct prefix vertices.

## Original-edge difference inventory

Every prefix edge crosses from the low block to the high block; absolute differences therefore equal high minus low. The complete list of actual prefix edges is:

| Original edge or edge group | Differences |
|---|---|
| `b:2:0--l:2:0:j`, `0<=j<t` | `[K+1,K+t]`, in reverse leaf order |
| `s:2--b:2:0` | `K+t+1` |
| `s:2--s:3` | `K+t+2` |
| `s:1--s:2` | `K+t+3` |
| `s:1--b:1:0` | `K+t+4` |
| `b:1:0--l:1:0:j`, `0<=j<r` | `[K+t+5,K+t+r+4]` |
| `s:0--s:1` | `K+t+r+5` |
| `b:0:0` to `s:0` and its `q` leaves | `[K+t+r+6,m]` |

For the last row, the `q+1` neighbors have exactly the labels `[0,q]`; subtracting them from `m` gives `[m-q,m]=[K+t+r+6,m]` with no repetition. The rows are disjoint and consecutive, cover exactly `[K+1,m]`, and account for all `m-K` actual prefix edges. Thus the unused differences are exactly `[1,K]`, and the crossing port is the actual `s:3=K+a+1`. In the minimum case `q=r=t=1,K=2`, `a=5,m=11`: prefix labels are `[0,4]` and `[7,11]`, prefix differences are `[3,11]`, and the actual port is `8`.

## Derivation using the original `s:1--s:2` edge

Cut the actual edge `s:1--s:2`. The left component B contains `s:0,s:1`, both first branch centers and their named leaves. Define `n_B=q+r+4`, `p_B=q+2`, and

```text
s:0=x                   b:1:0=q+1         s:1=q+2       b:0:0=q+r+3
l:0:0:j=j               for 0<=j<x
l:0:0:j=j+1             for x<=j<q
l:1:0:j=q+3+j           for 0<=j<r
```

This is an independently proved supplier, not a quotation of an upstream sublemma. Its low labels `[0,q+1]` are `s:0`, first leaves, and `b:1:0`; its high labels `[q+2,q+r+3]` are `s:1`, the second leaves, and `b:0:0`. The differences of the actual edges `s:1--b:1:0`, `b:1:0--l:1:0:j`, and `s:0--s:1` are respectively `1`, `[2,r+1]`, and `r+2`. The `q+1` edges from `b:0:0=q+r+3` to the vertices labeled `[0,q]` use exactly `[r+3,q+r+3]`. These are consecutive and exhaust `1..n_B-1`. Every edge crosses the low/high cut. The actual ports are `L_B=s:0=x`, `U_B=s:1=p_B`, so `x_B=x`, `y_B=0`. The actual witness `s:0--s:1` has all component vertices within distance at most two: first-branch leaves lie via `b:0:0`, second-branch leaves via `b:1:0`.

The right component A contains `s:2,s:3,b:2:0` and the third leaves. Retained [L008](../references/upstream/bounded/research__LEMMAS.md.archive.md), with branch size `t` and zero padding, gives `s:2=0`, `b:2:0=t+1`, `l:2:0:j=j+1`, `s:3=t+2`. It has `n_A=t+3`, low labels `[0,t]`, high labels `[t+1,t+2]`, `p_A=t+1`, and differences `1..t+2`. Its actual ports are `L_A=s:2=0` and `U_A=s:3=p_A+1`; their offsets are `x_A=0`, `y_A=1`. The original edge `s:2--s:3` witnesses the component, since its other vertices are at distance at most two from that path.

Apply the retained [R241 binary composition](../references/upstream/mdl/N241_relational_ports.md), whose mathematical return is [source lines 4364–4405](https://github.com/drkmtr1/Math-Discovery-Lab/blob/858a8c1fcfda87ba40bb1adee498a6131504a803/research/candidates/volume-010.md#L4364-L4405), with A as the right component and B as the left. Its condition `x_A=y_B=0` holds. The added edge `L_A--U_B` is exactly the cut original edge `s:2--s:1`; it creates no connector vertex or identification. R241 maps all A labels by `+p_B=q+2`, leaves B low labels fixed, and maps B high labels by `+n_A=t+3`. The component differences become `1..t+2` and `t+4..q+r+t+6`, while the restored edge has difference `n_A=t+3`. They therefore partition `1..q+r+t+6`. Its returned physical ports are `L_B=s:0` and `U_A=s:3`, with combined low size `p_A+p_B=a` and `s:3=a+1`. The concatenated witnessing path is the original `s:0--s:1--s:2--s:3`.

The retained R241 statement's original unreviewed header is superseded within its exact scope by the [separate review](https://github.com/drkmtr1/Math-Discovery-Lab/blob/858a8c1fcfda87ba40bb1adee498a6131504a803/research/candidates/volume-010.md#L4447-L4479) and [director disposition](https://github.com/drkmtr1/Math-Discovery-Lab/blob/858a8c1fcfda87ba40bb1adee498a6131504a803/research/candidates/volume-010.md#L4488-L4505), at MDL commit `858a8c1fcfda87ba40bb1adee498a6131504a803`, source blob `faca17cfa4c484127413762adc0c36b771a18f71`. The L008 archive corresponds to the [pinned Bounded Search source](https://github.com/drkmtr1/MDL_Bounded_Search/blob/e48b94eec4091b4fe189e325cab2eda464409943/research/LEMMAS.md#L21), commit `e48b94eec4091b4fe189e325cab2eda464409943`, source blob `f942e3b8b7628353ef7cf9d8cf53759c2eed0478`; the pinned upstream blob and retained L008 text were compared read-only for this task. These source dispositions and this project review are separate from formal or human verification.

Finally add `K` to every high-class label of this combined alpha seed, leaving all low labels unchanged. The high block moves from `[a,m-K]` to `[K+a,m]`; every original prefix edge crosses classes, so each difference increases by exactly `K`, from `[1,m-K]` to `[K+1,m]`. Direct substitution gives exactly the displayed named prefix, including its physical port and `b:0:0=m`. The corresponding gap is the claimed label inventory.

## Completion at the actual `s:3` port

The accepted normalized construction from [B2_NONADJACENT_CONSUMER.md](B2_NONADJACENT_CONSUMER.md) depends mathematically on the stated resources and actual path incidence, rather than on a particular spelling of its physical port. Its bases are

```text
C_2=(3,1,0), C_3=(4,1,0,2), C_4=(5,1,2,0,3).
```

For `K>=5`, if `C_(K-3)=(K-2,x_1,...,x_(K-3))`, use

```text
C_K=(K+1,1,K-1,0,K-2-x_1,...,K-2-x_(K-3)).
```

Inductively the shorter suffix contains exactly `[0,K-4]`; the reflected tail contains `[2,K-2]`, disjoint from new `1,K-1,0`, so the suffix of `C_K` is exactly `[0,K-1]`. The first three new edge differences are `K,K-2,K-1`; reflecting the entire shorter sequence maps its initial `K-2` to the new `0`, so the connecting edge and following reflected edges reproduce all shorter differences `[1,K-3]`. The three base cases directly have suffix labels `[0,K-1]` and differences `[1,K]`. Every recurrence step decreases K by three to one of the bases; the finite computation terminates.

Translate by `a`. The first value is `a+K+1`, exactly the already assigned original `s:3`; for `1<=i<=K` assign `s:(3+i)=a+c_i`. The actual original suffix edges use each of `1..K` once, its new labels use exactly `[a,a+K-1]`, and every prefix label remains fixed. The complete original graph therefore has all vertex labels `0..m` and edge differences `1..m` once each. The existing public B2 helper remains fixed to physical `s:2`; applying its underlying sequence to `s:3` does not rename that helper's contract or alter `interval_boundary`.

At K=1 the proposed resource contract itself would leave label `a` at distance 2 from the required port `a+2`, whereas the sole unused difference is 1. Thus this particular continuation does not cover K=1; other labelings and boundaries are not excluded. Values `q<r` are outside this formula, not proved nongraceful. Nonzero padding, extra branches, a fourth branched section, arbitrary repetition and universal lobster coverage remain separate obligations. Finite validation corroborates the symbolic proof rather than replacing it.
