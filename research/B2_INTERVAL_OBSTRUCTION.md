# Why a successful fixed interval need not repeat

**Claim:** For the unit family `q=r=1,z0=z1=0`, with any K>=3, no valid prefix can return the above-side interval starting at ell=2. This is a restricted interface obstruction, not a nongraceful-tree claim. The mathematical role independently checked the argument below. No historical novelty is claimed.

## Exact proposed interface

Here `m=K+6`. The prefix through `s:2` has seven vertices and six edges. The proposed state leaves labels `2,...,K+1`, differences `1,...,K`, and active label `f(s:2)=K+2`.

Consequently the seven prefix labels must be

\[
\{0,1\}\ \cup\ \{K+2,K+3,K+4,K+5,K+6\},
\]

and its six actual edge differences must be exactly `K+1,...,K+6`.

The prefix's bipartition is

\[
A=\{s:1,b:0:0,l:1:0:0\},\qquad
B=\{s:0,b:1:0,l:0:0:0,s:2\},
\]

of sizes three and four. In particular, `s:1` and `s:2` are in opposite parts.

## K>=4

Two high labels differ by at most four, which is at most K, and the two low labels differ by one. Neither kind of edge can supply a required prefix difference greater than K. Thus every prefix edge must cross between the two low-labeled vertices and the five high-labeled vertices.

A connected bipartite graph has its two color classes fixed up to swapping: choosing the color of one vertex determines all others by parity of distance. This prefix's classes have sizes three and four, so it cannot have a two-versus-five proper coloring. Contradiction.

## Boundary case K=3

Now the prefix uses low labels0,1 and high labels5,6,7,8,9, with active `s:2=5`; its required differences are4,5,6,7,8,9. The only eligible high-high pair is5--9, producing difference4. If that edge is absent, the same bipartition argument applies.

If it is present, vertex5 is the actual prefix leaf `s:2`, whose sole prefix neighbor is `s:1`; therefore `s:1=9`. Remove this leaf and its difference4 edge. The remaining six vertices form the path

```text
l:0:0:0, b:0:0, s:0, s:1, b:1:0, l:1:0:0
```

in that successive order, with labels0,1,6,7,8,9 and remaining differences5,...,9. Differences between two of6,...,9 are at most three, so every remaining edge must cross low/high. A six-vertex path has three vertices in each bipartition class, yet only two low labels are available. Contradiction.

## The obstruction has the right scope

The release preserves a checked ell=2 example at K=1. At K=2, one explicit full witness is `s:0=7,s:1=0,s:2=4,s:3=2,s:4=3,b:0:0=1,l:0:0:0=6,b:1:0=8,l:1:0:0=5`; direct subtraction on the original edges gives1,...,8 once each. Thus the above ell=2 prescription succeeds for these small values and fails for every K>=3.

The independent balanced supplier instead chooses ell=3 when t=1, returns active K+3 and works for every K>=1. The failed fixed interval therefore identifies a real assumption to change. It does not contradict ordinary gracefulness, the successful shifted construction, or the possibility of another boundary representation.
