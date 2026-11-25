# D153 — Topological parity in the two-section D143 embedding

Task `LCL-ORDINARY-SPINE-TWO-FIRST-CENTER-ONE-DIRECT-LEAF-001`. Counts and parameters are exact integers, excluding booleans. All profiles refer to the original named vertices and parent incidences.

## 1. Scope and graph counts

Use the exact [D143 two-section embedding](ORDINARY_SPINE_TWO_SECTION_CUT_STATE.md) and return on an independently supplied named D134 p=1 prefix with n=2c+2 edges, actual frontier v oriented to zero, and crossing spectrum [d,n] at c with d=c+2. The actual next spine vertices are u,w, attached by the original edges vu,uw. The two sections add 2K vertices and 2K edges, with n≥2K. A successful D143 completion supplies a reduced exterior tree on the fresh exterior vertices and v. It has lower fresh width A, upper fresh width B, s=2K−A−B gap leaves and s≥K. The reduced tree is labeled on [0,A+B], separates every edge after A, and has v=A. The D143 formation proof also places both spine vertices and all positive centers in that exterior. These inherited premises specify the embedding and exact D134 return.

Write C_i for the number of positive centers, D_i for the number of direct leaves and T_i for the total terminal leaves at centers in section i. Color the original tree with v in the lower graph class. The two spine edges put u in the upper graph class and w in the lower graph class. First-section centers and direct leaves are actual children of u, hence lower, and each terminal of a first-section center is upper. Second-section centers and direct leaves are actual children of w, hence upper, and every terminal of a second-section center is lower. Consequently the fresh graph-class cardinalities are

    N_low  = 1 + C_1 + D_1 + T_2,
    N_high = 1 + C_2 + D_2 + T_1.

The constants count w and u respectively. Each zero entry in a profile contributes one actual direct leaf and no center or terminal. An empty profile contributes its spine vertex alone. Arbitrarily many positive centers and their named terminal indices are counted by their own parent incidences. No old vertices enter these fresh totals, and N_low+N_high=2K.

## 2. Exact crossing counts and topological parity

The connected reduced exterior crosses its cut on each actual edge. Its two reduced label classes therefore agree with the graph classes on the exterior, since they agree at their common root v. In particular the A lower fresh exterior vertices have the lower graph color and the B upper fresh exterior vertices have the upper graph color. Each gap leaf takes the graph color opposite the color of its own exterior parent.

Let L be the number of gap leaves with a lower exterior parent and U the number with an upper exterior parent. Counting the same fresh graph colors, including the actual gap leaves, gives

    N_low = A + U,    N_high = B + L.

For the following edge count use the physical label cut in the gap. Put g=s−K and k=K−A. Since A+B+s=2K, k=B+g and s−k=A+g. The physical gap-source alphabet is [0,s−1], with k sources below the return cut and s−k above or at it. As D143 requires the exact residual difference spectrum, a gap edge crosses that cut exactly when its image coordinate is at least K. There are g such image coordinates. Write x for sources physically below the cut at an upper host and y for sources physically at or above the cut at a lower host. These two mutually exclusive actual incidence types are exactly the gap crossings, so x+y=g. Counting by parent side gives

    L=(k−x)+y = B+2y,
    U=x+(s−k−y) = A+2x.

This rederives [D144](ORDINARY_SPINE_TWO_SECTION_GAP_ALLOCATION.md) aggregate balance. Combining the two counts gives the exact necessary equations

    N_low  = 2(A+x),    N_high = 2(B+y).

Therefore both fresh graph classes have even cardinality, or equivalently

    1+C_1+D_1+T_2 ≡ 0 (mod 2),
    1+C_2+D_2+T_1 ≡ 0 (mod 2).

The physical side of a gap source depends on its assigned label. Its graph class depends on its actual parent, even when its label lies on the same physical side as its parent. The equations use each of those facts in its respective count.

For a selected named exterior that meets D143 and leaves only actual gap leaves, both crossing counts are forced by the topology and widths:

    x=N_low/2−A=(U−A)/2,
    y=N_high/2−B=(L−B)/2.

The necessary nonnegative integer condition is equivalently even N_low,N_high and A≤N_low/2, B≤N_high/2. Given those conditions and the inherited inventories, x+y=K−A−B=g. The side and parent count table at the aggregate level is then
```
                         lower host    upper host
    physically lower        B+y            x
    physically upper          y          A+x
```
with the required row and column sums. This proves equivalence for the aggregate counting restrictions, and leaves the actual image bijection, individual host eligibility and quotas to be checked.

The graph counts use the original profile alone. Exterior terminal or direct-leaf selections can change A,B,L,U and the values of x,y, while the graph-class parities are invariant. Role permutations keep every actual parent and color fixed. For an actual maximum-frontier input D143 conjugates both labelings and the cuts to the oriented minimum-frontier coordinates. This preserves the named tree, incidences, absolute weights and crossing statuses. The argument uses v to fix the graph color, so both actual polarities obey the same condition.

## 3. The selected two-first-center family

Prescribe (2r+1,2t) at u and (2p,2q,0) at w with independently specified r,t,p,q≥1. The first section has 2r+2t+4 fresh vertices, the second has 2p+2q+4. Thus K=r+t+p+q+4 and n≥2K is required. Here C_1=C_2=2, D_1=0, D_2=1, T_1=2r+2t+1 and T_2=2p+2q. It follows that

    N_low  = 2p+2q+3,
    N_high = 2r+2t+5.

Both counts are odd. Therefore every D143 exterior and gap completion fails throughout this infinite named family, in either polarity. The exclusion holds both with exterior terminals allowed and with them prohibited. It addresses the declared D143 embedding and return contract. Other ordinary graceful labelings remain outside the claim.

## 4. Retained symbolic controls

For the rows below M=p+q. The graph counts follow by substitution into §1 using the exact original profiles. The displayed widths and counts are those of the cited positive constructions. They agree with the crossing-count equations throughout the respective stated parameter domains.

| Positive control | (N_low,N_high) | (A,B) | Forced (x,y) |
|---|---|---|---|
| [D149](ORDINARY_SPINE_TWO_CENTER_EVEN_QUOTA_SUPPLIER.md), q≥2 in role order | (2M+2,10) | (3,4) | (M−2,1) |
| D149, q=1 in role order | (2M+2,10) | (3,5) | (M−2,0) |
| [D150](ORDINARY_SPINE_TWO_TO_ONE_TERMINAL_SUPPLIER.md), terminal-enabled | (2M+2,10) | (3,5) | (M−2,0) |
| D150, terminal-free where admitted | (2M+2,10) | (2,3) | (M−1,2) |
| [D152](ORDINARY_SPINE_TWO_DIRECT_LEAF_BOUNDARY.md), packets | (2M+2,2r+6) | (3,4) | (M−2,r−1) |
| D152, (r,p,q)=(4,2,2) | (10,14) | (5,7) | (0,0) |

For a test of insufficiency use [D151](ORDINARY_SPINE_ONE_DIRECT_LEAF_EXTERIOR_OBSTRUCTION.md) on (2r),(2p,2q,0), with its inherited size premises. The graph counts are (2M+2,2r+4), both even. Even the aggregate counts can pass on a reduced exterior: keep all the terminals and the direct leaf in the gap, use A=2,B=3, and reduced labels v,u,w,a and the two second centers respectively 2,3,0,1,4,5. The actual exterior weights are [1,5], and the equations give x=M−1,y=r−1, both nonnegative. However D151 forces two distinct direct gap leaves at w, where there is only one. This is a symbolic control, with no new named numerical original or campaign replay. All retained positive and obstruction scopes remain intact.

## 5. Method disposition

**RESOLVED SYMBOLICALLY BEFORE NUMERICAL EXECUTION.** The parity obstruction settles the authorized existence question throughout its infinite domain. No numerical corpus or hybrid campaign preparation is required for this result. Method choice under KEEP v11 follows mathematical leverage, with separately authorized hybrid discovery at genuine unresolved mathematical bottlenecks. The proof supplies a necessary admission check and exact aggregate crossing counts. Feasibility after those checks remains a separate question for a later authorized topology. The closed pilot, sealed D130, capped D148 execution and its twelve undecided two-center pairs retain their historical statuses.
