# D214 independent rooted-cluster and exterior-shell composition

**PROVED WITHIN EXACT SCOPE.** The exact named original `[[p],[q_1,...,q_ell],[1],[t]]` is ordinary graceful for independently chosen positive integers p,t,qᵢ and ℓ≥3. The central supply uses the visually verified rooted existence theorem of Frank Van Bussel. The shell and the proof on the named union are direct and independent. [Primary-source assessment](../evidence/validation/D214_ROOTED_CLUSTER_EXTERIOR_SHELL/PRIMARY_SOURCES.md)

## 1. Isolate and supply the actual center-zero cluster

Use the four-vertex original spine `s:0,s:1,s:2,s:3`. The j-th center of section i is `b:i:j`, with original indexed terminals `l:i:j:d`, using zero-based center and terminal indices. In the cluster C retain only `s:1`, its ℓ actual centers and their qᵢ respective terminals. Its edges are the ℓ center attachments and Σqᵢ terminal incidences, so n=ℓ+Σqᵢ.

Every vertex of C is within distance two of `s:1`. Terminals belonging to distinct centers are at distance four, since their unique path meets `s:1`. Thus C has diameter four and `s:1` has eccentricity two. Every other vertex is distance at least three from a terminal in another branch, so `s:1` is the unique center. Its degree in C is ℓ, counting the actual central cluster neighbors only.

Van Bussel's thesis Theorem 4.5, printed page 112, supplies a 0-centred graceful labeling of every diameter-four tree whose central degree is at least three. By Definition 4.1 on printed page 102, the actual unique center of this even-diameter tree receives 0. The degree-two case of Theorem 4.4 is outside this application. The odd-degree result and the even-degree completion are documented separately within the proof of Theorem 4.5, without a parity requirement on the qᵢ in the resulting theorem. The archival scan resolves an OCR rendering that could otherwise suggest a strict degree inequality. [Official primary thesis](https://www.nlc-bnc.ca/obj/s4/f2/dsk1/tape3/PQDD_0011/MQ53395.pdf#page=123) · [Source audit](../evidence/validation/D214_ROOTED_CLUSTER_EXTERIOR_SHELL/PRIMARY_SOURCES.md)

To transport unlabeled existence, use any isomorphism from the actual named C to a tree carrying the asserted labeling. The unique center must map to the unique center. Each incidence `s:1--b:1:j` and `b:1:j--l:1:j:d` maps to its corresponding incidence under that bijection. Pulling back the labels retains every original name and exact endpoint difference. The resulting f has f(`s:1`)=0, labels [0,n] and differences [1,n]. Ordinary gracefulness is enough for C.

## 2. Independently supply the actual outer alpha component

Let H be the exact original `[[p],[],[1],[t]]`. It retains all four spine names and their three actual edges. Its one center at each of sections 0, 2, and 3 retains its own indexed terminals. For the nine-edge seed let the spine labels be (5,4,8,1), the center labels (3,2,9), and their index-zero terminal labels (6,7,0). In those respective incidence orders, direct subtraction gives spine weights (1,4,7), center weights (2,6,8), and terminal weights (3,5,9). The labels occur once each in [0,9]. At cut 5 the lower vertices have labels {0,1,2,3,4} and the upper vertices labels {5,6,7,8,9}. The spine edges, the three center attachments and the three terminal edges all cross it. The actual root `s:1` has maximum lower label 4.

Put u=p−1, v=t−1 and k=9+u+v. Carry each of the ten seed names to its label under E(x)=x+v I(x≥1)+u I(x≥6), where the indicators are on old numerical labels. The images of 0, [1,5] and [6,9] are respectively {0}, [1+v,5+v] and [6+v+u,k]. Give the additional left terminal indices 1 through u the successive labels [6+v,5+v+u]. Give the additional right indices 1 through v the labels [1,v]. The three old images and these two fresh intervals partition [0,k]. An interval whose right endpoint is smaller than its left endpoint is empty.

The shift at old cut 1 contributes v to the difference of the only incident edge at label 0, of old weight 9. The old cut 6 crosses precisely the edges of weights 3 through 9. This follows from their endpoint table: weights 1 and 2 have both endpoints below 6, and the other seven each have one endpoint at 6 or higher and the other below 6. Endpoint subtraction therefore leaves 1 and 2 unchanged, sends old weights 3 through 8 to [3+u,8+u], and sends 9 to k. The new left terminals join their actual center of label 3+v, giving the exact differences [3,2+u]. The new right terminals join their actual center of label k, giving [k−v,k−1]=[9+u,8+u+v]. These inventories are disjoint and exhaust [1,k].

At cut 5+v all old vertices retain their relative side from cut 5. In particular E(4)=4+v and E(5)=5+v. Each new left terminal is on the upper side and its center 3+v is lower. Each new right terminal is lower and its center k is upper. Thus g is an alpha labeling of H, with maximum lower label A=4+v at `s:1`. No equality of p and t enters the construction. For u=0 or v=0 the corresponding label and weight intervals are empty, and for u=v=0 the construction recovers the seed.

## 3. Direct named shared-root composition

The original is exactly the union of C and H. Their only common vertex is r=`s:1`, and their edge sets are disjoint. In particular both spine incidences at r belong to H, and the r-to-central-center incidences belong to C. Define F as follows.

```text
F(z) = A+f(z)       for z in C, including r
F(z) = g(z)         for z in H other than r with g(z)<A
F(z) = n+g(z)       for z in H other than r with g(z)>A.
```

The value g=A occurs only at r, and the C formula gives that same value because f(r)=0. The three rows use the disjoint consecutive intervals [A,A+n], [0,A−1] and [A+n+1,n+k], respectively. Their union is [0,n+k], so F is bijective and labels the root once.

Translation preserves each C difference, giving [1,n]. For an actual H edge let l≤A<h be the lower and upper old labels under g. Its combined endpoints have labels l and n+h, even when l=A at the root. The difference is therefore n+(h−l). The alpha property of g applies to all H edges, so these differences exhaust [n+1,n+k]. The partition into actual C and H edge sets now proves gracefulness. At the physical cut A+n+1 all shell edges cross and all cluster edges stay below, a statement about the verified weight bands.

The exact union is a tree since it joins two trees at one actual vertex. Its original four spine vertices and three spine edges already belong to H. Every off-spine center in either piece is adjacent to its actual original spine parent. Every terminal is adjacent to its own center. Thus the original spine witnesses the lobster property directly. The output preserves multiplicities, all center and terminal indices and every original incidence, with no added connector, duplicated root or padded branch.

## 4. Prescribed hand controls

Use the exact named roles from Section 1 in every row. For a shell the three center groups are in section order 0,2,3. Terminal tuples are in original index order, including the fixed index zero before any additional labels.

| Shell control | p,t | u,v | k | Spine labels | Center labels | Terminal tuples | Cut |
|---|---|---|---:|---|---|---|---:|
| Nine-edge seed | 1,1 | 0,0 | 9 | (5,4,8,1) | (3,2,9) | (6); (7); (0) | 5 |
| Unequal positive widths | 2,3 | 1,2 | 12 | (7,6,11,3) | (5,4,12) | (9,8); (10); (0,1,2) | 7 |
| One zero width | 1,2 | 0,1 | 10 | (6,5,9,2) | (4,3,10) | (7); (8); (0,1) | 6 |

| Shell control | Actual spine weights | Actual center-attachment weights | Actual terminal weights |
|---|---|---|---|
| Nine-edge seed | (1,4,7) | (2,6,8) | (3); (5); (9) |
| Unequal positive widths | (1,5,8) | (2,7,9) | (4,3); (6); (12,11,10) |
| One zero width | (1,4,7) | (2,6,8) | (3); (5); (10,9) |

In each row the labels fill [0,k] and the displayed absolute differences fill [1,k] once each. The named endpoints place every actual edge across the stated cut, with `s:1` immediately below it.

For the full control take the exact original `[[2],[1,2,1],[1],[3]]`. Independently of the shell, give the isolated cluster root 0 and centers `b:1:0,b:1:1,b:1:2` labels (1,6,7). Give the three respective terminal tuples (5), (3,4), (2). Against centers 7 and 1 the labels 2 and 5 consume weights 5 and 4. The remaining labels 3 and 4 at center 6 consume weights 3 and 2. The root attachments consume 1,6,7, so this exact seven-edge cluster has the full weight alphabet and labels [0,7]. It was supplied before inserting it into the unequal shell row.

Here n=7, A=6, k=12. The full original spine gets (14,6,18,3), with actual spine weights (8,12,15).

| Actual center | F at center | F on original terminals by index | Actual center-attachment weight | Actual terminal weights |
|---|---:|---|---:|---|
| `b:0:0` | 5 | (16,15) | 9 | (11,10) |
| `b:1:0` | 7 | (11) | 1 | (4) |
| `b:1:1` | 12 | (9,10) | 6 | (3,2) |
| `b:1:2` | 13 | (8) | 7 | (5) |
| `b:2:0` | 4 | (17) | 14 | (13) |
| `b:3:0` | 19 | (0,1,2) | 16 | (19,18,17) |

The three label bands are [0,5], [6,13], [14,19]. Actual cluster differences are exactly [1,7]. The actual shell differences, including its spine weights, are exactly [8,19]. This verifies the named original with unequal flanks, unequal central quotas and a single label for `s:1`.

## 5. Exact relation to retained work

The arithmetic agrees with Van Bussel's canonical amalgamation (thesis Theorem 1.14, printed page 18). To compare the root conventions, reverse each alpha class of g by l↦A−l on [0,A] and h↦A+1+k−h on [A+1,k]. Every crossing weight d becomes k+1−d, so the reversed shell is alpha graceful and places its root at zero. The within-class reversal in Theorem 1.14 recovers g before the upper shift, and the other operand is ordinary graceful at its root zero. The source construction and the direct formula in Section 3 therefore agree after this normalization. [Official thesis, Theorem 1.14](https://www.nlc-bnc.ca/obj/s4/f2/dsk1/tape3/PQDD_0011/MQ53395.pdf#page=29)

[D206](ORDINARY_SPINE_BOUNDARY_ROOT_JOINT_BLOCK.md#1-shared-boundary-and-exact-resources) has the same numerical label and difference partition for its shared boundary root. Its named lobster statement uses concatenation of witness spines at endpoints. Here the shell root `s:1` is interior to the actual four-vertex witness and has two shell spine neighbors. Section 3 proves the union and lobster membership without that premise. [D208](ORDINARY_SPINE_REVERSE_BLOCK_COMPOSITION.md) provides reversed pendant-entry blocks on original connectors and uses the concatenation interface. The present root placement instead comes from a separately supplied alpha shell on the entire exterior.

[D209](ORDINARY_SPINE_TWO_SIDED_ORDINARY_SUPPLIER.md), [D210](ORDINARY_SPINE_SIMULTANEOUS_ORDINARY_SUPPLIER.md) and [D211](ORDINARY_SPINE_COORDINATED_FOUR_HOST_SUPPLIER.md) establish their respective two-central-center continuation or allocation domains. D214 gives the specified unit exterior quota at section 2 and arbitrary central multiplicity ℓ≥3 and quotas. It does not extend those results to a larger section-2 quota or subsume their coverage. [D212](SIMULTANEOUS_SAFE_GAP_QUOTA_GROWTH.md) provides simultaneous matched-gap growth when a graceful original already has the requisite compatible cuts and hosts. [D213](ALL_CENTER_SAFE_GAP_STRUCTURAL_LIMIT.md) bounds the all-center version of that architecture. Here the arbitrary central quota vector is supplied on its own cluster and stretched into the shell once. There is no all-center matched-gap premise or renewable insertion invariant.

The retained [N107 rooted factors](../references/upstream/mdl/N107_retained_record.md) use root zero with sum and even-multiplicity constraints to supply particular common signed-label and difference resources for pairing. [N121 rooted input and list composition](../references/upstream/mdl/N121_retained_record.md) supplies root-zero odd-degree factors with odd quotas and a compatible list under its own degree pattern. The D214 rooted input needs only center-zero ordinary gracefulness, which allows arbitrary positive quotas by the verified theorem. It provides no stronger signature required by those MDL constructions. The shell attaches at one actual root, in contrast to [R241](../references/upstream/mdl/N241_relational_ports.md)'s disjoint alpha operands and literal joining edge. This is coverage for the specified LCL original, with historical provenance documented and no novelty claim.

In particular D214 supplies ordinary graceful labelings of the D212 B3 and B4 originals, since their central multiplicities are three and four. The registered simultaneous matched-gap certificate questions for B2, B3 and B4 remain undecided. For the D214 slice with ℓ≥11, D213 and D214 together show that the family is ordinary graceful while no labeling of an original in that slice can certify every actual center simultaneously under D212.

The b>1 exterior-shell domain and arbitrary multiple interior clusters remain separate obligations. No degree-two rooted classification, diagnostic, software change or successor was undertaken.
