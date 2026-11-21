# Bounded-search hypotheses and dispositions

> ARCHIVED SOURCE EVIDENCE. Historical proposals, reviews, restrictions, and instructions below are quotations from the pinned source. They do not govern the new project. This excerpt is not a new review, formal verification, or a novelty claim. Later adoption/correction passages included here control the retained historical disposition.

Original: [research/HYPOTHESES.md](https://github.com/drkmtr1/MDL_Bounded_Search/blob/e48b94eec4091b4fe189e325cab2eda464409943/research/HYPOTHESES.md)  
Commit: `e48b94eec4091b4fe189e325cab2eda464409943`  
Verified source Git blob: `c61c2c788c18f275a07b67eee4ad015caa646de1`  
Curated scope: Complete file at the pinned commit. Historical review/provenance limits remain part of the source record.

## Source lines 1–25

[Pinned source range](https://github.com/drkmtr1/MDL_Bounded_Search/blob/e48b94eec4091b4fe189e325cab2eda464409943/research/HYPOTHESES.md#L1-L25)

# Hypotheses

H001: For every integer N>=3 and 1<=q<=N-2, at a=0 with R=Q={1,...,N}, there exists a legal assignment of one center, q specified leaves and one distinct next spine vertex. Counterexample: a stated N,q with no allocation; proof must supply an assignment for all N,q. Relation: strengthens the one-step interval feasibility observation, not greedy continuation or suffix closure. E001: NOT_FALSIFIED_WITHIN_BOUNDS, now proved by L001. Originality unresolved.

H002: For N>=3, 1<=q<=N-2, after L001's specified placement, another edge from its new active label exists if and only if N>=2q+5. Counterexample requires either an admissible next label when the inequality fails, or absence when it holds. E002 tested N<=30; all 406 cases matched. L002 proves the statement. This is a property of that particular placement, not a statement about every possible placement.

H003 (FALSIFIED): for every N>=4 and 1<=q<=N-3, from root 0 with R=Q=[1,N], there exists an assignment of a q-leaf branch and a next spine edge leaving R'=Q'=[1,k], k=N-q-2, with next active label k+1. E003 exhausted 15 cases through N=8; a general impossibility proof is L003. This concerns this exact interface, not arbitrary residual interfaces or graceful completion.

H004 (PROVED conditional local construction): root 0 and finite unused resources R=Q=S, S positive integers. If b in S and A subset S\{b}, |A|=q, with {|b-x|: x in A}=A, then a branch with center b and leaves A preserves equal residual sets S\({b} union A), at the same root. This is a sufficient condition for a single branch, not a guarantee for an arbitrary sequence. A counterexample to equality alone as a closure condition is recorded as C007.

H005 (proved as L005; conditional composition): For any finite ordered nonnegative branch-size list q_1,...,q_r, define t_1=1, b_i=2t_i+q_i-1 when q_i>0 and b_i=t_i when q_i=0, with t_(i+1)=b_i+1. If root a=0 and R=Q=[1,N] with N>=t_(r+1), then all branches plus a next spine edge can be allocated legally. E004 tests 240 cases; separate mathematical review confirms proof. This imposes a strong extra resource budget, not ordinary gracefulness.

H006 (NOT_FALSIFIED_WITHIN_BOUNDS): For every finite ordered list q_i>=0, let N=1+sum_i(1+q_i). At root 0 with R=Q=[1,N], there is an allocation of all requested branches and one next edge using every label and difference. A counterexample is a list with exhaustively established absence of such fixed-root allocation; unrestricted nongracefulness does not follow. E005 found and separately verified witnesses for all 35 lists of length 1..3 with q_i<=2 and N<=8. No universal proof or initial-supply guarantee for this stronger fixed-root condition is known.

H007 (proved as L006, separately reviewed): In L005, order positive branch sizes ascending, followed by zero sizes, to minimize the required threshold over branch permutations within that construction. This makes no claim of optimality among other allocations.

H006 update: OPEN for unequal positive branch sizes. L007 proves arbitrary repeated equal positive sizes and any zero branches at exact budget; L008 proves at most one positive branch of any size. E006 tested 223 lists with r<=4, q_i<=4 and N<=10; all have independently verified witnesses. Finite evidence is not a proof of arbitrary lists.

H008 (proved L009, separately reviewed): K>=1, 1<=r<=K+2, z>=K+1. A first spine section with r one-leaf branches and z direct leaves, followed by a next spine edge and any caterpillar suffix of K edges, has a graceful labeling. The construction uses root 0 and N=K+1+2r+z. This is a sufficient restricted family, not a condition on every lobster.

H009 (proved L010, separately reviewed): For K>=1, r>=1 and ordered positive branch sizes q_1,...,q_r, let z>=0 and N=K+1+sum_i(q_i+1)+z. Define t_1=K+2, b_i=2t_i+q_i-1, t_(i+1)=b_i+1. If N>=b_r, the first section with those branches and z direct leaves, a next spine edge, and any prescribed K-edge caterpillar suffix is graceful. This is a sufficient restricted condition; a failed bound says nothing about other constructions.

H010: proved as a restricted caterpillar-suffix construction by the separately reviewed frozen proof verification/pilot_inputs/H010-proof.txt, submission 552157963012f02a455db099261fb503a9abc9b96f6488ee7c6dfc699f2b9872 and gate receipt 26f1f665d8696c8feec3b0e871f83e5fe7c63f80787b1259fd8da9eea85e4251. E009's independent computational verification disposition remains pending full provenance review. No arbitrary suffix or minimality conclusion.

H011 / P004-C1 (REFUTED): For every legal ordered m=9 path prefix a-b-c, if a one-leaf branch, a two-leaf branch, and a two-edge spine suffix at c are each separately feasible using the same initial unused labels and differences, and c has at least three distinct available incident differences, then all three requests can be allocated jointly. This fails at (a,b,c)=(0,1,3), by the separately reviewed C008 obstruction. See [precise hypothesis](pass_p004/COMPATIBILITY_PLAN.md), [counterexample](pass_p004/C1_COUNTEREXAMPLE.md), and [counterexample gate receipt](verification/promotions/f5db81806443273f133619c1a988c74d61d88f8356f1f76e50bce979f80dca29.json). The finite investigation found 512 failing antecedents in 680 fixed-prefix states; it does not refute unrestricted tree gracefulness or H006.

---

