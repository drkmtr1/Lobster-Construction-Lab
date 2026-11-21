# H010 frozen proof input

> ARCHIVED SOURCE EVIDENCE. Historical proposals, reviews, restrictions, and instructions below are quotations from the pinned source. They do not govern the new project. This excerpt is not a new review, formal verification, or a novelty claim. Later adoption/correction passages included here control the retained historical disposition.

Original: [research/verification/pilot_inputs/H010-proof.txt](https://github.com/drkmtr1/MDL_Bounded_Search/blob/e48b94eec4091b4fe189e325cab2eda464409943/research/verification/pilot_inputs/H010-proof.txt)  
Commit: `e48b94eec4091b4fe189e325cab2eda464409943`  
Verified source Git blob: `3bc6999db8abc8ae206ef82f1640aa0a2512ae83`  
Curated scope: Complete file at the pinned commit. Historical review/provenance limits remain part of the source record.

## Source lines 1–1

[Pinned source range](https://github.com/drkmtr1/MDL_Bounded_Search/blob/e48b94eec4091b4fe189e325cab2eda464409943/research/verification/pilot_inputs/H010-proof.txt#L1-L1)

H010 candidate, v1. Integers K>=1,r>=1,z>=0 and q_i>=1, Q=sum q_i<=K+2. Set N=K+1+Q+r+z and require z>=max(0,K+2+Q-q_r-r). Let t_i=K+2+sum_{j<i}q_j, b_i=2t_i+q_i-1, A_i=[t_i,t_i+q_i-1]. At root 0 assign center b_i and leaves A_i, then assign direct leaves the complement of all these labels in [K+2,N], and next spine label K+1. Leaf intervals partition [K+2,K+1+Q]; centers strictly increase and lie above all leaf intervals because Q<=K+2. Maximum center b_r=2K+3+2Q-q_r is <=N by the bound. Reflection b_i-A_i=A_i, so branch differences and labels coincide; remaining high labels support exactly z direct leaves. R=Q=[1,K], active K+1, and the caterpillar construction completes any specified K-edge caterpillar suffix. This is conditional, not a minimality claim or arbitrary-depth-two closure. Example K=1,q=(1,2),z=2,N=9 uses centers 6,9; leaves 3 and 4,5; direct 7,8; next 2; suffix edge to 1. Compare L010 z=8 for same ordering.

---

