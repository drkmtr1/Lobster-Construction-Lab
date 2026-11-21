# B2-BALANCED-SUPPLY — a direct zero-padding construction

**Disposition:** reviewed project construction, implemented in `two_section_balanced(q,K)`. The mathematical and implementation roles separately recalculated the label and actual-edge partitions. The proof below establishes the stated parameterized family; finite tests verify its implementation. No historical novelty, Lean verification, unequal-branch coverage or universal lobster claim is made.

## 1. Exact theorem

Let `t,K` be arbitrary positive integers. Take the original profile

```text
[[t],[t]] + [[] for _ in range(K+1)].
```

Its spine is `s:0,...,s:K+2`. A branch `b:0:0` at `s:0` has t terminal leaves, and a branch `b:1:0` at `s:1` has t terminal leaves. There are no additional direct leaves. Set

\[
m=2t+K+4.
\]

There is an explicitly and independently constructed prefix through the actual vertex `s:2` which leaves

\[
R=\{t+2,\ldots,K+t+1\},\qquad D=\{1,\ldots,K\},
\qquad f(s:2)=K+t+2.
\]

The remaining original target is exactly the K-edge path from `s:2` to `s:K+2`, and it has an explicit graceful completion using those resources. Consequently every tree in this stated family has the prescribed returned interface and a complete graceful labeling.

## 2. Prefix formula

Assign the following labels, with `j=0,...,t-1`:

| Actual vertex | Label |
|---|---:|
| `s:0` | `m` |
| `b:0:0` | `0` |
| `l:0:0:j` | `K+t+4+j` |
| `s:1` | `t+1` |
| `b:1:0` | `K+t+3` |
| `l:1:0:j` | `j+1` |
| `s:2` | `K+t+2` |

Every value is computed from t,K and the original vertex's role. No full graceful labeling, searched successful prefix or unknown compatible input is required.

## 3. Vertex inventory

The label zero at `b:0:0`, the t labels `1,...,t` on the second branch's terminal leaves, and label `t+1` at `s:1` form exactly `[0,t+1]`.

The labels at `s:2`, `b:1:0`, the first branch's terminal leaves, and `s:0` form exactly `[K+t+2,m]`. The two intervals are disjoint because K>=1. All assigned labels therefore lie in `0..m` and are distinct. Their union leaves exactly the K-element interval

\[
R=[t+2,K+t+1].
\]

There are `2t+5` assigned prefix vertices, matching the `(t+2)+(t+3)` assigned labels. The only unassigned vertices are the K original suffix vertices `s:3,...,s:K+2`.

## 4. Actual edge-difference inventory

Use the original edges; no attachment is moved and no connector is inserted.

| Original edge or group | Absolute difference(s) |
|---|---|
| `s:1 -- s:2` | `K+1` |
| `s:1 -- b:1:0` | `K+2` |
| `b:1:0 -- l:1:0:j` | Every value in `[K+3,K+t+2]`, once each |
| `s:0 -- s:1` | `K+t+3` |
| `b:0:0 -- l:0:0:j` | Every value in `[K+t+4,K+2t+3]`, once each |
| `s:0 -- b:0:0` | `m=K+2t+4` |

For the second terminal group, subtraction gives `K+t+3-(j+1)=K+t+2-j`, which runs through its stated interval in reverse. The first terminal group subtracts zero. The remaining differences follow directly from the two spine labels and branch-center labels.

These six blocks are consecutive and disjoint. Their union is exactly `[K+1,m]`, with `2t+4` values for `2t+4` prefix edges. Thus the unused difference set is exactly `D=[1,K]`.

## 5. Physical interface and completion

The sole edge from the assigned prefix to an unassigned vertex is the original edge `s:2--s:3`. The active label is `K+t+2`, one above the upper endpoint of R.

Starting from this high endpoint, label successive suffix vertices by alternately taking the lowest and highest still-unused label in R. The first difference is K. After taking the low endpoint, the new active label is one below the new unused interval; taking the high endpoint next gives difference K-1 and places the active label one above the remaining interval. Induction repeats the same endpoint condition. Each step consumes one original vertex, one unused label and the largest remaining difference.

After exactly K steps all suffix vertices are labeled and the suffix differences are `K,K-1,...,1`. They are disjoint from the prefix differences. Together the two parts use every vertex label `0..m` and every actual edge difference `1..m` exactly once. This proves the theorem for every positive t,K.

The endpoint interval mechanism is the retained caterpillar consumer in [Bounded Search MATHEMATICS.md](https://github.com/drkmtr1/MDL_Bounded_Search/blob/e48b94eec4091b4fe189e325cab2eda464409943/MATHEMATICS.md#6-caterpillar-interval-baseline). The balanced prefix formula is a derivation recorded in this project, not an additional upstream lemma.

## 6. Why this is independent supply and what remains

The constructor terminates after explicitly labeling the finite input graph. Formula evaluation requires one assignment per output vertex; the implementation additionally performs consistency and independent certificate checks. It produces a usable state from the parameters and original topology, so it meets the independent-supplier requirement on this domain. This proof, rather than extrapolation from a table, carries the quantifiers over t,K.

The retained padded composition also handles unequal positive branch sizes but requires substantial direct-leaf budgets. This balanced formula removes those budgets when the two branch sizes agree. No conclusion is drawn for unequal sizes, additional positive branches in a section, arbitrary further branched sections, or all lobsters.

At K=0 the same prefix arithmetic can be viewed as an alpha-labeled fixed seed with its actual exit at the least high label; adding K to the high side explains the supplied gap. The implemented theorem and API retain K>=1. This observation motivates the separate unequal-seed task in `NEXT_TASK.md`; existence of the required unequal seed is not assumed.

## 7. Source overlap and validation status

The ordinary gracefulness of special lobster/spider families may already be covered by retained or published constructions. For t<=2 the family is within the maximum-degree-three domain of the newly inspected author-posted Lean archive. No exhaustive historical comparison has been conducted for this particular labeling/interface. The contribution asserted here is an explicit, reviewed project supplier with its exact usable return state.

`tests/test_constructions.py` checks complete witnesses and independently rebuilt partial inventories for varied positive t,K, including boundaries and larger values. `tests/test_ingest.py` checks safe dispatch. The release's balanced example uses t=2,K=3. See `evidence/validation/VALIDATION_REPORT.md` for the executed environment and scope.
