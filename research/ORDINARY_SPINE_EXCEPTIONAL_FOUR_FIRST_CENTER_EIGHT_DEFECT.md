# D166 — Four-first-center eight-defect parity-chain classification

Task LCL-ORDINARY-SPINE-EXCEPTIONAL-FOUR-FIRST-CENTER-EIGHT-DEFECT-001. All parameters are exact integers. Intervals include their endpoints, and reversed intervals are empty. Retain the declared D157 placement, including its connected crossing exterior and leaf-only gap. The input is an independent named \(S_{-1}\) prefix with actual extreme frontier \(v\), oriented label \(G(v)=0\), \(n=2c+2\), \(d=c+2\), and cut \(c\). Cut equality belongs to the upper side. The desired output is again \(S_{-1}\).

## 1. Exact statement, topology and exterior

The original first terminal quotas are \(1,3,4,4\) in any physical branch order. The two second positive quotas \(p,q\) have odd total \(R=p+q\). There is one actual direct leaf at the new spine vertex \(w\). Require \(n\ge 2K=R+21\), and put \(m=n+2K\). On the stated width-\((6,4)\) exterior with \(p\) at reduced host 10 and \(q\) at reduced host 8, **feasibility is exactly \(R\ge7\) and \(q\ge3\)**. Necessity permits selectable compatible first-center roles. Sufficiency uses the single first-role quota assignment below. With both second roles selectable, **the fixed exterior and full E+ class are feasible exactly when \(R\ge7\)**. The result concerns the declared D157 arrangement. The T class and ordinary nongracefulness are outside its scope.

The first section at \(u\) contributes one spine vertex, four positive centers and 12 terminals. The second at \(w\) contributes one spine vertex, two positive centers, one actual direct leaf and \(R\) terminals. Every fresh vertex has its own actual parent including the two spine attachments, so the fresh edge and vertex counts both equal \(17+4+R=2K\). With \(v\) in the lower graph class, the fresh lower class contains \(w\), the four first centers and the \(R\) second terminals. The fresh upper class contains \(u\), the two second centers, the direct leaf and the 12 first terminals. Thus \(N_{\rm low}=5+R\) and \(N_{\rm high}=16\).

For the exterior take \(A=6,B=4\). Use \(v=6,u=7,w=0\) in reduced labels, with the first-center roles \(b=2,a=3,c_1=4,Z=5\) and the second roles \(Q=8,P=10\). Here \(c_1\) is an actual center, separate from the cut \(c\). Assign \(b,a\) to the actual quota-one and quota-three centers respectively. Assign \(Z\) to the earliest actual quota-four center by original branch index and \(c_1\) to the other. Select the first actual indexed terminal at \(a\) for label 9 and the first at \(P\) for label 1. The actual direct leaf at \(w\) is a gap leaf.

The exact first exterior incidences \(vu,uZ,uc_1,ua,ub\) and \(a\) to its selected terminal have weights \(1,2,3,4,5,6\), respectively. The remaining exterior incidences \(uw,wQ,P\) to its selected terminal, and \(wP\) have weights \(7,8,9,10\), respectively. Their labels cover \([0,10]\) once, and each edge crosses the reduced cut between 6 and 7. The named exterior is connected through the actual spine and parent incidences. All original positive centers remain present, including \(P\) when its only terminal is selected for the exterior.

## 2. Gap coordinates, crossing counts and forced reservations

Use \(k=K-6=(R+9)/2\), \(s=2K-10=2k+2\), and \(J=s+3=2k+5\). The minimum positive odd total is three, so \(K\ge12\), \(s\ge K\), and \(6\le K\le6+s\). Place the old lower and upper labels using shifts 6 and \(6+s\) in the minimum orientation. Expand every upper exterior label by \(n+s\). The return cut is \(C=c+K\). The gap leaf of coordinate \(i\) has label \(6+c+i\). Its actual edge weight is \(d-1+\pi(i)\), with image formula \(i+5-j\) at a lower reduced host \(j\) and \(s+\beta+1-i\) at an upper reduced host \(6+\beta\). The first formula subtracts the lower host label from the gap label. The second subtracts the gap label from the expanded upper host and uses \(n-c=d\).

The gap source is physically lower iff \(i<k\). Its edge crosses iff its parent is on the opposite side. To give the exact output weight spectrum, a legal gap arrow must have \(\pi(i)\in[0,s-1]\) and \(\pi(i)\ge K\) iff that edge crosses. In row notation \(L_j=j,H_j=J-j\), the source lower and upper intervals are \(L_{[0,k-1]},H_{[4,k+5]}\). These cover \([0,k-1]\) and \([k,s-1]\) as coordinate sets. The noncrossing and crossing destination intervals are \(L_{[0,k+5]},H_{[4,k-1]}\), covering \([0,K-1]\) and \([K,s-1]\). Thus the two row partitions are exact separately. Each arrow below is legal only within its required destination row.

| Actual host | From \(L_j\) | From \(H_j\) |
|---|---|---|
| \(b\) | \(L_{j+3}\) | \(H_{j-3}\) |
| \(a\) | \(L_{j+2}\) | \(H_{j-2}\) |
| \(c_1\) | \(L_{j+1}\) | \(H_{j-1}\) |
| \(Z\) | \(L_j\) | \(H_j\) |
| \(w\) | \(L_{j+5}\) | \(H_{j-5}\) |
| \(Q\) | \(H_j\) | \(L_j\) |
| \(P\) | \(H_{j-2}\) | \(L_{j+2}\) |

The first five hosts are physically lower, so their \(H\)-source arrows cross and their \(L\)-source arrows do not. The upper parents \(Q,P\) have the opposite crossing pattern. This also explains why the return-cut predicate must be used to restrict the row formulas.

Let \(x\) count lower sources at upper hosts and \(y\) upper sources at lower hosts. There must be \(s-K=x+y\) crossing gap weights, since the exterior and old crossing bands are already filled. The lower-host gap count is \(k-x+y=B+2y\) and the upper-host count is \(A+2x\). The connected crossing exterior assigns sides according to graph color from \(v\), and a gap leaf has the color opposite its actual parent. Thus \(N_{\rm low}=2(A+x)\), \(N_{\rm high}=2(B+y)\). On this exterior \(x=k-8,\ y=4\). In particular \(k\ge8\), equivalent to \(R\ge7\).

The two upper images are at least 4, because their smaller intercept is \(s+3\) and \(i\le s-1\). All lower translations are nonnegative with the only neutral host at \(Z\). Inducting on destinations \(0,1,2,3\), any positive translation would require a previously used source, so each destination forces its equal source at \(Z\). For any compatible first-role assignment, \(Z\) has quota at least four. Since the original first quotas have maximum four, it takes its full quota in these four reservations. Under the supplied roles the other lower-host gap capacities are \(b=1,a=2,c_1=4,w=1\). After the neutral assignments, exactly four assignments to lower hosts are in each source row: \(y=4\) in \(H\), and \(k-x-4=4\) in \(L\). The rest have actual quota \(q\) at \(Q\) and \(p-1\) at \(P\).

## 3. Fixed-exterior necessity of \(q\ge3\)

Image \(L_4\) cannot be reached by a positive translation from a lower source once \(L_0,\ldots,L_3\) are consumed, and there is no neutral capacity left. Among upper sources, \(P\) would need \(H_2\), outside the source interval. Thus \(H_4\) must use \(Q\). At the opposite end, \(H_{k+5}\) cannot use \(P\) because \(L_{k+7}\) is out of range. A lower host would need a shift at least six to reach \(H_{[4,k-1]}\). So \(H_{k+5}\) uses \(Q\) at \(L_{k+5}\). These required sources are distinct when \(k\ge8\), and \(q\ge2\).

If \(q=2\), \(H_{k+4}\) has no \(Q\) capacity and its \(P\) image \(L_{k+6}\) is unavailable. A lower host must shift by at least five, and only \(w\) does this. That uses the unique direct leaf on \(H_{k+4}\to H_{k-1}\). Next \(H_{k+3}\) has no \(Q\) capacity and its \(P\) image \(L_{k+5}\) is occupied. Its only possible lower host would need a shift at least four, which only the exhausted \(w\) can provide. This contradiction proves \(q\ge3\). Every row endpoint in the argument exists at \(k=8\) and above. The argument depends on numerical shifts and original host capacities rather than the choices among first centers that fill those shifts. It gives a fixed-exterior obstruction.

## 4. Exact residual matching

The supplied roles have eight nonneutral lower-host uses with shifts \(1,1,1,1,2,2,3,5\) and sum 16. Let \(X,Y\) denote their source indices in \(L,H\) and \(X',Y'\) their respective translated destination indices. Valid reservations have distinct sources in each row and distinct images in each row. After the neutral reservations, the surviving \(L\to H\) matching is on \([4,k-1]\) with source holes \(X\) and destination holes \(Y'\). Each surviving source moves by zero at \(Q\) or by \(-2\) at \(P\). The surviving \(H\to L\) matching is on \([4,k+5]\) with source holes \(Y\) and destination holes \(X'\). Here \(P\) moves by \(+2\). Comparing sums on the two sides separately gives
~~~
2 N_PL = ΣY′ − ΣX
2 N_PH = ΣY − ΣX′
N_PL + N_PH = ΣY − ΣX − 8.
~~~
The last identity uses \(\sum X'-\sum X+\sum Y-\sum Y'=16\). A compatible exact quota therefore requires \(p-1=\sum Y-\sum X-8\).

For exact feasibility of a parity path, let \(S_j,D_j\) be the surviving source and destination indicators in that parity and \(B_j\) the indicator that source \(j\) uses \(P\). In the \(L\to H\) direction use increasing index, with
~~~
D_j = S_j − B_j + B_{j+2},    B_first = 0,    B_past_last = 0.
~~~
The first boundary forbids an image before the path, and the last boundary disallows an incoming arrow from a nonexistent source. This recurrence is necessary from the incoming identity and shifted arrows. It determines all \(B_j\), and it is sufficient exactly when \(B_j\) is integral, \(0\le B_j\le S_j\), and both boundaries hold. Assign its indicated shifts and the incoming count at each destination is exactly \(D_j\). Reverse the path order for \(H\to L\) to obtain the same recurrence. It applies to arbitrary legal reservations on this exterior. The total number of shifted assignments must equal the physical quota at \(P\).

A common hole has \(S_j=D_j=0\), which forces \(B_j=B_{j+2}=0\); it is a barrier to a moving repair. Cancel common holes only in selecting residual endpoints and keep those cells absent. For a path with one source hole \(x\) and one destination hole \(z\), the \(L\to H\) repair needs \(x\le z\) and shifts the surviving sources \(x+2,x+4,\ldots,z\) to \(x,x+2,\ldots,z-2\). For \(H\to L\) it needs \(z\le x\) and shifts sources \(z,z+2,\ldots,x-2\) to \(z+2,z+4,\ldots,x\). All other surviving indices act by identity. Equality has empty repair and makes the coincident hole common. Each moving interval must be free of common holes of its own parity. A common hole in an interval would violate the required shifted source or destination, equivalently its zero recurrence boundary. This is why moments and mere endpoint dominance across common holes do not suffice. The cases below have at most one pair of remaining holes per parity in each direction.

## 5. Constructive cases

Reserve \(L_0,\ldots,L_3\) at \(Z\) throughout, and take \(X=\{4,5,6,7\}\). Every row entry marked with a host means the actual incidence with that parent. Images below follow from the host shifts in Section 2.

### A. \(p=1\)

Here \(q\ge6\) is even and \(k\ge8\). Use the following complete nonneutral reservations.

| Source | Host | Image | Source | Host | Image |
|---|---|---|---|---|---|
| \(L_4\) | \(c_1\) | \(L_5\) | \(H_5\) | \(c_1\) | \(H_4\) |
| \(L_5\) | \(a\) | \(L_7\) | \(H_7\) | \(c_1\) | \(H_6\) |
| \(L_6\) | \(a\) | \(L_8\) | \(H_8\) | \(c_1\) | \(H_7\) |
| \(L_7\) | \(b\) | \(L_{10}\) | \(H_{10}\) | \(w\) | \(H_5\) |

All source and image indices lie in their stated rows even at \(k=8\). In sets, \(X'=Y=\{5,7,8,10\}\) and \(Y'=X=\{4,5,6,7\}\). Every remaining source uses \(Q\), giving both row bijections by index identity. The lower quotas are exactly one at \(b\), two at \(a\), four at \(c_1\), four at \(Z\) including the neutral cells, and one at \(w\). There are zero gap leaves at \(P\), which retains its selected actual exterior terminal. In particular the \(\{1,6\}\) pair is feasible on this first profile.

### B. \(p=2\)

Here \(q\ge5\) is odd and \(k\ge8\).

| Source | Host | Image | Source | Host | Image |
|---|---|---|---|---|---|
| \(L_4\) | \(c_1\) | \(L_5\) | \(H_6\) | \(a\) | \(H_4\) |
| \(L_5\) | \(c_1\) | \(L_6\) | \(H_{10}\) | \(w\) | \(H_5\) |
| \(L_6\) | \(a\) | \(L_8\) | \(H_7\) | \(c_1\) | \(H_6\) |
| \(L_7\) | \(b\) | \(L_{10}\) | \(H_8\) | \(c_1\) | \(H_7\) |

Again the indices are legal and the named lower quotas are exactly \(b=1,a=2,c_1=4,Z=4,w=1\). Now \(Y'=X\), and \(X'=\{5,6,8,10\}\), \(Y=\{6,7,8,10\}\). In \(H\to L\) the common holes 6,8,10 remain absent. The odd path has only source hole 7 and destination hole 5. Its sole move is \(H_5\to L_7\) at \(P\). All other surviving indices across either direction go to \(Q\). Both image rows are filled exactly once.

### C. \(p=3+2t,\ t\ge0\)

Require \(q\ge4\) even, so \(k\ge8+t\).

| Source | Host | Image | Source | Host | Image |
|---|---|---|---|---|---|
| \(L_4\) | \(c_1\) | \(L_5\) | \(H_5\) | \(c_1\) | \(H_4\) |
| \(L_5\) | \(c_1\) | \(L_6\) | \(H_6\) | \(c_1\) | \(H_5\) |
| \(L_6\) | \(a\) | \(L_8\) | \(H_{9+t}\) | \(b\) | \(H_{6+t}\) |
| \(L_7\) | \(a\) | \(L_9\) | \(H_{12+t}\) | \(w\) | \(H_{7+t}\) |

Here \(X'=\{5,6,8,9\},Y=\{5,6,9+t,12+t\},Y'=\{4,5,6+t,7+t\}\). The \(L\) reservation sources and \(H\) reservation images fit since \(6+t\le k-2\), \(7+t\le k-1\). All \(H\) reservation sources fit since \(12+t\le k+4\), and the \(L\) images lie in \([4,k+5]\). The reservations use \(b=1,a=2,c_1=4,Z=4,w=1\).

For \(L\to H\) cancel 4 and 5. For even \(t\), the ordered source-to-destination hole pairs are \(6\to6+t\) and \(7\to7+t\). For odd \(t\), they are \(6\to7+t\) and \(7\to6+t\). Both orders are legal and the base common holes are below the paths. At \(t=0\) both remaining pairs are equal and cancel, and at \(t=1\) the odd pair is equal and cancels. For \(H\to L\) cancel 5 and 6. For even \(t\) pair source holes \(9+t,12+t\) to destination holes \(9,8\) respectively. For odd \(t\) pair them to destinations \(8,9\) respectively. The destinations are never above the source holes. At \(t=0\) the odd pair at 9 cancels. The common holes at 5 and 6 are below the moving intervals. The remaining parity repairs are exact and independent. The moments give \(N_{PL}=t,\ N_{PH}=2+t\), so \(P\) receives exactly \(2+2t=p-1\).

### D. \(p=4+2t,\ t\ge0\)

Require \(q\ge3\) odd, again giving \(k\ge8+t\).

| Source | Host | Image | Source | Host | Image |
|---|---|---|---|---|---|
| \(L_4\) | \(c_1\) | \(L_5\) | \(H_5\) | \(c_1\) | \(H_4\) |
| \(L_5\) | \(c_1\) | \(L_6\) | \(H_7\) | \(a\) | \(H_5\) |
| \(L_6\) | \(c_1\) | \(L_7\) | \(H_{9+t}\) | \(b\) | \(H_{6+t}\) |
| \(L_7\) | \(a\) | \(L_9\) | \(H_{12+t}\) | \(w\) | \(H_{7+t}\) |

The sets are \(X'=\{5,6,7,9\},Y=\{5,7,9+t,12+t\},Y'=\{4,5,6+t,7+t\}\). The same row bounds hold and the named lower quotas are exactly \(b=1,a=2,c_1=4,Z=4,w=1\). The \(L\to H\) endpoint pairs, including equality and base common holes, are exactly those just proved for Case C. In \(H\to L\) cancel 5 and 7. For even \(t\) the two source holes \(9+t,12+t\) pair to \(9,6\) respectively. For odd \(t\) they pair to \(6,9\) respectively. These endpoints have the required parity and direction. The odd common holes 5 and 7 lie below its smallest possible moving index 9. The even path has no basic common hole, so the common 7 never obstructs a move of the even path. At \(t=0\) the odd pair at 9 cancels. These are exact, disjoint repairs on their surviving parity paths. The moments give \(N_{PL}=t,\ N_{PH}=3+t\), so \(P\) receives \(3+2t=p-1\).

In all four cases the \(s-12=R-1\) residual sources give \(q\) to \(Q\) after accounting for \(p-1\) at \(P\). All \(L\) reservations, including the four neutral ones, go to lower hosts and do not cross. All four \(H\) reservations go to lower hosts and cross, including the actual \(w\) leaf. Remaining \(L\)-source assignments go to upper hosts and cross, and remaining \(H\)-source assignments go to upper hosts and do not. Thus there are precisely \(x=k-8\) and \(y=4\) actual crossing incidences of the two types. Each arrow stays in its permitted destination row and all images are used once. Each case consumes its actual named gap quotas and hence its full original quotas after restoring the two exterior terminals.

## 6. Exact full E+ classification and saved controls

For positive \(p,q\) of odd sum, the four cases exhaust \(R\ge7,\ q\ge3\). At \(p=1,2\) the sum bound gives respectively \(q\ge6\) even and \(q\ge5\) odd. For odd \(p\ge3\), \(q\ge3\) means even \(q\ge4\). The other case is even \(p\ge4\) with odd \(q\ge3\). With selectable second roles place the larger quota at \(Q\). It is at least four for \(R\ge7\).

For arbitrary E+ exteriors in the declared D157 arrangement, count selected terminals from the first and second sections by \(e_1,e_2\), and write \(h\) for the exterior direct-leaf indicator. In reduced labels \(A=5+e_2\) and \(B=3+e_1+h\) by the rooted graph classes. Weight one forces \(vu\) with \(v=A,u=A+1\). For the terminal balance, consider the arithmetic reference where each lower slot \(j\in[1,A-1]\) contributes \(A+1-j\) at \(u\), and each upper slot \(A+\beta\) for \(\beta\ge2\) contributes \(A+\beta\) at \(w\), with \(vu,uw\) contributing 1 and \(A+1\). This reference has exactly \([1,A+B]\). A selected lower terminal at a true second center changes its contribution by \(\beta-1>0\). A selected upper terminal of a true first center reduces its contribution by the positive reduced label of that center. All other contributions retain the reference value. Matching the required difference sum forces a terminal on each side whenever any is selected, so E+ implies \(e_2\ge1\). Now \(5+R=N_{\rm low}=2(A+x)\ge12\), which gives \(R\ge7\). The explicit width-\((6,4)\) supplier covers all such cases. Both directions of this full E+ theorem are symbolic. The \(q\ge3\) obstruction at preassigned numerical roles concerns the stated fixed exterior. There is no transported finite negative in D166.

The frozen original target-0428 has first \((1,3,4,4)\), second \((5,4,0)\), and recorded digest `6f4cc649a76e055160ade2e856544762df550e4f49235df0c17e181421760256`. Its archived E+ arm used \(p=4,q=5,k=9,t=0,s=20\). The physical roles in increasing first branch index are \(b,a,Z,c_1\), and in the two second positive indices \(Q,P\). The two exterior terminals are `l:28:1:0` and `l:29:1:0`. Case D puts the actual direct leaf `b:29:2` at \(H_{12}\), i.e. source \(J-12=11\), and image 16. These agree with the archived feature and parent `s:29`. The theorem does not require equality with all saved coordinates.

The frozen original target-0429 has first \((1,3,4,4)\), second \((5,6,0)\), and recorded digest `ac1aa0aab83479ced6949d84651eb3267a0ac83bca4bc5f263f4dbfca6385636`. Its actual named prefix is the independently supplied D164 prefix (74 edges, maximum frontier `s:27`, actual cut 39 and oriented \(c=36\)). With \(p=6,q=5\), Case D has \(k=10,t=1,K=16,s=22,J=25\) and \(74\ge32\). The physical roles and chosen terminal indices remain as in target-0428. The actual direct leaf `b:29:2` at `s:29` uses \(H_{13}\), giving source 12 and image 17. This is a symbolic instance of the proved theorem and establishes E+ supply for that named original under the stated arrangement. Neither arm has a completed historical D164 disposition. Its T question and the D164 finite separation hypothesis remain undecided. [Local control bindings](../evidence/validation/LCL_ORDINARY_SPINE_EXCEPTIONAL_FOUR_FIRST_CENTER_EIGHT_DEFECT_001/CUSTODY.json)

## 7. Exact named reconstruction, return and composition

Each actual selected terminal is named at its own parent and given its specified exterior label. Assign increasing constructed gap coordinates within each host to that host's remaining original terminal indices in increasing order, and give the actual direct leaf its own designated coordinate. This keeps the original graph and witnessing spine. The old map and its fresh complement are
~~~
L_old   = [6,c+5] ⊔ [c+s+6,n+s+6]
L_fresh = [0,5] ⊔ [c+6,c+s+5] ⊔ [n+s+7,m]
D_old   = [1,d−2] ⊔ [d−1+s,n+s]
D_fresh = [d−1,d+s−2] ⊔ [n+s+1,m].
~~~
The label intervals follow by applying the two old translations. The old graph's cut membership is preserved by \(6\le K\le6+s\). Old crossing weights gain \(s\) and old noncrossing weights retain their values. The named exterior uses the two outside fresh label intervals and all its crossing weights gain \(n+s\), yielding the high fresh band. The gap label coordinate and its image each exhaust \([0,s-1]\) once, so they fill the entire middle vertex band and entire low fresh weight band. Its crossing weights are \([d+K-1,d+s-2]\) and its noncrossing weights \([d-1,d+K-2]\). Since \(s\ge K\), the old crossing weights lie at or above \(d+K-1\). Taken together, the complete graceful bijections are \([0,m]\) for labels and \([1,m]\) for weights, with crossing \([d+K-1,m]\) and complementary noncrossing \([1,d+K-2]\). The return has \(w=0\), cut \(C=c+K\), and \(m=2C+2\), as required for \(S_{-1}\).

At the first-section boundary let \(S_b,S_a,S_{c_1},S_Z\) be the actual gap-source sets of the four first centers. Let \(I=S_b\sqcup S_a\sqcup S_{c_1}\sqcup S_Z\) and \(J_1=(S_b+3)\sqcup(S_a+2)\sqcup(S_{c_1}+1)\sqcup S_Z\). Distinct reserved sources prove disjointness of the first union. The exact destination bijection proves disjointness of the second. Write \(I'\) and \(J_2\) for the respective complements in \([0,s-1]\). Excluding old \(v\), the fresh exterior labels supplied by the first section are \(E_1=\{2,3,4,5,n+s+7,n+s+9\}\) and those remaining are \(E_2=\{0,1,n+s+8,n+s+10\}\). The first reduced incidences exhaust \([1,6]\) and the remaining ones exhaust \([7,10]\) before expansion. The exact intermediate inventories are therefore
~~~
used labels        L_old ⊔ E₁ ⊔ (6+c+I)
remaining labels   E₂ ⊔ (6+c+I′)
used weights       D_old ⊔ (n+s+[1,6]) ⊔ (d−1+J₁)
remaining weights  (n+s+[7,10]) ⊔ (d−1+J₂).
~~~
The label-side partitions are intersections with \([0,C-1]\) and \([C,m]\). In particular the lower gap coordinates in the two parts are the intersections of \(I,I'\) with \([0,k-1]\). All exterior weight contributions cross. The old crossing and noncrossing bands remain as written, and in \(d-1+J_i\) the crossing and noncrossing parts correspond to \(J_i\cap[K,s-1]\) and \(J_i\cap[0,K-1]\). The literal unfinished connector is \(uw\) at oriented endpoints \(n+s+7,0\). Its crossing weight \(n+s+7\) stays in the remaining inventory at this boundary.

For actual minimum polarity retain the orientation, so the actual old lower shift is six and the upper shift \(6+s\). For actual maximum polarity orient the input by \(G=n-g\) and complement the output about \(m\), exchanging actual cuts \(n+1-c\) and \(m+1-C\) relative to the oriented cuts. An actual old lower label \(g\) has \(G\ge c\), hence goes to \(m-(n-g+6+s)=g+4\). An actual old upper label receives \(4+s\). Membership is preserved. Complement both intermediate label sets, exchange their side classifications and keep the absolute weights and crossing flags. The maximum-polarity endpoints are \(u=3,w=m\) with the same connector weight.

In an admitted finite sequence use only named initializers and transitions at their own required phases, sizes, actual ports and inventories, including the D157/D165 premises when using those blocks. The constructor supplies its exact state without inspection of any future labeling. At boundary \(i\) an existing label \(g\) retains its actual cut side at every later placement. Let \(C_i\) be that boundary's actual cut and \(\Lambda_i,\Sigma_i\) the sums of subsequent actual lower shifts and gap widths. Induction gives final label \(g+\Lambda_i+\Sigma_i\mathbf1[g\ge C_i]\). Existing crossing weights gain \(\Sigma_i\), and the others stay fixed. Apply the same map to this block's used intermediate labels and existing weights and to the assigned endpoints and crossing weight of the literal unfinished edge. Complements in the final palettes give the remaining resources, including later blocks. Finite intervals, exact quota lists and finite suffix sums all terminate. This proves immutable composition on admitted finite sequences within the stated arrangements.

## 8. Strategic reassessment

D165 used four nonneutral lower-host reservations. D166 uses eight, with shared holes and paired parity paths. For this exterior the conservation recurrence gives unique residual \(P,Q\) matching for any legal complete lower-host reservations, or an exact obstruction at a parity, boundary or physical quota condition. The moment supplies the total \(P\) count once the residual paths are feasible. This provides a reusable conditional allocation representation using the exceptional incidences and prefix sums rather than an arbitrary image mask. A broader theorem still needs a way to choose legal reservations from actual first-center quotas. Widths changing the two upper offsets also require a new proof of the residual path structure. The current pair of infinite families does not establish general exterior supply.

The proposed next question is a symbolic reservation criterion on this width, using the four- and eight-defect results as controls. It is unstarted. The proved eight-defect result requires no new hybrid execution on this family.
