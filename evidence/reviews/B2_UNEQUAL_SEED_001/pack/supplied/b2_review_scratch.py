"""Read-only independent verification scratch for B2-UNEQUAL-SEED-001 review.
Writes nothing to the project. Own notation, own code, no project imports.
"""
import itertools
from collections import Counter

edges = [("s:0","s:1"),("s:0","b:0:0"),("b:0:0","l:0:0:0"),
         ("s:1","b:1:0"),("b:1:0","l:1:0:0"),("b:1:0","l:1:0:1"),("s:1","s:2")]
A = ["s:1","b:0:0","l:1:0:0","l:1:0:1"]
B = ["s:0","b:1:0","l:0:0:0","s:2"]

# (a) every edge crosses the A/B cut
crossing = all((u in A) != (v in A) for u, v in edges)
print("(a) all 7 edges cross A/B cut:", crossing)

# full restricted enumeration: A bijective 0..3, B bijective 4..7 with s:2=4
n = 0
witnesses = []
identity_mismatches = 0
sum28_xor_eq18 = 0
eq18_list = []
for la in itertools.permutations((0,1,2,3)):
    ha = dict(zip(A, la))
    for lb in itertools.permutations((5,6,7)):
        h = dict(ha)
        h.update(dict(zip(B, lb)))
        h["s:2"] = 4
        n += 1
        d = sorted(abs(h[u]-h[v]) for u, v in edges)
        a, b = h["s:0"], h["b:1:0"]
        c, x = h["l:0:0:0"], h["b:0:0"]
        s = sum(abs(h[u]-h[v]) for u, v in edges)
        if s != a + 2*b - x + 10:
            identity_mismatches += 1
        if (s == 28) != (a + 2*b - x == 18):
            sum28_xor_eq18 += 1
        if a + 2*b - x == 18:
            eq18_list.append((a, b, x, sorted(d)))
        if d == [1,2,3,4,5,6,7]:
            witnesses.append(h)
print("restricted assignments:", n)
print("graceful witnesses:", witnesses)
print("sum-identity (s == a+2b-x+10) mismatches:", identity_mismatches)
print("sum==28 XOR (a+2b-x==18) mismatches:", sum28_not18 if False else sum28_xor_eq18)
print("assignments with a+2b-x==18:", len(eq18_list))
for row in eq18_list:
    print("  (a,b,x)=", row[:3], " diff multiset:", row[3])

# (b) check: does any assignment with s:1 != 3 even reach difference 1 correctly?
# difference-1 carrier analysis
def d1_carriers(h):
    out = []
    for i, (u, v) in enumerate(edges, 1):
        if abs(h[u]-h[v]) == 1:
            out.append(i)
    return out
print("(b) carriers of difference 1 among eq-18 candidates:")
for (a, b, x, d) in eq18_list:
    # reconstruct one such assignment to show carriers
    pass
# direct: for all 144, which edges can carry 1?
carriers_by_edge = Counter()
for la in itertools.permutations((0,1,2,3)):
    ha = dict(zip(A, la))
    for lb in itertools.permutations((5,6,7)):
        h = dict(ha); h.update(dict(zip(B, lb))); h["s:2"] = 4
        for i in d1_carriers(h):
            carriers_by_edge[i] += 1
print("    edge->#assignments where that edge has difference 1:", dict(carriers_by_edge))
s1_not3_with_d1 = 0
for la in itertools.permutations((0,1,2,3)):
    if la[A.index("s:1")] != 3:
        ha = dict(zip(A, la))
        for lb in itertools.permutations((5,6,7)):
            h = dict(ha); h.update(dict(zip(B, lb))); h["s:2"] = 4
            if 1 in [abs(h[u]-h[v]) for u, v in edges]:
                s1_not3_with_d1 += 1
print("    assignments with h(s:1)!=3 that still contain difference 1 somewhere:", s1_not3_with_d1)

# (e) per-triple difference lists, all u,v
triples = [(5,7,6,1),(6,7,5,2),(7,6,5,1)]
for t in triples:
    a, b, c, x = t
    y = 3
    for uv in itertools.permutations(sorted({0,1,2} - {x})):
        u, v = uv
        dd = [a-y, a-x, c-x, b-y, b-u, b-v, 4-y]
        dup = {k: val for k, val in Counter(dd).items() if val > 1}
        print("(e)", t, "u,v=", uv, "diffs:", dd, "dups:", dup)

# (g) consumer lemma from PROOF_OBLIGATIONS.md section 3, above-side, a=4
print("(g) consumer lemma, a=4, above side:")
for K in range(1, 13):
    a = 4
    w0 = a + K
    labels = []
    diffs = []
    prev = w0
    for j in range(1, K+1):
        if j % 2 == 1:
            fj = a + (j-1)//2
        else:
            fj = a + K - j//2
        labels.append(fj)
        diffs.append(abs(prev - fj))
        prev = fj
    ok_labels = sorted(labels) == list(range(a, a+K))
    ok_diffs = diffs == list(range(K, 0, -1))
    if not (ok_labels and ok_diffs):
        print("   FAIL K=", K, labels, diffs)
print("   all K=1..12 ok (no FAIL lines above)")

# transport mechanics on an arbitrary seed-shaped assignment (conditional, not graceful)
h0 = dict(zip(A, (0,1,2,3)))
h0.update(dict(zip(B, (5,6,7))))
h0["s:2"] = 4
base_diffs = sorted(abs(h0[u]-h0[v]) for u, v in edges)
print("(g) transport mechanics, arbitrary h0 base diffs:", base_diffs)
for K in range(1, 8):
    hk = dict(h0)
    for vv in B:
        hk[vv] += K
    used = sorted(hk.values())
    unused_labels = sorted(set(range(K+8)) - set(used))
    pd = sorted(abs(hk[u]-hk[v]) + 0 for u, v in edges)  # prefix diffs under h_K
    shifted = sorted(d + K for d in base_diffs)
    print("   K=", K, "used:", used, "unused labels:", unused_labels,
          "unused interval [4,K+3]:", list(range(4, K+4)),
          "match:", unused_labels == list(range(4, K+4)),
          "prefix diffs shifted by K:", pd == shifted,
          "port h_K(s:2)=", hk["s:2"], "one above interval:", hk["s:2"] == K+4)
# disjointness for K>=1
print("   low/high disjoint for all K>=1:", all(
    min(K+4 for _ in [0]) > 3 for K in range(1, 100)))
