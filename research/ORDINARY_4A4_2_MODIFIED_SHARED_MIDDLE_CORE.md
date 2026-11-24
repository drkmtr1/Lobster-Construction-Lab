# D128 — Four–odd–four modified shared-middle supplier

For every exact odd integer a≥3, the ordered original `[[4,a,4],[2]]` has an explicit ordinary graceful labeling at pins `(s:0,s:1,b:1:0)=(0,a+15,1)`. The fixed physical outer quotas are four. Two disjoint reserved batches share the middle host and contribute a−2 and one of its terminals, respectively.

## Named core and unused inventories

The original consists of two spine vertices, four centers and a+10 indexed terminals. Its spine edge, four center attachments and all terminal edges give m=a+15 edges and m+1 vertices. Every center attaches to its own spine vertex and each terminal to its own named center. This makes a tree whose centers and terminals are respectively one and two edges from `s:0--s:1`.

Write X, M, Z for the actual left centers at indices 0, 1, 2. Keep the [D123 modified core](ORDINARY_U3U_2_MODIFIED_SHARED_MIDDLE_CORE.md). The spine carries (0,m), the X, M, Z and right centers carry (2,m−6,m−4,1), X index 0 and M index 0 carry m−3 and m−5, and the two right terminals carry m−1 and m−2. The ten vertices induce a connected acyclic core. In original incidence order its weights are m on the spine, 2 on the X attachment, m−5 on X's reserved terminal, m−6 on the M attachment, 1 on M's reserved terminal, m−4 on the Z attachment, m−1 on the right attachment, and m−2 and m−3 on the two right terminals. Hence the distinct core labels are [0,2] and [m−6,m], and the distinct core weights are {1,2} and [m−6,m]. The unused label and difference sets are both [3,m−7]. The named vacancies at X, M and Z have quotas (3,a−1,4).

Every graceful labeling has an even excess-degree weighted sum, because each absolute edge difference is congruent to the sum of its endpoint labels modulo two and the total label and weight sums coincide. At the required pins and supplied centers that sum is `4·2+a(m−6)+4(m−4)+m+2`. Here m is even and at least 18, so the sum is even. The explicit resource partitions give sufficiency below.

## Joint reservations

Set t=(m−2)/2, e=m−8, I=[6,e], J={3,4,5,m−7}, and w(x)=m−4−x. These are integral since a is odd. We have e=a+7, so I has a+2 entries. The four J labels are distinct because m−7≥11. Its lower part is [3,5] and the upper singleton is e+1, so I and J partition [3,m−7]. The endpoints of I sum to m−2=2t. In fact
```text
t−2−6 = e−(t+2) = (m−18)/2 = (a−3)/2 ≥ 0.
```
Thus t−2, t, t+2 lie in I. When a=3, t−2 is the lower endpoint and t+2 the upper endpoint. The map w reverses all of [3,m−7] onto itself and sends I to [4,e−2].

For A on X/M take the label palette I minus {t} and the difference palette w(I) minus {t−4}. For B on M/Z take J plus {t} and w(J) plus {t−4}. Since t−4=w(t+2) is in w(I), including when t+2=e, the transfer preserves both full disjoint partitions. A has a+1 labels and weights and B has five of each. These palettes come directly from the parameter.

## Batch A — Select the midpoint at X and every pair at M

Every label in I is strictly between X and M, giving X weight x−2 and M weight m−6−x. In the reference palette w(I), X is always eligible. The two top labels e−1,e have M weights 3 and 2 and are forced to X. On [6,e−2], the reflection x↦m−4−x exchanges the two options and preserves the interval, whose endpoints sum to m−4. The midpoint is t−1 and its two equal weights t−3 form a single loop. All other labels fall into complete parallel pairs with distinct weight vertices and opposite host tags. Since the X map is bijective on I, their difference vertices and those of the forced endpoints are disjoint and cover w(I).

The labels t−2 and t form a pair even at a=3, when t−2=6 and t=e−2. The X and M rows are (t−4,t−2) and (t−2,t−4), respectively. Deleting label t and weight t−4 leaves t−2 forced to M at t−2 and does not alter any other component. The interval [6,e−2] has a labels. Before deletion it has (a−1)/2 pairs and one loop. Thus actual A has two forced X half-edges, one forced M half-edge, (a−3)/2 intact parallel pairs and one midpoint loop. Each such component has one label per difference vertex, and all rows and difference vertices are covered. In X/M order the exact integral X projection is `{2+2j+epsilon : 0≤j≤(a−3)/2, j integer, epsilon in {0,1}}`.

Choose j=0 and epsilon=1. X receives the midpoint and both forced upper labels, namely {t−1,e−1,e}. M receives every intact pair and the forced label t−2, namely [6,e−2] minus {t−1,t}. The sizes are exactly three and a−2. When a=3, the surviving M palette consists solely of t−2 and there are no intact pairs to allocate.

Independently the X weights are {t−3,e−3,e−2}. The decreasing map m−6−x sends [6,e−2] bijectively to [4,e−4], and deleting its inputs t−1,t removes t−3,t−4. Both removed weights are within that band, even when t−4=4 at a=3. Taking the disjoint union with the three X weights gives precisely [4,e−2] minus {t−4}, each once.

## Batch B — Fixed complementary chains

Both M and Z exceed all reserved labels. The Z and M weights are w(x) and w(x+2). Label t has M weight t−4, while its Z weight w(t)=t−2 lies in w(I) and is not t−4. A J label could give t−4 at Z only at t+2, or at M only at t. Neither belongs to J. For x in J the Z row is eligible and the M row is eligible exactly when x+2 belongs to J. In J only 3 has this property, since 4+2=6 and 5+2=7 are in I and m−7+2 exceeds the largest residual label. The upper singleton m−7 is therefore separate.

| Label | Eligible M weight | Eligible Z weight |
| --- | ---: | ---: |
| 3 | m−9 | m−7 |
| 4 | — | m−8 |
| 5 | — | m−9 |
| t | t−4 | — |
| m−7 | — | 3 |

The chain {3,5} joins two distinct vertices m−7 and m−9 through label 3 and has the Z half-edge of label 5 at m−9. Weight m−7 can only come from label 3 at Z. Weight m−9 is then consumed by label 5 at Z. This agrees with the R226 rooted tree extraction away from the half-edge vertex. Each of {4} and {m−7} is a singleton chain with a Z half-edge, and t is an isolated M half-edge. Every component balances, all reserved vertices are covered, and every label has an option. The unique extraction sends all four J labels to Z and t to M, giving quota (1,4) and exact integral M projection {1}. Their distinct weights are w(J) and t−4, which exhaust the B reservation.

## Assembly on the actual original

| Host | Terminal labels in physical index order |
| --- | --- |
| X | (m−3,t−1,e−1,e) |
| M | m−5, then increasing [6,e−2] minus {t−1,t}, then t |
| Z | (3,4,5,m−7) |
| Right | (m−1,m−2) |

A fills X indices 1 through 3 and M indices 1 through a−2. B fills M index a−1 and Z indices 0 through 3. The shared host M stays unchanged. These disjoint actual named slots exhaust all original vacancies and give aggregate quotas (4,a,4,2) including the core terminals. The independently supplied tree core has injective labels and distinct weights. Each batch has two distinct fixed core hosts one edge from the spine, actual named leaves, distinct integer labels avoiding the hosts and equally many distinct positive reserved differences. The full disjoint resource partitions, component balance and exact integral allocations satisfy [R226 revision 2, Section 10](../references/upstream/mdl/N226_R226_two_host_completion.md#n226-closeout). The direct weight calculations also independently prove [1,m] with multiplicity one, and the label partition proves [0,m] with multiplicity one. All names, incidence multiplicities and the witnessing spine are preserved.

Orient edges from the class containing `s:0`. The left terminals and right center belong to that class, and the three left centers, exit and right terminals belong to the other. All four X terminal labels exceed 2, and M's reserved terminal m−5 exceeds its host by one. The other M and Z terminals are below their hosts because their labels belong to [3,m−7]. The right terminal labels exceed one and all spine and attachment edges are positive. Thus precisely those five specified incidences are negative.

The exit is the terminal endpoint of the witnessing spine with exact neighbors `s:0` at zero and off-spine `b:1:0` at one, and the exit carries m. These are the exact [D112](ORDINARY_EXTREME_SPINE_GROWTH.md) premises. The construction checks exact integer type, odd parity and a≥3, so booleans, nonintegers, evens and smaller inputs are rejected. The bounded increasing scans and named writes take O(a) indexed operations and terminate.

## Scope of consolidation

This proof supplies only the named four–odd–four order. The D122 fixed-core obstruction and D125 historical union retain their exact scopes. D127's literal theorem covers the outer odd positions. For the middle-odd order, the earlier canonical suppliers explicitly require the first even quota to be at least six. Therefore a middle-odd order with the first even quota below six and the last at least six remains outside those literal statements. The role correspondence suggests a future consolidation of that case.
