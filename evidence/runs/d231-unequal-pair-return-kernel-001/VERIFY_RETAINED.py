"""Evidence-only verification of the completed D231 positive kernel, using stdlib."""
from collections import Counter, defaultdict
from hashlib import sha256
from itertools import permutations, product
import json
from pathlib import Path

A = Path(__file__).resolve().parent
RAW = A / "records"
READ = lambda path: json.loads(path.read_bytes())
OLD = (("L",1,5,7),("L",2,7,8),("L",3,10,10),("L",4,2,1),("L",5,8,6),
       ("L",6,3,0),("L",8,9,4),("H",1,0,9),("H",2,6,2),("H",3,4,3),("H",4,1,5))
ROLES = (("L1",),("H1","L9"),("L2","L3","L4","H2","H3","H4","L5","L6","L7","L8",
                              "L12","H5","H6","H7","H8"),("L10",))


def graph(profile, folded):
    result = [(f"s:{i}", f"s:{i+1}") for i in range(3)]
    for section, row in enumerate(profile):
        attach = {0: 1, 3: 2}.get(section, section) if folded else section
        for arm, quota in enumerate(row):
            host = f"b:{section}:{arm}"
            result.append((f"s:{attach}", host))
            result.extend((host, f"l:{section}:{arm}:{j}") for j in range(quota))
    return result


def digest(edges, labels):
    body = json.dumps({"edges": edges, "labels": labels}, ensure_ascii=False, allow_nan=False,
                      sort_keys=True, separators=(",", ":"))
    return sha256(body.encode("utf-8")).hexdigest()


def spectra(profile, labels):
    original, fold = graph(profile, False), graph(profile, True)
    m = len(original)
    assert set(labels) == {v for e in original for v in e}
    assert all(type(x) is int for x in labels.values())
    assert sorted(labels.values()) == list(range(m+1))
    for edges in (original, fold):
        assert sorted(abs(labels[a]-labels[b]) for a,b in edges) == list(range(1,m+1))
    exterior = ("b:0:0", "b:3:0")
    old = [abs(labels[f"s:{i}"]-labels[x]) for i,x in zip((1,2),exterior)]
    new = [abs(labels[f"s:{i}"]-labels[x]) for i,x in zip((0,3),exterior)]
    assert old == new[::-1] and set(old) == {1,m-10}
    return (digest(original, labels), digest(fold, labels))


def verify_certificate(quotas, rows, certificate):
    n = sum(quotas)
    size, m = 11+2*n, 33+2*n
    allowed_in = ({("L", x) for x in range(n) if x != 2} | {("L", n+2)}
                  | {("U", x) for x in range(-2, n-2)})
    allowed_w = ({("L", x) for x in range(n-4) if x != 1} | {("L", n-3)}
                 | {("U", x) for x in range(-2, n+2)})
    hosts = Counter((tag,k) for k,q in enumerate(quotas,1) for tag in ("L","H") for _ in range(q))
    hosts["L",3] -= 1
    hosts["L",4] -= 1
    hosts.update((("L",7),("L",8)))
    assert Counter(tuple(row[0]) for row in rows) == hosts
    assert len(rows) == 2*n == len(allowed_in) == len(allowed_w)
    assert set(tuple(row[1]) for row in rows) == allowed_in
    assert set(tuple(row[2]) for row in rows) == allowed_w
    decode = lambda x: x[1] if x[0] == "L" else size-4-x[1]
    full = [(tuple(host), decode(x), decode(w)) for host,x,w in rows]
    full.extend(((t,k+4),i+n,w+n-4) for t,k,i,w in OLD if (t,k) not in (("L",3),("L",4)))
    full.extend(((("L",4),2,1), (("L",3),size-1,size-1)))
    assert sorted(i for _,i,_ in full) == list(range(size))
    assert sorted(w for _,_,w in full) == list(range(size))
    labels_at = defaultdict(list)
    for (tag,k),i,w in full:
        center = k if tag == "L" else m-k
        assert abs(center-(13+i)) == 10+w
        labels_at[f"{tag}{k}"].append(13+i)
    a,b,c,d = quotas
    profile = [[a],[a,1],[b,c,d,b,c,d]+[1]*9,[1]]
    assert certificate["profile"] == profile and certificate["edge_count"] == m
    named = {f"s:{i}": label for i,label in enumerate((m-9,0,m,11))}
    for s,section in enumerate(profile):
        for arm,(role,q) in enumerate(zip(ROLES[s],section,strict=True)):
            k = int(role[1:])
            named[f"b:{s}:{arm}"] = k if role[0]=="L" else m-k
            labels = sorted(labels_at.pop(role))
            assert len(labels) == q
            named.update((f"l:{s}:{arm}:{j}",label) for j,label in enumerate(labels))
    assert not labels_at and certificate["labels"] == named
    reversed_names = {}
    for name,label in named.items():
        t,s,*rest = name.split(":")
        reversed_names[":".join((t,str(3-int(s)),*rest))] = label
    calculated = spectra(profile,named) + spectra(profile[::-1],reversed_names)
    assert calculated == tuple(certificate[name] for name in ("original_sha256","fold_sha256",
                                                               "reverse_original_sha256","reverse_fold_sha256"))


keys = sorted({tuple(sorted((1,b,c,d))) for b,c,d in product(range(1,10,2),repeat=3)
               if 1 < max(b,c,d) <= 7 or max(b,c,d)==9 and min(b,c,d)>=3})
assert len(keys)==29
total = rows_count = endpoints = max_nodes = max_attempts = nodes = attempts = 0
paths = {"session.json","summary.json"}
report = []
for i,key in enumerate(keys):
    prefix = f"key-{i:02d}"
    decision, primary, audit = [READ(RAW / name) for name in
        (prefix+".json", prefix+"-placement-00-primary.json", prefix+"-placement-00-audit.json")]
    paths.update((prefix+".json",prefix+"-placement-00-primary.json",prefix+"-placement-00-audit.json"))
    placements = sorted(set(permutations(key)))
    assert decision == {"key":list(key),"placements":list(map(list,placements)),
                        "completed_statuses":["VERIFIED_POSITIVE"],"disposition":"COVERED","positive_placement":0}
    assert all(r["aggregate_index"] == i and r["placement_index"] == 0 and
               r["placement"] == list(key) for r in (primary,audit))
    assert primary["status"] == "WITNESS_PENDING_AUDIT" and audit["status"] == "VERIFIED_POSITIVE"
    verify_certificate(key,primary["rows"],audit["certificate"])
    counters = primary["counters"]
    assert audit["counters"]["row_attempts"] == counters["row_attempts"] and audit["counters"]["nodes"] == counters["nodes"]
    new_nodes, new_attempts = counters["nodes"]["primary"], counters["row_attempts"]["primary"]
    max_nodes = max(max_nodes,new_nodes-nodes)
    max_attempts = max(max_attempts,new_attempts-attempts)
    nodes, attempts = new_nodes, new_attempts
    total += len(placements)
    rows_count += len(primary["rows"])
    endpoints += 4*audit["certificate"]["edge_count"]
    report.append({"aggregate_key":list(key),"covered_placement":0,"unvisited":len(placements)-1})
assert total == 322 and {p.name for p in RAW.iterdir()} == paths
summary = READ(RAW / "summary.json")
assert summary["complete_positive_coverage"] is True and summary["stop_reason"] is None and summary["unfinished_aggregates"] == 0
assert summary["completed_by_disposition"] == {"COVERED":29}
assert summary["counters_before_summary"]["nodes"] == {"primary":nodes}
assert summary["counters_before_summary"]["row_attempts"] == {"primary":attempts}
receipt = A / "admission.json"
receipt_sha = sha256(receipt.read_bytes()).hexdigest()
session = READ(RAW / "session.json")
obs = READ(A / "foreground.json")
outer = READ(A / "outer.json")
assert session["admission"] == READ(receipt)
assert {r["admission_sha256"] for r in (session,obs)} == {receipt_sha} and outer["receipt_sha256"] == receipt_sha
assert READ(A / "released.json")["resume_attempt_committed"] is True and obs["resume_previous_count"] == 1
assert obs["job_final"]["lifetime"] == 2 and obs["job_final"]["active"] == 0 and obs["job_limits"]["active_limit"] == 2
assert obs["worker_signaled"] and obs["launcher_signaled"] and outer["observer_signaled"]
assert obs["launcher_exit_code"] == outer["observer_exit"] == 0
assert (obs["job_final"]["kernel"]+obs["job_final"]["user"])/10_000_000 + outer["observer_cpu_seconds"] + outer["outer_monitor_cpu_seconds"] == outer["combined_cpu_seconds"]
assert outer["combined_cpu_seconds"] <= 900 and outer["foreground_seconds"] <= 1200
records = len(paths)
num_bytes = sum((RAW / p).stat().st_size for p in paths)
assert summary["evidence_before_summary"] == {"records":records-1,"bytes":num_bytes-(RAW / "summary.json").stat().st_size}
print(json.dumps(dict(verified_positives=len(keys),unvisited=total-len(keys),approved_placements=total,
                     endpoint_differences=endpoints,residual_rows=rows_count,graph_digests=4*len(keys),
                     primary_nodes=nodes,primary_row_attempts=attempts,max_nodes_per_placement=max_nodes,
                     max_attempts_per_placement=max_attempts,records=records,bytes=num_bytes,keys=report),indent=2))
