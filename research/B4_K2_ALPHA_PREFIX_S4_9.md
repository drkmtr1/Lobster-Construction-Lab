# B4-K2-ALPHA-PREFIX-S4-9-001

## Original prefix and conditional completion

Let T be the [frozen D063 original](../evidence/validation/B4_K2_D062_TWO_EDGE_TRANSPORT_001/target_original.json)
with profile `[[2],[2],[2],[2],[],[],[]]`. Withhold only s:5 and s:6.
The induced named P has profile `[[2],[2],[2],[2],[]]`, spine s:0
through s:4, and the same four branch centers and eight terminal
leaves. It has 17 vertices and 16 edges. The only pending edges of
T are s:4--s:5 and s:5--s:6. Each center is one edge from the
appropriate original spine and every terminal is two edges away.

With physical s:4 high, alternating the spine forces
s:0,s:2,s:4 high and s:1,s:3 low. Each center is opposite its spine
attachment and each of its two terminals is opposite the center.
Thus L has eight original names, s:1, s:3, b:0:0, b:2:0 and the
four terminals at sections 1 and 3. H has the other nine,
s:0,s:2,s:4,b:1:0,b:3:0 and the four terminals at sections 0 and 2.
The classes are disjoint, cover P, and every original edge joins them.

Suppose f labels L by 0..7 and H by 8..16 bijectively, uses each
original difference 1..16 once, and has f(s:4)=9. Keep the low labels
and increase each high label by two. The used labels are [0,7] and
[10,18], leaving the exact complement R={8,9} in [0,18]. Each
original edge increases in difference by two because its high
endpoint was larger and its low endpoint is unchanged. Hence the
used differences are [3,18] and D={1,2}. Physical s:4 becomes 11.
The assignments s:5=9 and s:6=8 use both holes and give the actual
pending weights 2 and 1. This argument proves the consumer from the
supplied-P hypotheses independently of how f is obtained.

## Direct analytic supply on P

The two extreme constraints are that difference 16 uses an original
0--16 edge and difference 1 uses an original 7--8 edge. Since
physical s:4 is pinned to 9 and touches only s:3 in P, choose
s:3=7 to use difference 2 there, and b:3:0=8 for difference 1 on
their original attachment. Choose s:2=16 and b:2:0=0 to use
difference 16 on their actual edge. This gives weight 9 on s:2--s:3.
Choose s:1=2 for weight 14 on s:1--s:2 and put 15 on the first
terminal of the zero host for weight 15. These are constructive
choices within the required classes.

The high-label sum is 108 and the low-label sum is 28.
Each original edge has one high and one low endpoint, so the sum
of edge differences equals the high degree-weighted sum minus the
low degree-weighted sum. Above their degree-one contributions, the
high vertices contribute f(s:0)+2(f(s:2)+f(b:1:0)+f(b:3:0)).
The low vertices contribute 2(f(s:1)+f(s:3)+f(b:0:0)+f(b:2:0)).
Consequently every supplier has

```text
f(s:0)+2(f(s:2)+f(b:1:0)+f(b:3:0)-f(s:1)-f(s:3)-f(b:0:0)-f(b:2:0))=56.
```

Here 56 is 1+...+16 minus (108-28). In particular f(s:0) is
even. With the chosen values, taking s:0=10 gives
f(b:1:0)=f(b:0:0)+8. Select the remaining low label 6 for b:0:0,
so b:1:0 is 14. The original edges s:0--s:1, s:0--b:0:0 and
s:1--b:1:0 give 8, 4 and 12. Assign 11 to the other third terminal.
The remaining high labels 12 and 13 at the first terminals contribute
6 and 7 at their center 6. The remaining low labels are 1,3,4,5
and the remaining differences are 3,5,10,13. At the second center
14, take terminals 1 and 4 for weights 13 and 10. At the fourth
center 8, use 3 and 5 for weights 5 and 3.

| Physical names in order | Labels | Differences |
|---|---|---|
| s:0, s:1, s:2, s:3, s:4 | 10, 2, 16, 7, 9 | 8, 14, 9, 2 |
| b:0:0, l:0:0:0, l:0:0:1 | 6, 12, 13 | 4, 6, 7 |
| b:1:0, l:1:0:0, l:1:0:1 | 14, 1, 4 | 12, 13, 10 |
| b:2:0, l:2:0:0, l:2:0:1 | 0, 15, 11 | 16, 15, 11 |
| b:3:0, l:3:0:0, l:3:0:1 | 8, 3, 5 | 1, 5, 3 |

The spine row follows consecutive incidences. Every branch row lists
its attachment first, then the two named terminal edges in order.
The label lists give exactly the required integer ranges on L and H.
The differences are a permutation of 1..16, and physical s:4 is 9.
This supplies the prefix directly from its own incidences and resource
arithmetic. The conditional completion above now supplies the exact
finite original T at q=r=t=K=2. No feasibility query is necessary.

The [evidence bundle](../evidence/validation/B4_K2_ALPHA_PREFIX_S4_9_001/README.md) records original-bound
certificate checks, a separate standard-library audit, and distinct
graph and label-ledger identities. This construction is for one finite
target. The universal interior continuation for q,r,t≥2 and K≥2
remains open. D062 and the restricted D063–D065 failures retain
their stated scope.
