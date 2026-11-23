"""Independent arithmetic check of the fixed catalog's archived inputs."""
from collections import Counter
from functools import cache
from hashlib import sha256
from itertools import product
import json
from pathlib import Path
import subprocess
import sys
from time import process_time

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
PARENT = "38686d24850c63f5c92baa3ecf116c53d5f83577"
SPINE = [f"s:{i}" for i in range(6)]
FIRST, SECOND = "b:0:0", "b:1:0"
RULES = (
    "first-case-b", "first-direct-23", "second-alternative", "nested-cuts",
    "zero-host-lift", "physical-singleton", "retained-q-one", "retained-r-one",
)


def require(condition, message):
    if not condition:
        raise ValueError(message)


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def digest(blob):
    return sha256(blob).hexdigest()


def ledger_id(graph_digest, labels):
    return digest(canonical({"graph_digest": graph_digest, "labels": sorted(labels.items())}))


@cache
def blob(path):
    require(not Path(path).is_absolute() and ".." not in path.split("/"), "invalid archive path")
    return subprocess.check_output(["git", "show", f"{PARENT}:{path}"], cwd=ROOT)


def bind(ref):
    content = blob(ref["path"])
    require(digest(content) == ref["sha256"], f"archive hash mismatch: {ref['path']}")
    return content


def from_ref(ref):
    return json.loads(bind(ref))


def audit_provenance(index):
    published_entries = {}
    for refs in index["provenance"].values():
        for ref in refs.values():
            bind(ref)
        if "manifest" not in refs:
            continue
        manifest = from_ref(refs["manifest"])
        entries = manifest["files"]
        if isinstance(entries, list):
            entries = {entry["path"]: entry for entry in entries}
        folder = Path(refs["manifest"]["path"]).parent
        published_entries.update({(folder / name).as_posix(): entry for name, entry in entries.items()})
        for role in ("audit", "review"):
            ref = refs[role]
            entry = entries[Path(ref["path"]).relative_to(folder).as_posix()]
            require(entry["sha256"] == ref["sha256"] and entry["bytes"] == len(bind(ref)),
                    f"manifest {role}: {ref['path']}")
        external = manifest["external_proof"]
        require(external == {**refs["proof"], "bytes": len(bind(refs["proof"]))}, "proof manifest")
        require(from_ref(refs["audit"])["status"] == "PASS", "retained audit status")
    for ref in index["other_sources"]:
        bind(ref)
    return published_entries


def named_arithmetic(original, certificate, q, r, t=None):
    """Check each retained named role and edge multiplicity before hashing."""
    graph = original["graph"]
    profile = [[q], [r], [] if t is None else [t], [2], [], []]
    role_expectations = {v: {"kind": "spine", "section": i} for i, v in enumerate(SPINE)}
    edge_expectations = Counter(tuple(sorted(edge)) for edge in zip(SPINE, SPINE[1:]))
    for section, terminals in enumerate(profile):
        if not terminals:
            continue
        center = f"b:{section}:0"
        role_expectations[center] = {"kind": "branch", "section": section, "branch": 0}
        edge_expectations[tuple(sorted([SPINE[section], center]))] = 1
        for j in range(terminals[0]):
            leaf = f"l:{section}:0:{j}"
            role_expectations[leaf] = {"kind": "leaf", "section": section, "branch": 0, "leaf": j}
            edge_expectations[tuple(sorted([center, leaf]))] = 1
    actual_edges = Counter(tuple(sorted(edge)) for edge in graph["edges"])
    require(graph["profile"] == profile and graph["spine"] == SPINE and graph["schema_version"] == 1,
            "wrong ordered original")
    require(certificate.get("witness", SPINE) == SPINE, "saved physical witness")
    require(graph["roles"] == role_expectations and Counter(graph["vertices"]) == Counter(role_expectations.keys()),
            "physical role or vertex multiplicity mismatch")
    require(actual_edges == edge_expectations, "edge multiplicity mismatch")
    payload = {"vertices": sorted(graph["vertices"]), "edges": sorted(sorted(e) for e in graph["edges"]),
               "profile": profile, "spine": SPINE, "roles": role_expectations}
    identity = digest(canonical(payload))
    label = certificate["labels"]
    m = len(graph["edges"])
    require(m + 1 == len(graph["vertices"]) and set(label) == set(role_expectations), "ledger shape")
    require(all(type(value) is int for value in label.values()) and sorted(label.values()) == list(range(m + 1)),
            "label bijection")
    weights = [abs(label[u] - label[v]) for u, v in graph["edges"]]
    require(sorted(weights) == list(range(1, m + 1)), "difference bijection")
    rows = [{"edge": edge, "difference": value} for edge, value in zip(graph["edges"], weights)]
    require(certificate["ledger"] == rows, "saved named edge ledger")
    checked = certificate["checker"]
    require(identity == original["graph_digest"] == certificate["graph_digest"] == checked["graph_digest"],
            "graph identity mismatch")
    require(checked["valid"] is True and checked["errors"] == [] and checked["n"] == m + 1
            and checked["m"] == m and checked["edge_differences"] == weights, "saved checker binding")
    return rows


def register(records, key):
    identities = {}
    for record in records:
        identity = record[key]
        earlier = identities.get(identity)
        require(earlier is None or earlier["labels"] == record["labels"], "distinct ledger conflation")
        identities[identity] = record
    return identities


def require_cut_binding(state, predicate, proof, verified_cuts):
    require(state["ledger_id"] == predicate["ledger_id"], "cut ledger ID mismatch")
    key = (state["ledger_id"], predicate["host"], predicate["threshold"], tuple(predicate["spectrum"]), proof)
    require(key in verified_cuts, "cut proof mismatch")


def must_reject(operation, expected):
    try:
        operation()
    except ValueError as error:
        require(str(error) == expected, f"unexpected rejection: {error}")
        return str(error)
    raise ValueError("adverse check accepted an invalid binding")


def append_low_batch(seed, host_section, c, count, old_count):
    labels = {name: value + count * (value >= c) for name, value in seed.items()}
    for j in range(count):
        labels[f"l:{host_section}:0:{old_count+j}"] = c+j
    return labels


def audit_atlas(index):
    rows = index["atlas"]["rows"]
    require(index["atlas"]["profile"] == "[[q],[r],[t],[2]] + [[]]*(K+1)"
            and index["atlas"]["parameter_type"] == "positive exact integers", "atlas named domain")
    for row in rows:
        require(set(row["domain"]) == {"q", "r", "t", "K"}, "atlas axes")
        require(all(bound in ([1, 1], [1, None], [2, None]) for bound in row["domain"].values()), "atlas split")
        require(all(key in RULES for key in row["route"]), "atlas rule reference")
    # Each box is constant on the two symbolic classes 1 and >=2 per axis.
    for q, r, t, K in product((1, 2), repeat=4):
        points = dict(q=q, r=r, t=t, K=K)
        matches = [row for row in rows if all(lo <= points[axis] and (hi is None or points[axis] <= hi)
                   for axis, (lo, hi) in row["domain"].items())]
        require(len(matches) == 1, f"atlas gap or overlap at {points}")
        expected = ("D051", ["retained-q-one"]) if q == 1 else (
            ("D043", ["retained-r-one"]) if r == 1 else (
                ("D062", list(RULES[3:6])) if K == 1 else (("D037", []) if t == 1 else (None, []))))
        row = matches[0]
        require((row["source"], row["route"]) == expected, f"atlas source or rule error at {points}")
        require(row["status"] == ("proved" if expected[0] else "unproved"), "atlas disposition")
    return 16


def main():
    started = process_time()
    require(sys.version_info[:2] in {(3, 12), (3, 13)}, "project Python 3.12 or 3.13 required")
    index_path = HERE / "index.json"
    index = json.loads(index_path.read_bytes())
    require(index["starting_commit"] == PARENT and index["schema_version"] == 1, "catalog source revision")
    limits = index["limits"]
    require(limits == dict(workers=1, ledger_records=6, rule_records=8, failure_records=4, atlas_rows=20,
                           cut_checks=64, process_cpu_seconds=30, bytes_per_record=1000000, total_new_bytes=5000000,
                           solver_queries=0, labeling_enumeration=0, new_graphs=0), "declared limits")
    require(all(len(records) <= limits[cap] for records, cap in (
        (index["ledgers"], "ledger_records"), (index["rules"], "rule_records"),
        (index["failures"], "failure_records"), (index["atlas"]["rows"], "atlas_rows"))), "record cap")
    published_entries = audit_provenance(index)
    registry = {}
    evidence = []
    for state, spec in zip(index["ledgers"], (
        ("case-b-22", 2, 2, "D058"), ("case-b-grown-32", 3, 2, "D059"),
        ("direct-23", 2, 3, "D060"), ("alternative-22", 2, 2, "D061"),
        ("alternative-grown-23", 2, 3, "D061"), ("nested-34", 3, 4, "D062"),
    ), strict=True):
        key, q, r, decision = spec
        require(state["key"] == key and state["decision"] == decision, "ledger roster")
        src = index["provenance"][decision]
        require(state["verification"] == src["audit"] and state["manifest"] == src["manifest"], "verification binding")
        for role in ("original", "certificate"):
            ref = state[role]
            entry = published_entries[ref["path"]]
            require(entry["sha256"] == ref["sha256"] and entry["bytes"] == len(bind(ref)), "archived ledger manifest")
        original, cert = from_ref(state["original"]), from_ref(state["certificate"])
        rows = named_arithmetic(original, cert, q, r)
        label = state["labels"]
        identity = ledger_id(original["graph_digest"], label)
        require(label == cert["labels"] and identity == state["ledger_id"] and state["spine"] == SPINE
                and state["graph_digest"] == original["graph_digest"] and state["profile"] == original["graph"]["profile"],
                "ledger/certificate binding")
        m = len(rows)
        require(state["root"] == {"vertex": "s:2", "label": m} and label["s:2"] == m and label[state["zero"]] == 0,
                "physical root or zero")
        require(state["hosts"] == {host: label[host] for host in (FIRST, SECOND, "b:3:0")}, "physical hosts")
        registry[identity] = (state, rows)
        evidence.append(dict(key=key, ledger_id=identity, graph_digest=state["graph_digest"], edge_differences=rows))
    require(len(register(index["ledgers"], "ledger_id")) == 6, "ledger IDs reused")
    b, g, d, a, s, j = index["ledgers"]
    require(b["graph_digest"] == a["graph_digest"] and d["graph_digest"] == s["graph_digest"]
            and len({x["graph_digest"] for x in index["ledgers"]}) == 4, "expected co-original pairs")
    expected_cuts = (
        [(FIRST, 11, [9, 14], "D059"), (FIRST, 12, [10, 14], "D059"), (FIRST, 13, [11, 14], "D059")],
        [(FIRST, 12, [10, 15], "D059")],
        [(FIRST, c, [c-2, 15], "D060") for c in (6, 12, 13, 14)],
        [(FIRST, 7, [6, 14], "D062"), (SECOND, 13, [11, 14], "D061")],
        [(SECOND, 14, [12, 15], "D061")],
        [(FIRST, 8, [7, 17], "D062"), (SECOND, 16, [14, 17], "D062")],
    )

    @cache
    def crossings(identity, c):
        require(crossings.cache_info().misses <= limits["cut_checks"], "cut check cap")
        state, rows = registry[identity]
        label = state["labels"]
        edges = [row for row in rows if min(label[v] for v in row["edge"]) < c <= max(label[v] for v in row["edge"])]
        return edges, sorted(row["difference"] for row in edges)

    verified_cuts = set()
    cut_receipts = []
    for (identity, (state, rows)), expected in zip(registry.items(), expected_cuts, strict=True):
        require(len(state["cuts"]) == len(expected), "supplied predicate count")
        for predicate, (host, c, band, source) in zip(state["cuts"], expected, strict=True):
            require(predicate == dict(ledger_id=identity, host=host, threshold=c, spectrum=band, source=source),
                    "unrecognized ledger/cut source")
            edges, weights = crossings(identity, c)
            require(state["hosts"][host] < c and weights == list(range(c-state["hosts"][host], len(rows)+1))
                    and [weights[0], weights[-1]] == band, "positive cut spectrum")
            verified_cuts.add((identity, host, c, tuple(band), source))
            cut_receipts.append(dict(**predicate, edges=edges))

    audits = {k: from_ref(index["provenance"][k]["audit"]) for k in ("D059", "D060")}
    controls = (
        (b, 9, 15, audits["D059"]["core_q2_cuts"][SECOND]),
        (g, 9, 16, audits["D059"]["core_q3_cuts"][SECOND]),
        (d, 10, 16, audits["D060"]["cut_tables"][SECOND]),
    )
    failure_receipts = []
    require(len(index["failures"]) == 4, "required scoped controls")
    for failure, (state, host_label, end, archived), key, source in zip(
            index["failures"][:3], controls,
            ("D059-case-b-second", "D059-grown-second", "D060-direct-second"),
            ("D059", "D059", "D060"), strict=True):
        identity = state["ledger_id"]
        require((failure["key"], failure["source"], failure["ledger_id"], failure["host"],
                 failure["host_label"], failure["cuts"]) == (key, source, identity, SECOND, host_label, [0, end])
                and state["hosts"][SECOND] == host_label, "failure scope binding")
        for c, archived_cut in zip(range(end+1), archived, strict=True):
            edges, weights = crossings(identity, c)
            start = c-host_label if host_label < c else host_label-c+1
            expected = list(range(start, end))
            require(archived_cut["c"] == c and archived_cut["host_label"] == host_label
                    and archived_cut["crossing_edges"] == edges
                    and archived_cut.get("crossing_spectrum", archived_cut.get("spectrum")) == weights
                    and archived_cut.get("required_spectrum", archived_cut.get("required")) == expected
                    and weights != expected and archived_cut["matches"] is False, "fixed-ledger negative control")
        failure_receipts.append(dict(key=key, checked_cuts=end+1, matches=0))
    plan = index["failures"][3]
    require((plan["key"], plan["source"], plan["ledger_id"]) == ("D061-right-zero-top-pair", "D061", None),
            "right-zero partial plan binding")

    rules = dict(zip(RULES, index["rules"], strict=True))
    for key, rule in rules.items():
        require(rule["key"] == key and all(sid in index["provenance"] for sid in rule["sources"]), "rule provenance")
    for key, state, index_of_cut, source in (
        (RULES[0], b, 0, "D059"), (RULES[1], d, 1, "D060"), (RULES[2], a, 1, "D061"),
        (RULES[3], a, 0, "D062"), (RULES[3], a, 1, "D061"),
    ):
        rule = rules[key]
        p = rule["premise"] if key != RULES[3] else rule["premise"]["initial"][index_of_cut]
        require(rule["input_state"] == {"ledger_id": state["ledger_id"]}
                and source in rule["sources"] and p["label"] == state["hosts"][p["host"]], "rule input binding")
        require_cut_binding(state, {"ledger_id": state["ledger_id"], "host": p["host"], "threshold": p["cut"],
                                    "spectrum": p["spectrum"]}, source, verified_cuts)
    nested = rules[RULES[3]]
    require(nested["premise"]["h"] == "q-2" and nested["premise"]["k"] == "r-2"
            and nested["updated_cut"] == dict(first=dict(cut="7+h", spectrum=["6+h", "m"]),
                                              second=dict(cut="13+h+k", spectrum=["11+h+k", "m"])),
            "nested parameter or returned cuts")
    h, k = 1, 2
    require(append_low_batch(b["labels"], 0, 11, 1, 2) == g["labels"]
            and append_low_batch(a["labels"], 1, 13, 1, 2) == s["labels"], "archived one-step formulas")
    first_second = append_low_batch(append_low_batch(a["labels"], 0, 7, h, 2), 1, 13+h, k, 2)
    second_first = append_low_batch(append_low_batch(a["labels"], 1, 13, k, 2), 0, 7, h, 2)
    direct = {v: value + h*(value >= 7) + k*(value >= 13) for v, value in a["labels"].items()}
    direct.update({"l:0:0:2": 7, "l:1:0:2": 14, "l:1:0:3": 15})
    require(direct == first_second == second_first == j["labels"], "nested archived pointwise formula")
    require(nested["difference_blocks"] == [["1","5"],["6","5+h"],["6+h","10+h"],
                                            ["11+h","10+h+k"],["11+h+k","14+h+k"]], "symbolic edge bands")
    seed_rows = registry[a["ledger_id"]][1]
    final_edges = {tuple(row["edge"]): row["difference"] for row in registry[j["ledger_id"]][1]}
    for row in seed_rows:
        w = row["difference"]
        require(final_edges[tuple(row["edge"])] == w + h*(w >= 6) + k*(w >= 11), "nested edge group at example")
    for edge, weight in (([FIRST, "l:0:0:2"], 6), ([SECOND, "l:1:0:2"], 12), ([SECOND, "l:1:0:3"], 13)):
        require(final_edges[tuple(edge)] == weight, "new terminal difference in example")

    others = {Path(ref["path"]).name: ref for ref in index["other_sources"]}
    lift_ref = others["lift-q3-r4-t1.json"]
    lift_original_ref = others["lift-q3-r4-t1-original.json"]
    for ref in (lift_ref, lift_original_ref):
        entry = published_entries[ref["path"]]
        require(entry["sha256"] == ref["sha256"] and entry["bytes"] == len(bind(ref)), "archived lift manifest")
    lift = from_ref(lift_ref)
    lift_rows = named_arithmetic(from_ref(lift_original_ref), lift, 3, 4, 1)
    translated = {v: value+1 for v, value in j["labels"].items()}
    translated.update({"b:2:0": 0, "l:2:0:0": j["root"]["label"]+2})
    require(lift["labels"] == translated, "archived lift")
    prefix = dict(translated)
    end = prefix.pop("s:5")
    pending = [row for row in lift_rows if "s:5" in row["edge"]]
    R = sorted(set(range(len(lift_rows)+1))-set(prefix.values()))
    D = sorted(set(range(1, len(lift_rows)+1))-{row["difference"] for row in lift_rows if "s:5" not in row["edge"]})
    actual = dict(R=R, D=D, port=["s:4", prefix["s:4"]], completion=["s:5", end], pending_edge=["s:4","s:5"])
    symbolic = rules["physical-singleton"]["resources"]["by_core_supply"]
    require(symbolic["nested-cuts"] == dict(R=["q+9"], D=[1], port=["s:4","q+8"],
                                           completion=["s:5","q+9"], pending_edge=["s:4","s:5"]),
            "nested symbolic inventories")
    require(actual["R"] == [12] and actual["D"] == [1] and pending == [{"edge":actual["pending_edge"],"difference":1}]
            and actual["port"] == ["s:4", 11] and end == 12
            and lift["interface"]["R"] == R and lift["interface"]["D"] == D
            and lift["interface"]["prefix"] == prefix, "archived singleton inventories")
    for name, state in zip(RULES[:3], (b, d, a), strict=True):
        f = state["labels"]
        resources = symbolic[name]
        require(resources["R"] == [f["s:5"]+1] and resources["D"] == [abs(f["s:4"]-f["s:5"])]
                and resources["port"] == ["s:4",f["s:4"]+1] and resources["completion"] == ["s:5",f["s:5"]+1]
                and resources["pending_edge"] == ["s:4","s:5"], "fixed family singleton")

    graph_only = must_reject(lambda: register([b, a], "graph_digest"), "distinct ledger conflation")
    bad_ref = dict(a["cuts"][1], ledger_id=b["ledger_id"])
    bad_id = must_reject(lambda: require_cut_binding(a, bad_ref, "D061", verified_cuts), "cut ledger ID mismatch")
    wrong_source = must_reject(lambda: require_cut_binding(a, a["cuts"][1], "D059", verified_cuts), "cut proof mismatch")
    history = {}
    for filename in ("raw_query.json", "raw_result.json"):
        ref = others[filename]
        require(from_ref(ref)["status"] == "INCOMPLETE", f"historical status: {filename}")
        history[ref["path"]] = ref["sha256"]
    cells = audit_atlas(index)
    elapsed = process_time() - started
    require(elapsed <= limits["process_cpu_seconds"], "process CPU cap")
    report = dict(status="PASS", task=index["task"], parent=PARENT,
                  counts=dict(ledgers=len(evidence), distinct_ledger_graphs=4, rules=len(rules),
                              failures=len(index["failures"]), atlas_rows=len(index["atlas"]["rows"]),
                              atlas_symbolic_cells=cells, cut_checks=crossings.cache_info().misses,
                              additional_retained_lift=1, new_graphs=0, solver_queries=0, labeling_enumeration=0),
                  ledgers=evidence, verified_cuts=cut_receipts, fixed_ledger_failures=failure_receipts,
                  proof_only_partial_plan=plan["key"], lifted_example=actual, historical_incomplete_sha256=history,
                  adverse=dict(graph_digest_only=graph_only, mismatched_ledger_id=bad_id, mismatched_cut_proof=wrong_source),
                  identities=dict(index_sha256=digest(index_path.read_bytes()),
                                  auditor_sha256=digest(Path(__file__).read_bytes()),
                                  git_pinned_source_count=blob.cache_info().misses),
                  runtime=dict(implementation=sys.implementation.name, version=sys.version,
                               platform=sys.platform, cpu_seconds=elapsed),
                  symbolic_status="Source proof bindings audited. Quantified formula fidelity and closure receive separate mathematical review.")
    output = (json.dumps(report, indent=2, sort_keys=True) + "\n").encode()
    sizes = [p.stat().st_size for p in HERE.iterdir() if p.is_file()] + [len(output)]
    require(max(sizes) <= limits["bytes_per_record"] and sum(sizes) <= limits["total_new_bytes"], "output byte cap")
    with (HERE / "audit_result.json").open("xb") as target:
        target.write(output)
    print(f"PASS: 6 ledgers, 8 rules, 4 scoped failures, 8 atlas rows, {crossings.cache_info().misses} cut checks.")


if __name__ == "__main__":
    main()
