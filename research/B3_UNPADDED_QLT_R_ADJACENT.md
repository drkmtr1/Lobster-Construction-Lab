# B3-UNPADDED-QLT-R-ADJACENT-001

**Disposition: ACCEPT** on the domain below. A separate AI mathematical reviewer checked the supplied components, the restored original edge and ports, both prefix inventories, and the adjacent continuation. A separate AI implementation reviewer accepted the exact parameter admission, the original-path validation and reuse of the adjacent consumer at `s:3`. The reviewer checked the saved receipts and confirmed that the regression and arithmetic audit cover the same 12 targets. This project corollary uses R241 and a class-reversed alpha labeling on the L008 topology. No historical novelty, human peer review or formal verification is claimed. [Validation record](../evidence/validation/B3_UNPADDED_QLT_R_ADJACENT_001/README.md)

## Original graph and prefix

Take integer parameters `1<=q<r`, `1<=t<=q+1`, `K>=1`, with zero padding. The original profile is `[[q],[r],[t]]+[[]]*(K+1)` in that order. Its `K+4` spine vertices are `s:0,...,s:(K+3)`, joined consecutively. For each `i=0,1,2`, the center `b:i:0` is joined to `s:i` and to its original named leaves `l:i:0:j`, with counts `q,r,t`, respectively. Thus the edge count is `(K+3)+3+q+r+t=m=q+r+t+K+6` and the order is `m+1`. The prefix covers `s:0,...,s:3` and all branches. The remaining vertices are exactly `s:4,...,s:(K+3)`, whose incident edges are the consecutive spine edges from `s:3` onward. Only `s:3--s:4` crosses from assigned to unassigned vertices.

Set `a=q+t+3` and assign the original prefix as follows.

```text
s:0=t          s:1=K+a+t+2     s:2=a-1        s:3=K+a
b:0:0=K+a+2    b:1:0=0         b:2:0=K+a+1
l:0:0:j=j+1                 for 0<=j<t-1
l:0:0:j=j+2                 for t-1<=j<q
l:1:0:j=K+a+3+j             for 0<=j<t-1
l:1:0:j=K+a+4+j             for t-1<=j<r
l:2:0:j=q+2+j               for 0<=j<t
```

The first leaves carry `[1,t-1]` and `[t+1,q+1]` in increasing named order. Inserting `s:0=t` gives exactly `[1,q+1]`. The third leaves occupy `[q+2,q+t+1]`. Adding label `0` at `b:1:0` and `a-1=q+t+2` at `s:2` gives the full low block `[0,a-1]`. At `t=1` both initial leaf subranges with `j<t-1` are empty. At `t=q+1` the first branch's second subrange is empty and its leaves fill `[1,q]`. At `q=1` the only possibilities are `t=1` and `t=2`, so the only first leaf has label `2` or `1`, respectively, while `s:0` has the other label. The inequality `t<=q+1<=r` ensures that the middle block has room for its port label and all `r` leaves throughout these cases.

The vertices `s:3,b:2:0,b:0:0` give `K+a,K+a+1,K+a+2`. The middle leaves occupy `[K+a+3,K+a+t+1]` and `[K+a+t+3,K+a+r+3]`, so inserting `s:1=K+a+t+2` gives `[K+a+3,m]`, since `m=K+a+r+3`. The two prefix blocks `[0,a-1]` and `[K+a,m]` are disjoint and have `a+(r+4)=m-K+1` labels for exactly that many original prefix vertices. All labels are in range and distinct. The gap consists of exactly the `K` unused labels `[a,a+K-1]`.

## Original-edge difference partition

Every assigned edge crosses between the low and high blocks, so high minus low gives its difference. The rows below account for the three prefix spine edges, all three branch attachments, and every terminal edge once.

| Original edge or group | Calculation | Differences |
|---|---|---|
| `s:2--s:3` | `K+a-(a-1)` | `K+1` |
| `s:2--b:2:0` | `K+a+1-(a-1)` | `K+2` |
| `b:2:0--l:2:0:j`, `0<=j<t` | `K+t+2-j` | `[K+3,K+t+2]` |
| `s:1--s:2` | `K+a+t+2-(a-1)` | `K+t+3` |
| `b:0:0` to `s:0` and all first leaves | `K+a+2` minus each value in `[1,q+1]` | `[K+t+4,K+a+1]` |
| `s:0--s:1` | `K+a+t+2-t` | `K+a+2` |
| `b:1:0` to `s:1` and all middle leaves | Subtract `0` from each value in `[K+a+3,m]` | `[K+a+3,m]` |

These consecutive disjoint groups cover `[K+1,m]` once, leaving exactly `[1,K]`. The original physical port `s:3=K+a` is immediately above the unused label interval.

## Composition along `s:1--s:2`

Cut the actual edge `s:1--s:2` of the prefix. The left tree B has `n_B=q+r+4` vertices and low class size `p_B=q+2`. Give it local labels `b:0:0=q+2`, `b:1:0=0`, `s:0=t` and `s:1=q+2+t`. The first leaves carry `[1,q+1]` with `t` omitted, in increasing named order. The middle leaves carry `[q+3,q+r+3]` with `q+2+t` omitted, also in increasing named order. In each list, the skipped value is in range because `1<=t<=q+1<=r`. The actual low vertices carry exactly `[0,q+1]`, and the high vertices exactly `[q+2,q+r+3]`. Every edge crosses the cut. The first star, including the attachment to `s:0`, has differences `[1,q+1]` by subtracting all neighbor labels `[1,q+1]` from `q+2`. The spine edge `s:0--s:1` gives `q+2`. The middle star, including its attachment to `s:1`, gives `[q+3,q+r+3]` directly from its high neighbor labels at center `0`. This proves B is alpha graceful and derives this component supplier directly. Its actual ports are `L_B=s:0`, `U_B=s:1`, with offsets `x_B=y_B=t`. The edge `s:0--s:1` is the witnessing path since each center is at distance one and each leaf at distance two.

The right tree A has `n_A=t+3` vertices and low class size `p_A=t+1`. Give it `s:2=t`, `l:2:0:j=j` for `0<=j<t`, `b:2:0=t+2`, `s:3=t+1`. The low labels are `[0,t]` and the high labels are `[t+1,t+2]`. The center `b:2:0` meets each low label from `0` through `t` and produces differences `[2,t+2]`. The edge `s:2--s:3` gives `1`, proving alpha gracefulness. Its actual ports are `L_A=s:2`, `U_A=s:3`, with offsets `x_A=t`, `y_A=0`. The path `s:2--s:3` witnesses this tree because every other vertex lies within two edges of it.

For the source derivation of A, the zero-padding L008 labeling puts `0` at `s:2`, `t+1` at `b:2:0`, `t+2` at `s:3`, and gives the third leaves the values `1..t`. Choose the allowed L008 assignment `t-j` at the original named leaf `l:2:0:j`. Reverse the low interval by `f -> t-f` and the high interval by `f -> 2t+3-f`. These maps preserve their respective classes, and an edge of old difference `d=h-l` now has difference `(2t+3-h)-(t-l)=t+3-d`. Hence the reversal permutes the differences `1..t+2` and gives the displayed A labels, including `j` at the same named leaf. The retained topology and root-zero source labeling are documented in the [L008 archive](../references/upstream/bounded/research__LEMMAS.md.archive.md) and [pinned L008](https://github.com/drkmtr1/MDL_Bounded_Search/blob/e48b94eec4091b4fe189e325cab2eda464409943/research/LEMMAS.md#L21), source blob `f942e3b8b7628353ef7cf9d8cf53759c2eed0478`.

Apply retained R241 with A as the right component and B as the left. Its condition is `x_A=y_B=t`, so `L_A--U_B` is exactly the original `s:2--s:1` and gives difference `n_A=t+3`. R241 adds `p_B=q+2` to every A label, keeps B's low labels, and adds `n_A=t+3` to B's high labels. A's differences remain `[1,t+2]` and B's become `[t+4,q+r+t+6]`. Together with the connector they give `[1,m-K]`. The seed label blocks in order are B low `[0,q+1]`, A low `[q+2,a-1]`, A high `[a,a+1]`, and B high `[a+2,m-K]`. The alpha cut is at their low size `a`. The returned actual ports are `L_B=s:0` at `t` and `U_A=s:3` at `a`, with offsets `(t,0)`. The original `s:0--s:1--s:2--s:3` concatenates the witnessing paths. This application uses the [retained R241 argument](../references/upstream/mdl/N241_relational_ports.md), [pinned proof](https://github.com/drkmtr1/Math-Discovery-Lab/blob/858a8c1fcfda87ba40bb1adee498a6131504a803/research/candidates/volume-010.md#L4364-L4405), and [adopted disposition](https://github.com/drkmtr1/Math-Discovery-Lab/blob/858a8c1fcfda87ba40bb1adee498a6131504a803/research/candidates/volume-010.md#L4488-L4505), source blob `faca17cfa4c484127413762adc0c36b771a18f71`.

Now add `K` to every seed high label. The high block moves to `[K+a,m]`, and each original prefix edge gains exactly `K` in its difference because it joins a low and a high vertex. The named labels after substitution are exactly those in the prefix formula. For the middle leaves specifically, the B labels `q+3+j` for `j<t-1` and `q+4+j` for `j>=t-1` gain `t+3+K`, giving `K+a+3+j` and `K+a+4+j` respectively.

## Adjacent continuation and scope

Let `w_i=s:(3+i)` for `0<=i<=K`, with `f(w_0)=a+K`. Assign `f(w_i)=a+(i-1)//2` for odd `i` and `f(w_i)=a+K-i//2` for even `i>=2`. The `ceil(K/2)` odd positions increase from `a` to `a+ceil(K/2)-1`. The `floor(K/2)` even positions decrease from `a+K-1` to `a+ceil(K/2)`, with the even subsequence empty at `K=1`. Thus they together use exactly `[a,a+K-1]` once. At odd `i=2u+1`, the preceding value `a+K-u` exceeds the current value `a+u` by `K-2u=K-i+1`, including the first edge at `u=0`. At even `i=2u`, the current value `a+K-u` exceeds the preceding value `a+u-1` by `K-2u+1=K-i+1`. Thus the original path takes differences `K,K-1,...,1`, and the combined labeling is graceful with the prefix intact. At `K=1` the original edge `s:3--s:4` has labels `a+1,a` and difference `1`. The construction terminates after the finite prefix formulas and exactly `K` suffix assignments. See the [adjacent path-consumer proof](PROOF_OBLIGATIONS.md#active-endpoint-above-the-interval).

The accepted `q>=r`, `K>=2` branch returns the nonadjacent port `a+K+1`. This `q<r` branch returns the adjacent port `a+K` for `1<=t<=q+1`, including `K=1`. The region `q<r`, `t>=q+2` remains outside this construction and no nongracefulness conclusion follows. The earlier branch's `K=1` case, padding, additional positive branches, further branched sections and arbitrary repetition remain separate proof obligations. The parameters independently supply the complete labeling without requiring a searched prefix or a supplied whole-target labeling. Finite evidence corroborates the symbolic proof. See the [accepted nonadjacent B3 proof](B3_UNPADDED_QGE_R.md).
