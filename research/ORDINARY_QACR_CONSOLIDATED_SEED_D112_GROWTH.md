# D125 — Consolidated three-center seed suppliers and indexed right growth

For the precise union below and every exact integer r≥2, the ordered original `[[q,a,c],[r]]` has an explicit ordinary graceful labeling at physical pins `s:0=0`, `s:1=q+a+c+r+5`, `b:1:0=1`. This consolidates the accepted seed suppliers and applies the already proved [D112 growth theorem](ORDINARY_EXTREME_SPINE_GROWTH.md) to their exact named outputs.

## Exact union and dispatch

All quotas below are exact integers. The seed has right quota two. The sectors are disjoint by left parity. Within Sector III, the listed priority resolves overlap.

| Sector | Ordered left quota condition | Deterministic supplier |
| --- | --- | --- |
| I | All odd, q≥5 and a,c≥3 | [D120](ORDINARY_QAC_2_ODD_C_DISJOINT_R226_SUPPLIER.md) |
| II, canonical | q≥5 and a≥3 odd, c≥2 even | [D119](ORDINARY_QAC_2_EVEN_C_DISJOINT_R226_SUPPLIER.md) |
| II, other covered orders | Exactly one even quota at least two, both odd quotas at least three, at least one odd quota at least five | [D121](ORDINARY_QAC_2_TWO_ODD_ONE_EVEN_ROLE_TRANSPORT.md), with C at the unique even index, H at the least index of an odd quota at least five, and L at the remaining index |
| III, first priority | Even q,c≥6, a=3 | [D123](ORDINARY_U3U_2_MODIFIED_SHARED_MIDDLE_CORE.md) when q=c, [D124](ORDINARY_Q3C_2_UNEQUAL_MODIFIED_SHARED_MIDDLE_CORE.md) otherwise |
| III, remaining covered orders | Even q≥6 and c≥2, odd a≥3, with a≥5 or c≤q−4 | [D122](ORDINARY_QAC_2_TWO_EVEN_FIXED_CORE_CLASSIFICATION.md), using its exact two-vacancy branch at a=3 and four-vacancy branch at a≥5 |

The accepted positive D118 family is D119's pointwise specialization at c=2. D119's progressions then give exactly D118's four reserved B labels and differences, and the same ordered host allocations and named terminal assignments give the D118 labeling. D121 includes the whole Sector II. Its accepted role map is the identity exactly in the canonical branch, since C must be at index 2 and H at index 0 there. In other covered orders we use only the accepted D121 rule.

The first Sector III branch covers all a=3, c≥6 within the even outer bounds. For a=3 and c=2 the D122 bound c≤q−4 holds for every q≥6. At a=3 and c=4 it holds precisely for even q≥8, leaving exactly (6,3,4) uncovered within Sector III's minima. All odd a≥5 in this sector satisfy the other D122 condition. When a=3 and 6≤c≤q−4, the D124 branch takes priority and D122 remains an alternative on its original labeled core. At q=c the D122 cutoff cannot hold. The D122 and modified cores have different physical labels and need no pointwise agreement.

For the first inclusion, every dispatched branch satisfies the exact hypotheses of the named accepted theorem in the table. For the reverse inclusion, D120 supplies Sector I, D118 and D119 only supply canonical Sector II, and D121 supplies precisely the stated Sector II. The positive sector of D122 lies in Sector III, including its overlap with the priority branch, and D123 and D124 partition that priority branch into equal and unequal outer quotas. Thus the dispatch covers precisely the accepted positive D118–D124 union. No added role permutation or extra seed premise enters the argument.

Reject non-exact integers, including booleans, negative left quotas and r<2 as invalid. A zero left entry describes a degree-one center directly attached to the spine and lies outside the supplier union. The coverage result OUTSIDE_ESTABLISHED_COVERAGE is distinct from a proved fixed-interface obstruction. In particular (6,3,4) remains outside this union and the archived D122 obstruction for it applies to D122's own fixed labeled core. D122 excludes every completion of that core at a=3 and c≥q−2 by the residual parity-class capacity. The modified core can supply members of that sector. The coverage result gives no verdict on a different core at the unresolved triple.

## Indexed growth at the same physical exit

Let n=q+a+c+7 be the seed edge count and m=n+r−2=q+a+c+r+5 the final edge count. The final original has two spine vertices, four centers, q+a+c indexed left terminals and r indexed right terminals. There is one spine edge, there are four distinct attachments and every terminal has exactly one indexed pendant incidence. This gives m+1 vertices and m edges and builds a tree. Its centers lie one edge from the spine and its terminals two. Keeping only right indices 0 and 1 induces the exact named seed with every other original name, role, edge and incidence multiplicity unchanged.

Let g be the selected accepted ordinary graceful seed labeling on that actual induced subtree. D118–D120 and D122–D124 give the actual named spine and center attachments in their constructions. D121 fixes the entire spine and right section in its proved named incidence correspondence, so the same properties and pins hold after its accepted transport. Each possible selected seed has pins (0,n,1), with `s:1` the terminal endpoint, predecessor `s:0`, and exact neighbor set `{s:0,b:1:0}`. The right center is off the spine, and `s:1` carries the current maximum n. All suppliers give n−1 and n−2 at right indices 0 and 1, respectively, including the D121 case by its fixed right names. This checks every D112 premise.

Evaluate all seed core labels, intervals, reflection centers and assignments at n. The final rule is
```text
f(s:1) = m
f(l:1:0:k) = n+k−2  for 2≤k≤r−1
f(v) = g(v)        for every other seed vertex
```
At r=2 the fresh index interval is empty and m=n, so agreement is pointwise. At right quota r the current edge count is m. The next actual name `l:1:0:r` is fresh and its unique new edge attaches to the same off-spine right center. The label n+r−2=m there and the raised exit m+1 are exactly D112. Only the right center's degree increases among old vertices. The new terminal has degree one and distance two from the preserved witnessing spine. Old vertices, roles, incidences and distances are retained. Exit neighbors and pins remain correct at the new maximum. Finite induction gives the displayed indexed labeling and exact original for every r≥2.

## Direct full inventories and signs

Independently of the growth theorem, the old non-exit vertices carry [0,n−1] once. The fresh indices carry [n,m−1] once and the final exit carries m. These disjoint parts exhaust [0,m]. The seed spine and right attachment had weights n and n−1. Since they are the only incidences at the old exit, every other seed weight stays in [1,n−2], each once. Each fresh right terminal k gives weight n+k−3 by subtraction of the right center's one, so these edges give [n−1,m−2] once. The final right attachment and spine have weights m−1 and m, respectively. The four edge groups and their weight bands are disjoint and exhaustive. Both newly inserted intervals are empty at r=2. If right index 0 incorrectly used m−1 rather than its fixed n−1 at r≥3, it would collide with the last fresh index r−1, whose label is n+r−3=m−1.

Orient from the traversal class containing the entrance. It contains the right center, and the exit and each right terminal are in the opposite class. All unchanged signed differences retain their signs and values. The changed spine and right attachment are positive, as is each new right-terminal incidence. Every negative signed incidence of the seed therefore persists unchanged. No separation or sign hypothesis is imposed.

Each retained seed emits its indexed labels and incidences by linear scans in its quotas. D121 uses the same numerical allocation and a constant-time index correspondence per output. A single output pass over the fresh right indices and the exit substitution use O(q+a+c+r) indexed operations in total and terminate. The finite verified boundary at r=2 uses stored labels only. The quantified growth proof is symbolic.

## Obstruction and remaining scope

For a graceful labeling the total of the differences equals the total of the labels. Modulo two an absolute edge difference equals the sum of its two endpoint labels. Thus the excess-degree weighted sum is even. The left-center excess degrees are q,a,c. The exit has excess degree one and label m, the right center has excess degree r and label one, the entrance label is zero, and every terminal has excess degree zero. At the prescribed pins,
```text
q f(b:0:0) + a f(b:0:1) + c f(b:0:2) + m + r ≡ 0 (mod 2)
m + r = q + a + c + 2r + 5
```
When all three left quotas are even, including zero under the degree-one center convention, the center terms are even while m+r is odd. Hence the prescribed physical interface is impossible for every exact integer r≥2 in that all-even sector. This proof concerns the three pins.

In the two-even sector, the single odd quota at either outer center remains outside the established ordered domain, as do smaller quotas and the remaining uncovered ordered cases. Sector II requires the stated minima for each even and odd quota, and Sector I requires its stated ordered minima. Direct-leaf centers, other center multiplicities, interior empty sections, alternative physical interfaces and general ordinary spine composition remain separate obligations. The present result is an indexed application of supplied seed families.
