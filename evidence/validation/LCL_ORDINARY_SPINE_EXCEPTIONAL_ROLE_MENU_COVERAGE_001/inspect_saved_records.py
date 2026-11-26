import collections
import hashlib
import json
from pathlib import Path
import time
import zipfile

root = Path("evidence")
run = root / "runs/d164-exceptional-four-first-001"
inputs = root / "validation/LCL_ORDINARY_SPINE_EXCEPTIONAL_FOUR_FIRST_CENTER_MATCHED_001_PREP/input"
out = Path(__file__).parent

def sha(data):
    return hashlib.sha256(data).hexdigest()

def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()

def save(name, value):
    (out / name).write_bytes((json.dumps(value, sort_keys=True, indent=2, ensure_ascii=False) + "\n").encode())

def read(file):
    return json.loads(file.read_bytes())

def edge(pair):
    return tuple(sorted(pair))

def edges(graph):
    return set(map(edge, graph["edges"]))

def digest(graph):
    record = {key: graph[key] for key in ("profile", "spine", "roles")}
    record.update(vertices=sorted(graph["vertices"]), edges=sorted(edges(graph)))
    return sha(canonical(record))

def interval(a, b):
    return list(range(a, b + 1))

def weights(labels, es):
    return {e: abs(labels[e[0]] - labels[e[1]]) for e in es}

def crossing(labels, es, cut):
    return {e for e in es if (labels[e[0]] < cut) != (labels[e[1]] < cut)}

def binding(path):
    data = path.read_bytes()
    return {"path": path.as_posix(), "bytes": len(data), "sha256": sha(data)}

def inspect():
    cpu, wall = time.process_time(), time.perf_counter()
    recon_path, zip_path = run / "RECONCILIATION.json", run / "OFFICIAL_RAW.zip"
    assert binding(recon_path)["sha256"] == "90fbb1ad38a9723ac2470894090e1ce7f6501f15a60e14500c3aff2b6b46f7b8"
    assert binding(zip_path)["sha256"] == "6ecb659aaefc4a574f39d1da8c3bb88b53517ea9381cc25fa332144f822a7c19"
    data = read(recon_path)
    summary = data["summary"]
    assert (summary["status"], summary["finite_hypothesis"], summary["paired_audits"],
            summary["completed_arms"], summary["separating"]) == ("INCOMPLETE", "UNDECIDED", 428, 856, 0)
    index = {i["id"]: i for i in read(inputs / "corpus_index.json")["targets"]}
    shards = {}

    def original(t):
        i = index[t]
        if i["shard"] not in shards:
            shards[i["shard"]] = {x["id"]: x for x in read(inputs / i["shard"])}
        o = shards[i["shard"]][t]
        assert sha(canonical(o) + b"\n") == i["record_sha256"] and digest(o["graph"]) == i["digest"] == o["digest"]
        assert (o["parameters"], o["K"], o["suffix"]) == (i["parameters"], i["K"], i["suffix"])
        return i, o

    prefix = read(inputs / "prefix.json")
    G, pg, v = prefix["oriented_labels"], prefix["graph"], prefix["frontier"]
    n, c, d = prefix["n"], prefix["c"], prefix["d"]
    assert (n, c, d, v, prefix["actual_cut"], prefix["polarity"]) == (74,36,38,"s:27",39,"maximum")
    assert digest(pg) == prefix["digest"]
    assert G[v] == 0 and pg["spine"][-1] == v and set(G) == set(pg["vertices"])
    assert sorted(G.values()) == interval(0,n) and prefix["actual_labels"] == {z:n-G[z] for z in G}
    pe = edges(pg)
    pw, px = weights(G,pe), crossing(G,pe,c)
    assert sorted(pw[e] for e in px) == prefix["crossing"] == interval(d-1,n)
    assert sorted(pw[e] for e in pe-px) == prefix["noncrossing"] == interval(1,d-2)

    rows = {r["target"]: r for r in data["rows"]}
    assert len(rows) == 428
    selected = [r for r in data["rows"] if r["arms"]["E+"]["claim"] == "YES"]
    inventories = collections.Counter(tuple(sorted(r["parameters"][:4])) for r in selected)
    assert inventories == {(1,1,2,4):40,(1,1,4,4):12,(1,2,3,4):48,(1,3,4,4):8}
    assert len({r["digest"] for r in selected}) == 108
    assert [r["target"] for r in selected] == sorted(r["target"] for r in selected)
    bases = {
        (1,1,4,4): ("target-0129","target-0132","target-0137","target-0134","target-0138","target-0135"),
        (1,2,3,4): ("target-0237","target-0240","target-0245","target-0242","target-0246","target-0243"),
    }
    base_at = {t:(inv,p,q) for inv,ts in bases.items()
               for p,(t,q) in enumerate(zip(ts,(6,5,4,3,4,3)),1)}
    records, base_hits = [], set()
    mem = {x["name"]: x for x in data["raw_members"]}
    with zipfile.ZipFile(zip_path) as arc:
        def member(binding_record):
            raw = arc.read(binding_record["file"])
            assert (len(raw), sha(raw)) == (binding_record["bytes"], binding_record["sha256"])
            return json.loads(raw)

        def freeze(r):
            t = r["target"]
            i, _ = original(t)
            b = r["arms"]["E+"]
            assert i["digest"] == r["digest"] and i["parameters"] == r["parameters"]
            return {"target":t, "digest":i["digest"], "original_record_sha256":i["record_sha256"],
                    "shard":i["shard"], "ordered_parameters":i["parameters"], "pair":r["pair"],
                    "e_plus":{j:b[j] for j in ("file","bytes","sha256")}}

        assert len(mem) == len(arc.namelist()) == 1288 and set(mem) == set(arc.namelist())
        for name, record in mem.items():
            raw = arc.read(name)
            assert (len(raw), sha(raw)) == (record["bytes"], record["sha256"]), name
        population = []
        for r in selected:
            ref = freeze(r)
            assert member(ref["pair"]) == dict(target=ref["target"], graph_digest=ref["digest"],
                                              E="YES", arms={"T":"YES","E+":"YES"}, separating=False)
            raw = member(ref["e_plus"])
            assert (raw["target"],raw["digest"],raw["result"]["claim"]) == (ref["target"],ref["digest"],"YES")
            population.append(ref)
        save("POPULATION.json", {"archive":binding(zip_path), "prefix":binding(inputs/"prefix.json"),
                                 "reconciliation":binding(recon_path), "population":population,
                                 "inventory_counts":[dict(quotas=k,count=v) for k,v in sorted(inventories.items())]})

        for ref in population:
            target = ref["target"]
            i, o = original(target)
            g, K = o["graph"], o["K"]
            es, roles = edges(g), g["roles"]
            assert len(es) == len(g["edges"])
            s, k, m, C = 2*K-10, K-6, n+2*K, c+K
            J = s+3
            F, R = o["T1"], o["T2"]
            assert n >= 2*K and s >= K and 2*K == F+R+9 and F%2 == 0 and R%2 == 1
            assert g["profile"] == pg["profile"] + o["suffix"] and g["spine"][:-2] == pg["spine"]
            assert {z:roles[z] for z in G} == pg["roles"]
            u,w = g["spine"][-2:]
            us,ws = roles[u]["section"],roles[w]["section"]
            first,second,parents = {},{},{}
            fresh_edges = {edge((v,u)), edge((u,w))}
            direct = None
            for section, sp, quotas, full in ((us,u,o["suffix"][0],first),(ws,w,o["suffix"][1],second)):
                for slot, quota in enumerate(quotas):
                    host = f"b:{section}:{slot}"
                    assert roles[host] == dict(branch=slot,kind="branch",section=section)
                    fresh_edges.add(edge((sp,host)))
                    if quota:
                        full[host] = quota
                    else:
                        assert section == ws and direct is None
                        direct = host
                        parents[direct] = w
                    for j in range(quota):
                        leaf = f"l:{section}:{slot}:{j}"
                        assert roles[leaf] == dict(branch=slot,kind="leaf",leaf=j,section=section)
                        fresh_edges.add(edge((host,leaf)))
                        parents[leaf] = host
            assert direct and es == pe | fresh_edges and not pe & fresh_edges
            assert set(g["vertices"]) == set(G) | {u,w} | set(first) | set(second) | set(parents)
            raw = member(ref["e_plus"])
            a, sol = raw["audit"], raw["result"]["solution"]
            assert raw["arm"] == "E+" and raw["K"] == K and raw["parameters"] == i["parameters"]
            assert a["status"] == "PASS_INDEPENDENT_RECONSTRUCTION" and a["original"] == g and a["graph_digest"] == i["digest"]
            red = a["reduced"]
            rr = {j:z for z,j in red.items()}
            assert sorted(red.values()) == interval(0,10) and (rr[6],rr[7],rr[0]) == (v,u,w), target
            assert {rr[j] for j in (2,3,4,5)} == set(first) and {rr[8],rr[10]} == set(second)
            assert direct not in red and parents[rr[9]] == rr[3] and parents[rr[1]] == rr[10]
            assert (sol["A"],sol["B"],sol["reduced"]) == (6,4,red)
            terminals = [dict(parent=rr[h],parent_reduced=h,reduced=t,terminal=rr[t]) for h,t in ((3,9),(10,1))]
            ex = {e for e in es if set(e) <= set(red)}
            assert ex == set(map(edge,a["exterior_edges"])) == {
                edge(t) for t in [(v,u),(u,w),(w,rr[8]),(w,rr[10]),(rr[3],rr[9]),(rr[10],rr[1])]
                + [(u,rr[j]) for j in (2,3,4,5)]}
            ew = weights(red, ex)
            assert crossing(red, ex, 7) == ex and sorted(ew.values()) == a["reduced_weights"] == interval(1,10)
            e1 = {rr[j] for j in (2,3,4,5,7,9)}
            assert sorted(t for e,t in ew.items() if set(e) <= e1|{v}) == interval(1,6)
            assert all(roles[z]["section"] == us for z in e1)
            assert all(roles[z]["section"] == ws for z in set(red)-e1-{v})
            p,q = second[rr[10]], second[rr[8]]
            first_roles = [first[rr[j]] for j in (2,3,4,5)]
            assert sum(first_roles) == F and p+q == R
            if target in base_at:
                inv, bp, bq = base_at[target]
                assert tuple(sorted(first_roles)) == inv and (p,q)==(bp,bq), (target,p,q)
                expected = (1,3,2,4) if inv == (1,2,3,4) else ((4,1,1,4) if p%2 else (1,1,4,4))
                assert tuple(first_roles) == expected, (target,first_roles)
                base_hits.add(target)

            actual = a["actual_labels"]
            L = {z:m-j for z,j in actual.items()}
            assert a["polarity"] == "maximum" and a["cut"] == m+1-C
            assert sorted(actual.values()) == interval(0,m) and set(actual) == set(g["vertices"])
            assert all(L[z] == j+6+(s if j>=c else 0) and ((L[z]<C)==(j<c)) for z,j in G.items())
            assert all(L[z] == j+(n+s if j>6 else 0) for z,j in red.items())
            assert a["expanded_exterior_actual"] == {z:actual[z] for z in red}
            W,X = weights(L,es), crossing(L,es,C)
            assert crossing(actual,es,a["cut"]) == X
            assert sorted(W.values()) == interval(1,m)
            assert sorted(W[e] for e in X) == a["crossing"] == interval(d+K-1,m)
            assert sorted(W[e] for e in es-X) == a["noncrossing"] == interval(1,d+K-2)
            assert a["certificate"]["valid"] and a["certificate"]["graph_digest"] == i["digest"]
            assert sorted(a["certificate"]["edge_differences"]) == interval(1,m)

            shifts = {rr[2]:3,rr[3]:2,rr[4]:1,rr[5]:0,w:5}
            reflect = {rr[8]:s+3,rr[10]:s+5}
            displacements = ({z:dict(kind="translation",offset=t) for z,t in shifts.items()} |
                             {z:dict(kind="reflection",intercept=t) for z,t in reflect.items()})
            gap = sorted(a["gap"],key=lambda z:z["source"])
            assert len(gap) == s and {z["leaf"] for z in gap} == set(L)-set(G)-set(red)
            assert [z["source"] for z in gap] == sorted(z["image"] for z in gap) == interval(0,s-1)
            assert [[z["host"],z["image"]] for z in gap] == sol["assignment"]
            quotas = first | second | {w:1}
            quotas[rr[3]] -= 1
            quotas[rr[10]] -= 1
            seen = collections.Counter(z["host"] for z in gap)
            assert set(seen) <= set(quotas) and quotas == a["gap_quotas"] == {h:seen[h] for h in quotas}, target
            paths = {"L_to_H":[],"H_to_L":[]}
            reserved = []
            x = y = 0
            for z in gap:
                leaf,h,src,img = (z[j] for j in ("leaf","host","source","image"))
                assert parents[leaf] == h and z["label_oriented"] == L[leaf] == c+6+src
                assert img == (src+shifts[h] if h in shifts else reflect[h]-src)
                assert z["weight"] == W[edge((leaf,h))] == d-1+img
                assert z["crossing"] == (edge((leaf,h)) in X) == (img>=K) == ((src<k) != (h in shifts))
                assert (L[leaf]<C) == (src<k)
                x += src<k and h in reflect
                y += src>=k and h in shifts
                folded = z | dict(folded_source=["L",src] if src<k else ["H",J-src],
                                   folded_image=["L",img] if img<K else ["H",J-img])
                group = reserved if h in shifts else paths["L_to_H" if src<k else "H_to_L"]
                group.append(folded)
            assert x == (R-7)//2 and y == (F-4)//2 and x+y == s-K
            assert a["crossing_counts"] == dict(lower_source_upper_host=x,upper_source_lower_host=y)
            feature = rows[target]["arms"]["E+"]["feature"]
            for name,value in dict(A=6,B=4,e1=1,e2=1,h=0,s=s,terminals=terminals,neutral=rr[5],
                                   displacements=displacements,upper_index_two=rr[8],upper_index_two_gap_quota=q).items():
                assert a["exterior_structure"][name] == feature[name] == value, (target,name)
            assert feature["gap_quotas"] == quotas and (feature["x"],feature["y"]) == (x,y)
            direct_rec, = [z for z in gap if z["leaf"]==direct]
            assert feature["direct_gap"] == {j:direct_rec[j] for j in ("source","image","crossing")}
            used = set(G) | {z for z in L if z not in G and roles[z]["section"] == us}
            ue = {e for e in es if set(e) <= used}
            assert {e for e in es if len(set(e)&used)==1} == {edge((u,w))}
            for name,vs,eds in (("used",used,ue),("remaining",set(L)-used,es-ue)):
                for key,items in dict(labels=[actual[z] for z in vs],weights=[W[e] for e in eds],
                                      crossing=[W[e] for e in eds & X],noncrossing=[W[e] for e in eds-X]).items():
                    assert sorted(items) == a["resources"][name+"_"+key], (target,name,key)
            assert a["connector"] == dict(ends=[u,w],labels=[actual[u],actual[w]],weight=n+s+7,crossing=True)
            assert feature["connector_weight"] == n+s+7
            records.append(ref | dict(physical_roles=dict(zip(("v","u","w","b","a","c1","Z","Q","P"),
                           (v,u,w,rr[2],rr[3],rr[4],rr[5],rr[8],rr[10]))),
                           first_role_full_quotas=first_roles,second_role_full_quotas=dict(P=p,Q=q),
                           fixed_base=target in base_at, reduced=red, reduced_edges=sorted(ex),terminals=terminals,
                           direct_leaf=direct, K=K,k=k,s=s,J=J,m=m,actual_cut=a["cut"],oriented_cut=C,
                           gap_quotas=quotas,lower_host_reservations=reserved,paths=paths,
                           crossing_counts=a["crossing_counts"],actual_resources=a["resources"],connector=a["connector"],
                           first_gap_sources=sorted(z["source"] for z in gap if z["leaf"] in used),
                           first_gap_images=sorted(z["image"] for z in gap if z["leaf"] in used)))
        assert base_hits == set(base_at) and len(records) == 108
        negative = freeze(rows["target-0057"])
        _, no = original(negative["target"])
        na = member(negative["e_plus"])
        assert no["suffix"] == [[1,1,2,4],[1,6,0]] and na["digest"] == negative["digest"]
        assert na["result"]["claim"] == "NO" and na["audit"]["status"] == "PASS_INDEPENDENT_EXHAUSTION"
        assert na["result"]["counts"]["qualified_exteriors"] == na["audit"]["counts"]["qualified_exteriors"] == 66
        assert na["result"]["counts"]["qualified_strata"] == na["audit"]["counts"]["qualified_strata"]
        assert member(negative["pair"])["arms"] == {"T":"YES","E+":"NO"}
        pending,_ = original("target-0429")
        assert "target-0429" not in rows and not any(z.startswith("target-0429") for z in mem)
        assert pending["digest"] == "ac1aa0aab83479ced6949d84651eb3267a0ac83bca4bc5f263f4dbfca6385636"
        save("COVERAGE.json", dict(verified_records=records,
             adverse_control=negative | dict(saved_claim="NO",qualified_exteriors=66,saved_basis=na["audit"]["basis"]),
             historical_incomplete_control=dict(original_digest=pending["digest"],
                     original_record_sha256=pending["record_sha256"],historical_arms_completed=0,target=pending["id"])))
    save("ARCHIVE_CHECK.json", dict(
         input_bindings=[binding(p) for p in (zip_path,recon_path,inputs/"corpus_index.json",inputs/"prefix.json",
                                                *(inputs/j for j in sorted(shards)))],
         verified_archive_members=len(mem),covered_records=len(records),fixed_bases=len(base_hits),
         prefix_digest=prefix["digest"],prefix_frontier=v,
         process_cpu_seconds=time.process_time()-cpu, internal_wall_seconds=time.perf_counter()-wall,
         scope="Saved-record identity and endpoint reconciliation. The historical verifier and scientific engines were not invoked."))
    print(f"Reconciled {len(records)} positives including {len(base_hits)} bases and {len(mem)} archive member bindings.")

if __name__ == "__main__":
    inspect()
