# MDL N145: retained record

> ARCHIVED SOURCE EVIDENCE. Historical proposals, reviews, restrictions, and instructions below are quotations from the pinned source. They do not govern the new project. This excerpt is not a new review, formal verification, or a novelty claim. Later adoption/correction passages included here control the retained historical disposition.

Original: [research/candidates/volume-006.md](https://github.com/drkmtr1/Math-Discovery-Lab/blob/858a8c1fcfda87ba40bb1adee498a6131504a803/research/candidates/volume-006.md)  
Commit: `858a8c1fcfda87ba40bb1adee498a6131504a803`  
Verified source Git blob: `79e3fdaeafcf0048435c7507df16c68645bc879a`  
Curated scope: Complete selected historical session: statement, construction/argument, review and bounded disposition; original limits retained.

## Source lines 2735–2838

[Pinned source range](https://github.com/drkmtr1/Math-Discovery-Lab/blob/858a8c1fcfda87ba40bb1adee498a6131504a803/research/candidates/volume-006.md#L2735-L2838)

## MDL-NEXT-145 — mirrored two-port composition for actual diameter-five inputs (October 23, 2026)

<!-- MDL migration anchor; historical heading ID -->
<a id="objective-and-admission"></a>
### Objective and admission

N144 screened the retained Hrnčiar–Haviar (HH) diameter-five construction and Koh–Rogers–Tan (KRT) compatible-forest theorem. HH Theorem 3 gives ordinary gracefulness for each diameter-five block, but does not by itself promise the two extreme center labels needed for composition. KRT's literal Theorem 5 attaches one selected vertex per component, so its statement alone does not give two distinct ports at an interior block. The second mission tested a mirrored compatible forest whose actual connectors alternate between the two centers. Explorer-first-pass and route selection are recorded in the cycle closeout.

<!-- MDL migration anchor; historical heading ID -->
<a id="h145-a--exact-family-and-evidence-level"></a>
### H145-A — exact family and evidence level

Let an admitted diameter-five block have adjacent centers x,y, no terminal directly at either center, p odd-terminal branches and r even-terminal branches at x, and q odd-terminal branches and s even-terminal branches at y, where p,r,s are positive odd integers and q is a nonnegative even integer. Every branch has a positive terminal quota: odd branches have arbitrary positive odd quotas, and even branches arbitrary positive even quotas. In particular x has p+r children and y has q+s children. HH Case 1.1.1 supplies a graceful labeling with theta(x)=1, theta(y)=n, where n is the block order.

Take m=2k+epsilon>=1 blocks, k>=0, epsilon in {0,1}, in physical order

    D1,D1,D2,D2,...,Dk,Dk[,C].

Each repeated pair consists of two identically valued copies of its selected block; different pairs can have different orders and profiles. Optional C is an independently selected block from the same admitted HH profile class. In physical position t, orient the block as (y,x) for odd t and (x,y) for even t, and join consecutive displayed centers. Thus connectors alternate x-to-x and y-to-y, using distinct ports at each interior block. Every resulting tree in this family is gracefully labeled. For m=1 this is just its input block; the nontrivial composition starts at m=2. The claim does not cover arbitrary ordering of unpaired blocks.

Evidence: complete written construction, manually checked certificates, and separate-context AI Reviewer SCOPED PASS. This is not formal verification, qualified human review, historical novelty clearance, or a universal lobster result.

<!-- MDL migration anchor; historical heading ID -->
<a id="actual-hh-extreme-center-inputs"></a>
### Actual HH extreme-center inputs

Write R=p+q+r+s=2h+1, O=p+q, and E=r+s. Then O is odd and E is even and at least two. List the desired branch quotas t_1,...,t_R with the O odd quotas first and the E even quotas last. Put

    T = sum(t_j),       M = R+1+T.

Both R and T are odd, hence M is odd. In labels 0,...,M, set branch-center labels v_(2a-1)=a and v_(2a)=M-a. Join centers 0,M, join every v_j to M, and initially attach all terminal labels [h+2,M-h-1] to v_1=1. The vertex inventory is exactly {0,M}, the labels 1,...,h+1 and M-h,...,M-1, and the remaining interval [h+2,M-h-1]. The initial edge weights partition as

    {M}, [1,h], [M-h-1,M-1], [h+1,M-h-2],

so this is an explicit graceful tree.

If a current set of terminal leaves S is moved from parent u to a recipient v outside S, and S=u+v-S, reflection z -> u+v-z matches each old incident difference to a new one. Thus the affected difference multiset is preserved. Here v_j+v_(j+1)=M for odd j and M+1 for even j.

For 1<=j<=O, with current consecutive terminal interval [L,U] and quota t_j=2a+1, transfer [L+a,U-a-1] if j is odd and [L+a+1,U-a] if j is even. Each leaves exactly 2a+1 terminals at v_j and has endpoint sum v_j+v_(j+1). Since O<=R-2 and all later quotas are positive, each transferred interval is nonempty. After this odd-quota phase, the residual interval has even size and endpoint sum M. Split it into two adjacent equal-length intervals [L,U] union [V,W], so L+W=U+V=M.

For O<j<R, write t_j=2a. Maintain two disjoint, ordered, equal-length intervals with L+W=U+V. If j is even, transfer [L+a,U] union [V+1,W-a+1]; if j is odd, transfer [L+a-1,U-1] union [V,W-a]. The two transferred intervals have equal length, each the old half-length minus a; they remain nonempty because at least one positive even quota remains after this transfer. The transferred set is symmetric about (v_j+v_(j+1))/2; the donor retains exactly 2a terminals and the new pair of intervals has the required cross-sum, increased by one for even j and decreased by one for odd j. All recipient vertices are branch centers outside the terminal-label interval, and the transferred labels are current terminal leaves. The final branch v_R retains its full positive even quota.

Pair consecutive branches as (v_1,v_2),(v_3,v_4),...,(v_(R-2),v_(R-1)), leaving the last even branch unpaired. Among the pairs are (O-1)/2 odd-odd pairs, one odd-even pair, and (E-2)/2 even-even pairs. Before assigning quota identities, place the x-owned branches in the mixed pair and in (p-1)/2 odd-odd and (r-1)/2 even-even pairs. These pairs exist because q is even and s>=1 is odd. Move each selected whole pair from parent M to parent 0. Its two child labels sum to M, so its two parent-edge weights are exchanged; internal branch weights are unchanged. This preserves gracefulness and gives exactly the required branch profile at both centers. Adding one to every label gives

    theta: V(D) -> {1,...,n},       theta(x)=1, theta(y)=n.

This explicitly expands HH Case 1.1.1 (printed pp. 138-139); it does not infer port availability from the general HH diameter-five theorem.

<!-- MDL migration anchor; historical heading ID -->
<a id="mirrored-compatible-forest-labels-differences-holes"></a>
### Mirrored compatible forest: labels, differences, holes

Index m independently certified inputs G_i, with identical valued copies at mirrored indices i,m+1-i. An optional middle input is independent. Write n_i=|V(G_i)|=n_(m+1-i), S_j=sum_(a=1..j)n_a, S_0=0, and N=S_m. Let P_i be the even-distance class from x_i; let Q_i be its complement. Identical valued copies satisfy the KRT beau-pair requirements: their P-label sets agree and, for each edge weight, the signed difference theta(Q)-theta(P) agrees. For nonidentical inputs, these two conditions must be checked explicitly.

Set

    phi(v) = theta_i(v)+S_(i-1),  v in P_i,
             theta_i(v)+S_(m-i),  v in Q_i.

For a mirrored pair i,j=m+1-i, the equal local P-sets and their complements fill both global intervals [S_(i-1)+1,S_i] and [S_(j-1)+1,S_j] once. A middle block fills its own interval. Therefore phi is a bijection onto {1,...,N}.

For i<=floor(m/2), define T_i=sum(n_a, a=i..m+1-i), with T_(i+1)=0 for an empty sum, and H_i=n_i+T_(i+1)=S_(m-i)-S_(i-1).

For every local edge of weight d, the two corresponding mirrored edges have global weights H_i+delta and H_i-delta, where delta=theta(Q)-theta(P), 1<=|delta|<=n_i-1. Since H_i>=n_i, both are positive. Beau-pair signed agreement ensures this for each local weight d, whose absolute values run once through 1,...,n_i-1. The pair contributes exactly

    [T_(i+1)+1,H_i-1] union [H_i+1,T_i-1].

A middle block contributes 1,...,n_mid-1. Thus the missing weights are H_1,T_2,H_2,T_3,..., ending at H_k for m=2k, or at H_k,T_(k+1)=n_mid for m=2k+1. These are m-1 distinct holes in {1,...,N-1}. This reconstruction does not use KRT's printed i=m endpoint, whose formula is undefined for even m and is outside the edge-weight range for odd m.

<!-- MDL migration anchor; historical heading ID -->
<a id="two-actual-ports-graph-identity-and-domain-separation"></a>
### Two actual ports, graph identity and domain separation

The two center labels are

    A_i=phi(x_i)=1+S_(i-1),
    B_i=phi(y_i)=n_i+S_(m-i)=N+1-A_i.

Use zigzag component indices 1,m,2,m-1,... . Consecutive A-label differences are H_a in odd connector positions and T_(a+1) in even positions. Since B_i=N+1-A_i, the same connector differences result at the y-ports. Connect x-to-x in odd positions and y-to-y in even positions. This fills every hole exactly once. The quotient graph on the blocks is a path, so the result is a tree with all differences 1,...,N-1. This is proved by direct spectrum completion; KRT's single-attachment-vertex Theorem 5 is not used as a two-port assertion.

In physical order the path is

    (y_1,x_1),(x_m,y_m),(y_2,x_2),(x_(m-1),y_(m-1)),... .

It is exactly D1,D1,D2,D2,...[,C], with the prescribed orientation; each interior block uses different centers on its incoming and outgoing edges. Every noncenter vertex is at distance at most two from the center path. A terminal at either endpoint center is distance 2m+3 from a terminal at the other endpoint; hence the diameter is exactly 2m+3. The graph is a lobster. For this stated positive height-two family, deleting leaves twice leaves exactly the center path, an isomorphism-invariant backbone. Each block contributes one odd-child-count center q+s and one even-child-count center p+r. For m>=2, there are at least two odd counts, so these graphs fall outside N135/N141's fixed center-path class (first count odd and every later count even) in either path orientation. This is a project-domain comparison, not historical noncoverage.

<!-- MDL migration anchor; historical heading ID -->
<a id="manual-certificates-and-review"></a>
### Manual certificates and review

The smallest input has p=r=s=1,q=0, with quota 1 at the sole odd branch at x, quota 2 at its even branch, and quota 2 at the even branch at y; its order is 10. The 12-vertex input has quota 3 at the odd branch at x, quota 2 at its even branch and quota 2 at the even branch at y. The 14-vertex boundary example has p=r=s=1,q=2, with odd quotas 1 at x and 1,1 at y, and even quotas 2 at each of the two even branches. These seeds were checked manually, including all edge differences. The unequal-order assembly uses orders 10,12,10, total order 32, and physical order G_1,G_3,G_2. Its center pairs are (1,32),(23,10),(11,22), connectors have weights 22 and 12, and the six-center path is 32,1,23,10,22,11. Its internal weight sets are

    G1 {16,23,24,25,26,27,29,30,31}
    G3 {13,14,15,17,18,19,20,21,28}
    G2 {1,...,11}.

Together with 12 and 22 these partition 1,...,31, and the vertex labels partition 1,...,32. The separate Reviewer independently subtracted every edge and checked every vertex. For reproducibility, the global assignments are: G1 centers 1,32; children 24 with terminal 8, 31 with terminals 4,6, and 3 with terminals 27,29. G3 centers 23,10; children 2 with terminal 30, 9 with terminals 26,28, and 25 with terminals 5,7. G2 centers 11,22; children 12 with terminals 14,19,20, 21 with terminals 15,17, and 13 with terminals 16,18. The connectors are 1--23 and 10--22. The diameter is nine. No mathematical executable or certificate program was used.

The edge subtraction ledger is: G1, 32-1=31, 24-1=23, 24-8=16, 31-1=30, 31-4=27, 31-6=25, 32-3=29, 27-3=24, 29-3=26; G3, 23-10=13, 23-2=21, 30-2=28, 23-9=14, 26-9=17, 28-9=19, 25-10=15, 25-5=20, 25-7=18; G2, 22-11=11, 12-11=1, 14-12=2, 19-12=7, 20-12=8, 21-11=10, 21-15=6, 21-17=4, 22-13=9, 16-13=3, 18-13=5; connectors, 23-1=22 and 22-10=12.

**Disposition:** H145-A is a complete written construction with actual infinite-family input supply, manually verified certificates and separate AI Reviewer SCOPED PASS. Operation correctness, input existence and application are established for the stated domain. Historical formula priority and coverage of equivalent graphs remain unresolved; no new publication search was performed. Significance is a reusable two-port completion for paired unequal-order HH-profile blocks, beyond the stated N135/N141 fixed domain. Mirrored pairing remains a substantial restriction; arbitrary unpaired sequences, broader lobsters, alpha-labeling and the universal graceful lobster conjecture are not settled. Practical benefit, formal verification and qualified human review are not established. Preserve the N144 correction to the HH Figure 18 profile and the printed KRT endpoint qualification in the linked source and cycle records.
<!-- MDL migration anchor; historical heading ID -->
<a id="mdl-next-146--unequal-order-hh-block-composition-october-23-2026"></a>
# MDL-NEXT-146 — Unequal-Order HH Block Composition (October 23, 2026)

---

