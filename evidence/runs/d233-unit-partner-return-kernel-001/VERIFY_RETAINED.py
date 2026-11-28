"""Evidence-only verification of the D233 retained records, using stdlib."""
from collections import Counter, defaultdict
from hashlib import sha256
from itertools import combinations, product
import json
import re
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


def verify_certificate(placement, rows, certificate):
    low, high = placement
    n = (sum(low) + sum(high)) // 2
    size, m = 11+2*n, 33+2*n
    allowed_in = ({("L", x) for x in range(n) if x != 2} | {("L", n+2)}
                  | {("U", x) for x in range(-2, n-2)})
    allowed_w = ({("L", x) for x in range(n-4) if x != 1} | {("L", n-3)}
                 | {("U", x) for x in range(-2, n+2)})
    hosts = Counter({(tag, k): q for tag, quotas in (("L", low), ("H", high))
                     for k, q in enumerate(quotas, 1)})
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
    assert all(type(tag) is str and type(value) is int
               for row in rows for tag, value in row)
    assert sorted(i for _,i,_ in full) == list(range(size))
    assert sorted(w for _,_,w in full) == list(range(size))
    labels_at = defaultdict(list)
    for (tag,k),i,w in full:
        center = k if tag == "L" else m-k
        assert abs(center-(13+i)) == 10+w
        labels_at[f"{tag}{k}"].append(13+i)
    profile = [[low[0]], [high[0], 1], list(low[1:])+list(high[1:])+[1]*9, [1]]
    assert certificate["profile"] == profile and certificate["edges"] == m
    named = {f"s:{i}": label for i,label in enumerate((m-9,0,m,11))}
    for s,section in enumerate(profile):
        for arm,(role,q) in enumerate(zip(ROLES[s],section,strict=True)):
            k = int(role[1:])
            named[f"b:{s}:{arm}"] = k if role[0]=="L" else m-k
            labels = sorted(labels_at.pop(role))
            assert len(labels) == q
            named.update((f"l:{s}:{arm}:{j}",label) for j,label in enumerate(labels))
    assert not labels_at and certificate["labels"] == named
    assert all(type(label) is int for label in certificate["labels"].values())
    reversed_names = {}
    for name,label in named.items():
        t,s,*rest = name.split(":")
        reversed_names[":".join((t,str(3-int(s)),*rest))] = label
    calculated = spectra(profile,named) + spectra(profile[::-1],reversed_names)
    assert calculated == tuple(certificate[name] for name in ("original_sha256","fold_sha256",
                                                               "reverse_original_sha256","reverse_fold_sha256"))


def registry():
    # Enumerate occupied offsets first, then values at those offsets, then bits.
    groups = defaultdict(list)
    for t, values in ((2,(7,9)),(3,(3,5,7,9,11)),(4,(3,5,7,9,11,13,15))):
        for positions in combinations(range(4), t):
            for order in product(values, repeat=t):
                key = (1,) * (4-t) + tuple(sorted(order))
                for flags in range(1 << t):
                    sides = [[1]*4, [1]*4]
                    for j, (k,q) in enumerate(zip(positions,order,strict=True)):
                        sides[(flags >> j) & 1][k] = q
                    groups[key].append(tuple(map(tuple,sides)))
    def preference(pair):
        low, high = pair
        return (-high[2], sum(x>1 for x in high),
                sum(abs(k-3) for k,q in enumerate(low,1) if q>1), pair)
    assert len(groups) == 248 and sum(map(len, groups.values())) == 42512
    return tuple((key,tuple(sorted(groups[key],key=preference))) for key in sorted(groups))


def classify(primary, audit):
    if primary is None:
        assert audit is None
        return "UNVISITED"
    p = primary["status"]
    if p == "INCOMPLETE":
        assert audit is None and primary["reason"] == "PRIMARY_PLACEMENT_NODES"
        return "PRIMARY_INCOMPLETE"
    if audit is None:
        assert p in ("WITNESS_PENDING_AUDIT","EXHAUSTION_PENDING_AUDIT")
        return p
    a = audit["status"]
    expected = {"VERIFIED_POSITIVE":"WITNESS_PENDING_AUDIT", "REJECTED":"WITNESS_PENDING_AUDIT",
                "CORROBORATED_EXCLUSION":"EXHAUSTION_PENDING_AUDIT",
                "INCOMPLETE":"EXHAUSTION_PENDING_AUDIT","CONTRADICTION":"EXHAUSTION_PENDING_AUDIT"}
    assert p == expected[a]
    if a == "INCOMPLETE":
        assert audit["reason"] == "AUDIT_PLACEMENT_NODES"
        return "AUDIT_INCOMPLETE"
    if a == "CORROBORATED_EXCLUSION":
        required = primary["counters"]
        confirmed = audit["counters"]
        for metric in ("nodes", "row_attempts"):
            assert confirmed[metric]["primary"] == required[metric]["primary"]
            assert confirmed[metric]["audit"] > required[metric].get("audit", 0)
        assert confirmed["nodes"]["audit"] - required["nodes"].get("audit",0) <= 400000
    return a


def scientific_inventory():
    index = {}
    for path in RAW.iterdir():
        assert path.is_file() and path.stat().st_size <= 65536
        if path.name.endswith(".tmp"):
            assert re.fullmatch(r".+\.json\.[a-f0-9]{32}\.tmp", path.name), path
            continue
        if path.name in ("session.json","summary.json"):
            continue
        match = re.fullmatch(r"key-(\d{3})(?:-placement-(\d{3})-(primary|audit))?\.json", path.name)
        assert match, path
        k, p, kind = match.groups()
        identity = (int(k), None if p is None else int(p), kind)
        assert identity not in index
        index[identity] = READ(path)
    return index


def verify():
    assert {i for _,_,i,_ in OLD} == {w for _,_,_,w in OLD} == set(range(11))
    assert all(w == (i+3-k if t=="L" else 10-k-i) for t,k,i,w in OLD)
    by_record = scientific_inventory()
    snapshots = [data["counters"] for data in by_record.values() if "counters" in data]
    groups = registry()
    dispositions = Counter()
    subsets = {tag: {"aggregates":Counter(),"placements":Counter()} for tag in ("nonbinary_only","includes_three")}
    observations = Counter()
    report = []
    residual_rows = lifted_rows = endpoint_differences = 0
    for index, (key, placements) in enumerate(groups):
        counts = Counter()
        positive = []
        events = []
        visited = []
        for j, placement in enumerate(placements):
            p = by_record.pop((index,j,"primary"),None)
            a = by_record.pop((index,j,"audit"),None)
            for data in (p,a):
                if data:
                    assert data["key_index"] == index and data["placement_index"] == j
                    assert data["placement"] == list(map(list,placement))
            status = classify(p,a)
            counts[status] += 1
            if status != "UNVISITED":
                visited.append([j,status])
            if status == "VERIFIED_POSITIVE":
                verify_certificate(placement,p["rows"],a["certificate"])
                residual_rows += len(p["rows"])
                lifted_rows += len(p["rows"])+11
                endpoint_differences += 4*a["certificate"]["edges"]
                positive.append(j)
            events.append(status)
        assert len(positive) <= 1
        assert not positive or all(s == "UNVISITED" for s in events[positive[0]+1:])
        disposition = ("COVERED" if positive else
                       "ARCHITECTURE_EXCLUDED" if counts["CORROBORATED_EXCLUSION"] == len(placements)
                       else "UNRESOLVED")
        dispositions[disposition] += 1
        sub = subsets["includes_three" if 3 in key else "nonbinary_only"]
        sub["aggregates"][disposition] += 1
        sub["placements"].update(counts)
        obs = by_record.pop((index,None,None),None)
        if obs:
            assert obs["aggregate"] == list(key) and obs["placement_count"] == len(placements)
            assert obs["disposition"] == disposition
            assert obs["positive_placement_index"] == (positive[0] if positive else None)
            last = positive[0]+1 if positive else len(placements)
            translated = [
                (s if s in ("VERIFIED_POSITIVE","CORROBORATED_EXCLUSION") else "UNRESOLVED")
                for s in events[:last]
            ]
            assert obs["statuses"] == translated and all(s != "UNVISITED" for s in events[:last])
            observations[disposition] += 1
        report.append({"index":index, "aggregate":key, "status":disposition,
                       "placements":len(placements), "counts":counts,
                       "visited":visited, "aggregate_record":obs is not None})
    assert not by_record
    assert (sum(subsets["nonbinary_only"]["aggregates"].values()),
            sum(subsets["nonbinary_only"]["placements"].values())) == (149,22880)
    assert (sum(subsets["includes_three"]["aggregates"].values()),
            sum(subsets["includes_three"]["placements"].values())) == (99,19632)
    size = sum(f.stat().st_size for f in RAW.iterdir())
    temporary = [f.name for f in RAW.iterdir() if f.name.endswith(".tmp")]
    records = sum(1 for f in RAW.iterdir() if not f.name.endswith(".tmp"))
    assert records <= 10000 and size <= 64*1024**2
    summary_path = RAW / "summary.json"
    summary = READ(summary_path) if summary_path.exists() else None
    if summary:
        counts = summary["counters_before_summary"]
        assert summary["completed_by_disposition"] == observations
        assert summary["unfinished_aggregates"] == 248-sum(observations.values())
        assert summary["complete_positive_coverage"] == (observations["COVERED"] == 248)
        assert not temporary
        assert summary["evidence_before_summary"] == {"records":records-1,
            "bytes":size-summary_path.stat().st_size}
        assert sum(counts["nodes"].values()) <= 100000000
        assert sum(counts["row_attempts"].values()) <= 54415360

    # If the immutable prefix ends within the first round, charge the exact
    # row-generation inventory of the next placement against the terminal counter.
    def row_attempt_limit(pair):
        low, high = pair
        return (sum(low)+sum(high)) * (8 + int(low[2]>1) + int(low[3]>1))

    interrupted = None
    visited = [(row["index"], j) for row in report for j, _ in row["visited"]]
    latest = max(snapshots, key=lambda row: row["wall_seconds"]) if snapshots else None
    if summary and summary["stop_reason"] == "CPU" and latest and visited:
        length = len(visited)
        if visited == [(i,0) for i in range(length)] and length < len(groups):
            prior_attempts = sum(row_attempt_limit(groups[i][1][0]) for i in range(length))
            remaining_attempts = counts["row_attempts"].get("primary",0) - prior_attempts
            if remaining_attempts > 0:
                pair = groups[length][1][0]
                assert remaining_attempts <= row_attempt_limit(pair)
                raw_known = latest["row_attempts"]["primary"]
                prefixes = [sum(row_attempt_limit(groups[i][1][0]) for i in range(k+1))
                            for k in range(length)]
                snapshot_key = prefixes.index(raw_known)
                assert all(report[i]["visited"] == [[0,"PRIMARY_INCOMPLETE"]]
                           for i in range(snapshot_key+1,length))
                charged = (counts["nodes"]["primary"]-latest["nodes"]["primary"]
                           -200000*(length-1-snapshot_key))
                assert 0 <= charged <= 200000
                interrupted = {"key_index":length,"placement_index":0,"placement":pair,
                               "aggregate":groups[length][0],"row_attempts":remaining_attempts,
                               "primary_charges":charged,"provenance":"terminal accounting and exact record prefix"}
                report[length]["counts"]["UNVISITED"] -= 1
                report[length]["counts"]["INTERRUPTED_UNRECORDED"] += 1
                scope = subsets["includes_three" if 3 in groups[length][0] else "nonbinary_only"]
                scope["placements"]["UNVISITED"] -= 1
                scope["placements"]["INTERRUPTED_UNRECORDED"] += 1

    receipt_path = A / "admission.json"
    receipt_sha = sha256(receipt_path.read_bytes()).hexdigest()
    session = READ(RAW / "session.json")
    obs = READ(A / "foreground.json") if (A / "foreground.json").exists() else None
    outer = READ(A / "outer.json")
    assert session["admission"] == READ(receipt_path)
    assert session["admission_sha256"] == outer["receipt_sha256"] == receipt_sha
    assert READ(A / "released.json")["resume_attempt_committed"] is True
    assert outer["observer_signaled"]
    overhead = outer["observer_cpu_seconds"]+outer["outer_monitor_cpu_seconds"]
    if obs:
        assert obs["admission_sha256"] == receipt_sha and obs["resume_previous_count"] == 1
        assert obs["job_final"]["lifetime"] == 2 and obs["job_final"]["active"] == 0
        assert obs["job_limits"]["active_limit"] == 2 and obs["worker_signaled"] and obs["launcher_signaled"]
        combined = (obs["job_final"]["kernel"]+obs["job_final"]["user"])/10000000 + overhead
    else:
        assert outer["outer_status"] in ("OUTER_WALL","OUTER_SAMPLED_CPU","OUTER_ERROR")
        assert set(outer["member_exit"]) == {"suspended","worker"}
        assert all(row["signaled"] for row in outer["member_exit"].values())
        combined = overhead + sum(row["cpu_seconds"] for row in outer["member_exit"].values())
    assert combined == outer["combined_cpu_seconds"] or abs(combined - outer["combined_cpu_seconds"]) < 1e-8
    print(json.dumps({"aggregate_dispositions":dispositions,"subdomains":subsets,"summary":summary,
                      "observed_aggregate_records":observations,"scientific_records":records,"scientific_bytes":size,
                      "latest_durable_counters":max(snapshots,key=lambda r:r["wall_seconds"]) if snapshots else None,
                      "temporary_files":temporary,"receipt_sha256":receipt_sha,"interrupted_placement":interrupted,
                      "measured_combined_cpu_seconds":combined,"measured_foreground_seconds":outer["foreground_seconds"],"residual_rows":residual_rows,"lifted_rows":lifted_rows,
                      "graph_digests":4*dispositions["COVERED"],"endpoint_differences":endpoint_differences,
                      "placement_inventory":report},indent=2))

if __name__ == "__main__":
    verify()
